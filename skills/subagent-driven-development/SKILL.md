---
name: subagent-driven-development
description: Use this skill when implementing an approved plan in the current session by delegating mostly independent tasks to fresh subagents, then requiring spec review, code-quality review, and fresh controller verification before moving on.
---

# Subagent-Driven Development

Use this skill after the plan is written and approved. Keep the controller session for coordination, review gates, and final verification.

## Workflow

1. Confirm the plan is approved and the workspace is safe to edit.
2. Extract the task list up front, including acceptance criteria, dependencies, and any shared constraints.
3. Check task coupling before dispatching work. Merge or serialize tasks that touch the same files, APIs, selectors, migrations, or shared contracts.
4. For each task, send one fresh implementation subagent the task text, acceptance criteria, working directory, and the codebase context it actually needs.
5. If the implementer reports `NEEDS_CONTEXT` or `BLOCKED`, change the context, scope, or model before retrying. Do not brute-force the same prompt again.
6. Run spec review with [references/spec-reviewer-prompt.md](references/spec-reviewer-prompt.md).
7. Run code-quality review with [references/code-quality-reviewer-prompt.md](references/code-quality-reviewer-prompt.md).
8. Verify the task yourself in the controller session with the relevant tests, checks, or manual verification.
9. Record reusable learnings for later tasks, then move to the next task.
10. After all tasks are complete, run fresh whole-branch verification and a whole-diff review when the change is large or cross-cutting.

## References

- [references/implementer-prompt.md](references/implementer-prompt.md)
- [references/spec-reviewer-prompt.md](references/spec-reviewer-prompt.md)
- [references/code-quality-reviewer-prompt.md](references/code-quality-reviewer-prompt.md)

## Guardrails

- Use this only when the plan is already approved and the tasks are mostly independent.
- Do not make subagents read the plan file directly. Paste only the relevant task text and context.
- Do not dispatch conflicting tasks in parallel.
- Do not skip spec review, code-quality review, or controller verification because a task looks simple.
- Do not trust an implementation success report without fresh verification evidence.
- If your environment cannot dispatch fresh subagents, keep the same loop inline instead of pretending delegation exists.
