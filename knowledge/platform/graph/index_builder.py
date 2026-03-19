#!/usr/bin/env python3
"""
Unified Knowledge Graph Index Builder

Scans 9+ knowledge stores across dbt-agent and CAF (analytics-workspace) and produces a unified graph index
at docs/knowledge-graph/unified-index.json. The index contains metadata nodes
and relationship edges — content stays in the underlying stores.

Usage:
    .venv/bin/python3 tools/kg/index_builder.py              # Full rebuild
    .venv/bin/python3 tools/kg/index_builder.py --store learnings  # Rebuild one store
    .venv/bin/python3 tools/kg/index_builder.py --stats       # Show index statistics
    .venv/bin/python3 tools/kg/index_builder.py --validate    # Check for broken edges
    .venv/bin/python3 tools/kg/index_builder.py --incremental file1 file2  # Re-index changed files only
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from typing import Optional
import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

# Resolve workspace root (analytics-workspace) — this is the promoted AW copy
# index_builder.py → graph/ → platform/ → knowledge/ → analytics-workspace/
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent.parent
PROJECT_ROOT = WORKSPACE_ROOT / "dbt-agent"  # dbt-agent is a child of workspace
CAF_ROOT = WORKSPACE_ROOT  # AW IS the CAF root
DBT_ENTERPRISE_ROOT = WORKSPACE_ROOT / "dbt-enterprise"
OUTPUT_PATH = WORKSPACE_ROOT / "knowledge" / "platform" / "graph" / "unified-index.json"


# ---------------------------------------------------------------------------
# Domain vocabulary for topic extraction (no LLM needed)
# ---------------------------------------------------------------------------

DOMAIN_VOCABULARY = {
    # dbt concepts
    "incremental", "materialized", "staging", "intermediate", "mart",
    "compile", "run", "build", "test", "parse", "snapshot", "seed",
    "ref", "source", "macro", "jinja", "cte", "grain", "contract",
    "model", "schema", "yaml", "config", "defer", "partial-parse",
    # Redshift
    "redshift", "distkey", "sortkey", "spectrum", "merge", "vacuum",
    # Strategies
    "delete-insert", "full-refresh", "append",
    # Data concepts
    "join", "filter", "aggregate", "window", "union", "deduplicate",
    "null", "duplicate", "cardinality", "fan-out", "suppression",
    "variance", "inflation", "missing-column", "compile-error", "timeout",
    # Pipeline names
    "disbursements", "merchant-spend", "funds-movement", "registration",
    "ewallet", "cohort", "demographics", "arc-insights", "wonderwall",
    "interchange", "samsung", "tokenization",
    # Transactions & business
    "posted", "transaction", "auth", "declined", "approval", "attempt",
    "wallet", "tokenize", "gbos", "baas", "prevention",
    "disbursement", "rovo", "gft", "aci", "processor",
    "pos-entry-mode", "revenue",
    # Agent / handoff
    "handoff", "plan",
    # Reference artifacts
    "canonical", "playbook", "troubleshoot", "cheatsheet",
    "manifest", "casting", "dictionary", "edw",
    "controlled-vocabulary",
    # Tools
    "metricflow", "semantic-layer", "tableau", "ci-cd", "github-actions",
    "mcp", "fusion", "linter", "lint", "parser", "mining",
    # QA
    "qa", "validation", "variance-analysis", "decision-trace",
    # Redshift runtime / performance
    "wlm", "timeout", "abort", "spiller", "skewed",
    "scan", "hash-join", "nested-loop", "broadcast", "redistribute",
    "statistics", "analyze", "stale",
    # SQL patterns
    "eav", "pivot", "unpivot", "subquery", "correlated",
    "not-exists", "not-in", "left-join",
    # Research / architecture
    "alma", "skillsbench", "trustgraph", "reification",
    "context-graph", "knowledge-graph", "ontology",
    "kepler", "dash", "competitive", "benchmark",
    "memory", "persistence", "embedding", "vector",
    # System
    "skill", "rule", "learning", "experience", "knowledge-base",
    "agent", "orchestrator", "pipeline", "migration", "optimization",
    "preflight", "lineage", "discovery", "context", "meta-context",
    "coverage", "confidence", "false-confidence",
    # Multi-agent
    "ensemble", "analyst", "builder", "architect",
    "onboarding", "explainer", "workflow",
}

# Known bigrams to detect
DOMAIN_BIGRAMS = {
    "full refresh": "full-refresh",
    "delete insert": "delete-insert",
    "fan out": "fan-out",
    "semantic layer": "semantic-layer",
    "partial parse": "partial-parse",
    "decision trace": "decision-trace",
    "knowledge base": "knowledge-base",
    "compile error": "compile-error",
    "missing column": "missing-column",
    "variance analysis": "variance-analysis",
    "ci cd": "ci-cd",
    "meta context": "meta-context",
    "false confidence": "false-confidence",
    "unit test": "unit-test",
    "row count": "row-count",
    "merge inflation": "merge-inflation",
    "arc insights": "arc-insights",
    "merchant spend": "merchant-spend",
    "funds movement": "funds-movement",
    "controlled vocabulary": "controlled-vocabulary",
    "posted transaction": "posted-transaction",
    "declined transaction": "declined-transaction",
    "type casting": "type-casting",
    "field mapping": "field-mapping",
    "gold standard": "gold-standard",
    "data limitation": "data-limitation",
    "pos entry": "pos-entry-mode",
    "interchange revenue": "interchange-revenue",
    "wlm timeout": "wlm-timeout",
    "wlm abort": "wlm-abort",
    "hash join": "hash-join",
    "nested loop": "nested-loop",
    "not exists": "not-exists",
    "not in": "not-in",
    "left join": "left-join",
    "knowledge graph": "knowledge-graph",
    "context graph": "context-graph",
    "query log": "query-log",
    "query mining": "query-mining",
    "anti pattern": "anti-pattern",
    "agent memory": "agent-memory",
    "multi agent": "multi-agent",
    "trust graph": "trustgraph",
}

STOPWORDS = {
    "the", "a", "an", "is", "was", "were", "are", "been", "be", "have", "has",
    "had", "do", "does", "did", "will", "would", "could", "should", "may",
    "might", "shall", "can", "to", "of", "in", "for", "on", "with", "at",
    "by", "from", "as", "into", "through", "during", "before", "after",
    "above", "below", "between", "out", "off", "over", "under", "again",
    "further", "then", "once", "here", "there", "when", "where", "why",
    "how", "all", "each", "every", "both", "few", "more", "most", "other",
    "some", "such", "no", "nor", "not", "only", "own", "same", "so",
    "than", "too", "very", "just", "because", "but", "and", "or", "if",
    "while", "about", "up", "that", "this", "it", "its", "they", "them",
    "we", "us", "you", "your", "he", "she", "his", "her",
}


def extract_topics(text: str, max_topics: int = 12) -> list[str]:
    """Extract topic keywords from text using vocabulary matching.

    Increased default to 12 topics for richer metadata on knowledge docs.
    """
    if not text:
        return []

    text_lower = text.lower()
    topics = set()

    # Check bigrams first
    for bigram, normalized in DOMAIN_BIGRAMS.items():
        if bigram in text_lower:
            topics.add(normalized)

    # Split into words, remove punctuation
    words = re.findall(r'[a-z][a-z0-9_-]*', text_lower)

    # Match against vocabulary
    for word in words:
        if word in DOMAIN_VOCABULARY and word not in STOPWORDS:
            topics.add(word)

    # Also check hyphenated forms
    for i in range(len(words) - 1):
        hyphenated = f"{words[i]}-{words[i+1]}"
        if hyphenated in DOMAIN_VOCABULARY:
            topics.add(hyphenated)

    return sorted(topics)[:max_topics]


def extract_topics_from_file(filepath: Path, max_topics: int = 12) -> list[str]:
    """Extract topics from a file by sampling filename, title, headers, and body.

    Reads the first ~2000 chars of the file plus all ## headers for richer
    topic extraction than filename+title alone.
    """
    try:
        content = filepath.read_text()
    except Exception:
        return extract_topics(filepath.stem.replace("-", " "), max_topics)

    lines = content.splitlines()
    filename_text = filepath.stem.replace("-", " ").replace("_", " ")

    # Collect: filename + all headers + first ~2000 chars of body
    header_text = ""
    body_text = ""
    body_chars = 0
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            header_text += " " + stripped.lstrip("#").strip()
        elif body_chars < 2000:
            body_text += " " + stripped
            body_chars += len(stripped)

    combined = f"{filename_text} {header_text} {body_text}"
    return extract_topics(combined, max_topics)


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Node:
    id: str
    store: str
    store_path: str
    type: str
    title: str
    topics: list[str]
    summary: str
    anchor: str
    weight: float = 1.0
    created: str = ""
    last_accessed: Optional[str] = None
    # CAF + research enhancements
    domain: str = "agent"
    repo: str = "dbt-agent"
    detail_level: str = "L1"
    l0_summary: str = ""
    valid_from: Optional[str] = None
    valid_until: Optional[str] = None
    promoted_to_caf: bool = False
    evidence_log: list = field(default_factory=list)


@dataclass
class Edge:
    from_id: str
    to_id: str
    type: str
    strength: float = 1.0
    evidence: str = ""


# ---------------------------------------------------------------------------
# Base scanner
# ---------------------------------------------------------------------------

class StoreScanner(ABC):
    @abstractmethod
    def scan(self) -> tuple[list[Node], list[Edge]]:
        """Return nodes and intra-store edges."""
        pass


# ---------------------------------------------------------------------------
# Learnings Scanner
# ---------------------------------------------------------------------------

class LearningsScanner(StoreScanner):
    """Scan shared/learnings/cross-cutting/*.yaml and PROTOTYPE-distilled-learnings.yaml"""

    def scan(self) -> tuple[list[Node], list[Edge]]:
        nodes = []
        edges = []

        # Scan cross-cutting YAML files
        cross_cutting_dir = PROJECT_ROOT / "shared" / "learnings" / "cross-cutting"
        if cross_cutting_dir.exists():
            for yaml_file in sorted(cross_cutting_dir.glob("*.yaml")):
                file_nodes, file_edges = self._scan_learnings_yaml(yaml_file)
                nodes.extend(file_nodes)
                edges.extend(file_edges)

        # Scan PROTOTYPE file (different format — domain_facts + pipelines)
        proto_path = PROJECT_ROOT / "shared" / "learnings" / "PROTOTYPE-distilled-learnings.yaml"
        if proto_path.exists():
            proto_nodes, proto_edges = self._scan_prototype(proto_path)
            nodes.extend(proto_nodes)
            edges.extend(proto_edges)

        return nodes, edges

    def _scan_learnings_yaml(self, filepath: Path) -> tuple[list[Node], list[Edge]]:
        """Parse a cross-cutting learnings YAML file.

        Format: top-level keys like error_fixes, patterns, workflow_patterns, domain_knowledge
        Each contains a list of dicts with id, trigger, action, etc.
        """
        nodes = []
        edges = []
        rel_path = str(filepath.relative_to(PROJECT_ROOT))

        try:
            import yaml
            with open(filepath) as f:
                data = yaml.safe_load(f)
        except Exception:
            # Fallback: simple regex-based parsing
            data = self._parse_yaml_simple(filepath)

        if not isinstance(data, dict):
            return nodes, edges

        domain = data.get("domain", "unknown")

        # Scan all list-valued keys (error_fixes, patterns, domain_knowledge, etc.)
        for section_key, entries in data.items():
            if not isinstance(entries, list):
                continue

            for entry in entries:
                if not isinstance(entry, dict) or "id" not in entry:
                    continue

                entry_id = entry["id"]
                trigger = entry.get("trigger", "")
                action = entry.get("action", "")
                rationale = entry.get("rationale", "")
                pipeline = entry.get("pipeline", "")
                model = entry.get("model", "")
                date = entry.get("date", "")
                trace_id = entry.get("trace_id", "")

                # Determine type from section key
                type_map = {
                    "error_fixes": "error_fix",
                    "patterns": "pattern",
                    "workflow_patterns": "workflow_pattern",
                    "domain_knowledge": "domain_knowledge",
                }
                node_type = type_map.get(section_key, section_key.rstrip("s"))

                # Build topics from trigger + action + pipeline + model
                topic_text = f"{trigger} {action} {pipeline} {model} {domain}"
                topics = extract_topics(topic_text)

                title = (action[:117] + "...") if len(action) > 120 else action
                summary = trigger[:200] if trigger else action[:200]

                node = Node(
                    id=entry_id,
                    store="learnings",
                    store_path=rel_path,
                    type=node_type,
                    title=title or f"Learning {entry_id}",
                    topics=topics,
                    summary=summary,
                    anchor=entry_id,
                    created=str(date) if date else "",
                    valid_from=str(date) if date else None,
                    l0_summary=f"{node_type}: {title[:50]}",
                )
                nodes.append(node)

                # Edge to trace if trace_id exists
                if trace_id:
                    edges.append(Edge(
                        from_id=entry_id,
                        to_id=trace_id,
                        type="derived_from",
                        evidence=f"Learning {entry_id} extracted from trace {trace_id}",
                    ))

        return nodes, edges

    def _scan_prototype(self, filepath: Path) -> tuple[list[Node], list[Edge]]:
        """Parse the PROTOTYPE distilled learnings (different format: pipelines with domain_facts)."""
        nodes = []
        edges = []
        rel_path = str(filepath.relative_to(PROJECT_ROOT))

        try:
            import yaml
            with open(filepath) as f:
                data = yaml.safe_load(f)
        except Exception:
            return nodes, edges

        if not isinstance(data, dict):
            return nodes, edges

        pipelines = data.get("pipelines", {})
        if not isinstance(pipelines, dict):
            return nodes, edges

        for pipeline_name, pipeline_data in pipelines.items():
            if not isinstance(pipeline_data, dict):
                continue

            facts = pipeline_data.get("domain_facts", [])
            if not isinstance(facts, list):
                continue

            for i, fact in enumerate(facts):
                if not isinstance(fact, dict):
                    continue
                fact_text = fact.get("fact", "")
                if not fact_text:
                    continue

                fact_id = f"proto-{pipeline_name}-{i+1:03d}"
                topics = extract_topics(f"{fact_text} {pipeline_name}")

                nodes.append(Node(
                    id=fact_id,
                    store="learnings",
                    store_path=rel_path,
                    type="domain_fact",
                    title=(fact_text[:117] + "...") if len(fact_text) > 120 else fact_text,
                    topics=topics,
                    summary=fact_text[:200],
                    anchor=fact_id,
                    l0_summary=f"fact: {fact_text[:50]}",
                ))

        return nodes, edges

    def _parse_yaml_simple(self, filepath: Path) -> dict:
        """Fallback YAML parsing without PyYAML."""
        # Try importing yaml
        try:
            import yaml
            with open(filepath) as f:
                return yaml.safe_load(f)
        except ImportError:
            pass

        # Very basic parsing for our known format
        content = filepath.read_text()
        result = {"domain": "unknown"}
        current_section = None
        current_entry = {}
        entries_by_section = {}

        for line in content.splitlines():
            # Top-level section (e.g., "error_fixes:")
            if re.match(r'^[a-z_]+:', line) and not line.startswith(' '):
                key, _, val = line.partition(':')
                val = val.strip()
                if val:
                    result[key] = val.strip('" ')
                else:
                    current_section = key
                    entries_by_section[current_section] = []
            # New entry in section
            elif line.strip().startswith('- id:'):
                if current_entry and current_section:
                    entries_by_section[current_section].append(current_entry)
                current_entry = {"id": line.split(':', 1)[1].strip()}
            # Entry field
            elif line.strip().startswith(('trace_id:', 'trigger:', 'action:',
                                          'rationale:', 'level:', 'pipeline:',
                                          'model:', 'date:', 'cost_minutes:',
                                          'when_applicable:', 'when_not_applicable:')):
                key, _, val = line.strip().partition(':')
                current_entry[key.strip()] = val.strip().strip('"')

        if current_entry and current_section:
            entries_by_section[current_section].append(current_entry)

        result.update(entries_by_section)
        return result


# ---------------------------------------------------------------------------
# Traces Scanner
# ---------------------------------------------------------------------------

class TracesScanner(StoreScanner):
    """Scan shared/decision-traces/traces.json"""

    def scan(self) -> tuple[list[Node], list[Edge]]:
        nodes = []
        edges = []
        traces_path = PROJECT_ROOT / "shared" / "decision-traces" / "traces.json"

        if not traces_path.exists():
            return nodes, edges

        rel_path = str(traces_path.relative_to(PROJECT_ROOT))

        try:
            data = json.loads(traces_path.read_text())
        except Exception:
            return nodes, edges

        traces = data.get("traces", [])

        for trace in traces:
            if not isinstance(trace, dict):
                continue

            trace_id = trace.get("id", "")
            if not trace_id:
                continue

            problem = trace.get("problem", {})
            resolution = trace.get("resolution", {})
            model = trace.get("model", "")
            timestamp = trace.get("timestamp", "")

            symptom = problem.get("symptom", "")
            error_type = problem.get("error_type", "")
            fix = resolution.get("fix", "")
            root_cause = resolution.get("root_cause", "")
            fix_category = resolution.get("fix_category", "")

            # Build title: symptom -> fix (truncated)
            symptom_short = symptom[:80] if symptom else "Unknown symptom"
            fix_short = fix[:40] if fix else "Unknown fix"
            title = f"{symptom_short}"
            if len(title) > 120:
                title = title[:117] + "..."

            # Topics
            topic_text = f"{error_type} {model} {fix_category} {symptom} {fix}"
            topics = extract_topics(topic_text)

            summary = root_cause[:200] if root_cause else symptom[:200]

            created = ""
            if timestamp:
                try:
                    created = timestamp[:10]  # Extract date part
                except Exception:
                    pass

            nodes.append(Node(
                id=trace_id,
                store="traces",
                store_path=rel_path,
                type="decision_trace",
                title=title,
                topics=topics,
                summary=summary,
                anchor=trace_id,
                created=created,
                valid_from=created or None,
                l0_summary=f"trace: {error_type} on {model}"[:50],
            ))

        return nodes, edges


# ---------------------------------------------------------------------------
# Rules Scanner
# ---------------------------------------------------------------------------

class RulesScanner(StoreScanner):
    """Scan shared/decision-traces/rules.json AND .claude/rules/*.md"""

    def scan(self) -> tuple[list[Node], list[Edge]]:
        nodes = []
        edges = []

        # Part A: Synthesized rules from rules.json
        a_nodes, a_edges = self._scan_synthesized_rules()
        nodes.extend(a_nodes)
        edges.extend(a_edges)

        # Part B: Claude behavioral rules from .claude/rules/*.md
        b_nodes, b_edges = self._scan_claude_rules()
        nodes.extend(b_nodes)
        edges.extend(b_edges)

        return nodes, edges

    def _scan_synthesized_rules(self) -> tuple[list[Node], list[Edge]]:
        nodes = []
        edges = []
        rules_path = PROJECT_ROOT / "shared" / "decision-traces" / "rules.json"

        if not rules_path.exists():
            return nodes, edges

        rel_path = str(rules_path.relative_to(PROJECT_ROOT))

        try:
            data = json.loads(rules_path.read_text())
        except Exception:
            return nodes, edges

        rules = data.get("rules", [])

        for rule in rules:
            if not isinstance(rule, dict):
                continue

            pattern_id = rule.get("pattern_id", "")
            if not pattern_id:
                continue

            pattern = rule.get("pattern", {})
            action = rule.get("recommended_action", {})
            source_traces = rule.get("source_traces", [])
            confidence = rule.get("confidence", "medium")
            created = rule.get("created", "")

            generalized_symptom = pattern.get("generalized_symptom", "")
            error_types = pattern.get("error_types", [])
            contexts = pattern.get("contexts", [])
            first_try = action.get("first_try", "")

            title = generalized_symptom[:120] if generalized_symptom else f"Rule {pattern_id}"
            summary = f"{generalized_symptom} -> {first_try}"[:200]

            # Topics from error_types + contexts + symptom
            topic_text = " ".join(error_types + contexts) + " " + generalized_symptom
            topics = extract_topics(topic_text)

            nodes.append(Node(
                id=pattern_id,
                store="rules",
                store_path=rel_path,
                type="synthesized_rule",
                title=title,
                topics=topics,
                summary=summary,
                anchor=pattern_id,
                created=created[:10] if created else "",
                valid_from=created[:10] if created else None,
                l0_summary=f"rule: {title[:45]}",
            ))

            # Edges to source traces
            for trace_id in source_traces:
                edges.append(Edge(
                    from_id=pattern_id,
                    to_id=trace_id,
                    type="derived_from",
                    evidence=f"Rule {pattern_id} synthesized from trace {trace_id}",
                ))

        return nodes, edges

    def _scan_claude_rules(self) -> tuple[list[Node], list[Edge]]:
        nodes = []
        edges = []
        rules_dir = PROJECT_ROOT / ".claude" / "rules"

        if not rules_dir.exists():
            return nodes, edges

        for md_file in sorted(rules_dir.glob("*.md")):
            rel_path = str(md_file.relative_to(PROJECT_ROOT))
            filename = md_file.stem

            try:
                content = md_file.read_text()
            except Exception:
                continue

            lines = content.splitlines()

            # Extract title (first H1)
            title = filename.replace("-", " ").title()
            for line in lines:
                if line.startswith("# "):
                    title = line[2:].strip()
                    break

            # Extract summary (first non-heading, non-empty paragraph)
            summary = ""
            in_paragraph = False
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    if in_paragraph:
                        break
                    continue
                if stripped.startswith("#"):
                    in_paragraph = False
                    continue
                summary += " " + stripped
                in_paragraph = True
            summary = summary.strip()[:200]

            # Topics from filename + title + summary
            topic_text = f"{filename.replace('-', ' ')} {title} {summary}"
            topics = extract_topics(topic_text)

            node_id = f"rule-{filename}"

            nodes.append(Node(
                id=node_id,
                store="claude_rules",
                store_path=rel_path,
                type="behavioral_rule",
                title=title[:120],
                topics=topics,
                summary=summary,
                anchor=node_id,
                l0_summary=f"rule: {title[:45]}",
            ))

        return nodes, edges


# ---------------------------------------------------------------------------
# Experiences Scanner
# ---------------------------------------------------------------------------

class ExperiencesScanner(StoreScanner):
    """Scan docs/knowledge-graph/experiences.json — cluster by tag, not individual nodes."""

    def scan(self) -> tuple[list[Node], list[Edge]]:
        nodes = []
        edges = []
        exp_path = PROJECT_ROOT / "docs" / "knowledge-graph" / "experiences.json"

        if not exp_path.exists():
            return nodes, edges

        rel_path = str(exp_path.relative_to(PROJECT_ROOT))

        try:
            data = json.loads(exp_path.read_text())
        except Exception:
            return nodes, edges

        experiences = data.get("experiences", data if isinstance(data, list) else [])

        # Group by tags
        tag_clusters: dict[str, list[dict]] = {}
        for exp in experiences:
            if not isinstance(exp, dict):
                continue
            tags = exp.get("tags", [])
            if not tags:
                tags = ["untagged"]
            for tag in tags:
                if tag not in tag_clusters:
                    tag_clusters[tag] = []
                tag_clusters[tag].append(exp)

        # Create cluster nodes for tags with 3+ experiences
        for tag, cluster in sorted(tag_clusters.items()):
            if len(cluster) < 3:
                continue
            if tag == "untagged":
                continue  # Skip untagged cluster (too noisy)

            cluster_id = f"exp-cluster-{tag}"

            # Find most common outcome
            outcomes = Counter(
                e.get("context", {}).get("outcome", "unknown") for e in cluster
            )
            common_outcome = outcomes.most_common(1)[0][0] if outcomes else "mixed"

            # Collect related tags from cluster members
            related_tags = Counter()
            for e in cluster:
                for t in e.get("tags", []):
                    if t != tag and t != "untagged":
                        related_tags[t] += 1
            top_related = [t for t, _ in related_tags.most_common(5)]

            topics = [tag] + top_related
            topics = [t for t in topics if t][:8]

            title = f"{len(cluster)} sessions involving {tag}"
            summary = f"Cluster of {len(cluster)} experiences tagged '{tag}'. Most common outcome: {common_outcome}. Related topics: {', '.join(top_related[:3])}."

            nodes.append(Node(
                id=cluster_id,
                store="experiences",
                store_path=rel_path,
                type="experience_cluster",
                title=title[:120],
                topics=topics,
                summary=summary[:200],
                anchor=cluster_id,
                l0_summary=f"exp: {len(cluster)} {tag} sessions",
            ))

        return nodes, edges


# ---------------------------------------------------------------------------
# Skills Scanner
# ---------------------------------------------------------------------------

class SkillsScanner(StoreScanner):
    """Scan .claude/skills/*/SKILL.md — create nodes for each skill."""

    def scan(self) -> tuple[list[Node], list[Edge]]:
        nodes = []
        edges = []
        skills_dirs = [
            (PROJECT_ROOT / ".claude" / "skills", PROJECT_ROOT, "dbt-agent"),
            (CAF_ROOT / ".claude" / "skills", CAF_ROOT, "caf"),
        ]

        for skills_dir, root, repo in skills_dirs:
            if not skills_dir.exists():
                continue
            self._scan_skills_dir(skills_dir, root, repo, nodes, edges)

        return nodes, edges

    def _scan_skills_dir(self, skills_dir: Path, root: Path, repo: str,
                         nodes: list, edges: list):
        for skill_dir in sorted(skills_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            if skill_dir.name.startswith("_"):
                continue  # Skip _archived

            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue

            rel_path = str(skill_md.relative_to(root))
            folder_name = skill_dir.name

            try:
                content = skill_md.read_text()
            except Exception:
                continue

            # Parse YAML frontmatter
            name = folder_name
            description = ""
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter = parts[1]
                    # Extract name
                    name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
                    if name_match:
                        name = name_match.group(1).strip()
                    # Extract description (handles >, |, and inline forms)
                    desc_match = re.search(r'description:\s*[>|]?\s*\n((?:\s+.+\n)*)', frontmatter)
                    if desc_match:
                        description = desc_match.group(1).strip()
                    elif re.search(r'^description:\s*(.+)$', frontmatter, re.MULTILINE):
                        description = re.search(r'^description:\s*(.+)$', frontmatter, re.MULTILINE).group(1).strip()

            # Also extract first body paragraph for richer topic extraction
            body = content.split("---", 2)[-1] if content.startswith("---") else content
            first_para = ""
            for line in body.splitlines():
                stripped = line.strip()
                if not stripped or stripped.startswith("#") or stripped.startswith("---"):
                    if first_para:
                        break
                    continue
                if stripped.startswith("|") or stripped.startswith("```"):
                    if first_para:
                        break
                    continue
                first_para += " " + stripped
            if first_para:
                description = (description + " " + first_para.strip())[:500]

            # Topics from name + description
            topic_text = f"{folder_name.replace('-', ' ')} {name} {description}"
            topics = extract_topics(topic_text)

            skill_id = f"skill-{folder_name}"

            nodes.append(Node(
                id=skill_id,
                store="skills",
                store_path=rel_path,
                type="skill",
                title=name[:120],
                topics=topics,
                summary=description[:200] if description else f"Skill: {name}",
                anchor=skill_id,
                l0_summary=f"skill: {name[:45]}",
            ))

            # Scan resources/ subdirectory
            resources_dir = skill_dir / "resources"
            if resources_dir.exists() and resources_dir.is_dir():
                for res_file in sorted(resources_dir.glob("*.md")):
                    res_rel_path = str(res_file.relative_to(root))
                    res_name = res_file.stem
                    res_id = f"skill-{folder_name}-{res_name}"

                    # Read first few lines for title
                    try:
                        res_content = res_file.read_text()
                        res_lines = res_content.splitlines()
                        res_title = res_name.replace("-", " ").title()
                        for line in res_lines:
                            if line.startswith("# "):
                                res_title = line[2:].strip()
                                break
                    except Exception:
                        res_title = res_name

                    res_topics = extract_topics(f"{res_name.replace('-', ' ')} {res_title} {folder_name}")

                    nodes.append(Node(
                        id=res_id,
                        store="skills",
                        store_path=res_rel_path,
                        type="skill_resource",
                        title=res_title[:120],
                        topics=res_topics,
                        summary=f"Resource for {name}: {res_title}"[:200],
                        anchor=res_id,
                        l0_summary=f"resource: {res_title[:40]}",
                    ))

                    # Edge to parent skill
                    edges.append(Edge(
                        from_id=res_id,
                        to_id=skill_id,
                        type="elaborated_in",
                        evidence=f"Resource file for skill {name}",
                    ))


# ---------------------------------------------------------------------------
# Knowledge Base + Reference Docs Scanner
# ---------------------------------------------------------------------------

class DocsScanner(StoreScanner):
    """Scan shared/knowledge-base/*.md and shared/reference/*.md"""

    DIRS = [
        ("shared/knowledge-base", "knowledge_base", "kb"),
        ("shared/reference", "reference", "ref"),
    ]

    def scan(self) -> tuple[list[Node], list[Edge]]:
        nodes = []
        edges = []

        for dir_rel, store_name, prefix in self.DIRS:
            dir_path = PROJECT_ROOT / dir_rel
            if not dir_path.exists():
                continue

            for md_file in sorted(dir_path.glob("*.md")):
                rel_path = str(md_file.relative_to(PROJECT_ROOT))
                filename = md_file.stem
                node_id = f"{prefix}-{filename}"

                try:
                    content = md_file.read_text()
                except Exception:
                    continue

                lines = content.splitlines()

                # Extract title (first H1)
                title = filename.replace("-", " ").title()
                for line in lines:
                    if line.startswith("# "):
                        title = line[2:].strip()
                        break

                # Extract summary (first non-heading paragraph)
                summary = ""
                for line in lines:
                    stripped = line.strip()
                    if not stripped or stripped.startswith("#") or stripped.startswith("---"):
                        if summary:
                            break
                        continue
                    if stripped.startswith("|") or stripped.startswith("```"):
                        if summary:
                            break
                        continue
                    summary += " " + stripped

                summary = summary.strip()[:200]

                topics = extract_topics(f"{filename.replace('-', ' ')} {title} {summary}")

                nodes.append(Node(
                    id=node_id,
                    store=store_name,
                    store_path=rel_path,
                    type="reference_doc",
                    title=title[:120],
                    topics=topics,
                    summary=summary,
                    anchor=node_id,
                    l0_summary=f"doc: {title[:45]}",
                ))

        return nodes, edges


# ---------------------------------------------------------------------------
# CAF Reference Docs Scanner
# ---------------------------------------------------------------------------

class CAFDocsScanner(StoreScanner):
    """Scan knowledge/domains/*/reference/*.md and *.yml from analytics-workspace (CAF)."""

    DOMAIN_MAP = {
        "dbt-pipelines": "agent",
        "redshift": "agent",
        "semantic-layer": "agent",
        "data-storytelling": "content",
        "feature-store": "agent",
        "tpg-pipelines": "agent",
    }

    def scan(self) -> tuple[list[Node], list[Edge]]:
        nodes = []
        edges = []
        domains_dir = CAF_ROOT / "knowledge" / "domains"

        if not domains_dir.exists():
            return nodes, edges

        for domain_dir in sorted(domains_dir.iterdir()):
            if not domain_dir.is_dir():
                continue
            ref_dir = domain_dir / "reference"
            if not ref_dir.exists():
                continue

            domain_name = domain_dir.name
            domain_tag = self.DOMAIN_MAP.get(domain_name, "agent")

            for ref_file in sorted(ref_dir.glob("*")):
                if ref_file.suffix not in (".md", ".yml", ".yaml"):
                    continue

                try:
                    rel_path = str(ref_file.relative_to(CAF_ROOT))
                except ValueError:
                    rel_path = str(ref_file)

                filename = ref_file.stem
                node_id = f"caf-ref-{domain_name}-{filename}"

                try:
                    content = ref_file.read_text()
                except Exception:
                    continue

                lines = content.splitlines()

                # Extract title
                title = filename.replace("-", " ").title()
                for line in lines:
                    if line.startswith("# "):
                        title = line[2:].strip()
                        break

                # Extract summary (first non-heading paragraph)
                summary = ""
                for line in lines:
                    stripped = line.strip()
                    if not stripped or stripped.startswith("#") or stripped.startswith("---"):
                        if summary:
                            break
                        continue
                    if stripped.startswith("|") or stripped.startswith("```"):
                        if summary:
                            break
                        continue
                    summary += " " + stripped

                summary = summary.strip()[:200]

                topics = extract_topics_from_file(ref_file)

                nodes.append(Node(
                    id=node_id,
                    store="caf_reference",
                    store_path=rel_path,
                    type="reference_doc",
                    title=title[:120],
                    topics=topics,
                    summary=summary,
                    anchor=node_id,
                    domain=domain_tag,
                    repo="caf",
                    l0_summary=f"caf-doc: {title[:40]}",
                ))

        # Also scan knowledge/platform/research/ and knowledge/platform/*.md
        platform_dirs = [
            (CAF_ROOT / "knowledge" / "platform" / "research", "research"),
            (CAF_ROOT / "knowledge" / "platform", "platform"),
        ]
        for scan_dir, prefix in platform_dirs:
            if not scan_dir.exists():
                continue
            # For "platform" prefix, only scan .md files directly (not subdirs)
            glob_pattern = "*.md" if prefix == "platform" else "**/*.md"
            for md_file in sorted(scan_dir.glob(glob_pattern)):
                if md_file.name.startswith(".") or md_file.name == "README.md":
                    continue
                # Skip files in graph/ (that's us)
                if "graph" in md_file.parts:
                    continue

                try:
                    rel_path = str(md_file.relative_to(CAF_ROOT))
                except ValueError:
                    rel_path = str(md_file)

                filename = md_file.stem
                node_id = f"caf-ref-{prefix}-{filename}"

                try:
                    content = md_file.read_text()
                except Exception:
                    continue

                lines = content.splitlines()
                title = filename.replace("-", " ").title()
                for line in lines:
                    if line.startswith("# "):
                        title = line[2:].strip()
                        break

                summary = ""
                for line in lines:
                    stripped = line.strip()
                    if not stripped or stripped.startswith("#") or stripped.startswith("---"):
                        if summary:
                            break
                        continue
                    if stripped.startswith("|") or stripped.startswith("```"):
                        if summary:
                            break
                        continue
                    summary += " " + stripped
                summary = summary.strip()[:200]

                topics = extract_topics_from_file(md_file)

                nodes.append(Node(
                    id=node_id,
                    store="caf_reference",
                    store_path=rel_path,
                    type="reference_doc",
                    title=title[:120],
                    topics=topics,
                    summary=summary,
                    anchor=node_id,
                    domain="system",
                    repo="caf",
                    l0_summary=f"caf-{prefix}: {title[:40]}",
                ))

        return nodes, edges


# ---------------------------------------------------------------------------
# Tools Scanner
# ---------------------------------------------------------------------------

class ToolsScanner(StoreScanner):
    """Scan tools/ directory from analytics-workspace for linters, pipelines, etc."""

    def scan(self) -> tuple[list[Node], list[Edge]]:
        nodes = []
        edges = []
        tools_dir = CAF_ROOT / "tools"

        if not tools_dir.exists():
            return nodes, edges

        for tool_file in sorted(tools_dir.glob("**/*.py")):
            if tool_file.name.startswith("__"):
                continue

            try:
                rel_path = str(tool_file.relative_to(CAF_ROOT))
            except ValueError:
                rel_path = str(tool_file)

            filename = tool_file.stem
            parent = tool_file.parent.name if tool_file.parent != tools_dir else "tools"
            node_id = f"tool-{parent}-{filename}"

            try:
                content = tool_file.read_text()
            except Exception:
                continue

            # Extract docstring as summary
            lines = content.splitlines()
            title = f"{parent}/{filename}.py"
            summary = ""
            in_docstring = False
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    if in_docstring:
                        break
                    in_docstring = True
                    # Single-line docstring
                    inner = stripped[3:]
                    if inner.endswith('"""') or inner.endswith("'''"):
                        summary = inner[:-3].strip()
                        break
                    summary = inner.strip()
                    continue
                if in_docstring:
                    if stripped.endswith('"""') or stripped.endswith("'''"):
                        summary += " " + stripped[:-3].strip()
                        break
                    summary += " " + stripped

            summary = summary.strip()[:200]
            if not summary:
                summary = f"Python tool: {parent}/{filename}"

            topics = extract_topics_from_file(tool_file)

            nodes.append(Node(
                id=node_id,
                store="caf_tools",
                store_path=rel_path,
                type="tool",
                title=title,
                topics=topics,
                summary=summary,
                anchor=node_id,
                domain="system",
                repo="caf",
                l0_summary=f"tool: {title[:45]}",
            ))

        return nodes, edges


# ---------------------------------------------------------------------------
# CAF Traces Scanner
# ---------------------------------------------------------------------------

class CAFTracesScanner(StoreScanner):
    """Scan knowledge/domains/dbt-pipelines/decision-traces/traces-full.json from CAF."""

    def scan(self) -> tuple[list[Node], list[Edge]]:
        nodes = []
        edges = []
        traces_path = CAF_ROOT / "knowledge" / "domains" / "dbt-pipelines" / "decision-traces" / "traces-full.json"

        if not traces_path.exists():
            return nodes, edges

        try:
            rel_path = str(traces_path.relative_to(CAF_ROOT))
        except ValueError:
            rel_path = str(traces_path)

        try:
            data = json.loads(traces_path.read_text())
        except Exception:
            return nodes, edges

        traces = data.get("traces", [])

        for trace in traces:
            if not isinstance(trace, dict):
                continue

            trace_id = trace.get("id", "")
            if not trace_id:
                continue

            # Prefix to avoid collisions with dbt-agent local traces
            caf_trace_id = f"caf-trace-{trace_id}"

            problem = trace.get("problem", {})
            resolution = trace.get("resolution", {})
            model = trace.get("model", "")
            timestamp = trace.get("timestamp", "")

            symptom = problem.get("symptom", "")
            error_type = problem.get("error_type", "")
            fix = resolution.get("fix", "")
            root_cause = resolution.get("root_cause", "")
            fix_category = resolution.get("fix_category", "")

            symptom_short = symptom[:80] if symptom else "Unknown symptom"
            title = symptom_short
            if len(title) > 120:
                title = title[:117] + "..."

            topic_text = f"{error_type} {model} {fix_category} {symptom} {fix}"
            topics = extract_topics(topic_text)

            summary = root_cause[:200] if root_cause else symptom[:200]

            created = ""
            if timestamp:
                try:
                    created = timestamp[:10]
                except Exception:
                    pass

            nodes.append(Node(
                id=caf_trace_id,
                store="caf_traces",
                store_path=rel_path,
                type="decision_trace",
                title=title,
                topics=topics,
                summary=summary,
                anchor=trace_id,
                created=created,
                valid_from=created or None,
                domain="agent",
                repo="caf",
                l0_summary=f"caf-trace: {error_type} on {model}"[:50],
            ))

            # Edge to dbt-agent local trace with same ID (if it exists)
            edges.append(Edge(
                from_id=caf_trace_id,
                to_id=trace_id,
                type="same_as",
                evidence=f"CAF promoted copy of trace {trace_id}",
            ))

        return nodes, edges


# ---------------------------------------------------------------------------
# Enterprise Docs Scanner
# ---------------------------------------------------------------------------

class EnterpriseDocsScanner(StoreScanner):
    """Scan dbt-enterprise docs/business_context/*.md and docs/models_documentation/**/*.md."""

    def scan(self) -> tuple[list[Node], list[Edge]]:
        nodes = []
        edges = []

        if not DBT_ENTERPRISE_ROOT.exists():
            return nodes, edges

        # Scan docs/business_context/*.md
        biz_ctx_dir = DBT_ENTERPRISE_ROOT / "docs" / "business_context"
        if biz_ctx_dir.exists():
            for md_file in sorted(biz_ctx_dir.glob("*.md")):
                node = self._scan_md_file(md_file, "biz-ctx")
                if node:
                    nodes.append(node)

        # Scan docs/models_documentation/**/*.md (recursive)
        models_doc_dir = DBT_ENTERPRISE_ROOT / "docs" / "models_documentation"
        if models_doc_dir.exists():
            for md_file in sorted(models_doc_dir.rglob("*.md")):
                node = self._scan_md_file(md_file, "model-doc")
                if node:
                    nodes.append(node)

        return nodes, edges

    def _scan_md_file(self, md_file: Path, prefix: str) -> Optional[Node]:
        """Parse a single markdown file into a Node."""
        try:
            rel_path = str(md_file.relative_to(DBT_ENTERPRISE_ROOT))
        except ValueError:
            rel_path = str(md_file)

        filename = md_file.stem
        # Include parent dir for model-doc to disambiguate
        if prefix == "model-doc":
            parent_name = md_file.parent.name
            node_id = f"ent-doc-{parent_name}-{filename}"
        else:
            node_id = f"ent-doc-{filename}"

        try:
            content = md_file.read_text()
        except Exception:
            return None

        lines = content.splitlines()

        # Extract title (first H1)
        title = filename.replace("-", " ").replace("_", " ").title()
        for line in lines:
            if line.startswith("# "):
                title = line[2:].strip()
                break

        # Extract summary (first non-heading paragraph)
        summary = ""
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or stripped.startswith("---"):
                if summary:
                    break
                continue
            if stripped.startswith("|") or stripped.startswith("```"):
                if summary:
                    break
                continue
            summary += " " + stripped

        summary = summary.strip()[:200]

        topics = extract_topics(
            f"{filename.replace('-', ' ').replace('_', ' ')} {title} {summary}"
        )

        return Node(
            id=node_id,
            store="enterprise_docs",
            store_path=rel_path,
            type="reference_doc",
            title=title[:120],
            topics=topics,
            summary=summary,
            anchor=node_id,
            domain="business",
            repo="dbt-enterprise",
            l0_summary=f"ent-doc: {title[:40]}",
        )


# ---------------------------------------------------------------------------
# Handoffs Scanner
# ---------------------------------------------------------------------------

class HandoffsScanner(StoreScanner):
    """Scan handoffs/*/PLAN.md, handoffs/*.md, and handoffs/*.yaml (skip _templates/)."""

    def scan(self) -> tuple[list[Node], list[Edge]]:
        nodes = []
        edges = []
        handoffs_dir = PROJECT_ROOT / "handoffs"

        if not handoffs_dir.exists():
            return nodes, edges

        # 1. Top-level .md files
        for md_file in sorted(handoffs_dir.glob("*.md")):
            node = self._scan_md_handoff(md_file)
            if node:
                nodes.append(node)

        # 2. Top-level .yaml files
        for yaml_file in sorted(handoffs_dir.glob("*.yaml")):
            node = self._scan_yaml_handoff(yaml_file)
            if node:
                nodes.append(node)

        # 3. Subdirectory PLAN.md files (and active/*.md, completed/*.md, etc.)
        for sub_dir in sorted(handoffs_dir.iterdir()):
            if not sub_dir.is_dir():
                continue
            if sub_dir.name.startswith("_"):
                continue  # Skip _templates

            for md_file in sorted(sub_dir.glob("*.md")):
                node = self._scan_md_handoff(md_file, is_plan=(md_file.name == "PLAN.md"))
                if node:
                    nodes.append(node)

        return nodes, edges

    def _scan_md_handoff(self, md_file: Path, is_plan: bool = False) -> Optional[Node]:
        """Parse a handoff markdown file."""
        rel_path = str(md_file.relative_to(PROJECT_ROOT))
        filename = md_file.stem

        # Build a unique node_id from path
        parts = Path(rel_path).parts  # ('handoffs', 'disbursements', 'PLAN.md') etc.
        if len(parts) >= 3:
            # Subdirectory file: handoffs/<subdir>/<file>
            node_id = f"handoff-{parts[-2]}-{filename}"
        else:
            node_id = f"handoff-{filename}"

        try:
            content = md_file.read_text()
        except Exception:
            return None

        lines = content.splitlines()

        # Parse YAML frontmatter for phase/status if present
        phase = ""
        status = ""
        fm_text = ""
        if content.startswith("---"):
            fm_parts = content.split("---", 2)
            if len(fm_parts) >= 3:
                fm_text = fm_parts[1]
                phase_match = re.search(r'^phase:\s*(.+)$', fm_text, re.MULTILINE)
                if phase_match:
                    phase = phase_match.group(1).strip()
                status_match = re.search(r'^status:\s*(.+)$', fm_text, re.MULTILINE)
                if status_match:
                    status = status_match.group(1).strip()

        # Extract title (first H1)
        title = filename.replace("-", " ").replace("_", " ").title()
        for line in lines:
            if line.startswith("# "):
                title = line[2:].strip()
                break

        # Extract summary
        summary = ""
        past_frontmatter = not content.startswith("---")
        for line in lines:
            stripped = line.strip()
            if stripped == "---":
                past_frontmatter = True
                continue
            if not past_frontmatter:
                continue
            if not stripped or stripped.startswith("#"):
                if summary:
                    break
                continue
            if stripped.startswith("|") or stripped.startswith("```"):
                if summary:
                    break
                continue
            summary += " " + stripped

        summary = summary.strip()[:200]

        if phase:
            summary = f"[phase: {phase}] {summary}"[:200]

        topic_text = f"{filename.replace('-', ' ').replace('_', ' ')} {title} {summary} {phase} {status}"
        topics = extract_topics(topic_text)

        node_type = "pipeline_plan" if is_plan else "handoff"

        return Node(
            id=node_id,
            store="handoffs",
            store_path=rel_path,
            type=node_type,
            title=title[:120],
            topics=topics,
            summary=summary,
            anchor=node_id,
            domain="agent",
            repo="dbt-agent",
            l0_summary=f"handoff: {title[:40]}",
        )

    def _scan_yaml_handoff(self, yaml_file: Path) -> Optional[Node]:
        """Parse a handoff YAML file (e.g., PIPELINE_REGISTRY.yaml)."""
        rel_path = str(yaml_file.relative_to(PROJECT_ROOT))
        filename = yaml_file.stem
        node_id = f"handoff-{filename}"

        try:
            content = yaml_file.read_text()
        except Exception:
            return None

        # Extract a basic summary from first few non-comment lines
        summary_lines = []
        for line in content.splitlines()[:20]:
            stripped = line.strip()
            if stripped.startswith("#"):
                # YAML comment — use as summary text
                summary_lines.append(stripped.lstrip("# ").strip())
            elif stripped and not stripped.startswith("---"):
                summary_lines.append(stripped)

        summary = " ".join(summary_lines)[:200]

        title = filename.replace("-", " ").replace("_", " ").title()
        topics = extract_topics(f"{filename.replace('-', ' ').replace('_', ' ')} {summary}")

        return Node(
            id=node_id,
            store="handoffs",
            store_path=rel_path,
            type="registry",
            title=title[:120],
            topics=topics,
            summary=summary,
            anchor=node_id,
            domain="agent",
            repo="dbt-agent",
            l0_summary=f"handoff: {title[:40]}",
        )


# ---------------------------------------------------------------------------
# Cross-Store Edge Inference
# ---------------------------------------------------------------------------

def infer_cross_store_edges(nodes: dict[str, Node]) -> list[Edge]:
    """Find relationships between nodes in different stores using topic overlap."""
    edges = []
    edge_counts: dict[str, int] = {}  # node_id -> edge count (cap at 10)

    node_list = list(nodes.values())

    for i in range(len(node_list)):
        n1 = node_list[i]
        if edge_counts.get(n1.id, 0) >= 10:
            continue

        for j in range(i + 1, len(node_list)):
            n2 = node_list[j]

            # Only cross-store edges
            if n1.store == n2.store:
                continue

            if edge_counts.get(n2.id, 0) >= 10:
                continue

            # Strategy 1: Topic overlap (Jaccard similarity)
            s1 = set(n1.topics)
            s2 = set(n2.topics)
            if not s1 or not s2:
                continue

            intersection = s1 & s2
            union = s1 | s2

            if len(intersection) < 2:
                continue

            jaccard = len(intersection) / len(union)

            if jaccard >= 0.3:
                # Determine edge type based on store combinations
                stores = {n1.store, n2.store}
                if "learnings" in stores and "traces" in stores:
                    edge_type = "reinforces"
                elif "rules" in stores or "claude_rules" in stores:
                    edge_type = "reinforces"
                elif "skills" in stores:
                    edge_type = "elaborated_in"
                else:
                    edge_type = "related"

                shared = sorted(intersection)[:3]
                edges.append(Edge(
                    from_id=n1.id,
                    to_id=n2.id,
                    type=edge_type,
                    strength=round(jaccard, 3),
                    evidence=f"Shared topics: {', '.join(shared)}",
                ))

                edge_counts[n1.id] = edge_counts.get(n1.id, 0) + 1
                edge_counts[n2.id] = edge_counts.get(n2.id, 0) + 1

    return edges


# ---------------------------------------------------------------------------
# Validation + Stats
# ---------------------------------------------------------------------------

def validate_index(index: Optional[dict] = None) -> bool:
    """Check for broken edges, orphan nodes, and print health report."""
    if index is None:
        if not OUTPUT_PATH.exists():
            print("ERROR: No index file found. Run a full build first.")
            return False
        index = json.loads(OUTPUT_PATH.read_text())

    node_ids = set(index.get("nodes", {}).keys())
    edges = index.get("edges", [])
    stats = index.get("stats", {})

    broken = 0
    for edge in edges:
        if edge.get("from_id") not in node_ids:
            print(f"  BROKEN: edge from '{edge.get('from_id')}' (not in nodes)")
            broken += 1
        if edge.get("to_id") not in node_ids:
            print(f"  BROKEN: edge to '{edge.get('to_id')}' (not in nodes)")
            broken += 1

    # Count orphan nodes (no edges at all)
    connected = set()
    for edge in edges:
        connected.add(edge.get("from_id"))
        connected.add(edge.get("to_id"))
    orphans = node_ids - connected
    orphan_pct = (len(orphans) / len(node_ids) * 100) if node_ids else 0

    # Edge counts per node
    edge_per_node = Counter()
    for edge in edges:
        edge_per_node[edge.get("from_id")] += 1
        edge_per_node[edge.get("to_id")] += 1

    avg_edges = sum(edge_per_node.values()) / len(edge_per_node) if edge_per_node else 0
    max_edges = max(edge_per_node.values()) if edge_per_node else 0
    heaviest_node = edge_per_node.most_common(1)[0][0] if edge_per_node else "none"

    # Weight check
    weights = [n.get("weight", 1.0) for n in index.get("nodes", {}).values()]
    min_weight = min(weights) if weights else 1.0

    print("\nGraph Health Report")
    print("=" * 40)
    print(f"  Nodes:           {stats.get('total_nodes', len(node_ids))}")
    print(f"  Edges:           {stats.get('total_edges', len(edges))}")
    print(f"  Stores indexed:  {stats.get('stores_indexed', 0)}")
    print(f"  Broken edges:    {broken}")
    print(f"  Orphan nodes:    {len(orphans)} ({orphan_pct:.1f}%)")
    print(f"  Avg edges/node:  {avg_edges:.1f}")
    print(f"  Max edges (node):{max_edges} ({heaviest_node})")
    print(f"  Min weight:      {min_weight}")

    if broken > 0:
        print("\n  FAIL: Broken edges found")
        return False

    # Warnings
    if len(node_ids) < 50:
        print(f"\n  WARN: Low node count ({len(node_ids)})")
    if orphan_pct > 30:
        print(f"\n  WARN: High orphan rate ({orphan_pct:.1f}%)")

    print("\n  PASS: No broken edges")
    return True


def print_stats(index: Optional[dict] = None):
    """Show index statistics breakdown."""
    if index is None:
        if not OUTPUT_PATH.exists():
            print("ERROR: No index file found. Run a full build first.")
            return
        index = json.loads(OUTPUT_PATH.read_text())

    stats = index.get("stats", {})

    print("\nUnified Knowledge Graph Index Statistics")
    print("=" * 50)
    print(f"  Version:       {index.get('version', '?')}")
    print(f"  Built at:      {index.get('built_at', '?')}")
    print(f"  Total nodes:   {stats.get('total_nodes', 0)}")
    print(f"  Total edges:   {stats.get('total_edges', 0)}")
    print(f"  Stores:        {stats.get('stores_indexed', 0)}")

    nodes_by_store = stats.get("nodes_by_store", {})
    if nodes_by_store:
        print("\n  Nodes by store:")
        for store, count in sorted(nodes_by_store.items(), key=lambda x: -x[1]):
            print(f"    {store:20s}  {count}")

    edges_by_type = stats.get("edges_by_type", {})
    if edges_by_type:
        print("\n  Edges by type:")
        for etype, count in sorted(edges_by_type.items(), key=lambda x: -x[1]):
            print(f"    {etype:25s}  {count}")

    # Cross-store edge count
    edges = index.get("edges", [])
    nodes = index.get("nodes", {})
    cross_store = 0
    for e in edges:
        n1 = nodes.get(e.get("from_id", ""), {})
        n2 = nodes.get(e.get("to_id", ""), {})
        if n1.get("store") != n2.get("store"):
            cross_store += 1
    print(f"\n  Cross-store edges: {cross_store}")

    # File size
    if OUTPUT_PATH.exists():
        size_kb = OUTPUT_PATH.stat().st_size / 1024
        print(f"  Index file size:   {size_kb:.1f} KB")


# ---------------------------------------------------------------------------
# Incremental Update Helpers
# ---------------------------------------------------------------------------

# Map file paths to store scanner + store names
_FILE_STORE_MAP = [
    ("shared/learnings/", "learnings", {"learnings"}),
    ("shared/decision-traces/traces.json", "traces", {"traces"}),
    ("shared/decision-traces/rules.json", "rules", {"rules"}),
    (".claude/rules/", "rules", {"claude_rules"}),
    (".claude/skills/", "skills", {"skills"}),
    ("shared/knowledge-base/", "docs", {"knowledge_base"}),
    ("shared/reference/", "docs", {"reference"}),
    ("docs/knowledge-graph/experiences.json", "experiences", {"experiences"}),
    # CAF paths (relative to CAF_ROOT, detected via special prefix)
    ("caf://knowledge/domains/", "caf_docs", {"caf_reference"}),
    ("caf://knowledge/domains/dbt-pipelines/decision-traces/", "caf_traces", {"caf_traces"}),
    # dbt-enterprise docs (detected via special prefix)
    ("ent://docs/business_context/", "enterprise_docs", {"enterprise_docs"}),
    ("ent://docs/models_documentation/", "enterprise_docs", {"enterprise_docs"}),
    # Handoffs
    ("handoffs/", "handoffs", {"handoffs"}),
]

SCANNER_MAP = {
    "learnings": LearningsScanner,
    "traces": TracesScanner,
    "rules": RulesScanner,
    "experiences": ExperiencesScanner,
    "skills": SkillsScanner,
    "docs": DocsScanner,
    "caf_docs": CAFDocsScanner,
    "caf_traces": CAFTracesScanner,
    "enterprise_docs": EnterpriseDocsScanner,
    "handoffs": HandoffsScanner,
}


def _detect_store(filepath: str) -> Optional[tuple[str, set[str]]]:
    """Given a relative file path, return (scanner_key, store_names) or None."""
    for prefix, scanner_key, store_names in _FILE_STORE_MAP:
        if prefix.startswith("caf://"):
            # CAF paths: check if file is relative to CAF_ROOT
            caf_prefix = prefix[len("caf://"):]
            try:
                caf_rel = str(Path(filepath).resolve().relative_to(CAF_ROOT))
            except ValueError:
                caf_rel = filepath
            if caf_rel.startswith(caf_prefix):
                return scanner_key, store_names
        elif prefix.startswith("ent://"):
            # dbt-enterprise paths: check if file is relative to DBT_ENTERPRISE_ROOT
            ent_prefix = prefix[len("ent://"):]
            try:
                ent_rel = str(Path(filepath).resolve().relative_to(DBT_ENTERPRISE_ROOT))
            except ValueError:
                ent_rel = filepath
            if ent_rel.startswith(ent_prefix):
                return scanner_key, store_names
        elif filepath.startswith(prefix) or filepath == prefix.rstrip("/"):
            return scanner_key, store_names
    return None


def _load_index() -> dict:
    """Load existing index or return empty structure."""
    if OUTPUT_PATH.exists():
        try:
            return json.loads(OUTPUT_PATH.read_text())
        except Exception:
            pass
    return {"version": "1.0", "nodes": {}, "edges": [], "stats": {}}


def _write_index(index: dict):
    """Write index to disk."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(index, indent=2, default=str))


def incremental_update(changed_files: list[str]) -> dict:
    """Re-index only files that changed. Remove old nodes from those files,
    re-scan the affected stores, and re-infer edges for new nodes."""

    index = _load_index()
    if not index.get("nodes"):
        print("No existing index. Running full rebuild instead.")
        return build_index()

    # Determine which stores are affected
    affected_scanners: dict[str, set[str]] = {}  # scanner_key -> store_names
    affected_file_paths: set[str] = set()

    for filepath in changed_files:
        # Normalize to relative path from project root
        try:
            rel = str(Path(filepath).resolve().relative_to(PROJECT_ROOT))
        except ValueError:
            rel = filepath  # Already relative

        result = _detect_store(rel)
        if result:
            scanner_key, store_names = result
            if scanner_key not in affected_scanners:
                affected_scanners[scanner_key] = set()
            affected_scanners[scanner_key] |= store_names
            affected_file_paths.add(rel)
        else:
            print(f"  Skip (not a knowledge file): {filepath}")

    if not affected_scanners:
        print("No knowledge files changed. Index unchanged.")
        return index

    # For each affected store:
    #   1. Remove nodes whose store_path matches any changed file
    #   2. Remove edges that reference removed nodes
    #   3. Re-scan the entire scanner (scanners are designed for full store scan)
    #   4. Add new nodes + intra-store edges

    # Step 1: Remove nodes from affected store names
    removed_stores: set[str] = set()
    for store_names in affected_scanners.values():
        removed_stores |= store_names

    # Keep nodes not in affected stores
    kept_nodes: dict[str, dict] = {}
    removed_ids: set[str] = set()
    for nid, ndata in index.get("nodes", {}).items():
        if ndata.get("store") in removed_stores:
            removed_ids.add(nid)
        else:
            kept_nodes[nid] = ndata

    print(f"  Removing {len(removed_ids)} nodes from stores: {', '.join(sorted(removed_stores))}")

    # Step 2: Remove edges touching removed nodes + all cross-store edges
    # (cross-store edges will be re-inferred)
    kept_edges = []
    for edata in index.get("edges", []):
        from_id = edata.get("from_id", "")
        to_id = edata.get("to_id", "")
        if from_id in removed_ids or to_id in removed_ids:
            continue
        # Also remove cross-store edges (they'll be re-inferred)
        from_store = kept_nodes.get(from_id, {}).get("store")
        to_store = kept_nodes.get(to_id, {}).get("store")
        if from_store and to_store and from_store != to_store:
            # Keep cross-store edges between unaffected stores
            kept_edges.append(edata)
        elif from_store and to_store:
            kept_edges.append(edata)

    # Step 3: Re-scan affected stores
    new_nodes: dict[str, Node] = {}
    new_intra_edges: list[Edge] = []

    for scanner_key in affected_scanners:
        scanner_cls = SCANNER_MAP.get(scanner_key)
        if not scanner_cls:
            continue
        scanner = scanner_cls()
        try:
            nodes, edges = scanner.scan()
            for node in nodes:
                new_nodes[node.id] = node
            new_intra_edges.extend(edges)
            print(f"  Re-scanned {scanner_key}: {len(nodes)} nodes, {len(edges)} edges")
        except Exception as e:
            print(f"  Re-scan {scanner_key}: ERROR - {e}")

    # Step 4: Merge kept + new nodes
    all_nodes: dict[str, Node] = {}
    # Convert kept_nodes dicts back to Node objects for edge inference
    for nid, ndata in kept_nodes.items():
        all_nodes[nid] = Node(
            id=nid,
            store=ndata.get("store", ""),
            store_path=ndata.get("store_path", ""),
            type=ndata.get("type", ""),
            title=ndata.get("title", ""),
            topics=ndata.get("topics", []),
            summary=ndata.get("summary", ""),
            anchor=ndata.get("anchor", ""),
            weight=ndata.get("weight", 1.0),
            created=ndata.get("created", ""),
            last_accessed=ndata.get("last_accessed"),
            domain=ndata.get("domain", "agent"),
            repo=ndata.get("repo", "dbt-agent"),
            detail_level=ndata.get("detail_level", "L1"),
            l0_summary=ndata.get("l0_summary", ""),
            valid_from=ndata.get("valid_from"),
            valid_until=ndata.get("valid_until"),
            promoted_to_caf=ndata.get("promoted_to_caf", False),
            evidence_log=ndata.get("evidence_log", []),
        )
    all_nodes.update(new_nodes)

    # Step 5: Re-infer cross-store edges (for all nodes, since new nodes need connections)
    print("  Re-inferring cross-store edges...")
    cross_edges = infer_cross_store_edges(all_nodes)
    print(f"  Cross-store: {len(cross_edges)} edges")

    # Combine all edges
    all_edges: list[Edge] = []
    # Convert kept_edges dicts to Edge objects
    for edata in kept_edges:
        from_store = all_nodes.get(edata.get("from_id", ""), Node(id="", store="", store_path="", type="", title="", topics=[], summary="", anchor="")).store
        to_store = all_nodes.get(edata.get("to_id", ""), Node(id="", store="", store_path="", type="", title="", topics=[], summary="", anchor="")).store
        # Only keep intra-store edges from kept nodes (cross-store were re-inferred)
        if from_store == to_store:
            all_edges.append(Edge(
                from_id=edata["from_id"],
                to_id=edata["to_id"],
                type=edata["type"],
                strength=edata.get("strength", 1.0),
                evidence=edata.get("evidence", ""),
            ))
    all_edges.extend(new_intra_edges)
    all_edges.extend(cross_edges)

    # Deduplicate
    seen = set()
    unique_edges = []
    for edge in all_edges:
        key = (edge.from_id, edge.to_id, edge.type)
        if key not in seen:
            seen.add(key)
            unique_edges.append(edge)

    # Rebuild stats
    stores = set(n.store for n in all_nodes.values())
    edge_type_counts = Counter(e.type for e in unique_edges)

    updated_index = {
        "version": "1.0",
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "stats": {
            "total_nodes": len(all_nodes),
            "total_edges": len(unique_edges),
            "stores_indexed": len(stores),
            "nodes_by_store": {
                store: sum(1 for n in all_nodes.values() if n.store == store)
                for store in sorted(stores)
            },
            "edges_by_type": dict(edge_type_counts.most_common()),
        },
        "nodes": {
            nid: {k: v for k, v in asdict(node).items() if v is not None or k in ("last_accessed", "valid_from", "valid_until")}
            for nid, node in sorted(all_nodes.items())
        },
        "edges": [
            {
                "from_id": e.from_id,
                "to_id": e.to_id,
                "type": e.type,
                "strength": e.strength,
                "evidence": e.evidence,
            }
            for e in unique_edges
        ],
    }

    _write_index(updated_index)
    print(f"\nIncremental update: {len(all_nodes)} nodes, {len(unique_edges)} edges -> {OUTPUT_PATH}")
    return updated_index


# ---------------------------------------------------------------------------
# Main Builder
# ---------------------------------------------------------------------------

def build_index(store_filter: Optional[str] = None) -> dict:
    """Main entry point. Scan all stores, infer edges, write index."""

    scanner_map = {
        "learnings": LearningsScanner,
        "traces": TracesScanner,
        "rules": RulesScanner,
        "experiences": ExperiencesScanner,
        "skills": SkillsScanner,
        "docs": DocsScanner,
        "caf_docs": CAFDocsScanner,
        "caf_traces": CAFTracesScanner,
        "caf_tools": ToolsScanner,
        "enterprise_docs": EnterpriseDocsScanner,
        "handoffs": HandoffsScanner,
    }

    if store_filter:
        if store_filter not in scanner_map:
            print(f"Unknown store: {store_filter}")
            print(f"Available: {', '.join(scanner_map.keys())}")
            sys.exit(1)
        scanners = [scanner_map[store_filter]()]
    else:
        scanners = [cls() for cls in scanner_map.values()]

    all_nodes: dict[str, Node] = {}
    all_edges: list[Edge] = []

    # If rebuilding a single store, load existing index and remove that store's nodes
    if store_filter and OUTPUT_PATH.exists():
        try:
            existing = json.loads(OUTPUT_PATH.read_text())
            # Map store filter to store names
            store_names = {
                "learnings": {"learnings"},
                "traces": {"traces"},
                "rules": {"rules", "claude_rules"},
                "experiences": {"experiences"},
                "skills": {"skills"},
                "docs": {"knowledge_base", "reference"},
                "caf_docs": {"caf_reference"},
                "caf_traces": {"caf_traces"},
                "enterprise_docs": {"enterprise_docs"},
                "handoffs": {"handoffs"},
            }
            remove_stores = store_names.get(store_filter, {store_filter})

            for nid, ndata in existing.get("nodes", {}).items():
                if ndata.get("store") not in remove_stores:
                    # Reconstruct Node from dict
                    node = Node(
                        id=nid,
                        store=ndata.get("store", ""),
                        store_path=ndata.get("store_path", ""),
                        type=ndata.get("type", ""),
                        title=ndata.get("title", ""),
                        topics=ndata.get("topics", []),
                        summary=ndata.get("summary", ""),
                        anchor=ndata.get("anchor", ""),
                        weight=ndata.get("weight", 1.0),
                        created=ndata.get("created", ""),
                        last_accessed=ndata.get("last_accessed"),
                    )
                    all_nodes[nid] = node

            # Keep edges where neither end is in removed stores
            for edata in existing.get("edges", []):
                from_store = existing["nodes"].get(edata.get("from_id"), {}).get("store")
                to_store = existing["nodes"].get(edata.get("to_id"), {}).get("store")
                if from_store not in remove_stores and to_store not in remove_stores:
                    all_edges.append(Edge(
                        from_id=edata["from_id"],
                        to_id=edata["to_id"],
                        type=edata["type"],
                        strength=edata.get("strength", 1.0),
                        evidence=edata.get("evidence", ""),
                    ))
        except Exception as e:
            print(f"Warning: Could not load existing index: {e}")

    for scanner in scanners:
        scanner_name = scanner.__class__.__name__
        try:
            nodes, edges = scanner.scan()
            for node in nodes:
                all_nodes[node.id] = node
            all_edges.extend(edges)
            print(f"  {scanner_name}: {len(nodes)} nodes, {len(edges)} edges")
        except Exception as e:
            print(f"  {scanner_name}: ERROR - {e}")

    # Cross-store edge inference
    print("  Inferring cross-store edges...")
    cross_edges = infer_cross_store_edges(all_nodes)
    all_edges.extend(cross_edges)
    print(f"  Cross-store: {len(cross_edges)} edges")

    # Deduplicate edges (same from+to+type)
    seen = set()
    unique_edges = []
    for edge in all_edges:
        key = (edge.from_id, edge.to_id, edge.type)
        if key not in seen:
            seen.add(key)
            unique_edges.append(edge)

    # Compute stats
    stores = set(n.store for n in all_nodes.values())
    edge_type_counts = Counter(e.type for e in unique_edges)

    index = {
        "version": "1.0",
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "stats": {
            "total_nodes": len(all_nodes),
            "total_edges": len(unique_edges),
            "stores_indexed": len(stores),
            "nodes_by_store": {
                store: sum(1 for n in all_nodes.values() if n.store == store)
                for store in sorted(stores)
            },
            "edges_by_type": dict(edge_type_counts.most_common()),
        },
        "nodes": {
            nid: {k: v for k, v in asdict(node).items() if v is not None or k in ("last_accessed", "valid_from", "valid_until")}
            for nid, node in sorted(all_nodes.items())
        },
        "edges": [
            {
                "from_id": e.from_id,
                "to_id": e.to_id,
                "type": e.type,
                "strength": e.strength,
                "evidence": e.evidence,
            }
            for e in unique_edges
        ],
    }

    # Write
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(index, indent=2, default=str))

    print(f"\nBuilt index: {len(all_nodes)} nodes, {len(unique_edges)} edges -> {OUTPUT_PATH}")
    return index


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    args = sys.argv[1:]

    if "--stats" in args:
        print_stats()
    elif "--validate" in args:
        ok = validate_index()
        sys.exit(0 if ok else 1)
    elif "--incremental" in args:
        idx = args.index("--incremental")
        changed = [a for a in args[idx + 1:] if not a.startswith("--")]
        if not changed:
            print("Usage: --incremental <file1> [file2] ...")
            print("Example: --incremental shared/learnings/cross-cutting/dbt-qa.yaml .claude/rules/new-rule.md")
            sys.exit(1)
        index = incremental_update(changed)
        print_stats(index)
        print()
        validate_index(index)
    elif "--store" in args:
        idx = args.index("--store")
        if idx + 1 < len(args):
            store = args[idx + 1]
            index = build_index(store_filter=store)
            print_stats(index)
        else:
            print("Usage: --store <store_name>")
            sys.exit(1)
    else:
        index = build_index()
        print_stats(index)
        print()
        validate_index(index)
