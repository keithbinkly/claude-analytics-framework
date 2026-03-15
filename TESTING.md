# Migration Testing Guide

Test prompts to verify the AI Team Workspace works correctly. Run these from a **fresh Claude session** in the workspace root.

---

## 1. Orientation (Does Claude know where it is?)

### 1a. Basic orientation
```
What is this workspace and what repos does it coordinate?
```
**Look for:** Three-repo model (workspace = brain, dbt-enterprise = hands, dbt-agent = reference). Should NOT mention Snowflake, ADLC, Graniterock, or role/specialist agents.

### 1b. Routing knowledge
```
If I need to run dbt compile, where do I do that?
```
**Look for:** "dbt-enterprise" — not here. Should mention `cd` to dbt-enterprise.

### 1c. Skill awareness
```
What skills are available for pipeline work?
```
**Look for:** References the skill activation table in CLAUDE.md. Names specific skills (dbt-migration, dbt-qa, dbt-preflight, etc.).

---

## 2. Skill Loading (Do keywords trigger the right skill?)

### 2a. QA skill
```
I need to QA a dbt model — what's the methodology?
```
**Look for:** 4-template system, variance analysis (not row counts), <0.1% threshold, decision traces. Should read `.claude/skills/dbt-qa/SKILL.md`.

### 2b. Preflight skill
```
I'm about to run a model that joins 3 large tables. Is it safe?
```
**Look for:** Preflight checklist — upstream row counts, join risk assessment, runtime estimate, suggestion to sample first if large. Should reference the preflight skill.

### 2c. Redshift optimization
```
This query is slow on Redshift — how do I optimize it?
```
**Look for:** DISTKEY/SORTKEY advice, anti-pattern check (NOT IN → NOT EXISTS, OR in JOIN → UNION ALL), reference to `anti-pattern-impact.yml` with specific multipliers (4.18x, 4.07x).

### 2d. Semantic layer
```
I need to add a new metric to the semantic layer. What's our convention?
```
**Look for:** Loads semantic layer developer skill. Should mention MetricFlow, our dual installation (Fusion vs Core 1.10), and reference semantic layer domain knowledge.

### 2e. Data storytelling
```
I want to create a data story about approval rate trends. How do I start?
```
**Look for:** Loads data-storytelling skill. References the end-to-end workflow (ensemble → viz spec → chart → narrative page).

---

## 3. Domain Knowledge (Does Claude read our team files?)

### 3a. Canonical models
```
What canonical models exist for transaction data?
```
**Look for:** Reads `knowledge/domains/dbt-pipelines/reference/canonical-models-registry.md` and returns specific model names from our registry — not generic dbt advice.

### 3b. Anti-patterns with numbers
```
What are the top SQL anti-patterns to avoid?
```
**Look for:** Specific multipliers from our reference: NOT IN (4.18x), OR in JOIN (4.07x), deep nesting (3.06x), SELECT * (2.08x). Not generic "avoid SELECT *" advice.

### 3c. QA decision traces
```
Have we seen QA issues with incremental models before?
```
**Look for:** Reads `knowledge/domains/dbt-pipelines/decision-traces/rules.json` or `selected-traces.json` and returns specific past cases.

### 3d. Troubleshooting
```
I'm getting a "column not found" error after dbt compile succeeds. What's going on?
```
**Look for:** Reads troubleshooting reference. Should explain: compiled SQL ≠ materialized data, need `dbt run --full-refresh`, not more SQL edits. References the circuit breaker rule.

---

## 4. Pipeline Workflow (Do commands and routing work?)

### 4a. Pipeline status
```
/pipeline-status
```
**Look for:** Reads pipeline registry from `repos/dbt-agent/handoffs/PIPELINE_REGISTRY.yaml` (or explains how to find it). Should NOT error about missing files.

### 4b. Pipeline resume
```
/pipeline-resume disbursements
```
**Look for:** Attempts to load state from `repos/dbt-agent/handoffs/disbursements/PLAN.md`. Understands it needs to route execution to dbt-enterprise.

### 4c. Builder agent
```
/builder
```
**Look for:** Loads builder agent definition. References compile-before-run rule, canonical model scan, preflight checks. Should mention dbt-enterprise as execution target.

### 4d. QA agent
```
/qa
```
**Look for:** Loads QA agent. References 4-template methodology, decision traces, dual-mode execution (API vs CLI).

---

## 5. Cross-Repo Search (Do symlinks work?)

### 5a. Find a dbt model
```
Find all models related to "funds_movement" in our dbt project
```
**Look for:** Searches `repos/dbt-enterprise/` via symlink. Returns actual file paths from dbt-enterprise.

### 5b. Find dbt-agent reference
```
Where is the canonical models registry?
```
**Look for:** Finds it in BOTH `knowledge/domains/dbt-pipelines/reference/canonical-models-registry.md` (workspace copy) AND `repos/dbt-agent/shared/knowledge-base/canonical-models-registry.md` (original).

### 5c. Find across repos
```
Search all repos for references to "mart_disbursements"
```
**Look for:** Results from multiple repos via the `repos/` symlinks.

---

## 6. Analysis Workflow

### 6a. Analyst ensemble
```
/analyze What's driving the decline in ewallet approval rates for Amazon Flex?
```
**Look for:** Loads the multi-analyst ensemble skill. Dispatches analyst agents. Uses `execute_sql` via MCP for data queries.

### 6b. Explore data
```
/explore-data I want to understand the merchant_spend source tables
```
**Look for:** Loads data discovery skill. Systematic profiling approach (source inventory → schema → volume → filters → joins → cardinality).

---

## 7. Non-Claude Agent Compatibility

### 7a. Cursor/GPT orientation
Open the workspace in Cursor (or another AI tool). Ask:
```
Read AGENT_ENTRYPOINT.md and explain how this workspace is structured.
```
**Look for:** The non-Claude agent can understand the three-repo model, routing rules, and where to find workflow definitions — all from AGENT_ENTRYPOINT.md without needing Claude-specific features.

### 7b. Workflow navigation without slash commands
```
Read .claude/manifests/workflow-contracts.yaml and explain how to run QA on a dbt model.
```
**Look for:** The agent reads the machine-readable workflow contract and can navigate to the right files and repos.

---

## 8. Regression (Is dbt-agent still intact?)

Open a separate Claude session in `/Users/kbinkly/git-repos/dbt-agent`.

### 8a. Basic functionality
```
/pipeline-status
```
**Look for:** Works exactly as before. No errors about missing files.

### 8b. Skill loading
```
I need to QA a model
```
**Look for:** Loads dbt-qa skill from dbt-agent's own `.claude/skills/`, not from the workspace.

### 8c. File integrity
```bash
# Run manually in terminal
cd /Users/kbinkly/git-repos/dbt-agent
echo "Commands: $(ls .claude/commands/*.md | wc -l)"   # 24
echo "Agents: $(ls .claude/agents/*.md | wc -l)"       # 26
echo "Skills: $(ls -d .claude/skills/*/ | wc -l)"      # 45
echo "Rules: $(ls .claude/rules/*.md | wc -l)"         # 21
git diff --stat .claude/ shared/                        # Only pre-existing changes
```

---

## Automated Readiness Check

Run the quick script version:
```bash
cd /Users/kbinkly/git-repos/claude-analytics-framework
bash scripts/check-workspace-readiness.sh
```

---

## Scoring

| Category | Tests | Pass if |
|----------|-------|---------|
| Orientation (1a-1c) | 3 | Claude describes correct architecture, no Graniterock references |
| Skill loading (2a-2e) | 5 | Correct skill loads for each keyword category |
| Domain knowledge (3a-3d) | 4 | Answers grounded in team files, not generic LLM knowledge |
| Pipeline workflow (4a-4d) | 4 | Commands route correctly, agents load |
| Cross-repo search (5a-5c) | 3 | Finds files across repos via symlinks |
| Analysis (6a-6b) | 2 | Ensemble and exploration workflows initiate |
| Non-Claude compat (7a-7b) | 2 | Non-Claude agents can navigate |
| Regression (8a-8c) | 3 | dbt-agent works identically to before |
| **Total** | **26** | **All pass** |
