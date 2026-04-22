# AGENTS.md

## MCPeas project contract

This repository follows the MCPeas MCP build standard.

Work in this order:
1. Read `docs/mcpeas/spec.md`.
2. Inspect existing code before proposing new files.
3. Prefer the generated `mcp-use` project structure. Do not hand-roll server, widget, build, or inspector boilerplate when the scaffold already provides it.
4. Implement mock-first, then replace mocks with real integrations behind the same schemas.
5. Keep one tool focused on one user job.
6. Preserve the payload boundary:
   - `structuredContent`: concise, schema-shaped, model-safe data.
   - `content`: natural-language explanation for the model and transcript.
   - `_meta`: widget-only or large details; never secrets.
7. Use widgets for browsing, comparing, selecting, visualizing, editing, or repeated interaction.
8. Never commit secrets, credentials, personal tokens, raw private data, or production-only config.

## Required project files

- `docs/mcpeas/spec.md`
- `evals/golden-prompts.json`
- `.codex/config.toml`
- `.codex/agents/code-mapper.toml`
- `.codex/agents/docs-researcher.toml`
- `.codex/agents/mcp-reviewer.toml`
- `scripts/mcpeas_check.py`

## Commands

Use the commands that exist in this repository. For the default scaffold, prefer:

```bash
npm run dev
npm run build
npm test
npx @modelcontextprotocol/inspector@latest
python scripts/mcpeas_check.py .
```

## Review standard

Before final handoff, report:

- files changed
- commands run
- golden prompts updated or skipped with reason
- quality gates passed or failed
- risks that still need human review

## Codex subagent guidance

Use subagents only when they make the work better, not to create ceremony.

Recommended prompts:

- `code_mapper`: "Map the MCP server, tools, widget resources, auth paths, and test commands. Return only file paths and risks."
- `docs_researcher`: "Verify the current docs for the APIs touched here. Return only source-backed constraints and examples."
- `mcp_reviewer`: "Review tool schemas, annotations, payload split, widget registration, auth, and quality gates. Return blockers first."
