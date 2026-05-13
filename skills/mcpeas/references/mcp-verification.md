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

`mcpjam apps conformance` runs a 7-check server-side validation of the MCP Apps surface. Descriptions are taken verbatim from the CLI output:

1. `ui-tools-present` — at least one tool advertises MCP Apps UI metadata through `_meta.ui.resourceUri` (or the deprecated `ui/resourceUri`).
2. `ui-tool-metadata-valid` — tools with UI metadata use a `ui://` resource URI and valid `visibility` values.
3. `ui-tool-input-schema-valid` — UI tools provide a non-null JSON Schema object as their `inputSchema`.
4. `ui-listed-resources-valid` — UI resources returned by `resources/list` use `ui://` URIs and the MCP Apps HTML MIME type.
5. `ui-resources-readable` — every UI resource referenced by a tool or listed by the server can be fetched with `resources/read`.
6. `ui-resource-contents-valid` — UI resource contents use the MCP Apps HTML MIME type (`text/html;profile=mcp-app`) and provide exactly one HTML payload via `text` or `blob`.
7. `ui-resource-meta-valid` — UI resource metadata uses valid `csp`, `permissions`, `domain`, and `prefersBorder` shapes.

Exits 0 on all passing, 1 on any failure. This is **server-side** conformance only — host behaviors like `ui/initialize`, sandbox proxying, and display-mode handling are not validated.

## CI usage

```bash
# Emit JUnit XML for CI reporters
mcpjam apps conformance --url <URL> --reporter junit-xml > apps-report.xml
```
