#!/usr/bin/env python3
"""Validate structural health of this Agent Skill package.

Run from the skill root:
    python3 scripts/check_skill.py

The script performs offline checks only: frontmatter, name/description constraints,
referenced files, body length, and eval JSON shape. It performs no network access
and writes no files.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RESERVED = {"anthropic", "claude"}
XML_RE = re.compile(r"<[^>]+>")
REF_RE = re.compile(r"`((?:references|scripts|assets|evals)/[^`]+)`")


def parse_frontmatter(text: str) -> tuple[dict[str, object], str, list[str]]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, text, ["SKILL.md must start with YAML frontmatter"]
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text, ["SKILL.md missing closing frontmatter delimiter"]
    raw = text[4:end].strip("\n")
    body = text[end + len("\n---"):].lstrip("\n")
    meta: dict[str, object] = {}
    current_map: str | None = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith("  ") and current_map:
            key, sep, value = line.strip().partition(":")
            if sep:
                value = value.strip().strip('"').strip("'")
                existing = meta.setdefault(current_map, {})
                if isinstance(existing, dict):
                    existing[key] = value
            continue
        current_map = None
        key, sep, value = line.partition(":")
        if not sep:
            errors.append(f"frontmatter line lacks ':' separator: {line!r}")
            continue
        key = key.strip()
        value = value.strip()
        if value == "":
            meta[key] = {}
            current_map = key
        else:
            meta[key] = value.strip('"').strip("'")
    return meta, body, errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []
    skill_path = root / "SKILL.md"
    if not skill_path.exists():
        print("ERROR: SKILL.md not found", file=sys.stderr)
        return 1

    meta, body, fm_errors = parse_frontmatter(skill_path.read_text(encoding="utf-8"))
    errors.extend(fm_errors)

    name = str(meta.get("name", ""))
    desc = str(meta.get("description", ""))
    if not name:
        errors.append("frontmatter.name is required")
    if name != root.name:
        errors.append(f"name {name!r} must match parent directory {root.name!r}")
    if not NAME_RE.match(name):
        errors.append(f"name {name!r} must be lowercase letters/digits/hyphens, no leading/trailing/consecutive hyphens")
    if len(name) > 64:
        errors.append(f"name is {len(name)} chars; max 64")
    if any(word in name.split("-") for word in RESERVED):
        errors.append("name must not contain reserved words 'anthropic' or 'claude'")
    if XML_RE.search(name):
        errors.append("name must not contain XML tags")

    if not desc:
        errors.append("frontmatter.description is required")
    if len(desc) > 1024:
        errors.append(f"description is {len(desc)} chars; max 1024")
    if XML_RE.search(desc):
        errors.append("description must not contain XML tags")

    body_lines = body.splitlines()
    if len(body_lines) > 500:
        errors.append(f"SKILL.md body is {len(body_lines)} lines; max recommended 500")

    for ref in sorted(set(REF_RE.findall(body))):
        # Placeholders like assets/<article-slug>-illustrations/ describe runtime output paths,
        # not bundled resources that should exist in the package.
        if "<" in ref or ">" in ref:
            continue
        ref_path = root / ref
        if not ref_path.exists():
            errors.append(f"referenced file does not exist: {ref}")

    for rel in ["evals/triggers.json", "evals/evals.json"]:
        p = root / rel
        if not p.exists():
            errors.append(f"missing {rel}")
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{rel} invalid JSON: {exc}")
            continue
        if rel.endswith("triggers.json"):
            cases = data.get("cases", [])
            if data.get("runs_per_case", 0) < 3:
                errors.append("triggers.json runs_per_case should be at least 3")
            if len(cases) < 20:
                errors.append("triggers.json should include about 20 cases")
            should = [c for c in cases if c.get("should_trigger") is True]
            should_not = [c for c in cases if c.get("should_trigger") is False]
            if len(should) < 9 or len(should_not) < 9:
                errors.append("triggers.json should include roughly balanced should/should-not cases")
        else:
            if data.get("skill_name") != name:
                errors.append("evals.json skill_name must match frontmatter.name")
            evals = data.get("evals", [])
            if not (10 <= len(evals) <= 20):
                errors.append("evals.json should include 10-20 cases")
            for ev in evals:
                for required in ["id", "prompt", "expected_output", "expectations"]:
                    if required not in ev:
                        errors.append(f"eval {ev.get('id', '?')} missing {required}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("OK: skill package passed structural checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
