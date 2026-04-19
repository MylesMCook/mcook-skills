# Reviewer Harness Defaults

Last verified locally on April 19, 2026 after checking current docs, local CLI help, wrapper smoke runs, and failure-path simulations.

## Common wrapper contract

All bundled reviewer wrappers expose the same base interface:

- `--repo PATH`
- `--prompt-file PATH`
- `--output-file PATH`
- optional `--stdin-file PATH`
- optional `--model MODEL`
- optional `--timeout-seconds N`

Shared wrapper behavior:

- canonicalize paths before any `cd`
- merge `--prompt-file` and `--stdin-file` into one attached input payload
- write a final markdown file plus raw sidecars next to it
- classify failures as `MISSING_CLI`, `AUTH_FAILURE`, `TIMEOUT`, `CAPACITY_FAILURE`, `MALFORMED_OUTPUT`, `CLI_FAILURE`, or `CALLER_MISUSE`

## Host -> default reviewer order

- Codex host -> Claude Code and Gemini CLI first, then a fresh Codex subagent to complete the trio
- Claude host -> Codex CLI and Gemini CLI first, then Claude Code to complete the trio
- Gemini host -> Codex CLI and Claude Code first, then Gemini CLI to complete the trio
- any other host -> Codex CLI, Claude Code, and Gemini CLI

## Default reviewer set

- small, medium, or risky change -> Skeptic + Architect + Minimalist when all three reviewer paths are available
- architecture plan -> Architect is mandatory
- deletion or simplification decision -> Minimalist is mandatory

## Availability policy

- In a Codex host, a fresh Codex subagent is the default Codex reviewer path.
- Outside a Codex host, or when subagents are unavailable, Codex CLI is the fallback Codex reviewer path.
- Codex reviewer and Claude Code are the primary reviewer dependencies.
- Gemini CLI is the default third reviewer when it is installed and authenticated.
- If Gemini is missing, unauthenticated, rate-limited, capacity-blocked, or times out, continue with Codex + Claude and report reduced reviewer diversity.

## Codex reviewer

In a Codex host, spawn a fresh Codex subagent for the Codex reviewer instead of invoking `codex exec` recursively.

Prompt it with:

- repo root and review scope
- assigned lens
- read-only instruction
- precise output contract from `references/reviewer-prompt.md`
- any compact diff, plan, or context file path it should inspect

Close the subagent after synthesis.

## Codex CLI fallback

Use `scripts/run_codex_reviewer.sh`.

Default behavior:

- `codex exec`
- read-only sandbox only
- approvals `never`
- `--json`
- `--output-last-message`
- `--ephemeral`
- wrapper timeout enabled
- auto-add `--skip-git-repo-check` when the target repo is not a git repo

Important notes:

- The wrapper rejects any `--sandbox` value other than `read-only`.
- Ambient plugin warnings or unrelated skill-load warnings are environment noise unless they cause the wrapper to fail.

## Claude Code

Use `scripts/run_claude_reviewer.sh`.

Default behavior:

- `claude -p`
- `--output-format json`
- `--no-session-persistence`
- `--permission-mode dontAsk`
- `--tools Read,Grep,Glob`
- `--disable-slash-commands`
- `--max-turns 10`
- `--effort medium`
- wrapper timeout enabled

Important notes:

- The wrapper uses direct prompts, not slash commands or skills.
- Attached context is piped through stdin instead of being expanded into one giant CLI argument.

## Gemini CLI

Use `scripts/run_gemini_reviewer.sh`.

Default behavior:

- `gemini -p`
- `--approval-mode plan`
- `--sandbox`
- `--output-format json`
- wrapper timeout enabled

Important notes:

- Gemini runs in read-only plan mode.
- Capacity or rate-limit failures are treated as reduced reviewer diversity, not silent drops.

## Claude agent teams

Claude agent teams are documented and useful for parallel same-family collaboration, including parallel code review. They are intentionally non-default here because this skill is built around cross-family reviewer diversity.
