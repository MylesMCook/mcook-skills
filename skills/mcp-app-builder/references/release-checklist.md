# Release Checklist

Use this checklist before finalizing a recommendation or implementation plan.

## Planning complete

- The branch is explicit: `server-only`, `server + UI`, or `MCPB`.
- The use case, golden prompts, and negative prompts are named.
- Each tool has a clear job, schema, and annotation stance.
- The recommendation explains why the rejected branches are worse fits.

## Implementation readiness

- Transport and hosting are explicit.
- SDK and runtime are explicit.
- Payload boundaries between `structuredContent`, `content`, and `_meta` are explicit.
- If UI exists, the resource URI, bridge contract, CSP, and widget domain are explicit.
- If auth exists, the OAuth resource metadata, `securitySchemes`, and re-auth behavior are explicit.

## Testing

- Unit coverage exists for tool handlers and edge cases.
- MCP Inspector is part of the local loop.
- ChatGPT developer mode is part of the validation path.
- Mobile is included when the recommendation includes UI.
- Discovery is checked against direct, indirect, and negative prompts.

## Troubleshooting pass

- If tools do not appear, verify the `/mcp` endpoint and tool registration.
- If the widget does not render, verify the `text/html;profile=mcp-app` resource, CSP, and bundle loading.
- If the wrong tool fires, revise metadata before widening scope.
- If auth loops, verify protected resource metadata, OAuth metadata, scopes, and `WWW-Authenticate` signaling.
- If stale UI keeps appearing, version the widget resource URI.

## Submission readiness

- The server is publicly reachable over HTTPS.
- Review credentials work outside the local network and do not require MFA.
- Tool annotations match real behavior.
- Privacy-sensitive fields are minimized and intentional.
- Test prompts and expected outcomes are written clearly.
- The recommendation states whether public submission is in scope or intentionally deferred.
