# MAP Commit Validation Design Specification

> **Status:** Draft
>
> This specification defines MAP's semantic, descriptor-aware Commit Validation: the validation
> that determines whether a complete staged Nursery may be persisted.

---

## 1. Purpose and authority

This specification owns descriptor-aware validation orchestration, subject boundaries, effective
constraint and binding discovery, static dispatch, result aggregation, and the Commit acceptance
decision.

It relies on:

- the [Validation Architecture](validation-arch.md) for MAP's broader validation landscape,
  execution layers, and Runtime Recognition position;
- Core Schema, the type-system constraint model, and the
  [Validation Extension Schema Design Specification](validation-schema-design-spec.md) for
  constraint/rule vocabulary and the one-way extension's implementation/result vocabulary;
- the [Descriptor-Kernel Semantic Rules](../type-system/descriptor-semantics-rules.md) and
  descriptor runtime for effective contracts and descriptor semantics; and
- the [Relationship Occurrence Persistence Design Specification](../transactions/relationship-persistence-design-spec.md)
  for relationship occurrence persistence and cross-Space inverse materialization.

The [Commit Validation Implementation Plan](commit-validation-impl-plan.md)
defines the incremental delivery of this target design.

This specification does not define descriptor-independent PVL, dynamic rule implementation
loading, persisted validation evidence, Runtime Recognition protocol, or cross-Space inverse
reconciliation.

## 2. Design invariants

- Commit is the sole semantic validation boundary for persistence. Every producer stages content in
  a Nursery and reaches this boundary.
- Commit validates the complete Nursery before any persistence write.
- Every Commit runs descriptor-aware validation for every staged holon in that Nursery.
  `ValidationState` is an observation from an earlier or current pass, never a scheduling cache
  that permits Commit to skip a holon.
- A type's effective `Constraints` are configured definitional commitments: accepting an instance
  asserts conformance to every applicable configured invariant.
- A type's effective `ValidationBindings` select the remaining applicable fixed or contextual
  Commit rules; they do not duplicate constraint configuration.
- Constraint holons and validation-rule holons are ordinary staged subjects. When either is staged,
  Commit validates it through its own governing `DescribedBy` type before relying on it as schema
  data for another subject.
- An unbound `ValidationRule` is not applicable. An active mandatory binding without a compatible
  handler produces `UnsupportedValidationRule` and blocks Commit.
- Validation uses ordinary descriptor-runtime effective-member products. It has no binding
  catalog or separate lineage walk.
- Lower-level validators receive only the dependencies needed to validate their own subjects. They
  do not traverse upward to a containing property, holon, or Nursery.
- Validation state and diagnostics are transient `StagedHolon` Commit state. They are not persisted
  content of the holon under assessment.

## 3. Terms and relationship model

`Constraints` is the additive declared relationship from an applicable type to configured
constraint holons. `ValidationBindings` is the additive declared relationship from an applicable
type to compatible non-constraint `ValidationRule` holons.

```text
Applicable Type —Constraints→ Constraint
Applicable Type —ValidationBindings→ ValidationRule
```

The generic relationship contracts are Core-owned. An active occurrence is declared on the actual
applicable type, not generically on `TypeDescriptor`. Its ordinary effective relationship surface
carries inherited commitments. Constraint applicability is validated from the concrete constraint
type's `ApplicableToDescriptorTypes` targets and the constrained descriptor's `Extends` lineage;
malformed attachment remains a descriptor/schema self-conformance invariant.

Descriptor Runtime exposes the generic primitive
`effective_relationship_targets(member)`, which returns the populated effective targets of an
additive relationship member together with their ancestor-before-local provenance. Validation uses
the `effective_constraints()` and `effective_validation_bindings()` convenience wrappers over
that primitive. `available_relationships` may report which relationship members are permitted; it
is not a substitute for populated effective targets.

The **governing descriptor** is the descriptor whose effective commitments govern a particular
validation subject. The **prospective current-Space occurrence collection** is the bounded local
relationship view that Commit evaluates before persistence.

## 4. Validation subjects and dependency direction

Architectural validator contracts use standard MAP reference or wrapper types at subsystem
boundaries. Rust implementations may borrow those wrappers internally, but raw `&Holon` and parent
pointers are not the validation contract. The precise staged-holon wrapper may be selected by the
Commit runtime; it is represented below as `StagedHolonHandle`.

| Validator | Subject | Required inputs | Must not depend on |
|---|---|---|---|
| Holon | `StagedHolonHandle` | `HolonDescriptorReference`, Commit context | property/value parent context |
| Property | one effective property and optional value | `PropertyTypeReference`, property subject | containing holon |
| Value | one populated value | `ValueTypeReference`, value subject | containing property or holon |
| Relationship | one declared occurrence | `DeclaredRelationshipTypeReference`, local occurrence scope | wider source-holon state |
| Multi-hop | bounded occurrence pattern | prospective current-Space view | remote-Space state |

An opaque subject path may accompany a lower-level input for diagnostics. It conveys provenance; it
does not provide an upward navigation dependency.

Each executed configured constraint receives its constraint instance, concrete constraint type,
subject-specific input, and only the execution context it requires. Each executed non-constraint
rule receives its identity, selected binding occurrence, subject-specific input, and only the
execution context required for that rule. A representative conceptual shape is:

```text
RuleInvocation<Subject>
  rule: ValidationRuleReference
  binding: occurrence of ValidationBindings
  subject: Subject
  execution_context: Subject-appropriate context

ConstraintInvocation<Subject>
  constraint: ConstraintReference
  constraint_type: ConstraintTypeReference
  subject: Subject
  execution_context: Subject-appropriate context
```

## 5. Rust validation contracts

The first implementation defines its validation contracts in the WASM-safe `holons_validation`
crate. It consumes standard shared-object and descriptor-runtime wrappers; it must not introduce a
parallel graph model, raw-holon public API, or a validation-specific descriptor cache.

`ValidationResult` is a future schema/evidence holon. It is not the transient Rust result type for
Commit. The Rust contracts below describe only the in-memory decision and diagnostics of one
Commit attempt.

### 5.1 Violation and report types

The shared validation error contract must be structured, serializable, and independent of a
particular validator implementation. It belongs beside `HolonError` and is exposed through a single
top-level error variant, following the same dependency-safe pattern as the PVL violation contract:

```rust
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum HolonError {
    // existing variants
    CommitValidation(CommitValidationViolation),
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CommitValidationViolation {
    pub kind: CommitValidationViolationKind,
    pub rule_key: Option<ValidationRuleKey>,
    pub severity: ValidationSeverity,
    pub blocking: bool,
    pub subject: ValidationSubjectPath,
    pub descriptor: Option<LocalId>,
    pub message: MapString,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum CommitValidationViolationKind {
    NoDescriptor,
    UnsupportedValidationRule,
    UnsupportedConstraintType {
        constraint: ConstraintReference,
        constraint_type: ConstraintTypeReference,
    },
    RuleViolation { code: MapString },
    UnresolvedLocalDependency,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum ValidationSubjectPath {
    Holon { holon: HolonReference },
    Property { holon: HolonReference, name: PropertyName },
    Value { holon: HolonReference, property: PropertyName },
    Relationship {
        source: HolonReference,
        name: RelationshipName,
        target: HolonReference,
    },
    Transaction,
}

#[derive(Clone, Debug, Default, PartialEq, Eq)]
pub struct CommitValidationReport {
    pub violations: Vec<CommitValidationViolation>,
}

impl CommitValidationReport {
    pub fn is_accepted(&self) -> bool;
    pub fn has_blocking_violation(&self) -> bool;
}
```

`ValidationRuleKey` is the stable authored semantic rule key, not a storage identity. The exact
wire representation of `HolonReference`, `LocalId`, `PropertyName`, `RelationshipName`, and
`ValidationSeverity` follows their existing shared MAP definitions; this specification does not
create parallel identifier or string types. `HolonReference` preserves the standard MAP wrapper
pattern for either a staged or saved subject; a validator does not expose a raw `Holon` merely to
report its path.

`message` is actionable local diagnostic text, not a consensus-visible canonical message. Stable
machine interpretation uses `kind`, `rule_key`, and the rule-specific `code`.

The validation orchestrator returns a complete `CommitValidationReport` for semantic outcomes. It
does not use `Result` for an ordinary failed validation: a blocking report is an expected Commit
decision. `Result<_, HolonError>` remains appropriate for operational failures that prevent the
validator from constructing a report. After clearing prior validation-originated findings for the
pass, Commit records each report violation as `HolonError::CommitValidation` on the applicable
`StagedHolon.errors`; transaction-wide findings are retained on the Commit outcome when no single
staged holon is the sole subject.

### 5.2 Validator entry points and contexts

The public orchestration entry point is conceptually:

```rust
pub fn validate_nursery(
    nursery: &mut Nursery,
    services: &CommitValidationServices,
) -> Result<CommitValidationReport, HolonError>;
```

`CommitValidationServices` is an immutable bundle of existing descriptor/runtime services needed
to resolve descriptors, read effective relationships, and read the current-Space relationship
snapshot. It must not contain mutable staging state, a binding catalog, or an unbounded remote
resolver.

The orchestrator alone mutates `StagedHolon.validation_state` and manages validation-originated
staged-holon errors. At the beginning of a pass it removes only prior
`HolonError::CommitValidation` findings, preserving unrelated Commit errors; at the end it records
the current pass's findings. Lower-level validators return findings through a collector and cannot
mutate their parent subject:

```rust
pub struct ValidationCollector {
    // ordered findings; private representation
}

impl ValidationCollector {
    pub fn record(&mut self, violation: CommitValidationViolation);
}

pub fn validate_holon(
    subject: HolonValidationSubject<'_>,
    context: &HolonValidationContext<'_>,
    collector: &mut ValidationCollector,
);

pub fn validate_property(
    subject: PropertyValidationSubject<'_>,
    context: &PropertyValidationContext<'_>,
    collector: &mut ValidationCollector,
);

pub fn validate_value(
    subject: ValueValidationSubject<'_>,
    context: &ValueValidationContext<'_>,
    collector: &mut ValidationCollector,
);

pub fn validate_relationship(
    subject: RelationshipValidationSubject<'_>,
    context: &RelationshipValidationContext<'_>,
    collector: &mut ValidationCollector,
);

pub fn validate_prospective_relationships(
    view: &ProspectiveLocalRelationshipView,
    context: &TransactionValidationContext<'_>,
    collector: &mut ValidationCollector,
);
```

Subjects contain the validation object and its governing descriptor wrapper. Contexts contain only
the bounded execution dependencies stated in [Section 4](#4-validation-subjects-and-dependency-direction).
In particular, `ValueValidationSubject` has no property or holon reference, and
`PropertyValidationSubject` has no containing-holon reference. A diagnostic path may be carried
separately as immutable provenance.

The aggregate phase receives a distinct, read-only `ProspectiveLocalRelationshipView`. It is
constructed by the Commit orchestrator from the current-Space snapshot and normalized staged
deltas; relationship validators do not construct it themselves.

### 5.3 Constraint and rule invocation with static dispatch

An effective constraint is represented as its typed occurrence, rather than as reconstructed
descriptor-property parameters. It retains the configured instance and contribution provenance
needed for diagnostics. An effective rule binding is represented as a typed occurrence rather than
as an unqualified rule reference. It retains rule identity and binding provenance; it does not
carry constraint parameter overrides:

```rust
pub struct ResolvedValidationBinding {
    pub rule: ValidationRuleReference,
    pub declaring_descriptor: HolonDescriptorReference,
}

pub struct ResolvedConstraint {
    pub constraint: ConstraintReference,
    pub constraint_type: ConstraintTypeReference,
    pub declaring_descriptor: HolonDescriptorReference,
}

pub enum ValidationInvocation<'a> {
    Holon {
        binding: &'a ResolvedValidationBinding,
        subject: HolonValidationSubject<'a>,
        context: HolonRuleContext<'a>,
    },
    Property {
        binding: &'a ResolvedValidationBinding,
        subject: PropertyValidationSubject<'a>,
        context: PropertyRuleContext<'a>,
    },
    Value {
        binding: &'a ResolvedValidationBinding,
        subject: ValueValidationSubject<'a>,
        context: ValueRuleContext<'a>,
    },
    Relationship {
        binding: &'a ResolvedValidationBinding,
        subject: RelationshipValidationSubject<'a>,
        context: RelationshipRuleContext<'a>,
    },
    Transaction {
        binding: &'a ResolvedValidationBinding,
        context: TransactionRuleContext<'a>,
    },
}

pub type StaticRuleHandler = fn(ValidationInvocation<'_>, &mut ValidationCollector);

pub struct StaticRuleRegistry;

impl StaticRuleRegistry {
    pub fn lookup(key: &ValidationRuleKey) -> Option<StaticRuleHandler>;
}

pub struct StaticConstraintRegistry;

impl StaticConstraintRegistry {
    pub fn lookup(type_key: &ConstraintTypeKey) -> Option<StaticConstraintHandler>;
}
```

The registries are static Rust tables or exhaustive `match` expressions over canonical rule keys
and concrete constraint type keys. They are not trait-object factories, dynamic library loaders,
`ValidationImplementation` resolvers, or schema catalogs. Before invocation, the orchestrator
verifies a constraint's applicability and a binding's compatible rule family. A missing compatible
handler records the appropriate unsupported semantic finding; incompatible attachment or binding is
a descriptor/schema conformance failure, not a best-effort runtime dispatch decision.

### 5.4 State transition ownership

`ValidationState` remains the existing runtime enum on `StagedHolon`:

```rust
pub enum ValidationState {
    NoDescriptor,
    ValidationRequired,
    Validated,
    Invalid,
}
```

The state records the most recent relevant outcome; it does not authorize persistence and is never
read to decide whether a holon receives Commit validation. Every mutation that can change
descriptor selection, effective properties, populated values, declared relationships, or binding
applicability may mark a prior result stale by setting `NoDescriptor`, `Validated`, or `Invalid` to
`ValidationRequired`. Missing such an invalidation is a UI/status defect, not a route around Commit
validation.

The Commit orchestrator makes the only result transitions: descriptor resolution failure produces
`NoDescriptor`; a blocking local or aggregate finding produces `Invalid`; a holon whose applicable
local checks pass becomes `Validated`. Every Commit runs the aggregate current-Space relationship
pass, including for holons whose prior state was `Validated`.

## 6. Core Commit validation algorithm

Commit executes this algorithm over the complete Nursery:

1. Start a fresh validation pass: clear prior validation-originated diagnostics while preserving
   unrelated Commit errors, and iterate over every staged holon in the Nursery regardless of its
   prior `ValidationState`.
2. For each staged holon, resolve its governing descriptor with `holon_descriptor()`.
3. If resolution fails, set `NoDescriptor`, record a blocking descriptor-resolution result, and
   skip descriptor-dependent validation for that holon.
4. Otherwise run, in canonical order:
   1. collect and evaluate effective `Constraints` applicable to the holon subject;
   2. collect and evaluate effective `ValidationBindings` applicable to the holon subject;
   3. perform Holon Validation;
   4. for every effective property, collect/evaluate its constraints and bindings, then perform
      Property Validation;
   5. for every present property value, collect/evaluate the selected value type's constraints and
      bindings, then perform Value Validation;
   6. for every declared relationship occurrence, collect/evaluate the relationship descriptor's
      constraints and bindings, then perform Relationship Validation.
5. Construct the prospective current-Space occurrence collection and run Multi-hop Relationship
   Validation and other bounded aggregate rules.
6. Accumulate all results. Any blocking result marks the relevant staged holon `Invalid` where
   applicable and rejects the complete Commit before any persistence write.
7. When no blocking result exists, mark successfully assessed staged holons `Validated` and
   persist the Commit normally.

Mutations may mark their prior observed result `ValidationRequired`, but Commit does not use that
state to select work. Aggregate validation may invalidate a holon that had been `Validated` in a
prior pass.

`DescribedBy` resolution is bootstrap navigation, not a special hard-coded exactly-one rule. Its
minimum and maximum cardinality are enforced by ordinary generic relationship-cardinality
validation, as for every declared relationship.

## 7. Constraint and binding discovery, compatibility, and dispatch

For each validation subject:

1. resolve the subject's governing descriptor;
2. read its effective `Constraints` through `effective_constraints()`;
3. resolve every constraint target and verify its concrete type's applicability and static
   constraint handler; if no compatible handler exists, accumulate blocking
   `UnsupportedConstraintType { constraint, constraint_type }` and do not evaluate that
   constraint;
4. evaluate every applicable configured constraint with its own configuration;
5. read its effective `ValidationBindings` through `effective_validation_bindings()`;
6. select the rule occurrences applicable to the validator level and execution context;
7. resolve the target `ValidationRule`;
8. dispatch the canonical rule identity through the static implementation registry; and
9. accumulate all findings.

Binding compatibility is a descriptor/schema self-conformance invariant. A bound rule family must
be compatible with the declaring type's effective kind; for example, a string-value rule cannot be
bound to a declared relationship type. VAL0b has no active binding occurrence, so it introduces no
additional compatibility taxonomy or runtime check. The first active-binding capability must prove
both compatible pairing acceptance and incompatible-pairing rejection during descriptor/schema
self-conformance, before handler dispatch. Commit separately verifies that every active binding
has a compatible static handler. A mandatory active binding that lacks one fails closed with
`UnsupportedValidationRule`.

Static function or enum dispatch keyed by concrete constraint type and canonical rule identity is
the initial implementation mechanism. It preserves configured invariant data and stable rule
identities without prematurely introducing dynamic dispatch.

## 8. Holon Validation

Holon Validation is governed by `D(H)`, the staged holon's governing descriptor. It evaluates
whole-holon rules and orchestrates downward delegation; it does not make property or value rules
depend on the holon itself.

Its rules include, as implemented and bound:

- instantiability of the governing type;
- populated properties not represented by the effective instance contract, subject to any
  descriptor-defined open-property policy; and
- other whole-holon commitments of `D(H)`.

After its own rules, the Holon Validator enumerates the effective property contract, including
absent properties, and separately enumerates declared relationship occurrences.

## 9. Property Validation

Property Validation is governed by the resolved effective `PropertyType`. Its subject consists of
the property identity, that descriptor, and an optional value. It determines required-property
presence and other property-level commitments without receiving its containing holon.

For a present value, Property Validation resolves the selected `ValueType`, creates the narrower
Value Validation input, and delegates. An absent optional property does not enter Value Validation.

## 10. Value Validation

Value Validation is governed only by the `ValueType` selected by its `PropertyType`. It assesses
intrinsic validity of the value for that type, including native `BaseValue`/`ValueType` kind
compatibility and every effective configured value constraint, such as length, range, pattern, or
allowed values. Enum membership and other fixed type semantics remain rules or descriptor-kernel
algorithms where they are not configured constraints.

A value-kind mismatch produces a result and prevents type-specific validation for that value. A
Value Validator does not know which property holds the value or which holon owns that property.

## 11. Relationship Validation

Relationship Validation is governed by the resolved `DeclaredRelationshipType`. Its subject is one
declared occurrence plus the bounded local occurrence context required by its rule. It evaluates
declaredness, endpoint compatibility, ordering, duplicate policy, applicable configured
constraints, and other single-occurrence commitments.

It does not assume that inverse occurrences have already been persisted. Rules that need more than
one occurrence use the Multi-hop Relationship Validation scope.

## 12. Multi-hop Relationship Validation

Multi-hop Relationship Validation evaluates bounded patterns and aggregate commitments after the
per-holon traversal. It includes local pre-commit inverse validation: before accepting a declared
relationship update, Commit evaluates every required inverse occurrence as though it were already
materialized in the current MAP Space. It does not persist either direction until this evaluation
has passed.

For a declared occurrence:

```text
A —R→ B
```

whose inverse descriptor is `R⁻¹`, the prospective local view also contains:

```text
B —R⁻¹→ A
```

when `B`, the source of the inverse occurrence, belongs to the committing Space. `R` and `R⁻¹`
are distinct directional descriptors and may carry different cardinality, duplicate, ordering,
endpoint, or other constraints. Validating only the declared direction is therefore insufficient.

### 12.1 Prospective local occurrence collection

The scope is the prospective occurrence collection of the committing MAP Space:

```text
locally committed occurrences
− locally removed or superseded occurrences in this Commit
+ locally staged declared occurrences
+ locally derived inverse occurrences whose source is in this Space
```

This view supports source- and inverse-side local cardinality, duplicates, ordering, endpoint
compatibility, and bounded cross-relationship obligations. `DS-CARD-001` evaluates every effective
applicable `CardinalityConstraint` against the relevant directional bucket; all must pass. The
declared update is the event Commit accepts or rejects, so applicable local inverse constraints are
included before acceptance.

Commit does not rebuild the entire Space graph. It evaluates only the directional occurrence
buckets affected by the staged relationship deltas. A bucket is conceptually identified by:

```text
(source_holon_identity, relationship_descriptor_identity)
```

For `A —R→ B`, the affected buckets are `(A, R)` and, when `B` is local, `(B, R⁻¹)`.

### 12.2 Normalize declared relationship deltas

Before evaluating constraints, Commit normalizes staged relationship mutations into logical deltas
over semantic relationship occurrences:

```text
Add(occurrence)
Remove(semantic_occurrence_identity)
Replace(old_occurrence, new_occurrence)
```

`Replace` normalizes to removal plus addition. Multiple mutations to the same semantic occurrence
within one Commit must collapse to their net effect; for example, add followed by remove produces
no net delta. An occurrence carries the semantic information required for validation and paired
materialization: its identity, directional descriptor, source, target, ordering/properties where
applicable, and whether it is declared or locally derived inverse state.

### 12.3 Derive and validate local inverse deltas

For every normalized declared delta, Commit resolves the inverse descriptor through `HasInverse`.
When the target is in the committing Space, it derives the corresponding inverse delta with the
same semantic occurrence identity and reversed endpoints:

| Declared delta | Derived local inverse delta |
|---|---|
| Add `A —R→ B` | Add `B —R⁻¹→ A` |
| Remove `A —R→ B` | Remove `B —R⁻¹→ A` |
| Replace target `B₁` with `B₂` | Remove `B₁ —R⁻¹→ A`; add `B₂ —R⁻¹→ A` |

Commit applies the ordinary relationship validation rules independently to every affected
directional occurrence and bucket. This includes occurrence shape, declaredness, endpoint
compatibility, duplicate policy, ordering, and cardinality. Inverse validation is not a special
inverse-cardinality rule; it is ordinary relationship validation applied to a derived occurrence
under the inverse descriptor.

An unavailable target or descriptor needed for an applicable local rule is a normal unresolved
validation dependency and must not be treated as evidence that the rule passed.

### 12.4 Relationship commit plan and concurrency

Only after all affected local buckets pass validation does Commit prepare a storage-ready logical
relationship plan. The plan contains the declared operations, required local inverse operations,
and the versions or other concurrency preconditions of the affected buckets. The storage layer
persists this prepared plan; it does not infer inverse semantics or repair omitted local inverses.

Validation and persistence must be protected from stale local bucket reads. For example, two
Commits must not each observe 49 occurrences under a maximum of 50 and independently add one.
An implementation may serialize mutations to an affected bucket, use compare-and-swap/version
preconditions, re-read and revalidate before writing, or provide equivalent transaction isolation.
The semantic requirement is that a successful Commit is not based on a prospective local view made
stale by a competing successful Commit.

### 12.5 Cross-Space boundary

An inverse whose source belongs to another MAP Space may be materialized later through MAP's pull
model. Commit neither waits for that work, pushes it, reserves remote capacity, nor reports a
successful local forward Commit as provisional. A later remote conflict is a future Runtime
Recognition, governance, reconciliation, or repair concern; it does not retroactively invalidate
the immutable version accepted by the declaring Commit.

## 13. Results, state, and persistence decision

Validation accumulates stable, actionable results with rule identity, severity, outcome, and a
subject path. The parent orchestrator may attach broader provenance to a result returned by a
lower-level validator; lower-level validators do not retrieve that provenance themselves.

`StagedHolon.validation_state` uses:

- `NoDescriptor` when governing-descriptor resolution failed;
- `ValidationRequired` when no current observed outcome is available, including after a mutation
  marked the prior result stale;
- `Validated` after the most recent applicable local validation found no blocking result; and
- `Invalid` after the most recent pass found a blocking result.

No blocking result may be persisted. Before each pass, Commit replaces—not indefinitely
accumulates—validation-originated errors with the current findings, while preserving unrelated
Commit errors. The validation state and errors remain transient Commit runtime state, separate from
immutable holon content.

## 14. Non-goals and deferred work

This capability does not define:

- Runtime Recognition inputs, recognition outcomes, activation, or governance protocol;
- cross-Space inverse reconciliation, conflict resolution, or repair;
- dynamic or extension-loaded rule executors;
- persisted validation evidence, receipts, rule sets, or generic profiles; or
- descriptor-independent PVL and Integrity callback behavior.

Runtime Recognition remains distinct: it establishes whether a current AgentSpace recognizes data
under its current activation and governance state. It is temporal, revocable, AgentSpace-specific,
and does not reinterpret immutable Commit validity.

## 15. Conformance scenarios

The implementation and its tests must demonstrate at least:

- a missing governing descriptor produces `NoDescriptor` and blocks Commit;
- a holon marked `Validated` by an earlier pass is still validated again by the next Commit;
- a corrected staged holon has its prior validation-originated errors replaced by the new pass's
  findings, while unrelated Commit errors remain available;
- an inherited active binding is discovered through ordinary effective relationships;
- an unbound seeded rule is not discovered;
- an active mandatory binding without a handler produces `UnsupportedValidationRule` and blocks
  Commit;
- an effective attached constraint without a compatible handler produces
  `UnsupportedConstraintType`, identifies both the constraint instance and concrete constraint
  type, and blocks Commit;
- a missing required property is assessed even when absent from the property map;
- a value-kind mismatch prevents value-type-specific rule execution;
- a local inverse cardinality violation blocks Commit; and
- a deferred cross-Space inverse does not make a successful forward Commit pending or provisional.
