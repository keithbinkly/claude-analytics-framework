<!--
source_of_truth: caf
mirrored_from: dbt-agent/shared/reference/MANDATORY_COMPILE_RULE.md
-->

> CAF migration note: this is the portable CAF version of the compile-first rule. It applies whenever dbt execution work is routed from CAF into `dbt-enterprise`.

# Mandatory Compile Rule

## Rule

Always run `dbt compile` before `dbt run`.

No exceptions for dbt model changes, config changes, or Jinja changes.

## Required Sequence

```bash
dbt compile --select model_name
dbt run --select model_name
```

Never skip straight to `dbt run`.

## Why

Compile is fast and cheap. Failed warehouse runs are slower and costlier.

Compile catches:

- SQL syntax errors
- missing columns
- bad aliases and join references
- `GROUP BY` mistakes
- macro and Jinja errors
- bad `ref()` calls

Compile does not fully catch:

- data-quality problems at runtime
- performance issues
- some incremental edge cases

## Workflow Integration

Before every dbt execution:

1. make the changes
2. compile the exact scope
3. review errors or warnings
4. only then run

## Enforcement Checklist

- modified files identified
- `dbt compile --select <scope>` ran
- compile succeeded
- only then proceed to `dbt run`
