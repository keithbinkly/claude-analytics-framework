# /explore-data — Systematic Data Exploration

Sweeps a multi-dimensional dataset to discover baselines, trends, anomalies,
and drivers. Ranks findings by business impact. Produces visualization specs
for designer handoff via /data-story.

**Lighter than /analyze.** 4 steps, 2 agents, 10 constraints.
/analyze is hypothesis-driven (question -> evidence). This is discovery-driven (data -> stories).

---

## Step 0: Identify the Dataset

**What to explore:**
- If user specified a semantic model -> use those metrics
- If user specified a topic -> `mcp__dbt-mcp__list_metrics` to find relevant metrics
- If user said "explore everything" -> list metric families, suggest a starting point

**Scope confirmation:**
- Metrics: which metric family? (e.g., spend, disbursements, registrations)
- Time range: default trailing 12 months if unspecified
- Dimensions: all available (the Explorer sweeps them all)

Run `mcp__dbt-mcp__list_metrics` and `mcp__dbt-mcp__get_dimensions` to map the terrain.

---

## Step 1: Schema Discovery & Canvas

### 1a. Schema Discovery

Map the complete schema for selected metrics:

```
mcp__dbt-mcp__get_dimensions(metrics=[...])
```

Record:
- Exact metric names (as returned by list_metrics)
- All dimensions with entity prefixes (as returned by get_dimensions)
- Time dimension grain options

### 1b. Data-Puller Canvas

Read `.claude/agents/data-puller.md` for the full canvas protocol.

Dispatch the Data-Puller to pre-query ALL dimensions:

```
Task(
  subagent_type="general-purpose",
  prompt="You are the Data-Puller. Read your instructions at .claude/agents/data-puller.md.
         Execute the Canvas Protocol for these metrics: [metric list].
         Schema: [paste verified schema].
         Time range: [date range].
         Save results to /tmp/{topic}-exploration-data.md",
  description="Data-Puller canvas",
  model="sonnet"
)
```

Wait for canvas completion. Read `/tmp/{topic}-exploration-data.md` to verify
data was retrieved.

**Reality check:** These datasets are small (200-400 rows, 15-20KB text).
The canvas should capture everything.

### 1c. Source Tie-Out (Lightweight)

Run a quick source tie-out on the 2 most important metrics only:

```
Task(
  subagent_type="general-purpose",
  prompt="You are the Source Tie-Out agent. Read .claude/agents/source-tie-out.md.
         Canvas output is at: [canvas path].
         LIGHTWEIGHT MODE: Check only the top 2 metrics by volume.
         Run the tie-out protocol and report results.",
  description="Source tie-out (lightweight)",
  model="sonnet"
)
```

If FAIL: re-run canvas. If WARN: note the caveat for the Explorer.

---

## Step 2: Explorer Sweep

Read `.claude/agents/explorer-analyst.md` for the full sweep protocol.
Read `.claude/skills/explorer-ensemble/SKILL.md` for shared constraints.

Dispatch the Explorer:

```
Task(
  subagent_type="general-purpose",
  prompt="You are the Explorer Analyst. Read your instructions at
         .claude/agents/explorer-analyst.md.

         CANVAS DATA:
         [paste or reference /tmp/{topic}-exploration-data.md]

         SCHEMA:
         [paste verified schema with exact metric/dimension names]

         TOPIC: {topic description}
         DOMAIN: {business domain}
         TIME RANGE: {date range}

         Execute the full 6-phase Systematic Sweep Protocol.
         Output the exploration_report YAML at the end.",
  description="Explorer sweep"
)
```

**Note:** The Explorer has NO direct MCP access. It works only from the canvas data.
This is the same anti-hallucination architecture proven in /analyze (0 fabrications
across 4+ production runs since Upgrade #7).

---

## Step 3: Lightweight Verification

For the top 5 findings by impact tier:

1. **Dimension value check:** Does every cited dimension value appear in the canvas?
2. **Number check:** Does one key number per finding match the canvas data?
3. **Direction check:** If a trend is claimed, does the data show that direction?

If a finding fails:
- MINOR error (rounding, slight mismatch): annotate and keep
- MAJOR error (wrong direction, fabricated value): demote to LOW impact

This is lighter than /analyze's full Result-Checker. The canvas-only architecture
already prevents most fabrication — this is a safety net, not a gate.

---

## Step 4: Present Report

Output the Explorer's report. Two audiences:

### For the User: Readable Summary

```
## Exploration Report: {Topic}

**Dataset:** {metrics} | **Period:** {date range} | **Dimensions swept:** {N}

### CRITICAL

**F1: {Title}**
{2-3 sentence narrative with labeled data points}
Impact: {dollar/user estimate} | Confidence: {z-score or effect size}

### HIGH

**F2: {Title}**
...

### Stories (correlated findings)

**{Story title}** — connects F1, F3, F5
{How these findings relate}

### Gaps

- {What data would strengthen these findings}
```

### For the Designer: Viz Specs

```
## Designer Handoff

{N} visualization specs ready for /data-story.

### F1: {Title}
- Chart: {type}
- Data: x={dim}, y={metric}, series={dim}
- Insight: {1-sentence}
- Title: {active title}
- Notes: {emphasis guidance}

### F2: {Title}
...
```

---

## Integration with /data-story

To build a data story from Explorer findings:

```
/data-story
  -> Analyst voice uses Explorer's viz specs as starting point
  -> Narrator voice builds arc from Explorer's ranked findings
  -> Designer voice renders charts from Explorer's data mappings
```

The Explorer output replaces the Analyst's chart selection phase —
the designer can go straight to building.

---

## Configuration

| Parameter | Default | Override |
|-----------|---------|---------|
| Time range | 12 months | User-specified |
| Max findings | 15 | Adjust in prompt |
| Impact threshold | MEDIUM+ get viz specs | Lower to LOW for exhaustive |
| Drill-downs | Canvas only | Future: enable mid-sweep drills |

---

## Design Lineage

Adapted from /analyze (Phase 10, 8 upgrades). Carries forward:
- Anti-hallucination: canvas-only data access (Upgrade #7-8)
- Progressive anchoring: BASELINE->DEVIATION->CO-OCCURRENCE->MECHANISM (#16)
- Anomaly detection primitives: z-scores, percentiles, HHI, change rates (#21)
- Statistical significance pre-filter: prevents narrating noise (#14)
- Data-point labeling rules (persistent rule)
- Composition check: ecological fallacy prevention (Phase 9)

Drops /analyze's heavy machinery:
- 4 analyst personas -> 1 unified Explorer
- Critic + Integration Validator -> lightweight spot-check
- Partner writeback, failure library -> not Explorer's job
- SMART goals, decision framing -> Explorer discovers, doesn't decide
