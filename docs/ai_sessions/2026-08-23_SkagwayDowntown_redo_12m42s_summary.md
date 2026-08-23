# Skagway Downtown Redo 12m42s Summary

## Purpose

Create a new single-batch timed-cue narration package for the revised
12:42 Skagway downtown video. This batch uses a new naming convention and does
not modify the older `SkagwayDowntown_part_*` products.

## Batch

- Batch name: `SkagwayDowntown_Redo_2026_06_24_12m42s`
- Scene ID: `SDR001`
- Speaker profile: `yulong_new_001`
- Generation mode: `timed_cue_qwen3_tts`
- Planned video timeline: `00:00:00.000` to `00:12:42.000`
- Source scene CSV:
  `transcripts/scenes_SkagwayDowntown_Redo_2026_06_24_12m42s.csv`
- Source cue CSV:
  `transcripts/subtitle_cues_SkagwayDowntown_Redo_2026_06_24_12m42s.csv`

## Cue Protocol

- User-provided table times are interpreted as `M:SS:FF` at 30 fps.
- Subtitle cue format remains English first, Chinese second.
- Chinese cue text is the exact voice text for that generated cue.
- English text is a faithful translation of the Chinese cue.
- Cue text is split tightly for DaVinci one-line readability.
- Validation command uses `--max-cue-chars 90 --fail-on-cue-length`.
- Final cue table: 92 cues, max Chinese cue length 44 characters, max English
  cue length 79 characters.
- Dense late-video narration required shifted internal cue timing to avoid
  overlap while preserving the user-provided narration text.

## Generated Deliverables

- WAV:
  `output/audio_scenes/SkagwayDowntown_Redo_2026_06_24_12m42s/SkagwayDowntown_Redo_2026_06_24_12m42s.wav`
- Bilingual SRT:
  `output/captions/SkagwayDowntown_Redo_2026_06_24_12m42s/SkagwayDowntown_Redo_2026_06_24_12m42s.bilingual.srt`
- Bilingual VTT:
  `output/captions/SkagwayDowntown_Redo_2026_06_24_12m42s/SkagwayDowntown_Redo_2026_06_24_12m42s.bilingual.vtt`
- Manifest:
  `output/manifests/manifest_SkagwayDowntown_Redo_2026_06_24_12m42s.csv`

Generated media remains local output and is not tracked by git.

## Tooling Change

`scripts/generate_long_scene_assets.py` now supports
`--reuse-existing-cue-audio` for timed-cue generation. This allows interrupted
Qwen3-TTS runs to resume by reusing existing per-cue WAV chunks when the cue
text has not changed.

During this batch, one generated chunk for `cue_070b2` was abnormally long
for the text `景观列车。`. The bad local chunk was moved aside and regenerated;
the final assembled WAV uses the regenerated chunk.

## Verification

- Strict cue validation passed with:
  `--require-reviewed --max-cue-chars 90 --fail-on-cue-length`
- Cue count check passed: 92 cue rows and 0 missing current cue chunks.
- Generator syntax check passed:
  `.venv-qwen3-tts/bin/python -m py_compile scripts/generate_long_scene_assets.py`
- `soxi` result for final WAV:
  mono, 48000 Hz, 16-bit PCM, duration `00:12:42.48`.

## Notes

- The older Skagway downtown outputs were intentionally not changed.
- The untracked workbook `transcripts/Time_point_Skagway_Downtown.xlsx` was
  present before this work and was left untouched.
