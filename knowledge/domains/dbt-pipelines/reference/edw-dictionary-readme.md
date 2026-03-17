# EDW Data Dictionary - Quick Start

## What Just Happened?

You pasted **1,054 rows** of EDW field definitions from Confluence into `seeds/r1_edw_dictionary.csv`. This is now a **searchable reference** for business definitions that can be pulled into staging model YAML files.

## Conversion Summary

✅ **Converted**: TSV → CSV format  
✅ **File**: `seeds/r1_edw_dictionary.csv`  
✅ **Coverage**: 44 EDW entities, 884 fields with definitions (84%)  
✅ **Created**: 3 utility scripts for easy lookups

## Quick Commands

### 1. Look up a field definition
```bash
python .claude/quick-reference/dictionary_lookup.py merchant_nm
```

### 2. See all fields for a table
```bash
python .claude/quick-reference/dictionary_lookup.py --table FCT_POSTED_TRANSACTION
```

### 3. Search by keyword
```bash
python .claude/quick-reference/dictionary_lookup.py --search "interchange"
```

### 4. Generate YAML for staging model
```bash
python .claude/quick-reference/generate_staging_yml_from_dictionary.py FCT_POSTED_TRANSACTION
```

## Table → Staging Model Mapping

| EDW Entity | Staging Model | Fields |
|------------|---------------|--------|
| `FCT_POSTED_TRANSACTION` | `stg_edw__fct_posted_transaction` | 80 |
| `FCT_AUTHORIZATION_TRANSACTION` | `stg_edw__fct_authorization_transaction` | 75 |
| `DIM_ACCOUNT` | `stg_edw__dim_account` | 81 |
| `DIM_PRODUCT` | `stg_edw__dim_product` | 26 |
| `DIM_TXN_TYPE_HIERARCHY` | `stg_edw__dim_txn_type_hierarchy` | 38 |

## Example: Adding Definitions to Staging YML

**Your current staging model** (`stg_edw__fct_posted_transaction.sql`) has inline comments but no YML documentation.

**Quick workflow:**
```bash
# 1. Generate YAML skeleton
python .claude/quick-reference/generate_staging_yml_from_dictionary.py FCT_POSTED_TRANSACTION > /tmp/posted_yml.txt

# 2. Create/update schema.yml
# Copy relevant columns from /tmp/posted_yml.txt

# 3. View in dbt docs
dbt docs generate
dbt docs serve
```

## Files Created

1. **`.claude/quick-reference/generate_staging_yml_from_dictionary.py`**  
   Generates complete YAML column definitions from dictionary

2. **`.claude/quick-reference/dictionary_lookup.py`**  
   Interactive lookup tool for fields, tables, and keyword searches

3. **`.claude/quick-reference/using-edw-dictionary.md`**  
   Comprehensive guide with examples and best practices

4. **`.claude/quick-reference/README-dictionary.md`** (this file)  
   Quick start guide

## Statistics

```
📊 EDW DATA DICTIONARY SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Fields:              1,053
Unique EDW Entities:       44
Fields with Definitions:   884 (84.0%)
Primary Keys:              56
Foreign Keys:              137

Entity Types:
  • Fact Tables (FCT_*):     9
  • Dimension Tables (DIM_*): 35
  • Reference Tables:         0
```

## Top 10 Tables by Field Count

1. **DIM_ACCOUNT** (81 fields) - Account master data
2. **FCT_POSTED_TRANSACTION** (80 fields) - Settled transactions
3. **FCT_AUTHORIZATION_TRANSACTION** (75 fields) - Auth attempts
4. **FCT_ACCOUNT_BALANCE_DTL** (73 fields) - Account balance details
5. **FCT_AUTHORIZATION_TXN_AUDIT** (62 fields) - Auth audit trail
6. **FCT_DLY_ACCT_TXN_SUMMARY** (59 fields) - Daily account transaction summary
7. **FCT_DLY_POSTED_TXN_SUMMARY** (54 fields) - Daily posted transaction summary
8. **DIM_TXN_TYPE_HIERARCHY** (38 fields) - Transaction type taxonomy
9. **DIM_DATE** (34 fields) - Date dimension
10. **FCT_INTERCHANGE_TRANSACTION** (29 fields) - Interchange revenue/expense

## Next Steps

### Immediate Actions
- [ ] Test lookup scripts on a few tables you're working with
- [ ] Add dictionary definitions to 2-3 key staging models
- [ ] Share with team: "We now have searchable EDW definitions!"

### Future Enhancements
- [ ] Create dbt macro to auto-inject descriptions at compile time
- [ ] Add dbt test: validate staging columns exist in dictionary
- [ ] Create reverse mapping: staging model → EDW entity
- [ ] Integrate with dbt-expectations for data type validation

## Pro Tips

💡 **Keep it updated**: When Confluence dictionary changes, re-export and replace the CSV

💡 **Version control**: Dictionary is now in git - track changes over time

💡 **CI/CD**: Could add pre-commit hook to validate staging YMLs reference dictionary

💡 **Search patterns**: Use `grep` for quick lookups:
```bash
# Find all foreign keys to DIM_ACCOUNT
grep "ACCT_UID" seeds/r1_edw_dictionary.csv | grep "FK.*YES"

# Find all date fields
grep -i "dttm\|_dt" seeds/r1_edw_dictionary.csv
```

## Related Documentation

- **Comprehensive Guide**: `.claude/quick-reference/using-edw-dictionary.md`
- **Field Mappings**: `.claude/quick-reference/field-mappings.md`
- **Session Log**: `.claude/session-logs/2025-10-09-merchant-decline-analytics.md`

---

**Questions?** Run the lookup scripts or check `using-edw-dictionary.md` for detailed examples.
