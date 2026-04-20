# Compatibility Matrix

Last verified locally on April 20, 2026.

This matrix covers only the behaviors `adversarial-review` depends on.

| Surface | Behavior relied on | Current source of truth | Local verification | Default decision |
| --- | --- | --- | --- | --- |
| Strategy `cross-family` | Codex + Claude Code + Gemini reviewer paths when available | skill docs plus wrapper docs | doc pass plus wrapper smoke | default strategy |
| Strategy `native-provider` | provider-specific reviewer path when the runtime behavior itself is the subject | skill docs plus live probe where needed | doc pass plus provider probe | optional strategy |
| Claude CLI | headless `claude -p`, OAuth-compatible auth, prompt argument plus stdin context, JSON output, `--permission-mode plan`, strict MCP config, slash commands disabled, read/search tools only, `--no-session-persistence`, `--max-turns`, `--effort` | Claude CLI docs plus local `claude --help` and live probe | happy-path smoke, attached-context smoke, stubbed failure matrix | default Architect reviewer path |
| Claude agent teams | parallel same-family review exists | Claude agent teams docs | doc pass only | researched, non-default |
| Gemini CLI | headless `-p`, stream JSON output, `--approval-mode plan`, disposable copy sandbox by default, optional process sandbox when configured, session cleanup when persistence is observable, and explicit plan or memory caveats | Gemini CLI docs plus local `gemini --help` and live probe | happy-path smoke, attached-context smoke, stubbed failure matrix | default Minimalist reviewer path |
| Codex CLI | top-level `--ask-for-approval`, `codex exec`, read-only sandbox, `--json`, `--output-last-message`, `--ephemeral`, `--skip-git-repo-check` | Codex CLI docs plus local `codex --help` and `codex exec --help` | happy-path smoke, attached-context smoke, stubbed failure matrix | fallback Codex reviewer path outside Codex host |
| Codex subagents | parallel spawned reviewers, inherited sandbox and approval state in `codex-host`, no stronger isolation claim | Codex subagent docs plus live in-host probe | one live in-host reviewer flow | default Codex reviewer path in `codex-host` |

Notes:

- Doc drift and local CLI drift both matter. A reviewer claim survives only when it matches current docs or local CLI evidence.
- Claude agent teams are intentionally excluded from the default runtime because this skill optimizes for cross-family reviewer diversity.
- For provider-specific strictness, auth, session, or memory claims, prefer docs plus a live probe over help text alone when the local help is incomplete.
