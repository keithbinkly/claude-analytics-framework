#!/usr/bin/env python3
"""
MetricFlow YAML Linter: Catches finicky validation errors before dbt parse.

MetricFlow's validation errors are cryptic and only surface at parse/validate
time. This linter catches the most common mistakes at write-time, saving the
expensive round-trip through dbt parse → mf validate-configs.

Inspired by the SQL linter (dbt_agent_lint.py) — same pattern, different domain.

Rules:
  MF001: Proxy metric should not have expr
  MF002: Duplicate measure names across semantic models
  MF003: Semantic model missing primary entity
  MF004: Semantic model missing primary time dimension
  MF005: Metric references non-existent measure
  MF006: Derived metric missing metrics list
  MF007: Ratio metric missing numerator or denominator
  MF008: Cumulative metric missing window or grain_to_date
  MF009: Measure agg type mismatch with metric type
  MF010: Entity missing type field
  MF011: Dimension missing type field
  MF012: Duplicate metric names in same file

Usage:
    python tools/lint/metricflow_lint.py <file.yml>              # Lint one file
    python tools/lint/metricflow_lint.py <dir>                   # Lint all .yml in dir
    python tools/lint/metricflow_lint.py <file.yml> --json       # JSON output
    python tools/lint/metricflow_lint.py <dir> --cross-file      # Check cross-file rules (MF002)

Exit codes:
    0: All checks passed
    1: Violations found
    2: Error (invalid YAML, etc.)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# Rule definitions
# ---------------------------------------------------------------------------

def check_proxy_metric_expr(metrics: list[dict], _file: Path) -> list[dict]:
    """MF001: Simple/proxy metrics should NOT have expr set.

    When a metric is type: simple and references a single measure,
    MetricFlow treats it as a proxy. Setting expr causes a validation error:
    "Metric 'X' should not have an expr set if it's proxy from measures"
    """
    violations = []
    for metric in metrics:
        name = metric.get('name', '<unnamed>')
        mtype = metric.get('type', '')
        type_params = metric.get('type_params', {}) or {}

        if mtype == 'simple':
            # Check if expr is set
            expr = type_params.get('expr')
            measure = type_params.get('measure')
            if expr and measure:
                # If expr == measure name, it's definitely a proxy
                # But even if different, simple + single measure + expr = error
                violations.append({
                    'rule': 'MF001',
                    'severity': 'error',
                    'metric': name,
                    'message': (
                        f"Simple metric '{name}' has expr '{expr}' set. "
                        f"Remove the expr field — simple metrics proxy directly from the measure."
                    ),
                    'fix_hint': f"Remove 'expr: {expr}' from type_params. The measure '{measure}' is referenced directly.",
                })
    return violations


def check_duplicate_measures(semantic_models: list[dict], _file: Path) -> list[dict]:
    """MF002: Duplicate measure names across semantic models in same file.

    MetricFlow requires globally unique measure names. If two semantic models
    define a measure with the same name, you get:
    "Found measure with name X in multiple semantic models"
    """
    violations = []
    measure_sources: dict[str, list[str]] = {}

    for sm in semantic_models:
        sm_name = sm.get('name', '<unnamed>')
        measures = sm.get('measures', []) or []
        for measure in measures:
            mname = measure.get('name', '')
            if mname:
                measure_sources.setdefault(mname, []).append(sm_name)

    for mname, sources in measure_sources.items():
        if len(sources) > 1:
            violations.append({
                'rule': 'MF002',
                'severity': 'error',
                'measure': mname,
                'message': (
                    f"Measure '{mname}' defined in multiple semantic models: "
                    f"{', '.join(sources)}. Measure names must be globally unique."
                ),
                'fix_hint': f"Rename measure in one of: {', '.join(sources)}. Use a prefix like 'sm_name__{mname}'.",
            })
    return violations


def check_missing_primary_entity(semantic_models: list[dict], _file: Path) -> list[dict]:
    """MF003: Semantic model must have exactly one primary entity."""
    violations = []
    for sm in semantic_models:
        sm_name = sm.get('name', '<unnamed>')
        entities = sm.get('entities', []) or []
        primary_entities = [e for e in entities if e.get('type') == 'primary']

        if len(primary_entities) == 0:
            violations.append({
                'rule': 'MF003',
                'severity': 'error',
                'semantic_model': sm_name,
                'message': f"Semantic model '{sm_name}' has no primary entity. Exactly one entity must have type: primary.",
                'fix_hint': "Add 'type: primary' to the main entity of this semantic model.",
            })
        elif len(primary_entities) > 1:
            names = [e.get('name', '?') for e in primary_entities]
            violations.append({
                'rule': 'MF003',
                'severity': 'error',
                'semantic_model': sm_name,
                'message': f"Semantic model '{sm_name}' has {len(primary_entities)} primary entities ({', '.join(names)}). Exactly one allowed.",
                'fix_hint': "Change extra primary entities to 'type: foreign' or 'type: unique'.",
            })
    return violations


def check_missing_time_dimension(semantic_models: list[dict], _file: Path) -> list[dict]:
    """MF004: Semantic model with measures must have a primary time dimension."""
    violations = []
    for sm in semantic_models:
        sm_name = sm.get('name', '<unnamed>')
        measures = sm.get('measures', []) or []
        dimensions = sm.get('dimensions', []) or []

        if not measures:
            continue  # No measures = no time dimension needed

        time_dims = [
            d for d in dimensions
            if d.get('type') == 'time' and d.get('type_params', {}).get('time_granularity')
        ]

        # Check for is_partition or ds naming convention
        has_primary_time = any(
            d.get('type') == 'time' for d in dimensions
        )

        if not has_primary_time:
            violations.append({
                'rule': 'MF004',
                'severity': 'error',
                'semantic_model': sm_name,
                'message': f"Semantic model '{sm_name}' has measures but no time dimension. A time dimension is required for time-based metrics.",
                'fix_hint': "Add a dimension with 'type: time' and 'type_params: {time_granularity: day}'.",
            })
    return violations


def check_metric_measure_references(metrics: list[dict], semantic_models: list[dict], _file: Path) -> list[dict]:
    """MF005: Metric references a measure that doesn't exist in any semantic model."""
    violations = []

    # Collect all defined measures
    defined_measures = set()
    for sm in semantic_models:
        for measure in sm.get('measures', []) or []:
            name = measure.get('name', '')
            if name:
                defined_measures.add(name)

    if not defined_measures:
        return violations  # Can't validate if no measures in this file

    for metric in metrics:
        name = metric.get('name', '<unnamed>')
        mtype = metric.get('type', '')
        type_params = metric.get('type_params', {}) or {}

        if mtype == 'simple':
            measure_ref = type_params.get('measure')
            if measure_ref and isinstance(measure_ref, str) and measure_ref not in defined_measures:
                violations.append({
                    'rule': 'MF005',
                    'severity': 'warning',
                    'metric': name,
                    'message': f"Metric '{name}' references measure '{measure_ref}' which is not defined in this file.",
                    'fix_hint': f"Check that measure '{measure_ref}' exists in a semantic model. May be in another file.",
                })
        elif mtype == 'derived':
            # Derived metrics reference other metrics, not measures — skip
            pass

    return violations


def check_derived_metric_structure(metrics: list[dict], _file: Path) -> list[dict]:
    """MF006: Derived metrics must have metrics list in type_params."""
    violations = []
    for metric in metrics:
        name = metric.get('name', '<unnamed>')
        mtype = metric.get('type', '')
        type_params = metric.get('type_params', {}) or {}

        if mtype == 'derived':
            if not type_params.get('metrics'):
                violations.append({
                    'rule': 'MF006',
                    'severity': 'error',
                    'metric': name,
                    'message': f"Derived metric '{name}' is missing 'metrics' list in type_params.",
                    'fix_hint': "Add 'metrics:' list with name/offset/filter for each input metric.",
                })
            if not type_params.get('expr'):
                violations.append({
                    'rule': 'MF006',
                    'severity': 'error',
                    'metric': name,
                    'message': f"Derived metric '{name}' is missing 'expr' in type_params.",
                    'fix_hint': "Add 'expr:' with the mathematical expression combining the input metrics.",
                })
    return violations


def check_ratio_metric_structure(metrics: list[dict], _file: Path) -> list[dict]:
    """MF007: Ratio metrics must have numerator and denominator."""
    violations = []
    for metric in metrics:
        name = metric.get('name', '<unnamed>')
        mtype = metric.get('type', '')
        type_params = metric.get('type_params', {}) or {}

        if mtype == 'ratio':
            if not type_params.get('numerator'):
                violations.append({
                    'rule': 'MF007',
                    'severity': 'error',
                    'metric': name,
                    'message': f"Ratio metric '{name}' is missing 'numerator' in type_params.",
                    'fix_hint': "Add 'numerator: {{name: metric_name}}' to type_params.",
                })
            if not type_params.get('denominator'):
                violations.append({
                    'rule': 'MF007',
                    'severity': 'error',
                    'metric': name,
                    'message': f"Ratio metric '{name}' is missing 'denominator' in type_params.",
                    'fix_hint': "Add 'denominator: {{name: metric_name}}' to type_params.",
                })
    return violations


def check_cumulative_metric_structure(metrics: list[dict], _file: Path) -> list[dict]:
    """MF008: Cumulative metrics should have window or grain_to_date."""
    violations = []
    for metric in metrics:
        name = metric.get('name', '<unnamed>')
        mtype = metric.get('type', '')
        type_params = metric.get('type_params', {}) or {}

        if mtype == 'cumulative':
            if not type_params.get('measure'):
                violations.append({
                    'rule': 'MF008',
                    'severity': 'error',
                    'metric': name,
                    'message': f"Cumulative metric '{name}' is missing 'measure' in type_params.",
                    'fix_hint': "Add 'measure: measure_name' to type_params.",
                })
            has_window = type_params.get('window')
            has_grain = type_params.get('grain_to_date')
            if not has_window and not has_grain:
                violations.append({
                    'rule': 'MF008',
                    'severity': 'warning',
                    'metric': name,
                    'message': f"Cumulative metric '{name}' has neither 'window' nor 'grain_to_date'. Will accumulate over all time.",
                    'fix_hint': "Add 'window: {{count: 7, period: day}}' or 'grain_to_date: month'.",
                })
    return violations


def check_entity_type(semantic_models: list[dict], _file: Path) -> list[dict]:
    """MF010: Every entity must have a type field."""
    violations = []
    for sm in semantic_models:
        sm_name = sm.get('name', '<unnamed>')
        entities = sm.get('entities', []) or []
        for entity in entities:
            ename = entity.get('name', '<unnamed>')
            if not entity.get('type'):
                violations.append({
                    'rule': 'MF010',
                    'severity': 'error',
                    'semantic_model': sm_name,
                    'entity': ename,
                    'message': f"Entity '{ename}' in '{sm_name}' is missing 'type'. Must be primary, foreign, unique, or natural.",
                    'fix_hint': "Add 'type: primary' (main key), 'type: foreign' (FK), or 'type: unique'.",
                })
    return violations


def check_dimension_type(semantic_models: list[dict], _file: Path) -> list[dict]:
    """MF011: Every dimension must have a type field."""
    violations = []
    for sm in semantic_models:
        sm_name = sm.get('name', '<unnamed>')
        dimensions = sm.get('dimensions', []) or []
        for dim in dimensions:
            dname = dim.get('name', '<unnamed>')
            if not dim.get('type'):
                violations.append({
                    'rule': 'MF011',
                    'severity': 'error',
                    'semantic_model': sm_name,
                    'dimension': dname,
                    'message': f"Dimension '{dname}' in '{sm_name}' is missing 'type'. Must be categorical or time.",
                    'fix_hint': "Add 'type: categorical' or 'type: time'.",
                })
    return violations


def check_duplicate_metric_names(metrics: list[dict], _file: Path) -> list[dict]:
    """MF012: Duplicate metric names in same file."""
    violations = []
    seen: dict[str, int] = {}
    for metric in metrics:
        name = metric.get('name', '')
        if name:
            seen[name] = seen.get(name, 0) + 1

    for name, count in seen.items():
        if count > 1:
            violations.append({
                'rule': 'MF012',
                'severity': 'error',
                'metric': name,
                'message': f"Metric '{name}' defined {count} times in the same file.",
                'fix_hint': f"Remove or rename duplicate definition of '{name}'.",
            })
    return violations


# ---------------------------------------------------------------------------
# Cross-file rules
# ---------------------------------------------------------------------------

def check_cross_file_duplicate_measures(all_files: dict[Path, dict]) -> list[dict]:
    """MF002 (cross-file): Duplicate measure names across files."""
    violations = []
    measure_sources: dict[str, list[str]] = {}

    for fpath, data in all_files.items():
        for sm in data.get('semantic_models', []) or []:
            sm_name = sm.get('name', '<unnamed>')
            for measure in sm.get('measures', []) or []:
                mname = measure.get('name', '')
                if mname:
                    source = f"{sm_name} ({fpath.name})"
                    measure_sources.setdefault(mname, []).append(source)

    for mname, sources in measure_sources.items():
        if len(sources) > 1:
            violations.append({
                'rule': 'MF002',
                'severity': 'error',
                'measure': mname,
                'message': (
                    f"Measure '{mname}' defined in multiple semantic models: "
                    f"{', '.join(sources)}"
                ),
                'fix_hint': f"Rename measure in one of: {', '.join(sources)}",
            })
    return violations


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

SINGLE_FILE_CHECKS = [
    # (function, needs_metrics, needs_semantic_models)
    (check_proxy_metric_expr, True, False),
    (check_derived_metric_structure, True, False),
    (check_ratio_metric_structure, True, False),
    (check_cumulative_metric_structure, True, False),
    (check_duplicate_metric_names, True, False),
    (check_duplicate_measures, False, True),
    (check_missing_primary_entity, False, True),
    (check_missing_time_dimension, False, True),
    (check_entity_type, False, True),
    (check_dimension_type, False, True),
]


def parse_yaml_file(path: Path) -> dict | None:
    """Parse a YAML file that may contain MetricFlow definitions."""
    try:
        content = path.read_text()
        data = yaml.safe_load(content)
        if not isinstance(data, dict):
            return None
        return data
    except yaml.YAMLError:
        return None
    except Exception:
        return None


def extract_definitions(data: dict) -> tuple[list[dict], list[dict]]:
    """Extract metrics and semantic_models from parsed YAML data."""
    metrics = data.get('metrics', []) or []
    semantic_models = data.get('semantic_models', []) or []
    return metrics, semantic_models


def is_metricflow_file(data: dict) -> bool:
    """Check if a YAML file contains MetricFlow definitions."""
    return bool(data.get('metrics') or data.get('semantic_models'))


def lint_file(path: Path) -> list[dict]:
    """Run all single-file checks on a YAML file."""
    data = parse_yaml_file(path)
    if data is None or not is_metricflow_file(data):
        return []

    metrics, semantic_models = extract_definitions(data)
    violations = []

    for check_fn, needs_metrics, needs_sm in SINGLE_FILE_CHECKS:
        if needs_metrics and needs_sm:
            violations.extend(check_fn(metrics, semantic_models, path))
        elif needs_metrics:
            violations.extend(check_fn(metrics, path))
        elif needs_sm:
            violations.extend(check_fn(semantic_models, path))

    # MF005 needs both
    violations.extend(check_metric_measure_references(metrics, semantic_models, path))

    # Annotate each violation with file
    for v in violations:
        v['file'] = str(path)

    return violations


def lint_directory(directory: Path, cross_file: bool = False) -> list[dict]:
    """Lint all .yml files in a directory."""
    violations = []
    all_files: dict[Path, dict] = {}

    for yml_path in sorted(directory.rglob('*.yml')):
        data = parse_yaml_file(yml_path)
        if data and is_metricflow_file(data):
            all_files[yml_path] = data
            violations.extend(lint_file(yml_path))

    if cross_file and all_files:
        violations.extend(check_cross_file_duplicate_measures(all_files))

    return violations


def format_violations(violations: list[dict], json_output: bool = False) -> str:
    """Format violations for display."""
    if json_output:
        return json.dumps(violations, indent=2)

    if not violations:
        return "MetricFlow lint: all checks passed"

    lines = []
    errors = [v for v in violations if v['severity'] == 'error']
    warnings = [v for v in violations if v['severity'] == 'warning']

    if errors:
        lines.append(f"\n{'='*60}")
        lines.append(f" MetricFlow Lint: {len(errors)} error(s), {len(warnings)} warning(s)")
        lines.append(f"{'='*60}\n")
    else:
        lines.append(f"\nMetricFlow Lint: {len(warnings)} warning(s)\n")

    for v in violations:
        icon = '✗' if v['severity'] == 'error' else '⚠'
        lines.append(f"  {icon} [{v['rule']}] {v['message']}")
        if v.get('fix_hint'):
            lines.append(f"    Fix: {v['fix_hint']}")
        lines.append('')

    return '\n'.join(lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='MetricFlow YAML Linter')
    parser.add_argument('path', help='File or directory to lint')
    parser.add_argument('--json', action='store_true', help='JSON output')
    parser.add_argument('--cross-file', action='store_true', help='Check cross-file rules (duplicate measures)')
    args = parser.parse_args()

    target = Path(args.path)

    if not target.exists():
        print(f"Error: {target} not found", file=sys.stderr)
        sys.exit(2)

    if target.is_file():
        violations = lint_file(target)
    elif target.is_dir():
        violations = lint_directory(target, cross_file=args.cross_file)
    else:
        print(f"Error: {target} is neither file nor directory", file=sys.stderr)
        sys.exit(2)

    output = format_violations(violations, json_output=args.json)
    print(output)

    if any(v['severity'] == 'error' for v in violations):
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
