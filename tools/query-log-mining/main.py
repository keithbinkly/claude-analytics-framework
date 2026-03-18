#!/usr/bin/env python3
"""
Query Log Mining - Main Orchestration Script

Coordinates the extraction of structured knowledge from Redshift query logs.

Usage:
    python -m tools.query_log_mining.main <command> [options]

Commands:
    parse           Parse all queries and cache results
    extract-joins   Build join registry from parsed queries
    mine-aliases    Extract column aliases for vocabulary
    infer-semantic  Infer dimensions, measures, entities
    analyze-impact  Correlate anti-patterns with execution time
    run-all         Run complete pipeline

Examples:
    # Run complete pipeline
    python -m tools.query_log_mining.main run-all \\
        --input query_logs.xlsx \\
        --output-dir shared/reference/

    # Parse and cache (run once, reuse cache)
    python -m tools.query_log_mining.main parse \\
        --input query_logs.xlsx \\
        --output cache/parsed_queries.parquet

    # Extract joins from cached data
    python -m tools.query_log_mining.main extract-joins \\
        --input cache/parsed_queries.parquet \\
        --output shared/reference/join-registry.yml
"""

import argparse
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# Check for required dependencies
MISSING_DEPS = []

try:
    import polars as pl
except ImportError:
    MISSING_DEPS.append("polars")

try:
    import sqlglot
except ImportError:
    MISSING_DEPS.append("sqlglot")

try:
    import yaml
except ImportError:
    MISSING_DEPS.append("pyyaml")

if MISSING_DEPS:
    print(f"Missing dependencies: {', '.join(MISSING_DEPS)}")
    print("Install with: pip install " + " ".join(MISSING_DEPS))
    sys.exit(1)

from .parser import QueryParser, ParsedQuery, filter_by_schemas
from .join_extractor import JoinExtractor
from .alias_miner import AliasMiner
from .semantic_inferrer import SemanticInferrer
from .anti_pattern_analyzer import AntiPatternAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_queries_from_file(filepath: str) -> pl.DataFrame:
    """
    Load queries from Excel or JSON file.

    Expects columns like 'querytxt' or 'query_text' for SQL,
    and optionally 'total_exec_time' or 'execution_time' for timing.

    Args:
        filepath: Path to input file

    Returns:
        Polars DataFrame with normalized column names
    """
    logger.info(f"Loading queries from {filepath}")

    # Read file based on extension
    if filepath.endswith('.json'):
        df = pl.read_json(filepath)
    else:
        # Default to Excel
        df = pl.read_excel(filepath)

    logger.info(f"Loaded {len(df)} rows with columns: {df.columns}")

    # Normalize column names
    column_mapping = {}

    # Find query text column (prefer full_query_text over ambiguous 'query')
    # Priority order: full_query_text > querytxt > query_text > sql > query
    query_cols_priority = ['full_query_text', 'querytxt', 'query_text', 'querytext', 'sql_text', 'sql', 'query']
    df_cols_lower = {col.lower(): col for col in df.columns}
    for preferred in query_cols_priority:
        if preferred in df_cols_lower:
            column_mapping[df_cols_lower[preferred]] = 'query_text'
            break

    # Find execution time column
    time_cols_priority = ['executiontime_sec', 'total_exec_time', 'execution_time', 'exec_time', 'runtime', 'elapsed']
    for preferred in time_cols_priority:
        if preferred in df_cols_lower:
            column_mapping[df_cols_lower[preferred]] = 'execution_time'
            break

    if column_mapping:
        df = df.rename(column_mapping)

    if 'query_text' not in df.columns:
        raise ValueError(
            f"Could not find query text column. Available: {df.columns}"
        )

    # Filter out null/empty queries
    df = df.filter(pl.col('query_text').is_not_null())
    df = df.filter(pl.col('query_text').str.len_chars() > 10)

    logger.info(f"After filtering: {len(df)} valid queries")

    return df


def load_queries_from_parquet(filepath: str) -> pl.DataFrame:
    """Load queries from Parquet cache file."""
    logger.info(f"Loading cached queries from {filepath}")
    return pl.read_parquet(filepath)


def save_queries_to_parquet(df: pl.DataFrame, filepath: str) -> None:
    """Save queries to Parquet cache file."""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(filepath)
    logger.info(f"Saved {len(df)} queries to {filepath}")


def parse_queries(df: pl.DataFrame, limit: Optional[int] = None) -> list[tuple]:
    """
    Parse all queries and return list of (ParsedQuery, execution_time) tuples.

    Args:
        df: DataFrame with 'query_text' and optionally 'execution_time'
        limit: Optional limit on number of queries to parse

    Returns:
        List of (ParsedQuery, Optional[float]) tuples
    """
    parser = QueryParser()
    results = []

    queries = df['query_text'].to_list()
    exec_times = df['execution_time'].to_list() if 'execution_time' in df.columns else [None] * len(queries)

    if limit:
        queries = queries[:limit]
        exec_times = exec_times[:limit]

    total = len(queries)
    logger.info(f"Parsing {total} queries...")

    for i, (sql, exec_time) in enumerate(zip(queries, exec_times)):
        if i % 10000 == 0:
            logger.info(f"Progress: {i}/{total} ({100*i/total:.1f}%)")

        try:
            parsed = parser.parse(sql)
            results.append((parsed, exec_time))
        except Exception as e:
            logger.warning(f"Failed to parse query {i}: {e}")
            # Still track the failure
            failed = ParsedQuery(
                original_sql=sql[:500],
                is_valid=False,
                error_message=str(e)
            )
            results.append((failed, exec_time))

    valid_count = sum(1 for p, _ in results if p.is_valid)
    logger.info(f"Parsed {total} queries: {valid_count} valid, {total - valid_count} failed")

    return results


def cmd_parse(args) -> None:
    """Parse command: Parse queries and cache results."""
    df = load_queries_from_file(args.input)

    # Parse queries
    results = parse_queries(df, limit=args.limit)

    # Serialize to parquet-compatible format
    records = []
    for parsed, exec_time in results:
        records.append({
            'query_text': parsed.original_sql[:10000],  # Truncate long queries
            'is_valid': parsed.is_valid,
            'error_message': parsed.error_message,
            'tables': ','.join(parsed.tables),
            'has_select_star': parsed.has_select_star,
            'has_distinct_in_agg': parsed.has_distinct_in_agg,
            'has_or_in_join': parsed.has_or_in_join,
            'has_cross_join': parsed.has_cross_join,
            'has_not_in_subquery': parsed.has_not_in_subquery,
            'subquery_depth': parsed.subquery_depth,
            'execution_time': exec_time,
            # Store joins as JSON string
            'joins_json': str([
                {
                    'source_table': j.source_table,
                    'source_column': j.source_column,
                    'target_table': j.target_table,
                    'target_column': j.target_column,
                    'join_type': j.join_type
                }
                for j in parsed.joins
            ]),
            'aggregations_json': str([
                {
                    'function': a.function,
                    'column': a.column,
                    'alias': a.alias,
                    'is_distinct': a.is_distinct
                }
                for a in parsed.aggregations
            ]),
            'aliases_json': str([
                {
                    'source_table': a.source_table,
                    'source_column': a.source_column,
                    'alias': a.alias
                }
                for a in parsed.aliases
            ]),
            'group_by': ','.join(parsed.group_by_columns),
        })

    result_df = pl.DataFrame(records)
    save_queries_to_parquet(result_df, args.output)

    print(f"\n✅ Parsed {len(results)} queries")
    print(f"   Valid: {sum(1 for p, _ in results if p.is_valid)}")
    print(f"   Saved to: {args.output}")


def cmd_extract_joins(args) -> None:
    """Extract joins command: Build join registry."""
    # Load parsed queries
    if args.input.endswith('.parquet'):
        df = load_queries_from_parquet(args.input)
    else:
        df = load_queries_from_file(args.input)
        results = parse_queries(df, limit=args.limit)

        # Build from fresh parse
        extractor = JoinExtractor()
        for parsed, exec_time in results:
            extractor.add_query(parsed, exec_time)

        extractor.save_yaml(args.output)
        print(f"\n✅ Extracted joins to {args.output}")
        print(extractor.summary())
        return

    # Build from cached parquet
    import ast

    extractor = JoinExtractor()

    for row in df.iter_rows(named=True):
        # Reconstruct ParsedQuery from cached data
        joins_data = ast.literal_eval(row.get('joins_json', '[]'))

        from .parser import JoinInfo
        joins = [
            JoinInfo(
                source_table=j['source_table'],
                source_column=j['source_column'],
                target_table=j['target_table'],
                target_column=j['target_column'],
                join_type=j['join_type'],
                condition_text=""
            )
            for j in joins_data
        ]

        parsed = ParsedQuery(
            original_sql="",
            is_valid=row.get('is_valid', False),
            joins=joins
        )

        extractor.add_query(parsed, row.get('execution_time'))

    extractor.save_yaml(args.output)
    print(f"\n✅ Extracted joins to {args.output}")
    print(extractor.summary())


def cmd_mine_aliases(args) -> None:
    """Mine aliases command: Build controlled vocabulary."""
    if args.input.endswith('.parquet'):
        df = load_queries_from_parquet(args.input)
    else:
        df = load_queries_from_file(args.input)
        results = parse_queries(df, limit=args.limit)

        miner = AliasMiner()
        for parsed, _ in results:
            miner.add_query(parsed)

        miner.save_yaml(args.output)
        print(f"\n✅ Mined aliases to {args.output}")
        print(miner.summary())
        return

    # Build from cached parquet
    import ast

    miner = AliasMiner()

    for row in df.iter_rows(named=True):
        aliases_data = ast.literal_eval(row.get('aliases_json', '[]'))

        from .parser import AliasInfo
        aliases = [
            AliasInfo(
                source_table=a.get('source_table'),
                source_column=a['source_column'],
                alias=a['alias']
            )
            for a in aliases_data
        ]

        parsed = ParsedQuery(
            original_sql="",
            is_valid=row.get('is_valid', False),
            aliases=aliases
        )

        miner.add_query(parsed)

    miner.save_yaml(args.output)
    print(f"\n✅ Mined aliases to {args.output}")
    print(miner.summary())


def cmd_infer_semantic(args) -> None:
    """Infer semantic elements command."""
    if args.input.endswith('.parquet'):
        df = load_queries_from_parquet(args.input)
    else:
        df = load_queries_from_file(args.input)
        results = parse_queries(df, limit=args.limit)

        inferrer = SemanticInferrer()
        for parsed, _ in results:
            inferrer.add_query(parsed)

        inferrer.save_yaml(args.output)
        print(f"\n✅ Inferred semantic elements to {args.output}")
        print(inferrer.summary())
        return

    # Build from cached parquet - need full re-parse for semantic inference
    logger.warning("Semantic inference from parquet cache not fully implemented")
    logger.warning("Run with Excel input for complete inference")


def cmd_analyze_impact(args) -> None:
    """Analyze anti-pattern impact command."""
    if args.input.endswith('.parquet'):
        df = load_queries_from_parquet(args.input)
    else:
        df = load_queries_from_file(args.input)
        results = parse_queries(df, limit=args.limit)

        analyzer = AntiPatternAnalyzer()
        for parsed, exec_time in results:
            analyzer.add_query(parsed, exec_time)

        analyzer.save_yaml(args.output)
        print(f"\n✅ Analyzed anti-pattern impact to {args.output}")
        print(analyzer.summary())
        return

    # Build from cached parquet
    analyzer = AntiPatternAnalyzer()

    for row in df.iter_rows(named=True):
        parsed = ParsedQuery(
            original_sql="",
            is_valid=row.get('is_valid', False),
            has_select_star=row.get('has_select_star', False),
            has_distinct_in_agg=row.get('has_distinct_in_agg', False),
            has_or_in_join=row.get('has_or_in_join', False),
            has_cross_join=row.get('has_cross_join', False),
            has_not_in_subquery=row.get('has_not_in_subquery', False),
            subquery_depth=row.get('subquery_depth', 0),
        )

        analyzer.add_query(parsed, row.get('execution_time'))

    analyzer.save_yaml(args.output)
    print(f"\n✅ Analyzed anti-pattern impact to {args.output}")
    print(analyzer.summary())


def cmd_run_all(args) -> None:
    """Run all extraction steps."""
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load and parse
    df = load_queries_from_file(args.input)
    results = parse_queries(df, limit=args.limit)

    # Apply schema filter if specified
    if args.schemas:
        schemas = [s.strip() for s in args.schemas.split(',')]
        exclude_patterns = None
        if hasattr(args, 'exclude') and args.exclude:
            exclude_patterns = [p.strip() for p in args.exclude.split(',')]
            print(f"\n🔍 Filtering to schemas: {schemas}, excluding: {exclude_patterns}")
        else:
            print(f"\n🔍 Filtering to schemas: {schemas}")

        original_count = len(results)

        # Filter parsed queries by schema (and exclude patterns)
        parsed_only = [r[0] for r in results]
        exec_times = [r[1] for r in results]
        filtered_parsed = filter_by_schemas(parsed_only, schemas, exclude_patterns=exclude_patterns)

        # Rebuild results with matching exec times
        filtered_indices = set(id(p) for p in filtered_parsed)
        results = [(p, t) for p, t in zip(parsed_only, exec_times)
                   if id(p) in filtered_indices]

        print(f"   Filtered: {len(results)} of {original_count} queries match")

    # Output file prefix (e.g., "baas-" for baas-join-registry.yml)
    prefix = args.output_prefix if hasattr(args, 'output_prefix') else ''

    # Save cache
    cache_path = output_dir / "cache" / "parsed_queries.parquet"
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    # Extract joins
    print("\n" + "=" * 50)
    print("STEP 1: Extracting joins...")
    extractor = JoinExtractor()
    for parsed, exec_time in results:
        extractor.add_query(parsed, exec_time)
    extractor.save_yaml(str(output_dir / f"{prefix}join-registry.yml"))
    print(extractor.summary())

    # Mine aliases
    print("\n" + "=" * 50)
    print("STEP 2: Mining aliases...")
    miner = AliasMiner()
    for parsed, _ in results:
        miner.add_query(parsed)
    miner.save_yaml(str(output_dir / f"{prefix}controlled-vocabulary.yml"))
    print(miner.summary())

    # Infer semantics
    print("\n" + "=" * 50)
    print("STEP 3: Inferring semantic elements...")
    inferrer = SemanticInferrer()
    for parsed, _ in results:
        inferrer.add_query(parsed)
    inferrer.save_yaml(str(output_dir / f"{prefix}semantic-candidates.yml"))
    print(inferrer.summary())

    # Analyze anti-patterns
    print("\n" + "=" * 50)
    print("STEP 4: Analyzing anti-pattern impact...")
    analyzer = AntiPatternAnalyzer()
    for parsed, exec_time in results:
        analyzer.add_query(parsed, exec_time)
    analyzer.save_yaml(str(output_dir / f"{prefix}anti-pattern-impact.yml"))
    print(analyzer.summary())

    # Final summary
    print("\n" + "=" * 50)
    print("COMPLETE!")
    print(f"\nOutput files in {output_dir}:")
    for f in output_dir.glob("*.yml"):
        print(f"  - {f.name}")


def main():
    parser = argparse.ArgumentParser(
        description="Query Log Mining Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Parse command
    parse_parser = subparsers.add_parser('parse', help='Parse queries and cache')
    parse_parser.add_argument('--input', '-i', required=True, help='Input Excel file')
    parse_parser.add_argument('--output', '-o', required=True, help='Output Parquet file')
    parse_parser.add_argument('--limit', '-n', type=int, help='Limit queries to parse')

    # Extract joins command
    joins_parser = subparsers.add_parser('extract-joins', help='Extract join registry')
    joins_parser.add_argument('--input', '-i', required=True, help='Input file (Excel or Parquet)')
    joins_parser.add_argument('--output', '-o', required=True, help='Output YAML file')
    joins_parser.add_argument('--limit', '-n', type=int, help='Limit queries')

    # Mine aliases command
    alias_parser = subparsers.add_parser('mine-aliases', help='Mine column aliases')
    alias_parser.add_argument('--input', '-i', required=True, help='Input file')
    alias_parser.add_argument('--output', '-o', required=True, help='Output YAML file')
    alias_parser.add_argument('--limit', '-n', type=int, help='Limit queries')

    # Infer semantic command
    semantic_parser = subparsers.add_parser('infer-semantic', help='Infer semantic elements')
    semantic_parser.add_argument('--input', '-i', required=True, help='Input file')
    semantic_parser.add_argument('--output', '-o', required=True, help='Output YAML file')
    semantic_parser.add_argument('--limit', '-n', type=int, help='Limit queries')

    # Analyze impact command
    impact_parser = subparsers.add_parser('analyze-impact', help='Analyze anti-pattern impact')
    impact_parser.add_argument('--input', '-i', required=True, help='Input file')
    impact_parser.add_argument('--output', '-o', required=True, help='Output YAML file')
    impact_parser.add_argument('--limit', '-n', type=int, help='Limit queries')

    # Run all command
    all_parser = subparsers.add_parser('run-all', help='Run complete pipeline')
    all_parser.add_argument('--input', '-i', required=True, help='Input Excel file')
    all_parser.add_argument('--output-dir', '-o', required=True, help='Output directory')
    all_parser.add_argument('--limit', '-n', type=int, help='Limit queries')
    all_parser.add_argument('--schemas', '-s', type=str,
                           help='Filter to schemas (comma-separated, e.g., "edw,gbos,ods")')
    all_parser.add_argument('--exclude', '-x', type=str,
                           help='Exclude table patterns (comma-separated, e.g., "volt_,#")')
    all_parser.add_argument('--output-prefix', type=str, default='',
                           help='Prefix for output files (e.g., "baas-" for baas-join-registry.yml)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Dispatch to command handler
    commands = {
        'parse': cmd_parse,
        'extract-joins': cmd_extract_joins,
        'mine-aliases': cmd_mine_aliases,
        'infer-semantic': cmd_infer_semantic,
        'analyze-impact': cmd_analyze_impact,
        'run-all': cmd_run_all,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
