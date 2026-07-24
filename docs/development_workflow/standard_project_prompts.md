# Standard Project Prompt Templates

## Purpose

Use these prompt templates in Codex projects to keep sessions consistent,
auditable, and easy to resume.

Each prompt requires the assistant to end the response with a marker. The marker
shows which prompt was answered.

## Prompt Index

| Prompt | When To Use | Persisted Output Record | Response Marker |
| --- | --- | --- | --- |
| Project Status Review | Ask what project this is, what is complete, and what is waiting | Optional: `docs/ai_sessions/YYYY-MM-DD_project_status_review.md` | `[[PROMPT:PROJECT_STATUS_REVIEW]]` |
| Start Project Session | Begin a new work session before edits | `docs/ai_sessions/YYYY-MM-DD_session_start_review.md` | `[[PROMPT:PROJECT_SESSION_START]]` |
| Implement Approved Work | Execute an approved task | `docs/ai_sessions/YYYY-MM-DD_<short_name>_implementation_summary.md` | `[[PROMPT:PROJECT_IMPLEMENTATION]]` |
| Wrap Up Or Pause Session | Pause, exit, or hand off current state | Optional: `docs/ai_sessions/YYYY-MM-DD_session_wrap_up.md` | `[[PROMPT:PROJECT_SESSION_WRAP_UP]]` |

Persisted output records should summarize useful state. Do not paste the full
chat transcript.

## Executable Prompt Files

For day-to-day use, ask Codex to read and execute one of these files:

```text
docs/development_workflow/prompts/01_project_status_review_prompt.md
docs/development_workflow/prompts/02_project_session_start_prompt.md
docs/development_workflow/prompts/03_project_implementation_prompt.md
docs/development_workflow/prompts/04_project_session_wrap_up_prompt.md
```

Example:

```text
Read docs/development_workflow/prompts/02_project_session_start_prompt.md and execute its content.
```

## Prompt 1: Project Status Review

Use this when asking "which project is this?", "what is the status?", or "what
are you waiting from me?"

```text
Please perform a project status review.

Before making any repository changes:

1. Confirm the current project folder and Git repository.
2. Read AGENTS.md, README.md, and the key workflow docs.
3. Check git status, latest commits, ignored local assets, and generated outputs.
4. Identify the current project goal.
5. Identify what has been completed.
6. Identify what remains.
7. Identify exactly what input, approval, or decision is needed from me.

Present:

- Project
- Goal
- Current Status
- Completed Work
- Uncommitted Or Ignored Local Work
- What Is Needed From Me
- Recommended Next Step

Do not modify source code, generated outputs, configuration, prompts, or
documentation unless I explicitly approve.

End your response with this exact marker:

[[PROMPT:PROJECT_STATUS_REVIEW]]
```

## Prompt 2: Start Project Session

Use this before starting a new session of work in a project.

```text
We are starting a project session.

Before making any repository changes:

1. Confirm the current project folder and Git repository.
2. Read AGENTS.md.
3. Read README.md.
4. Read docs/development_workflow/standard_project_prompts.md.
5. Read the project-specific workflow and setup docs.
6. Check git status and latest commits.
7. Verify required local prerequisites for the requested task.
8. Review relevant previous session notes under docs/ai_sessions/.

Present:

- Project Identity
- Session Goal
- Current Repository Status
- Relevant Context Reviewed
- Execution Plan
- Risks / Assumptions
- Exact Approval Needed

Do not modify source code, generated outputs, configuration, prompts, or
documentation during this review, except for a required session-start record if
the project protocol asks for one.

Wait for my approval before implementation.

End your response with this exact marker:

[[PROMPT:PROJECT_SESSION_START]]
```

## Prompt 3: Implement Approved Work

Use this after approving a specific plan.

```text
The project session plan has been approved.

Implement only the approved scope.

Before editing files, restate:

- approved objective;
- in-scope files or outputs;
- explicitly deferred work;
- relevant privacy or generated-output rules.

During implementation:

1. Keep changes scoped and maintainable.
2. Follow existing project patterns.
3. Keep documentation synchronized with code and workflow behavior.
4. Keep private files, secrets, generated outputs, models, and environments out
   of git unless explicitly approved.
5. Run relevant validators, tests, syntax checks, and output inspections.
6. Create or update a concise implementation summary under docs/ai_sessions/
   when the work materially changes the project.

After implementation, present:

- Summary of Changes
- Files Modified
- Documentation Updated
- Generated Outputs
- Tests / Verification Executed
- Remaining Issues
- Recommended Next Step
- Recommended Commit Message, if a commit is appropriate

Do not commit, push, tag, or rewrite history unless I explicitly approve.

End your response with this exact marker:

[[PROMPT:PROJECT_IMPLEMENTATION]]
```

## Prompt 4: Wrap Up Or Pause Session

Use this before pausing, exiting Codex, switching projects, or handing off work
to a future session.

```text
We are pausing or wrapping up this project session.

Perform a session wrap-up review:

1. Check git status and latest commits.
2. List uncommitted tracked changes.
3. List important ignored local assets or generated outputs.
4. Confirm whether tests or validators pass.
5. Confirm whether documentation is synchronized.
6. Confirm whether private files and generated outputs remain ignored.
7. Summarize completed work.
8. Summarize remaining work.
9. State exactly what should happen next when returning.

Present:

- Project
- Completed This Session
- Committed Work
- Uncommitted Work
- Ignored Local Outputs / Assets
- Verification
- Remaining Issues
- Return Prompt

Do not commit, push, tag, rewrite history, delete files, or modify project files
unless I explicitly approve.

End your response with this exact marker:

[[PROMPT:PROJECT_SESSION_WRAP_UP]]
```

## Voice Clone NextStage Notes

For this project, the key docs are:

```text
docs/source_handoff.md
docs/setup_and_private_assets.md
docs/long_scene_workflow.md
docs/long_scene_generation_instructions.md
```

The active project folder is:

```text
/Users/xieyulong2022/AI_Learn/Codex/voice_clone_NextStage
```

The old source project is read-only unless explicitly approved:

```text
/Users/xieyulong2022/AI_Learn/Codex/voice_clone
```

Generated media, model files, virtual environments, voice samples, and private
voice profiles must remain ignored by git.
