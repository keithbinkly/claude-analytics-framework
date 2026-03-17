# QA Standards

## No Row Counts

Never use row count comparisons as QA validation. Always use granular variance analysis (Template 1: dimension-level breakdown with variance percentage). Acceptance threshold for critical metrics: <0.1% variance.

Row count matching masks filter mismatches, calculation errors, and grain violations.

## Never Modify a Test to Pass

A failing test is evidence of a real problem. Before taking any action on a failing test, investigate the root cause. "Just make the test pass" is a rationalization that hides bugs — especially under time pressure.

## Test Per Layer

Add dbt tests layer-by-layer during model creation — not all at once after all models are built. When writing a staging model, immediately add PK tests and compile+run them before moving to intermediate. Errors at one layer must be fixed before building the next.

A staging PK violation propagates to all downstream models before being caught. Fix it at the source.

## Search Traces First

Before investigating any QA issue, variance, or test failure, search decision traces first: check `dbt-agent/shared/decision-traces/rules.json` for matching rules, then `dbt-agent/shared/decision-traces/traces.json` for similar past cases. Only start fresh investigation if no match is found.

## Define Grain Before Building

Before building any intermediate or mart model, explicitly define and document the grain (what makes each row unique). Never start building when grain is unclear. Aggregating up is easy; disaggregating down requires a full rebuild.

## Anti-Pattern Check

At session end, scan all modified SQL for: `NOT IN (subquery)` (4.18x slower), `OR` in JOIN (4.07x slower), deep nesting 3+ levels (3.06x slower), `SELECT *` (2.08x slower). Refactor before ending the session.
