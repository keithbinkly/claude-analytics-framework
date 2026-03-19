---
name: data-storytelling
description: |
  End-to-end workflow from business question to narrative data storytelling page. Chains
  the analyst ensemble, visualization spec design, chart comparison, critic review, semantic
  layer queries, and narrative page build into a single reproducible process. Use when asked
  to "tell the story of", "create a data story", "build a narrative page", "data narrative",
  "analysis to visualization", or "end-to-end analysis with charts".
---

# Data Storytelling Workflow

Business question in, narrative HTML page out. This skill chains analysis, visualization
design, and page building into a reproducible 12-step process.

**When to use:** After an `/analyze` run produces findings worth communicating — or when
starting fresh with a question that deserves a visual narrative, not just a text answer.

**Output:** A single-file HTML page with ECharts, narrative text, and insight callouts.

**Design system:** `resources/design-system.md` — CSS vars, color tokens, ECharts helpers, HTML structure.

**Shortcuts:**
- If findings already exist (from a prior `/analyze`), start at Step 3.
- If chart types already chosen, start at Step 9.
- Steps 5-8 can be skipped for fast-track delivery (quality drops).

---

## The 12-Step Process

```
 1. Question Framing ─────────────────────── Define the question + audience
 2. Ensemble Analysis (/analyze) ─────────── 4 analysts + critic + synthesis
 3. Story Architecture ───────────────────── Design narrative beats (CTR framework)
 3.5 Narrative Review ───────────────────── Verify story coherence before charting
 4. Findings Review ──────────────────────── Extract chartable claims (constrained by beats)
 5. VIZ Spec Design ──────────────────────── Map beats → chart specs (intent-driven)
 6. Comparison Page Build ────────────────── N×4 grid of chart alternatives
 7. Critic Review ────────────────────────── 3 themed critics evaluate
 8. Fix Application ──────────────────────── Apply P0/P1 critic fixes
 9. User Selection ───────────────────────── User picks 1 chart per VIZ
10. Semantic Layer Queries ───────────────── Query real data for each chart
11. Storytelling Page Build ──────────────── Narrative HTML with selections + data
12. Deploy & Review ──────────────────────── Mobile preview, iterate
```

---

## Step 1: Question Framing

Define the business question, audience, and narrative arc before touching any data.

**Narrative arc types:**

| Arc | Shape | Example |
|-----|-------|---------|
| Discovery | "We found X" | eWallet adoption landscape |
| Paradox | "X should cause Y, but doesn't" | High adoption + low approval |
| Comparison | "A vs B reveals Z" | Chip vs contactless approval |
| Journey | "X changed over time because Y" | Monthly eWallet growth |
| Gap | "Current vs possible" | Underperformance vs benchmark |

**Output:** 3-5 sentence brief: question, audience, arc, expected chart count.

---

## Step 2: Ensemble Analysis

Run `/analyze` with the framed question — dispatches 4 analysts, critic verifies, synthesizer produces consensus.

**Quality gate:** At least 3 findings with HIGH or MEDIUM confidence + metric evidence. If <3, reconsider scope.

---

## Step 3: Story Architecture

Dispatch the Story Architect agent (`read .claude/agents/story-architect.md`). Pass synthesis output + original question.

Read the `story_architecture` YAML output — it drives section ordering, headlines, and chart selection in Step 5.

### Step 3.5: Narrative Review

Dispatch the Narrative Reviewer (`read .claude/agents/narrative-reviewer.md`). Pass story architecture YAML.

| Verdict | Action |
|---|---|
| PASS | Proceed to Step 4 |
| REVISE | Send issues back to Story Architect. Max 2 revision rounds. |
| RESTRUCTURE | Re-run Step 3 from scratch with reviewer feedback. Max 1. Escalate to user if still fails. |

---

## Step 4: Findings Review

Extract chartable claims from synthesis. Each finding MUST map to a beat from the story architecture.

**Classify each finding:**
- **Chartable** — metric + dimension + comparison that benefits from visual encoding → assign VIZ-NN
- **Text-only** — better stated as a sentence (e.g., "100% contactless approval")
- **KPI-worthy** — single number for a KPI card, not a chart

**Target:** 6-10 VIZ specs. Fewer = too thin. More = reader fatigue.

**VIZ spec format:**
```
VIZ-[NN]: [Title]
Requirement: [What the chart must show]
Data shape: [N metrics, N categories, temporal?, reference values?]
Narrative role: [Which story beat this serves]
```

---

## Step 5: VIZ Spec Design

Map each VIZ spec to chart type candidates using the FT Visual Vocabulary.

**MANDATORY:** Read `shared/reference/dashboard-design-guidelines.md` and `.claude/skills/echarts/SKILL.md` first.

**Data relationship → chart type:**
- Comparison → bar, lollipop, dot plot
- Change over time → line, area, slope
- Part-to-whole → stacked bar, treemap, waffle
- Correlation → scatter, bubble
- Distribution → histogram, box plot
- Deviation → diverging bar, bullet chart
- Flow → sankey, waterfall

For each VIZ: select default + 3-4 genuine alternatives with trade-offs stated. Write to `docs/visualizations/[topic]-viz-alternatives.md`.

**Anti-patterns:**
- All alternatives are bar chart variations — push harder
- Alternative has no scenario where it genuinely beats the default
- No trade-off stated

---

## Step 6: Comparison Page Build

Create `docs/visualizations/[topic]-viz-comparison.html` with synthetic/representative data.
Layout: one row per VIZ spec, one column per alternative (A-E). Each cell 280×220px.
Design system: `resources/design-system.md`.

---

## Step 7: Critic Review

Launch 3 parallel critic agents against the comparison page:

1. **Encoding Accuracy** — right visual encoding? axes scaled? zero-baseline? misleading?
2. **Visual Design** — color/contrast/accessibility, typography, spacing, data-ink ratio
3. **Communication** — answers the business question in <5 seconds? labels sufficient?

Each critic cites specific VIZ-[NN] + Selection [X]. Rate: PASS / WARN / FAIL.

**Output:** Prioritized fix list: P0 (FAIL — must fix), P1 (WARN — should fix), P2 (nice to have).

**Deconfliction:** Encoding Accuracy > Visual Design > Communication. When critics conflict, favor the one aligned with design guidelines Section 1 (Purpose Before Pixels).

---

## Step 8: Fix Application

Apply P0 fixes first, then P1. Group by VIZ spec (touch each chart once). Skip P2 unless trivial.

---

## Step 9: User Selection

Present the comparison page. Walk through each VIZ: "For VIZ-01, which selection? A/B/C/D/E."

Record in a table:
```
| VIZ | Selection | Chart Type |
| 01  | A         | Horizontal Bar — Sorted |
```

Save selections via `/save`.

---

## Step 10: Semantic Layer Queries

**MANDATORY:** Load MCP tools first. Query certified metrics only — never fabricate data.

**MetricFlow dimension prefix pattern (CRITICAL):**
```
Simple metric on `merchant_auth_event` entity:
  ✅ merchant_auth_event__mcc_category
  ❌ mcc_category (will fail)

metric_time is always unprefixed:
  ✅ metric_time
  ❌ merchant_auth_event__metric_time (will fail)
```

**Discovery per chart:**
1. `mcp__dbt__list_metrics` → find metric name
2. `mcp__dbt__get_dimensions(metrics=[{name:"metric_name"}])` → list valid dimensions
3. `mcp__dbt__query_metrics(metrics, group_by, order_by, limit=500)`
4. Parse result → extract data arrays for ECharts

---

## Step 11: Storytelling Page Build

Create `docs/visualizations/[topic]-data-story.html`. HTML structure and ECharts config: `resources/design-system.md`.
**Labels and annotations:** Read `resources/annotation-and-labeling.md` before configuring any chart labels. Use the quick lookup table (chart type × density → strategy) and run the anti-pattern checklist (Section 6) before shipping.

Self-contained: no external dependencies except Google Fonts + ECharts CDN.

---

## Step 12: Deploy & Review

```bash
cp docs/visualizations/[topic]-data-story.html ~/Obsidian-Vault/ClaudeUpdates/
lsof -ti:8080 | xargs kill -9 2>/dev/null; sleep 1
cd ~/Obsidian-Vault/ClaudeUpdates && nohup python3 -m http.server 8080 > /dev/null 2>&1 &
# Tell user: http://192.168.1.56:8080/[topic]-data-story.html
```

Run `/save` to update workstream state.

---

## Quality Gates

| Step | Gate | Fail Action |
|------|------|-------------|
| 2 | ≥3 HIGH/MEDIUM confidence findings | Re-scope question or run follow-up |
| 5 | Each VIZ has ≥3 genuine alternatives | Push harder on alternatives |
| 7 | 0 FAIL ratings from critics | Fix before proceeding |
| 10 | All chart data from semantic layer | Flag missing metrics — don't fabricate |
| 11 | Page renders on mobile | Fix responsive issues |
| 12 | User approves final page | Iterate until approved |

---

## Artifacts Produced

| Step | Artifact | Location |
|------|----------|----------|
| 5 | Alternatives catalog | `docs/visualizations/[topic]-viz-alternatives.md` |
| 6 | Comparison page | `docs/visualizations/[topic]-viz-comparison.html` |
| 11 | Storytelling page | `docs/visualizations/[topic]-data-story.html` |

---

## Lessons Learned

1. **Entity-prefix dimensions in MetricFlow.** Always run `get_dimensions` first — don't guess.
2. **Synthetic data first, real data last.** Build comparison page (Step 6) with fake data. Only query semantic layer for final page (Step 10).
3. **Critics find real issues.** The deconfliction step is essential — critics sometimes contradict each other.
4. **Narrative > chart.** Section titles and insight callouts do more work than the chart itself.
5. **KPIs frame the tension.** Pick numbers that make the reader curious enough to scroll.
6. **The simultaneous-cliff pattern.** When all categories show simultaneous metric movement, it's a system-level change — check before attributing individual explanations.

---

## Resources

- `resources/design-system.md` — CSS vars, color tokens, typography, ECharts helpers, HTML templates
- `resources/annotation-and-labeling.md` — **Label decision system.** Chart type × density → label strategy, ECharts config, collision heuristics, anti-pattern checklist. Read Section 0 (quick lookup table) before writing any chart labels.
- `shared/reference/dashboard-design-guidelines.md` — Purpose Before Pixels, cognitive efficiency
- `.claude/skills/echarts/SKILL.md` — ECharts configuration patterns
- `.claude/skills/ai-analyst-ensemble/SKILL.md` — Ensemble for Step 2
- `.claude/skills/interactive-dashboard-builder/SKILL.md` — Chart type selection (FT Visual Vocabulary)
- `shared/knowledge-base/partners/INDEX.md` — Per-partner analytical briefs
