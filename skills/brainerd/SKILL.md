---
name: brainerd
description: Use when the user asks to set up, populate, or maintain a repo-local `brain/` memory surface — initializing the `brain/` directory and the managed Brainerd block in `AGENTS.md`, reflecting durable learnings from the current session into principles or notes, or reviewing older session history to surface missed learnings. Harness-agnostic; works wherever the agent has repo filesystem access.
---

# Brainerd

Brainerd is a repo-local memory convention: a `brain/` directory of stable
principles and durable notes, plus a managed block in `AGENTS.md` that teaches
future agents how to read and extend it. This skill describes how to use it.
It is instruction-only and makes no assumptions about the host harness.

## When to use

- The user asks to set up, bootstrap, or repair a `brain/` in this repo.
- The user asks to persist a durable learning from the current conversation.
- The user asks to review older session history for learnings that should
  have been captured but were not.
- The user asks to apply or discard a previously staged rumination preview.

## When not to use

- The repo already has a `brain/` and the user only wants an ambient read
  to inform other work — just open `brain/index.md` and
  `brain/principles.md` directly and continue. No Brainerd action is needed.
- The user wants to capture one-off task state, a todo list, secrets,
  credentials, or a raw transcript. These do not belong in the brain.
- The user has not asked to touch repo memory at all.

## Ambient read protocol

Before any non-trivial work in a repo that already contains a `brain/`:

1. Open `brain/index.md` and `brain/principles.md`.
2. Open deeper principle files or notes on demand when their topics are
   relevant to the task at hand.
3. Treat principles as stable defaults and notes as specific durable
   learnings. Do not edit either unless the user asked for a Brainerd write.

## Actions

Infer which action the user wants before doing anything. If intent is
ambiguous between preview, apply, and discard, stop and ask.

- **`init`** — create or repair `brain/` and the managed Brainerd block in
  `AGENTS.md`. Show the user a preview of what will be written before
  writing. See [references/brain-layout.md](references/brain-layout.md).
- **`reflect`** — distill durable learnings from the current conversation
  into the smallest useful change: prefer updating an existing principle,
  otherwise add one focused note under `brain/notes/<kebab-topic>.md`. See
  [references/reflect.md](references/reflect.md).
- **`ruminate-preview`** — review older repo-scoped session history and
  stage a preview only. Do not write brain files on a fresh rumination run.
  See [references/ruminate.md](references/ruminate.md).
- **`ruminate-apply`** — apply a previously staged rumination preview.
- **`ruminate-discard`** — discard a previously staged rumination preview
  without writing anything.

## Write discipline

- Edit only under `brain/` and the managed Brainerd block in `AGENTS.md`.
- Never hand-edit generated entrypoints (`brain/index.md`,
  `brain/principles.md`) — regenerate them from the underlying principle
  and note files instead.
- Never store secrets, credentials, one-off task state, or transcript
  excerpts. Distill learnings; do not paste conversations.
- Imported memory from a harness belongs under `brain/imports/<harness>/`
  and is read-only from this skill's perspective.
- See [references/guardrails.md](references/guardrails.md) for the full
  list of hard rules.

## Summary contract

Every Brainerd action ends with a visible `Brainerd summary:` block that
states, in plain language:

- what was written (file paths, one-line description per file),
- what was only previewed,
- what was discarded,
- or why no brain changes were written.

If you took no action, say so explicitly instead of staying silent.

## References

- [references/brain-layout.md](references/brain-layout.md) — the on-disk
  contract: what files exist in `brain/`, where, and what each is for.
- [references/reflect.md](references/reflect.md) — step-by-step
  walkthrough of the `reflect` action.
- [references/ruminate.md](references/ruminate.md) — step-by-step
  walkthrough of `ruminate-preview`, `ruminate-apply`, and
  `ruminate-discard`.
- [references/guardrails.md](references/guardrails.md) — hard rules about
  what to write and what to never write.
