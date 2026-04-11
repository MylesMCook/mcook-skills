---
name: subagent-driven-development
description: Use this skill after a plan is approved when you want controller-led execution that delegates mostly independent tasks to fresh subagents, applies proportional review gates, and keeps controller verification mandatory before moving on.
---

# Subagent-Driven Development

Use this skill after the plan is written and approved. Keep the controller session as the manager and wrangler: decompose the work, route models, run review gates, verify outcomes, and close agents that are no longer needed.

## Workflow

1. Confirm the plan is approved and the workspace is safe to edit.
2. Extract the task list up front, including acceptance criteria, dependencies, shared constraints, and likely ownership boundaries.
3. Default to a manager posture. Delegate aggressively when tasks are bounded and independent. Keep only blocking, tightly coupled, or controller-only work local.
4. Bootstrap context narrowly. If the repo has a canonical instruction or memory entrypoint such as `AGENTS.md`, `CLAUDE.md`, `WORKFLOW.md`, or a memory index, point each worker there first before adding broader context.
5. Route models by default:
   - controller: `gpt-5.4`
   - implementers: `gpt-5.3-codex-spark`
   - reviewers and explorers: `gpt-5.4-mini`
   Escalate the model, scope, or context when a task is blocked by ambiguity, depth, or coupling. Do not brute-force the same prompt again.
6. Check task coupling before dispatching work. Merge or serialize tasks that touch the same files, APIs, selectors, migrations, browser state, or shared contracts.
7. For each task, send one fresh implementation subagent the task text, acceptance criteria, working directory, owned write scope, and only the codebase context it actually needs.
8. If a task needs browser work, give that agent its own isolated `agent-browser` session. Never share a live browser session across agents.
9. Run review gates proportionally:
   - keep controller verification mandatory every time
   - keep both spec review and code-quality review for risky, cross-cutting, shared-contract, or user-visible changes
   - allow a lighter targeted review pass for tiny doc or tightly scoped mechanical tasks when manager judgment says the full loop would be pure ceremony
10. Verify the task yourself in the controller session with the relevant tests, checks, or manual verification.
11. Record reusable learnings for later tasks, then close completed agents once their output is fully reviewed and no longer needed, especially before spawning more.
12. After all tasks are complete, run fresh whole-branch verification and a whole-diff review when the change is large or cross-cutting.

## References

- [references/implementer-prompt.md](references/implementer-prompt.md)
- [references/spec-reviewer-prompt.md](references/spec-reviewer-prompt.md)
- [references/code-quality-reviewer-prompt.md](references/code-quality-reviewer-prompt.md)

## Guardrails

- Use this only when the plan is already approved and the tasks are mostly independent.
- Do not make subagents read the plan file directly. Paste only the relevant task text and context.
- Do not flood workers with broad context when a canonical repo entrypoint exists.
- Do not dispatch conflicting tasks in parallel or give two agents the same write surface.
- Do not share browser sessions, refs, or mutable browser state across agents.
- Do not skip controller verification, and do not relax review depth for risky or shared-behavior changes.
- Do not trust an implementation success report without fresh verification evidence.
- Do not leave finished agents open just because they might be useful later. Close them and respawn if needed.
- If your environment cannot dispatch fresh subagents, keep the same loop inline instead of pretending delegation exists.
