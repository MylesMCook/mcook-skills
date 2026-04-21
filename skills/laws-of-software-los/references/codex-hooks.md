# Codex Always-On LOS Code Hooks

This skill includes an optional Codex hook suite that makes the architecture laws closer to always-on during coding sessions.

The hooks are intentionally deterministic and dependency-free. They do not replace human review or repository-specific CI, but they raise the floor by adding context before generation, blocking obviously destructive shell commands, reviewing command results, and running a final diff/generated-code gate before Codex stops.

## What the hooks enforce

| Hook | Purpose | LOS effect |
|---|---|---|
| `SessionStart` | Injects durable developer context at startup/resume. | Makes LOS mode active before the first answer. |
| `UserPromptSubmit` | Adds turn-specific generation constraints. | Pushes the initial code output toward simplicity, reversibility, tests, timeouts, migration safety, compatibility, and observability. |
| `PreToolUse` | Reviews Bash commands before execution. | Blocks broad deletes, force pushes, destructive database commands, remote-code pipes, unsafe TLS flags, and similar footguns. |
| `PermissionRequest` | Allows safe validation/read commands, denies known-dangerous commands. | Reduces friction for tests/lints while keeping risky escalation visible. |
| `PostToolUse` | Reviews validation output and current diff after Bash. | Stops the model from treating failed tests or high-risk diff findings as success. |
| `Stop` | Runs the final LOS gate on changed files and generated code blocks. | Forces one continuation when high-risk issues remain before final output. |

## Install

From the skill root:

```bash
python3 scripts/install_codex_hooks.py --repo /path/to/repo
```

For all Codex sessions on the machine:

```bash
python3 scripts/install_codex_hooks.py --scope global
```

Development mode with live symlinks:

```bash
python3 scripts/install_codex_hooks.py --repo /path/to/repo --mode symlink
```

Dry run:

```bash
python3 scripts/install_codex_hooks.py --repo /path/to/repo --dry-run
```

Print the hook JSON without installing:

```bash
python3 scripts/install_codex_hooks.py --scope repo --print-hooks-json
```

The installer:

1. Copies hook scripts into `.codex/hooks/laws-of-software-los/` or `~/.codex/hooks/laws-of-software-los/`.
2. Merges hook groups into `.codex/hooks.json` or `~/.codex/hooks.json`.
3. Enables the required feature flag in `.codex/config.toml` or `~/.codex/config.toml`:

```toml
[features]
codex_hooks = true
```

If an existing `hooks.json` is modified, the installer writes a numbered `.bak` file first.

## Manual install

Repo-local hooks can also be installed manually:

```bash
mkdir -p .codex/hooks/laws-of-software-los
cp scripts/los_code_gate.py scripts/codex_hooks/*.py .codex/hooks/laws-of-software-los/
cp assets/codex-hooks/hooks.repo.json .codex/hooks.json
cat >> .codex/config.toml <<'TOML'

[features]
codex_hooks = true
TOML
```

Use `assets/codex-hooks/hooks.global.json` for a global install under `~/.codex`.

## LOS Code Gate checks

Run directly:

```bash
python3 scripts/los_code_gate.py --repo . --changed
python3 scripts/los_code_gate.py --repo . --changed --json
python3 scripts/los_code_gate.py --input path/to/file.py
python3 scripts/los_code_gate.py --stdin < assistant-output.md
```

The gate checks for high-signal engineering law violations:

- Hardcoded secrets and private keys.
- Disabled TLS, auth/security bypass language, wildcard credentialed CORS.
- Dynamic execution and shell injection risks.
- SQL string interpolation near query/execute calls.
- Remote calls without timeout/cancellation policy.
- Queue/event/distributed flows without idempotency, retry/backoff, DLQ, timeout, or backpressure.
- Caches without TTL/invalidation/staleness/source-of-truth policy.
- Schema/data migrations without rollback, transaction, backup, reconciliation, or expand/contract strategy.
- API-surface changes without tests/compatibility/deprecation/contract coverage.
- Production code changes without adjacent tests.
- Silent exception swallowing and unbounded loops.

## Tuning guidance

Use the hooks as a baseline. For a real repository, add project-specific checks:

- Required test commands and package-manager conventions.
- Approved secrets/config APIs.
- Framework-specific route and migration patterns.
- Organization-specific API compatibility rules.
- Service ownership and observability requirements.
- Deployment environment safety rules.

Prefer adding narrow checks over weakening broad ones. If a hook blocks legitimate work, make the safe path explicit rather than bypassing the hook.

## Limitations

Codex hooks are an enforcement aid, not a security boundary. Current Codex hook behavior has important constraints:

- Hooks are experimental and Windows support is disabled.
- Hook files are discovered next to active Codex config layers, most usefully `~/.codex/hooks.json` or `<repo>/.codex/hooks.json`.
- Matching hooks from multiple files all run.
- `PreToolUse`, `PermissionRequest`, and `PostToolUse` currently match Bash; they do not intercept every possible file write, MCP call, web search, or non-shell tool.
- `PostToolUse` cannot undo side effects from a command that already ran.
- `Stop` continuation can push the model to fix issues before final output, but it is still a feedback loop, not a mathematical guarantee.

Because of those limits, the skill also instructs the agent to run the gate directly and to use normal repository CI/tests.
