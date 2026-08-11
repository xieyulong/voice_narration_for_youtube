# Skagway Xiaohai Regeneration Summary

## Date

2026-07-26

## Scope

Regenerate the Skagway White Pass Railway narration with the Xiaohai reference
voice while preserving the original Skagway batch outputs.

## Inputs

- `transcripts/scenes_skagway_white_pass_railway_Xiaohai_001.csv`
- `transcripts/subtitle_cues_skagway_white_pass_railway_Xiaohai_001.csv`
- `voice_profiles/owner_calm/profile.yaml`

The Xiaohai private reference entry uses:

```text
samples/clean/sample_xiaohai_zhang_new_001_clean.wav
```

The raw source file available in this checkout is:

```text
samples/raw/Sample_Xiaohai_New_001.wav
```

## Generated Local Outputs

Generated outputs are ignored by git:

```text
output/audio_scenes/skagway_white_pass_railway_Xiaohai_001/skagway_white_pass_railway_Xiaohai.wav
output/audio_chunks/skagway_white_pass_railway_Xiaohai_001/skagway_white_pass_railway_Xiaohai/
output/captions/skagway_white_pass_railway_Xiaohai_001/skagway_white_pass_railway_Xiaohai.bilingual.srt
output/captions/skagway_white_pass_railway_Xiaohai_001/skagway_white_pass_railway_Xiaohai.bilingual.vtt
output/manifests/manifest_skagway_white_pass_railway_Xiaohai_001.csv
```

Final WAV verification:

```text
Duration: 00:02:37.12
Sample Rate: 48000
Channels: mono
Encoding: 16-bit Signed Integer PCM
```

The manifest records:

```text
duration_seconds: 157.120
generation_mode: chunked_qwen3_tts
subtitle_cue_count: 20
```

## Verification

```text
Validation passed
Dry run passed
Ran 7 tests: OK
git diff --check passed
```
