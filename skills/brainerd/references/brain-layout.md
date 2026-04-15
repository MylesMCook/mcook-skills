# Brain Layout

The on-disk contract for a repo-local `brain/`. `init` creates this shape;
`reflect` and `ruminate` extend it. Every file is plain Markdown.

## Directory tree

```
<repo-root>/
├── AGENTS.md              # contains a managed Brainerd block (see below)
└── brain/
    ├── index.md           # generated entrypoint, links principles + notes
    ├── principles.md      # generated index of principle files
    ├── principles/
    │   └── <topic>.md     # one stable engineering principle per file
    ├── notes/
    │   └── <topic>.md     # one focused durable learning per file
    └── imports/
        └── <harness>/     # read-only imported memory (e.g., claude/, codex/)
```

## File purposes

- **`brain/index.md`** — the ambient entrypoint every agent should read
  before non-trivial work. Links to `principles.md` and to individual note
  files. Regenerated from the files beneath it; never hand-edited.
- **`brain/principles.md`** — a flat index of every file under
  `brain/principles/`. Also regenerated, not hand-edited.
- **`brain/principles/<topic>.md`** — stable engineering defaults and
  preferences that apply across the repo. One concept per file. Rewrite in
  place when a principle evolves; do not accumulate stale alternatives.
- **`brain/notes/<topic>.md`** — durable learnings scoped to a specific
  area, pattern, or pitfall. One focused topic per file. Notes may be
  deleted or promoted into principles over time.
- **`brain/imports/<harness>/`** — memory imported from a host harness
  (for example, a Claude memory export). Read-only from this skill's
  perspective; never paste its contents into notes or principles verbatim.

## Naming rules

- Filenames are kebab-case: `boundary-discipline.md`, not
  `BoundaryDiscipline.md`.
- Titles inside files use Title Case and match the filename's topic.
- One concept per file. If a principle grows multiple distinct ideas,
  split it into separate files and regenerate the indexes.

## Managed `AGENTS.md` block

`init` adds or repairs a clearly delimited Brainerd section inside the
repo's `AGENTS.md`. The block explains:

- that a `brain/` exists and should be read before non-trivial work,
- which files are entrypoints (`brain/index.md`, `brain/principles.md`),
- the write discipline from this skill's guardrails,
- that the block itself is managed and should not be hand-edited outside
  a Brainerd `init` or repair pass.

If `AGENTS.md` does not exist, create a minimal one containing only the
Brainerd block. Do not invent unrelated repo guidance.
