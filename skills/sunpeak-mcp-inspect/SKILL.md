---
name: sunpeak-mcp-inspect
description: >
  Use when a user asks to inspect or debug a local MCP server or MCP App with
  Sunpeak's local inspector: start or connect to `sunpeak inspect` or a
  project dev inspector, keep simulation evidence separate from real server
  calls, and verify the rendered app with local browser or computer-control
  evidence.
---

# Sunpeak MCP Inspect

Use this skill to inspect a local Sunpeak inspector session and verify MCP
tool, resource, and rendered-app behavior without mixing fixture and live
evidence.

## Use when

- The user wants to inspect or debug a local MCP server or MCP App with
  Sunpeak.
- The task needs evidence about a simulation fixture, a real server call, or
  a rendered app state in the local inspector.
- The repo already has Sunpeak tests or fixtures and the user wants local
  verification.

## Do not use when

- The user wants live ChatGPT or Claude host validation.
- The task is generic browser QA unrelated to the Sunpeak inspector.

## Required capabilities

- local process control
- localhost HTTP polling
- browser/DOM/Playwright access, or computer-control access that can interact
  with the inspector and capture evidence

If you cannot inspect the UI, fail clearly with the expected inspector URL and
the missing capability. If you can open the browser but cannot inspect DOM,
console, or network state, continue with visible/manual verification only and
say exactly what was not checked.

## One evidence mode at a time

Choose exactly one mode before you interact with the inspector:

- `simulation`
- `real-call`
- `automated`

Do not report simulation success as real-call success, or real-call success
from fixture-only evidence.

## Fast path

1. Read `package.json`, `README*`, Sunpeak config, and nearby test docs. Prefer
   documented scripts and URLs over invented commands.
2. Prefer startup in this order:
   - documented project `dev`, `dev:inspect`, or `inspect`
   - documented Sunpeak test command when the user asked for automation
   - standalone `sunpeak inspect --server <url-or-command>`
3. If a project stop script exists, run it before starting new processes.
4. Record the commands, cwd, ports, and process handles you start.
5. Wait until the inspector responds over HTTP and visible Sunpeak UI
   landmarks appear.

## Mode rules

### `simulation`

- Select the intended simulation by URL or UI.
- Confirm the simulation name and target tool match the test case.
- Verify the fixture shape in Tool Result JSON or `toolResult`.
- If the JSON is valid but the app is blank, report a rendering issue.

### `real-call`

- Ensure no simulation is selected.
- Trigger a fresh run with explicit input.
- Verify that a new live call happened and no transport or protocol error was
  returned.
- Check only the fields the user, project code, or tests actually expect.

### `automated`

- Use existing Sunpeak tests or `mcp.callTool()` / `inspector.renderTool()`
  when available.
- Treat `source: "fixture"` as simulation evidence and `source: "server"` as
  live evidence.

## Verification

- Inspector URL is reachable.
- Target tool or resource is selectable.
- The chosen mode is explicit.
- Raw results match the expected contract.
- The rendered UI matches the expected state.
- Console or runtime errors are captured when possible. If not, say so.
- Host, theme, display mode, and device settings are recorded only when the
  bug or request makes them relevant.

## Teardown

- Prefer a project stop script such as `dev:stop`.
- Otherwise stop only the processes started during the current run.
- Report what you stopped.

## References

- CLI flags, URL parameters, simulation schema, and fixture-test reminders:
  [references/sunpeak-inspector.md](references/sunpeak-inspector.md)
