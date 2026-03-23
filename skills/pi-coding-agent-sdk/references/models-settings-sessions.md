# Models, Settings, And Sessions

Use this file when the task is about credentials, model selection, settings behavior, session persistence, event streams, or SDK run modes.

## Canonical Sources

- `packages/coding-agent/docs/sdk.md`
- `packages/coding-agent/docs/session.md`
- `packages/coding-agent/docs/settings.md`
- `packages/coding-agent/examples/sdk/09-api-keys-and-oauth.ts`
- `packages/coding-agent/examples/sdk/10-settings.ts`
- `packages/coding-agent/examples/sdk/11-sessions.ts`

## Auth And Models

Main exports:

- `AuthStorage`
- `ModelRegistry`
- `getModel()` from `@mariozechner/pi-ai`

API-key resolution order in `AuthStorage`:

1. runtime overrides from `setRuntimeApiKey()`
2. stored credentials in `auth.json`
3. environment variables
4. fallback resolver for custom provider keys from `models.json`

Model selection order when `createAgentSession()` receives no explicit model:

1. restore from session, if continuing
2. default from settings
3. first available configured model

## Settings

Main export: `SettingsManager`

Use:

- `SettingsManager.create(cwd?, agentDir?)` for file-backed merged settings
- `SettingsManager.inMemory(settings?)` for test or embedded use without file I/O

Behavior to remember:

- global settings live in `~/.pi/agent/settings.json`
- project settings live in `<cwd>/.pi/settings.json`
- project overrides global and nested objects merge
- setters update memory immediately but persist asynchronously
- call `await settingsManager.flush()` when you need durability
- read `settingsManager.drainErrors()` in the host layer; the manager does not print I/O failures itself

## Sessions

Main exports:

- `SessionManager`
- `AgentSession`

Common entry points:

- `SessionManager.inMemory()`
- `SessionManager.create(cwd, sessionDir?)`
- `SessionManager.continueRecent(cwd, sessionDir?)`
- `SessionManager.open(path)`
- `SessionManager.list(cwd, sessionDir?)`
- `SessionManager.listAll(progressCallback?)`

Important session concepts:

- Pi sessions are tree-shaped, not just flat chat logs
- `SessionManager` exposes path, tree, labels, and branching helpers
- `AgentSession` owns the live lifecycle, queueing, compaction, and event stream

When a question is about persistence structure or branching, inspect both:

- `packages/coding-agent/src/core/session-manager.ts`
- `packages/coding-agent/src/core/agent-session.ts`

## Events

The event stream from `session.subscribe()` is the main programmatic way to observe:

- assistant text deltas
- thinking deltas
- tool execution start, update, and end
- message start and end
- turn start and end
- agent start and end
- auto-compaction and auto-retry events

If the question is “which event should I listen to?”, start from `message_update`, `tool_execution_*`, `turn_end`, and `agent_end`.

## Run Modes

`packages/coding-agent/src/index.ts` exports:

- `InteractiveMode`
- `runPrintMode`
- `runRpcMode`

Use them when the user wants the SDK but does not want to rebuild a full interaction loop from scratch.

- `InteractiveMode` keeps the full TUI stack
- `runPrintMode` is the easiest single-shot headless mode
- `runRpcMode` is for subprocess or cross-language integrations
