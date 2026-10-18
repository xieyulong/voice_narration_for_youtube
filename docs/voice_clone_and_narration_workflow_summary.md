# User Workflow: Voice Clone To YouTube Narration

This document focuses on the actions the user must take. The AI-assisted
project handles the technical processing after each approval.

Voice cloning must only be performed with the speaker's permission.

## Start On A New Computer

This section assumes the person has an active monthly ChatGPT subscription and
has not yet installed Codex or prepared this project on the computer.

### 1. Install And Sign In To Codex

Choose one of these supported entry points:

- Install the [ChatGPT desktop app](https://chatgpt.com/download/) for macOS
  or Windows, sign in with the ChatGPT account, open Codex, and choose the
  project folder.
- Install the Codex CLI from a terminal with `npm install -g
  @openai/codex@latest`, run `codex`, and sign in with the ChatGPT account when
  prompted.

For normal interactive Codex use, follow the ChatGPT sign-in flow. Do not
confuse Codex with the separate OpenAI API CLI; an API key is not part of this
voice-cloning workflow unless the user separately chooses an API-based tool.

The official [Codex documentation](https://developers.openai.com/learn/codex)
and [OpenAI Developers plugin instructions](https://developers.openai.com/learn/developers-codex-plugin)
are the current references for installation and sign-in details.

### 2. Install Computer Prerequisites

On macOS, install the tools used by this repository:

    brew install git python@3.12 ffmpeg sox node
    brew install --cask audacity

Install DaVinci Resolve Studio separately from Blackmagic Design if it is not
already installed. A Windows user should install the Windows equivalents of
Git, Python 3.12, FFmpeg, SoX, Audacity, and DaVinci Resolve; the commands in
this document use macOS shell syntax.

### 3. Get The Repository

The public GitHub repository is:

    https://github.com/xieyulong/voice_narration_for_youtube

Clone it with:

    git clone https://github.com/xieyulong/voice_narration_for_youtube.git
    cd voice_narration_for_youtube

The repository is public, but the private voice samples, voice profile, local
Qwen3-TTS model, and generated WAV files are not included. They must be
transferred separately with the speaker's authorization.

Open this folder in Codex. The first request should be:

    Read AGENTS.md, README.md, docs/current_project_handoff.md, and
    docs/voice_clone_and_narration_workflow_summary.md. Report the setup
    status before changing anything.

### 4. Create The Local Python Environment

From the repository root, run:

    python3.12 -m venv .venv-qwen3-tts
    .venv-qwen3-tts/bin/python -m pip install --upgrade pip
    .venv-qwen3-tts/bin/python -m pip install -r requirements.txt

The current checkout documents `requirements.txt`, but that file is not
present in the repository at this time. Before a fresh installation, ask
Codex to inspect the existing environment or project history and restore a
reviewed dependency file. Do not guess package versions for a production
setup.

Verify the environment after dependencies are available:

    .venv-qwen3-tts/bin/python --version
    NUMBA_CACHE_DIR=/private/tmp/numba_cache \
    .venv-qwen3-tts/bin/python -c "import qwen_tts; print('qwen_tts import ok')"
    sox --version
    ffmpeg -version

### 5. Install Or Transfer The Local Model

The workflow uses the local Qwen3-TTS base model:

    models/qwen3-tts-12hz-0.6b-base

If the model is not transferred from an approved local backup, download the
corresponding model into that directory using the project's approved model
source and the local Hugging Face tooling:

    mkdir -p models
    .venv-qwen3-tts/bin/huggingface-cli download \
      Qwen/Qwen3-TTS-12Hz-0.6B-Base \
      --local-dir models/qwen3-tts-12hz-0.6b-base

Model files are large and are not stored in git.

### 6. Transfer The Private Voice Assets

With the speaker's authorization, copy the following private assets into the
matching paths:

    samples/raw/<raw_recording>.wav
    samples/clean/<clean_reference>.wav
    voice_profiles/<profile_name>/profile.yaml

The YAML profile must point to a clean WAV that exists on this computer and
must contain the exact transcript spoken in that WAV. Ask Codex to verify the
paths without exposing or committing the private audio.

### 7. Confirm The Setup Before Generating

Ask Codex to verify:

- The repository path and git status.
- The Python environment and `qwen_tts` import.
- The Qwen3-TTS model directory.
- The selected reference WAV and profile transcript.
- SoX, FFmpeg, and DaVinci Resolve availability.
- Whether generated output directories are ignored by git.

Only after this check should the user begin the recurring narration workflow
below.

## User Action Checklist

### 1. Provide A Voice Recording

Record the speaker reading a short, natural Chinese reference script.

The user should:

- Record in a quiet room.
- Keep the microphone position and speaking style consistent.
- Avoid music, echo, traffic, and other speakers.
- Provide the original recording as a WAV file.
- Provide the exact text spoken in the recording.

The AI will clean or prepare the reference file and place the private files in
the local sample folders. The user does not need to manually build a model.

### 2. Approve The Voice Reference

The user reviews and approves:

- The cleaned reference WAV.
- The exact reference transcript.
- The intended voice/style name, such as owner_calm.

The AI creates or updates the private Qwen3-TTS profile. A profile contains
the reference WAV path and the exact text spoken in that WAV.

The user-facing reference assets are stored locally under:

    samples/raw/
    samples/clean/
    voice_profiles/

These files are private and are not committed to git.

### 3. Provide The Narration Draft

The user provides the Chinese narration draft for the YouTube video.

The user should identify:

- The topic and intended video section.
- Any factual information that must be preserved.
- Preferred tone, such as calm, documentary, reflective, or energetic.
- Names, numbers, dates, and pronunciations that require special care.
- Any fixed wording that must not be changed.

The AI revises the draft for natural spoken Chinese and returns the proposed
narration and cue breakdown for approval.

### 4. Review The Cue Draft Before Audio Generation

Before synthesis, the user reviews the cue table supplied by the AI.

For every cue, the user checks:

- The Chinese text is accurate and natural.
- The Chinese text is exactly what should be spoken.
- The English translation preserves the meaning.
- English is first and Chinese is second.
- Each language should fit on one displayed line.
- Names, numbers, dates, and technical terms are correct.
- The cue order follows the intended narration.

The user approves the cue draft explicitly before audio generation begins.

The AI then writes the approved source files to:

    transcripts/scenes_<batch_name>.csv
    transcripts/subtitle_cues_<batch_name>.csv

### 5. Approve Generation Settings

Before the expensive generation step, the user confirms:

- Batch name.
- Voice profile and reference name.
- Model/reference voice to use.
- Whether the narration is continuous or contains intentional silence.
- Whether the output is one scene or multiple scenes.
- Whether an existing batch must be preserved by using a new batch name.

Recommended choices:

- Long continuous narration: chunked generation.
- Cue-specific timing or intentional silence: timed-cues generation.
- New revision: use a new batch name instead of overwriting an accepted batch.

The AI validates the CSV files and starts Qwen3-TTS only after approval.

### 6. Review The Generated Audio And Captions

The AI generates the final WAV, SRT, VTT, and manifest automatically. The user
reviews the deliverables, especially:

- The voice sounds like the approved speaker.
- The narration is complete and has no clipped cue endings.
- Cue transitions sound natural.
- Intended pauses are present or absent as requested.
- The SRT English line is first.
- The SRT Chinese line is second.
- Both lines fit visually without unwanted wrapping.
- The final duration is suitable for the video timeline.

The user should listen to the WAV and inspect the SRT in DaVinci Resolve. The
automated text-length check is useful, but it cannot prove visual subtitle fit.

### 7. Use The Files In DaVinci Resolve

The user imports these editor-facing files:

    output/audio_scenes/<batch_name>/<clip_name>.wav
    output/captions/<batch_name>/<clip_name>.bilingual.srt

The user then:

1. Places the WAV on the narration track.
2. Imports and places the SRT subtitle track.
3. Checks audio alignment with the video.
4. Checks subtitle position, font, safe area, and wrapping.
5. Makes any required editorial adjustments.
6. Renders the final YouTube video.

The optional VTT file can be used for web or platform caption workflows:

    output/captions/<batch_name>/<clip_name>.bilingual.vtt

The manifest is a reference file for paths, duration, cue count, and
generation mode:

    output/manifests/manifest_<batch_name>.csv

Internal chunk WAVs should not normally be imported into Resolve:

    output/audio_chunks/

### 8. Accept Or Request A Revision

The user either:

- Accepts the WAV/SRT package.
- Requests changes to the Chinese narration.
- Requests a translation correction.
- Requests different cue timing.
- Requests a new voice reference or style.

For a revision, the user should describe the exact cue, word, pause, or timing
problem. The AI creates a new batch name when the previous output should be
preserved.

### 9. Confirm The Handoff

When the package is accepted, the user asks the AI to:

- Verify the final files exist.
- Confirm WAV format and duration.
- Confirm subtitle cue count and timing.
- Update the project handoff documentation.
- Commit the tracked source CSVs and documentation if desired.

Generated media and private voice assets remain local unless the user chooses a
separate approved backup method.

## What The AI Automates

After user approval, the project automates most technical work:

- Creating the private voice profile YAML.
- Loading the local Qwen3-TTS model.
- Passing the reference WAV and transcript to Qwen3-TTS.
- Splitting long narration into internal generation chunks.
- Generating cloned-voice WAV audio.
- Concatenating internal chunks into one scene WAV.
- Generating bilingual SRT and VTT files.
- Measuring actual WAV duration.
- Retiming cues from measured audio when continuous timing is requested.
- Validating CSV structure, reviewed status, cue references, and cue length.
- Writing the delivery manifest.
- Running tests and checking file integrity.
- Updating the project handoff and session summary.

The user remains responsible for content accuracy, speaker authorization,
voice/reference approval, cue approval, final listening, subtitle appearance,
and final YouTube editorial decisions.

## File Formats

### Voice Reference

    WAV, private local reference recording

### Final Narration

    WAV
    Mono
    48,000 Hz
    16-bit PCM

### Captions

    SRT: primary Resolve subtitle file
    VTT: optional web/platform caption file

### Source And Handoff

    CSV: scene and subtitle source files
    CSV: delivery manifest
    MD: project instructions and session handoff

## Current Example

The latest completed package is:

    Ironman703_WashingtonTriCities_2026_09_20_continuous

It contains 81 bilingual cues and a continuous WAV with a measured duration of
00:08:14.480.
