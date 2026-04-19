---
name: ai-elements
description: Use AI Elements for React UIs that render AI-generated text, chat streams, tool calls, reasoning, or multimodal AI SDK messages with shadcn/ui.
---

# AI Elements

Use this skill when a React UI needs to render model output in the browser.

## Start here

- AI Elements is newer than model memory can be. Fetch current docs before choosing components:
  - `https://ai-sdk.dev/elements`
  - `https://ai-sdk.dev/elements/components`
- Install only the components you need.
- Do not build AI-text rendering from scratch when AI Elements fits.

## Use the smallest component that solves the job

- Any AI-generated markdown-like text: install `message` and render with `MessageResponse`
- AI SDK chat UIs: `conversation` plus `message`
- Tool invocations and results: `tool`
- Syntax-highlighted code: `code-block`
- Reasoning panels: `reasoning`
- Rich chat composer: `prompt-input`

## Install

Prefer the shadcn registry URL for only the components you need:

```bash
npx shadcn@latest add https://elements.ai-sdk.dev/api/registry/message.json
npx shadcn@latest add https://elements.ai-sdk.dev/api/registry/conversation.json
```

Do not install the whole registry unless the user explicitly needs the full suite.

## Required patterns

- Render browser-visible AI text with `MessageResponse` from `@/components/ai-elements/message`
- For `useChat` interfaces, prefer `Conversation` plus `Message`
- On the server, return `toUIMessageStreamResponse()` when the client renders AI Elements messages
- When using a custom chat endpoint, wire `useChat` through `DefaultChatTransport`
- Keep AI Elements components behind a `'use client'` boundary

## Avoid

- Rendering model output as raw JSX like `{text}` or `<p>{text}</p>`
- Installing the entire registry by default
- Adding `@ts-nocheck` to silence AI Elements type errors
- Treating AI Elements as a fit for non-React or non-shadcn projects without an explicit adaptation plan

## Common fixes

- Missing `@/components/ui/*` imports: install the required shadcn primitives
- Type errors in installed AI Elements components: reinstall the specific component with overwrite, then update `@base-ui/react` if needed
- Missing styles: ensure Tailwind scans `src/components/ai-elements/**/*.{ts,tsx}`
- Broken chat rendering: verify `toUIMessageStreamResponse()` on the server and `DefaultChatTransport` on the client
- Base UI mismatch: if shadcn was initialized against `base-ui`, switch back to Radix-backed components before debugging deeper

## Docs

- `https://ai-sdk.dev/elements`
- `https://ai-sdk.dev/elements/components`
- `https://github.com/vercel/ai-elements`
