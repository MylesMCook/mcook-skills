# Feedback Patterns

Use this file when the question is about responsiveness, loading, progress, animation, sound, haptics, or accessible state change.

## What Feedback Must Do

Good feedback answers:

1. Did the action register?
2. What is happening now?
3. What should the user expect next?

## Feedback Hierarchy

Match the weight of feedback to the weight of the event.

| Event level | Typical feedback |
| --- | --- |
| Tiny (hover, focus) | subtle visual change |
| Small (tap, toggle) | immediate state change |
| Medium (save, send) | state label + loading + completion |
| Large (purchase, publish, delete) | stronger confirmation, often with undo |
| Critical (failure, blocked action) | persistent, actionable message |

## Timing Defaults

These are useful defaults, not rigid laws:

- immediate press acknowledgment: under 100 ms
- show a loading state as soon as the user would otherwise doubt the action registered
- if work lasts more than a brief moment, show visible in-progress feedback
- if duration is known and material, prefer progress over a spinner
- success feedback should be noticeable but brief
- error feedback should persist long enough to act on

## Honest Loading

Never imply certainty you do not have.

Prefer:

- spinner for unknown duration
- progress bar when progress is meaningfully knowable
- skeletons only when they resemble incoming layout
- explicit retry or fallback on timeout
- copy that distinguishes "working" from "done"

## Channel Guidance

### Visual

Primary channel for most products. Use state change, copy, motion, iconography, and proximity to the source.

### Audio

Use sparingly for important confirmations or urgent alerts. Never make audio the only signal.

### Haptics

Use for tactile confirmation on mobile or device-specific contexts. Match system settings and action importance.

## Accessibility Checks

Always pressure-test feedback against:

- not relying on color alone
- visible focus indicators
- screen-reader announcement needs for important state changes
- reduced-motion alternatives
- accessible names for loading and progress states
- non-audio fallbacks for any sound cue

## Feedback Spec Template

```md
Feedback:
- Immediate acknowledgment:
- In-progress state:
- Success state:
- Error state:
- Optional audio/haptic:
- Accessibility notes:
```
