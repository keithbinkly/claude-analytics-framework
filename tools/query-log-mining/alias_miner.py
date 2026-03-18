"""
Alias Miner Module

Extracts column aliases from parsed queries to build a controlled vocabulary.
Identifies conflicts (same alias for different columns) for resolution.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional
import yaml
import logging
from datetime import datetime

from .parser import ParsedQuery, AliasInfo

logger = logging.getLogger(__name__)


@dataclass
class AliasStats:
    """Statistics for a single alias."""
    alias: str
    frequency: int = 0
    source_columns: dict = field(default_factory=lambda: defaultdict(int))

    def is_conflict(self) -> bool:
        """Check if this alias maps to multiple source columns."""
        return len(self.source_columns) > 1

    def canonical_source(self) -> str:
        """Get the most frequent source column for this alias."""
        if not self.source_columns:
            return "unknown"
        return max(self.source_columns.items(), key=lambda x: x[1])[0]


@dataclass
class CanonicalTerm:
    """A canonical term with all its aliases."""
    canonical: str
    aliases: list[tuple[str, int]]  # (alias, frequency) pairs
    source_columns: list[str]

    def to_dict(self) -> dict:
        """Convert to dictionary for YAML output."""
        return {
            "canonical": self.canonical,
            "aliases": [
                {"name": alias, "frequency": freq}
                for alias, freq in sorted(self.aliases, key=lambda x: -x[1])
            ],
            "source_columns": self.source_columns,
        }


@dataclass
class AliasConflict:
    """A conflict where one alias maps to multiple columns."""
    alias: str
    used_for: list[tuple[str, int]]  # (source_column, frequency) pairs
    resolution: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for YAML output."""
        result = {
            "alias": self.alias,
            "used_for": [
                {"column": col, "frequency": freq}
                for col, freq in sorted(self.used_for, key=lambda x: -x[1])
            ],
        }
        if self.resolution:
            result["resolution"] = self.resolution
        return result


class AliasMiner:
    """
    Mines column aliases to build controlled vocabulary.

    Usage:
        miner = AliasMiner()
        for parsed_query in parsed_queries:
            miner.add_query(parsed_query)
        vocabulary = miner.build_vocabulary()
        miner.save_yaml("controlled-vocabulary.yml")
    """

    def __init__(self):
        self._aliases: dict[str, AliasStats] = {}
        self._column_to_aliases: dict[str, set] = defaultdict(set)
        self._query_count = 0

    def add_query(self, parsed: ParsedQuery) -> None:
        """
        Add aliases from a parsed query.

        Args:
            parsed: ParsedQuery object
        """
        self._query_count += 1

        for alias_info in parsed.aliases:
            alias = alias_info.alias.lower()
            source = self._normalize_source(alias_info)

            # Track alias -> source
            if alias not in self._aliases:
                self._aliases[alias] = AliasStats(alias=alias)

            stats = self._aliases[alias]
            stats.frequency += 1
            stats.source_columns[source] += 1

            # Track source -> aliases (reverse mapping)
            self._column_to_aliases[source].add(alias)

    def _normalize_source(self, alias_info: AliasInfo) -> str:
        """Normalize source column reference."""
        source = alias_info.source_column

        # Add table prefix if available
        if alias_info.source_table:
            source = f"{alias_info.source_table}.{source}"

        return source.lower()

    def find_conflicts(self) -> list[AliasConflict]:
        """
        Find aliases that map to multiple source columns.

        Returns:
            List of AliasConflict objects
        """
        conflicts = []

        for alias, stats in self._aliases.items():
            if stats.is_conflict():
                used_for = list(stats.source_columns.items())

                # Generate resolution suggestion
                resolution = self._suggest_resolution(alias, used_for)

                conflicts.append(AliasConflict(
                    alias=alias,
                    used_for=used_for,
                    resolution=resolution
                ))

        # Sort by frequency (most impactful conflicts first)
        conflicts.sort(key=lambda x: sum(f for _, f in x.used_for), reverse=True)

        return conflicts

    def _suggest_resolution(
        self,
        alias: str,
        used_for: list[tuple[str, int]]
    ) -> str:
        """Suggest a resolution for an alias conflict."""
        # Extract table names from source columns
        suggestions = []

        for source, _ in used_for:
            parts = source.split('.')
            if len(parts) >= 2:
                table = parts[-2]  # Get table name
                column = parts[-1]
                suggestions.append(f"{table}_{column}")
            else:
                suggestions.append(f"{alias}_{len(suggestions) + 1}")

        return f"Disambiguate using prefixes: {', '.join(suggestions)}"

    def build_canonical_terms(self) -> list[CanonicalTerm]:
        """
        Build canonical terms from source columns.

        Groups aliases by their most common source column.

        Returns:
            List of CanonicalTerm objects
        """
        # Group by canonical source
        canonical_groups: dict[str, list[tuple[str, int]]] = defaultdict(list)

        for alias, stats in self._aliases.items():
            if not stats.is_conflict():
                # Single source - add to that source's group
                source = stats.canonical_source()
                canonical_groups[source].append((alias, stats.frequency))

        # Build terms
        terms = []
        for source, aliases in canonical_groups.items():
            # Find the most common alias to use as canonical name
            primary_alias = max(aliases, key=lambda x: x[1])[0]

            terms.append(CanonicalTerm(
                canonical=primary_alias,
                aliases=aliases,
                source_columns=[source]
            ))

        # Sort by total frequency
        terms.sort(
            key=lambda t: sum(f for _, f in t.aliases),
            reverse=True
        )

        return terms

    def build_vocabulary(self) -> dict:
        """
        Build the complete controlled vocabulary.

        Returns:
            Dictionary with canonical_terms and conflicts
        """
        terms = self.build_canonical_terms()
        conflicts = self.find_conflicts()

        return {
            "metadata": {
                "generated": datetime.now().isoformat(),
                "source": "Redshift query logs",
                "query_count": self._query_count,
                "total_aliases": len(self._aliases),
                "conflict_count": len(conflicts),
            },
            "canonical_terms": [t.to_dict() for t in terms[:100]],  # Top 100
            "conflicts": [c.to_dict() for c in conflicts],
        }

    def save_yaml(self, filepath: str) -> None:
        """
        Save vocabulary to YAML file.

        Args:
            filepath: Output file path
        """
        vocabulary = self.build_vocabulary()

        with open(filepath, 'w') as f:
            yaml.dump(vocabulary, f, default_flow_style=False, sort_keys=False)

        logger.info(f"Saved controlled vocabulary to {filepath}")
        logger.info(f"  Total aliases: {vocabulary['metadata']['total_aliases']}")
        logger.info(f"  Conflicts: {vocabulary['metadata']['conflict_count']}")

    def get_aliases_for_column(self, column: str) -> list[tuple[str, int]]:
        """
        Get all aliases used for a specific column.

        Args:
            column: Column name (optionally with table prefix)

        Returns:
            List of (alias, frequency) tuples
        """
        column_lower = column.lower()
        result = []

        for alias, stats in self._aliases.items():
            for source, freq in stats.source_columns.items():
                if source == column_lower or source.endswith(f".{column_lower}"):
                    result.append((alias, freq))

        return sorted(result, key=lambda x: -x[1])

    def get_column_for_alias(self, alias: str) -> Optional[str]:
        """
        Get the most likely column for an alias.

        Args:
            alias: Alias name

        Returns:
            Most frequent source column, or None if alias not found
        """
        alias_lower = alias.lower()
        if alias_lower in self._aliases:
            return self._aliases[alias_lower].canonical_source()
        return None

    def summary(self) -> str:
        """Generate summary statistics."""
        total_aliases = len(self._aliases)
        conflicts = self.find_conflicts()

        # Top aliases by frequency
        top_aliases = sorted(
            self._aliases.values(),
            key=lambda x: x.frequency,
            reverse=True
        )[:10]

        lines = [
            "Controlled Vocabulary Summary",
            "=" * 40,
            f"Total aliases: {total_aliases}",
            f"Conflicts: {len(conflicts)}",
            f"Queries analyzed: {self._query_count}",
            "",
            "Top 10 Aliases by Frequency:",
        ]

        for stats in top_aliases:
            conflict_marker = " [CONFLICT]" if stats.is_conflict() else ""
            lines.append(f"  {stats.alias}: {stats.frequency}{conflict_marker}")

        if conflicts:
            lines.append("")
            lines.append("Top Conflicts:")
            for conflict in conflicts[:5]:
                lines.append(f"  '{conflict.alias}' used for:")
                for col, freq in conflict.used_for[:3]:
                    lines.append(f"    - {col} ({freq}x)")

        return "\n".join(lines)


def mine_aliases_from_queries(
    parsed_queries: list[ParsedQuery],
    output_path: Optional[str] = None
) -> dict:
    """
    Convenience function to mine aliases from a list of parsed queries.

    Args:
        parsed_queries: List of ParsedQuery objects
        output_path: Optional path to save YAML output

    Returns:
        Controlled vocabulary dictionary
    """
    miner = AliasMiner()

    for parsed in parsed_queries:
        miner.add_query(parsed)

    if output_path:
        miner.save_yaml(output_path)

    return miner.build_vocabulary()


if __name__ == "__main__":
    # Quick test
    from .parser import QueryParser

    test_queries = [
        """
        SELECT
            da.acct_uid,
            SUM(pt.transactionamount) AS total_revenue,
            SUM(pt.transactionamount) AS txn_total
        FROM edw.fct_posted_transaction pt
        JOIN edw.dim_account da ON pt.acct_uid = da.acct_uid
        """,
        """
        SELECT
            pt.transactionamount AS amount,
            ft.fee_amount AS amount
        FROM edw.fct_posted_transaction pt
        JOIN edw.fct_fees ft ON pt.txn_id = ft.txn_id
        """,  # Conflict: 'amount' used for two columns
        """
        SELECT
            SUM(pt.transactionamount) AS revenue,
            COUNT(*) AS txn_count
        FROM edw.fct_posted_transaction pt
        """,
    ]

    parser = QueryParser()
    miner = AliasMiner()

    for sql in test_queries:
        parsed = parser.parse(sql)
        miner.add_query(parsed)

    print(miner.summary())
