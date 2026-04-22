# Codex Harness for MCPeas Projects

The harness exists to make Codex reliable across long MCP builds: stable instructions, bounded subagents, repeatable checks, and artifact-based handoffs.

## Files to add

```text
AGENTS.md
.codex/config.toml
.codex/agents/code-mapper.toml
.codex/agents/docs-researcher.toml
.codex/agents/mcp-reviewer.toml
docs/mcpeas/spec.md
docs/mcpeas/runbook.md
docs/mcpeas/research.md
evals/golden-prompts.json
scripts/mcpeas_check.py
```

Use `scripts/bootstrap_harness.py <project-dir> --name <project-name>` from this skill when possible.

## AGENTS.md intent

The project `AGENTS.md` should say:
- use MCPeas for all MCP/app/widget work
- update `docs/mcpeas/spec.md` before broad changes
- keep changes small and test-backed
- do not hand-roll generated mcp-use boilerplate
- never commit secrets
- prefer mock data before production integrations
- run the local check command before final handoff

## Custom agents

Use focused Codex subagents only when their work can proceed independently.

### code-mapper

Read-only. Finds entry points, schemas, tool handlers, widget resources, tests, and deployment config. Returns file/symbol evidence.

### docs-researcher

Read-only. Verifies current API behavior in official docs. Use it when SDK, MCP, Apps SDK, auth, deployment, or Codex behavior may have changed.

### mcp-reviewer

Read-only. Reviews the implemented MCP surface for tool quality, payload boundaries, widget safety, auth, errors, and test coverage.

## Suggested prompts

```text
Have code-mapper inspect this repo and return the current MCP surface: tools, resources, widgets, auth, tests, and deployment entry points. Do not edit files.
```

```text
Have docs-researcher verify the current mcp-use, Apps SDK, MCP protocol, and Codex config details that affect this change. Return only docs-backed deltas and links.
```

```text
Have mcp-reviewer review the changes against docs/mcpeas/spec.md and evals/golden-prompts.json. Return blocking issues first with file references.
```

## Bounded fan-out

Use at most three subagents for normal MCPeas work:
1. code-mapper
2. docs-researcher
3. mcp-reviewer

Keep recursive spawning disabled. Prefer one parent agent implementing after the read-only agents report.

## Local MCP server config

The project `.codex/config.toml` may include a disabled local server entry:

```toml
[mcp_servers.mcpeas_local]
url = "http://127.0.0.1:3000/mcp"
enabled = false
startup_timeout_sec = 20
tool_timeout_sec = 45
```

Keep it disabled by default so Codex startup does not fail when the dev server is not running. Enable it only during local integration testing.

## Check command

Each project should expose one simple check command, usually:

```bash
python scripts/mcpeas_check.py .
```

That command should verify the harness files exist, package scripts are present, golden prompts are non-empty, and obvious payload/test docs exist. It is not a replacement for unit tests or MCP Inspector.
