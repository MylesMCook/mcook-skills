# Ruminate

`ruminate` reviews **older** repo-scoped session history — not the current
conversation — for durable learnings that were never captured. It runs in
three phases: `preview`, `apply`, and `discard`. Preview is always separate
from apply; a fresh rumination never writes brain files in one shot.

## Sources of older history

Gather candidate history from whatever the host harness exposes. Examples:

- a local transcript directory the harness writes to,
- a session ID or thread ID the harness tracks,
- a user-supplied log file or export,
- a harness-specific memory tool, if one is available.

If no source of older repo-scoped history is available, stop and report
that ruminate is unsupported in this environment. Do not fabricate one.

Only use history scoped to the **current repo**. Cross-repo history leaks
unrelated context and must be filtered out before analysis.

## Phase 1: `ruminate-preview`

1. Read candidate history and look for the same kinds of durable content
   that `reflect` targets (see `reflect.md`).
2. Draft a preview document containing:
   - **`findingsSummary`** — 1–3 sentences describing the durable theme.
   - **`rationale`** — why this is durable and not one-off task state.
   - **`changes`** — a list of `{path, action, content}` entries for the
     files that would be written on apply.
3. **Stage** the preview to a predictable location in the repo's temp
   area (for example, a `.brainerd/staged-ruminate.json` file the user
   can inspect) — do not write anything under `brain/`.
4. Tell the user that a preview has been staged and no brain changes
   have been written yet. Include the staged path.

If readiness is insufficient (not enough signal, conflicting signals, no
repo-scoped history), stop without staging and say so in the summary.

## Phase 2: `ruminate-apply`

1. Re-read the staged preview. If none exists, stop and say so.
2. Apply the `changes` exactly as staged, under `brain/` only.
3. Regenerate `brain/index.md` and `brain/principles.md`.
4. Delete the staged preview file so it cannot be applied a second time.
5. Emit the `Brainerd summary:` block.

Never silently merge a staged preview with new findings during apply. If
new findings have appeared, discard and start a fresh preview.

## Phase 3: `ruminate-discard`

1. Delete the staged preview file if present.
2. Write nothing under `brain/`.
3. Emit a `Brainerd summary:` block stating that the preview was
   discarded and no brain changes were written.

## Ambiguity

If the user's request is ambiguous between `preview`, `apply`, and
`discard`, stop and ask. Guessing between these three is never safe.
