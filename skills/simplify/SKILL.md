---
name: simplify
description: Refine recently changed code for clarity, consistency, and maintainability without changing behavior. Use when the user explicitly asks to simplify, clean up, or lightly refactor touched code, reduce local complexity, remove redundancy, improve naming or structure, or make recent edits easier to read while preserving outputs, interfaces, tests, security, and accessibility.
---

# Simplify

Use this skill for narrow, behavior-preserving cleanup after code already exists. Favor local refinements over redesign.

## Workflow

1. Read the governing instructions for the repo and files you touch, starting with `AGENTS.md` and any closer scoped instructions.
2. If the repo has Brainerd memory (`brain/.brainerd-version`, `brain/index.md`, or `brain/principles.md`), read it before non-trivial work.
3. Determine the smallest valid scope:
   - use the recent diff when version control clearly shows the touched code
   - otherwise use the files or ranges named by the user
   - otherwise inspect the smallest plausible local area and avoid widening scope without a reason
4. Identify safe simplifications inside that scope:
   - reduce unnecessary branching or nesting
   - inline needless indirection
   - remove dead or duplicated code
   - improve names when the meaning becomes clearer
   - replace clever compact code with explicit code
   - delete comments that only narrate obvious code
5. Preserve behavior while simplifying:
   - do not change outputs, side effects, or error handling unless the user asks
   - do not change public interfaces unless the request clearly includes it
   - do not simplify away security, accessibility, tests, or explicit product requirements
6. Follow local conventions instead of imposing blanket style rules. Prefer what the repo already does unless the current code is clearly inconsistent or harmful.
7. Stop before broader redesign. If the real fix requires API changes, module boundary changes, abstraction changes, or architecture work, switch to `$simple-code` instead of stretching this skill.
8. Verify with the smallest relevant checks available for the touched scope: targeted tests, type checks, linters, or other local validation signals.

## Boundaries

Use `$simplify` for concrete post-edit cleanup of recent or specified code.

Use `$simple-code` for broader design simplification such as APIs, module boundaries, abstraction choices, test strategy, or architecture tradeoffs.

## Reporting

When finishing:

- summarize the meaningful simplifications
- note what you verified
- call out any risk, ambiguity, or area left unvalidated
