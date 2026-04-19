# Ruminate

Use `ruminate` for **older** repo-scoped history, not the current conversation.
There are only three valid actions: preview, apply, and discard.

## Sources of older history

Use only history clearly scoped to the current repo. If no repo-scoped history
source is available, stop and say rumination is unsupported here.

## `ruminate-preview`

1. Read older repo-scoped history and look for repeated corrections, stable
   preferences, recurring pitfalls, or missed durable project knowledge.
2. Stop without staging if the signal is weak, conflicting, or non-durable.
3. Draft a staged preview at `brain/.staging/ruminate-preview.json` with:
   - `findingsSummary`
   - `rationale`
   - `changes`: a list of `{path, action, content}` entries
4. Do not write durable brain files during preview.
5. Tell the user that the preview was staged and that no durable brain files
   were changed.

## `ruminate-apply`

1. Re-read `brain/.staging/ruminate-preview.json`. If it is missing, stop and
   say so.
2. Apply only the staged `changes` under `brain/principles/` or `brain/notes/`.
3. Regenerate `brain/index.md` and `brain/principles.md`.
4. Delete the staged preview.
5. End with `Brainerd summary:`.

Never mix fresh findings into apply. If you found new things, discard and stage
again.

## `ruminate-discard`

1. Delete `brain/.staging/ruminate-preview.json` if it exists.
2. Do not touch durable brain files.
3. End with `Brainerd summary:`.

If the user is ambiguous between preview, apply, and discard, ask.
