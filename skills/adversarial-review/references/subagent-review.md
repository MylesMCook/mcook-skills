# Codex Subagent Review

## Contract

Run exactly three ordinary fresh Codex subagents and label their returned results as:

- `codex-skeptic`
- `codex-architect`
- `codex-minimalist`

These labels are not required custom agent names or config files. Each subagent receives the same review target and repo rules, but a different lens. Run them in parallel when the host supports it. Collect final messages from all three before synthesis.

## Sandbox And Approvals

Codex subagents inherit the parent sandbox policy and approval state. They do not provide stronger isolation than the parent session. If the host exposes a read-only subagent option, use it. Otherwise, prompt reviewers to stay read-only and use a pre/post worktree check when reviewing a git worktree.

For git worktrees, record `git status --short` before launch and compare it after all subagents finish. If unexplained new changes appear during review, report `INCOMPLETE_COVERAGE`.

If the host cannot spawn subagents, return `CONTESTED` with `SUBAGENT_UNAVAILABLE`. Do not use outside reviewer tools or a single-agent fallback.

## Coverage Failures

A review has incomplete coverage when any required subagent:

- cannot be spawned
- fails before returning a final message
- times out
- returns empty or unusable output
- ignores the assigned lens
- performs or attempts a mutating action

Classify the issue with one of:

- `SUBAGENT_UNAVAILABLE`
- `SUBAGENT_FAILED`
- `TIMEOUT`
- `MALFORMED_OUTPUT`
- `INCOMPLETE_COVERAGE`
- `CALLER_MISUSE`

Incomplete coverage forces `CONTESTED` unless there is already an accepted high-severity finding, in which case return `REJECT`.

## Output Handling

Do not create `.tmp` review files by default. Use the subagents' returned final messages. If the user explicitly asks to save reviewer artifacts, write only after confirming the target location and keep artifacts out of committed source unless requested.
