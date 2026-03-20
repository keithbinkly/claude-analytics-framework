# Annotation & Labeling Decision System

A decision flow for labeling ECharts visualizations without visual feedback.
This is not a principle list — it is a chart-type-indexed lookup with specific
thresholds, ECharts config, and collision strategies.

**Sources:** Berinato (*Good Charts*), Yau (*Data Points*), Cairo (*Truthful Art*,
*Art of Insight*), Jones (*Avoiding Data Pitfalls*), Muth (Datawrapper), FT style,
designer napkin (empirical failures from data-centered.com builds).

---

## The Two Tests — Run Before Adding ANY Label

**Test 1: "Is each individual value important to expressing my idea?"** (Berinato, p. 127)
If NO → don't label every point. Let the pattern be the message.
If YES → you may need a table alongside the chart, not 20 labels.

**Test 2: "No treasure hunts."** (Groeger, in Cairo Ch. 17)
If a pattern IS the story → it MUST be annotated visibly.
If a pattern is NOT the story → it does NOT need a label.

Over-labeling and under-annotating are equally costly failures. One overwhelms;
the other hides the point.

**Principle hierarchy:** When tests conflict, "No treasure hunts" (Test 2) wins.
If a named entity from the narrative text must be identifiable on the chart, label it
even if density thresholds say "tooltip only." A reader searching for "Computer
Programmers" on a 341-point scatter because the text references it — that's a
treasure hunt. Label the named story points; let hideOverlap handle the rest.

---

**Hard floor: all chart text ≥ 11px.** Below 11px, readability drops sharply (ONS, Datawrapper). This includes data labels, markPoint callouts, axis labels, and annotation text. No exceptions.

## Quick Lookup: Chart Type → Label Strategy

| Chart Type | Data Density | Strategy | ECharts Config |
|------------|-------------|----------|---------------|
| **Line** ≤3 series | Low | endLabel, hide legend | `endLabel: {show:true}, legend:{show:false}` |
| **Line** 4-5 series | Medium | endLabel, thin legend as fallback | `endLabel: {show:true}` with offset stagger |
| **Line** 6+ series | High | Top N colored + labeled, rest gray, no label | Gray `lineStyle`, only hero series get `endLabel` |
| **Bar** ≤8 bars | Low | Label each bar | `label: {show:true, position:'top'}` |
| **Bar** 9-15 bars | Medium | Label max/min/story bars only | Selective `label` via data item override |
| **Bar** 16+ bars | High | No data labels, axis only | `label: {show:false}`, annotate with `markPoint` |
| **Bar** (horizontal) | Any | Label right of bar end | `label: {show:true, position:'right'}` |
| **Bar** (stacked seg) | ≥10% share | Inside segment | `label: {show:true, position:'inside'}` |
| **Bar** (stacked seg) | 5-9% share | Inside if text fits, else omit | Conditional per segment width |
| **Bar** (stacked seg) | <5% share | No label, tooltip only | `label: {show:false}` |
| **Scatter** ≤10 pts | Low | Label each point | `label: {show:true, position:'right'}` + per-point override |
| **Scatter** 11-30 pts | Medium | Label outliers + named points only | Per-item `label` in data, default `show:false` |
| **Scatter** 31+ pts | High | No labels, tooltip only | `label: {show:false}`, `emphasis.label: {show:true}` |
| **Pie/Donut** ≥20% slice | - | Inside centered | `label: {position:'inside'}` |
| **Pie/Donut** 10-19% slice | - | Inside near edge | `label: {position:'inside'}` (end) |
| **Pie/Donut** 5-9% slice | - | Outside with leader line | `label: {position:'outside'}, labelLine: {show:true}` |
| **Pie/Donut** <5% slice | - | Merge into "Other" | Combine before charting, keep ≤6 total |
| **Heatmap** ≤30 cells | Low | Value in each cell | `label: {show:true, fontSize:10}` |
| **Heatmap** 31-100 cells | Medium | Label extremes only | Default `show:false`, override for min/max cells |
| **Heatmap** 100+ cells | High | No cell labels | Rely on `visualMap` + tooltip |
| **Treemap** | Any | Abbreviate > rotate | `label: {formatter:'{b}'}`, short names, never `rotate:90` |

---

## 1. Data Labels — What, Where, How

### 1.1 WHAT to Label

**The value test:** Label a data point only when its specific value adds to the story.
"43% approval" on the outlier bar is useful. "43%" on one of 25 identical-looking bars
is noise.

**Thresholds (synthesized from 6 sources — no single book gives numeric cutoffs):**

| Element Count | Label Strategy |
|---------------|---------------|
| 1-7 | Label all — each value is distinguishable |
| 8-12 | Label story points only (max, min, outlier, highlighted) |
| 13-20 | Annotate 1-2 specific points with `markPoint`, no per-element labels |
| 21+ | No data labels at all; axis + tooltip + narrative text carry the values |

**When to use a table instead:** If the reader must read every labeled value to
understand the point → the artifact should be a table, not a chart. A chart shows
pattern; a table shows precision. (Berinato p. 128, Jones p. 147)

### 1.2 WHERE to Place Labels

**By chart type (ECharts `label.position` values):**

```
Line chart:
  endLabel: { show: true, formatter: '{a}', color: <series-color>,
    fontSize: 11, fontFamily: "'JetBrains Mono', monospace",
    offset: [8, 0] }
  → Grid right margin must be ≥80px to fit labels
  → If 4-5 series, stagger offset: [8, -6], [8, 6] alternating

Bar chart (vertical):
  Short bars (<40px tall): label: { position: 'top', distance: 4 }
  Tall bars (>60px): label: { position: 'insideTop', distance: 8 }
  → Never position: 'bottom' (conflicts with axis baseline)

Bar chart (horizontal):
  label: { position: 'right', distance: 8 }
  Wide bars (label < 60% of bar width): label: { position: 'insideRight' }

Scatter plot:
  Default: label: { position: 'right', distance: 6 }
  Near right edge: label: { position: 'left' }
  Dense cluster: use per-point position map (see Section 4)

Slope chart:
  Left points: label: { position: 'left' }
  Right points: label: { position: 'right' }
  Both ends labeled. Never mid-line.
```

**The proximity rule (Gestalt):** Every pixel of distance between label and referent
costs cognitive effort. "The further away the label, the harder it is to connect it
to its visual counterpart." (Berinato, p. 116)

- Direct label on the element = 0 cost
- Label 10px away = low cost
- Legend in a box = high cost (requires eye round-trip)
- Footnote or caption = highest cost

### 1.3 HOW to Style Labels

**Typography hierarchy (mandatory — do not invert):**

| Element | Size | Weight | Font | Color |
|---------|------|--------|------|-------|
| Chart title | 16-18px | 700 | Sans (Cabinet/Space Grotesk) | `var(--ink)` |
| Subtitle | 13-14px | 400 | Sans | `var(--ink-secondary)` |
| Axis title | 12px | 400 | Sans | `var(--ink-muted)` |
| Axis labels | 10-11px | 400 | Mono (JetBrains) | `var(--ink-muted)` |
| Data labels | 10-12px | 500-600 | Mono | Match series color |
| Annotations | 10-11px | 400 | Mono or Sans | `var(--ink-muted)` or series color |
| Source line | 9-10px | 400 | Sans | `var(--ink-dim)` |

**Minimum readable size:** 11px (ONS standard, Datawrapper guidance). Below 11px,
readability drops sharply for body-copy fonts. The prior 9px floor was too aggressive.

**Color matching rule:**
- Data labels → same color as the series they label
- Annotations → `ink-muted` OR series color (if pointing to specific series)
- Axis labels → `ink-muted` always
- Exception: label over dark fill → white/`ink` for contrast (4.5:1 WCAG minimum)

**One emphasis only (belt-and-suspenders rule, Berinato p. 129):**
A label gets ONE distinguishing treatment: size OR weight OR color. Not all three.
The "outlier value" label can be bold OR colored — not bold AND colored AND larger.
**Exception:** Contrast-required color doesn't count as emphasis. White text inside
a dark bar is WCAG compliance, not decoration — it doesn't consume the "one emphasis"
budget. You can still add ONE actual emphasis (bold OR size) on top of the contrast color.

---

## 2. Annotations — Contextual Text on Charts

### Annotation vs. Data Label

| | Data Label | Annotation |
|---|-----------|------------|
| Answers | "What is the value here?" | "What does this mean?" |
| Example | "43%" above a bar | "Recession begins →" with arrow |
| Anchored to | A specific data point | A region, event, or pattern |
| When to use | Precision matters | Context matters |

Both can coexist. A bar chart can have 2 labeled bars (data labels) AND a markLine
annotation ("Industry average: 37%").

### When Annotations Are Mandatory

1. **External events explain visible patterns** — "COVID lockdowns began here" on a
   trend inflection. The reader cannot supply this context themselves.
   (Yau Ch.6: the FlightAware example — chart is meaningless without annotation)

2. **The pattern IS the story** — if your title says "Revenue stalled in Q3," the Q3
   region needs a visible annotation. Otherwise: treasure hunt.
   (Groeger: "No treasure hunts!")

3. **Reference lines exist** — any horizontal/vertical reference line (target, average,
   threshold) MUST be labeled. A bare line is uninterpretable.

### ECharts Annotation Tools

```javascript
// Reference line with label
markLine: {
  silent: true, symbol: 'none',
  lineStyle: { type: 'dashed', color: CLR.inkDim + '60' },
  data: [{
    yAxis: 37,
    label: {
      show: true, position: 'insideEndTop',
      formatter: 'Industry avg: 37%',
      fontSize: 10, fontFamily: mono, color: CLR.inkMuted
    }
  }]
}

// Point annotation (callout)
markPoint: {
  symbol: 'circle', symbolSize: 0,
  data: [{
    coord: [xValue, yValue],
    label: {
      show: true, position: 'top', distance: 10,
      formatter: '{a|Peak: 342K}',
      rich: {
        a: {
          fontSize: 10, fontFamily: mono, color: CLR.ink,
          backgroundColor: CLR.surface + 'ee',
          borderColor: CLR.inkDim + '40',
          borderWidth: 1, borderRadius: 3, padding: [3, 6]
        }
      }
    }
  }]
}

// Shaded region (markArea — preferred over text boxes, Gestalt enclosure)
markArea: {
  silent: true, itemStyle: { color: CLR.accent + '15' },
  data: [[{xAxis: startDate}, {xAxis: endDate}]],
  label: {
    show: true, position: 'insideTop',
    formatter: 'Crisis period', fontSize: 10, color: CLR.inkMuted
  }
}
```

### In Split Layouts: Text Column IS the Annotation

In magazine-style split layouts (chart + text side by side), do NOT use HTML overlay
annotations with arrows. The text column itself serves as the annotation layer.
Use color-coded inline `<span>` elements to reference specific data points.

(Designer napkin, 2026-03-15: "Don't annotate split-layout charts with overlays.
The text column IS the annotation." Keith approved.)

---

## 3. Legends — The Fallback

### The Fallback Hierarchy

When direct labeling fails, fall back in this order:

```
1. Direct labels (ideal — on/near the element)
   ↓ if collisions
2. Selective labeling (only story points)
   ↓ if still cluttered
3. Abbreviation (shorten labels)
   ↓ if abbreviation is unclear
4. Leader lines (offset labels to clear area)
   ↓ if too many leader lines cross
5. Small multiples (split into panels)
   ↓ if comparison across panels is needed
6. Legend (last resort for identification)
   ↓ if interactive
7. Tooltip (interactive-only; unacceptable for static/print)
```

### Legend Rules When You Must Use One

- **Order matches chart:** Legend sequence = chart visual sequence.
  Largest-to-smallest bars → legend lists largest-to-smallest.
  (Designer napkin: "bar chart sort direction mismatching legend")

- **Position:** Immediately below title or above chart, NOT in a distant sidebar.
  Horizontal layout preferred: `legend: { top: 4, left: 'center', orient: 'horizontal' }`

- **Style:** Small, unobtrusive. `fontSize: 9-10`, `itemGap: 12`, `itemWidth: 12`.
  The legend should recede — it's infrastructure, not the story.

- **≤3 series:** endLabel replaces legend entirely. `legend: { show: false }`.
  This is the FT technique: end-of-line labels + no legend.

---

## 4. Collision Avoidance — Native ECharts First, Manual Heuristics Second

**Principle: Let the rendering engine place labels.** ECharts knows where every
element is after layout. Use its native collision features BEFORE writing manual
position logic. Manual heuristics are fallbacks, not defaults.

### 4.1 Native ECharts Label Features (Use These First)

```
FEATURE                    WHAT IT DOES                              WHEN TO USE
─────────────────────────────────────────────────────────────────────────────────
labelLayout.moveOverlap    Auto-shift colliding labels                Multi-series endLabels
  'shiftY'                   vertically                               Line charts
  'shiftX'                   horizontally                             Horizontal bar labels

labelLayout.hideOverlap    Auto-hide labels that collide              Dense scatter, bar charts
  true                       hides lower-priority labels               When some labels are OK to lose

labelLayout (function)     Per-label position adjustment              Scatter plots, custom layouts
                           Receives: labelRect, rect, align           Replaces manual quadrant logic
                           Returns: {x, y, dx, dy, rotate, align}    ECharts KNOWS where things are

avoidLabelOverlap          Native pie/donut collision handler         All pie/donut charts
  true                       repositions labels automatically          Always enable

label.alignTo              Align pie labels to container edge         Pie charts with outside labels
  'edge'                     newspaper-style clean alignment
  'labelLine'                align to leader line endpoint

axisLabel.hideOverlap      Auto-hide overlapping axis ticks           Dense category/time axes
  true                       ECharts 5.4+

label.overflow             Auto-truncate with ellipsis                Treemap, dense bars
  'truncate'                 clips text to available space
  'break'                    wraps text to next line

markPoint type:'max'       Auto-find max/min value                   Annotation callouts
markPoint type:'min'       No manual coord needed                    Peak/trough labels
markPoint type:'average'   ECharts computes the position             Reference annotations
```

### 4.2 The labelLayout Function — The Power Tool

For scatter plots and complex layouts, use `labelLayout` as a function instead of
manual position maps. ECharts passes you the computed label position — you adjust it:

```javascript
// ECharts knows where every label landed. You adjust from there.
labelLayout: function(params) {
  // params.labelRect — bounding box of the label as rendered
  // params.rect — bounding box of the data item (bar, point, etc.)
  // params.labelLinePoints — leader line coords (pie charts)
  // params.align, params.verticalAlign — current alignment
  return {
    // Nudge, don't replace — work WITH the engine's placement
    dy: params.labelRect.y < 20 ? 10 : 0,  // push down if near top edge
    moveOverlap: 'shiftY'                    // THEN let engine resolve remaining collisions
  };
}
```

**This replaces the manual quadrant heuristic** from earlier versions of this doc.
ECharts' spatial awareness is better than our data-shape guesses.

### 4.3 markPoint Auto-Positioning

Don't manually find peak coordinates. ECharts does it:

```javascript
// PREFER: Let ECharts find the max
markPoint: {
  data: [
    { type: 'max', name: 'Peak' },
    { type: 'min', name: 'Trough' }
  ],
  label: {
    show: true, position: 'top', distance: 12,
    formatter: function(p) { return p.name + ': ' + fmt(p.value); },
    fontSize: 11, fontFamily: mono, color: CLR.ink
  },
  symbolSize: 0  // invisible dot, visible label
}

// USE COORD ONLY when the story point isn't the statistical max/min
// e.g., "2019 inflection" on a line that continues rising after
markPoint: {
  data: [{
    coord: ['2019', specificValue],
    label: { /* rich text callout */ }
  }]
}
```

### 4.4 Per-Chart-Type Native Config

**Line charts (multi-series):**
```javascript
// Step 1: endLabel on each series
endLabel: { show: true, formatter: '{a}', color: seriesColor, fontSize: 11 },
// Step 2: Let ECharts resolve collisions
labelLayout: { moveOverlap: 'shiftY' },
// Step 3: Budget grid margin
grid: { right: 140 }  // wide enough for longest series name
```

**Scatter plots:**
```javascript
// Step 1: Label story-relevant points only (default show:false)
data: points.map(p => ({
  value: [p.x, p.y],
  name: p.name,
  label: { show: p.isStoryPoint }  // selective
})),
// Step 2: Let ECharts handle collision
labelLayout: { hideOverlap: true, moveOverlap: 'shiftY' }
```

**Pie/Donut:**
```javascript
avoidLabelOverlap: true,  // ALWAYS enable
label: {
  alignTo: 'edge',         // newspaper-style alignment
  formatter: '{b}: {d}%',  // name + percentage
  overflow: 'truncate'     // auto-ellipsis for long names
},
labelLine: { show: true, length: 15, length2: 10 }
```

**Bar charts (axis labels):**
```javascript
axisLabel: {
  hideOverlap: true,  // auto-hide rather than rotate
  overflow: 'truncate',
  width: 80  // max label width before truncation
}
// STILL NEVER: rotate: 45 or rotate: 90
```

### 4.5 Manual Heuristics (Fallbacks When Native Features Aren't Enough)

Use these ONLY after native features have been tried:

**Grid margin budget** (designer napkin — the clipping trap):
```javascript
grid: {
  left: Math.max(60, longestYLabel * 8 + 20),
  right: hasEndLabel ? 140 : 20,
  top: 32,
  bottom: Math.max(28, longestXLabel > 8 ? 40 : 28),
  containLabel: false
}
```
ECharts clips silently. Test LONGEST label against margins.

**Reference line label clipping:**
`markLine` labels with `position: 'end'` need right margin space.
Fix: use `position: 'insideEndTop'` (inside the grid area) or widen `grid.right`.

**Manual scatter position map** (only if labelLayout function doesn't resolve):
```javascript
const labelOverrides = {
  'Transportation': 'top',
  'Services': 'left',
  'Other': 'bottom'
};
// Per-point: label: { position: labelOverrides[name] || 'right' }
```

---

## 5. ECharts-Specific Implementation Patterns

### 5.1 The endLabel Pattern (FT-Style Line Labels)

```javascript
series: [{
  name: 'Series A',
  type: 'line',
  data: [...],
  endLabel: {
    show: true,
    formatter: '{a}',           // series name
    color: seriesColor,          // match the line
    fontSize: 11,
    fontWeight: 500,
    fontFamily: "'JetBrains Mono', monospace",
    offset: [8, 0],
    distance: 6
  },
  labelLayout: {
    moveOverlap: 'shiftY'       // ECharts 5.4+ auto-collision resolver
  },
  label: { show: false }        // no per-point labels
}]
```

### 5.2 Selective Data Labels via Data Items

```javascript
// Label only specific bars (the story points)
data: values.map((v, i) => {
  const isStoryPoint = i === maxIdx || i === minIdx || highlights.includes(categories[i]);
  return {
    value: v,
    label: {
      show: isStoryPoint,
      position: 'top',
      formatter: '{c}%',
      color: isStoryPoint ? accentColor : undefined,
      fontSize: 11,
      fontWeight: 600,
      fontFamily: "'JetBrains Mono', monospace"
    }
  };
})
```

### 5.3 Rich Text Callout Labels

```javascript
// PREFER: Auto-positioned at statistical extremes
markPoint: {
  data: [{ type: 'max', name: 'Peak' }],
  symbol: 'circle', symbolSize: 0,
  label: {
    show: true, position: 'top', distance: 12,
    formatter: '{bg|Peak: {c}}',
    rich: {
      bg: {
        fontSize: 11,
        fontFamily: "'JetBrains Mono', monospace",
        color: CLR.ink,
        backgroundColor: CLR.surface + 'ee',
        borderColor: CLR.inkDim + '40',
        borderWidth: 1, borderRadius: 3, padding: [4, 8]
      }
    }
  }
}

// MANUAL COORD: Only when the story point isn't a statistical extreme
markPoint: {
  symbol: 'circle', symbolSize: 0,
  data: [{
    coord: [x, y],  // use only when type:'max' won't find the right point
    label: {
      show: true, position: 'top', distance: 12,
      formatter: '{bg|Inflection: $1.2M in Q3}',
      rich: { bg: { /* same style */ } }
    }
  }]
}
```

### 5.4 hideOverlap for Dense Axes

```javascript
// Let ECharts auto-hide overlapping axis labels
axisLabel: {
  hideOverlap: true,  // ECharts 5.4+
  fontSize: 10,
  fontFamily: "'JetBrains Mono', monospace",
  color: CLR.inkMuted
}
```

### 5.5 Heatmap/Gradient Legend with Text Endpoints

```javascript
// Every color scale needs human-readable endpoint labels (designer napkin)
visualMap: {
  min: 0, max: 100,
  text: ['More complaints', 'Fewer'],  // NOT just numbers
  textStyle: { color: CLR.inkMuted, fontSize: 10 },
  inRange: { color: [lowColor, highColor] }
}
```

---

## 6. Anti-Pattern Checklist

Run this checklist before shipping any chart. Each item has burned us before.

| # | Anti-Pattern | Test | Fix |
|---|-------------|------|-----|
| L1 | Every value labeled | Count labels > 12? | Remove, keep story points only |
| L2 | Disconnected legend | Legend >100px from chart? | Direct label or position above chart |
| L3 | Belt-and-suspenders | Label has size AND bold AND color? | Pick one emphasis |
| L4 | Rotated/diagonal text | Any `rotate: 45` or `rotate: 90`? | Horizontal bars or abbreviate |
| L5 | Legend order ≠ chart order | Compare sequences | Match spatial order |
| L6 | Labels without units | "43" not "43%"? | Add unit to every label/tooltip |
| L7 | Treasure hunt | Key pattern unlabeled? | Annotate the story element |
| L8 | Title describes structure | "Revenue by Quarter"? | Assert: "Revenue stalled in Q3" |
| L9 | Grid clips labels | Longest label fits margins? | Budget grid margins manually |
| L10 | markLine label clipped | `grid.right` sufficient? | Use `insideEndTop` or widen margin |
| L11 | Treemap labels rotated | Narrow tile, `rotate: 90`? | Abbreviate (NE, MW) instead |
| L12 | Unlabeled micro-charts | Sparkline/mini-bar with no text? | Add monospace labels (FLX, WLT) |
| L13 | Hint references missing UI | "Hover legend" but no legend? | Audit hint text against rendered UI |
| L14 | Over-labeled trend | 20 quarterly values on a line? | Label START and END only |
| L15 | Color-coded title as legend | Title spans match >2 colors? | Use a real legend instead |

---

## 7. Mobile Considerations

| Rule | Desktop | Mobile (<600px) |
|------|---------|-----------------|
| Font size floor | 9px | 10px (nothing smaller) |
| endLabel | Standard offset | May need larger `grid.right` |
| Data labels | Show on story points | Reduce to top 1-2 only |
| Legend | Horizontal, inline | Wrap or move below chart |
| Annotations | Rich text callouts | Shorter text, larger touch targets |
| axis labels | Standard | `interval: 'auto'`, `hideOverlap: true` |

**Plot area height rule (Datawrapper, 2024):** Set height on the plot area (data only),
not the container. When long titles or annotations appear on mobile, the data space
stays constant — the container grows.

---

## Provenance

| Section | Primary Sources |
|---------|----------------|
| Tests 1-2 | Berinato (*Good Charts*), Groeger (in Cairo *Art of Insight*) |
| Quick Lookup | Synthesized from all 6 books + empirical data stories |
| Section 1 | Berinato, Yau, Cairo, craft guide synthesis |
| Section 2 | Yau, Groeger, designer decisions (2026-03-16) |
| Section 3 | Berinato p.116, FT style, designer napkin |
| Section 4 | Designer napkin (empirical failures), ECharts docs |
| Section 5 | ECharts API, existing data-story implementations |
| Section 6 | Designer napkin + book anti-patterns |
| Section 7 | Muth/Datawrapper, craft guide Section 8 |
| Web research | Datawrapper blog, ONS Service Manual, US Gov Data Standards, CFPB Design System, Evergreen, FT Visual Vocabulary, ECharts docs |
| Book re-mining | Berinato pp.115-132, Yau Ch.5-6, Cairo Figs.2.6-2.7, Groeger Ch.17, Jones Pitfall 5C/6A |
