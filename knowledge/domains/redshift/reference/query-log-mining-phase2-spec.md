# Query Log Mining: Phase 2 Extraction Spec

**Created:** 2025-12-27
**Purpose:** Extract maximum value from Redshift query logs for agent-facing knowledge
**Input:** `greendot_analytics_mtegysvc_compute_stats.xlsx` (474K queries, 30 days)
**Output:** Structured knowledge artifacts for dbt-agent consumption

---

## Executive Summary

Phase 1 extracted ~40% of available value (top tables, metrics, anti-patterns). Phase 2 targets the remaining 60%:

| Category | Phase 1 | Phase 2 |
|----------|---------|---------|
| Table frequency | ✅ Top 10 | Extend to all tables with domain classification |
| Metrics | ✅ Top 5 aggregations | All aggregation patterns → measure candidates |
| Join relationships | ✅ 4 table pairs | Complete join registry with metadata |
| Controlled vocabulary | ❌ | Alias mining → canonical term dictionary |
| Semantic model elements | ❌ | Dimension/measure/entity inference |
| Anti-pattern impact | ⚠️ Counts only | Correlate with execution time |

---

## Extraction Targets

### 1. Complete Join Registry

**Goal:** Build normalized registry of all join relationships with metadata.

**Extraction Logic:**
```python
# Parse JOIN conditions from query text
join_pattern = r'''
    (LEFT|RIGHT|INNER|OUTER|CROSS)?\s*JOIN\s+
    (\w+\.?\w+)\s+                    # target table
    (?:AS\s+)?(\w+)?\s*               # optional alias
    ON\s+(.+?)                        # join condition
    (?=LEFT|RIGHT|INNER|OUTER|CROSS|JOIN|WHERE|GROUP|ORDER|$)
'''
```

**Output Schema:**
```yaml
# shared/reference/join-registry.yml

metadata:
  generated: "2025-12-27"
  source: "Redshift query logs (30 days)"
  query_count: 474260
  unique_joins: <count>

joins_by_source:
  <source_table>:
    - target: <target_table>
      key: <join_column>
      frequency: <count>
      cardinality: "1:1" | "1:N" | "N:1" | "N:M"
      join_types:
        INNER: <count>
        LEFT: <count>
      avg_execution_sec: <float>
      canonical: true | false
      orphan_risk: true | false  # if LEFT JOIN and target is smaller

joins_by_target:
  # Reverse index for bidirectional lookup
  <target_table>:
    - source: <source_table>
      key: <join_column>
      frequency: <count>

edges:
  # Flat list for graph algorithms
  - source: <table>
    target: <table>
    weight: <frequency>
    key: <column>
```

**Cardinality Inference:**
- If `COUNT(DISTINCT a.key) ≈ COUNT(DISTINCT b.key)` → 1:1
- If `COUNT(DISTINCT a.key) >> COUNT(DISTINCT b.key)` → N:1
- If both high with many matches → N:M
- Use sample query execution to verify

---

### 2. Controlled Vocabulary (Alias Mining)

**Goal:** Extract column aliases to build canonical term dictionary.

**Extraction Logic:**
```python
# Extract AS <alias> patterns
alias_pattern = r'''
    (\w+\.)?(\w+)           # column reference
    \s+AS\s+
    ["\']?(\w+)["\']?       # alias (with optional quotes)
'''

# Also extract from SELECT list without AS
implicit_alias_pattern = r'''
    (\w+)\s*,               # just column name in SELECT
'''
```

**Output Schema:**
```yaml
# shared/reference/controlled-vocabulary.yml

metadata:
  generated: "2025-12-27"
  total_aliases: <count>
  conflict_count: <count>  # same column, different aliases

canonical_terms:
  # Canonical name → all observed aliases
  transaction_amount:
    canonical: transactionamount
    aliases:
      - txn_amt (frequency: 234)
      - trans_amount (frequency: 156)
      - amount (frequency: 89)
    source_columns:
      - tpg.cashreceiptsubledger.transactionamount
      - tpg.cashdisbursementsubledger.transactionamount
      - gbos.transaction.amount

  customer_id:
    canonical: acct_uid
    aliases:
      - customer_id (frequency: 567)
      - cust_id (frequency: 234)
      - account_id (frequency: 123)
    source_columns:
      - edw.dim_account.acct_uid
      - gbos.account.acct_uid

conflicts:
  # Same alias used for different columns
  - alias: "amount"
    used_for:
      - tpg.cashreceiptsubledger.transactionamount (freq: 89)
      - gbos.fee.fee_amount (freq: 45)
      - edw.dim_account.balance_amount (freq: 12)
    resolution: "Disambiguate by prefix (txn_amount, fee_amount, balance_amount)"
```

**Conflict Resolution Rules:**
1. Higher frequency wins for canonical designation
2. Conflicts flagged for human review
3. Generate disambiguation recommendations

---

### 3. Semantic Model Elements

**Goal:** Infer dimension, measure, and entity candidates from query patterns.

**Extraction Logic:**

**Dimensions (from GROUP BY):**
```python
group_by_pattern = r'GROUP\s+BY\s+(.+?)(?=HAVING|ORDER|LIMIT|$)'
# Columns appearing in GROUP BY = dimension candidates
```

**Measures (from aggregations):**
```python
agg_pattern = r'(SUM|COUNT|AVG|MIN|MAX)\s*\(\s*(DISTINCT\s+)?(.+?)\s*\)'
# Columns being aggregated = measure candidates
```

**Entities (from JOIN keys):**
```python
# Primary entity: column appears as target of many JOINs
# Foreign entity: column appears as source of JOINs
```

**Time Dimensions (from date filters):**
```python
time_filter_pattern = r'''
    (\w+\.?\w+)                     # column
    \s*(>=?|<=?|BETWEEN)\s*
    ['\"]?\d{4}-\d{2}-\d{2}         # date literal
'''
```

**Output Schema:**
```yaml
# shared/reference/semantic-candidates.yml

metadata:
  generated: "2025-12-27"
  tables_analyzed: <count>

tables:
  tpg.cashreceiptsubledger:
    dimensions:
      categorical:
        - name: journaltransactiontypeid
          frequency: 1234
          sample_values: [1, 2, 3, 4]
        - name: isdebit
          frequency: 218
          sample_values: [true, false]
      time:
        - name: transactiondate
          frequency: 892
          granularities_used: [day, month]

    measures:
      - name: transactionamount
        aggregations:
          SUM: 436
          AVG: 12
          COUNT: 5
        agg_recommendation: sum
      - name: feeamount
        aggregations:
          SUM: 89
        agg_recommendation: sum

    entities:
      - name: application_id
        type: foreign
        joins_to: tpg.application
        frequency: 1847
      - name: subledger_id
        type: primary
        cardinality: 12_000_000

  edw.dim_account:
    dimensions:
      categorical:
        - name: acct_link_type
          frequency: 456
          sample_values: ['PRIMARY', 'VAULT', 'SECONDARY']
    entities:
      - name: acct_uid
        type: primary
        cardinality: 18_000_000
        # This is the most-joined column in the warehouse
        inbound_join_frequency: 8934
```

---

### 4. Anti-Pattern Impact Correlation

**Goal:** Quantify execution time impact of each anti-pattern.

**Extraction Logic:**
```python
# For each query, detect anti-patterns AND capture execution time
# Build regression: execution_time ~ anti_pattern_flags + row_count

anti_patterns = {
    'SELECT *': r'SELECT\s+\*',
    'OR in JOIN': r'JOIN.+ON.+OR',
    'NOT IN subquery': r'NOT\s+IN\s*\(',
    'CROSS JOIN': r'CROSS\s+JOIN',
    'Nested subqueries': lambda sql: sql.count('SELECT') > 3,
    'DISTINCT in agg': r'COUNT\s*\(\s*DISTINCT',
}
```

**Output Schema:**
```yaml
# shared/reference/anti-pattern-impact.yml

metadata:
  generated: "2025-12-27"
  queries_analyzed: 474260

impact_by_pattern:
  - pattern: "SELECT *"
    frequency: 6635
    avg_execution_sec: 34.2
    median_execution_sec: 12.1
    avg_without_pattern: 18.7
    impact_multiplier: 1.83x  # queries with this pattern are 83% slower
    p95_execution_sec: 145.0

  - pattern: "OR in JOIN"
    frequency: 3850
    avg_execution_sec: 67.8
    median_execution_sec: 28.4
    avg_without_pattern: 21.3
    impact_multiplier: 3.18x
    p95_execution_sec: 312.0
    priority: P1  # Highest impact, fix first

  - pattern: "NOT IN subquery"
    frequency: 1964
    avg_execution_sec: 89.2
    impact_multiplier: 4.21x
    priority: P1

  - pattern: "CROSS JOIN"
    frequency: 449
    avg_execution_sec: 234.5
    impact_multiplier: 11.1x
    priority: P0  # Critical, always fix

# Combination effects (patterns that compound)
combinations:
  - patterns: ["SELECT *", "OR in JOIN"]
    frequency: 234
    avg_execution_sec: 156.7
    compounding_factor: 1.4x  # worse than sum of individual impacts
```

---

### 5. Ratio Metric Candidates

**Goal:** Identify division patterns that should become ratio metrics.

**Extraction Logic:**
```python
# Pattern: SUM(a) / SUM(b) or COUNT(a) / COUNT(b)
ratio_pattern = r'''
    (SUM|COUNT|AVG)\s*\([^)]+\)\s*   # numerator
    /\s*
    (SUM|COUNT|AVG)\s*\([^)]+\)      # denominator
'''
```

**Output Schema:**
```yaml
# shared/reference/ratio-metric-candidates.yml

candidates:
  - name: average_order_value
    pattern: "SUM(transactionamount) / COUNT(DISTINCT order_id)"
    frequency: 234
    numerator:
      measure: transactionamount
      aggregation: SUM
    denominator:
      measure: order_id
      aggregation: COUNT_DISTINCT
    recommendation: "Create ratio metric in semantic layer"

  - name: approval_rate
    pattern: "COUNT(approved) / COUNT(*)"
    frequency: 156
    filter_in_numerator: "status = 'APPROVED'"
    recommendation: "Create ratio metric with filter"
```

---

### 6. Saved Query Candidates

**Goal:** Identify common filter + grouping combinations for saved queries.

**Extraction Logic:**
```python
# Cluster queries by:
# - Tables used (same set)
# - Columns in GROUP BY (same set)
# - Filter patterns (similar WHERE clauses)

# Queries with >10 occurrences of same pattern = saved query candidate
```

**Output Schema:**
```yaml
# shared/reference/saved-query-candidates.yml

candidates:
  - name: daily_revenue_by_product
    frequency: 89
    pattern:
      tables:
        - tpg.cashreceiptsubledger
        - tpg.application
      group_by:
        - metric_time (day)
        - product_type
      metrics:
        - SUM(transactionamount)
        - COUNT(DISTINCT application_id)
      common_filters:
        - "transactiondate >= CURRENT_DATE - 30"
    recommendation: "Create saved query in semantic layer"

  - name: monthly_overdraft_summary
    frequency: 45
    pattern:
      tables:
        - edw.v_fct_deposit_acct_bal_dtl_hist
        - edw.dim_account
      group_by:
        - metric_time (month)
        - acct_link_type
      metrics:
        - COUNT(DISTINCT acct_uid)
        - SUM(overdraft_amount)
```

---

## Implementation Plan

### Tools Required

```python
# requirements.txt additions
sqlglot>=20.0.0      # SQL parsing with Redshift dialect
polars>=0.20.0       # Fast DataFrame operations
networkx>=3.0        # Graph building and algorithms
scikit-learn>=1.3    # For clustering similar queries
pyyaml>=6.0          # Output to YAML
```

### Script Structure

```
tools/
  query_log_mining/
    __init__.py
    parser.py           # SQL parsing with sqlglot
    join_extractor.py   # Extract join relationships
    alias_miner.py      # Extract column aliases
    semantic_inferrer.py # Infer dimensions/measures/entities
    anti_pattern_analyzer.py # Correlate patterns with execution time
    ratio_detector.py   # Find division patterns
    query_clusterer.py  # Cluster similar queries
    registry_builder.py # Build final YAML outputs
    main.py             # Orchestration
```

### Execution Steps

```bash
# 1. Parse all queries (expensive, cache results)
python -m tools.query_log_mining.main parse \
  --input greendot_analytics_mtegysvc_compute_stats.xlsx \
  --output cache/parsed_queries.parquet

# 2. Extract joins
python -m tools.query_log_mining.main extract-joins \
  --input cache/parsed_queries.parquet \
  --output shared/reference/join-registry.yml

# 3. Mine aliases
python -m tools.query_log_mining.main mine-aliases \
  --input cache/parsed_queries.parquet \
  --output shared/reference/controlled-vocabulary.yml

# 4. Infer semantic elements
python -m tools.query_log_mining.main infer-semantic \
  --input cache/parsed_queries.parquet \
  --output shared/reference/semantic-candidates.yml

# 5. Analyze anti-pattern impact
python -m tools.query_log_mining.main analyze-impact \
  --input cache/parsed_queries.parquet \
  --output shared/reference/anti-pattern-impact.yml

# 6. Detect ratio metrics
python -m tools.query_log_mining.main detect-ratios \
  --input cache/parsed_queries.parquet \
  --output shared/reference/ratio-metric-candidates.yml

# 7. Cluster for saved queries
python -m tools.query_log_mining.main cluster-queries \
  --input cache/parsed_queries.parquet \
  --output shared/reference/saved-query-candidates.yml
```

---

## Success Metrics

| Artifact | Target | Validation |
|----------|--------|------------|
| Join Registry | 100+ unique joins captured | Manual spot-check of top 10 |
| Controlled Vocabulary | 50+ canonical terms | Alias conflicts identified |
| Semantic Candidates | Dimension/measure for top 20 tables | Cross-reference with existing dbt models |
| Anti-Pattern Impact | All 6 patterns quantified | Statistical significance test |
| Ratio Metrics | 10+ candidates | Frequency >20 each |
| Saved Queries | 20+ candidates | Frequency >10 each |

---

## Future: Historical Data Expansion

**Decision Point:** After Phase 2 completes, evaluate:

1. **Did we miss seasonal patterns?** → Add 12 months history
2. **Are pattern frequencies stable?** → 30 days is sufficient
3. **Do we need trend detection?** → Add rolling window comparison

**If expanding to 12 months:**
- Switch from Excel to direct Redshift query (STL_QUERY + STL_QUERYTEXT)
- Sample to 10% of queries to manage volume
- Add `month` dimension to all outputs for trend analysis

---

## References

- [BigQuery Knowledge Engine](https://cloud.google.com/blog/products/data-analytics/data-analytics-innovations-at-next25) - Google's approach to auto-generating metadata from query logs
- [AWS: Enriching Metadata for Text-to-SQL](https://aws.amazon.com/blogs/big-data/enriching-metadata-for-accurate-text-to-sql-generation-for-amazon-athena/) - 27% accuracy improvement with enriched metadata
- [arXiv: Query Logs Analytics - Systematic Review](https://arxiv.org/html/2508.13949v1) - Academic framework for log curation
- [Select Star: Why LLMs Struggle with Text-to-SQL](https://www.selectstar.com/resources/text-to-sql-llm) - 42% of context-less queries miss critical filters

---

*Spec created by dbt-agent Learner, 2025-12-27*
