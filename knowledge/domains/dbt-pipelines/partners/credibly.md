# Credibly

> Analytical brief for Green Dot's BaaS partnership with Credibly. Living document — accumulates analyst findings over time.

**Last Updated**: 2026-02-12
**Last Researched**: 2026-02-11
**Data Quality Grade**: B- (merchant spend available; lending-specific metrics not in semantic layer)

---

## Business Context

| Metric | Value |
|--------|-------|
| Company Type | Private |
| Loan Volume | ~$2B+ originated since founding |
| Customer Base | Tens of thousands of SMBs |
| AI Patents | 2 granted in 3 months (Oct 2025, Jan 2026) |

**Product**: Credibly is a fintech lender specializing in SMB financing — working capital loans, merchant cash advances, and business expansion loans. Through its partnership with Green Dot, Credibly provides embedded business checking accounts to borrowers.

**Strategic Position**: Credibly is betting heavily on AI-automated underwriting (2 patents in 3 months). The macro environment is favorable: banks continue tightening SMB lending even as Fed cuts rates, pushing more borrowers to alternative lenders. Non-bank lender share has doubled from 20% to 40% since 2018. However, industry-wide online lender satisfaction collapsed from 15% to 2% net — customer experience is the critical differentiator.

**Key Relationship Dynamics**:
- Business checking cross-sell is the key Green Dot lever — lending is Credibly's core business, checking is the add-on
- Green Dot split: embedded finance continues under long-term exclusive agreement (7-year)
- Account adoption rates are the primary metric for Green Dot (not loan volume)
- Working capital borrowers are best repeat candidates — bridge financing also good
- Cloudsquare API integration (Mar 2025) streamlines broker channel

---

## Customer Segments

**By Loan Purpose**:
- **Working Capital**: Seasonal businesses, repeat borrowers, moderate risk — best for checking cross-sell
- **Growth/Expansion**: One-time larger loans, lower repeat rate, higher default risk
- **Bridge Financing**: Short-term needs, fast repayment, good repeat candidates

**By Industry Risk Profile**:
- **Low Risk** (Professional Services, SaaS): Higher approval rates, better terms, repeat borrowing
- **Medium Risk** (Retail, Food Service): Standard terms, moderate repeat rates
- **Higher Risk** (Construction, Hospitality): Stricter terms, lower repeat rates, economic sensitivity

**By Credit Profile**:
- **Prime Borrowers**: Alternative to bank loans, rate-shopping, lower loyalty
- **Near-Prime**: Core customer base, balanced risk-return, moderate repeat borrowing
- **Subprime**: Higher rates, less likely to qualify for repeat loans, collection focus

**Segmentation Implications**:
- Repeat borrowing rates vary 50%+ by loan purpose
- Account adoption (checking) higher among working capital borrowers
- Default risk metrics must be segment-adjusted for meaningful comparison

---

## Recent Developments

| Date | Development | Type | Metric Impact |
|------|-------------|------|---------------|
| 2026-01 | Second AI patent granted (US 12,505,113 B2) — affordability evaluation, offer structuring | Product | application_approval_rate, avg_loan_size — enhanced AI capabilities |
| 2026-01-21 | Fundbox raised $100M Series D + expanded to Australia | Market | Competitor expanding; less direct overlap (Fundbox = smaller loans) |
| 2026-01 | NFIB Optimism 99.3 (above 52-yr avg) but uncertainty index +7 points | Economic | Working capital may outperform expansion loans |
| 2025-11-23 | Green Dot $1.1B breakup — checking continues under 7-year agreement | Strategic | account_adoption_rate — continuity assured |
| 2025-10 | First AI patent granted (US 12,443,612 B2) — GenAI + neural networks for underwriting | Product | application_approval_rate, loan_origination_volume — faster decisions |
| 2025-03 | Cloudsquare API integration — direct Salesforce-to-Credibly broker pipeline | Product | loan_origination_volume — streamlined broker submissions |

**Market Context**:
- Non-bank lender share doubled: 20% → 40% since 2018; 74% of SMBs prefer non-bank
- Fed cut rates 3x in 2025 to 3.50-3.75%, but banks continued tightening (8% tightened for small firms)
- Online lender satisfaction collapsed: 15% → 2% net (Fed SBCS 2025) — CX is critical
- Texas, Louisiana, North Dakota enacted MCA regulations; ~12 states now have frameworks
- Capital One acquired Brex ($5.15B, Jan 2026) — reduces independent SMB fintech competitor

---

## Available Metrics (Semantic Layer)

### Merchant Spend (via `product_stack` = Credibly)
- `total_auth_amount`, `total_auth_count` — business checking card usage
- `total_approved_amount`, `total_approved_count` — successful transactions
- `total_decline_amount`, `total_decline_count` — failed transactions
- `decline_rate` — health indicator
- Dimensions: `merchant`, `mcc_category`, `mcc_desc`, `card_present`, `pos_entry_mode`, `responsecode`

### Disbursements (via `program_code` = Credibly programs)
- `total_completed_count`, `total_completed_amount` — loan disbursements / transfers
- `total_declined_count`, `total_failed_count` — failed disbursements
- `oct_success_rate` — instant transfer health
- `avg_transaction_size` — disbursement economics
- Dimensions: `transfer_type`, `global_fund_transfer_status_reason`, `debit_network`

### Registrations (via `product_stack` = Credibly)
- `registration_started`, `registration_passed`, `registration_failed` — checking account onboarding
- `activation_rate`, `pass_rate` — conversion from loan customer to checking customer
- Dimensions: `event_date`, `days_since_start`

---

## Data Quality Notes

- Merchant spend available for Credibly product_stack but expected to be lower volume than consumer partners
- Credibly's core business is lending — Green Dot only sees the checking/card side
- Loan volume, approval rates, default rates are Credibly-internal metrics not in our semantic layer
- Business checking usage patterns differ from consumer: fewer transactions, larger amounts, B2B payments
- Registration funnel may show unique patterns — borrowers being cross-sold to checking vs. checking-first

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

### 2026-02-12 100% decline rate — program appears broken or shut down
- **Claim**: Credibly's decline rate reached 100% in Feb 2026 (99.8% in Jan). Zero transactions are being approved. This is not a trend — it is a program-level operational issue requiring immediate investigation.
- **Evidence**: `spend_decline_rate_by_count` monthly. Nov: 71.8%, Dec: 95.8%, Jan: 99.8%, Feb: 100.0%. CNP approval: 0.0% in Feb.
- **Confidence**: HIGH (that something is operationally wrong) / LOW (3/10 that this represents normal business)
- **Gap**: Confirm with partner ops whether Credibly cards are intentionally blocked, program is winding down, or there is a configuration error.
- **Source**: Portfolio ensemble (all 4 analysts noted, Statistical rated 3/10 confidence as normal activity)
- **Session**: 4d33b7d5-110f-4dc7-9b28-dbbd54918659
- **Status**: ACTIVE

---

## Known Gaps

1. **No lending metrics** — Loan volume, approval rate, default rate, repeat borrowing are Credibly-internal
2. **No borrower segmentation** — Can't distinguish loan purpose, industry, or credit profile from Green Dot data
3. **No checking cross-sell conversion data** — Can't measure % of loan customers who adopt checking
4. **Lowest data volume** — Credibly likely has the smallest transaction footprint among the 5 partners
5. **AI underwriting impact unmeasurable** — Can't see if AI patents translate to faster/better decisions
6. **MCA regulation impact** — Can't measure state-level regulatory effects without geographic dimension

---

## Open Questions

- What is the actual checking account adoption rate among Credibly loan customers?
- How does business checking card usage differ from consumer card usage? (MCC distribution, avg amounts)
- Is there a correlation between loan disbursement timing and checking account activation?
- Do repeat borrowers use the checking account more actively than one-time borrowers?
- What is the registration-to-activation timeline compared to consumer partners?
- **Is Credibly's transaction volume material enough to analyze separately, or should it be grouped with "SMB partners"?**
