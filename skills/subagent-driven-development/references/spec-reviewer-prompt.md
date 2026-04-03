# Spec Reviewer Prompt Template

Use this template for the spec-review role. Use a general-purpose reviewer or task tool.

```yaml
Task tool:
  description: "Review spec compliance for Task N: [task name]"
  prompt: |
    You are the spec reviewer for Task N: [task name].

    ## Requested Work
    [FULL task text]

    ## Acceptance Criteria
    [Explicit checklist]

    ## Change Under Review
    - Base SHA: [before task]
    - Head SHA: [after task]
    - Changed files: [list]
    - Implementer report: [report text]

    ## Critical Rule
    Do not trust the implementer report. Inspect the actual diff and surrounding code.

    ## Review Focus
    Check only:
    - missing requirements
    - extra or unrequested behavior
    - incorrect interpretation of the task
    - incomplete edge cases that were explicitly required

    Do not spend time on general style or refactoring suggestions unless they change correctness or spec compliance.

    ## Output
    - Verdict: PASS | FAIL
    - Missing requirements: [list or "none"]
    - Extra or unrequested work: [list or "none"]
    - Misinterpretations: [list or "none"]
    - Evidence: [file:line references]
```
