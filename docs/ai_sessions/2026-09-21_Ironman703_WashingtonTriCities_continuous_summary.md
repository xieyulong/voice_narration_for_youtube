# IRONMAN 70.3 Washington Tri-Cities Continuous Narration Summary

## Purpose

Create a new long-form bilingual narration for the September 20, 2026
IRONMAN 70.3 Washington Tri-Cities event. The approved Chinese narration was
treated as one continuous narration, split into short reviewed cues, and
generated as one uninterrupted cue sequence.

## Batch

- Batch name: `Ironman703_WashingtonTriCities_2026_09_20_continuous`
- Scene ID: `IMTC20260920`
- Speaker profile: `yulong_new_001`
- Generation mode: `timed_cue_qwen3_tts`
- Measured duration: `00:08:14.480`
- Source scene CSV:
  `transcripts/scenes_Ironman703_WashingtonTriCities_2026_09_20_continuous.csv`
- Source cue CSV:
  `transcripts/subtitle_cues_Ironman703_WashingtonTriCities_2026_09_20_continuous.csv`

## Timing

- 81 approved bilingual cues were generated from the approved cue draft.
- Each cue start and end was retimed from the corresponding WAV frame count.
- Cue 1 starts at `00:00:00.000`; every following cue starts immediately after
  the preceding cue's measured audio end.
- No text was changed during retiming.

## Generated Deliverables

- WAV:
  `output/audio_scenes/Ironman703_WashingtonTriCities_2026_09_20_continuous/Ironman703_WashingtonTriCities_2026_09_20_continuous.wav`
- Bilingual SRT:
  `output/captions/Ironman703_WashingtonTriCities_2026_09_20_continuous/Ironman703_WashingtonTriCities_2026_09_20_continuous.bilingual.srt`
- Bilingual VTT:
  `output/captions/Ironman703_WashingtonTriCities_2026_09_20_continuous/Ironman703_WashingtonTriCities_2026_09_20_continuous.bilingual.vtt`
- Manifest:
  `output/manifests/manifest_Ironman703_WashingtonTriCities_2026_09_20_continuous.csv`

Generated media remains local output and is not tracked by git.

## Verification

- Strict cue validation passed with `--require-reviewed --max-cue-chars 90
  --fail-on-cue-length`.
- 81 cue WAV files were present and reused for final assembly.
- Final WAV verified with `soxi`: mono, 48000 Hz, 16-bit PCM, duration
  `00:08:14.480`.
- Final SRT begins at `00:00:00.000`, ends at `00:08:14.480`, and contains
  81 cues with continuous measured boundaries.
- Exact event counts retained from the user's draft where public verification
  was not available during preparation.
