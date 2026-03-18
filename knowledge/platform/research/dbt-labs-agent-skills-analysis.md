# dbt Labs Official Agent Skills vs Ours
*2026-01-31 | Private test group access*

**Repo:** `dbt-labs/dbt-agent-skills` (8 skills, superpowers framework)

---

## Their 8 Skills

| Skill                                           | Purpose                                          |
| ----------------------------------------------- | ------------------------------------------------ |
| `using-dbt-for-analytics-engineering`           | Core dbt work — models, tests, debugging         |
| `building-dbt-semantic-layer`                   | Semantic models — **uses new 1.12+ YAML spec**   |
| `adding-dbt-unit-test`                          | dbt native YAML unit tests                       |
| `answering-natural-language-questions-with-dbt` | Business question -> metric query routing        |
| `configuring-dbt-mcp-server`                    | MCP setup for Claude Desktop/Code/Cursor/VS Code |
| `fetching-dbt-docs`                             | `.md` URL trick for LLM-friendly doc fetching    |
| `migrating-dbt-core-to-fusion`                  | Core -> Fusion migration with dbt-autofix        |
| `troubleshooting-dbt-job-errors`                | dbt Cloud job failure diagnosis                  |

---

## What They Have That We Don't

### 1. Eval Framework (HIGH value)
KB note: we should try this out, and we should also figure out how we can test our qa agent performance against that ADE bench. Maybe we could blow the leaderboard out of the water? We really should do that 
`skill-eval` CLI for A/B testing skills:
- Define scenarios (prompt + context + expected behavior)
- Run with/without skills, compare outcomes
- Auto-grade with Claude
- HTML transcript review
- We have **nothing comparable** for measuring skill effectiveness

### 2. New 1.12+ Semantic Layer Spec (HIGH)
Metrics defined at column level, not separate `semantic_models:` block:
```yaml
models:
  - name: orders
    semantic_model:
      enabled: true
    columns:
      - name: order_id
        entity:
          type: primary
      - name: amount
        metrics:
          - type: simple
            name: total_revenue
            agg: sum
```
We're on 1.10 so correctly using legacy format, but need migration path.

### 3. `fetching-dbt-docs` Pattern (MEDIUM)
- Append `.md` to any `docs.getdbt.com` URL = clean markdown
- `llms.txt` index at `docs.getdbt.com/llms.txt`
- Simple bash search script for `llms-full.txt`

### 4. "Rationalizations That Mean STOP" (MEDIUM)
Prompt engineering pattern in their troubleshooting + AE skills:
| You're Thinking... | Reality |
|---|---|
| "Just make the test pass" | The test is telling you something is wrong |
| "It's probably just a flaky test" | "Flaky" means there's an issue. Find it. |
| "User explicitly asked for a new model" | Users request out of habit. Ask why. |

### 5. NL Question Routing (MEDIUM)
4-tier fallback: Semantic Layer -> Compiled SQL mod -> Model discovery -> Manifest analysis. More structured than our `ai-analyst-profile`.

### 6. superpowers Framework (MEDIUM)
- `skills-ref validate` CLI for skill structure validation
- Claude Code `.claude-plugin` marketplace distribution
- TDD-based skill creation methodology

---

## What We Have That They Don't

### The Big Gaps in Their System

| Our Capability | Their Status |
|---------------|-------------|
| **36 specialized skills** (vs 8) | Generic, not enterprise-specific |
| **Trigger-based auto-activation** | Manual skill loading only |
| **Cross-session memory** (PostgreSQL) | Completely stateless |
| **Decision traces** (case-based reasoning) | No institutional memory |
| **Ontological grounding** on metrics | Zero semantic guardrails |
| **Redshift-specific patterns** | Warehouse-agnostic |
| **4-agent pipeline workflow** with gates | Single-skill, no orchestration |
| **Pre-flight cost estimation** | Nothing comparable |
| **Controlled vocabulary enforcement** | Mentioned in best practices, not enforced |
| **Python SQL unit testing** (pytest+DuckDB) | Only dbt native YAML unit tests |
| **QA templates 1-4** (<0.1% variance) | Just "validate" |
| **Handoff system** for session continuity | No concept of this |
| **Hook infrastructure** | Skills are static documents |

---

## Key Architectural Differences

| Aspect       | dbt Labs                 | Ours                          |
| ------------ | ------------------------ | ----------------------------- |
| Framework    | superpowers marketplace  | Custom triggers + hooks       |
| Testing      | `skill-eval` A/B testing | Manual + decision traces      |
| Scope        | Generic (any warehouse)  | Enterprise BaaS i(Redshift)   |
| Skills       | 8                        | 36+                           |
| Activation   | Manual                   | Auto-trigger on keywords      |
| Memory       | None                     | PostgreSQL + experience store |
| Spec version | 1.12+ (bleeding edge)    | 1.10 (production)             |

---

## Top 3 to Adopt From Theirs

1. **Eval framework** -- Build `skill-eval` equivalent to A/B test whether our skills improve outcomes. Our trigger_suggester suggests but doesn't measure.

2. **`docs.getdbt.com/*.md` pattern** -- Simple, free, better than WebFetch. Add as utility.

3. **"Rationalizations" guardrail tables** -- Replicate in QA and migration skills. Prevents common agent shortcuts.

---

## Top 3 They Should Adopt From Ours

1. **Ontological grounding** -- Their semantic layer skill has no guidance on valid/invalid dimensions per metric. Agents will produce nonsense queries.

2. **Cross-session memory** -- Every session starts blank. Our experience store + recall is a generation ahead.

3. **Trigger-based activation** -- Right skill loads automatically. They rely on manual loading. 
4. 

> KB NOTE: “automatically” is completely theoretical. My experience has been that they do not load automatically, I need to call/invoke them. I have no evidence that a skilll has ever loaded automatically in fact. That’s why I’ve created slash commands to just intentionally invoke them 


---

## Session Context

This analysis came from the disbursements semantic layer implementation session. I built 30 metrics across 3 files, then you asked me to verify against the dbt spec -- which caught a `grain_to_date` vs `window` bug. That led to updating our skill with pitfall documentation, which led to this comparison.

The fix and the pitfalls section are now baked into `dbt-semantic-layer-developer/SKILL.md` so future sessions auto-load the rules.
