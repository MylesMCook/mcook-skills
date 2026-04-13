# Preferred OpenAI / Codex Preset

Use this when the detected harness is `codex` or `openai-chatgpt` and there is no stronger user, repo, or org routing override. This is a thin overlay on top of `references/harness-routing.md`, not a replacement for it.

## Intent

- keep a strong controller
- keep most workers cheaper
- lower reasoning or shrink scope before escalating model tier
- treat Spark as an optional speed tool, not the default correctness-critical worker
- avoid leaving the entire workflow on maximum reasoning

## Default Role Map

- **Controller:** `gpt-5.4`
  - `medium` for normal orchestration
  - `high` for architecture, root-cause debugging, or review arbitration
  - `xhigh` only after at least one failed decomposition or rescoping attempt
- **Implementer:** `gpt-5.4-mini`
  - `low` for narrow edits, docs, tests after the design is settled, and mechanical changes
  - `medium` for bounded multi-file implementation
  - promote to `gpt-5.4` at `low` or `medium` before trying `high`
- **Reviewer:** `gpt-5.4-mini` for targeted low-risk review; `gpt-5.4` for full or risky review
  - start at `low` or `medium`
  - use `high` only for subtle correctness risk or controller-reviewer disagreement
- **Explorer:** `gpt-5.4-mini` at `minimal` or `low` by default
  - use `gpt-5.3-codex-spark` at `minimal` or `low` only when the harness exposes it and the task is shallow, text-only, and read-only

## Task Shortcuts

Use `gpt-5.4-mini` first for:

- local bug fixes with clear root cause
- test follow-through after the design is settled
- docs
- mechanical renames
- inventory or grep-like scans
- simple UI copy or wiring changes in known files

Use `gpt-5.4` at `low` or `medium` for:

- bounded multi-file features
- ambiguous but contained bug fixes
- tricky review work
- cross-file changes that are still local enough to stay inside one task
- any worker that is starting to fail on synthesis rather than execution

Use `gpt-5.4` at `high` or `xhigh` only for:

- controller-only architecture work
- unclear root-cause debugging after a first pass failed
- migrations, shared contracts, or broad refactors
- review arbitration or rare synthesis deadlocks

## Spark Rules

Do not use Spark as the default implementer or reviewer. Use it only for near-instant, read-only, shallow text work such as quick file inventory, locating likely symbols, or summarizing a small diff. Switch back to the GPT-5.4 family for implementation, risky review, browser work, image understanding, or multi-step synthesis.

## If the Harness Cannot Pin Per-Worker Models

If the active session is already on `gpt-5.4`:

1. emulate explorer work with `minimal` or `low` effort and very narrow read-only prompts
2. emulate implementer work with `low` or `medium` effort and strict owned write scope
3. emulate reviewer work with a fresh, separate pass and a review-specific prompt
4. reserve `high` or `xhigh` for controller arbitration passes instead of every worker-like step

## Override Rules

- explicit user model choices win
- repo or org policy wins
- task risk can override this preset upward
- hard latency or cost constraints can override it downward
- unknown harness means fall back to role classes and reasoning budgets only
