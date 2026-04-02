# Evidence Capture and Triage

Collect enough evidence to tell the difference between an app bug, a timing problem, and a stale locator.

## Minimum Evidence Per Scenario

- final URL
- final title
- `errors`
- one screenshot

For mutations, also collect:

- `network requests --clear` before the action
- `network requests --filter '/api/'` after the action

## Useful Commands

```bash
agent-browser get url
agent-browser get title
agent-browser errors
agent-browser console
agent-browser screenshot ./shot.png
agent-browser network requests --clear
agent-browser network requests --filter '/api/'
```

## Triage Ladder

### 1. Confirm the route

If the page is blank or wrong, first confirm the URL is the route you intended.

### 2. Confirm the widget state

If you just opened a dialog, combobox, menu, or sheet, re-snapshot before acting.

### 3. Confirm the action actually fired

If a mutation is expected, check the network log. No request usually means:

- stale ref
- wrong target
- closed or rerendered dialog
- keyboard focus issue

### 4. Try a fallback input method

When `click` no-ops on a visible enabled control:

```bash
agent-browser focus @e7
agent-browser press Enter
```

### 5. Capture the failure cleanly

Take a screenshot and store the exact URL and command pattern that failed.
