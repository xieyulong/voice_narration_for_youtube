# Fujiyama Timed Narration Implementation Summary

## Date

2026-07-23

## Scope

Prepare a Fujiyama Richland short-video narration batch with intentional silence
between spoken segments.

## Files Added Or Changed

- `transcripts/scenes_fujiyama_richland_2026_07_20.csv`
- `transcripts/subtitle_cues_fujiyama_richland_2026_07_20.csv`
- `scripts/generate_long_scene_assets.py`
- `tests/test_generate_long_scene_assets.py`
- `docs/long_scene_workflow.md`

## Design

The Fujiyama video is 4:02 long, but the narration should not cover the entire
video. The batch uses timed subtitle cues where:

- `subtitle_zh` is the exact spoken Chinese narration for that segment;
- `subtitle_en` is the exact English translation of that same segment;
- each caption block displays exactly two text lines: English, then Chinese;
- `cue_start` places each speech segment on the video timeline;
- silence is preserved between cue starts.

The generator now supports `--generation-mode timed-cues`, which synthesizes
each cue separately and assembles one full-length scene WAV with silence between
the spoken cue audio.

## Generated Local Outputs

Generated outputs are ignored by git:

```text
output/audio_scenes/fujiyama_richland_2026_07_20/fujiyama_richland_2026_07_20.wav
output/audio_chunks/fujiyama_richland_2026_07_20/fujiyama_richland_2026_07_20/
output/captions/fujiyama_richland_2026_07_20/fujiyama_richland_2026_07_20.bilingual.srt
output/captions/fujiyama_richland_2026_07_20/fujiyama_richland_2026_07_20.bilingual.vtt
output/manifests/manifest_fujiyama_richland_2026_07_20.csv
```

Final WAV verification:

```text
Duration: 00:04:02.47
Sample Rate: 48000
Channels: mono
Encoding: 16-bit Signed Integer PCM
```

The manifest records:

```text
duration_seconds: 242.467
generation_mode: timed_cue_qwen3_tts
subtitle_cue_count: 14
```

## Verification

```text
Validation passed
Ran 7 tests: OK
```
