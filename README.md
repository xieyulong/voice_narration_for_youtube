# Voice Clone Next Stage

This project continues the original `voice_clone` workflow for longer
conversation-style Standard Chinese travel narration.

The goal is to preserve the reliable local Qwen3-TTS path while redesigning the
data model and generation flow around scene-level narration:

```text
scene-level reviewed narration CSV
    -> one long WAV per scene
    -> timed bilingual subtitle cues
    -> manifest for DaVinci Resolve Studio
```

The project remains destination-independent. Alaska or Amtrak material is only
input content, not an architectural assumption.

## Current Scope

- Local Qwen3-TTS workflow.
- CSV-first source data.
- Long single-WAV scene delivery.
- Bilingual subtitles as a presentation layer.
- DaVinci Resolve-ready audio and subtitle outputs.

## Start Here

1. Read `docs/source_handoff.md`.
2. Read `docs/setup_and_private_assets.md`.
3. Read `docs/long_scene_workflow.md`.
4. Use `docs/project_prompts.md` before starting work and before pausing or
   exiting the project.

## Privacy

Raw samples, clean samples, voice profiles, models, generated audio, captions,
manifests, and delivery packages are ignored by git.
