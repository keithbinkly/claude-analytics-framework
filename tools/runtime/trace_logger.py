#!/usr/bin/env python3
"""
Decision Trace Logger with PKO Integration

Logs decision traces and automatically:
1. Links traces to known failure modes
2. Discovers novel failure patterns
3. Updates the traces.json and index

Usage:
    from tools.runtime.trace_logger import log_trace, enrich_existing_traces

    # Log a new trace
    trace = {
        "id": "qa_2026-01-18_001",
        "model": "my_model",
        "problem": {"symptom": "..."},
        "resolution": {"fix": "..."}
    }
    log_trace(trace)

    # Enrich existing traces with failure mode links
    enrich_existing_traces()
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

# Import PKO diagnosis
TOOLS_PATH = Path(__file__).parent
import sys
sys.path.insert(0, str(TOOLS_PATH))

from pko_diagnose import discover_failure_mode


# Paths
TRACES_PATH = Path(__file__).parent.parent.parent / "shared/decision-traces/traces.json"
INDEX_PATH = Path(__file__).parent.parent.parent / "shared/decision-traces/index.json"
EMERGING_PATH = Path(__file__).parent.parent.parent / "shared/knowledge-base/pko/failure-modes/emerging.json"


def load_traces() -> dict:
    """Load existing traces."""
    if TRACES_PATH.exists():
        with open(TRACES_PATH) as f:
            return json.load(f)
    return {"version": "1.0", "traces": []}


def save_traces(data: dict) -> None:
    """Save traces to file."""
    data["last_updated"] = datetime.utcnow().isoformat() + "Z"
    with open(TRACES_PATH, "w") as f:
        json.dump(data, f, indent=2)


def load_emerging() -> dict:
    """Load emerging failure modes (awaiting confirmation)."""
    if EMERGING_PATH.exists():
        with open(EMERGING_PATH) as f:
            return json.load(f)
    return {"version": "1.0", "emerging_failure_modes": []}


def save_emerging(data: dict) -> None:
    """Save emerging failure modes."""
    EMERGING_PATH.parent.mkdir(parents=True, exist_ok=True)
    data["last_updated"] = datetime.utcnow().isoformat() + "Z"
    with open(EMERGING_PATH, "w") as f:
        json.dump(data, f, indent=2)


def log_trace(trace: dict) -> dict:
    """
    Log a new decision trace with PKO failure mode linking.

    Args:
        trace: Trace dict with id, model, problem, resolution fields

    Returns:
        Enriched trace with PKO fields added
    """
    # Discover linked failure mode
    discovery = discover_failure_mode(trace)

    # Add PKO fields to trace
    trace["pko"] = {
        "linked_failure_mode": discovery["matched_failure_mode"],
        "match_score": discovery["match_score"],
        "is_novel": discovery["is_novel"],
        "linked_at": datetime.utcnow().isoformat() + "Z"
    }

    # If it's a known failure, add the executes_procedure link
    if discovery["matched_failure_mode"]:
        trace["pko"]["executes_procedure"] = "pipeline-build-playbook"
        trace["pko"]["executes_step"] = _infer_step(trace)

    # Load and update traces
    data = load_traces()
    data["traces"].insert(0, trace)  # Add to beginning (most recent first)
    save_traces(data)

    # If novel, add to emerging failure modes
    if discovery["is_novel"] and discovery["suggested_failure_mode"]:
        emerging = load_emerging()
        emerging["emerging_failure_modes"].append(discovery["suggested_failure_mode"])
        save_emerging(emerging)
        print(f"Novel failure mode detected: {discovery['suggested_failure_mode']['name']}")

    return trace


def _infer_step(trace: dict) -> Optional[str]:
    """Infer which playbook step this trace relates to."""
    context = trace.get("problem", {}).get("context", "")
    fix_category = trace.get("resolution", {}).get("fix_category", "")

    # Simple mapping based on context/category
    if context == "migration":
        return "implement_model"
    elif context == "refactoring":
        return "implement_model"
    elif context == "incremental_testing":
        return "configure_incremental"
    elif fix_category == "join_cardinality":
        return "map_canonicals"
    elif fix_category == "data_quality":
        return "analyze_tech_spec"
    elif fix_category == "filter_missing":
        return "implement_model"

    return "validate_qa"  # Default to QA step


def enrich_existing_traces() -> dict:
    """
    Enrich existing traces with PKO failure mode links.

    Returns:
        Summary of enrichment results
    """
    data = load_traces()
    results = {
        "total_traces": len(data["traces"]),
        "already_linked": 0,
        "newly_linked": 0,
        "novel_detected": 0,
        "details": []
    }

    emerging = load_emerging()

    for trace in data["traces"]:
        # Skip if already has PKO data
        if "pko" in trace:
            results["already_linked"] += 1
            continue

        # Discover failure mode
        discovery = discover_failure_mode(trace)

        # Add PKO fields
        trace["pko"] = {
            "linked_failure_mode": discovery["matched_failure_mode"],
            "match_score": discovery["match_score"],
            "is_novel": discovery["is_novel"],
            "linked_at": datetime.utcnow().isoformat() + "Z"
        }

        if discovery["matched_failure_mode"]:
            trace["pko"]["executes_procedure"] = "pipeline-build-playbook"
            trace["pko"]["executes_step"] = _infer_step(trace)
            results["newly_linked"] += 1
            results["details"].append({
                "trace_id": trace["id"],
                "linked_to": discovery["matched_failure_mode"]
            })
        elif discovery["is_novel"]:
            results["novel_detected"] += 1
            if discovery["suggested_failure_mode"]:
                emerging["emerging_failure_modes"].append(discovery["suggested_failure_mode"])

    # Save updated data
    save_traces(data)
    save_emerging(emerging)

    return results


def get_traces_by_failure_mode(failure_mode_id: str) -> list[dict]:
    """Get all traces linked to a specific failure mode."""
    data = load_traces()
    return [
        t for t in data["traces"]
        if t.get("pko", {}).get("linked_failure_mode") == failure_mode_id
    ]


def get_novel_traces() -> list[dict]:
    """Get all traces flagged as novel (no matching failure mode)."""
    data = load_traces()
    return [
        t for t in data["traces"]
        if t.get("pko", {}).get("is_novel", False)
    ]


# CLI interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python trace_logger.py enrich  # Enrich existing traces")
        print("       python trace_logger.py novel   # Show novel traces")
        print("       python trace_logger.py by-fm <failure_mode_id>  # Get traces by FM")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "enrich":
        results = enrich_existing_traces()
        print(json.dumps(results, indent=2))

    elif cmd == "novel":
        novel = get_novel_traces()
        print(f"Found {len(novel)} novel traces:")
        for t in novel:
            print(f"  - {t['id']}: {t.get('problem', {}).get('symptom', '')[:60]}...")

    elif cmd == "by-fm" and len(sys.argv) > 2:
        fm_id = sys.argv[2]
        traces = get_traces_by_failure_mode(fm_id)
        print(f"Found {len(traces)} traces linked to {fm_id}:")
        for t in traces:
            print(f"  - {t['id']}: {t.get('model', 'unknown')}")

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
