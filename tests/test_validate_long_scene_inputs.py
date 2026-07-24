from __future__ import annotations

import csv
import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from scripts.validate_long_scene_inputs import main


SCENE_FIELDS = [
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
]
CUE_FIELDS = [
    "conversation_id",
    "scene_id",
    "cue_id",
    "cue_start",
    "cue_end",
    "subtitle_zh",
    "subtitle_en",
    "notes",
    "status",
]


class ValidateLongSceneInputsTest(unittest.TestCase):
    def test_valid_pair_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            scenes = Path(temp_dir) / "scenes.csv"
            cues = Path(temp_dir) / "cues.csv"
            write_csv(
                scenes,
                SCENE_FIELDS,
                [
                    {
                        "conversation_id": "trip",
                        "section_id": "skagway",
                        "scene_id": "001",
                        "clip_name": "skagway_scene",
                        "scene_title": "Skagway Scene",
                        "start_time": "",
                        "end_time": "",
                        "speaker": "owner_calm",
                        "style": "reflective",
                        "language": "zh",
                        "text": "这是一个测试场景。",
                        "notes": "",
                        "status": "reviewed",
                    }
                ],
            )
            write_csv(
                cues,
                CUE_FIELDS,
                [
                    {
                        "conversation_id": "trip",
                        "scene_id": "001",
                        "cue_id": "001",
                        "cue_start": "",
                        "cue_end": "",
                        "subtitle_zh": "这是一个测试场景。",
                        "subtitle_en": "This is a test scene.",
                        "notes": "",
                        "status": "reviewed",
                    }
                ],
            )

            self.assertEqual(
                main_with_args(
                    "--scenes",
                    str(scenes),
                    "--cues",
                    str(cues),
                    "--require-reviewed",
                ),
                0,
            )

    def test_unknown_scene_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            scenes = Path(temp_dir) / "scenes.csv"
            cues = Path(temp_dir) / "cues.csv"
            write_csv(
                scenes,
                SCENE_FIELDS,
                [
                    {
                        "conversation_id": "trip",
                        "section_id": "skagway",
                        "scene_id": "001",
                        "clip_name": "skagway_scene",
                        "scene_title": "Skagway Scene",
                        "start_time": "",
                        "end_time": "",
                        "speaker": "owner_calm",
                        "style": "reflective",
                        "language": "zh",
                        "text": "这是一个测试场景。",
                        "notes": "",
                        "status": "reviewed",
                    }
                ],
            )
            write_csv(
                cues,
                CUE_FIELDS,
                [
                    {
                        "conversation_id": "trip",
                        "scene_id": "999",
                        "cue_id": "001",
                        "cue_start": "",
                        "cue_end": "",
                        "subtitle_zh": "这是一个测试场景。",
                        "subtitle_en": "This is a test scene.",
                        "notes": "",
                        "status": "reviewed",
                    }
                ],
            )

            self.assertEqual(main_with_args("--scenes", str(scenes), "--cues", str(cues)), 1)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main_with_args(*args: str) -> int:
    import sys

    old_argv = sys.argv
    try:
        sys.argv = ["validate_long_scene_inputs.py", *args]
        with contextlib.redirect_stdout(io.StringIO()):
            return main()
    finally:
        sys.argv = old_argv


if __name__ == "__main__":
    unittest.main()
