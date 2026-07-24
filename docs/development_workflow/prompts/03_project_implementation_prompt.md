# 03 Project Implementation Prompt

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
