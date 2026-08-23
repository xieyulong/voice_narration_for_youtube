# WhitePassScenicTrainRide Part 005 Misc Insertions

## Purpose

This document records the additional user-supplied narration batch for the
first six minutes of the White Pass Scenic Train Ride redo.

Part 005 is an integrated supplemental overlay for the same
`WhitePassScenicTrainRide_Redo_2026_06_24_27m15s` video package documented in
`docs/ai_sessions/2026-08-15_WhitePassScenicTrainRide_redo_wrapup.md`. It
should be used with parts 001 through 004, not treated as a separate project or
replacement for the main four batches.

## Batch Name

```text
WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_005_mile_misc
```

## Source

The user supplied ten new Chinese narration insertions with `01:MM:SS:FF`
timecodes. The fixed leading `01:` prefix was interpreted the same way as the
previous WhitePass timing table: the usable video-relative position is the
remaining `MM:SS:FF` value at 30 fps.

The narration source was added to:

```text
scripts/build_whitepass_step1_annotation.py
```

as `MISC_NARRATIONS`, separate from the original 28 timing-table narrations.

## Generated Source CSVs

```text
transcripts/scenes_WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_005_mile_misc.csv
transcripts/subtitle_cues_WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_005_mile_misc.csv
```

The subtitle cue CSV contains 16 reviewed cues. The cues were authored as
short bilingual segments before SRT/VTT generation, following the revised
subtitle protocol:

- English first, Chinese second.
- English is a faithful translation of the Chinese cue.
- Each cue is short enough to fit the `--max-cue-chars 90` validation budget.
- If one English line would need to become a summary, split the Chinese cue
  into smaller natural segments instead of weakening the translation.
- Qwen3-TTS receives complete short Chinese utterances where practical.

## Generated Deliverables

Audio:

```text
output/audio_scenes/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_005_mile_misc/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_005_mile_misc.wav
```

Subtitles:

```text
output/captions/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_005_mile_misc/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_005_mile_misc.bilingual.srt
output/captions/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_005_mile_misc/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_005_mile_misc.bilingual.vtt
```

Manifest:

```text
output/manifests/manifest_WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_005_mile_misc.csv
```

## Generation Details

- Voice profile: `yulong_new_001`.
- Generation mode: `timed_cue_qwen3_tts`.
- Scene start: `00:00:00.000`.
- Scene end: `00:06:00.000`.
- Final WAV duration: `360.000` seconds.
- Final WAV format: mono, 48 kHz, 16-bit PCM.
- Subtitle cue count: 16.

The scene WAV starts at video time `00:00:00.000`, with silence before and
between timed cue insertions. Place the WAV at the start of the DaVinci Resolve
timeline for the intended cue positions to line up.

## Verification

- Part 005 scene and cue CSVs passed:

```bash
.venv-qwen3-tts/bin/python scripts/validate_long_scene_inputs.py \
  --scenes transcripts/scenes_WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_005_mile_misc.csv \
  --cues transcripts/subtitle_cues_WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_part_005_mile_misc.csv \
  --require-reviewed \
  --max-cue-chars 90 \
  --fail-on-cue-length
```

- `soxi` verified the final WAV as mono, 48 kHz, 16-bit PCM, 6:00.000.
- SRT, VTT, and manifest files exist.
- Cue duration review found small audio overlaps in the dense historical
  section:
  - `cue_009` exceeds the gap to `cue_010` by about 1.973 seconds.
  - `cue_010` exceeds the gap to `cue_011` by about 0.894 seconds.

These overlaps come from the close user-supplied start times around
`03:38-03:56` and the actual Qwen3-TTS spoken durations. Review this section in
DaVinci Resolve and decide whether to accept the overlap, shift later cue start
times, or shorten those two Chinese narration lines.
