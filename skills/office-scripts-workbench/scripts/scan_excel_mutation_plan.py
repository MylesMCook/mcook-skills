#!/usr/bin/env python3
"""
Scan an agent plan or code file for unsafe Excel workbook mutation patterns.

This is a heuristic guardrail. It is meant to catch plans like:
  download SharePoint workbook -> openpyxl/pandas/xlsxwriter -> save over original

Usage:
  python3 scripts/scan_excel_mutation_plan.py plan.md
  python3 scripts/scan_excel_mutation_plan.py agent_code.py --cloud --json
  python3 scripts/scan_excel_mutation_plan.py plan.md --cloud --fail-on warning

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
    evidence: Optional[str] = None,
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
    if evidence:
        issue["evidence"] = evidence[:160]
    issues.append(issue)


def find_patterns(source: str, patterns: List[Tuple[str, str]]) -> List[Tuple[str, re.Match[str]]]:
    found: List[Tuple[str, re.Match[str]]] = []
    for name, regex in patterns:
        for match in re.finditer(regex, source, flags=re.IGNORECASE | re.MULTILINE):
            found.append((name, match))
    return found


def sentence_for_index(source: str, index: int) -> str:
    start_candidates = [source.rfind(mark, 0, index) for mark in (".", "\n")]
    start = max(start_candidates) + 1
    end_candidates = [pos for pos in (source.find(mark, index) for mark in (".", "\n")) if pos >= 0]
    end = min(end_candidates) if end_candidates else len(source)
    return source[start:end].strip()


def window_for_index(source: str, index: int, radius: int = 140) -> str:
    return source[max(0, index - radius) : min(len(source), index + radius)]


def is_negated_overwrite_context(source: str, index: int) -> bool:
    sentence = sentence_for_index(source, index).lower()
    safe_negations = [
        r"\bdo\s+not\s+(?:read\s+or\s+)?overwrite\b",
        r"\bdo\s+not\s+save\s+over\b",
        r"\bdo\s+not\s+replace\s+the\s+original\b",
        r"\bdo\s+not\s+upload\s+back\b",
        r"\bnever\s+(?:read\s+or\s+)?overwrite\b",
        r"\bnever\s+save\s+over\b",
        r"\bavoid\s+(?:in[- ]place\s+)?(?:overwrite|replacement|upload\s+back)\b",
        r"\bwithout\s+overwriting\b",
        r"\bno\s+(?:source\s+)?overwrite\b",
        r"\bsource\s+workbook\s+(?:is|stays|remains)\s+preserved\b",
    ]
    return any(re.search(pattern, sentence) for pattern in safe_negations)


def is_affirmative_xlsxwriter_existing_use(source: str) -> bool:
    for match in re.finditer(r"\bxlsxwriter\b|engine\s*=\s*['\"]xlsxwriter['\"]", source, flags=re.I):
        window = window_for_index(source, match.start()).lower()
        if re.search(r"\b(new|brand[- ]new|create|generated?|artifact|output\s+path)\b", window):
            continue
        if re.search(r"\b(do\s+not|never|avoid)\b.{0,60}\b(existing|modify|read|overwrite)\b", window):
            continue
        if re.search(r"\b(existing|modify|mutate|update|edit|template|read|load|overwrite|save\s+over)\b", window):
            return True
    return False


CLOUD_PATTERNS = [
    ("onedrive", r"\bOneDrive\b|OneDrive\s*-|\\OneDrive\\|/OneDrive/"),
    ("sharepoint", r"\bSharePoint\b|sharepoint\.com|/sites/|/teams/"),
    ("teams", r"\bTeams\b"),
    ("office365-group", r"Office\s*365\s*Group|Microsoft\s*365\s*Group|group\s+drive"),
    ("document-library", r"document\s+library|Excel\s+Online|Excel\s+Business\s+\(Online\)"),
    ("sync-folder", r"\bsync(?:ed|ing)?\s+(?:folder|path|client)|cloud[- ]backed|coauthor"),
]

DANGEROUS_LIBRARY_PATTERNS = [
    ("openpyxl", r"\bopenpyxl\b|\bload_workbook\s*\("),
    ("pandas-excel", r"\bpandas\b|\bpd\.read_excel\b|\bpd\.ExcelWriter\b|\.to_excel\s*\("),
    ("xlsxwriter", r"\bxlsxwriter\b|engine\s*=\s*['\"]xlsxwriter['\"]"),
    ("sheetjs", r"\bSheetJS\b|\bXLSX\.(?:read|write|writeFile)\b"),
    ("libreoffice", r"\bLibreOffice\b|\bsoffice\b|--headless"),
    ("raw-xlsx-zip-xml", r"\bzipfile\b|\.xlsx\s+zip|xl/workbook\.xml|xl/worksheets|\[Content_Types\]\.xml|workbook\.xml\.rels"),
    ("desktop-com", r"\bwin32com\.client\b|\bxlwings\b|\bCOM automation\b"),
]

OVERWRITE_PATTERNS = [
    ("overwrite", r"\boverwrite\b|save\s+over|replace\s+the\s+original|upload\s+back|write\s+back\s+to\s+the\s+same\s+file"),
    ("same-path-save", r"\.save\s*\(\s*(?:path|file|filename|workbook_path|input_path)\s*\)|to_excel\s*\(\s*(?:path|file|filename|workbook_path|input_path)"),
    ("in-place", r"\bin[- ]place\b|mutate\s+the\s+source|live\s+workbook|production\s+workbook"),
]

CONCURRENCY_PATTERNS = [
    ("parallel", r"\bparallel\b|concurrent|simultaneous|multi(?:ple)?\s+writers"),
    ("open-workbook", r"\bopen\s+in\s+Excel\b|while\s+users?\s+(?:has|have)\s+it\s+open|coauthoring"),
    ("flow-race", r"multiple\s+flows|two\s+flows|logic\s+apps?|power\s+apps?"),
]

SAFE_API_PATTERNS = [
    ("office-scripts", r"\bOffice\s+Scripts?\b|\bExcelScript\b|Run\s+script|Automate\s+tab"),
    ("excel-object-model", r"workbook\.get(?:Table|Worksheet|Worksheets)|getRange(?:ByIndexes)?|setValues|addRows"),
    ("graph-excel", r"Microsoft\s+Graph\s+Excel|Graph\s+Excel\s+API|/workbook/|workbook-session-id|createSession"),
]


def scan_source(source: str, force_cloud: bool) -> Dict[str, object]:
    issues: List[Issue] = []

    cloud_hits = find_patterns(source, CLOUD_PATTERNS)
    library_hits = find_patterns(source, DANGEROUS_LIBRARY_PATTERNS)
    overwrite_hits = find_patterns(source, OVERWRITE_PATTERNS)
    concurrency_hits = find_patterns(source, CONCURRENCY_PATTERNS)
    safe_hits = find_patterns(source, SAFE_API_PATTERNS)

    cloud_context = force_cloud or bool(cloud_hits)

    if force_cloud and not cloud_hits:
        add_issue(
            issues,
            "info",
            "cloud-context-forced",
            "`--cloud` was supplied, so this scan treats the workbook as OneDrive/SharePoint/Teams-hosted.",
            suggestion="Prefer Office Scripts or Graph Excel APIs over direct .xlsx package mutation.",
        )

    for name, match in cloud_hits:
        line, col = line_col(source, match.start())
        add_issue(
            issues,
            "info",
            "cloud-workbook-context",
            f"Cloud workbook context detected: {name}.",
            line,
            col,
            "Treat existing workbook mutation as a cloud-safety-sensitive operation.",
            match.group(0),
        )

    for name, match in library_hits:
        line, col = line_col(source, match.start())
        if cloud_context:
            add_issue(
                issues,
                "error",
                "unsafe-cloud-xlsx-library",
                f"File-level Excel library/tool detected in cloud workbook context: {name}.",
                line,
                col,
                "Do not mutate an existing OneDrive/SharePoint workbook with file-level libraries. Use Office Scripts first; use Graph Excel APIs with a workbook session for service/API workflows.",
                match.group(0),
            )
        else:
            add_issue(
                issues,
                "warning",
                "xlsx-library-needs-scope-check",
                f"File-level Excel library/tool detected: {name}.",
                line,
                col,
                "This can be acceptable for new files, offline copies, or read-only inspection. Do not use it to overwrite an existing cloud production workbook.",
                match.group(0),
            )

    filtered_overwrite_hits = [
        (name, match) for name, match in overwrite_hits if not is_negated_overwrite_context(source, match.start())
    ]

    for name, match in filtered_overwrite_hits:
        line, col = line_col(source, match.start())
        severity = "error" if cloud_context else "warning"
        add_issue(
            issues,
            severity,
            "in-place-overwrite-risk",
            f"In-place overwrite/source replacement language detected: {name}.",
            line,
            col,
            "Preserve the original workbook. Prefer targeted table/range updates through Office Scripts or a new output file path for offline copies.",
            match.group(0),
        )

    for name, match in concurrency_hits:
        line, col = line_col(source, match.start())
        severity = "warning" if cloud_context else "info"
        add_issue(
            issues,
            severity,
            "concurrent-writer-risk",
            f"Concurrent writer / open workbook risk detected: {name}.",
            line,
            col,
            "Serialize writes to the workbook. Avoid simultaneous edits from Excel, Power Automate, Graph clients, and agent jobs.",
            match.group(0),
        )

    if safe_hits:
        for name, match in safe_hits[:5]:
            line, col = line_col(source, match.start())
            add_issue(
                issues,
                "info",
                "safe-api-marker",
                f"Safer Excel object-model/API marker detected: {name}.",
                line,
                col,
                "Continue with targeted workbook object updates and avoid whole-file replacement.",
                match.group(0),
            )

    # Special-case: xlsxwriter + existing workbook wording is wrong even outside cloud.
    if is_affirmative_xlsxwriter_existing_use(source):
        match = re.search(r"\bxlsxwriter\b", source, re.I)
        line, col = line_col(source, match.start()) if match else (None, None)
        add_issue(
            issues,
            "error",
            "xlsxwriter-existing-file-mismatch",
            "`xlsxwriter` is a writer for new files and is not an existing-workbook mutation tool.",
            line,
            col,
            "Use Office Scripts/Graph for existing cloud workbooks, or choose a new output file path for generated workbooks.",
        )

    if cloud_context and not library_hits and not safe_hits:
        add_issue(
            issues,
            "warning",
            "cloud-workbook-no-safe-mutation-layer",
            "Cloud workbook context detected, but no Office Scripts, ExcelScript, Power Automate Run script, or Graph Excel API path was found.",
            suggestion="Specify the safe mutation layer before implementing: Office Scripts first, Graph Excel API for explicit service/API workflows.",
        )

    counts = {"error": 0, "warning": 0, "info": 0}
    for issue in issues:
        counts[str(issue["severity"])] = counts.get(str(issue["severity"]), 0) + 1

    return {
        "cloud_context": cloud_context,
        "counts": counts,
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan plans/code for unsafe Excel workbook mutation patterns.")
    parser.add_argument("path", help="Path to a plan/code/text file to scan")
    parser.add_argument("--cloud", action="store_true", help="Treat target workbook as OneDrive/SharePoint/Teams-hosted")
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

    result = scan_source(source, args.cloud)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        counts = result["counts"]
        print(
            f"cloud_context={result['cloud_context']} "
            f"errors={counts['error']} warnings={counts['warning']} info={counts['info']}"
        )
        for issue in result["issues"]:
            loc = ""
            if "line" in issue:
                loc = f"{issue['line']}:{issue.get('column', 1)} "
            print(f"[{issue['severity']}] {loc}{issue['code']}: {issue['message']}")
            if issue.get("suggestion"):
                print(f"  suggestion: {issue['suggestion']}")

    fail = False
    if args.fail_on == "error" and result["counts"]["error"] > 0:
        fail = True
    elif args.fail_on == "warning" and (result["counts"]["error"] > 0 or result["counts"]["warning"] > 0):
        fail = True

    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
