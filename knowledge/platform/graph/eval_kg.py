#!/usr/bin/env python3
"""
Knowledge Graph Eval Suite

Measures whether graph_search surfaces the right knowledge for known problems.
Uses eval_cases.json — each case has a query and expected nodes/files that should
appear in the top-k results.

Usage:
    python3 knowledge/platform/graph/eval_kg.py              # Default k=5
    python3 knowledge/platform/graph/eval_kg.py --k 10       # Top-10
    python3 knowledge/platform/graph/eval_kg.py --verbose     # Show all results
    python3 knowledge/platform/graph/eval_kg.py --category qa # Filter by category

Metrics:
    - hit@k: Did ANY expected node appear in top-k? (binary per case)
    - precision@k: What fraction of expected nodes appeared in top-k?
    - MRR: Mean Reciprocal Rank of first expected hit
"""

import json
import sys
from pathlib import Path

# Add parent dirs so we can import graph_search
GRAPH_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(GRAPH_DIR))

from graph_search import _load_index, _match_nodes, _build_adjacency


def run_eval(k: int = 5, verbose: bool = False, category: str | None = None) -> dict:
    """Run the eval suite and return metrics."""

    cases_path = GRAPH_DIR / "eval_cases.json"
    cases_data = json.loads(cases_path.read_text())
    cases = cases_data["cases"]

    if category:
        cases = [c for c in cases if c["category"] == category]

    index = _load_index()
    _build_adjacency(index)

    results = []
    total_hit = 0
    total_precision = 0.0
    reciprocal_ranks = []

    for case in cases:
        query = case["query"]
        expected_nodes = set(case.get("expected_nodes", []))
        expected_files = set(case.get("expected_files", []))

        # Skip cases with no expected results (they test gaps, not retrieval)
        if not expected_nodes and not expected_files:
            if verbose:
                print(f"  SKIP {case['id']}: {case.get('note', 'no expected results')}")
            results.append({
                "id": case["id"],
                "category": case["category"],
                "status": "SKIP",
                "reason": case.get("note", "no expected results"),
            })
            continue

        # Run search
        matches = _match_nodes(query, index)
        top_k = matches[:k]
        top_k_ids = [m[0] for m in top_k]
        top_k_paths = []
        for node_id in top_k_ids:
            node = index["nodes"].get(node_id, {})
            top_k_paths.append(node.get("store_path", ""))

        # Check hits
        node_hits = expected_nodes & set(top_k_ids)
        file_hits = expected_files & set(top_k_paths)
        all_hits = node_hits | file_hits
        hit = len(all_hits) > 0

        # Precision: fraction of expected items found
        total_expected = len(expected_nodes | expected_files)
        precision = len(all_hits) / total_expected if total_expected > 0 else 0.0

        # Reciprocal rank of first hit
        rr = 0.0
        for rank, node_id in enumerate(top_k_ids, 1):
            node = index["nodes"].get(node_id, {})
            node_path = node.get("store_path", "")
            if node_id in expected_nodes or node_path in expected_files:
                rr = 1.0 / rank
                break

        total_hit += int(hit)
        total_precision += precision
        reciprocal_ranks.append(rr)

        status = "HIT" if hit else "MISS"
        results.append({
            "id": case["id"],
            "category": case["category"],
            "status": status,
            "precision": precision,
            "rr": rr,
            "hits": list(all_hits),
            "top_k": [(nid, f"{score:.2f}") for nid, score in top_k[:3]],
        })

        if verbose or not hit:
            icon = "+" if hit else "x"
            print(f"  [{icon}] {case['id']} ({case['category']}): {status}")
            print(f"      query: \"{query}\"")
            if hit:
                print(f"      found: {list(all_hits)}")
                print(f"      rank: {int(1/rr) if rr > 0 else 'N/A'}, precision: {precision:.0%}")
            else:
                print(f"      expected: {list(expected_nodes | expected_files)}")
                print(f"      got top-3: {[m[0] for m in top_k[:3]]}")

    # Aggregate metrics
    scored_cases = [r for r in results if r["status"] != "SKIP"]
    n = len(scored_cases)

    metrics = {
        "total_cases": len(cases),
        "scored_cases": n,
        "skipped_cases": len(cases) - n,
        "hit_at_k": total_hit,
        "hit_rate": total_hit / n if n > 0 else 0.0,
        "mean_precision": total_precision / n if n > 0 else 0.0,
        "mrr": sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0.0,
        "k": k,
    }

    return {"metrics": metrics, "results": results}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="KG Retrieval Eval Suite")
    parser.add_argument("--k", type=int, default=5, help="Top-k for retrieval (default: 5)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show all results")
    parser.add_argument("--category", "-c", type=str, help="Filter by category")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    print(f"\nKG Retrieval Eval (k={args.k})")
    print("=" * 50)

    output = run_eval(k=args.k, verbose=args.verbose, category=args.category)
    m = output["metrics"]

    print(f"\n{'=' * 50}")
    print(f"Results: {m['hit_at_k']}/{m['scored_cases']} hit ({m['hit_rate']:.0%})")
    print(f"Mean Precision@{m['k']}: {m['mean_precision']:.0%}")
    print(f"MRR: {m['mrr']:.3f}")
    print(f"Skipped: {m['skipped_cases']} (no expected results — gap tests)")

    # Category breakdown
    categories = {}
    for r in output["results"]:
        if r["status"] == "SKIP":
            continue
        cat = r["category"]
        if cat not in categories:
            categories[cat] = {"hit": 0, "total": 0}
        categories[cat]["total"] += 1
        if r["status"] == "HIT":
            categories[cat]["hit"] += 1

    if categories:
        print(f"\nBy category:")
        for cat, counts in sorted(categories.items()):
            rate = counts["hit"] / counts["total"]
            print(f"  {cat}: {counts['hit']}/{counts['total']} ({rate:.0%})")

    if args.json:
        print(f"\n{json.dumps(output, indent=2)}")


if __name__ == "__main__":
    main()
