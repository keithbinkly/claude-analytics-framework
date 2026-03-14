<!--
source_of_truth: caf
mirrored_from: dbt-agent/shared/decision-traces/
-->

# Decision Traces

CAF-owned landing area for reusable QA and debugging decision traces.

## Current State

- CAF has promoted a curated `selected-traces.json` subset plus reusable `rules.json`.
- Active detailed traces still live in `dbt-agent/shared/decision-traces/`.
- CAF skills should treat those assets as fallback references until the trace migration slice lands.

## Migration Intent

Promote in stages:

1. Curated reusable rules
2. High-value recent traces
3. Full historical corpus if it remains useful and maintainable
