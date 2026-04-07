---
name: sunpeak-mcp-inspect
description: Inspect local MCP apps and MCP servers with Sunpeak. Use when the task is to start or connect to a Sunpeak inspector session, switch between simulation and real server-call modes, verify tool results or rendered app behavior, or debug local MCP app rendering using available browser or computer-control primitives. Prefer local inspector workflows, not live host testing or generic browser QA.
---

# Sunpeak MCP Inspect

Use this skill to inspect a local MCP server with Sunpeak and verify the rendered app behavior.

## Required capabilities

- local process control
- HTTP polling
- browser or computer-control primitives that can open a URL, inspect visible page state, interact with controls, and capture evidence

If no viable way to inspect the Sunpeak UI exists, fail clearly and report the expected inspector URL plus the missing capability.

If the environment can only launch a browser window but cannot inspect DOM state or console output, continue with visible/manual verification only and say exactly which checks could not be performed.

## Default behavior

- Prefer project-native scripts and documented URLs over invented commands.
- Prefer local inspector workflows, not live ChatGPT or Claude host testing.
- Prefer safe teardown that only affects processes started by the current run.
- Check current `sunpeak inspect` docs or `sunpeak inspect --help` if CLI flags appear to have changed.

## Discover the startup path

1. Detect the package manager from lockfiles:
   - `pnpm-lock.yaml` -> `pnpm run`
   - `yarn.lock` -> `yarn`
   - otherwise -> `npm run`
2. Read `package.json`, `README.md`, and nearby docs to discover:
   - the preferred inspector script
   - the preferred teardown script
   - the MCP server URL or stdio command
   - the inspector URL and port
   - the simulations directory
3. Prefer startup paths in this order:
   - `dev:inspect` plus `dev:stop`
   - separate worker plus inspector scripts such as `dev:worker` or `dev`, then `inspect`
   - standalone `sunpeak inspect --server <url-or-command> [--simulations <dir>]`
4. Treat a documented project URL as authoritative.
5. If the project does not document an inspector URL, use safe defaults only as hints:
   - `sunpeak inspect` default port is `3000`
   - use any project-specific port or simulation parameter discovered from repo artifacts ahead of that default

## Start safely

1. If a project-native stop script exists, run it first.
2. Start only the minimal set of processes needed for this run.
3. Record the process ids, terminal ids, or equivalent handles created by the run.
4. After each launch, do a short poll of startup output to catch immediate crashes.

## Readiness gate

Do not inspect immediately after process start.

1. Poll the documented inspector health endpoint if one exists.
2. Otherwise poll the documented inspector root URL.
3. Continue only after both conditions are true:
   - the inspector responds over HTTP
   - visible Sunpeak UI landmarks appear, such as the tool list, simulation selector, host controls, or inspector layout controls
4. If the port responds but the Sunpeak UI has not appeared, keep polling until timeout.
5. On timeout, report the startup output and stop.

## Inspect with strict mode discipline

Do not mix simulation evidence with live server-call evidence.

### Simulation mode

Use this mode to verify fixture wiring and deterministic inspector behavior.

1. Select the intended simulation.
2. Confirm the selected simulation matches the URL or visible inspector state.
3. Confirm Tool Result JSON exists and includes `structuredContent.render`.
4. If the chart is blank but the result contract is present, report a widget rendering issue rather than a transport issue.

### Live server-call mode

Use this mode to verify a real MCP round-trip.

1. Set Simulation to `None (call server)`.
2. Trigger `Run`.
3. Confirm a fresh real tool execution occurred and did not return a transport error.
4. Confirm the result includes:
   - `structuredContent.resultMetaVersion`
   - `structuredContent.render`
   - `structuredContent.render.renderable === true`
   - `structuredContent.render.editorUrl` when that field is expected

Never report live-path success from simulation-only evidence.

## Verification checklist

Before finishing, verify all of the following that the environment can actually support:

- the inspector is reachable at the correct local URL
- the tool list is visible and the target tool is selectable
- at least one successful result includes `structuredContent.resultMetaVersion`
- at least one successful result includes `structuredContent.render.renderable === true`
- `structuredContent.render.editorUrl` is non-empty when expected
- runtime or console errors are reported if the environment can inspect them

If the environment cannot inspect console output, state that explicitly instead of implying a clean console.

If the chart is blank but the result contract is valid, report it explicitly as a widget rendering issue.

## Teardown and safety

1. Prefer project-native teardown such as `dev:stop`.
2. If no project-native teardown exists, stop only the processes started by the current run.
3. Do not use broad port-kill or machine-wide process-kill patterns.
4. Report which processes or terminals were stopped and how they were stopped.
