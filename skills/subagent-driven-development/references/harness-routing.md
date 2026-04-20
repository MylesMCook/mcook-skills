# Harness-Aware Routing Reference

Use this when the current harness is unclear, when model selection materially affects cost or latency, or when the user wants concrete defaults for a specific environment.

## Detection

Prefer these signals in order:

1. explicit system, developer, or user statement
2. harness-specific tools, commands, or UI labels
3. visible model names or agent settings
4. local harness docs or config files in the workspace
5. fallback to `unknown`

Record a short profile before routing work:

- Harness: `codex-host`, `codex-cli`, `claude-code`, `gemini-cli`, `openai-chatgpt`, or `unknown`
- Can spawn fresh workers?
- Worker dispatch path: host subagents, task tool, external CLI, or inline fallback
- Can pin a model per worker?
- Can set reasoning effort?
- Can switch models mid-session?
- Auth source viable: user session, API key, helper, or mixed
- Sandbox, approval, and filesystem state inherited by workers?
- Session state persistent enough to reuse, or does it need cleanup after each worker?
- Is native fan-out strict enough to use for isolated workers?
- Can isolate browser sessions?
- Can parallelize safely?

If a control is unavailable, do not fake it. Preserve the same routing logic through scope, sequencing, and prompt specificity instead.

Apply explicit user, repo, or org routing rules first. Optional local presets tune defaults only after the harness is known.

## Role Classes

- **Controller:** strongest available reasoning and coding setup. Use it for decomposition, conflict resolution, review arbitration, final verification, and risky task prompts.
- **Implementer:** fastest setup that should still pass review for the task class. Use it for bounded edits, focused diffs, test follow-through, and mechanical execution once the design is settled.
- **Reviewer:** smallest setup that can inspect the diff accurately for the risk level. Escalate for risky, user-visible, or shared-contract changes.
- **Explorer:** cheapest fast read-only worker. Promote only when synthesis or design judgment is needed.

Baseline reasoning:

- **Explorer:** minimal or low
- **Implementer:** low for narrow tasks, medium for bounded multi-file work
- **Reviewer:** low for targeted review, medium for full review
- **Controller:** medium by default, high only when ambiguity or arbitration justifies it

Reserve maximum reasoning for rare controller-only deadlocks, not routine execution.

## Routing Policy

1. Prefer shrinking the task and tightening context before jumping to a larger model.
2. Start implementers on the cheapest model that can reliably handle the task class.
3. Promote when you see ambiguity, repeated misses, review failures, or cross-file reasoning demands.
4. Use stronger models for architecture changes, migrations, shared contracts, novel algorithms, unclear bug hunts, and review arbitration.
5. Use cheaper or faster models for narrow edits, docs, mechanical renames, settled test follow-through, and structured inventory work.
6. Once a stronger model resolves the ambiguous part, move follow-on execution back to a cheaper tier unless the remaining work is still risky.

## Harness Profiles

### `codex-host`

- Auth source viable: host session, plus any configured helper-backed auth
- Sandbox / approval inheritance: workers inherit host sandbox and approval state; host subagents alone do not make a worker reviewer-safe
- Session persistence / cleanup: host session can persist across workers; clean up browser state, temp files, and leftover subagents explicitly
- Native fan-out strict enough to use?: yes, when host subagents are available and isolation is still adequate
- Notes: use host subagents directly; do not route host worker tasks through the Codex CLI to fake delegation

### `codex-cli`

- Auth source viable: local CLI auth, helper-backed auth, or whatever the CLI session exposes
- Sandbox / approval inheritance: CLI workers do not inherit a host subagent sandbox model; each spawned command or process needs its own safety check
- Session persistence / cleanup: process-local state may persist within a CLI session; clean up shells, files, and temp artifacts manually
- Native fan-out strict enough to use?: no, not as a substitute for host subagents
- Notes: use direct CLI execution for local worker loops only when no host worker mechanism exists

### `claude-code`

- Auth source viable: interactive OAuth auth for normal scripted workers; API key or helper-backed auth only when explicitly using `--bare`
- Sandbox / approval inheritance: scripted workers need explicit permission and tool constraints; do not assume GUI/session approvals carry over
- Session persistence / cleanup: session state can linger in interactive use; scripted workers need explicit cleanup between runs
- Native fan-out strict enough to use?: partial at best; prefer explicit worker orchestration instead of assuming native isolation
- Notes: `claude --help` is incomplete, `--max-turns` works in print mode, and `--bare` changes auth to API key/helper only, so do not use it when the required auth source is OAuth

### `gemini-cli`

- Auth source viable: interactive login or configured helper/API-backed auth, depending on the launch mode
- Sandbox / approval inheritance: approval mode does not guarantee non-mutation by itself; use a disposable copy sandbox when process sandboxing is unavailable
- Session persistence / cleanup: session state can persist across turns; clean up worker state and output files explicitly
- Native fan-out strict enough to use?: partial; use routing classes, but do not treat plan mode as a full safety boundary
- Notes: `pro` and `flash` are routing classes or aliases, and `--approval-mode plan` is not enough by itself for non-mutation guarantees

### `openai-chatgpt`

- Auth source viable: host user session, plus any configured helper-backed auth
- Sandbox / approval inheritance: host workers inherit the active chat session context; isolate write scope and approval assumptions per worker
- Session persistence / cleanup: session state persists by default; clean up scratch artifacts and browser state between workers
- Native fan-out strict enough to use?: yes, when the host exposes fresh subagents or task workers
- Notes: use the host worker mechanism directly; keep the controller in charge of review and verification

### `unknown`

- Auth source viable: unknown
- Sandbox / approval inheritance: unknown
- Session persistence / cleanup: unknown
- Native fan-out strict enough to use?: no
- Notes: fall back to role classes, narrow prompts, and conservative sequencing

## `codex-host` / `openai-chatgpt`

Use this when the harness clearly exposes `codex-host` or `openai-chatgpt` model controls. If the user, repo, or org provides a stronger routing rule, use that instead.

In `codex-host` or `openai-chatgpt`, "fresh worker" means the host's fresh subagent or task-worker mechanism when it is available. Do not invoke `codex exec` from inside Codex to simulate a worker. If host subagents are unavailable, preserve the manager loop inline with tighter prompts and separate review passes.

- **Controller:** `gpt-5.4`
  - `medium` for normal orchestration
  - `high` for architecture, root-cause debugging, or review arbitration
  - `xhigh` only for rare synthesis deadlocks where smaller steps already failed
- **Implementer:** `gpt-5.4-mini`
  - `low` for narrow mechanical tasks
  - `medium` for bounded multi-file edits
  - promote to `gpt-5.4` after repeated misses, hard ambiguity, or broad coupling
- **Spec reviewer:** `gpt-5.4-mini` for targeted low-risk review; `gpt-5.4` for full or risky review
- **Code-quality reviewer:** same as spec review, but bias upward for cross-cutting, user-visible, or hard-to-test changes
- **Explorer:** `gpt-5.3-codex-spark` only when available and the task is shallow, text-only, read-only, and latency-sensitive; otherwise use `gpt-5.4-mini`

Do not use Spark for implementation, risky review, browser work, image understanding, broad tool use, cross-file synthesis, or nuanced review judgment.

If the harness only exposes the GPT-5.4 family, that is enough. Use `gpt-5.4` for the controller and riskier reviews, and `gpt-5.4-mini` for implementers, targeted reviews, and explorers.

If the OpenAI-based environment does not expose per-worker model controls, keep the same role separation through narrower prompts, separate passes, and reasoning-effort changes where available.

## Other Harness Families

In `claude-code`, map the flagship reasoning model to controller, the midsize coding model to implementer, the most reliable diff reader to reviewer, and the cheapest fast model to explorer.

In `gemini-cli`, map `pro` to controller or stronger review, `flash` to implementer or explorer, and only treat plan mode as a routing hint; do not assume it prevents mutation.

In unknown or mixed environments, use capability labels only and promote based on observed failures rather than instinct.

## Escalation

Escalate in this order:

1. shrink the task
2. tighten the context
3. raise reasoning one step
4. promote one model tier
5. split or serialize coupled work
6. pull the task back to the controller

## Prompting Implications

When the harness supports explicit model or reasoning hints, include them in the worker request or agent definition.

When the harness exposes host subagents, dispatch workers through that mechanism directly. Do not route Codex-hosted worker tasks through the Codex CLI.

When the harness does not support them:

- keep prompts shorter and sharper for smaller models
- narrow write scope more aggressively
- separate implementation from review into distinct passes
- promote only when evidence says the cheaper setup is failing

## Hard Rules

- Never claim a model is available unless the harness exposes it.
- Never assume Spark exists outside `codex-host` or `openai-chatgpt`.
- Never keep every worker on maximum reasoning by default.
- Never keep a cheap reviewer after repeated misses.
- Never confuse latency optimization with correctness verification.
- Never invoke Codex CLI from inside Codex to fake subagent dispatch.
