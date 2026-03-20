# ECharts Native Features — When to Use What

Use-case-driven guide to ECharts features beyond basic chart types.
Organized by "what are you trying to do?" not "what does the API offer?"

**Principle: Don't force features in. Each feature below has a "use when" and
a "don't use when." If neither condition matches your chart, skip it.**

Researched from ECharts 6.0.0 docs, handbook, and source code (2026-03-18).

---

## Staggered Animation — `animationDelay`

**Use when:** A bar chart has 10+ bars and the sequence matters (ranking, time
progression, building a gradient). The staggered reveal turns a static chart
into a narrative — "watch the pattern build."

**Don't use when:** The chart has <8 elements (stagger is barely perceptible),
it's a line chart (staggering points on a line looks glitchy — the whole line
should draw at once), or the chart updates frequently (repeated stagger annoys).

```javascript
series: [{
  type: 'bar',
  data: [...],
  animationDelay: function(idx) { return idx * 60; },
  animationEasing: 'cubicOut'
}]
```

**Timing guidance:** 40-80ms per element. 24 bars × 60ms = 1.4s total reveal.
Much longer than 2s feels sluggish. Much shorter than 0.8s is imperceptible.

**Gotcha:** A global `animationDuration` at the chart option level overrides
per-series `animationDelay`. If you set both, the global duration wins and all
bars animate simultaneously. Fix: remove the global `animationDuration` and set
`animationDuration` per-series instead (e.g., 400ms per bar, staggered start).

---

## Connected Charts — `echarts.connect`

**Use when:** Two or more charts on the same page share a meaningful axis
(same time range, same categories) and are close enough visually that a
synchronized crosshair helps comparison. The classic case: a line chart +
bar chart showing the same time period, where hovering one shows the
corresponding point on the other.

**Don't use when:** Charts have different X-axes (different time ranges,
different categories), charts are in different sections of a long scroll page
(user won't see both simultaneously), or one chart is a map/treemap (no
shared axis to synchronize on).

```javascript
// After all chart instances are created:
chartA.group = 'comparison';
chartB.group = 'comparison';
echarts.connect('comparison');
```

**What syncs:** Tooltip position, axis crosshair, legend selection, dataZoom.
Two lines of code. No event handlers needed.

---

## universalTransition — Chart Morphing

**Use when:** Your narrative transitions from one view of the data to another
(bar → pie showing the same categories, scatter → treemap grouping the same
points). The morph shows the reader that it's the same data, just a different
lens. This is the single highest-impact feature for scrollytelling.

**Don't use when:** The two charts show different datasets (the morph would be
meaningless — it's not the same data rearranging, it's different data appearing).
Also don't use for charts that are all visible simultaneously — morph is for
sequential reveals where one chart replaces another.

```javascript
// State A: bar chart
chart.setOption({
  series: [{
    id: 'main',  // MUST match between states
    universalTransition: { enabled: true, divideShape: 'split' },
    type: 'bar', data: barData
  }]
});

// State B: pie chart (triggered by scroll waypoint or button)
chart.setOption({
  series: [{
    id: 'main',  // same id → morph animation
    universalTransition: { enabled: true },
    type: 'pie', data: pieData
  }]
});
```

**`divideShape`:** `'split'` for bars/areas (one shape becomes many),
`'clone'` for scatter (many shapes rearrange). Wrong choice = ugly animation.

**Requirement:** Series `id` must match between states. ECharts 5.2+.

---

## graphic Component — Editorial Annotations

**Use when:** You need annotation elements that aren't anchored to data
coordinates — editorial text boxes, callout arrows, branding, or explanatory
diagrams that overlay the chart. Unlike markPoint/markLine (which are
data-bound), graphic elements are positioned by pixel or percentage.

**Don't use when:** The annotation IS about a specific data point — use
markPoint for that. Graphic is for page-level editorial, not data-level.

```javascript
graphic: [
  {
    type: 'text',
    left: '12%', top: '15%',
    style: {
      text: 'Recession\nperiod',
      fontSize: 12,
      fill: '#94a3b8',
      font: "12px 'JetBrains Mono', monospace"
    }
  },
  {
    type: 'line',
    shape: { x1: 100, y1: 80, x2: 200, y2: 120 },
    style: { stroke: '#64748b', lineWidth: 1 }
  }
]
```

**Gotcha:** Graphic elements don't move with data zoom or axis changes.
They're fixed to the canvas. Use for static annotations only.

---

## dataset + encode — Declare Data Once

**Use when:** Multiple charts in the same story use the same base data filtered
or sorted differently. Instead of maintaining parallel JS arrays, declare one
dataset and filter inside ECharts.

**Don't use when:** Each chart has unique data from different sources, or the
data preprocessing is complex enough that JS is clearer than declarative transforms.

```javascript
option = {
  dataset: [
    { source: allData },                                    // index 0: raw
    { transform: { type: 'filter',                          // index 1: filtered
        config: { dimension: 'growth', '>': 0 } } },
    { transform: { type: 'sort',                            // index 2: sorted
        config: { dimension: 'value', order: 'desc' } } }
  ],
  series: [
    { type: 'bar', datasetIndex: 1, encode: { x: 'name', y: 'value' } },
    { type: 'bar', datasetIndex: 2, encode: { x: 'name', y: 'value' } }
  ]
};
```

---

## SVG Renderer

**Use when:** Chart has <1,000 data points AND you care about text crispness
(editorial presentation, PDF export). SVG renders text as DOM elements — crisper
than canvas at any zoom level, works with CSS print styles.

**Don't use when:** Chart has >2,000 points (SVG DOM gets heavy), chart needs
heavy animation (canvas is faster), or chart is a heatmap/treemap with many cells.

```javascript
var chart = echarts.init(el, null, { renderer: 'svg' });
```

---

## Responsive Media Queries

**Use when:** A chart needs different configuration at different container widths
(hide legend on mobile, reduce font sizes, change grid margins). Built into
ECharts — based on container size, not viewport.

**Don't use when:** Your responsive needs are CSS-only (hiding elements,
stacking layouts). Use CSS media queries for page layout, ECharts media for
chart-internal config.

```javascript
option = {
  // Desktop defaults
  legend: { show: true },
  grid: { left: 80, right: 40 },
  // Mobile overrides (container-width based)
  media: [
    {
      query: { maxWidth: 500 },
      option: {
        legend: { show: false },
        grid: { left: 40, right: 20 },
        series: [{ label: { show: false } }]
      }
    }
  ]
};
```

---

## aria + decal — Accessibility

**Use when:** Always. Every chart on a public site should have `aria.enabled`.
Add `decal` when the chart has 3+ color-coded categories that are indistinguishable
under colorblindness.

**Don't use when:** Never skip aria on public content.

```javascript
// Minimal (always add this)
aria: { enabled: true },

// With custom description
aria: {
  enabled: true,
  label: {
    description: 'Bar chart showing job gains and losses by occupation category'
  }
},

// Decal patterns for colorblind safety
aria: {
  enabled: true,
  decal: { show: true }  // geometric patterns overlay each series
}
```

---

## dispatchAction — Programmatic Interaction

**Use when:** Building scrollytelling where scroll waypoints should highlight
specific data points, show tooltips, or zoom to ranges. The Pudding/NYT
pattern: as the reader scrolls, the chart responds.

**Don't use when:** The chart is static with no scroll interaction, or the
interactivity is better handled by rebuilding the chart (setOption) rather
than highlighting within it.

```javascript
// On scroll waypoint: highlight a specific bar
chart.dispatchAction({
  type: 'highlight',
  seriesIndex: 0,
  dataIndex: 5
});

// Show tooltip programmatically
chart.dispatchAction({
  type: 'showTip',
  seriesIndex: 0,
  dataIndex: 5
});

// Downplay (remove highlight)
chart.dispatchAction({ type: 'downplay' });
```

---

## sampling — Large Datasets

**Use when:** A line chart has 500+ data points. One-line addition that
preserves peaks/valleys better than averaging.

**Don't use when:** The chart has <200 points (no visual difference), or every
individual data point matters (sampling drops points).

```javascript
series: [{
  type: 'line',
  sampling: 'lttb',  // Largest Triangle Three Buckets — best general-purpose
  data: thousandsOfPoints
}]
```

**Options:** `'lttb'` (recommended — preserves visual shape), `'average'`
(smooths), `'max'` / `'min'` (preserves extremes).

---

## timeline — Animated Playback

**Use when:** You have the same chart structure across multiple time periods
and want a play/pause control to step through them. Monthly snapshots,
yearly comparisons, election results by reporting time.

**Don't use when:** The data is already a continuous time series on the X-axis
(that's just a line chart), or the time periods require different chart types
(use universalTransition instead).

```javascript
option = {
  timeline: {
    data: ['2020', '2021', '2022', '2023', '2024'],
    autoPlay: false,
    playInterval: 1500,
    bottom: 10
  },
  options: [
    { title: { text: '2020' }, series: [{ data: data2020 }] },
    { title: { text: '2021' }, series: [{ data: data2021 }] },
    // ...
  ]
};
```

---

## Beeswarm — Jittered Scatter (v6)

**Use when:** A categorical scatter plot has many overlapping points at the
same Y-value. Beeswarm distributes them horizontally while preserving the
value axis. Perfect for showing individual data points grouped by category
without the overplotting problem.

**Don't use when:** You have <5 points per category (just use a dot plot),
or the continuous axis matters more than showing individual points (use a
box plot or violin).

```javascript
series: [{
  type: 'scatter',
  jitter: { x: 0.3 },          // horizontal spread
  jitterOverlap: false,         // prevent overlapping dots
  data: [...]
}]
```

**ECharts 6.0+ only.**

---

## Quick Decision Table

| I want to... | Use | Not |
|---|---|---|
| Reveal bars sequentially | `animationDelay` | Manual setTimeout |
| Sync crosshair across charts | `echarts.connect` | Custom event listeners |
| Morph bar → pie on scroll | `universalTransition` | dispose + reinit |
| Annotate with editorial text | `graphic` component | HTML overlay divs |
| Filter data for different charts | `dataset` transform | Pre-filtered JS arrays |
| Crisp text for print/editorial | `renderer: 'svg'` | Canvas (default) |
| Adapt chart for mobile | ECharts `media` queries | JS resize handlers |
| Accessibility on public charts | `aria: { enabled: true }` | Nothing (bad) |
| Highlight on scroll waypoint | `dispatchAction` | setOption rebuild |
| Handle 1000+ point lines | `sampling: 'lttb'` | Manual downsampling |
| Playback through time periods | `timeline` component | setInterval loop |
| Show individual dots by category | Beeswarm `jitter` (v6) | Overlapping scatter |
