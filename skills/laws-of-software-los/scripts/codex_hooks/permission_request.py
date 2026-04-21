#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys

# Reuse the same denial logic when available.
try:
    from pre_tool_use_policy import classify
except Exception:  # pragma: no cover
    classify = None


SAFE_READ_OR_VALIDATE = re.compile(
    r"^\s*(git\s+(status|diff|show|log|rev-parse|grep)|"
    r"(python3?|uv|pytest|ruff|mypy|pyright|npm|pnpm|yarn|bun|go|cargo|make|npx)\b[^\n]*(test|lint|check|fmt|format|vet|clippy|typecheck|tsc|eslint|prettier|build)|"
    r"(ls|pwd|cat|sed|awk|grep|rg|find)\b)",
    re.IGNORECASE,
)


def load_event() -> dict:
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def command_from_event(event: dict) -> str:
    tool_input = event.get("tool_input") or {}
    return str(tool_input.get("command") or "") if isinstance(tool_input, dict) else ""


def main() -> int:
    event = load_event()
    command = command_from_event(event)

    risk = classify(command) if classify else None
    if risk is not None:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PermissionRequest",
                "decision": {
                    "behavior": "deny",
                    "message": f"{risk.severity}: {risk.reason} Safer path: {risk.safer}",
                },
            }
        }))
        return 0

    # Let low-risk validation/read-only commands proceed without a friction prompt.
    if SAFE_READ_OR_VALIDATE.search(command):
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PermissionRequest",
                "decision": {"behavior": "allow"},
            }
        }))
        return 0

    # No decision: normal Codex approval flow.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
