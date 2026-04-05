---
name: brainerd
description: Use this skill to install and operate Brainerd repo memory from one self-contained skill across Pi, Codex, and Claude. Trigger it when the user wants to set up Brainerd in a repo, create or repair the managed `brain/` and `AGENTS.md` surfaces, reflect durable learnings from the current conversation, review older repo-scoped session history for missed durable knowledge, or apply or discard a staged Brainerd rumination preview.
---

# Brainerd

Brainerd may already be ambient in repos that have a brain. In that case the
active harness should already be reading `brain/index.md` and
`brain/principles.md` before non-trivial work. Use this skill for explicit
Brainerd writes and Brainerd setup.

On Windows, replace `.sh` wrapper calls with the matching `.cmd` file under
`./scripts/`.

## Infer the action first

- `init`: create or repair the repo-local `brain/` and the managed Brainerd
  block in `AGENTS.md`.
- `reflect`: persist durable learnings from the current conversation.
- `ruminate-preview`: review older repo-scoped session history and stage a
  preview only.
- `ruminate-apply`: apply an already staged rumination preview.
- `ruminate-discard`: discard an already staged rumination preview.
- If the user clearly wants only ambient reads from an existing brain, do not
  write anything.
- If intent is genuinely ambiguous between preview, apply, and discard, stop
  and ask instead of guessing.

## Detect the harness

1. If the run exposes Pi Brainerd tools such as `brainerd_current_session`,
   `brainerd_repo_sessions`, `brainerd_stage_ruminate`,
   `brainerd_get_staged_ruminate`, or `brainerd_apply_changes`, stay inside the
   Pi tool flow. Do not use shell wrappers in that branch.
2. If `CODEX_THREAD_ID` is present, use the bundled Codex wrapper:

```bash
./scripts/brainerd-codex.sh ...
```

3. If `BRAINERD_CLAUDE_SESSION_ID` or `BRAINERD_CLAUDE_TRANSCRIPT_PATH` is
   present, use the bundled Claude wrapper:

```bash
./scripts/brainerd-claude.sh ...
```

4. If none of those signals match, stop and report that harness detection
   failed. Do not guess.

## Pi workflow

1. Read the ambient brain context already injected into the run. Open
   additional `brain/` files only when needed.
2. For `init`, use the guarded `/pi-init` surface. Review the bootstrap
   preview before writing. Only apply the bootstrap note when the user
   explicitly asks for it or confirms after seeing the preview.
3. For `reflect`, call `brainerd_current_session`, distill the smallest durable
   change that helps future sessions, prefer updating an existing principle, and
   apply changes only through `brainerd_apply_changes`.
4. For `ruminate-preview`, call `brainerd_repo_sessions`, derive findings, and
   stage the preview through `brainerd_stage_ruminate`. Do not write brain files
   during preview.
5. For `ruminate-apply`, call `brainerd_get_staged_ruminate` first, then apply
   only that staged proposal through `brainerd_apply_changes`.
6. For `ruminate-discard`, reject the staged preview through the Pi confirmation
   flow if it is available. If the harness does not expose a discard path, stop
   after reporting that no brain changes were written.

## Codex and Claude workflow

1. Read `brain/index.md` and `brain/principles.md` before choosing a target.
2. For `init`, run the matching wrapper:

```bash
./scripts/brainerd-codex.sh init
./scripts/brainerd-claude.sh init
```

3. Review the bootstrap preview before writing it. Only apply the operations
   note when the user explicitly asked for it or confirms after seeing the
   preview:

```bash
./scripts/brainerd-codex.sh init --apply-bootstrap
./scripts/brainerd-claude.sh init --apply-bootstrap
```

4. For `reflect`, run the matching current-session command:

```bash
./scripts/brainerd-codex.sh current-session
./scripts/brainerd-claude.sh current-session
```

5. Distill the smallest durable change that helps future Pi, Codex, or Claude
   work. Prefer updating an existing principle file. Otherwise target one
   focused note under `brain/notes/<kebab-case-topic>.md`.
6. Write a small JSON payload to `/tmp/brainerd-reflect.json` with a `changes`
   array, then apply only through the matching wrapper:

```bash
./scripts/brainerd-codex.sh apply-changes --input /tmp/brainerd-reflect.json
./scripts/brainerd-claude.sh apply-changes --input /tmp/brainerd-reflect.json
```

7. For `ruminate-apply` or `ruminate-discard`, check for an already staged
   preview first:

```bash
./scripts/brainerd-codex.sh staged-ruminate
./scripts/brainerd-claude.sh staged-ruminate
```

8. Apply or discard only through the matching wrapper:

```bash
./scripts/brainerd-codex.sh apply-staged-ruminate
./scripts/brainerd-claude.sh apply-staged-ruminate
./scripts/brainerd-codex.sh discard-staged-ruminate
./scripts/brainerd-claude.sh discard-staged-ruminate
```

9. For `ruminate-preview`, start a fresh preview with the matching repo-sessions
   command, use only the returned repo-scoped history, and stop if readiness is
   `insufficient` or `unsupported`:

```bash
./scripts/brainerd-codex.sh repo-sessions
./scripts/brainerd-claude.sh repo-sessions
```

10. If there is a real durable finding, write `/tmp/brainerd-ruminate.json`
    with `findingsSummary`, `rationale`, and `changes`, then stage it only
    through:

```bash
./scripts/brainerd-codex.sh stage-ruminate --input /tmp/brainerd-ruminate.json
./scripts/brainerd-claude.sh stage-ruminate --input /tmp/brainerd-ruminate.json
```

11. A fresh rumination run is preview-only. Tell the user when a preview is
    staged and that no brain changes were written yet.

## Guardrails

- Edit only under `brain/` plus the managed Brainerd block in `AGENTS.md`.
- Do not hand-edit generated entrypoints like `brain/index.md` or
  `brain/principles.md`; let the helper sync them.
- Do not store secrets, one-off task state, or generic skill instructions.
- Do not dump transcript excerpts into the brain. Distill them into durable
  notes or principles.
- Claude imports belong under `brain/imports/claude/`; never copy imported
  Claude memory files verbatim into user-owned notes.
- End with a visible `Brainerd summary:` section that says what changed, what
  was only previewed, what was discarded, or why no brain changes were written.
