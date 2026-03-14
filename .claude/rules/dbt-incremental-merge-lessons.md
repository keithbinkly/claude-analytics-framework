# dbt Incremental Strategy: merge vs delete+insert on Redshift

## Key Lesson (2026-03-04)

**Problem:** `incremental_strategy='merge'` with composite unique keys (10-16 columns) on Redshift causes **per-row amount inflation** at month boundaries — NOT row duplication.

**Mechanism:**
- The lookback window re-processes rows at date boundaries
- Merge key with many columns doesn't always find exact matches
- Creates new aggregation rows with additive amounts on the same date
- Row counts stay normal but `SUM(amt)/COUNT(*)` per row is 10-27x inflated

**Diagnosis:**
```sql
-- If avg_per_row is 10x+ normal on specific dates, it's merge overlap
SELECT calendar_date,
  COUNT(*) as rows,
  SUM(attempt_amt) as total,
  ROUND(SUM(attempt_amt) / COUNT(*), 2) as avg_per_row
FROM model
GROUP BY 1
ORDER BY avg_per_row DESC
```

**Fix:** `incremental_strategy='delete+insert'` with `unique_key='calendar_date'`
- Cleanly wipes and replaces each date's rows
- No composite key matching issues
- Much cheaper on Redshift (no hash join for merge)

## CI with Schema Changes

When adding new columns to incremental models:
- `on_schema_change='sync_all_columns'` handles it automatically
- CI does incremental run → ALTER TABLE ADD COLUMN → new columns populated for lookback window only
- Historical rows get NULL for new columns (acceptable for CI)
- Full refresh on prod after merge to populate all historical rows

## UNION ALL + Denominator Mismatch

When a model UNIONs approved + declined transactions:
- `total_ewallet_amt` from both sides = ALL tokenized (approved + declined)
- `approve_amt` = approved only
- Ratio of `total_ewallet / approve_amt` can exceed 100% — this is NOT an error
- Use `total_ewallet / attempt_amt` for correct percentage
- Or add split columns (`approved_ewallet_amt`, `declined_ewallet_amt`) to separate by approval status
