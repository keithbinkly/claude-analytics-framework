# Comprehensive Plan: Redshift Granular Performance Mining & Recommendation Engine

**Objective:** Expand institutional knowledge by mining granular Redshift logs (`svl_query_metrics`) to identify specific performance bottlenecks, build a searchable Anti-Pattern Directory, and provide actionable rewrite recommendations for analysts.

**Audience:** Analysts & Engineers running ad-hoc queries and automated scripts.
**Outcome:** Reduced warehouse load, faster query times, and an AI-accessible knowledge base for instant optimizations.

---

## Phase 1: Knowledge Consolidation & Audit (Current Baseline)
**Status: ✅ COMPLETED**

We have established a strong semantic foundation. We must now layer "Physical Execution Reality" on top of "Semantic Intent."

### Existing Assets (Verified)
1.  **Semantic Schemas:** `patterns.schema.json` (Joins, Aliases, Filters).
2.  **Mined Artifacts (Phase 1-3):**
    *   `outputs/phase1/patterns.yaml`: Join topology from ODS/EDW.
    *   `outputs/phase3/business_concepts.yaml`: Logic specifications.
    *   `outputs/phase3/dbt_test_candidates.yaml`: Quality rules.
3.  **Extraction Tools:**
    *   `redshift_microstrategysvc_compute_stats_granular.sql`: (New) The physical probe.
    *   `tools/kg/agent_integration`: Existing search interface.

### The Missing Link
We have "What joins to what" (Semantic). We treat all joins as equal.
We *need* "What joins *poorly* to what" (Physical). We need to verify if a canonical join is actually a performance killer in practice.

---

## Phase 2: The "Granular" Pipeline Design
**Status: ✅ COMPLETED**
*( Delivered in `models/marts/ops/redshift_granular_mining.sql` )*

We will upgrade the extraction script to capture the **Minimum Viable Physical Signal (MVPS)**.

### 2.1 Enhanced Extraction Query (`redshift_granular_mining.sql`)
We will modify the current script to:
1.  **Scope**: Last 3-7 days (Rolling window).
2.  **Target**: All Users (captured: `svc_dbt_bi`, `etluser`, `microstrategysvc`, Ad-hoc).
3.  **Granularity**: Step-level metrics (`svl_query_metrics`).
4.  **Table Resolution**: Join `stl_scan` to resolve Table IDs to Table Names (for SCAN steps).
    *   *Note:* Non-scan steps (joins) inherit context from their input streams, which is harder to link directly to a single table without parsing. We will map SCAN steps to Tables and JOIN steps to "Operations between streams."
5.  **Failure Analysis**: Include `aborted` flag and `error_message` (from `stl_query` or `stl_error`) to categorize "Performance Failures" vs "Syntax Failures."

**Metric Schema (The "Physical Signature"):**
*   **Identity**: `query_fingerprint`, `user_group`, `timestamp`
*   **Flow**: `scan_rows` → `join_rows` → `return_rows` (The "Funnel")
*   **Resources**: `cpu_time`, `blocks_read`, `spilled_blocks` (Memory pressure)
*   **Skew**: `cpu_skew`, `io_skew` (Distribution health)

---

## Phase 3: The "Anti-Pattern" Directory (Signatures)
**Status: ✅ COMPLETED**
*( Delivered in `docs/research/mining/ANTI_PATTERN_DIRECTORY.md` )*

We will define a generic "Anti-Pattern Library" using logical rules against the metrics above. This replaces subjective "reviews" with objective "scans."

### 3.1 The Library (Signatures)

| ID | Anti-Pattern Name | Detection Rule (Signature) | Root Cause | Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| **AP-01** | **The Disk Spiller** | `step_label IN ('hashjoin', 'sort')` AND `temp_blocks > 0` | Memory Exhaustion (Join/Sort > Slot Memory) | 1. Check cartesian. 2. Increase WLM slots. 3. Reduce columns. |
| **AP-02** | **The Cartesian Bomb** | `join_rows > (scan_rows_left + scan_rows_right) * 10` | Join Logic Error (Fan-out) | Check join keys for uniqueness. Add distinct or group by early. |
| **AP-03** | **The Ghost Scanner** | `scan_rows > 1M` AND `return_rows < 100` AND `step_label='scan'` | Inefficient Filtering | Filter column is not a SORTKEY. Add filtering column to sort/dist keys. |
| **AP-04** | **The Skewed Worker** | `cpu_skew > 0.95` OR `io_skew > 0.95` | Distribution Error | Change DISTKEY to a high-cardinality column (e.g., `user_id` vs `status`). |
| **AP-05** | **The Serial Leader** | `step_label='aggr'` AND `cpu_time`=High | Leader Node Saturation | Remove `LISTAGG`, `MEDIAN`, or complex Python UDFs. |
| **AP-06** | **The Aborted Timeout** | `aborted=1` AND `duration > timeout_threshold` | Resource Contention | Check `AP-01` metrics just before abort. |

---

## Phase 4: Recommendation Engine & Searchability
**Status: ⚠️ PARTIALLY COMPLETED**
*( Delivered in `docs/research/mining/MINED_OPPORTUNITIES.md` and `performance_profiles_sample.json`. Next step: Integration with Agent Search Tools. )*

To make this "AI Retrieval Ready," we will transform the mined data into two artifacts.

### 4.1 The "Query Performance Profile" Json
A searchable index of every query pattern running in production.
```json
{
  "fingerprint": "a1b2c3d4...",
  "semantic_name": "monthly_sales_report",
  "tables": ["fact_sales", "dim_products"],
  "performance": {
    "avg_duration": 45.0,
    "p95_duration": 120.0,
    "scans": [
      {"table": "fact_sales", "rows": 50000000, "efficiency": "LOW (Ghost Scanner)"}
    ],
    "joins": [
      {"step": 3, "type": "hash", "spill": true, "anti_pattern": "AP-01"}
    ]
  },
  "recommendation": "High Priority: Fix Join on Step 3 (Disk Spill). Add Sort Key to 'fact_sales'."
}
```

### 4.2 The Retrieval Strategy (AI Prompt Integration)
When an analyst asks: *"How can I improve this query?"*
1.  **Fingerprint:** The AI fingerprints their new query.
2.  **Lookup:** Checks if this pattern (or similar table combos) exists in our Profile Index.
3.  **Response:**
    *   *Matched:* "This query pattern runs daily and spills to disk 50% of the time. Recommended fix: ..."
    *   *Unmatched:* "This is a new pattern, but it uses `fact_sales` which has a known 'Ghost Scan' risk on column `date`. Ensure `date` is indexed."

---

## Phase 5: Action Strategy (Execution)

### Priority 1: High-Leverage Mining (Days 1-2)
*   **Action:** Run updated `redshift_granular_mining.sql` for the last **3 days**.
*   **Target:** `microstrategysvc` (Automated Reports) and `svc_dbt_bi` (Pipeline).
*   **Output:** `performance_profiles_sample.json`.
*   **Validation:** Manually verified generic Anti-Patterns against known slow queries.

### Priority 2: Cataloging the "Worst Offenders" (Days 3-4)
*   **Action:** Filter the output for top 20 queries by `total_cpu_time` that flag an Anti-Pattern.
*   **Deliverable:** A "Hit List" of 20 scripts to rewrite immediately. This proves value.

### Priority 3: The "Analyst Tool" (Days 5+)
*   **Action:** Ingest the full 30-day history into the Knowledge Graph (or simple vector store).
*   **Deliverable:** An MCP Tool or Slash Command (`/check-performance`) that users can trigger.

---

## Next Steps for You (Immediate)

1.  **Direct:** I will update the `redshift_microstrategysvc_compute_stats_granular.sql` file to include `stl_scan` (for table names) and `aborted` flags.
2.  **Execute:** Run this for the last 3 days to get a sample dataset.
3.  **Analyze:** Process the sample to create the first batch of "Anti-Pattern Signatures" (verify if our definitions hold water).
