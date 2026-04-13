---
name: git-it-out
description: "Use this skill when the user wants you to finish already-mostly-complete work and carry it through repo-native closeout: final verification, PR or branch wrap-up, merge/release/deploy/publish steps, tracker updates, and a concise handoff. Reach for it on prompts like 'ship this', 'merge and close this out', 'take this over the line', 'take this off my plate', 'finish the session', or 'get this into production'. Do not use it for greenfield implementation, open-ended debugging, broad refactors, or inventing a release process from scratch."
---

# Git It Out

Use this skill when the work is substantially complete and the user wants the agent to own the remaining closeout without reopening the whole plan.

## Boundaries

- Use it for last-mile closure: push, PR, merge, release, deploy, publish, tracker, and handoff work.
- Do not use it for greenfield implementation, broad refactors, deep debugging, or release-process design from scratch.
- If you discover the work is not actually closeable yet, clear only the blockers required to reach the intended finish line, then stop expanding scope.

## Load `references/finish-checklist.md` when

- the finish line touches more than one surface, such as PR plus tracker plus deploy,
- an irreversible action is about to happen,
- repo policy or branch protection adds gates you must satisfy, or
- you need a completion checklist before handing back status.

## Default Stance

- Treat the request as permission to own closeout, not to brainstorm.
- Infer the intended landing path from repo instructions, branch or PR state, CI signals, release config, deployment config, and task context before asking questions.
- Prefer the repo's native path over generic Git habits.
- Treat repo-native checkpoint, release, or closeout tooling such as Entire as first-class only when it is actually configured.
- Default to the smallest action that truly reaches the requested finish line.
- Ask only when the irreversible target is ambiguous, credentials or authority are missing, or repo or user policy requires approval.

## Closeout Procedure

1. Inspect the state: git status, active branch, pending diffs, PR or review state, CI, release or deploy config, and task context.
2. Determine the actual finish line: branch push, PR update or open, merge, release, deploy, publish, production, or handoff-ready partial completion because of an external blocker.
3. Identify required gates for that finish line: tests, lint, build, typecheck, approvals, changelog or release notes, tracker state, migrations, feature flags, checkpoint capture, or other repo-native checks.
4. Run the last useful validation for the chosen finish line and fix only finish-blocking issues. Re-run until the gate passes or you hit a true blocker.
5. Execute the repo-native finish steps in order.
6. Clean up every surface that is part of done: PR, branch, tracker, release artifact, deploy surface, checkpoints, and handoff notes.
7. Report the final state clearly, including anything that could not be completed.

## Ask vs Act

- Keep moving when the standard target is clear from repo context.
- Ask before merge, release, deploy, publish, or delete-branch actions only when the destination or policy gate is unclear.
- If an external system blocks the last step, complete everything up to that blocker and leave a precise handoff.

## Guardrails

- Do not invent a release or deployment process.
- Do not treat "finish the session" as permission to ship to production when the repo's normal finish line is only a branch or PR.
- Do not assume Git usage alone means Entire is active.
- Do not broaden scope into unrelated cleanup or quality polish.
- Do not both merge and deploy unless the workflow actually requires both.
- Do not leave branch, tracker, release, or handoff cleanup half-done when it is part of the finish line.
- Do not hide skipped checks, failed gates, residual risk, or manual follow-up.

## Output

- What landed.
- Where it landed.
- What was verified.
- Which surfaces were updated.
- Any residual risk, remaining blocker, or next follow-up.
