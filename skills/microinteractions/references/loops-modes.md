# Loops and Modes

Use this file when the interaction changes over time, repeats, adapts, teaches, or behaves differently in a mode.

## Loops

A loop answers: what happens the next time this interaction occurs?

### Closed loops

A bounded interaction with a clear end.

Examples:

- form submit
- countdown timer
- one-time confirmation

### Open loops

An interaction that continues until stopped or changed.

Examples:

- repeating alarm
- autosave
- notification cadence
- recurring reminder

## Good Loop Behavior

Prefer loops that help the user by:

- reducing repeated setup
- removing beginner hints after competence is shown
- adapting frequency downward when ignored
- preserving continuity across sessions

Be careful with loops that:

- increase interruption over time
- quietly shift defaults toward business goals
- become harder to escape
- change behavior without explanation

## Modes

A mode is a temporary state where the same control behaves differently.

Modes are risky because users carry forward the last rule they learned.

If a mode is necessary:

- make the mode unmistakable
- make entry and exit deliberate
- keep the number of modes low
- avoid hiding dangerous actions inside modes
- restore a stable default when reasonable

## Progressive Reduction

A good default is:

- more guidance on first use
- less scaffolding on repeat use
- same core meaning throughout

Example: first few sessions show a tooltip; later sessions keep the interaction but remove the hint.

## Loop / Mode Spec Template

```md
Loops / Modes:
- Repeat-use behavior:
- First-time assistance:
- Adaptation over time:
- Any modes:
- Mode visibility:
- Exit / reset behavior:
```
