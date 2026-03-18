# Query Log Mining Toolkit

**Purpose:** Extract structured knowledge from Redshift query logs for agent consumption.

**Spec:** [`docs/specs/query-log-mining-phase2-spec.md`](../../docs/specs/query-log-mining-phase2-spec.md)

---

## Quick Start

```bash
# Install dependencies
pip install sqlglot polars networkx pyyaml scikit-learn openpyxl

# Run complete pipeline
python -m tools.query_log_mining.main run-all \
  --input path/to/query_logs.xlsx \
  --output-dir shared/reference/
```

---

## What This Does

Builds on Phase 1 narrative analysis to create **machine-parseable YAML artifacts**:

| Artifact | File | Agent Use Case |
|----------|------|----------------|
| Join Registry | `join-registry.yml` | "What tables join with X?" |
| Controlled Vocabulary | `controlled-vocabulary.yml` | "What's the canonical name for this column?" |
| Semantic Candidates | `semantic-candidates.yml` | "What measures/dimensions should I create?" |
| Anti-Pattern Impact | `anti-pattern-impact.yml` | "How bad is SELECT * really?" |
| Ratio Metrics | `ratio-metric-candidates.yml` | "What derived metrics exist?" |
| Saved Queries | `saved-query-candidates.yml` | "What query patterns repeat?" |

---

## Modules

### `parser.py` - SQL Parsing

```python
from tools.query_log_mining import QueryParser

parser = QueryParser()
parsed = parser.parse(sql_text)
# Returns: AST, tables, columns, joins, aggregations
```

Uses `sqlglot` with Redshift dialect for accurate parsing.

### `join_extractor.py` - Join Relationships

```python
from tools.query_log_mining import JoinExtractor

extractor = JoinExtractor()
joins = extractor.extract_all(parsed_queries)
# Returns: Normalized join registry with frequency, cardinality
```

Outputs dual-indexed registry (by source AND target) for fast lookup.

### `alias_miner.py` - Controlled Vocabulary

```python
from tools.query_log_mining import AliasMiner

miner = AliasMiner()
vocabulary = miner.extract_all(parsed_queries)
# Returns: Canonical terms, aliases, conflicts
```

Identifies alias conflicts (same alias for different columns) for resolution.

### `semantic_inferrer.py` - Semantic Model Elements

```python
from tools.query_log_mining import SemanticInferrer

inferrer = SemanticInferrer()
candidates = inferrer.infer_all(parsed_queries)
# Returns: Dimension/measure/entity candidates per table
```

Uses GROUP BY for dimensions, aggregations for measures, JOIN keys for entities.

### `anti_pattern_analyzer.py` - Impact Correlation

```python
from tools.query_log_mining import AntiPatternAnalyzer

analyzer = AntiPatternAnalyzer()
impact = analyzer.analyze(parsed_queries, execution_times)
# Returns: Pattern -> execution time correlation
```

Quantifies actual performance impact of each anti-pattern.

---

## Commands

```bash
# Parse and cache (expensive, run once)
python -m tools.query_log_mining.main parse \
  --input query_logs.xlsx \
  --output cache/parsed_queries.parquet

# Extract joins
python -m tools.query_log_mining.main extract-joins \
  --input cache/parsed_queries.parquet \
  --output shared/reference/join-registry.yml

# Mine aliases
python -m tools.query_log_mining.main mine-aliases \
  --input cache/parsed_queries.parquet \
  --output shared/reference/controlled-vocabulary.yml

# Infer semantic elements
python -m tools.query_log_mining.main infer-semantic \
  --input cache/parsed_queries.parquet \
  --output shared/reference/semantic-candidates.yml

# Analyze anti-pattern impact
python -m tools.query_log_mining.main analyze-impact \
  --input cache/parsed_queries.parquet \
  --output shared/reference/anti-pattern-impact.yml

# Run all steps
python -m tools.query_log_mining.main run-all \
  --input query_logs.xlsx \
  --output-dir shared/reference/
```

### Schema Filtering (NEW)

Filter extraction to specific schemas for focused analysis:

```bash
# BaaS-focused extraction (EDW, GBOS, ODS only)
python -m tools.query_log_mining.main run-all \
  --input query_logs.xlsx \
  --output-dir shared/reference/ \
  --schemas edw,gbos,ods \
  --output-prefix baas-

# TPG-focused extraction
python -m tools.query_log_mining.main run-all \
  --input query_logs.xlsx \
  --output-dir shared/reference/ \
  --schemas tpg,edw \
  --output-prefix tpg-
```

**Options:**
- `--schemas` - Comma-separated list of schemas to include (e.g., `edw,gbos,ods`)
- `--output-prefix` - Prefix for output files (e.g., `baas-` produces `baas-join-registry.yml`)

---

## Input Format

Expects Excel/CSV with columns:
- `query_text` or `querytxt` - SQL query text
- `execution_time` or `total_exec_time` - Execution time in seconds
- `starttime` - Query start timestamp (optional, for temporal analysis)
- `rows` or `rows_returned` - Row count (optional)

---

## Relationship to Phase 1

| Phase | Output | Purpose |
|-------|--------|---------|
| **Phase 1** | `baas-schema-join-patterns.md` | Human-readable narrative |
| **Phase 1** | `2025-12-26-redshift-query-log-mining.md` | Executive summary |
| **Phase 2** | `*.yml` files | Machine-parseable for agents |

Phase 2 **builds on** Phase 1, does not replace it. Narrative docs remain valuable for human readers.

---

## Integration with Agents

### unified_retrieval()

Query log artifacts are indexed in the knowledge graph:

```python
from tools.kg.agent_integration import unified_retrieval

# Find join patterns
result = unified_retrieval("How do I join gbos.account to edw.dim_account?")
# Returns join registry entry with frequency, cardinality
```

### Experience Store

New patterns logged for cross-agent retrieval:

```python
from tools.kg.experience_store import ExperienceStore

store = ExperienceStore()
store.log_experience(
    pattern="EDW account enrichment join",
    context="gbos.account -> edw.dim_account via sor_acct_id",
    tags=["join", "edw", "gbos"]
)
```

---

## Success Metrics

| Artifact | Target | Validation |
|----------|--------|------------|
| Join Registry | 100+ unique joins | Spot-check top 10 |
| Vocabulary | 50+ canonical terms | Conflicts identified |
| Semantic Candidates | Top 20 tables covered | Cross-ref with dbt models |
| Anti-Pattern Impact | All 6 patterns quantified | Statistical significance |

---

## Extending

To add new extraction targets:

1. Create new module in `tools/query_log_mining/`
2. Add command to `main.py`
3. Update output schema in spec
4. Add tests in `tests/query_log_mining/`

---

*Created: 2025-12-27*
*Spec: docs/specs/query-log-mining-phase2-spec.md*
