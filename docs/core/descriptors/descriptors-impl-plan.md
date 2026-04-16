# MAP Descriptor Architecture Implementation Plan

## Status

Proposed

This plan translates the current descriptor and schema ripple design specs into a concrete, incremental implementation roadmap using small, composable PRs.

---

## Guiding Principles

- Schema is authoritative for all structural concerns
- Descriptors are the semantic anchor of behavior
- Commands are execution plumbing, not semantics
- Behavior must be descriptor-bound (no freestanding semantics)
- Implementation proceeds incrementally with working system at every step
- Each PR introduces one coherent concept
- Schema extensions precede dependent implementation
- Prefer Codex-driven schema artifact derivation over bespoke generators while schema-dependent artifacts are still exploratory
- Only harden repeated Codex workflows into dedicated tooling where repetition and stability justify the maintenance cost

---

## Bootstrap Framing

There is an intentional bootstrap phase in this plan.

MAP's intended end state is descriptor-driven validation. Structural and semantic invariants should ultimately be enforced through descriptor-defined rules, not through a parallel collection of permanent special-case validators.

That creates an early implementation catch-22:

- the descriptor layer is needed in order to perform descriptor-driven validation
- but the schema must remain valid while that layer is being built

During the bootstrap phase:

- schema correctness is maintained primarily through disciplined authoring, review, fixtures, and targeted tests
- required invariants are treated as design constraints immediately
- automated enforcement of those invariants is introduced only once the descriptor layer can enforce them descriptor-first
- schema-derived artifact updates may be performed through documented Codex workflows rather than permanent toolchains

Therefore this plan deliberately avoids introducing a permanent "special validator" for ontology rules such as `Extends` cardinality. Early phases should not be read as implying that full automated schema validation already exists.

In addition:

- the existing Holon Data Loader flow is accepted as the current loading substrate
- this plan does not begin by refactoring the loader pipeline
- this plan also does not begin by introducing new schema-specific tooling as a prerequisite

The first implementation focus is the runtime descriptor layer itself.

---

## Phase Overview

| Phase | Focus |
|------|------|
| 1 | Descriptor runtime abstractions and shared access patterns |
| 2 | Schema-backed descriptor accessors |
| 3 | ValueDescriptor behavior (validation + operators runtime) |
| 4 | CommandDescriptor (minimal schema anchor) |
| 5 | Descriptor-bound command routing (static dispatch) |
| 6 | Dispatch redistribution (descriptor-local) |
| 7 | TypeScript interface realignment |
| 8 | Schema ripple workflow (expanded) |
| 9 | Schema extensions (operators, command enrichment) |

---

## Phase 1 — Descriptor Runtime Abstractions and Shared Access Patterns

### Goal
Establish the runtime descriptor layer as thin typed wrappers over descriptor holons.

### Changes
- Implement descriptor wrappers:
    - HolonDescriptor
    - PropertyDescriptor
    - ValueDescriptor
    - RelationshipDescriptor
- Implement shared runtime abstractions:
    - Descriptor trait
    - TypeHeader
    - inheritance traversal helpers
    - ergonomic descriptor lookup entrypoints where appropriate
- Keep wrappers thin over HolonReference-backed descriptor holons
- No semantic behavior changes yet

### Acceptance Criteria
- Runtime descriptor wrappers exist as thin views over descriptor holons
- Shared abstractions such as Descriptor and TypeHeader are implemented
- Inheritance traversal helpers support flattened lookup behavior
- No semantic behavior beyond structural runtime access is introduced in this phase

---

## Phase 2 — Schema-Backed Descriptor Accessors

### Goal
Expose the current core schema's structural descriptor surface through schema-backed runtime accessors.

### Changes
- Using the authoritative core schema, derive the current descriptor accessor surface for:
    - shared descriptor/header accessors
    - HolonDescriptor
    - PropertyDescriptor
    - RelationshipDescriptor
    - declared/inverse relationship descriptor accessors where schema-backed
- Integrate those accessors into the runtime descriptor layer
- Keep the derivation process Codex-driven and reviewable rather than requiring a permanent generator in this phase
- Preserve strict "no accessor without schema backing" rules

### Acceptance Criteria
- The current schema-backed descriptor accessor surface is available through the runtime descriptor layer
- No unsupported accessor is introduced without schema backing
- Known current-schema deficiencies are handled explicitly rather than implicitly patched in code
- Accessor behavior is validated by tests against the current authoritative core schema

---

## Phase 3 — ValueDescriptor Behavior (Runtime)

### Goal
Anchor the first real semantic behavior in descriptors via ValueDescriptor.

### Changes
- Implement on ValueDescriptor:
    - is_valid()
    - supports_operator()
    - apply_operator()
- Implement operators as static Rust logic
- Keep operator semantics descriptor-bound
- Do not add schema operator metadata yet

### Constraints
- No global operator registry
- Operator set must remain compatible with future schema representation

### Acceptance Criteria
- Value validation runs through ValueDescriptor
- Query layer can use ValueDescriptor operators
- No operator semantics outside ValueDescriptor

---

## Phase 4 — Introduce CommandDescriptor (Minimal Schema Anchor)

### Goal
Anchor commands in schema early.

### Changes

#### Schema
Add:
- CommandDescriptor type
- Minimal properties:
    - command_name
- Canonical relationship:
    - `(TypeDescriptor)-[AffordsCommand]->(CommandDescriptor)`
- Command identity:
    - `command_name` is unique within the affording descriptor
- Routing identity:
    - command routing resolves by `(descriptor, command_name)`
- Affordance direction:
    - the primary affordance lives on the descriptor side
- Cardinality:
    - a descriptor may afford multiple commands
    - a command may be afforded by multiple descriptors only if that remains semantically intentional and unambiguous in routing

#### Runtime
- No change to execution yet
- No parameter modeling yet

### Acceptance Criteria
- Commands exist as descriptor-linked schema elements
- Canonical affordance relationship and routing identity are defined clearly enough to support later routing work
- No change in command execution behavior

---

## Phase 5 — Descriptor-Bound Command Routing (Static)

### Goal
Bind commands to descriptor semantics.

### Changes
- Map existing commands → CommandDescriptor instances
- Introduce routing layer:
    - (descriptor, command) → Rust implementation
- Keep static dispatch (match/registry)

### Acceptance Criteria
- All commands have descriptor ownership
- No freestanding commands remain
- Existing functionality unchanged

---

## Phase 6 — Dispatch Redistribution

### Goal
Move away from centralized dispatch.

### Changes
- Replace central dispatch table with:
    - descriptor-local dispatch modules
- Example:
    - ValueDescriptor handles value commands
    - HolonDescriptor handles holon commands

### Acceptance Criteria
- No central “god dispatcher”
- Dispatch organized by descriptor type
- Static execution remains

---

## Phase 7 — TypeScript Interface Realignment

### Goal
Align client API with descriptor model.

### Changes
- Introduce TS descriptor clients:
    - TypeDescriptorClient
    - PropertyDescriptorClient
    - ValueTypeClient
- Wrap existing commands through descriptor-oriented API
- Gradually deprecate function-group-based API

### Acceptance Criteria
- TS API mirrors descriptor structure
- No breaking changes required initially

---

## Phase 8 — Schema Ripple Workflow (Expanded)

### Goal
Make schema authority operational.

### Changes
Expand the schema ripple workflow so it can reliably:

- validate schema
- normalize schema
- update schema-derived artifacts
- compute impact manifest

Schema-derived artifacts include:
- descriptor accessors
- property/relationship enums
- schema lookup tables

Impact manifest includes:
- changed schema items
- affected descriptors
- affected commands
- manual checkpoints

### CI Enforcement
Fail if:
- schema invalid
- schema-derived artifacts stale
- unresolved blocking checkpoints

### Acceptance Criteria
- Schema change triggers a reliable ripple workflow
- Impact manifest produced
- CI enforces consistency
- Bootstrap-era checks may still rely on authoring discipline plus targeted tests where descriptor-driven validation is not yet available
- Dedicated tooling is optional in this phase; Codex-driven execution is acceptable if the workflow is documented and reproducible

---

## Phase 9 — Schema Extensions

### Goal
Move runtime behavior into schema over time.

### Changes

#### Operators
- Extend ValueType schema to define:
    - supported operators
- Replace runtime-only operator definitions

#### Commands
- Extend CommandDescriptor:
    - input/output modeling
    - richer metadata

#### Optional
- introduce descriptor-afforded dances in schema

### Acceptance Criteria
- Operators derive from schema
- Command structure is schema-defined
- Runtime logic aligns with schema

---

## Cross-Cutting Invariants and Enforcement

### Design Invariants

These invariants apply throughout the plan, even before automated descriptor-driven enforcement exists:

- max one Extends
- no Extends cycles
- no duplicate inherited property names
- no duplicate inherited relationship names
- every holon has exactly one DescribedBy

### Bootstrap-Phase Enforcement

Before descriptor-driven validation is available broadly, these invariants are maintained through:

- careful schema authoring
- code review
- focused fixtures
- targeted tests

No permanent special-case validator should be introduced for these rules solely to bridge the bootstrap phase.

### Descriptor-Driven Enforcement

Once the descriptor layer is sufficiently implemented, these invariants should be enforced through descriptor-driven validation at commit/runtime boundaries rather than by ad hoc validators.

### Runtime Safety Checks

- fail on invalid descriptor graphs
- fail on invalid operator usage
- fail on missing descriptor linkage

---

## Manual Implementation Checkpoints

Must be surfaced via the schema ripple workflow:

- value validation logic
- operator semantics
- command handlers
- query execution logic
- tests for new behaviors

CI must fail if blocking checkpoints remain unresolved.

---

## Key Design Constraints Maintained

- descriptors are thin wrappers over HolonReference
- no duplicated ontology state
- schema is single source of truth
- behavior is descriptor-bound
- static dispatch in this phase
- no TypeScript-side semantic duplication

---

## Summary

This plan incrementally transforms MAP into a descriptor-driven system by:

1. establishing the runtime descriptor layer
2. integrating schema-backed structural accessors
3. binding first semantic behavior to ValueDescriptor
4. anchoring commands in schema
5. redistributing dispatch to descriptor level
6. expanding the schema ripple workflow around descriptor-driven development

The result is a system where:

- ontology defines structure and behavior
- schema changes propagate deterministically
- runtime stays aligned with the model
- future dynamic dispatch can be introduced without redesign
