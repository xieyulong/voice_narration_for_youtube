"""Create reviewed scene and subtitle-cue CSVs from the Step 1 draft."""

from __future__ import annotations

import csv
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRANSCRIPTS = ROOT / "transcripts"
BUILDER = ROOT / "scripts/build_whitepass_step1_annotation.py"


SubtitleSegment = tuple[str, str]


def load_narrations() -> list[list[SubtitleSegment]]:
    spec = importlib.util.spec_from_file_location("step1_builder", BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load Step 1 narration draft")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.NARRATIONS


def narration_pair(segments: list[SubtitleSegment]) -> tuple[str, str]:
    english = " ".join(segment[0] for segment in segments)
    chinese = "".join(segment[1] for segment in segments)
    return english, chinese


ROWS = [
    ("01:00:00:00", "start", ""),
    ("01:03:30:30", "Mile 0.0: Skagway - Sea Level", "double"),
    ("01:04:05:26", "Mile 2.0: Maintenance Shops", "double"),
    ("01:05:06:15", "Mile 5.8: Denver - 402FT", "double"),
    ("01:06:38:01", "Mile 8.7: Clifton - 849FT", "double"),
    ("01:06:45:29", "Mile 8.8: Buchanan Rock - 849FT", "double"),
    ("01:06:59:13", "Mile 11.5: Bridal Veil Falls - 1334FT", ""),
    ("01:07:51:26", "Mile 10.4: Black Cross Rock - 1090FT", "double"),
    ("01:08:59:12", "Mile 12.3: Heney Station - 1573FT", ""),
    ("01:09:52:27", "Mile 14.0: Glacier Station - 1871FT", ""),
    ("01:11:16:24", "Mile 15.6: Slippery Rock - 2139FT", ""),
    ("01:11:44:22", "Mile 16.0: Tunnel Mountain - 2275FT", "double"),
    ("01:13:00:08", "Mile 17.0: Inspiration Point - 2413FT", "double"),
    ("01:13:25:16", "Mile 17.5: Dead Horse Gulch - 2463FT", ""),
    ("01:14:22:08", "Mile 18.6: Steel Bridge - 2613FT", "double"),
    ("01:14:45:11", "Mile 18.8: Tunnel - 2715FT", ""),
    ("01:16:04:13", "Mile 20.4: White Pass - 2888FT", ""),
    ("01:19:12:27", "Mile 18.6: Steel Bridge - 2613FT", "double"),
    ("01:19:29:01", "Mile 17.0: Inspiration Point - 2413FT", "double"),
    ("01:19:40:12", "Mile 16.0: Tunnel Mountain - 2275FT", "double"),
    ("01:21:57:05", "Mile 11.4: Foy - 1400FT", ""),
    ("01:22:36:01", "Mile 10.4: Black Cross Rock - 1090FT", "double"),
    ("01:23:10:25", "Mile 8.8: Buchanan Rock - 849FT", "double"),
    ("01:23:17:09", "Mile 8.5: Clifton - 849FT", "double"),
    ("01:25:05:26", "Mile 6.9: Rocky Point - 637FT", ""),
    ("01:25:23:20", "Mile 5.8: Denver - 402FT", "double"),
    ("01:25:39:20", "Mile 2.0: Maintenance Shops", "double"),
    ("01:26:04:25", "Mile 0.0: Skagway Downtown - Sea Level", "double"),
]

SEGMENTS = [
    (1, "00_00_to_08_59", 0, 8, "Outbound climb from Skagway"),
    (2, "08_59_to_16_04", 8, 16, "Upper route and White Pass approach"),
    (3, "16_04_to_21_57", 16, 20, "Summit and beginning of return descent"),
    (4, "21_57_to_27_15", 20, 28, "Return through the lower route to Skagway"),
]


def to_seconds(timecode: str) -> float:
    parts = timecode.split(":")
    if len(parts) != 4:
        raise ValueError(f"Unexpected timecode: {timecode}")
    _hour, minute, second, frame = parts
    return int(minute) * 60 + int(second) + int(frame) / 30.0


def timecode(seconds: float) -> str:
    total_frames = round(seconds * 30)
    minutes, frame = divmod(total_frames, 30 * 60)
    second, frame = divmod(frame, 30)
    return f"00:{minutes:02d}:{second:02d}.{frame * 1000 // 30:03d}"


def segment_time_ranges(
    start: float,
    end: float,
    segments: list[SubtitleSegment],
) -> list[tuple[float, float]]:
    if end <= start:
        raise ValueError("Segment end must be after start")
    weights = [max(len("".join(chinese.split())), 1) for _english, chinese in segments]
    total_weight = sum(weights)
    duration = end - start
    ranges = []
    cursor = start
    for index, weight in enumerate(weights):
        if index == len(weights) - 1:
            next_cursor = end
        else:
            next_cursor = cursor + (duration * weight / total_weight)
        ranges.append((cursor, next_cursor))
        cursor = next_cursor
    return ranges


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    narrations = load_narrations()
    if len(ROWS) != len(narrations):
        raise RuntimeError("Timing rows and narration rows do not match")
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)

    for part, range_name, start_index, end_index, title in SEGMENTS:
        batch = (
            "WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_"
            f"part_{part:03d}_mile_{range_name}"
        )
        entries = []
        for index in range(start_index, end_index):
            start = to_seconds(ROWS[index][0])
            next_start = (
                to_seconds(ROWS[index + 1][0])
                if index + 1 < end_index
                else to_seconds(ROWS[end_index][0])
                if end_index < len(ROWS)
                else 1635.833333
            )
            english, chinese = narration_pair(narrations[index])
            entries.append(
                {
                    "index": index,
                    "start": start,
                    "end": next_start,
                    "location": ROWS[index][1],
                    "double": ROWS[index][2],
                    "english": english,
                    "chinese": chinese,
                    "segments": narrations[index],
                }
            )

        scene_id = f"{batch}_scene"
        scene_start = entries[0]["start"]
        scene_end = entries[-1]["end"]
        scene_fields = [
            "conversation_id", "section_id", "scene_id", "clip_name",
            "scene_title", "start_time", "end_time", "speaker", "style",
            "language", "text", "notes", "status",
        ]
        scene_row = {
            "conversation_id": "WhitePassScenicTrainRide_Redo_2026_06_24",
            "section_id": f"part_{part:03d}",
            "scene_id": scene_id,
            "clip_name": batch,
            "scene_title": title,
            "start_time": timecode(scene_start),
            "end_time": timecode(scene_end),
            "speaker": "yulong_new_001",
            "style": "calm documentary travel narration",
            "language": "zh",
            "text": "\n".join(item["chinese"] for item in entries),
            "notes": "Step 1 reviewed draft; double markers preserved as separate journey appearances.",
            "status": "reviewed",
        }
        cue_fields = [
            "conversation_id", "scene_id", "cue_id", "cue_start", "cue_end",
            "subtitle_zh", "subtitle_en", "notes", "status",
        ]
        cue_rows = []
        cue_number = 1
        for item in entries:
            pass_label = "double location" if item["double"] else "single location"
            segment_ranges = segment_time_ranges(
                item["start"],
                item["end"],
                item["segments"],
            )
            segment_count = len(item["segments"])
            for segment_index, ((start, end), segment) in enumerate(
                zip(segment_ranges, item["segments"]),
                start=1,
            ):
                english, chinese = segment
                cue_rows.append(
                    {
                        "conversation_id": scene_row["conversation_id"],
                        "scene_id": scene_id,
                        "cue_id": f"cue_{cue_number:03d}",
                        "cue_start": timecode(start),
                        "cue_end": timecode(end),
                        "subtitle_zh": chinese,
                        "subtitle_en": english,
                        "notes": (
                            f"{item['location']}; {pass_label}; segment "
                            f"{segment_index}/{segment_count}; "
                            "absolute video-relative timing."
                        ),
                        "status": "reviewed",
                    }
                )
                cue_number += 1
        write_csv(TRANSCRIPTS / f"scenes_{batch}.csv", scene_fields, [scene_row])
        write_csv(TRANSCRIPTS / f"subtitle_cues_{batch}.csv", cue_fields, cue_rows)
        print(batch)


if __name__ == "__main__":
    main()
