---
name: quiver-ai
description: Integrate or troubleshoot QuiverAI's API at api.quiver.ai for listing models, generating SVGs from text, and vectorizing images into SVG. Use when Codex needs to wire QuiverAI into a Node.js or REST client, handle QUIVERAI_API_KEY safely, debug QuiverAI HTTP errors or rate limits, or decide whether direct API calls are enough versus when to expose QuiverAI through an MCP server.
---

# QuiverAI

Use this skill for QuiverAI API integration work. Start with direct API calls or the official Node.js SDK. Escalate to a remote MCP server only when the job needs reusable live tools, centralized auth, or a shareable agent surface.

## Workflow

1. Read `references/api.md` for the current API surface and official doc links.
2. If the user wants a hosted agent surface, read `references/remote-mcp.md` and use `$building-mcp-server-on-cloudflare`.
3. Choose the smallest viable integration surface:
   - Node.js project: prefer `@quiverai/sdk`.
   - Other languages or thin integrations: call the REST API directly.
4. Load auth from `QUIVERAI_API_KEY`. Keep the key in an environment variable or secret manager. Never commit it.
5. Start with the smallest useful endpoint:
   - `GET /v1/models` to discover available model IDs
   - `POST /v1/svgs/generations` for text-to-SVG
   - `POST /v1/svgs/vectorizations` for image-to-SVG
6. Default to non-streaming calls. Use `stream: true` only when the caller explicitly needs server-sent events.
7. Handle failures deliberately:
   - respect `Retry-After` and `X-RateLimit-*`
   - use exponential backoff for `429`, `502`, and `503`
   - surface `request_id` from error payloads when present
8. Report what you wired: endpoints used, auth source, and any rate-limit or billing constraint that matters.

## Secret Handling

- Do not write the user's API key into `SKILL.md`, `references/`, tests, examples, committed config, or git history.
- For local PowerShell work, set the key in-session:

```powershell
$env:QUIVERAI_API_KEY = "<your-key>"
```

- For app code, read `process.env.QUIVERAI_API_KEY` or the language equivalent.
- For shared or production systems, use deployment environment variables or a secret manager.
- For Cloudflare Workers, store the key as a Worker secret, for example `wrangler secret put QUIVERAI_API_KEY`.

## Remote MCP on Cloudflare

Prefer a Cloudflare remote MCP server when the user wants QuiverAI available as reusable tools in Claude, Cursor, ChatGPT, or other MCP clients.

Default design:

- Host a focused remote MCP server over Streamable HTTP at `/mcp`
- Keep `QUIVERAI_API_KEY` server-side as a Worker secret
- Add OAuth for MCP client access; this protects your MCP tools, not the upstream Quiver credential
- Expose a small tool surface instead of the entire Quiver API:
  - `quiver_list_models`
  - `quiver_generate_svg`
  - `quiver_vectorize_svg`

Auth default:

- Internal or team-only use: prefer Cloudflare Access as the OAuth provider
- Broader shared use: prefer a third-party OAuth provider or an existing identity system

Do not hand the raw Quiver API key to MCP clients. The Worker should call Quiver on behalf of authenticated users.

## Skill vs MCP Server

Use this skill alone when the job is:

- local integration work inside one repo
- guidance on auth, endpoints, request shapes, or retries
- one-off scripts or application code that can call QuiverAI directly

Build an MCP server only when the job needs:

- stable QuiverAI tools for ChatGPT, Codex, or other MCP clients
- centralized custody of the API key on a server boundary
- reusable typed tools instead of ad hoc HTTP code in each project
- a shared integration surface across multiple repos or agents

If those do apply, prefer a Cloudflare remote MCP with OAuth. If they do not, stay with direct SDK or REST integration.
