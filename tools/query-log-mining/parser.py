"""
SQL Parser Module

Parses SQL queries using sqlglot with Redshift dialect.
Extracts structured information for downstream analysis.
"""

import re
from dataclasses import dataclass, field
from typing import Optional
import logging

try:
    import sqlglot
    from sqlglot import exp
    from sqlglot.errors import ParseError
    SQLGLOT_AVAILABLE = True
except ImportError:
    SQLGLOT_AVAILABLE = False
    logging.warning("sqlglot not installed. Run: pip install sqlglot")

logger = logging.getLogger(__name__)


@dataclass
class JoinInfo:
    """Represents a single JOIN relationship."""
    source_table: str
    source_column: str
    target_table: str
    target_column: str
    join_type: str  # INNER, LEFT, RIGHT, CROSS, etc.
    condition_text: str  # Original condition for complex cases


@dataclass
class AggregationInfo:
    """Represents an aggregation operation."""
    function: str  # SUM, COUNT, AVG, etc.
    column: str
    alias: Optional[str] = None
    is_distinct: bool = False


@dataclass
class AliasInfo:
    """Represents a column alias."""
    source_table: Optional[str]
    source_column: str
    alias: str


@dataclass
class ParsedQuery:
    """Complete parsed query information."""
    original_sql: str
    is_valid: bool
    error_message: Optional[str] = None

    # Extracted elements
    tables: list[str] = field(default_factory=list)
    columns: list[str] = field(default_factory=list)
    joins: list[JoinInfo] = field(default_factory=list)
    aggregations: list[AggregationInfo] = field(default_factory=list)
    aliases: list[AliasInfo] = field(default_factory=list)
    group_by_columns: list[str] = field(default_factory=list)
    where_columns: list[str] = field(default_factory=list)

    # Table alias resolution (alias → full schema.table name)
    # Enables filtering by schema (e.g., BaaS: edw, gbos, ods)
    table_alias_map: dict[str, str] = field(default_factory=dict)

    # Anti-pattern flags
    has_select_star: bool = False
    has_distinct_in_agg: bool = False
    has_or_in_join: bool = False
    has_cross_join: bool = False
    has_not_in_subquery: bool = False
    subquery_depth: int = 0

    # Metadata
    query_type: str = "SELECT"  # SELECT, INSERT, UPDATE, DELETE, CREATE, etc.


class QueryParser:
    """
    Parses SQL queries and extracts structured information.

    Usage:
        parser = QueryParser()
        result = parser.parse(sql_text)
        print(result.tables)
        print(result.joins)
    """

    def __init__(self, dialect: str = "redshift"):
        """
        Initialize parser with SQL dialect.

        Args:
            dialect: SQL dialect for parsing (default: redshift)
        """
        if not SQLGLOT_AVAILABLE:
            raise ImportError("sqlglot required. Run: pip install sqlglot")

        self.dialect = dialect
        self._compiled_patterns = self._compile_patterns()

    def _compile_patterns(self) -> dict:
        """Pre-compile regex patterns for performance."""
        return {
            'select_star': re.compile(r'\bSELECT\s+\*', re.IGNORECASE),
            'not_in': re.compile(r'\bNOT\s+IN\s*\(', re.IGNORECASE),
            'cross_join': re.compile(r'\bCROSS\s+JOIN\b', re.IGNORECASE),
            'or_in_join': re.compile(
                r'\bJOIN\b.*?\bON\b.*?\bOR\b',
                re.IGNORECASE | re.DOTALL
            ),
            'table_ref': re.compile(
                r'(?:FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)?)',
                re.IGNORECASE
            ),
        }

    def parse(self, sql: str) -> ParsedQuery:
        """
        Parse a SQL query and extract structured information.

        Args:
            sql: SQL query text

        Returns:
            ParsedQuery with extracted information
        """
        result = ParsedQuery(original_sql=sql, is_valid=False)

        if not sql or not sql.strip():
            result.error_message = "Empty query"
            return result

        # Quick pattern detection (works even if parsing fails)
        self._detect_anti_patterns(sql, result)

        try:
            # Parse with sqlglot
            parsed = sqlglot.parse(sql, dialect=self.dialect)

            if not parsed or not parsed[0]:
                result.error_message = "No statements parsed"
                # Fall back to regex extraction
                self._extract_with_regex(sql, result)
                return result

            ast = parsed[0]
            result.is_valid = True
            result.query_type = type(ast).__name__.upper()

            # Extract elements from AST
            self._extract_tables(ast, result)
            self._extract_columns(ast, result)
            self._extract_joins(ast, result)
            self._extract_aggregations(ast, result)
            self._extract_aliases(ast, result)
            self._extract_group_by(ast, result)
            self._extract_where_columns(ast, result)
            result.subquery_depth = self._count_subquery_depth(ast)

        except ParseError as e:
            result.error_message = str(e)
            # Fall back to regex extraction
            self._extract_with_regex(sql, result)

        except Exception as e:
            result.error_message = f"Unexpected error: {str(e)}"
            logger.warning(f"Parse error for query: {sql[:100]}... Error: {e}")
            self._extract_with_regex(sql, result)

        return result

    def _detect_anti_patterns(self, sql: str, result: ParsedQuery) -> None:
        """Detect anti-patterns using regex (fast, works on any SQL)."""
        patterns = self._compiled_patterns

        result.has_select_star = bool(patterns['select_star'].search(sql))
        result.has_not_in_subquery = bool(patterns['not_in'].search(sql))
        result.has_cross_join = bool(patterns['cross_join'].search(sql))
        result.has_or_in_join = bool(patterns['or_in_join'].search(sql))

        # Count SELECT keywords for nesting depth estimate
        select_count = sql.upper().count('SELECT')
        result.subquery_depth = max(0, select_count - 1)

    def _extract_tables(self, ast: exp.Expression, result: ParsedQuery) -> None:
        """Extract all table references from AST and build alias→table map."""
        tables = set()
        alias_map = {}

        for table in ast.find_all(exp.Table):
            table_name = table.name
            if table.db:
                table_name = f"{table.db}.{table_name}"
            if table.catalog:
                table_name = f"{table.catalog}.{table_name}"

            full_name = table_name.lower()
            tables.add(full_name)

            # Build alias→full_table_name map
            # Handle: FROM schema.table AS alias, FROM schema.table alias
            if table.alias:
                alias_map[table.alias.lower()] = full_name
            else:
                # No alias - table references itself by last component
                base_name = table.name.lower()
                alias_map[base_name] = full_name

        result.tables = sorted(tables)
        result.table_alias_map = alias_map

    def _extract_columns(self, ast: exp.Expression, result: ParsedQuery) -> None:
        """Extract all column references from AST."""
        columns = set()

        for col in ast.find_all(exp.Column):
            col_name = col.name
            if col.table:
                col_name = f"{col.table}.{col_name}"
            columns.add(col_name.lower())

        result.columns = sorted(columns)

    def _extract_joins(self, ast: exp.Expression, result: ParsedQuery) -> None:
        """Extract JOIN relationships from AST with alias resolution."""
        joins = []

        for join in ast.find_all(exp.Join):
            join_type = "INNER"
            if join.side:
                join_type = join.side.upper()
            if join.kind:
                join_type = join.kind.upper()

            # Get target table
            target_table = None
            if isinstance(join.this, exp.Table):
                target_table = join.this.name
                if join.this.db:
                    target_table = f"{join.this.db}.{target_table}"

            # Parse ON condition - pass alias_map for full table name resolution
            if join.args.get("on"):
                on_expr = join.args["on"]
                self._extract_join_conditions(
                    on_expr, target_table, join_type, joins,
                    alias_map=result.table_alias_map
                )

        result.joins = joins

        # Check for OR in join conditions
        for join_info in joins:
            if ' OR ' in join_info.condition_text.upper():
                result.has_or_in_join = True
                break

    def _extract_join_conditions(
        self,
        on_expr: exp.Expression,
        target_table: Optional[str],
        join_type: str,
        joins: list[JoinInfo],
        alias_map: dict[str, str] = None
    ) -> None:
        """Extract individual join conditions from ON expression.

        Args:
            alias_map: Maps table aliases to full schema.table names.
                       Enables filtering by schema (e.g., edw, gbos, ods).
        """
        condition_text = on_expr.sql() if hasattr(on_expr, 'sql') else str(on_expr)
        alias_map = alias_map or {}

        # Find equality conditions (most common)
        for eq in on_expr.find_all(exp.EQ):
            left = eq.left
            right = eq.right

            if isinstance(left, exp.Column) and isinstance(right, exp.Column):
                # Get alias/reference from SQL
                source_alias = (left.table or "unknown").lower()
                target_alias = (right.table or target_table or "unknown").lower()

                # Resolve aliases to full table names
                source_table = alias_map.get(source_alias, source_alias)
                target_table_name = alias_map.get(target_alias, target_alias)

                source_col = left.name
                target_col = right.name

                joins.append(JoinInfo(
                    source_table=source_table.lower(),
                    source_column=source_col.lower(),
                    target_table=target_table_name.lower(),
                    target_column=target_col.lower(),
                    join_type=join_type,
                    condition_text=condition_text
                ))

    def _extract_aggregations(self, ast: exp.Expression, result: ParsedQuery) -> None:
        """Extract aggregation functions from AST."""
        aggs = []
        agg_types = (exp.Sum, exp.Count, exp.Avg, exp.Min, exp.Max)

        for agg in ast.find_all(agg_types):
            func_name = type(agg).__name__.upper()

            # Get the column being aggregated
            col_name = "unknown"
            is_distinct = False

            if agg.this:
                if isinstance(agg.this, exp.Distinct):
                    is_distinct = True
                    result.has_distinct_in_agg = True
                    if agg.this.expressions:
                        inner = agg.this.expressions[0]
                        if isinstance(inner, exp.Column):
                            col_name = inner.name
                            if inner.table:
                                col_name = f"{inner.table}.{col_name}"
                elif isinstance(agg.this, exp.Column):
                    col_name = agg.this.name
                    if agg.this.table:
                        col_name = f"{agg.this.table}.{col_name}"
                elif isinstance(agg.this, exp.Star):
                    col_name = "*"

            # Get alias if present
            alias = None
            parent = agg.parent
            if isinstance(parent, exp.Alias):
                alias = parent.alias

            aggs.append(AggregationInfo(
                function=func_name,
                column=col_name.lower(),
                alias=alias.lower() if alias else None,
                is_distinct=is_distinct
            ))

        result.aggregations = aggs

    def _extract_aliases(self, ast: exp.Expression, result: ParsedQuery) -> None:
        """Extract column aliases from SELECT list."""
        aliases = []

        for alias_expr in ast.find_all(exp.Alias):
            alias_name = alias_expr.alias

            source = alias_expr.this
            source_table = None
            source_column = None

            if isinstance(source, exp.Column):
                source_column = source.name
                source_table = source.table
            elif isinstance(source, (exp.Sum, exp.Count, exp.Avg, exp.Min, exp.Max)):
                # Aggregation with alias
                if source.this and isinstance(source.this, exp.Column):
                    source_column = f"{type(source).__name__}({source.this.name})"
                else:
                    source_column = type(source).__name__
            else:
                # Complex expression
                source_column = source.sql() if hasattr(source, 'sql') else str(source)

            if alias_name and source_column:
                aliases.append(AliasInfo(
                    source_table=source_table.lower() if source_table else None,
                    source_column=source_column.lower() if source_column else "expression",
                    alias=alias_name.lower()
                ))

        result.aliases = aliases

    def _extract_group_by(self, ast: exp.Expression, result: ParsedQuery) -> None:
        """Extract GROUP BY columns."""
        group_by_cols = []

        for group in ast.find_all(exp.Group):
            for expr in group.expressions:
                if isinstance(expr, exp.Column):
                    col_name = expr.name
                    if expr.table:
                        col_name = f"{expr.table}.{col_name}"
                    group_by_cols.append(col_name.lower())
                elif isinstance(expr, exp.Literal):
                    # GROUP BY 1, 2, 3 style
                    group_by_cols.append(f"position_{expr.this}")

        result.group_by_columns = group_by_cols

    def _extract_where_columns(self, ast: exp.Expression, result: ParsedQuery) -> None:
        """Extract columns used in WHERE clause."""
        where_cols = set()

        for where in ast.find_all(exp.Where):
            for col in where.find_all(exp.Column):
                col_name = col.name
                if col.table:
                    col_name = f"{col.table}.{col_name}"
                where_cols.add(col_name.lower())

        result.where_columns = sorted(where_cols)

    def _count_subquery_depth(self, ast: exp.Expression) -> int:
        """Count maximum subquery nesting depth."""
        max_depth = 0

        def count_depth(node: exp.Expression, current_depth: int) -> None:
            nonlocal max_depth

            if isinstance(node, exp.Subquery):
                current_depth += 1
                max_depth = max(max_depth, current_depth)

            for child in node.iter_expressions():
                count_depth(child, current_depth)

        count_depth(ast, 0)
        return max_depth

    def _extract_with_regex(self, sql: str, result: ParsedQuery) -> None:
        """Fallback extraction using regex when parsing fails."""
        # Extract tables
        table_matches = self._compiled_patterns['table_ref'].findall(sql)
        result.tables = list(set(t.lower() for t in table_matches))

        # Mark as partially valid
        result.is_valid = False
        if not result.error_message:
            result.error_message = "Parsed with regex fallback"


def parse_query_batch(queries: list[str], dialect: str = "redshift") -> list[ParsedQuery]:
    """
    Parse a batch of queries.

    Args:
        queries: List of SQL query strings
        dialect: SQL dialect

    Returns:
        List of ParsedQuery results
    """
    parser = QueryParser(dialect=dialect)
    return [parser.parse(q) for q in queries]


def filter_by_schemas(
    parsed_queries: list[ParsedQuery],
    schemas: list[str],
    require_all: bool = False,
    exclude_patterns: list[str] = None
) -> list[ParsedQuery]:
    """
    Filter parsed queries to those using tables from specified schemas.

    Args:
        parsed_queries: List of ParsedQuery results
        schemas: List of schema names to filter by (e.g., ['edw', 'gbos', 'ods'])
        require_all: If True, query must use tables from ALL schemas.
                     If False, query must use tables from ANY schema.
        exclude_patterns: List of table name prefixes to exclude (e.g., ['volt_', '#'])

    Returns:
        Filtered list of ParsedQuery results

    Example:
        # Filter to BaaS-relevant queries, excluding volt temp tables
        baas_queries = filter_by_schemas(
            queries,
            ['edw', 'gbos', 'ods'],
            exclude_patterns=['volt_', 'volt_tt_']
        )
    """
    schemas_lower = [s.lower() for s in schemas]
    exclude_patterns = [p.lower() for p in (exclude_patterns or [])]
    filtered = []

    for pq in parsed_queries:
        # Extract schemas from tables (schema.table format)
        query_schemas = set()
        has_excluded = False

        for table in pq.tables:
            table_lower = table.lower()

            # Check exclusion patterns
            if exclude_patterns:
                for pattern in exclude_patterns:
                    if table_lower.startswith(pattern) or f'.{pattern}' in table_lower:
                        has_excluded = True
                        break

            if '.' in table:
                schema = table.split('.')[0]
                query_schemas.add(schema)

        # Skip if query uses excluded tables
        if has_excluded:
            continue

        if require_all:
            # Must have ALL specified schemas
            if all(s in query_schemas for s in schemas_lower):
                filtered.append(pq)
        else:
            # Must have ANY specified schema
            if any(s in query_schemas for s in schemas_lower):
                filtered.append(pq)

    return filtered


if __name__ == "__main__":
    # Quick test - demonstrates alias resolution
    test_sql = """
    SELECT
        da.acct_uid,
        SUM(pt.transactionamount) AS total_revenue,
        COUNT(DISTINCT pt.txn_id) AS txn_count
    FROM edw.fct_posted_transaction pt
    LEFT JOIN edw.dim_account da ON pt.acct_uid = da.acct_uid
    WHERE da.sor_uid = 24
    GROUP BY da.acct_uid
    """

    parser = QueryParser()
    result = parser.parse(test_sql)

    print(f"Valid: {result.is_valid}")
    print(f"Tables: {result.tables}")
    print(f"Alias Map: {result.table_alias_map}")  # NEW: Shows alias→full_table resolution
    print(f"Joins (resolved): {[(j.source_table, j.target_table, j.join_type) for j in result.joins]}")
    print(f"Aggregations: {[(a.function, a.column, a.alias) for a in result.aggregations]}")
    print(f"GROUP BY: {result.group_by_columns}")
    print(f"Anti-patterns: select*={result.has_select_star}, distinct_agg={result.has_distinct_in_agg}")

    # Test schema filtering
    print("\n--- Schema Filtering Test ---")
    queries = [result]
    baas_queries = filter_by_schemas(queries, ['edw', 'gbos', 'ods'])
    print(f"BaaS filter (edw/gbos/ods): {len(baas_queries)} of {len(queries)} queries match")
