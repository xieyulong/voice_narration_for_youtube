# Long Scene Generation Instructions

## Purpose

This document explains how the long-scene narration workflow was developed and
how to use it to create DaVinci Resolve-ready narration files.

It is the practical handoff for future work in this project.

## What Was Built

The original `voice_clone` project generated one WAV file per short transcript
row. This project extends that workflow for longer scene-level narration:

```text
scene CSV + subtitle cue CSV
    -> validate inputs
    -> generate internal Qwen3-TTS chunk WAVs
    -> concatenate chunks into one scene WAV
    -> generate bilingual SRT/VTT subtitles
    -> write a DaVinci Resolve manifest
```

The main design decision is that the editor-facing unit is one scene, even when
the generator uses smaller internal chunks.

## Why Chunked Generation Is Used

The first Skagway narration is about three minutes long. A single full-scene
Qwen3-TTS call on the local CPU setup was too slow and produced no WAV after
several minutes.

The implemented solution is chunked synthesis:

1. Split the scene narration into sentence-aware chunks.
2. Generate one temporary WAV per chunk.
3. Use SoX to concatenate the chunk WAVs.
4. Deliver one final scene-level WAV for DaVinci Resolve.

The manifest records this as:

```text
generation_mode: chunked_qwen3_tts
```

## Important Files

Source and documentation files tracked by git:

```text
scripts/validate_long_scene_inputs.py
scripts/generate_long_scene_assets.py
tests/test_validate_long_scene_inputs.py
tests/test_generate_long_scene_assets.py
docs/long_scene_workflow.md
docs/setup_and_private_assets.md
docs/long_scene_generation_instructions.md
```

Private or generated files ignored by git:

```text
.venv-qwen3-tts/
models/
samples/raw/
samples/clean/
voice_profiles/owner_calm/profile.yaml
output/audio_chunks/
output/audio_scenes/
output/captions/
output/manifests/
```

## What You Need To Prepare

For each new long narration batch, prepare two CSV files.

For timing-table based videos, one source timing row is a narration block, not
necessarily one subtitle cue. Draft the Chinese narration and then split it
immediately into short bilingual segments. The Step 2 source should emit one
subtitle cue row per segment so long subtitle cues are never created in the
first place.

For final delivery, every reviewed subtitle cue must pass the validator with
`--max-cue-chars 90 --fail-on-cue-length`. This is the automated source-text
budget used to keep each English and Chinese line short enough for DaVinci
Resolve. It is not a substitute for final visual review in Resolve, because
font, subtitle style, resolution, and safe-area settings determine actual
wrapping.

### Scene CSV

Path pattern:

```text
transcripts/scenes_<batch_name>.csv
```

Required columns:

```text
conversation_id
section_id
scene_id
clip_name
scene_title
start_time
end_time
speaker
style
language
text
notes
status
```

The most important field is `text`. It contains the full Chinese narration that
Qwen3-TTS will speak.

Use:

```text
status: reviewed
```

when the narration text is ready for generation.

### Subtitle Cue CSV

Path pattern:

```text
transcripts/subtitle_cues_<batch_name>.csv
```

Required columns:

```text
conversation_id
scene_id
cue_id
cue_start
cue_end
subtitle_zh
subtitle_en
notes
status
```

Rules:

- Keep each cue to two displayed lines: English first, Chinese second.
- Keep each cue short enough that each language usually fits on one line in
  DaVinci Resolve.
- Enforce the source-text limit with `--max-cue-chars 90
  --fail-on-cue-length` before generation or delivery.
- Make `subtitle_en` a faithful translation of `subtitle_zh`; do not use a
  shortened English summary.
- If the English line would become a summary to fit the budget, split the
  Chinese narration into shorter natural cue segments instead.
- If one timing row contains several meaning units, create several subtitle cue
  rows inside that timing window before generating SRT/VTT files.
- Leave `cue_start` and `cue_end` blank if exact timing is not known yet.
- Use `status: reviewed` when the cue wording is approved.
- The generator will distribute blank cue timing evenly across the actual WAV
  duration.

## Voice Reference

The active reference for this workflow is:

```text
voice_profiles/owner_calm/profile.yaml
profile reference: yulong_new_001
clean WAV: samples/clean/sample_yulong_new_001_clean.wav
raw source WAV: samples/raw/Sample_YulongXie_New_001.wav
```

Use the clean WAV for Qwen3-TTS generation. The raw WAV is preserved only as
source material.

## Commands

Run all commands from the project root:

```bash
cd /Users/xieyulong2022/AI_Learn/Codex/voice_clone_NextStage
```

### 1. Validate Input CSVs

For the current Skagway batch:

```bash
.venv-qwen3-tts/bin/python scripts/validate_long_scene_inputs.py \
  --scenes transcripts/scenes_skagway_white_pass_railway_001.csv \
  --cues transcripts/subtitle_cues_skagway_white_pass_railway_001.csv \
  --require-reviewed \
  --max-cue-chars 90 \
  --fail-on-cue-length
```

Expected result:

```text
Validation passed
```

### 2. Preview The Generation Plan

This does not write files:

```bash
.venv-qwen3-tts/bin/python scripts/generate_long_scene_assets.py \
  --batch-name skagway_white_pass_railway_001 \
  --scenes transcripts/scenes_skagway_white_pass_railway_001.csv \
  --cues transcripts/subtitle_cues_skagway_white_pass_railway_001.csv \
  --profile-reference yulong_new_001 \
  --generation-mode chunked \
  --dry-run
```

### 3. Generate The Final Long Scene Files

This generates chunk WAVs, one final scene WAV, bilingual captions, and a
manifest:

```bash
NUMBA_CACHE_DIR=/private/tmp/numba_cache \
.venv-qwen3-tts/bin/python scripts/generate_long_scene_assets.py \
  --batch-name skagway_white_pass_railway_001 \
  --scenes transcripts/scenes_skagway_white_pass_railway_001.csv \
  --cues transcripts/subtitle_cues_skagway_white_pass_railway_001.csv \
  --profile-reference yulong_new_001 \
  --generation-mode chunked \
  --synthesize
```

Use `--overwrite` only when regenerating an existing batch:

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

## Files To Load Into DaVinci Resolve

For the current successful Skagway batch, load these files:

Audio:

```text
output/audio_scenes/skagway_white_pass_railway_001/skagway_white_pass_railway.wav
```

Bilingual subtitle:

```text
output/captions/skagway_white_pass_railway_001/skagway_white_pass_railway.bilingual.srt
```

Optional VTT subtitle:

```text
output/captions/skagway_white_pass_railway_001/skagway_white_pass_railway.bilingual.vtt
```

Placement/reference manifest:

```text
output/manifests/manifest_skagway_white_pass_railway_001.csv
```

Internal chunk WAVs are for troubleshooting only:

```text
output/audio_chunks/skagway_white_pass_railway_001/skagway_white_pass_railway/
```

Do not load the chunk WAVs into DaVinci Resolve unless you are debugging a
specific section.

## Current Successful Output

The first accepted long-scene output is:

```text
batch_name: skagway_white_pass_railway_001
generation_mode: chunked_qwen3_tts
duration_seconds: 175.760
subtitle_cue_count: 20
```

Final WAV properties:

```text
Channels: mono
Sample Rate: 48000
Precision: 16-bit
Duration: 00:02:55.76
Encoding: 16-bit Signed Integer PCM
```

## Future Enhancement Notes

Useful next improvements:

- Add a script option to assign subtitle timing based on narration chunk
  boundaries instead of even distribution.
- Add a package command that copies the final WAV, SRT, and manifest into
  `output/packages/<batch_name>/`.
- Add a review report that compares scene text length, generated duration, cue
  count, and average subtitle duration.
- Add support for multiple scenes in one batch while still allowing one scene to
  be regenerated independently.
- Add optional loudness normalization after concatenation.

Keep the same rule for future changes: source CSVs and documentation are
tracked; generated media and private voice assets remain local and ignored.
