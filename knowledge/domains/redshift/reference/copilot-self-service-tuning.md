# Self-Service Query Tuning with GitHub Copilot

This repository contains a **Redshift Anti-Pattern Directory** and specific optimization rules derived from our mining of the `redshift_granular_mining` table. You can use GitHub Copilot to evaluate your own queries against this knowledge base.

## 🚀 How to Use

### 1. Setup
Ensure you have this repository (`dbt-agent`) open in your workspace, or explicitly reference the `docs/research/mining/ANTI_PATTERN_DIRECTORY.md` file in your chat context.

### 2. The Prompt
Open the SQL file you want to tune, then open the Copilot Chat panel and use a prompt like this:

> "@workspace Analyze the SQL in the active editor against the patterns defined in `docs/research/mining/ANTI_PATTERN_DIRECTORY.md`. Does it exhibit traits of 'The Disk Spiller' or 'The Skewed Worker'? Suggest a rewrite based on the guidelines in `optimization_gallery`."

### 3. What to Expect
Copilot will:
1.  **Scan your query** for structural hallmarks (e.g., `DISTINCT` on `CASE WHEN`, `OR` in `JOIN`).
2.  **Match against definitions**: It will cite "The Disk Spiller" if it sees massive intermediate row expansion.
3.  **Provide a Rewrite**: It will generate an optimized block (e.g., using a CTE for pre-aggregation) modeled after the examples in `docs/research/mining/optimization_gallery/`.

## 🛠️ Example Session

**User:**
"Is this query efficient?"
```sql
SELECT DISTINCT 
    CASE WHEN name LIKE '%Walmart%' THEN 'Walmart' ELSE name END 
FROM transactions
```

**Copilot:**
"No. This matches the **'Mega-Case Disk Spiller'** anti-pattern.
**Risk**: Computing strings before deduplication causes excessive memory usage.
**Fix**: Aggregate first, then transform.

**Optimized SQL:**
```sql
WITH grouped AS (
    SELECT name FROM transactions GROUP BY 1
)
SELECT CASE WHEN ... FROM grouped
...
```

## 📚 Reference Artifacts
- **[Anti-Pattern Directory](ANTI_PATTERN_DIRECTORY.md)**: The encyclopedia of "Bad SQL".
- **[Optimization Gallery](optimization_gallery/)**: Verified Before/After patterns.
