#!/usr/bin/env python3
"""
Unified Knowledge Graph Search API

Searches the graph index, traverses relationships, and returns content
from underlying stores. Single entry point for all knowledge retrieval.

Usage:
    .venv/bin/python3 -m tools.kg.graph_search "incremental merge"
    .venv/bin/python3 -m tools.kg.graph_search "merge" --stores learnings,traces
    .venv/bin/python3 -m tools.kg.graph_search "merge" --depth 2
    .venv/bin/python3 -m tools.kg.graph_search "merge" --json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

# Resolve workspace root (analytics-workspace) — this is the promoted AW copy
# graph_search.py → graph/ → platform/ → knowledge/ → analytics-workspace/
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent.parent
PROJECT_ROOT = WORKSPACE_ROOT / "dbt-agent"  # dbt-agent content uses relative paths from here
INDEX_PATH = WORKSPACE_ROOT / "knowledge" / "platform" / "graph" / "unified-index.json"


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class GraphResult:
    node_id: str
    store: str
    type: str
    title: str
    relevance: float
    content: str
    related: list[dict]  # [{node_id, store, title, edge_type}]
    store_path: str


# ---------------------------------------------------------------------------
# Index loading (cached in-memory for the process lifetime)
# ---------------------------------------------------------------------------

_cached_index: dict | None = None
_cached_adjacency: dict | None = None


def _load_index() -> dict:
    """Load the unified index JSON. Cached after first call."""
    global _cached_index
    if _cached_index is not None:
        return _cached_index
    if not INDEX_PATH.exists():
        print(f"ERROR: Index not found at {INDEX_PATH}", file=sys.stderr)
        print("Run: .venv/bin/python3 -m tools.kg.index_builder", file=sys.stderr)
        sys.exit(1)
    _cached_index = json.loads(INDEX_PATH.read_text())
    return _cached_index


def _build_adjacency(index: dict) -> dict[str, list[tuple[str, dict]]]:
    """Build adjacency list from edges. Returns {node_id: [(neighbor_id, edge_dict)]}."""
    global _cached_adjacency
    if _cached_adjacency is not None:
        return _cached_adjacency
    adj: dict[str, list[tuple[str, dict]]] = {}
    for edge in index.get("edges", []):
        fid = edge["from_id"]
        tid = edge["to_id"]
        adj.setdefault(fid, []).append((tid, edge))
        adj.setdefault(tid, []).append((fid, edge))
    _cached_adjacency = adj
    return _cached_adjacency


# ---------------------------------------------------------------------------
# Step 2.1.1: Query -> Matching Nodes
# ---------------------------------------------------------------------------

def _match_nodes(
    query: str,
    index: dict,
    stores: list[str] | None = None,
    min_weight: float = 0.3,
) -> list[tuple[str, float]]:
    """Find nodes matching the query. Returns (node_id, relevance_score) pairs."""

    query_lower = query.lower()
    query_words = set(query_lower.split())

    scored = []
    for node_id, node in index["nodes"].items():
        # Store filter
        if stores and node["store"] not in stores:
            continue

        # Weight filter
        if node.get("weight", 1.0) < min_weight:
            continue

        # Skip promoted-to-CAF nodes (suppressed)
        if node.get("promoted_to_caf", False):
            continue

        score = 0.0

        # 1. Topic match (highest signal) -- check both exact and substring
        node_topics = set(node.get("topics", []))
        topic_overlap = query_words & node_topics
        score += len(topic_overlap) * 0.3

        # Also check if any query word is a substring of a topic or vice versa
        for qw in query_words:
            for t in node_topics:
                if qw != t and (qw in t or t in qw):
                    score += 0.15

        # 2. Title substring match (full query phrase)
        title_lower = node.get("title", "").lower()
        if query_lower in title_lower:
            score += 0.5

        # 3. Summary substring match (full query phrase)
        summary_lower = node.get("summary", "").lower()
        if query_lower in summary_lower:
            score += 0.2

        # 4. Individual word matches in title
        title_words = set(title_lower.split())
        word_overlap = query_words & title_words
        score += len(word_overlap) * 0.1

        # 5. Individual word matches in summary
        summary_words = set(summary_lower.split())
        summary_word_overlap = query_words & summary_words
        score += len(summary_word_overlap) * 0.05

        # 6. Apply curator weight multiplier
        score *= node.get("weight", 1.0)

        if score > 0:
            scored.append((node_id, score))

    return sorted(scored, key=lambda x: -x[1])


# ---------------------------------------------------------------------------
# Step 2.1.2: Graph Traversal
# ---------------------------------------------------------------------------

def _traverse(
    node_id: str,
    adjacency: dict[str, list[tuple[str, dict]]],
    depth: int,
    visited: set[str],
) -> list[tuple[str, dict]]:
    """Follow edges from a node up to `depth` hops.
    Returns list of (neighbor_id, edge_dict) pairs."""

    if depth == 0 or node_id in visited:
        return []

    visited.add(node_id)
    results = []

    for neighbor_id, edge in adjacency.get(node_id, []):
        if neighbor_id not in visited:
            results.append((neighbor_id, edge))
            # Recurse for deeper traversal
            results.extend(_traverse(neighbor_id, adjacency, depth - 1, visited))

    return results


def _find_edge_type(adjacency: dict, from_id: str, to_id: str) -> str:
    """Find the edge type between two nodes."""
    for neighbor_id, edge in adjacency.get(from_id, []):
        if neighbor_id == to_id:
            return edge.get("type", "related")
    return "related"


# ---------------------------------------------------------------------------
# Step 2.1.3: Content Retrieval (fetch from underlying stores)
# ---------------------------------------------------------------------------

def _resolve_path(store_path: str) -> Path:
    """Resolve a store_path to an absolute Path. Tries dbt-agent first, then workspace root."""
    # Try dbt-agent (most store_paths are relative to PROJECT_ROOT)
    p = PROJECT_ROOT / store_path
    if p.exists():
        return p
    # Try workspace root (for CAF/enterprise paths like knowledge/... or docs/...)
    p2 = WORKSPACE_ROOT / store_path
    if p2.exists():
        return p2
    # Try without leading slash
    p3 = PROJECT_ROOT / store_path.lstrip("/")
    if p3.exists():
        return p3
    return p  # Return original even if missing


def _fetch_learning(path: str, anchor: str) -> str:
    """Parse YAML file, find entry by anchor (id), return trigger + action + rationale."""
    fpath = _resolve_path(path)
    if not fpath.exists():
        return f"[File not found: {path}]"

    text = fpath.read_text()

    # Find the entry block by ID using regex
    # Entries look like: "  - id: efx-007\n    ...\n    ...\n"
    pattern = rf"  - id:\s*{anchor}\b(.*?)(?=\n  - id:|\npatterns:|\nworkflow_patterns:|\ndata_insights:|\ndomain_knowledge:|\Z)"
    match = __import__("re").search(pattern, text, __import__("re").DOTALL)
    if not match:
        return f"[Entry {anchor} not found in {path}]"

    block = match.group(0)

    # Extract key fields
    trigger = _extract_yaml_field(block, "trigger")
    action = _extract_yaml_field(block, "action")
    rationale = _extract_yaml_field(block, "rationale")

    parts = []
    if trigger:
        parts.append(f"TRIGGER: {trigger}")
    if action:
        parts.append(f"ACTION: {action}")
    if rationale:
        parts.append(f"RATIONALE: {rationale}")
    return "\n".join(parts) if parts else block.strip()[:500]


def _extract_yaml_field(block: str, field_name: str) -> str:
    """Extract a quoted or unquoted YAML field value from a text block."""
    import re
    # Match: field_name: "value" or field_name: 'value' or field_name: value
    pattern = rf'{field_name}:\s*"([^"]*)"'
    m = re.search(pattern, block)
    if m:
        return m.group(1)
    pattern = rf"{field_name}:\s*'([^']*)'"
    m = re.search(pattern, block)
    if m:
        return m.group(1)
    pattern = rf"{field_name}:\s*(.+)"
    m = re.search(pattern, block)
    if m:
        val = m.group(1).strip()
        # Don't return if it's another key
        if val and not val.startswith("-"):
            return val
    return ""


def _fetch_trace(path: str, anchor: str) -> str:
    """Parse traces.json, find trace by id, return problem + resolution."""
    fpath = _resolve_path(path)
    if not fpath.exists():
        return f"[File not found: {path}]"

    data = json.loads(fpath.read_text())
    traces = data.get("traces", [])
    for trace in traces:
        if trace.get("id") == anchor:
            symptom = trace.get("problem", {}).get("symptom", "")
            root_cause = trace.get("resolution", {}).get("root_cause", "")
            fix = trace.get("resolution", {}).get("fix", "")
            return f"PROBLEM: {symptom}\nROOT CAUSE: {root_cause}\nFIX: {fix}"

    return f"[Trace {anchor} not found in {path}]"


def _fetch_synthesized_rule(path: str, anchor: str) -> str:
    """Parse rules.json, find rule by pattern_id, return pattern + action."""
    fpath = _resolve_path(path)
    if not fpath.exists():
        return f"[File not found: {path}]"

    data = json.loads(fpath.read_text())
    rules = data.get("rules", [])
    for rule in rules:
        if rule.get("pattern_id") == anchor:
            symptom = rule.get("pattern", {}).get("generalized_symptom", "")
            first_try = rule.get("recommended_action", {}).get("first_try", "")
            rationale = rule.get("recommended_action", {}).get("rationale", "")
            return f"PATTERN: {symptom}\nACTION: {first_try}\nRATIONALE: {rationale}"

    return f"[Rule {anchor} not found in {path}]"


def _fetch_markdown(path: str, max_chars: int = 500) -> str:
    """Read markdown file, return first max_chars of content."""
    fpath = _resolve_path(path)
    if not fpath.exists():
        return f"[File not found: {path}]"

    text = fpath.read_text()
    # Strip leading whitespace and # heading markers for cleaner output
    lines = text.strip().split("\n")
    # Skip empty lines at start
    content_lines = []
    for line in lines:
        content_lines.append(line)
    content = "\n".join(content_lines)
    if len(content) > max_chars:
        content = content[:max_chars] + "..."
    return content


def _fetch_experience_cluster(path: str, anchor: str) -> str:
    """Return summary for an experience cluster node."""
    # anchor format: "exp-cluster-{tag}" or "exp-{id}"
    fpath = _resolve_path(path)
    if not fpath.exists():
        return f"[File not found: {path}]"

    if anchor.startswith("exp-cluster-"):
        tag = anchor.replace("exp-cluster-", "")
        data = json.loads(fpath.read_text())
        experiences = data.get("experiences", data) if isinstance(data, dict) else data
        matching = [e for e in experiences if tag in e.get("tags", [])]
        if matching:
            descs = [e.get("description", "")[:100] for e in matching[:3]]
            return f"{len(matching)} sessions involving '{tag}'.\nExamples:\n" + "\n".join(
                f"  - {d}" for d in descs
            )
        return f"Experience cluster for tag '{tag}'"
    else:
        # Individual experience
        data = json.loads(fpath.read_text())
        experiences = data.get("experiences", data) if isinstance(data, dict) else data
        for exp in experiences:
            if exp.get("id") == anchor:
                desc = exp.get("description", "")
                return desc[:500]
        return f"[Experience {anchor} not found]"


def _fetch_content(node: dict) -> str:
    """Pull actual content from the underlying store for a matched node."""
    store = node["store"]
    path = node.get("store_path", "")
    anchor = node.get("anchor", "")

    if store == "learnings":
        return _fetch_learning(path, anchor)
    elif store == "traces":
        return _fetch_trace(path, anchor)
    elif store == "rules" and node.get("type") == "synthesized_rule":
        return _fetch_synthesized_rule(path, anchor)
    elif store == "claude_rules":
        return _fetch_markdown(path, max_chars=500)
    elif store == "skills":
        return _fetch_markdown(path, max_chars=500)
    elif store in ("knowledge_base", "reference"):
        return _fetch_markdown(path, max_chars=500)
    elif store == "experiences":
        return _fetch_experience_cluster(path, anchor)

    return f"[Content from {store}:{path}]"


# ---------------------------------------------------------------------------
# Step 2.1.4: Main Search Function
# ---------------------------------------------------------------------------

def search_graph(
    query: str,
    max_results: int = 10,
    stores: list[str] | None = None,
    traverse_depth: int = 1,
    min_weight: float = 0.3,
) -> list[GraphResult]:
    """
    Search the unified knowledge graph.

    Returns ranked results with content pulled from underlying stores.
    """
    index = _load_index()
    adjacency = _build_adjacency(index)

    # 1. Find matching nodes
    matches = _match_nodes(query, index, stores, min_weight)

    # 2. For top matches, traverse to find related nodes and fetch content
    results = []
    for node_id, score in matches[:max_results]:
        node = index["nodes"][node_id]

        # Traverse edges
        connected = _traverse(node_id, adjacency, traverse_depth, set())
        related = []
        for cid, edge in connected[:5]:  # cap related at 5
            cnode = index["nodes"].get(cid)
            if cnode:
                edge_type = edge.get("type", "related")
                related.append({
                    "node_id": cid,
                    "store": cnode["store"],
                    "title": cnode["title"],
                    "edge_type": edge_type,
                })

        content = _fetch_content(node)

        results.append(GraphResult(
            node_id=node_id,
            store=node["store"],
            type=node["type"],
            title=node["title"],
            relevance=round(score, 3),
            content=content,
            related=related,
            store_path=node.get("store_path", ""),
        ))

    # 3. Update last_accessed timestamps (non-blocking, best-effort)
    _update_access_times(index, [r.node_id for r in results])

    return results


# ---------------------------------------------------------------------------
# Access time tracking
# ---------------------------------------------------------------------------

def _update_access_times(index: dict, node_ids: list[str]) -> None:
    """Update last_accessed timestamps in the index. Best-effort, no crash on failure."""
    if not node_ids:
        return
    try:
        now = datetime.now(timezone.utc).isoformat()
        changed = False
        for nid in node_ids:
            if nid in index["nodes"]:
                index["nodes"][nid]["last_accessed"] = now
                changed = True
        if changed:
            INDEX_PATH.write_text(json.dumps(index, indent=2))
    except Exception:
        pass  # Non-critical -- don't crash search for timestamp updates


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

STORE_LABELS = {
    "learnings": "LEARNING",
    "traces": "TRACE",
    "rules": "RULE",
    "claude_rules": "RULE",
    "skills": "SKILL",
    "knowledge_base": "KB",
    "reference": "REF",
    "experiences": "EXP",
}


def format_human(results: list[GraphResult], query: str, elapsed_ms: float) -> str:
    """Format results for human-readable CLI output."""
    if not results:
        return f'No results for "{query}" ({elapsed_ms:.0f}ms)'

    stores_found = set(r.store for r in results)
    lines = [
        f'Found {len(results)} results across {len(stores_found)} stores ({elapsed_ms:.0f}ms):',
        "",
    ]

    for i, r in enumerate(results, 1):
        label = STORE_LABELS.get(r.store, r.store.upper())
        lines.append(f"[{i}] {label} {r.node_id} (relevance: {r.relevance}, weight: 1.0)")
        lines.append(f"    {r.title[:120]}")
        lines.append(f"    -> {r.store_path}")

        # Show content preview (first 2 lines)
        if r.content and not r.content.startswith("["):
            content_lines = r.content.strip().split("\n")
            for cl in content_lines[:2]:
                lines.append(f"    | {cl[:120]}")

        # Show related nodes
        if r.related:
            lines.append("    Related:")
            for j, rel in enumerate(r.related):
                rel_label = STORE_LABELS.get(rel["store"], rel["store"].upper())
                connector = "|--" if j < len(r.related) - 1 else "`--"
                lines.append(
                    f"      {connector} {rel_label} {rel['node_id']} ({rel['edge_type']}) "
                    f'"{rel["title"][:60]}"'
                )

        lines.append("")

    return "\n".join(lines)


def format_json(results: list[GraphResult]) -> str:
    """Format results as JSON for programmatic consumption."""
    return json.dumps([asdict(r) for r in results], indent=2)


# ---------------------------------------------------------------------------
# CLI interface
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Search the unified knowledge graph",
        prog="python3 -m tools.kg.graph_search",
    )
    parser.add_argument("query", help="Search query")
    parser.add_argument(
        "--stores",
        help="Comma-separated store filter (e.g. learnings,traces)",
        default=None,
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=1,
        help="Edge traversal depth (default: 1)",
    )
    parser.add_argument(
        "--max",
        type=int,
        default=10,
        help="Maximum results (default: 10)",
    )
    parser.add_argument(
        "--min-weight",
        type=float,
        default=0.3,
        help="Minimum node weight (default: 0.3)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON",
    )

    args = parser.parse_args()

    store_filter = args.stores.split(",") if args.stores else None

    t0 = time.monotonic()
    results = search_graph(
        query=args.query,
        max_results=args.max,
        stores=store_filter,
        traverse_depth=args.depth,
        min_weight=args.min_weight,
    )
    elapsed_ms = (time.monotonic() - t0) * 1000

    if args.json:
        print(format_json(results))
    else:
        print(format_human(results, args.query, elapsed_ms))


if __name__ == "__main__":
    main()
