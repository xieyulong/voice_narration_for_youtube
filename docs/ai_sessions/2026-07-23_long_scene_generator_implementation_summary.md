# Long Scene Generator Implementation Summary

## Date

2026-07-23

## Scope

Add the first long-scene asset generator for validated scene CSVs and subtitle
cue CSVs.

## Files Changed

- `scripts/generate_long_scene_assets.py`
- `tests/test_generate_long_scene_assets.py`
- `docs/long_scene_workflow.md`

## Behavior

The generator validates the scene/cue pair, loads the private voice profile,
selects a reference voice, and prepares scene-level deliverables for a batch.

It supports three usage levels:

- `--dry-run`: validate and print the planned asset paths without writing files.
- default: write bilingual SRT/VTT captions and a manifest using estimated
  duration, but do not synthesize audio.
- `--synthesize`: generate one Qwen3-TTS WAV per scene, then write captions and
  manifest using actual audio duration.

For long narration, use `--generation-mode chunked`. A single full-scene
Qwen3-TTS call on CPU was too slow for the first Skagway scene and was stopped
before any WAV file was written.

Audio generation still requires explicit approval of exact inputs before use.

## Verification

Run these checks after implementation:

```bash
.venv-qwen3-tts/bin/python scripts/generate_long_scene_assets.py \
  --batch-name skagway_white_pass_railway_001 \
  --scenes transcripts/scenes_skagway_white_pass_railway_001.csv \
  --cues transcripts/subtitle_cues_skagway_white_pass_railway_001.csv \
  --dry-run

.venv-qwen3-tts/bin/python -m unittest discover -s tests

.venv-qwen3-tts/bin/python -m py_compile \
  scripts/validate_long_scene_inputs.py \
  scripts/generate_long_scene_assets.py \
  tests/test_validate_long_scene_inputs.py \
  tests/test_generate_long_scene_assets.py

git diff --check
```

## First Synthesis Result

The first full-scene single-call synthesis attempt was stopped after several
minutes because it had not produced an output WAV. Chunked synthesis was then
used successfully:

```bash
NUMBA_CACHE_DIR=/private/tmp/numba_cache \
.venv-qwen3-tts/bin/python scripts/generate_long_scene_assets.py \
  --batch-name skagway_white_pass_railway_001 \
  --scenes transcripts/scenes_skagway_white_pass_railway_001.csv \
  --cues transcripts/subtitle_cues_skagway_white_pass_railway_001.csv \
  --profile-reference yulong_new_001 \
  --generation-mode chunked \
  --synthesize \
  --overwrite
```

Generated local outputs:

- `output/audio_chunks/skagway_white_pass_railway_001/skagway_white_pass_railway/`
- `output/audio_scenes/skagway_white_pass_railway_001/skagway_white_pass_railway.wav`
- `output/captions/skagway_white_pass_railway_001/skagway_white_pass_railway.bilingual.srt`
- `output/captions/skagway_white_pass_railway_001/skagway_white_pass_railway.bilingual.vtt`
- `output/manifests/manifest_skagway_white_pass_railway_001.csv`

The final WAV is mono, 48 kHz, 16-bit PCM, and 175.760 seconds long.
