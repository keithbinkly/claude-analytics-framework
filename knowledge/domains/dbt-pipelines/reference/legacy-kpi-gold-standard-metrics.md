<!--
source_of_truth: analytics-workspace
mirrored_from: dbt-agent/shared/knowledge-base/legacy-kpi-gold-standard-metrics.md
-->

> analytics-workspace migration note: this is a curated analytics-workspace copy of the certified KPI reference used for requirements framing and QA benchmarking. Use it from workspace root, then validate against the execution repo and certified source tables as needed.

# Legacy KPI Gold Standard Metrics

Certified metric reference for validating or framing new pipeline work against established KPI definitions.

## Why It Matters

This reference is useful because it captures:

- certified business metrics reviewed by Finance and Operations
- common benchmark products and time windows
- tolerance expectations for validation
- recurring edge cases that affect interpretation

## QA Validation Protocol

Use this reference when scoping or validating a new pipeline:

1. compare new-model outputs to the certified KPI source where applicable
2. test representative products
3. validate recent months plus a historical baseline
4. apply metric-specific tolerance thresholds

## Typical Tolerances

| Metric class | Suggested threshold |
|--------------|---------------------|
| financial metrics | `< 0.01%` variance |
| count metrics | `< 0.1%` variance |
| derived metrics | `< 1%` variance |

## Common Benchmark Metric Families

- active-user metrics
- monthly and annual active metrics
- transaction volume metrics
- transaction amount metrics
- account lifecycle metrics
- activation and funding metrics
- fee metrics
- direct deposit metrics
- tax refund metrics
- gross dollar volume

## Example Certified Metrics

- `30-Day Actives #`
- `90-Day Actives #`
- `Purchase #`
- `Purchase $`
- `ATM Withdrawal #`
- `New Accounts #`
- `Funded Activations #`
- `MMF #`
- `PRGB DD Ever #`
- `GDV $`

## Practical Usage

When using this reference in business-context or QA work, document:

- which metrics were benchmarked
- which products were used as samples
- which date range was tested
- what tolerance threshold applied
- whether any edge-case interpretation was required

## Known Interpretation Risks

- some metrics include blocked or suspended accounts
- signed vs positive-only amount conventions may differ
- seasonal metrics should be validated in the right period
- product-specific settlement timing can create expected timing differences
