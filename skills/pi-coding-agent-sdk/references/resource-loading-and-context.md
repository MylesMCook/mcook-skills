# Resource Loading And Context

Use this file when the task is about `DefaultResourceLoader`, resource discovery, `AGENTS.md`, skills, prompts, themes, or extension loading paths.

## Canonical Sources

- `packages/coding-agent/docs/sdk.md`
- `packages/coding-agent/docs/extensions.md`
- `packages/coding-agent/src/core/resource-loader.ts`
- `packages/coding-agent/src/core/skills.ts`
- `packages/coding-agent/src/core/package-manager.ts`

## Default Discovery Model

`createAgentSession()` uses `DefaultResourceLoader` unless the caller provides a custom loader.

### From `cwd`

- Project extensions: `.pi/extensions/`
- Project skills: `.pi/skills/`
- Shared project skills: `.agents/skills/` in `cwd` and ancestor directories, up to the git root or filesystem root
- Project prompts: `.pi/prompts/`
- Context files: `AGENTS.md` walking upward from `cwd`

### From `agentDir`

Default `agentDir` is `~/.pi/agent`.

- Global extensions: `extensions/`
- Global skills: `skills/`
- Shared user skills: `~/.agents/skills/`
- Global prompts: `prompts/`
- Global context file: `AGENTS.md`
- Runtime files: `settings.json`, `models.json`, `auth.json`, `sessions/`

## Important Loader Behavior

- If the caller passes a custom `ResourceLoader`, `cwd` and `agentDir` no longer control resource discovery.
- Even with a custom loader, `cwd` and `agentDir` still influence session naming and tool path resolution.
- `await loader.reload()` is the normal boundary before using a loader-driven session configuration.

## High-Value Override Hooks

| Need | Hook or option |
| --- | --- |
| Replace system prompt | `systemPromptOverride` |
| Append system prompt text | `appendSystemPromptOverride` |
| Add extension files directly | `additionalExtensionPaths` |
| Create inline extensions | `extensionFactories` |
| Filter or inject skills | `skillsOverride` |
| Inject `AGENTS.md`-style files | `agentsFilesOverride` |
| Filter or inject prompt templates | `promptsOverride` |
| Share extension events outside the loader | `eventBus` |

## Context Files

Use `agentsFilesOverride` when the caller needs to inject virtual or synthetic context files without depending on on-disk `AGENTS.md` discovery.

This is the main SDK surface for “pretend this app has an AGENTS file” behavior.

## Skills And Prompts

- Skills and prompt templates are normal discovered resources under `DefaultResourceLoader`.
- If the caller wants a minimal or tightly controlled embedding, they can replace discovery with `skillsOverride`, `promptsOverride`, and `agentsFilesOverride`.
- `packages/coding-agent/examples/sdk/04-skills.ts` and `07-context-files.ts` are the quickest examples for injected resources.

## Practical Pattern

`~/projects/pi-extensions/packages/agent-kit/executor.ts` is a good local example of a fully controlled embedding:

- disables default extensions, prompt templates, themes, and skills
- injects a system prompt directly
- injects an explicit skill list
- strips inherited `AGENTS.md` files

Use that pattern when the host app wants reproducible agent state instead of normal user/project discovery.
