#!/usr/bin/env python3
"""
Install Laws of Software (LOS) hooks for Codex.

Default: repo-local install into <repo>/.codex so the guardrails travel with the
project. Use --scope global to install into ~/.codex for all Codex sessions.

No third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path


SKILL_NAME = "laws-of-software-los"
HOOK_DIR_NAME = SKILL_NAME


def command_for(scope: str, script_name: str) -> str:
    if scope == "global":
        return f'python3 "$HOME/.codex/hooks/{HOOK_DIR_NAME}/{script_name}"'
    return f'python3 "$(git rev-parse --show-toplevel)/.codex/hooks/{HOOK_DIR_NAME}/{script_name}"'


def hook_config(scope: str) -> dict:
    return {
        "hooks": {
            "SessionStart": [
                {
                    "matcher": "startup|resume",
                    "hooks": [
                        {
                            "type": "command",
                            "command": command_for(scope, "session_start.py"),
                            "statusMessage": "Loading LOS architecture guardrails",
                            "timeout": 10,
                        }
                    ],
                }
            ],
            "UserPromptSubmit": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": command_for(scope, "user_prompt_submit.py"),
                            "statusMessage": "Applying LOS-first context",
                            "timeout": 10,
                        }
                    ],
                }
            ],
            "PreToolUse": [
                {
                    "matcher": "Bash",
                    "hooks": [
                        {
                            "type": "command",
                            "command": command_for(scope, "pre_tool_use_policy.py"),
                            "statusMessage": "Checking command against LOS policy",
                            "timeout": 10,
                        }
                    ],
                }
            ],
            "PermissionRequest": [
                {
                    "matcher": "Bash",
                    "hooks": [
                        {
                            "type": "command",
                            "command": command_for(scope, "permission_request.py"),
                            "statusMessage": "Checking approval request against LOS policy",
                            "timeout": 10,
                        }
                    ],
                }
            ],
            "PostToolUse": [
                {
                    "matcher": "Bash",
                    "hooks": [
                        {
                            "type": "command",
                            "command": command_for(scope, "post_tool_use_review.py"),
                            "statusMessage": "Reviewing command output and current diff",
                            "timeout": 30,
                        }
                    ],
                }
            ],
            "Stop": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": command_for(scope, "stop_los_code_gate.py"),
                            "statusMessage": "Running LOS final gate",
                            "timeout": 30,
                        }
                    ],
                }
            ],
        }
    }


def read_json(path: Path) -> dict:
    if not path.exists():
        return {"hooks": {}}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"error: {path} is not valid JSON: {exc}") from exc


def group_commands(group: dict) -> set[str]:
    commands = set()
    for hook in group.get("hooks", []):
        if isinstance(hook, dict) and hook.get("type") == "command" and hook.get("command"):
            commands.add(str(hook["command"]))
    return commands


def merge_hooks(existing: dict, addition: dict) -> tuple[dict, int]:
    existing.setdefault("hooks", {})
    added = 0
    for event, groups in addition.get("hooks", {}).items():
        current = existing["hooks"].setdefault(event, [])
        existing_commands = set()
        for group in current:
            if isinstance(group, dict):
                existing_commands |= group_commands(group)

        for group in groups:
            commands = group_commands(group)
            if commands and commands <= existing_commands:
                continue
            current.append(group)
            existing_commands |= commands
            added += 1
    return existing, added


def backup(path: Path) -> Path | None:
    if not path.exists():
        return None
    idx = 1
    while True:
        candidate = path.with_suffix(path.suffix + f".bak{idx}")
        if not candidate.exists():
            shutil.copy2(path, candidate)
            return candidate
        idx += 1


def update_config_toml(path: Path) -> bool:
    if path.exists():
        text = path.read_text(encoding="utf-8")
    else:
        text = ""

    if re_has_codex_hooks(text):
        return False

    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.strip() == "[features]":
            lines.insert(idx + 1, "codex_hooks = true")
            path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
            return True

    addition = "\n[features]\ncodex_hooks = true\n"
    path.write_text((text.rstrip() + "\n" + addition if text.strip() else addition.lstrip()), encoding="utf-8")
    return True


def re_has_codex_hooks(text: str) -> bool:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if stripped.startswith("codex_hooks"):
            return True
    return False


def copy_or_link(src: Path, dest: Path, mode: str, dry_run: bool) -> None:
    if dry_run:
        print(f"would install {src} -> {dest} ({mode})")
        return

    if dest.exists() or dest.is_symlink():
        if dest.is_dir() and not dest.is_symlink():
            shutil.rmtree(dest)
        else:
            dest.unlink()

    if mode == "symlink":
        dest.symlink_to(src.resolve(), target_is_directory=src.is_dir())
    else:
        if src.is_dir():
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)


def install_scripts(skill_root: Path, target_hook_dir: Path, mode: str, dry_run: bool) -> None:
    source_hook_dir = skill_root / "scripts" / "codex_hooks"
    if not source_hook_dir.exists():
        raise SystemExit(f"error: missing source hook directory: {source_hook_dir}")

    if dry_run:
        print(f"would create {target_hook_dir}")
    else:
        target_hook_dir.mkdir(parents=True, exist_ok=True)

    for src in sorted(source_hook_dir.glob("*.py")):
        copy_or_link(src, target_hook_dir / src.name, mode, dry_run)

    gate = skill_root / "scripts" / "los_code_gate.py"
    copy_or_link(gate, target_hook_dir / "los_code_gate.py", mode, dry_run)


def target_root(args: argparse.Namespace) -> Path:
    if args.scope == "global":
        return Path.home() / ".codex"
    return Path(args.repo).resolve() / ".codex"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Install Codex LOS hooks for this skill.")
    parser.add_argument("--repo", default=".", help="Repository root for repo-local install. Ignored with --scope global.")
    parser.add_argument("--scope", choices=["repo", "global"], default="repo", help="Install into <repo>/.codex or ~/.codex.")
    parser.add_argument("--mode", choices=["copy", "symlink"], default="copy", help="Copy scripts or symlink them for live development.")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without writing files.")
    parser.add_argument("--print-hooks-json", action="store_true", help="Print the hook config that would be merged.")
    args = parser.parse_args(argv)

    skill_root = Path(__file__).resolve().parents[1]
    addition = hook_config(args.scope)

    if args.print_hooks_json:
        print(json.dumps(addition, indent=2))
        return 0

    codex_root = target_root(args)
    hooks_json = codex_root / "hooks.json"
    config_toml = codex_root / "config.toml"
    hook_dir = codex_root / "hooks" / HOOK_DIR_NAME

    if args.dry_run:
        print(f"target scope: {args.scope}")
        print(f"codex root: {codex_root}")
    else:
        codex_root.mkdir(parents=True, exist_ok=True)

    install_scripts(skill_root, hook_dir, args.mode, args.dry_run)

    existing = read_json(hooks_json)
    merged, added = merge_hooks(existing, addition)
    if args.dry_run:
        print(f"would merge {added} hook group(s) into {hooks_json}")
    else:
        if added:
            backed_up = backup(hooks_json)
            hooks_json.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
            if backed_up:
                print(f"backed up existing hooks to {backed_up}")
            print(f"merged {added} hook group(s) into {hooks_json}")
        else:
            print(f"hooks already present in {hooks_json}")

    if args.dry_run:
        print(f"would ensure codex_hooks feature flag in {config_toml}")
    else:
        changed = update_config_toml(config_toml)
        if changed:
            print(f"enabled codex_hooks feature flag in {config_toml}")
        else:
            print(f"codex_hooks feature flag already present in {config_toml}")

    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
