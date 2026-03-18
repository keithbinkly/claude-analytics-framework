"""
Join Extractor Module

Extracts join relationships from parsed queries and builds a normalized registry.
Outputs dual-indexed YAML for fast bidirectional lookup.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional
import yaml
import logging
from datetime import datetime

from .parser import ParsedQuery, JoinInfo

logger = logging.getLogger(__name__)


@dataclass
class JoinStats:
    """Statistics for a single join relationship."""
    source_table: str
    source_column: str
    target_table: str
    target_column: str

    # Frequency metrics
    frequency: int = 0
    join_types: dict = field(default_factory=lambda: defaultdict(int))

    # Performance metrics (populated if execution times provided)
    avg_execution_sec: Optional[float] = None
    median_execution_sec: Optional[float] = None
    p95_execution_sec: Optional[float] = None

    # Quality flags
    canonical: bool = False  # Appears in production dbt models
    orphan_risk: bool = False  # LEFT JOIN to smaller table

    def to_dict(self) -> dict:
        """Convert to dictionary for YAML output."""
        result = {
            "target": self.target_table,
            "key": f"{self.source_column} = {self.target_column}",
            "frequency": self.frequency,
            "join_types": dict(self.join_types),
        }

        if self.avg_execution_sec is not None:
            result["avg_execution_sec"] = round(self.avg_execution_sec, 2)
        if self.canonical:
            result["canonical"] = True
        if self.orphan_risk:
            result["orphan_risk"] = True

        return result


@dataclass
class JoinEdge:
    """Flat edge representation for graph algorithms."""
    source: str
    target: str
    weight: int
    key: str


class JoinExtractor:
    """
    Extracts join relationships and builds normalized registry.

    Usage:
        extractor = JoinExtractor()
        for parsed_query in parsed_queries:
            extractor.add_query(parsed_query)
        registry = extractor.build_registry()
        extractor.save_yaml("join-registry.yml")
    """

    def __init__(self):
        self._joins: dict[tuple, JoinStats] = {}
        self._execution_times: dict[tuple, list] = defaultdict(list)
        self._query_count = 0

    def add_query(
        self,
        parsed: ParsedQuery,
        execution_time: Optional[float] = None
    ) -> None:
        """
        Add joins from a parsed query to the registry.

        Args:
            parsed: ParsedQuery object
            execution_time: Query execution time in seconds (optional)
        """
        self._query_count += 1

        for join in parsed.joins:
            key = self._make_key(join)

            if key not in self._joins:
                self._joins[key] = JoinStats(
                    source_table=join.source_table,
                    source_column=join.source_column,
                    target_table=join.target_table,
                    target_column=join.target_column
                )

            stats = self._joins[key]
            stats.frequency += 1
            stats.join_types[join.join_type] += 1

            # Track LEFT JOIN orphan risk
            if join.join_type in ("LEFT", "LEFT OUTER"):
                stats.orphan_risk = True

            # Track execution time
            if execution_time is not None:
                self._execution_times[key].append(execution_time)

    def _make_key(self, join: JoinInfo) -> tuple:
        """Create unique key for a join relationship."""
        # Normalize direction (always source < target alphabetically for dedup)
        tables = sorted([
            (join.source_table, join.source_column),
            (join.target_table, join.target_column)
        ])
        return (
            tables[0][0], tables[0][1],
            tables[1][0], tables[1][1]
        )

    def compute_stats(self) -> None:
        """Compute execution time statistics for all joins."""
        import statistics

        for key, times in self._execution_times.items():
            if key in self._joins and times:
                stats = self._joins[key]
                stats.avg_execution_sec = statistics.mean(times)
                stats.median_execution_sec = statistics.median(times)
                if len(times) >= 20:
                    sorted_times = sorted(times)
                    p95_idx = int(len(sorted_times) * 0.95)
                    stats.p95_execution_sec = sorted_times[p95_idx]

    def mark_canonical(self, canonical_joins: list[tuple]) -> None:
        """
        Mark joins that appear in production dbt models.

        Args:
            canonical_joins: List of (source_table, target_table) tuples
        """
        canonical_set = set(canonical_joins)

        for key, stats in self._joins.items():
            source_table = stats.source_table
            target_table = stats.target_table

            if (source_table, target_table) in canonical_set:
                stats.canonical = True
            elif (target_table, source_table) in canonical_set:
                stats.canonical = True

    def build_registry(self) -> dict:
        """
        Build the complete join registry.

        Returns:
            Dictionary with joins_by_source, joins_by_target, and edges
        """
        self.compute_stats()

        # Build indexes
        by_source = defaultdict(list)
        by_target = defaultdict(list)
        edges = []

        for key, stats in self._joins.items():
            # Index by source
            by_source[stats.source_table].append(stats.to_dict())

            # Index by target (reverse lookup)
            reverse_entry = {
                "source": stats.source_table,
                "key": f"{stats.source_column} = {stats.target_column}",
                "frequency": stats.frequency,
            }
            by_target[stats.target_table].append(reverse_entry)

            # Flat edge for graph
            edges.append({
                "source": stats.source_table,
                "target": stats.target_table,
                "weight": stats.frequency,
                "key": stats.source_column,
            })

        # Sort by frequency within each index
        for table in by_source:
            by_source[table].sort(key=lambda x: x["frequency"], reverse=True)
        for table in by_target:
            by_target[table].sort(key=lambda x: x["frequency"], reverse=True)

        # Sort edges by weight
        edges.sort(key=lambda x: x["weight"], reverse=True)

        return {
            "metadata": {
                "generated": datetime.now().isoformat(),
                "source": "Redshift query logs",
                "query_count": self._query_count,
                "unique_joins": len(self._joins),
            },
            "joins_by_source": dict(by_source),
            "joins_by_target": dict(by_target),
            "edges": edges,
        }

    def save_yaml(self, filepath: str) -> None:
        """
        Save registry to YAML file.

        Args:
            filepath: Output file path
        """
        registry = self.build_registry()

        with open(filepath, 'w') as f:
            yaml.dump(registry, f, default_flow_style=False, sort_keys=False)

        logger.info(f"Saved join registry to {filepath}")
        logger.info(f"  Unique joins: {registry['metadata']['unique_joins']}")
        logger.info(f"  Query count: {registry['metadata']['query_count']}")

    def get_top_joins(self, n: int = 20) -> list[JoinStats]:
        """
        Get top N joins by frequency.

        Args:
            n: Number of joins to return

        Returns:
            List of JoinStats sorted by frequency
        """
        sorted_joins = sorted(
            self._joins.values(),
            key=lambda x: x.frequency,
            reverse=True
        )
        return sorted_joins[:n]

    def get_joins_for_table(self, table: str) -> list[JoinStats]:
        """
        Get all joins involving a specific table.

        Args:
            table: Table name (schema.table or just table)

        Returns:
            List of JoinStats for that table
        """
        table_lower = table.lower()
        return [
            stats for stats in self._joins.values()
            if stats.source_table == table_lower or stats.target_table == table_lower
        ]

    def summary(self) -> str:
        """Generate summary statistics."""
        total_joins = len(self._joins)
        total_frequency = sum(s.frequency for s in self._joins.values())
        canonical_count = sum(1 for s in self._joins.values() if s.canonical)
        orphan_risk_count = sum(1 for s in self._joins.values() if s.orphan_risk)

        # Top tables by join involvement
        table_frequency = defaultdict(int)
        for stats in self._joins.values():
            table_frequency[stats.source_table] += stats.frequency
            table_frequency[stats.target_table] += stats.frequency

        top_tables = sorted(
            table_frequency.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        lines = [
            "Join Registry Summary",
            "=" * 40,
            f"Unique joins: {total_joins}",
            f"Total occurrences: {total_frequency}",
            f"Canonical joins: {canonical_count}",
            f"Orphan risk joins: {orphan_risk_count}",
            "",
            "Top 10 Tables by Join Frequency:",
        ]

        for table, freq in top_tables:
            lines.append(f"  {table}: {freq}")

        return "\n".join(lines)


def extract_joins_from_queries(
    parsed_queries: list[ParsedQuery],
    execution_times: Optional[list[float]] = None,
    output_path: Optional[str] = None
) -> dict:
    """
    Convenience function to extract joins from a list of parsed queries.

    Args:
        parsed_queries: List of ParsedQuery objects
        execution_times: Optional list of execution times (parallel to queries)
        output_path: Optional path to save YAML output

    Returns:
        Join registry dictionary
    """
    extractor = JoinExtractor()

    for i, parsed in enumerate(parsed_queries):
        exec_time = execution_times[i] if execution_times else None
        extractor.add_query(parsed, exec_time)

    if output_path:
        extractor.save_yaml(output_path)

    return extractor.build_registry()


if __name__ == "__main__":
    # Quick test
    from .parser import QueryParser

    test_queries = [
        """
        SELECT da.acct_uid, SUM(pt.amount) AS total
        FROM edw.fct_posted_transaction pt
        JOIN edw.dim_account da ON pt.acct_uid = da.acct_uid
        GROUP BY da.acct_uid
        """,
        """
        SELECT da.acct_uid, dp.product_name
        FROM edw.dim_account da
        LEFT JOIN edw.dim_product dp ON da.product_uid = dp.product_uid
        """,
        """
        SELECT da.acct_uid, SUM(pt.amount)
        FROM edw.fct_posted_transaction pt
        JOIN edw.dim_account da ON pt.acct_uid = da.acct_uid
        GROUP BY da.acct_uid
        """,  # Duplicate to test frequency
    ]

    parser = QueryParser()
    extractor = JoinExtractor()

    for sql in test_queries:
        parsed = parser.parse(sql)
        extractor.add_query(parsed, execution_time=10.5)

    print(extractor.summary())
    print("\nTop joins:")
    for join in extractor.get_top_joins(5):
        print(f"  {join.source_table} -> {join.target_table}: {join.frequency}")
