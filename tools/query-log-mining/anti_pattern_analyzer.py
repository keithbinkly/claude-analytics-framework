"""
Anti-Pattern Impact Analyzer Module

Correlates anti-patterns with execution time to quantify actual performance impact.
Enables data-driven prioritization of fixes.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional
import yaml
import logging
import statistics
from datetime import datetime

from .parser import ParsedQuery

logger = logging.getLogger(__name__)


@dataclass
class PatternImpact:
    """Impact statistics for a single anti-pattern."""
    pattern: str
    frequency: int = 0
    execution_times: list = field(default_factory=list)

    # Computed stats
    avg_execution_sec: Optional[float] = None
    median_execution_sec: Optional[float] = None
    p95_execution_sec: Optional[float] = None
    std_dev: Optional[float] = None

    # Comparison with baseline
    baseline_avg: Optional[float] = None  # Avg of queries WITHOUT this pattern
    impact_multiplier: Optional[float] = None

    # Priority assignment
    priority: Optional[str] = None  # P0, P1, P2, P3

    def compute_stats(self) -> None:
        """Compute statistics from collected execution times."""
        if not self.execution_times:
            return

        times = self.execution_times
        self.avg_execution_sec = statistics.mean(times)
        self.median_execution_sec = statistics.median(times)

        if len(times) >= 2:
            self.std_dev = statistics.stdev(times)

        if len(times) >= 20:
            sorted_times = sorted(times)
            p95_idx = int(len(sorted_times) * 0.95)
            self.p95_execution_sec = sorted_times[p95_idx]

    def compute_impact(self, baseline_avg: float) -> None:
        """Compute impact multiplier compared to baseline."""
        self.baseline_avg = baseline_avg
        if baseline_avg and baseline_avg > 0 and self.avg_execution_sec:
            self.impact_multiplier = round(self.avg_execution_sec / baseline_avg, 2)
            self._assign_priority()

    def _assign_priority(self) -> None:
        """Assign priority based on impact and frequency."""
        if not self.impact_multiplier:
            self.priority = "P3"
            return

        # High impact OR high frequency = higher priority
        if self.impact_multiplier >= 5.0 or (self.impact_multiplier >= 2.0 and self.frequency >= 1000):
            self.priority = "P0"
        elif self.impact_multiplier >= 3.0 or (self.impact_multiplier >= 1.5 and self.frequency >= 500):
            self.priority = "P1"
        elif self.impact_multiplier >= 2.0:
            self.priority = "P2"
        else:
            self.priority = "P3"

    def to_dict(self) -> dict:
        result = {
            "pattern": self.pattern,
            "frequency": self.frequency,
        }

        if self.avg_execution_sec is not None:
            result["avg_execution_sec"] = round(self.avg_execution_sec, 2)
        if self.median_execution_sec is not None:
            result["median_execution_sec"] = round(self.median_execution_sec, 2)
        if self.p95_execution_sec is not None:
            result["p95_execution_sec"] = round(self.p95_execution_sec, 2)
        if self.baseline_avg is not None:
            result["baseline_avg_sec"] = round(self.baseline_avg, 2)
        if self.impact_multiplier is not None:
            result["impact_multiplier"] = f"{self.impact_multiplier}x"
        if self.priority:
            result["priority"] = self.priority

        return result


@dataclass
class PatternCombination:
    """Impact of pattern combinations (compounding effects)."""
    patterns: tuple
    frequency: int = 0
    execution_times: list = field(default_factory=list)
    avg_execution_sec: Optional[float] = None
    expected_avg: Optional[float] = None  # Sum of individual impacts
    compounding_factor: Optional[float] = None

    def compute_stats(self) -> None:
        if self.execution_times:
            self.avg_execution_sec = statistics.mean(self.execution_times)

    def compute_compounding(self, expected_avg: float) -> None:
        """Compute whether combination is worse than sum of parts."""
        self.expected_avg = expected_avg
        if expected_avg and expected_avg > 0 and self.avg_execution_sec:
            self.compounding_factor = round(self.avg_execution_sec / expected_avg, 2)

    def to_dict(self) -> dict:
        return {
            "patterns": list(self.patterns),
            "frequency": self.frequency,
            "avg_execution_sec": round(self.avg_execution_sec, 2) if self.avg_execution_sec else None,
            "compounding_factor": f"{self.compounding_factor}x" if self.compounding_factor else None,
        }


class AntiPatternAnalyzer:
    """
    Analyzes anti-pattern impact on query performance.

    Usage:
        analyzer = AntiPatternAnalyzer()
        for parsed, exec_time in zip(parsed_queries, execution_times):
            analyzer.add_query(parsed, exec_time)
        impact = analyzer.build_impact_report()
        analyzer.save_yaml("anti-pattern-impact.yml")
    """

    # Anti-pattern definitions
    PATTERNS = [
        "SELECT *",
        "DISTINCT in aggregation",
        "OR in JOIN",
        "CROSS JOIN",
        "NOT IN subquery",
        "Deep nesting (3+ levels)",
    ]

    def __init__(self):
        self._pattern_stats: dict[str, PatternImpact] = {
            p: PatternImpact(pattern=p) for p in self.PATTERNS
        }
        self._combinations: dict[tuple, PatternCombination] = {}
        self._all_times: list[float] = []
        self._clean_times: list[float] = []  # Queries with no anti-patterns
        self._query_count = 0

    def add_query(
        self,
        parsed: ParsedQuery,
        execution_time: Optional[float] = None
    ) -> None:
        """
        Add a query for anti-pattern analysis.

        Args:
            parsed: ParsedQuery object
            execution_time: Query execution time in seconds
        """
        self._query_count += 1

        if execution_time is not None:
            self._all_times.append(execution_time)

        # Detect which patterns are present
        detected = self._detect_patterns(parsed)

        if not detected and execution_time is not None:
            # Clean query - no anti-patterns
            self._clean_times.append(execution_time)

        # Track individual patterns
        for pattern in detected:
            self._pattern_stats[pattern].frequency += 1
            if execution_time is not None:
                self._pattern_stats[pattern].execution_times.append(execution_time)

        # Track combinations (2+ patterns)
        if len(detected) >= 2:
            combo_key = tuple(sorted(detected))
            if combo_key not in self._combinations:
                self._combinations[combo_key] = PatternCombination(patterns=combo_key)

            self._combinations[combo_key].frequency += 1
            if execution_time is not None:
                self._combinations[combo_key].execution_times.append(execution_time)

    def _detect_patterns(self, parsed: ParsedQuery) -> list[str]:
        """Detect which anti-patterns are present in a parsed query."""
        detected = []

        if parsed.has_select_star:
            detected.append("SELECT *")
        if parsed.has_distinct_in_agg:
            detected.append("DISTINCT in aggregation")
        if parsed.has_or_in_join:
            detected.append("OR in JOIN")
        if parsed.has_cross_join:
            detected.append("CROSS JOIN")
        if parsed.has_not_in_subquery:
            detected.append("NOT IN subquery")
        if parsed.subquery_depth >= 3:
            detected.append("Deep nesting (3+ levels)")

        return detected

    def compute_all_stats(self) -> None:
        """Compute statistics for all patterns."""
        # Baseline = clean queries (no anti-patterns)
        baseline_avg = None
        if self._clean_times:
            baseline_avg = statistics.mean(self._clean_times)
        elif self._all_times:
            # Fallback to overall average
            baseline_avg = statistics.mean(self._all_times)

        # Compute individual pattern stats
        for pattern_impact in self._pattern_stats.values():
            pattern_impact.compute_stats()
            if baseline_avg:
                pattern_impact.compute_impact(baseline_avg)

        # Compute combination stats
        for combo in self._combinations.values():
            combo.compute_stats()

            # Expected = sum of individual pattern impacts above baseline
            if baseline_avg:
                expected_overhead = sum(
                    (self._pattern_stats[p].avg_execution_sec or 0) - baseline_avg
                    for p in combo.patterns
                    if p in self._pattern_stats and self._pattern_stats[p].avg_execution_sec
                )
                expected_avg = baseline_avg + expected_overhead
                combo.compute_compounding(expected_avg)

    def build_impact_report(self) -> dict:
        """
        Build the complete impact report.

        Returns:
            Dictionary with pattern impacts and combinations
        """
        self.compute_all_stats()

        # Sort patterns by impact
        sorted_patterns = sorted(
            self._pattern_stats.values(),
            key=lambda p: p.impact_multiplier or 0,
            reverse=True
        )

        # Sort combinations by frequency
        sorted_combos = sorted(
            self._combinations.values(),
            key=lambda c: c.frequency,
            reverse=True
        )[:20]  # Top 20 combinations

        # Calculate baseline stats
        baseline_stats = {}
        if self._clean_times:
            baseline_stats = {
                "clean_query_count": len(self._clean_times),
                "clean_avg_sec": round(statistics.mean(self._clean_times), 2),
                "clean_median_sec": round(statistics.median(self._clean_times), 2),
            }

        return {
            "metadata": {
                "generated": datetime.now().isoformat(),
                "source": "Redshift query logs",
                "query_count": self._query_count,
                "queries_with_execution_time": len(self._all_times),
            },
            "baseline": baseline_stats,
            "impact_by_pattern": [p.to_dict() for p in sorted_patterns],
            "combinations": [c.to_dict() for c in sorted_combos if c.frequency >= 10],
        }

    def save_yaml(self, filepath: str) -> None:
        """
        Save impact report to YAML file.

        Args:
            filepath: Output file path
        """
        report = self.build_impact_report()

        with open(filepath, 'w') as f:
            yaml.dump(report, f, default_flow_style=False, sort_keys=False)

        logger.info(f"Saved anti-pattern impact report to {filepath}")
        logger.info(f"  Queries analyzed: {report['metadata']['query_count']}")

    def get_high_impact_patterns(self, threshold: float = 2.0) -> list[PatternImpact]:
        """
        Get patterns with impact multiplier above threshold.

        Args:
            threshold: Minimum impact multiplier

        Returns:
            List of PatternImpact objects
        """
        self.compute_all_stats()
        return [
            p for p in self._pattern_stats.values()
            if p.impact_multiplier and p.impact_multiplier >= threshold
        ]

    def summary(self) -> str:
        """Generate summary statistics."""
        self.compute_all_stats()

        lines = [
            "Anti-Pattern Impact Summary",
            "=" * 40,
            f"Total queries: {self._query_count}",
            f"Clean queries (no patterns): {len(self._clean_times)}",
            "",
        ]

        if self._clean_times:
            lines.append(f"Baseline (clean) avg: {statistics.mean(self._clean_times):.2f} sec")
            lines.append("")

        lines.append("Pattern Impact (sorted by multiplier):")

        for pattern in sorted(
            self._pattern_stats.values(),
            key=lambda p: p.impact_multiplier or 0,
            reverse=True
        ):
            if pattern.frequency > 0:
                mult = f"{pattern.impact_multiplier}x" if pattern.impact_multiplier else "N/A"
                pri = pattern.priority or "N/A"
                lines.append(
                    f"  [{pri}] {pattern.pattern}: {pattern.frequency}x, {mult} slower"
                )

        return "\n".join(lines)


def analyze_anti_patterns(
    parsed_queries: list[ParsedQuery],
    execution_times: Optional[list[float]] = None,
    output_path: Optional[str] = None
) -> dict:
    """
    Convenience function to analyze anti-patterns from parsed queries.

    Args:
        parsed_queries: List of ParsedQuery objects
        execution_times: Optional list of execution times (parallel to queries)
        output_path: Optional path to save YAML output

    Returns:
        Impact report dictionary
    """
    analyzer = AntiPatternAnalyzer()

    for i, parsed in enumerate(parsed_queries):
        exec_time = execution_times[i] if execution_times else None
        analyzer.add_query(parsed, exec_time)

    if output_path:
        analyzer.save_yaml(output_path)

    return analyzer.build_impact_report()


if __name__ == "__main__":
    # Quick test with synthetic data
    from .parser import QueryParser

    test_data = [
        # Clean query
        ("SELECT a, b FROM t1 JOIN t2 ON t1.id = t2.id", 5.0),
        # SELECT *
        ("SELECT * FROM t1", 15.0),
        ("SELECT * FROM t1 JOIN t2 ON t1.id = t2.id", 20.0),
        # OR in JOIN
        ("SELECT a FROM t1 JOIN t2 ON t1.id = t2.id OR t1.name = t2.name", 45.0),
        # CROSS JOIN
        ("SELECT a FROM t1 CROSS JOIN t2", 120.0),
        # Combination
        ("SELECT * FROM t1 CROSS JOIN t2", 180.0),
        # NOT IN
        ("SELECT a FROM t1 WHERE id NOT IN (SELECT id FROM t2)", 60.0),
    ]

    parser = QueryParser()
    analyzer = AntiPatternAnalyzer()

    for sql, exec_time in test_data:
        parsed = parser.parse(sql)
        analyzer.add_query(parsed, exec_time)

    print(analyzer.summary())
