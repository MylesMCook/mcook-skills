# Guardrails

Hard rules for every Brainerd action. Treat these as non-negotiable.

## Scope of writes

- Edit only files under `brain/` and the managed Brainerd block inside
  `AGENTS.md`. Nothing else in the repo is owned by this skill.
- Do not modify code, config, tests, or documentation outside those
  two surfaces as part of a Brainerd action.

## Generated entrypoints

- `brain/index.md` and `brain/principles.md` are regenerated from the
  underlying principle and note files. Never hand-edit them. Rebuild them
  whenever you add, rename, or delete a file beneath `brain/`.

## What never goes into the brain

- Secrets, credentials, tokens, API keys, or anything resembling them.
- One-off task state ("currently editing file X", "waiting on review from
  Y"). The brain is for durable knowledge only.
- Raw transcript excerpts, tool outputs, or quoted conversation blocks.
  Distill learnings into your own prose.
- Generic skill instructions that already live in another skill's
  `SKILL.md`. Do not duplicate them here.

## Imported memory

- Memory imported from a host harness lives under
  `brain/imports/<harness>/` and is read-only from this skill's
  perspective.
- Never copy the contents of an imported file verbatim into
  `brain/principles/` or `brain/notes/`. If a learning is worth keeping,
  distill it in your own words and cite the import path.

## Ambiguity

- If the user's intent is ambiguous between `ruminate-preview`,
  `ruminate-apply`, and `ruminate-discard`, stop and ask. Do not guess.
- If the user only wants an ambient read from an existing brain, do not
  write anything.

## Minimum-change bias

- Prefer updating an existing principle over adding a new note.
- Prefer updating an existing note over adding a new one.
- Prefer one sharper sentence over a new file.
- Do not create more than one or two files in a single action. If a
  learning seems to demand more, it probably is not durable yet.

## Summary discipline

Every Brainerd action ends with a visible `Brainerd summary:` block. If
no brain changes were written, the summary still runs and explains why.
Silence is never acceptable after a Brainerd action.
