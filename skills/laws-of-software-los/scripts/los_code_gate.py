#!/usr/bin/env python3
"""
LOS Code Gate for the laws-of-software-los skill.

A dependency-free, heuristic quality gate that checks changed code and generated
code snippets for violations of the Laws of Software Engineering as operational
engineering constraints: simplicity, reversibility, compatibility, observability,
testability, data safety, distributed failure handling, and security boundaries.

This is a guardrail, not a proof system. Treat findings as prompts for review.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, Optional


SEVERITY_ORDER = {"Blocker": 0, "High": 1, "Medium": 2, "Low": 3}

SOURCE_EXTENSIONS = {
    ".py", ".pyw", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs",
    ".go", ".java", ".kt", ".kts", ".rb", ".php", ".cs", ".rs",
    ".c", ".cc", ".cpp", ".h", ".hpp", ".swift", ".scala", ".sh",
    ".bash", ".zsh", ".sql", ".tf", ".yaml", ".yml", ".json",
    ".toml", ".dockerfile", ".gradle", ".proto",
}

DOC_EXTENSIONS = {".md", ".mdx", ".rst", ".txt", ".adoc"}

IGNORED_DIR_PARTS = {
    ".git", ".hg", ".svn", "node_modules", "vendor", ".venv", "venv",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "dist", "build", "coverage", ".next", ".turbo", "target",
}

TEST_MARKERS = (
    "/test/", "/tests/", "/__tests__/", ".test.", ".spec.", "_test.",
    "test_", "_spec.", "/spec/",
)


@dataclass
class Finding:
    severity: str
    category: str
    law_lens: str
    file: str
    line: Optional[int]
    evidence: str
    fix: str


def severity_rank(severity: str) -> int:
    return SEVERITY_ORDER.get(severity, 99)


def is_ignored_path(path: Path | str) -> bool:
    parts = Path(path).parts
    return any(part in IGNORED_DIR_PARTS for part in parts)


def is_source_path(path: Path | str) -> bool:
    p = Path(path)
    name = p.name.lower()
    suffix = p.suffix.lower()
    if is_ignored_path(p):
        return False
    return suffix in SOURCE_EXTENSIONS or name in {
        "dockerfile", "makefile", "rakefile", "gemfile", "justfile",
        "go.mod", "go.sum", "package.json", "pnpm-lock.yaml",
        "yarn.lock", "requirements.txt", "pyproject.toml",
    }


def is_doc_path(path: Path | str) -> bool:
    return Path(path).suffix.lower() in DOC_EXTENSIONS


def is_test_path(path: Path | str) -> bool:
    normalized = "/" + str(path).replace("\\", "/").lower()
    return any(marker in normalized for marker in TEST_MARKERS)


def run_git(repo: Path, args: list[str]) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=str(repo),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            check=False,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except Exception as exc:  # pragma: no cover - defensive in hook environments
        return 127, "", str(exc)


def is_git_repo(repo: Path) -> bool:
    code, out, _ = run_git(repo, ["rev-parse", "--is-inside-work-tree"])
    return code == 0 and out.strip() == "true"


def changed_files(repo: Path) -> list[Path]:
    if not is_git_repo(repo):
        return []

    candidates: set[str] = set()

    # Tracked changes against HEAD.
    code, out, _ = run_git(repo, ["diff", "--name-only", "--diff-filter=ACMRTUXB", "HEAD", "--"])
    if code == 0:
        candidates.update(line.strip() for line in out.splitlines() if line.strip())

    # Staged-only changes may not appear in some workflows.
    code, out, _ = run_git(repo, ["diff", "--cached", "--name-only", "--diff-filter=ACMRTUXB", "--"])
    if code == 0:
        candidates.update(line.strip() for line in out.splitlines() if line.strip())

    # Untracked source files.
    code, out, _ = run_git(repo, ["ls-files", "--others", "--exclude-standard"])
    if code == 0:
        candidates.update(line.strip() for line in out.splitlines() if line.strip())

    paths: list[Path] = []
    for rel in sorted(candidates):
        p = (repo / rel).resolve()
        try:
            p.relative_to(repo.resolve())
        except ValueError:
            continue
        if p.exists() and p.is_file() and not is_ignored_path(Path(rel)):
            paths.append(p)
    return paths


def all_reasonable_source_files(repo: Path, limit: int = 200) -> list[Path]:
    paths: list[Path] = []
    for p in repo.rglob("*"):
        if len(paths) >= limit:
            break
        if p.is_file() and is_source_path(p.relative_to(repo)):
            paths.append(p)
    return paths


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def line_number_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def add_regex_findings(
    findings: list[Finding],
    *,
    text: str,
    file: str,
    patterns: Iterable[tuple[str, str, str, str, str]],
) -> None:
    for pattern, severity, category, law, fix in patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL):
            evidence = " ".join(match.group(0).strip().split())
            if len(evidence) > 220:
                evidence = evidence[:217] + "..."
            findings.append(
                Finding(
                    severity=severity,
                    category=category,
                    law_lens=law,
                    file=file,
                    line=line_number_for_offset(text, match.start()),
                    evidence=evidence,
                    fix=fix,
                )
            )


def is_placeholder_secret(value: str) -> bool:
    value_l = value.lower()
    return any(
        token in value_l
        for token in (
            "example", "dummy", "fake", "placeholder", "changeme", "change-me",
            "your_", "your-", "xxx", "xxxx", "test", "sample", "<", ">", "${", "env.",
            "process.env", "os.environ",
        )
    )


def detect_hardcoded_secrets(text: str, file: str) -> list[Finding]:
    findings: list[Finding] = []

    key_value_pattern = re.compile(
        r"""(?P<name>api[_-]?key|secret|password|passwd|pwd|token|client[_-]?secret|private[_-]?key)\s*[:=]\s*(?P<quote>['"])(?P<value>[^'"\n]{8,})(?P=quote)""",
        re.IGNORECASE,
    )
    for match in key_value_pattern.finditer(text):
        value = match.group("value")
        if is_placeholder_secret(value):
            continue
        findings.append(
            Finding(
                "Blocker",
                "Hardcoded secret",
                "Murphy's Law / Broken Windows / Least Astonishment",
                file,
                line_number_for_offset(text, match.start()),
                "Hardcoded credential-like value assigned to " + match.group("name"),
                "Move the value to a secret manager or environment variable, rotate the exposed secret if real, and add a test/config check preventing reintroduction.",
            )
        )

    aws_pattern = re.compile(r"\bAKIA[0-9A-Z]{16}\b")
    for match in aws_pattern.finditer(text):
        findings.append(
            Finding(
                "Blocker",
                "AWS access key-looking token",
                "Murphy's Law / Broken Windows",
                file,
                line_number_for_offset(text, match.start()),
                match.group(0),
                "Remove the key, rotate it if real, and read credentials from managed identity or a secret manager.",
            )
        )

    private_key_pattern = re.compile(r"-----BEGIN (?:RSA |DSA |EC |OPENSSH |)?PRIVATE KEY-----")
    for match in private_key_pattern.finditer(text):
        findings.append(
            Finding(
                "Blocker",
                "Private key material committed",
                "Murphy's Law / Broken Windows",
                file,
                line_number_for_offset(text, match.start()),
                match.group(0),
                "Remove private key material from source, rotate it, and load it securely at runtime.",
            )
        )

    return findings


def python_call_missing_kw(line: str, call_regex: str, kw: str) -> bool:
    if not re.search(call_regex, line):
        return False
    return kw not in line


def analyze_text(text: str, file: str = "<text>", *, source_like: bool = True) -> list[Finding]:
    findings: list[Finding] = []
    lowered = text.lower()

    findings.extend(detect_hardcoded_secrets(text, file))

    common_patterns = [
        (
            r"\b(eval|exec)\s*\(",
            "High",
            "Dynamic code execution",
            "Kernighan's Law / Murphy's Law",
            "Avoid dynamic execution. Replace it with explicit parsing/dispatch, or tightly sandbox and validate inputs with tests.",
        ),
        (
            r"subprocess\.(?:run|popen|call|check_call|check_output)\s*\([^)\n]*shell\s*=\s*True",
            "High",
            "Shell injection risk",
            "Murphy's Law / Least Astonishment",
            "Avoid shell=True; pass an argv list, quote inputs safely, and add tests for malicious arguments.",
        ),
        (
            r"(?:os\.system|popen2?\.|commands\.getoutput)\s*\(",
            "High",
            "Unsafe shell execution",
            "Murphy's Law / Least Astonishment",
            "Use a safer subprocess API with argv arrays and input validation.",
        ),
        (
            r"\bnew\s+Function\s*\(|\beval\s*\(",
            "High",
            "Dynamic JavaScript execution",
            "Kernighan's Law / Murphy's Law",
            "Replace dynamic JavaScript execution with explicit functions or a vetted expression parser.",
        ),
        (
            r"verify\s*=\s*False|rejectUnauthorized\s*:\s*false|NODE_TLS_REJECT_UNAUTHORIZED\s*=\s*['\"]?0",
            "Blocker",
            "TLS verification disabled",
            "Murphy's Law / Broken Windows",
            "Do not disable TLS verification. Fix trust roots/certificates or scope an explicit local-dev-only exception.",
        ),
        (
            r"Access-Control-Allow-Origin['\"]?\s*[:,=]\s*['\"]\*['\"][\s\S]{0,200}(Access-Control-Allow-Credentials|credentials\s*:\s*true)",
            "High",
            "Wildcard CORS with credentials",
            "Least Astonishment / Murphy's Law",
            "Use an explicit origin allowlist when credentials are enabled and add regression tests.",
        ),
        (
            r"(disable|bypass|skip)\s+(auth|authentication|authorization|permission|csrf|security)",
            "High",
            "Security bypass language",
            "Broken Windows / Murphy's Law",
            "Do not ship bypasses. If this is test-only, isolate it behind test fixtures and name the boundary clearly.",
        ),
        (
            r"except\s+(?:Exception|BaseException)?\s*:\s*(?:pass|\n\s*pass\b)",
            "Medium",
            "Silent exception swallow",
            "Broken Windows / Murphy's Law",
            "Handle the expected exception, log context, preserve failure signal, or re-raise.",
        ),
        (
            r"catch\s*\([^)]*\)\s*\{\s*\}",
            "Medium",
            "Silent catch block",
            "Broken Windows / Murphy's Law",
            "Handle or surface the error; add telemetry and tests for the failure path.",
        ),
        (
            r"while\s+true\s*:\s*(?![\s\S]{0,200}(sleep|await|break|timeout|backoff))",
            "Medium",
            "Potential unbounded loop",
            "Murphy's Law / Backpressure",
            "Add a bounded exit condition, timeout, sleep/backoff, and cancellation path.",
        ),
        (
            r"for\s*\(\s*;\s*;\s*\)(?![\s\S]{0,200}(sleep|await|break|timeout|backoff))",
            "Medium",
            "Potential unbounded loop",
            "Murphy's Law / Backpressure",
            "Add a bounded exit condition, timeout, delay/backoff, and cancellation path.",
        ),
    ]
    add_regex_findings(findings, text=text, file=file, patterns=common_patterns)

    # SQL injection heuristics.
    sql_concat_patterns = [
        r"(execute|query)\s*\(\s*f['\"][\s\S]{0,120}\b(select|insert|update|delete|where)\b",
        r"(execute|query)\s*\(\s*['\"][\s\S]{0,120}\b(select|insert|update|delete|where)\b[\s\S]{0,120}\+",
        r"(execute|query)\s*\(\s*`[\s\S]{0,160}\$\{[\s\S]{0,80}\b(select|insert|update|delete|where)\b",
    ]
    for pattern in sql_concat_patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE | re.MULTILINE):
            findings.append(
                Finding(
                    "High",
                    "Possible SQL injection",
                    "Murphy's Law / Hyrum's Law",
                    file,
                    line_number_for_offset(text, match.start()),
                    "Dynamic SQL construction near execute/query",
                    "Use parameterized queries or a query builder, and add tests proving user input is not executable SQL.",
                )
            )

    # Network calls missing explicit timeout.
    for match in re.finditer(r"requests\.(get|post|put|patch|delete)\s*\((?P<args>[^\n)]*)\)", text, re.IGNORECASE):
        if "timeout" not in match.group("args").lower():
            findings.append(
                Finding(
                    "High",
                    "Network call without timeout",
                    "Fallacies of Distributed Computing / Murphy's Law",
                    file,
                    line_number_for_offset(text, match.start()),
                    match.group(0).strip(),
                    "Set an explicit timeout budget and handle timeout errors with bounded retries/backoff where appropriate.",
                )
            )

    for match in re.finditer(r"axios\.(get|post|put|patch|delete)\s*\((?P<args>[^\n)]*)\)", text, re.IGNORECASE):
        if "timeout" not in match.group("args").lower():
            findings.append(
                Finding(
                    "Medium",
                    "HTTP client call lacks timeout policy",
                    "Fallacies of Distributed Computing / Murphy's Law",
                    file,
                    line_number_for_offset(text, match.start()),
                    match.group(0).strip(),
                    "Configure an explicit timeout, retry/backoff policy, and error handling path.",
                )
            )

    # JavaScript fetch cannot take timeout directly, but production fetches should use AbortController/signal.
    if re.search(r"\bfetch\s*\(", text) and not re.search(r"AbortController|signal\s*:", text):
        findings.append(
            Finding(
                "Medium",
                "fetch call lacks cancellation/timeout signal",
                "Fallacies of Distributed Computing / Murphy's Law",
                file,
                None,
                "fetch(...) found without AbortController/signal nearby",
                "Use AbortController or a platform timeout wrapper and test timeout behavior.",
            )
        )

    # TODOs: low by default, high if they indicate security/compat/data gaps.
    for match in re.finditer(r"\b(TODO|FIXME|HACK)\b[^\n]{0,180}", text, flags=re.IGNORECASE):
        evidence = match.group(0).strip()
        sev = "High" if re.search(r"auth|security|permission|encrypt|migration|rollback|data loss|compat|timeout", evidence, re.IGNORECASE) else "Low"
        findings.append(
            Finding(
                sev,
                "Unresolved engineering debt marker",
                "Broken Windows / Technical Debt",
                file,
                line_number_for_offset(text, match.start()),
                evidence,
                "Resolve before shipping, convert to a tracked issue with owner/date, or prove it is non-blocking.",
            )
        )

    # Contextual missing-policy checks. These intentionally fire once per text.
    if re.search(r"\b(kafka|sqs|sns|rabbitmq|pubsub|queue|event bus|consumer|producer|webhook)\b", lowered):
        if not re.search(r"\b(idempotent|idempotency|dedupe|deduplicate|retry|backoff|dead[- ]letter|dlq|timeout|backpressure)\b", lowered):
            findings.append(
                Finding(
                    "High",
                    "Async/distributed flow lacks failure semantics",
                    "Fallacies of Distributed Computing / Murphy's Law / CAP",
                    file,
                    None,
                    "Queue/event/distributed terms found without idempotency/retry/backoff/DLQ/backpressure/timeout terms",
                    "Define idempotency keys, bounded retries with backoff, DLQ/replay, ordering expectations, and observability.",
                )
            )

    if re.search(r"\b(redis|memcached|cache|caching|cached)\b", lowered):
        if not re.search(r"\b(ttl|expire|expiry|invalidate|invalidation|stale|coheren|source of truth)\b", lowered):
            findings.append(
                Finding(
                    "Medium",
                    "Cache lacks invalidation/staleness policy",
                    "Phil Karlton / Hyrum's Law / Least Astonishment",
                    file,
                    None,
                    "Cache terms found without TTL/invalidation/staleness/source-of-truth terms",
                    "State TTL, invalidation triggers, stale-read tolerance, source of truth, and tests around freshness.",
                )
            )

    if re.search(r"\b(route|router|endpoint|controller|api|public function|export function|export const|fastapi|express|flask|django)\b", lowered):
        if re.search(r"\b(remove|rename|breaking|delete endpoint|change response|change status|schema)\b", lowered) and not re.search(r"\b(version|deprecat|compat|migration guide|contract test|backward|backwards)\b", lowered):
            findings.append(
                Finding(
                    "High",
                    "API compatibility/migration policy missing",
                    "Hyrum's Law / Postel's Law / Least Astonishment",
                    file,
                    None,
                    "API change language found without version/deprecation/compatibility/contract-test terms",
                    "Add compatibility rules, versioning/deprecation window, consumer migration notes, and contract tests.",
                )
            )

    if re.search(r"\b(create table|alter table|drop table|drop column|rename column|backfill|migration)\b", lowered):
        if not re.search(r"\b(rollback|revert|down|transaction|backup|restore|reconcile|reconciliation|expand|contract|backfill)\b", lowered):
            findings.append(
                Finding(
                    "High",
                    "Data migration lacks rollback/reconciliation plan",
                    "Murphy's Law / CAP / Lehman's Laws",
                    file,
                    None,
                    "Migration/schema terms found without rollback/reconciliation/transaction/backup terms",
                    "Use expand/contract or reversible migration steps; document rollback, backup/restore, and reconciliation.",
                )
            )

    return dedupe_findings(findings)


def dedupe_findings(findings: list[Finding]) -> list[Finding]:
    seen: set[tuple[str, str, str, Optional[int], str]] = set()
    unique: list[Finding] = []
    for f in findings:
        key = (f.severity, f.category, f.file, f.line, f.evidence[:80])
        if key not in seen:
            seen.add(key)
            unique.append(f)
    return sorted(unique, key=lambda f: (severity_rank(f.severity), f.file, f.line or 0, f.category))


def extract_code_blocks(markdown: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    for match in re.finditer(r"```(?P<lang>[A-Za-z0-9_+.-]*)\n(?P<code>[\s\S]*?)```", markdown):
        lang = match.group("lang") or "text"
        code = match.group("code")
        if len(code.strip()) >= 20:
            blocks.append((lang, code))
    return blocks


def analyze_assistant_message(message: str) -> list[Finding]:
    findings: list[Finding] = []
    for idx, (lang, code) in enumerate(extract_code_blocks(message), start=1):
        if lang.lower() in {"text", "markdown", "md", "diff"} and not re.search(r"\b(function|class|def |import |const |let |var |SELECT|CREATE|ALTER|resource |module )\b", code):
            continue
        findings.extend(analyze_text(code, f"<assistant-code-block-{idx}:{lang}>"))
    return dedupe_findings(findings)


def analyze_paths(paths: list[Path], repo: Path | None = None) -> list[Finding]:
    findings: list[Finding] = []
    for path in paths:
        rel = str(path)
        if repo is not None:
            try:
                rel = str(path.relative_to(repo))
            except ValueError:
                rel = str(path)
        if not is_source_path(rel) and not is_doc_path(rel):
            continue
        text = read_text(path)
        if not text.strip():
            continue
        # Scan source and config files. Docs are scanned for embedded obvious secret/key material only.
        if is_source_path(rel):
            findings.extend(analyze_text(text, rel))
        else:
            findings.extend(detect_hardcoded_secrets(text, rel))
    return dedupe_findings(findings)


def repo_level_findings(repo: Path, paths: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    rel_paths = []
    for p in paths:
        try:
            rel_paths.append(str(p.relative_to(repo)))
        except ValueError:
            rel_paths.append(str(p))

    changed_source = [p for p in rel_paths if is_source_path(p) and not is_test_path(p)]
    changed_tests = [p for p in rel_paths if is_test_path(p)]

    if changed_source and not changed_tests:
        # Do not make every one-line config/doc source edit a blocker; still warn strongly for code.
        code_count = len(changed_source)
        severity = "High" if code_count >= 1 else "Medium"
        findings.append(
            Finding(
                severity,
                "Code changed without tests",
                "Testing Pyramid / Pesticide Paradox / Murphy's Law",
                "<repo-diff>",
                None,
                f"{code_count} non-test source/config file(s) changed and no test/spec file changed",
                "Add or update focused tests, or explicitly document why existing tests cover this change and run them before final output.",
            )
        )

    api_like = [p for p in changed_source if re.search(r"(api|route|router|controller|handler|schema|proto|graphql|openapi|swagger)", p, re.IGNORECASE)]
    if api_like and not changed_tests:
        findings.append(
            Finding(
                "High",
                "API-surface change lacks adjacent tests",
                "Hyrum's Law / Postel's Law / Least Astonishment",
                "<repo-diff>",
                None,
                ", ".join(api_like[:5]),
                "Add contract/API tests and document compatibility/deprecation behavior for changed API surface.",
            )
        )

    migration_like = [p for p in changed_source if re.search(r"(migration|migrations|schema|\.sql$)", p, re.IGNORECASE)]
    for rel in migration_like:
        text = read_text(repo / rel)
        if re.search(r"\b(drop|alter|rename|update|delete|create table|add column)\b", text, re.IGNORECASE):
            if not re.search(r"\b(rollback|revert|down|transaction|backup|restore|reconcile|expand|contract|backfill)\b", text, re.IGNORECASE):
                findings.append(
                    Finding(
                        "High",
                        "Migration file lacks rollback/reconciliation detail",
                        "Murphy's Law / CAP / Lehman's Laws",
                        rel,
                        None,
                        "Schema/data migration changed without rollback/reconciliation/transaction terms",
                        "Add reversible steps or a clear rollback/repair plan with backup, reconciliation, and validation queries.",
                    )
                )

    return dedupe_findings(findings)


def analyze_repo(repo: Path, *, changed_only: bool = True, include_repo_level: bool = True) -> dict:
    repo = repo.resolve()
    paths = changed_files(repo) if changed_only else all_reasonable_source_files(repo)
    findings = analyze_paths(paths, repo=repo)
    if include_repo_level:
        findings.extend(repo_level_findings(repo, paths))
    findings = dedupe_findings(findings)
    return summarize(findings, files=[str(p.relative_to(repo)) if p.is_relative_to(repo) else str(p) for p in paths], repo=str(repo))


def summarize(findings: list[Finding], **extra: object) -> dict:
    counts: dict[str, int] = {}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1
    worst = None
    if findings:
        worst = sorted(findings, key=lambda f: severity_rank(f.severity))[0].severity
    return {
        **extra,
        "summary": {
            "total": len(findings),
            "bySeverity": {sev: counts.get(sev, 0) for sev in ["Blocker", "High", "Medium", "Low"] if counts.get(sev, 0)},
            "worstSeverity": worst,
        },
        "findings": [asdict(f) for f in sorted(findings, key=lambda f: (severity_rank(f.severity), f.file, f.line or 0, f.category))],
    }


def markdown_report(result: dict) -> str:
    lines: list[str] = ["# LOS Code Gate", ""]
    if "repo" in result:
        lines.append(f"Repository: `{result['repo']}`")
    if "files" in result:
        files = result.get("files") or []
        lines.append(f"Files inspected: {len(files)}")
    lines.append("")
    summary = result.get("summary", {})
    total = int(summary.get("total", 0))
    if total == 0:
        lines.append("No heuristic law-gate violations detected.")
        lines.append("")
        lines.append("Still verify behavior with tests, observability, rollout/rollback, and human judgment.")
        return "\n".join(lines)

    by_sev = summary.get("bySeverity", {})
    sev_text = ", ".join(f"{k}: {v}" for k, v in by_sev.items())
    lines.append(f"Findings: {total}" + (f" ({sev_text})" if sev_text else ""))
    lines.append("")
    for idx, f in enumerate(result["findings"], start=1):
        loc = f["file"] + (f":{f['line']}" if f.get("line") else "")
        lines.append(f"## {idx}. {f['severity']}: {f['category']}")
        lines.append("")
        lines.append(f"**Location:** `{loc}`")
        lines.append("")
        lines.append(f"**Law lens:** {f['law_lens']}")
        lines.append("")
        lines.append(f"**Evidence:** {f['evidence']}")
        lines.append("")
        lines.append(f"**Fix:** {f['fix']}")
        lines.append("")
    return "\n".join(lines)


def has_findings_at_or_above(result: dict, threshold: str) -> bool:
    threshold_rank = severity_rank(threshold)
    for f in result.get("findings", []):
        if severity_rank(f.get("severity", "Low")) <= threshold_rank:
            return True
    return False


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Heuristic law gate for code, diffs, and generated code blocks.")
    source = parser.add_mutually_exclusive_group(required=False)
    source.add_argument("--repo", default=None, help="Repository root to inspect. Defaults to current directory for --changed.")
    source.add_argument("--input", "-i", help="File to inspect.")
    parser.add_argument("--stdin", action="store_true", help="Read text from stdin and inspect it as generated code/Markdown.")
    parser.add_argument("--changed", action="store_true", help="Inspect changed files in the repo instead of all source files.")
    parser.add_argument("--all", action="store_true", help="Inspect up to 200 source files in the repo.")
    parser.add_argument("--assistant-message", help="Path to a file containing an assistant message; scans code blocks.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    parser.add_argument("--fail-on", choices=["Blocker", "High", "Medium", "Low"], default=None, help="Exit 1 if any finding at or above this severity is found.")
    args = parser.parse_args(argv)

    result: dict
    if args.stdin:
        text = sys.stdin.read()
        findings = analyze_assistant_message(text)
        if not findings:
            findings = analyze_text(text, "<stdin>")
        result = summarize(findings, input="<stdin>")
    elif args.assistant_message:
        path = Path(args.assistant_message)
        findings = analyze_assistant_message(read_text(path))
        result = summarize(findings, input=str(path))
    elif args.input:
        path = Path(args.input)
        if not path.exists():
            print(f"error: input file not found: {path}", file=sys.stderr)
            return 2
        findings = analyze_text(read_text(path), str(path))
        result = summarize(findings, input=str(path))
    else:
        repo = Path(args.repo or os.getcwd())
        result = analyze_repo(repo, changed_only=not args.all)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(markdown_report(result))

    if args.fail_on and has_findings_at_or_above(result, args.fail_on):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
