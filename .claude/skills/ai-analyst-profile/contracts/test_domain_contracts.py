"""
Domain Contract Tests for AI Analyst Profile

Validates:
1. Domain pack structure and required fields
2. Metrics/dimensions referenced exist in semantic layer
3. Routing keywords map to valid domains
4. Question templates are answerable with available metrics
5. Guardrails reference valid fields

Run with: pytest .claude/skills/kb-ai-analyst-profile/contracts/
"""

import os
import yaml
import pytest
from pathlib import Path
from typing import Any


# --- Fixtures ---

@pytest.fixture(scope="module")
def base_path() -> Path:
    """Return the base path for the AI analyst profile skill."""
    # Handle both running from repo root and from contracts dir
    current = Path(__file__).parent
    if current.name == "contracts":
        return current.parent
    return current


@pytest.fixture(scope="module")
def operations_domain(base_path: Path) -> dict[str, Any]:
    """Load the operations domain pack."""
    domain_path = base_path / "domain_packs" / "operations.yaml"
    with open(domain_path) as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def routing_config(base_path: Path) -> dict[str, Any]:
    """Load the routing keywords configuration."""
    routing_path = base_path / "routing" / "keywords.yaml"
    with open(routing_path) as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def domain_contracts(base_path: Path) -> dict[str, Any]:
    """Load the domain contracts definition."""
    contracts_path = base_path / "contracts" / "domain_contracts.yaml"
    with open(contracts_path) as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def semantic_layer_metrics() -> set[str]:
    """
    Return the set of metrics available in the semantic layer.

    In a full implementation, this would query the MCP server.
    For now, we maintain a static list based on actual semantic layer.
    """
    return {
        # Volume metrics
        "spend_total_auth_attempts",
        "spend_total_approvals",
        "spend_total_declines",
        "spend_total_auth_attempt_amount",
        "spend_total_approval_amount",
        "spend_total_decline_amount",
        # Rate metrics
        "spend_approval_rate_by_count",
        "spend_decline_rate_by_count",
        "spend_approval_rate_by_amount",
        "spend_decline_rate_by_amount",
        # Channel metrics
        "spend_cp_approval_rate",
        "spend_cnp_approval_rate",
        "spend_contactless_approval_rate",
        "spend_chip_approval_rate",
        "spend_manual_entry_approval_rate",
        "spend_approval_rate_gap_cp_vs_cnp",
        # Cardholder metrics
        "spend_pct_cardholders_affected_by_declines",
        "spend_declines_per_affected_cardholder",
        "spend_distinct_cardholders",
        "spend_distinct_cardholders_with_declines",
        # Transaction size metrics
        "spend_avg_attempt_transaction_size",
        "spend_avg_approval_transaction_size",
        "spend_avg_decline_transaction_size",
        # Channel-specific counts
        "spend_cp_attempt_cnt",
        "spend_cp_approve_cnt",
        "spend_cp_decline_cnt",
        "spend_cnp_attempt_cnt",
        "spend_cnp_approve_cnt",
        "spend_cnp_decline_cnt",
        "spend_contactless_attempt_cnt",
        "spend_contactless_approve_cnt",
        "spend_chip_attempt_cnt",
        "spend_chip_approve_cnt",
        "spend_manual_entry_attempt_cnt",
        "spend_manual_entry_approve_cnt",
        # eWallet metrics
        "spend_ewallet_total_amt",
        "spend_ewallet_total_cnt",
        "spend_ewallet_share_by_amount",
        "spend_ewallet_share_by_count",
        "spend_apple_pay_amt",
        "spend_apple_pay_cnt",
        "spend_apple_pay_share",
        "spend_google_pay_amt",
        "spend_google_pay_cnt",
        "spend_samsung_pay_amt",
        "spend_samsung_pay_cnt",
        # Activity metrics
        "spend_active_90d_amt",
        "spend_active_90d_cnt",
        "spend_active_90d_share_by_amount",
        "spend_active_90d_share_by_count",
        # Derived metrics
        "spend_cp_share_of_volume",
        "spend_contactless_share_of_cp",
        # Cardholder grain
        "spend_cardholder_total_attempts",
        "spend_cardholder_total_approvals",
        "spend_cardholder_total_declines",
        "spend_cardholder_decline_rate",
    }


@pytest.fixture(scope="module")
def semantic_layer_dimensions() -> set[str]:
    """
    Return the set of dimensions available in the semantic layer.

    In a full implementation, this would query the MCP server.
    """
    return {
        "metric_time",
        "merchant_auth_event__product_stack",
        "merchant_auth_event__pos_entry_mode",
        "merchant_auth_event__card_present",
        "merchant_auth_event__responsecode",
        "merchant_auth_event__mcc_category",
        "merchant_auth_event__mcc_desc",
        "merchant_auth_event__merchant",
        # Cardholder grain dimensions
        "cardholder_auth_event__product_stack",
        "cardholder_auth_event__responsecode",
        "cardholder_auth_event__merchant",
    }


# --- Domain Pack Validation Tests ---

class TestOperationsDomainPackStructure:
    """Validate that the operations domain pack has all required fields."""

    def test_operations_domain_has_required_fields(self, operations_domain: dict):
        """Domain pack has: domain, description, semantic_layer, question_templates, guardrails."""
        required_fields = [
            "domain",
            "description",
            "semantic_layer",
            "question_templates",
            "guardrails",
        ]
        for field in required_fields:
            assert field in operations_domain, f"Missing required field: {field}"

    def test_operations_domain_name_matches(self, operations_domain: dict):
        """Domain field should be 'operations'."""
        assert operations_domain["domain"] == "operations"

    def test_operations_has_version(self, operations_domain: dict):
        """Domain pack should have a version."""
        assert "version" in operations_domain
        assert operations_domain["version"] is not None

    def test_semantic_layer_has_metrics_and_dimensions(self, operations_domain: dict):
        """Semantic layer section must have metrics and dimensions."""
        semantic_layer = operations_domain["semantic_layer"]
        assert "metrics" in semantic_layer, "Missing metrics in semantic_layer"
        assert "dimensions" in semantic_layer, "Missing dimensions in semantic_layer"
        assert len(semantic_layer["metrics"]) > 0, "No metrics defined"
        assert len(semantic_layer["dimensions"]) > 0, "No dimensions defined"

    def test_guardrails_has_required_sections(self, operations_domain: dict):
        """Guardrails should have contracts, assumptions, and rules."""
        guardrails = operations_domain["guardrails"]
        assert "contracts" in guardrails, "Missing contracts in guardrails"
        assert "assumptions" in guardrails, "Missing assumptions in guardrails"
        assert "rules" in guardrails, "Missing rules in guardrails"


class TestOperationsMetricsExist:
    """Validate that metrics referenced in domain pack exist in semantic layer."""

    def test_operations_metrics_exist_in_semantic_layer(
        self, operations_domain: dict, semantic_layer_metrics: set[str]
    ):
        """All metrics referenced in domain pack exist in actual semantic layer."""
        domain_metrics = [m["name"] for m in operations_domain["semantic_layer"]["metrics"]]
        missing_metrics = []

        for metric in domain_metrics:
            if metric not in semantic_layer_metrics:
                missing_metrics.append(metric)

        assert not missing_metrics, (
            f"Metrics in domain pack not found in semantic layer: {missing_metrics}"
        )

    def test_contract_required_metrics_exist(
        self, domain_contracts: dict, semantic_layer_metrics: set[str]
    ):
        """All metrics required by contract exist in semantic layer."""
        required_metrics = domain_contracts["contracts"]["operations"]["required_metrics"]
        missing_metrics = []

        for metric in required_metrics:
            if metric not in semantic_layer_metrics:
                missing_metrics.append(metric)

        assert not missing_metrics, (
            f"Contract required metrics not in semantic layer: {missing_metrics}"
        )


class TestOperationsDimensionsExist:
    """Validate that dimensions referenced in domain pack exist in semantic layer."""

    def test_operations_dimensions_exist_in_semantic_layer(
        self, operations_domain: dict, semantic_layer_dimensions: set[str]
    ):
        """All dimensions referenced in domain pack exist in actual semantic layer."""
        domain_dimensions = [d["name"] for d in operations_domain["semantic_layer"]["dimensions"]]
        missing_dimensions = []

        for dimension in domain_dimensions:
            if dimension not in semantic_layer_dimensions:
                missing_dimensions.append(dimension)

        assert not missing_dimensions, (
            f"Dimensions in domain pack not found in semantic layer: {missing_dimensions}"
        )

    def test_contract_required_dimensions_exist(
        self, domain_contracts: dict, semantic_layer_dimensions: set[str]
    ):
        """All dimensions required by contract exist in semantic layer."""
        required_dimensions = domain_contracts["contracts"]["operations"]["required_dimensions"]
        missing_dimensions = []

        for dimension in required_dimensions:
            if dimension not in semantic_layer_dimensions:
                missing_dimensions.append(dimension)

        assert not missing_dimensions, (
            f"Contract required dimensions not in semantic layer: {missing_dimensions}"
        )


# --- Routing Validation Tests ---

class TestRoutingKeywords:
    """Validate routing configuration."""

    def test_routing_keywords_map_to_valid_domains(
        self, routing_config: dict, base_path: Path
    ):
        """Every domain in keywords.yaml has a corresponding domain pack."""
        domains = routing_config.get("domains", {})

        for domain_name, domain_config in domains.items():
            # Skip placeholders
            if domain_config.get("status") == "placeholder":
                continue

            domain_pack_path = domain_config.get("domain_pack", "")
            full_path = base_path / domain_pack_path

            assert full_path.exists(), (
                f"Domain '{domain_name}' references non-existent pack: {domain_pack_path}"
            )

    def test_active_domains_have_keywords(self, routing_config: dict):
        """Active domains must have at least one keyword."""
        domains = routing_config.get("domains", {})

        for domain_name, domain_config in domains.items():
            if domain_config.get("status") == "placeholder":
                continue

            keywords = domain_config.get("keywords", [])
            assert len(keywords) > 0, (
                f"Active domain '{domain_name}' has no keywords"
            )

    def test_no_keyword_conflicts_in_active_domains(self, routing_config: dict):
        """No keyword appears in multiple active domains without documentation."""
        domains = routing_config.get("domains", {})
        keyword_to_domains: dict[str, list[str]] = {}

        for domain_name, domain_config in domains.items():
            if domain_config.get("status") == "placeholder":
                continue

            for keyword in domain_config.get("keywords", []):
                keyword_lower = keyword.lower()
                if keyword_lower not in keyword_to_domains:
                    keyword_to_domains[keyword_lower] = []
                keyword_to_domains[keyword_lower].append(domain_name)

        conflicts = {k: v for k, v in keyword_to_domains.items() if len(v) > 1}

        assert not conflicts, (
            f"Keywords appear in multiple active domains: {conflicts}"
        )

    def test_routing_has_conflict_resolution(self, routing_config: dict):
        """Routing config should have conflict resolution strategy."""
        assert "conflict_resolution" in routing_config
        assert "strategy" in routing_config["conflict_resolution"]


# --- Question Answering Contract Tests ---

class TestQuestionsAreAnswerable:
    """Validate that question templates can be answered with available metrics/dimensions."""

    def test_operations_questions_are_answerable(
        self,
        operations_domain: dict,
        semantic_layer_metrics: set[str],
        semantic_layer_dimensions: set[str],
    ):
        """Each question template can be answered with available metrics/dimensions."""
        question_templates = operations_domain.get("question_templates", [])
        domain_metrics = {m["name"] for m in operations_domain["semantic_layer"]["metrics"]}
        domain_dimensions = {d["name"] for d in operations_domain["semantic_layer"]["dimensions"]}
        # Also include aliases
        for d in operations_domain["semantic_layer"]["dimensions"]:
            if "alias" in d:
                domain_dimensions.add(d["alias"])

        issues = []

        for template in question_templates:
            pattern = template.get("pattern", "")
            template_metrics = template.get("metrics", [])
            template_dimensions = template.get("dimensions", [])

            # Check metrics
            for metric in template_metrics:
                if metric not in domain_metrics:
                    issues.append(
                        f"Template '{pattern}' references metric '{metric}' "
                        f"not in domain pack"
                    )
                if metric not in semantic_layer_metrics:
                    issues.append(
                        f"Template '{pattern}' references metric '{metric}' "
                        f"not in semantic layer"
                    )

            # Check dimensions
            for dimension in template_dimensions:
                # Check both full name and alias
                if dimension not in domain_dimensions:
                    issues.append(
                        f"Template '{pattern}' references dimension '{dimension}' "
                        f"not in domain pack"
                    )

        assert not issues, "Question template issues:\n" + "\n".join(issues)

    def test_contract_sample_questions_are_answerable(
        self,
        domain_contracts: dict,
        semantic_layer_metrics: set[str],
    ):
        """Sample questions in contracts reference available metrics."""
        sample_questions = domain_contracts["contracts"]["operations"]["sample_questions"]
        issues = []

        for sq in sample_questions:
            question = sq["question"]
            expected_metrics = sq.get("expected_metrics", [])

            for metric in expected_metrics:
                if metric not in semantic_layer_metrics:
                    issues.append(
                        f"Sample question '{question}' expects metric '{metric}' "
                        f"not in semantic layer"
                    )

        assert not issues, "Sample question issues:\n" + "\n".join(issues)


# --- Guardrail Contract Tests ---

class TestGuardrailsAreEnforceable:
    """Validate that guardrail rules reference valid fields."""

    def test_guardrails_reference_valid_metrics(
        self, operations_domain: dict, semantic_layer_metrics: set[str]
    ):
        """Guardrail metric expectations reference valid metrics."""
        guardrails = operations_domain.get("guardrails", {})
        contracts = guardrails.get("contracts", {})
        metric_expectations = contracts.get("metric_expectations", {})

        invalid_metrics = []
        for metric_name in metric_expectations.keys():
            if metric_name not in semantic_layer_metrics:
                invalid_metrics.append(metric_name)

        assert not invalid_metrics, (
            f"Guardrail metric expectations reference invalid metrics: {invalid_metrics}"
        )

    def test_contract_guardrail_rules_reference_valid_metrics(
        self, domain_contracts: dict, semantic_layer_metrics: set[str]
    ):
        """Contract guardrail rules reference valid metrics."""
        guardrail_rules = domain_contracts["contracts"]["operations"]["guardrail_rules"]
        invalid_metrics = []

        for rule in guardrail_rules:
            metric = rule.get("metric")
            if metric and metric not in semantic_layer_metrics:
                invalid_metrics.append(f"{rule['rule']}: {metric}")

        assert not invalid_metrics, (
            f"Guardrail rules reference invalid metrics: {invalid_metrics}"
        )

    def test_guardrails_have_valid_ranges(self, operations_domain: dict):
        """Guardrail expected ranges are valid (min <= max)."""
        guardrails = operations_domain.get("guardrails", {})
        contracts = guardrails.get("contracts", {})
        metric_expectations = contracts.get("metric_expectations", {})

        invalid_ranges = []
        for metric_name, expectations in metric_expectations.items():
            expected_range = expectations.get("expected_range", [])
            if len(expected_range) == 2:
                if expected_range[0] > expected_range[1]:
                    invalid_ranges.append(
                        f"{metric_name}: {expected_range} (min > max)"
                    )

        assert not invalid_ranges, (
            f"Invalid guardrail ranges: {invalid_ranges}"
        )


# --- Cross-Validation Tests ---

class TestDomainPackConsistency:
    """Cross-validate domain pack with contracts and routing."""

    def test_domain_metrics_cover_contract_requirements(
        self, operations_domain: dict, domain_contracts: dict
    ):
        """Domain pack metrics should cover all contract required metrics."""
        domain_metrics = {m["name"] for m in operations_domain["semantic_layer"]["metrics"]}
        required_metrics = set(
            domain_contracts["contracts"]["operations"]["required_metrics"]
        )

        missing = required_metrics - domain_metrics
        assert not missing, (
            f"Domain pack missing contract-required metrics: {missing}"
        )

    def test_domain_dimensions_cover_contract_requirements(
        self, operations_domain: dict, domain_contracts: dict
    ):
        """Domain pack dimensions should cover all contract required dimensions."""
        domain_dimensions = {d["name"] for d in operations_domain["semantic_layer"]["dimensions"]}
        required_dimensions = set(
            domain_contracts["contracts"]["operations"]["required_dimensions"]
        )

        missing = required_dimensions - domain_dimensions
        assert not missing, (
            f"Domain pack missing contract-required dimensions: {missing}"
        )

    def test_routing_keywords_align_with_domain_routing(
        self, operations_domain: dict, routing_config: dict
    ):
        """Domain pack routing keywords should be subset of routing config keywords."""
        domain_keywords = set(
            k.lower() for k in operations_domain.get("routing", {}).get("keywords", [])
        )
        routing_keywords = set(
            k.lower() for k in routing_config["domains"]["operations"].get("keywords", [])
        )

        # Domain keywords should align with (be subset of or equal to) routing keywords
        # This is a soft check - domain can have its own additional context
        if domain_keywords and routing_keywords:
            overlap = domain_keywords & routing_keywords
            assert len(overlap) > 0, (
                "Domain routing keywords have no overlap with central routing config"
            )


# --- Integration Test (Optional - requires MCP) ---

class TestSemanticLayerIntegration:
    """
    Integration tests that verify against actual semantic layer.

    These tests are marked as optional and require MCP connection.
    Run with: pytest -m integration
    """

    @pytest.mark.skip(reason="Requires MCP connection - run manually with MCP enabled")
    def test_live_metrics_match_fixture(self):
        """
        Verify fixture metrics match actual semantic layer.

        Would use mcp__dbt-mcp__list_metrics to get actual metrics.
        """
        pass

    @pytest.mark.skip(reason="Requires MCP connection - run manually with MCP enabled")
    def test_live_dimensions_match_fixture(self):
        """
        Verify fixture dimensions match actual semantic layer.

        Would use mcp__dbt-mcp__get_dimensions to get actual dimensions.
        """
        pass
