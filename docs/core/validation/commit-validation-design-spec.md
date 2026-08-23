# MAP Commit Validation Design Specification

> **Status:** Draft
>
> This specification defines MAP's semantic, descriptor-aware Commit Validation: the validation
> that determines whether a complete staged Nursery may be persisted.

---

## 1. Purpose and authority

This specification owns descriptor-aware validation orchestration, subject boundaries, binding
discovery, static rule dispatch, result aggregation, and the Commit acceptance decision.

It relies on:

- the [Validation Architecture](validation-arch.md) for MAP's broader validation landscape,
  execution layers, and Runtime Recognition position;
- the [Validation Schema Design Specification](validation-schema-design-spec.md) for the schema
  shape of `ValidationRule`, `ValidationBindings`, implementations, and results;
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
- A type's effective `ValidationBindings` are definitional commitments: accepting an instance
  asserts conformance to the applicable implemented rules.
- An unbound `ValidationRule` is not applicable. An active mandatory binding without a compatible
  handler produces `UnsupportedValidationRule` and blocks Commit.
- Validation uses ordinary descriptor runtime products, including
  `ReadableHolon::available_relationships`; it has no binding catalog or separate lineage walk.
- Lower-level validators receive only the dependencies needed to validate their own subjects. They
  do not traverse upward to a containing property, holon, or Nursery.
- Validation state and diagnostics are transient `StagedHolon` Commit state. They are not persisted
  content of the holon under assessment.

## 3. Terms and relationship model

`ValidationBindings` is the additive, definitional declared relationship from an applicable type to
a compatible `ValidationRule`.

```text
Applicable Type —ValidationBindings→ ValidationRule
```

The generic relationship contract is co-defined by Core and Validation. An active occurrence is
declared on the actual applicable type, not generically on `TypeDescriptor`. Its ordinary effective
relationship surface carries inherited commitments.

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

Each executed rule receives its identity, the selected binding occurrence, resolved parameters, a
subject-specific input, and only the execution context required for that rule. A representative
conceptual shape is:

```text
RuleInvocation<Subject>
  rule: ValidationRuleReference
  binding: occurrence of ValidationBindings
  subject: Subject
  parameters: ResolvedValidationParameters
  execution_context: Subject-appropriate context
```

## 5. Core Commit validation algorithm

Commit executes this algorithm over the complete Nursery:

1. Identify staged holons whose local validation state is `ValidationRequired`; a previously
   `Validated` holon may be reused only while its validation dependencies are unchanged.
2. For each such staged holon, resolve its governing descriptor with `holon_descriptor()`.
3. If resolution fails, set `NoDescriptor`, record a blocking descriptor-resolution result, and
   skip descriptor-dependent validation for that holon.
4. Otherwise run, in canonical order:
   1. Holon Validation;
   2. Property Validation for every effective property;
   3. Value Validation for every present property value;
   4. Relationship Validation for every declared relationship occurrence.
5. Construct the prospective current-Space occurrence collection and run Multi-hop Relationship
   Validation and other bounded aggregate rules.
6. Accumulate all results. Any blocking result marks the relevant staged holon `Invalid` where
   applicable and rejects the complete Commit before any persistence write.
7. When no blocking result exists, mark successfully assessed staged holons `Validated` and
   persist the Commit normally.

Mutations to descriptor selection, properties, declared relationships, or other declared validation
dependencies change `Validated` to `ValidationRequired`. Aggregate validation may still invalidate
an otherwise locally validated holon.

`DescribedBy` resolution is bootstrap navigation, not a special hard-coded exactly-one rule. Its
minimum and maximum cardinality are enforced by ordinary generic relationship-cardinality
validation, as for every declared relationship.

## 6. Binding discovery, compatibility, and dispatch

For each validation subject:

1. resolve the subject's governing descriptor;
2. read its effective `ValidationBindings` through
   `ReadableHolon::available_relationships`;
3. select the occurrences applicable to the validator level and execution context;
4. resolve the target `ValidationRule` and binding parameters;
5. dispatch the canonical rule identity through the static implementation registry; and
6. accumulate its results.

Binding compatibility is a descriptor/schema self-conformance invariant. A bound rule family must
be compatible with the declaring type's effective kind; for example, a string-value rule cannot be
bound to a declared relationship type. Commit separately verifies that every active binding has a
compatible static handler. A mandatory active binding that lacks one fails closed with
`UnsupportedValidationRule`.

Static function or enum dispatch keyed by canonical rule identity is the initial implementation
mechanism. It preserves stable semantic identities without prematurely introducing dynamic
dispatch.

## 7. Holon Validation

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

## 8. Property Validation

Property Validation is governed by the resolved effective `PropertyType`. Its subject consists of
the property identity, that descriptor, and an optional value. It determines required-property
presence and other property-level commitments without receiving its containing holon.

For a present value, Property Validation resolves the selected `ValueType`, creates the narrower
Value Validation input, and delegates. An absent optional property does not enter Value Validation.

## 9. Value Validation

Value Validation is governed only by the `ValueType` selected by its `PropertyType`. It assesses
intrinsic validity of the value for that type, including native `BaseValue`/`ValueType` kind
compatibility and type-specific rules such as length, range, enum membership, or deterministic
format.

A value-kind mismatch produces a result and prevents type-specific validation for that value. A
Value Validator does not know which property holds the value or which holon owns that property.

## 10. Relationship Validation

Relationship Validation is governed by the resolved `DeclaredRelationshipType`. Its subject is one
declared occurrence plus the bounded local occurrence context required by its rule. It evaluates
declaredness, endpoint compatibility, ordering, duplicate policy, and other single-occurrence
commitments.

It does not assume that inverse occurrences have already been persisted. Rules that need more than
one occurrence use the Multi-hop Relationship Validation scope.

## 11. Multi-hop Relationship Validation

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

### 11.1 Prospective local occurrence collection

The scope is the prospective occurrence collection of the committing MAP Space:

```text
locally committed occurrences
− locally removed or superseded occurrences in this Commit
+ locally staged declared occurrences
+ locally derived inverse occurrences whose source is in this Space
```

This view supports source- and inverse-side local cardinality, duplicates, ordering, endpoint
compatibility, and bounded cross-relationship obligations. The declared update is the event Commit
accepts or rejects, so applicable local inverse constraints are included before acceptance.

Commit does not rebuild the entire Space graph. It evaluates only the directional occurrence
buckets affected by the staged relationship deltas. A bucket is conceptually identified by:

```text
(source_holon_identity, relationship_descriptor_identity)
```

For `A —R→ B`, the affected buckets are `(A, R)` and, when `B` is local, `(B, R⁻¹)`.

### 11.2 Normalize declared relationship deltas

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

### 11.3 Derive and validate local inverse deltas

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

### 11.4 Relationship commit plan and concurrency

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

### 11.5 Cross-Space boundary

An inverse whose source belongs to another MAP Space may be materialized later through MAP's pull
model. Commit neither waits for that work, pushes it, reserves remote capacity, nor reports a
successful local forward Commit as provisional. A later remote conflict is a future Runtime
Recognition, governance, reconciliation, or repair concern; it does not retroactively invalidate
the immutable version accepted by the declaring Commit.

## 12. Results, state, and persistence decision

Validation accumulates stable, actionable results with rule identity, severity, outcome, and a
subject path. The parent orchestrator may attach broader provenance to a result returned by a
lower-level validator; lower-level validators do not retrieve that provenance themselves.

`StagedHolon.validation_state` uses:

- `NoDescriptor` when governing-descriptor resolution failed;
- `ValidationRequired` when validation has not run or has been invalidated by mutation;
- `Validated` after successful applicable local validation; and
- `Invalid` after a blocking result.

No blocking result may be persisted. The validation state and accumulated errors remain transient
Commit runtime state, separate from immutable holon content.

## 13. Non-goals and deferred work

This capability does not define:

- Runtime Recognition inputs, recognition outcomes, activation, or governance protocol;
- cross-Space inverse reconciliation, conflict resolution, or repair;
- dynamic or extension-loaded rule executors;
- persisted validation evidence, receipts, rule sets, or generic profiles; or
- descriptor-independent PVL and Integrity callback behavior.

Runtime Recognition remains distinct: it establishes whether a current AgentSpace recognizes data
under its current activation and governance state. It is temporal, revocable, AgentSpace-specific,
and does not reinterpret immutable Commit validity.

## 14. Conformance scenarios

The implementation and its tests must demonstrate at least:

- a missing governing descriptor produces `NoDescriptor` and blocks Commit;
- an inherited active binding is discovered through ordinary effective relationships;
- an unbound seeded rule is not discovered;
- an active mandatory binding without a handler produces `UnsupportedValidationRule` and blocks
  Commit;
- a missing required property is assessed even when absent from the property map;
- a value-kind mismatch prevents value-type-specific rule execution;
- a local inverse cardinality violation blocks Commit; and
- a deferred cross-Space inverse does not make a successful forward Commit pending or provisional.
