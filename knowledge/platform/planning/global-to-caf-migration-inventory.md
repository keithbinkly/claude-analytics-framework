# Global To CAF Migration Inventory

Purpose: classify analytics-related assets currently living in `~/.claude/` and decide whether they should move into `claude-analytics-framework`.

## Decision Rule
Move an asset into CAF if it is:
- analytics-team specific
- part of the shared analytics operating model
- used across CAF, `dbt-enterprise`, and `data-centered`
- something another analytics teammate would need in order to work effectively

Keep an asset in `~/.claude/` if it is:
- truly universal across unrelated domains
- personal rather than team/platform level
- not meaningfully part of the analytics operating system

## Current Recommendation

### Migrate Into CAF First
These are high-confidence analytics-platform assets.

#### Global manifest and residency logic
- `~/.claude/AGENTS.md`
  - Reason: currently acts as a cross-repo source of truth for analytics agents and residency
  - Target in CAF: `.claude/manifests/`
  - Disposition: mirror into CAF first, then deprecate global-first usage for analytics only when CAF-owned sections are stable

#### Global analytics agent manifests and commands
- `~/.claude/commands/system-architect.md`
- `~/.claude/commands/designer.md`
- `~/.claude/AGENTS.md` analytics-specific sections

Reason:
- these are analytics-platform operating assets and should become CAF-owned

Disposition:
- copy or mirror into CAF

#### Global analytics agent memory
- `~/.claude/agent-memory/system-architect/`
- `~/.claude/agent-memory/designer/`

Reason:
- these are global agents invoked across multiple repos
- the clean residency rule already says global agents keep memory in `~/.claude/agent-memory/`

Disposition:
- keep global
- reference from CAF manifests and commands

#### Global commands that behave like analytics-platform commands
- `~/.claude/commands/system-architect.md`
- `~/.claude/commands/designer.md`
- `~/.claude/commands/load.md`
- `~/.claude/commands/save.md`
- `~/.claude/commands/project-recap.md`
- `~/.claude/commands/plan-review.md`
- `~/.claude/commands/diff-review.md`
- `~/.claude/commands/visual-explainer.md`
- `~/.claude/commands/generate-web-diagram.md`
- `~/.claude/commands/agentic-image-gen.md`
- `~/.claude/commands/docs.md`

Reason:
- these are part of the shared analytics workflow or the analytics storytelling/design layer
- they should be visible from CAF without depending on home-directory state

Target in CAF:
- `.claude/commands/`

Disposition:
- copy into CAF, then either leave compatibility stubs in `~/.claude/commands/` or later retire the global copy if desired

### Candidate For Selective Migration
These need a case-by-case decision.

#### Global skills with strong analytics relevance
Possible move candidates:
- research/documentation skills used as part of the analytics platform operating model
- design/visualization skills that are core to `data-centered` + CAF
- workflow and coordination skills that underpin cross-repo analytics work

Likely candidate categories:
- analytics storytelling and design
- cross-repo coordination
- platform planning and workstream management
- workspace discovery and help for analytics users

Disposition:
- inventory by usage frequency and ownership
- move analytics-core skills first
- leave generic engineering skills global only if they remain broadly useful outside analytics

### Keep Global For Now
These look like universal or personal/global assets unless later proven otherwise.

#### Personal/global agents and memory
- `~/.claude/agent-memory/life-admin/`
- `/life-admin`

Reason:
- not part of the analytics operating system

Disposition:
- keep in `~/.claude/`

#### Broadly generic skill library
Examples:
- general debugging
- general code search/router tools
- math stack
- generic sub-agent helpers
- broadly applicable hook/skill development helpers

Reason:
- these are not analytics-platform specific by default

Disposition:
- keep global unless the analytics platform needs a curated local copy or wrapper

## Migration Order
1. Move the manifest logic into CAF
2. Move `system-architect` and `designer` command logic into CAF
3. Move analytics-oriented `load` and `save` workflow logic into CAF
4. Review global skills and classify them into:
   - move to CAF
   - wrap in CAF
   - keep global

## Cutover Strategy
For each migrated asset:
1. Create the CAF-owned version
2. Update CAF manifests and bootstrap docs
3. Update nested repo bootstraps to point to CAF
4. Optionally leave a short compatibility stub in `~/.claude/` that points to CAF
5. Stop treating the global copy as canonical for analytics work

Ownership note:
- default to mirror/copy semantics first
- only re-home or retire the original after explicit confirmation

## Definition Of Done
This migration is complete when:
- analytics agents can bootstrap from CAF without needing `~/.claude` command/manifests as a primary source of truth
- CAF owns the shared analytics operating model
- global agent memory remains cleanly global
- `~/.claude` is reduced to universal or personal tooling plus canonical memory for truly global agents
