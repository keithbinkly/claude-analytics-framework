# Analytics Manager — Napkin

Corrections, anti-patterns, and common analysis failures.

---

## Anti-Patterns

### Raw SQL Against Base Tables
**Problem:** Answering stakeholder questions with ad-hoc SQL instead of certified semantic-layer metrics.
**Fix:** Use the semantic layer only. If the metric does not exist, say so and log the gap.

### Including Today In Batch Data
**Problem:** Reporting a partial day as if it were complete.
**Fix:** End date defaults to yesterday unless the user explicitly wants partial-day data.

### Unequal Time Windows
**Problem:** Comparing a partial current period to a full prior period.
**Fix:** Use apples-to-apples windows such as Dec 1-14 vs Nov 1-14.

### Skipping Query Approval
**Problem:** Running a wide or ambiguous analysis before confirming the exact metrics, dimensions, and date range.
**Fix:** Present the plan first, then wait for approval.

### Hiding Source Environment
**Problem:** Presenting results without stating whether they came from PROD or DEV.
**Fix:** Always disclose the source environment in the answer.

### Filling Metric Gaps With Narrative
**Problem:** Pretending a question was answered when the certified metric does not actually exist.
**Fix:** Be explicit about missing coverage and route the gap to Context Builder.

## Patterns That Work

- Semantic-layer-only answers
- Partner-context-first interpretation
- Direct answer first, then evidence, then insights
- Explicit source disclosure in every analysis
- Clear statement of metric gaps when coverage is incomplete
# Analytics Manager — Napkin

Corrections, anti-patterns, and analysis mistakes. Updated as patterns emerge.

---

## Anti-Patterns

### Raw SQL on Base Tables
**Problem:** Writing `SELECT SUM(amount) FROM table` instead of using certified metrics.
**Fix:** ONLY use semantic layer queries. If the metric doesn't exist, report the gap — don't work around it.

### Including Today's Date
**Problem:** Querying data that includes today. Batch-loaded data means today is always incomplete.
**Fix:** End date = yesterday. Always. No exceptions.

### Mismatched Comparison Periods
**Problem:** Comparing Dec 1-14 vs all of November (14 days vs 30 days).
**Fix:** Same length periods. Dec 1-14 vs Nov 1-14. Or full Dec vs full Nov (both complete months only).

### Running Queries Without Approval
**Problem:** Executing queries before the user confirms scope, date range, and metrics.
**Fix:** Present the query plan. Wait for explicit OK. The user may want different parameters.

### Not Disclosing Data Source
**Problem:** Showing results without saying whether they came from PROD or DEV.
**Fix:** Always disclose. "Querying PROD data" or "Querying DEV — production values may differ."

### Fabricating When Metrics Don't Exist
**Problem:** Attempting manual calculations when a certified metric isn't available.
**Fix:** Say "I don't have a certified metric for [X]." List alternatives. Flag gap for Context Builder.

### Aggregate-to-Subgroup Fallacy (2026-02-18)
**Problem:** Observing an aggregate trend (avg txn/cardholder dropped while cardholder base grew) and attributing it to subgroup composition ("new cardholders are less active") without subgroup data.
**Fix:** Never attribute aggregate trends to subgroup behavior without disaggregated data. "Average activity dropped" ≠ "new users are less active." Could be: behavior change across all users, seasonal effects, methodology changes (e.g., processor migration). State what the data SHOWS, not what it MIGHT mean.
**Real example:** Scatter plot showed txn/cardholder decreasing over time as bases grew. Claimed "new cardholders are less active than incumbents" — but had zero cohort-level data to distinguish new vs tenured cardholder behavior. The leftward drift was likely the Oct 2025 processor migration resetting the baseline, not a composition effect.

### Causal Language From Observational Data
**Problem:** Using causal language ("driven by", "caused by", "due to") when the data only shows correlation or co-occurrence.
**Fix:** Use precise language that matches the evidence level:
- **Data shows**: "X and Y move together" / "X coincides with Y" / "X correlates with Y"
- **NOT**: "X drives Y" / "X caused Y" / "Y is due to X"
- If you want to claim causation, state what additional data or analysis would be needed to establish it.

### Over-Narration of Charts
**Problem:** Adding narrative elements to chart titles/callouts that sound insightful but go beyond what the visualization actually shows. Makes the dashboard sound smarter than the evidence supports.
**Fix:** Chart titles and callouts should describe what IS VISIBLE in the chart, not what you INFER from it. "Decline rate gap persists at 18pp" (observable) vs "New cohorts drag down portfolio quality" (inference requiring cohort data).

### Generic/Banal Insights (2026-02-18)
**Problem:** LLMs default to consensus patterns from training data, producing "insights" that any human would already know. Examples: "Price is a factor in decisions", "Spend varies by partner", "Users value reliability." These waste stakeholder attention and erode trust.
**Fix:** Apply the actionability test: "If a business manager reads this, what would they do differently?" If the answer is nothing, it's not an insight — it's background knowledge. Every finding must connect to a concrete action or decision. Generic truths don't survive this filter.
**Source:** Caitlin Sullivan — "How to Do AI Analysis You Can Actually Trust" (Lenny's Newsletter)

### Unverified Data Citations (2026-02-18)
**Problem:** Citing numbers in findings that don't trace to any query result. LLMs generate statistically plausible numbers that feel correct. Sometimes happens via rounding, memory, or hallucination during narrative writing.
**Fix:** Every number in a finding must trace to a specific query result (tool + result). After writing findings, verify each data point: VERIFIED (in output), PARAPHRASED (derived with shown calculation), or NOT FOUND (delete it). If you can't point to the query result, the number doesn't exist.
**Source:** Caitlin Sullivan's "quote verification" pattern adapted for data analysis

## Patterns That Work

- **Multi-analyst ensemble** for complex questions: 4 perspectives catch blind spots (4.28/5.0 validation)
- **PROD-first, DEV-fallback**: Always try MCP production connection first
- **Partner-specific context loading**: Different partners care about different metrics and vocabulary
- **Direct answer → details → insights** presentation order: Lead with the answer, then support it
- **Metric gap tracking**: Every "I can't answer this" becomes a tracked gap for Context Builder

### Upstream Drill-Down for Generic Categories (2026-03-14)
**Pattern:** When a semantic layer dimension contains a high-pct generic category (e.g., "Declined" at 44.7%), the semantic layer answer is incomplete. Drill into the upstream pipeline stages to find the granular codes that got rolled up.
**Workflow:**
1. Identify the generic bucket via semantic layer (`query_metrics` with dimension grouping)
2. Find the upstream intermediate model that has the raw codes (`execute_sql` + `information_schema.columns`)
3. Query the raw codes within that bucket (e.g., `network_association_response_code` for ISO 8583)
4. Cross-reference with dimensional cuts (destination bank, time, etc.) for concentration analysis
5. Write findings back into the data story with both the semantic-layer shares AND the cracked-open detail
**Key insight:** This is a valid exception to "certified metrics only" — you're not _replacing_ the semantic layer answer, you're _enriching_ it by explaining what's inside a generic rollup. The semantic layer tells you the bucket is 44.7%; the upstream tells you 61% of that is fraud flags from two neobanks.
**Real example:** Samsung "Declined" (69,793 txns) → ISO 8583 code 59 (suspected fraud, 42,950) concentrated at Bancorp (51%) + Stride (16%). June spike was 31K code-59 alone. Without this drill-down, the data story just said "generic declines are falling" — unhelpful. With it: "neobank fraud flags were the root cause and have been 97.6% resolved."
