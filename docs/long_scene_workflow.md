# Long Scene Narration Workflow

## Goal

Generate longer conversation-style Standard Chinese travel narration while
preserving the original Qwen3-TTS workflow and DaVinci Resolve delivery pattern.

The main output unit is a scene:

```text
one scene -> one final WAV -> one timed bilingual subtitle file
```

Internal chunks may exist for generation reliability, but they are not the
editor-facing unit.

## Design Principles

- Keep CSV as the durable authoring format.
- Keep generated audio and captions out of git.
- Preserve accepted scene outputs by using batch names.
- Separate spoken narration from subtitle cue timing.
- Treat subtitles as a presentation layer, not a different story.
- Allow one scene to be regenerated without overwriting other accepted scenes.

## Folder Model

```text
transcripts/
  scenes_<batch>.csv
  subtitle_cues_<batch>.csv

output/
  audio_scenes/<batch>/
  audio_chunks/<batch>/
  captions/<batch>/
  manifests/manifest_<batch>.csv
  packages/<batch>/
```

## Scene CSV

`transcripts/scenes_<batch>.csv` is the scene-level source of truth.

Recommended fields:

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

Field use:

- `conversation_id`: story arc or travel episode identifier.
- `section_id`: chapter or major video section.
- `scene_id`: stable scene identifier.
- `clip_name`: filesystem-safe output stem.
- `scene_title`: human-readable scene label.
- `start_time`, `end_time`: target DaVinci timeline slot.
- `speaker`: current voice or future multi-speaker label.
- `style`: calm, reflective, documentary, humorous, or similar.
- `language`: usually `zh`.
- `text`: full spoken Chinese narration for the whole scene.
- `notes`: planning notes not spoken aloud.
- `status`: `draft`, `reviewed`, `generated`, `accepted`, or `needs_regen`.

## Subtitle Cue CSV

`transcripts/subtitle_cues_<batch>.csv` controls readable subtitles for each
scene.

Recommended fields:

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

- Each cue displays at most two lines: English first, Chinese second.
- `subtitle_zh` should stay semantically faithful to the narration.
- `subtitle_en` should be a compact translation of the cue.
- Cue timing is relative to the scene WAV unless a script explicitly converts
  it to the full timeline.

## Generation Flow

1. Draft or edit `scenes_<batch>.csv`.
2. Review all scene `text` values before generation.
3. Draft or edit `subtitle_cues_<batch>.csv`.
4. Run a dry-run validator before synthesis.
5. Generate one final scene WAV per scene.
6. Write scene-level captions and a manifest.
7. Review actual `duration_seconds` against the target timeline slot.
8. Import WAV and SRT files into DaVinci Resolve Studio.

## Validation Command

Validate a scene CSV and its subtitle cue CSV before synthesis:

```bash
.venv-qwen3-tts/bin/python scripts/validate_long_scene_inputs.py \
  --scenes transcripts/scenes_<batch>.csv \
  --cues transcripts/subtitle_cues_<batch>.csv \
  --require-reviewed
```

For the first Skagway batch:

```bash
.venv-qwen3-tts/bin/python scripts/validate_long_scene_inputs.py \
  --scenes transcripts/scenes_skagway_white_pass_railway_001.csv \
  --cues transcripts/subtitle_cues_skagway_white_pass_railway_001.csv \
  --require-reviewed
```

The validator checks:

- required columns and required values;
- unique scene IDs and clip names;
- cue rows reference known scenes;
- reviewed scenes have subtitle cues;
- reviewed scenes have reviewed or accepted cues when `--require-reviewed` is
  used;
- optional start/end time pairs are both blank or both valid;
- subtitle lines are not unusually long;
- very long scene text is flagged as a chunking warning.

## Generator Commands

Preview the generation plan without writing files:

```bash
.venv-qwen3-tts/bin/python scripts/generate_long_scene_assets.py \
  --batch-name skagway_white_pass_railway_001 \
  --scenes transcripts/scenes_skagway_white_pass_railway_001.csv \
  --cues transcripts/subtitle_cues_skagway_white_pass_railway_001.csv \
  --dry-run
```

Write estimated-timing captions and a manifest without generating audio:

```bash
.venv-qwen3-tts/bin/python scripts/generate_long_scene_assets.py \
  --batch-name skagway_white_pass_railway_001 \
  --scenes transcripts/scenes_skagway_white_pass_railway_001.csv \
  --cues transcripts/subtitle_cues_skagway_white_pass_railway_001.csv
```

Generate Qwen3-TTS audio only after confirming the exact inputs:

```bash
NUMBA_CACHE_DIR=/private/tmp/numba_cache \
.venv-qwen3-tts/bin/python scripts/generate_long_scene_assets.py \
  --batch-name skagway_white_pass_railway_001 \
  --scenes transcripts/scenes_skagway_white_pass_railway_001.csv \
  --cues transcripts/subtitle_cues_skagway_white_pass_railway_001.csv \
  --profile-reference yulong_new_001 \
  --synthesize
```

Without `--synthesize`, the generator writes only scene-level bilingual SRT/VTT
files and a manifest using estimated narration duration. This is useful for
checking package shape before spending time on TTS generation.

## Single-WAV Scene Strategy

Preferred behavior:

```text
scene text -> Qwen3-TTS -> output/audio_scenes/<batch>/<clip_name>.wav
```

Fallback behavior for long or unstable scenes:

```text
scene text
    -> planned internal chunks
    -> Qwen3-TTS chunk WAVs
    -> SoX/FFmpeg concatenate
    -> one final scene WAV
```

The manifest should record whether a scene was generated as a single call or
assembled from internal chunks.

## Manifest

`output/manifests/manifest_<batch>.csv` should include:

```text
conversation_id
section_id
scene_id
clip_name
start_time
end_time
planned_duration_seconds
duration_seconds
generation_mode
speaker
style
audio_path
bilingual_srt_path
subtitle_cue_count
status
notes
```

## Long-Form Validation

Before synthesis, validate:

- required CSV fields are present;
- `scene_id` and `clip_name` are unique;
- reviewed scenes have non-empty text;
- subtitle cues exist for reviewed scenes;
- subtitle cues have English and Chinese text;
- cue order is stable;
- planned duration is present for timeline-bound scenes;
- estimated narration density is not obviously too high.

After synthesis, validate:

- one final WAV exists for each generated scene;
- WAV sample rate is 48 kHz for video editing;
- manifest duration matches the WAV;
- subtitle cue count matches the subtitle CSV;
- accepted outputs are not overwritten by a later experiment.

## Batch Naming

Use a distinct batch name for each experiment:

```text
alaska_long_scene_001
alaska_long_scene_001_regen_a
amtrak_conversation_001
```

Never overwrite accepted batches unless the user explicitly approves that.
