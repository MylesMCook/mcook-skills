#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

try:
    from los_code_gate import analyze_repo
except Exception:  # pragma: no cover
    analyze_repo = None


FAILURE_MARKERS = re.compile(
    r"(FAILED|FAILURES?|ERRORS?|Traceback \(most recent call last\)|AssertionError|"
    r"TypeError|ReferenceError|SyntaxError|lint failed|tests? failed|"
    r"Command failed|exit code [1-9]\d*)",
    re.IGNORECASE,
)

VALIDATION_COMMAND = re.compile(
    r"\b(test|pytest|jest|vitest|mocha|go test|cargo test|ruff|eslint|mypy|pyright|tsc|lint|check|clippy|build)\b",
    re.IGNORECASE,
)


def load_event() -> dict:
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def as_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value)
    except Exception:
        return str(value)


def command_from_event(event: dict) -> str:
    tool_input = event.get("tool_input") or {}
    return str(tool_input.get("command") or "") if isinstance(tool_input, dict) else ""


def block(reason: str, additional: str | None = None) -> None:
    payload = {
        "decision": "block",
        "reason": reason,
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": additional or reason,
        },
    }
    print(json.dumps(payload))


def compact_findings(result: dict, limit: int = 5) -> str:
    lines = []
    for f in result.get("findings", [])[:limit]:
        loc = f.get("file", "<unknown>")
        if f.get("line"):
            loc += f":{f['line']}"
        lines.append(f"- {f.get('severity')}: {f.get('category')} at {loc}: {f.get('fix')}")
    if len(result.get("findings", [])) > limit:
        lines.append(f"- ...and {len(result.get('findings', [])) - limit} more.")
    return "\n".join(lines)


def main() -> int:
    event = load_event()
    command = command_from_event(event)
    response = as_text(event.get("tool_response"))

    if VALIDATION_COMMAND.search(command) and FAILURE_MARKERS.search(response):
        block(
            "Validation appears to have failed. Do not finalize until tests/lint/typecheck/build failures are fixed or explicitly scoped with evidence.",
            "Fix the failing validation output before final response; if unrelated, document why and run the smallest relevant passing check.",
        )
        return 0

    # Opportunistic diff scan after shell commands. This cannot undo side effects,
    # but it can keep Codex from treating risky output as success.
    cwd = Path(str(event.get("cwd") or os.getcwd()))
    if analyze_repo is not None:
        try:
            result = analyze_repo(cwd, changed_only=True, include_repo_level=True)
            high = [f for f in result.get("findings", []) if f.get("severity") in {"Blocker", "High"}]
            if high:
                block(
                    "LOS gate found high-risk issues in the current diff:\n" + compact_findings(result),
                    "Revise the code before continuing: remove blockers, add tests/rollback/timeouts/compatibility/observability as applicable.",
                )
                return 0
        except Exception:
            pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
