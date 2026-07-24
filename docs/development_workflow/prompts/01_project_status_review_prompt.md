# 01 Project Status Review Prompt

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
