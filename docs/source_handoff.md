# Source Handoff

## Purpose

This project continues the original local `voice_clone` project, but it should
not modify that repository unless the user explicitly asks.

Original repository:

```text
/Users/xieyulong2022/AI_Learn/Codex/voice_clone
```

Current repository:

```text
/Users/xieyulong2022/AI_Learn/Codex/voice_clone_NextStage
```

## Primary Handoff

Read this source file first when refreshing context:

```text
/Users/xieyulong2022/AI_Learn/Codex/voice_clone/docs/current_project_status_and_annotation_workflow.md
```

It records:

- the current short-segment workflow;
- the Qwen3-TTS command pattern;
- the current Yulong reference WAV path and exact reference text;
- long-narration target behavior;
- recommended long-form CSV fields;
- DaVinci Resolve delivery pattern;
- known limitations and remaining work.

## Required Original Docs

Review these files before changing the next-stage workflow:

```text
/Users/xieyulong2022/AI_Learn/Codex/voice_clone/README.md
/Users/xieyulong2022/AI_Learn/Codex/voice_clone/docs/environment_plan.md
/Users/xieyulong2022/AI_Learn/Codex/voice_clone/docs/workflow.md
/Users/xieyulong2022/AI_Learn/Codex/voice_clone/docs/qwen3_tts_voice_clone_generation_workflow.md
/Users/xieyulong2022/AI_Learn/Codex/voice_clone/docs/voice_clone_plan.md
/Users/xieyulong2022/AI_Learn/Codex/voice_clone/docs/app_list.md
/Users/xieyulong2022/AI_Learn/Codex/voice_clone/docs/davinci_resolve_workflow.md
/Users/xieyulong2022/AI_Learn/Codex/voice_clone/requirements.txt
```

## Assets Copied To This Project

The private raw and clean voice samples from the original project may be copied
into this project when approved by the user:

```text
samples/raw/
samples/clean/
```

These files are ignored by git.

Do not copy generated output files from the old project unless explicitly
approved.

## Current Design Direction

Preserve the proven Qwen3-TTS reference-audio flow, but redesign the durable
inputs around long scene-level narration:

```text
one scene
    -> one reviewed long narration record
    -> optional internal generation chunks
    -> one final scene WAV
    -> multiple subtitle cue records
```
