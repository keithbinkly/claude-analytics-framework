# Data Limitations Reference

Known data model limitations that prevent certain analytics. Use this to:
1. Quickly answer "can we do X?" questions
2. Provide stakeholders with accurate explanations
3. Suggest alternatives when the ideal approach isn't possible

---

## Limitation 1: Virtual Card Transaction Attribution

**Date Discovered:** December 2025
**Investigation:** `handoffs/interchange_revenue_migration/phase0-virtual-card-deep-dive.md`
**Decision Doc:** `handoffs/interchange_revenue_migration/model-docs/virtual-card-DESCOPED.md`

### The Ask

"Show me transactions made with virtual cards vs physical cards"

### Why It's Not Possible

| Data Point | Available? | Location |
|------------|------------|----------|
| Account has virtual card | Yes | `dim_payment_instrument_type.pymt_instrument_type_desc = 'Virtual Account'` |
| Which instrument used per txn | **No** | `pymt_instrument_uid` not in `fct_authorization_transaction` |
| Card not present flag | Yes | `card_present_ind` / `pos_entry_mode` |

**Root cause:** Transactions only record `pymt_identifier_uid`, which is shared by ALL instruments on an account (physical + virtual). Cannot distinguish which specific card was used.

**Compounding factor:** 23M+ accounts have BOTH physical and virtual cards.

### Stakeholder Response

> "The transaction data doesn't record which specific card instrument was used for each transaction. We CAN tell you Apple Pay vs Google Pay vs physical card via eWallet attribution, which gives you the payment method insight you're looking for."

### Alternative

Use **eWallet attribution** instead:
- Transaction-level: knows exactly which wallet (Apple Pay, Google Pay, Samsung Pay)
- Pattern: `gbos.paymentidentifierdevice` + `gbos.wallettype`
- See: `model-docs/ewallet-attribution-README.md`

---

## Template: Adding New Limitations

```markdown
## Limitation N: [Short Name]

**Date Discovered:** [Month Year]
**Investigation:** [link to discovery doc]
**Decision Doc:** [link to decision/descoped doc]

### The Ask

"[What stakeholders asked for]"

### Why It's Not Possible

| Data Point | Available? | Location |
|------------|------------|----------|
| [what's needed] | Yes/No | [where it is or isn't] |

**Root cause:** [Technical explanation]

### Stakeholder Response

> "[Copy-paste response for stakeholders]"

### Alternative

[What CAN be done instead]
```

---

*Last updated: December 2025*
