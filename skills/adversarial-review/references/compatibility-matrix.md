# Compatibility Matrix

Last verified locally on April 19, 2026.

This matrix covers only the behaviors `adversarial-review` depends on.

| Surface | Behavior relied on | Current source of truth | Local verification | Default decision |
| --- | --- | --- | --- | --- |
| Claude CLI | headless `claude -p`, piped stdin context, JSON output, `--tools`, `--permission-mode`, `--no-session-persistence`, `--max-turns`, `--effort`, `--disable-slash-commands` | Claude CLI docs plus local `claude --help` | happy-path smoke, attached-context smoke, stubbed failure matrix | default Architect reviewer path |
| Claude agent teams | parallel same-family review exists | Claude agent teams docs | doc pass only | researched, non-default |
| Gemini CLI | headless `-p`, JSON output, `--approval-mode plan`, `--sandbox` | Gemini CLI docs plus local `gemini --help` | happy-path smoke, attached-context smoke, stubbed failure matrix | default Minimalist reviewer path |
| Codex CLI | `codex exec`, read-only sandbox, `--json`, `--output-last-message`, `--ephemeral`, `--skip-git-repo-check` | Codex CLI docs plus local `codex exec --help` | happy-path smoke, attached-context smoke, stubbed failure matrix | fallback Codex reviewer path outside Codex host |
| Codex subagents | parallel spawned reviewers, inherited sandbox, read-only reviewer route in Codex host | Codex subagent docs | one live in-host reviewer flow | default Codex reviewer path in Codex host |

Notes:

- Doc drift and local CLI drift both matter. A reviewer claim survives only when it matches current docs or local CLI evidence.
- Claude agent teams are intentionally excluded from the default runtime because this skill optimizes for cross-family reviewer diversity.
