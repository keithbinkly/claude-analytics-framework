# ECharts Chart Directory

> **How to use**: Start with the question you're asking about your data — how does it differ, how does it rank, how does it change — then scan the matching section below. Each entry has a `Choose when` (why this variant) and `Not when` (what disqualifies it, with the better alternative). Data shape tells you if your data fits. This organization follows the FT Visual Vocabulary's 8-category framework.
>
> Source: https://echarts.apache.org/examples/en/index.html

---

## 1. Deviation
**Question: How does this differ from a reference value?**

Use when comparing actual vs. expected, gains vs. losses, or divergence from a baseline. The reference point (zero, a target, a prior period) is as important as the values themselves.

> **Disambiguation — Deviation vs. Ranking:** When data has mixed positive and negative values, both sections may seem to fit. Ask: *is the zero line the story?* If the insight is "who gained vs. who lost" (the sign matters), you're in Deviation. If the insight is "who is biggest/smallest" and negatives are incidental, you're in Ranking — sort by absolute value and use Horizontal Bar.

---

- **Bar with Negative Values**: https://echarts.apache.org/examples/en/editor.html?c=bar-negative2
  - Data shape: 1 metric with positive and negative values, categorical axis
  - Choose when: showing gains vs. losses, deltas, net impact by category; the zero line is the story
  - Not when: all values are positive (use Horizontal Bar or Basic Bar under Ranking); sequential driver analysis (use Waterfall under Part-to-Whole)

- **Area Pieces (Threshold Shading)**: https://echarts.apache.org/examples/en/editor.html?c=area-pieces
  - Data shape: 1 metric over time with threshold rules
  - Choose when: visual signaling above/below a target (profit/loss, budget threshold, SLA breach); the line crossing the threshold is the key event
  - Not when: multiple thresholds at once — gets visually noisy (use markLine + conditional bar color instead); threshold is not meaningful (use Basic Area under Change over Time)

- **Waterfall Chart**: https://echarts.apache.org/examples/en/editor.html?c=bar-waterfall
  - Data shape: 1 metric, sequential additive/subtractive contributions leading to a total
  - Choose when: explaining how a total deviates from a starting point step-by-step (variance bridges, driver decomposition, P&L walk); each bar is a positive or negative deviation from the running total
  - Not when: contributions don't sum to a meaningful total; audience unfamiliar with waterfall convention; composition at a single point is the story (use Stacked Bar under Part-to-Whole)
  - (also under Part-to-Whole)

- **Confidence Band**: https://echarts.apache.org/examples/en/editor.html?c=confidence-band
  - Data shape: metric + upper/lower bound series
  - Choose when: showing uncertainty, forecasts, SLA ranges, or acceptable variance bands; deviation from the central line matters
  - Not when: bounds are so tight they visually collapse into the main line (just use a Basic Line under Change over Time)

---

## 2. Correlation
**Question: What is the relationship between these variables?**

Use when you want to show how two or more variables move together (or don't). The shape of the relationship — linear, clustered, dispersed — is the finding.

---

- **Basic Scatter**: https://echarts.apache.org/examples/en/editor.html?c=scatter-simple
  - Data shape: 2 metrics (X, Y), optional series grouping
  - Choose when: testing correlation between two variables; identifying outliers and clusters; ≥10 data points
  - Not when: one axis is time (use Basic Line under Change over Time); <10 data points (pattern won't be visible)

- **Regression Scatter**: https://echarts.apache.org/examples/en/editor.html?c=scatter-linear-regression
  - Data shape: 2 metrics + computed regression line
  - Choose when: asserting a linear trend/relationship with statistical backing
  - Not when: relationship is non-linear (use Exponential Regression below); audience won't understand regression context

- **Exponential Regression**: https://echarts.apache.org/examples/en/editor.html?c=scatter-exponential-regression
  - Data shape: 2 metrics with non-linear relationship
  - Choose when: diminishing returns or exponential growth pattern
  - Not when: relationship is roughly linear (use Regression Scatter above)

- **Bubble Chart**: https://echarts.apache.org/examples/en/editor.html?c=bubble-gradient
  - Data shape: 3 metrics (X, Y, Size), optionally Color for 4th
  - Choose when: comparing entities across 3 continuous dimensions (e.g., volume × rate × revenue)
  - Not when: only 2 dimensions (use Basic Scatter — bubble adds complexity for no reason); precise size comparison needed (area encoding is inaccurate)

- **Effect Scatter**: https://echarts.apache.org/examples/en/editor.html?c=scatter-effect
  - Data shape: 2 metrics with highlighted subset
  - Choose when: calling attention to specific points (top-N, anomalies) on a scatter
  - Not when: all points are equally important — ripple effect loses meaning when everything glows

- **Scatter Matrix**: https://echarts.apache.org/examples/en/editor.html?c=scatter-matrix
  - Data shape: 3+ metrics, all-pairs comparison
  - Choose when: exploratory analysis of multivariate relationships; you don't yet know which 2 variables matter
  - Not when: you already know which 2 variables matter (use Basic Scatter); presenting to non-analysts

- **Single Axis Scatter**: https://echarts.apache.org/examples/en/editor.html?c=scatter-single-axis
  - Data shape: 1 categorical axis, 1 metric
  - Choose when: showing distribution of a single metric across categories (strip plot); comparing density patterns per group
  - Not when: boxplot would better summarize the distribution (see Distribution); >100 points per category (overplotting)
  - (also under Distribution)

- **Punch Card**: https://echarts.apache.org/examples/en/editor.html?c=scatter-punchCard
  - Data shape: 2 categorical axes, 1 size metric
  - Choose when: sparse matrix where many cells are empty; emphasis on specific intersections (e.g., hour × day with few active slots)
  - Not when: dense matrix (use Heatmap on Cartesian below — color scales better than bubble size for dense grids)

- **Large Scale Scatter**: https://echarts.apache.org/examples/en/editor.html?c=scatter-large
  - Data shape: 10K+ points
  - Choose when: raw grain visualization where aggregation would lose the pattern (anomaly detection, density mapping)
  - Not when: <1K points (standard Basic Scatter works); must use SVG renderer (this needs Canvas)

- **Mixed Line and Bar**: https://echarts.apache.org/examples/en/editor.html?c=mix-line-bar
  - Data shape: 2 metrics on shared time axis, often dual Y-axes
  - Choose when: volume metric (bar) vs. rate metric (line) — e.g., spend + approval rate; the interplay between the two metrics is the insight
  - Not when: both metrics are same type (use dual lines under Change over Time); dual axes will mislead (check if scaling distorts the narrative)
  - (also under Change over Time)

- **Heatmap on Cartesian**: https://echarts.apache.org/examples/en/editor.html?c=heatmap-cartesian
  - Data shape: 2 categorical axes + 1 metric
  - Choose when: spotting patterns across two dimensions (cohort × age, hour × day, product × region); color gradient reveals correlation structure
  - Not when: one axis is continuous time with many points (use Basic Line); sparse matrix (use Punch Card above)

- **Heatmap Large**: https://echarts.apache.org/examples/en/editor.html?c=heatmap-large
  - Data shape: large grid (100×100+) + 1 metric
  - Choose when: high-density pattern scanning at scale; standard Heatmap on Cartesian would be too slow
  - Not when: standard heatmap handles the size; audience needs to read individual cell values

- **Correlation Matrix**: https://echarts.apache.org/examples/en/editor.html?c=matrix-correlation-heatmap
  - Data shape: N×N metric correlations
  - Choose when: identifying which KPIs co-move; exploratory correlation scan across many variables at once
  - Not when: you know which 2 variables to test (use Basic Scatter)

- **Basic Parallel**: https://echarts.apache.org/examples/en/editor.html?c=parallel-simple
  - Data shape: 4+ metrics per entity, many entities
  - Choose when: exploratory analysis of high-dimensional tradeoffs; brushing to filter clusters by profile shape
  - Not when: <4 dimensions (use Basic Scatter); presenting to non-analysts (unfamiliar chart type)

- **Force Layout**: https://echarts.apache.org/examples/en/editor.html?c=graph-force
  - Data shape: nodes + weighted links
  - Choose when: cluster and community detection; relationship density is the insight; which nodes are central
  - Not when: >200 nodes (hairball — aggregate first); quantitative comparison needed (use bar or scatter)

- **Graph on Cartesian**: https://echarts.apache.org/examples/en/editor.html?c=graph-grid
  - Data shape: nodes + links with quantitative X/Y positions
  - Choose when: network structure plus measurable node attributes (scatter + links); axis positions are meaningful
  - Not when: no meaningful axis positions exist (use Force Layout above)

---

## 3. Ranking
**Question: What is the relative position of items in an ordered list?**

Use when the order itself is the finding — which is highest, lowest, or where something sits in relation to others. Magnitude matters, but rank is the primary message.

---

- **Horizontal Bar**: https://echarts.apache.org/examples/en/editor.html?c=bar-y-category
  - Data shape: 1 metric, categorical Y-axis, sorted descending. For **grouped** comparison: 2–3 metrics per category (ECharts: multiple series, no `stack` — bars sit side-by-side)
  - Choose when: >7 categories; long category labels; ranking/leaderboard display; the reader needs to scan names quickly. **Grouped variant:** comparing 2–3 related metrics per category (e.g., hires vs. exits, actual vs. budget, this year vs. last year)
  - Not when: ≤5 short-label categories (vertical bar is more conventional); values have meaningful positive/negative sign (use Bar with Negative Values under Deviation — the zero line matters there); >3 metrics per category in grouped mode (too cluttered — use small multiples or a different chart type)

- **Lollipop Chart** (ECharts: scatter + custom line segments via `renderItem`, or bar with `barWidth: 2` + scatter overlay)
  - Data shape: 1 metric, categorical axis, sorted
  - Choose when: same use case as Horizontal Bar but for presentation/editorial contexts where visual lightness matters; fewer ink pixels makes the data points themselves more prominent; CFO/board decks
  - Not when: dashboard context where bar fill aids scanning; audience expects conventional bar charts

- **Basic Bar (Vertical)**: https://echarts.apache.org/examples/en/editor.html?c=bar-simple
  - Data shape: 1 metric, 1 series, ≤10 categories
  - Choose when: comparing magnitude across a small set of categories where rank order is clear
  - Not when: >10 categories (use Horizontal Bar above); categories have long labels (use Horizontal Bar); data is time-based (use Basic Line under Change over Time)
  - (also under Magnitude)

- **Bar with Background**: https://echarts.apache.org/examples/en/editor.html?c=bar-background
  - Data shape: 1 metric + maximum/capacity reference
  - Choose when: actual vs. capacity/goal in a single bar (utilization, completion rate); the gap to maximum is part of the ranking story
  - Not when: no meaningful maximum exists — background bar implies a ceiling

- **Axis Align with Tick**: https://echarts.apache.org/examples/en/editor.html?c=bar-tick-align
  - Data shape: 1 metric, 1 series, dense categorical axis
  - Choose when: precise bar-to-label alignment on dashboards with tight spacing; a styling refinement for ranked bar charts
  - Not when: standard bar alignment is fine (this is a styling variant, not a different chart type)

- **Bump Chart**: https://echarts.apache.org/examples/en/editor.html?c=bump-chart
  - Data shape: rank per category over time periods
  - Choose when: rank position changes are the story, not absolute values; showing who overtook whom
  - Not when: absolute values matter more than rank; >10 categories (unreadable)
  - (also under Change over Time)

---

## 4. Distribution
**Question: How are values spread across a range?**

Use when the shape of the data — where it clusters, how wide it spreads, whether it's skewed — is the insight. The full picture of values matters, not just the average or total.

---

- **Boxplot (Multiple Categories)**: https://echarts.apache.org/examples/en/editor.html?c=boxplot-multi
  - Data shape: distribution summary (min, Q1, median, Q3, max) per category
  - Choose when: comparing spread, skew, and outliers across groups; data volume per group is large enough to summarize
  - Not when: audience unfamiliar with boxplot convention; individual data points matter (use Single Axis Scatter under Correlation)

- **Histogram (Custom)**: https://echarts.apache.org/examples/en/editor.html?c=bar-histogram
  - Data shape: numeric values binned into frequency buckets
  - Choose when: showing how values are distributed (transaction sizes, response times, score spreads)
  - Not when: comparing distributions across multiple groups (use Boxplot above or overlaid density)

- **Single Axis Scatter**: https://echarts.apache.org/examples/en/editor.html?c=scatter-single-axis
  - Data shape: 1 categorical axis, 1 metric
  - Choose when: revealing individual data points and their spread within categories; fewer than ~50 points per category
  - Not when: boxplot would better summarize; >100 points per category (overplotting)
  - (also under Correlation)

- **Error Bar (Custom)**: https://echarts.apache.org/examples/en/editor.html?c=custom-error-bar
  - Data shape: metric + error/confidence bounds per point
  - Choose when: uncertainty or variance around each measurement matters; summarizing distribution spread at each point
  - Not when: bounds are uniform/trivial (just mention in annotation)
  - (also under Change over Time)

- **Confusion Matrix**: https://echarts.apache.org/examples/en/editor.html?c=matrix-confusion
  - Data shape: predicted vs actual categories
  - Choose when: evaluating classification model performance; showing how predictions distribute across true classes
  - Not when: not a classification problem

---

## 5. Change over Time
**Question: How does this trend, shift, or evolve?**

Use when time is the primary axis and the pattern of change — direction, rate, volatility, seasonality — is the story. The temporal sequence is structurally meaningful.

---

- **Basic Line**: https://echarts.apache.org/examples/en/editor.html?c=line-simple
  - Data shape: 1 metric, 1–5 series, time or ordered categories
  - Choose when: clean comparison of absolute values over time; ≤5 series
  - Not when: >5 series (spaghetti — use small multiples or highlight one); data is noisy (use Smoothed Line below)

- **Smoothed Line**: https://echarts.apache.org/examples/en/editor.html?c=line-smooth
  - Data shape: 1 metric, 1+ series, time axis
  - Choose when: trend matters more than individual data points; long time ranges with volatility
  - Not when: audience needs to read exact values at specific dates (smoothing shifts perceived positions)

- **Step Line**: https://echarts.apache.org/examples/en/editor.html?c=line-step
  - Data shape: 1 metric, time axis, discrete state changes
  - Choose when: values change in discrete jumps, not gradually (pricing tiers, system status, inventory)
  - Not when: underlying data is continuous — step styling misrepresents the transition

- **Basic Area**: https://echarts.apache.org/examples/en/editor.html?c=area-basic
  - Data shape: 1 metric, time axis, filled below line
  - Choose when: cumulative magnitude matters as much as the trend (volume, not just rate); single series
  - Not when: multiple overlapping series — areas obscure each other (use Stacked Area below or plain Basic Line)

- **Stacked Line**: https://echarts.apache.org/examples/en/editor.html?c=line-stack
  - Data shape: 1 metric, 2+ series, time axis
  - Choose when: total + part-to-whole contribution over time; reading individual series values matters
  - Not when: you want volume emphasis (use Stacked Area below); series cross frequently (hard to read stacked)

- **Stacked Area**: https://echarts.apache.org/examples/en/editor.html?c=area-stack
  - Data shape: 1 metric, 2+ series, time axis
  - Choose when: total volume + composition over time; area fill emphasizes magnitude alongside trend
  - Not when: individual series values must be precisely readable (stacking distorts upper series); >6 series (use ThemeRiver below); proportional share matters more than absolute volume (use 100% Stacked Area below)

- **100% Stacked Area**: https://echarts.apache.org/examples/en/editor.html?c=area-stack (configure with `stack: 'total'` + percentage normalization in data)
  - Data shape: 1 metric, 2+ series, time axis, normalized to 100%
  - Choose when: proportional share over time is the story — "what % of total did each segment contribute, and how did that shift?"; absolute volume is irrelevant or misleading (e.g., growing total obscures share loss)
  - Not when: absolute volumes matter (use Stacked Area above); comparing two snapshots only (use 100% Stacked Bar under Part-to-Whole)
  - (also under Part-to-Whole)

- **ThemeRiver**: https://echarts.apache.org/examples/en/editor.html?c=themeRiver-basic
  - Data shape: 1 metric, 2+ series (typically many), time axis
  - Choose when: showing cyclical volume shifts between many series; >6 series where Stacked Area above is too rigid
  - Not when: precise per-series values needed (area distortion); ≤5 series (Stacked Area is clearer); proportional share is the story and you have >6 series (no normalized ThemeRiver exists — consolidate series to ≤6 and use 100% Stacked Area above)
  - (also under Part-to-Whole)

- **Gradient Line**: https://echarts.apache.org/examples/en/editor.html?c=line-gradient
  - Data shape: 1 metric, time axis
  - Choose when: decorative sparkline behind a BAN card; visual polish for presentation-grade summary
  - Not when: audience needs to read the chart analytically (gradient obscures precise perception)

- **Multiple X Axes**: https://echarts.apache.org/examples/en/editor.html?c=multiple-x-axis
  - Data shape: 2 series with different time domains or granularities
  - Choose when: this-year vs last-year aligned by day-of-year; comparing two different time scales on one chart
  - Not when: series share the same time axis (just use Basic Line with 2 series)

- **Mixed Line and Bar**: https://echarts.apache.org/examples/en/editor.html?c=mix-line-bar
  - Data shape: 2 metrics on shared time axis, often dual Y-axes
  - Choose when: volume metric (bar) vs. rate metric (line) over time — e.g., spend + approval rate
  - Not when: both metrics are the same type (use Basic Line with 2 series); dual axes will mislead
  - (also under Correlation)

- **Basic Candlestick**: https://echarts.apache.org/examples/en/editor.html?c=candlestick-simple
  - Data shape: open, high, low, close per time unit
  - Choose when: range AND direction per time bucket; financial OHLC or daily min/max/open/close
  - Not when: audience unfamiliar with OHLC convention; only min/max matter (use error bars or range area)

- **Large Scale Candlestick**: https://echarts.apache.org/examples/en/editor.html?c=candlestick-large
  - Data shape: OHLC with 1000+ time periods
  - Choose when: multi-year history needs Canvas-mode performance
  - Not when: <500 periods (standard Basic Candlestick handles it)

- **OHLC Chart (Custom)**: https://echarts.apache.org/examples/en/editor.html?c=custom-ohlc
  - Data shape: open, high, low, close
  - Choose when: cleaner visual than candlestick bodies; integrating into a dashboard with simpler styling
  - Not when: audience expects candlestick convention (finance users)

- **Calendar Heatmap**: https://echarts.apache.org/examples/en/editor.html?c=calendar-heatmap
  - Data shape: daily date + 1 metric
  - Choose when: daily seasonality and spike patterns; week-of-year / day-of-week structure is part of the story
  - Not when: trend direction over time is the story (use Basic Line — calendar layout breaks temporal continuity)

- **Error Bar (Custom)**: https://echarts.apache.org/examples/en/editor.html?c=custom-error-bar
  - Data shape: metric + error/confidence bounds per time point
  - Choose when: uncertainty or variance around each time-series measurement matters
  - Not when: bounds are uniform/trivial (just annotate it)
  - (also under Distribution)

- **Bump Chart**: https://echarts.apache.org/examples/en/editor.html?c=bump-chart
  - Data shape: rank per category over time periods
  - Choose when: rank position changes are the story, not absolute values; showing who overtook whom
  - Not when: absolute values matter more than rank; >10 categories (unreadable)
  - (also under Ranking)

---

## 6. Part-to-Whole
**Question: How does this divide into components?**

Use when the composition — what share each piece contributes to a total — is the insight. The parts must sum to a meaningful whole.

---

- **Waterfall Chart**: https://echarts.apache.org/examples/en/editor.html?c=bar-waterfall
  - Data shape: 1 metric, sequential additive/subtractive contributions leading to a total
  - Choose when: explaining how a total changes step-by-step (variance bridges, driver decomposition, P&L walk)
  - Not when: contributions don't sum to a meaningful total; audience unfamiliar with waterfall convention
  - (also under Deviation)

- **Stacked Bar**: https://echarts.apache.org/examples/en/editor.html?c=bar-stack
  - Data shape: 1 metric, 1 category axis, 2+ series
  - Choose when: comparing total volume while showing composition across categories; ≤5 stack segments
  - Not when: comparing individual segment sizes precisely (stacking makes upper segments hard to compare); >5 segments (consolidate into "Other")

- **100% Stacked Bar**: https://echarts.apache.org/examples/en/editor.html?c=bar-stack-normalization
  - Data shape: 1 metric, 1 category axis, 2+ series (normalized to 100%)
  - Choose when: comparing relative distribution across categories regardless of total volume; proportional share is the message
  - Not when: absolute totals matter — normalization hides volume differences (use Stacked Bar above)

- **Doughnut Chart**: https://echarts.apache.org/examples/en/editor.html?c=pie-doughnut
  - Data shape: 1 metric, categorical slices, must sum to 100%
  - Choose when: ≤5 slices; proportions resemble recognizable fractions (25%, 50%); BAN number in the center hole
  - Not when: >5 categories (consolidate to "Other" or use Stacked Bar above); slices are similar size (hard to distinguish); comparing across multiple groups

- **Half Doughnut**: https://echarts.apache.org/examples/en/editor.html?c=pie-half-donut
  - Data shape: 1 metric, categorical slices
  - Choose when: tight vertical space; gauge-like feel for a composition metric inside a KPI tile
  - Not when: you have room for a full Doughnut; audience expects gauge semantics (actual → target)

- **Nightingale (Rose)**: https://echarts.apache.org/examples/en/editor.html?c=pie-roseType
  - Data shape: 1 metric, many categories
  - Choose when: emphasizing magnitude differences across many categories via radius encoding; decorative/editorial context
  - Not when: precise comparison needed (area encoding is inaccurate per Cleveland & McGill); almost always prefer a sorted Horizontal Bar under Ranking

- **Basic Tree**: https://echarts.apache.org/examples/en/editor.html?c=tree-basic
  - Data shape: hierarchy with labels (no size metric)
  - Choose when: showing structure/relationships (org chart, taxonomy, dependency tree); the hierarchy itself is the content
  - Not when: you need to compare magnitude — tree shows structure, not size (use Treemap below)

- **Treemap**: https://echarts.apache.org/examples/en/editor.html?c=treemap-simple
  - Data shape: hierarchical categories + 1 size metric
  - Choose when: comparing many categories by size with nested drill-down; space-efficient part-to-whole for large taxonomies
  - Not when: hierarchy is flat (use Stacked Bar above); precise comparison needed (area encoding is inaccurate)

- **Sunburst**: https://echarts.apache.org/examples/en/editor.html?c=sunburst-simple
  - Data shape: hierarchical categories + 1 metric
  - Choose when: emphasizing hierarchy depth; interactive drill-down into nested levels with radial layout
  - Not when: >3 hierarchy levels (outer rings become unreadable); audience unfamiliar with radial layouts

- **100% Stacked Area**: https://echarts.apache.org/examples/en/editor.html?c=area-stack (configure with percentage normalization)
  - Data shape: 1 metric, 2+ series, time axis, normalized to 100%
  - Choose when: proportional share over time — how composition shifts regardless of total volume growth
  - Not when: absolute volumes matter (use Stacked Area under Change over Time)
  - (also under Change over Time)

- **ThemeRiver**: https://echarts.apache.org/examples/en/editor.html?c=themeRiver-basic
  - Data shape: 1 metric, 2+ series, time axis
  - Choose when: composition shifts between many series over time; the flowing band shape communicates proportional change
  - Not when: precise per-series values needed (area distortion); ≤5 series (Stacked Area under Change over Time is clearer); proportional share with >6 series (consolidate to ≤6 segments and use 100% Stacked Area)
  - (also under Change over Time)

---

## 7. Magnitude
**Question: How big is this compared to that?**

Use when size comparisons across categories are the primary message, and rank order is secondary or irrelevant. The absolute or relative scale of each item matters.

---

- **Basic Bar (Vertical)**: https://echarts.apache.org/examples/en/editor.html?c=bar-simple
  - Data shape: 1 metric, 1 series, ≤10 categories
  - Choose when: direct size comparison across a small set of categories where rank is less important than scale
  - Not when: >10 categories (use Horizontal Bar under Ranking); data is time-based (use Basic Line under Change over Time)
  - (also under Ranking)

- **Simple Gauge**: https://echarts.apache.org/examples/en/editor.html?c=gauge-simple
  - Data shape: 1 metric + target range
  - Choose when: single KPI status vs threshold; familiar speedometer metaphor; dashboard tile context
  - Not when: multiple KPIs (use bullet charts — gauges waste space); no meaningful target range exists

- **Progress Gauge**: https://echarts.apache.org/examples/en/editor.html?c=gauge-progress
  - Data shape: 1 metric as % of goal
  - Choose when: progress-toward-goal in a compact circular form; tight dashboard tile
  - Not when: you have room for a progress bar (simpler, more space-efficient)

- **Basic Radar**: https://echarts.apache.org/examples/en/editor.html?c=radar
  - Data shape: 3–8 metrics per entity, normalized to comparable scales
  - Choose when: comparing the "shape" of multi-metric profiles (strengths/weaknesses pattern); shape comparison is the insight
  - Not when: >8 axes (unreadable); metrics aren't on comparable scales; precise values matter (use grouped Stacked Bar)

- **Multiple Radar**: https://echarts.apache.org/examples/en/editor.html?c=radar-multiple
  - Data shape: 2–4 entities on the same axes
  - Choose when: overlaying profiles for direct comparison (segment A vs B); shape differences are the story
  - Not when: >4 entities overlap (use small multiples of individual radars)

- **Pictorial Bar**: https://echarts.apache.org/examples/en/editor.html?c=pictorialBar-bar-transition
  - Data shape: 1 metric, categorical axis
  - Choose when: infographic/presentation style; branded or illustrative bar encoding where visual impact matters
  - Not when: analytical dashboard (decorative encoding reduces precision)

---

## 8. Flow
**Question: How does volume move through a sequence or divide across paths?**

Use when the journey through stages — what enters, drops off, or splits — is the story. The connection between stages is as important as the values at each stage.

---

- **Funnel Chart**: https://echarts.apache.org/examples/en/editor.html?c=funnel
  - Data shape: ordered stages + 1 metric (each stage ≤ previous)
  - Choose when: visualizing conversion/drop-off through sequential steps; the shrinkage is the insight
  - Not when: stages don't have a natural order; values don't decrease monotonically (use Basic Bar under Magnitude)

- **Funnel Compare**: https://echarts.apache.org/examples/en/editor.html?c=funnel-align
  - Data shape: 2+ funnel series (same stages, different segments)
  - Choose when: comparing conversion across segments (channels, cohorts, A/B test arms)
  - Not when: >3 funnels (too cluttered — use grouped bars per stage instead)

- **Basic Sankey**: https://echarts.apache.org/examples/en/editor.html?c=sankey-simple
  - Data shape: nodes + weighted directed flows
  - Choose when: showing how volume distributes across multiple paths between stages; fan-out and fan-in matter
  - Not when: only one path per item (use Funnel above); >50 nodes (visual spaghetti)

- **Sankey with Levels**: https://echarts.apache.org/examples/en/editor.html?c=sankey-levels
  - Data shape: nodes + flows + explicit stage grouping
  - Choose when: clear left-to-right stage structure; color-coding by stage clarifies the flow
  - Not when: stages are ambiguous or items can skip stages

- **Chord Diagram**: https://echarts.apache.org/examples/en/editor.html?c=chord-simple
  - Data shape: categories + bilateral relationship weights
  - Choose when: bidirectional flows between entities (cross-usage, migration both ways, trade relationships)
  - Not when: flow is unidirectional (use Sankey above); >10 categories (visual overload)

- **Lines Flow (Geo)**: https://echarts.apache.org/examples/en/editor.html?c=lines-ny
  - Data shape: origin/destination paths + intensity
  - Choose when: movement or routing patterns on a geographic base; the spatial path of flow matters
  - Not when: flow volumes matter more than geography (use Basic Sankey above)
  - (also under Spatial)

---

## 9. Spatial
**Question: Where does this happen geographically?**

Use when location and geographic pattern are the primary insight — where clusters form, which regions lead or lag, how patterns vary across space.

---

- **Map Scatter (Geo)**: https://echarts.apache.org/examples/en/editor.html?c=scatter-map
  - Data shape: lat/long coordinates + metric
  - Choose when: geographic distribution IS the primary insight; point-level clustering on a map
  - Not when: story is about ranking or comparison by region (use Horizontal Bar under Ranking — maps hide magnitude differences)

- **Choropleth + Scatter**: https://echarts.apache.org/examples/en/editor.html?c=geo-choropleth-scatter
  - Data shape: region-level metric + point-level events
  - Choose when: regional intensity with city-level detail overlay; both scales of geography matter
  - Not when: story is comparison or ranking by region (use Horizontal Bar under Ranking — maps distort by area)

- **SVG Map**: https://echarts.apache.org/examples/en/editor.html?c=geo-svg-map
  - Data shape: custom map/floorplan + metrics
  - Choose when: non-standard geography (building layout, custom territory, process diagram)
  - Not when: standard geographic data — use built-in maps above

- **Lines Flow (Geo)**: https://echarts.apache.org/examples/en/editor.html?c=lines-ny
  - Data shape: origin/destination paths + intensity
  - Choose when: movement or routing patterns on a geographic base; migration, logistics, network paths
  - Not when: flow volumes matter more than geography (use Basic Sankey under Flow)
  - (also under Flow)

---

## Interaction Patterns
**These are modifiers, not primary chart types.** Add these behaviors to charts from the sections above when you need user-driven exploration. The underlying chart relationship (ranking, magnitude, etc.) should be chosen first; the interaction layer is added on top.

---

- **Drilldown Bar**: https://echarts.apache.org/examples/en/editor.html?c=bar-drilldown
  - Data shape: hierarchical categories
  - Choose when: summary-to-detail exploration (region → country → city); user needs to navigate hierarchy on demand
  - Not when: hierarchy is flat or only 2 levels (just use filter + basic bar); static delivery (PDF/email)

- **Bar Race (Animation)**: https://echarts.apache.org/examples/en/editor.html?c=bar-race
  - Data shape: rank/value over many time periods
  - Choose when: narrative presentation showing leadership changes over time; storytelling context
  - Not when: analytical dashboard (animation blocks comparison); static delivery (PDF/email)

- **Brush Selectable Bar**: https://echarts.apache.org/examples/en/editor.html?c=bar-brush
  - Data shape: standard bar chart used as a dashboard filter
  - Choose when: bar chart acts as a filter control for other dashboard elements; cross-filtering is the UX
  - Not when: no linked charts to filter — brush selection serves no purpose

---

## Layout Modifiers
**These are not chart types — they are layout strategies applied to any chart from the sections above.** Choose the chart type first, then decide if a layout modifier improves readability. Modifiers can be combined with any Interaction Pattern.

---

- **Small Multiples** (ECharts: multiple series in a `grid` array, or custom `graphic` layout)
  - Apply when: >5 series on one chart causes spaghetti/overlap; comparing the *shape* of each series independently matters; audience needs to isolate patterns per category
  - Implementation: Create a grid of identical charts, one per series, sharing the same axes and scale. In ECharts, use multiple `grid`/`xAxis`/`yAxis` entries with `gridIndex`.
  - Not when: ≤4 series (overlay with legend is clearer); the *interaction* between series is the story (lines crossing, one overtaking another — keep them on one chart); space is very constrained (each panel needs minimum ~200×150px)
  - Pairs well with: Basic Line, Basic Area, Basic Bar, Scatter — any chart that gets cluttered with many series

- **Faceted Grid** (ECharts: dataset transform with `grid` array)
  - Apply when: same chart type needs repeating across a categorical dimension (region, segment, product); direct visual comparison across facets is the goal
  - Implementation: Like small multiples but driven by a categorical split rather than series count. Each facet gets the same chart config with filtered data.
  - Not when: categories have vastly different scales (shared axis will compress small-value facets); >12 facets (too many panels to scan)

---

## Specialized
**Niche chart types for specific structural needs.** These don't fit neatly into the question-based framework — they solve specific representational problems.

---

- **Calendar Grid**: https://echarts.apache.org/examples/en/editor.html?c=calendar-simple
  - Data shape: date structure + optional metric
  - Choose when: calendar scaffold for event annotations; week/month layout is the organizing principle rather than time trend
  - Not when: trend is the story (use Basic Line under Change over Time — calendar layout fragments temporal continuity)

- **Gantt Chart (Custom)**: https://echarts.apache.org/examples/en/editor.html?c=custom-gantt-flight
  - Data shape: start/end timestamps per item
  - Choose when: timelines, durations, overlapping events, batch schedules; the span and overlap of items is the content
  - Not when: no time overlap between items (use sorted bar or table)
