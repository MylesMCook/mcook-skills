# Reflect

Use `reflect` for durable learnings from the current conversation.

## Steps

1. If the repo is not initialized yet, run `init` first.
2. Read `brain/index.md` and `brain/principles.md`. Open deeper files only if
   they are clearly relevant.
3. Keep only durable material:
   - recurring user preferences
   - stable engineering defaults
   - recurring pitfalls
   - non-obvious repo conventions
4. Ignore:
   - task state
   - raw transcript text
   - tool output
   - secrets or identifiers that do not belong in durable memory
5. Make the smallest durable change in this order:
   1. update an existing principle
   2. update an existing note
   3. add one new note
   4. add one new principle
6. Keep new or updated files short: a title and a few bullets is enough.
7. Preview before writing unless the user explicitly asked you to persist the
   learning now.
8. After writing, regenerate `brain/index.md` and `brain/principles.md`.
9. End with `Brainerd summary:` listing written paths, previewed paths, and any
   learnings you intentionally dropped.

If nothing durable is present, say so. A no-op reflect is valid.
