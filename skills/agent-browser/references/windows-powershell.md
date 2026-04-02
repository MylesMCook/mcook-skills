# Windows and PowerShell

This machine runs PowerShell 5. Treat it as a different shell environment from Bash.

## Rules

- Quote refs: `agent-browser click '@e1'`
- Set `AGENT_BROWSER_SESSION` explicitly for each scenario
- Do not use Bash-style `&&`
- Prefer separate invocations when intermediate output matters
- Use `focus` plus `press Enter` when a dialog button click appears to no-op

## Session Setup

```powershell
$runId = "probe-$(Get-Date -Format yyyyMMdd-HHmmss)"
$env:AGENT_BROWSER_SESSION = "$runId-auth"
```

## Safe Stepwise Pattern

```powershell
agent-browser open https://example.com/login
agent-browser snapshot -i --json
agent-browser fill '@e1' 'user@example.com'
agent-browser fill '@e2' 'password'
agent-browser snapshot -i --json
agent-browser click '@e3'
agent-browser wait 1500
agent-browser get url
```

## Session Persistence Distinction

- `AGENT_BROWSER_SESSION` or `--session`: isolated ephemeral browser context
- `AGENT_BROWSER_SESSION_NAME` or `--session-name`: persisted cookies and localStorage across runs

Use `--session-name` only when you want that persistence.

## Wait Strategy

`wait --load networkidle` works well on simple pages. On SPAs or sites with persistent traffic, prefer:

- `wait <selector>`
- `wait --url <pattern>`
- `wait 1500` or another fixed delay as a last-resort stabilization step
