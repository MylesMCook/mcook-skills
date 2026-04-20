# Verdict Format

## Intent

<what the author is trying to achieve>

## Reviewer Coverage

- Codex reviewer / Skeptic: success | failed | not run
- Claude Code / Architect: success | failed | not run
- Gemini CLI / Minimalist: success | failed | not run

## Verdict: PASS | CONTESTED | REJECT

<one-line summary>

## Findings

<numbered list ordered by severity: high -> medium -> low>

For each finding include:

- **[severity]** Description with file:line references
- Harness: which reviewer path raised it
- Lens: which reviewer lens raised it
- Evidence: what concrete code path, diff hunk, or failure scenario supports it
- Recommendation: concrete action, not vague advice
- Lead judgment: accept | reject — one-line rationale

Reject or demote any finding about CLI flags, auth, or runtime behavior if it conflicts with current docs or local CLI evidence.

## What Went Well

<1-3 things the reviewers found no issue with>

## Harness Failures / Evidence Gaps

<missing reviewers, failed runs, thin evidence, or unresolved uncertainty>

When applicable, name the exact failure class:

- `MISSING_CLI`
- `AUTH_FAILURE`
- `TIMEOUT`
- `CAPACITY_FAILURE`
- `MALFORMED_OUTPUT`
- `INPUT_ERROR`
- `TURN_LIMIT`
- `CLI_FAILURE`
- `CALLER_MISUSE`
- `CLEANUP_FAILURE`

## Lead Judgment

<brief synthesis that says what should block ship and what should not>

## Verdict Logic

- **PASS** — no accepted high-severity findings remain
- **CONTESTED** — at least one high-severity claim remains materially disputed or under-evidenced
- **REJECT** — at least one accepted high-severity finding blocks ship
