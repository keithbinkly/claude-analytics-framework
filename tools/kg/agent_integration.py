#!/usr/bin/env python3
"""
Agent Integration for Knowledge Graph.

This module provides helper functions for agents to leverage the KG
for faster, more accurate information retrieval.

Usage in agent code:
    from tools.kg.agent_integration import enrich_context, smart_search

    # Get relevant context for a user query
    context = enrich_context("How do I implement incremental models?")

    # Smart search that combines KG + concept awareness
    results = smart_search("QA validation template")
"""

import json
import re
import time
from pathlib import Path
from typing import List, Dict, Optional, Callable, Any
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field

from .agent_wrapper import get_kg, KGAgentWrapper, ChunkResult


# ==================== Parallel Execution Infrastructure ====================

@dataclass
class SearchMetrics:
    """Metrics for a single search operation."""
    source: str
    latency_ms: float
    result_count: int
    success: bool
    error: Optional[str] = None


@dataclass
class ParallelSearchResult:
    """Result of parallel search execution with instrumentation."""
    total_latency_ms: float
    sequential_latency_ms: float  # What it would have taken sequentially
    speedup_factor: float
    metrics: List[SearchMetrics] = field(default_factory=list)
    results: Dict[str, Any] = field(default_factory=dict)

    def summary(self) -> str:
        """Human-readable summary of parallel execution."""
        return (
            f"Parallel: {self.total_latency_ms:.0f}ms | "
            f"Sequential: {self.sequential_latency_ms:.0f}ms | "
            f"Speedup: {self.speedup_factor:.1f}x | "
            f"Sources: {len(self.metrics)}"
        )


def _timed_execution(name: str, func: Callable, *args, **kwargs) -> tuple:
    """Execute a function with timing instrumentation."""
    start = time.perf_counter()
    try:
        result = func(*args, **kwargs)
        latency = (time.perf_counter() - start) * 1000  # ms
        return (name, result, latency, None)
    except Exception as e:
        latency = (time.perf_counter() - start) * 1000
        return (name, None, latency, str(e))


def execute_parallel_searches(
    search_funcs: Dict[str, tuple],  # name -> (func, args, kwargs)
    max_workers: int = 8,
    timeout_seconds: float = 30.0
) -> ParallelSearchResult:
    """
    Execute multiple search functions in parallel with instrumentation.

    Args:
        search_funcs: Dict mapping source name to (function, args, kwargs)
        max_workers: Maximum concurrent threads (optimal: 4-12 per Relace.ai research)
        timeout_seconds: Maximum time to wait for all searches

    Returns:
        ParallelSearchResult with timing metrics and results

    Example:
        result = execute_parallel_searches({
            'experience': (get_similar_experiences, (query,), {'max_results': 5}),
            'manifest': (_search_manifest, (query,), {'max_results': 5}),
            'kg': (kg.find_relevant_chunks, (query,), {'max_results': 10}),
        })
    """
    start_total = time.perf_counter()
    metrics = []
    results = {}
    sequential_estimate = 0.0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}

        for name, (func, args, kwargs) in search_funcs.items():
            future = executor.submit(_timed_execution, name, func, *args, **kwargs)
            futures[future] = name

        for future in as_completed(futures, timeout=timeout_seconds):
            name, result, latency, error = future.result()

            # Track sequential estimate (sum of all latencies)
            sequential_estimate += latency

            # Count results
            if result is None:
                result_count = 0
            elif isinstance(result, list):
                result_count = len(result)
            elif isinstance(result, dict):
                result_count = len(result.get('items', result.get('chunks', [result])))
            else:
                result_count = 1

            metrics.append(SearchMetrics(
                source=name,
                latency_ms=latency,
                result_count=result_count,
                success=error is None,
                error=error
            ))

            if error is None:
                results[name] = result

    total_latency = (time.perf_counter() - start_total) * 1000
    speedup = sequential_estimate / total_latency if total_latency > 0 else 1.0

    return ParallelSearchResult(
        total_latency_ms=total_latency,
        sequential_latency_ms=sequential_estimate,
        speedup_factor=speedup,
        metrics=metrics,
        results=results
    )


def enrich_context(
    query: str,
    max_tokens: int = 3000,
    include_concepts: bool = True,
    include_skills: bool = True
) -> Dict:
    """
    Enrich agent context with relevant KG information.

    This is the primary entry point for agents. Given a user query,
    returns relevant chunks, concepts, and skill suggestions.

    Args:
        query: User's question or task description
        max_tokens: Token budget for retrieved content
        include_concepts: Whether to include concept definitions
        include_skills: Whether to suggest relevant skills

    Returns:
        Dict with:
        - chunks: List of relevant content chunks
        - concepts: Matched concept definitions
        - suggested_skills: Skills that might help
        - summary: One-line summary of what was found

    Example:
        >>> context = enrich_context("migrate legacy SQL to dbt")
        >>> print(context['summary'])
        "Found 5 chunks about migration, 2 concepts, suggested skill: dbt-migration"
    """
    kg = get_kg()

    # Allocate token budget
    chunk_budget = int(max_tokens * 0.7)  # 70% for chunks
    concept_budget = int(max_tokens * 0.2)  # 20% for concepts

    result = {
        'chunks': [],
        'concepts': [],
        'suggested_skills': [],
        'summary': ''
    }

    # 1. Find relevant chunks
    chunks = kg.find_relevant_chunks(query, max_tokens=chunk_budget)
    result['chunks'] = [
        {
            'content': c.content,
            'source': c.source_doc,
            'score': round(c.score, 2)
        }
        for c in chunks
    ]

    # 2. Extract and lookup concepts mentioned in query
    if include_concepts:
        concept_keywords = _extract_concept_keywords(query)
        for keyword in concept_keywords[:3]:  # Limit to top 3
            ctx = kg.get_concept_context(keyword)
            if ctx.get('found'):
                result['concepts'].append({
                    'label': ctx.get('label'),
                    'definition': ctx.get('definition', '')[:200],
                    'related_docs': ctx.get('related_docs', [])[:5]
                })

    # 3. Suggest relevant skills based on query
    if include_skills:
        result['suggested_skills'] = _suggest_skills(query, kg)

    # 4. Generate summary
    chunk_count = len(result['chunks'])
    concept_count = len(result['concepts'])
    skill_suggestion = result['suggested_skills'][0] if result['suggested_skills'] else None

    summary_parts = []
    if chunk_count:
        summary_parts.append(f"Found {chunk_count} relevant chunks")
    if concept_count:
        summary_parts.append(f"{concept_count} concepts")
    if skill_suggestion:
        summary_parts.append(f"suggested skill: {skill_suggestion}")

    result['summary'] = ', '.join(summary_parts) if summary_parts else "No relevant content found"

    return result


def smart_search(
    query: str,
    max_results: int = 10,
    search_type: str = 'hybrid'
) -> List[Dict]:
    """
    Smart search combining keyword and semantic matching.

    Args:
        query: Search query
        max_results: Maximum results to return
        search_type: 'keyword', 'concept', or 'hybrid' (default)

    Returns:
        List of search results with source, preview, and relevance score
    """
    kg = get_kg()

    chunks = kg.find_relevant_chunks(query, max_results=max_results)

    return [
        {
            'source': c.source_doc,
            'preview': c.content[:300] + '...' if len(c.content) > 300 else c.content,
            'score': round(c.score, 2),
            'concepts': c.concepts[:5] if c.concepts else []
        }
        for c in chunks
    ]


def get_skill_context_for_activation(skill_name: str) -> Dict:
    """
    Get full context needed when activating a skill.

    Returns everything an agent needs to effectively use a skill:
    - Skill metadata
    - Key concepts it implements
    - Related reference documents
    - Sample chunks from the skill file

    Args:
        skill_name: Skill identifier (e.g., "dbt-migration")

    Returns:
        Dict with skill context ready for agent consumption
    """
    kg = get_kg()

    context = kg.get_skill_context(skill_name)

    if not context.get('found'):
        return {
            'found': False,
            'skill_name': skill_name,
            'message': f"Skill '{skill_name}' not found in knowledge graph"
        }

    # Enrich with related chunks
    related_chunks = kg.find_relevant_chunks(
        skill_name.replace('kb-', '').replace('-', ' '),
        max_results=5,
        max_tokens=1500
    )

    return {
        'found': True,
        'skill_name': skill_name,
        'path': context.get('path'),
        'concepts': context.get('concepts', []),
        'related_content': [
            {'source': c.source_doc, 'preview': c.content[:200]}
            for c in related_chunks
        ]
    }


def check_before_edit(file_path: str) -> Dict:
    """
    Check impact before editing a file.

    Call this before modifying any documentation to understand
    what other documents depend on it.

    Args:
        file_path: Path to file being edited

    Returns:
        Dict with:
        - dependents: List of files that reference this one
        - concepts: Concepts defined in this file
        - risk_level: 'low', 'medium', 'high' based on dependent count
    """
    kg = get_kg()

    impacts = kg.impact_analysis(file_path)

    dependent_count = len(impacts)

    if dependent_count == 0:
        risk_level = 'low'
        message = "No other documents depend on this file"
    elif dependent_count < 5:
        risk_level = 'medium'
        message = f"{dependent_count} documents reference this file"
    else:
        risk_level = 'high'
        message = f"⚠️ {dependent_count} documents depend on this - review carefully"

    return {
        'file_path': file_path,
        'dependents': [
            {'path': d.get('path'), 'relationship': d.get('relationship')}
            for d in impacts
        ],
        'dependent_count': dependent_count,
        'risk_level': risk_level,
        'message': message
    }


def suggest_placement_for_insight(insight_text: str, max_similar: int = 5) -> Dict:
    """
    Suggest where to place a new insight based on existing content.

    Use this when the learning agent extracts insights from blog posts,
    documentation, or other sources and needs to know where to store them.

    Args:
        insight_text: The new insight/content to be placed
        max_similar: Maximum similar documents to analyze

    Returns:
        Dict with:
        - suggested_folder: Best folder for this content
        - similar_docs: Existing docs with similar content
        - related_concepts: Concepts this insight relates to
        - potential_duplicates: Docs that might already cover this
        - reasoning: Explanation of the suggestion

    Example:
        >>> result = suggest_placement_for_insight(
        ...     "Use MERGE for incremental loads when handling deletes"
        ... )
        >>> print(result['suggested_folder'])
        "shared/knowledge-base"
        >>> print(result['related_concepts'])
        ["Incremental Strategy", "Migration Pattern"]
    """
    kg = get_kg()

    # 1. Find similar existing content
    similar_chunks = kg.find_relevant_chunks(insight_text, max_results=max_similar * 2)

    # 2. Get concept matches
    context = enrich_context(insight_text, max_tokens=1500)

    # 3. Analyze folder distribution of similar docs
    folder_scores = {}
    seen_docs = set()

    for chunk in similar_chunks:
        doc_path = chunk.source_doc
        if doc_path in seen_docs:
            continue
        seen_docs.add(doc_path)

        # Extract folder (first 2 path segments)
        parts = doc_path.split('/')
        if len(parts) >= 2:
            folder = '/'.join(parts[:2])
        else:
            folder = 'root'

        # Weight by relevance score
        folder_scores[folder] = folder_scores.get(folder, 0) + chunk.score

    # 4. Determine best folder
    if folder_scores:
        suggested_folder = max(folder_scores, key=folder_scores.get)
    else:
        suggested_folder = 'shared/knowledge-base'  # Default

    # 5. Check for potential duplicates (high similarity)
    potential_duplicates = [
        chunk.source_doc for chunk in similar_chunks
        if chunk.score > 0.6
    ][:3]

    # 6. Build reasoning
    similar_doc_list = list(seen_docs)[:max_similar]
    concept_labels = [c['label'] for c in context.get('concepts', [])]

    if potential_duplicates:
        reasoning = f"⚠️ High similarity with {potential_duplicates[0]} - check for duplication. "
    else:
        reasoning = ""

    reasoning += f"Found {len(similar_doc_list)} related docs, most in '{suggested_folder}'."

    if concept_labels:
        reasoning += f" Relates to concepts: {', '.join(concept_labels)}."

    return {
        'suggested_folder': suggested_folder,
        'similar_docs': similar_doc_list,
        'related_concepts': concept_labels,
        'potential_duplicates': potential_duplicates,
        'folder_scores': {k: round(v, 2) for k, v in sorted(
            folder_scores.items(), key=lambda x: -x[1]
        )[:5]},
        'reasoning': reasoning
    }


# ==================== Helper Functions ====================

def _extract_concept_keywords(query: str) -> List[str]:
    """Extract potential concept keywords from a query."""
    # Key domain terms that map to concepts
    concept_terms = {
        'migration': 'migration',
        'migrate': 'migration',
        'canonical': 'canonical model',
        'qa': 'qa strategy',
        'validation': 'qa strategy',
        'incremental': 'incremental strategy',
        'semantic': 'semantic layer',
        'metric': 'semantic layer',
        'medallion': 'medallion architecture',
        'staging': 'medallion architecture',
        'intermediate': 'medallion architecture',
        'mart': 'medallion architecture',
        'data product': 'data product',
        'sla': 'sla monitoring',
    }

    query_lower = query.lower()
    found = []

    for term, concept in concept_terms.items():
        if term in query_lower and concept not in found:
            found.append(concept)

    return found


def _suggest_skills(query: str, kg: KGAgentWrapper) -> List[str]:
    """Suggest relevant skills based on query content."""
    # Keyword to skill mapping
    skill_triggers = {
        'migrate': 'dbt-migration',
        'migration': 'dbt-migration',
        'legacy': 'dbt-migration',
        'optimize': 'dbt-redshift-optimization',
        'performance': 'dbt-redshift-optimization',
        'slow': 'dbt-redshift-optimization',
        'qa': 'dbt-qa-execution',
        'test': 'dbt-qa-execution',
        'validate': 'dbt-qa-execution',
        'canonical': 'dbt-canonical-model-finder',
        'reuse': 'dbt-canonical-model-finder',
        'folder': 'dbt-model-placement-advisor',
        'where should': 'dbt-model-placement-advisor',
        'placement': 'dbt-model-placement-advisor',
        'style': 'dbt-style-evaluator',
        'semantic': 'dbt-semantic-layer-developer',
        'metric': 'dbt-semantic-layer-developer',
    }

    query_lower = query.lower()
    suggested = []

    for trigger, skill in skill_triggers.items():
        if trigger in query_lower and skill not in suggested:
            suggested.append(skill)

    return suggested[:3]  # Max 3 suggestions


# ==================== Context Health Checks ====================

def check_context_health(chunks: List[Dict], query: str = None) -> Dict:
    """
    Check context for common failure modes.

    Detects:
    - Poisoning: Potentially hallucinated or incorrect content
    - Distraction: Irrelevant content that could mislead
    - Clash: Contradictory information
    - Confusion: Ambiguous or unclear content

    Args:
        chunks: List of chunk dicts with 'content' and 'source' keys
        query: Optional query to check relevance against

    Returns:
        Dict with health status and any issues found
    """
    issues = []
    warnings = []

    # 1. Check for poisoning indicators (hallucination markers)
    poisoning_markers = [
        (r'\b(I think|I believe|probably|maybe|might be)\b', 'uncertainty_language'),
        (r'\b(as an AI|as a language model)\b', 'ai_self_reference'),
        (r'\b(I cannot|I don\'t have access)\b', 'capability_limitation'),
        (r'(TODO|FIXME|XXX|HACK)\b', 'incomplete_marker'),
    ]

    for chunk in chunks:
        content = chunk.get('content', '')
        source = chunk.get('source', chunk.get('source_doc', 'unknown'))

        for pattern, marker_type in poisoning_markers:
            if re.search(pattern, content, re.IGNORECASE):
                warnings.append({
                    'type': 'poisoning_risk',
                    'marker': marker_type,
                    'source': source,
                    'preview': content[:100]
                })

    # 2. Check for distraction (low relevance if query provided)
    if query:
        query_words = set(re.findall(r'\b\w{4,}\b', query.lower()))

        for chunk in chunks:
            content = chunk.get('content', '').lower()
            content_words = set(re.findall(r'\b\w{4,}\b', content))

            overlap = len(query_words & content_words)
            relevance = overlap / max(len(query_words), 1)

            if relevance < 0.1 and len(content) > 100:
                warnings.append({
                    'type': 'distraction_risk',
                    'relevance': round(relevance, 3),
                    'source': chunk.get('source', chunk.get('source_doc', 'unknown')),
                    'message': 'Low relevance to query - may distract'
                })

    # 3. Check for clash (contradictory patterns)
    all_content = ' '.join(c.get('content', '') for c in chunks).lower()

    # Find "always use X" and check for "never use X"
    always_matches = re.findall(r'always use (\w+)', all_content)
    for term in always_matches:
        if re.search(rf'never use {term}', all_content):
            issues.append({
                'type': 'clash',
                'pattern': f"Contradictory: 'always use {term}' vs 'never use {term}'",
                'severity': 'high'
            })

    # Find "must X" and check for "do not X"
    must_matches = re.findall(r'must (\w+)', all_content)
    for term in must_matches:
        if re.search(rf'do not {term}', all_content):
            issues.append({
                'type': 'clash',
                'pattern': f"Contradictory: 'must {term}' vs 'do not {term}'",
                'severity': 'high'
            })

    # Check for required vs optional
    if 'required' in all_content and 'optional' in all_content:
        issues.append({
            'type': 'clash',
            'pattern': "Both 'required' and 'optional' mentioned - may conflict",
            'severity': 'medium'
        })

    # 4. Check for confusion (ambiguous content)
    confusion_markers = [
        (r'\b(depends|it varies|context-dependent)\b', 'ambiguous_guidance'),
        (r'\b(see also|refer to|check)\b.*\b(documentation|docs)\b', 'external_reference'),
        (r'\?\s*$', 'ends_with_question'),  # Content ending with question
    ]

    for chunk in chunks:
        content = chunk.get('content', '')

        for pattern, marker_type in confusion_markers:
            if re.search(pattern, content, re.IGNORECASE):
                warnings.append({
                    'type': 'confusion_risk',
                    'marker': marker_type,
                    'source': chunk.get('source', chunk.get('source_doc', 'unknown'))
                })

    # Calculate health score
    issue_penalty = len(issues) * 0.2
    warning_penalty = len(warnings) * 0.05
    health_score = max(0, 1.0 - issue_penalty - warning_penalty)

    # Determine status
    if issues:
        status = 'unhealthy'
    elif len(warnings) > 3:
        status = 'degraded'
    elif warnings:
        status = 'warning'
    else:
        status = 'healthy'

    return {
        'status': status,
        'health_score': round(health_score, 2),
        'issues': issues,
        'warnings': warnings[:10],  # Limit warnings shown
        'total_warnings': len(warnings),
        'chunks_checked': len(chunks),
        'summary': _generate_health_summary(status, issues, warnings)
    }


def _generate_health_summary(status: str, issues: List, warnings: List) -> str:
    """Generate human-readable health summary."""
    if status == 'healthy':
        return "✅ Context looks healthy - no issues detected"

    parts = []

    if issues:
        parts.append(f"❌ {len(issues)} critical issues (contradictions found)")

    poisoning = [w for w in warnings if w['type'] == 'poisoning_risk']
    distraction = [w for w in warnings if w['type'] == 'distraction_risk']
    confusion = [w for w in warnings if w['type'] == 'confusion_risk']

    if poisoning:
        parts.append(f"⚠️ {len(poisoning)} poisoning risks (uncertain/incomplete content)")
    if distraction:
        parts.append(f"⚠️ {len(distraction)} distraction risks (low relevance)")
    if confusion:
        parts.append(f"⚠️ {len(confusion)} confusion risks (ambiguous content)")

    return '; '.join(parts) if parts else "Context has minor warnings"


def validate_before_retrieval(query: str, max_chunks: int = 10) -> Dict:
    """
    Validate context health before returning to agent.

    Retrieves chunks and checks them for issues before use.

    Args:
        query: The search query
        max_chunks: Maximum chunks to retrieve and check

    Returns:
        Dict with chunks and health status
    """
    kg = get_kg()
    chunks = kg.find_relevant_chunks(query, max_results=max_chunks)

    # Convert to dict format for health check
    chunk_dicts = [
        {
            'content': c.content,
            'source': c.source_doc,
            'score': c.score
        }
        for c in chunks
    ]

    health = check_context_health(chunk_dicts, query)

    return {
        'chunks': chunk_dicts,
        'health': health,
        'safe_to_use': health['status'] in ['healthy', 'warning'],
        'recommendation': _get_health_recommendation(health)
    }


def _get_health_recommendation(health: Dict) -> str:
    """Get recommendation based on health status."""
    if health['status'] == 'healthy':
        return "Proceed with retrieved context"
    elif health['status'] == 'warning':
        return "Proceed with caution - verify critical information"
    elif health['status'] == 'degraded':
        return "Consider filtering low-relevance chunks before use"
    else:
        return "⚠️ Review context manually - contradictions detected"


# ==================== Unified Retrieval (Hybrid Integration) ====================

# Code query indicators - patterns that suggest looking at model code/SQL
CODE_QUERY_PATTERNS = [
    r'\bwhich model',
    r'\bwhat model',
    r'\bfind model',
    r'\bsearch model',
    r'\bwhere.*used',
    r'\bwhere.*column',
    r'\bcompiled sql',
    r'\bcompiled code',
    r'\blineage',
    r'\bparent.*model',
    r'\bchild.*model',
    r'\bupstream',
    r'\bdownstream',
    r'\bref\(',
    r'\bsource\(',
    r'\bmodel.*use',
    r'\bcolumn.*used',
    r'\bwho.*ref',
    r'\bdepend',
]


def _is_code_query(query: str) -> bool:
    """
    Detect if query is about model code/SQL rather than documentation.

    Returns True if query seems to be asking about:
    - Which models use a column
    - Model lineage (parents/children)
    - Compiled SQL patterns
    - Where something is referenced
    """
    query_lower = query.lower()

    for pattern in CODE_QUERY_PATTERNS:
        if re.search(pattern, query_lower):
            return True

    return False


def _search_manifest(query: str, max_results: int = 5) -> List[Dict]:
    """
    Search dbt manifest for models matching query.

    Searches:
    - Compiled SQL for patterns
    - Model names
    - Column names in metadata

    Returns list of matching models with context.
    """
    import sys
    from pathlib import Path

    # Add manifest parser to path
    skill_path = Path(__file__).parent.parent.parent / '.claude' / 'skills' / 'dbt-manifest-parser'
    if not skill_path.exists():
        # Backward compatibility: skill was archived but still usable
        skill_path = Path(__file__).parent.parent.parent / '.claude' / 'skills' / '_archived' / 'dbt-manifest-parser'
    if str(skill_path) not in sys.path:
        sys.path.insert(0, str(skill_path))

    try:
        from utils import ManifestParser
        parser = ManifestParser()

        # Extract search terms from query
        # Remove common words to get the actual search pattern
        stopwords = {'which', 'what', 'where', 'how', 'model', 'models', 'use', 'uses', 'used',
                    'the', 'a', 'an', 'is', 'are', 'in', 'on', 'for', 'to', 'of', 'column',
                    'find', 'search', 'get', 'show', 'compiled', 'sql'}

        words = re.findall(r'\b\w+\b', query.lower())
        search_terms = [w for w in words if w not in stopwords and len(w) > 2]

        results = []
        seen_models = set()

        for term in search_terms[:3]:  # Limit to top 3 terms
            matches = parser.search_models_by_sql_pattern(term)

            for match in matches:
                if match['model'] not in seen_models:
                    seen_models.add(match['model'])

                    # Get additional context
                    try:
                        lineage = parser.get_model_lineage(match['model'])
                        compiled_preview = parser.get_compiled_sql(match['model'])[:300]
                    except:
                        lineage = {'parent_count': 0, 'child_count': 0}
                        compiled_preview = ""

                    results.append({
                        'type': 'model_code',
                        'source': f"manifest:{match['model']}",
                        'content': f"**Model: {match['model']}**\n"
                                  f"Path: {match['path']}\n"
                                  f"Materialization: {match['materialized']}\n"
                                  f"Parents: {lineage.get('parent_count', 0)}, "
                                  f"Children: {lineage.get('child_count', 0)}\n"
                                  f"Matched term: '{term}'\n\n"
                                  f"SQL Preview:\n```sql\n{compiled_preview}...\n```",
                        'score': 0.9,  # High score for direct code matches
                        'model_name': match['model'],
                        'match_term': term
                    })

                    if len(results) >= max_results:
                        return results

        return results

    except FileNotFoundError:
        # Manifest not found - return empty
        return []
    except Exception as e:
        # Log but don't fail
        print(f"Manifest search warning: {e}")
        return []


def unified_retrieval(
    query: str,
    max_chunks: int = 10,
    experience_threshold: float = 0.15,
    include_health_check: bool = True,
    include_manifest: bool = True,
    agent_name: str = "unknown",
    parallel: bool = True,
    max_workers: int = 8
) -> Dict:
    """
    Hybrid retrieval combining Experience Store, KG, Manifest, and health checks.

    This is the recommended entry point for agents. It:
    1. Checks Experience Store for high-confidence matches (fast path)
    2. Retrieves from KG for comprehensive documentation
    3. Searches Manifest for model code/SQL if query appears code-related
    4. Validates combined context for health issues
    5. Returns structured result with metadata

    NEW in v2.0: Parallel execution for 2-4x speedup (Fast Agentic Search pattern)

    Args:
        query: The search query
        max_chunks: Maximum KG chunks to retrieve
        experience_threshold: Minimum score for experience matches (0-1)
        include_health_check: Whether to run health validation
        include_manifest: Whether to search manifest for code queries
        agent_name: Name of requesting agent (for logging)
        parallel: Whether to run searches in parallel (default: True)
        max_workers: Maximum concurrent threads (optimal: 4-12)

    Returns:
        Dict with:
        - context: Combined list of experience + manifest + KG content
        - health: Health check results (if enabled)
        - experience_hits: Number of high-confidence experience matches
        - manifest_hits: Number of model code matches
        - kg_chunks: Number of KG chunks retrieved
        - safe_to_use: Boolean indicating if context is safe
        - recommendation: Human-readable recommendation
        - performance: Parallel execution metrics (latency, speedup)

    Example:
        # Documentation query
        result = unified_retrieval("How do I handle deletes in incremental?")

        # Code query - automatically searches manifest
        result = unified_retrieval("Which models use mcc_desc column?")
        # → Returns models from manifest + related documentation

        # Sequential mode (for debugging)
        result = unified_retrieval("query", parallel=False)
    """
    from .experience_store import get_similar_experiences
    from .graph_search import search_graph as _graph_search

    is_code = _is_code_query(query)
    kg = get_kg()

    # ==================== PARALLEL EXECUTION PATH ====================
    if parallel:
        # Build search function registry
        search_funcs = {
            'experience': (
                get_similar_experiences,
                (query,),
                {'max_results': 5}
            ),
            'kg': (
                kg.find_relevant_chunks,
                (query,),
                {'max_results': max_chunks}
            ),
            'knowledge_graph': (
                _graph_search,
                (query,),
                {'max_results': 5, 'traverse_depth': 1}
            ),
        }

        # Add manifest search if this is a code query
        if include_manifest and is_code:
            search_funcs['manifest'] = (
                _search_manifest,
                (query,),
                {'max_results': 5}
            )

        # Execute all searches in parallel
        parallel_result = execute_parallel_searches(
            search_funcs,
            max_workers=max_workers
        )

        # Extract results
        experiences = parallel_result.results.get('experience', [])
        chunks = parallel_result.results.get('kg', [])
        manifest_results = parallel_result.results.get('manifest', [])
        graph_results = parallel_result.results.get('knowledge_graph', [])

        performance_metrics = {
            'parallel_enabled': True,
            'total_latency_ms': parallel_result.total_latency_ms,
            'sequential_estimate_ms': parallel_result.sequential_latency_ms,
            'speedup_factor': parallel_result.speedup_factor,
            'sources_searched': len(parallel_result.metrics),
            'per_source': [
                {
                    'source': m.source,
                    'latency_ms': m.latency_ms,
                    'result_count': m.result_count,
                    'success': m.success,
                    'error': m.error
                }
                for m in parallel_result.metrics
            ]
        }

    # ==================== SEQUENTIAL EXECUTION PATH ====================
    else:
        start_total = time.perf_counter()
        source_timings = []

        # 1. Experience check
        start = time.perf_counter()
        experiences = get_similar_experiences(query, max_results=5)
        source_timings.append(('experience', (time.perf_counter() - start) * 1000))

        # 2. Manifest search (if code query)
        manifest_results = []
        if include_manifest and is_code:
            start = time.perf_counter()
            manifest_results = _search_manifest(query, max_results=5)
            source_timings.append(('manifest', (time.perf_counter() - start) * 1000))

        # 3. KG retrieval
        start = time.perf_counter()
        chunks = kg.find_relevant_chunks(query, max_results=max_chunks)
        source_timings.append(('kg', (time.perf_counter() - start) * 1000))

        # 4. Knowledge graph search (learnings, traces, rules, skills)
        start = time.perf_counter()
        try:
            graph_results = _graph_search(query, max_results=5, traverse_depth=1)
        except Exception:
            graph_results = []
        source_timings.append(('knowledge_graph', (time.perf_counter() - start) * 1000))

        total_latency = (time.perf_counter() - start_total) * 1000

        performance_metrics = {
            'parallel_enabled': False,
            'total_latency_ms': total_latency,
            'sequential_estimate_ms': total_latency,
            'speedup_factor': 1.0,
            'sources_searched': len(source_timings),
            'per_source': [
                {'source': name, 'latency_ms': latency}
                for name, latency in source_timings
            ]
        }

    # ==================== COMBINE RESULTS ====================
    high_confidence = [e for e in experiences if e['score'] >= experience_threshold]

    # Build combined context (experience → manifest → KG order)
    combined_context = []

    # Add high-confidence experiences as "proven solutions"
    if high_confidence:
        for exp in high_confidence:
            combined_context.append({
                'type': 'experience',
                'source': f"agent:{exp['agent']}",
                'content': f"**Proven Solution** (from {exp['agent']} agent):\n"
                          f"Problem: {exp['problem']}\n"
                          f"Solution: {exp['solution']}\n"
                          f"Confidence: {exp['score']:.0%}",
                'score': exp['score'],
                'tags': exp.get('tags', [])
            })

    # Add manifest results (model code matches)
    if manifest_results:
        combined_context.extend(manifest_results)

    # Add knowledge graph results (learnings, traces, rules, skills)
    if graph_results:
        for gr in graph_results:
            related_summary = ""
            if hasattr(gr, 'related') and gr.related:
                related_titles = [r.get('title', '')[:60] for r in gr.related[:3]]
                related_summary = " | See also: " + ", ".join(related_titles)
            combined_context.append({
                'type': 'knowledge_graph',
                'source': f"{gr.store}:{gr.store_path}" if hasattr(gr, 'store_path') else gr.store,
                'content': f"**{gr.title}**\n{gr.content}{related_summary}",
                'score': gr.relevance if hasattr(gr, 'relevance') else 0.5,
                'node_id': gr.node_id if hasattr(gr, 'node_id') else None,
                'store': gr.store if hasattr(gr, 'store') else 'unknown',
            })

    # Add KG chunks
    for chunk in chunks:
        combined_context.append({
            'type': 'documentation',
            'source': chunk.source_doc,
            'content': chunk.content,
            'score': chunk.score
        })

    # Health check if enabled (always sequential - depends on combined results)
    health = None
    safe_to_use = True
    recommendation = "Context retrieved successfully"

    if include_health_check and combined_context:
        health = check_context_health(combined_context, query)
        safe_to_use = health['status'] in ['healthy', 'warning']
        recommendation = _get_health_recommendation(health)

    # Return structured result with performance metrics
    return {
        'query': query,
        'context': combined_context,
        'health': health,
        'experience_hits': len(high_confidence),
        'experience_details': high_confidence,
        'manifest_hits': len(manifest_results) if manifest_results else 0,
        'manifest_details': manifest_results if manifest_results else [],
        'graph_hits': len(graph_results) if graph_results else 0,
        'kg_chunks': len(chunks) if chunks else 0,
        'total_items': len(combined_context),
        'is_code_query': is_code,
        'safe_to_use': safe_to_use,
        'recommendation': recommendation,
        'performance': performance_metrics,
        'metadata': {
            'agent': agent_name,
            'experience_threshold': experience_threshold,
            'health_check_enabled': include_health_check,
            'manifest_search_enabled': include_manifest,
            'parallel_enabled': parallel,
            'max_workers': max_workers if parallel else None
        }
    }


def log_agent_resolution(
    agent: str,
    query: str,
    solution: str,
    context: Dict = None,
    outcome: str = "success"
) -> Dict:
    """
    Log a successful resolution for cross-agent learning.

    Call this after an agent successfully completes a task.
    The resolution will be available to other agents via unified_retrieval().

    Args:
        agent: Name of the agent (migration, qa, discovery, etc.)
        query: The original problem/question
        solution: What worked (concise description)
        context: Additional context (model name, technique, etc.)
        outcome: success, partial, or failed

    Returns:
        Dict with logged experience details

    Example:
        log_agent_resolution(
            agent="migration",
            query="Handle deletes in incremental model",
            solution="Use delete+insert pattern with merge on unique key",
            context={"model": "int_transactions", "technique": "merge"}
        )
    """
    from .experience_store import log_agent_success, ExperienceStore

    if outcome == "success":
        exp = log_agent_success(agent, query, solution, context)
        return {
            'logged': True,
            'experience_id': exp.id,
            'agent': agent,
            'message': f"Experience logged: {exp.id}"
        }
    else:
        # Log non-success outcomes too (for learning what doesn't work)
        store = ExperienceStore()
        exp = store.log_experience(
            agent=agent,
            problem=query,
            solution=solution,
            context=context or {},
            outcome=outcome
        )
        return {
            'logged': True,
            'experience_id': exp.id,
            'agent': agent,
            'outcome': outcome,
            'message': f"Experience logged with outcome: {outcome}"
        }


def get_system_health() -> Dict:
    """
    Get overall health of the knowledge system.

    Combines KB quality metrics with experience store stats.
    Use for monitoring and alerting.

    Returns:
        Dict with system-wide health metrics
    """
    from .kb_quality import KBQualityTester
    from .experience_store import ExperienceStore

    # Get KB metrics (fast version - skip full report)
    kg = get_kg()
    chunks = kg.chunks_data or []

    # Get experience stats
    store = ExperienceStore()
    exp_summary = store.get_pattern_summary()

    return {
        'kb': {
            'total_chunks': len(chunks),
            'status': 'healthy' if len(chunks) > 1000 else 'degraded'
        },
        'experience_store': {
            'total_experiences': exp_summary['total_experiences'],
            'by_agent': exp_summary['by_agent'],
            'success_rate': exp_summary['success_rate'],
            'top_patterns': exp_summary['top_patterns'][:5]
        },
        'overall_status': 'operational',
        'recommendation': 'System healthy' if exp_summary['total_experiences'] > 0 else 'Build experience corpus by logging successful resolutions'
    }


# ==================== get_context() - Unified Entry Point ====================

@dataclass
class ContextResult:
    """Result of get_context() call with obligations and skill suggestions."""
    context: List[Dict]
    suggested_skills: List[str]
    obligations: List[str]
    health: Dict
    safe_to_use: bool
    recommendation: str
    performance: Dict
    metadata: Dict

    def summary(self) -> str:
        """Human-readable summary."""
        return (
            f"Context: {len(self.context)} items | "
            f"Skills: {', '.join(self.suggested_skills) or 'none'} | "
            f"Obligations: {len(self.obligations)} | "
            f"Health: {self.health.get('status', 'unknown')}"
        )


def get_context(
    query: str,
    scope: str = "auto",
    max_chunks: int = 10,
    include_health_check: bool = True,
    include_manifest: bool = True,
    parallel: bool = True
) -> ContextResult:
    """
    Single entry point for all context retrieval.

    This is the primary API for agents. It:
    1. Detects query type (migration, qa, semantic, discovery, architecture)
    2. Retrieves relevant context from Experience + KG + Manifest
    3. Suggests skills based on query content
    4. Infers obligations for this task type
    5. Updates session state to mark context_retrieved = True
    6. Returns structured result ready for agent consumption

    Args:
        query: The user's question or task description
        scope: "auto" (detect), "docs", "code", or "all"
        max_chunks: Maximum KG chunks to retrieve
        include_health_check: Whether to validate context health
        include_manifest: Whether to search manifest for code queries
        parallel: Whether to run searches in parallel

    Returns:
        ContextResult with context, suggested_skills, obligations, and health

    Example:
        result = get_context("migrate merchant_spend pipeline")
        # result.suggested_skills = ["dbt-migration"]
        # result.obligations = ["preflight", "canonical_check", "compile", "verify"]

        result = get_context("Which models use mcc_desc?")
        # result.context includes manifest matches
        # result.obligations = ["context"]  # simple query
    """
    from ..runtime.session import (
        load_session,
        save_session,
        start_session,
        infer_task_type,
    )
    from ..runtime.guards import mark_context_retrieved

    # 1. Infer task type from query
    task_type = infer_task_type(query)

    # 2. Get or create session
    session = load_session()
    if not session.user_query:
        # New session - initialize with task type
        session = start_session(task_type, query)
    else:
        # Existing session - update query if different
        if session.user_query != query:
            session.user_query = query
            session.task_type = task_type

    # 3. Get obligations for this task type
    default_obligations = {
        "migration": ["context", "preflight", "canonical_check", "compile", "verify"],
        "qa": ["context", "verify"],
        "semantic": ["context"],
        "discovery": ["context"],
        "architecture": ["context", "canonical_check"],
        "default": ["context"],
    }
    obligations = default_obligations.get(task_type, default_obligations["default"])

    # 4. Get skill suggestions via keyword matching
    suggested_skills = _suggest_skills(query, get_kg())

    # Update skill triggers with consolidated skill names
    skill_trigger_updates = {
        'dbt-qa-execution': 'dbt-qa',
        'dbt-canonical-model-finder': 'dbt-standards',
        'dbt-model-placement-advisor': 'dbt-standards',
        'dbt-style-evaluator': 'dbt-standards',
    }

    # Map old skill names to new consolidated names
    suggested_skills = [
        skill_trigger_updates.get(skill, skill)
        for skill in suggested_skills
    ]
    # Remove duplicates while preserving order
    seen = set()
    suggested_skills = [
        s for s in suggested_skills
        if not (s in seen or seen.add(s))
    ]

    # 5. Perform unified retrieval
    retrieval_result = unified_retrieval(
        query=query,
        max_chunks=max_chunks,
        include_health_check=include_health_check,
        include_manifest=include_manifest,
        parallel=parallel,
    )

    # 6. Update session state
    session.state.context_retrieved = True
    session.suggested_skills = suggested_skills
    session.obligations = obligations
    session.log_tool_event(
        "get_context",
        success=True,
        details={
            "query": query[:100],
            "task_type": task_type,
            "items_retrieved": retrieval_result["total_items"],
        },
    )
    save_session(session)

    # 7. Emit telemetry
    try:
        from ..runtime.telemetry import emit_tool_event
        emit_tool_event(
            "get_context",
            success=True,
            context={
                "query": query[:100],
                "task_type": task_type,
                "total_items": retrieval_result["total_items"],
                "experience_hits": retrieval_result["experience_hits"],
                "manifest_hits": retrieval_result["manifest_hits"],
                "kg_chunks": retrieval_result["kg_chunks"],
            },
        )
    except ImportError:
        pass  # Telemetry not available yet

    # 8. Build result
    return ContextResult(
        context=retrieval_result["context"],
        suggested_skills=suggested_skills,
        obligations=obligations,
        health=retrieval_result.get("health") or {},
        safe_to_use=retrieval_result["safe_to_use"],
        recommendation=retrieval_result["recommendation"],
        performance=retrieval_result["performance"],
        metadata={
            "task_type": task_type,
            "session_id": session.session_id,
            "query": query,
            "is_code_query": retrieval_result["is_code_query"],
        },
    )


# ==================== CLI for Agent Use ====================

def cli_search(query: str, output_format: str = "text", max_chunks: int = 10) -> None:
    """
    CLI entry point for unified_retrieval.

    Usage:
        python -m tools.kg.agent_integration search "your query"
        python -m tools.kg.agent_integration search "your query" --json
        python -m tools.kg.agent_integration search "your query" --max 5
    """
    result = unified_retrieval(query, max_chunks=max_chunks)

    if output_format == "json":
        # JSON output for programmatic use
        import json
        # Remove non-serializable items
        output = {
            'query': result['query'],
            'total_items': result['total_items'],
            'experience_hits': result['experience_hits'],
            'manifest_hits': result['manifest_hits'],
            'kg_chunks': result['kg_chunks'],
            'is_code_query': result['is_code_query'],
            'safe_to_use': result['safe_to_use'],
            'recommendation': result['recommendation'],
            'performance': result['performance'],
            'context': [
                {
                    'type': c.get('type'),
                    'source': c.get('source'),
                    'content': c.get('content', '')[:500],  # Truncate for readability
                    'score': c.get('score')
                }
                for c in result['context'][:10]  # Limit output
            ]
        }
        print(json.dumps(output, indent=2, default=str))
    else:
        # Human-readable text output
        print(f"\n{'='*60}")
        print(f"🔍 UNIFIED SEARCH: {query}")
        print(f"{'='*60}\n")

        # Performance summary
        perf = result['performance']
        print(f"⚡ Performance: {perf['total_latency_ms']:.0f}ms", end="")
        if perf['parallel_enabled']:
            print(f" (parallel, {perf['speedup_factor']:.1f}x speedup)")
        else:
            print(" (sequential)")

        # Results summary
        print(f"\n📊 Results: {result['total_items']} items")
        print(f"   • Experience hits: {result['experience_hits']}")
        print(f"   • Manifest hits: {result['manifest_hits']}")
        print(f"   • KG chunks: {result['kg_chunks']}")
        print(f"   • Code query: {result['is_code_query']}")

        # Health status
        if result.get('health'):
            health = result['health']
            status_icon = "✅" if health['status'] == 'healthy' else "⚠️" if health['status'] == 'warning' else "❌"
            print(f"\n🏥 Health: {status_icon} {health['status']} (score: {health['health_score']})")

        # Top results
        print(f"\n📄 Top Results:")
        print("-" * 50)
        for i, ctx in enumerate(result['context'][:5], 1):
            type_icon = "💡" if ctx['type'] == 'experience' else "📦" if ctx['type'] == 'model_code' else "📚"
            score = f"[{ctx.get('score', 0):.2f}]" if ctx.get('score') else ""
            print(f"\n{i}. {type_icon} {ctx['type'].upper()} {score}")
            print(f"   Source: {ctx.get('source', 'unknown')}")
            content = ctx.get('content', '')[:200]
            print(f"   {content}...")

        print(f"\n{'='*60}")
        print(f"💬 Recommendation: {result['recommendation']}")
        print(f"{'='*60}\n")


def cli_health() -> None:
    """Show system health status."""
    health = get_system_health()
    print(f"\n🏥 KNOWLEDGE SYSTEM HEALTH")
    print("=" * 40)
    print(f"Overall: {health['overall_status']}")
    print(f"\nKnowledge Base:")
    print(f"  • Chunks: {health['kb']['total_chunks']}")
    print(f"  • Status: {health['kb']['status']}")
    print(f"\nExperience Store:")
    print(f"  • Total: {health['experience_store']['total_experiences']}")
    print(f"  • Success rate: {health['experience_store']['success_rate']:.0%}")
    print(f"\n💬 {health['recommendation']}\n")


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description="Knowledge Graph Agent Integration CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search with parallel execution (default)
  python -m tools.kg.agent_integration search "How do I handle deletes?"

  # JSON output for programmatic use
  python -m tools.kg.agent_integration search "Which models use calendar_date?" --json

  # Limit results
  python -m tools.kg.agent_integration search "incremental strategy" --max 5

  # Check system health
  python -m tools.kg.agent_integration health

  # Legacy enrich_context (for backward compatibility)
  python -m tools.kg.agent_integration enrich "migrate legacy SQL"
"""
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Search command (primary)
    search_parser = subparsers.add_parser('search', help='Unified search across all sources')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--json', action='store_true', help='Output as JSON')
    search_parser.add_argument('--max', type=int, default=10, help='Max results (default: 10)')

    # Health command
    health_parser = subparsers.add_parser('health', help='Show system health')

    # Enrich command (legacy)
    enrich_parser = subparsers.add_parser('enrich', help='Legacy enrich_context')
    enrich_parser.add_argument('query', help='Query to enrich')

    args = parser.parse_args()

    if args.command == 'search':
        output_format = 'json' if args.json else 'text'
        cli_search(args.query, output_format=output_format, max_chunks=args.max)

    elif args.command == 'health':
        cli_health()

    elif args.command == 'enrich':
        # Legacy behavior
        query = args.query
        print(f"\n🔍 Query: {query}\n")
        context = enrich_context(query)
        print(f"📊 Summary: {context['summary']}\n")
        if context['concepts']:
            print("💡 Concepts:")
            for c in context['concepts']:
                print(f"   • {c['label']}: {c['definition'][:100]}...")
        if context['suggested_skills']:
            print(f"\n🛠️  Suggested skills: {', '.join(context['suggested_skills'])}")
        if context['chunks']:
            print(f"\n📄 Top {len(context['chunks'])} chunks:")
            for i, chunk in enumerate(context['chunks'][:3], 1):
                print(f"   {i}. [{chunk['score']}] {chunk['source']}")
                print(f"      {chunk['content'][:150]}...")

    else:
        parser.print_help()
