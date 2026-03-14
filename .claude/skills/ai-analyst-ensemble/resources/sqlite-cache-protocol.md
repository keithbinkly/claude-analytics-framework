# SQLite Query Cache Protocol

Analysts should query the warehouse ONCE per metric/dimension/grain combination, then
iterate on the cached results locally. This prevents redundant warehouse queries and
enables sub-ms iteration on data exploration.

**Inspired by:** Datasette pattern (Simon Willison), DAAF (2025) data caching layer

## How It Works

### Phase 1: Warm the Cache (Step 3.5 of /analyze)

After the VERIFIED SCHEMA is available (Step 2.5), execute a set of broad "canvas queries"
that pull the core data analysts will need. These are intentionally wide — they pull more
data than any single analyst needs, because the cost of one broad query is much less than
the cost of 4 analysts each making 6-10 narrow queries.

**Canvas query strategy:**
```
For each metric group relevant to the user's question:
  1. Query at the finest useful grain (usually DAY) with ALL relevant dimensions
  2. Use a generous time window (the question's scope + 1 month buffer on each side)
  3. Store the result
```

Example for disbursements analysis:
```python
# Canvas query: all disbursement metrics × all dimensions × daily grain
result = query_metrics(
    metrics=["total_disbursement_amount", "disbursement_count", "disbursement_success_rate"],
    group_by=[
        {"name": "metric_time", "grain": "DAY", "type": "time_dimension"},
        {"name": "disbursement_daily_metrics__partner_name", "type": "dimension", "grain": null},
        {"name": "disbursement_daily_metrics__disbursement_type", "type": "dimension", "grain": null}
    ],
    order_by=[{"name": "metric_time", "descending": false}]
)
```

### Phase 2: Write to SQLite

Use `dbt show` with a SQL query that writes results to a local SQLite database.
Alternatively, use Python via Bash to create and populate the cache:

```bash
python3 -c "
import sqlite3, json, sys

# Data comes from stdin as JSON
data = json.load(sys.stdin)

conn = sqlite3.connect('/tmp/analyst_cache.db')
cursor = conn.cursor()

# Create table from first row's keys
if data:
    cols = list(data[0].keys())
    col_defs = ', '.join(f'\"{c}\" TEXT' for c in cols)
    cursor.execute(f'CREATE TABLE IF NOT EXISTS cache ({col_defs})')

    # Insert all rows
    placeholders = ', '.join('?' * len(cols))
    for row in data:
        cursor.execute(f'INSERT INTO cache VALUES ({placeholders})',
                       [str(row.get(c, '')) for c in cols])

conn.commit()
conn.close()
print(f'Cached {len(data)} rows to /tmp/analyst_cache.db')
"
```

### Phase 3: Analysts Query the Cache

Analysts use `dbt show` with SQL against the cache instead of `query_metrics` for follow-up
queries. The first query still goes to the warehouse (via query_metrics), but subsequent
slicing/filtering/aggregation happens locally.

**When to use the cache:**
- Follow-up queries that filter or re-aggregate data you already have
- Cross-sectional comparisons (different dimensions on the same metric)
- Time window adjustments (zooming in on a period within your original pull)

**When to go to the warehouse:**
- Querying a metric not in the cache
- Querying a dimension not in the cache
- Querying at a finer grain than the cache has

## Integration with QUERY PLAN

The QUERY PLAN (constraint #20) should note whether the query can be served from cache:

```
QUERY PLAN [N]:
- Intent: [...]
- Source: CACHE | WAREHOUSE  ← NEW field
- Metrics: [...]
- ...
```

If Source is CACHE: use a SQL query against /tmp/analyst_cache.db
If Source is WAREHOUSE: use query_metrics (and consider adding result to cache)

## Rules

- Cache lives at `/tmp/analyst_cache.db` for the duration of the /analyze session
- Cache is ephemeral — deleted after analysis completes
- Maximum cache size: 100K rows (if a canvas query returns more, apply a LIMIT)
- Cache table names: `cache_<metric_group>` (e.g., `cache_disbursements`, `cache_approvals`)
- Always verify cache freshness against the warehouse if results seem stale
