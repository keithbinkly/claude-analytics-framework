# Slash Commands Guide

Quick reference for all available `/commands`. Run any command by typing its name in Claude Code.

---

## Daily Workflow

| Command | When to Use | What It Does |
|---------|-------------|--------------|
| `/morning-review` | Start of day/session | Checks audit, inbox, dots, handoff action items, trigger queue. Recommends focus. |
| `/development-kickoff` | Starting pipeline work | Loads all 12 dbt skills + quick-reference files. Checks active handoffs and open dots. |

## Learning Loop

| Command | When to Use | What It Does |
|---------|-------------|--------------|
| `/learning-loop` | Weekly or on-demand | Runs full pipeline: task extraction → trigger suggestions → review queue → summary. |
| `/trigger-review` | When queue has pending items | Interactive review of suggested trigger phrases. Approve → updates SKILL.md. Reject → marks skipped. |
| `/synthesize-traces` | After 5+ new decision traces | Clusters similar traces into generalized rules. Promotes high-confidence patterns. |

## Pipeline Lifecycle (Deterministic Workflow Commands)

Structured commands for progressing through the 4-phase pipeline workflow. These eliminate NLP ambiguity — the agent always knows exactly what to do.

| Command | When to Use | What It Does |
|---------|-------------|--------------|
| `/pipeline-new [name]` | Starting a new pipeline | Creates PLAN.md, dot, registry entry. Loads Phase 1 skills. Begins work immediately. |
| `/pipeline-status [name?]` | Checking progress | Shows phase, gate status, artifacts, blockers. No name = all pipelines. |
| `/pipeline-gate [keyword]` | Approving a phase transition | Validates gate requirements, advances to next phase, loads next skills. Keywords: `requirements`, `discovery`, `architecture`, `deploy`. |
| `/pipeline-resume [name]` | Continuing from a previous session | Loads full context from PLAN.md, loads phase-appropriate skills, presents next action. |
| `/pipeline-close [name]` | Pipeline is done | Extracts learnings, updates registry, archives. |
| `/pipeline-docs [name] [type?]` | After pipeline or standalone | Generates docs from pipeline artifacts: diagrams, design docs, blog posts, PPTX, data product YAMLs. |

### Pipeline Lifecycle Sequence
```
/pipeline-new merchant-spend        → Creates pipeline, starts Phase 1
  (capture requirements...)
/pipeline-gate requirements         → Requirements approved → Phase 2
  (profile sources, analyze legacy...)
/pipeline-gate discovery            → Data findings approved → Phase 3
  (design architecture, write tech spec...)
/pipeline-gate architecture         → Tech spec approved → Phase 4
  (build models, run QA...)
/pipeline-gate deploy               → QA passed, ready for production
/pipeline-docs merchant-spend       → Generate diagrams, blog post, design doc, PPTX
/pipeline-close merchant-spend      → Extract learnings, archive
```

### Cross-Session Resume
```
(new session)
/pipeline-resume merchant-spend  → Loads full context, presents where we left off
```

### Documentation Types (via `/pipeline-docs`)
```
/pipeline-docs [name] diagram      → HTML architecture diagram with SVG flows
/pipeline-docs [name] design-doc   → Formal design document + Mermaid diagrams
/pipeline-docs [name] blog         → Polished blog post
/pipeline-docs [name] pptx         → PowerPoint deck for stakeholders
/pipeline-docs [name] data-product → Governance YAML for data product catalog
/pipeline-docs [name] all          → Generate everything
```

## Analysis Workflows

| Command | When to Use | What It Does |
|---------|-------------|--------------|
| `/analyze` | Business question | Multi-analyst ensemble (4 personas + critic + synthesizer). Writes findings back to partner docs. |
| `/explore-data` | Discovery | Sweeps a dataset systematically. Ranks findings by impact. Produces viz specs for /data-story. |
| `/analyst` | Analysis session | Loads Analytics Manager persona with full context. |

## Agent Personas

| Command | When to Use | What It Does |
|---------|-------------|--------------|
| `/builder` | Implementation work | Loads Builder agent with pipeline engineering memory. |
| `/qa` | Validation work | Loads QA agent with validation methodology memory. |
| `/context-builder` | Semantic layer work | Loads Context Builder with MetricFlow/ontology memory. |
| `/system-architect` | System evolution | Loads System Architect with architecture memory. |

## Pipeline Development (Utilities)

| Command | When to Use | What It Does |
|---------|-------------|--------------|
| `/development-kickoff` | Start of any dbt session | Loads all skills, references, canonical models. Shows active work. |
| `/check-join` | Writing JOIN logic | Validates join patterns against the BaaS join registry. |
| `/log_work_to_dots` | After completing work | Documents work with full context linking for cross-session continuity. |

## Documentation & Visualization

| Command | When to Use | What It Does |
|---------|-------------|--------------|
| `/visualize-plan` | After a plan is proposed | Transforms a plan into a polished HTML doc with Mermaid diagrams, color-coded phases, and infographic layout. |

---

## Workstream Management

| Command | When to Use | What It Does |
|---------|-------------|--------------|
| `/load [name?]` | Start of session | Loads workstream or pipeline context. Shows picker if no name given. |
| `/save [name?]` | End of session | Saves current progress to workstream YAML. Captures session GUID. |

---

## Recommended Sequences

### Morning Startup
```
/morning-review          → See what needs attention
/load                    → Pick workstream or pipeline to resume
```

### New Pipeline Work
```
/pipeline-new [name]     → Creates infrastructure + starts Phase 1
  (complete phase work)
/pipeline-gate           → Auto-detects pending gate, approves
  (repeat until done)
/pipeline-close [name]   → Extract learnings, archive
```

### Analysis Work
```
/analyst                 → Load Analytics Manager context
/analyze [question]      → Run multi-analyst ensemble
/explore-data            → Discovery sweep of a dataset
```

### End of Session
```
/save                    → Save workstream state
/log_work_to_dots        → Capture what was done (if not using /save)
```

### Weekly Maintenance
```
/learning-loop           → Run extraction pipeline
/trigger-review          → Approve/reject queued suggestions
/synthesize-traces       → Consolidate decision traces
```

---

## How Commands Work

Each command is a markdown file in this directory (`.claude/commands/`). Claude Code reads the file as a prompt and follows the workflow steps inside.

To create a new command: add a `.md` file here with a `# Title`, workflow steps, and any bash commands to run.

---

## Automation (Cron)

The daily system audit runs automatically at 8 AM weekdays via crontab:
- Extracts session metrics
- Checks skill underutilization
- Generates trigger suggestions
- Filters suggestions into review queue
- Scans handoffs for unresolved action items

Results land in `dbt-agent/data/inbox/system-evolution.md` — surfaced by `/morning-review`.

If no audit ran today (machine was asleep at 8 AM), run manually:
```bash
/Users/kbinkly/git-dbt-agent/tools/analysis/session_metrics_cron.sh system-audit
```
