# Context Builder — Napkin

Corrections, anti-patterns, and MetricFlow gotchas. Updated as patterns emerge.

---

## Anti-Patterns

### MetricFlow Syntax Traps
- `type: derived` requires `metrics:` list with `offset_window` or `filter` — not raw SQL
- `cumulative` metrics need `window` OR `grain_to_date`, never both
- `period_over_period` uses `offset_window: 1` with `metric_time` dimension — don't use custom date dimensions
- Entity relationships: `type: foreign` on the many side, `type: primary` on the one side — not the other way around

### Orphan Definitions
**Problem:** Creating metrics that reference dimensions not defined in any semantic model.
**Fix:** Trace the full path: metric → measure → semantic model → entity → dimension. All must exist.

### Duplicate Metric Names
**Problem:** Same metric defined in multiple semantic models with slightly different logic.
**Fix:** Search existing definitions before creating. Use `dbt ls --resource-type metric` to check coverage.

### Business Context as Comments
**Problem:** Putting business logic explanations in SQL comments instead of YML descriptions.
**Fix:** Business context belongs in `description:` fields in YML. That's what the semantic layer surfaces.

### Schema Drift Blindness
**Problem:** Semantic model references a column that was renamed or removed in the source.
**Fix:** Run `dbt parse` after changes. Validate against actual warehouse schema.

## Patterns That Work

- **Dimension hierarchy in entity definitions**: product_stack → partner → sub_partner as entity relationships
- **Derived metrics for ratios**: Define components (numerator, denominator) as simple metrics, then compose
- **Analysis plans as YAML**: Structured analysis templates that reference certified metrics
- **Description inheritance**: Base descriptions in staging, enriched in intermediate, business-ready in mart
- **Semantic model per grain**: One semantic model per unique grain (daily transactions, monthly summaries, etc.)

---

## Additional Anti-Patterns (mined from production, Feb 2026)

### DEV Schema Staleness Mistaken for Metric Error
**Problem:** MetricFlow query returns zeros for recent dates. Agent spends time debugging metric definition, measure aggregation, and entity joins — all correct. Root cause: DEV schema is weeks behind PROD.
**Fix:** Check PROD schema first. Rule: if DEV returns zeros for dates within the last 30 days, assume staleness before assuming metric error.

### High-Cardinality Dimension in MetricFlow Query
**Problem:** `mf query --metrics gdv --group-by merchant_name` times out. Merchant name, account_uid, and other high-cardinality dimensions cannot be grouped via MetricFlow — the query planner generates an unbounded cross-join.
**Fix:** Use `dbt show --inline` for high-cardinality breakouts. MetricFlow is for low-cardinality dimensions: product, portfolio, brand, time_class. This is an architectural limit, not a fixable config.

### zsh BRACECCL Not Set — MetricFlow Template Syntax Fails
**Problem:** `mf query --metrics gdv --where "{{ ... }}"` fails with "no matches found" or similar glob error. macOS zsh interprets `{{ }}` as glob patterns.
**Fix:** Add `setopt BRACECCL` to `~/.zshrc` and reload shell before running mf commands. Verify with: `echo {a,b,c}` should output `a b c` not a glob error.

### Integer Division in Rate Metrics
**Problem:** `approval_rate = approved / total` returns 0 when both values are integers (integer division in SQL). MetricFlow ratio metrics inherit the SQL type of the underlying measures.
**Fix:** Cast numerator or denominator to DECIMAL before the ratio: `CAST(approved AS DECIMAL(18,4)) / NULLIF(total, 0)`. Always include NULLIF to prevent division-by-zero errors.

### UNION ALL Schema Mismatch with Upstream Deferral Enabled
**Problem:** After adding a column to one branch of a UNION ALL, dbt0301 errors persist even after fixing all branches. Root cause: upstream deferral (`upstream_prod_enabled: true`) causes `dbt show` to use PROD column schema instead of local schema.
**Fix:** Two-step: (1) add column to ALL branches, (2) temporarily set `upstream_prod_enabled: false` during validation. Re-enable after validating local schema.

### Dual dbt Environment — Running mf Against Fusion
**Problem:** `mf validate-configs` or `mf query` fails with confusing errors when run in the main Fusion environment. MetricFlow requires dbt Core.
**Fix:** Always run `source .venv/bin/activate` before any `mf` command. The `.venv` contains dbt Core with MetricFlow. Fusion and Core coexist — do not mix.

### Timestamp Non-Determinism in Event Selection
**Problem:** A query selecting the "latest" event per account returns different results across runs. Root cause: two events share identical microsecond timestamps; ORDER BY timestamp alone is non-deterministic.
**Fix:** Add surrogate/activity key as tiebreaker: `ORDER BY event_timestamp DESC, activity_key DESC`. Always include a deterministic tiebreaker column in any event-selection window function.

### Wrong Tier for Metric Type
**Problem:** Querying STOCK metrics (Net Ledger Balance, Active Account count at a specific date) from the Detail (event-level) tier. Point-in-time stock metrics require complex window logic that doesn't exist in the event stream.
**Fix:** STOCK metrics live in Gold tier only. FLOW metrics (GDV, Purchase, Revenue) can come from either tier. RATE metrics (GDV/Active) use Gold for reliable denominator counts. Consult the metric type map before querying.
