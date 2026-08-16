# WhitePassScenicTrainRide Redo: Step 1 Analysis

## Scope

Step 1 sampled the recreated 27-minute White Pass Scenic Train video at the
timing points in the supplied workbook, reviewed the five PNG references, and
drafted bilingual narration for every timing row. No voice synthesis was run.

## Inputs Checked

- Video: `/Users/xieyulong2022/Local_NoSync_Folder/2026_06_20_to_27_Alaska/Youtube/2026_June24_Skaway_part2_WhitePass.mov`
- Workbook: `materials_for_whitepass_train/Time_point_WhitePassScenicTrian.xlsx`
- PNG references: `materials_for_whitepass_train/PNG_001_IMG_9233.PNG` through
  `PNG_005_IMG_9239.PNG`
- Video duration: 1,635.833333 seconds, approximately 27:15.83.
- Video frame rate: 30 fps, 3840 x 2160.

## Timing Interpretation

The workbook timecodes use a fixed leading `01:` prefix. For this video, the
usable timeline position is the remaining `MM:SS:FF` portion. At 30 fps,
`01:03:30:30` normalizes to approximately 03:31.000 because frame 30 rolls
into the next second.

The workbook contains 28 timing rows, including the opening row. Rows marked
`double` were retained as separate outbound and return narration entries.

One source data issue remains visible in the original workbook: row 23 contains
`01;21:57:05` with a semicolon. The annotated copy preserves that original cell
unchanged; for analysis it was interpreted as approximately 21:57.17.

## Video Sampling Observations

- The opening shows the train and passengers in Skagway.
- The outbound sequence climbs from the Skagway rail yard through forest,
  mountain slopes, Glacier Gorge, Tunnel Mountain, Inspiration Point, Dead
  Horse Gulch, the Steel Bridge, the newer tunnel, and White Pass Summit.
- The return sequence visibly differs: the camera sees the Steel Bridge,
  Inspiration Point, Tunnel Mountain, Foy, Black Cross signage, Buchanan Rock,
  Clifton signage, Rocky Point, Denver, the maintenance shops, and Skagway from
  the descending train.
- The annotated narration uses different wording for repeated locations rather
  than treating them as one cue.

## Reference And Research Notes

The PNG material supports the mile markers and elevations, the descriptions of
the maintenance shops, Denver, Buchanan Rock, Bridal Veil Falls, Black Cross
Rock, Heney Station, Glacier Station, Tunnel Mountain, Inspiration Point, Dead
Horse Gulch, Steel Bridge, Tunnel, and White Pass Summit. It also provides
background on Skagway, the 1896 discovery, the 1897 news-driven stampede, and
the White Pass and Chilkoot Trails.

The main factual references used for the draft were:

- White Pass & Yukon Route history: <https://wpyr.com/history/>
- National Park Service, History of the White Pass Trail:
  <https://www.nps.gov/klgo/learn/historyculture/white-pass-history.htm>
- National Park Service, The Historic Chilkoot Trail:
  <https://home.nps.gov/klgo/learn/historyculture/historic-chilkoot-trail.htm>
- National Park Service, Skagway Historic District and White Pass:
  <https://home.nps.gov/places/skagway-historic-district-and-white-pass.htm>

Where the PNG, workbook, and sources use slightly different elevation values,
the narration uses approximate wording such as “接近三千英尺” rather than
introducing a conflicting precision claim.

## Step 1 Deliverable

The annotated workbook is:

`materials_for_whitepass_train/WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_timing_narration.xlsx`

Column E is `Bilingual Narration`. Each populated cell contains two logical
blocks:

1. English subtitle narration.
2. Chinese narration text.

The English text is a faithful translation of the Chinese narration, not a
shortened summary. The Chinese line is the candidate text for the later
cloned-voice narration. The workbook is a draft source for review before Step
2 batch generation.

For SRT/VTT delivery, long timing rows are split into multiple short bilingual
subtitle segments during Step 2 authoring. The subtitle CSV is therefore the
first generated artifact that contains multiple cues per timing row; the SRT is
not split after a long cue has already been created.
