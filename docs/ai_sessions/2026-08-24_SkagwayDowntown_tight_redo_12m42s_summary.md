# Skagway Downtown Tight Redo 12m42s Summary

## Purpose

Create a reduced narration pass for the same 12:42 Skagway downtown video,
using a new non-overwriting batch name and tighter English captions for
DaVinci one-line readability.

## Batch

- Batch name: `SkagwayDowntown_TightRedo_2026_06_24_12m42s`
- Scene ID: `SDT001`
- Speaker profile: `yulong_new_001`
- Generation mode: `timed_cue_qwen3_tts`
- Planned video timeline: `00:00:00.000` to `00:12:42.000`
- Draft source: `draft_Skagway_Downtone.csv`
- Source scene CSV:
  `transcripts/scenes_SkagwayDowntown_TightRedo_2026_06_24_12m42s.csv`
- Source cue CSV:
  `transcripts/subtitle_cues_SkagwayDowntown_TightRedo_2026_06_24_12m42s.csv`

## Cue Protocol

- User draft times were used as timeline anchors.
- The reduced narration intentionally leaves quiet gaps between some anchors.
- Chinese cue text matches the generated Chinese voice text for each cue.
- English cues were translated tightly to reduce line wrapping in DaVinci.
- Final cue table: 35 cues, max Chinese cue length 32 characters, max English
  cue length 52 characters.
- The draft time `11:33:33` is invalid as a 30 fps frame time, so it was
  normalized to `00:11:33.000` and noted in the cue CSV.

## Generated Deliverables

- WAV:
  `output/audio_scenes/SkagwayDowntown_TightRedo_2026_06_24_12m42s/SkagwayDowntown_TightRedo_2026_06_24_12m42s.wav`
- Bilingual SRT:
  `output/captions/SkagwayDowntown_TightRedo_2026_06_24_12m42s/SkagwayDowntown_TightRedo_2026_06_24_12m42s.bilingual.srt`
- Bilingual VTT:
  `output/captions/SkagwayDowntown_TightRedo_2026_06_24_12m42s/SkagwayDowntown_TightRedo_2026_06_24_12m42s.bilingual.vtt`
- Manifest:
  `output/manifests/manifest_SkagwayDowntown_TightRedo_2026_06_24_12m42s.csv`

Generated media remains local output and is not tracked by git.

## Verification

- Strict cue validation passed with:
  `--require-reviewed --max-cue-chars 90 --fail-on-cue-length`
- Cue count check passed: 35 cue rows and 0 missing current cue chunks.
- Final cue lengths: max Chinese 32, max English 52.
- `soxi` result for final WAV:
  mono, 48000 Hz, 16-bit PCM, duration `00:12:42.00`.

## Notes

- The previous `SkagwayDowntown_Redo_2026_06_24_12m42s` outputs were not
  overwritten.
- `transcripts/Time_point_Skagway_Downtown.xlsx` already has local changes in
  the working tree and was not modified by this batch.
