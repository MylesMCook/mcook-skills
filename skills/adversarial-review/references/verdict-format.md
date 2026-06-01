# Verdict Format

## Intent

<what the author is trying to achieve>

## Reviewer Coverage

- codex-skeptic / Skeptic: success | failed | not run
- codex-architect / Architect: success | failed | not run
- codex-minimalist / Minimalist: success | failed | not run

## Verdict: PASS | CONTESTED | REJECT

<one-line summary>

## Findings

<numbered list ordered by severity: high -> medium -> low>

For each finding include:

- **[severity]** Description with file:line references
- Reviewer: which Codex subagent raised it
- Lens: which reviewer lens raised it
- Evidence: what concrete code path, diff hunk, or failure scenario supports it
- Recommendation: concrete action, not vague advice
- Lead judgment: accept | reject - one-line rationale

Reject or demote any finding that lacks concrete evidence.

## What Went Well

<1-3 things the reviewers found no issue with>

## Coverage Failures / Evidence Gaps

<missing reviewers, failed runs, thin evidence, or unresolved uncertainty>

When applicable, name the exact failure class:

- `SUBAGENT_UNAVAILABLE`
- `SUBAGENT_FAILED`
- `TIMEOUT`
- `MALFORMED_OUTPUT`
- `INCOMPLETE_COVERAGE`
- `CALLER_MISUSE`

## Lead Judgment

<brief synthesis that says what should block ship and what should not>

## Verdict Logic

- **PASS** - all three reviewers completed and no accepted high-severity findings remain; accepted medium or low findings may remain as non-blocking recommendations
- **CONTESTED** - coverage is incomplete, a high-severity claim remains materially disputed, or evidence is too thin to clear the change
- **REJECT** - at least one accepted high-severity finding blocks ship
