#!/usr/bin/env python3
"""Bootstrap the MCPeas Codex harness into an MCP project.

Usage:
  python bootstrap_harness.py /path/to/project --name my-app
  python bootstrap_harness.py . --name my-app --force
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import shutil
from pathlib import Path

PROJECT_MANIFESTS = [
    "package.json",
    "pyproject.toml",
    "Cargo.toml",
    "deno.json",
    "deno.jsonc",
]


def render(text: str, project_name: str) -> str:
    return (
        text.replace("{{PROJECT_NAME}}", project_name)
        .replace("{{DATE}}", _dt.date.today().isoformat())
    )


def copy_text(src: Path, dst: Path, project_name: str, force: bool, created: list[str], skipped: list[str]) -> None:
    if dst.exists() and not force:
        skipped.append(str(dst))
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(render(src.read_text(), project_name), encoding="utf-8")
    created.append(str(dst))


def copy_binary(src: Path, dst: Path, force: bool, created: list[str], skipped: list[str]) -> None:
    if dst.exists() and not force:
        skipped.append(str(dst))
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    created.append(str(dst))


def detect_project_manifests(root: Path) -> list[str]:
    return [name for name in PROJECT_MANIFESTS if (root / name).exists()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap MCPeas Codex harness files.")
    parser.add_argument("project_dir", type=Path)
    parser.add_argument("--name", required=True, help="Project name for templates.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing harness files.")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    templates = skill_root / "templates"
    target = args.project_dir.resolve()
    target.mkdir(parents=True, exist_ok=True)
    manifests = detect_project_manifests(target)

    created: list[str] = []
    skipped: list[str] = []
    warnings: list[str] = []

    mapping = {
        templates / "AGENTS.md": target / "AGENTS.md",
        templates / "codex-config.toml": target / ".codex" / "config.toml",
        templates / "codex-agents" / "code-mapper.toml": target / ".codex" / "agents" / "code-mapper.toml",
        templates / "codex-agents" / "docs-researcher.toml": target / ".codex" / "agents" / "docs-researcher.toml",
        templates / "codex-agents" / "mcp-reviewer.toml": target / ".codex" / "agents" / "mcp-reviewer.toml",
        templates / "spec.md": target / "docs" / "mcpeas" / "spec.md",
        templates / "runbook.md": target / "docs" / "mcpeas" / "runbook.md",
        templates / "research.md": target / "docs" / "mcpeas" / "research.md",
        templates / "tool-inventory.md": target / "docs" / "mcpeas" / "tool-inventory.md",
        templates / "golden-prompts.json": target / "evals" / "golden-prompts.json",
    }

    for src, dst in mapping.items():
        copy_text(src, dst, args.name, args.force, created, skipped)

    copy_binary(skill_root / "scripts" / "check_project.py", target / "scripts" / "mcpeas_check.py", args.force, created, skipped)

    next_commands = ["python scripts/mcpeas_check.py ."]
    if "package.json" in manifests:
        next_commands.extend(
            [
                "npm run build",
                "npx @modelcontextprotocol/inspector@latest",
            ]
        )
    elif manifests:
        warnings.append(
            "Detected a non-Node project manifest. MCPeas harness files were added, but Node-specific build and Inspector commands are omitted."
        )
    else:
        warnings.append(
            "No project manifest detected. bootstrap_harness.py only adds MCPeas harness files; it does not scaffold the app itself."
        )
        warnings.append(
            "Scaffold the project first or copy these harness files into an existing project before running build or Inspector commands."
        )

    result = {
        "ok": True,
        "project_dir": str(target),
        "detected_project_manifests": manifests,
        "created": created,
        "skipped_existing": skipped,
        "warnings": warnings,
        "next_commands": next_commands,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
