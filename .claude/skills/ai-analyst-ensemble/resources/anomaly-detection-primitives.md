# Anomaly Detection Primitives

Reusable statistical building blocks for any analyst. Use these to QUANTIFY
when something is "unusual" rather than relying on subjective judgment.

**Inspired by:** DAAF (2025) statistical primitives, SiriusBI data quality agent

## Available Primitives

### 1. Z-Score (Standard Score)

**Use when:** You want to say a value is "unusually high/low" compared to its peers or history.

**Formula:** `z = (value - mean) / stddev`

**SQL (via dbt show or cache query):**
```sql
SELECT
  dimension_col,
  metric_col,
  AVG(metric_col) OVER () AS mean_val,
  STDDEV(metric_col) OVER () AS stddev_val,
  (metric_col - AVG(metric_col) OVER ()) / NULLIF(STDDEV(metric_col) OVER (), 0) AS z_score
FROM cache_<table>
WHERE <filters>
```

**Interpretation:**
| |z| Range | Label | Meaning |
|---|---|---|
| < 1.0 | NORMAL | Within 1 standard deviation — not remarkable |
| 1.0 - 2.0 | NOTABLE | 1-2 standard deviations — worth mentioning |
| 2.0 - 3.0 | ANOMALOUS | 2-3 standard deviations — likely a real signal |
| > 3.0 | EXTREME | Beyond 3 standard deviations — investigate immediately |

**Rules:**
- NEVER say "anomalous" without a z-score or equivalent quantification
- When reporting z-scores, always state the comparison group (e.g., "z=2.3 vs. other partners in same MCC")
- Z-scores on <10 observations are unreliable — note this prominently
- For heavily skewed metrics (e.g., transaction amounts), use percentile rank instead

### 2. Percentile Rank

**Use when:** Data is skewed (not normally distributed) or you want a more intuitive measure.

**SQL:**
```sql
SELECT
  dimension_col,
  metric_col,
  PERCENT_RANK() OVER (ORDER BY metric_col) AS percentile_rank,
  NTILE(100) OVER (ORDER BY metric_col) AS percentile_bucket
FROM cache_<table>
WHERE <filters>
```

**Interpretation:**
| Percentile | Label | Meaning |
|---|---|---|
| 25th - 75th | MIDDLE | Interquartile range — typical |
| 5th - 25th or 75th - 95th | OUTER | Notable — at the edges |
| < 5th or > 95th | EXTREME | Top/bottom 5% — investigate |
| < 1st or > 99th | OUTLIER | Rare — almost certainly a real signal or data issue |

### 3. Moving Average + Deviation Band

**Use when:** Detecting trend breaks in time series data.

**SQL:**
```sql
SELECT
  metric_time,
  metric_col,
  AVG(metric_col) OVER (ORDER BY metric_time ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma_7,
  STDDEV(metric_col) OVER (ORDER BY metric_time ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS rolling_std,
  CASE
    WHEN ABS(metric_col - AVG(metric_col) OVER (ORDER BY metric_time ROWS BETWEEN 6 PRECEDING AND CURRENT ROW))
         > 2 * STDDEV(metric_col) OVER (ORDER BY metric_time ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
    THEN 'ANOMALOUS'
    ELSE 'NORMAL'
  END AS deviation_flag
FROM cache_<table>
WHERE <filters>
ORDER BY metric_time
```

**Rules:**
- Window size should be stated explicitly (7-day, 30-day, etc.)
- The first N-1 windows are unreliable — exclude from anomaly flagging
- Use 2σ bands by default, 3σ for noisy metrics

### 4. Period-over-Period Change Rate

**Use when:** Comparing successive periods (MoM, WoW, YoY).

**SQL:**
```sql
SELECT
  metric_time,
  metric_col,
  LAG(metric_col) OVER (ORDER BY metric_time) AS prev_period,
  (metric_col - LAG(metric_col) OVER (ORDER BY metric_time))
    / NULLIF(LAG(metric_col) OVER (ORDER BY metric_time), 0) * 100 AS pct_change,
  CASE
    WHEN ABS((metric_col - LAG(metric_col) OVER (ORDER BY metric_time))
      / NULLIF(LAG(metric_col) OVER (ORDER BY metric_time), 0)) > 0.20
    THEN 'LARGE_CHANGE'
    ELSE 'NORMAL'
  END AS change_flag
FROM cache_<table>
WHERE <filters>
ORDER BY metric_time
```

**Thresholds (default, adjustable per metric):**
| Change | Label |
|---|---|
| < 5% | STABLE |
| 5-20% | MODERATE |
| > 20% | LARGE_CHANGE |
| > 50% | INVESTIGATE |

### 5. Concentration Index (HHI)

**Use when:** Checking if a metric is excessively concentrated in one segment.

**SQL:**
```sql
WITH shares AS (
  SELECT
    dimension_col,
    metric_col,
    metric_col * 1.0 / SUM(metric_col) OVER () AS share
  FROM cache_<table>
  WHERE <filters>
)
SELECT
  *,
  POWER(share, 2) AS hhi_contribution,
  SUM(POWER(share, 2)) OVER () AS total_hhi
FROM shares
ORDER BY share DESC
```

**Interpretation:**
| HHI | Label | Meaning |
|---|---|---|
| < 0.15 | DIVERSIFIED | No single segment dominates |
| 0.15 - 0.25 | MODERATE | Some concentration — note it |
| > 0.25 | CONCENTRATED | Highly concentrated — major finding |

## How Analysts Should Use These

1. **In QUERY PLANs:** Reference which primitive you'll use
   ```
   QUERY PLAN [3]:
   - Intent: Identify anomalous partners by disbursement success rate
   - Primitive: Z-SCORE across partner dimension
   ```

2. **In findings:** Always include the quantification
   ```
   FINDING: Partner X has anomalously low success rate
   - Z-score: -2.7 vs. peer group of 8 partners in same MCC
   - Percentile: 3rd percentile
   - Label: ANOMALOUS (beyond 2σ)
   ```

3. **In evidence tables:** Add a column for the statistical label
   ```
   | Partner | Success Rate | Z-Score | Label |
   |---------|-------------|---------|-------|
   | X       | 72.1%       | -2.7    | ANOMALOUS |
   | Y       | 94.3%       | +0.8    | NORMAL |
   ```

## Adding New Primitives

To add a new primitive, append to this file with:
1. Name and "Use when" description
2. SQL template (using cache_<table> and <filters> placeholders)
3. Interpretation table with labeled thresholds
4. Rules for proper use
