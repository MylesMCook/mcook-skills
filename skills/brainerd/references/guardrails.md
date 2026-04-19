# Guardrails

Hard rules for every Brainerd action. Treat these as non-negotiable.

## Scope of writes

- Edit only files under `brain/` and the managed Brainerd block in `AGENTS.md`.
- Do not modify code, config, tests, tickets, or docs outside those surfaces.
- `brain/.staging/ruminate-preview.json` is the only transient exception.

## Generated entrypoints

- `brain/index.md` and `brain/principles.md` are generated from the underlying
  note and principle files.
- Never hand-edit them.
- Rebuild them whenever files under `brain/principles/` or `brain/notes/`
  change.

## What never goes into the brain

- secrets, credentials, tokens, or API keys
- one-off task state
- raw transcript excerpts or tool output
- generic instructions that belong in some other skill

## Imported memory

- Imported memory lives under `brain/imports/<source>/` and is read-only.
- Never copy imported text verbatim into `brain/principles/` or
  `brain/notes/`. Distill it.

## Ambiguity

- If the user only wants an ambient read from an existing brain, do not write.
- If the user is ambiguous between `ruminate-preview`, `ruminate-apply`, and
  `ruminate-discard`, stop and ask.

## Minimum-change bias

- Prefer updating an existing principle over adding a new note.
- Prefer updating an existing note over adding a new one.
- Prefer one sharper sentence over a new file.
- If you want more than one or two durable file changes, the learning is
  probably not distilled yet.

## Summary discipline

Every Brainerd action ends with a visible `Brainerd summary:` block. Silence is
never acceptable after a Brainerd action.
