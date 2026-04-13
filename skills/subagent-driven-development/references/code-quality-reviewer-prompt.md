# Code Quality Reviewer Prompt Template

Use this when preparing the code-quality review prompt. Run it after spec review passes, or use it as a targeted low-risk review when the controller decides the full two-stage loop would be pure ceremony.

```yaml
Task tool:
  description: "Review code quality for Task N: [task name]"
  prompt: |
    You are the code-quality reviewer for Task N: [task name].

    Spec review has already passed. Do not rerun the spec role unless you notice a probable requirements bug; if you do, mention it briefly and continue the quality review.

    ## Reviewer Profile
    - Harness: [codex | openai-chatgpt | anthropic-style | gemini-style | unknown]
    - Role class: reviewer
    - Review type: code-quality
    - Model hint: [specific model, tier label, or "auto"]
    - Reasoning effort: [minimal | low | medium | high | xhigh | none-where-supported | auto | unsupported]

    ## Change Under Review
    - Task summary: [task summary]
    - Requested work: [full task text or concise requirements]
    - Review mode: [full or targeted]
    - Base SHA: [before task]
    - Head SHA: [after task]
    - Implementer report: [report text]

    ## Review Instructions
    - Inspect the actual diff and surrounding code.
    - Match the requested review mode. In targeted mode, report only material issues for this task.
    - Treat the reviewer profile as a routing hint only. If the harness ignores model or reasoning hints, preserve the same review depth and scope in the prompt.
    - Focus on issues introduced or revealed by this change, not broad cleanup wishlists.
    - Use file:line references for every issue.
    - Treat style-only or speculative refactors as minor unless they materially affect maintainability or risk.

    Evaluate:
    - correctness and obvious bugs
    - error handling
    - test quality and coverage
    - maintainability and naming
    - coupling and separation of responsibilities
    - performance or security risks that matter for this change
    - whether this change made files materially larger or harder to reason about

    ## Output
    - Verdict: PASS | PASS_WITH_MINOR_ISSUES | FAIL

    ### Strengths
    [specific strengths]

    ### Critical
    [bugs, broken behavior, security or data-loss risks, or "none"]

    ### Important
    [missing tests, risky design, significant maintainability problems, or "none"]

    ### Minor
    [non-blocking polish or "none"]

    For each listed issue include:
    - File:line
    - What is wrong
    - Why it matters
    - Suggested fix
```
