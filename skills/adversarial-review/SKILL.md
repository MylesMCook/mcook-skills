---
name: adversarial-review
description: Use this skill when you need a serious code review, diff review, or implementation-plan review from independent reviewers. In Codex hosts, use a fresh Codex subagent for the Codex reviewer; otherwise fall back to Codex CLI, Claude Code, and Gemini CLI when available. Synthesizes a PASS, CONTESTED, or REJECT verdict.
compatibility: Requires git and at least one independent reviewer path. CLI fallback reviewers require bash, python3, and authenticated reviewer CLIs. Gemini CLI (`gemini`) is optional.
metadata:
  author: mcook-skills
  version: "1.1.2"
---

# Adversarial Review

Use this skill to get adversarial review from independent reviewers instead of same-thread validation.

## Defaults

- Prefer host subagents for same-host Codex review and the bundled CLI harness scripts for external CLI reviewers. Do not hand-assemble raw CLI commands.
- Default reviewer set is Codex reviewer + Claude Code + Gemini CLI when all three reviewer paths are available.
- Prefer cross-family reviewers first:
  - host Codex -> Claude Code and Gemini CLI first, then a fresh Codex subagent to complete the trio
  - host Claude Code -> Codex CLI and Gemini CLI first, then Claude Code to complete the trio
  - host Gemini CLI -> Codex CLI and Claude Code first, then Gemini CLI to complete the trio
  - any other host -> Codex CLI + Claude Code + Gemini CLI by default
- If only one primary harness is available, still run it and report reduced reviewer diversity.
- Run all three reviewers for small changes too when they are available.
- If Gemini is missing, unauthenticated, or fails, continue with Codex + Claude and report reduced reviewer diversity.
- In a Codex host, do not call the Codex CLI recursively just to get a Codex reviewer. Spawn a fresh Codex subagent when the host exposes subagents; use `scripts/run_codex_reviewer.sh` only as fallback when subagents are unavailable or the host is not Codex.
- Do not substitute same-model subagents for external CLI diversity except for the Codex-hosted Codex reviewer case above.

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
4. Keep prompts small. Let Codex, Claude, and Gemini inspect the repo directly through their reviewer paths.
5. Never dump the whole repo into the prompt.

## Assign reviewers

Default lens assignment:

- Codex reviewer -> Skeptic
- Claude Code -> Architect
- Gemini CLI -> Minimalist

Reassign only when the task clearly needs it. Good examples:

- security or correctness heavy -> put the strongest available harness on Skeptic
- architecture or refactor plan -> put Claude Code or Codex on Architect
- overengineering, sprawl, or deletion question -> use Gemini on Minimalist when available; otherwise assign Minimalist to the strongest remaining reviewer

## Launch reviewers

Use host subagents for the Codex reviewer when running inside Codex. Use the bundled scripts for CLI reviewers instead of raw CLI calls.

### Codex reviewer

When the host is Codex and fresh subagents are available, spawn one fresh Codex subagent for the Codex reviewer. Give it the reviewer prompt, repo root, assigned lens, read-only scope, and output contract. Ask it to report findings directly in the same markdown format used by the CLI harnesses. Close it after synthesis.

If the host is not Codex, or Codex subagents are unavailable, use `scripts/run_codex_reviewer.sh` as the fallback Codex reviewer path.

The fallback script uses `codex exec` in non-interactive mode with a read-only sandbox, no approval prompts, a structured raw log, and a separate final markdown output file.

### Claude Code

Use `scripts/run_claude_reviewer.sh` for Claude reviewers.

It already uses `claude -p` in print mode, disables session persistence, caps turns, and runs in locked-down read-only mode with only the tools needed for review.

### Gemini CLI

Use `scripts/run_gemini_reviewer.sh` for the default Minimalist reviewer when Gemini CLI is installed and authenticated.

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
3. Treat Gemini failure as non-fatal when Codex and Claude completed successfully, but record the reduced reviewer diversity.
4. Deduplicate overlapping findings.
5. Reject weak or hand-wavy claims. Keep only findings with evidence, concrete failure scenarios, or direct file references.
6. Produce the final verdict using `references/verdict-format.md`.
7. For each finding, make a lead judgment: accept or reject with a one-line rationale.

## Guardrails

- Review only. Do not make code changes, do not commit, and do not open a PR as part of this skill.
- Do not use `codex --full-auto`, `codex --yolo`, `claude --permission-mode bypassPermissions`, `claude --dangerously-skip-permissions`, `gemini --approval-mode yolo`, or `gemini -y` for reviewer runs.
- Do not invoke Codex CLI from inside a Codex host when a fresh Codex subagent is available.
- Do not silently drop a failed reviewer.
- Do not block the whole review on Gemini availability.
- Do not spend turns rediscovering CLI syntax. The scripts already encode the default harness behavior.
- In Claude print mode, do not tell Claude to use slash commands or skills. Describe the task directly.
- In Gemini plan mode, do not ask Gemini to implement anything or exit plan mode.
