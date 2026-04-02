# Local Dev App E2E Pattern

Use `agent-browser` as the browser executor and keep app bootstrap outside the browser.

## Suggested Run Contract

- choose a run id such as `app-ab-20260401-2230`
- use one session per scenario
- write screenshots and notes into a run folder
- keep a manifest with final URL, title, screenshots, and findings

Example session names:

```text
app-ab-20260401-2230-auth
app-ab-20260401-2230-events
app-ab-20260401-2230-mobile
```

## Scenario Checklist

For each scenario:

1. open the route
2. snapshot
3. perform the action
4. re-snapshot after route or widget changes
5. capture:
   - final URL
   - title
   - page errors
   - console output when useful
   - network requests for mutations
   - at least one screenshot
6. restore baseline if the scenario mutates persistent state

## Route Sanity

Before blaming `agent-browser`, confirm the route is real in the app. A blank page on the wrong route is an app-path problem, not a browser-automation failure.

## Mutation Verification

For create, update, delete, or toggle flows:

```bash
agent-browser network requests --clear
# perform action
agent-browser wait 1500
agent-browser network requests --filter '/api/'
```

This quickly distinguishes:

- successful UI action with server mutation
- UI no-op
- route mismatch
- client-side error

## Mobile Pass

Include at least one narrow viewport run:

```bash
agent-browser set viewport 390 844
```

Test:

- login
- navigation sheet or drawer
- one main list route
- one settings or CRUD route
