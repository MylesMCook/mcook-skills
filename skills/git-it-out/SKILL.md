---
name: git-it-out
description: Finish the last-mile ship and closeout work. Use when users say things like "ship this," "deploy this," "merge this," "finish this tonight," "close this out," or "get this over the line," and the job is to carry work through final verification, branch or PR closure, deploy or release steps, tracker cleanup, and a short handoff or release summary.
---

# Git It Out

Use this skill when the work is mostly done and the job is to finish the landing cleanly.

## Default Stance

- Treat the request as permission to finish the work, not to brainstorm.
- Infer the real finish line from repo instructions, branch state, CI status, deployment config, and task context before asking questions.
- Prefer the repo's existing release, merge, and deployment path over a generic workflow.

## Closeout Flow

1. Inspect the current state: repo status, active branch, pending diffs, CI or test signals, release or deploy config, and task context.
2. Identify the actual landing path: push a branch, update or open a PR, merge, deploy, publish, cut a release, or some repo-specific combination.
3. Run the last useful verification for that landing path and fix only what blocks closeout.
4. Execute the repo-native finish steps in order.
5. Update the formal tracker or working notes if the workflow calls for it, then write a short handoff or release note when that would prevent next-day confusion.
6. Report the final state clearly.

## Ask vs Act

- Ask only when the irreversible target is genuinely ambiguous, credentials or authority are missing, or repo or user policy requires a gate.
- If one finish path is clearly standard, keep moving.
- If an external blocker stops the last step, complete everything up to that blocker and say exactly what remains.

## Guardrails

- Do not invent a release or deploy process.
- Do not broaden the scope into unrelated feature work or cleanup.
- Do not both merge and deploy unless the actual workflow requires both.
- Do not leave branch, tracker, or release cleanup half-done when it is part of the finish line.
- Do not hide skipped checks, residual risk, or manual follow-up.

## Output Shape

- State what landed.
- State where it landed.
- State what tracker, PR, deploy, or release surfaces were updated.
- State any residual risk or next-day follow-up in one short section.
