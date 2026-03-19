# Wealthfront

> Analytical brief for Green Dot's BaaS partnership with Wealthfront. Living document — accumulates analyst findings over time.

**Last Updated**: 2026-02-12
**Last Researched**: 2026-02-11
**Data Quality Grade**: B (merchant spend validated; deposit flow data limited to Green Dot's view)

---

## Business Context

| Metric | Value |
|--------|-------|
| Public Listing | Nasdaq: WLTH (IPO Dec 12, 2025 at $14/share; ~$8.20 as of Feb 2026) |
| AUM | $88.2B (at IPO) |
| Customer Base | 1.3M clients |
| Revenue | $339M (S-1 disclosed), $123M net income |
| Key Risk | $208M net deposit outflows (Q4 2025); CEO conflict-of-interest scandal |

**Product**: Wealthfront is a digital wealth management platform offering automated investment portfolios, high-yield cash accounts, and financial planning tools. The "Wealthfront Cash Account" provides checking features, debit card access, and direct deposit — powered by Green Dot Bank.

**CRITICAL CONTEXT — IN CRISIS**: Wealthfront IPO'd Dec 12, 2025, then stock fell ~42% to ~$8.20. Two catalysts: $208M net deposit outflows in first reported quarter and CEO conflict-of-interest scandal (95.1% personal ownership of home-lending entity). Multiple securities fraud investigations launched.

**Strategic Position**:
- **Cash management = 76% of revenue** (S-1 disclosure) — interchange from Green Dot debit card is material to Wealthfront's business model
- $208M outflows directly reduce Green Dot program economics
- Joint Cash Account launch (mid-2025) doubles debit cards per household — positive for Green Dot interchange even if per-account balances decline
- Goldman Sachs expects 2 more Fed cuts (March and June 2026) — each cut compresses cash management spread
- Green Dot split: 7-year exclusive agreement provides continuity despite Wealthfront turbulence

**Key Relationship Dynamics**:
- Green Dot interchange revenue directly tied to Wealthfront's debit card usage
- Deposit outflows are the #1 metric to watch — directly impacts program size
- Joint accounts are the bright spot (2 cards per household)
- Cash Account APY raised to 3.30% (referral 3.80-4.05%) as defensive measure
- Multi-product users (investment + cash) have 3-4x lower churn — cash-only customers most at risk

---

## Customer Segments

**By Account Balance**:
- **High Net Worth** (>$100k): Low churn, high engagement, responsive to premium features
- **Growing Savers** ($25k-$100k): Core demographic, medium engagement, rate-sensitive
- **New Investors** (<$25k): Younger, exploring options, higher churn, price-conscious

**By Product Mix**:
- **Cash-Only Customers**: Lower engagement, rate-driven behavior, **highest churn risk** — most likely to leave during current crisis
- **Investment-Only Customers**: Moderate engagement, market-sensitive behavior
- **Multi-Product Users**: Highest retention (3-4x lower churn), integrated financial life, best unit economics

**By Demographics**:
- **Millennials/Gen Z**: Tech-forward, mobile-first, feature-driven engagement
- **Gen X**: Larger balances, goal-oriented, stability-focused
- **High-Income Professionals**: Premium features, tax optimization, low churn

**Segmentation Implications**:
- Multi-product customers have 3-4x lower churn than cash-only
- Interest rate changes affect segments differently (cash users most sensitive)
- Debit card usage correlates with retention
- CEO scandal + deposit outflows create multi-factor churn risk concentrated in cash-only segment

---

## Recent Developments

| Date | Development | Type | Metric Impact |
|------|-------------|------|---------------|
| 2026-01-30 | Cash Account APY raised to 3.30% (referral 3.80-4.05%) — defensive measure | Product | cash_account_balances, customer_churn_rate — stem outflows |
| 2026-01-12 | First earnings: $208M net deposit outflows; stock dropped 17% | Financial | cash_account_balances, customer_churn_rate — RED FLAG |
| 2026-01-12 | CEO 95.1% ownership of home-lending entity disclosed; fraud investigations | Strategic | customer_churn_rate, customer_acquisition — trust crisis |
| 2025-12-12 | IPO on Nasdaq at $14/share, raising $485M. S-1: cash mgmt = 76% of revenue | Strategic | All metrics — public scrutiny, interchange revenue disclosed |
| 2025-11-19 | Home Lending launched in CO then TX. Median waitlist: age 35, $310K balance | Product | multi_product_adoption, customer_churn_rate — mortgage = sticky |
| 2025-H2 | Nasdaq-100 Direct Indexing launched. $5K min, 0.12% fee | Product | multi_product_adoption, avg_account_balance — attracts HNW |
| 2025-H2 | Cash Account UX: transaction search, CSV export, real-time notifications | Product | debit_card_usage_rate — better UX increases engagement |
| 2025-07 | Joint Cash Account launched — dual debit cards, joint direct deposit | Product | debit_card_usage_rate, cash_account_balances — 2x cards per household |
| 2025-06-01 | Bond Ladder fee reduced 0.25% → 0.15% | Product | multi_product_adoption — more competitive pricing |

---

## Available Metrics (Semantic Layer)

### Merchant Spend (via `product_stack` = Wealthfront)
- `total_auth_amount`, `total_auth_count` — debit card transaction volume
- `total_approved_amount`, `total_approved_count` — successful transactions
- `total_decline_amount`, `total_decline_count` — failed transactions
- `decline_rate`, `ewallet_decline_rate` — health indicators
- Dimensions: `merchant`, `mcc_category`, `mcc_desc`, `card_present`, `pos_entry_mode`, `responsecode`

### Disbursements (via `program_code` = Wealthfront programs)
- `total_completed_count`, `total_completed_amount` — transfers/withdrawals
- `total_declined_count`, `total_failed_count` — failed transfers
- `oct_success_rate` — instant transfer health
- `avg_transaction_size` — transfer economics
- Dimensions: `transfer_type`, `global_fund_transfer_status_reason`, `debit_network`

### Registrations (via `product_stack` = Wealthfront)
- `registration_started`, `registration_passed`, `registration_failed` — onboarding funnel
- `activation_rate`, `pass_rate` — conversion health
- Dimensions: `event_date`, `days_since_start`

---

## Data Quality Notes

- Merchant spend validated for Wealthfront product_stack
- Wealthfront debit card usage patterns differ from other partners — consumers using it as primary checking
- $208M outflow period (Q4 2025) may show up as declining transaction volume and registration slowdown
- Joint account launch (mid-2025) may show as registration spike — each joint account = 2 debit cards
- Cannot distinguish cash-only vs. multi-product customers from Green Dot data alone
- Interest rate sensitivity means seasonal/macro patterns may dominate partner-specific trends

---

## Analyst Findings

<!--
WRITEBACK SECTION — Appended by /analyze after each synthesis.
Schema per finding (danielrosehill evidence chain):

### [YYYY-MM-DD] [Brief title]
- **Claim**: [What the analysis found]
- **Evidence**: [Specific metrics, queries, and values that support the claim]
- **Confidence**: HIGH | MEDIUM | LOW
- **Gap**: [What additional data would strengthen or refute this claim]
- **Source**: [Which analyst(s) surfaced this]
- **Session**: [GUID]
- **Status**: ACTIVE | SUPERSEDED | DISPROVEN
-->

### 2026-02-12 Healthiest decline rate in portfolio despite corporate crisis
- **Claim**: Wealthfront's decline rate (15.8-18.7%) is the best in the portfolio and stable, despite $208M outflows, -42% stock, and CEO scandal. CNP approval rate (~72%) is HALF the portfolio's decline burden. The crisis is an AUM/stock story, not a cardholder behavior story.
- **Evidence**: `spend_decline_rate_by_count` monthly. Nov: 15.8%, Dec: 16.3%, Jan: 18.7%, Feb: 17.9%. CNP approval: 69.9-74.3% (best of any partner). CP: 96.4-97.2%.
- **Confidence**: HIGH
- **Gap**: If deposit outflows accelerate and avg account balance drops below spending thresholds, decline rates could spike. Monitor for insufficient-funds share increasing.
- **Source**: Portfolio ensemble. Exploratory flagged as "unexpected outperformer"; Statistical confirmed stability (7/10 confidence as noise).
- **Session**: 4d33b7d5-110f-4dc7-9b28-dbbd54918659
- **Status**: ACTIVE

### 2026-02-19 Highest eWallet adoption (31.8%) with best approval rate — validates wallet+healthy accounts
- **Claim**: Wealthfront leads all partners in eWallet adoption (31.8%) AND has the highest overall approval rate (74.7%). CP approval is 94.0%. This combination indicates that high-eWallet adoption co-occurs with healthy cardholder populations, not lower approval.
- **Evidence**: `spend_ewallet_share_by_count` by product_stack: Wealthfront 31.8%. `spend_approval_rate_by_count`: 74.7%. `spend_cp_approval_rate`: 94.0%.
- **Confidence**: HIGH
- **Gap**: Correlation, not causation — Wealthfront demographics (higher-income, better-funded) likely explain both high eWallet and high approval independently.
- **Source**: Forensic + Exploratory (consensus); Critic confirmed no causal claim
- **Session**: dafdc0f0-7a3e-41a1-b04c-84215ea1aa7a
- **Status**: ACTIVE

### 2026-02-23 Geographic: Most geographically distinct partner — knowledge-economy coastal footprint
- **Claim**: Wealthfront is the only partner statistically distinct from ALL other partners (JS distance >0.20 against all four). Effect size w=0.48 (LARGE), geographic HHI=823 (1.49x the 5-partner average of 554). CA holds 22.6% of Wealthfront accounts (PI=1.93, 44% of chi-sq deviation). DC is EXTREME at PI~4.0 (z=+5.7–7.7σ depending on pop baseline). Under-indexes inland/lower-income states: WV (PI=0.31), MS (PI=0.35), KY (PI=0.38). The Wealthfront/Amazon Flex polarity traces the US income divide — MS (+1.55 Flex-dominant) to DC (-2.99 Wealthfront-dominant). NY over-indexes at PI=1.40 (49.8% of NY's 5-partner account mix, making NY the most concentrated top-5 state at HHI=0.34).
- **Evidence**: 252,366 accounts (2025), `int_baas_account_details_extended` joined to `stg_edw__dim_account`. KL divergence=0.107 nats (highest of all partners). Chi-sq=58,018. CA contribution: 25,739 (44%). Result-Checker independently verified CA count (56,874) and Crypto-NY artifact (61 accounts).
- **Confidence**: HIGH (N=252,366; all measures independently verified by Result-Checker)
- **Gap**: CA concentration (22.6% in one state) represents geographic risk — any CA-specific regulatory change, competitive entry, or natural disaster would disproportionately affect this partner. The income-following pattern is INFERRED from external Census data cross-walked with partner positioning, not directly measured in our data.
- **Source**: Consensus (4/4 analysts); Statistical provided effect sizes and JS distances, Exploratory surfaced income polarity pattern
- **Session**: geo-distribution-2026-02-23
- **Status**: ACTIVE

### 2026-02-24 Metro-level: Knowledge-economy coastal footprint, 9 metros to 50%
- **Claim**: Investment (Wealthfront) dominates knowledge-economy coastal metros at CBSA level: SJ(PI=1.65, z=+2.43), SF(1.58, z=+2.14), Seattle(1.42), DC(1.37), NY(1.32), LA(1.35). Needs only 9 metros to reach 50% of its base vs 12 for Gig/Consumer — most concentrated partner by this measure. Strongly anti-correlated with Gig Economy (r=-0.79, p<0.01, n=30). Expansion gaps: Kansas City (-1,533 accounts below parity), Charlotte (-1,415), Detroit (-1,147).
- **Evidence**: `int_geo__account_geography` top 30 CBSAs, 2025 registrations (N=518,871). CBSA HHI=0.0444 (highest of 5 partners). Metro share=60.22%. CV of PI vector=0.221 (lowest — consistently above parity rather than spiking).
- **Confidence**: HIGH (PI values verified 4/4 analysts; correlation tested against r>0.361 threshold at n=30)
- **Gap**: Time-series PI data would distinguish durable patterns from period-specific. Mid-market expansion feasibility unknown post-IPO crisis ($208M outflows).
- **Source**: Consensus (4/4 analysts); Statistical quantified correlation and z-scores; Business sized gaps
- **Session**: a8d61a76-4442-4c03-a0ff-d8d899ecac9b
- **Status**: ACTIVE

### 2026-02-19 Automotive declines at $3,592/avg — likely limit/funding issue, not ISF
- **Claim**: Wealthfront Automotive MCC shows 810 declines at $3,592 avg over 4 months ($2.9M total). This is the highest per-decline amount of any partner×MCC combination. Given Wealthfront cardholders hold investment accounts, true ISF at this ticket size is unlikely — suggesting a card limit, funding timing, or authorization policy mismatch rather than cardholder financial distress.
- **Evidence**: `mrt_merchant_auth_decline_analytics` by mcc_category and product_stack. Wealthfront Automotive: 810 declines, $2.9M, $3,592 avg. Compare: Dayforce Automotive $582 avg, QuickBooks $527 avg.
- **Confidence**: MEDIUM (volume observed; ISF-unlikely hypothesis is INFERRED from cardholder profile context)
- **Gap**: Need response code breakdown restricted to Wealthfront Automotive to confirm root cause. If ISF, may indicate same-day funding gap between investment liquidation and card availability.
- **Source**: Business (surfaced) + Exploratory (confirmed anomaly); 3/4 analysts noted
- **Session**: 3bf85050-88f8-403b-a3ae-c9de6e68ea53
- **Status**: ACTIVE

---

## Known Gaps

0. **Geographic dimension partially available** — State-level analysis via ZIP-to-state mapping now works (see 2026-02-23 finding). CA concentration risk (22.6%) identified. Sub-state metro-level analysis still unavailable.
1. **No deposit balance data** — Can't directly measure the $208M outflow from Green Dot's perspective
2. **No product mix dimension** — Can't distinguish cash-only vs. multi-product customers
3. **No AUM data** — Investment portfolio metrics are Wealthfront-internal
4. **No interest rate sensitivity dimension** — Can't directly tie behavior to APY changes
5. **Joint account identification** — May not be distinguishable from individual accounts in Green Dot data
6. **Home lending impact** — Mortgage customers should be stickier, but can't measure from card data

---

## Open Questions

- Is there a measurable decline in transaction volume or registration rates post-IPO crisis (Jan 2026)?
- Do joint account holders (since mid-2025) show different spending patterns than individual accounts?
- What does the MCC distribution look like? (Wealthfront users likely skew toward daily essentials, subscriptions)
- How does Wealthfront's decline rate compare to other partners? (Consumer checking use case)
- Can we detect the defensive APY raise (Jan 2026) impact on new registrations?
- **HIGH PRIORITY**: Is the deposit outflow visible in our disbursement data as increased withdrawal volume?
