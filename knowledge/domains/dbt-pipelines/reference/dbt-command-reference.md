# dbt Command Reference for Copilot Execution

Quick reference for dbt commands used during handoff package execution.

**Source**: [dbt Docs - Commands](https://docs.getdbt.com/category/list-of-commands) | **Last Updated**: 2025-10-17

---

## 🎯 Common Workflow Commands

### `dbt compile`
**Purpose**: Validate SQL compiles without running against warehouse

**Usage**:
```bash
dbt compile --select <model_name>
```

**Common Flags**:
- `--select <selector>` - Compile specific models
- `--vars '{key: value}'` - Pass variables

**When to Use**:
- Step 1 of handoff execution (validate syntax)
- Before running expensive models
- Debugging Jinja/macro logic

**Example**:
```bash
# Compile single model and dependencies
dbt compile --select +int_interchange__revenue_calc

# Compile with custom variables
dbt compile --select my_model --vars '{"env": "dev"}'
```

---

### `dbt run`
**Purpose**: Execute compiled SQL models against target database

**Usage**:
```bash
dbt run --select <selector> [flags]
```

**Common Flags**:
| Flag | Description | Example |
|------|-------------|---------|
| `--select <selector>` | Run specific models | `--select int_interchange+` |
| `--exclude <selector>` | Exclude models | `--exclude tag:deprecated` |
| `--full-refresh` | Treat incremental as table | `--full-refresh` |
| `--vars '{}'` | Pass runtime variables | `--vars '{"start_date": "2024-01-01"}'` |
| `--threads <n>` | Parallel execution | `--threads 4` |
| `--defer` | Use prod artifacts for unbuilt upstreams | `--defer` |
| `--state <path>` | Compare against previous state | `--state ./target/` |

**When to Use**:
- Step 3 of handoff execution (run models full-refresh)
- Step 5 of handoff execution (test incremental)

**Examples**:
```bash
# Full refresh for initial load
dbt run --select int_interchange__revenue_calc+ --full-refresh

# Incremental run (test incremental behavior)
dbt run --select int_interchange__revenue_calc

# Run modified models only
dbt run --select state:modified+ --defer --state ./prod-target/
```

---

### `dbt test`
**Purpose**: Run data quality tests on models, sources, snapshots

**Usage**:
```bash
dbt test --select <selector>
```

**Common Flags**:
- `--select <selector>` - Test specific models
- `--exclude <selector>` - Exclude tests
- `--store-failures` - Store failing rows for inspection

**When to Use**:
- After running models (data quality validation)
- Part of `dbt build` workflow

**Examples**:
```bash
# Test single model
dbt test --select int_interchange__revenue_calc

# Test all marts
dbt test --select marts.*

# Store failures for investigation
dbt test --select my_model --store-failures
```

---

### `dbt build`
**Purpose**: Run models AND tests in DAG order (comprehensive execution)

**Usage**:
```bash
dbt build --select <selector>
```

**What it does**:
1. Runs models (like `dbt run`)
2. Tests models (like `dbt test`)
3. Snapshots (if applicable)
4. Seeds (if applicable)
**All in correct dependency order**

**Common Flags**: Same as `dbt run` + `dbt test`

**When to Use**:
- Production deployments
- When you want comprehensive validation
- Alternative to separate run + test

**Example**:
```bash
# Build entire pipeline with tests
dbt build --select int_interchange__revenue_calc+

# Build only changed models
dbt build --select state:modified+
```

---

### `dbt show`
**Purpose**: Preview query results (like `SELECT * LIMIT N`)

**Usage**:
```bash
dbt show --select <model_name> [--limit N]
dbt show --inline "<sql_query>" [--limit N]
```

**Common Flags**:
- `--limit <n>` - Number of rows to return (default: 5)
- `--inline "<sql>"` - Execute arbitrary SQL

**When to Use**:
- Step 4 of handoff execution (QA validation preview)
- Debugging data issues
- Quick spot checks

**Examples**:
```bash
# Preview model output
dbt show --select int_interchange__revenue_calc --limit 10

# Execute inline QA query
dbt show --inline "
  SELECT product, SUM(revenue)
  FROM {{ ref('int_interchange__revenue_calc') }}
  WHERE calendar_month = '2024-09-01'
  GROUP BY 1
" --limit 100
```

---

### `dbt ls` (list)
**Purpose**: Preview which models will be selected (dry run)

**Usage**:
```bash
dbt ls --select <selector>
```

**When to Use**:
- Step 2 of handoff execution (check dependencies)
- Before running expensive selectors
- Debugging selection syntax

**Examples**:
```bash
# List all dependencies
dbt ls --select +int_interchange__revenue_calc

# Check what would run with state:modified
dbt ls --select state:modified+

# List by resource type
dbt ls --resource-type model --select marts.*
```

---

## 🔧 Utility Commands

### `dbt deps`
**Purpose**: Install packages from `packages.yml`

```bash
dbt deps
```

**When to Use**: After updating `packages.yml` or cloning repo

---

### `dbt clean`
**Purpose**: Delete compiled files in `target/` and `dbt_packages/`

```bash
dbt clean
```

**When to Use**: Troubleshooting compilation issues, fresh start

---

### `dbt debug`
**Purpose**: Test database connection and validate setup

```bash
dbt debug
```

**When to Use**: Connection errors, initial setup validation

---

### `dbt parse`
**Purpose**: Parse project without running (validates structure)

```bash
dbt parse
```

**When to Use**: CI checks, validate refactoring doesn't break structure

---

## 🎨 Node Selection Syntax

### Basic Selectors

| Selector | Description | Example |
|----------|-------------|---------|
| `model_name` | Specific model | `int_interchange__revenue_calc` |
| `path/to/models` | Directory path | `marts/finance` |
| `tag:tag_name` | By tag | `tag:daily` |
| `package:name` | By package | `package:dbt_utils` |
| `source:name` | By source | `source:edw` |

### Graph Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `+` (prefix) | Model + all parents (upstream) | `+int_interchange__revenue_calc` |
| `+` (suffix) | Model + all children (downstream) | `int_interchange__revenue_calc+` |
| `n+` | Model + N levels of parents | `2+int_interchange__revenue_calc` |
| `+n` | Model + N levels of children | `int_interchange__revenue_calc+1` |
| `@` | Model only (no deps) | `@int_interchange__revenue_calc` |

### Combining Selectors

**Union (space-separated)**:
```bash
dbt run --select model_a model_b model_c
```

**Intersection (comma-separated)**:
```bash
# Models in marts/finance AND tagged daily
dbt run --select marts/finance,tag:daily
```

**Exclusion**:
```bash
# All marts except deprecated
dbt run --select marts.* --exclude tag:deprecated
```

### State-Based Selection

**Modified models** (requires `--state` path):
```bash
# Run only changed models + downstream
dbt run --select state:modified+ --defer --state ./prod-artifacts/
```

**New models**:
```bash
dbt run --select state:new --state ./prod-artifacts/
```

---

## 🚨 Common Patterns for Handoff Execution

### Pattern 1: Full Pipeline Run (First Time)
```bash
# Step 1: Compile
dbt compile --select +mrt_interchange__revenue_by_product

# Step 2: Check dependencies
dbt ls --select +mrt_interchange__revenue_by_product

# Step 3: Run full-refresh
dbt run --select +mrt_interchange__revenue_by_product --full-refresh

# Step 4: Test
dbt test --select +mrt_interchange__revenue_by_product
```

### Pattern 2: Incremental Model Testing
```bash
# First run (full-refresh)
dbt run --select int_interchange__revenue_calc --full-refresh

# Second run (incremental - should only process new data)
dbt run --select int_interchange__revenue_calc

# Verify incremental worked (check row count increased appropriately)
```

### Pattern 3: QA Validation with dbt show
```bash
# Quick preview of QA query results
dbt show --inline "
WITH new_metrics AS (
    SELECT calendar_month, SUM(revenue) AS total
    FROM {{ ref('int_interchange__revenue_calc') }}
    GROUP BY 1
),
legacy_metrics AS (
    SELECT calendar_month, SUM(revenue) AS total
    FROM {{ ref('stg_analytics__bia_edwkpi_fkm_master') }}
    WHERE metric = 'Interchange Revenue $'
    GROUP BY 1
)
SELECT
    n.calendar_month,
    n.total AS new_total,
    l.total AS legacy_total,
    (n.total - l.total) / l.total * 100 AS pct_variance
FROM new_metrics n
JOIN legacy_metrics l USING (calendar_month)
ORDER BY 1 DESC
" --limit 50
```

### Pattern 4: Changed Models Only (CI/Development)
```bash
# Assumes you have --state artifacts from production
dbt build --select state:modified+ --defer --state ./target-prod/
```

---

## 📊 Status Codes (dbt run)

| Code | Status | Description |
|------|--------|-------------|
| 1 | Queued | Waiting to execute |
| 2 | Starting | Initializing |
| 3 | Running | Executing SQL |
| 10 | Success | Completed successfully |
| 20 | Error | Failed with error |
| 30 | Canceled | User canceled |
| 40 | Skipped | Not selected or dependencies failed |

---

## 🔍 Troubleshooting with dbt Fusion

### Use Fusion's Semantic Understanding

**Instead of guessing**, ask Fusion:
```
"Why did this compilation fail?"
"What's wrong with this SQL syntax?"
"How do I select all models in the marts layer?"
```

### Common Issues

**Issue**: "Could not find model X"
- **Fix**: Run `dbt ls --select X` to verify model name/path
- **Fix**: Run `dbt deps` if it's a package model

**Issue**: "Compilation Error: relation does not exist"
- **Fix**: Model may not exist in database - run upstream models first
- **Fix**: Use `dbt compile --select +X` to check all dependencies

**Issue**: "Incremental model not working (full refresh every time)"
- **Fix**: Check `unique_key` config matches actual columns
- **Fix**: Verify `{{ this }}` references are correct
- **Fix**: Test with `--full-refresh` vs without

---

## 💡 Best Practices for Copilot

### ✅ Do This
- **Preview with `dbt ls`** before expensive runs
- **Use `dbt show --inline`** for QA query validation (faster than full run)
- **Report actual outputs**: Include row counts, execution time, variance %
- **Use `--full-refresh` first**, then test incremental behavior
- **Check dependencies** with `dbt compile --select +model` before running

### ❌ Avoid This
- Running models without `--select` (runs entire project)
- Skipping QA validation step
- Assuming incremental works without testing
- Using `dbt run` when `dbt build` would catch test failures

---

## 📚 Related Resources

- **Official Docs**: https://docs.getdbt.com/reference/dbt-commands
- **Node Selection**: https://docs.getdbt.com/reference/node-selection/syntax
- **Handoff Template**: `shared/templates/handoff-package-template.md`
- **Pipeline Playbook**: `shared/reference/pipeline-build-playbook.md`

---

**Quick Reference Card** (copy-paste ready):
```bash
# Common handoff workflow
dbt compile --select +model        # Validate syntax
dbt ls --select +model              # Check dependencies
dbt run --select model+ --full-refresh  # First run (full)
dbt run --select model              # Test incremental
dbt test --select model             # Data quality tests
dbt show --inline "SELECT ..." --limit 100  # QA validation
```
