#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys


DANGEROUS_PROMPT = re.compile(
    r"(hardcode\s+(?:the\s+)?(?:secret|token|password|api key)|"
    r"(?:disable|bypass|skip)\s+(?:auth|authorization|authentication|security|tests?|lint|validation)|"
    r"ignore\s+(?:security|failing tests|test failures|lint errors)|"
    r"ship\s+it\s+without\s+(?:tests|validation|review))",
    re.IGNORECASE,
)

CODE_PROMPT = re.compile(
    r"\b(code|implement|edit|fix|bug|refactor|api|endpoint|database|migration|schema|service|queue|cache|"
    r"architecture|design|test|lint|deploy|rollback|performance|latency|security|auth|typescript|python|"
    r"javascript|go|java|rust|sql|terraform|kubernetes|docker)\b",
    re.IGNORECASE,
)

CONTEXT = """For this turn, apply LOS-first generation. If you write or change code, start from the simplest reversible design and make the first patch/output include the required safety properties: tests or an explicit test rationale, no hardcoded secrets, no auth/security bypass, explicit timeout/error handling for remote calls, migration rollback/reconciliation for data changes, API compatibility for public behavior, and observability/ownership for production paths. Run or request validation before finalizing."""

LIGHT_CONTEXT = """Laws of Software mode remains active: prefer simple, reversible, tested, observable, compatible changes; do not hide tradeoffs or validation gaps."""


def load_event() -> dict:
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def main() -> int:
    event = load_event()
    prompt = str(event.get("prompt") or "")

    if DANGEROUS_PROMPT.search(prompt):
        print(json.dumps({
            "decision": "block",
            "reason": (
                "This prompt asks to bypass core LOS safeguards. Restate the request with a safe approach: "
                "preserve authentication/security, keep validation visible, use secrets management, and include tests or an explicit risk-managed exception."
            ),
        }))
        return 0

    additional = CONTEXT if CODE_PROMPT.search(prompt) else LIGHT_CONTEXT
    print(json.dumps({
        "continue": True,
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": additional,
        },
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
