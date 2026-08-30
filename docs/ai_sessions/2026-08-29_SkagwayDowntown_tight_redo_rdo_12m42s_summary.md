# Skagway Downtown Tight Redo rdo 12m42s Summary

## Purpose

Rebuild the `SkagwayDowntown_TightRedo_2026_06_24_12m42s` timed-cue
narration package with the same source narration and cue text, but with
measured cue timing adjustments to avoid consecutive-cue overlap truncation.

## Batch

- Batch name: `SkagwayDowntown_TightRedo_rdo_2026_06_24_12m42s`
- Scene ID: `SDT001`
- Speaker profile: `yulong_new_001`
- Generation mode: `timed_cue_qwen3_tts`
- Planned video timeline: `00:00:00.000` to `00:12:42.000`
- Draft source: `draft_Skagway_Downtone.csv`
- Source scene CSV:
  `transcripts/scenes_SkagwayDowntown_TightRedo_rdo_2026_06_24_12m42s.csv`
- Source cue CSV:
  `transcripts/subtitle_cues_SkagwayDowntown_TightRedo_rdo_2026_06_24_12m42s.csv`

## Timing Changes

- Preserved all Chinese cue text, English cue text, and scene narration text
  from the prior TightRedo source.
- Reused the existing per-cue WAV chunks because the spoken text did not
  change.
- Rebuilt cue timing from measured cue WAV durations.
- Added a 0.25 second guard before normal consecutive cue starts when the
  previous measured cue audio would otherwise overlap the next cue.
- Made final cue rows 32 through 35 contiguous, with each following cue
  starting immediately after the previous measured cue audio ends.
- Verified there are no negative measured audio gaps between consecutive cues.

The reported truncation pairs were corrected by moving the following cue start:

- cue rows 1 and 2: protected the ending word in cue row 1.
- cue rows 8 and 9: protected the ending phrase in cue row 8.
- cue rows 11 and 12: protected the ending phrase in cue row 11.
- cue rows 23 and 24: protected the ending phrase in cue row 23.

## Generated Deliverables

- WAV:
  `output/audio_scenes/SkagwayDowntown_TightRedo_rdo_2026_06_24_12m42s/SkagwayDowntown_TightRedo_rdo_2026_06_24_12m42s.wav`
- Bilingual SRT:
  `output/captions/SkagwayDowntown_TightRedo_rdo_2026_06_24_12m42s/SkagwayDowntown_TightRedo_rdo_2026_06_24_12m42s.bilingual.srt`
- Bilingual VTT:
  `output/captions/SkagwayDowntown_TightRedo_rdo_2026_06_24_12m42s/SkagwayDowntown_TightRedo_rdo_2026_06_24_12m42s.bilingual.vtt`
- Manifest:
  `output/manifests/manifest_SkagwayDowntown_TightRedo_rdo_2026_06_24_12m42s.csv`

Generated media remains local output and is not tracked by git.

## Verification

- Strict cue validation passed with:
  `--require-reviewed --max-cue-chars 90 --fail-on-cue-length`
- Text preservation check passed:
  35 cue rows, same Chinese cue text, same English cue text, same scene text.
- Targeted syntax check passed:
  `.venv-qwen3-tts/bin/python -m py_compile scripts/generate_long_scene_assets.py scripts/validate_long_scene_inputs.py`
- Measured spacing check passed:
  35 cue rows and 0 negative audio gaps.
- `soxi` result for final WAV:
  mono, 48000 Hz, 16-bit PCM, duration `00:12:42.00`.

## Notes

- The previous `SkagwayDowntown_TightRedo_2026_06_24_12m42s` outputs were not
  overwritten.
- The `rdo` batch was assembled with `--reuse-existing-cue-audio`; no new
  Qwen3-TTS cue synthesis was needed because cue wording did not change.
