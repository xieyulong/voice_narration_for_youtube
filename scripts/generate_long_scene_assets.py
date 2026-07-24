"""Generate long-scene narration deliverables from scene and subtitle cue CSVs."""

from __future__ import annotations

import argparse
import csv
import logging
import shutil
import subprocess
from dataclasses import dataclass, replace
from pathlib import Path

import soundfile as sf

try:
    from validate_long_scene_inputs import CsvData, read_csv, validate
except ImportError:
    from scripts.validate_long_scene_inputs import CsvData, read_csv, validate


LOGGER = logging.getLogger(__name__)
DEFAULT_FRAME_RATE = 30.0


@dataclass(frozen=True)
class Scene:
    conversation_id: str
    section_id: str
    scene_id: str
    clip_name: str
    scene_title: str
    start_time: str
    end_time: str
    speaker: str
    style: str
    language: str
    text: str
    notes: str
    status: str


@dataclass(frozen=True)
class SubtitleCue:
    conversation_id: str
    scene_id: str
    cue_id: str
    cue_start: str
    cue_end: str
    subtitle_zh: str
    subtitle_en: str
    notes: str
    status: str


@dataclass(frozen=True)
class VoiceReference:
    name: str
    audio: Path
    text: str


@dataclass(frozen=True)
class VoiceProfile:
    name: str
    engine: str
    language: str
    references: list[VoiceReference]


@dataclass(frozen=True)
class SceneAsset:
    scene: Scene
    duration_seconds: float
    audio_path: Path
    bilingual_srt_path: Path
    bilingual_vtt_path: Path
    subtitle_cue_count: int
    generation_mode: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate scene-level caption files, manifest rows, and optional "
            "Qwen3-TTS WAV files from long-scene CSV inputs."
        )
    )
    parser.add_argument("--batch-name", required=True, help="Output batch name.")
    parser.add_argument("--scenes", required=True, help="Scene CSV path.")
    parser.add_argument("--cues", required=True, help="Subtitle cue CSV path.")
    parser.add_argument(
        "--voice-profile",
        default="voice_profiles/owner_calm/profile.yaml",
        help="Private Qwen3-TTS voice profile YAML.",
    )
    parser.add_argument(
        "--profile-reference",
        help="Named reference inside the voice profile. Defaults to first reference.",
    )
    parser.add_argument(
        "--model-dir",
        default="models/qwen3-tts-12hz-0.6b-base",
        help="Local Qwen3-TTS model directory.",
    )
    parser.add_argument(
        "--audio-output-root",
        default="output/audio_scenes",
        help="Root directory for scene WAV files.",
    )
    parser.add_argument(
        "--caption-output-root",
        default="output/captions",
        help="Root directory for scene caption files.",
    )
    parser.add_argument(
        "--manifest-dir",
        default="output/manifests",
        help="Directory for manifest CSV files.",
    )
    parser.add_argument(
        "--estimated-chars-per-second",
        type=float,
        default=4.2,
        help="Dry-run duration estimate for Chinese narration text.",
    )
    parser.add_argument(
        "--sample-rate",
        type=int,
        default=48000,
        help="Final WAV sample rate for generated audio.",
    )
    parser.add_argument(
        "--device",
        default="cpu",
        help="Qwen3-TTS device_map when --synthesize is used.",
    )
    parser.add_argument(
        "--dtype",
        default="float32",
        choices=["float32", "bfloat16", "float16"],
        help="Qwen3-TTS dtype when --synthesize is used.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and print the generation plan without writing outputs.",
    )
    parser.add_argument(
        "--synthesize",
        action="store_true",
        help="Generate Qwen3-TTS WAV audio. Without this, only captions/manifest are written.",
    )
    parser.add_argument(
        "--generation-mode",
        choices=["auto", "single", "chunked"],
        default="auto",
        help=(
            "Audio generation mode when --synthesize is used. "
            "Auto uses chunked generation for long scene text."
        ),
    )
    parser.add_argument(
        "--chunk-max-chars",
        type=int,
        default=180,
        help="Maximum Chinese text characters per chunk in chunked synthesis.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow replacing existing output files.",
    )
    return parser.parse_args()


def setup_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def load_yaml(path: Path) -> dict:
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError("PyYAML is required for voice profile support") from exc

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Voice profile must contain a mapping: {path}")
    return data


def load_voice_profile(path: Path) -> VoiceProfile:
    if not path.exists():
        raise FileNotFoundError(f"Voice profile not found: {path}")

    data = load_yaml(path)
    references = data.get("references")
    if not isinstance(references, list) or not references:
        raise ValueError(f"Voice profile requires references: {path}")

    parsed_references = []
    for index, reference in enumerate(references, start=1):
        if not isinstance(reference, dict):
            raise ValueError(f"Voice profile reference {index} must be a mapping")
        name = str(reference.get("name") or f"reference_{index:03d}").strip()
        audio = str(reference.get("audio") or "").strip()
        text = str(reference.get("text") or "").strip()
        if not audio:
            raise ValueError(f"Voice profile reference {index} requires audio")
        if not text:
            raise ValueError(f"Voice profile reference {index} requires text")
        parsed_references.append(VoiceReference(name=name, audio=Path(audio), text=text))

    engine = str(data.get("engine") or "").strip()
    if engine != "qwen3_tts":
        raise ValueError(f"Unsupported voice profile engine: {engine}")

    return VoiceProfile(
        name=str(data.get("name") or path.parent.name).strip(),
        engine=engine,
        language=str(data.get("language") or "chinese").strip(),
        references=parsed_references,
    )


def select_reference(profile: VoiceProfile, reference_name: str | None) -> VoiceReference:
    if not reference_name:
        return profile.references[0]
    for reference in profile.references:
        if reference.name == reference_name:
            return reference
    available = ", ".join(reference.name for reference in profile.references)
    raise ValueError(f"Voice profile reference not found: {reference_name}. Available: {available}")


def validate_runtime_inputs(
    args: argparse.Namespace,
    voice_profile: VoiceProfile,
    selected_reference: VoiceReference,
) -> None:
    if not selected_reference.audio.exists():
        raise FileNotFoundError(f"Reference audio not found: {selected_reference.audio}")
    if args.synthesize and not Path(args.model_dir).exists():
        raise FileNotFoundError(f"Model directory not found: {args.model_dir}")
    if args.estimated_chars_per_second <= 0:
        raise ValueError("--estimated-chars-per-second must be greater than zero")
    if args.sample_rate <= 0:
        raise ValueError("--sample-rate must be greater than zero")
    if args.chunk_max_chars <= 0:
        raise ValueError("--chunk-max-chars must be greater than zero")
    if not voice_profile.references:
        raise ValueError("Voice profile has no references")


def rows_to_scenes(data: CsvData) -> list[Scene]:
    return [Scene(**row) for row in data.rows]


def rows_to_cues(data: CsvData) -> list[SubtitleCue]:
    return [SubtitleCue(**row) for row in data.rows]


def group_cues_by_scene(cues: list[SubtitleCue]) -> dict[tuple[str, str], list[SubtitleCue]]:
    grouped: dict[tuple[str, str], list[SubtitleCue]] = {}
    for cue in cues:
        grouped.setdefault((cue.conversation_id, cue.scene_id), []).append(cue)
    return grouped


def estimate_duration(text: str, chars_per_second: float) -> float:
    meaningful_chars = len("".join(text.split()))
    return max(1.0, meaningful_chars / chars_per_second)


def load_qwen_model(model_dir: Path, device: str, dtype_name: str):
    import torch
    from qwen_tts import Qwen3TTSModel

    dtype_map = {
        "float32": torch.float32,
        "bfloat16": torch.bfloat16,
        "float16": torch.float16,
    }
    return Qwen3TTSModel.from_pretrained(
        str(model_dir),
        device_map=device,
        dtype=dtype_map[dtype_name],
        attn_implementation=None,
    )


def generate_audio(
    *,
    model,
    scene: Scene,
    voice_profile: VoiceProfile,
    reference: VoiceReference,
    output_path: Path,
    sample_rate: int,
) -> float:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = output_path.with_name(f"{output_path.stem}.qwen_tmp.wav")

    wavs, source_rate = model.generate_voice_clone(
        text=scene.text,
        language=voice_profile.language,
        ref_audio=str(reference.audio),
        ref_text=reference.text,
        x_vector_only_mode=False,
        non_streaming_mode=True,
    )
    sf.write(temp_path, wavs[0], source_rate)

    if source_rate == sample_rate:
        temp_path.replace(output_path)
    else:
        resample_with_sox(temp_path, output_path, sample_rate)
        temp_path.unlink(missing_ok=True)

    return wav_duration(output_path)


def generate_chunked_audio(
    *,
    model,
    scene: Scene,
    voice_profile: VoiceProfile,
    reference: VoiceReference,
    output_path: Path,
    chunk_dir: Path,
    sample_rate: int,
    chunk_max_chars: int,
) -> float:
    chunks = split_text_chunks(scene.text, chunk_max_chars)
    if not chunks:
        raise ValueError(f"Scene {scene.scene_id}: no text chunks to synthesize")

    chunk_dir.mkdir(parents=True, exist_ok=True)
    chunk_paths = []
    for index, chunk_text in enumerate(chunks, start=1):
        chunk_scene = replace(scene, text=chunk_text)
        chunk_path = chunk_dir / f"{scene.clip_name}_chunk_{index:03d}.wav"
        LOGGER.info(
            "Generating chunk %s/%s for %s: %s",
            index,
            len(chunks),
            scene.clip_name,
            chunk_path,
        )
        generate_audio(
            model=model,
            scene=chunk_scene,
            voice_profile=voice_profile,
            reference=reference,
            output_path=chunk_path,
            sample_rate=sample_rate,
        )
        chunk_paths.append(chunk_path)

    concatenate_wavs(chunk_paths, output_path)
    return wav_duration(output_path)


def split_text_chunks(text: str, max_chars: int) -> list[str]:
    normalized = " ".join(text.split())
    if not normalized:
        return []

    sentences = []
    current = []
    for char in normalized:
        current.append(char)
        if char in "。！？!?":
            sentence = "".join(current).strip()
            if sentence:
                sentences.append(sentence)
            current = []
    remainder = "".join(current).strip()
    if remainder:
        sentences.append(remainder)

    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(sentence) > max_chars:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""
            chunks.extend(split_long_text(sentence, max_chars))
            continue
        candidate = f"{current_chunk}{sentence}" if not current_chunk else f"{current_chunk}{sentence}"
        if current_chunk and len(candidate) > max_chars:
            chunks.append(current_chunk)
            current_chunk = sentence
        else:
            current_chunk = candidate
    if current_chunk:
        chunks.append(current_chunk)
    return chunks


def split_long_text(text: str, max_chars: int) -> list[str]:
    return [text[index : index + max_chars] for index in range(0, len(text), max_chars)]


def concatenate_wavs(input_paths: list[Path], output_path: Path) -> None:
    if not input_paths:
        raise ValueError("No chunk WAV files were generated")
    if shutil.which("sox") is None:
        raise RuntimeError("SoX is required to concatenate generated WAV files")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["sox", *[str(path) for path in input_paths], str(output_path)],
        check=True,
    )


def resample_with_sox(input_path: Path, output_path: Path, sample_rate: int) -> None:
    if shutil.which("sox") is None:
        raise RuntimeError("SoX is required to resample generated WAV files")
    subprocess.run(
        ["sox", str(input_path), "-r", str(sample_rate), str(output_path)],
        check=True,
    )


def wav_duration(path: Path) -> float:
    info = sf.info(path)
    return info.frames / info.samplerate


def ensure_can_write(paths: list[Path], overwrite: bool) -> None:
    if overwrite:
        return
    existing = [path for path in paths if path.exists()]
    if existing:
        rendered = "\n".join(str(path) for path in existing)
        raise FileExistsError(f"Output files already exist. Use --overwrite:\n{rendered}")


def build_scene_assets(
    *,
    scenes: list[Scene],
    cues_by_scene: dict[tuple[str, str], list[SubtitleCue]],
    args: argparse.Namespace,
    voice_profile: VoiceProfile,
    selected_reference: VoiceReference,
) -> list[SceneAsset]:
    audio_dir = Path(args.audio_output_root) / args.batch_name
    chunk_root = Path("output/audio_chunks") / args.batch_name
    caption_dir = Path(args.caption_output_root) / args.batch_name
    manifest_path = Path(args.manifest_dir) / f"manifest_{args.batch_name}.csv"
    planned_paths = [manifest_path]
    for scene in scenes:
        planned_paths.extend(
            [
                audio_dir / f"{scene.clip_name}.wav",
                caption_dir / f"{scene.clip_name}.bilingual.srt",
                caption_dir / f"{scene.clip_name}.bilingual.vtt",
            ]
        )
    if not args.synthesize:
        planned_paths = [path for path in planned_paths if path.suffix != ".wav"]
    if not args.dry_run:
        ensure_can_write(planned_paths, args.overwrite)

    model = None
    if args.synthesize:
        LOGGER.info("Loading Qwen3-TTS model from %s", args.model_dir)
        LOGGER.info(
            "Using voice profile %s reference %s",
            voice_profile.name,
            selected_reference.name,
        )
        model = load_qwen_model(Path(args.model_dir), args.device, args.dtype)

    assets = []
    for scene in scenes:
        scene_cues = cues_by_scene[(scene.conversation_id, scene.scene_id)]
        audio_path = audio_dir / f"{scene.clip_name}.wav"
        bilingual_srt_path = caption_dir / f"{scene.clip_name}.bilingual.srt"
        bilingual_vtt_path = caption_dir / f"{scene.clip_name}.bilingual.vtt"

        if args.synthesize:
            generation_mode = resolve_generation_mode(scene.text, args)
            LOGGER.info("Generating scene audio: %s", audio_path)
            if generation_mode == "chunked_qwen3_tts":
                duration_seconds = generate_chunked_audio(
                    model=model,
                    scene=scene,
                    voice_profile=voice_profile,
                    reference=selected_reference,
                    output_path=audio_path,
                    chunk_dir=chunk_root / scene.clip_name,
                    sample_rate=args.sample_rate,
                    chunk_max_chars=args.chunk_max_chars,
                )
            else:
                duration_seconds = generate_audio(
                    model=model,
                    scene=scene,
                    voice_profile=voice_profile,
                    reference=selected_reference,
                    output_path=audio_path,
                    sample_rate=args.sample_rate,
                )
        else:
            duration_seconds = estimate_duration(scene.text, args.estimated_chars_per_second)
            generation_mode = "estimated_no_audio"

        if not args.dry_run:
            write_scene_captions(
                srt_path=bilingual_srt_path,
                vtt_path=bilingual_vtt_path,
                cues=scene_cues,
                duration_seconds=duration_seconds,
            )

        assets.append(
            SceneAsset(
                scene=scene,
                duration_seconds=duration_seconds,
                audio_path=audio_path,
                bilingual_srt_path=bilingual_srt_path,
                bilingual_vtt_path=bilingual_vtt_path,
                subtitle_cue_count=len(scene_cues),
                generation_mode=generation_mode,
            )
        )

    if not args.dry_run:
        write_manifest(manifest_path, assets)
    return assets


def resolve_generation_mode(text: str, args: argparse.Namespace) -> str:
    if args.generation_mode == "chunked":
        return "chunked_qwen3_tts"
    if args.generation_mode == "single":
        return "single_call_qwen3_tts"
    if len(text) > args.chunk_max_chars:
        return "chunked_qwen3_tts"
    return "single_call_qwen3_tts"


def write_scene_captions(
    *,
    srt_path: Path,
    vtt_path: Path,
    cues: list[SubtitleCue],
    duration_seconds: float,
) -> None:
    srt_path.parent.mkdir(parents=True, exist_ok=True)
    srt_blocks = []
    vtt_blocks = ["WEBVTT", ""]
    for index, cue in enumerate(cues, start=1):
        start_seconds, end_seconds = cue_times(cue, index - 1, len(cues), duration_seconds)
        text = f"{cue.subtitle_en}\n{cue.subtitle_zh}"
        srt_blocks.extend(
            [
                str(index),
                f"{format_srt_time(start_seconds)} --> {format_srt_time(end_seconds)}",
                text,
                "",
            ]
        )
        vtt_blocks.extend(
            [
                f"{format_vtt_time(start_seconds)} --> {format_vtt_time(end_seconds)}",
                text,
                "",
            ]
        )

    srt_path.write_text("\n".join(srt_blocks), encoding="utf-8")
    vtt_path.write_text("\n".join(vtt_blocks), encoding="utf-8")


def cue_times(
    cue: SubtitleCue,
    index: int,
    cue_count: int,
    duration_seconds: float,
) -> tuple[float, float]:
    if cue.cue_start and cue.cue_end:
        start = parse_timecode(cue.cue_start)
        end = parse_timecode(cue.cue_end)
        if start is not None and end is not None:
            return start, end

    cue_duration = duration_seconds / max(cue_count, 1)
    return index * cue_duration, (index + 1) * cue_duration


def parse_timecode(value: str) -> float | None:
    try:
        from validate_long_scene_inputs import parse_timecode as parse_validated_timecode
    except ImportError:
        from scripts.validate_long_scene_inputs import (
            parse_timecode as parse_validated_timecode,
        )

    return parse_validated_timecode(value)


def format_srt_time(seconds: float) -> str:
    hours, remainder = divmod(max(seconds, 0.0), 3600)
    minutes, secs = divmod(remainder, 60)
    millis = round((secs - int(secs)) * 1000)
    whole_seconds = int(secs)
    if millis == 1000:
        whole_seconds += 1
        millis = 0
    return f"{int(hours):02d}:{int(minutes):02d}:{whole_seconds:02d},{millis:03d}"


def format_vtt_time(seconds: float) -> str:
    return format_srt_time(seconds).replace(",", ".")


def write_manifest(path: Path, assets: list[SceneAsset]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "conversation_id",
            "section_id",
            "scene_id",
            "clip_name",
            "scene_title",
            "start_time",
            "end_time",
            "planned_duration_seconds",
            "duration_seconds",
            "generation_mode",
            "speaker",
            "style",
            "audio_path",
            "bilingual_srt_path",
            "bilingual_vtt_path",
            "subtitle_cue_count",
            "status",
            "notes",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for asset in assets:
            scene = asset.scene
            planned_duration = planned_duration_seconds(scene)
            writer.writerow(
                {
                    "conversation_id": scene.conversation_id,
                    "section_id": scene.section_id,
                    "scene_id": scene.scene_id,
                    "clip_name": scene.clip_name,
                    "scene_title": scene.scene_title,
                    "start_time": scene.start_time,
                    "end_time": scene.end_time,
                    "planned_duration_seconds": format_optional_seconds(planned_duration),
                    "duration_seconds": f"{asset.duration_seconds:.3f}",
                    "generation_mode": asset.generation_mode,
                    "speaker": scene.speaker,
                    "style": scene.style,
                    "audio_path": asset.audio_path.as_posix(),
                    "bilingual_srt_path": asset.bilingual_srt_path.as_posix(),
                    "bilingual_vtt_path": asset.bilingual_vtt_path.as_posix(),
                    "subtitle_cue_count": str(asset.subtitle_cue_count),
                    "status": scene.status,
                    "notes": scene.notes,
                }
            )


def planned_duration_seconds(scene: Scene) -> float | None:
    if not scene.start_time or not scene.end_time:
        return None
    start = parse_timecode(scene.start_time)
    end = parse_timecode(scene.end_time)
    if start is None or end is None:
        return None
    return max(end - start, 0.0)


def format_optional_seconds(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.3f}"


def print_plan(assets: list[SceneAsset], dry_run: bool) -> None:
    action = "Planned" if dry_run else "Generated"
    print(f"{action} {len(assets)} scene asset set(s)")
    for asset in assets:
        print(
            f"- {asset.scene.scene_id} {asset.scene.clip_name}: "
            f"{asset.duration_seconds:.3f}s, {asset.subtitle_cue_count} subtitle cues, "
            f"mode={asset.generation_mode}"
        )
        print(f"  audio: {asset.audio_path}")
        print(f"  srt: {asset.bilingual_srt_path}")


def main() -> int:
    setup_logging()
    args = parse_args()
    try:
        scene_data = read_csv(Path(args.scenes))
        cue_data = read_csv(Path(args.cues))
        validation_args = argparse.Namespace(require_reviewed=True, max_cue_chars=90)
        result = validate(scene_data, cue_data, validation_args)
        if not result.ok:
            for error in result.errors:
                print(f"ERROR: {error}")
            return 1
        for warning in result.warnings:
            LOGGER.warning(warning)

        voice_profile = load_voice_profile(Path(args.voice_profile))
        selected_reference = select_reference(voice_profile, args.profile_reference)
        validate_runtime_inputs(args, voice_profile, selected_reference)
        scenes = rows_to_scenes(scene_data)
        cues = rows_to_cues(cue_data)
        assets = build_scene_assets(
            scenes=scenes,
            cues_by_scene=group_cues_by_scene(cues),
            args=args,
            voice_profile=voice_profile,
            selected_reference=selected_reference,
        )
    except (FileExistsError, FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 2

    print_plan(assets, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
