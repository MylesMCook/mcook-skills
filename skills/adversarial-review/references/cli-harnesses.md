# Reviewer Harness Defaults

Last verified locally on April 20, 2026 after checking current docs, local CLI help, wrapper smoke runs, and failure-path simulations.

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
- use `--prompt-file` for the primary prompt and `--stdin-file` for attached review context when the CLI supports that split
- write a final markdown file plus raw sidecars next to it
- classify failures as `MISSING_CLI`, `AUTH_FAILURE`, `TIMEOUT`, `CAPACITY_FAILURE`, `MALFORMED_OUTPUT`, `INPUT_ERROR`, `TURN_LIMIT`, `CLI_FAILURE`, `CALLER_MISUSE`, or `CLEANUP_FAILURE`

## Strategy names

- `cross-family` is the default strategy. Use Codex, Claude Code, and Gemini reviewer paths when available.
- `native-provider` is optional. Use a provider's own reviewer path when the task is specifically about that provider's runtime behavior or when the cross-family path is unavailable.
- Treat official docs as the baseline source. Use a local probe when the docs are incomplete or the claim depends on current CLI behavior.

## Host -> default reviewer order

- `codex-host` -> Claude Code and Gemini CLI first, then a fresh Codex subagent to complete the trio
- `claude-code` -> Codex CLI and Gemini CLI first, then Claude Code to complete the trio
- `gemini-cli` -> Codex CLI and Claude Code first, then Gemini CLI to complete the trio
- `openai-chatgpt` or `unknown` -> Codex CLI, Claude Code, and Gemini CLI

## Default reviewer set

- small, medium, or risky change -> Skeptic + Architect + Minimalist when all three reviewer paths are available
- architecture plan -> Architect is mandatory
- deletion or simplification decision -> Minimalist is mandatory

## Availability policy

- In `codex-host`, a fresh Codex subagent is the default Codex reviewer path.
- Outside `codex-host`, or when subagents are unavailable, Codex CLI is the fallback Codex reviewer path.
- Codex reviewer and Claude Code are the primary reviewer dependencies.
- Gemini CLI is the default third reviewer when it is installed and authenticated.
- If Gemini is missing, unauthenticated, rate-limited, capacity-blocked, or times out, continue with Codex + Claude and report reduced reviewer diversity.

## Codex reviewer

In `codex-host`, spawn a fresh Codex subagent for the Codex reviewer instead of invoking `codex exec` recursively.

Prompt it with:

- repo root and review scope
- assigned lens
- read-only instruction
- precise output contract from `references/reviewer-prompt.md`
- any compact diff, plan, or context file path it should inspect

Close the subagent after synthesis.

Important notes:

- A Codex host subagent inherits the parent sandbox and approval state. Do not describe it as stronger isolation than the parent actually provides.
- Treat the host subagent path as read-only only when the surrounding session already enforces that.
- If the review depends on a stricter Codex runtime claim, verify it with current docs or a live probe before writing it down.

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
- `codex exec` still needs current auth and CLI availability; missing CLI or auth becomes `MISSING_CLI` or `AUTH_FAILURE`.
- Ambient plugin warnings or unrelated skill-load warnings are environment noise unless they cause the wrapper to fail.

## Claude Code

Use `scripts/run_claude_reviewer.sh`.

Default behavior:

- `claude -p`
- `--output-format json`
- `--no-session-persistence`
- `--permission-mode plan`
- `--strict-mcp-config`
- `--disable-slash-commands`
- `--tools Read,Grep,Glob`
- `--allowedTools Read,Grep,Glob`
- `--max-turns 10`
- `--effort medium`
- wrapper timeout enabled

Important notes:

- The wrapper uses direct prompts, not slash commands or skills.
- OAuth login is supported by default. Do not require an API key for normal reviewer use.
- `--bare` is not the default because Claude Code documents that it never reads OAuth or keychain auth. Use it only for an explicitly API-key/helper-backed environment.
- `claude --help` is incomplete for some flags. Use current docs plus a live probe when the claim depends on current print-mode behavior.
- `--no-session-persistence` keeps the run from being resumed later. Keep that behavior in the wrapper contract.
- If the current claim depends on hook, memory, or auth behavior, confirm it with a live probe. `claude --help` is not enough on its own.

## Gemini CLI

Use `scripts/run_gemini_reviewer.sh`.

Default behavior:

- `gemini -p`
- `--approval-mode plan`
- disposable copy sandbox by default, so the real repo is never the Gemini working directory
- `--output-format stream-json`
- delete any persisted session after the run when one appears in the project session list
- wrapper timeout enabled

Important notes:

- `--approval-mode plan` is not inherently read-only. Treat it as plan mode, not as a blanket guarantee against writes or persistence.
- Gemini process sandboxing is optional and must be requested with `ADVERSARIAL_REVIEW_GEMINI_SANDBOX_MODE=process`. That path requires the local Gemini sandbox backend to work.
- Explicitly forbid `save_memory`, plan exit, task-tracker writes, skill activation, session-resume behavior, and mutating actions in the prompt when the review must stay read-only.
- Verify current memory, session, and plan behavior with a local probe before turning it into a hard claim.
- When a session shows up in `--list-sessions`, cleanup failure is a hard failure. If the session does not appear in the list, treat that as already clean.
- Capacity or rate-limit failures are treated as reduced reviewer diversity, not silent drops.

## Claude agent teams

Claude agent teams are documented and useful for parallel same-family collaboration, including parallel code review. They are intentionally non-default here because this skill is built around cross-family reviewer diversity.
