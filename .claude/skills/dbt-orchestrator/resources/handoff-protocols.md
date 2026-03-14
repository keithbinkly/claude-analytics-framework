<!--
source_of_truth: caf
mirrored_from: dbt-agent/.claude/skills/dbt-orchestrator/resources/handoff-protocols.md
-->

# Handoff Protocols

CAF-owned handoff contract for pipeline phases.

## Artifact Chain

Each phase should hand off a concrete artifact to the next:

- Phase 1 -> `business-context.md`
- Phase 2 -> `data-discovery-report.md`
- Phase 3 -> `tech-spec.md`
- Phase 4 -> `qa-report.md`

## Starter Templates

CAF-owned starter templates for common handoff artifacts:

- `../resources/plan-template.md`
- `../../dbt-business-context/resources/business-context-template.md`
- `../../dbt-data-discovery/resources/data-discovery-template.md`
- `../../dbt-qa/resources/qa-report-template.md`
- `../../dbt-migration/resources/qa-execution-handoff-template.md`

## Minimum Handoff Requirements

### Phase 1 -> Phase 2

`business-context.md` should include:

- overview
- source information
- key metrics
- acceptance criteria
- domain glossary

### Phase 2 -> Phase 3

`data-discovery-report.md` should include:

- executive summary
- source inventory
- schema validation
- volume trace
- suppression risks

### Phase 3 -> Phase 4

`tech-spec.md` should include:

- model inventory
- transformation rules
- test requirements
- dependencies
- risks and mitigations

### Phase 4 -> Review

`qa-report.md` should include:

- execution summary
- compilation status
- variance analysis
- dbt test results
- recommendation

If the builder agent is handing work to a QA or execution agent, prefer creating a richer execution handoff package as well using:

- `../../dbt-migration/resources/qa-execution-handoff-template.md`

## Validation Rule

Before a gate transition:

- verify the artifact exists
- verify the required sections exist
- verify the artifact is the latest available representation of the phase output

## Storage Rule During Migration

Active artifacts still live in `dbt-agent` while CAF owns the workflow contract.

That means:

- read the handoff contract from CAF
- read and update the live handoff files where the current pipeline state lives

Do not pretend CAF already owns the live artifact store if it does not.
