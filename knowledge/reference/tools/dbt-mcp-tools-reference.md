<!--
source_of_truth: analytics-workspace
mirrored_from: dbt-agent/shared/reference/dbt-mcp-tools-reference.md
-->

> analytics-workspace migration note: this is a promoted copy from `dbt-agent`. Prefer this analytics-workspace path first. If a referenced companion doc has not been promoted yet, fall back to `dbt-agent`.

# dbt MCP Tools Reference

> **Purpose**: Comprehensive reference for all dbt MCP server tools available to Claude Code.
> **Critical**: These tools are the key enabler for the 4-agent workflow. USE THEM.

---

## VPN Architecture: API vs CLI Execution Paths

dbt MCP tools use **two different execution paths**. This determines what works without VPN.

| Execution Path | Route | VPN Required? |
|----------------|-------|---------------|
| **API tools** | SQL ships to dbt Cloud REST API → dbt Cloud connects to warehouse | **No** |
| **CLI tools** | Invokes dbt CLI locally → resolves warehouse hostname from your network | **Yes** |

### API Tools (No VPN — Read-Only Warehouse Access)

`execute_sql`, `query_metrics`, `get_model_details`, `get_source_details`, `get_related_models`, `get_model_health`, `get_column_lineage`, `get_model_parents`, `get_model_children`, `get_all_models`, `get_all_sources`, `list_metrics`, `get_dimensions`, `text_to_sql`, `get_metrics_compiled_sql`

### CLI Tools (VPN Required — Local Execution)

`compile`, `run`, `build`, `test`, `show`, `parse`, `docs`, `ls`

### Data Profiling Without VPN

Use `execute_sql` for quick data profiling when VPN is off:

```sql
-- Column discovery
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'dbt' AND table_name = 'my_model'
ORDER BY ordinal_position

-- Quick sample (use raw table names, not {{ ref() }})
SELECT * FROM schema.table LIMIT 10

-- Value distribution
SELECT column, COUNT(*) as cnt
FROM schema.table GROUP BY 1 ORDER BY 2 DESC LIMIT 20

-- Null audit
SELECT COUNT(*) as total,
  SUM(CASE WHEN col IS NULL THEN 1 ELSE 0 END) as nulls
FROM schema.table

-- Date range
SELECT MIN(event_date), MAX(event_date), COUNT(DISTINCT event_date)
FROM schema.table
```

**Important**: `execute_sql` uses raw table/schema names. For `{{ ref() }}` and `{{ source() }}` support, use `dbt show --inline` (requires VPN).

---

## Quick Reference by Workflow Phase

| Phase | Primary Tools | Purpose |
|-------|---------------|---------|
| **Phase 1: Requirements** | `search`, `get_all_models` | Find existing patterns |
| **Phase 2: Data Discovery** | `show`, `get_source_details`, `get_column_lineage` | Profile data, validate schemas |
| **Phase 3: Architecture** | `get_model_details`, `get_related_models`, `get_model_health` | Design model inventory |
| **Phase 4: Implementation** | `compile`, `build`, `run`, `test`, `generate_*` | Build and validate |
| **QA Execution** | `show`, `execute_sql`, `test`, `get_model_health` | Deep validation |

---

## Tool Categories

### 1. dbt CLI Commands (Local Execution)

#### `build`
**Purpose**: Execute models, tests, snapshots, and seeds in dependency order

```
Use: After implementation to validate entire pipeline
Command pattern: dbt build --select model_name+
Best practice: Always build with + to include downstream
```

#### `compile`
**Purpose**: Generate executable SQL without running it

```
Use: MANDATORY before any run command (12-30x ROI on catching errors)
Command pattern: dbt compile --select model_name
Output: target/compiled/ directory with resolved SQL
```

#### `run`
**Purpose**: Materialize models in the database

```
Use: After compile succeeds
Command pattern: dbt run --select model_name --full-refresh
Note: Use --full-refresh for initial runs, omit for incremental
```

#### `test`
**Purpose**: Validate data integrity

```
Use: After run to verify data quality
Command pattern: dbt test --select model_name
```

#### `show` ⭐ KEY TOOL FOR DATA DISCOVERY
**Purpose**: Execute queries against the warehouse and preview results

```
Use Cases:
- Profile source data (row counts, date ranges, distributions)
- Validate schema assumptions
- Run volume trace queries
- Execute ad-hoc validation queries

Command patterns:
  dbt show --select model_name                    # Preview model output
  dbt show --inline "SELECT COUNT(*) FROM ..."    # Run arbitrary SQL
  dbt show --select model_name --limit 100        # Customize row limit

Default: Returns 5 rows. Use --limit N for more.
```

**Data Discovery Patterns with `dbt show`:**
```sql
-- Profile source table
dbt show --inline "
  SELECT
    COUNT(*) as row_count,
    MIN(created_date) as earliest,
    MAX(created_date) as latest,
    COUNT(DISTINCT account_id) as unique_accounts
  FROM {{ source('schema', 'table') }}
"

-- Check column distribution
dbt show --inline "
  SELECT
    status,
    COUNT(*) as cnt,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as pct
  FROM {{ source('schema', 'table') }}
  GROUP BY 1
  ORDER BY 2 DESC
" --limit 20

-- Validate join success rate
dbt show --inline "
  SELECT
    COUNT(*) as total,
    COUNT(b.id) as matched,
    ROUND(100.0 * COUNT(b.id) / COUNT(*), 2) as match_rate
  FROM {{ ref('model_a') }} a
  LEFT JOIN {{ ref('model_b') }} b ON a.key = b.key
"
```

#### `ls` (list)
**Purpose**: List project resources

```
Use: Check dependencies before build
Command pattern: dbt ls --select +model_name --resource-type model
```

#### `parse`
**Purpose**: Validate project files

```
Use: Quick syntax check
Command pattern: dbt parse
```

#### `docs`
**Purpose**: Generate project documentation

```
Use: After implementation complete
Command pattern: dbt docs generate && dbt docs serve
```

---

### 2. Semantic Layer Tools

#### `list_metrics`
**Purpose**: Retrieve all defined metrics

```
Use: Understand existing metric landscape before building new
```

#### `get_dimensions`
**Purpose**: Get dimensions available for specified metrics

```
Use: When designing metrics in tech spec
```

#### `query_metrics`
**Purpose**: Execute metric queries with grouping, ordering, filtering

```
Use: Validate metric calculations against expectations
```

#### `get_metrics_compiled_sql`
**Purpose**: Get compiled SQL for metrics without execution

```
Use: Debug metric definitions, understand generated queries
```

---

### 3. Metadata Discovery (Discovery API) ⭐ KEY FOR ARCHITECTURE

#### `get_all_models` / `get_mart_models`
**Purpose**: Retrieve model information

```
Use: Inventory existing models during architecture phase
```

#### `get_model_details`
**Purpose**: Get detailed model metadata

```
Use: Understand model configuration, columns, tests
Returns: Config, columns, tests, description, materialization
```

#### `get_model_parents` / `get_model_children`
**Purpose**: Get lineage relationships

```
Use:
- Map dependencies during data discovery
- Impact analysis before changes
- Validate architecture decisions
```

#### `get_model_health` ⭐ QUALITY SIGNAL
**Purpose**: Retrieve health signals for models

```
Use:
- Assess model reliability during architecture
- Identify risky dependencies
- Prioritize QA focus
```

#### `get_all_sources` / `get_source_details`
**Purpose**: Get source table metadata

```
Use: Data discovery phase - understand raw data landscape
Returns: Columns, freshness, descriptions
```

#### `get_column_lineage` ⭐ CRITICAL FOR TRANSFORMATION RULES
**Purpose**: Column-level lineage across project DAG

```
Use:
- Map transformation rules in tech spec
- Understand data flow for specific columns
- Impact analysis for schema changes
```

#### `search`
**Purpose**: Exact string matching against code and descriptions

```
Use: Find existing patterns, canonical models, similar logic
```

#### `get_related_models` ⭐ CANONICAL MODEL DISCOVERY
**Purpose**: Semantic similarity search for related models

```
Use:
- Find canonical models to reuse
- Discover similar transformations
- Avoid duplicate logic
```

---

### 4. Code Generation ⭐ ACCELERATE IMPLEMENTATION

#### `generate_source`
**Purpose**: Generate source YAML from database tables

```
Use: When onboarding new sources in staging layer
Output: _sources.yml with column definitions
```

#### `generate_model_yaml`
**Purpose**: Generate model YAML documentation

```
Use: After model creation, generate schema.yml
Output: Column descriptions, tests scaffold
```

#### `generate_staging_model`
**Purpose**: Generate staging model SQL

```
Use: Create stg_ models from sources
Output: SQL with column renaming, type casting
```

#### `text_to_sql`
**Purpose**: Convert natural language to SQL

```
Use: Prototype queries from business requirements
Caution: Always validate generated SQL
```

#### `execute_sql` ⭐ VPN-FREE WAREHOUSE ACCESS
**Purpose**: Run arbitrary SQL on the warehouse via dbt Cloud API (no VPN needed)

```
Use: Data profiling, column discovery, sample rows, validation queries
Route: SQL → dbt Cloud REST API → dbt Cloud's warehouse connection → results
Note: Uses raw table names (schema.table), NOT {{ ref() }} or {{ source() }}
      Read-only SELECT queries. Cannot materialize (CREATE TABLE AS).
      Ideal fallback when VPN is off but you need warehouse data.
```

---

### 5. Job Management (dbt Cloud)

#### `list_jobs` / `get_job_details`
**Purpose**: View job configurations

#### `trigger_job_run`
**Purpose**: Start a job run

#### `list_job_runs` / `get_job_run_details`
**Purpose**: Monitor run status

#### `get_job_run_artifacts`
**Purpose**: Access run artifacts (manifest, logs)

---

### 6. Fusion Tools

#### `compile_sql`
**Purpose**: Compile SQL in project context

```
Use: Validate SQL with Jinja resolution
```

---

## Integration by Skill

### dbt-data-discovery (Phase 2)

**Primary Tools:**
```
dbt show --inline "..."      # Profile source data
get_source_details           # Source metadata
get_column_lineage           # Understand transformations
get_model_parents/children   # Map relationships
```

**Example Workflow:**
```
1. get_all_sources → List available sources
2. get_source_details → Get column info for target source
3. dbt show --inline → Profile data (counts, distributions, NULLs)
4. dbt show --inline → Run volume trace queries
5. get_column_lineage → Map how columns flow through existing models
```

### dbt-tech-spec-writer (Phase 3)

**Primary Tools:**
```
get_all_models              # Inventory existing models
get_model_details           # Understand configurations
get_related_models          # Find canonical models to reuse
get_model_health            # Assess quality signals
search                      # Find specific patterns
```

**Example Workflow:**
```
1. get_related_models → Find similar existing models
2. get_model_details → Understand their structure
3. get_model_health → Assess quality signals
4. search → Find specific patterns or business logic
5. Design model inventory based on findings
```

### dbt-migration (Phase 4)

**Primary Tools:**
```
compile                     # MANDATORY before run
build / run / test          # Execute models
generate_source             # Create source YAML
generate_model_yaml         # Generate documentation
generate_staging_model      # Accelerate staging layer
```

**Example Workflow:**
```
1. generate_staging_model → Create stg_ models if needed
2. Write intermediate/mart models
3. compile → Validate SQL (MANDATORY)
4. run --full-refresh → Execute models
5. test → Validate data quality
6. generate_model_yaml → Create documentation
```

### dbt-qa-execution

**Primary Tools:**
```
dbt show --inline "..."     # Execute validation queries
test                        # Run data tests
execute_sql                 # Run comparison queries
get_model_health            # Check health signals
```

**Example Workflow:**
```
1. dbt show → Execute QA comparison queries
2. dbt show → Drill down by dimensions
3. test → Run all model tests
4. get_model_health → Verify health signals
5. dbt show → Validate incremental behavior
```

---

## Critical Rules

### Rule 1: Always Compile Before Run
```
❌ WRONG: dbt run --select model
✅ CORRECT: dbt compile --select model && dbt run --select model
```
ROI: 12-30x faster error detection

### Rule 2: Use `dbt show` for Data Discovery
```
❌ WRONG: Assume data characteristics from schema
✅ CORRECT: Profile with dbt show before designing
```
Prevents: 99% suppression issues (GBOS incident)

### Rule 3: Check Dependencies First
```
❌ WRONG: Build model without checking upstream
✅ CORRECT: dbt ls --select +model --resource-type model
```
Alternative: Use manifest-parser skill for instant lineage

### Rule 4: Use `get_related_models` for Reuse
```
❌ WRONG: Build new model without checking for existing
✅ CORRECT: get_related_models to find canonical candidates
```
Target: 75-90% reuse from existing models

### Rule 5: Leverage Code Generation
```
❌ WRONG: Write all YAML by hand
✅ CORRECT: generate_source, generate_model_yaml to scaffold
```
Time saved: 50-70% on documentation

---

## MCP Tool Cheat Sheet

```
DATA DISCOVERY:
  dbt show --inline "SELECT ..."     # Query data
  get_source_details                 # Source metadata
  get_column_lineage                 # Column flow

ARCHITECTURE:
  get_related_models                 # Find similar models
  get_model_health                   # Quality signals
  search                             # Pattern matching

IMPLEMENTATION:
  compile                            # Validate SQL
  build / run / test                 # Execute
  generate_*                         # Code generation

VALIDATION:
  dbt show                           # QA queries
  test                               # Data tests
  execute_sql                        # Comparison queries
```

---

## Troubleshooting

### MCP Server Not Responding
```bash
# Check if server is running
# Config: ~/.cursor/dbt-mcp.env

# Restart by refreshing Claude Code session
```

### Tool Not Found
```
Ensure dbt-mcp is configured in .mcp.json
Check tool groups enabled in dbt-mcp.env
```

### Permission Denied
```
Verify dbt Cloud token has required permissions
Check environment IDs match project settings
```

### Semantic Layer API Query Succeeds But Parsing Fails

Symptoms:
- `createQuery` and poll query return `status=SUCCESSFUL`
- `totalRows` is non-zero
- JSON parsing fails on `jsonResult` with `JSONDecodeError`

Root cause:
- `jsonResult` may be base64-encoded JSON (not plain JSON text).

Resolution pattern:
1. Use `createQuery` + poll `query` until terminal status (`SUCCESSFUL` or `FAILED`).
2. If `jsonResult` exists, attempt parse in this order:
   - `json.loads(jsonResult)`
   - `json.loads(base64.b64decode(jsonResult).decode("utf-8"))`
3. Persist raw create/poll responses for reproducibility.

Python parser snippet:
```python
import base64
import json

def parse_json_result(blob: str):
  if not blob:
    return None
  try:
    return json.loads(blob)
  except json.JSONDecodeError:
    pass
  try:
    decoded = base64.b64decode(blob).decode("utf-8")
    return json.loads(decoded)
  except Exception:
    return None
```

Operational notes:
- Prefer explicit GraphQL calls when preconfigured tasks produce malformed heredoc output or stale shell state.
- If shell prompt shows heredoc continuation state, rerun commands as a single non-interactive command and log to file.
- Keep environment binding explicit (service token + environment ID from `.mcp.json`).

---

## Related Resources

- **CLAUDE.md** - MCP connection settings
- **dbt-data-discovery** - Uses show, get_source_details
- **dbt-tech-spec-writer** - Uses get_model_*, search
- **dbt-migration** - Uses compile, build, generate_*
- **dbt-qa-execution** - Uses show, test, execute_sql
