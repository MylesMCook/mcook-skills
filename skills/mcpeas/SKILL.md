---
name: mcpeas
description: >-
  Build or heavily reshape a greenfield or mostly-greenfield MCP app around one
  opinionated default: a hosted TypeScript `mcp-use` MCP Apps project with
  Streamable HTTP at `/mcp`, deliberate `structuredContent`/`content`/`_meta`
  payload design, widget readiness from day one, and a bundled Codex harness
  (`AGENTS.md`, `.codex/*`, spec, golden prompts, local check script). Use when
  Codex should follow the MCPeas standard instead of comparing many MCP stack
  options. Do not use for generic MCP advice, MCPB-only packaging,
  stdio/local-only servers, or unrelated coding tasks.
---

# MCPeas

Use this skill when the job needs one strong default for MCP work, not a menu of architectures.

If the user wants broader option comparison or lighter OpenAI Apps SDK guidance, use `mcp-app-builder` instead.

## Default build path

For greenfield or mostly-greenfield work, default to:

- `npx create-mcp-use-app <project-name> --template mcp-apps`
- hosted Streamable HTTP at `/mcp`
- `mcp-use` server APIs
- Zod schemas with `.describe()` on every field
- intentional payload split across `structuredContent`, `content`, and `_meta`
- widget readiness even if the first release ships tool-only
- Codex harness files from this skill's `scripts/` and `templates/`

Do not ask the user to choose TypeScript vs Python vs Rust, hosted vs local, or widget vs no widget unless a hard stop applies.

## Hard stops

Use the smallest compatible deviation only when one of these is true:

1. The user explicitly requires Rust, Python, MCPB, stdio-only, or local desktop/filesystem/OS access.
2. You are modifying an existing production repo whose stack cannot reasonably host a small TypeScript MCP service.
3. The target client cannot call hosted Streamable HTTP and the task is specifically about that client.
4. Security, compliance, or deployment constraints make hosted HTTP impossible.

State the hard stop briefly. Do not turn the answer into a long alternatives comparison.

## Workflow

1. If docs, SDK APIs, versions, or platform behavior could matter, read `references/research-basis.md`.
2. Read `references/architecture-standard.md` before designing tools, routes, files, or widget boundaries.
3. Read `references/codex-harness.md` before adding Codex harness files or subagent guidance.
4. Write a concrete build spec in project docs or in your answer before coding:
   - user job and non-goals
   - golden prompts: 5 direct, 5 indirect, 5 negative
   - tool inventory with schemas, annotations, payload shape, and auth stance
   - widget plan, even if the first version does not need UI yet
   - deployment and validation gates
5. For new projects, scaffold with the `mcp-use` CLI. Do not hand-roll the initial server, widget build, package metadata, or inspector setup unless you are inside an existing repo that already owns those pieces.
6. Add or refresh the Codex harness:
   - use `python scripts/bootstrap_harness.py <project-dir> --name <project-name>` when possible
   - otherwise copy the matching files from `templates/`
7. Implement thin vertical slices:
   - mock data first
   - one tool per user job
   - one widget per visual task
   - auth only when the tool exposes user-specific data or performs writes
   - rate limits and cache for expensive or external calls
8. Validate with `references/quality-gates.md`.
9. Use `python scripts/check_project.py <project-dir>` as a local harness sanity check.
10. Final response must include changed files, commands run, gates passed or failed, and any remaining hard-stop-driven risk.

## Tool and payload rules

- Prefer kebab-case tool names unless an external schema requires an exact name.
- Descriptions should start with `Use this when...` and note when not to use the tool if ambiguity is likely.
- Split read and write tools.
- Prefer enums, bounds, and nullable behavior over broad free-form strings.
- Set `readOnlyHint`, `destructiveHint`, and `openWorldHint` truthfully.
- Keep `structuredContent` concise and model-safe.
- Put large, sensitive, or widget-only details in `_meta`.
- Never put secrets in tool results or widget state.

## Widget rules

- Use widgets for browsing, comparing, picking, visualizing, editing, or repeated interaction.
- Register MCP Apps resources with `text/html;profile=mcp-app`.
- Version widget resource URIs when the bundle contract changes.
- Treat the MCP Apps bridge as baseline. Treat `window.openai` as optional ChatGPT-specific enhancement and feature-detect it.

## Load on demand

Read only what the current task needs:

- `references/research-basis.md`
- `references/architecture-standard.md`
- `references/codex-harness.md`
- `references/quality-gates.md`
- `scripts/bootstrap_harness.py`
- `scripts/check_project.py`
- files under `templates/`
