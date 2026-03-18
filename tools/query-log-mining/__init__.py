"""
Query Log Mining Toolkit

Extracts structured knowledge from Redshift query logs for agent consumption.

Phase 2 of query log analysis - builds on Phase 1 narrative reports to create
machine-parseable YAML artifacts for:
- Join relationships (weighted graph)
- Controlled vocabulary (alias mining)
- Semantic model candidates (dimensions, measures, entities)
- Anti-pattern impact correlation
- Ratio metric candidates
- Saved query candidates

Usage:
    python -m tools.query_log_mining.main <command> [options]

Commands:
    parse           Parse all queries and cache results
    extract-joins   Build join registry from parsed queries
    mine-aliases    Extract column aliases for vocabulary
    infer-semantic  Infer dimensions, measures, entities
    analyze-impact  Correlate anti-patterns with execution time
    detect-ratios   Find ratio metric patterns
    cluster-queries Find saved query candidates
    run-all         Run complete pipeline

See: docs/specs/query-log-mining-phase2-spec.md for full specification
"""

__version__ = "0.1.0"
__author__ = "dbt-agent"

from .parser import QueryParser
from .join_extractor import JoinExtractor
from .alias_miner import AliasMiner
from .semantic_inferrer import SemanticInferrer
from .anti_pattern_analyzer import AntiPatternAnalyzer

__all__ = [
    "QueryParser",
    "JoinExtractor",
    "AliasMiner",
    "SemanticInferrer",
    "AntiPatternAnalyzer",
]
