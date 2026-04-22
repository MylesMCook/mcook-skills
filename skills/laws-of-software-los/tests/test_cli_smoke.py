#!/usr/bin/env python3
"""Smoke tests for LOS helper scripts."""

from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = SKILL_ROOT / "scripts"
SCRIPTS = [
    "adr_lint.py",
    "arch_law_check.py",
    "install_codex_hooks.py",
    "los_code_gate.py",
]


class ScriptHelpSmokeTests(unittest.TestCase):
    def test_help_for_each_script(self) -> None:
        for script_name in SCRIPTS:
            with self.subTest(script=script_name):
                script_path = SCRIPT_DIR / script_name
                proc = subprocess.run(
                    ["python3", str(script_path), "--help"],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                output = f"{proc.stdout}\n{proc.stderr}".lower()
                self.assertEqual(proc.returncode, 0, output)
                self.assertIn("usage", output)


if __name__ == "__main__":
    unittest.main()
