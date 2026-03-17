# analytics-workspace Team Fitness Assessment

**Author:** System Architect (domain agent)
**Date:** 2026-03-13
**Status:** Assessment complete. Actionable recommendations below.

**Purpose:** Determine whether analytics-workspace in its current state is ready for the team's dbt work — specifically sharing with teammates doing data science feature store and TPG pipelines.

---

## Verdict

**analytics-workspace is a useful shell, but needs significant retooling before it's team-ready.** The repo infrastructure (directory structure, gitignore, MCP config, symlink pattern) is sound. The agent architecture, commands, and skills are built for a different stack and workflow model. Keep the shell, replace the internals.

---

## What analytics-workspace Was Built For vs What We Need

| Dimension | analytics-workspace Today (Graniterock/Dylan) | What We Need |
|-----------|-------------------------------|--------------|
| **Data warehouse** | Snowflake | Redshift |
| **Cloud** | AWS (generic) + Azure planned | AWS (specific to our infra) |
| **Orchestration** | Orchestra, Prefect, dlthub | dbt Cloud jobs, MCP API |
| **BI tool** | Tableau | Semantic layer + custom HTML dashboards |
| **Agent model** | 9 roles + 15 specialists, confidence-based delegation | Two-tier: domain agents (Opus) + task agents (Sonnet) |
| **Workflow** | ADLC (idea → research → build → deploy → observe) | Pipeline lifecycle (requirements → discovery → architecture → implementation) |
| **Commands** | `/idea`, `/research`, `/build`, `/setup`, `/onboard` | `/pipeline-new`, `/pipeline-resume`, `/analyze`, `/explore-data` |
| **Skills** | 4 generic (project-setup, PR description, dbt scaffolder, doc validator) | 30+ specialized (migration, QA, preflight, semantic layer, data storytelling...) |

---

## What to Keep (Useful Shell)

### 1. Directory structure
The `knowledge/` hierarchy is well-designed for team contributions:
```
knowledge/
  platform/planning/     ← already in use (migration docs live here)
  domains/               ← natural landing zone for team domain knowledge
  reference/             ← cross-cutting reference material
```

### 2. `repos/` symlink pattern
Already has `.gitignore` excluding `repos/*` (except README.md) and documentation explaining the clone/symlink approach. Ready for Phase 1 cross-repo search.

### 3. MCP configuration
`.claude/settings.json` already has `dbt@dbt-agent-marketplace` enabled — same MCP server we use in dbt-agent. No reconfiguration needed.

### 4. Git infrastructure
`.gitignore` is well-structured. Branch protection rules documented. PR workflow documented.

### 5. Detection/analysis libraries
`libraries/detection/` contains anomaly detection, drift detection, quality scoring, and statistical testing utilities. Generic enough to be useful across any warehouse.

---

## What to Replace or Archive

### 1. Agent architecture (`.claude/agents/`)

**Current state:** 900-line README describing Role → Specialist hierarchy with confidence thresholds. 9 role agents (analytics-engineer, data-engineer, bi-developer, ui-ux-developer, data-architect, business-analyst, qa-engineer, dba, project-manager) + 15 specialists (aws-expert, snowflake-expert, tableau-expert, etc.)

**Problem:** This is a fundamentally different agent model. Our proven pattern uses domain agents (Builder, QA, Analyst, Designer) as Opus-class peers, not a role/specialist tree with confidence-based delegation.

**Recommendation:** Archive the existing agent definitions into `docs/archive/graniterock-agents/`. Create new agent definitions based on our two-tier model:
- Promote Builder, QA, Analyst agent specs from dbt-agent
- Add new domain agent specs for feature store and TPG work (team-contributed)

### 2. Commands (`.claude/commands/`)

**Current state:** ADLC-style commands: `/idea`, `/research`, `/build`, `/setup`, `/onboard`, `/start`, `/switch`, `/complete`, `/pause`, `/push`, `/pr`

**Problem:** None of these map to our pipeline lifecycle. `/build` is generic feature branching, not dbt pipeline construction. `/research` is GitHub issue analysis, not data discovery.

**Recommendation:** Archive existing commands. Phase 3 will promote pipeline lifecycle commands from dbt-agent. Add team-contributable command slots for feature store and TPG workflows.

### 3. Skills (`.claude/skills/`)

**Current state:** 4 implemented (project-setup, PR description, dbt-model-scaffolder, doc-validator) + 8 planned. All generic/Snowflake-oriented.

**Problem:** `dbt-model-scaffolder` generates Snowflake-style boilerplate. Other skills are too generic to be useful alongside our 30+ specialized skills.

**Recommendation:** Keep `documentation-validator` (potentially useful). Archive the rest. Skills slot is the primary landing zone for promoted dbt-agent skills in Phase 3.

### 4. CLAUDE.md

**Current state:** Snowflake/AWS setup wizard, ADLC workflow commands, three-layer architecture description, branch protection rules.

**Problem:** References `/idea`, `/setup`, `/onboard` commands. Describes Snowflake MCP setup. No mention of Redshift, pipeline lifecycle, QA standards, or preflight checks.

**Recommendation:** Rewrite to serve as the team's shared analytics control plane bootstrap. Reference promoted skills, pipeline commands, and agent specs. Keep MCP setup instructions (already correct for dbt Cloud).

---

## What to Add for Team Use

### 1. Team domain knowledge folders

```
knowledge/domains/
  dbt-pipelines/          ← promoted from dbt-agent (canonical models, patterns, QA)
  feature-store/          ← NEW: team-contributed by data science colleagues
  tpg-pipelines/          ← NEW: team-contributed by TPG pipeline builders
  semantic-layer/         ← promoted from dbt-agent
  data-storytelling/      ← promoted from dbt-agent/data-centered
```

Each domain folder should have:
- `README.md` — what this domain covers, who owns it
- `patterns/` — proven approaches, templates
- `reference/` — external docs, tool guides
- `decisions/` — why we do things this way

### 2. Contribution guide

Teammates need a clear path to add their knowledge without understanding the full migration architecture:

```
CONTRIBUTING.md (new)
  - How to add a domain folder
  - How to add reference material
  - How to request a new skill or command
  - What lives in analytics-workspace vs what lives in your project repo
```

### 3. Team onboarding context

For teammates encountering analytics-workspace for the first time:

```
knowledge/onboarding/
  what-is-analytics-workspace.md  ← 1-page explainer
  how-to-contribute.md    ← practical guide
  domain-index.md         ← what knowledge exists where
```

---

## Fitness Scorecard

| Criterion | Score | Notes |
|-----------|-------|-------|
| Directory structure | **8/10** | `knowledge/` hierarchy is good; needs `domains/` populated |
| Agent architecture | **2/10** | Wrong model entirely — needs full replacement |
| Commands | **2/10** | ADLC commands, not pipeline lifecycle |
| Skills | **3/10** | 4 generic skills vs our 30+ specialized |
| MCP/tooling | **9/10** | dbt Cloud MCP already configured correctly |
| Cross-repo search | **7/10** | Infrastructure ready, symlinks not yet created |
| Team contribution paths | **3/10** | No domain folders, no contribution guide |
| Documentation | **4/10** | Well-documented but for wrong stack |

**Overall: 4.7/10** — good bones, wrong internals.

---

## Recommended Sequence

1. **Phase 1 (now):** Create symlinks in `repos/`, archive Graniterock agent/skill/command files, create `knowledge/domains/` skeleton with README templates
2. **Phase 2:** Add contribution guide, rewrite CLAUDE.md for analytics team use
3. **Phase 3:** Promote highest-leverage dbt-agent assets (per decomposition inventory)
4. **Team invitation:** After Phase 2, teammates can start adding to `knowledge/domains/feature-store/` and `knowledge/domains/tpg-pipelines/` without needing to understand the full architecture

---

## Key Principle

**analytics-workspace earns authority by replacing capabilities, not by declaration.** No one should be told to "use analytics-workspace" until analytics-workspace can actually do something useful for them. The domain folders are the entry point — teammates contribute knowledge there. Pipeline lifecycle commands and QA skills come later through promotion.
