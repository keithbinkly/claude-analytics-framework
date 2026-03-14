# Discovery Before Building

## When Required

Before building models on any: unfamiliar source data, multi-stage pipeline (3+ stages), or migrated legacy script.

## The 6 Steps (Iron Rule: Complete All)

1. **Source inventory** — what tables exist, what do they contain
2. **Schema validation** — column types, nullability, expected vs actual
3. **Volume trace** — row counts per partition, growth patterns
4. **Filter distribution** — how filters affect row counts (the 99% suppression trap)
5. **Join success rate** — inner vs left join row differences
6. **Cardinality analysis** — unique key counts, fan-out risk

All six are required for every table you will build models on.

## Rationalizations That Lead to Skipping (Red Flags)

- "I don't have time" → Discovery takes 5 minutes. Debugging takes 90.
- "Standard patterns, I know this data" → The 99% suppression incident was on "standard" data.
- "I'll check if something looks wrong" → By then you've built 3 models on bad assumptions.

## The 99% Suppression Incident

7,149 events → 14 after filters. 90-minute diagnosis. Could have been caught in 5 minutes with proper data discovery.
