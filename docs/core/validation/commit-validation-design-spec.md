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

- Commit is the target sole public production persistence gate. Every public producer of a MAP
  state mutation ultimately reaches this boundary. Internal node/entry persistence and SmartLink
  creation or removal consume a prepared Commit plan and are not independently callable
  persistence paths.
- `LocalHolonSpace` bootstrap is the sole intended permanent exception to that public-gate rule. It
  remains a narrowly scoped bootstrap path, not a second general ingress or mutation API.
- The initial validation track delivers gate convergence for create, update, and relationship-
  occurrence mutation. Holon deletion must ultimately use a prepared Commit plan as well, but the
  current direct `DeleteHolon` ingress remains a tracked implementation gap until a dedicated
  deletion capability defines and delivers deletion planning and `Allow` / `Block` / `Cascade`
  execution. It is not a second supported gate or a permanent architectural exception.
- Commit validates the complete Nursery before any persistence write.
- Every Commit runs descriptor-aware validation for every staged holon in that Nursery.
  `ValidationState` is an observation from an earlier or current pass, never a scheduling cache
  that permits Commit to skip a holon.
- A type's effective `Constraints` are configured definitional commitments: accepting an instance
  asserts conformance to every applicable configured invariant.
- A type's effective `ValidationBindings` select the remaining applicable fixed or contextual
  Commit rules; they do not duplicate constraint configuration.
- Every currently configured constraint and authored Commit binding is mandatory and blocking.
  Semantic findings retain `Error` severity; there is no current advisory profile, severity
  override, or minimum-blocking policy.
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
- Staging any descriptor schedules validation of its owning Schema aggregate over the prospective
  persisted-plus-staged `Components` collection, whether or not the Schema holon itself was staged.

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

The first implementation defines orchestration contracts in the separate WASM-safe
`holons_validation` crate. Dependency-safe finding primitives live in `core_types` so
`StagedHolon` can store findings without depending upward on validator contexts or registries.
`core_types` is the correct home because it already sits below `holons_core` and above
`integrity_core_types`. Descriptor-aware validation vocabulary must not be added to
`integrity_core_types`, which stays descriptor-independent for PVL.
`holons_validation` consumes standard shared-object and descriptor-runtime wrappers; it must not
introduce a parallel graph model, raw-holon public API, or validation-specific descriptor cache.

`ValidationResult` is a future schema/evidence holon. It is not the transient Rust result type for
Commit. The Rust contracts below describe only the in-memory decision and diagnostics of one
Commit attempt.

### 5.1 Violation and report types

Commit uses four distinct outcome types:

1. dependency-light `CommitValidationViolation` for one identity-only semantic finding;
2. serializable `CommitValidationReport` for all findings and a derived acceptance decision;
3. `HolonError` only for operational failures that prevent reliable assessment; and
4. `ValidationResult` only for separately designed durable evidence.

The first two contracts are structured, serializable, and independent of a particular validator
implementation. Representative shapes are:

```rust
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CommitValidationViolation {
    pub kind: CommitValidationViolationKind,
    pub rule_key: Option<String>,
    pub severity: ValidationSeverity,
    pub subject: ValidationSubjectPath,
    pub descriptor_identity: Option<String>,
    pub message: String,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum CommitValidationViolationKind {
    NoDescriptor,
    UnsupportedValidationRule,
    UnsupportedConstraintType {
        constraint_identity: String,
        constraint_type_identity: String,
    },
    RuleViolation { code: String },
    UnresolvedLocalDependency,
    RelationshipCoordinationRequired,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum ValidationSubjectPath {
    Holon { holon_identity: String },
    Property { holon_identity: String, name: String },
    Value { holon_identity: String, property: String },
    Relationship {
        source_identity: String,
        name: String,
        target_identity: String,
    },
    Transaction,
}

#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct CommitValidationReport {
    pub violations: Vec<CommitValidationViolation>,
}

impl CommitValidationReport {
    pub fn is_accepted(&self) -> bool;
    pub fn violation_count(&self) -> usize;
}
```

The strings above denote dependency-safe serialized identity and path values; the implementation
may use existing lower-level newtypes when doing so preserves the dependency direction. Findings
must not store bound runtime references. The validator uses ordinary bound references internally
and projects identity-only paths into the report.

Because findings are identity-only, they cross the boundary unchanged: `StagedHolonWire` in
`holons_boundary` carries the staged holon's findings collection beside its existing
`validation_state`, separate from its operational `errors`.

`message` is actionable local diagnostic text, not a consensus-visible canonical message. Stable
machine interpretation uses `kind`, `rule_key`, and the rule-specific `code`.

Every current violation has `Error` severity and derives a rejected decision; severity is retained
for diagnostics and future evidence compatibility, not current blocking policy. The validation
orchestrator returns a complete `CommitValidationReport` for semantic outcomes. It does not use
`Result` for an ordinary rejection. `Result<_, HolonError>` remains appropriate only for an
operational failure that prevents construction of a reliable report.

After a pass, Commit projects identity-only report findings into the applicable
`StagedHolon.validation_findings` collection. It does not wrap them in an operational error variant
or mix them with operational errors. Transaction-wide findings remain on the report when no single
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

The orchestrator alone replaces `StagedHolon.validation_state` and
`StagedHolon.validation_findings`. It prepares the complete new state and identity-only finding set
for each subject, then uses the controlled `holons_core` replacement operation to install both
together. Operational errors remain separate and untouched. Lower-level validators return findings
through a collector and cannot mutate their parent subject:

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

### 5.3 Rule invocation and internal constraint evaluation

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
`ValidationImplementation` resolvers, or schema catalogs. `StaticRuleRegistry` is Commit's
commitment-dispatch surface for effective `ValidationBindings`. `StaticConstraintRegistry` is an
internal typed evaluator used by the governing conformance handler; a constraint attachment does
not create a second Commit-policy or commitment-dispatch surface.

Before invocation, the governing conformance handler verifies a constraint's applicability, and
the Commit orchestrator verifies a binding's compatible rule family. A missing compatible
constraint handler records `UnsupportedConstraintType`; a missing compatible rule handler records
`UnsupportedValidationRule`. Incompatible attachment or binding is a descriptor/schema
self-conformance failure, not a best-effort runtime dispatch decision.

Failure of an applicable, well-formed definitional constraint is unconditionally Commit-blocking.
Constraint types therefore carry no Commit severity or blocking-policy metadata. The governing
conformance rule supplies the finding's stable rule identity, code, and severity—for example,
`PropertyValueConformance.ValidationRule` governs configured value constraints, while
`DS-CARD-001` governs configured relationship cardinality. A finding for a reused constraint must
identify the constrained subject and the constraint contribution's declaring-descriptor
provenance, not only the shared constraint instance.

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

`holons_core` exposes only the descriptor/validation facade required by this orchestration:
effective targets with provenance, constraint and binding convenience accessors, subtype
compatibility, property snapshots, native value-kind checking, and controlled staged-outcome
replacement. Commit and `holons_validation` must not bypass references or add parallel mutation,
lookup, or persistence operations.

## 6. Core Commit validation algorithm

Commit executes a fresh validation pass over the complete Nursery. It prepares replacement
validation state and finding collections without altering operational errors and assesses every
staged holon regardless of its prior `ValidationState`.

The pass proceeds in dependency order:

1. **Prepare prospective inputs.** Resolve governing descriptors and effective contracts where
   possible, normalize staged relationship deltas, identify affected Schemas, and construct the
   prospective Schema-component and locally authoritative relationship views needed by later
   validation. A governing-descriptor resolution failure records `NoDescriptor`, prevents
   descriptor-dependent checks for that subject, and rejects Commit.
2. **Establish prospective schema readiness.** Validate staged descriptors, constraints, and rules
   through their own governing descriptors, and validate each affected Schema once over its
   prospective persisted-plus-staged `Components` collection. Staging any descriptor schedules its
   owning Schema even when the Schema holon itself was not staged. Commit does not rely on an
   invalid prospective schema commitment when assessing another subject; a dependent check that
   cannot therefore be completed records an explicit blocking finding rather than being omitted.
3. **Traverse every usable staged subject.** Holon Validation runs for each staged holon with a
   usable governing descriptor and enumerates its complete effective member contract. Property
   Validation includes absent effective properties so required-member checks are not selected only
   from populated state. Value Validation runs for each present property value. Relationship
   Validation enumerates effective declared relationship members and their prospective directional
   buckets, including empty buckets, rather than starting only from populated occurrences.
4. **Evaluate both commitment paths independently.** At every applicable subject level, validation
   unconditionally discovers and evaluates effective configured constraints. Separately, it
   discovers and dispatches effective `ValidationBindings` for non-constraint rules. Neither the
   absence of bindings nor the absence of populated relationship occurrences suppresses mandatory
   constraint evaluation.
5. **Run bounded aggregate validation.** Evaluate affected locally authoritative directional
   relationship buckets, locally realizable inverse effects, and other bounded multi-subject
   commitments against their prospective views. A required check outside the available authority
   fails closed with the applicable dependency or coordination finding.
6. **Complete the decision.** An accepted report requires complete mandatory-commitment coverage
   and no findings. Any finding marks the relevant staged holon `Invalid` where applicable and
   rejects the complete persistence-candidate set before any write. When the report is accepted,
   Commit marks successfully assessed staged holons `Validated`, prepares the complete node and
   relationship persistence plan, and passes that plan to internal persistence operations.

Mutations may mark their prior observed result `ValidationRequired`, but Commit does not use that
state to select work. Aggregate validation may invalidate a holon that had been `Validated` in a
prior pass.

`DescribedBy` resolution is bootstrap navigation, not a special hard-coded exactly-one rule. Its
minimum and maximum cardinality are enforced by ordinary generic relationship-cardinality
validation, as for every declared relationship.

## 7. Mandatory constraint evaluation and validation-binding dispatch

Commit reaches descriptor-backed validation commitments through two independent paths. Effective
`Constraints` occurrences carry mandatory definitional semantics. Effective
`ValidationBindings` occurrences activate the remaining fixed or contextual non-constraint rules.
The shared subject traversal invokes both paths; a bound rule is not required to trigger constraint
discovery or evaluation.

### 7.1 Effective constraints

For every applicable validation subject, the subject validator reads the governing descriptor's
effective `Constraints` through `effective_constraints()`. The presence of an effective constraint
occurrence is sufficient to make that constraint mandatory. For every occurrence, validation:

1. resolves the configured instance and concrete constraint type while retaining the constrained
   subject and declaring-descriptor provenance;
2. verifies attachment applicability;
3. resolves a subject- and context-compatible evaluator through the internal
   `StaticConstraintRegistry`; if none exists, it accumulates blocking
   `UnsupportedConstraintType { constraint_identity, constraint_type_identity }`;
4. evaluates the configured invariant immediately or schedules it for the bounded aggregate phase
   required by its subject scope; and
5. accumulates any failure or authoritative inability to evaluate as a blocking finding.

`StaticConstraintRegistry` is an implementation dispatch mechanism, not an activation or policy
gate. A constraint attachment is never ignored because no validation rule is bound. Constraint
findings carry a stable semantic code, the constraint instance and concrete type identities, the
constrained subject, and declaring-descriptor provenance; they do not require a
`ValidationRule` identity.

### 7.2 Effective validation bindings

Independently, the subject validator reads effective `ValidationBindings` through
`effective_validation_bindings()`. Each occurrence activates its target non-constraint
`ValidationRule` for the compatible validator level and bounded execution context. Commit resolves
the binding and rule identity, verifies rule-family and subject compatibility, dispatches the rule
through `StaticRuleRegistry`, and accumulates its findings. An active mandatory binding without a
compatible handler produces `UnsupportedValidationRule` and rejects Commit. An unbound rule remains
inactive; an attached constraint does not.

### 7.3 Coverage and staged delivery

An accepted report proves that every applicable effective constraint and every active effective
validation binding was evaluated in its required bounded context. Each mandatory commitment must
either complete, produce a semantic failure, fail closed as unsupported or incompatible, or produce
an explicit blocking dependency or coordination finding. An empty accepted report therefore means
complete mandatory coverage with no violations, not that no handler was invoked.

Incremental delivery does not weaken this invariant. Before final production activation, explicit
Capability 1–4 validator exercises reject when they encounter an unsupported mandatory constraint.
Capability 1 is therefore permitted to demonstrate fail-closed full-Nursery rejection rather than
a complete accepted Nursery. The universal production Commit gate is activated only after every
constraint type reachable from the loaded schema corpus has a compatible evaluator and the final
activation coverage tests pass.

Binding compatibility is a descriptor/schema self-conformance invariant. A bound rule family must
be compatible with the declaring type's effective kind; for example, a string-value rule cannot be
bound to a declared relationship type. VAL0b has no active binding occurrence, so it introduces no
additional compatibility taxonomy or runtime check. The first active-binding capability must prove
both compatible pairing acceptance and incompatible-pairing rejection during descriptor/schema
self-conformance, before handler dispatch. Commit separately verifies that every active binding
has a compatible static handler. A mandatory active binding that lacks one fails closed with
`UnsupportedValidationRule`.

Static function or enum dispatch keyed by canonical rule identity, with internal constraint
evaluation keyed by concrete constraint type, is the initial implementation mechanism. It
preserves configured invariant data and stable rule identities without prematurely introducing
dynamic dispatch.

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

The
[Relationship Occurrence Persistence Design Specification](../transactions/relationship-persistence-design-spec.md)
owns authoritative local buckets, prepared declared/inverse plans, normal-order zome-call
persistence, source-chain conflict reload/revalidation, and retry/failure behavior. Commit
Validation supplies the assessed prospective deltas and accepted report; it does not define a
second concurrency or SmartLink persistence protocol here.

### 12.5 Cross-Space boundary

An inverse whose source belongs to another MAP Space may be materialized later through MAP's pull
model. Commit neither waits for that work, pushes it, reserves remote capacity, nor reports a
successful local forward Commit as provisional. A later remote conflict is a future Runtime
Recognition, governance, reconciliation, or repair concern; it does not retroactively invalidate
the immutable version accepted by the declaring Commit.

That ordinary inverse deferral does not permit an incomplete observation to satisfy a rule that
actually requires multi-cell aggregate authority. When an applicable rule cannot be assessed from
the locally authoritative buckets and explicitly requires such coordination, Commit emits the
`RelationshipCoordinationRequired` `Error`-severity finding and rejects the Commit. Cross-cell DHT
reads are not treated as a serializable snapshot. Multi-cell relationship coordination is deferred
to a future Relationship Coordination capability.

## 13. Results, state, and persistence decision

Validation accumulates stable, actionable findings with rule identity, severity, and a subject
path. The parent orchestrator may attach broader provenance to a finding returned by a
lower-level validator; lower-level validators do not retrieve that provenance themselves.

`StagedHolon.validation_state` uses:

- `NoDescriptor` when governing-descriptor resolution failed;
- `ValidationRequired` when no current observed outcome is available, including after a mutation
  marked the prior result stale;
- `Validated` after the most recent applicable local validation found no blocking result; and
- `Invalid` after the most recent pass found a blocking result.

No rejected report may be persisted. After each pass, Commit replaces—not indefinitely
accumulates—the validation state and identity-only findings together, while preserving operational
errors separately. The validation state and findings remain transient Commit runtime state,
separate from immutable holon content.

The public Commit response distinguishes semantic rejection, explicit abandonment, operational
persistence failure, and success. Its wire projection includes:

- `Rejected` when assessment completed and the report decision is rejection;
- `RejectedHolons`, containing the staged holon identities associated with findings;
- the serializable `CommitValidationReport` projection; and
- a violation count derived from that report rather than maintained as independent state.

`Abandoned` continues to mean an explicit caller/runtime lifecycle choice. A `HolonError` means
assessment or persistence could not complete reliably. Neither is projected as `Rejected`.

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
- a corrected staged holon has its prior validation findings and state replaced together by the
  new pass's outcome, while operational errors remain separate;
- staging a descriptor validates its owning Schema's prospective persisted-plus-staged
  `Components` collection even when the Schema holon is absent from the Nursery;
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
- a rule requiring unavailable multi-cell aggregate authority emits
  `RelationshipCoordinationRequired` and rejects Commit;
- a deferred cross-Space inverse does not make a successful forward Commit pending or provisional;
  and
- response fixtures distinguish rejection with report projection from abandonment and operational
  failure and derive the violation count from the report.
