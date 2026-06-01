---
name: adversarial-review
description: Use this skill when you need a serious code review, diff review, or implementation-plan review from independent reviewers. In Codex hosts, run exactly three fresh Codex subagents with Skeptic, Architect, and Minimalist lenses. Return a PASS, CONTESTED, or REJECT verdict.
---

# Adversarial Review

Use this skill to get independent review from three Codex subagents instead of same-thread self-validation.

## First Read

Open these before launching reviewers:

- `references/reviewer-lenses.md`
- `references/reviewer-prompt.md`
- `references/subagent-review.md`
- `references/verdict-format.md`

If the repo has local project instructions and they matter to the change, read them before prompting reviewers:

- `AGENTS.md`
- `brain/principles.md`

## Workflow

1. Identify the review target: diff, staged changes, PR branch, implementation plan, or a tight file list.
2. Write one sentence of intent: what the author is trying to achieve.
3. Gather the smallest useful context:
   - primary diff or staged changes
   - directly touched files
   - 1-3 nearby dependency files when needed
   - repo principles or project rules
4. If the target is a git worktree, record the pre-review `git status --short` state.
5. Spawn exactly three ordinary fresh Codex subagents in parallel, then label their returned results as:
   - `codex-skeptic` with the Skeptic lens
   - `codex-architect` with the Architect lens
   - `codex-minimalist` with the Minimalist lens
6. Give each subagent the same review target, same intent, same repo principles, and exactly one lens.
7. Instruct every subagent to stay read-only, avoid file writes, and return only markdown findings or `No material findings.`
8. Wait for all three final messages, then close the subagents.
9. If the target is a git worktree, compare post-review `git status --short` with the pre-review state. Treat unexplained new changes as `INCOMPLETE_COVERAGE`.
10. Synthesize with `references/verdict-format.md`:
   - verify all three subagent results exist and are usable
   - record missing, failed, timed-out, malformed, or incomplete reviewers under coverage
   - reject weak or hand-wavy claims; keep only evidence-backed findings
   - make a lead judgment for each finding: `accept` or `reject` with a one-line rationale
11. Return `PASS`, `CONTESTED`, or `REJECT`.

## Defaults

- Exactly three Codex subagents are required for a complete review.
- Do not call outside reviewer tools.
- Do not fall back to a single local reviewer.
- Do not write `.tmp` review files by default; use returned subagent messages.
- If any subagent cannot run or returns unusable output, return `CONTESTED` with an explicit coverage failure.
- If the host cannot spawn Codex subagents, return `CONTESTED` with `SUBAGENT_UNAVAILABLE`.
- A Codex subagent inherits the parent sandbox and approval state. Do not describe it as stronger isolation than the parent actually provides.

## Failure Labels

Use only these orchestration failure labels:

- `SUBAGENT_UNAVAILABLE`
- `SUBAGENT_FAILED`
- `TIMEOUT`
- `MALFORMED_OUTPUT`
- `INCOMPLETE_COVERAGE`
- `CALLER_MISUSE`

## Guardrails

- Review only. Do not edit files, commit, open a PR, or run implementation commands as part of this skill.
- Do not silently drop a failed reviewer.
- Do not merge lenses. Each reviewer uses exactly one lens.
- Do not claim a reviewer found an issue unless the finding has concrete evidence.
- If coverage is complete and no accepted high-severity finding survives synthesis, return `PASS`. Include accepted medium or low findings as non-blocking recommendations.
