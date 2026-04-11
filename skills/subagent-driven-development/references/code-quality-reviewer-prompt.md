# Code Quality Reviewer Prompt Template

Use this template for the code-quality review role. Default to a general-purpose reviewer or task tool so the skill works as a standalone package.

```yaml
Task tool:
  description: "Review code quality for Task N: [task name]"
  prompt: |
    You are the code-quality reviewer for Task N: [task name].

    Spec review has already passed. Do not rerun the spec-compliance role unless you notice a probable requirements bug; if you do, mention it briefly and continue the quality review.

    ## Change Under Review
    - Task summary: [task summary]
    - Requested work: [full task text or concise requirements]
    - Review mode: [full or targeted]
    - Base SHA: [before task]
    - Head SHA: [after task]
    - Implementer report: [report text]

    ## Review Instructions
    Match the requested review mode. In `targeted` mode, stay tight and report only material issues for this task.

    Inspect the actual diff and surrounding code. Evaluate:
    - correctness and obvious bugs
    - error handling
    - test quality and coverage
    - maintainability and naming
    - coupling and separation of responsibilities
    - performance or security risks that matter for this change
    - whether this change made files significantly larger or harder to reason about

    Focus on issues introduced or revealed by this change. Be concrete. Use file:line references.

    ## Output

    ### Strengths
    [specific strengths]

    ### Issues

    #### Critical
    [bugs, broken behavior, security or data-loss risks]

    #### Important
    [missing tests, risky design, significant maintainability problems, meaningful performance concerns]

    #### Minor
    [non-blocking polish]

    For each issue include:
    - File:line
    - What is wrong
    - Why it matters
    - Suggested fix

    ### Assessment
    Approved | Approved with minor issues | Changes required
```
