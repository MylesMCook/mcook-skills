---
name: issue-handoff
description: Use when one AI agent needs to hand work to another agent with fresh context. Produce a self-contained handoff prompt with evidence, unknowns, and the next action. Create files only if explicitly asked.
---

# Issue Handoff

Turn agent findings into a self-contained handoff another agent can act on without prior thread context.

## Core rule

Default output is one ready-to-send prompt block.
- Prefer prompt text, not files.
- Create files only if the user explicitly asks.
- Preserve evidence.
- Preserve uncertainty.
- Assume the receiving agent has not seen the current conversation.

## Workflow

1. Extract:
- problem
- current state
- affected scope
- evidence
- expected result
- requested next action

2. Ask for missing critical details only. If something is unknown, mark it `Unknown` instead of guessing.

3. Return this exact shape:

```text
You are taking over this task with no prior thread context.

Problem:
- ...

Why this was handed off:
- ...

Current state:
- ...

Affected scope:
- ...

Observed behavior:
- ...

Expected behavior:
- ...

Evidence:
- ...
- ...

Repro steps:
- 1) ...
- 2) ...

Unknowns:
- ...

Acceptance criteria:
- ...

Constraints:
- ...

Requested next action:
- ...

Success looks like:
- ...

Files:
- prompt-only handoff unless user provided files.
```

4. Keep it operational.
- Do not add backstory.
- Do not write ticket prose.
- Do not assume shared memory between agents.

## Optional file handoff (only if requested)

Create `handoff-YYYY-MM-DD-issue.md` with the same content as above.
