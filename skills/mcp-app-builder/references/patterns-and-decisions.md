# Patterns And Decisions

Use this file to make the branch choice and the architecture recommendation concrete.

## Branch selection

Choose `server-only` when:

- The task only needs tool calls and model narration.
- Inline UI adds little value relative to added complexity.
- The main job is read or write actions that can be explained cleanly in text.

Choose `server + UI` when:

- The user needs inspection, editing, picking, visualization, or other repeated interaction inline.
- The UI meaningfully reduces ambiguity or repeated tool calls.
- The experience benefits from structured results rendered in an iframe.

Choose `MCPB` when:

- The server must touch local files, desktop apps, localhost services, device APIs, or OS state.
- The app cannot reasonably be hosted as a shared HTTPS MCP endpoint.

Do not choose `MCPB` just because local development is convenient.

## Transport and runtime

- Prefer hosted HTTPS MCP for anything ChatGPT-facing or shareable.
- Use TypeScript when the surrounding stack is already Node or React.
- Use Python when the backend ecosystem, data tooling, or existing codebase clearly favors it.
- Treat local stdio as a spike or debugging path, not the default recommendation.

## Tool design rules

- Keep one user job per tool.
- Write tool descriptions in a direct "Use this when..." style.
- Keep arguments explicit and constrained with enums or clear nullable behavior where possible.
- Split read and write tools unless there is a strong reason not to.
- Mark `readOnlyHint`, `destructiveHint`, and `openWorldHint` accurately.
- Do not hide irreversible behavior behind vague tool descriptions.

## Payload design

- Put model-visible, compact reasoning data in `structuredContent`.
- Put optional model narration in `content`.
- Put large, sensitive, or widget-only data in `_meta`.
- Keep `structuredContent` small enough for the model to reason over without noise.
- Do not leak secrets, tokens, internal IDs, or debug traces into any user-visible payload.

## UI rules

- Register widget resources as `text/html;profile=mcp-app`.
- Version the resource URI when the widget bundle changes in a breaking way.
- Use the MCP Apps bridge as the default runtime contract.
- Treat `window.openai` as optional and ChatGPT-specific.
- Define CSP and widget domain deliberately whenever UI exists.
- Prefer data tools plus render tools when that gives the model better control or prevents unnecessary widget remounts.

## Auth and state

- Default to anonymous or read-only flows when that satisfies the use case.
- Move to OAuth when tools expose user-specific data or perform writes.
- Keep memory and persisted state as hints, not hidden requirements.
- Reconfirm destructive or high-risk writes in the current turn.

## Company knowledge compatibility

Only recommend `search` and `fetch` when the app genuinely aims to act as a knowledge source. If that is the goal:

- Match the MCP input schema exactly.
- Return canonical `url` values for citations.
- Keep those tools read-only.

## Failure patterns to avoid

- Generic "kitchen sink" tools that do several unrelated jobs.
- Widget recommendations without a clear user-facing interaction need.
- UI advice that assumes `window.openai` is the portable baseline.
- Submission advice without CSP, review credentials, or realistic test prompts.
- Defaulting to MCPB when a hosted HTTPS server is sufficient.
