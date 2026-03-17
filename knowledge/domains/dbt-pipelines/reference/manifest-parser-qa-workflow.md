# Using Manifest Parser for QA Lineage Analysis

## Quick Reference: Getting Model Lineage

### Step 1: Find Your Model in Manifest

```python
import json
from pathlib import Path

# Load manifest
manifest_path = Path('/Users/kbinkly/git-repos/dbt_projects/dbt-enterprise/target/manifest.json')
with open(manifest_path) as f:
    manifest = json.load(f)

# Find model
target_model = 'your_model_name'
unique_id = None
for node_id, node in manifest['nodes'].items():
    if node.get('name') == target_model and node.get('resource_type') == 'model':
        unique_id = node_id
        break
```

### Step 2: Get Direct Parents (Where to Start QA)

```python
# These are the immediate upstream models you need to verify first
parents = manifest['parent_map'].get(unique_id, [])

print(f"Start QA here - Direct Parents ({len(parents)}):")
for parent_id in parents:
    if parent_id in manifest['nodes']:
        parent_node = manifest['nodes'][parent_id]
        print(f"  - {parent_node['name']}")
```

### Step 3: Get Full Lineage (For Complex Pipelines)

```python
def get_all_parents(manifest, node_id, visited=None):
    """Recursively get all upstream dependencies"""
    if visited is None:
        visited = set()
    if node_id in visited:
        return []
    visited.add(node_id)

    direct_parents = manifest['parent_map'].get(node_id, [])
    all_parents = list(direct_parents)

    for parent_id in direct_parents:
        all_parents.extend(get_all_parents(manifest, parent_id, visited))

    return all_parents

all_parents = get_all_parents(manifest, unique_id)
print(f"Total upstream dependencies: {len(set(all_parents))}")
```

---

## Example: QA Workflow for mart_rtp__multi_period_metrics

### Lineage Analysis Results

**Direct Parents (Start Here)**:
1. ✅ `int_rtp__aggregated_transfers` - Aggregated metrics layer
2. ✅ `stg_edw__dim_date` - Date dimension

**Full Upstream Chain**:
- **Staging**: 16 models (data ingestion layer)
- **Intermediate**: 2 models (business logic layer)
- **Sources**: 16 raw tables
- **Total**: 34 upstream dependencies

### QA Build Order

**Option A: Fast QA (7-day temp filter)**
```bash
# 1. Check if direct parents exist and are current
SELECT MAX(calendar_date) FROM int_rtp__aggregated_transfers;
SELECT MAX(calendar_date) FROM stg_edw__dim_date;

# 2. If stale, rebuild direct parents only
dbt run --select int_rtp__aggregated_transfers --full-refresh

# 3. Build target mart with temp filter
# (Add temp filter to mart SQL first)
dbt run --select mart_rtp__multi_period_metrics
```

**Option B: Full Lineage QA**
```bash
# 1. Build entire upstream tree
dbt run --select +mart_rtp__multi_period_metrics --exclude mart_rtp__multi_period_metrics

# 2. Verify intermediate layer
dbt test --select int_rtp__aggregated_transfers

# 3. Build target mart
dbt run --select mart_rtp__multi_period_metrics
```

---

## Decision Tree: Which Dependencies to Rebuild?

```
START: QA new mart model
│
├─ Check manifest: Get direct parents
│  └─ parent_map[unique_id]
│
├─ For each parent:
│  ├─ Check warehouse: SELECT MAX(date) FROM parent_model
│  │
│  ├─ If data is CURRENT (< 1 day old):
│  │  └─ ✅ SKIP rebuild (use existing)
│  │
│  ├─ If data is STALE (> 1 day old):
│  │  ├─ Check parent's manifest metadata
│  │  ├─ If incremental: dbt run --select parent
│  │  └─ If table: dbt run --select parent --full-refresh
│  │
│  └─ If model MISSING:
│     └─ Check parent's parents (recursive)
│        └─ Build entire upstream: dbt run --select +parent
│
└─ After all parents current:
   └─ Build target: dbt run --select target_model
```

---

## Practical Example Session

### Scenario: QA mart_rtp__multi_period_metrics

```python
# 1. Get lineage (30 seconds)
from manifest_parser import get_model_lineage

lineage = get_model_lineage('mart_rtp__multi_period_metrics')
# Result: 2 direct parents, 34 total upstream

# 2. Check parent freshness (1 minute)
SELECT
    'int_rtp__aggregated_transfers' as model,
    MAX(calendar_date) as max_date,
    DATEDIFF('day', MAX(calendar_date), CURRENT_DATE) as days_old
FROM analytics.int_rtp__aggregated_transfers

UNION ALL

SELECT
    'stg_edw__dim_date',
    MAX(calendar_date),
    DATEDIFF('day', MAX(calendar_date), CURRENT_DATE)
FROM analytics.stg_edw__dim_date;

# Results:
# int_rtp__aggregated_transfers: 2024-11-05 (2 days old - STALE)
# stg_edw__dim_date: 2024-11-06 (1 day old - OK)

# 3. Rebuild stale parent (5 minutes with temp filter)
# Add temp filter to int_rtp__aggregated_transfers.sql:
# WHERE calendar_date >= dateadd('day', -7, current_date)
# -- ⚠️ TODO: REMOVE after QA passes

dbt run --select int_rtp__aggregated_transfers

# 4. Build target mart (2 minutes with temp filter)
# Add same temp filter to mart_rtp__multi_period_metrics.sql

dbt run --select mart_rtp__multi_period_metrics

# 5. Run QA validation
# Use Template 1 from qa-validation-checklist.md
```

**Total Time**: 10 minutes (vs 60-90 min building entire lineage blind)

---

## Key Functions for Manifest Parser Skill

### Core Functions to Implement

```python
# manifest_parser.py

def get_model_lineage(model_name):
    """
    Returns: {
        'model_name': str,
        'unique_id': str,
        'parents': [parent_ids],
        'children': [child_ids],
        'parent_count': int,
        'child_count': int
    }
    """
    manifest = load_manifest()
    unique_id = find_unique_id(manifest, model_name)

    return {
        'model_name': model_name,
        'unique_id': unique_id,
        'parents': manifest['parent_map'].get(unique_id, []),
        'children': manifest['child_map'].get(unique_id, []),
        'parent_count': len(manifest['parent_map'].get(unique_id, [])),
        'child_count': len(manifest['child_map'].get(unique_id, []))
    }

def get_parent_models_names(model_name):
    """
    Returns human-readable parent model names
    """
    manifest = load_manifest()
    unique_id = find_unique_id(manifest, model_name)
    parents = manifest['parent_map'].get(unique_id, [])

    parent_names = []
    for parent_id in parents:
        if parent_id in manifest['nodes']:
            parent_names.append(manifest['nodes'][parent_id]['name'])
        elif parent_id in manifest['sources']:
            source = manifest['sources'][parent_id]
            parent_names.append(f"{source['source_name']}.{source['name']}")

    return parent_names

def get_full_upstream_lineage(model_name):
    """
    Returns all upstream dependencies organized by layer
    """
    manifest = load_manifest()
    unique_id = find_unique_id(manifest, model_name)

    def get_all_parents(node_id, visited=None):
        if visited is None:
            visited = set()
        if node_id in visited:
            return []
        visited.add(node_id)

        direct_parents = manifest['parent_map'].get(node_id, [])
        all_parents = list(direct_parents)

        for parent_id in direct_parents:
            all_parents.extend(get_all_parents(parent_id, visited))

        return all_parents

    all_parents = get_all_parents(unique_id)

    # Organize by layer
    by_layer = {
        'staging': [],
        'intermediate': [],
        'marts': [],
        'sources': []
    }

    for parent_id in set(all_parents):
        if parent_id in manifest['nodes']:
            node = manifest['nodes'][parent_id]
            path = node.get('original_file_path', '')
            name = node['name']

            if 'staging' in path:
                by_layer['staging'].append(name)
            elif 'intermediate' in path:
                by_layer['intermediate'].append(name)
            elif 'marts' in path:
                by_layer['marts'].append(name)

        elif parent_id in manifest['sources']:
            source = manifest['sources'][parent_id]
            by_layer['sources'].append(f"{source['source_name']}.{source['name']}")

    return {
        'by_layer': by_layer,
        'total_count': len(set(all_parents))
    }
```

---

## Integration with QA Workflow

### Update qa-validation-checklist.md Phase 2.0

```markdown
### 2.0 Dependency Analysis (MANDATORY)

**Step 1: Get lineage (30 seconds)**
```python
from manifest_parser import get_parent_models_names

parents = get_parent_models_names('mart_rtp__multi_period_metrics')
# Returns: ['int_rtp__aggregated_transfers', 'stg_edw__dim_date']
```

**Step 2: Check parent freshness (1 minute)**
```sql
-- For each parent, check if rebuild needed
SELECT MAX(calendar_date) FROM analytics.{parent_model};
```

**Step 3: Build dependencies (variable)**
- If current (< 1 day): ✅ Skip
- If stale (1-7 days): Incremental build
- If very stale (> 7 days): Full refresh
- If missing: Build full upstream lineage

**Step 4: Build target**
- Add temp filter for fast QA
- Build target model
```

---

## Time Savings Summary

| Method | Time | Outcome |
|--------|------|---------|
| **No lineage check** | 0 min | ❌ Build fails, discover missing deps via errors (60-90 min wasted) |
| **dbt ls command** | 5-10 min | ✅ Full list, but slow |
| **Manifest parser** | 30 sec | ✅ Instant lineage + impact analysis |

**ROI**: 10-20x faster than dbt ls, prevents 60-90 min of error-driven iteration

---

## References

- **Manifest Parser Skill**: `.claude/skills/manifest-parser/SKILL.md`
- **QA Checklist**: `shared/reference/qa-validation-checklist.md`
- **Session Learning**: `session-logs/2025-11-06_interchange_qa_learnings.md` (Mistake #1)
