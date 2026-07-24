# Setup And Private Assets

## Purpose

This document records the local setup needed for the long-scene Qwen3-TTS
workflow and how private files should be handled in this new project.

## Machine Tools

Install Homebrew if needed:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Install command-line tools:

```bash
brew install python@3.12 ffmpeg sox
```

Install Audacity:

```bash
brew install --cask audacity
```

DaVinci Resolve Studio is usually installed from Blackmagic Design rather than
managed by this repository. Confirm it exists under `/Applications`.

## Python Environment

Create the Qwen3-TTS environment from the repository root:

```bash
python3.12 -m venv .venv-qwen3-tts
.venv-qwen3-tts/bin/python -m pip install --upgrade pip
.venv-qwen3-tts/bin/python -m pip install -r requirements.txt
```

Verify:

```bash
.venv-qwen3-tts/bin/python --version
NUMBA_CACHE_DIR=/private/tmp/numba_cache .venv-qwen3-tts/bin/python -c "import qwen_tts; print('qwen_tts import ok')"
sox --version
ffmpeg -version
```

The `NUMBA_CACHE_DIR` setting avoids a known local import failure where Numba
tries to cache functions inside package paths that are not writable in the
current execution context.

The FlashAttention warning is acceptable for local CPU testing:

```text
Warning: flash-attn is not installed. Will only run the manual PyTorch version.
```

Do not install `flash-attn` on this Mac unless a separate GPU/hardware review
shows it is appropriate.

## Model Setup

The old project used:

```text
models/qwen3-tts-12hz-0.6b-base
```

The corresponding Hugging Face model is:

```text
Qwen/Qwen3-TTS-12Hz-0.6B-Base
```

Fresh download pattern:

```bash
mkdir -p models
.venv-qwen3-tts/bin/huggingface-cli download \
  Qwen/Qwen3-TTS-12Hz-0.6B-Base \
  --local-dir models/qwen3-tts-12hz-0.6b-base
```

Model files are ignored by git.

## Private Voice Samples

Private samples belong in:

```text
samples/raw/
samples/clean/
```

These folders are ignored by git except for `.gitkeep` placeholders.

Current Yulong clean reference from the original project:

```text
samples/clean/sample_yulong_new_001_clean.wav
```

Reference text used for the recent Yulong batches:

```text
今天的旅程从清晨开始，空气很凉，路上的人也不多。我们沿着海边慢慢往前走，远处的云层被阳光染成了很柔和的颜色。这一刻的风景并不喧闹，却让人很容易安静下来。如果把这一天剪成一段视频，我希望它听起来像一次轻松而真实的回忆。
```

If private files are missing, recreate the voice profile by recording a fresh
WAV in Audacity, saving the raw file under `samples/raw/`, exporting a clean WAV
under `samples/clean/`, and preserving the exact spoken text with the generation
command.

## Private Voice Profiles

Active local voice profiles belong in:

```text
voice_profiles/
```

These files are ignored by git because they can reference private voice samples
and preserve exact reference text.

The current copied local profile is:

```text
voice_profiles/owner_calm/profile.yaml
```

The active default reference should be the Yulong clean sample:

```text
name: yulong_new_001
audio: samples/clean/sample_yulong_new_001_clean.wav
```

The corresponding raw recording copied from the old project is:

```text
samples/raw/Sample_YulongXie_New_001.wav
```

Use the clean WAV for Qwen3-TTS generation. The raw WAV is source material for
future cleaning or comparison.

The same profile may also keep alternate calm references:

```text
samples/clean/calm_001.wav
samples/clean/calm_002.wav
samples/clean/calm_003.wav
```

Use this profile for local Qwen3-TTS tests only after confirming the referenced
WAV files exist in the current project.

## What Not To Copy From The Old Project

Do not copy old generated outputs by default:

```text
output/audio_clips/
output/captions/
output/manifest*.csv
```

Do not copy old models or voice profiles unless the user explicitly approves
that scope. The current approval only covers raw and clean voice sample files.
