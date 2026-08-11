# Validation Implementation Plan v2.0
## Descriptor-Aware Layered Validation Delivery Sequence

## Purpose

This document defines the implementation plan for the shared MAP validation framework.

The goal is to build a reusable, descriptor-aware validation subsystem that can be consumed by:

- Holon Data Loader
- Nursery validation
- coordinator-side preflight validation
- future runtime validation
- import pipelines
- diagnostics
- developer tooling

This plan owns **Descriptor-Aware Holon Validation**: validation above descriptor-independent PVL
that validates ordinary and descriptor holons against resolved descriptor semantics through the
Holon Validator. Concrete syntaxes such as TDL and MAP JSON may feed this layer through Holon
Loading, but they do not own descriptor-semantic enforcement.

The [Validation Schema Design Spec](validation-schema-design-spec.md) owns the schema package shape
for `ValidationRule` families, `Validations` attachment relationships,
`MetaValidationRule`, the local `Validate` operator, `ValidationImplementation`,
`ValidationRuleSet`, `ValidationResult`, and supporting validation metadata.
The provisional TDL seed corpus lives in
[validation-schema-seed.tdl](validation-schema-seed.tdl) until it is stable enough to promote into
`map-holons/schema-src`.
`VAL0` tracks the near-term documentation and seed precursor work for this reconciliation. It is
not the late implementation ticket for the full holonic validation commitment shape; `VAL8`
remains that implementation milestone and builds on the `VAL0` precursor.

The implementation should introduce a descriptor-aware validation crate under `shared_crates`
separate from the existing PVL-oriented `shared_validation` crate. The existing crate currently
contains descriptor-independent Integrity/PVL rules and should remain guest-safe or be renamed to
make that boundary explicit. Descriptor-Aware Holon Validation belongs in a separate shared crate
that can depend on descriptor-runtime and host/coordinator-facing types without pulling those
dependencies into the Integrity Zome.

The validation framework owns:

- validation rule abstractions
- validation contexts
- layered validator orchestration
- descriptor-aware validation delegation
- stable `ValidationRule` identities and descriptor-authored validation commitments
- shared validation entry points
- validation results
- reusable validation implementations

It deliberately does **not** own:

- descriptor retrieval
- descriptor-kernel effective-product computation
- TypeActivation
- Holochain Integrity callback implementation
- descriptor-independent PVL semantics

Those concerns are addressed by the Descriptor Runtime Platform and PVL implementation plans.

---

# Delivery Principles

- Validation is layered.
- Each validation layer owns a distinct validation context.
- Each validation layer exposes a single validation trait.
- Individual validation rules implement that trait.
- Validation delegates from holons to their bound property, value, and relationship validators.
- Descriptor-driven checks consume kernel-computed effective specifications; they do not implement
  a second inheritance or conformance algorithm.
- Holonic `ValidationRule` identity is part of the runtime validation shape from the start, even
  when execution remains built-in and hard-coded.
- MAP schema loading seeds Core Schema-derived `ValidationRule` commitments as a non-revokable base
  set attached through typekind-compatible `Validations` relationships.
- The Validation Schema source corpus includes TDL definitions for validation-owned types,
  MAP-seeded core `ValidationRule` instances, and their seeded `Validations` attachments.
- Application and extension schemas declare additional instance validation commitments through the
  same typekind-compatible `Validations` relationships.
- Descriptor-Aware Holon Validation code lives in a shared descriptor-aware validation crate, not
  in the PVL/Integrity-focused `shared_validation` crate.
- Validation-owned holon types and relationships belong to a Validation Schema package.
  `Validations` relationships move into MAP Core only if a concrete bootstrap constraint requires a
  narrower Core-owned attachment hook.
- `MetaValidationRule` describes ValidationRule family descriptors. ValidationRule family
  descriptors afford the local `Validate` operator through `AffordsOperator`.
- Rust `ValidationRule` wrappers expose schema-backed metadata from ValidationRule holons and
  implement the initial built-in `Validate` execution path. They do not replace the holons or the
  descriptor-kernel algorithms.
- Rule invocation is initially hard-coded.
- Future descriptor-defined rule dispatch must not require validator redesign.
- Validators operate only on the descriptor supplied by the caller.
- Descriptor lookup is outside the validator framework.

---

# Validation Layers

Validation proceeds through four levels.

## Holon

Responsible for validating an entire holon.

Delegates property validation.

---

## Property

Responsible for validating one property.

Delegates value validation.

---

## Generic Value

Responsible for:

- verifying native value kind
- dispatching to type-specific validation

Delegates to value-type validators.

---

## Type-Specific Value

Responsible for validating descriptor-defined constraints for one native value kind.

Examples include:

- String
- Integer
- Boolean
- Enum
- Bytes

---

# Milestone 1 — Validation Foundation

## Outcome

Shared validation infrastructure exists independently of descriptors or Holochain.

---

## PR 1 — Validation Foundation Types

**Estimate:** 2 pts

### Goal

Introduce the shared validation model.

### Deliverables

- ValidationResult
- ValidationSeverity
- ValidationRule identifiers
- validation helper types

### Dependencies

None

### Exit Criteria

Shared validation types are stable and reusable.

---

## PR 2 — Validation Rule Traits and Contexts

**Estimate:** 3 pts

### Goal

Define the layered validation interfaces.

### Deliverables

Validation traits for:

- HolonValidator
- PropertyValidator
- ValueValidator
- type-specific value validators

Validation contexts for each layer.

### Dependencies

- PR 1

### Exit Criteria

Each validation layer has:

- one validation trait
- one validation context

---

# Milestone 2 — Holon Validation

## Outcome

Descriptor-aware holon validation framework exists.
Exactly-one-`DescribedBy` checking is enforced by a MAP-seeded, non-authorable `ValidationRule`
commitment and is a prerequisite for collecting additional descriptor-authored `Validations`.

---

## PR 3 — Holon Validator Framework

**Estimate:** 3 pts

### Goal

Implement descriptor-aware holon validation.

### Deliverables

Holon validation rules:

- IsDescribedRule
- RequiredPropertiesRule
- NoUndescribedPropertiesRule

Hard-coded rule orchestration.

Delegation to property validation.

### Dependencies

- PR 2

### Exit Criteria

Holon validation delegates correctly.

---

## PR 4 — Property Validator Framework

**Estimate:** 2 pts

### Goal

Implement property validation.

### Deliverables

Property validation rules:

- RequiredPropertyRule

Delegation to generic value validation.

### Dependencies

- PR 3

### Exit Criteria

Property validation delegates correctly.

---

# Milestone 3 — Generic Value Validation

## Outcome

Generic descriptor-aware value validation exists.
BaseValue-vs-ValueType kind matching is enforced by a MAP-seeded, non-authorable
`ValidationRule` commitment attached through `Validations`; application and extension descriptor
authors cannot remove or override it.

---

## PR 5 — Generic Value Validator

**Estimate:** 2 pts

### Goal

Validate native value kind before type-specific validation.

### Deliverables

Validation rule:

- PropertyValueTypeRule

Dispatch to type-specific validators.

### Dependencies

- PR 4

### Exit Criteria

Incorrect native value kinds are rejected.

Correct kinds delegate.

---

# Milestone 4 — Type-Specific Value Validation

## Outcome

Native MAP value types have reusable validation.

---

## PR 6 — String Value Validator

**Estimate:** 2 pts

### Goal

Implement String validation.

### Deliverables

Validation rules:

- LengthValidationRule

### Dependencies

- PR 5

### Exit Criteria

Descriptor-defined string constraints enforced.

---

## PR 7 — Integer, Boolean, Enum, and Bytes Validators

**Estimate:** 3 pts

### Goal

Implement remaining native value validators.

### Deliverables

Validation rules including:

- RangeValidationRule
- LegalVariantRule
- native Boolean validation
- bytes-length validation

### Dependencies

- PR 5

### Exit Criteria

All supported native value kinds validated.

---

# Milestone 5 — Relationship Validation

## Outcome

Relationship validation framework exists.

---

## PR 8 — Relationship Validator Framework

**Estimate:** 3 pts

### Goal

Implement descriptor-aware relationship validation.

### Deliverables

Relationship validation trait.

Relationship validation context.

Initial descriptor-aware relationship rules.

### Dependencies

- PR 3

### Exit Criteria

Relationship validation framework exists.

Higher-order relationship semantics remain deferred.

---

# Milestone 5A — Holonic Validation Commitment Shape

## Outcome

Descriptor-Aware Holon Validation has a runtime shape for validation commitments, even before
dynamic validation execution is implemented.

Core Schema-derived validation rules are addressable by stable `ValidationRule` identities and
seeded by MAP schema loading as a non-revokable base set. Type descriptors can express additional
validation commitments through typekind-compatible `Validations` relationships, and the validator
can report unsupported mandatory rules without silently passing invalid data.

The track also establishes the Validation Schema packaging boundary: `ValidationRule` families,
`ValidationImplementation`, `ValidationRuleSet`, `ValidationResult`, and supporting validation
metadata belong to the Validation Schema. `Validations` attachment relationships also belong to the
Validation Schema unless bootstrapping proves a minimal Core-owned attachment hook is necessary.

---

## PR 8D0 — Validation Schema Bootstrap Spike

**Estimate:** 1 pt

### Goal

Confirm where explicit MAP-seeded `Validations` relationships must live during schema loading and
descriptor validation.

### Deliverables

- Trace the load order and dependency closure for MAP Core, the Validation Schema, MAP-seeded core
  `ValidationRule` holons, MAP-seeded core `Validations` relationships, and an extension schema
  that declares additional validation commitments.
- Identify whether any core descriptor must attach seeded validation rules before the Validation
  Schema is available.
- Keep the default architecture that `Validations` attachment relationships are Validation
  Schema-owned unless a
  concrete bootstrap failure requires a minimal Core-owned hook.
- Document the decision in the Validation Schema spec and update the implementation plan if the
  spike changes the package boundary.

### Dependencies

- Descriptor Runtime Platform load-order assumptions

### Exit Criteria

The implementation track starts with an explicit bootstrap decision rather than an implicit
cross-schema dependency assumption.

---

## PR 8D — ValidationRule Identity Model and Wrapper Dispatch

**Estimate:** 3 pts

### Goal

Package MAP-seeded core validations and extension-authored validations behind family-specific
ValidationRule wrappers that implement `Validate` and dispatch internally by concrete rule holon
identity.

### Deliverables

- Stable authored semantic keys for each built-in validation rule, suitable for wrapper dispatch
  and diagnostics.
- Initial MAP-seeded core rule inventory aligned with the Validation Schema Design Spec, mapping
  each concrete rule key to its family, validator level, and `DS-*` semantic authority where
  applicable.
- Explicit MAP-seeded `Validations` relationship instances that attach every core semantic rule to
  the applicable core descriptor family as loadable schema data.
- Explicit classification of MAP-seeded rules as non-authorable base commitments, including
  exactly-one `DescribedBy` and BaseValue-vs-ValueType matching, so application and extension
  descriptor authors cannot remove, replace, opt into, or opt out of them.
- Rust typed wrappers over `HolonReference`s to `ValidationRule` holons where useful for accessing
  rule metadata, dispatch inputs, and built-in `Validate` execution.
- Static wrapper factory that maps rule-family descriptor identity to the matching Rust wrapper.
- Internal wrapper dispatch by concrete rule holon key for families that support multiple concrete
  rules.
- Rule metadata needed for diagnostics, including validator level, default severity, blocking
  behavior, minimum blocking behavior, and supported validation layers.
- `UnsupportedValidationRule` result handling for mandatory rules whose implementation is not
  available in the current execution profile.

### Dependencies

- PR 8D0
- PRs 1-8
- Descriptor Runtime Platform

### Exit Criteria

Built-in validation can still execute without dynamic dispatch, but every MAP-seeded core check is
wrapped, reported, and reasoned about as a distinct `ValidationRule`.
Mandatory applicable rules without a compatible wrapper-based `Validate` implementation block
commit-oriented validation profiles.

---

## PR 8E — Validation Schema Package Boundary

**Estimate:** 3 pts

### Goal

Define the validation-owned schema package boundary without moving validation execution to dynamic
dispatch.

### Deliverables

- Validation Schema inventory for `ValidationRule` families, `ValidationImplementation`,
  `ValidationRuleSet`, `ValidationResult`, `MetaValidationRule`, `Validate.OperatorType`,
  `Validations` attachment relationships, and supporting metadata.
- Refined TDL definitions, starting from
  [validation-schema-seed.tdl](validation-schema-seed.tdl), for every seeded Validation Schema
  type, rule-family descriptor, MAP-seeded core rule instance, and seeded `Validations`
  relationship attachment.
- Mechanical audit proving the seed corpus contains a distinct seeded `ValidationRule` identity for
  every stable `DS-*` rule ID in the Descriptor-Kernel Semantic Rules index.
- Abstract `ValidationRule.HolonType` root and concrete rule-family descriptors that describe
  concrete validation rule holons.
- Common `Validate.OperatorType` afforded by abstract `ValidationRule.HolonType` and inherited by
  concrete rule-family descriptors through additive operator affordance semantics.
- Narrow operator-affordance decision: ValidationRule family descriptors afford `Validate`, without
  adding `AffordsOperator` broadly to every `MetaHolonType` instance contract.
- `InheritanceMode Additive` baseline for `Validations` attachment relationships.
- Explicit deferral of `ValidationRuleSet` expansion and execution unless an initial schema
  requires it.
- Bootstrap decision for whether `Validations` attachment relationships remain Validation
  Schema-owned or require a minimal Core-owned attachment hook.
- Dependency declaration between MAP Core and the Validation Schema sufficient for descriptor
  authors to attach validation commitments without absorbing the validation object model into Core.
- Documentation of which validation concepts remain transient runtime structures until their
  holon types are needed as durable evidence.

### Dependencies

- PR 8D

### Exit Criteria

Extension authors have a named Validation Schema package to target, and MAP Core does not absorb
the validation object model.

---

## PR 8E1 — Descriptor-Aware Validation Crate Boundary

**Estimate:** 3 pts

### Goal

Create the Rust crate boundary for Descriptor-Aware Holon Validation without mixing it into the
PVL/Integrity-focused `shared_validation` crate.

### Deliverables

- Add a descriptor-aware validation crate under `shared_crates`, with a name that clearly separates
  it from descriptor-independent PVL validation.
- Keep `shared_crates/shared_validation` limited to PVL/integrity-safe validation rules, or rename
  it in a focused follow-up if the current name proves misleading.
- Define initial modules for validation contexts, `ValidationResult`, `ValidationRule` wrapper
  traits, family-specific wrappers, and the static wrapper factory.
- Depend on descriptor-runtime and holon-core crates only from the descriptor-aware validation
  crate, not from Integrity/PVL validation code.
- Add workspace wiring and compile checks proving Integrity Zome crates do not acquire
  descriptor-aware validation dependencies.

### Dependencies

- PR 8D
- PR 8E

### Exit Criteria

Descriptor-Aware Holon Validation has a shared Rust home suitable for coordinator, loader,
Nursery, import, and tooling consumers, while PVL validation remains guest-safe and
descriptor-independent.

---

## PR 8F — Validations Collection and Effective Rule Sets

**Estimate:** 5 pts

### Goal

Collect descriptor-authored validation commitments from type descriptors without changing the
existing descriptor-kernel conformance algorithms.

### Deliverables

- Schema-backed `Validations` relationship handling.
- Effective validation declaration computation over the descriptor's own `Extends` lineage using
  the relationship descriptor's `InheritanceMode`.
- Duplicate, override, and incompatible-rule diagnostics according to the Validation Schema
  declaration.
- Severity and blocking-behavior narrowing from the `ValidationRule` default through
  `Validations` bindings and active validation profiles.
- Layered parameter handling: rule-defined parameter schemas/defaults, binding/profile overrides,
  and descriptor-owned semantic parameters without creating a second source of descriptor truth.
- Validation-profile filtering by layer, operation, and validator level.
- Tests proving that meta-type validation declarations govern descriptor holons themselves and do
  not automatically apply to the runtime instances described by those descriptor holons.

### Dependencies

- PR 8E1
- Descriptor Runtime Platform

### Exit Criteria

Extension schemas can express validation commitments as data by attaching `ValidationRule` holons
to type descriptors through typekind-compatible `Validations` relationships; execution remains
limited to registered individual rule implementations.

---

# Milestone 5B — Schema 2.0 Descriptor-Semantic Rule Coverage

## Outcome

The Holon Validator covers the Schema 2.0 `DS-*` rule families required to validate ordinary and
descriptor holons after loader reference resolution and descriptor-default materialization.

The Descriptor-Kernel Semantic Rules define the meaning of each rule. This milestone wires those
rules into validation scopes, deterministic result accumulation, and consumer-facing diagnostics.
It must not create a second inheritance, effective-contract, endpoint-compatibility, or conformance
algorithm.

---

## PR 8A — Descriptor Structure, Classification, and Contract Rules

**Estimate:** 5 pts

### Goal

Validate descriptor structure and effective contract coherence through the Holon Validator while
delegating semantic products to `HolonDescriptor` and descriptor-kernel helpers.

### Deliverables

- `DS-STRUCT-*` validation for `DescribedBy`, `Extends`, lineage termination, and descriptor root
  invariants.
- `DS-SCHEMA-*` validation for acyclic versioned schema dependencies, direct cross-schema
  dependency declarations, and Core accumulator baselines.
- `DS-KIND-*` validation for explicit Instance TypeKind anchors, abstract anchors, root
  exceptions, and graph-derived describing-category pairing.
- `DS-CONTRACT-*` validation for inherited-member redeclaration, unique member names, well-formed
  effective member definitions, and member-kind compatibility.
- Deterministic diagnostics with descriptor and member provenance.

### Dependencies

- PR 3
- PR 8
- PR 8F
- Descriptor Runtime Platform

### Exit Criteria

Descriptor holons are validated against Schema 2.0 structure, classification, schema dependency,
and effective-contract invariants without hard-coded category tables or duplicated descriptor
algorithms.

---

## PR 8B — Property, Value, Enum, and Key Conformance Rules

**Estimate:** 5 pts

### Goal

Validate property and key conformance for completed staged holons using effective contracts and
type-specific value validators.

### Deliverables

- `DS-CONFORM-*` validation for concrete describing types and member-specific minimum enforcement
  on abstract descriptors.
- `DS-BIND-*` validation that populated property and relationship names bind uniquely in separate
  namespaces to descriptor identities in the effective contract.
- `DS-PROP-*` validation for required property presence, value conformance, and
  additional-property policy.
- `DS-ENUM-*` validation for unique effective enum member names, exact token membership, and token
  non-retroactivity.
- `DS-KEY-*` validation for effective instance-key-rule selection, explicit keylessness, key
  presence, computed key value, and package/dependency-scope uniqueness.
- String-length validation pinned to Unicode 17.0.0 UAX #29 extended grapheme clusters without
  normalization, with shared native and WASM fixtures.

### Dependencies

- PRs 5-7
- PR 8A

### Exit Criteria

Ordinary and descriptor holon properties, values, enums, and keys validate against the effective
contract with deterministic, independently accumulated violations.

---

## PR 8C — Relationship Semantics and Occurrence Rules

**Estimate:** 5 pts

### Goal

Validate descriptor-aware relationship declarations and occurrences while keeping transaction- and
open-graph-dependent checks in Nursery or runtime layers.

### Deliverables

- `DS-REL-*` validation for bijective inverse pairing, mirrored effective endpoints, and
  directional deletion semantic declarations.
- `DS-OCC-*` validation for occurrence grouping by resolved descriptor identity, endpoint
  compatibility, ordering and duplicate policy, and additional-relationship policy.
- `DS-CARD-001` validation where the active validation context supplies the required transaction or
  graph snapshot.
- Explicit deferral of pairwise `Allow`/`Block`/`Cascade` deletion execution semantics until that
  proposed design is settled.

### Dependencies

- PR 8
- PR 8A

### Exit Criteria

Relationship descriptors and relationship occurrences validate through the shared relationship
validator, with cardinality enforced only in validation contexts that can supply the needed graph
view.

---

# Milestone 6 — Descriptor-Orchestrated Validation

## Outcome

Validation execution is driven by effective validation declarations where implementations are
available.

---

## PR 9 — Descriptor-Orchestrated Validation

**Estimate:** 5 pts

### Goal

Move validator orchestration to descriptor-defined rule lists.

### Deliverables

Descriptor-driven validator selection.

Temporary Rust dispatch table.

Hard-coded Rust implementations retained.

### Dependencies

- PRs 3-8F
- Descriptor Runtime Platform

### Exit Criteria

Descriptors determine which validators execute.

Rust remains the execution engine.

---

# Milestone 7 — Shared Validation Entry Points

## Outcome

All consumers invoke one validation surface.

---

## PR 10 — Shared Validation Entry Points

**Estimate:** 2 pts

### Goal

Provide shared validation APIs.

### Deliverables

Shared entry points for:

- create
- update
- delete
- relationship validation

Operation-specific validation contexts.

### Dependencies

- PR 9

### Exit Criteria

All consumers share one validation implementation.

---

# Milestone 8 — Consumer Integration

## Outcome

Validation framework is reused across MAP.

---

## PR 11 — Holon Data Loader Integration

**Estimate:** 3 pts

### Goal

Use shared validation during type loading.

### Deliverables

Descriptor-aware loader validation.

Shared test fixtures.

### Dependencies

- PR 10

### Exit Criteria

Loader uses shared validation.

---

## PR 12 — Nursery Validation Integration

**Estimate:** 3 pts

### Goal

Use shared validation during staged transaction validation.

### Deliverables

Nursery validation integration.

Transaction-aware validation contexts.

### Dependencies

- PR 10
- Transaction infrastructure

### Exit Criteria

Nursery delegates descriptor-aware validation.

---

## PR 13 — Validation Results and Evidence

**Estimate:** 2 pts

### Goal

Provide reusable validation reporting.

### Deliverables

ValidationResult aggregation.

Validation outcome classification.

Evidence model.

### Dependencies

- PR 10

### Exit Criteria

Validation results reusable across consumers.

---

## PR 14 — Validation Diagnostics and Fixtures

**Estimate:** 3 pts

### Goal

Provide regression fixtures and diagnostics.

### Deliverables

Shared fixtures.

Validation diagnostics.

Regression suite.

### Dependencies

- PRs 10–13

### Exit Criteria

Validation behavior is observable and regression-tested.

---

# Relationship to the PVL Implementation Plan

The shared validation framework has no implementation dependency on the PVL implementation plan.

Instead, the descriptor-independent PVL implementation consumes selected components of this framework, including:

- Validation Foundation Types
- Validation Rule Traits and Contexts
- Holon Validator Framework
- Property Validator Framework
- Generic Value Validator
- Type-Specific Value Validators
- Relationship Validator Framework
- Shared Validation Entry Points
- Validation Results
- Validation Diagnostics and Fixtures

Descriptor-independent PVL supplies its own:

- Integrity-safe validation contexts
- resource-limit rules
- native structural validation
- Holochain callback integration
- dependency-budget enforcement

while reusing the common validation infrastructure wherever appropriate.

---

# Critical Path

Precursor: `VAL0` captures the Descriptor-Aware Validation TDL/docs seed reconciliation needed
before the implementation sequence is handed to the validation track.

1. Validation Foundation Types
2. Validation Rule Traits and Contexts
3. Holon Validator Framework
4. Property Validator Framework
5. Generic Value Validator
6. Type-Specific Value Validators
7. Relationship Validator Framework
8. Holonic Validation Commitment Shape
9. Schema 2.0 Descriptor-Semantic Rule Coverage
10. Descriptor-Orchestrated Validation
11. Shared Validation Entry Points
12. Holon Data Loader Integration
13. Nursery Validation Integration
14. Validation Results and Evidence
15. Validation Diagnostics and Fixtures
