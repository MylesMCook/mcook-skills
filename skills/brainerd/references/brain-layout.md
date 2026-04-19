# Brain Layout

The on-disk contract for a repo-local `brain/`. Keep every file short and plain
Markdown.

## Directory tree

```
<repo-root>/
├── AGENTS.md              # contains one managed Brainerd block
└── brain/
    ├── index.md           # generated entrypoint
    ├── principles.md      # generated principle index
    ├── principles/
    │   └── <topic>.md     # one stable engineering principle per file
    ├── notes/
    │   └── <topic>.md     # one focused durable learning per file
    ├── imports/
    │   └── <source>/      # read-only imported memory
    └── .staging/          # optional transient staging area
        └── ruminate-preview.json
```

## File purposes

- `brain/index.md` is the ambient entrypoint. Read it before non-trivial repo
  work. It is generated and never hand-edited.
- `brain/principles.md` is the flat index of files under `brain/principles/`.
  It is generated and never hand-edited.
- `brain/principles/<topic>.md` holds stable repo-wide defaults. Rewrite in
  place when a principle changes.
- `brain/notes/<topic>.md` holds one focused durable learning.
- `brain/imports/<source>/` holds read-only imported memory.
- `brain/.staging/ruminate-preview.json` is optional and transient. It exists
  only between `ruminate-preview` and `ruminate-apply` or `ruminate-discard`.

## Naming rules

- Filenames are kebab-case.
- Titles inside files use Title Case and match the filename's topic.
- One concept per file.

## Managed `AGENTS.md` block

`init` owns one clearly delimited Brainerd block in `AGENTS.md`.

- If `AGENTS.md` does not exist, create a minimal file containing only that
  block.
- If `AGENTS.md` exists, preserve all user-authored content outside the block.
- Repair the managed block with `init`, not by hand.
