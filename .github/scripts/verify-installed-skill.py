#!/usr/bin/env python3
"""Verify an installed SKILL.md after `skills add`.

Usage:
    verify-installed-skill.py <path-to-SKILL.md> <expected-skill-name>

Exits 0 on success, 1 on any error. Errors are emitted as GitHub Actions
annotations.
"""

from __future__ import annotations

import pathlib
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("PyYAML is required\n")
    sys.exit(2)


def main() -> int:
    if len(sys.argv) != 3:
        sys.stderr.write(
            "usage: verify-installed-skill.py <SKILL.md> <expected-name>\n"
        )
        return 2

    path = pathlib.Path(sys.argv[1])
    expected = sys.argv[2]

    if not path.is_file():
        print(f"::error file={path}::file does not exist")
        return 1

    text = path.read_text(encoding="utf-8")
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        print(f"::error file={path}::missing YAML frontmatter fences")
        return 1

    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        print(f"::error file={path}::invalid YAML: {exc}")
        return 1

    if not isinstance(data, dict):
        print(f"::error file={path}::frontmatter is not a mapping")
        return 1

    for key in ("name", "description"):
        value = data.get(key)
        if not isinstance(value, str) or not value.strip():
            print(f"::error file={path}::missing or empty `{key}`")
            return 1

    if data["name"] != expected:
        print(
            f"::error file={path}::frontmatter name {data['name']!r} "
            f"does not match directory {expected!r}"
        )
        return 1

    print(f"ok: {expected}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
