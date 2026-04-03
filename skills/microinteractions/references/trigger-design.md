# Trigger Design

Use this file when the question is mainly about discoverability, affordance, gesture safety, control states, or where an action should live.

## Trigger Checklist

For any trigger, answer:

1. Can a first-time user find it quickly?
2. Does its appearance match the action?
3. Is the primary action visually more prominent than nearby alternatives?
4. Are all meaningful states visible?
5. If the trigger is hidden or gestural, is there a visible fallback?

## Trigger Types

### Manual triggers

Use for direct user intent:

- tap or click
- type
- drag
- swipe
- long press
- keyboard shortcut
- voice

### System triggers

Use when the system should respond to a condition:

- threshold crossed
- new data arrived
- time elapsed
- state changed
- error detected
- inactivity timeout

System triggers should be relevant, suppressible when appropriate, and calibrated to avoid alert fatigue.

## Control-State Minimum

Most interactive controls need these states:

| State | Why it matters |
| --- | --- |
| Default | Shows availability |
| Hover / focus | Confirms interactivity and supports non-pointer users |
| Pressed / active | Confirms the action registered |
| Disabled | Explains unavailability |
| Loading | Prevents duplicate action and signals work in progress |

Common additional states:

| State | Use when |
| --- | --- |
| Selected / on | Toggle or persistent state |
| Error | Validation or failed action |
| Success | Briefly confirm completion |

## Hidden-Trigger Safety

Hidden gestures are acceptable only when they are:

- a shortcut for an already-available action
- aligned with platform conventions
- non-destructive or easily undoable
- teachable at the right moment

Avoid relying on a hidden gesture as the only path to a critical action.

## Placement Heuristics

Prefer:

- primary action near the main task flow
- destructive actions visually separated
- frequent actions easier to reach than rare ones
- inline actions for inline content
- bottom-third reachability on mobile when the action is frequent

## Trigger Spec Template

```md
Trigger:
- Type:
- Discoverability:
- States shown:
- Placement:
- Visible fallback (if any):
- Duplicate-action handling:
```
