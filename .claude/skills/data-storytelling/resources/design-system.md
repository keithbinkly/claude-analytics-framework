# Data Storytelling Design System

## CSS Variables (Dark Theme)

```css
:root {
  --bg:#0f172a; --card:#1e293b; --bdr:#334155; --s6:#475569;
  --t1:#e2e8f0; --t2:#94a3b8; --t3:#64748b; --t4:#475569;
  --pk:#f472b6; --sk:#38bdf8; --am:#fbbf24; --em:#34d399; --vi:#a78bfa;
  --ff:'Space Grotesk','Inter',system-ui,sans-serif;
  --fm:'Space Mono','JetBrains Mono',monospace;
}
```

## Color Palette Usage

| Token | Hex | Role |
|-------|-----|------|
| PK | #f472b6 | Warning, negative, alert |
| SK | #38bdf8 | Primary accent, links, default KPI |
| AM | #fbbf24 | Section numbers, highlights |
| EM | #34d399 | Positive, success, good KPI |
| VI | #a78bfa | Secondary accent, gradients |

## Typography Scale

| Element | Font | Size | Weight |
|---------|------|------|--------|
| Hero h1 | Space Grotesk | 32px | 700 |
| Section h2 | Space Grotesk | 22px | 700 |
| Narrative | Space Grotesk | 14px | 400 |
| Section number | Space Mono | 11px | 700 |
| KPI value | Space Mono | 28px | 700 |
| KPI label | Space Grotesk | 11px | 400 |
| Insight label | Space Mono | 10px | 700 |
| Chart tooltip | Space Grotesk | 11px | 400 |

## Layout

- Max width: 900px, centered
- Section spacing: 64px margin-bottom
- Chart container: 10px border-radius, 16px padding, card background
- Chart height: 340px default, 400px tall, 300px short
- KPI grid: 4-column, 2-column on mobile (<600px)

## ECharts Shared Config

```javascript
// JS variables (comparison page and storytelling page)
const T='#e2e8f0', M='#94a3b8', D='#64748b', B='#334155';
const S6='#475569', S8='#1e293b', S9='#0f172a';
const PK='#f472b6', SK='#38bdf8', AM='#fbbf24', EM='#34d399', VI='#a78bfa';
const FF="'Space Grotesk','Inter',system-ui,sans-serif";
const FM="'Space Mono','JetBrains Mono',monospace";

// Always spread `base` into every chart option
const base = {
  backgroundColor:'transparent',
  textStyle:{fontFamily:FF, color:T},
  animation:true, animationDuration:600
};

// Tooltip helper (use for every chart)
const tt = (trigger='axis') => ({
  trigger, backgroundColor:S8, borderColor:B,
  textStyle:{color:T, fontSize:11, fontFamily:FF}
});

// Grid helper (consistent margins)
const grd = (l=60, r=20, t=32, b=28) => ({left:l, right:r, top:t, bottom:b});
```

## Key Rules

- Dark theme (--bg:#0f172a) — matches the storytelling page
- Space Grotesk for text, Space Mono for data labels
- No chart borders — container card provides structure
- Tooltips always dark-on-dark with the `tt()` helper
- Title above chart, type label below
- Embed data arrays directly in `<script>` (no external fetches)
- Every chart: `echarts.init(document.getElementById('cN'))` in a DOMContentLoaded listener
- Resize handler: `window.addEventListener('resize', () => { c1.resize(); c2.resize(); ... })`

## HTML Section Structure

```html
<!-- Hero: Title + subtitle + meta -->
<header class="hero">
  <h1>[Story Title]</h1>
  <p class="sub">[1-2 sentence thesis]</p>
  <p class="meta">dbt Semantic Layer · AI Analyst Ensemble · [date]</p>
</header>

<!-- KPI row: 3-4 headline numbers -->
<div class="kpi-row">
  <div class="kpi"><div class="val">[N]</div><div class="lbl">[label]</div></div>
</div>

<!-- Sections: One per VIZ spec -->
<div class="section" id="s1">
  <div class="section-num">01 — [Section Title]</div>
  <h2>[Insight headline as sentence]</h2>
  <p class="narrative">[2-3 sentences: what the chart shows and why it matters]</p>
  <div class="chart-wrap"><div class="chart-box" id="c1"></div></div>
  <div class="insight">
    <div class="label">Observation</div>
    <p>[Key takeaway from this chart]</p>
  </div>
</div>
```

## Narrative Writing Rules

- Section title = action verb or discovery statement, NOT chart description
  - Good: "01 — The Surge" / "eWallet adoption varies 12x across merchant categories"
  - Bad: "01 — Bar Chart of eWallet Share"
- Lead with the finding, then support with specific numbers
- Bold key numbers: `<strong>24.4%</strong>`
- Insight callout: One sentence, the "so what"

## KPI Selection Rules

- Pick 3-4 numbers that frame the story's tension
- At least one should be surprising or contradictory
- Use `.val.warn` (pink) for concerning metrics, `.val.good` (green) for positive
- Default `.val` (blue) for neutral context
