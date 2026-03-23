# Tools, Extensions, And Prompts

Use this file when the task is about built-in tools, custom tools, extensions, commands, prompt templates, or which surface should own behavior.

## Canonical Sources

- `packages/coding-agent/docs/sdk.md`
- `packages/coding-agent/docs/extensions.md`
- `packages/coding-agent/examples/sdk/05-tools.ts`
- `packages/coding-agent/examples/sdk/06-extensions.ts`
- `packages/coding-agent/examples/sdk/08-prompt-templates.ts`
- `packages/coding-agent/src/core/tools/`
- `packages/coding-agent/src/core/extensions/`

## Choose The Right Surface

| Need | Prefer |
| --- | --- |
| Inline host-app tool definition | `customTools` on `createAgentSession()` |
| Reusable tool loaded by discovery | Extension with `pi.registerTool()` |
| Read-only review agent | `readOnlyTools` or `createReadOnlyTools(cwd)` |
| Explicit built-in tool subset | `tools: [readTool, bashTool, ...]` or factory-created equivalents |
| Custom `cwd` plus explicit tools | `createReadTool(cwd)` and other factory functions |
| Slash-style reusable text expansion | Prompt templates |
| Stateful hooks, commands, UI, or event interception | Extensions |

## Built-In Tools

The prebuilt tool exports such as `readTool`, `bashTool`, and `codingTools` use `process.cwd()`.

If the caller sets a custom `cwd` and also passes explicit `tools`, switch to the factory APIs:

- `createCodingTools(cwd)`
- `createReadOnlyTools(cwd)`
- `createReadTool(cwd)` and friends

If the caller does not pass `tools`, the SDK wires the default built-in tools for the configured `cwd`.

## `customTools` Vs Extension-Registered Tools

Use `customTools` when:

- the tool lives inside one embedding or app
- the host wants to pass tool definitions directly
- there is no need for discovery, commands, or extension lifecycle hooks

Use extension-registered tools when:

- the tool should be discoverable from resource loading
- the tool needs event hooks, commands, UI, or shared extension state
- the tool should behave like part of the normal Pi runtime

Important nuance:

- `examples/sdk/06-extensions.ts` frames extensions as the main custom-tool system
- `docs/sdk.md` still documents `customTools` as a first-class public option

Both are valid. `customTools` is the direct SDK embedding path. Extensions are the reusable runtime path.

## Prompt Templates And Slash Commands

Prompt templates are file-backed content expansions that users invoke like slash commands.

- `session.prompt()` expands file-based prompt templates before sending or queueing
- `steer()` and `followUp()` also expand file-based prompt templates
- extension commands execute immediately, even during streaming, and manage their own interaction flow

Treat prompt templates as content expansion and extension commands as active runtime behavior.

## Extension Capabilities

Extensions can:

- subscribe to lifecycle and tool events
- block or modify behavior
- register tools
- register commands, shortcuts, and flags
- use `ctx.ui` for confirm, input, notify, status, widgets, and custom UI
- persist state into the session

If the task is specifically about custom UI, command handlers, or event interception, load `packages/coding-agent/docs/extensions.md` after establishing the high-level SDK wiring.

## Useful Local References

- `~/projects/pi-extensions/packages/agent-kit/executor.ts`
  shows a headless embedding that uses `createAgentSession`, `DefaultResourceLoader`, `SessionManager`, and `SettingsManager` together.
- `~/projects/pi-extensions/tests/utils/pi-test-harness.ts`
  shows how to load extensions through real Pi runtime paths in tests instead of mocking the entire extension API.
