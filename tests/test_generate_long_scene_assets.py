from __future__ import annotations

import csv
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

import soundfile as sf

from scripts.generate_long_scene_assets import (
    Scene,
    SubtitleCue,
    assemble_timed_wav,
    cue_times,
    estimate_duration,
    split_text_chunks,
    write_manifest,
    write_scene_captions,
)


class GenerateLongSceneAssetsTest(unittest.TestCase):
    def test_estimate_duration_ignores_spaces(self) -> None:
        self.assertAlmostEqual(estimate_duration("一 二 三 四", 2.0), 2.0)

    def test_blank_cue_times_are_evenly_distributed(self) -> None:
        cue = SubtitleCue(
            conversation_id="trip",
            scene_id="001",
            cue_id="002",
            cue_start="",
            cue_end="",
            subtitle_zh="第二句。",
            subtitle_en="Second line.",
            notes="",
            status="reviewed",
        )

        self.assertEqual(cue_times(cue, 1, 4, 40.0), (10.0, 20.0))

    def test_split_text_chunks_keeps_sentence_boundaries(self) -> None:
        chunks = split_text_chunks("第一句很短。第二句也很短。第三句还是很短。", 12)

        self.assertEqual(chunks, ["第一句很短。", "第二句也很短。", "第三句还是很短。"])

    def test_write_scene_captions_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            srt_path = root / "scene.bilingual.srt"
            vtt_path = root / "scene.bilingual.vtt"
            cue = SubtitleCue(
                conversation_id="trip",
                scene_id="001",
                cue_id="001",
                cue_start="",
                cue_end="",
                subtitle_zh="第一句。",
                subtitle_en="First line.",
                notes="",
                status="reviewed",
            )
            write_scene_captions(
                srt_path=srt_path,
                vtt_path=vtt_path,
                cues=[cue],
                duration_seconds=3.0,
            )

            self.assertIn("First line.\n第一句。", srt_path.read_text(encoding="utf-8"))
            self.assertTrue(vtt_path.read_text(encoding="utf-8").startswith("WEBVTT"))

            scene = Scene(
                conversation_id="trip",
                section_id="skagway",
                scene_id="001",
                clip_name="scene",
                scene_title="Scene",
                start_time="",
                end_time="",
                speaker="owner_calm",
                style="reflective",
                language="zh",
                text="第一句。",
                notes="",
                status="reviewed",
            )
            manifest = root / "manifest.csv"
            asset = Namespace(
                scene=scene,
                duration_seconds=3.0,
                audio_path=root / "scene.wav",
                bilingual_srt_path=srt_path,
                bilingual_vtt_path=vtt_path,
                subtitle_cue_count=1,
                generation_mode="estimated_no_audio",
            )
            write_manifest(manifest, [asset])

            with manifest.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["clip_name"], "scene")
            self.assertEqual(rows[0]["duration_seconds"], "3.000")

    def test_assemble_timed_wav_keeps_silence_between_cues(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            first = root / "first.wav"
            second = root / "second.wav"
            output = root / "output.wav"
            sf.write(first, [0.25, 0.25], 2, subtype="PCM_16")
            sf.write(second, [0.5, 0.5], 2, subtype="PCM_16")
            cue_one = SubtitleCue(
                conversation_id="trip",
                scene_id="001",
                cue_id="001",
                cue_start="00:00:00",
                cue_end="00:00:01",
                subtitle_zh="一",
                subtitle_en="One",
                notes="",
                status="reviewed",
            )
            cue_two = SubtitleCue(
                conversation_id="trip",
                scene_id="001",
                cue_id="002",
                cue_start="00:00:03",
                cue_end="00:00:04",
                subtitle_zh="二",
                subtitle_en="Two",
                notes="",
                status="reviewed",
            )

            assemble_timed_wav(
                generated_cues=[
                    (cue_one, first, 0.0, 1.0),
                    (cue_two, second, 3.0, 1.0),
                ],
                output_path=output,
                sample_rate=2,
                total_duration=4.0,
            )

            data, rate = sf.read(output, dtype="float32")
            self.assertEqual(rate, 2)
            self.assertEqual(len(data), 8)
            self.assertTrue(abs(data[3]) < 0.01)


if __name__ == "__main__":
    unittest.main()
