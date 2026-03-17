# Visualize Plan

Transform a plan, spec, or proposal into a polished HTML document with Mermaid diagrams, color-coded sections, and infographic-style layout.

---

## Step 0: Activate Skills (MANDATORY — do this first)

Read these SKILL.md files to load their patterns, templates, and color systems:

```bash
cat .claude/skills/architecture-diagram-creator/SKILL.md
cat .claude/skills/design-document-writer/SKILL.md
```

If the plan is dbt-related (pipelines, models, migrations), also load:
```bash
cat .claude/skills/dbt-tech-spec-writer/SKILL.md
```

These skills provide: HTML structure patterns, SVG diagram generation via `tools/mermaid/render-svg.mjs`, semantic color palette, section templates, and design document structure.

---

## Arguments

- **Source**: A plan file path, dot file, clipboard paste, or "the plan from this conversation"
- **Output**: Defaults to `docs/research/[plan-name]-visual.html`

---

## Workflow

### Step 1: Identify the Source Plan

Ask the user if not obvious:
- File path (e.g., `dbt-agent/.dots/some-plan.md`, `dbt-agent/handoffs/pipeline/PLAN.md`)
- Pasted text in conversation
- "The plan we just discussed"

Read the full source. Extract:
- **Title** and purpose
- **Phases / steps** (numbered or sequential)
- **Components** (systems, models, tools, agents involved)
- **Data flows** (inputs → processing → outputs)
- **Decisions** (choices made, alternatives considered)
- **Dependencies** (what blocks what)
- **Risks / considerations**

### Step 2: Design the Diagrams

Generate Mermaid diagrams using `tools/mermaid/render-svg.mjs` with themed SVGs.

**Required diagrams** (generate at least 2-3):

1. **High-level flow** (always):
```bash
node tools/mermaid/render-svg.mjs --theme tokyo-night -o /tmp/plan-flow.svg 'graph LR
  A[Phase 1] --> B[Phase 2]
  B --> C[Phase 3]'
```

2. **Component architecture** (if system/technical plan):
```bash
node tools/mermaid/render-svg.mjs --theme catppuccin-mocha -o /tmp/plan-arch.svg 'graph TD
  subgraph Input
    A[Source 1]
    B[Source 2]
  end
  subgraph Processing
    C[Transform]
  end
  subgraph Output
    D[Result]
  end
  A --> C
  B --> C
  C --> D'
```

3. **Sequence / timeline** (if multi-agent or phased):
```bash
node tools/mermaid/render-svg.mjs --theme github-dark -o /tmp/plan-sequence.svg 'sequenceDiagram
  Actor->>System: Request
  System->>Worker: Process
  Worker-->>System: Result
  System-->>Actor: Response'
```

4. **Decision tree** (if plan has branching logic):
```bash
node tools/mermaid/render-svg.mjs --theme nord -o /tmp/plan-decisions.svg 'graph TD
  A{Decision?}
  A -->|Yes| B[Path A]
  A -->|No| C[Path B]'
```

**Available themes**: `tokyo-night`, `catppuccin-mocha`, `github-dark`, `nord`, `dracula`, `one-dark`, `solarized-dark`

**Full syntax**: Read `tools/mermaid/CHEATSHEET.md` for node shapes, edge styles, subgraphs.

### Step 3: Build the HTML Document

Create a single self-contained HTML file. Inline the SVG diagrams directly.

**Color palette** (semantic):
- `#4299e1` — data / inputs (blue)
- `#ed8936` — processing / transforms (orange)
- `#9f7aea` — AI / agents / decisions (purple)
- `#48bb78` — success / outputs / done (green)
- `#fc8181` — risks / blockers / warnings (red)
- `#667eea → #764ba2` — gradient for headers

**HTML template**:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Plan Title]</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', system-ui, -apple-system, sans-serif;
      max-width: 1100px; margin: 0 auto; padding: 40px 24px;
      background: #0f172a; color: #e2e8f0;
      line-height: 1.6;
    }
    .hero {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white; padding: 48px 40px; border-radius: 16px;
      margin-bottom: 40px; position: relative; overflow: hidden;
    }
    .hero h1 { font-size: 2.2rem; font-weight: 700; margin-bottom: 12px; }
    .hero .subtitle { font-size: 1.1rem; opacity: 0.9; max-width: 700px; }
    .hero .meta {
      margin-top: 20px; display: flex; gap: 20px; flex-wrap: wrap;
      font-size: 0.9rem; opacity: 0.8;
    }
    .hero .meta span {
      background: rgba(255,255,255,0.15); padding: 4px 12px;
      border-radius: 20px;
    }

    .section {
      background: #1e293b; border-radius: 12px; padding: 32px;
      margin-bottom: 24px; border: 1px solid #334155;
    }
    .section h2 {
      font-size: 1.4rem; margin-bottom: 16px;
      display: flex; align-items: center; gap: 10px;
    }
    .section h2 .badge {
      font-size: 0.75rem; padding: 3px 10px; border-radius: 12px;
      font-weight: 600; text-transform: uppercase;
    }

    .phase-grid {
      display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px; margin-top: 16px;
    }
    .phase-card {
      background: #0f172a; border-radius: 10px; padding: 20px;
      border-left: 4px solid; position: relative;
    }
    .phase-card h3 { font-size: 1rem; margin-bottom: 8px; }
    .phase-card ul { padding-left: 18px; font-size: 0.9rem; color: #94a3b8; }
    .phase-card li { margin-bottom: 4px; }

    .diagram-container {
      background: #0f172a; border-radius: 10px; padding: 24px;
      margin: 16px 0; text-align: center; overflow-x: auto;
    }
    .diagram-container img, .diagram-container svg {
      max-width: 100%; height: auto;
    }
    .diagram-caption {
      font-size: 0.85rem; color: #64748b; margin-top: 8px;
      font-style: italic;
    }

    .kpi-row {
      display: flex; gap: 16px; flex-wrap: wrap; margin: 16px 0;
    }
    .kpi {
      background: #0f172a; border-radius: 10px; padding: 16px 20px;
      flex: 1; min-width: 140px; text-align: center;
    }
    .kpi .value { font-size: 1.8rem; font-weight: 700; }
    .kpi .label { font-size: 0.8rem; color: #64748b; margin-top: 4px; }

    .risk-item {
      display: flex; gap: 12px; padding: 12px 16px;
      background: #0f172a; border-radius: 8px; margin-bottom: 8px;
      border-left: 3px solid #fc8181;
    }
    .risk-item .severity {
      font-size: 0.75rem; font-weight: 700; padding: 2px 8px;
      border-radius: 4px; height: fit-content;
    }

    .decision-item {
      padding: 12px 16px; background: #0f172a;
      border-radius: 8px; margin-bottom: 8px;
      border-left: 3px solid #9f7aea;
    }

    table {
      width: 100%; border-collapse: collapse; margin: 12px 0;
      font-size: 0.9rem;
    }
    th { background: #0f172a; padding: 10px 12px; text-align: left; color: #94a3b8; font-weight: 600; }
    td { padding: 10px 12px; border-top: 1px solid #334155; }

    .tag { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; margin: 2px; }
    .tag-blue { background: rgba(66,153,225,0.2); color: #63b3ed; }
    .tag-green { background: rgba(72,187,120,0.2); color: #68d391; }
    .tag-purple { background: rgba(159,122,234,0.2); color: #b794f4; }
    .tag-orange { background: rgba(237,137,54,0.2); color: #f6ad55; }
    .tag-red { background: rgba(252,129,129,0.2); color: #feb2b2; }

    .footer {
      text-align: center; padding: 24px; color: #475569;
      font-size: 0.8rem; border-top: 1px solid #1e293b;
      margin-top: 40px;
    }

    @media (max-width: 600px) {
      body { padding: 16px; }
      .hero { padding: 24px; }
      .hero h1 { font-size: 1.6rem; }
      .phase-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>

  <!-- HERO -->
  <div class="hero">
    <h1>[Plan Title]</h1>
    <p class="subtitle">[1-2 sentence purpose statement]</p>
    <div class="meta">
      <span>[Date]</span>
      <span>[Phase count] Phases</span>
      <span>[Status]</span>
    </div>
  </div>

  <!-- KPIs / AT-A-GLANCE (optional — use if plan has metrics) -->
  <div class="section">
    <h2>At a Glance</h2>
    <div class="kpi-row">
      <div class="kpi"><div class="value" style="color:#4299e1">[X]</div><div class="label">[Metric]</div></div>
      <div class="kpi"><div class="value" style="color:#48bb78">[Y]</div><div class="label">[Metric]</div></div>
      <div class="kpi"><div class="value" style="color:#9f7aea">[Z]</div><div class="label">[Metric]</div></div>
    </div>
  </div>

  <!-- HIGH-LEVEL FLOW DIAGRAM -->
  <div class="section">
    <h2>Plan Overview</h2>
    <div class="diagram-container">
      <!-- Inline SVG from render-svg.mjs here -->
    </div>
    <p class="diagram-caption">High-level flow showing phases and dependencies</p>
  </div>

  <!-- PHASES (use phase-grid for parallel, sequential list for linear) -->
  <div class="section">
    <h2>Implementation Phases</h2>
    <div class="phase-grid">
      <div class="phase-card" style="border-color: #4299e1;">
        <h3 style="color: #4299e1;">Phase 1: [Name]</h3>
        <ul><li>[Step]</li><li>[Step]</li></ul>
      </div>
      <div class="phase-card" style="border-color: #ed8936;">
        <h3 style="color: #ed8936;">Phase 2: [Name]</h3>
        <ul><li>[Step]</li><li>[Step]</li></ul>
      </div>
      <div class="phase-card" style="border-color: #48bb78;">
        <h3 style="color: #48bb78;">Phase 3: [Name]</h3>
        <ul><li>[Step]</li><li>[Step]</li></ul>
      </div>
    </div>
  </div>

  <!-- ARCHITECTURE / COMPONENT DIAGRAM -->
  <div class="section">
    <h2>Architecture</h2>
    <div class="diagram-container">
      <!-- Inline SVG -->
    </div>
    <p class="diagram-caption">System components and data flow</p>
  </div>

  <!-- DECISIONS -->
  <div class="section">
    <h2>Key Decisions</h2>
    <div class="decision-item">
      <strong>[Decision]</strong><br>
      <span style="color:#94a3b8">[Rationale]</span>
    </div>
  </div>

  <!-- RISKS (if applicable) -->
  <div class="section">
    <h2>Risks & Considerations</h2>
    <div class="risk-item">
      <span class="severity" style="background:rgba(252,129,129,0.2);color:#feb2b2">HIGH</span>
      <div><strong>[Risk]</strong><br><span style="color:#94a3b8">[Mitigation]</span></div>
    </div>
  </div>

  <!-- SEQUENCE / TIMELINE DIAGRAM (if multi-step or multi-agent) -->
  <div class="section">
    <h2>Execution Sequence</h2>
    <div class="diagram-container">
      <!-- Inline SVG -->
    </div>
    <p class="diagram-caption">Step-by-step execution order</p>
  </div>

  <div class="footer">
    Generated by analytics workspace visualize-plan &mdash; [Date]
  </div>

</body>
</html>
```

### Step 4: Generate All Diagrams

Run `render-svg.mjs` for each diagram planned in Step 2. Save to `/tmp/` as intermediate files.

Read each SVG file and inline the content directly into the HTML (replace `<!-- Inline SVG -->` placeholders). This makes the HTML fully self-contained.

### Step 5: Populate Content

Fill in the HTML template with extracted content:
- Hero: title, subtitle, metadata tags
- KPIs: key numbers from the plan (phases, models, files, metrics)
- Phase cards: one per major phase/step with sub-items
- Decisions: key choices with rationale
- Risks: blockers, dependencies, considerations
- Remove sections that don't apply (not every plan has risks, KPIs, etc.)

### Step 6: Write and Open

```bash
# Write the file
# Default: docs/research/[plan-name]-visual.html

# Open in browser for review
open docs/research/[plan-name]-visual.html
```

Tell the user the output path and offer to adjust colors, add/remove sections, or regenerate diagrams.

---

## Quality Checklist

Before delivering:
- [ ] All SVGs render (test with `open /tmp/plan-flow.svg` first)
- [ ] HTML is self-contained (no external dependencies)
- [ ] Responsive layout (check at 600px width mentally)
- [ ] Dark theme is readable (sufficient contrast)
- [ ] Diagrams use different themes for visual variety
- [ ] Phase colors are distinct and semantic
- [ ] No placeholder text remains (`[Plan Title]` etc.)
- [ ] File size reasonable (< 500KB)

---

## Adaptation Notes

**For dbt pipelines**: Also read `dbt-tech-spec-writer` skill. Include model inventory table, transformation rules, dependency graph, and test requirements in dedicated sections.

**For system/tool plans**: Focus on component architecture, data flow, and sequence diagrams. Use the design-document-writer structure (scope, design overview, key decisions, alignment).

**For process/workflow plans**: Emphasize the sequence diagram and phase cards. Add a timeline or Gantt-style visualization if phases have dependencies.
