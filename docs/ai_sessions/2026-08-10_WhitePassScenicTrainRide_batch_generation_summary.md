# WhitePassScenicTrainRide Batch Generation Summary

## Date

2026-08-10

## Scope

Prepared and generated the first `WhitePassScenicTrainRide` bilingual narration
batches for DaVinci Resolve.

The user asked to ignore older Skagway/White Pass source files and use
`WhitePassScenicTrainRide` as the default naming string for newly created
files and output folders.

## Source CSV Batches

Committed source inputs:

```text
transcripts/scenes_WhitePassScenicTrainRide_test_001.csv
transcripts/subtitle_cues_WhitePassScenicTrainRide_test_001.csv
transcripts/scenes_WhitePassScenicTrainRide_mile_00_00_to_06_90.csv
transcripts/subtitle_cues_WhitePassScenicTrainRide_mile_00_00_to_06_90.csv
transcripts/scenes_WhitePassScenicTrainRide_mile_07_30_to_14_00.csv
transcripts/subtitle_cues_WhitePassScenicTrainRide_mile_07_30_to_14_00.csv
transcripts/scenes_WhitePassScenicTrainRide_mile_16_00_to_18_60.csv
transcripts/subtitle_cues_WhitePassScenicTrainRide_mile_16_00_to_18_60.csv
transcripts/scenes_WhitePassScenicTrainRide_mile_18_80_to_20_40.csv
transcripts/subtitle_cues_WhitePassScenicTrainRide_mile_18_80_to_20_40.csv
```

## Generated Local Outputs

Generated outputs are local-only and ignored by git.

Opening test:

```text
output/audio_scenes/WhitePassScenicTrainRide_test_001/WhitePassScenicTrainRide_test_001.wav
output/captions/WhitePassScenicTrainRide_test_001/WhitePassScenicTrainRide_test_001.bilingual.srt
output/captions/WhitePassScenicTrainRide_test_001/WhitePassScenicTrainRide_test_001.bilingual.vtt
output/manifests/manifest_WhitePassScenicTrainRide_test_001.csv
```

Mile-marker batches:

```text
output/audio_scenes/WhitePassScenicTrainRide_mile_00_00_to_06_90/WhitePassScenicTrainRide_mile_00_00_to_06_90.wav
output/captions/WhitePassScenicTrainRide_mile_00_00_to_06_90/WhitePassScenicTrainRide_mile_00_00_to_06_90.bilingual.srt
output/manifests/manifest_WhitePassScenicTrainRide_mile_00_00_to_06_90.csv

output/audio_scenes/WhitePassScenicTrainRide_mile_07_30_to_14_00/WhitePassScenicTrainRide_mile_07_30_to_14_00.wav
output/captions/WhitePassScenicTrainRide_mile_07_30_to_14_00/WhitePassScenicTrainRide_mile_07_30_to_14_00.bilingual.srt
output/manifests/manifest_WhitePassScenicTrainRide_mile_07_30_to_14_00.csv

output/audio_scenes/WhitePassScenicTrainRide_mile_16_00_to_18_60/WhitePassScenicTrainRide_mile_16_00_to_18_60.wav
output/captions/WhitePassScenicTrainRide_mile_16_00_to_18_60/WhitePassScenicTrainRide_mile_16_00_to_18_60.bilingual.srt
output/manifests/manifest_WhitePassScenicTrainRide_mile_16_00_to_18_60.csv

output/audio_scenes/WhitePassScenicTrainRide_mile_18_80_to_20_40/WhitePassScenicTrainRide_mile_18_80_to_20_40.wav
output/captions/WhitePassScenicTrainRide_mile_18_80_to_20_40/WhitePassScenicTrainRide_mile_18_80_to_20_40.bilingual.srt
output/manifests/manifest_WhitePassScenicTrainRide_mile_18_80_to_20_40.csv
```

## Durations

```text
WhitePassScenicTrainRide_test_001: 00:01:23.36
WhitePassScenicTrainRide_mile_00_00_to_06_90: 00:01:47.20
WhitePassScenicTrainRide_mile_07_30_to_14_00: 00:02:05.36
WhitePassScenicTrainRide_mile_16_00_to_18_60: 00:01:39.76
WhitePassScenicTrainRide_mile_18_80_to_20_40: 00:01:35.68
```

The four mile-marker files total `00:07:08.00`.

## Generation Notes

- `owner_calm` / `yulong_new_001` was used as the voice reference.
- The first three mile-marker outputs used `chunked_qwen3_tts`.
- The original long `mile_16_00_to_20_40` chunked run stalled on a long
  internal chunk, so that section was split into:
  - `WhitePassScenicTrainRide_mile_16_00_to_18_60`
  - `WhitePassScenicTrainRide_mile_18_80_to_20_40`
- The final `mile_18_80_to_20_40` output used `timed_cue_qwen3_tts` with
  provisional cue timings for reliable short-cue synthesis.

## Verification

Completed checks:

```text
validate_long_scene_inputs.py --require-reviewed: passed for all five batches
generate_long_scene_assets.py --dry-run: passed before synthesis
soxi: all generated WAV files are mono, 48 kHz, 16-bit PCM
git diff --check: passed
```

Generated audio, chunks, captions, and manifests remain ignored by git.
