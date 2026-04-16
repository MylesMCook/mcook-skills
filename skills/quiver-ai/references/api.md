# QuiverAI API Notes

Use the official docs as the source of truth:

- Introduction: https://docs.quiver.ai/api-reference/introduction
- Quickstart: https://docs.quiver.ai/getting-started/quickstart
- List Models: https://docs.quiver.ai/api-reference/models/list-models
- Text to SVG: https://docs.quiver.ai/api-reference/create-svgs/text-to-svg

## Current API Facts

Checked against the public docs on April 16, 2026.

- Base URL: `https://api.quiver.ai/v1`
- Auth: bearer token in `Authorization: Bearer <QUIVERAI_API_KEY>`
- JSON requests should send `Content-Type: application/json`
- Core endpoints documented in the introduction:
  - `GET /v1/models`
  - `GET /v1/models/{model}`
  - `POST /v1/svgs/generations`
  - `POST /v1/svgs/vectorizations`
- The docs show `arrow-preview` as an example model ID
- The official Node.js SDK package is `@quiverai/sdk`
- Non-streaming SVG responses return JSON with `id`, `created`, `data`, and optional `usage`
- Streaming SVG responses use `text/event-stream` with `reasoning`, `draft`, and `content` events, then `data: [DONE]`

## Rate Limits and Billing

- Public SVG generation and vectorization limit: `20` requests per `60` seconds
- Scope: per organization
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, and `Retry-After`
- Each successful generation or vectorization uses `1` credit
- Requests with `n > 1` consume `n` credits when they succeed

## Practical Defaults

- Call `GET /v1/models` before hardcoding a model ID
- Default to `stream: false` unless partial updates matter
- Treat `401`, `402`, `403`, `404`, `429`, `500`, `502`, and `503` as first-class cases in client code
- Include the API `request_id` in logs and user-visible diagnostics when present
