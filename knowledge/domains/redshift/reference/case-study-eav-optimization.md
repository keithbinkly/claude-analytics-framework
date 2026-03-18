# Case Study: Optimizing Repeated EAV Joins (GBOS Identity Validation)

## 1. The Discovery (Physical Mining)

Using the granular mining script, we identified a high-impact query executing on the Redshift cluster.

*   **Query ID:** `25292295`
*   **User:** `IAM:bramirez2@greendotcorp.com` (Ad-hoc analysis)
*   **Performance Signature:**
    *   **Execution Time:** 65.0 seconds
    *   **Rows Scanned:** ~270 Million (across multiple table touches)
    *   **Disk Spill:** 65 Blocks (Memory exhaustion)
    *   **Anti-Pattern:** **"The Multi-Pass EAV Join"**

### The "Before" Query Pattern
The query attempts to flatten a tall "Entity-Attribute-Value" (EAV) table (`identityvalidationrequestdetail`) by joining it repeatedly to the base table (`IdentityValidationRequest`) for every single attribute needed.

```sql
SELECT 
    ...
FROM gbos_vip.IdentityValidationRequest ivr
-- Pass 1: Get ProductTierKey
LEFT JOIN gbos_vip.identityvalidationrequestdetail ivrd_cip_pt 
    ON ivr.identityvalidationrequestkey = ivrd_cip_pt.identityvalidationrequestkey 
    AND ivrd_cip_pt.identityvalidationrequestattributename = 'ProductTierKey'
-- Pass 2: Get ProspectType
LEFT JOIN gbos_vip.identityvalidationrequestdetail pt 
    ON ivr.identityvalidationrequestkey = pt.identityvalidationrequestkey 
    AND pt.identityvalidationrequestattributename = 'ProspectType'
-- ... (Repeats for other attributes)
```

**Why this fails:**
Each `LEFT JOIN` forces the database engine to scan or seek into the massive Detail table separately. With 5 attributes, that's 5 lookups per Request row, or 5 full index scans if the optimizer gives up. The hash table for these joins grows large, spilling to disk.

---

## 2. The Solution (Aggregation Pivot)

We can replace **N joins** with **1 scan + Aggregation**. This is the standard "Pivot" pattern for EAV models.

### The "After" Recommendation

```sql
WITH pivoted_attributes AS (
    SELECT 
        identityvalidationrequestkey,
        -- Pivot logic: Scan once, bucket into columns
        MAX(CASE WHEN identityvalidationrequestattributename = 'ProductTierKey' 
            THEN identityvalidationrequestattributevalue END) as ProductTierKey,
        MAX(CASE WHEN identityvalidationrequestattributename = 'ProspectType' 
            THEN identityvalidationrequestattributevalue END) as ProspectType
    FROM gbos_vip.identityvalidationrequestdetail
    -- Optimization: Filter early only for what we need
    WHERE identityvalidationrequestattributename IN ('ProductTierKey', 'ProspectType')
    GROUP BY 1
)
SELECT 
    ...
FROM gbos_vip.IdentityValidationRequest ivr
LEFT JOIN pivoted_attributes pa 
    ON ivr.identityvalidationrequestkey = pa.identityvalidationrequestkey
-- Join to lookup tables (ProductTier) happens AFTER the pivot, on the clean result
LEFT JOIN gbos.producttier prdt 
    ON pa.ProductTierKey = prdt.producttierkey
```

### Expected Impact
*   **Scans:** Reduced from N (Attributes) to 1.
*   **Memory:** Aggregation uses less memory than holding multiple Hash Join tables.
*   **Speed:** Estimated 3x-5x performance improvement for ad-hoc queries like this.

---

## 3. Agent Execution Instructions (How to replicate)

### Prerequisite
You must have access to `dbt` and the `analyses/` folder in the `dbt-enterprise` repo.

### Step 1: Run the Miner
Execute the finding script to locate bad queries (high disk spill or long duration):
```bash
dbt show --inline "$(cat analyses/mining/find_bad_query.sql)" --limit 20
```
*   **Output:** Look for specific `query` IDs with `temp_blocks_to_disk > 0` or `scanned_table_ids` showing repetition.

### Step 2: Extract the Code
Once you have a Query ID (e.g., `12345`), fetch its text:
```bash
dbt show --inline "SELECT sequence, text FROM pg_catalog.stl_querytext WHERE query = 12345 ORDER BY sequence" --limit 100
```
*   *Note:* You may need to run this in chunks (sequence 0-20, 20-40) if the query is huge, as `dbt show` truncates output.

### Step 3: Identify the Anti-Pattern
Compare the code against the **Anti-Pattern Library** (see `GRANULAR_PERFORMANCE_MINING_PLAN.md`):
*   **Repeated Joins?** → EAV Anti-Pattern.
*   **`1=1` or `Cross Join`?** → Cartesian Bomb.
*   **`%LIKE%` on high volume?** → Ghost Scanner.

### Step 4: Propose the Fix
Draft the optimized SQL using standard patterns (like the Pivot CTE above) and present it to the user.

---

## 4. Deterministic vs. Probabilistic Nature

**Is this process deterministic?**
*   **Discovery (Deterministic):** The logs (`svl_query_metrics`) are immutable facts. If a query spilled 50 blocks yesterday, it will always show up in the logs as such. Any agent running the mining script will find the exact same "Bad Queries".
*   **Diagnosis (Probabilistic/Heuristic):** Identifying *why* it is bad requires pattern matching. An agent might misinterpret a "Cross Join" as intentional. However, checking against a strict "Anti-Pattern Library" (Scan Count > X, Join Count > Y) makes this highly deterministic.
*   **Optimization (Probabilistic):** Generative AI (like GPT-4/Claude) creates the rewritten SQL. The exact syntax (e.g., using `PIVOT` vs `MAX(CASE)`) might vary, but the *strategy* (reducing scans) remains constant based on the training data.

**Verdict:** The process is **90% Deterministic** if you follow the "Anti-Pattern Library" rules defined in this repo.
