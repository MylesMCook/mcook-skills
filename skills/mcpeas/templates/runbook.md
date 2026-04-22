# MCPeas runbook

## Local development

```bash
npm install
npm run dev
```

Open the MCP Inspector against the local `/mcp` endpoint.

## Build

```bash
npm run build
```

## Smoke tests

1. Run all direct golden prompts.
2. Run all indirect golden prompts.
3. Run all negative prompts and confirm the app refuses or routes away safely.
4. Check widget interactions, mobile layout, loading states, and error states.
5. Confirm no secrets appear in tool results, logs, widget state, or committed files.

## Release checks

- Production endpoint is HTTPS.
- Auth path has been tested with success, expiry, and denied states.
- Tool annotations are truthful.
- Widget CSP and domain are declared.
- Rate limits and external API failures are graceful.
- `docs/mcpeas/spec.md` matches implementation.
- `evals/golden-prompts.json` reflects current behavior.
