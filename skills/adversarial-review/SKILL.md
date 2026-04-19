---
name: adversarial-review
description: Use this skill when you need a serious code review, diff review, or implementation-plan review from independent reviewers. In Codex hosts, prefer a fresh Codex subagent for the Codex reviewer; otherwise use the Codex, Claude Code, and Gemini reviewer paths when available. Return a PASS, CONTESTED, or REJECT verdict.
---

# Adversarial Review

Use this skill to get independent review instead of same-thread self-validation.

## First read

Open these before launching reviewers:

- `references/reviewer-lenses.md`
- `references/reviewer-prompt.md`
- `references/cli-harnesses.md`
- `references/compatibility-matrix.md`
- `references/verdict-format.md`

If the repo has any of these files and they matter to the change, read them before prompting reviewers:

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `brain/principles.md`

## Workflow

1. Identify the review target: diff, staged changes, PR branch, implementation plan, or a tight file list.
2. Write one sentence of intent: what the author is trying to achieve.
3. Gather the smallest useful context:
   - primary diff or staged changes
   - directly touched files
   - 1-3 nearby dependency files when needed
   - repo principles or project rules
4. Assign reviewer lenses:
   - Codex reviewer -> Skeptic
   - Claude Code -> Architect
   - Gemini CLI -> Minimalist
5. Launch reviewers:
   - in a Codex host, prefer a fresh Codex subagent for the Codex reviewer
   - otherwise use `scripts/run_codex_reviewer.sh`
   - use `scripts/run_claude_reviewer.sh` for Claude Code
   - use `scripts/run_gemini_reviewer.sh` for Gemini CLI
6. Write each reviewer result to its own file, for example:
   - `.tmp/adversarial-review/codex-skeptic.md`
   - `.tmp/adversarial-review/claude-architect.md`
   - `.tmp/adversarial-review/gemini-minimalist.md`
7. Synthesize with `references/verdict-format.md`:
   - verify every expected output file exists and is non-empty
   - record missing reviewers, auth failures, timeouts, capacity failures, malformed output, or caller misuse under reviewer coverage or harness failures
   - reject reviewer claims about flags, auth, or runtime behavior unless they match current docs or local CLI evidence
   - reject weak or hand-wavy claims; keep only evidence-backed findings
   - make a lead judgment for each finding: `accept` or `reject` with a one-line rationale
8. Return `PASS`, `CONTESTED`, or `REJECT`.

## Defaults

- Prefer cross-family reviewer diversity first: Codex reviewer + Claude Code + Gemini CLI when all three are available.
- If only one reviewer path works, still run it and report reduced reviewer diversity.
- If Gemini is missing, unauthenticated, rate-limited, capacity-blocked, or times out, continue with Codex + Claude and report reduced reviewer diversity.
- Claude agent teams are researched but non-default. This skill is optimized for cross-family reviewer diversity, not same-family fan-out.
- Keep prompts compact. Let reviewers inspect the repo directly through their own tools.

## Guardrails

- Review only. Do not edit files, commit, or open a PR as part of this skill.
- In a Codex host, do not call Codex CLI recursively when a fresh Codex subagent is available.
- Do not use unsafe approval or sandbox bypass modes for reviewer runs.
- Do not silently drop a failed reviewer.
- Do not block the whole review on Gemini availability.
- In Claude print mode, describe the task directly. Do not rely on slash commands or skills.
- In Gemini plan mode, do not ask Gemini to implement anything or exit plan mode.
