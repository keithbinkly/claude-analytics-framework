"""
Semantic Inferrer Module

Infers semantic model elements (dimensions, measures, entities) from query patterns.
Uses GROUP BY for dimensions, aggregations for measures, JOIN keys for entities.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional
import yaml
import logging
import re
from datetime import datetime

from .parser import ParsedQuery, AggregationInfo, JoinInfo

logger = logging.getLogger(__name__)


@dataclass
class DimensionCandidate:
    """A candidate dimension inferred from GROUP BY usage."""
    name: str
    table: Optional[str]
    frequency: int = 0
    dimension_type: str = "categorical"  # categorical, time
    sample_values: list = field(default_factory=list)
    granularities_used: list = field(default_factory=list)  # For time dims

    def to_dict(self) -> dict:
        result = {
            "name": self.name,
            "frequency": self.frequency,
            "type": self.dimension_type,
        }
        if self.sample_values:
            result["sample_values"] = self.sample_values[:5]
        if self.granularities_used:
            result["granularities_used"] = list(set(self.granularities_used))
        return result


@dataclass
class MeasureCandidate:
    """A candidate measure inferred from aggregation usage."""
    name: str
    table: Optional[str]
    aggregations: dict = field(default_factory=lambda: defaultdict(int))

    @property
    def total_frequency(self) -> int:
        return sum(self.aggregations.values())

    @property
    def primary_aggregation(self) -> str:
        """Most common aggregation type for this measure."""
        if not self.aggregations:
            return "sum"
        return max(self.aggregations.items(), key=lambda x: x[1])[0].lower()

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "aggregations": dict(self.aggregations),
            "agg_recommendation": self.primary_aggregation,
            "total_frequency": self.total_frequency,
        }


@dataclass
class EntityCandidate:
    """A candidate entity inferred from JOIN key usage."""
    name: str
    table: str
    entity_type: str = "foreign"  # primary, foreign
    frequency: int = 0
    joins_to: list = field(default_factory=list)  # Other tables this joins to
    cardinality_hint: Optional[str] = None  # HIGH, MEDIUM, LOW

    def to_dict(self) -> dict:
        result = {
            "name": self.name,
            "type": self.entity_type,
            "frequency": self.frequency,
        }
        if self.joins_to:
            result["joins_to"] = list(set(self.joins_to))[:5]
        if self.cardinality_hint:
            result["cardinality_hint"] = self.cardinality_hint
        return result


@dataclass
class TableSemantics:
    """Semantic elements for a single table."""
    table: str
    dimensions: dict = field(default_factory=dict)  # name -> DimensionCandidate
    measures: dict = field(default_factory=dict)  # name -> MeasureCandidate
    entities: dict = field(default_factory=dict)  # name -> EntityCandidate

    def to_dict(self) -> dict:
        return {
            "dimensions": {
                "categorical": [
                    d.to_dict() for d in self.dimensions.values()
                    if d.dimension_type == "categorical"
                ],
                "time": [
                    d.to_dict() for d in self.dimensions.values()
                    if d.dimension_type == "time"
                ],
            },
            "measures": [m.to_dict() for m in self.measures.values()],
            "entities": [e.to_dict() for e in self.entities.values()],
        }


class SemanticInferrer:
    """
    Infers semantic model elements from query patterns.

    Usage:
        inferrer = SemanticInferrer()
        for parsed_query in parsed_queries:
            inferrer.add_query(parsed_query)
        candidates = inferrer.build_candidates()
        inferrer.save_yaml("semantic-candidates.yml")
    """

    # Patterns for detecting time-related columns
    TIME_COLUMN_PATTERNS = [
        r'.*_date$',
        r'.*_dt$',
        r'.*_dttm$',
        r'.*_time$',
        r'.*_timestamp$',
        r'^date_.*',
        r'^time_.*',
        r'^created_.*',
        r'^updated_.*',
        r'^posted_.*',
        r'^transaction_date',
        r'^metric_time',
    ]

    def __init__(self):
        self._tables: dict[str, TableSemantics] = {}
        self._query_count = 0
        self._time_patterns = [
            re.compile(p, re.IGNORECASE) for p in self.TIME_COLUMN_PATTERNS
        ]

    def add_query(self, parsed: ParsedQuery) -> None:
        """
        Add semantic elements from a parsed query.

        Args:
            parsed: ParsedQuery object
        """
        self._query_count += 1

        # Extract dimensions from GROUP BY
        self._extract_dimensions(parsed)

        # Extract measures from aggregations
        self._extract_measures(parsed)

        # Extract entities from JOIN keys
        self._extract_entities(parsed)

    def _get_or_create_table(self, table: str) -> TableSemantics:
        """Get or create TableSemantics for a table."""
        table_lower = table.lower()
        if table_lower not in self._tables:
            self._tables[table_lower] = TableSemantics(table=table_lower)
        return self._tables[table_lower]

    def _is_time_column(self, column: str) -> bool:
        """Check if column name suggests a time dimension."""
        for pattern in self._time_patterns:
            if pattern.match(column):
                return True
        return False

    def _extract_dimensions(self, parsed: ParsedQuery) -> None:
        """Extract dimension candidates from GROUP BY columns."""
        for col in parsed.group_by_columns:
            # Skip positional references (GROUP BY 1, 2, 3)
            if col.startswith("position_"):
                continue

            # Parse table.column format
            table, column = self._parse_column_ref(col)

            if not table:
                # Try to infer table from query context
                table = self._infer_table(column, parsed.tables)

            if table:
                table_semantics = self._get_or_create_table(table)

                if column not in table_semantics.dimensions:
                    dim_type = "time" if self._is_time_column(column) else "categorical"
                    table_semantics.dimensions[column] = DimensionCandidate(
                        name=column,
                        table=table,
                        dimension_type=dim_type
                    )

                table_semantics.dimensions[column].frequency += 1

    def _extract_measures(self, parsed: ParsedQuery) -> None:
        """Extract measure candidates from aggregations."""
        for agg in parsed.aggregations:
            # Skip COUNT(*) - not a true measure
            if agg.column == "*":
                continue

            # Parse table.column format
            table, column = self._parse_column_ref(agg.column)

            if not table:
                table = self._infer_table(column, parsed.tables)

            if table:
                table_semantics = self._get_or_create_table(table)

                if column not in table_semantics.measures:
                    table_semantics.measures[column] = MeasureCandidate(
                        name=column,
                        table=table
                    )

                table_semantics.measures[column].aggregations[agg.function] += 1

    def _extract_entities(self, parsed: ParsedQuery) -> None:
        """Extract entity candidates from JOIN keys."""
        for join in parsed.joins:
            # Source side entity
            source_table = self._get_or_create_table(join.source_table)
            source_col = join.source_column

            if source_col not in source_table.entities:
                source_table.entities[source_col] = EntityCandidate(
                    name=source_col,
                    table=join.source_table,
                    entity_type="foreign"
                )

            source_entity = source_table.entities[source_col]
            source_entity.frequency += 1
            source_entity.joins_to.append(join.target_table)

            # Target side entity (often primary key)
            target_table = self._get_or_create_table(join.target_table)
            target_col = join.target_column

            if target_col not in target_table.entities:
                target_table.entities[target_col] = EntityCandidate(
                    name=target_col,
                    table=join.target_table,
                    entity_type="primary"  # Assume target is primary
                )

            target_entity = target_table.entities[target_col]
            target_entity.frequency += 1

    def _parse_column_ref(self, col_ref: str) -> tuple[Optional[str], str]:
        """Parse 'table.column' or 'column' format."""
        parts = col_ref.split('.')
        if len(parts) >= 2:
            # Could be schema.table.column or table.column
            return parts[-2], parts[-1]
        return None, parts[-1]

    def _infer_table(self, column: str, tables: list[str]) -> Optional[str]:
        """Try to infer which table a column belongs to."""
        # Simple heuristic: if only one table, use it
        if len(tables) == 1:
            return tables[0]

        # Could be enhanced with schema knowledge
        return None

    def _infer_cardinality(self, entity: EntityCandidate) -> str:
        """Infer cardinality hint based on frequency and join patterns."""
        # High frequency + many unique join targets = likely primary key
        if entity.frequency > 100 and len(set(entity.joins_to)) > 5:
            return "HIGH"
        elif entity.frequency > 20:
            return "MEDIUM"
        return "LOW"

    def build_candidates(self) -> dict:
        """
        Build the complete semantic candidates registry.

        Returns:
            Dictionary with tables and their semantic elements
        """
        # Enrich with cardinality hints
        for table_semantics in self._tables.values():
            for entity in table_semantics.entities.values():
                entity.cardinality_hint = self._infer_cardinality(entity)

        # Sort tables by total frequency
        sorted_tables = sorted(
            self._tables.items(),
            key=lambda x: sum(
                d.frequency for d in x[1].dimensions.values()
            ) + sum(
                m.total_frequency for m in x[1].measures.values()
            ),
            reverse=True
        )

        return {
            "metadata": {
                "generated": datetime.now().isoformat(),
                "source": "Redshift query logs",
                "query_count": self._query_count,
                "tables_analyzed": len(self._tables),
            },
            "tables": {
                table: semantics.to_dict()
                for table, semantics in sorted_tables[:50]  # Top 50 tables
            },
        }

    def save_yaml(self, filepath: str) -> None:
        """
        Save candidates to YAML file.

        Args:
            filepath: Output file path
        """
        candidates = self.build_candidates()

        with open(filepath, 'w') as f:
            yaml.dump(candidates, f, default_flow_style=False, sort_keys=False)

        logger.info(f"Saved semantic candidates to {filepath}")
        logger.info(f"  Tables analyzed: {candidates['metadata']['tables_analyzed']}")

    def get_measures_for_table(self, table: str) -> list[MeasureCandidate]:
        """Get all measure candidates for a specific table."""
        table_lower = table.lower()
        if table_lower in self._tables:
            return list(self._tables[table_lower].measures.values())
        return []

    def get_dimensions_for_table(self, table: str) -> list[DimensionCandidate]:
        """Get all dimension candidates for a specific table."""
        table_lower = table.lower()
        if table_lower in self._tables:
            return list(self._tables[table_lower].dimensions.values())
        return []

    def summary(self) -> str:
        """Generate summary statistics."""
        total_dims = sum(len(t.dimensions) for t in self._tables.values())
        total_measures = sum(len(t.measures) for t in self._tables.values())
        total_entities = sum(len(t.entities) for t in self._tables.values())

        # Top tables by element count
        top_tables = sorted(
            self._tables.items(),
            key=lambda x: len(x[1].dimensions) + len(x[1].measures),
            reverse=True
        )[:10]

        lines = [
            "Semantic Candidates Summary",
            "=" * 40,
            f"Tables analyzed: {len(self._tables)}",
            f"Total dimensions: {total_dims}",
            f"Total measures: {total_measures}",
            f"Total entities: {total_entities}",
            f"Queries analyzed: {self._query_count}",
            "",
            "Top 10 Tables by Semantic Richness:",
        ]

        for table, semantics in top_tables:
            dims = len(semantics.dimensions)
            meas = len(semantics.measures)
            ents = len(semantics.entities)
            lines.append(f"  {table}: {dims}D / {meas}M / {ents}E")

        return "\n".join(lines)


def infer_semantics_from_queries(
    parsed_queries: list[ParsedQuery],
    output_path: Optional[str] = None
) -> dict:
    """
    Convenience function to infer semantics from a list of parsed queries.

    Args:
        parsed_queries: List of ParsedQuery objects
        output_path: Optional path to save YAML output

    Returns:
        Semantic candidates dictionary
    """
    inferrer = SemanticInferrer()

    for parsed in parsed_queries:
        inferrer.add_query(parsed)

    if output_path:
        inferrer.save_yaml(output_path)

    return inferrer.build_candidates()


if __name__ == "__main__":
    # Quick test
    from .parser import QueryParser

    test_queries = [
        """
        SELECT
            da.acct_uid,
            dd.calendar_date,
            dp.product_name,
            SUM(pt.transactionamount) AS total_revenue,
            COUNT(pt.txn_id) AS txn_count,
            AVG(pt.transactionamount) AS avg_amount
        FROM edw.fct_posted_transaction pt
        JOIN edw.dim_account da ON pt.acct_uid = da.acct_uid
        JOIN edw.dim_date dd ON pt.posted_dt_key = dd.date_key
        JOIN edw.dim_product dp ON da.product_uid = dp.product_uid
        GROUP BY da.acct_uid, dd.calendar_date, dp.product_name
        """,
        """
        SELECT
            da.sor_uid,
            SUM(pt.transactionamount) AS revenue
        FROM edw.fct_posted_transaction pt
        JOIN edw.dim_account da ON pt.acct_uid = da.acct_uid
        WHERE da.sor_uid = 24
        GROUP BY da.sor_uid
        """,
    ]

    parser = QueryParser()
    inferrer = SemanticInferrer()

    for sql in test_queries:
        parsed = parser.parse(sql)
        inferrer.add_query(parsed)

    print(inferrer.summary())

    print("\nMeasures for edw.fct_posted_transaction:")
    for measure in inferrer.get_measures_for_table("edw.fct_posted_transaction"):
        print(f"  {measure.name}: {dict(measure.aggregations)}")

    print("\nDimensions for edw.dim_account:")
    for dim in inferrer.get_dimensions_for_table("edw.dim_account"):
        print(f"  {dim.name}: {dim.dimension_type} ({dim.frequency}x)")
