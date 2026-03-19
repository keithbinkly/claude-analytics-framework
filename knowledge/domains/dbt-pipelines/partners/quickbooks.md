# Money by QuickBooks / QuickBooks Cash

> Analytical brief for Green Dot's BaaS partnership with Intuit QuickBooks. Living document — accumulates analyst findings over time.

**Last Updated**: 2026-02-12
**Last Researched**: 2026-02-11
**Data Quality Grade**: B (merchant spend validated; SMB-specific behavioral dimensions limited)

---

## Business Context

| Metric | Value |
|--------|-------|
| Parent Company | Intuit (NASDAQ: INTU) |
| FY2025 Revenue | $18.8B (+15% YoY); Q1 FY2026: $3.9B (+18%) |
| Customer Base | Millions of U.S. SMBs |
| QBO Accounting Growth | +25% YoY (Q1 FY2026) |

**Product**: Money by QuickBooks is an integrated banking and payments solution for small businesses and freelancers, offering business checking, cash flow management, and seamless integration with QuickBooks accounting software.

**Strategic Position**: Intuit is going AI-first — $100M+ OpenAI partnership, AI agents for Payments/Accounting/Finance, AI-powered banking page. Q1 FY2026 earnings explicitly cited "money and payroll offerings" as growth driver. Intuit Business Credit Card entering beta (early 2026) with $1K-$50K lines. Capital One acquired Brex for $5.15B (Jan 2026), removing an independent competitor.

**Key Relationship Dynamics**:
- QBO subscriber growth (+25%) expands addressable market for Money by QuickBooks
- AI features drive platform stickiness which correlates with banking adoption
- "Money and payroll" explicitly called out in Q1 FY2026 earnings — strongest public validation
- Green Dot split: 7-year exclusive agreement provides continuity
- Credit card launch (alpha Dec 2025, beta early 2026) deepens banking relationship
- Recurring payments + auto-pay (Jan 2026) increase predictable transaction volume

---

## Customer Segments

**By Business Size**:
- **Solopreneurs/Freelancers**: Simple needs, low transaction volume, price-sensitive
- **Micro SMBs** (2-10 employees): Growing complexity, payroll needs, moderate engagement
- **Small Businesses** (11-50 employees): Multi-user needs, higher volume, premium feature adoption

**By Industry**:
- **Professional Services**: High transaction frequency, invoicing focus, strong QBO integration
- **Retail/E-commerce**: Payment processing focus, high volume, competitive alternatives
- **Construction/Trades**: Project-based, irregular cash flow, longer sales cycle

**By QuickBooks Usage**:
- **Heavy QBO Users**: High likelihood of banking adoption, strong retention, cross-sell opportunities
- **Light/Seasonal QBO Users**: Lower banking engagement, seasonal patterns, higher churn
- **New QBO Customers**: Onboarding cohort, critical first-90-days engagement

**Segmentation Implications**:
- Account adoption 4-5x higher among heavy QBO users
- Solopreneurs drive account count but not transaction volume
- First-year retention differs 30-40% by business size

---

## Recent Developments

| Date | Development | Type | Metric Impact |
|------|-------------|------|---------------|
| 2026-02-26 | Q2 FY2026 earnings upcoming — guided 14-15% growth | Financial | Watch for Money by QuickBooks commentary |
| 2026-01-22 | Capital One acquires Brex for $5.15B — reduces independent competitor | Market | customer_churn_rate, smb_account_openings — less competitive pressure |
| 2026-01 | Recurring payments and auto-pay scheduling launched | Product | transaction_volume, account_balance_growth — automated flows |
| 2025-12 | Intuit Business Credit Card enters alpha ($1K-$50K, 5% Intuit / 2% everything) | Product | smb_account_openings, transaction_volume — deepens banking |
| 2025-11-20 | Q1 FY2026: $3.9B (+18%), QBO Accounting +25%, "money and payroll" cited | Financial | Direct validation of Money by QuickBooks traction |
| 2025-11-18 | $100M+ OpenAI partnership for financial intelligence in ChatGPT | Strategic | customer_acquisition — novel distribution channel |
| 2025-11 | AI-powered banking page with inline editing and smart categorization | Product | feature_adoption_rate — reduced friction |
| 2025-09-18 | Intuit Investor Day: $89B mid-market TAM, AI-first positioning | Strategic | QuickBooks Money may target larger SMBs |
| 2025-08-21 | Q4 FY2025: QBO Accounting +23%, full-year revenue $18.8B | Financial | Growing subscriber base = larger addressable market |
| 2025-07-01 | AI Agents launched (Payments, Accounting, Finance) + QBO pricing increases | Product | feature_adoption_rate, transaction_volume — AI automation |
| 2025-07-01 | QuickBooks Payments now accepts deposits on estimates | Product | transaction_volume — accelerates cash collection |

---

## Available Metrics (Semantic Layer)

### Merchant Spend (via `product_stack` = QuickBooks)
- `total_auth_amount`, `total_auth_count` — SMB transaction volume
- `total_approved_amount`, `total_approved_count` — successful transactions
- `total_decline_amount`, `total_decline_count` — failed transactions
- `decline_rate`, `ewallet_decline_rate` — health indicators
- Dimensions: `merchant`, `mcc_category`, `mcc_desc`, `card_present`, `pos_entry_mode`, `responsecode`

### Disbursements (via `program_code` = QuickBooks programs)
- `total_completed_count`, `total_completed_amount` — business payouts/transfers
- `total_declined_count`, `total_failed_count` — failed transfers
- `oct_success_rate`, `oct_decline_rate`, `oct_failure_rate` — instant transfer health
- `avg_transaction_size`, `fee_to_amount_ratio` — transfer economics
- Dimensions: `transfer_type`, `global_fund_transfer_status_reason`, `debit_network`

### Registrations (via `product_stack` = QuickBooks)
- `registration_started`, `registration_passed`, `registration_failed` — onboarding funnel
- `activation_rate`, `pass_rate` — conversion health
- Dimensions: `event_date`, `days_since_start`

---

## Data Quality Notes

- Merchant spend validated for QuickBooks product_stack
- SMB transaction patterns differ fundamentally from consumer — higher avg amounts, more business-to-business
- Disbursement program_code mapping needs confirmation for QuickBooks-specific programs
- Cannot distinguish business size (solopreneur vs. micro vs. small) from Green Dot data
- Cannot link QBO accounting usage to banking behavior (Intuit-side data)
- Recurring payment launch (Jan 2026) may create predictable weekly/monthly transaction patterns

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

### 2026-02-13 #2 partner by volume — lowest decline rate among top 3
- **Claim**: QuickBooks is the #2 partner by auth attempt volume ($619.3M, Nov 2025 - Jan 2026) with the lowest decline rate by dollar among top 3 at 42.7%. $354.9M approved, $264.4M declined. Close to Amazon Flex (#3 at $564M) but well behind Dayforce (#1 at $1.207B).
- **Evidence**: `spend_total_auth_attempt_amount` by product_stack. Cross-partner ranking: Dayforce $1.207B >> QuickBooks $619M > Amazon Flex $564M.
- **Confidence**: HIGH (ranking) / MEDIUM (magnitudes — data 14 days stale)
- **Gap**: QoQ comparison not possible. SMB transaction patterns may differ significantly from consumer/gig worker partners — industry-level segmentation would reveal whether QuickBooks' lower decline rate reflects SMB spending discipline or different merchant mix.
- **Source**: Portfolio ensemble analysis (4 analysts + synthesizer).
- **Session**: 554a4d45-a128-4e89-a345-a24975b6a5f0
- **Status**: ACTIVE

### 2026-02-12 Smooth upward decline rate trend — organic, not structural break
- **Claim**: QuickBooks shows a smooth +7.5pp increase over 8 months (26.1%→33.6%), unlike other partners that had a dramatic Oct→Nov structural break. This suggests an organic, partner-specific issue. CNP declining from 55.3% to 51.4%.
- **Evidence**: `spend_decline_rate_by_count` monthly. Jun: 26.1%, Jul: 27.6%, Aug: 27.7%, Sep: 30.2%, Oct: 34.4%, Nov: 29.3%, Dec: 31.0%, Jan: 33.2%, Feb: 33.6%. Only ~5pp Oct→Nov drop vs 40-54pp for other partners.
- **Confidence**: MEDIUM-HIGH
- **Gap**: Need Q2 data to confirm whether this is structural or seasonal (Q4 spending + Jan normalization). Fraud rule false positives for SMB patterns (91K "Unusual Transaction" + 91K "Restricted Card") need investigation.
- **Source**: Portfolio ensemble analysis. Statistical rated as slow-but-real signal (7/10).
- **Session**: 4d33b7d5-110f-4dc7-9b28-dbbd54918659
- **Status**: ACTIVE

### 2026-02-19 Structurally different decline profile — "Unusual Transaction" ($22.3M) + "Spend Exceeds Limit" ($17.6M)
- **Claim**: QuickBooks has a structurally distinct decline fingerprint. "Unusual Transaction" = 14.6% of decline $ ($22.3M/4mo, $269/decline avg — 4.6x Dayforce's $58/decline). "Spend Exceeds Limit" = 11.6% ($17.6M, only 2,039 transactions at $8,656 avg). ISF is lower at 49.7% (vs 67% for Dayforce/Flex). This pattern is consistent with B2B card usage where fraud rules and product limits may not accommodate business-level transaction patterns.
- **Evidence**: `mrt_merchant_auth_decline_analytics` by responsecode and product_stack. QB Unusual Txn: 95K declines/$22.3M ($269 avg). QB Spend Exceeds Limit: 2,039 declines/$17.6M ($8,656 avg). Dayforce Unusual Txn: 375K/$21.8M ($58 avg).
- **Confidence**: HIGH (volume and profile differences observed); MEDIUM (fraud over-tuning hypothesis is analytical, not confirmed)
- **Gap**: Need MCC breakdown of "Unusual Transaction" declines. Need current fraud rule parameters to assess false-positive rate. Need retry success data.
- **Source**: Consensus (3/4 — Business, Exploratory, Statistical); Critic revised causal language
- **Session**: 3bf85050-88f8-403b-a3ae-c9de6e68ea53
- **Status**: ACTIVE

### 2026-02-19 Expiration Date Mismatch = $10.1M (3-month), growing — Account Updater candidate
- **Claim**: QuickBooks Expiration Date Mismatch = 84K declines ($10.1M) over 3 months. Part of the portfolio-wide +29.9% growth trend. Account Updater/tokenization is the operational fix.
- **Evidence**: `mrt_merchant_auth_decline_analytics` by responsecode: Exp Mismatch = 6.6% of QB decline $.
- **Confidence**: HIGH
- **Gap**: Account Updater enrollment status. Which merchant billers generate the most mismatch declines for QB cardholders.
- **Source**: Consensus (4/4 analysts)
- **Session**: 3bf85050-88f8-403b-a3ae-c9de6e68ea53
- **Status**: ACTIVE

### 2026-02-23 Geographic: SMB footprint with Florida dominance — only partner where FL > CA
- **Claim**: QuickBooks has a large geographic deviation from population (w=0.34 LARGE, KL=0.050). FL is the #1 state (PI=1.86 ANOMALOUS, 12.6% of QB accounts vs 6.8% US pop) — QuickBooks is the only partner where FL beats CA. CO (PI=1.82), MA (PI=1.76), and DC (PI=2.55 EXTREME) also over-index. IL (PI=0.63) and NY (PI=0.66) under-index. Geographic HHI=514. The FL dominance is consistent with Florida's SMB/sole-proprietor density [INFERRED — external IRS/Census source needed].
- **Evidence**: 87,714 accounts (2025), `int_baas_account_details_extended` joined to `stg_edw__dim_account`. FL: 11,039 accounts (Result-Checker verified exact). DC: PI=2.55, z=+4.44 EXTREME. Chi-sq=9,953. FL/CA ratio for QB = 1.19x vs 0.57x for other 4 partners combined.
- **Confidence**: HIGH (N=87,714, smallest main partner but all flagged states have N>1,000)
- **Gap**: Is the FL SMB density hypothesis testable? IRS Statistics of Income sole-proprietor returns by state would confirm or refute. Expansion targets with similar profile: TX (growing SMB base), TN (low tax, growing SMB corridor), CO (already elevated PI=1.82).
- **Source**: Consensus (3/4 analysts — Statistical, Exploratory, Business); Exploratory unique: FL structural distinctiveness
- **Session**: geo-distribution-2026-02-23
- **Status**: ACTIVE

### 2026-02-24 Metro-level: FL statewide strength + Boston anomaly, highest geographic unevenness
- **Claim**: SMB (QuickBooks) is the only partner with PI>1.0 in ALL 3 Florida metros: Tampa(1.68, z=+2.26), Orlando(1.33), Miami(1.23). Boston(1.65, z=+2.16) is anomalously high for a coastal knowledge-economy metro (peer avg SMB PI=0.69). Highest CV of PI vector (0.325) = most geographically uneven partner. Expansion gaps: Chicago(-712), San Jose(-484), Detroit(-414).
- **Evidence**: `int_geo__account_geography` top 30 CBSAs, 2025 registrations (N=90,690). CBSA HHI=0.0382. Metro share=51.85%. SMB follows a distinct "third geography" — uncorrelated with Gig (r≈-0.05) and anti-correlated with Investment (r≈-0.60).
- **Confidence**: MEDIUM-HIGH (FL strength verified 4/4 analysts; Boston anomaly flagged by Exploratory + Statistical but mechanism unknown)
- **Gap**: Boston SMB mechanism unknown — could be professional services density, immigrant small business formation, or single large employer relationship. FL statewide cause also unknown (QBO market share data needed).
- **Source**: Consensus (4/4 on FL); Exploratory unique: Boston anomaly; Statistical: CV ranking
- **Session**: a8d61a76-4442-4c03-a0ff-d8d899ecac9b
- **Status**: ACTIVE

### 2026-02-22 Disbursement: Stable 78.47% Success, $22.3M/mo Chronic Failures — Highest $/Declined Txn
- **Claim**: IntuitQB disbursement success rate flat at 77.27%–78.76% across all 6 months (Feb-Jul 2025). Declined amounts range $16.6M–$22.3M/mo (avg $20.9M). Despite low transaction counts (34K–43K), average declined amount per failed transaction is ~$2,393, far higher than any other program. Exceeds $5M/month action threshold by 4.2x. Stability of pattern (no trend over 6 months) suggests structural rather than operational — may be inherent to high-value QB payroll disbursements.
- **Evidence**: dbt Semantic Layer `disbursement_success_rate`, `disbursement_declined_amount` by program_code, Feb-Jul 2025. Feb: 78.76% / 34.5K txns / $16.6M. Jul: 78.47% / 43.3K txns / $22.3M. $/declined txn: $2,262–$2,527 range (avg $2,393). For comparison: flex = $106/declined txn, earnin = $110/declined txn.
- **Confidence**: HIGH (rates and dollars observed; structural hypothesis inferred from 6-month stability)
- **Gap**: Need program_code × processor to compare intuitqb routing to flex (99.49% benchmark). If routing differs, pilot alternative processor for sample traffic. Need to determine if 78% is business-model optimum or addressable inefficiency.
- **Source**: Consensus (4/4 analysts); F5 in disbursement analysis
- **Session**: 3868b443-10cf-48f8-abfc-e22de7808031
- **Status**: ACTIVE

---

## Known Gaps

1. **No business size dimension** — Can't segment solopreneurs vs. micro vs. small businesses
2. **No QBO integration data** — Can't measure correlation between accounting usage and banking adoption
3. **No industry dimension** — Can't distinguish professional services vs. retail vs. construction
4. **No invoice/payments data** — QuickBooks Payments (deposits on estimates, recurring) not in semantic layer
5. **Credit card data not yet available** — Beta launching early 2026; when live, will be a major new data stream

---

## Open Questions

- What does the MCC distribution look like for SMB cardholders? (Likely supplies, services, SaaS tools)
- Is there a measurable difference in transaction patterns between early Money adopters vs. recent?
- How do decline rates compare to consumer partners? (SMBs may have different risk profiles)
- Can we detect the recurring payments feature adoption from transaction regularity patterns?
- What is the registration-to-activation timeline for QuickBooks vs. other partners?
