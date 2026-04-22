#!/usr/bin/env python3
"""MCPeas project checker.

This is intentionally lightweight. It checks harness completeness and obvious MCP app hygiene
without pretending to replace build/tests/Inspector/ChatGPT validation.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_FILES = [
    "AGENTS.md",
    ".codex/config.toml",
    ".codex/agents/code-mapper.toml",
    ".codex/agents/docs-researcher.toml",
    ".codex/agents/mcp-reviewer.toml",
    "docs/mcpeas/spec.md",
    "evals/golden-prompts.json",
]


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a project against the MCPeas harness baseline.")
    parser.add_argument("project_dir", nargs="?", default=".", type=Path)
    args = parser.parse_args()

    root = args.project_dir.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            errors.append(f"missing required file: {rel}")

    spec = root / "docs" / "mcpeas" / "spec.md"
    if spec.exists():
        text = spec.read_text(encoding="utf-8").lower()
        for phrase in ["architecture decision", "tool inventory", "widget plan", "payload boundary", "golden prompts", "validation gates"]:
            if phrase not in text:
                warnings.append(f"spec may be incomplete: missing '{phrase}' section")

    prompts = root / "evals" / "golden-prompts.json"
    if prompts.exists():
        try:
            data = read_json(prompts)
            for key in ["direct", "indirect", "negative"]:
                items = data.get(key)
                if not isinstance(items, list):
                    errors.append(f"golden-prompts.json missing list: {key}")
                elif len(items) < 5:
                    warnings.append(f"golden-prompts.json has fewer than 5 {key} prompts")
                for idx, item in enumerate(items or [], 1):
                    if not isinstance(item, dict) or not item.get("prompt") or not item.get("expected"):
                        warnings.append(f"golden-prompts.json {key}[{idx}] should include prompt and expected")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"golden-prompts.json is invalid JSON: {exc}")

    package_json = root / "package.json"
    if package_json.exists():
        try:
            package = read_json(package_json)
            scripts = package.get("scripts", {})
            if "dev" not in scripts:
                warnings.append("package.json has no npm run dev script")
            if "build" not in scripts:
                warnings.append("package.json has no npm run build script")
            deps = {**package.get("dependencies", {}), **package.get("devDependencies", {})}
            dep_names = set(deps)
            if not any("mcp" in name.lower() or "mcp-use" in name.lower() for name in dep_names):
                warnings.append("package.json dependencies do not obviously include MCP/mcp-use packages")
        except Exception as exc:  # noqa: BLE001
            warnings.append(f"could not parse package.json: {exc}")
    else:
        warnings.append("no package.json found; this may be fine before scaffold creation")

    config = root / ".codex" / "config.toml"
    if config.exists():
        cfg = config.read_text(encoding="utf-8")
        if "enabled = false" not in cfg:
            warnings.append(".codex/config.toml should keep local MCP server disabled until explicitly trusted")
        if "max_threads" not in cfg or "max_depth" not in cfg:
            warnings.append(".codex/config.toml should bound subagent fan-out with max_threads and max_depth")

    result = {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "checked": REQUIRED_FILES + ["package.json"],
    }
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
