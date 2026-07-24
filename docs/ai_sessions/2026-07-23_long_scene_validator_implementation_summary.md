# Long Scene Validator Implementation Summary

## Date

2026-07-23

## Scope

Build the first validator for long-scene narration CSVs and subtitle cue CSVs.

## Files Changed

- `scripts/validate_long_scene_inputs.py`
- `tests/test_validate_long_scene_inputs.py`
- `docs/long_scene_workflow.md`
- `transcripts/subtitle_cues_skagway_white_pass_railway_001.csv`

## Behavior

The validator checks required columns, required values, unique scene IDs and
clip names, cue references, reviewed cue readiness, optional time pairs, cue
line length warnings, and long scene text chunking warnings.

## Data Update

The Skagway subtitle cue statuses were changed from `draft_review_needed` to
`reviewed` because the user approved the drafted subtitle cues before this
implementation step.

## Verification

Run these checks after implementation:

```bash
.venv-qwen3-tts/bin/python scripts/validate_long_scene_inputs.py \
  --scenes transcripts/scenes_skagway_white_pass_railway_001.csv \
  --cues transcripts/subtitle_cues_skagway_white_pass_railway_001.csv \
  --require-reviewed

.venv-qwen3-tts/bin/python -m unittest discover -s tests

.venv-qwen3-tts/bin/python -m py_compile scripts/validate_long_scene_inputs.py \
  tests/test_validate_long_scene_inputs.py

git diff --check
```
