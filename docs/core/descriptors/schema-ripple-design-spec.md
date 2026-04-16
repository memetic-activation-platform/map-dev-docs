# Schema Ripple Design Spec

## Purpose

This spec defines the process by which changes to the authoritative MAP core schema ripple through affected components.

The goal is to make schema authority operational, not merely conceptual.

A core-schema change should:

- update everything derivable from schema
- identify downstream components affected by the change
- fail fast when required schema-derived artifacts are stale or inconsistent
- highlight the areas where manual implementation is still required

## Authoritative Source

The authoritative source of truth for the MAP Core Schema is:

- `host/import_files/map-schema/core-schema/`

All schema-ripple behavior described here begins from changes in those core-schema definitions.

## Goals

- increase velocity for schema evolution
- reduce human error after schema changes
- make schema impacts visible and reviewable
- distinguish clearly between generated work and manual follow-up
- enforce consistency in CI

## Non-Goals

- full automatic implementation of all behavior
- replacing design review for ontology changes
- solving schema migration/versioning in this phase
- generating semantic logic that is not derivable from schema

## Core Principle

Schema changes should flow through a predictable ripple process.

That process may be carried out by:

- Codex-driven workflows
- scripts
- dedicated tooling
- or a combination of the above

During the current exploratory phase, Codex-driven artifact derivation is preferred where it provides lower maintenance cost and greater flexibility than bespoke generators.

The process should answer four questions every time the schema changes:

1. What can be regenerated automatically?
2. What runtime or implementation surfaces are affected?
3. What manual work is now required?
4. Has all required follow-up been completed?

## Ripple Process

### Step 1: Detect schema change

Any change under `host/import_files/map-schema/core-schema/` is treated as a schema-impacting change.

### Step 2: Validate and normalize schema

The ripple process should:

- parse all core-schema JSON files
- verify cross-file references
- verify ontology invariants that are enforceable at schema-definition time
- produce a normalized understanding of the schema suitable for artifact derivation and impact analysis

Examples of invariants to validate here:

- every referenced descriptor exists
- every descriptor has valid `DescribedBy` / `Extends` structure
- `Extends` max cardinality is 1 where required
- no inherited property-name redeclarations
- no inherited relationship-name redeclarations
- no cycles in `Extends`

### Step 3: Derive or update schema-dependent artifacts

Everything derivable directly from schema should be regenerated or updated as part of the ripple process.

In the current phase, this derivation may be performed by Codex rather than by dedicated generators. The important requirement is that the derivation procedure is explicit, reviewable, and reproducible.

Examples:

- descriptor accessor methods
- generated descriptor wrapper support code
- typed property and relationship name enums/constants
- generated command/dance descriptor stubs where schema supports them
- schema manifests or lookup tables
- structural validation scaffolding
- test fixtures or schema snapshots where useful

### Step 4: Compute impact manifest

After derivation/update work, the ripple process should produce a machine-readable impact manifest describing what changed and what still needs human attention.

The impact manifest should include:

- changed schema definitions
- affected type kinds
- affected descriptor wrappers
- affected generated files
- affected commands
- affected dances
- affected validation modules
- affected query/operator modules
- required manual implementation checkpoints

### Step 5: Enforce in CI

CI should fail if:

- schema validation fails
- generated artifacts are stale
- generated code is missing for schema-defined elements
- removed schema elements are still referenced in code
- required manual implementation checkpoints are unresolved

## Schema-Derived Outputs

The following should be treated as first-class generated outputs when possible:

- descriptor accessors from `InstanceProperties` and `InstanceRelationships`
- descriptor capability inventories
- command descriptor scaffolding once `CommandDescriptor` is in schema
- operator metadata scaffolding once operator definitions are in `ValueType`
- lookup tables for descriptor resolution
- documentation summaries derived from schema

Schema-derived outputs should be:

- deterministic
- reproducible
- clearly separated from handwritten code
- easy to diff in review

In the current exploratory phase, “reproducible” means another Codex-guided run following the same documented ripple procedure should be able to reach the same artifact updates with the same schema inputs.

## Manual Implementation Checkpoints

Some impacts cannot be fully implemented from schema alone.

These should be reported explicitly as manual checkpoints rather than silently left to memory.

Examples:

- semantic validation logic for value types
- operator execution semantics
- command handler bodies
- dance protocol handlers
- transaction-sensitive inverse population logic
- query execution semantics
- tests for newly introduced behavior

The ripple process should never imply that missing manual logic is acceptable just because generation succeeded.

## Impact Manifest

The ripple process should emit a machine-readable manifest, for example JSON, describing the ripple effects of the schema change.

Suggested contents:

- `changed_schema_items`
- `generated_files_updated`
- `generated_files_expected`
- `affected_descriptor_kinds`
- `affected_runtime_modules`
- `affected_commands`
- `affected_queries`
- `manual_checkpoints`
- `recommended_tests`

Each manual checkpoint should include:

- identifier
- reason
- affected module or file area
- severity or blocking status

## Manual Checkpoint Resolution

A schema change is not complete until all blocking manual checkpoints are resolved.

This can be enforced by:

- checking in a resolved impact manifest
- checking in explicit completion markers
- or failing CI until the checkpoint list is empty

The process should prefer explicitness over convenience.

## CI Enforcement

CI should include checks for:

- schema parsing and normalization
- cross-reference validity
- ontology invariant validation
- generated artifact freshness
- impact manifest generation
- unresolved blocking manual checkpoints

Optional but recommended:

- targeted test selection based on affected descriptor kinds
- documentation regeneration checks
- schema snapshot diff review

## Suggested Execution Modes

The process should support one or more of the following execution modes:

- Codex-driven schema ripple workflow
- lightweight scripts for narrow repetitive tasks
- dedicated tooling where repetition and artifact stability justify the maintenance cost

Near-term preference:

- use Codex to inspect schema deltas, update schema-derived artifacts, and surface manual checkpoints
- avoid prematurely building and maintaining bespoke generators while artifact shapes are still exploratory

The exact implementation language is not specified here. What matters is that the process is deterministic, reviewable, and CI-friendly.

## Codex Workflow Expectations

If Codex is used as the primary ripple executor, the process must still be explicit.

At minimum, the documented Codex workflow should specify:

- which schema files to inspect
- which artifact classes must be reviewed or updated
- which outputs are expected to be schema-derived vs manually implemented
- which manual checkpoints must be surfaced
- which tests or verification steps must be run

Codex-driven derivation should not become implicit tribal knowledge.

## Relationship to Descriptor Specs

This spec complements, but does not replace:

- `docs/descriptors-design-spec.md`
- `docs/descriptors-behavior-design-spec.md`

Those specs define what descriptor behavior and structure should be.

This spec defines how schema changes should propagate through the codebase and delivery process.

## Initial Priority Targets

The first ripple workflow should focus on the highest-leverage areas:

- generated descriptor accessors
- schema invariant validation
- impact manifest generation
- CI enforcement for stale generated code

After that, expand to:

- `CommandDescriptor` scaffolding
- `ValueType` operator-definition scaffolding
- query impact reporting

## Summary

The schema ripple process should make core-schema authority actionable.

When the schema changes, MAP should reliably:

- validate the schema
- update derivable artifacts
- identify affected components
- surface manual work explicitly
- enforce completion in CI where practical

That process will let schema enhancements move faster while reducing the chance of silent drift between ontology, generated code, and handwritten implementation.
