# Data Storytelling

**Maintainer:** Keith
**Status:** Accepting contributions

## What This Covers

Turning data analysis into compelling visual narratives — dashboards, scrollytelling pages, data stories, ECharts configurations, and presentation design patterns.

## Why This Folder Matters

When you ask Claude to build a data story or dashboard, the quality depends on knowing our design system, chart preferences, layout patterns, and what's worked before. Generic chart advice produces generic output. Team-specific patterns produce polished, consistent deliverables.

## How Agents Use This Folder

Claude reads files here when:
- You mention "data story", "dashboard", "visualization", or "chart"
- You invoke `/data-story` or `/explore-data`
- You're building HTML pages with ECharts, D3, or other chart libraries

This folder works alongside several skills:
- `echarts` — ECharts configuration reference
- `interactive-dashboard-builder` — keyboard-navigable dashboard patterns
- `data-storytelling` — end-to-end story creation workflow
- `samwho-interactive-viz` — scroll-driven animation patterns

## What to Add

### `patterns/` — Proven visual approaches

- Dashboard layout templates (KPI bar + chart grid + detail table)
- Chart selection guide ("when to use ribbon chart vs stacked bar")
- Color palette patterns and dark mode considerations
- Section tab navigation standard (sticky tabs, frosted glass — see `.claude/rules/viz-section-tab-standard.md`)
- Mobile responsiveness patterns

### `reference/` — Design system and tools

- Color palettes and CSS variables
- Typography and spacing conventions
- ECharts version notes and gotchas (registerMap, visualMap overrides, etc.)
- Reference implementations (links to best examples we've built)
- Data format conventions (JSON structure for chart data)

### `decisions/` — Why we do things this way

- "Why we inline GeoJSON instead of fetching" (CORS on file:// protocol)
- "Why we use ECharts over D3 for most charts"
- "Why dark mode is the default"
- "Why scrollytelling uses IntersectionObserver, not scroll position"

## Getting Started

Start with what you know:

1. **Document one chart pattern** — your go-to chart type with the ECharts config that works
2. **Document one layout** — how you structure a dashboard page (HTML skeleton)
3. **Document one gotcha** — the rendering bug that cost you 2 hours

## Iteration Circuit Breaker

We have a rule (`.claude/rules/viz-iteration-circuit-breaker.md`): after 2 failed fix attempts on a visual bug, stop coding and research. This folder is where those research findings should land — so the next person doesn't hit the same bug.
