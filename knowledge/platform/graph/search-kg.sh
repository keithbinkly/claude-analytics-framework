#!/usr/bin/env bash
# Quick fuzzy search over the Knowledge Graph index
# Usage: ./search-kg.sh [optional initial query]
#
# Requires: fzf (brew install fzf)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INDEX="$SCRIPT_DIR/unified-index.json"

if ! command -v fzf &>/dev/null; then
  echo "fzf not installed. Install with: brew install fzf"
  exit 1
fi

if [[ ! -f "$INDEX" ]]; then
  echo "No index found at $INDEX. Run index_builder.py first."
  exit 1
fi

python3 -c "
import json, sys
with open('$INDEX') as f:
    data = json.load(f)
for n in data.get('nodes', []):
    ntype = n.get('type','?')[:12]
    domain = n.get('domain','?')[:10]
    nid = n.get('id','?')[:45]
    summary = n.get('l0_summary', n.get('title', ''))[:80]
    source = n.get('source_file','')[:50]
    print(f'{ntype:<12} {domain:<10} {nid:<45} {summary}  [{source}]')
" | fzf --query="${1:-}" \
    --header="TYPE         DOMAIN     ID                                            SUMMARY" \
    --preview="echo {}" \
    --height=80% \
    --layout=reverse \
    --multi
