#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass


@dataclass
class CommandRisk:
    severity: str
    reason: str
    safer: str


DENY_PATTERNS: list[tuple[re.Pattern[str], CommandRisk]] = [
    (re.compile(r"\brm\s+(-[^\n]*r[^\n]*f|-[^\n]*f[^\n]*r)[^\n]*(\s/|\s~|\s\$HOME|\s\.\s*$|\s\./?\s*$|\s\*)", re.I), CommandRisk("Blocker", "Broad recursive deletion can destroy the workspace or user data.", "Delete the narrow generated path only, list it first, and avoid wildcards/root/home.")),
    (re.compile(r"\bgit\s+reset\s+--hard\b|\bgit\s+clean\s+-[^\n]*[fdx][^\n]*[fdx]|\bgit\s+checkout\s+--\s+\.", re.I), CommandRisk("High", "This can discard user/agent work irreversibly.", "Show git status/diff first; revert only named files after confirmation.")),
    (re.compile(r"\bgit\s+push\s+(-[^\n]*f|--force|--mirror)\b", re.I), CommandRisk("High", "Force-pushing can rewrite shared history.", "Use a normal push or explain the protected branch/recovery plan and ask for approval outside the hook.")),
    (re.compile(r"\bchmod\s+-R\s+777\b|\bchown\s+-R\b", re.I), CommandRisk("High", "Recursive permission/ownership changes are broad and hard to reverse.", "Apply least-privilege permissions to the specific path that needs them.")),
    (re.compile(r"\b(curl|wget)\b[^\n|;]*(\|\s*(sh|bash|zsh|python|python3|node))", re.I), CommandRisk("High", "Piping remote code directly into an interpreter is not reproducible or reviewable.", "Download to a file, pin/checksum it, inspect it, then run if appropriate.")),
    (re.compile(r"\bterraform\s+(destroy|apply\s+-destroy)\b", re.I), CommandRisk("Blocker", "Infrastructure destruction requires explicit human-controlled rollout and rollback.", "Create a plan file and review it manually before any destructive apply.")),
    (re.compile(r"\bkubectl\s+delete\b[^\n]*(namespace|deployment|statefulset|pod|service|ingress|crd|pvc|pv|all)\b", re.I), CommandRisk("High", "Kubernetes deletion can cause production outage or data loss.", "Show context/namespace, use dry-run where available, and require explicit approval.")),
    (re.compile(r"\b(drop\s+database|drop\s+schema|drop\s+table|truncate\s+table)\b", re.I), CommandRisk("Blocker", "Destructive database operation needs backup, rollback, and explicit scope.", "Use a reversible migration with backup/restore and validation queries.")),
    (re.compile(r"\bdelete\s+from\s+\w+(?![\s\S]{0,120}\bwhere\b)", re.I), CommandRisk("Blocker", "DELETE without WHERE can erase entire tables.", "Add a WHERE clause, run a SELECT preview, and wrap in a transaction with rollback plan.")),
    (re.compile(r"\bsudo\b", re.I), CommandRisk("High", "Privilege escalation should not be automatic in an agent loop.", "Use project-local tools or ask the user for a narrow manual command.")),
    (re.compile(r"\bNODE_TLS_REJECT_UNAUTHORIZED\s*=\s*0\b|\b--insecure\b|\b-k\b", re.I), CommandRisk("High", "Disabling TLS verification normalizes insecure behavior.", "Fix certificates or scope a local-only exception with explicit risk notes.")),
]


def load_event() -> dict:
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def command_from_event(event: dict) -> str:
    tool_input = event.get("tool_input") or {}
    if isinstance(tool_input, dict):
        return str(tool_input.get("command") or "")
    return ""


def classify(command: str) -> CommandRisk | None:
    for pattern, risk in DENY_PATTERNS:
        if pattern.search(command):
            return risk
    return None


def main() -> int:
    event = load_event()
    command = command_from_event(event)
    risk = classify(command)
    if risk is None:
        return 0

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"{risk.severity}: {risk.reason} Safer path: {risk.safer}",
        }
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
