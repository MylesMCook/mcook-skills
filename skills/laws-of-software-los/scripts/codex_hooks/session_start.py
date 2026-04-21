#!/usr/bin/env python3
from __future__ import annotations

import json
import sys


CONTEXT = """Laws of Software (LOS) mode is active.

Before generating or editing code, make the first produced solution already satisfy the LOS gate:
- KISS/YAGNI/Gall: smallest working change; no speculative framework/platform.
- Hyrum/Postel/Least Astonishment: preserve observable API behavior unless compatibility, versioning, deprecation, and tests are explicit.
- Murphy/Distributed Fallacies/CAP: every remote, async, cache, migration, and data path needs timeout/retry/idempotency/backpressure/consistency/rollback as applicable.
- Broken Windows/Technical Debt/Testing Pyramid: no hardcoded secrets, auth bypasses, silent failures, skipped validation, or untested production code.
- Conway/Bus Factor: ownership, operability, logs/metrics/traces, and rollback matter for production changes.

Prefer plan-validate-execute for risky changes. Use the repo's tests and the bundled LOS gate before final output when code changes or code blocks are produced."""


def main() -> int:
    # Read and ignore the event payload; this hook always injects the durable contract.
    try:
        sys.stdin.read()
    except Exception:
        pass

    print(json.dumps({
        "continue": True,
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": CONTEXT,
        },
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
