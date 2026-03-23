# Surface And Examples

Use this file first when the task is about the public SDK surface, choosing an example, or deciding what to import.

## Public SDK Entry Points

Treat these as the main truth sources in this order:

1. `packages/coding-agent/docs/sdk.md`
2. `packages/coding-agent/examples/sdk/README.md`
3. The specific file under `packages/coding-agent/examples/sdk/`
4. `packages/coding-agent/src/index.ts` to confirm exports

If an API is not exported from `packages/coding-agent/src/index.ts`, do not recommend it as the normal integration surface.

## Export Groups To Reach For

| Need | Main exports |
| --- | --- |
| Create a session | `createAgentSession`, `AgentSession`, `CreateAgentSessionOptions` |
| Auth and model lookup | `AuthStorage`, `ModelRegistry` |
| Resource discovery | `DefaultResourceLoader`, `createEventBus`, `ResourceLoader` |
| Sessions and persistence | `SessionManager`, `AgentSession`, session entry types |
| Settings | `SettingsManager` |
| Built-in tools | `codingTools`, `readOnlyTools`, `readTool`, `bashTool`, `editTool`, `writeTool`, `grepTool`, `findTool`, `lsTool` |
| Custom cwd tools | `createCodingTools`, `createReadOnlyTools`, `createReadTool`, `createBashTool`, `createEditTool`, `createWriteTool`, `createGrepTool`, `createFindTool`, `createLsTool` |
| Skills and prompts | `Skill`, `PromptTemplate`, `loadSkills`, `loadSkillsFromDir` |
| Extensions and custom tools | `ExtensionAPI`, `ExtensionFactory`, `ToolDefinition`, `createExtensionRuntime` |
| Run modes | `InteractiveMode`, `runPrintMode`, `runRpcMode` |

## Example Matrix

| File | Use it for |
| --- | --- |
| `01-minimal.ts` | Fastest “just make a session” bootstrap with defaults |
| `02-custom-model.ts` | Explicit model and thinking selection |
| `03-custom-prompt.ts` | Replacing or appending to the system prompt |
| `04-skills.ts` | Filtering, injecting, or replacing discovered skills |
| `05-tools.ts` | Built-in tools, read-only mode, and custom `cwd` tool factories |
| `06-extensions.ts` | Extension discovery, inline extension factories, event hooks, reusable custom tools |
| `07-context-files.ts` | `AGENTS.md` and injected context files |
| `08-prompt-templates.ts` | File-based prompt templates used like slash commands |
| `09-api-keys-and-oauth.ts` | `AuthStorage`, `ModelRegistry`, runtime API-key overrides |
| `10-settings.ts` | Settings overrides, `flush()`, `drainErrors()`, in-memory settings |
| `11-sessions.ts` | Persistent vs in-memory sessions, continue/open/list patterns |
| `12-full-control.ts` | Explicit wiring with no default discovery and a custom `ResourceLoader` |

## Fast Routing

- If the user wants the smallest working integration, start from `01-minimal.ts`.
- If the user wants a custom host app or embedded agent, start from `01-minimal.ts`, then add only the surfaces they need.
- If the user is unsure which exported API to use, confirm against `packages/coding-agent/src/index.ts` before answering.
- If the user wants deep extension work, switch from `docs/sdk.md` to `docs/extensions.md` after you have the basic SDK shape.

## High-Value Notes

- `packages/coding-agent/examples/sdk/README.md` is useful as a task index, but the example filenames are the source of truth.
- The example README still refers to `08-slash-commands.ts`; the actual file is `08-prompt-templates.ts`.
- `packages/coding-agent/src/index.ts` exports both headless SDK helpers and interactive-mode surfaces. Do not assume the SDK is limited to `createAgentSession`.
