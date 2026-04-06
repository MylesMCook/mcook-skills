---
name: mcp-app-builder
description: Build ChatGPT apps and MCP servers with an apps-first workflow. Use when Codex needs to build or improve an MCP server, create a ChatGPT app, add widget UI, wrap an API with MCP, choose between hosted HTTPS delivery and MCPB, add auth/testing/submission readiness, or debug MCP app behavior. Prefer hosted Apps SDK patterns and only choose MCPB for true local-machine access.
---

# MCP App Builder

## Use when

- Build a hosted MCP server or ChatGPT app.
- Add or refine widget UI for an MCP tool flow.
- Wrap an API or product surface with MCP.
- Choose between `server-only`, `server + UI`, and `MCPB`.
- Add auth, testing, troubleshooting, or submission readiness to an existing app.

## Do not use when

- The task is generic non-OpenAI MCP work where ChatGPT and Apps SDK compatibility do not matter.
- The task is only about Codex plugin packaging, local skill packaging, or Cursor configuration.
- The job is already a known MCPB packaging task with platform-specific distribution details that exceed these references.

## Defaults

- Classify first: `server-only`, `server + UI`, or `MCPB`.
- Prefer hosted HTTPS MCP servers for anything shared, reviewable, or ChatGPT-facing.
- Add UI only when inline interaction materially improves the user job.
- Use the MCP Apps bridge by default; treat `window.openai` as an optional ChatGPT-only enhancement.
- Keep tool boundaries narrow, annotations accurate, and payloads split cleanly across `structuredContent`, `content`, and `_meta`.
- Prefer separate data tools and render tools when that reduces widget remounts or gives the model better control.
- Escalate to `MCPB` only for filesystem, desktop, localhost, or OS-bound requirements.

## Required workflow

1. Read `references/source-of-truth.md` first and choose the correct branch: `server-only`, `server + UI`, or `MCPB`.
2. Define the user job, golden prompts, tool surface, and metadata before writing implementation advice.
3. Pick transport and SDK deliberately, with hosted HTTPS as the default and local stdio only for short-lived spikes.
4. Specify each tool with intent, schema, annotations, and result shape before discussing handlers.
5. If UI exists, require a versioned `text/html;profile=mcp-app` resource, MCP Apps bridge messaging, and explicit CSP/domain decisions.
6. Cover auth, state, testing, troubleshooting, and submission readiness before finalizing the recommendation.

## Output contract

- Always produce a concrete build spec, not generic advice.
- Include the chosen branch and why it wins over the alternatives.
- Include transport and hosting choice, SDK/runtime choice, and the tool inventory with argument and result shapes.
- Include annotation decisions, payload boundaries, and any auth or storage requirements.
- Include the UI strategy when relevant: resource URI, bridge pattern, state approach, CSP, domain, and any `window.openai` usage.
- Include the test path: unit coverage, MCP Inspector, ChatGPT developer mode, and mobile checks when UI exists.
- Include release-readiness notes: troubleshooting risks, submission blockers, or why submission is out of scope.

## Load references

- Read `references/source-of-truth.md` first for the canonical OpenAI page order.
- Read `references/patterns-and-decisions.md` for branch selection, tool rules, payload design, UI architecture, and MCPB escalation.
- Read `references/release-checklist.md` before finalizing auth, testing, troubleshooting, or submission guidance.
