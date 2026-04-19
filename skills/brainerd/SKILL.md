---
name: brainerd
description: >
  Initialize or update a repo-local `brain/`: create the `brain/` folder and
  managed `AGENTS.md` block, reflect durable repo learnings into principles or
  notes, or preview, apply, or discard one repo-scoped rumination pass.
---

# Brainerd

Brainerd keeps repo memory in one place: `brain/` plus one managed block in
`AGENTS.md`.

## Use when

- The user asks to initialize or repair a repo brain.
- The user asks to remember something durable for this repo.
- The user asks to mine older repo-scoped history for missed durable
  learnings.
- The user asks to apply or discard a staged rumination preview.

## Do not use when

- The repo already has a `brain/` and the task only needs an ambient read.
  Open `brain/index.md` and `brain/principles.md` directly and continue.
- The user wants todo state, secrets, or raw transcript stored.
- The user has not asked to touch repo memory at all.

## One move at a time

Choose exactly one action before touching files:

- `init`
- `reflect`
- `ruminate-preview`
- `ruminate-apply`
- `ruminate-discard`

If the request is ambiguous between the three rumination actions, ask.

## Fast path

1. If `brain/index.md` and `brain/principles.md` exist, read them first.
2. Make the smallest durable change that solves the request.
3. Edit only `brain/` and the managed Brainerd block in `AGENTS.md`.
4. End every action with a visible `Brainerd summary:` block, even for
   previews and no-ops.

## Action references

- `init`:
  [references/init.md](references/init.md)
- `reflect`:
  [references/reflect.md](references/reflect.md)
- `ruminate-*`:
  [references/ruminate.md](references/ruminate.md)
- layout and hard rules:
  [references/brain-layout.md](references/brain-layout.md),
  [references/guardrails.md](references/guardrails.md)
