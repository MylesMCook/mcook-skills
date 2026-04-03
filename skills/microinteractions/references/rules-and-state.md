# Rules and State

Use this file when the question is about sequencing, validation, async behavior, failure handling, or state transitions.

## Goal-First Method

Before writing rules, define the user goal in one sentence.

Then derive the rules from that goal:

1. Minimum required input
2. Simplest happy path
3. Constraints and boundaries
4. Failure modes
5. Recovery path
6. Completion condition

## State Model

A useful default state model for many microinteractions is:

```text
idle
→ precheck / validation
→ loading / processing
→ success | recoverable error | terminal error
→ optional retry / undo / done
```

Add states only when they change what the user can perceive or do.

## Rules Checklist

Check all that matter:

- what happens immediately after the trigger
- whether repeat activation is prevented, queued, or ignored
- what the user can still do while processing
- minimum, maximum, or format constraints
- what happens on timeout, offline, or partial failure
- whether user input is preserved on failure
- whether the user can cancel, retry, or undo
- what happens if they leave mid-action
- how the interaction ends

## High-Trust Defaults

Prefer these defaults unless the task suggests otherwise:

- validate early when it reduces wasted effort
- preserve user-entered data on error
- disable or guard the primary trigger during loading
- use undo for reversible destructive actions
- keep failure copy specific and actionable
- return the user to a stable, understandable state

## Async-Action Spec

For buttons and similar async actions, this default often works well:

1. Press registers immediately
2. Control enters loading state immediately
3. Duplicate activation is blocked
4. Request runs
5. Success confirms completion and returns to an intelligible resting state
6. Error restores actionability and preserves user work
7. Retry path is obvious

## Compact Rule Spec Template

```md
Rules:
- Goal:
- Preconditions:
- Sequence:
- While processing:
- Prevented actions:
- Failure handling:
- Recovery path:
- End state:
```
