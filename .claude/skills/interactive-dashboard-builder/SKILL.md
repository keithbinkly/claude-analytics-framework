---
name: interactive-dashboard-builder
description: Build keyboard-navigable interactive HTML dashboards with deep-dive analytics. Use when asked to "build a dashboard", "create an interactive report", "data story", or "deep dive visualization".
---

# Interactive Dashboard Builder

Build keyboard-first, interactive HTML dashboards using ECharts + vanilla JS. No React, no build step — single-file HTML artifacts served via python HTTP server.

**Triggers**: interactive dashboard, keyboard dashboard, echarts dashboard, deep dive, analyst dashboard, data story

---

## Architecture Overview

```
Single HTML File
├── <style>  — Tailwind-inspired CSS (no CDN, hand-rolled)
├── <body>   — Semantic HTML: header, narrative, KPI row, chart panels, matrix, footer
├── Status Bar (fixed bottom) — InstaChart pattern
├── Help Overlay — keyboard shortcut reference
├── Toast System — ephemeral feedback
└── <script>
    ├── Palette & Shared Config (P, TT, AX, SPLIT, fmt)
    ├── Chart Registry (registerChart → charts[])
    ├── Chart Definitions (CH1–CHn)
    ├── State Machine (focus, grid, labels)
    ├── Keyboard Handler
    ├── Click-to-Focus
    └── Resize / Fullscreen handlers
```

---

## Core Patterns

### 1. Chart Registry

Every chart goes through `registerChart()` which stores the instance, element, panel reference, original options (deep cloned), and view configuration.

```javascript
const charts = [];

function registerChart(id, option, name, opts = {}) {
  const el = document.getElementById(id);
  const instance = echarts.init(el);
  instance.setOption(option);
  const panel = el.closest('.panel');
  const views = opts.views || ['line', 'bar'];
  charts.push({
    instance, el, panel, name,
    origOption: deepClone(option),
    views,
    toggleable: opts.toggleable !== false,
    viewIdx: 0
  });
  return instance;
}
```

**Key properties:**
- `origOption` — deep clone preserving functions (for safe toggle/restore)
- `views` — array of chart types this chart can cycle through (e.g. `['bar', 'line']`)
- `toggleable` — set `false` for charts that shouldn't toggle (e.g. waterfall)
- `viewIdx` — current position in the views cycle

### 2. Deep Clone (Function-Safe)

**Critical pattern.** `JSON.parse(JSON.stringify())` strips JavaScript functions (formatters, callbacks). This kills `fmt()` abbreviations and custom label formatters after toggle/restore.

```javascript
function deepClone(obj) {
  if (obj === null || typeof obj !== 'object') return obj;
  if (typeof obj === 'function') return obj;
  if (Array.isArray(obj)) return obj.map(deepClone);
  const clone = {};
  for (const key of Object.keys(obj)) clone[key] = deepClone(obj[key]);
  return clone;
}
```

**When to use:** Any time you store or restore ECharts options that contain formatter functions.

### 3. Number Abbreviation

```javascript
function fmt(n) {
  if (n >= 1e6) return (n / 1e6).toFixed(1) + 'M';
  if (n >= 1e3) return (n / 1e3).toFixed(0) + 'K';
  return n.toString();
}
```

Wire into tooltips globally and per-series labels:
```javascript
const TT = { ..., valueFormatter: v => typeof v === 'number' ? fmt(v) : v };
// Per-series:
label: { formatter: p => fmt(p.value) }
```

### 4. Chart Type Toggle

Rebuilds the FULL option from `origOption` with proper type conversion. Uses `setOption(opt, true)` — **notMerge mode** — to avoid stale properties.

```javascript
function toggleChartType() {
  const c = charts[state.focusIdx];
  c.viewIdx = (c.viewIdx + 1) % c.views.length;
  const targetType = c.views[c.viewIdx];

  // Return to original = just restore
  if (c.viewIdx === 0) {
    c.instance.setOption(deepClone(c.origOption), true);
    return;
  }

  // Build converted option
  const opt = deepClone(c.origOption);
  opt.series = opt.series.map(s => {
    if (s.itemStyle?.color === 'transparent') return s; // skip spacers
    const converted = { ...s, type: targetType };
    if (targetType === 'bar') {
      delete converted.areaStyle;
      delete converted.lineStyle;
      delete converted.symbol;
      delete converted.symbolSize;
      converted.itemStyle = { ...converted.itemStyle, borderRadius: [3,3,0,0] };
    } else if (targetType === 'line') {
      delete converted.barWidth;
      delete converted.barGap;
      delete converted.stack;
      converted.symbolSize = converted.symbolSize || 5;
    }
    return converted;
  });
  c.instance.setOption(opt, true);
}
```

### 5. Label Cycling (Safe)

Only toggles `show` on/off. **Never touches formatters** — they must survive.

```javascript
function cycleLabels() {
  state.labelMode = (state.labelMode + 1) % 2;
  const show = state.labelMode === 0;
  const targets = state.focusIdx >= 0 ? [charts[state.focusIdx]] : charts;
  targets.forEach(c => {
    const opt = c.instance.getOption();
    c.instance.setOption({
      series: opt.series.map(() => ({ label: { show } }))
    });
  });
}
```

### 6. Click-to-Focus

Panels have `data-chart-idx` attributes and `cursor: pointer`. Click toggles focus.

```javascript
document.querySelectorAll('.panel[data-chart-idx]').forEach(panel => {
  panel.addEventListener('click', (e) => {
    if (e.target.closest('canvas')) return; // don't steal ECharts interactions
    const idx = parseInt(panel.getAttribute('data-chart-idx'));
    if (state.focusIdx === idx) {
      setFocus(-1); // click again to clear
    } else {
      setFocus(idx);
    }
  });
});
```

---

## Keyboard Shortcuts (InstaChart-Inspired)

| Key | Action | Scope |
|-----|--------|-------|
| `j` / `k` | Navigate focus next / previous | Global |
| `1`–`8` | Jump to chart by number | Global |
| `0` | Clear focus | Global |
| `g` | Cycle grid: dashed → solid → off | Focused or all |
| `m` | Toggle labels on/off | Focused or all |
| `t` | Toggle chart type (line ↔ bar) | Focused only |
| `e` | Export focused chart as PNG | Focused only |
| `a` | Export all charts as PNGs | Global |
| `f` | Fullscreen focused chart | Focused only |
| `?` / `h` | Toggle help overlay | Global |
| `Esc` | Close help / exit fullscreen / clear focus | Context-dependent |

**Design principle:** When focused, controls apply to focused chart only. When unfocused, `g` and `m` apply to all charts.

---

## UX Components

### Status Bar (fixed bottom)
Shows: focus state, grid mode, label mode, quick shortcut hints.

### Toast Notifications
Ephemeral feedback (2s) for every action. Shows key pressed + result.

### Help Overlay
Full shortcut reference. Triggered by `?`. Dismisses on `?` or `Esc`.

### Focus Ring
Focused panel gets amber border + glow (`border-color: #fbbf24; box-shadow: 0 0 0 1px #fbbf24`).

---

## Color Palette: Tailwind on Slate

```
Data Colors (Tailwind 400-level):
  pink-400    #f472b6  — primary metric, decline, alert
  sky-400     #38bdf8  — secondary metric, comparison, positive
  amber-400   #fbbf24  — accent, focus ring, warnings
  emerald-400 #34d399  — tertiary, categorical
  violet-400  #a78bfa  — quaternary, categorical

Background (Tailwind Slate):
  slate-900   #0f172a  — body background
  slate-800   #1e293b  — panel/card background
  slate-700   #334155  — borders, dividers, grid lines

Text (Tailwind Slate):
  slate-200   #e2e8f0  — primary text, data labels
  slate-400   #94a3b8  — axis labels, secondary text
  slate-500   #64748b  — muted text, subtitles
  slate-600   #475569  — tertiary text, hints

Typography:
  Space Grotesk  — headings, narrative, axis categories
  Space Mono     — numbers, KPIs, labels, code-like elements
```

### Semantic Mapping

| Meaning | Color | Tailwind |
|---------|-------|----------|
| Primary metric / decline / alert | `#f472b6` | pink-400 |
| Comparison / adjusted / positive | `#38bdf8` | sky-400 |
| Accent / focus / warning | `#fbbf24` | amber-400 |
| Tertiary / categorical A | `#34d399` | emerald-400 |
| Tertiary / categorical B | `#a78bfa` | violet-400 |

---

## Shared ECharts Config

```javascript
const P = {
  pink:'#f472b6', sky:'#38bdf8', amber:'#fbbf24',
  emerald:'#34d399', violet:'#a78bfa',
  slate4:'#94a3b8', slate5:'#64748b', slate6:'#475569',
  bg:'#1e293b', border:'#334155', text:'#e2e8f0'
};
const Pt = { // rgba prefixes for opacity variants
  pink:'rgba(244,114,182,', sky:'rgba(56,189,248,',
  amber:'rgba(251,191,36,', emerald:'rgba(52,211,153,',
  violet:'rgba(167,139,250,'
};
const TT = {
  backgroundColor:'#1e293b', borderColor:'#334155',
  textStyle: { color:'#e2e8f0', fontSize:12, fontFamily:'Space Mono' },
  valueFormatter: v => typeof v === 'number' ? fmt(v) : v
};
const AX = { color: P.slate4, fontSize: 11, fontFamily: 'Space Mono' };
const SPLIT = { lineStyle: { color: P.border, type: 'dashed' } };
const ALINE = { lineStyle: { color: P.border } };
```

---

## Font Size Reference

| Element | Size | Font |
|---------|------|------|
| Page title | 24px | Space Grotesk 700 |
| Subtitle | 13px | Space Mono |
| Narrative | 14px | Space Grotesk |
| KPI value | 32px | Space Mono 700 |
| KPI label | 11px | Space Mono uppercase |
| KPI comparison | 13px | Space Mono |
| Section heading | 16px | Space Grotesk 700 |
| Panel title | 14px | Space Grotesk 600 |
| Panel subtitle | 11px | Space Mono |
| Chart axis labels | 11px | Space Mono |
| Chart data labels | 11–13px | Space Mono |
| Legend text | 11px | Space Mono |
| Tooltip text | 12px | Space Mono |
| Callout | 13px | Space Grotesk |
| Footer | 11px | Space Mono |
| Status bar | 12px | Space Mono |

---

## Layout Structure

```
header (flex: title left, hint-pill right)
narrative (border-left accent, italic insight)
kpi-row (4-col grid)
section-heading + chart rows (row-2 = 2-col, row-3 = 3-col, row-full = 1-col)
callout (border-left accent, summary insight)
matrix-grid (CSS grid, concurrence table)
footer (source attribution)
status-bar (fixed bottom)
help-overlay (centered modal)
toast (fixed top-right, auto-dismiss)
```

**Panel HTML pattern:**
```html
<div class="panel" data-chart-idx="0">
  <span class="focus-badge">focused</span>
  <h3>Chart Title</h3>
  <div class="ps">one-line context subtitle</div>
  <div class="chart ch-t" id="ch_name"></div>
</div>
```

Chart heights: `ch-t` = 280px (tall/hero), `ch-m` = 240px (standard).

---

## Delivery

```bash
# Save to Obsidian vault
[your-output-dir]/[name].html

# Start HTTP server for mobile viewing
lsof -ti:8080 | xargs kill -9 2>/dev/null; sleep 1
cd "[your-output-dir]" && nohup python3 -m http.server 8080 > /dev/null 2>&1 &

# View on phone
# http://192.168.1.56:8080/[name].html
```

---

## Version Control

Always create new files for major iterations. Never overwrite previous versions.
- `[name].html` — v1 (static)
- `[name]-v2.html` — v2 (interactive)

This preserves the ability to compare, rollback, or reference earlier designs.

---

## Lessons Learned

1. **`JSON.parse/stringify` kills formatters** — always use `deepClone()` for ECharts options
2. **`setOption()` merges by default** — use `setOption(opt, true)` (notMerge) for type toggles
3. **Label cycling must only toggle `show`** — setting `formatter: undefined` permanently destroys abbreviation
4. **Legend positioning**: vertical right-side legends (`right:0, orient:'vertical', top:'middle'`) avoid axis overlap on multi-series charts
5. **Series-level `itemStyle.color`** required for legend color inheritance — per-data-point colors alone don't propagate to legend swatches
6. **React is NOT needed** — `document.addEventListener('keydown', handler)` + state object is sufficient for dashboard interactivity
7. **Font sizes need deliberate bumping** — ECharts defaults and initial CSS tend too small on dark backgrounds; plan for +2px pass
8. **ECharts has NO native ribbon chart** — build with `custom` series + `sampleBezier()` polygon approximation. See `echarts/SKILL.md` "Special: Ribbon Chart" section for full pattern.
9. **ECharts `graphic` element styles reset on `setOption`** — must include full style (font, fill, etc.) in every update call, not just the text. Partial style updates overwrite the entire style object.
10. **ECharts `polygon` type only supports straight lines** — for smooth curves, sample bezier with 12+ points. `type: 'path'` with `pathData` uses bounding-box-relative coords (not absolute), so polygon is preferred.

---

## Dependencies

- **ECharts 5.5.0** via CDN: `https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js`
- **Google Fonts**: Space Grotesk (400,500,600,700) + Space Mono (400,700)
- No other dependencies. No build step. No framework.

---

## Relationship to Other Skills

| Skill | Relationship |
|-------|-------------|
| **echarts** | ECharts capability reference — rich text, chart types, config patterns, events, performance. Read this for "how do I do X in ECharts?" |
| **mviz** | Static report generator (JSON spec → HTML). Use mviz for quick one-off reports. Use this skill for interactive analyst dashboards. |
| **dashboard-design-guidelines** | Design theory reference. This skill implements those principles with Tailwind palette + interactivity. |
| **serve-html** | Delivery mechanism. This skill creates the artifact; serve-html delivers it. |
| **architecture-diagram-creator** | Different purpose — system diagrams, not data dashboards. |
| **frontend-design** | General frontend skill. This is specialized for data analyst dashboards. |
