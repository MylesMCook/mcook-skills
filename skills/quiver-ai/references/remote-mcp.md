# QuiverAI Remote MCP on Cloudflare

Use this path when the user wants QuiverAI exposed as reusable MCP tools instead of calling the API directly inside one app.

Primary docs:

- Cloudflare MCP overview: https://developers.cloudflare.com/agents/model-context-protocol/
- Remote MCP guide: https://developers.cloudflare.com/agents/guides/remote-mcp-server/
- Authorization: https://developers.cloudflare.com/agents/model-context-protocol/authorization/
- Testing: https://developers.cloudflare.com/agents/guides/test-remote-mcp-server/
- QuiverAI API intro: https://docs.quiver.ai/api-reference/introduction

## Recommendation

For QuiverAI, prefer a small remote MCP server on Cloudflare Workers rather than wrapping every endpoint.

Recommended tools:

- `quiver_list_models`
  - Calls `GET /v1/models`
  - Use to discover valid model IDs before generation
- `quiver_generate_svg`
  - Calls `POST /v1/svgs/generations`
  - Inputs should cover prompt, model, optional instructions, optional references, `n`, and sampling controls
- `quiver_vectorize_svg`
  - Calls `POST /v1/svgs/vectorizations`
  - Keep image input shape aligned with current Quiver docs when implementing

Keep tool descriptions concrete. Cloudflare recommends fewer, well-designed tools with scoped permissions over mirroring a full API.

## Auth Boundary

There are two separate auth concerns:

1. MCP client authorization
   - Remote MCP uses Streamable HTTP plus OAuth
   - Cloudflare supports Cloudflare Access, third-party OAuth providers, or your own OAuth flow
2. Upstream QuiverAI authentication
   - Quiver uses `Authorization: Bearer <QUIVERAI_API_KEY>`
   - Keep this key only on the Worker as a secret

Important: OAuth on the MCP server does not mean the client ever receives the Quiver API key.

## Default OAuth Choice

- Team or internal use: Cloudflare Access is the simplest default
- External users or product login: use an existing OAuth identity provider

Cloudflare's authorization docs note that remote MCP users authenticate with the OAuth provider, then grant the MCP client scoped access to server tools.

## Suggested Cloudflare Shape

- Worker route: `/mcp`
- Transport: remote MCP over Streamable HTTP
- Secret storage: `wrangler secret put QUIVERAI_API_KEY`
- Runtime: Cloudflare Workers with the Agents MCP support
- Testing:
  - local with MCP Inspector
  - real client via `mcp-remote` for Claude Desktop
  - direct remote-client connection where supported

## Bootstrap Choices

Cloudflare documents starter templates for remote MCP servers:

- authless starter for quick experiments
- OAuth starters for GitHub and Google

Use an OAuth-enabled starter when the server will leave local testing.

## Quiver-Specific Guidance

- Start each workflow by validating model IDs with `quiver_list_models`
- Default to non-streaming Quiver calls unless incremental output is needed
- Respect Quiver rate-limit and retry headers
- Surface Quiver `request_id` values in server logs or tool responses when failures happen
- Keep the server narrow; do not add generic fetch or passthrough tools
