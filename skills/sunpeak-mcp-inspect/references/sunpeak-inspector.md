# Sunpeak Inspector Reference

Use this when you need exact Sunpeak flag, URL, fixture, or test recall.
Prefer project docs and `sunpeak inspect --help` if they disagree.

## Common commands

```bash
sunpeak inspect --server <url-or-command>
sunpeak inspect --server http://localhost:8000/mcp --simulations tests/simulations --port 3000 --name "My App"
sunpeak test
sunpeak test --e2e
sunpeak test --visual
sunpeak test --visual --update
```

- `--server` is required.
- `--simulations` points at the fixture directory.
- `--port` defaults to `3000`.
- `--cwd` and repeatable `--env KEY=VALUE` may be available for stdio servers.
- Project `dev` scripts often start the inspector at `localhost:3000` and the
  MCP server at `localhost:8000`, but project docs and scripts win.

## Useful URL parameters

- `tool=<name>` for real-call workflows
- `simulation=<name>` for fixture workflows
- `host=chatgpt|claude`
- `theme=light|dark`
- `displayMode=inline|pip|fullscreen`
- `deviceType=mobile|tablet|desktop|unknown`
- `touch=true|false`
- `hover=true|false`
- `sidebar=false`
- `devOverlay=false`
- `prodResources=true`

## Minimal simulation shape

```json
{
  "tool": "search",
  "toolInput": { "query": "headphones" },
  "toolResult": {
    "content": [{ "type": "text", "text": "Results returned." }],
    "structuredContent": { "results": [{ "name": "Example" }] }
  },
  "serverTools": {
    "review": { "structuredContent": { "status": "success" } }
  }
}
```

- `tool` is the Sunpeak tool file name or MCP tool name.
- `toolResult.structuredContent` is what the app reads via `useToolData()`.
- `serverTools` mocks app-initiated `callServerTool` calls.

## Fixture test reminders

```ts
const protocol = await mcp.callTool('search', { query: 'headphones' });
const rendered = await inspector.renderTool('search', { query: 'headphones' }, {
  theme: 'dark',
  displayMode: 'fullscreen',
});
await expect(rendered.app().locator('text=headphones')).toBeVisible();
```

- `mcp.*` is protocol-only.
- `inspector.renderTool()` renders the app.
- `result.app()` scopes to the app iframe.
- Treat `source: "fixture"` as simulation evidence and `source: "server"` as
  live evidence.
