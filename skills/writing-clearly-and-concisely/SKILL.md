---
name: writing-clearly-and-concisely
description: "Use when drafting, rewriting, editing, summarizing, or polishing prose for humans: docs, README/API docs, PRs, commit text, emails, Slack, reports, explanations, UI copy, comments, or final answers. Preserve meaning, choose a reader-appropriate tone, cut filler, and make the result easier to act on."
---

# Writing Clearly and Concisely

Use this skill for human-facing prose. The job is to say the right thing to the right reader with no wasted motion.

## Workflow

1. Identify the purpose, reader, channel, tone, and length. Infer defaults unless the missing detail would materially change the result.
2. Protect the non-negotiables: facts, names, dates, figures, technical terms, constraints, citations, caveats, and user wording that must stay.
3. Lead with the answer, ask, decision, or recommendation. Add structure only when it improves scanning.
4. Edit in passes:
   - structure: remove throat-clearing, repeated setup, and fake conclusions
   - sentences: prefer active voice, direct subjects, concrete verbs, and parallel structure
   - words: cut hedges, filler, hype, duplicated modifiers, and vague nouns
   - tone: keep it calm, specific, and appropriate for the relationship
5. Do a final check for accuracy, readability, and length.

## Defaults

- Drafting from scratch: return the finished prose first. Explain choices only when assumptions or tradeoffs matter.
- Editing supplied text: start with `Revised:`. Add `What changed:` only when the rewrite is substantial or the user asked.
- Reviewing without rewriting: lead with the main issues and concrete fixes.
- Multiple options: provide 2-3 meaningfully different versions, not a pile of near-duplicates.
- Missing facts: use placeholders like `[date]`, `[metric]`, or `[source]` instead of inventing details.
- High-stakes text: preserve caveats and flag facts that need verification.

## Guardrails

- Preserve facts, uncertainty, and technical precision.
- Clarity beats brevity. Cut only when meaning survives.
- Follow the user's requested tone, format, audience, or word limit before any house style.
- Do not mechanically "humanize" code, logs, legal text, citations, or commands.

## Common fixes

- Put the point first.
- Replace vague abstractions with specific nouns and verbs.
- Remove filler like `in order to`, `it is important to note`, `overall`, and `in conclusion`.
- Replace hype like `robust`, `seamless`, `cutting-edge`, and `best-in-class` with observable claims or delete it.
- Prefer direct phrasing: `use` over `utilize`, `help` over `facilitate`, `now` over `at this point in time`.

## References

Read only what the task needs:

- `references/format-playbook.md` for docs, READMEs, PRs, commits, workplace writing, summaries, reports, and UI copy
- `references/signs-of-ai-writing.md` to strip generic AI polish and filler
- `references/elements-of-style/03-elementary-principles-of-composition.md` for substantial drafts and rewrites
- `references/elements-of-style/02-elementary-rules-of-usage.md` for grammar and punctuation checks
- `references/elements-of-style/04-a-few-matters-of-form.md` for headings, bullets, tables, quotations, and formatting
- `references/elements-of-style/05-words-and-expressions-commonly-misused.md` for word-choice cleanup
- `references/elements-of-style/01-introductory.md` only for quick orientation

## Final check

Before sending, ask:

- Is the main point visible early?
- Did I preserve every fact and constraint?
- Can the reader act on this?
- Did I remove generic filler without sanding off the meaning?
