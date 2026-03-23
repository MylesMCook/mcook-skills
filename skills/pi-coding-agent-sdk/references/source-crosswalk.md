# Source Crosswalk

Use this file only when the public docs or examples are not enough, or when the user explicitly asks where a behavior lives in pi-mono.

## Main SDK Package

Start in `packages/coding-agent`.

| Path | Why it matters |
| --- | --- |
| `packages/coding-agent/src/index.ts` | Public exports and the fastest way to confirm the supported surface |
| `packages/coding-agent/src/core/sdk.ts` | `createAgentSession()` wiring and tool-factory helpers |
| `packages/coding-agent/src/core/agent-session.ts` | Live session lifecycle, prompt queueing, streaming, compaction integration |
| `packages/coding-agent/src/core/session-manager.ts` | Session files, trees, branching, listing, and persistence helpers |
| `packages/coding-agent/src/core/settings-manager.ts` | Settings merge, persistence, overrides, flush, and error draining |
| `packages/coding-agent/src/core/auth-storage.ts` | Credential storage and runtime API-key overrides |
| `packages/coding-agent/src/core/model-registry.ts` | Built-in and custom model lookup plus availability checks |
| `packages/coding-agent/src/core/resource-loader.ts` | Discovery and assembly of extensions, skills, prompts, themes, and context files |
| `packages/coding-agent/src/core/skills.ts` | Skill loading and skill-prompt formatting |
| `packages/coding-agent/src/core/package-manager.ts` | Package and resource resolution under discovery |
| `packages/coding-agent/src/core/extensions/` | Extension runtime, loader, event wiring, tool wrapping |
| `packages/coding-agent/src/core/tools/` | Built-in tool implementations and truncation behavior |
| `packages/coding-agent/src/modes/index.ts` | `InteractiveMode`, `runPrintMode`, and `runRpcMode` exports |
| `packages/coding-agent/src/modes/interactive/components/` | TUI components exported for extensions and interactive UI work |

## Adjacent pi-mono Packages

Use these only when the question escapes the public coding-agent package.

| Package | Role |
| --- | --- |
| `packages/agent` | Lower-level agent engine and state machinery exported as `@mariozechner/pi-agent-core` |
| `packages/ai` | Model/provider abstraction layer exported as `@mariozechner/pi-ai`; this is where `getModel()` and provider integrations live |
| `packages/tui` | Terminal UI primitives exported as `@mariozechner/pi-tui`; relevant for interactive mode and extension UI components |

## Local Real-World Usage

These are optional local references on this machine, not upstream truth sources:

| Path | Why it is useful |
| --- | --- |
| `~/projects/pi-extensions/packages/agent-kit/executor.ts` | Headless subagent embedding built around `createAgentSession`, `DefaultResourceLoader`, `SessionManager`, and `SettingsManager` |
| `~/projects/pi-extensions/tests/utils/pi-test-harness.ts` | Testing pattern that loads extensions through real Pi runtime paths instead of deep mocks |

Use these local files when the question is “how are people actually composing the SDK in practice?” after you have already grounded the answer in the upstream surface.
