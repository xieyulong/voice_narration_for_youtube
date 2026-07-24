"""Validate long-scene narration and subtitle cue CSV inputs."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SCENE_REQUIRED_FIELDS = {
    "conversation_id",
    "section_id",
    "scene_id",
    "clip_name",
    "scene_title",
    "start_time",
    "end_time",
    "speaker",
    "style",
    "language",
    "text",
    "notes",
    "status",
}
CUE_REQUIRED_FIELDS = {
    "conversation_id",
    "scene_id",
    "cue_id",
    "cue_start",
    "cue_end",
    "subtitle_zh",
    "subtitle_en",
    "notes",
    "status",
}
SCENE_STATUSES = {"draft", "reviewed", "generated", "accepted", "needs_regen"}
CUE_STATUSES = {"draft", "draft_review_needed", "reviewed", "accepted", "needs_regen"}
TIMECODE_PATTERN = re.compile(
    r"^(?:(?P<hours>\d{1,2}):)?(?P<minutes>\d{1,2}):(?P<seconds>\d{1,2})"
    r"(?:(?P<millis>[.,]\d{1,3})|:(?P<frames>\d{1,2}))?$"
)
SLUG_PATTERN = re.compile(r"^[A-Za-z0-9._-]+$")


@dataclass(frozen=True)
class CsvData:
    path: Path
    fieldnames: list[str]
    rows: list[dict[str, str]]


@dataclass
class ValidationResult:
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate long-scene narration and subtitle cue CSV files."
    )
    parser.add_argument("--scenes", required=True, help="Scene CSV path.")
    parser.add_argument("--cues", required=True, help="Subtitle cue CSV path.")
    parser.add_argument(
        "--require-reviewed",
        action="store_true",
        help="Fail if reviewed scenes do not have reviewed or accepted cue rows.",
    )
    parser.add_argument(
        "--max-cue-chars",
        type=int,
        default=90,
        help="Warn when either subtitle line exceeds this character count.",
    )
    return parser.parse_args()


def read_csv(path: Path) -> CsvData:
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header row: {path}")
        rows = []
        for line_number, row in enumerate(reader, start=2):
            if row.get(None):
                extras = ", ".join(row[None])
                raise ValueError(
                    f"{path}:{line_number}: row has extra values: {extras}"
                )
            rows.append({key: (value or "").strip() for key, value in row.items()})

    return CsvData(path=path, fieldnames=reader.fieldnames, rows=rows)


def validate(scenes: CsvData, cues: CsvData, args: argparse.Namespace) -> ValidationResult:
    result = ValidationResult(errors=[], warnings=[])
    validate_headers(scenes, SCENE_REQUIRED_FIELDS, result)
    validate_headers(cues, CUE_REQUIRED_FIELDS, result)
    if result.errors:
        return result

    scene_keys = validate_scenes(scenes, result)
    validate_cues(cues, scene_keys, args, result)
    validate_scene_cue_coverage(scenes, cues, args, result)
    return result


def validate_headers(
    data: CsvData,
    required_fields: set[str],
    result: ValidationResult,
) -> None:
    fieldnames = set(data.fieldnames)
    missing = sorted(required_fields - fieldnames)
    if missing:
        result.error(f"{data.path}: missing required columns: {', '.join(missing)}")
    if not data.rows:
        result.error(f"{data.path}: file has no data rows")


def validate_scenes(
    scenes: CsvData,
    result: ValidationResult,
) -> set[tuple[str, str]]:
    seen_scene_keys: set[tuple[str, str]] = set()
    seen_clip_names: set[str] = set()

    for index, row in enumerate(scenes.rows, start=2):
        label = f"{scenes.path}:{index}"
        required_values = [
            "conversation_id",
            "section_id",
            "scene_id",
            "clip_name",
            "scene_title",
            "speaker",
            "style",
            "language",
            "text",
            "status",
        ]
        require_values(row, required_values, label, result)

        scene_key = (row["conversation_id"], row["scene_id"])
        if scene_key in seen_scene_keys:
            result.error(f"{label}: duplicate conversation_id/scene_id {scene_key}")
        seen_scene_keys.add(scene_key)

        clip_name = row["clip_name"]
        if clip_name in seen_clip_names:
            result.error(f"{label}: duplicate clip_name {clip_name}")
        seen_clip_names.add(clip_name)
        if clip_name and not SLUG_PATTERN.match(clip_name):
            result.error(f"{label}: clip_name is not filesystem-safe: {clip_name}")

        status = row["status"]
        if status and status not in SCENE_STATUSES:
            result.error(f"{label}: unsupported scene status: {status}")

        validate_optional_time_pair(
            row["start_time"],
            row["end_time"],
            label,
            "scene",
            result,
        )

        if len(row["text"]) > 900:
            result.warn(
                f"{label}: scene text is {len(row['text'])} characters; "
                "single-call TTS may be unstable, so chunking may be needed"
            )
    return seen_scene_keys


def validate_cues(
    cues: CsvData,
    scene_keys: set[tuple[str, str]],
    args: argparse.Namespace,
    result: ValidationResult,
) -> None:
    seen_cue_keys: set[tuple[str, str, str]] = set()
    previous_cue_id_by_scene: dict[tuple[str, str], str] = {}

    for index, row in enumerate(cues.rows, start=2):
        label = f"{cues.path}:{index}"
        required_values = [
            "conversation_id",
            "scene_id",
            "cue_id",
            "subtitle_zh",
            "subtitle_en",
            "status",
        ]
        require_values(row, required_values, label, result)

        scene_key = (row["conversation_id"], row["scene_id"])
        if scene_key not in scene_keys:
            result.error(f"{label}: cue references unknown scene {scene_key}")

        cue_key = (row["conversation_id"], row["scene_id"], row["cue_id"])
        if cue_key in seen_cue_keys:
            result.error(f"{label}: duplicate cue key {cue_key}")
        seen_cue_keys.add(cue_key)

        previous_cue_id = previous_cue_id_by_scene.get(scene_key)
        if previous_cue_id and natural_key(row["cue_id"]) < natural_key(previous_cue_id):
            result.warn(
                f"{label}: cue_id {row['cue_id']} sorts before previous cue "
                f"{previous_cue_id}"
            )
        previous_cue_id_by_scene[scene_key] = row["cue_id"]

        status = row["status"]
        if status and status not in CUE_STATUSES:
            result.error(f"{label}: unsupported cue status: {status}")

        validate_optional_time_pair(
            row["cue_start"],
            row["cue_end"],
            label,
            "cue",
            result,
        )

        for field in ["subtitle_zh", "subtitle_en"]:
            if len(row[field]) > args.max_cue_chars:
                result.warn(
                    f"{label}: {field} is {len(row[field])} characters; "
                    f"recommended max is {args.max_cue_chars}"
                )


def validate_scene_cue_coverage(
    scenes: CsvData,
    cues: CsvData,
    args: argparse.Namespace,
    result: ValidationResult,
) -> None:
    cues_by_scene: dict[tuple[str, str], list[dict[str, str]]] = {}
    for cue in cues.rows:
        key = (cue["conversation_id"], cue["scene_id"])
        cues_by_scene.setdefault(key, []).append(cue)

    for index, scene in enumerate(scenes.rows, start=2):
        label = f"{scenes.path}:{index}"
        key = (scene["conversation_id"], scene["scene_id"])
        scene_cues = cues_by_scene.get(key, [])
        if scene["status"] in {"reviewed", "generated", "accepted"} and not scene_cues:
            result.error(f"{label}: reviewed/generated scene has no subtitle cues")
            continue

        if args.require_reviewed and scene["status"] == "reviewed":
            unfinished = [
                cue["cue_id"]
                for cue in scene_cues
                if cue["status"] not in {"reviewed", "accepted"}
            ]
            if unfinished:
                result.error(
                    f"{label}: scene requires reviewed cues, but these cue IDs "
                    f"are not reviewed: {', '.join(unfinished)}"
                )


def require_values(
    row: dict[str, str],
    fields: list[str],
    label: str,
    result: ValidationResult,
) -> None:
    for field in fields:
        if not row.get(field):
            result.error(f"{label}: {field} is required")


def validate_optional_time_pair(
    start: str,
    end: str,
    label: str,
    kind: str,
    result: ValidationResult,
) -> None:
    if bool(start) != bool(end):
        result.error(f"{label}: {kind} start and end must both be set or both blank")
        return
    if not start and not end:
        return

    start_seconds = parse_timecode(start)
    end_seconds = parse_timecode(end)
    if start_seconds is None:
        result.error(f"{label}: unsupported {kind} start time: {start}")
        return
    if end_seconds is None:
        result.error(f"{label}: unsupported {kind} end time: {end}")
        return
    if end_seconds <= start_seconds:
        result.error(f"{label}: {kind} end time must be after start time")


def parse_timecode(value: str) -> float | None:
    match = TIMECODE_PATTERN.match(value)
    if not match:
        return None
    hours = int(match.group("hours") or 0)
    minutes = int(match.group("minutes"))
    seconds = int(match.group("seconds"))
    millis_text = match.group("millis")
    frames_text = match.group("frames")

    if minutes >= 60 or seconds >= 60:
        return None
    total = (hours * 3600) + (minutes * 60) + seconds
    if millis_text:
        total += float(f"0{millis_text.replace(',', '.')}")
    if frames_text:
        frames = int(frames_text)
        if frames >= 30:
            return None
        total += frames / 30.0
    return total


def natural_key(value: str) -> tuple[int, str]:
    if value.isdigit():
        return (int(value), value)
    return (sys.maxsize, value)


def print_result(result: ValidationResult) -> None:
    if result.errors:
        print("Validation failed")
        for error in result.errors:
            print(f"ERROR: {error}")
    else:
        print("Validation passed")

    for warning in result.warnings:
        print(f"WARNING: {warning}")


def main() -> int:
    args = parse_args()
    try:
        scenes = read_csv(Path(args.scenes))
        cues = read_csv(Path(args.cues))
        result = validate(scenes, cues, args)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print_result(result)
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
