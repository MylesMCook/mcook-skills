#!/usr/bin/env python3
"""Lint SKILL.md frontmatter across the mcook-skills catalog.

Enforces the rule in AGENTS.md: every skill must have a valid SKILL.md whose
YAML frontmatter contains `name` and `description`. Extra keys are allowed for
a known allowlist (compatibility, metadata, allowed-tools) and produce a
warning otherwise.

Exit codes:
    0 = no errors (warnings allowed)
    1 = at least one error
"""

from __future__ import annotations

import os
import pathlib
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "PyYAML is required. Install with `pip install pyyaml` or use the "
        "python3 image with PyYAML preinstalled.\n"
    )
    sys.exit(2)


REQUIRED_KEYS = {"name", "description"}
ALLOWED_EXTRA_KEYS = {"compatibility", "metadata", "allowed-tools"}
SKILLS_DIR = pathlib.Path("skills")


def parse_frontmatter(text: str) -> tuple[dict | None, str | None]:
    """Return (data, error). data is None on failure."""
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return None, "missing opening `---` fence on line 1"
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return None, "missing closing `---` fence"
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        return None, f"invalid YAML: {exc}"
    if not isinstance(data, dict):
        return None, "frontmatter is not a mapping"
    return data, None


def lint_skill(skill_md: pathlib.Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    text = skill_md.read_text(encoding="utf-8")
    data, err = parse_frontmatter(text)
    if err is not None:
        errors.append(err)
        return errors, warnings

    for key in REQUIRED_KEYS:
        value = data.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"missing or empty `{key}`")

    skill_name = skill_md.parent.name
    fm_name = data.get("name") if isinstance(data.get("name"), str) else None
    if fm_name and fm_name != skill_name:
        errors.append(
            f"frontmatter `name: {fm_name}` does not match directory "
            f"`{skill_name}`"
        )

    extras = set(data.keys()) - REQUIRED_KEYS - ALLOWED_EXTRA_KEYS
    if extras:
        warnings.append(
            "unexpected frontmatter keys: " + ", ".join(sorted(extras))
        )

    return errors, warnings


def main() -> int:
    if not SKILLS_DIR.is_dir():
        sys.stderr.write(f"no `{SKILLS_DIR}/` directory found\n")
        return 2

    skill_mds = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_mds:
        sys.stderr.write(f"no `{SKILLS_DIR}/*/SKILL.md` files found\n")
        return 2

    total_errors = 0
    total_warnings = 0
    rows: list[tuple[str, str, int, int]] = []

    for skill_md in skill_mds:
        errors, warnings = lint_skill(skill_md)
        total_errors += len(errors)
        total_warnings += len(warnings)
        status = "ok" if not errors else "error"
        rows.append((skill_md.parent.name, status, len(errors), len(warnings)))

        rel = skill_md.as_posix()
        for msg in errors:
            print(f"::error file={rel}::{msg}")
        for msg in warnings:
            print(f"::warning file={rel}::{msg}")

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as fh:
            fh.write("## Frontmatter lint\n\n")
            fh.write(
                f"Scanned **{len(skill_mds)}** skills \u2014 "
                f"**{total_errors}** error(s), "
                f"**{total_warnings}** warning(s).\n\n"
            )
            fh.write("| Skill | Status | Errors | Warnings |\n")
            fh.write("| --- | --- | ---: | ---: |\n")
            for name, status, errs, warns in rows:
                icon = "\u2705" if status == "ok" else "\u274c"
                fh.write(f"| `{name}` | {icon} {status} | {errs} | {warns} |\n")

    print(
        f"\nLinted {len(skill_mds)} skills: "
        f"{total_errors} error(s), {total_warnings} warning(s)."
    )
    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main())
