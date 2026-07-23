# AGENTS.md

# Travel Media Assistant

## Project Mission

Travel Media Assistant is an AI-assisted workflow for organizing, enriching,
analyzing, and editing travel photos and videos.

This repository focuses on long-form voice-clone narration and subtitle
delivery. The architecture must remain destination-independent.

## Engineering Principles

- Architecture before implementation.
- Documentation is part of the implementation.
- Maintain maintainability over shortcuts.
- Keep changes incremental and well-tested.
- Prefer reusable, extensible designs.
- Preserve backward compatibility whenever practical.
- Keep the workflow simple unless a real workflow need justifies more
  structure.

## Development Workflow

Before implementation work:

1. Review the repository.
2. Review all required documentation.
3. Verify prerequisites.
4. Present repository review, execution plan, and risks or assumptions.
5. Wait for user approval.

Use the prompts in `docs/project_prompts.md` to start work and to pause or exit
cleanly.

## Coding Standards

- Python 3.11+.
- Follow PEP8.
- Use type hints.
- Prefer dataclasses where appropriate.
- Keep functions small and focused.
- Use logging instead of print().
- Avoid duplicated logic.
- Preserve architectural consistency.

## Documentation Requirements

Documentation is required for every architectural or functional change.

Keep synchronized:

- `README.md`
- workflow documentation
- setup documentation
- development/session notes
- user-facing prompts

## Testing

For every implementation:

- Run relevant tests or syntax checks.
- Add tests for new functionality when scripts are added.
- Report test results.

## Git Policy

Never perform these actions unless explicitly instructed:

- Commit
- Push
- Tag
- Rewrite history
- Force push

Instead, prepare commit recommendations and wait for approval.

## Repository Rules

Do not:

- Modify the old `voice_clone` repo unless explicitly asked.
- Modify unrelated files.
- Delete documentation.
- Rename directories without approval.
- Remove existing functionality without approval.
- Change repository structure unless required by the design.

Keep private voice data, voice profiles, models, generated media, and local
delivery files out of git.
