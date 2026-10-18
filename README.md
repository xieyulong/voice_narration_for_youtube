# Voice Clone Next Stage

This project continues the original `voice_clone` workflow for longer
conversation-style Standard Chinese travel narration.

Public GitHub repository:

```text
https://github.com/xieyulong/voice_narration_for_youtube
```

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

## Latest Completed Task

The latest completed narration package is:

```text
Ironman703_WashingtonTriCities_2026_09_20_continuous
```

Start from `docs/current_project_handoff.md` for the active handoff and
`docs/ai_sessions/2026-09-21_Ironman703_WashingtonTriCities_continuous_summary.md`
for the task summary, generated deliverable paths, validation results, and
return context.

## Start Here

1. Read `docs/current_project_handoff.md` for the active task handoff.
2. Read `docs/source_handoff.md`.
3. Read `docs/setup_and_private_assets.md`.
4. Read `docs/long_scene_workflow.md`.
5. Read `docs/long_scene_generation_instructions.md`.
6. Use `docs/development_workflow/standard_project_prompts.md` before starting
   work, implementing approved changes, reviewing status, or pausing/exiting
   the project.
7. Read `docs/voice_clone_and_narration_workflow_summary.md` for the complete
   voice-reference, narration-generation, subtitle, and YouTube delivery flow.

For daily use, invoke one numbered prompt file directly, for example:

```text
Read docs/development_workflow/prompts/02_project_session_start_prompt.md and execute its content.
```

## Privacy

Raw samples, clean samples, voice profiles, models, generated audio, captions,
manifests, and delivery packages are ignored by git.
