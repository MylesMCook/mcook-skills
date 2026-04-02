# Session Management

Use sessions to isolate browser state, not to share refs.

## Core Rules

- `AGENT_BROWSER_SESSION` and `--session` isolate cookies, storage, tabs, and history.
- Refs from `snapshot` are valid only inside the same session and current page state.
- `--session-name` persists cookies and localStorage across browser restarts. It is not the same thing as `AGENT_BROWSER_SESSION`.
- Close sessions when you are done, especially after local QA runs.

## What Is Isolated

Each session gets its own:

- cookies
- localStorage and sessionStorage
- IndexedDB
- cache
- history
- tab set

## Recommended Naming

Use semantic names:

```text
<run-id>-login
<run-id>-events
<run-id>-mobile
<run-id>-wikipedia
```

For local app testing, this makes screenshots, logs, and scenario notes line up cleanly.

## Ephemeral Session Pattern

PowerShell:

```powershell
$env:AGENT_BROWSER_SESSION = "probe-$(Get-Date -Format yyyyMMdd-HHmmss)-$([guid]::NewGuid().ToString('N').Substring(0,4))"
agent-browser open https://example.com
```

Bash:

```bash
export AGENT_BROWSER_SESSION="probe-$(date +%Y%m%d-%H%M%S)-$(openssl rand -hex 2)"
agent-browser open https://example.com
```

## Persistence Pattern

Use `--session-name` only when you intentionally want auth restored across runs:

```bash
agent-browser --session-name myapp open https://app.example.com/login
# ... login ...
agent-browser close

agent-browser --session-name myapp open https://app.example.com/dashboard
```

## Parallel vs Serial

Parallel sessions are fine for low-interaction scraping or independent snapshots.

Prefer serial execution when:

- validating the CLI itself
- running mutation-heavy CRUD flows
- debugging timing-sensitive issues
- collecting evidence from a single dev environment

Interactive QA on one machine is usually less noisy when each scenario runs to completion before the next begins.

## Cleanup

```bash
agent-browser session list
agent-browser close
agent-browser close --all
```

Use `close --all` only when you are intentionally clearing the whole machine state. Otherwise close only the sessions you created for the current task.
