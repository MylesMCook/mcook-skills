---
name: laws-of-software-los
description: >-
  Use when software architecture, migrations, reviews, reliability,
  performance, security, observability, or incidents need explicit tradeoffs,
  the smallest reversible path, and concrete validation. Trigger on design,
  ADR, refactor, and review work. Skip tiny syntax fixes, mechanical
  formatting, and non-software tasks.
---

# Laws of Software (LOS)

Apply this skill when software work needs principal-level judgment, explicit tradeoffs, and a credible validation path.

This skill is original synthesis inspired by the public law list at `https://lawsofsoftwareengineering.com/`. Use the source site for canonical law descriptions and updates.

## Default posture

- Prefer the smallest reversible design.
- Preserve compatibility unless a migration plan says otherwise.
- Assume failure across remote or distributed paths.
- Treat data changes as dangerous.
- Keep security and operability in scope.
- Name the tradeoffs and the remaining risk.

## When to use

- architecture, system design, APIs, service boundaries, or infrastructure direction
- RFCs, ADRs, migration plans, incidents, codebase structure, or technical strategy
- code changes where data safety, compatibility, reliability, security, or operability matter
- distributed systems, scalability, performance, technical debt, testing, rollout, rollback, or team ownership

Do not use this skill for tiny syntax fixes, rote formatting, or non-software work.

## Working loop

1. Frame the real problem.
   State the goal, actors, constraints, non-goals, and success signal. If a missing fact would not change the answer, make a minimal assumption and proceed.
2. Map the current system.
   Inspect boundaries, ownership, dependencies, trust boundaries, runtime, and failure domains before changing anything.
3. Generate the smallest credible path.
   For architecture work, compare 2-4 viable options and always include the simplest one. For code work, prefer the smallest safe patch.
4. Stress-test with the relevant laws.
   Use `references/law-index.md` only when it will change the answer. Pick 3-8 laws, not all 56.
5. Decide and verify.
   Make rationale, rollout, rollback, and validation explicit. Run relevant scripts or repo checks when they materially help.
6. Close with evidence.
   State the recommendation or change, what was validated, and the remaining material risk.

## Response default

- Start with a recommendation.
- Then cover the key tradeoffs, the validation or rollout/rollback plan, and the remaining risk.
- For code-producing tasks, add focused tests or say exactly what narrower validation ran and why.

## Law groups

Use `references/law-index.md` when you need the full 56-law pass. Common groups:

- architecture and distributed systems
- teams and ownership
- planning and estimation
- quality, testing, and evolution
- scale and performance
- local design and code clarity
- decision quality and bias

Do not law-dump. Use the 3-8 laws that change the answer.

## Guardrails

- Microservices are not the default.
- Rewrites are guilty until proven necessary.
- Performance claims without workload and evidence are guesses.
- "Future-proofing" needs a near-term scenario.
- Distributed flows need timeouts, retry bounds, idempotency, backpressure, consistency decisions, and observability.
- A design with no owner, migration plan, or rollback path is not production-ready.
- A code change with no tests or explicit validation is not production-ready.

## Optional Codex hooks

Use repo or machine hooks only when the user explicitly wants LOS guardrails to stay active across a session or repository.

Install from the skill root:

```bash
python3 scripts/install_codex_hooks.py --repo /path/to/repo
python3 scripts/install_codex_hooks.py --scope global
```

Read `references/codex-hooks.md` before changing hook behavior. The hooks are guardrails, not a security boundary. Current Codex docs do not support the hook flow on Windows.

## Scripts

Run these from the skill root when they fit the artifact in front of you:

```bash
python3 scripts/los_code_gate.py --repo . --changed
python3 scripts/los_code_gate.py --repo . --changed --json
python3 scripts/los_code_gate.py --input path/to/file.py
python3 scripts/los_code_gate.py --stdin < assistant-output.md

python3 scripts/arch_law_check.py --input path/to/design.md
python3 scripts/arch_law_check.py --input path/to/design.md --json
python3 scripts/adr_lint.py --input path/to/adr.md
```

Use the scripts as heuristic reviewers. They help catch omissions; they do not replace judgment.

## References

Load only what the task needs:

- `references/architecture-playbook.md` for concrete system-design guidance
- `references/review-rubrics.md` for architecture, API, migration, planning, or code-structure reviews
- `references/decision-frameworks.md` for technology choices, metrics, and cognitive traps
- `references/prompts-and-templates.md` for polished answer structures
- `references/codex-hooks.md` for hook installation or tuning
- `references/evaluation-guide.md` for trigger and output evaluation

Use templates in `assets/` when they save time; do not load them by default.
