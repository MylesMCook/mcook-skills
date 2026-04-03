---
name: microinteractions
description: Use this skill when the user needs to design or audit one contained interaction moment such as button states, validation, loading, toggles, confirmations, undo, or other small state changes that need to feel clear, responsive, and trustworthy.
---

# Microinteractions

Use this skill for one contained product moment at a time: a save button, toggle, validation state, pull-to-refresh, retry flow, undo pattern, loading state, or confirmation moment.

## Workflow

1. Define the moment in one sentence:
   - moment
   - user goal
   - context
   - risk level
2. Map the four core parts:
   - trigger
   - rules
   - feedback
   - loops or modes
3. Pressure-test the trust-breaking edges:
   - repeated taps
   - slow network, offline, or timeout
   - interruption or navigation away
   - partial success
   - undo, cancel, or retry
   - empty, disabled, loading, error, and success states
   - first-time versus repeat use
4. Simplify before embellishing. Prefer one obvious primary action, honest progress, visible alternatives to hidden gestures, and undo over scary confirmation flows when it is safe.
5. Check accessibility and platform fit, especially keyboard or focus behavior, touch targets, color-independent state changes, reduced motion, and screen-reader announcements for important changes.
6. Return one default recommendation in a useful shape. For implementation-heavy requests, translate it into a compact state table, transition rules, copy, timing, and accessibility notes.

## Output Shape

Use this structure unless the user asks for a different format:

```md
## Microinteraction
## User goal
## Trigger
## Rules
## Feedback
## Loops / Modes
## Edge cases
## Accessibility & platform fit
## Simplify / signature moment
## Recommended changes
```

## References

Load only the files that match the problem:

- [references/trigger-design.md](references/trigger-design.md) for discoverability, affordance, gestures, placement, or control states
- [references/rules-and-state.md](references/rules-and-state.md) for validation, sequencing, async behavior, retries, or failure handling
- [references/feedback-patterns.md](references/feedback-patterns.md) for responsiveness, loading, progress, animation, haptics, sound, or accessible feedback
- [references/loops-modes.md](references/loops-modes.md) for repeat use, onboarding hints, personalization, notification cadence, or modal behavior
- [references/signature-moments.md](references/signature-moments.md) when the user wants delight, brand expression, or a memorable detail
- [references/case-studies.md](references/case-studies.md) when a worked example would help

## Guardrails

- Keep the scope on the moment, not the whole product.
- For net-new design, propose one default design rather than a menu of equal options.
- For audits, prioritize trust gaps, missing states, and misleading behavior.
- Do not add delight that slows down completion, especially for destructive, financial, or urgent actions.
