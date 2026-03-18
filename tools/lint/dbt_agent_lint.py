#!/usr/bin/env python3
"""
dbt-agent linter: Machine-enforceable rules for dbt model development.

Inspired by Factory.ai's "Agents write the code; linters write the law" pattern.
Checks SQL source files at write-time for anti-patterns, structural issues,
naming conventions, and dbt-specific requirements.

Usage:
    python tools/lint/dbt_agent_lint.py <file_path>           # Lint one file
    python tools/lint/dbt_agent_lint.py <file_path> --json    # JSON output
    python tools/lint/dbt_agent_lint.py <dir_path>            # Lint all .sql in dir

Exit codes:
    0: All checks passed
    1: Violations found
    2: Error
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Union


# ---------------------------------------------------------------------------
# Rule definitions
# ---------------------------------------------------------------------------

def check_select_star(sql: str, _path: Path) -> list[dict]:
    """P0: SELECT * is 2.08x slower on columnar Redshift."""
    violations = []
    for i, line in enumerate(sql.splitlines(), 1):
        stripped = line.strip().upper()
        # Skip comments
        if stripped.startswith("--"):
            continue
        # Match SELECT * FROM but NOT SELECT * FROM in Jinja blocks that are
        # likely generating dynamic SQL, and not inside comments
        if re.search(r"\bSELECT\s+\*\s+FROM\b", stripped):
            # Allow in CTEs that immediately feed a final select with explicit cols
            # and in dbt snapshots (which require SELECT *)
            violations.append({
                "rule": "no-select-star",
                "severity": "warning",
                "line": i,
                "message": "SELECT * detected (2.08x slower on Redshift). List explicit columns.",
                "impact": "2.08x",
                "fix_hint": "Replace SELECT * with explicit column names.",
            })
    return violations


def check_not_in_subquery(sql: str, _path: Path) -> list[dict]:
    """P0: NOT IN subquery is 4.18x slower."""
    violations = []
    sql_upper = sql.upper()
    for m in re.finditer(r"\bNOT\s+IN\s*\(\s*SELECT\b", sql_upper, re.DOTALL):
        line_num = sql[:m.start()].count("\n") + 1
        violations.append({
            "rule": "no-not-in-subquery",
            "severity": "error",
            "line": line_num,
            "message": "NOT IN (SELECT ...) detected (4.18x slower). Use NOT EXISTS.",
            "impact": "4.18x",
            "fix_hint": "Rewrite as NOT EXISTS (SELECT 1 FROM ... WHERE ...).",
        })
    return violations


def check_or_in_join(sql: str, _path: Path) -> list[dict]:
    """P0: OR in JOIN is 4.07x slower."""
    violations = []
    sql_upper = sql.upper()
    # Match JOIN ... ON ... OR ... (within the same logical block)
    for m in re.finditer(
        r"\bJOIN\b[^;]*?\bON\b[^;]*?\bOR\b",
        sql_upper,
        re.DOTALL,
    ):
        # Rough line number from the OR position
        or_pos = m.end() - 2  # position of the OR
        line_num = sql[:or_pos].count("\n") + 1
        violations.append({
            "rule": "no-or-in-join",
            "severity": "error",
            "line": line_num,
            "message": "OR in JOIN condition detected (4.07x slower). Split into UNION ALL.",
            "impact": "4.07x",
            "fix_hint": "Split the JOIN into two separate queries with UNION ALL.",
        })
    return violations


def check_deep_nesting(sql: str, _path: Path) -> list[dict]:
    """P0: Deep subquery nesting 3+ levels is 3.06x slower."""
    violations = []
    sql_upper = sql.upper()
    # Find 3+ nested SELECT-in-parentheses (subqueries, not CTEs)
    if re.search(
        r"\(\s*SELECT\b.*\(\s*SELECT\b.*\(\s*SELECT\b",
        sql_upper,
        re.DOTALL,
    ):
        violations.append({
            "rule": "no-deep-nesting",
            "severity": "warning",
            "line": None,
            "message": "3+ levels of subquery nesting detected (3.06x slower). Refactor to CTEs.",
            "impact": "3.06x",
            "fix_hint": "Extract inner subqueries into WITH (CTE) blocks.",
        })
    return violations


def check_env_filter(sql: str, path: Path) -> list[dict]:
    """Require environment filter macro in date-filtered intermediate models."""
    violations = []
    sql_upper = sql.upper()
    path_str = str(path)

    # Only check intermediate and mart models (not staging, tests, macros, etc.)
    if "/models/" not in path_str:
        return violations
    if "/staging/" in path_str or "/sources/" in path_str:
        return violations

    # Check if the model filters on dates
    has_date_filter = bool(re.search(
        r"\b(WHERE|AND)\b[^;]*\b(DATE|CREATED_AT|UPDATED_AT|POSTED_DATE|AUTH_DATE|TRANSACTION_DATE|LOAD_DATE)\b",
        sql_upper,
    ))

    if not has_date_filter:
        return violations

    # Check if environment filter macro is present
    has_env_macro = bool(re.search(
        r"\{\{[\s]*(transactions_full_refresh_filter|batch_full_refresh_filter|"
        r"incremental_filter|env_var\s*\(\s*['\"]DBT_CLOUD_ENVIRONMENT)",
        sql,
        re.IGNORECASE,
    ))

    if not has_env_macro:
        violations.append({
            "rule": "require-env-filter",
            "severity": "warning",
            "line": None,
            "message": "Date-filtered model missing environment filter macro. Dev/CI builds may scan full history.",
            "impact": "perf",
            "fix_hint": "Add {{ transactions_full_refresh_filter }} or {{ batch_full_refresh_filter }}.",
        })

    return violations


def check_hardcoded_dates(sql: str, _path: Path) -> list[dict]:
    """Detect hardcoded date literals in WHERE clauses."""
    violations = []
    for i, line in enumerate(sql.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("--"):
            continue
        # Match date literals like '2024-01-01' in non-comment lines
        for m in re.finditer(r"'(\d{4}-\d{2}-\d{2})'", stripped):
            violations.append({
                "rule": "no-hardcoded-dates",
                "severity": "warning",
                "line": i,
                "message": f"Hardcoded date literal '{m.group(1)}' detected. Use macro or variable.",
                "impact": "maintainability",
                "fix_hint": "Replace with environment-aware macro or dbt variable.",
            })
    return violations


def check_raw_table_refs(sql: str, path: Path) -> list[dict]:
    """Detect raw table references that should use ref() or source()."""
    violations = []
    path_str = str(path)

    # Only check dbt model files
    if "/models/" not in path_str:
        return violations

    # Skip if this is clearly not a dbt model (no config block, no ref/source anywhere)
    has_jinja = "{{" in sql or "{%" in sql
    if not has_jinja:
        return violations  # Probably not a dbt model

    # Look for schema.table patterns that aren't inside Jinja
    # Common raw table patterns: schema.table_name
    for i, line in enumerate(sql.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("--"):
            continue
        # Skip Jinja lines
        if "{{" in stripped or "{%" in stripped:
            continue
        # Detect FROM/JOIN followed by schema.table (not a ref/source)
        for m in re.finditer(
            r"\b(?:FROM|JOIN)\s+(\w+\.\w+)\b",
            stripped,
            re.IGNORECASE,
        ):
            table_ref = m.group(1)
            # Exclude common non-table references
            if table_ref.lower() in ("this.column", "pg_catalog.pg_class"):
                continue
            violations.append({
                "rule": "require-ref-or-source",
                "severity": "error",
                "line": i,
                "message": f"Raw table reference '{table_ref}' detected. Use ref() or source().",
                "impact": "lineage",
                "fix_hint": f"Replace with {{{{ ref('{table_ref.split('.')[-1]}') }}}} or {{{{ source(...) }}}}.",
            })

    return violations


def check_naming_convention(sql: str, path: Path) -> list[dict]:
    """Validate model file naming conventions."""
    violations = []
    path_str = str(path)

    if "/models/" not in path_str:
        return violations

    name = path.stem  # filename without extension

    # Determine expected prefix from folder
    if "/intermediate/" in path_str or "/intermediate_NEW/" in path_str:
        if not name.startswith("int_"):
            violations.append({
                "rule": "naming-convention",
                "severity": "warning",
                "line": None,
                "message": f"Intermediate model '{name}' should start with 'int_' prefix.",
                "impact": "discoverability",
                "fix_hint": f"Rename to int_{name}.sql.",
            })
    elif "/marts/" in path_str or "/marts_NEW/" in path_str:
        if not (name.startswith("mrt_") or name.startswith("mart_")):
            violations.append({
                "rule": "naming-convention",
                "severity": "warning",
                "line": None,
                "message": f"Mart model '{name}' should start with 'mrt_' or 'mart_' prefix.",
                "impact": "discoverability",
                "fix_hint": f"Rename to mrt_{name}.sql.",
            })
    elif "/staging/" in path_str:
        if not name.startswith("stg_"):
            violations.append({
                "rule": "naming-convention",
                "severity": "warning",
                "line": None,
                "message": f"Staging model '{name}' should start with 'stg_' prefix.",
                "impact": "discoverability",
                "fix_hint": f"Rename to stg_{name}.sql.",
            })

    return violations


def check_folder_placement(sql: str, path: Path) -> list[dict]:
    """Validate model is in the correct folder based on content."""
    violations = []
    path_str = str(path)
    sql_upper = sql.upper()

    if "/models/" not in path_str:
        return violations

    # Check: transaction models shouldn't be in foundations/
    if "/foundations/" in path_str:
        transaction_signals = [
            "TRANSACTION", "AUTH_DATE", "POSTED_DATE", "TXN_",
            "INTERCHANGE", "SETTLEMENT",
        ]
        signal_count = sum(1 for s in transaction_signals if s in sql_upper)
        if signal_count >= 2:
            violations.append({
                "rule": "folder-placement",
                "severity": "warning",
                "line": None,
                "message": "Transaction-related model in foundations/ folder. Should be in transactions/.",
                "impact": "architecture",
                "fix_hint": "Move to intermediate_NEW/transactions/ per folder-structure-and-naming.md.",
            })

    # Check: path depth > 5 levels under models/
    models_idx = path_str.find("/models/")
    if models_idx >= 0:
        relative = path_str[models_idx + len("/models/"):]
        depth = relative.count("/")
        if depth > 5:
            violations.append({
                "rule": "max-path-depth",
                "severity": "warning",
                "line": None,
                "message": f"Model path depth is {depth} levels (max recommended: 5).",
                "impact": "navigability",
                "fix_hint": "Flatten folder structure per architecture guidelines.",
            })

    return violations


# ---------------------------------------------------------------------------
# Rule registry
# ---------------------------------------------------------------------------

ALL_RULES = [
    check_select_star,
    check_not_in_subquery,
    check_or_in_join,
    check_deep_nesting,
    check_env_filter,
    check_hardcoded_dates,
    check_raw_table_refs,
    check_naming_convention,
    check_folder_placement,
]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def lint_file(file_path: str | Path) -> dict:
    """
    Lint a single SQL file. Returns structured result.

    Returns:
        {
            "file": str,
            "passed": bool,
            "error_count": int,
            "warning_count": int,
            "violations": [...]
        }
    """
    path = Path(file_path)

    if not path.exists():
        return {"file": str(path), "passed": False, "error": "File not found",
                "error_count": 0, "warning_count": 0, "violations": []}

    if path.suffix != ".sql":
        return {"file": str(path), "passed": True,
                "error_count": 0, "warning_count": 0, "violations": []}

    sql = path.read_text()
    violations = []

    for rule_fn in ALL_RULES:
        try:
            violations.extend(rule_fn(sql, path))
        except Exception as e:
            violations.append({
                "rule": rule_fn.__name__,
                "severity": "internal-error",
                "line": None,
                "message": f"Rule check failed: {e}",
            })

    error_count = sum(1 for v in violations if v.get("severity") == "error")
    warning_count = sum(1 for v in violations if v.get("severity") == "warning")

    return {
        "file": str(path),
        "passed": error_count == 0,
        "error_count": error_count,
        "warning_count": warning_count,
        "violations": violations,
    }


def lint_directory(dir_path: str | Path) -> list[dict]:
    """Lint all .sql files in a directory recursively."""
    results = []
    for sql_file in sorted(Path(dir_path).rglob("*.sql")):
        results.append(lint_file(sql_file))
    return results


def format_human(result: dict) -> str:
    """Format a single file result for human-readable output."""
    if not result["violations"]:
        return f"  {result['file']}: PASS"

    lines = [f"  {result['file']}: {result['error_count']} errors, {result['warning_count']} warnings"]
    for v in result["violations"]:
        loc = f"L{v['line']}" if v.get("line") else "---"
        sev = v["severity"].upper()[:3]
        lines.append(f"    [{sev}] {loc}: {v['message']}")
    return "\n".join(lines)


def format_agent_feedback(result: dict) -> str:
    """Format result as concise agent feedback for hook injection."""
    if result["passed"] and not result["violations"]:
        return ""

    parts = []
    errors = [v for v in result["violations"] if v["severity"] == "error"]
    warnings = [v for v in result["violations"] if v["severity"] == "warning"]

    if errors:
        parts.append(f"LINT ERRORS ({len(errors)}) - must fix:")
        for v in errors:
            loc = f"line {v['line']}" if v.get("line") else "file-level"
            parts.append(f"  - [{v['rule']}] {loc}: {v['message']}")
            if v.get("fix_hint"):
                parts.append(f"    Fix: {v['fix_hint']}")

    if warnings:
        parts.append(f"LINT WARNINGS ({len(warnings)}):")
        for v in warnings:
            loc = f"line {v['line']}" if v.get("line") else "file-level"
            parts.append(f"  - [{v['rule']}] {loc}: {v['message']}")

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: dbt_agent_lint.py <file_or_dir> [--json]", file=sys.stderr)
        sys.exit(2)

    target = Path(sys.argv[1])
    as_json = "--json" in sys.argv

    if target.is_dir():
        results = lint_directory(target)
    elif target.is_file():
        results = [lint_file(target)]
    else:
        print(f"Error: {target} not found", file=sys.stderr)
        sys.exit(2)

    if as_json:
        print(json.dumps(results, indent=2))
    else:
        total_errors = sum(r["error_count"] for r in results)
        total_warnings = sum(r["warning_count"] for r in results)
        files_checked = len(results)
        files_passed = sum(1 for r in results if r["passed"] and not r["violations"])

        for r in results:
            output = format_human(r)
            if output:
                print(output)

        print(f"\n{files_checked} files checked, {files_passed} passed, "
              f"{total_errors} errors, {total_warnings} warnings")

    has_errors = any(r["error_count"] > 0 for r in results)
    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
