---
name: adversarial-review
description: Use this skill when you need a serious code review, diff review, or implementation-plan review from external CLI reviewers. It defaults to Codex CLI and Claude Code, can add Gemini CLI as an optional third reviewer, and synthesizes a PASS, CONTESTED, or REJECT verdict.
compatibility: Requires bash, python3, git, and at least one authenticated primary reviewer CLI (`codex` or `claude`). Gemini CLI (`gemini`) is optional.
metadata:
  author: mcook-skills
  version: "1.1.1"
---

# Adversarial Review

Use this skill to get adversarial review from external CLI reviewers instead of same-thread validation.

## Defaults

- Prefer the bundled CLI harness scripts instead of hand-assembling raw CLI commands.
- Default reviewer pair is Codex CLI + Claude Code.
- Prefer cross-family reviewers first:
  - host Codex -> Claude Code, then Gemini CLI only if installed and verified, then Codex only as a fallback or tie-breaker
  - host Claude Code -> Codex CLI, then Gemini CLI only if installed and verified, then Claude only as a fallback or tie-breaker
  - host Gemini CLI -> Codex CLI + Claude Code first when available; Gemini only as a third reviewer or fallback when the other two are unavailable
  - any other host -> Codex CLI + Claude Code by default; add Gemini CLI only when installed and verified
- If only one primary harness is available, still run it and report reduced reviewer diversity.
- For small changes, run Codex + Claude when both are available.
- For medium, risky, or architectural changes, add Gemini as a third reviewer only when available and the harness has passed a quick smoke test in the current environment.
- Do not substitute same-model subagents when an external CLI harness is available.

## First read

Open these files before launching reviewers:

- `references/reviewer-lenses.md`
- `references/reviewer-prompt.md`
- `references/cli-harnesses.md`
- `references/verdict-format.md`

If the repo has any of these files and they are relevant, read them before prompting reviewers:

- `brain/principles.md`
- `CLAUDE.md`
- `AGENTS.md`
- `GEMINI.md`

## Build the review scope

1. Identify the object of review: diff, staged changes, PR branch, implementation plan, or a tight file list.
2. Write one sentence of intent: what the author is trying to achieve.
3. Gather the smallest useful context:
   - primary diff or staged changes
   - directly touched files
   - 1-3 nearby dependency files when needed
   - repo principles or project rules
4. Keep prompts small. Let Codex and Claude inspect the repo directly. Only add Gemini when the extra dissent or minimalist pressure is worth the extra harness complexity.
5. Never dump the whole repo into the prompt.

## Assign reviewers

Default lens assignment:

- Codex CLI -> Skeptic
- Claude Code -> Architect
- Gemini CLI -> Minimalist (optional third reviewer)

Reassign only when the task clearly needs it. Good examples:

- security or correctness heavy -> put the strongest available harness on Skeptic
- architecture or refactor plan -> put Claude Code or Codex on Architect
- overengineering, sprawl, or deletion question -> use Gemini on Minimalist when available; otherwise assign Minimalist to the strongest remaining reviewer

## Launch reviewers

Use the bundled scripts instead of raw CLI calls.

### Codex CLI

Use `scripts/run_codex_reviewer.sh` for Codex reviewers.

It already uses `codex exec` in non-interactive mode with a read-only sandbox, no approval prompts, a structured raw log, and a separate final markdown output file.

### Claude Code

Use `scripts/run_claude_reviewer.sh` for Claude reviewers.

It already uses `claude -p` in print mode, disables session persistence, caps turns, and runs in locked-down read-only mode with only the tools needed for review.

### Gemini CLI

Use `scripts/run_gemini_reviewer.sh` only as an optional third reviewer or fallback.

It already uses headless `gemini -p`, sandboxing, and read-only plan mode guardrails so the run stays review-only.

### Output locations

Write each reviewer result to its own file, for example:

- `.tmp/adversarial-review/codex-skeptic.md`
- `.tmp/adversarial-review/claude-architect.md`
- `.tmp/adversarial-review/gemini-minimalist.md`

Keep matching raw logs next to them when a harness emits structured output.

## Synthesis

1. Verify every expected output file exists and is non-empty.
2. If a harness failed, include that failure explicitly under reviewer coverage or harness failures.
3. Treat Gemini failure as non-fatal when Codex or Claude completed successfully.
4. Deduplicate overlapping findings.
5. Reject weak or hand-wavy claims. Keep only findings with evidence, concrete failure scenarios, or direct file references.
6. Produce the final verdict using `references/verdict-format.md`.
7. For each finding, make a lead judgment: accept or reject with a one-line rationale.

## Guardrails

- Review only. Do not make code changes, do not commit, and do not open a PR as part of this skill.
- Do not use `codex --full-auto`, `codex --yolo`, `claude --permission-mode bypassPermissions`, `claude --dangerously-skip-permissions`, `gemini --approval-mode yolo`, or `gemini -y` for reviewer runs.
- Do not silently drop a failed reviewer.
- Do not block the whole review on optional Gemini availability.
- Do not spend turns rediscovering CLI syntax. The scripts already encode the default harness behavior.
- In Claude print mode, do not tell Claude to use slash commands or skills. Describe the task directly.
- In Gemini plan mode, do not ask Gemini to implement anything or exit plan mode.
