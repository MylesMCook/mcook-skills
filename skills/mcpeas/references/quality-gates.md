# MCPeas Quality Gates

Run these gates before final handoff. Mark each PASS, FAIL, or NOT RUN with evidence.

## Gate 1: Source freshness

Pass when current docs were checked for any unstable dependency:
- Agent Skills packaging/discovery
- OpenAI Apps SDK
- MCP protocol
- mcp-use
- Codex config, skills, subagents, MCP
- deployment host and auth provider docs

## Gate 2: Spec exists

Pass when `docs/mcpeas/spec.md` includes:
- user job and non-goals
- 5 direct prompts
- 5 indirect prompts
- 5 negative prompts
- tool inventory
- widget plan
- auth/storage/deployment stance
- test plan

## Gate 3: Tool surface

Pass when every tool:
- has one job
- has an action-oriented name
- starts its description with "Use this when..."
- has Zod validation and `.describe()` on fields
- has accurate annotations
- handles expected errors with a graceful error response
- declares or documents output shape

## Gate 4: Payload boundaries

Pass when:
- model-visible `structuredContent` is compact and non-secret
- `content` is short and useful or absent
- `_meta` is only widget/host detail and contains no secrets
- output schemas are used where practical

## Gate 5: Widget readiness

Pass when widget-backed features:
- use MCP Apps-compatible resource MIME type
- define bridge behavior
- define CSP and resource domains
- avoid relying on `window.openai` for portable baseline behavior
- feature-detect ChatGPT-only enhancements
- handle loading, empty, error, and mobile states

## Gate 6: Security

Pass when:
- no secrets are hardcoded
- `.env.example` documents required variables
- destructive tools require explicit user intent and accurate annotations
- auth is enforced server-side, not from client hints
- external calls are rate-limited/cached when needed
- logs avoid tokens and private data

## Gate 7: Codex harness

Pass when:
- `AGENTS.md` exists
- `.codex/config.toml` exists with bounded subagent settings
- focused custom agents exist
- `docs/mcpeas/runbook.md` and `docs/mcpeas/research.md` exist
- `docs/mcpeas/tool-inventory.md` exists or the tool inventory lives somewhere equally explicit
- golden prompts exist
- local check script runs
- docs/runbook tells Codex how to reproduce the app

## Gate 8: Validation

Minimum local validation:
- package install succeeded
- typecheck/build succeeded
- unit tests or handler tests ran
- `mcpjam server doctor --url <URL> --quiet --format json` passed (or explicitly not run with reason)
- `mcpjam apps conformance --url <URL> --quiet --format json` passed 7/7 for MCP Apps work (or explicitly not run with reason)
- ChatGPT developer mode was used for HTTPS apps or explicitly not run with reason
- golden prompts were evaluated or explicitly queued with reason

See `references/mcp-verification.md` for mcpjam install, all commands, CI/JUnit flags.

## Handoff format

```md
Changed files:
- ...

Commands run:
- `...` — PASS/FAIL

Gates:
- Gate 1 Source freshness — PASS (...)
- ...

Remaining risks:
- ...
```
