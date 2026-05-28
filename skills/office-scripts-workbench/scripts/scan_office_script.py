#!/usr/bin/env python3
"""
Static scanner for Microsoft Excel Office Scripts.

This is a heuristic preflight checker, not a TypeScript compiler. It catches
common Office Scripts issues that agents repeatedly miss.

Usage:
  python3 scripts/scan_office_script.py script.ts
  python3 scripts/scan_office_script.py script.ts --json
  python3 scripts/scan_office_script.py script.ts --fail-on error

Exit codes:
  0 - scan completed; no requested fail threshold reached
  1 - fail threshold reached
  2 - usage/file error
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


Issue = Dict[str, object]


def strip_comments_and_strings(source: str) -> str:
    """Return source with comments and string bodies masked for simpler regex checks."""
    result = []
    i = 0
    n = len(source)
    in_line = False
    in_block = False
    in_string: Optional[str] = None
    escape = False

    while i < n:
        ch = source[i]
        nxt = source[i + 1] if i + 1 < n else ""

        if in_line:
            if ch == "\n":
                in_line = False
                result.append(ch)
            else:
                result.append(" ")
            i += 1
            continue

        if in_block:
            if ch == "*" and nxt == "/":
                result.extend("  ")
                in_block = False
                i += 2
            else:
                result.append("\n" if ch == "\n" else " ")
                i += 1
            continue

        if in_string:
            if escape:
                result.append(" ")
                escape = False
            elif ch == "\\":
                result.append(" ")
                escape = True
            elif ch == in_string:
                result.append(" ")
                in_string = None
            else:
                result.append("\n" if ch == "\n" else " ")
            i += 1
            continue

        if ch == "/" and nxt == "/":
            result.extend("  ")
            in_line = True
            i += 2
            continue
        if ch == "/" and nxt == "*":
            result.extend("  ")
            in_block = True
            i += 2
            continue
        if ch in ("'", '"', "`"):
            result.append(" ")
            in_string = ch
            i += 1
            continue

        result.append(ch)
        i += 1

    return "".join(result)


def line_col(source: str, index: int) -> Tuple[int, int]:
    line = source.count("\n", 0, index) + 1
    last_newline = source.rfind("\n", 0, index)
    col = index + 1 if last_newline < 0 else index - last_newline
    return line, col


def add_issue(
    issues: List[Issue],
    severity: str,
    code: str,
    message: str,
    line: Optional[int] = None,
    col: Optional[int] = None,
    suggestion: Optional[str] = None,
) -> None:
    issue: Issue = {
        "severity": severity,
        "code": code,
        "message": message,
    }
    if line is not None:
        issue["line"] = line
    if col is not None:
        issue["column"] = col
    if suggestion:
        issue["suggestion"] = suggestion
    issues.append(issue)


def find_main_signature(clean: str) -> Optional[re.Match[str]]:
    return re.search(r"\b(?:async\s+)?function\s+main\s*\(([^)]*)\)\s*(?::\s*([^{]+))?", clean)


def scan_source(source: str) -> Dict[str, object]:
    clean = strip_comments_and_strings(source)
    issues: List[Issue] = []

    main = find_main_signature(clean)
    if not main:
        add_issue(
            issues,
            "error",
            "missing-main",
            "No `function main(...)` entry point was found.",
            suggestion="Add `function main(workbook: ExcelScript.Workbook) { ... }`.",
        )
    else:
        params = main.group(1).strip()
        is_async = main.group(0).lstrip().startswith("async")
        first = params.split(",", 1)[0].strip() if params else ""
        if "ExcelScript.Workbook" not in first:
            line, col = line_col(clean, main.start())
            add_issue(
                issues,
                "error",
                "main-workbook-param",
                "The first `main` parameter is not typed as `ExcelScript.Workbook`.",
                line,
                col,
                "Use `function main(workbook: ExcelScript.Workbook, ...)`.",
            )
        if "fetch" in clean and not is_async:
            line, col = line_col(clean, main.start())
            add_issue(
                issues,
                "error",
                "fetch-requires-async-main",
                "`fetch` is used but `main` is not marked `async`.",
                line,
                col,
                "Use `async function main(workbook: ExcelScript.Workbook): Promise<...>` and await fetch/json calls.",
            )

    patterns = [
        (r":\s*any\b", "error", "explicit-any", "Explicit `any` is not allowed in Office Scripts.", "Replace with an interface, union, `object`, or a concrete type."),
        (r"\bas\s+any\b", "error", "cast-any", "`as any` is not allowed in Office Scripts.", "Use a real interface or a narrower cast."),
        (r"\blet\s+[A-Za-z_$][\w$]*\s*;", "error", "implicit-any-let", "Uninitialized `let` declaration may become implicit `any`.", "Initialize the variable or add an explicit type."),
        (r"\beval\s*\(", "error", "eval-unsupported", "`eval` is unsupported.", "Parse data explicitly or use typed JSON/interfaces."),
        (r"\bfunction\s*\*", "error", "generator-unsupported", "Generator functions are unsupported with Office Scripts APIs.", "Use normal loops/functions."),
        (r"\b(?:let|const|var|function|class)\s+(Excel|ExcelScript|console)\b", "error", "reserved-identifier", "Reserved Office Scripts identifier is declared.", "Rename the identifier."),
        (r"\bExcel\.run\s*\(", "error", "office-addin-api", "`Excel.run` is for Office Add-ins, not Office Scripts.", "Use direct `ExcelScript` APIs from the workbook parameter."),
        (r"\bcontext\.sync\s*\(", "error", "office-addin-context-sync", "`context.sync` is for Office Add-ins, not Office Scripts.", "Remove request-context code and use Office Scripts APIs directly."),
        (r"\bOffice\.context\b|\bOfficeRuntime\b", "warning", "office-addin-runtime", "Office Add-ins runtime API detected.", "Confirm this is actually an Office Script, not add-in code."),
        (r"\b(document|window|localStorage|sessionStorage)\b", "warning", "browser-api", "Browser/DOM storage API detected; Office Scripts does not support these as a normal data channel.", "Use workbook data, parameters, return values, or supported external calls."),
        (r"\.sort\s*\(", "warning", "array-sort-risk", "`Array.sort` can be incompatible around Office Scripts API objects.", "Sort plain local data values, not ExcelScript objects."),
    ]

    for regex, severity, code, message, suggestion in patterns:
        for m in re.finditer(regex, clean):
            line, col = line_col(clean, m.start())
            add_issue(issues, severity, code, message, line, col, suggestion)

    # Traditional function expressions used as array callbacks.
    callback_regex = re.compile(r"\.(map|filter|forEach|reduce|some|every|find)\s*\(\s*function\b")
    for m in callback_regex.finditer(clean):
        line, col = line_col(clean, m.start())
        add_issue(
            issues,
            "error",
            "array-callback-not-arrow",
            "Array callback uses `function`; Office Scripts expects arrow callbacks.",
            line,
            col,
            "Use `(item) => { ... }`.",
        )

    # Constructors containing console or ExcelScript-ish calls.
    constructor_regex = re.compile(r"\bconstructor\s*\([^)]*\)\s*\{(?P<body>.*?)\n\s*\}", re.S)
    for m in constructor_regex.finditer(clean):
        body = m.group("body")
        if "console." in body or "workbook." in body or "ExcelScript." in body or re.search(r"\.\s*(get|set|add|delete|clear|copyFrom)\w*\s*\(", body):
            line, col = line_col(clean, m.start())
            add_issue(
                issues,
                "warning",
                "constructor-sync-risk",
                "Constructor appears to call console or workbook APIs; constructors cannot handle Office Scripts synchronization safely.",
                line,
                col,
                "Move workbook/API work to an initialization method called from `main`.",
            )

    # Fetch-specific Power Automate warning.
    if re.search(r"\bfetch\s*\(", clean):
        first_fetch = re.search(r"\bfetch\s*\(", clean)
        line, col = line_col(clean, first_fetch.start()) if first_fetch else (None, None)
        add_issue(
            issues,
            "warning",
            "fetch-power-automate",
            "`fetch` works for Excel-run scripts but fails when run through Power Automate.",
            line,
            col,
            "For Power Automate, call external services in the flow and pass data into the script.",
        )
        if not re.search(r"\bawait\s+fetch\s*\(", clean):
            add_issue(
                issues,
                "warning",
                "fetch-without-await",
                "`fetch` appears without `await`.",
                line,
                col,
                "Await `fetch` and `response.json()` so the script does not finish early.",
            )

    # Hot loop heuristic. Track real brace scopes for for/while blocks so a
    # later batched write after local aggregation is not treated as loop I/O.
    lines = clean.splitlines()
    loop_stack: List[Tuple[int, int]] = []
    workbook_call = re.compile(r"\.(getValues|getValue|getRange|getUsedRange|getWorksheet|getTable|setValues|setValue|addRows)\s*\(")
    loop_start = re.compile(r"\b(for|while)\s*\(")
    brace_depth = 0
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if loop_stack and workbook_call.search(line):
            add_issue(
                issues,
                "warning",
                "workbook-call-in-loop",
                "Workbook/range API call appears inside a loop.",
                i,
                line.find(".") + 1 if "." in line else 1,
                "Read ranges once before the loop, transform locally, then write once or in batches.",
            )
        if loop_stack and "try" in stripped:
            add_issue(
                issues,
                "warning",
                "try-catch-in-loop",
                "`try` appears inside or near a loop.",
                i,
                max(1, line.find("try") + 1),
                "Move try/catch around a batch operation or expected failure boundary.",
            )
        starts_loop = bool(loop_start.search(line))
        opens = line.count("{")
        closes = line.count("}")
        if starts_loop:
            loop_stack.append((i, brace_depth + opens - closes))
        brace_depth += opens - closes
        while loop_stack and brace_depth <= loop_stack[-1][1]:
            loop_stack.pop()

    counts = {"error": 0, "warning": 0, "info": 0}
    for issue in issues:
        counts[str(issue["severity"])] = counts.get(str(issue["severity"]), 0) + 1

    return {"counts": counts, "issues": issues}


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan a TypeScript Office Script for common pitfalls.")
    parser.add_argument("path", help="Path to .ts Office Script file")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument(
        "--fail-on",
        choices=["never", "error", "warning"],
        default="never",
        help="Exit 1 if findings at this severity or higher exist. Default: never.",
    )
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists() or not path.is_file():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2

    try:
        source = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        print(f"error: could not read as UTF-8: {exc}", file=sys.stderr)
        return 2

    result = scan_source(source)
    result["path"] = str(path)

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        counts = result["counts"]
        print(f"{path}: {counts['error']} error(s), {counts['warning']} warning(s)")
        for issue in result["issues"]:
            loc = ""
            if "line" in issue:
                loc = f":{issue['line']}:{issue.get('column', 1)}"
            print(f"{issue['severity'].upper()} {issue['code']}{loc}: {issue['message']}")
            if issue.get("suggestion"):
                print(f"  suggestion: {issue['suggestion']}")

    counts = result["counts"]
    if args.fail_on == "error" and counts["error"] > 0:
        return 1
    if args.fail_on == "warning" and (counts["error"] > 0 or counts["warning"] > 0):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
