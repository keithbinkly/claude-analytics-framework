# Pipeline Documentation Generator

Generate communication-ready documentation from pipeline artifacts. Turns raw handoff files into diagrams, blog posts, presentations, and design documents.

**Usage:**
- `/pipeline-docs [name]` — generate docs for a specific pipeline
- `/pipeline-docs [name] [type]` — generate a specific doc type

---

## Document Types

| Type | Skill Used | Output | Audience |
|------|-----------|--------|----------|
| `diagram` | architecture-diagram-creator | HTML with SVG flow diagrams | Stakeholders, onboarding |
| `design-doc` | design-document-writer | Markdown design doc + Mermaid | Architecture review, Confluence |
| `blog` | blog-post-writer | Polished blog post | data-centered.com, external |
| `pptx` | pptx-powerpoint-generator | PowerPoint deck | Leadership, cross-team |
| `data-product` | synq-data-product-architect | data-product.yml | Data governance catalog |
| `all` | All of the above | Multiple artifacts | Full documentation package |

---

## Steps

### 1. Identify Pipeline

Pipeline name from argument: `$ARGUMENTS` (first word)

If no pipeline specified, list completed or active pipelines from `repos/dbt-agent/handoffs/PIPELINE_REGISTRY.yaml`.

### 2. Load Pipeline Artifacts

Read ALL existing artifacts for the pipeline (these are the source material):

```bash
ls /Users/kbinkly/git-repos/dbt-agent/handoffs/$PIPELINE_NAME/
```

Expected sources:
- `business-context.md` — metrics, acceptance criteria, stakeholder context
- `data-discovery-report.md` — source tables, schema, volume, risks
- `tech-spec.md` — model inventory, transformations, architecture decisions
- `qa-report.md` — variance results, test results, performance

Also check for:
- Pipeline dot (`repos/dbt-agent/.dots/pipeline-$PIPELINE_NAME.md`) — status, gate history
- Any models created (search for the pipeline's model files in dbt-enterprise)

### 3. Route to Requested Document Type

If specific type requested (second argument), generate just that one.
If no type or "all", present menu:

```
## Pipeline Documentation: [NAME]

Available artifacts to generate from:
- [x] Business Context (Phase 1)
- [x] Data Discovery Report (Phase 2)
- [x] Tech Spec (Phase 3)
- [x] QA Report (Phase 4)

### What would you like to generate?

1. **Architecture Diagram** — Interactive HTML with data flow, model layers, business context
2. **Design Document** — Formal spec with Mermaid diagrams, suitable for Confluence
3. **Blog Post** — "How we migrated [pipeline]" narrative for data-centered.com
4. **Presentation** — PowerPoint deck summarizing the pipeline
5. **Data Product Definition** — Governance YAML for the data product catalog
6. **All of the above**

Pick one or more (comma-separated), or type 'all':
```

### 4. Generate Documents

#### Architecture Diagram (`diagram`)

Load skill: `architecture-diagram-creator`

Source from: ALL pipeline artifacts

The diagram should include:
- **Business context section** — from business-context.md (metrics, stakeholders)
- **Data flow section** — from data-discovery-report.md (sources → staging → intermediate → marts)
- **Model inventory** — from tech-spec.md (all models with layers, dependencies)
- **Quality metrics** — from qa-report.md (variance, test pass rate)

Output to: `repos/dbt-agent/handoffs/$PIPELINE_NAME/docs/architecture-diagram.html`

---

#### Design Document (`design-doc`)

Load skill: `design-document-writer`

Source from: tech-spec.md (primary), business-context.md (context), data-discovery-report.md (data)

The design doc should follow the skill's format:
- Problem statement (from business-context.md)
- Technical approach (from tech-spec.md)
- Mermaid diagrams (generated from model inventory + data flow)
- Trade-offs and decisions (from tech-spec.md architecture decisions)
- Testing strategy (from qa-report.md)

Output to: `repos/dbt-agent/handoffs/$PIPELINE_NAME/docs/design-document.md`

---

#### Blog Post (`blog`)

Load skill: `blog-post-writer`

Source from: ALL pipeline artifacts + pipeline dot (for timeline)

The blog post should:
- Lead with the problem (from business-context.md)
- Show the process (phases, gate approvals, key decisions)
- Include specific metrics (from qa-report.md: variance, reuse %, build time)
- Be in Keith's voice (problem-first, specific metrics, honest about limitations)
- Target: data-centered.com

Output to: `repos/dbt-agent/handoffs/$PIPELINE_NAME/docs/blog-post.md`

---

#### Presentation (`pptx`)

Load skill: `pptx-powerpoint-generator`

Source from: ALL pipeline artifacts

Suggested slide structure:
1. Title: "[Pipeline Name] Migration"
2. Problem/Context (from business-context.md)
3. Data Landscape (from data-discovery-report.md)
4. Architecture (from tech-spec.md — model diagram)
5. Results (from qa-report.md — variance, tests, performance)
6. Learnings / Next Steps

Output to: `repos/dbt-agent/handoffs/$PIPELINE_NAME/docs/pipeline-overview.pptx`

---

#### Data Product Definition (`data-product`)

Load skill: `synq-data-product-architect`

Source from: tech-spec.md (models, ownership), business-context.md (stakeholders)

Generate YAML definition with:
- Product name, description, owner
- Models included (from tech-spec model inventory)
- Quality contracts (from qa-report.md test definitions)
- SLA targets (from performance metrics)
- Priority classification (P1-P4)

Output to: `repos/dbt-agent/handoffs/$PIPELINE_NAME/docs/data-product.yml`

---

### 5. Present Results

```
## Documentation Generated: [NAME]

| Document | Path | Status |
|----------|------|--------|
| Architecture Diagram | repos/dbt-agent/handoffs/[name]/docs/architecture-diagram.html | Created |
| Design Document | repos/dbt-agent/handoffs/[name]/docs/design-document.md | Created |
| Blog Post | repos/dbt-agent/handoffs/[name]/docs/blog-post.md | Created |
| Presentation | repos/dbt-agent/handoffs/[name]/docs/pipeline-overview.pptx | Created |
| Data Product | repos/dbt-agent/handoffs/[name]/docs/data-product.yml | Created |

### Next Actions
- Review and edit blog post for data-centered.com
- Serve diagram: `python3 -m http.server 8080` in docs/ directory
- Upload presentation to SharePoint/Google Drive
```

---

## Standalone Use (No Pipeline)

This command can also generate docs from ad-hoc content:

```
/pipeline-docs --standalone diagram
```

In standalone mode, ask the user what to document and use the relevant skill directly.

---

## Schema Documentation (Phase 4 Integration)

During Phase 4 implementation, the `dbt-standards` skill should automatically generate `schema.yml` for every model built. This is NOT a post-pipeline task — it happens during model creation.

Ensure Phase 4 model building includes:
1. Write .sql model
2. Write schema.yml with model description + column descriptions
3. Run `dbt compile` to validate

The `dbt-standards` skill Section 3 ("Schema Documentation") has the templates.
