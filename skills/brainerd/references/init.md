# Init

`init` creates or repairs the smallest usable Brainerd setup.

## Write only these surfaces

- the managed Brainerd block in `AGENTS.md`
- `brain/index.md`
- `brain/principles.md`
- `brain/principles/`
- `brain/notes/`
- `brain/imports/`

Create `brain/.staging/` only when a rumination preview is actually staged.

## Steps

1. Inspect `AGENTS.md`, `brain/index.md`, `brain/principles.md`,
   `brain/principles/`, and `brain/notes/`.
2. Preview the exact writes first unless the user explicitly asked you to
   initialize or repair the brain now.
3. Create or repair the managed Brainerd block in `AGENTS.md`. Preserve all
   non-Brainerd content outside that block.
4. Create any missing `brain/` directories. Do not invent notes or principles
   just to fill space.
5. Create minimal generated entrypoints:
   - `brain/index.md` links to `brain/principles.md` and notes that deeper
     notes live under `brain/notes/`.
   - `brain/principles.md` lists principle files or says there are none yet.
6. End with `Brainerd summary:` listing what was previewed, written, or skipped.

## Managed block template

Use one clearly delimited block:

```md
## Brainerd
<!-- BEGIN BRAINERD MANAGED BLOCK -->
This repo uses a local `brain/` for durable memory.

Before non-trivial work:
1. Read `brain/index.md`.
2. Read `brain/principles.md`.
3. Open deeper notes only when relevant.

Write discipline:
- Edit only under `brain/` and this managed block.
- Never hand-edit `brain/index.md` or `brain/principles.md`.
- Keep durable knowledge only: no secrets, no transcript snippets, no task
  state.

This block is managed by Brainerd. Repair it with Brainerd `init`, not by hand.
<!-- END BRAINERD MANAGED BLOCK -->
```
