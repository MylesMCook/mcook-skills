# Research Basis

This skill is opinionated because the source material converges on a small number of reliable defaults.

## Official Agent Skills guidance

Agent Skills are directories containing `SKILL.md` plus optional `scripts/`, `references/`, and `assets/`. `SKILL.md` requires YAML frontmatter with `name` and `description`. Agents use progressive disclosure: they first see only the skill metadata, then load full instructions when the task matches.

MCPeas implication:
- keep `SKILL.md` focused
- push durable detail into `references/`
- include scripts only when they provide repeatable mechanical value

Primary docs:
- https://agentskills.io/llms.txt
- https://agentskills.io/specification
- https://agentskills.io/skill-creation/best-practices
- https://agentskills.io/skill-creation/evaluating-skills
- https://developers.openai.com/codex/skills

## OpenAI Apps SDK and ChatGPT MCP Apps

Apps SDK apps connect to ChatGPT through an MCP server. A UI component is optional and renders in an iframe. ChatGPT implements the open MCP Apps UI standard, so portable widgets should target the MCP Apps bridge first.

MCPeas implication:
- server is required
- widget is optional but should be planned early
- ChatGPT-only `window.openai` features are enhancements, not baseline

Primary docs:
- https://developers.openai.com/apps-sdk/quickstart
- https://developers.openai.com/apps-sdk/plan/use-case
- https://developers.openai.com/apps-sdk/plan/tools
- https://developers.openai.com/apps-sdk/build/mcp-server
- https://developers.openai.com/apps-sdk/build/chatgpt-ui
- https://developers.openai.com/apps-sdk/deploy/testing

## MCP protocol

MCP defines stdio and Streamable HTTP transports. Streamable HTTP servers expose a single MCP endpoint and must account for Origin validation, localhost binding, and authentication. Tools are model-controlled and should be exposed with metadata, schemas, and human-in-the-loop safety for sensitive operations.

MCPeas implication:
- hosted Streamable HTTP is the default for shareable/ChatGPT-facing apps
- stdio/local is for local-machine needs
- annotations and confirmation posture matter

Primary docs:
- https://modelcontextprotocol.io/specification/2025-06-18/basic/transports
- https://modelcontextprotocol.io/specification/2025-06-18/server/tools
- https://modelcontextprotocol.io/specification/2025-06-18/server/resources
- https://modelcontextprotocol.io/specification/2025-06-18/server/prompts

## mcp-use

The `mcp-apps-builder` skill directs agents to scaffold with `npx create-mcp-use-app`, use the `mcp-apps` template when unsure, avoid manually creating boilerplate, and build with tools/resources/prompts/widgets. It emphasizes Zod descriptions, response helpers, accurate annotations, `error()` for graceful failures, and widget resources for visual interaction.

MCPeas implication:
- `npx create-mcp-use-app <name> --template mcp-apps` is the default
- do not hand-roll initial project files
- widget-ready project layout is worth the small upfront cost

Primary files:
- https://github.com/mcp-use/mcp-use/tree/main/skills/mcp-apps-builder
- https://raw.githubusercontent.com/mcp-use/mcp-use/main/skills/mcp-apps-builder/SKILL.md
- https://raw.githubusercontent.com/mcp-use/mcp-use/main/skills/mcp-apps-builder/references/foundations/quickstart.md
- https://raw.githubusercontent.com/mcp-use/mcp-use/main/skills/mcp-apps-builder/references/server/tools.md
- https://raw.githubusercontent.com/mcp-use/mcp-use/main/skills/mcp-apps-builder/references/widgets/basics.md

## Anthropic MCP builder

The Anthropic MCP builder emphasizes deep research, TypeScript as recommended stack, Streamable HTTP for remote servers, stdio for local servers, tool naming/discoverability, actionable errors, output schemas/structured content, annotations, Inspector testing, and evaluations with independent, read-only, complex, verifiable questions.

MCPeas implication:
- research before implementation
- TypeScript + Streamable HTTP default
- build evals, not just code

Primary files:
- https://github.com/anthropics/skills/tree/main/skills/mcp-builder
- https://raw.githubusercontent.com/anthropics/skills/main/skills/mcp-builder/SKILL.md

## Rust MCP generator

The Rust generator is useful evidence for what a strong Rust path looks like, but it is not the MCPeas default. Use it only when Rust is explicitly required or the host/runtime strongly demands Rust.

Primary file:
- https://raw.githubusercontent.com/github/awesome-copilot/main/skills/rust-mcp-server-generator/SKILL.md

## Retired branch-selection guidance

Earlier guidance in this repo used a more explicit branch model for `server-only`, `server + UI`, and `MCPB`. MCPeas keeps the useful defaults from that older approach, but removes the architecture menu and makes one path the default.

## Codex harnessing

Codex reads `AGENTS.md` before work and layers global/project instructions. Codex skills use progressive disclosure and live in repository/user/admin/system locations. Codex supports MCP in CLI and IDE via `config.toml`. Codex subagents can be configured with focused TOML files and are best kept narrow, bounded, and explicit.

MCPeas implication:
- every project gets AGENTS.md
- every project gets bounded Codex subagent config
- docs-researcher/code-mapper/reviewer are default read-only helpers
- local MCP server config is disabled by default until the dev server is running

Primary docs:
- https://developers.openai.com/codex/guides/agents-md
- https://developers.openai.com/codex/skills
- https://developers.openai.com/codex/mcp
- https://developers.openai.com/codex/subagents
- https://developers.openai.com/codex/config-basic
- https://developers.openai.com/codex/config-reference

## npx skills

The Vercel Labs `skills` CLI installs skills from GitHub URLs, direct repo paths, or local paths; supports `--global`, `--agent codex`, `--skill`, `--copy`, listing, removing, updating, and initialization. Codex global skills install under `~/.codex/skills/`; project skills under `.agents/skills/`.

Primary repo:
- https://github.com/vercel-labs/skills
