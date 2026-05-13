# MCP Local Verification

Default local verification tool: `mcpjam` — stateless, fast, CLI-only. No browser needed.

Docs: https://docs.mcpjam.com

## Install

```bash
npm i -g @mcpjam/cli
```

## Commands

```bash
# Health check: probe, connect, capabilities sweep
mcpjam server doctor --url http://127.0.0.1:8765/mcp --quiet --format json

# MCP Apps conformance — 7-check suite (see below)
mcpjam apps conformance --url <URL> --quiet --format json

# Inspect tools / resources
mcpjam tools list     --url <URL> --quiet --format json
mcpjam tools call     --url <URL> --tool-name <NAME> --tool-args '{...}' --quiet --format json
mcpjam resources list --url <URL> --quiet --format json
mcpjam resources read --url <URL> --uri <ui://...> --quiet --format json
```

## Apps conformance checks

`mcpjam apps conformance` validates the dual-namespace `_meta` and `ui://` resource wiring required by MCP Apps:

1. `ui-tools-present` — at least one ui-tool is declared.
2. `ui-tool-metadata-valid` — `_meta` contains valid `ui.resourceUri` and `openai/outputTemplate`.
3. `ui-tool-input-schema-valid` — input schemas are well-formed JSON Schema.
4. `ui-listed-resources-valid` — `ui://` resources appear in the resource list.
5. `ui-resources-readable` — each `ui://` resource responds to a read request.
6. `ui-resource-contents-valid` — resource contents are non-empty.
7. `ui-resource-meta-valid` — resource MIME is `text/html;profile=mcp-app`.

Exits 0 on all passing, 1 on any failure.

## CI usage

```bash
# Emit JUnit XML for CI reporters
mcpjam apps conformance --url <URL> --reporter junit-xml > apps-report.xml
```
