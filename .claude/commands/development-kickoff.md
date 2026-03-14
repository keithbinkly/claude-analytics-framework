# Development Kickoff

Full dbt development session initialization. Loads all relevant skills, checks active work, and gets you oriented for pipeline development.

Run this once at the start of a development session instead of relying on keyword-triggered skill loading.

---

## Skills Loaded

This command explicitly activates context for all dbt development skills:

- **dbt-orchestrator** — Workflow coordination, phase management
- **dbt-business-context** — Requirements capture, transcript parsing
- **dbt-standards** — Model placement, naming, canonical reuse
- **dbt-preflight** — Cost estimation, runtime thresholds
- **dbt-migration** — 4-phase pipeline migration implementation
- **dbt-qa** — QA templates 1-4, variance analysis, unit testing
- **dbt-lineage** — Dependency mapping, impact analysis
- **dbt-redshift-optimization** — DISTKEY/SORTKEY, anti-patterns
- **dbt-semantic-layer-developer** — MetricFlow, semantic models
- **dbt-data-discovery** — Source profiling, schema analysis
- **dbt-tech-spec-writer** — Architecture documents, formal specs
- **dbt-fundamentals** — Medallion architecture, materializations

---

## Steps

### 1. Load Quick-Reference Files

Read the mandatory pre-flight references:

```
repos/dbt-agent/shared/knowledge-base/migration-quick-reference.md
repos/dbt-agent/shared/knowledge-base/canonical-models-registry.md
repos/dbt-agent/shared/knowledge-base/folder-structure-and-naming.md
repos/dbt-agent/shared/reference/qa-validation-checklist.md
repos/dbt-agent/shared/reference/anti-pattern-impact.yml
repos/dbt-agent/shared/reference/baas-join-registry.yml
```

Confirm each loaded (do not paste contents — just confirm availability).

### 2. Check Active Handoffs

```bash
ls /Users/kbinkly/git-repos/dbt-agent/handoffs/*/PLAN.md 2>/dev/null
```

For each active plan, read the YAML frontmatter and current phase. Summarize:
- Pipeline name
- Current phase
- Last activity date
- Blockers (if any)

### 3. Check Open Dots

```bash
ls /Users/kbinkly/git-repos/dbt-agent/.dots/*.md
```

Filter for pipeline-related dots (tags containing "pipeline", "migration", "dbt"). Show status and priority.

### 4. Load Canonical Models Registry

Read `repos/dbt-agent/shared/knowledge-base/canonical-models-registry.md` and note:
- Total canonical models available
- Recently added models (if timestamped)
- Coverage gaps (domains without canonical models)

### 5. Check VPN State Context

Remind user:
- **VPN ON** → Can run `dbt compile`, `dbt run`, `dbt show`, warehouse queries via MCP
- **VPN OFF** → Planning, writing, skill development, SQL unit tests only

### 6. Present Orientation

```
## Development Kickoff — YYYY-MM-DD

### Skills Active
All 12 dbt skills loaded

### Quick Reference
[X/6] reference files loaded

### Active Pipelines
[list or "none — ready for new work"]

### Open Pipeline Dots
[list or "none"]

### VPN Reminder
[ON/OFF implications]

### What would you like to work on?
1. Resume [pipeline name] — currently in Phase X
2. Start new pipeline — run "new pipeline [name]"
3. QA/validation work
4. Other: [describe]
```

---

## When to Use

- Start of any dbt development session
- Switching from non-dbt work back to pipeline development
- After a long break from pipeline work
- When you want all skills available without remembering trigger keywords
