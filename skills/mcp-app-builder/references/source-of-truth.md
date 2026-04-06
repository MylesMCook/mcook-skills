# Source Of Truth

Use the current OpenAI docs as the canonical architecture source.

## Read order

1. [Research use cases](https://developers.openai.com/apps-sdk/plan/use-case/)
   Capture the real user jobs, direct prompts, indirect prompts, and negative prompts before designing tools.
2. [Define tools](https://developers.openai.com/apps-sdk/plan/tools/)
   Turn the use cases into a clean tool surface with one job per tool.
3. [Optimize metadata](https://developers.openai.com/apps-sdk/guides/optimize-metadata/)
   Tune discovery, descriptions, parameter docs, and annotations against a golden prompt set.
4. [Quickstart](https://developers.openai.com/apps-sdk/quickstart/)
   Use for the shortest current end-to-end example of an MCP server plus optional UI.
5. [Build your MCP server](https://developers.openai.com/apps-sdk/build/mcp-server/)
   Use for server architecture, resource registration, tool descriptors, payload separation, annotations, UI metadata, and advanced capability details.
6. [Build your ChatGPT UI](https://developers.openai.com/apps-sdk/build/chatgpt-ui/)
   Use when the branch is `server + UI` and the job needs an iframe component.
7. [Authentication](https://developers.openai.com/apps-sdk/build/auth/)
   Use whenever the app exposes user data, write actions, or linked account flows.
8. [Test your integration](https://developers.openai.com/apps-sdk/deploy/testing/)
   Use for unit coverage, Inspector, developer mode, and regression checks.
9. [Troubleshooting](https://developers.openai.com/apps-sdk/deploy/troubleshooting/)
   Use when widgets fail to render, discovery misses, auth loops, or deployment behavior is unclear.
10. [Submit and maintain your app](https://developers.openai.com/apps-sdk/deploy/submission/)
    Use when the recommendation should include public review, launch, or long-term maintenance readiness.

## Stable defaults to keep

- Start with the Apps SDK flow, not generic MCP advice.
- Treat hosted HTTPS as the normal path for anything meant to work in ChatGPT.
- Treat the MCP Apps bridge as the baseline UI contract.
- Use `window.openai` only for optional ChatGPT-specific enhancements.
- Keep `SKILL.md` guidance short and push durable detail into references.

## Extra context

- [Agent Skills](https://developers.openai.com/codex/skills/)
  This is only relevant to how the skill itself should be packaged and discovered: concise `SKILL.md`, progressive disclosure, optional references, and instruction-first design.
