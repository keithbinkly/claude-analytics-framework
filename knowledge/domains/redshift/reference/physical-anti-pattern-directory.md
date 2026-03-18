# Redshift Anti-Pattern Directory

This directory defines the "Performance Signatures" used to automatically detect inefficient queries in the Redshift environment. These rules are applied to the granular metrics captured in `analytics.microstrategysvc_compute_stats_granular` (sourced from `svl_query_metrics`).

---

## 🚫 AP-01: The Disk Spiller

**Signature:**
*   `temp_blocks_to_disk > 0`
*   Typically occurs in `hashjoin` or `sort` steps.

**Diagnosis:**
The query operation (Join or Sort) requires more memory than is allocated to the query slot. Redshift is forced to write intermediate results to disk (slow I/O), significantly degrading performance.

**Common Causes:**
1.  **Cartesian Products:** Joining without sufficient keys, creating massive intermediate result sets.
2.  **Wide Tables:** Selecting fewer columns (`SELECT *`) fills memory buffers faster.
3.  **Inefficient Joins:** Hash joining two very large unsorted tables.

**Recommendations:**
*   **Reduce Columns:** Select only necessary columns to reduce row width.
*   **Review Join Logic:** Ensure join keys are unique where expected (check for fan-out).
*   **WLM Tuning:** If valid, the query might simply need a larger slot (Engineer task).

---

## 🚫 AP-02: The Skewed Worker

**Signature:**
*   `cpu_skew > 0.95` OR `io_skew > 0.95`
*   Metric represents the ratio of difference between the busiest node and the average node.

**Diagnosis:**
One node/slice is doing significantly more work than others. Parallelism is broken. The query is only as fast as its slowest node.

**Common Causes:**
1.  **Poor Distribution Key:** The table is distributed by a low-cardinality column or a column with nulls (all nulls go to one slice).
2.  **Group By Skew:** Aggregating by a skewed value.
3.  **Broadcast Moves:** A large table is being broadcast to all nodes to join with a distributed table.

**Recommendations:**
*   **Check DISTKEY:** Ensure tables involved are distributed by a column with high cardinality and even distribution (e.g., `AccountKey` vs `Status`).
*   **Update Statistics:** Run `ANALYZE` to help the optimizer choose the right distribution style.

---

## 🚫 AP-03: The Ghost Scanner

**Signature:**
*   `scan_row_count > 10,000,000` (High Scan)
*   `return_row_count < 100` (Low Return)
*   *Note: In the granular script, we separate this via `step_label='scan'`.*

**Diagnosis:**
The database scans massive amounts of data but throws almost all of it away during filtering. Indices (Sort Keys) are missing or ineffective.

**Common Causes:**
1.  **Missing SORTKEY:** The column in the `WHERE` clause is not a Sort Key.
2.  **Functions on Columns:** `WHERE DATE_TRUNC('month', created_date) = ...` defeats the zone map.
3.  **Unsorted Data:** The table needs a `VACUUM`.

**Recommendations:**
*   **Add SORTKEY:** Add the frequently filtered column to the Sort Key.
*   **Remove Functions:** Rewrite filters to use raw column ranges (e.g., `created_date BETWEEN ...`).
*   **VACUUM:** Re-sort the physical storage.

---

## 🚫 AP-04: The Cartesian Bomb (Row Explosion)

**Signature:**
*   `join_row_count > (left_input_rows + right_input_rows) * 10`
*   *Proxy used in script: `row_count > 100M` in HashJoin.*

**Diagnosis:**
A join operation produces significantly more rows than existed in the inputs. This is usually unintended row duplication (fan-out).

**Common Causes:**
1.  **Many-to-Many Joins:** Joining on non-unique keys on both sides.
2.  **Missing Join Keys:** Forgetting a key in a composite key relationship.
3.  **Duplicate Data:** Source tables have duplicates.

**Recommendations:**
*   **Verify Grain:** Check `DISTINCT` counts on join keys.
*   **Aggregate First:** Aggregate (`GROUP BY`) the child table to the parent's grain *before* joining.

---

## 🚫 AP-05: The Serial Leader

**Signature:**
*   `step_label = 'aggr'` AND `cpu_time` is High
*   Query runs on the Leader Node (Single threaded).

**Diagnosis:**
Final aggregation or computation is happening on the Leader Node instead of Compute Nodes, creating a bottleneck.

**Common Causes:**
1.  **Complex String Aggregation:** `LISTAGG` can force leader processing.
2.  **Median/Percentiles:** Some window functions run on the leader.
3.  **Micro-Querying:** Too much logic in the final `SELECT` list.

**Recommendations:**
*   **Push Down:** Try to force aggregation on compute nodes using subqueries.
*   **Simplify:** Remove complex Leader-only functions if possible.

---

## Usage
These signatures are automatically detected by the `generate_performance_profiles.sql` analysis script.
