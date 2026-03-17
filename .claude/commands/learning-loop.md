# Learning Loop

Run the full system evolution audit — same as the weekday 8am cron job.
Use this as a manual fallback when the cron doesn't fire (weekends, laptop asleep, etc.).

---

## Steps

### 1. Scorecard Metrics

Extract session metrics and generate report:

```bash
cd /Users/kbinkly/git-repos/analytics-workspace/dbt-agent && .venv/bin/python3 tools/analysis/session_metrics_extractor.py extract-all --since 2025-12-01 2>/dev/null || echo "(session extractor not available)"
```

```bash
cd /Users/kbinkly/git-repos/analytics-workspace/dbt-agent && .venv/bin/python3 tools/analysis/session_metrics_extractor.py report 2>/dev/null || echo "(report not available)"
```

Report: summary of session metrics.

### 2. Skill Underutilization

Analyze which skills should have been invoked but weren't:

```bash
cd /Users/kbinkly/git-repos/analytics-workspace/dbt-agent && .venv/bin/python3 -m tools.chatops.skill_underutilization 2>/dev/null || echo "(underutilization check not available)"
```

Report: missed invocation count, top underutilized skills.

### 3. Trigger Suggestions

Generate trigger suggestions from underutilization data, queue for review, and scan handoffs:

```bash
cd /Users/kbinkly/git-repos/analytics-workspace/dbt-agent && .venv/bin/python3 -m tools.chatops.trigger_suggester
```

```bash
cd /Users/kbinkly/git-repos/analytics-workspace/dbt-agent && .venv/bin/python3 -m tools.chatops.trigger_review_writer
```

```bash
cd /Users/kbinkly/git-repos/analytics-workspace/dbt-agent && .venv/bin/python3 -m tools.chatops.handoff_action_scanner 2>/dev/null || echo "(handoff scanner not available)"
```

Report: total suggestions, high-confidence count, items queued.

### 4. Runtime Telemetry

Check runtime performance of recent sessions:

```bash
cd /Users/kbinkly/git-repos/analytics-workspace/dbt-agent && .venv/bin/python3 -m tools.runtime.telemetry --last 100 2>/dev/null || echo "(no runtime telemetry)"
```

Report: any performance anomalies.

### 5. Knowledge Graph Health

Check KG integrity:

```bash
cd /Users/kbinkly/git-repos/analytics-workspace/dbt-agent && .venv/bin/python3 -m tools.kg.agent_integration health 2>/dev/null || echo "(KG health check not available)"
```

Report: node/edge counts, any issues.

### 6. Skill Wiring Validation

Validate all skills are properly wired:

```bash
cd /Users/kbinkly/git-repos/analytics-workspace/dbt-agent && .venv/bin/python3 tools/validate_wiring.py 2>/dev/null || echo "(wiring check not available)"
```

Report: any broken wiring.

### 7. Distilled Learnings

Show the current state of distilled learnings and check for pending reviews:

```bash
cd /Users/kbinkly/git-repos/analytics-workspace/dbt-agent && .venv/bin/python3 -m tools.chatops.learning_retrieval --summary
```

Check importance scoring stats on the current experience store:

```bash
cd /Users/kbinkly/git-repos/analytics-workspace/dbt-agent && .venv/bin/python3 -m tools.chatops.importance_scorer 2>/dev/null || echo "(importance scorer not available)"
```

Check distillation staging queue:

```bash
cd /Users/kbinkly/git-repos/analytics-workspace/dbt-agent && .venv/bin/python3 -m tools.chatops.distillation_staging --stats 2>/dev/null || echo "(staging not available)"
```

If unprocessed > 0, show them:

```bash
cd /Users/kbinkly/git-repos/analytics-workspace/dbt-agent && .venv/bin/python3 -m tools.chatops.distillation_staging --show 2>/dev/null
```

**Distillation**: If there are unprocessed candidates, distill them into structured learnings:
1. Read each candidate's description, evidence, tags, and context
2. Determine the learning type: `error_fix`, `domain_knowledge`, `investigation_shortcut`, `user_preference`, or `gotcha`
3. For each, write a structured entry to the appropriate `dbt-agent/shared/learnings/cross-cutting/{domain}.yaml` file
4. Follow the existing format (see `dbt-agent/shared/learnings/cross-cutting/dbt-qa.yaml` for reference)
5. After distilling, mark candidates as processed:
```bash
cd /Users/kbinkly/git-repos/analytics-workspace/dbt-agent && .venv/bin/python3 -m tools.chatops.distillation_staging --clear-processed
```

Check for any pending learnings awaiting review:

```bash
ls /Users/kbinkly/git-repos/analytics-workspace/dbt-agent/shared/learnings/pending/*.yaml 2>/dev/null | wc -l
```

If pending > 0, list them:

```bash
ls /Users/kbinkly/git-repos/analytics-workspace/dbt-agent/shared/learnings/pending/
```

Report: total distilled learnings, importance filter stats, staging queue stats, pending review count.

### 7.5 Curator Gate

Check which learnings have been applied and whether they improved outcomes:

```bash
cd /Users/kbinkly/git-repos/analytics-workspace/dbt-agent && .venv/bin/python3 -m tools.chatops.learning_tracker --stats 2>/dev/null || echo "(tracker not available)"
```

```bash
cd /Users/kbinkly/git-repos/analytics-workspace/dbt-agent && .venv/bin/python3 -m tools.chatops.learning_tracker --curate 2>/dev/null || echo "(not enough data for curation)"
```

Report: learnings applied, sessions tracked, curator verdicts (positive/negative/inconclusive).

If any learnings show NEGATIVE verdict (error recurred despite learning, or metrics below baseline):
- Flag for review — may need to be refined or rolled back
- Do NOT auto-remove — present to user for decision

### 8. Queue Summary

Read the current state of the trigger review queue:

```bash
cat dbt-agent/.dots/dbt-agent-trigger-review-queue.md
```

Count:
- `- [ ]` = pending
- `- [x]` = applied
- `- [~]` = rejected

### 9. Record KPI Trend + Save Audit

Record today's aggregate KPIs to the trend file and save the audit:

```bash
cd /Users/kbinkly/git-repos/analytics-workspace/dbt-agent && .venv/bin/python3 tools/analysis/record_kpis.py
```

Report: KPI snapshot recorded (or "already recorded today").

Save the audit output to the standard location:

```bash
cat > /Users/kbinkly/git-repos/analytics-workspace/dbt-agent/data/telemetry/audits/system-audit-$(date +%Y-%m-%d).md << 'AUDIT_EOF'
[paste the full audit output from steps 1-8 above]
AUDIT_EOF
```

Trend data: `dbt-agent/data/telemetry/kpi_trend.json`
Audit file: `dbt-agent/data/telemetry/audits/system-audit-YYYY-MM-DD.md`

### 10. System Improvement Recommendations

If you identified potential system improvements during the audit (new tools needed, workflow
changes, automation opportunities), list them here as **recommendations only**:

```
#### Recommendations for System Architect

| # | Recommendation | Confidence | Rationale |
|---|---------------|------------|-----------|
| 1 | [description] | high/med/low | [why] |
```

**IMPORTANT:** Do NOT implement these yourself. Do NOT create new scripts, modify commands,
or change automation. The System Architect (/system-architect) evaluates recommendations
and routes approved items to implementation agents.

### 11. Offer Next Step

If distillation candidates > 0:
> "There are N candidates staged for distillation. They were processed in step 7 above."

If pending learnings > 0:
> "There are N distilled learnings ready for review in dbt-agent/shared/learnings/pending/."

If pending trigger items > 0:
> "There are N trigger suggestions ready for review. Run `/trigger-review` to approve or reject them."

If recommendations > 0:
> "There are N system improvement recommendations. Run `/system-architect` to evaluate them."

If all == 0:
> "Learning loop is up to date. No pending reviews."

---

## Output Format

```
## System Evolution Audit (Manual)

### 1. Scorecard Metrics
[summary or "not available"]

### 2. Skill Underutilization
[missed invocations summary]

### 3. Trigger Suggestions
- Suggestions: X total, Y high-confidence
- Review Queue: X new items queued

### 4. Runtime Telemetry
[summary or "no data"]

### 5. Knowledge Graph Health
[node/edge counts or "not available"]

### 6. Skill Wiring
[pass/fail summary]

### 7. Distilled Learnings
- Total: X across Y domain files
- Importance filter: X% noise filtered, Y distillation candidates
- Staging queue: X unprocessed, Y processed
- Distilled this run: N new learnings (or "none staged")
- Pending review: N

### 8. Queue State
- Pending: X
- Applied: Y
- Rejected: Z

### 9. KPI Trend
- Recorded: [date]
- Trend file: dbt-agent/data/telemetry/kpi_trend.json

### Next Step
-> [recommendation]
```
