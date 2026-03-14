---
name: echarts
description: ECharts configuration reference for building rich interactive charts. Use when creating dashboards, configuring chart options, or asked about "ECharts config", "chart options", "visual map", or "rich text labels".
---

# ECharts Reference

Comprehensive ECharts 5.5+ capability reference for building interactive data visualizations. Covers rich text, chart types, configuration patterns, events, and performance — the things pre-training doesn't reliably know.

**Triggers**: echarts, rich text, chart config, echarts option, axis formatter, visual map, dataset, echarts event

**Chart Directory**: `resources/chart-directory.md` — 60+ chart types with BI use cases, data shapes, and "choose when" guidance. Read this first to pick the right chart for your data.

**Consumer Finance Playbook**: `resources/consumer-finance-playbook.md` — 20 ECharts-ready chart specs across 10 analytical techniques (K-shape divergence, indexed baselines, contribution decomposition, gap charts, radar, heatmaps, gauges, geo maps, runway analysis, partner dashboards). Each has SQL metric definitions and ECharts config sketches.

---

## 1. Rich Text — Inline Legends, Colored Titles, Badges

The killer feature you're probably here for. Rich text lets you embed **colored series names directly in titles, labels, and axis labels** — eliminating the need for a separate legend.

### Syntax

```javascript
{
  title: {
    text: '{services|Services} leads at 40% — {retail|Retail} surges in Q4',
    textStyle: {
      rich: {
        services: { color: '#f472b6', fontWeight: 'bold', fontSize: 16 },
        retail:   { color: '#38bdf8', fontWeight: 'bold', fontSize: 16 }
      }
    }
  }
}
```

**Markup pattern:** `{styleName|visible text}` — define styles in `rich:{}`, reference them in the formatter string.

### Rich Text Properties (per fragment)

| Property | Type | Notes |
|----------|------|-------|
| `color` | string | Text fill color |
| `fontSize` | number | In pixels |
| `fontWeight` | string/number | `'bold'`, `'normal'`, 400-900 |
| `fontFamily` | string | Font name |
| `fontStyle` | string | `'normal'`, `'italic'` |
| `backgroundColor` | string/object | Solid color OR `{ image: 'url' }` for icons |
| `borderColor` | string | Fragment border |
| `borderWidth` | number | Border thickness |
| `borderRadius` | number/array | Corner rounding |
| `padding` | number/array | `[top, right, bottom, left]` |
| `width` | number/string | Fragment width (`'100%'` for full line) |
| `height` | number | Fragment height |
| `lineHeight` | number | Vertical spacing |
| `align` | string | `'left'`, `'center'`, `'right'` |
| `verticalAlign` | string | `'top'`, `'middle'`, `'bottom'` |
| `textBorderColor` | string | Text stroke color |
| `textBorderWidth` | number | Text stroke width |
| `textShadowColor` | string | Text shadow |
| `textShadowBlur` | number | Shadow blur radius |

### Pattern: Inline Legend in Title

Embed series colors in chart title — no separate legend needed:

```javascript
title: {
  text: [
    '{swatch1|●} {name1|Services}  ',
    '{swatch2|●} {name2|Retail}  ',
    '{swatch3|●} {name3|Gas}'
  ].join(''),
  left: 'center',
  textStyle: {
    fontSize: 13,
    fontFamily: 'Space Mono',
    rich: {
      swatch1: { color: '#f472b6', fontSize: 14 },
      name1:   { color: '#f472b6', fontSize: 12, padding: [0, 12, 0, 0] },
      swatch2: { color: '#38bdf8', fontSize: 14 },
      name2:   { color: '#38bdf8', fontSize: 12, padding: [0, 12, 0, 0] },
      swatch3: { color: '#fbbf24', fontSize: 14 },
      name3:   { color: '#fbbf24', fontSize: 12 }
    }
  }
}
```

### Pattern: Rich Text Data Labels

Multi-style labels on chart elements:

```javascript
series: [{
  type: 'bar',
  label: {
    show: true,
    position: 'top',
    formatter: function(p) {
      return '{value|' + fmt(p.value) + '}\n{pct|' + pct(p) + '%}';
    },
    rich: {
      value: { color: '#e2e8f0', fontSize: 13, fontFamily: 'Space Mono', fontWeight: 'bold' },
      pct:   { color: '#94a3b8', fontSize: 10, fontFamily: 'Space Mono' }
    }
  }
}]
```

### Pattern: Colored Badge / Pill

```javascript
rich: {
  badge: {
    backgroundColor: '#f472b6',
    color: '#fff',
    borderRadius: 10,
    padding: [2, 6, 2, 6],
    fontSize: 10,
    fontWeight: 'bold'
  }
}
// Usage: '{badge|NEW}'
```

### Pattern: Horizontal Rule in Label

```javascript
rich: {
  hr: {
    borderColor: '#475569',
    borderWidth: 0.5,
    width: '100%',
    height: 0
  }
}
// Usage: '{hr|}' on its own line
```

### Pattern: Rich Text Axis Labels

```javascript
xAxis: {
  axisLabel: {
    formatter: function(value) {
      if (value === 'Holiday Peak') {
        return '{highlight|' + value + '}';
      }
      return '{normal|' + value + '}';
    },
    rich: {
      highlight: { color: '#fbbf24', fontWeight: 'bold', fontSize: 12 },
      normal:    { color: '#94a3b8', fontSize: 11 }
    }
  }
}
```

### Pattern: Rich Legend Formatter

```javascript
legend: {
  formatter: function(name) {
    // Look up data to show value next to legend item
    var value = dataMap[name];
    return '{name|' + name + '}  {val|' + fmt(value) + '}';
  },
  textStyle: {
    rich: {
      name: { fontSize: 12, color: '#e2e8f0', width: 80 },
      val:  { fontSize: 12, color: '#94a3b8', fontFamily: 'Space Mono', align: 'right', width: 60 }
    }
  }
}
```

### Layout Rules

- Fragments are **inline-block** (like CSS)
- `'\n'` creates line breaks
- Largest `lineHeight` in a row determines row height
- Horizontal flow: left-aligned → right-aligned → center fills remainder
- `width` and `height` only work when `rich:{}` is defined at the label level

---

## 2. Chart Types (22 Series Types)

### Cartesian (Grid-based)
| Type | When to Use | Key Config |
|------|-------------|------------|
| `line` | Trends over time | `smooth`, `areaStyle`, `stack` |
| `bar` | Category comparison | `stack`, `barWidth`, `barGap` |
| `scatter` | Correlation, outliers | `symbolSize` (data-driven), `encode` |
| `effectScatter` | Highlighted points | `rippleEffect`, `showEffectOn` |
| `candlestick` | OHLC, range data | `[open, close, low, high]` |
| `boxplot` | Distribution comparison | `layout: 'horizontal'` |
| `heatmap` | 2D density | `visualMap` required |
| `pictorialBar` | Infographic bars | `symbol`, `symbolRepeat` |
| `custom` | Anything else | `renderItem` callback |

### Polar
| Type | When | Key Config |
|------|------|------------|
| `radar` | Multi-metric profiles | `indicator[]`, shape: 'circle'/'polygon' |

### Hierarchical
| Type | When | Key Config |
|------|------|------------|
| `tree` | Parent-child structure | `orient`, `layout: 'radial'` |
| `treemap` | Size-encoded hierarchy | `visibleMin`, `levels[]` |
| `sunburst` | Radial hierarchy | `radius`, `levels[]` |

### Relationship
| Type | When | Key Config |
|------|------|------------|
| `graph` | Network/relationships | `layout: 'force'`, `links[]` |
| `sankey` | Flow volumes | `nodes[]`, `links[]`, `orient` |

### Part-to-Whole
| Type | When | Key Config |
|------|------|------------|
| `pie` | Share of total (<7 slices) | `radius: ['40%','70%']` for donut |
| `funnel` | Sequential drop-off | `sort: 'descending'` |

### Flow / Temporal
| Type | When | Key Config |
|------|------|------------|
| `themeRiver` | Volume shifts over time | `[date, value, name]` data format |
| `parallel` | Multi-dimensional comparison | `parallelAxis[]` |
| `lines` | Geographic flow | `coordinateSystem: 'geo'` |

### Indicator
| Type | When | Key Config |
|------|------|------------|
| `gauge` | KPI vs threshold | `detail`, `progress`, `pointer` |

### Special: Bump Chart (Ranking Over Time)

ECharts has a native bump chart example that shows rank shifts — directly relevant for category ranking visualization:

```javascript
// Bump chart: line chart with rank-based y-axis
// Each series is a category; y-value is its rank per period
series: categories.map(function(cat) {
  return {
    name: cat,
    type: 'line',
    data: periods.map(function(p) { return rankOf(cat, p); }),
    symbolSize: 20,
    label: { show: true, formatter: '{b}', fontSize: 12 },
    lineStyle: { width: 3 },
    emphasis: { focus: 'series' }
  };
});
// Y-axis inverted (rank 1 at top):
yAxis: { type: 'value', inverse: true, min: 1, max: numCategories }
```

Full directory of chart types with BI use cases: `docs/guides/echarts-chart-directory.md`

### Special: Ribbon Chart (Power BI-style, Rank-Reordering Stacked Ribbons)

ECharts has NO native ribbon chart ([closed as not planned](https://github.com/apache/echarts/issues/13820)). Build one using `custom` series with bezier polygon rendering. Categories reorder at each time point based on value — ribbons cross as ranks change.

**Key technique:** Approximate cubic bezier curves with sampled polygon points (ECharts `polygon` type doesn't support curves natively).

```javascript
// 1. Bezier sampler — converts cubic bezier to polygon points
function sampleBezier(p0, p1, p2, p3, steps) {
  var pts = [];
  for (var i = 0; i <= steps; i++) {
    var t = i / steps, t1 = 1 - t;
    pts.push([
      t1*t1*t1*p0[0] + 3*t1*t1*t*p1[0] + 3*t1*t*t*p2[0] + t*t*t*p3[0],
      t1*t1*t1*p0[1] + 3*t1*t1*t*p1[1] + 3*t1*t*t*p2[1] + t*t*t*p3[1]
    ]);
  }
  return pts;
}

// 2. Compute stacked positions per time point (ascending sort → biggest on top)
var stackPos = []; // stackPos[timeIdx][category] = {bottom, top}
timePoints.forEach(function(t, ti) {
  var sorted = categories.map(function(cat) {
    return { cat: cat, val: data[cat][ti] };
  });
  sorted.sort(function(a, b) { return a.val - b.val; }); // ascending: smallest at bottom
  var pos = {}, cumY = 0;
  sorted.forEach(function(item) {
    pos[item.cat] = { bottom: cumY, top: cumY + item.val };
    cumY += item.val;
  });
  stackPos.push(pos);
});

// 3. One custom series per category
series: categories.map(function(cat) {
  return {
    type: 'custom',
    name: cat,
    data: segmentIndices, // [0,0], [1,0], ..., [N-2, 0]
    renderItem: function(params, api) {
      var idx = params.dataIndex;
      // Pixel coords via api.coord([xIdx, yVal])
      var lt = api.coord([idx, stackPos[idx][cat].top]);
      var lb = api.coord([idx, stackPos[idx][cat].bottom]);
      var rt = api.coord([idx+1, stackPos[idx+1][cat].top]);
      var rb = api.coord([idx+1, stackPos[idx+1][cat].bottom]);
      var lx = lt[0], rx = rt[0], cpx = (lx + rx) / 2;

      // Top edge left→right, bottom edge right→left (closed polygon)
      var topPts = sampleBezier([lx,lt[1]], [cpx,lt[1]], [cpx,rt[1]], [rx,rt[1]], 12);
      var botPts = sampleBezier([rx,rb[1]], [cpx,rb[1]], [cpx,lb[1]], [lx,lb[1]], 12);

      return {
        type: 'polygon',
        shape: { points: topPts.concat(botPts), smooth: 0 },
        style: { fill: colors[cat], opacity: 0.78 },
        emphasis: { style: { opacity: 1 } }
      };
    },
    emphasis: { focus: 'series' }
  };
});
```

**Tooltip trick:** Add an invisible `bar` series (`itemStyle: {color:'transparent'}`) with `tooltip.trigger:'axis'` to capture hover events across the full chart width. Custom series alone don't trigger axis tooltips reliably.

**Sort direction:** `ascending` sort puts smallest at bottom → biggest on top (matches Power BI behavior where highest-ranked ribbon is at the top).

**Working example:** `/Users/kbinkly/Obsidian-Vault/ClaudeUpdates/merchant-spend-amazon-mcc-v3.html` — 10 MCC categories, 26 weeks, full bezier ribbon chart with ranked tooltip.

---

## 3. Configuration Patterns

### Global Text Style

Apply once, inherit everywhere:

```javascript
{
  textStyle: {
    fontFamily: "'Space Grotesk', 'Inter', system-ui, sans-serif",
    color: '#e2e8f0'
  }
}
```

### Tooltip (Rich HTML)

```javascript
tooltip: {
  trigger: 'axis',          // 'item' for pie/scatter, 'axis' for line/bar
  backgroundColor: '#1e293b',
  borderColor: '#334155',
  textStyle: { color: '#e2e8f0', fontSize: 12, fontFamily: 'Space Mono' },
  formatter: function(params) {
    // Return raw HTML string for full control
    var html = '<div style="font-weight:700">' + params[0].axisValue + '</div>';
    params.forEach(function(p) {
      html += '<div>' +
        '<span style="display:inline-block;width:10px;height:10px;' +
        'border-radius:2px;background:' + p.color + ';margin-right:4px"></span>' +
        p.seriesName + ': <b>' + fmt(p.value) + '</b></div>';
    });
    return html;
  },
  axisPointer: {
    type: 'cross',           // 'line', 'shadow', 'cross', 'none'
    crossStyle: { color: '#94a3b8' }
  }
}
```

### Grid (Chart Area)

```javascript
grid: {
  top: 40,      // Leave room for title
  right: 10,    // or 80 for right-side legend
  bottom: 30,   // or 60 for rotated labels
  left: 55,     // or 70 for formatted y-axis
  containLabel: true  // Auto-adjust for label overflow
}
```

### Legend

```javascript
legend: {
  // Positioned right side, vertical:
  orient: 'vertical',
  right: 0,
  top: 'middle',
  icon: 'roundRect',        // 'circle', 'rect', 'roundRect', 'triangle', 'diamond', 'pin', 'arrow', 'none'
  itemWidth: 12,
  itemHeight: 12,
  itemGap: 8,
  textStyle: { color: '#94a3b8', fontSize: 11, fontFamily: 'Space Mono' },
  // Or hidden (use inline legend in title instead):
  show: false
}
```

### Axis Configuration

```javascript
xAxis: {
  type: 'category',         // 'value', 'time', 'log'
  data: categories,
  axisLabel: {
    color: '#94a3b8',
    fontSize: 11,
    fontFamily: 'Space Mono',
    rotate: 45,              // Rotated labels
    formatter: function(v) { return v.substring(5); }  // Trim year prefix
  },
  axisLine: { lineStyle: { color: '#334155' } },
  axisTick: { show: false },
  splitLine: { show: false }  // Guidelines default off per design guidelines
},
yAxis: {
  type: 'value',
  axisLabel: {
    color: '#94a3b8',
    fontSize: 11,
    fontFamily: 'Space Mono',
    formatter: function(v) { return fmt(v); }
  },
  splitLine: { show: false },  // Default off; toggle with 'g' key
  // Dual axis: use yAxisIndex on series
  // Inverse: inverse: true (for rank charts)
  // Log: type: 'log', logBase: 10
}
```

### Reference Lines (markLine)

```javascript
series: [{
  markLine: {
    silent: true,
    symbol: 'none',
    lineStyle: { color: '#fbbf24', type: 'dashed', width: 1.5 },
    label: {
      formatter: 'AVG: {c}',
      color: '#fbbf24',
      fontSize: 11,
      fontFamily: 'Space Mono'
    },
    data: [
      { type: 'average', name: 'Average' },
      // Fixed value:
      // { yAxis: 1000000, name: 'Target' }
      // Percentile (manual):
      // { yAxis: computedP50, name: 'Median' }
    ]
  }
}]
```

### Visual Map (Color Encoding)

```javascript
visualMap: {
  // Continuous gradient:
  type: 'continuous',
  min: 0, max: 100,
  inRange: { color: ['#334155', '#f472b6'] },  // low → high
  textStyle: { color: '#94a3b8' },
  // Piecewise (discrete buckets):
  // type: 'piecewise',
  // pieces: [
  //   { min: 0, max: 50, color: '#334155', label: 'Low' },
  //   { min: 50, max: 100, color: '#f472b6', label: 'High' }
  // ]
}
```

### DataZoom (Scroll/Filter)

```javascript
dataZoom: [
  {
    type: 'slider',          // 'inside' for mouse wheel
    start: 0, end: 100,     // Initial view percentage
    xAxisIndex: [0],
    bottom: 0,
    height: 20,
    borderColor: '#334155',
    backgroundColor: '#1e293b',
    fillerColor: 'rgba(244,114,182,0.2)',
    handleStyle: { color: '#f472b6' },
    textStyle: { color: '#94a3b8', fontSize: 10 }
  }
]
```

### Dataset (Declarative Data)

```javascript
// Instead of inline data per series, use dataset:
dataset: {
  source: [
    ['week',    'Services', 'Retail', 'Gas'],
    ['08/04',   8312000,    2451000,  1890000],
    ['08/11',   8540000,    2380000,  1920000]
  ]
},
// Then series just declare type + encode:
series: [
  { type: 'bar', encode: { x: 'week', y: 'Services' } },
  { type: 'bar', encode: { x: 'week', y: 'Retail' } }
]

// Object array format also works:
dataset: {
  source: [
    { week: '08/04', services: 8312000, retail: 2451000 },
    { week: '08/11', services: 8540000, retail: 2380000 }
  ]
}
```

### Data Transforms (Filter/Sort)

```javascript
dataset: [
  { source: rawData },
  {
    transform: {
      type: 'filter',
      config: { dimension: 'category', '=': 'Services' }
    }
  },
  {
    transform: {
      type: 'sort',
      config: { dimension: 'value', order: 'desc' }
    }
  }
],
series: [
  { type: 'bar', datasetIndex: 1 },  // Uses filtered data
  { type: 'bar', datasetIndex: 2 }   // Uses sorted data
]
```

---

## 4. Event Handling

### Mouse Events on Chart Elements

```javascript
chart.on('click', function(params) {
  // params.componentType: 'series', 'markLine', 'markPoint', etc.
  // params.seriesType: 'bar', 'line', etc.
  // params.seriesIndex, params.dataIndex, params.name, params.value
  // params.color: the color of the clicked item
  console.log('Clicked:', params.name, params.value);
});

// Target specific series:
chart.on('click', 'series.bar', handler);
chart.on('click', { seriesName: 'Services' }, handler);
```

### Component Events

```javascript
chart.on('legendselectchanged', function(params) {
  var isSelected = params.selected[params.name];
});

chart.on('datazoom', function(params) {
  var start = params.start;
  var end = params.end;
});

chart.on('brushselected', function(params) {
  // Brush selection data
});
```

### Programmatic Actions (dispatchAction)

```javascript
// Highlight a data point:
chart.dispatchAction({ type: 'highlight', seriesIndex: 0, dataIndex: 5 });
chart.dispatchAction({ type: 'downplay', seriesIndex: 0, dataIndex: 5 });

// Show tooltip programmatically:
chart.dispatchAction({ type: 'showTip', seriesIndex: 0, dataIndex: 5 });
chart.dispatchAction({ type: 'hideTip' });

// Toggle legend selection:
chart.dispatchAction({ type: 'legendToggleSelect', name: 'Services' });
```

### Blank Area Detection

```javascript
chart.getZr().on('click', function(event) {
  if (!event.target) {
    // Clicked on empty canvas — clear selection, reset zoom, etc.
  }
});
```

---

## 5. Performance & Rendering

### Large Datasets

- **progressive rendering**: Auto-enabled for >5K points. Set `progressive: 400` (points per frame)
- **largeThreshold**: Default 2000. Above this, ECharts uses optimized large-data mode
- **sampling**: `'lttb'` (Largest Triangle Three Buckets) for line charts with >10K points
- **TypedArray**: ECharts uses internally for memory efficiency

```javascript
series: [{
  type: 'line',
  large: true,
  largeThreshold: 2000,
  sampling: 'lttb',        // or 'average', 'min', 'max', 'sum'
  progressive: 500,
  data: bigArray
}]
```

### Renderer Selection

```javascript
// SVG (better for <1K elements, crisp export, smaller file):
echarts.init(el, null, { renderer: 'svg' });

// Canvas (default — better for >1K elements, animations):
echarts.init(el, null, { renderer: 'canvas' });
```

### Resize Handling

```javascript
window.addEventListener('resize', function() {
  charts.forEach(function(c) { c.instance.resize(); });
});
```

### Dispose on Unmount

```javascript
// Always dispose when removing from DOM to prevent memory leaks:
chart.dispose();
```

---

## 6. Animation & Transitions

```javascript
{
  animation: true,
  animationDuration: 1000,
  animationEasing: 'cubicOut',
  // Per-item stagger:
  animationDelay: function(idx) { return idx * 50; },
  // Update animation (when data changes):
  animationDurationUpdate: 500,
  animationEasingUpdate: 'cubicInOut'
}
```

### Universal Transitions (v5.0+)

Smooth morphing when switching chart types:

```javascript
series: [{
  type: 'bar',
  universalTransition: true,
  id: 'myData'  // Same id enables transition
}]
// Later, update with:
chart.setOption({
  series: [{ type: 'pie', universalTransition: true, id: 'myData' }]
});
```

---

## 7. Graphic Component (Custom Drawing)

Draw arbitrary shapes on the chart canvas:

```javascript
graphic: [
  {
    type: 'text',
    left: 'center', top: 50,
    style: {
      text: 'Annotation',
      fontSize: 14,
      fill: '#fbbf24'
    }
  },
  {
    type: 'rect',
    shape: { x: 100, y: 200, width: 80, height: 30 },
    style: {
      fill: 'rgba(244,114,182,0.2)',
      stroke: '#f472b6'
    }
  },
  {
    type: 'image',
    style: {
      image: 'path/to/logo.png',
      x: 10, y: 10, width: 40, height: 40
    }
  }
]
```

---

## 8. setOption Behavior

### Merge vs Replace

```javascript
// DEFAULT: Merge mode — new option merges into existing
chart.setOption(partialOption);
// Only the properties you specify are updated; others preserved

// NOT-MERGE: Full replace — completely replaces the option
chart.setOption(fullOption, true);
// Use for chart type toggle, major restructuring

// REPLACE-MERGE (v5+): Replace specific components by id
chart.setOption(newOption, { replaceMerge: ['series'] });
// Replaces series array but merges everything else
```

**When to use notMerge:**
- Toggling chart type (line ↔ bar)
- Removing series that existed before
- Any time partial merge leaves stale properties

---

## 9. Lessons from Dashboard Building

1. **`JSON.parse/stringify` kills formatters** — always use `deepClone()` that preserves functions
2. **`setOption()` merges by default** — use `setOption(opt, true)` for type toggles
3. **Label cycling must only toggle `show`** — setting `formatter: undefined` permanently destroys it
4. **Series-level `itemStyle.color` required** for legend color inheritance
5. **ThemeRiver does NOT support rank reordering** — use rank-ordered stacked bars or bump chart instead
6. **Rich text `width`/`height` only work when `rich:{}` is defined** at the label level
7. **Font sizes tend too small on dark backgrounds** — plan for +2px from your first guess
8. **Right-side vertical legends** (`right:0, orient:'vertical'`) avoid axis overlap
9. **`containLabel: true` on grid** prevents label clipping — use it unless you need pixel-precise layout
10. **Tooltip HTML formatter** is more flexible than template strings — use for multi-line, colored swatches

---

## 10. Connected Charts — Linked Tooltips & Zoom

**One line** to synchronize hover, zoom, and highlights across multiple charts:

```javascript
// After creating all chart instances:
echarts.connect([chart1, chart2, chart3, chart4]);

// Or connect by group name:
chart1.group = 'dashboard';
chart2.group = 'dashboard';
echarts.connect('dashboard');
```

**What syncs automatically:**
- Tooltip appears on ALL connected charts at the same data index
- DataZoom range syncs across charts
- Legend selection syncs

**axisPointer linking** (finer control — crosshair sync without full connect):

```javascript
// Add to each chart that shares an x-axis:
axisPointer: {
  link: [{ xAxisIndex: 'all' }],
  type: 'line',
  lineStyle: { color: '#fbbf24', width: 1 }
}
```

---

## 11. Toolbox — Built-in Toolbar

ECharts ships a full analyst toolbar. These features replace custom JS code:

```javascript
toolbox: {
  show: true,
  right: 10,
  top: 0,
  iconStyle: { borderColor: '#94a3b8' },
  emphasis: { iconStyle: { borderColor: '#e2e8f0' } },
  feature: {
    // Save as PNG — replaces custom 'e' key export
    saveAsImage: {
      pixelRatio: 2,           // Retina-quality export
      backgroundColor: '#0f172a',
      title: 'Save'
    },

    // Toggle chart type — replaces custom 't' key toggle
    magicType: {
      type: ['line', 'bar', 'stack'],
      title: { line: 'Line', bar: 'Bar', stack: 'Stack' }
    },

    // Show raw data table behind the chart
    dataView: {
      readOnly: true,
      title: 'Data',
      lang: ['Data View', 'Close', 'Refresh'],
      backgroundColor: '#1e293b',
      textColor: '#e2e8f0',
      textareaColor: '#0f172a',
      textareaBorderColor: '#334155'
    },

    // Brush-to-zoom on x-axis
    dataZoom: {
      title: { zoom: 'Zoom', back: 'Reset' }
    },

    // Reset to original view
    restore: { title: 'Reset' }
  }
}
```

**When to use vs custom keyboard:** Toolbox is visual (icon clicks). Keep keyboard shortcuts for power users; toolbox for casual viewers. They can coexist.

---

## 12. Bar Racing — Animated Rank Changes

Native animated ranking chart that auto-plays through time periods. Bars smoothly reorder as categories overtake each other.

```javascript
// Setup: one setInterval frame per time period
var currentIdx = 0;

function updateRace() {
  var weekData = CHART_CATEGORIES.map(function(cat) {
    return { name: cat, value: CHART_RAW[cat][currentIdx] };
  });
  weekData.sort(function(a, b) { return a.value - b.value; });

  chart.setOption({
    yAxis: { data: weekData.map(function(d) { return d.name; }) },
    series: [{
      data: weekData.map(function(d) {
        return { value: d.value, itemStyle: { color: CHART_COLORS[d.name] } };
      })
    }],
    graphic: [{
      type: 'text',
      right: 50, bottom: 60,
      style: {
        text: WEEKS[currentIdx],
        font: 'bold 36px Space Mono',
        fill: 'rgba(100, 116, 139, 0.3)'
      }
    }]
  });
  currentIdx = (currentIdx + 1) % WEEKS.length;
}

// Initial config:
var opt = {
  yAxis: {
    type: 'category',
    inverse: true,
    animationDuration: 300,
    animationDurationUpdate: 300
  },
  xAxis: {
    type: 'value',
    max: 'dataMax',
    axisLabel: { formatter: function(v) { return fmtShort(v); } }
  },
  series: [{
    type: 'bar',
    realtimeSort: true,
    label: {
      show: true,
      position: 'right',
      formatter: function(p) { return fmt(p.value); }
    }
  }],
  animationDuration: 0,
  animationDurationUpdate: 1500,
  animationEasing: 'linear',
  animationEasingUpdate: 'linear'
};

// Play: update every 1.5s
setInterval(updateRace, 1500);
```

**Key config:**
- `realtimeSort: true` — bars reorder automatically on data update
- `yAxis.inverse: true` — #1 rank at top
- `animationDurationUpdate: 1500` — smooth transition speed
- Big date watermark via `graphic` component

---

## 13. markArea — Shade Time Regions

Highlight date ranges directly on the chart data area:

```javascript
series: [{
  // ... your series config ...
  markArea: {
    silent: true,
    itemStyle: { color: 'rgba(251,191,36,0.06)' },
    data: [
      [
        { xAxis: '2025/11/24', name: 'Holiday Season' },
        { xAxis: '2025/12/29' }
      ]
    ],
    label: {
      show: true,
      position: 'insideTop',
      formatter: '{b}',
      color: '#fbbf24',
      fontSize: 10,
      fontFamily: 'Space Mono',
      fontStyle: 'italic'
    }
  }
}]
```

**markPoint** for single-point callouts:

```javascript
markPoint: {
  data: [
    { type: 'max', name: 'Peak' },
    { type: 'min', name: 'Trough' },
    // Fixed position:
    { coord: ['2025/12/15', 28600000], name: 'Holiday Peak', value: '$28.6M' }
  ],
  symbol: 'pin',
  symbolSize: 40,
  label: { color: '#e2e8f0', fontSize: 10, fontFamily: 'Space Mono' }
}
```

---

## 14. Universal Transition — Morphing Between Chart Types

Smooth cinematic animation when switching chart types (v5.2+). Bars morph into pie slices, scatter points coalesce into lines.

```javascript
// Enable on each series:
series: [{
  type: 'bar',
  id: 'spend',                    // Same id links the transition
  universalTransition: true,
  data: barData
}]

// Switch to pie — bars morph into slices:
chart.setOption({
  series: [{
    type: 'pie',
    id: 'spend',
    universalTransition: true,
    radius: ['30%', '70%'],
    data: pieData
  }]
});
```

**Drill-down with groupId** — bars split into sub-categories:

```javascript
// Top-level: each bar represents a group
series: [{
  type: 'bar',
  id: 'categories',
  universalTransition: true,
  data: [
    { name: 'Services', value: 240000000, groupId: 'services' },
    { name: 'Retail', value: 85000000, groupId: 'retail' }
  ]
}]

// On click, drill into 'Services' sub-categories:
chart.on('click', function(params) {
  chart.setOption({
    series: [{
      type: 'bar',
      id: 'categories',
      universalTransition: true,
      dataGroupId: 'services',    // Animate from the 'services' bar
      data: [
        { name: 'Consulting', value: 120000000 },
        { name: 'IT Services', value: 80000000 },
        { name: 'Maintenance', value: 40000000 }
      ]
    }]
  });
});
```

---

## 15. Brush Selection — Draw to Filter

Let users drag-select date ranges or data regions:

```javascript
brush: {
  toolbox: ['lineX', 'clear'],    // 'rect', 'polygon', 'lineX', 'lineY', 'keep', 'clear'
  xAxisIndex: 0,
  brushStyle: {
    borderWidth: 1,
    color: 'rgba(251,191,36,0.1)',
    borderColor: '#fbbf24'
  },
  outOfBrush: {
    colorAlpha: 0.2              // Dim unselected data
  }
}
```

**React to brush selection:**

```javascript
chart.on('brushselected', function(params) {
  var areas = params.batch[0].areas;
  if (areas.length) {
    var range = areas[0].coordRange;  // [startIdx, endIdx]
    // Filter other charts, update KPIs, etc.
  }
});
```

**Combine with toolbox** for the icon:

```javascript
toolbox: { feature: { brush: { type: ['lineX', 'clear'] } } }
```

---

## 16. Accessibility — ARIA & Decal Patterns

### Auto-generated Screen Reader Descriptions

```javascript
aria: {
  enabled: true,
  label: {
    description: 'Amazon Flex approved spend by MCC category, August 2025 through January 2026'
  }
}
```

ECharts auto-generates accessible descriptions from chart structure. Screen readers announce chart type, series count, data ranges.

### Decal Patterns (Colorblind-Safe)

```javascript
// One line to add patterns to ALL series:
aria: {
  enabled: true,
  decal: { show: true }
}

// Or per-series custom patterns:
series: [{
  itemStyle: {
    decal: {
      symbol: 'rect',           // 'circle', 'rect', 'roundRect', 'triangle', 'diamond', 'pin', 'arrow'
      symbolSize: 1,
      rotation: Math.PI / 4,    // 45-degree hatching
      color: 'rgba(0,0,0,0.15)',
      dashArrayX: 5,
      dashArrayY: 5
    }
  }
}]
```

Adds hatching/dots/stripes to chart fills alongside colors. Print-friendly on monochrome printers.

---

## 17. Timeline Component — Playable Data Scrubber

Built-in timeline bar for animating through data states:

```javascript
{
  baseOption: {
    timeline: {
      data: ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan'],
      autoPlay: true,
      playInterval: 2000,
      loop: true,
      bottom: 0,
      lineStyle: { color: '#334155' },
      itemStyle: { color: '#f472b6' },
      checkpointStyle: { color: '#fbbf24', borderColor: '#fbbf24' },
      controlStyle: { color: '#94a3b8', borderColor: '#94a3b8' },
      label: { color: '#94a3b8', fontFamily: 'Space Mono', fontSize: 10 }
    },
    // ... shared options (title, tooltip, grid, xAxis, yAxis) ...
  },
  options: [
    { series: [{ data: augData }] },    // Aug frame
    { series: [{ data: sepData }] },    // Sep frame
    { series: [{ data: octData }] },    // Oct frame
    // ... each frame overrides the baseOption
  ]
}
```

**Key config:**
- `autoPlay: true` — starts playing automatically
- `playInterval: 2000` — milliseconds per frame
- `loop: true` — cycles continuously
- Each `options[i]` merges into `baseOption` for that frame

---

## 18. Custom Series (renderItem) — Draw Anything

The escape hatch for charts ECharts doesn't have natively:

```javascript
series: [{
  type: 'custom',
  renderItem: function(params, api) {
    // api.value(dimIdx) — get data value
    // api.coord([x, y]) — convert data to pixel
    // api.size([dataWidth, dataHeight]) — get pixel size of data range

    var x = api.coord([api.value(0), 0])[0];
    var y = api.coord([0, api.value(1)])[1];
    var width = api.size([1, 0])[0] * 0.6;
    var height = api.coord([0, 0])[1] - y;

    return {
      type: 'group',
      children: [
        {
          type: 'rect',
          shape: { x: x - width / 2, y: y, width: width, height: height },
          style: api.style({ fill: '#f472b6' })
        },
        {
          type: 'text',
          style: {
            text: fmt(api.value(1)),
            x: x, y: y - 10,
            textAlign: 'center',
            fill: '#e2e8f0',
            fontSize: 10
          }
        }
      ]
    };
  },
  data: myData
}]
```

**Built-in return types:** `rect`, `circle`, `ring`, `sector`, `arc`, `polygon`, `polyline`, `line`, `bezierCurve`, `text`, `image`, `group`

**Use cases:** Error bars, confidence intervals, Gantt charts, lollipop charts, violin plots, custom waterfall, candlestick variants, swim lane diagrams.

---

## 19. Keyframe Animations

Multi-step animations on graphic elements and custom series:

```javascript
graphic: [{
  type: 'circle',
  shape: { cx: 200, cy: 200, r: 20 },
  style: { fill: '#f472b6' },
  keyframeAnimation: [{
    duration: 2000,
    loop: true,
    keyframes: [
      { percent: 0, scaleX: 1, scaleY: 1, style: { opacity: 1 } },
      { percent: 0.5, scaleX: 1.5, scaleY: 1.5, easing: 'cubicOut', style: { opacity: 0.6 } },
      { percent: 1, scaleX: 1, scaleY: 1, style: { opacity: 1 } }
    ]
  }]
}]
```

**Custom series enter/leave animations:**

```javascript
// In renderItem return:
return {
  type: 'rect',
  shape: { ... },
  transition: ['shape', 'style'],    // Animate these props on update
  enterFrom: { style: { opacity: 0 }, x: -100 },   // Entry animation
  leaveTo: { style: { opacity: 0 }, x: 100 }        // Exit animation
};
```

**Use cases:** Pulsing KPI indicators, attention-drawing annotations, loading spinners, data point entry effects.

---

## 20. State Management — emphasis / blur / select

Three built-in states for interactive highlighting:

```javascript
series: [{
  // Emphasis: hover highlighting (default behavior)
  emphasis: {
    focus: 'series',              // Dim everything except hovered series
    blurScope: 'coordinateSystem', // or 'global', 'series'
    itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0,0,0,0.3)' },
    label: { show: true, fontSize: 14 }
  },

  // Blur: how OTHER elements look when something is emphasized
  blur: {
    itemStyle: { opacity: 0.15 },
    lineStyle: { opacity: 0.15 }
  },

  // Select: click-to-select (persists, unlike hover)
  select: {
    itemStyle: { borderWidth: 2, borderColor: '#fbbf24' },
    label: { show: true, fontWeight: 'bold' }
  },
  selectedMode: 'multiple'         // 'single', 'multiple', 'series', false
}]

// Listen to selection:
chart.on('selectchanged', function(params) {
  // params.fromAction: 'select' or 'unselect'
  // params.selected: array of selected data
});
```

**`emphasis.disabled: true`** — turn off hover effects for specific series.

---

## Dependencies

- **ECharts 5.5.0** via CDN: `https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js`
- For 3D: `https://cdn.jsdelivr.net/npm/echarts-gl@2/dist/echarts-gl.min.js`
- For maps: register map JSON via `echarts.registerMap('mapName', geoJson)`

---

## Related Files

| Need | File |
|------|------|
| Dashboard builder (keyboard, registry, interactivity) | `.claude/skills/interactive-dashboard-builder/SKILL.md` |
| Design guidelines (color, layout, KPI, storytelling) | `shared/reference/dashboard-design-guidelines.md` |
| Chart type directory with BI use cases | `docs/guides/echarts-chart-directory.md` |
| ECharts cheat sheet | https://echarts.apache.org/en/cheat-sheet.html |
| ECharts examples gallery | https://echarts.apache.org/examples/en/index.html |
| ECharts full option reference | https://echarts.apache.org/en/option.html |
