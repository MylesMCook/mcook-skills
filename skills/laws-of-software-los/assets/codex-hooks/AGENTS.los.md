# Laws of Software (LOS) Code Mode

Use this file as optional `AGENTS.md` content when you want repository-local reinforcement alongside Codex hooks.

## Always-on code contract

When creating or changing code:

1. Prefer the smallest reversible change that solves the real problem.
2. Do not introduce speculative frameworks, platforms, abstractions, or future-proofing without evidence.
3. Preserve public/API behavior unless versioning, deprecation, migration, compatibility notes, and contract tests are included.
4. Never hardcode secrets, disable auth/security/TLS, or hide failing validation.
5. Add or update focused tests for production code changes; if no test is practical, state the risk and the compensating validation.
6. Give remote calls explicit timeouts/cancellation and bounded retry/backoff behavior.
7. Give async/event/queue flows idempotency, dedupe, retry/backoff, DLQ/replay, and observability.
8. Give data migrations rollback/reconciliation/backup/restore or expand/contract safety.
9. Add logs/metrics/traces/alerts for production failure modes.
10. Final answer must state validation run and any remaining risk.

Run:

```bash
python3 .codex/hooks/laws-of-software-los/los_code_gate.py --repo . --changed
```

Fix Blocker/High findings before final output, or clearly mark the result as non-production-ready.
