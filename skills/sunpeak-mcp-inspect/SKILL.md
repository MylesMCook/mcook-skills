---
name: sunpeak-mcp-inspect
description: Inspect MCP apps with Sunpeak in Cursor Browser using project-native scripts, robust readiness checks, and safe teardown.
---

# Sunpeak MCP Inspect

Use this skill to run Sunpeak MCP inspection in a Cursor Browser-first workflow across different projects and machines.

## Required capability preflight

Before any startup step, confirm `cursor-ide-browser` MCP tools are available.

If unavailable:
- Print the expected inspector URL for the project.
- Stop immediately.
- Do not fall back to opening the OS browser.

## Package manager detection

Detect the package manager from the project root before running scripts:
- `pnpm-lock.yaml` -> `pnpm run`
- `yarn.lock` -> `yarn`
- otherwise -> `npm run`

Never hardcode `pnpm`.

## Execution model

Use two paths only.

### Path A: canonical (`dev:inspect` exists)

1. Resolve `<pmRun>` from package manager detection.
2. Confirm `dev:stop` exists. If missing, fail with a clear message.
3. Run `<pmRun> dev:stop`.
4. Launch `<pmRun> dev:inspect` in the background (`Shell` with `block_until_ms: 0`).
5. Record the background terminal id and process id.
6. Run a short `Await` poll (2-3 seconds) to verify startup logs and no immediate crash.
7. Continue to readiness gate.

### Path B: generic fallback (`dev:inspect` absent)

1. Resolve `<pmRun>` from package manager detection.
2. Confirm `dev:stop` exists. If missing, fail with a clear message.
3. Run `<pmRun> dev:stop`.
4. Read `package.json` to detect worker script in priority order:
   - `dev:worker`
   - `dev`
5. Detect inspector launch in priority order:
   - `inspect`
   - `node scripts/sunpeak-inspect.mjs` (only if script file exists)
6. Read `docs/e2e-testing.md` or `README.md` to discover the exact inspector URL and any `simulation` query parameter.
7. If docs are absent, use safe defaults as hints only:
   - worker port hint: `8787`
   - inspector port hint: `8710`
8. Start worker in background and record terminal id.
9. Start inspector in background and record terminal id.
10. Short `Await` poll (2-3 seconds) for both processes.
11. Continue to readiness gate.

## Readiness gate

Do not navigate immediately after process start.

1. Poll `http://localhost:<inspectorPort>/` in 5-second intervals for up to 120 seconds.
2. After a successful HTTP response, take `browser_snapshot`.
3. Confirm a real Sunpeak UI landmark is present (for example tool list panel or inspect layout controls).
4. If only the port responds but no Sunpeak landmark appears, keep polling until timeout.
5. On timeout, report startup output and stop.

## Cursor Browser inspection flow

After readiness passes:

1. Navigate to the exact inspector URL.
2. Take `browser_snapshot`.
3. Verify tools list is visible.
4. Exercise at least one tool call.
5. Verify tool response renders in the preview/widget panel.
6. Check `browser_console_messages` for runtime errors.
7. Take a screenshot for confirmation artifacts.

Never use `open`, `dev:inspect:open`, or any OS-browser launch path.

## Teardown and safety

Use only project-native teardown:
- Run `<pmRun> dev:stop`

Do not use raw global process-kill fallbacks (`netstat/taskkill`, `lsof/kill`) from this skill.

Reason: global port-kill can terminate unrelated processes on shared machines.

After teardown, report:
- the terminal ids created by this run
- that `dev:stop` was used to terminate processes

## Project-specific canonical defaults (vega-viewer-mcp-server)

For this project, prefer the known inspector URL:

`http://localhost:8710/?simulation=preview_spec`

Treat this as authoritative unless project docs explicitly change it.
