#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

try:
    from los_code_gate import analyze_assistant_message, analyze_repo, dedupe_findings, summarize
except Exception:  # pragma: no cover
    analyze_assistant_message = None
    analyze_repo = None
    dedupe_findings = None
    summarize = None


def load_event() -> dict:
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def compact_findings(findings: list[dict], limit: int = 8) -> str:
    lines = []
    for f in findings[:limit]:
        loc = f.get("file", "<unknown>")
        if f.get("line"):
            loc += f":{f['line']}"
        lines.append(f"- {f.get('severity')}: {f.get('category')} at {loc}. Fix: {f.get('fix')}")
    if len(findings) > limit:
        lines.append(f"- ...and {len(findings) - limit} more.")
    return "\n".join(lines)


def main() -> int:
    event = load_event()
    cwd = Path(str(event.get("cwd") or os.getcwd()))
    last_message = str(event.get("last_assistant_message") or "")
    already_continued = bool(event.get("stop_hook_active"))

    findings: list[dict] = []
    files_inspected: list[str] = []

    if analyze_repo is not None:
        try:
            result = analyze_repo(cwd, changed_only=True, include_repo_level=True)
            findings.extend(result.get("findings", []))
            files_inspected = list(result.get("files", []))
        except Exception:
            pass

    if analyze_assistant_message is not None and last_message.strip():
        try:
            msg_findings = analyze_assistant_message(last_message)
            if summarize is not None:
                findings.extend(summarize(msg_findings).get("findings", []))
        except Exception:
            pass

    high = [f for f in findings if f.get("severity") in {"Blocker", "High"}]

    if high and not already_continued:
        reason = (
            "Continue before finalizing: the Laws of Software (LOS) gate found high-risk issues "
            "in the current diff or generated code. Fix them, add/adjust validation, or explicitly narrow the output so it is not presented as production-ready.\n\n"
            + compact_findings(high)
        )
        print(json.dumps({"decision": "block", "reason": reason[:5000]}))
        return 0

    if high and already_continued:
        print(json.dumps({
            "continue": True,
            "systemMessage": (
                "LOS gate still detects high-risk issues after one continuation. "
                "Surface them honestly in the final answer if they remain intentionally unresolved.\n"
                + compact_findings(high, limit=5)
            )[:5000],
        }))
        return 0

    # Soft warning for medium findings. Do not auto-continue on medium issues; use
    # them as final-answer caveats when relevant.
    medium = [f for f in findings if f.get("severity") == "Medium"]
    if medium:
        print(json.dumps({
            "continue": True,
            "systemMessage": (
                "LOS gate found medium-risk issues. Address them when practical or mention validation limits.\n"
                + compact_findings(medium, limit=5)
            )[:5000],
        }))
        return 0

    print(json.dumps({"continue": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
