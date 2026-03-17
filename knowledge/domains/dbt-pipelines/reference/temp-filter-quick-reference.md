# Temp Filter Management Quick Reference

## Problem
Temporary date filters added during development for "fast iteration" get forgotten, causing data suppression in production or QA.

**Example**: 7-day filter added Nov 6 for dev speed → Forgotten → Oct data shows 0 approvals → 60 min debugging

---

## Prevention (Use BEFORE Development)

### 1. Standardized Comment Pattern
```sql
-- ⚠️ TEMP_FILTER: [Reason] - Added [YYYY-MM-DD] by [initials]
-- ⚠️ TODO: REMOVE before [milestone]
and calendar_date >= dateadd('day', -7, current_date)
```

### 2. Pre-Commit Hook (One-time Setup)
```bash
# Install hook to warn before commits
cp tools/pre-commit-temp-filter-check.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

---

## Detection (Use BEFORE QA)

### Scan for Forgotten Filters
```bash
# Primary scan - finds documented temp filters
grep -r "TEMP_FILTER\|TODO: REMOVE" models/ --include="*.sql"

# Secondary scan - finds suspicious date filters
grep -rn "dateadd('day', -[7-9]\|dateadd('day', -[1-3][0-9]" models/intermediate/ --include="*.sql" \
  | grep -v "{% if is_incremental"  # Exclude valid incremental lookbacks
```

### Data Recency Test
```sql
-- Check for suspicious date gaps
SELECT 
    MIN(calendar_date) AS min_date,
    MAX(calendar_date) AS max_date,
    DATEDIFF('day', MIN(calendar_date), MAX(calendar_date)) + 1 AS expected_days,
    COUNT(DISTINCT calendar_date) AS actual_days,
    -- Flag if missing days (indicates filter)
    DATEDIFF('day', MIN(calendar_date), MAX(calendar_date)) + 1 - COUNT(DISTINCT calendar_date) AS missing_days
FROM your_model
WHERE calendar_date >= DATEADD('month', -6, CURRENT_DATE);
```

**Red Flag**: If `min_date` is exactly 7, 14, or 30 days ago = likely temp filter

---

## Remediation (Use AFTER Discovery)

### 1. Find the Model
```bash
# Search model and all upstream dependencies
dbt list --select +your_model --output name | \
  xargs -I {} find models -name "{}.sql" -exec grep -H "dateadd('day', -[0-9]" {} \;
```

### 2. Remove Filter
```sql
-- BEFORE
dim_date as (
    select * from {{ ref('stg_edw__dim_date') }}
    where {{ transactions_full_refresh_filter('calendar_date') }}
    and calendar_date >= dateadd('day', -7, current_date)  -- ⚠️ TEMP_FILTER
    {% if is_incremental() %}
    and calendar_date > (select max(calendar_date) - 3 from {{ this }})
    {% endif %}
)

-- AFTER
dim_date as (
    select * from {{ ref('stg_edw__dim_date') }}
    where {{ transactions_full_refresh_filter('calendar_date') }}
    {% if is_incremental() %}
    and calendar_date > (select max(calendar_date) - 3 from {{ this }})
    {% endif %}
)
```

### 3. Full Refresh Pipeline
```bash
# Must rebuild ALL downstream models to clear suppressed data
dbt run --select +fixed_model+ --full-refresh
```

### 4. Validate Fix
```sql
-- Verify historical data restored
SELECT 
    DATE_TRUNC('month', calendar_date) AS month,
    SUM(critical_metric) AS total
FROM your_model
GROUP BY 1
ORDER BY 1 DESC
LIMIT 12;  -- Should see 6+ months in dev environment
```

---

## Cost Analysis

| Scenario | Time Cost | Notes |
|----------|-----------|-------|
| **No prevention** | 45-90 min | 30-60 min debugging + 15-30 min pipeline refresh |
| **With pre-commit hook** | 5 sec | Instant warning during commit |
| **With pre-QA scan** | 10 sec | Quick grep before starting QA |
| **ROI** | **180-360x** | One-time 2 min setup saves hours per occurrence |

---

## Integration Points

### QA Checklist Integration
**Phase 3.2**: Mandatory temp filter scan before starting QA

**Phase 5.5**: Remove all temp filters before final sign-off

### dbt Project Config (Optional)
```yaml
# dbt_project.yml - Tag models with temp filters during dev
models:
  your_project:
    intermediate:
      temp_dev_models:
        +tags: ["temp_filter"]  # Remove tag when filters removed
```

Scan command:
```bash
grep -r "temp_filter" models/ --include="*.yml"
```

---

## References

- **Full Documentation**: `shared/knowledge-base/troubleshooting.md` → Temporary Development Filters
- **QA Workflow**: `shared/reference/qa-validation-checklist.md` → Phase 3.2
- **Pre-commit Hook**: `tools/pre-commit-temp-filter-check.sh`
- **Origin Session**: 2025-11-13 (Wealthfront semantic QA - Oct approval suppression)

---

**Last Updated**: 2025-11-13
