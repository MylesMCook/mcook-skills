# Snapshot and Refs

Refs are the fastest way to drive `agent-browser`, but only when you treat them as disposable.

## Core Rules

- Refs are session-local.
- Refs are page-state-local.
- Any navigation, modal open, listbox open, popover open, sheet open, or substantial rerender can invalidate the ref you just captured.
- When in doubt, re-snapshot.

## Standard Pattern

```bash
agent-browser open https://example.com
agent-browser snapshot -i --json
agent-browser click @e1
agent-browser wait 1000
agent-browser snapshot -i --json
```

## Re-Snapshot Triggers

Always re-snapshot after:

- navigation
- form submission
- opening dialogs
- opening dropdowns or comboboxes
- opening popovers or menus
- opening mobile sheets or drawers
- actions that change filter chips, table contents, or button enabled state

This last point matters in React apps: a button that was disabled before you filled the form may need a fresh snapshot before you click it.

## Locator Ladder

Use this order:

1. fresh ref from a new snapshot
2. re-snapshot and retry
3. semantic locator:
   - `find role`
   - `find text`
   - `find label`
   - `find placeholder`
4. CSS selector
5. keyboard fallback such as `focus` plus `press Enter`

## Dynamic Widget Pattern

For listboxes, menus, and dialogs:

```bash
agent-browser click @e15
agent-browser wait 500
agent-browser snapshot -i --json
agent-browser click @e4
```

Do not assume the ref from the pre-open page is still the right one after the widget appears.

## When Click No-Ops

If a visible enabled control seems to accept `click` but nothing happens:

1. verify you are still in the expected route
2. re-snapshot
3. confirm the button is enabled with `is enabled`
4. inspect `network requests`, `errors`, and `console`
5. try `focus` and `press Enter`

This is especially useful for modal submit buttons in React apps.

## Troubleshooting

### Ref from the wrong session

Symptom:

- the ref exists in notes from a previous step but fails now

Fix:

- confirm the current `AGENT_BROWSER_SESSION`
- take a fresh snapshot in the live session

### The element is not in the snapshot

Try:

- `scroll down 400`
- `scrollintoview <selector>`
- `wait 1000`
- `snapshot -i --json`

### Too many elements

Use:

- `snapshot -s "#main" -i --json`
- semantic `find` locators
- `screenshot --annotate` for spatial debugging
