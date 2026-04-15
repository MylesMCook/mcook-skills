# Reflect

`reflect` distills durable learnings from the **current conversation**
into the smallest useful change under `brain/`.

## Step 1: Read the current session

Scan the conversation so far for durable content:

- recurring preferences the user has expressed,
- engineering defaults they agreed to or corrected,
- pitfalls hit during the task that should not be hit again,
- non-obvious conventions of this repo discovered while working.

Ignore:

- the specific task state ("we are editing file X right now"),
- tool outputs, diffs, and raw transcript text,
- secrets, credentials, and one-off identifiers.

If nothing durable is actually present, stop and say so. A no-op reflect
is a valid outcome.

## Step 2: Pick the smallest change

Prefer, in order:

1. **Updating an existing principle file** under `brain/principles/`. One
   sharper sentence beats a new file.
2. **Updating an existing note** under `brain/notes/` if the learning
   extends something already captured.
3. **Creating one new note** under `brain/notes/<kebab-topic>.md`, scoped
   tightly to a single concept.
4. **Creating a new principle** only when the learning is a stable,
   repo-wide default — not a one-off.

Never create more than one or two files in a single reflect pass. If you
find yourself wanting to, the learnings are not durable enough yet.

## Step 3: Preview before writing

Show the user:

- the target file path,
- a diff-style preview (before → after, or the full new file if new),
- a one-line rationale for why this is durable.

## Step 4: Apply

Write the files only after the user confirms, or when the user's original
request already explicitly asked to persist. After writing, regenerate
`brain/index.md` and `brain/principles.md` so the indexes stay in sync
with the files that actually exist.

## Step 5: Summary

End with a `Brainerd summary:` block listing each path written, each path
only previewed, and any learnings intentionally dropped.
