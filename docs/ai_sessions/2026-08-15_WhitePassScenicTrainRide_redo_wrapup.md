# WhitePassScenicTrainRide Redo: Session Wrap-Up

## Purpose

This document is the handoff for the recreated Skagway White Pass Scenic Train
video narration task. Use it when exiting this session or returning to the
project for a similar video narration request.

## Completed Task

The source video was:

```text
/Users/xieyulong2022/Local_NoSync_Folder/2026_06_20_to_27_Alaska/Youtube/2026_June24_Skaway_part2_WhitePass.mov
```

Verified source duration: 1,635.833333 seconds, approximately 27:15.83.
Verified video format for sampling: 30 fps, 3840 x 2160.

The task was completed in two stages:

1. Sample the video at the timing points, read the supplied PNG references,
   research historical facts, and append bilingual narration to a copy of the
   timing table.
2. Generate Chinese cloned-voice narration and bilingual subtitle deliverables
   in manageable DaVinci Resolve batches.

## Source Analysis

The timing workbook was:

```text
materials_for_whitepass_train/Time_point_WhitePassScenicTrian.xlsx
```

The five PNG references were read from the same materials folder. They provided
milestone names, mile markers, elevations, route descriptions, Skagway history,
Klondike Gold Rush context, and White Pass and Chilkoot Trail background.

The primary online references used were:

- White Pass & Yukon Route history: https://wpyr.com/history/
- NPS History of the White Pass Trail:
  https://www.nps.gov/klgo/learn/historyculture/white-pass-history.htm
- NPS Historic Chilkoot Trail:
  https://home.nps.gov/klgo/learn/historyculture/historic-chilkoot-trail.htm
- NPS Skagway Historic District and White Pass:
  https://home.nps.gov/places/skagway-historic-district-and-white-pass.htm

## Timing Rules

The workbook contains 28 timing rows, including the opening row. A `double`
marker means the location appears during both the outbound and return journeys.
Those appearances were kept as separate narration cues with different wording.

The workbook uses a fixed leading `01:` timecode prefix. The usable timeline is
the remaining `MM:SS:FF` portion. At 30 fps, frame 30 rolls into the next
second. For example, `01:03:30:30` becomes approximately `03:31.000`.

The original workbook contains one malformed timecode, `01;21:57:05`, with a
semicolon. The original cell was preserved in the annotated workbook. The Step
2 CSV timing data interprets it as approximately `21:57.167`.

## Step 1 Deliverable

Annotated timing workbook:

```text
materials_for_whitepass_train/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_timing_narration.xlsx
```

Column E is `Bilingual Narration`. Each cell contains faithful English
translation text and the Chinese narration text:

1. English subtitle text translated from the Chinese narration.
2. Chinese narration text for the cloned voice.

The original timing workbook was not overwritten.

Step 1 analysis notes:

```text
docs/ai_sessions/2026-08-15_WhitePassScenicTrainRide_step1_analysis.md
```

## Step 2 Batch Structure

The overall naming string is:

```text
WhitePassScenicTrainRide_Redo_2026_06_24_27m15s
```

Four timed-cue batches were created:

```text
WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_001_mile_00_00_to_08_59
WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_002_mile_08_59_to_16_04
WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_003_mile_16_04_to_21_57
WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_004_mile_21_57_to_27_15
```

Each batch has:

- A reviewed scene CSV in `transcripts/`.
- A reviewed subtitle-cue CSV in `transcripts/`. One source timing row can
  produce multiple short subtitle cue rows.
- A scene-level Chinese WAV in `output/audio_scenes/<batch>/`.
- A bilingual SRT in `output/captions/<batch>/`.
- A bilingual VTT in `output/captions/<batch>/`.
- A DaVinci Resolve manifest in `output/manifests/`.

The exact scene and cue CSVs use the same batch names shown above.

## Scripts Created

Two reusable helper scripts were created for this task:

### `scripts/build_whitepass_step1_annotation.py`

Creates a new annotated XLSX copy from the supplied timing workbook. It keeps
the original timing, location, and `double` cells, adds the `Bilingual
Narration` column, and writes concise English plus Chinese text into each
timing row. It also applies a wrapped bilingual-cell style for Excel review.

Run from the repository root with:

```bash
.venv-qwen3-tts/bin/python scripts/build_whitepass_step1_annotation.py
```

### `scripts/build_whitepass_step2_csvs.py`

Converts the reviewed Step 1 narration draft into four reviewed scene CSVs and
four reviewed subtitle-cue CSVs. It normalizes the workbook timecodes to
video-relative timings, preserves separate outbound/return cues, and assigns
the four batch windows.

Run from the repository root with:

```bash
.venv-qwen3-tts/bin/python scripts/build_whitepass_step2_csvs.py
```

The main generator used for each batch was:

```bash
NUMBA_CACHE_DIR=/private/tmp/numba_cache \
.venv-qwen3-tts/bin/python scripts/generate_long_scene_assets.py \
  --batch-name <batch> \
  --scenes transcripts/scenes_<batch>.csv \
  --cues transcripts/subtitle_cues_<batch>.csv \
  --profile-reference yulong_new_001 \
  --generation-mode timed-cues \
  --synthesize \
  --overwrite
```

`timed-cues` was used so that each Chinese narration cue is spoken at its
specified video-relative start time and silence is preserved between cues.
For caption-only revisions against accepted WAVs, rerun this command without
`--synthesize`; this rewrites the SRT/VTT and manifest but does not overwrite
the WAV.

## Generation Details

- Voice profile: `yulong_new_001`.
- Clean reference: `samples/clean/sample_yulong_new_001_clean.wav`.
- Model: `models/qwen3-tts-12hz-0.6b-base`.
- Generation mode: `timed_cue_qwen3_tts`.
- Final WAV format: mono, 48 kHz, 16-bit PCM.
- Subtitle format: English first, Chinese second, exactly two logical lines.
- English subtitles are faithful translations of the Chinese cue segments, not
  shortened summaries.
- Long timing rows are split into multiple short subtitle cue rows before
  SRT/VTT generation.
- Numba cache: `NUMBA_CACHE_DIR=/private/tmp/numba_cache`.

Generated WAV durations:

| Batch | Duration | Cues |
| --- | ---: | ---: |
| Part 001 | 539.400 seconds | 21 |
| Part 002 | 425.033 seconds | 33 |
| Part 003 | 352.733 seconds | 16 |
| Part 004 | 318.667 seconds | 33 |
| Total | 1,635.833 seconds | 103 |

## DaVinci Resolve Upload Files

Import these four WAV files as audio and place each one at the matching start
time shown in its filename. Import the matching bilingual SRT file as the
subtitle track.

### Part 001: 00:00 to 08:59

Audio:

```text
output/audio_scenes/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_001_mile_00_00_to_08_59/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_001_mile_00_00_to_08_59.wav
```

Subtitles:

```text
output/captions/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_001_mile_00_00_to_08_59/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_001_mile_00_00_to_08_59.bilingual.srt
```

### Part 002: 08:59 to 16:04

Audio:

```text
output/audio_scenes/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_002_mile_08_59_to_16_04/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_002_mile_08_59_to_16_04.wav
```

Subtitles:

```text
output/captions/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_002_mile_08_59_to_16_04/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_002_mile_08_59_to_16_04.bilingual.srt
```

### Part 003: 16:04 to 21:57

Audio:

```text
output/audio_scenes/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_003_mile_16_04_to_21_57/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_003_mile_16_04_to_21_57.wav
```

Subtitles:

```text
output/captions/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_003_mile_16_04_to_21_57/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_003_mile_16_04_to_21_57.bilingual.srt
```

### Part 004: 21:57 to 27:15

Audio:

```text
output/audio_scenes/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_004_mile_21_57_to_27_15/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_004_mile_21_57_to_27_15.wav
```

Subtitles:

```text
output/captions/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_004_mile_21_57_to_27_15/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_004_mile_21_57_to_27_15.bilingual.srt
```

The corresponding `.bilingual.vtt` files are in the same caption folders and
can be used for alternate subtitle workflows or review. The manifest files are
for timing and verification; they are not required for the basic Resolve
import.

## Verification Completed

- All four scene and cue CSV pairs passed `validate_long_scene_inputs.py
  --require-reviewed --max-cue-chars 90 --fail-on-cue-length`.
- All generated WAV files were checked with `soxi`.
- All WAV files are mono, 48 kHz, 16-bit PCM.
- All four SRT files, VTT files, and manifests exist.
- Manifest duration total equals the source video duration.
- Both helper scripts passed Python compilation with a writable cache prefix.
- `git diff --check` passed.

## Files Created In This Session

Source-side files currently awaiting a Git decision:

```text
docs/long_scene_workflow.md
docs/long_scene_generation_instructions.md
docs/ai_sessions/2026-08-15_WhitePassScenicTrainRide_step1_analysis.md
docs/ai_sessions/2026-08-15_WhitePassScenicTrainRide_redo_wrapup.md
scripts/generate_long_scene_assets.py
scripts/validate_long_scene_inputs.py
scripts/build_whitepass_step1_annotation.py
scripts/build_whitepass_step2_csvs.py
tests/test_validate_long_scene_inputs.py
materials_for_whitepass_train/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_timing_narration.xlsx
transcripts/scenes_WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_*.csv
transcripts/subtitle_cues_WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_*.csv
```

Generated audio, captions, and manifests are normally ignored by Git.

An existing file named `Time_point_WhitePassScenicTrian_archived.xlsx` was
observed in the worktree and was not created or modified by this task. Preserve
it unless the user explicitly decides otherwise.

## Restart Workflow For The Next Similar Task

1. Start in `/Users/xieyulong2022/AI_Learn/Codex/voice_clone_NextStage`.
2. Read `AGENTS.md`, `README.md`, `docs/source_handoff.md`,
   `docs/long_scene_workflow.md`, and this wrap-up document.
3. Check `git status --short` and preserve unrelated user files.
4. Confirm the new video path, duration, timing workbook, screenshots, and
   desired default naming string.
5. Inspect the timing workbook and identify every `double` outbound/return row.
6. Sample the video at the normalized timing points.
7. Read the supplied PNG or screenshot references.
8. Verify historical claims with primary or authoritative sources.
9. Create a new annotated workbook without overwriting the source workbook.
10. Split each timing row into short bilingual subtitle segments before
    generating `subtitle_cues_<batch>.csv`.
11. Split the narration into manageable batches using the
    `WhitePassScenicTrainRide` naming convention.
12. Create reviewed scene and subtitle-cue CSVs.
13. Run the validator before synthesis.
14. Generate timed-cue WAV, SRT, VTT, and manifest outputs batch by batch.
15. Verify WAV format, durations, cue counts, caption files, and manifests.
16. Do not commit unless the user explicitly requests a commit. When approved,
    stage only the relevant source documents and CSVs; leave generated media and
    unrelated files untouched.

## Next Recommended Action

The current WhitePass redo deliverables are complete. The next action should be
reviewing the revised bilingual SRT files with the already accepted WAV batches
in DaVinci Resolve. Any wording or timing corrections should be made in the
source CSV/workbook first, then only the affected caption batch should be
regenerated without `--synthesize`.
