# Project Prompts

Use these prompts to keep work in this project deliberate and easy to resume.

## Before Starting Work

```text
We are starting work in:
/Users/xieyulong2022/AI_Learn/Codex/voice_clone_NextStage

Before making changes:

1. Review AGENTS.md.
2. Review README.md.
3. Review docs/source_handoff.md.
4. Review docs/setup_and_private_assets.md.
5. Review docs/long_scene_workflow.md.
6. Check git status.
7. Verify whether private samples, model files, and the Qwen3-TTS environment exist.

Present:

- Repository Review
- Goal For This Session
- Execution Plan
- Risks / Assumptions

Do not modify files until I approve the plan.
```

## Before Implementing A Long-Scene Workflow Change

```text
The setup/design review is approved.

Implement only the approved scope.

Rules:

- Preserve the original voice_clone repo; do not modify it.
- Keep private samples, voice profiles, models, generated audio, captions,
  manifests, and package outputs out of git.
- Keep the workflow CSV-first and folder-based unless there is a clear reason
  to add complexity.
- Keep documentation synchronized with scripts and data fields.
- Do not commit, push, tag, or rewrite git history.

Run relevant checks and report the results.
```

## Before Generating Audio

```text
Before generating Qwen3-TTS audio:

1. Confirm the input CSV path.
2. Confirm the batch name.
3. Confirm the reference WAV path.
4. Confirm the exact reference text.
5. Confirm the model directory.
6. Confirm whether generation should be a dry run, one scene only, or the full batch.

Do not start synthesis until I approve those exact inputs.
```

## Before Pausing Or Exiting

```text
We are pausing or exiting this project.

Please wrap up the current state:

1. Check git status.
2. List files modified in this session.
3. Confirm whether private/generated files are ignored.
4. Summarize completed work.
5. Summarize remaining work.
6. Recommend the next prompt to use when returning.
7. Do not commit unless I explicitly ask.
```

## Return Prompt

```text
I am returning to:
/Users/xieyulong2022/AI_Learn/Codex/voice_clone_NextStage

Use docs/project_prompts.md and start with the "Before Starting Work" checklist.
```
