# WhitePassScenicTrainRide Redo Workflow

## Purpose

This document records the agreed workflow for rebuilding the narration for the
recreated Skagway White Pass Scenic Train video. It is a guidance document for
this effort and future continuation batches.

## Video

Source video:

```text
/Users/xieyulong2022/Local_NoSync_Folder/2026_06_20_to_27_Alaska/Youtube/2026_June24_Skaway_part2_WhitePass.mov
```

Target duration: 27 minutes 15 seconds.

## Source Materials

The narration will be developed from four source groups:

1. Timing table:
   `materials_for_whitepass_train/Time_point_WhitePassScenicTrian.xlsx`
2. PNG reference images in `materials_for_whitepass_train/`.
3. The visual content at each timing point in the recreated video.
4. Carefully verified online sources for historical and factual details.

The PNG references provide milestone names, mile markers, elevations, route
history, Skagway background, the Klondike Gold Rush, the White Pass and Chilkoot
Trails, and related historical context.

## Timing And Duplicate Locations

The timing table is the synchronization source of truth. The final column may
contain `double`. This means the same general location appears twice in the
video, once during the outbound journey and once during the return journey.

Those appearances must remain separate narration cues. They should use
different wording or viewpoint appropriate to the visible footage, even when
the location name is the same.

Recommended cue identity pattern:

```text
<location>_outbound
<location>_return
```

The duplicate marker must never be collapsed into one narration entry.

## Narration And Subtitle Rules

- The voice narration is Chinese only.
- The active cloned voice is the owner's Standard Chinese voice profile,
  `yulong_new_001`.
- Subtitle cues are bilingual and contain exactly two displayed lines:
  English first, Chinese second.
- English subtitles must be a concise, faithful translation of the Chinese
  narration.
- Chinese subtitle text must match the spoken Chinese for timed-cue synthesis.
- Subtitle cues should be short enough to read comfortably and must stay within
  their assigned timing windows.
- Narration should use a calm, natural, documentary-style travel tone.

## File And Folder Naming

All files and folders for this redo effort should include the default string:

```text
WhitePassScenicTrainRide
```

Proposed batch name:

```text
WhitePassScenicTrainRide_Redo_2026_06_24_27m15s
```

Expected source files:

```text
transcripts/scenes_WhitePassScenicTrainRide_Redo_2026_06_24_27m15s.csv
transcripts/subtitle_cues_WhitePassScenicTrainRide_Redo_2026_06_24_27m15s.csv
```

Generated outputs should use the same batch name under the established
audio, captions, and manifest folders.

## Production Stages

1. Read and analyze every timing-table row.
2. Preserve every `double` location as separate outbound and return entries.
3. Match timing points to the corresponding video footage.
4. Use the PNG references to develop location-specific narration.
5. Verify historical and factual claims with authoritative online sources.
6. Draft the Chinese narration and bilingual subtitle cues.
7. Review cue length, timing, wording, and subtitle formatting.
8. Validate the reviewed scene and cue CSV files.
9. Generate Chinese WAV narration with the cloned voice.
10. Generate bilingual SRT, VTT, and a DaVinci Resolve manifest.
11. Verify WAV format, actual duration, cue count, and output paths.

## DaVinci Resolve Deliverables

The final delivery consists of:

- Scene-level Chinese WAV narration.
- Bilingual SRT subtitles.
- Bilingual VTT subtitles when useful for review or alternate import.
- Manifest containing timing, duration, cue count, and generation mode.

Generated audio, captions, manifests, private voice samples, voice profiles,
and model files are local workflow artifacts and should remain ignored by Git
unless explicitly requested otherwise.

## Approval Gates

Before narration generation, the source CSV text, cue wording, timing, and
voice reference must be confirmed. Drafting and factual research may proceed
first, but Qwen3-TTS synthesis should begin only after the reviewed inputs are
ready.

No new CSVs or audio files have been generated as part of recording this
understanding document.
