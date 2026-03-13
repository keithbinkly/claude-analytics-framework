# ADLC Planning Layer Documentation

**Layer 1: 💡 Planning Phase - Idea Management System**

This folder contains documentation for the ADLC Plan phase workflows:

## Key Workflows
- **Idea Capture**: `./scripts/idea.sh` and `/idea` command
- **Strategic Planning**: `./scripts/roadmap.sh` and `/roadmap` command
- **Business case validation** and impact analysis
- **Stakeholder feedback** integration
- **Long-term maintenance** planning

## Current Planning Docs
- `shared-agent-platform-monorepo-plan.md` - target architecture and phased migration plan for making CAF the shared control plane, while linked repos remain intact and `dbt-agent` stays fully usable as assets are promoted by copy
- `global-to-caf-migration-inventory.md` - classification of analytics-related assets currently living in `~/.claude/`, including the rule that global agent memory stays global
- `dbt-agent-decomposition-inventory.md` - prerequisite inventory framework for classifying what from `dbt-agent` should be promoted, retained, archived, or deduplicated, with explicit ownership labels for copied assets

## Related Manifests
- `.claude/manifests/workspace-manifest.yaml` - canonical workspace topology, precedence rules, and migration policy
- `.claude/manifests/repo-adapters.yaml` - per-repo routing rules, operating constraints, and shared-vs-local asset guidance

## Documentation Coming Soon
- Idea organization and clustering strategies
- Roadmap creation best practices
- Strategic planning templates
- Business case validation frameworks

## ADLC Alignment
This layer implements the **Plan** phase of the Analytics Development Lifecycle:
- Business case validation
- Implementation planning
- Stakeholder feedback loops
- Impact analysis
- Sustainability considerations