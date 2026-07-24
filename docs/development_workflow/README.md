# Development Workflow

This folder defines reusable Codex prompt templates and lightweight protocols
for this project.

The goal is to make every session answer the same core questions:

- what project is this;
- what is the current goal;
- what is the current status;
- what files and outputs matter;
- what exact prompt should be used to start, implement, and wrap up work.

## Core Files

- `standard_project_prompts.md`: reusable prompt templates for Codex projects.
- `prompts/`: individual executable prompt files numbered for easy lookup.
- `stage_prompts.md`: project-local pointer to the standard prompt flow.

Use `standard_project_prompts.md` when starting a session, approving
implementation, reviewing status, or pausing/exiting the project.

For normal use, invoke an individual prompt file directly. Example:

```text
Read docs/development_workflow/prompts/02_project_session_start_prompt.md and execute its content.
```
