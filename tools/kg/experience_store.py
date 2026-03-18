#!/usr/bin/env python3
"""
Spark-inspired Experience Store for Agent Learning.

Enables agents to learn from each other by capturing successful patterns
and sharing them across sessions.

Key concept: Migration agent solves problem → QA agent knows instantly

Architecture:
1. Experience capture - Log successful patterns from agent sessions
2. Pattern extraction - Cluster similar solutions
3. Cross-agent retrieval - Query other agents' learnings

Usage:
    from tools.kg.experience_store import ExperienceStore

    store = ExperienceStore()

    # Log a successful pattern
    store.log_experience(
        agent="migration",
        problem="Handle deletes in incremental model",
        solution="Use MERGE with delete+insert pattern",
        context={"model": "int_transactions", "technique": "merge"},
        outcome="success"
    )

    # Retrieve relevant experiences
    experiences = store.find_relevant_experiences(
        "How do I handle deletes?",
        max_results=5
    )
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, field, asdict
from collections import defaultdict
import hashlib


@dataclass
class Experience:
    """A captured experience from an agent session."""
    id: str
    agent: str  # Which agent logged this (migration, qa, discovery, etc.)
    problem: str  # What problem was being solved
    solution: str  # What worked
    context: Dict  # Additional context (model name, technique, etc.)
    outcome: str  # success, partial, failed
    timestamp: str
    tags: List[str] = field(default_factory=list)
    usefulness_score: float = 0.0  # Updated based on retrieval feedback


@dataclass
class ExperienceCluster:
    """Group of similar experiences."""
    pattern_name: str
    experiences: List[str]  # experience IDs
    summary: str
    frequency: int


class ExperienceStore:
    """
    Store and retrieve agent experiences for cross-agent learning.

    Implements Spark's "continuous experiential loop":
    - Capture interactions as structured traces
    - Merge into collective knowledge space
    - Retrieve contextualized recommendations
    """

    def __init__(self, store_path: Path = None):
        """Initialize experience store."""
        if store_path is None:
            store_path = Path(__file__).parent.parent.parent / "docs" / "knowledge-graph" / "experiences.json"

        self.store_path = store_path
        self.experiences: Dict[str, Experience] = {}
        self.clusters: List[ExperienceCluster] = []

        self._load()

    @staticmethod
    def _normalize_exp_data(exp_data: Dict) -> Dict:
        """Normalize auto-extracted experience format to Experience dataclass fields.

        Auto-extracted experiences have: id, session_id, type, context,
        description, evidence, tags, source, timestamp.
        Experience dataclass expects: id, agent, problem, solution, context,
        outcome, timestamp, tags, usefulness_score.
        """
        # If it already has 'agent' and 'problem', it's the native format
        if 'agent' in exp_data and 'problem' in exp_data:
            # Strip any extra keys the dataclass doesn't accept
            valid_keys = {'id', 'agent', 'problem', 'solution', 'context',
                          'outcome', 'timestamp', 'tags', 'usefulness_score'}
            return {k: v for k, v in exp_data.items() if k in valid_keys}

        # Map auto-extracted format → Experience format
        return {
            'id': exp_data.get('id', ''),
            'agent': exp_data.get('source', 'auto-extract'),
            'problem': exp_data.get('description', ''),
            'solution': exp_data.get('evidence', ''),
            'context': exp_data.get('context', {}),
            'outcome': exp_data.get('type', 'task_unit'),
            'timestamp': exp_data.get('timestamp', ''),
            'tags': exp_data.get('tags', []),
            'usefulness_score': exp_data.get('usefulness_score', 0.5),
        }

    def _load(self):
        """Load experiences from disk."""
        if self.store_path.exists():
            try:
                data = json.loads(self.store_path.read_text())
                for exp_data in data.get('experiences', []):
                    normalized = self._normalize_exp_data(exp_data)
                    exp = Experience(**normalized)
                    self.experiences[exp.id] = exp
                # Load clusters if present
                for cluster_data in data.get('clusters', []):
                    self.clusters.append(ExperienceCluster(**cluster_data))
            except Exception as e:
                print(f"Warning: Could not load experiences: {e}")

    def _save(self):
        """Persist experiences to disk."""
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            'experiences': [asdict(exp) for exp in self.experiences.values()],
            'clusters': [asdict(c) for c in self.clusters],
            'metadata': {
                'last_updated': datetime.now().isoformat(),
                'total_experiences': len(self.experiences),
                'total_clusters': len(self.clusters)
            }
        }
        self.store_path.write_text(json.dumps(data, indent=2))

    def _generate_id(self, problem: str, solution: str) -> str:
        """Generate unique ID for an experience."""
        content = f"{problem}:{solution}"
        return hashlib.sha256(content.encode()).hexdigest()[:12]

    def _extract_tags(self, problem: str, solution: str, context: Dict) -> List[str]:
        """Auto-extract tags from experience content."""
        text = f"{problem} {solution} {json.dumps(context)}".lower()

        tag_patterns = {
            'incremental': r'\bincremental\b',
            'merge': r'\bmerge\b',
            'delete': r'\bdelete\b',
            'qa': r'\bqa\b|\bvalidat',
            'migration': r'\bmigrat',
            'performance': r'\bperform|\boptimiz|\bslow\b',
            'semantic-layer': r'\bsemantic|\bmetric|\bdimension',
            'testing': r'\btest\b',
            'error': r'\berror|\bfail|\bbug\b',
            'architecture': r'\barchitect|\bpattern|\bdesign',
        }

        tags = []
        for tag, pattern in tag_patterns.items():
            if re.search(pattern, text):
                tags.append(tag)

        return tags

    def log_experience(
        self,
        agent: str,
        problem: str,
        solution: str,
        context: Dict = None,
        outcome: str = "success",
        tags: List[str] = None
    ) -> Experience:
        """
        Log a new experience from an agent session.

        Args:
            agent: Which agent logged this (migration, qa, discovery)
            problem: What problem was being solved
            solution: What worked (or didn't)
            context: Additional context (model name, technique, etc.)
            outcome: success, partial, or failed
            tags: Optional manual tags (auto-extracted if not provided)

        Returns:
            The created Experience object
        """
        context = context or {}

        # Generate ID and auto-extract tags
        exp_id = self._generate_id(problem, solution)
        auto_tags = self._extract_tags(problem, solution, context)
        all_tags = list(set((tags or []) + auto_tags))

        # Check for duplicate
        if exp_id in self.experiences:
            # Update existing experience's usefulness score
            existing = self.experiences[exp_id]
            existing.usefulness_score += 0.1  # Boost for repeated success
            self._save()
            return existing

        # Create new experience
        exp = Experience(
            id=exp_id,
            agent=agent,
            problem=problem,
            solution=solution,
            context=context,
            outcome=outcome,
            timestamp=datetime.now().isoformat(),
            tags=all_tags,
            usefulness_score=1.0 if outcome == "success" else 0.5
        )

        self.experiences[exp_id] = exp
        self._save()

        return exp

    def find_relevant_experiences(
        self,
        query: str,
        agent_filter: str = None,
        max_results: int = 5,
        min_score: float = 0.05
    ) -> List[Dict]:
        """
        Find experiences relevant to a query.

        Uses simple keyword matching + tag overlap for scoring.
        Cross-agent retrieval: if agent_filter is None, searches all agents.

        Args:
            query: What the agent is trying to solve
            agent_filter: Optional filter to specific agent's experiences
            max_results: Maximum experiences to return
            min_score: Minimum relevance score threshold

        Returns:
            List of relevant experiences with scores
        """
        query_words = set(re.findall(r'\b\w{4,}\b', query.lower()))
        query_tags = self._extract_tags(query, "", {})

        scored = []

        for exp in self.experiences.values():
            # Filter by agent if specified
            if agent_filter and exp.agent != agent_filter:
                continue

            # Only return successful experiences by default
            if exp.outcome == "failed":
                continue

            # Score by word overlap
            problem_words = set(re.findall(r'\b\w{4,}\b', exp.problem.lower()))
            solution_words = set(re.findall(r'\b\w{4,}\b', exp.solution.lower()))
            all_words = problem_words | solution_words

            word_overlap = len(query_words & all_words)
            word_score = word_overlap / max(len(query_words), 1)

            # Score by tag overlap
            tag_overlap = len(set(query_tags) & set(exp.tags))
            tag_score = tag_overlap / max(len(query_tags), 1) if query_tags else 0

            # Combined score with usefulness boost
            score = (word_score * 0.6 + tag_score * 0.4) * (1 + exp.usefulness_score * 0.1)

            if score >= min_score:
                scored.append({
                    'experience': exp,
                    'score': round(score, 3),
                    'matching_tags': list(set(query_tags) & set(exp.tags))
                })

        # Sort by score and return top results
        scored.sort(key=lambda x: -x['score'])

        return [
            {
                'id': s['experience'].id,
                'agent': s['experience'].agent,
                'problem': s['experience'].problem,
                'solution': s['experience'].solution,
                'tags': s['experience'].tags,
                'score': s['score'],
                'matching_tags': s['matching_tags']
            }
            for s in scored[:max_results]
        ]

    def get_agent_experiences(self, agent: str) -> List[Experience]:
        """Get all experiences from a specific agent."""
        return [exp for exp in self.experiences.values() if exp.agent == agent]

    def get_pattern_summary(self) -> Dict:
        """
        Get summary of learned patterns across all agents.

        Returns:
            Dict with pattern statistics and top patterns by frequency
        """
        # Group by tags
        tag_counts = defaultdict(int)
        agent_counts = defaultdict(int)
        outcome_counts = defaultdict(int)

        for exp in self.experiences.values():
            for tag in exp.tags:
                tag_counts[tag] += 1
            agent_counts[exp.agent] += 1
            outcome_counts[exp.outcome] += 1

        return {
            'total_experiences': len(self.experiences),
            'by_agent': dict(agent_counts),
            'by_outcome': dict(outcome_counts),
            'top_patterns': sorted(tag_counts.items(), key=lambda x: -x[1])[:10],
            'success_rate': outcome_counts.get('success', 0) / max(len(self.experiences), 1)
        }

    def mark_useful(self, experience_id: str, boost: float = 0.2):
        """Mark an experience as useful (was retrieved and helped)."""
        if experience_id in self.experiences:
            self.experiences[experience_id].usefulness_score += boost
            self._save()

    def export_for_training(self) -> List[Dict]:
        """
        Export experiences in format suitable for fine-tuning.

        Returns list of problem/solution pairs for training data.
        """
        return [
            {
                'input': exp.problem,
                'output': exp.solution,
                'context': exp.context,
                'agent': exp.agent,
                'tags': exp.tags
            }
            for exp in self.experiences.values()
            if exp.outcome == "success" and exp.usefulness_score >= 1.0
        ]


# ==================== Integration Functions ====================

def log_agent_success(
    agent: str,
    problem: str,
    solution: str,
    context: Dict = None
) -> Experience:
    """
    Convenience function to log a successful experience.

    Call this when an agent successfully solves a problem.
    """
    store = ExperienceStore()
    return store.log_experience(
        agent=agent,
        problem=problem,
        solution=solution,
        context=context,
        outcome="success"
    )


def get_similar_experiences(query: str, max_results: int = 5) -> List[Dict]:
    """
    Convenience function to find similar experiences.

    Call this when an agent encounters a problem to check if
    another agent has already solved something similar.
    """
    store = ExperienceStore()
    return store.find_relevant_experiences(query, max_results=max_results)


# ==================== CLI ====================

if __name__ == "__main__":
    import sys

    store = ExperienceStore()

    if len(sys.argv) > 1 and sys.argv[1] == "summary":
        summary = store.get_pattern_summary()
        print(f"\n📊 Experience Store Summary")
        print(f"═══════════════════════════")
        print(f"Total experiences: {summary['total_experiences']}")
        print(f"Success rate: {summary['success_rate']:.1%}")
        print(f"\nBy agent: {summary['by_agent']}")
        print(f"By outcome: {summary['by_outcome']}")
        print(f"\nTop patterns: {summary['top_patterns']}")

    elif len(sys.argv) > 2 and sys.argv[1] == "search":
        query = ' '.join(sys.argv[2:])
        results = store.find_relevant_experiences(query)
        print(f"\n🔍 Searching: {query}")
        print(f"═══════════════════════════")
        if results:
            for r in results:
                print(f"\n[{r['score']}] {r['agent']}: {r['problem'][:50]}...")
                print(f"   → {r['solution'][:80]}...")
                print(f"   Tags: {', '.join(r['tags'])}")
        else:
            print("No relevant experiences found.")

    else:
        print("Usage:")
        print("  python -m tools.kg.experience_store summary")
        print("  python -m tools.kg.experience_store search <query>")
