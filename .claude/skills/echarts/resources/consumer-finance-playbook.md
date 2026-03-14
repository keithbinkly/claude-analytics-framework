# Consumer Finance Visualization Playbook

**ECharts-Ready Chart Specifications for Advanced Analytics Views**
*Derived from 40+ industry reports · February 2026*

---

## How to Use This Document

Each chart spec below includes: what it shows, why it matters, the exact metric definitions, axis/series configuration for ECharts, and which segmentation dimensions from the metrics playbook it requires. Charts are organized by analytical technique, not by topic — so you can find the right *type* of view and adapt it to your data.

The BofA Consumer Checkpoint is the gold standard for these visualizations. Their key techniques:

- **YoY % change, not levels** — shows momentum and direction, normalizes for scale
- **3-month moving averages** — smooths noise while preserving trend
- **Indexed baselines** (set one series = 100) — enables multi-series comparison on a common scale
- **Contribution decomposition** — stacked bars showing what drove the total change
- **Divergence charts** — gap between two series as the primary visual, not the series themselves

---

## Technique 1: Income-Stratified YoY Trend Lines

### Chart 1.1 — The K-Shape: Card Spending Growth by Income Tercile

**What it shows:** Monthly YoY% card spending growth for lower, middle, and higher-income households on a single chart. The visual gap between the lines *is* the story.

**Why it matters:** This is the single most important chart in consumer finance right now. The 6x gap (lower +0.4% vs. higher +2.4% in Dec 2025) is the defining feature of the economy. Tracking its width over time shows whether bifurcation is widening or narrowing.

**Metric definition:**
```sql
card_spending_yoy_pct = (current_month_spend - same_month_prior_year_spend)
                        / same_month_prior_year_spend * 100

-- Apply 3-month moving average per BofA methodology
card_spending_yoy_3mo_avg = AVG(card_spending_yoy_pct)
                            OVER (PARTITION BY income_tercile
                                  ORDER BY month_date
                                  ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)
```

**ECharts config sketch:**
- **Type:** Line chart, 3 series
- **X-axis:** Monthly dates (Jan 2024 → present)
- **Y-axis:** YoY % change (format: "+2.4%")
- **Series:** `lower_income` (red/warm), `middle_income` (gray/neutral), `higher_income` (blue/cool)
- **Reference line:** Y = 0 (dashed, marks growth/contraction boundary)
- **Annotation:** Shade the area between lower and higher lines to visually encode the gap width
- **Tooltip:** Show all three values + the gap (higher minus lower) for the hovered month
- **Smoothing:** Use 3-month moving average per BofA methodology, not ECharts `smooth: true`

**Companion computed metric:**
```sql
k_shape_gap = higher_income_yoy_3mo_avg - lower_income_yoy_3mo_avg
```
Track this as a standalone KPI. Current value: 2.0pp (December 2025). Widest since BofA began tracking.

---

### Chart 1.2 — Wage Growth Divergence by Income Tercile

**Same structure as 1.1** but for after-tax wage/salary growth YoY%. The wage chart explains *why* the spending chart looks the way it does.

**Current data points:**
| Month | Lower Income | Higher Income | Gap |
|---|---|---|---|
| Jul 2025 | +1.3% | +3.2% | 1.9pp |
| Sep 2025 | (uptick) | +3.2% | ~1.9pp |
| Nov 2025 | +1.4% | +4.0% | 2.6pp |
| Jan 2026 | +0.9% | +3.7% | 2.8pp |

**Overlay opportunity:** Plot CPI (2.7%) as a horizontal reference line. Any income group below this line is experiencing real wage decline. Currently lower-income is well below; middle is near; higher is above. This single reference line transforms the chart from "different growth rates" to "who is falling behind inflation."

---

### Chart 1.3 — The Wealth Effect: Top 5% Discretionary Spending vs. S&P 500

**What it shows:** BofA's most analytically sophisticated chart. It plots the *gap* in discretionary spending growth between the top 5% by income and the middle-income cohort alongside S&P 500 YoY% returns. The correlation is tight.

**Why it matters:** Proves that the wealth effect — not wages — drives the top tier's spending. Implies that a stock market correction would collapse the spending engine that's masking lower-tier deterioration.

**Metric definition:**
```sql
wealth_effect_spending_gap = top_5pct_discretionary_yoy - middle_income_discretionary_yoy

-- Discretionary = total card spend less groceries, gas, utilities (BofA definition)
discretionary_spend = total_spend - grocery_spend - gas_spend - utility_spend
```

**ECharts config sketch:**
- **Type:** Dual-axis line chart
- **X-axis:** Monthly dates (Jan 2020 → present to capture full pandemic/recovery cycle)
- **Left Y-axis:** Spending gap in percentage points
- **Right Y-axis:** S&P 500 YoY % return
- **Series 1:** Spending gap (solid line, primary color)
- **Series 2:** S&P 500 YoY% (dashed line, secondary color)
- **Key insight annotation:** Call out periods where S&P declines preceded spending gap compression (2022 drawdown → wealth effect reversal)

---

## Technique 2: Indexed Baseline Comparisons

### Chart 2.1 — Household Cash Reserves vs. Pre-Pandemic (Index = 100)

**What it shows:** Multiple account types (checking, savings, CDs, brokerage, money market) each indexed to their January 2020 level = 100. Shows how consumers have shifted where they hold cash, not just how much.

**Why it matters:** JPMorgan found checking/savings balances are 17pp below pre-pandemic trends — alarming in isolation. But total cash reserves including CDs and brokerage accounts grew 3–5% YoY in 2025. Consumers shifted to higher-yielding accounts, not genuine distress. This chart catches that nuance; a simple balance chart would miss it.

**Metric definition:**
```sql
indexed_balance = (current_month_avg_balance / jan_2020_avg_balance) * 100

-- Compute for each account type separately
-- Also compute an "all liquid" composite
```

**ECharts config sketch:**
- **Type:** Multi-line chart, 5-6 series
- **X-axis:** Monthly dates (Jan 2020 → present)
- **Y-axis:** Index (100 = Jan 2020 level). No %, no $, just the index number.
- **Series:** `checking` (declining below 100), `savings` (declining below 100), `cd_accounts` (rising well above 100), `brokerage` (rising well above 100), `money_market` (rising), `total_liquid` (the composite, bolded/thicker line)
- **Reference line:** Y = 100 (the pre-pandemic baseline)
- **Key insight:** Checking and savings lines cross below 100 while total liquid stays above — the visual instantly communicates the reallocation story

**Segmentation overlay:** Run this chart separately for each income tercile. The reallocation story is strongest among higher-income households. Lower-income households show genuine depletion across all account types.

---

### Chart 2.2 — Credit Score Distribution Shift (Index = 2019)

**What it shows:** The three FICO score bands (750+, 600–749, below 600) each indexed to their 2019 population share = 100. Shows the K-shaped divergence in credit health.

**Why it matters:** The middle band shrank from 38.1% to 33.8% (index drops to ~89). Upper band grew. Lower band grew. The "hollowing out of the middle" is a story that indexed visualization tells far more powerfully than a table of percentages.

**Data:**
| Band | 2019 Share | 2021 Share | 2025 Share | Index (2019=100) |
|---|---|---|---|---|
| 750+ (super prime) | ~37% | ~40% | ~41% | ~111 |
| 600–749 (middle) | ~38% | ~38% | ~34% | ~89 |
| Below 600 (subprime) | ~14% | ~12% | ~14% | ~100 |

**ECharts config sketch:**
- **Type:** Line chart, 3 series
- **X-axis:** Annual (2019, 2020, 2021, 2022, 2023, 2024, 2025)
- **Y-axis:** Index (100 = 2019 share)
- **Reference line:** Y = 100
- **Visual:** Upper band line rises and diverges from the sinking middle band — the K-shape emerges visually

---

### Chart 2.3 — Delinquency Rates Indexed to Pre-Pandemic

**What it shows:** Multiple credit products (credit cards, auto, mortgage, student loan, personal loan) each indexed to their pre-pandemic delinquency rate = 100.

**Why it matters:** Absolute delinquency rates for different products are on completely different scales (credit cards ~2.4%, mortgages ~1.4%, student loans ~16%). Indexing them makes cross-product comparison possible. You can immediately see that student loans exploded while credit cards merely returned to baseline.

**Data (indexed to pre-pandemic rate = 100):**
| Product | Pre-Pandemic Rate | Current Rate | Index |
|---|---|---|---|
| Credit Card 90+ DPD | ~2.3% | 2.37% | ~103 |
| Auto 60+ DPD | ~1.33% | 1.38% | ~104 |
| Mortgage 60+ DPD | ~1.2% | 1.44% | ~120 |
| Student Loan 90+ DPD | ~6% | 16.32% | ~272 |
| Personal Loan 60+ DPD | ~3.5% | 3.49% | ~100 |

**ECharts config sketch:**
- **Type:** Multi-line chart
- **Y-axis:** Index (100 = pre-pandemic). Student loans will visually dominate — that IS the story.
- **Alternative:** Bar chart showing current index value per product, sorted descending. Student loans at 272, mortgage at 120, credit cards at 103, personal loans at 100.

---

## Technique 3: Contribution Decomposition (Stacked Bars)

### Chart 3.1 — MoM Spending Growth: Category Contribution

**What it shows:** Total MoM% spending change decomposed into contributions from services, retail (ex-gas, ex-restaurants), gasoline, and restaurants. This is BofA's signature Exhibit 1.

**Why it matters:** Knowing that total spending rose 0.2% MoM is less useful than knowing *what drove it*. If gasoline prices fell but services spending rose, the composition tells you whether the growth is sustainable or mechanical.

**Metric definition:**
```sql
-- Contribution of category c to total MoM growth:
category_contribution = (category_c_spend_current - category_c_spend_prior)
                        / total_spend_prior * 100

-- Sum of all category contributions = total MoM% growth
```

**ECharts config sketch:**
- **Type:** Stacked bar chart
- **X-axis:** Monthly dates
- **Y-axis:** MoM % change
- **Stacks:** `services` (blue), `retail_ex_gas_restaurants` (green), `gasoline` (yellow), `restaurants` (orange)
- **Bars above 0:** Positive contributions. Below 0: negative contributions. Net line overlaid.
- **Key:** This is a waterfall-style decomposition. ECharts can handle this with `stack: 'total'` and negative values.

---

### Chart 3.2 — What's Driving Inflation: CPI Category Contributions

**What it shows:** The total CPI YoY% decomposed by category contribution (shelter, food, energy, healthcare, transportation, other). Shows which categories are driving and which are relieving inflation pressure.

**Current data (Dec 2025, 2.7% total):**
| Category | YoY% | Weight | Contribution |
|---|---|---|---|
| Shelter | +3.2% | ~34% | ~1.09pp |
| Food | +3.1% | ~14% | ~0.43pp |
| Hospital services | +6.7% | ~2% | ~0.13pp |
| Insurance | +8.2% | ~3% | ~0.25pp |
| Gasoline | -3.4% | ~4% | ~-0.14pp |
| Other | various | ~43% | ~0.94pp |

**ECharts config sketch:**
- **Type:** Stacked bar chart (monthly) or horizontal waterfall for a single month
- **Insight:** Shelter alone contributes ~1.1pp of the 2.7% total. Gasoline is the only meaningful deflationary offset. Healthcare and insurance are small in weight but fast-growing — the chart shows why consumers feel inflation is worse than the headline.

---

## Technique 4: Divergence / Gap Charts

### Chart 4.1 — The Sentiment-Action Gap

**What it shows:** Consumer confidence index (Conference Board or Michigan) plotted against actual spending growth (BofA card data or Mastercard SpendingPulse). The gap between the two series is the story.

**Why it matters:** This is the most important methodological insight from Q4 2025: survey-based data should be structurally discounted relative to transaction data. Visualizing the gap over time shows it widening to historic proportions.

**ECharts config sketch:**
- **Type:** Dual-axis line chart
- **Left Y-axis:** Sentiment index (Conference Board, inverted scale so that decline = visual decline)
- **Right Y-axis:** YoY spending growth %
- **Shaded area:** Between the two lines, colored to show when they diverge (sentiment down, spending up = orange/warning)
- **Time range:** Jan 2020 → present (captures pandemic, recovery, current divergence)
- **Annotation:** Mark Q4 2025 as the widest gap on record

---

### Chart 4.2 — Conference Board vs. Michigan: The Sentiment Divergence

**What it shows:** Both sentiment indices on a common indexed scale (each = 100 at a chosen baseline month). Shows when they agree and disagree.

**Why it matters:** In October 2025, both were declining. By January 2026, they diverged — Conference Board collapsed to 84.5 while Michigan improved to 57.3. This new divergence signals they're measuring different things (labor market vs. inflation perceptions) and analysts must choose which to weight.

**Metric definition:**
```sql
-- Index both to same baseline month (e.g., Jan 2024 = 100)
cb_indexed = (conference_board_current / conference_board_jan2024) * 100
mich_indexed = (michigan_current / michigan_jan2024) * 100
```

**ECharts config sketch:**
- **Type:** Line chart, 2 series
- **Y-axis:** Index (Jan 2024 = 100)
- **Reference line:** Y = 100
- **Shaded region:** Between the lines where they diverge post-October 2025
- **Annotation:** "CB weighs labor market; Michigan weighs inflation perceptions"

---

### Chart 4.3 — Real Wage Growth by Income Tier (Wage minus CPI)

**What it shows:** After-tax wage growth minus CPI for each income tercile. Series above 0 = real wage gains; below 0 = real wage decline.

**Why it matters:** The most direct measure of whether households are getting ahead or falling behind. Currently: lower-income at -1.8pp (0.9% wage vs. 2.7% CPI), higher-income at +1.0pp (3.7% vs. 2.7%). The zero line creates immediate visual comprehension.

**ECharts config sketch:**
- **Type:** Area chart, 3 series (one per tercile)
- **X-axis:** Monthly
- **Y-axis:** Real wage growth (wage YoY% minus CPI YoY%)
- **Reference line:** Y = 0 (bold — the inflation breakeven)
- **Coloring:** Areas above 0 in green, below 0 in red, per series
- **Current state:** Lower-income series has been below zero for months; higher-income stays above

---

## Technique 5: Generational Comparison Patterns

### Chart 5.1 — Radar Chart: Generational Financial Profile

**What it shows:** A radar/spider chart with 6 axes comparing Gen Z, Millennials, Gen X, and Boomers across standardized financial health dimensions.

**Axes (each normalized 0–100 where 100 = "best"):**
| Dimension | Gen Z | Millennial | Gen X | Boomer |
|---|---|---|---|---|
| Credit score (norm) | 45 | 55 | 68 | 82 |
| Score stability (inv. volatility) | 40 | 60 | 75 | 90 |
| Spending growth | 95 | 65 | 50 | 40 |
| BNPL independence (inv. usage) | 30 | 35 | 60 | 85 |
| Emergency fund confidence | 25 | 40 | 55 | 70 |
| Housing affordability | 20 | 40 | 55 | 75 |

**ECharts config sketch:**
- **Type:** Radar chart, 4 overlapping polygons
- **Key insight:** Gen Z's polygon is spiked high on spending growth but collapsed on every stability/security dimension — the "paradox" as a shape

---

### Chart 5.2 — Small Multiples: Spending Growth by Generation × Income

**What it shows:** A grid of small line charts — rows = generations, columns = income terciles — each showing YoY card spending growth over time. 12 mini-charts total (4 generations × 3 income tiers).

**Why it matters:** The aggregate K-shape masks that the generational and income effects *interact*. Low-income Gen Z is a completely different story from high-income Gen Z. BofA noted that younger generations' spending is "particularly sensitive to changes in their wages as they have relatively lower assets." This chart surfaces those interactions.

**ECharts config sketch:**
- **Type:** Grid layout of line charts (ECharts `grid` with multiple `xAxis`/`yAxis` pairs)
- **Shared Y-axis scale** across all 12 panels for direct comparison
- **Highlight:** Low-income Gen Z panel will show the most volatility; high-income Boomer panel will show the most stability

---

## Technique 6: Distribution Shifts Over Time

### Chart 6.1 — Credit Score Distribution: Stacked Area Over Time

**What it shows:** Population share in each credit risk tier (super prime, prime plus, prime, near prime, subprime) as stacked areas over time. The visual shows the middle compressing while top and bottom expand.

**Data (TransUnion risk tiers):**
| Tier | 2019 | 2021 | 2023 | 2025 |
|---|---|---|---|---|
| Super Prime (781+) | 37.1% | ~39% | ~40% | 40.9% |
| Prime Plus (720–780) | ~18% | ~18% | ~17% | ~17% |
| Prime (660–719) | ~17% | ~17% | ~16% | ~15% |
| Near Prime (600–659) | ~14% | ~14% | ~13% | ~13% |
| Subprime (<600) | ~14% | ~12% | ~13% | 14.4% |

**ECharts config sketch:**
- **Type:** Stacked area chart (100% stacked or absolute)
- **X-axis:** Quarterly or annual
- **Y-axis:** Population share %
- **Coloring:** Gradient from green (super prime) to red (subprime)
- **Key insight:** The green band expands, the red band expands, the middle bands compress — the K-shape in credit

---

### Chart 6.2 — Payment Hierarchy Heatmap

**What it shows:** A heatmap matrix where rows = credit products (auto, mortgage, personal, credit card, student loan) and columns = time periods. Cell color intensity = delinquency rate relative to that product's own baseline.

**Why it matters:** FICO found auto loans are now the highest payment priority (reversing the traditional mortgage-first hierarchy). A heatmap shows the *relative* stress across products over time, revealing the priority shift. Student loans will glow hot; auto loans will stay cool.

**ECharts config sketch:**
- **Type:** Heatmap
- **X-axis:** Quarterly periods
- **Y-axis:** Product type (ordered by payment priority rank: auto, mortgage, personal, card, student)
- **Color scale:** Green (below baseline delinquency) → Yellow (at baseline) → Red (above baseline)
- **Cell value:** Index relative to pre-pandemic delinquency rate

---

## Technique 7: Composite Scores & Gauges

### Chart 7.1 — Consumer Financial Stress Score Dashboard

**What it shows:** The composite stress score from the metrics playbook (max 8.0), broken into its component signals, displayed as a gauge with drill-down.

**Components (from metrics playbook):**
| Signal | Weight | Threshold | Current Population % Above |
|---|---|---|---|
| Credit utilization > 50% | 1.0 | 50% util | ~25% |
| Any account 30+ DPD | 2.0 | Any delinquency | ~12% |
| Score volatility ≥ 50pts | 1.0 | 50pt swing | ~8% (14.1% Gen Z) |
| BNPL for groceries | 1.5 | Financing essentials | ~8% |
| Cash reserve < 1 month | 1.5 | Reserve index < 0.33 | ~30% |
| Housing cost > 30% income | 1.0 | HUD cost-burdened | ~35% |

**ECharts config sketch:**
- **Type:** Gauge chart (primary) + horizontal stacked bar (component breakdown)
- **Gauge:** 0–8 scale, colored zones: 0–1 green, 1–3 yellow, 3–5 orange, 5–8 red
- **Segmented bar below:** Shows population distribution across stress categories (severe/moderate/mild/healthy)
- **Drill-down:** Click a segment to see which component signals are most prevalent in that population

---

### Chart 7.2 — Recession Probability Signal Timeline

**What it shows:** Conference Board Expectations Index over time with the recession-warning threshold (80) as a bold reference line. Shaded bands mark actual recession periods.

**Why it matters:** The Expectations Index has been below 80 for 12 consecutive months — the longest such run without an actual recession. Either the indicator has lost predictive power (the sentiment-action gap thesis) or a recession is being delayed, not prevented.

**ECharts config sketch:**
- **Type:** Line chart with markArea for recession periods
- **Y-axis:** Expectations Index value
- **Reference line:** Y = 80 (bold, labeled "Recession Signal Threshold")
- **Shaded regions:** Gray bands for actual NBER recession periods
- **Annotation:** Mark current 12-month run below 80; note prior instances and lag to recession onset

---

## Technique 8: Geographic / Regional Views

### Chart 8.1 — E-Commerce Growth Heatmap by Metro

**What it shows:** A choropleth or bubble map showing metro-level e-commerce YoY growth during holiday 2024 (Visa data). Sunbelt markets visually dominate.

**Data:**
| Metro | E-Commerce YoY | vs. National (+6.7%) |
|---|---|---|
| Tampa | +10.6% | +3.9pp |
| Phoenix | +10.0% | +3.3pp |
| Minneapolis | +8.9% | +2.2pp |
| Dallas | +8.4% | +1.7pp |
| Charlotte | +7.9% | +1.2pp |
| National | +6.7% | baseline |

**ECharts config sketch:**
- **Type:** Map (US) with bubble size = absolute spending, bubble color = growth rate relative to national
- **Color scale:** Blue (below national) → White (at national) → Orange/Red (above national)
- **Alternative:** Ranked horizontal bar chart, sorted by growth rate, with national average as reference line

---

### Chart 8.2 — Fed District Economic Conditions Choropleth

**What it shows:** The 12 Federal Reserve districts colored by their Beige Book economic condition assessment (expanding / stable / contracting).

**Current data (Jan 2026 Beige Book):** 8 districts growing, up from 1 in November. Visualizing the shift from November to January as two side-by-side maps shows the shutdown recovery.

**ECharts config sketch:**
- **Type:** US map with Fed district boundaries
- **Coloring:** Green (expanding), Yellow (stable), Red (contracting)
- **Small multiples:** Side-by-side for Nov 2025 vs. Jan 2026 to show the shift

---

## Technique 9: Time-to-Event / Runway Analysis

### Chart 9.1 — Savings Buffer Depletion Runway

**What it shows:** For each income tier or wealth percentile, the estimated months until liquid savings buffers (above pre-pandemic baseline) are exhausted at current depletion rates.

**Why it matters:** RBC estimates the bottom 80% hold ~$76K per household in liquid cushion above pre-pandemic levels. The saving rate is at 3.5% and falling. This chart answers: "how long can this last?"

**Metric definition:**
```sql
-- Simplified depletion model
months_of_runway = excess_liquid_balance / monthly_net_savings_drawdown

-- Where:
excess_liquid_balance = current_liquid_assets - pre_pandemic_liquid_assets
monthly_net_savings_drawdown = monthly_spend - monthly_income  -- when negative = drawdown
```

**ECharts config sketch:**
- **Type:** Horizontal bar chart, one bar per income/wealth segment
- **X-axis:** Months of remaining buffer
- **Color:** Green (24+ months) → Yellow (12–24) → Orange (6–12) → Red (<6)
- **Reference lines:** 6 months, 12 months, 18 months
- **Current estimates:** Bottom 80% ≈ 12–18 months under adverse conditions. Top 20% ≈ effectively unlimited.

---

## Technique 10: Green Dot Partner-Specific Dashboards

### Chart 10.1 — Amazon Flex: Gig Worker Financial Health Scorecard

**Recommended panel of 4 mini-charts:**

1. **Lower-income spending growth** (line, YoY%, monthly) — tracks purchasing power
2. **BNPL late payment rate, Gen Z** (line, quarterly) — tracks credit stress in core demographic
3. **Gig work hours index** (line, indexed to Jan 2024 = 100) — tracks demand for gig work (Goldman data)
4. **Paycheck-to-paycheck rate** (area chart, monthly) — tracks financial precarity in target population

### Chart 10.2 — Intuit QuickBooks: Small Business Stress Dashboard

**Recommended panel of 4 mini-charts:**

1. **QuickBooks Small Business Employment Index** (bar, monthly net change) — tracks hiring/firing
2. **NFIB price plans** (line, % raising prices, monthly) — tracks margin compression
3. **SBA lending volume** (bar, quarterly) — tracks capital demand
4. **Small vs. large business payroll growth** (dual-line, ADP data) — tracks the migration of jobs from small to large enterprises

### Chart 10.3 — Wealthfront: Wealth Effect Dashboard

**Recommended panel of 4 mini-charts:**

1. **S&P 500 vs. top-5% discretionary spending gap** (dual-axis line) — tracks the wealth effect
2. **Luxury retail spending growth** (line, AmEx data) — tracks premium spending
3. **Michigan sentiment by stock portfolio ownership** (diverging bar) — tracks confidence bifurcation
4. **Robo-advisory AUM** (area chart, quarterly) — tracks market growth

### Chart 10.4 — Ceridian Dayforce: EWA Demand Indicators

**Recommended panel of 4 mini-charts:**

1. **Real wage growth, lower income** (line with 0-reference, monthly) — tracks the gap EWA fills
2. **Saving rate** (line, monthly) — tracks buffer depletion
3. **Consumer credit growth SAAR** (line, monthly) — tracks compensatory borrowing
4. **Paycheck-to-paycheck rate by income source** (stacked bar: salaried vs. hourly vs. gig) — tracks target population growth

---

## Appendix: Quick Reference — Chart Type Selection Guide

| Analytical Question | Chart Type | Key Feature |
|---|---|---|
| How is metric X trending over time? | Line chart, YoY% | 3-month moving average smoothing |
| How do two groups compare over time? | Dual-line with shaded gap | Gap width = story |
| How do 3+ groups compare on different scales? | Indexed baseline (=100) | Normalizes for scale |
| What drove the total change? | Stacked bar (contribution) | Components sum to total |
| How is a population distributed? | Stacked area (over time) | Shows distribution shift |
| Which category is most stressed? | Heatmap (product × time) | Color = relative intensity |
| How much runway remains? | Horizontal bar with zones | Color bands for thresholds |
| What's the overall health picture? | Radar chart (multi-dimension) | Shape = profile |
| Where are geographic hotspots? | Map with bubble/choropleth | Color/size = metric |
| How does a composite score break down? | Gauge + segmented bar | Drill-down to components |

---

## Appendix: Segmentation Dimensions Available for Chart Faceting

Any chart above can be faceted (small multiples) by any segmentation from the metrics playbook:

| Dimension | Values | Best For |
|---|---|---|
| `income_tercile` | lower / middle / higher | Spending, wage, delinquency charts |
| `generation` | gen_z / millennial / gen_x / boomer | Behavioral and credit charts |
| `credit_risk_tier` | super_prime → subprime | Credit condition charts |
| `housing_burden_tier` | severely_burdened / cost_burdened / affordable | Housing-related analysis |
| `bnpl_archetype` | strategic / necessity / essentials / struggling | Payment method analysis |
| `stress_category` | severe / moderate / mild / healthy | Composite health dashboards |
| `regional_economic_condition` | expanding / stable / contracting | Geographic analysis |
| `wealth_effect_tier` | high / moderate / low sensitivity | Market-linked analysis |
| `trade_down_type` | quantity / brand / cross_category / deferral | Behavioral segmentation |

**Faceting rule of thumb:** If the aggregate chart tells a boring story but you suspect bifurcation, facet by `income_tercile` first — it almost always reveals the hidden narrative.

---

*End of document. All chart specifications derived from public industry report methodologies (primarily BofA Consumer Checkpoint, FICO, TransUnion, McKinsey, Fed Beige Book). Adapt metric definitions to your data schema before implementation.*