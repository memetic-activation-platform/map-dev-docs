# MAP Runtime Shared Types (v1.5)

## ChangeLog

### v1.5

- clarifies that concrete `HolonCollectionType` makes persisted collections first-class holons that may be targeted by `HolonReference`
- clarifies that read-side resolution should increasingly exploit ordinary reference resolution of collection holons
- records that the write-side `HolonCollection` direction previously framed in Issue 541 is intentional but deferred
- specifies likely `HolonCollection` semantic accessors and states that their implementation should be pulled in on demand by concrete enhancements

### v1.4

- aligns runtime shared type terminology with the MAP Type System v2.0 design
- clarifies that runtime shared types are not descriptor roots, meta-types, or abstract type anchors
- clarifies that persisted runtime holons are described by concrete type descriptors, not by `DescriptorRoot` or abstract descriptors
- reaffirms that `BaseValue` is the scalar runtime substrate while value type descriptors carry value semantics

### v1.3

- clarifies that `ExecutionPlan` variables belong to `ExecutionPlan` holons, not to `HolonCollection`

### v1.2

- re-centers plural holon-backed results on the existing `HolonCollection`
- demotes `BoundHolonCollection` from canonical runtime shared type to deferred candidate
- clarifies that query/navigation work does not require special algebra data types such as foundational `RowSet`, `Path`, or graph result objects
- clarifies that navigation behavior is reached through Commands and Dances without mixing their envelopes

### v1.1

- adds `Focal Space` as a shared runtime context term used by commands, dances, queries, and SDK-facing interaction flows
- clarifies that focal space supplies a default runtime context without overriding explicit scopes, Home Space ownership, TrustChannel policy, or transaction boundaries

### v1.0

- establishes the canonical runtime shared type family reused across commands, dances, queries, and related pathways
- distinguishes runtime shared types from descriptors and runtime envelopes
- defines holon-backed runtime shared types centered on `HolonReference` and `HolonCollection`
- defines materialized projection and result types centered on `BaseValue`, `Row`, and `RowSet`
- narrows direct `Holon` usage to infrastructure-level full-state transfer such as cache hydration
- classifies legacy bridge and implementation-helper types in an Appendix disposition table

This document defines the canonical runtime shared types reused across higher-level MAP surfaces.

For the broader cross-layer architecture that situates runtime shared types
between integrity representations, shared objects, references, and typed core
structs, see `../holon-layered-representation-design-spec.md`.

These types are shared across surfaces such as:

- commands
- dances
- queries
- SDK-facing result shapes where appropriate

They are not the same thing as:

- descriptor types
- meta-types
- abstract type anchors
- surface-owned runtime envelopes

They also do not force every surface to use the same internal execution carrier.
For example, the current MAP query design uses `HolonCollection` as its primary internal holon result carrier while retaining scalar and row-shaped types as projection or boundary contracts.

In the MAP Type System v2.0 model, `DescriptorRoot`, TypeKind-specific
meta-types, and abstract type descriptors organize schema meaning. They are not
runtime shared carriers. When a runtime value is persisted as a holon, that
holon is described by a concrete type descriptor such as `Book.HolonType` or
`ExecutionPlan.HolonType`, never by `DescriptorRoot` or an abstract type
descriptor.

---

## 1. Core Posture

MAP runtime shared types have two coordinated subfamilies:

- primary bound runtime shared types
- secondary materialized projection and result types

The key rule is:

> Runtime shared types should be holon-bound first and projection-shaped second.

This means:

- intermediate execution should preserve identity-bearing holon-backed types as long as possible
- projection should be deferred until a contract, operator boundary, or serialization need requires it
- materialized scalar and row-shaped types remain important, but they are secondary relative to the bound side of the family

### `Focal Space`

`Focal Space` is the `HolonSpace` that provides the default runtime context for an interaction when no narrower or explicit space is supplied.

It is usually the participant's current I-Space or selected We-Space.

Focal Space is shared runtime context, not a query-only concept. It may be used by:

- commands, as the default target or interpretation context
- dances, as the default affordance discovery or execution context
- queries, as the default seed scope
- SDK-facing flows, as the current interaction space

Focal Space does not override:

- an explicit command target
- an explicit dance subject
- an explicit query `ExecutionDomain`
- a holon's Home Space
- TrustChannel policy
- transaction or snapshot boundaries

Related distinctions:

- `Focal Space` is the current default interaction context.
- `ExecutionDomain` is the set of spaces allowed to participate in a query seed operation.
- `Home Space` is the authoritative owner of a holon and its adjacency.

---

## 2. Primary Holon-Backed Runtime Shared Types

Primary holon-backed runtime shared types are the main identity-preserving runtime-carried types shared across commands, dances, navigation operation dances, and SDK-facing surfaces.

They are:

- identity-bearing
- reference-layer-aligned
- projection-deferred by default

### `HolonReference`

`HolonReference` is the foundational singular bound runtime shared type.

It is the correct opaque handle for holon-bound execution because it:

- preserves transaction-relative behavior
- hides transient vs staged vs saved distinctions
- routes reads through the correct backing implementation
- avoids exposing fetch timing to call sites

Use `HolonReference` when a runtime shared type needs to refer to a singular holon-bound object without forcing property projection.

### `HolonCollection`

`HolonCollection` is the canonical plural holon-backed runtime carrier for the current MAP implementation posture.

Because `HolonCollectionType` is now a concrete schema-recognized holon type, a persisted collection may also be the target of an ordinary `HolonReference`.

This creates an important read-side simplification opportunity:

- collection-bearing reads do not always need to be treated as bespoke plural payloads
- in many cases, a caller may resolve a `HolonReference` to a collection holon and then inflate an ergonomic `HolonCollection` view from its descriptor and related collection semantics
- collection identity, collection semantics, and collection membership can increasingly be modeled through ordinary persisted holons and relationships

This document therefore distinguishes:

- persisted collection holons, which are first-class schema-recognized holons
- `HolonCollection` as the runtime shared type used to carry or expose plural holon-backed state ergonomically in memory

MAP already defines:

```rust
pub struct HolonCollection {
    state: CollectionState,
    members: Vec<HolonReference>,
    keyed_index: BTreeMap<MapString, usize>,
}
```

This gives MAP the shape needed for holon-oriented navigation:

- collection lifecycle state
- ordered holon references
- keyed lookup
- continued navigation through `HolonReference`

Use `HolonCollection` when a runtime shared type needs to carry a plural holon-backed result without collapsing it into projected rows.

Variables, output binding names, and derivation structure should not be embedded in `HolonCollection`.
Those belong to operation intent, `ExecutionPlan` holons, `InteractiveNavigationSession`, or result holons.

### Read-Side Semantic Accessors

Some read-side callers have schema-backed expectations about collection shape and should be able to express those expectations directly rather than manually inspecting `members`.

Highly likely accessors include:

```rust
impl HolonCollection {
    pub fn expect_required_single(
        &self,
        context: CollectionContext,
    ) -> Result<&HolonReference, CollectionShapeError>;

    pub fn expect_optional_single(
        &self,
        context: CollectionContext,
    ) -> Result<Option<&HolonReference>, CollectionShapeError>;
}
```

Semantics:

- `expect_required_single(...)` succeeds only when the collection contains exactly one member and returns that member
- `expect_optional_single(...)` succeeds when the collection contains zero or one member and returns `None` or that sole member
- both accessors fail when the actual member count violates the expected shape
- errors should include enough context to identify the relationship, property, or access path that expected the shape

These accessors are appropriate where:

- the caller already has a schema-backed cardinality expectation
- the caller would otherwise index into `members` or manually inspect length
- a domain-specific invariant error is more appropriate than an incidental empty or out-of-bounds error

Examples of likely early consumers include relationships whose schema semantics already imply a single target, such as `DescribedBy`.

This document specifies these accessors as likely runtime shared API surface, but their implementation should remain on demand:

- the signatures and semantics may be specified in advance
- a concrete enhancement may pull one or more accessors into scope when it has an immediate need
- accessors should be introduced when they simplify a real call site with a real schema-backed expectation, not as speculative upfront API inventory

These accessors do not require `HolonCollection` to become an enum or trait family. They can be introduced against the existing struct representation and preserved if the internal representation evolves later.

### Relationship to Deferred Write-Side Work

Typed write-side `HolonCollection` input remains a valid future direction, but the work previously framed in Issue 541 is deferred.

This deferment is intentional:

- the blast radius of end-to-end write-side command, wire, runtime, and SDK changes is large
- the more immediate payoff from concrete `HolonCollectionType` is read-side simplification through first-class collection identity and ordinary reference resolution
- future write-side work should be reconsidered after that read-side simplification has been better explored

### `BoundHolonCollection`

`BoundHolonCollection` is a deferred candidate, not a canonical runtime shared type in the current design.

Do not introduce `BoundHolonCollection` unless a future contract needs lifecycle or semantic obligations that `HolonCollection` plus surrounding plan/session/result structure cannot represent.

Examples of future obligations that might justify a distinct type:

- a collection must itself be a persisted holon with independent lifecycle
- a collection must carry descriptor-owned collection semantics beyond membership
- a cross-surface contract needs a first-class collection reference rather than an inline collection value
- a result-set artifact must be independently shared, authorized, or versioned

Until then, named plural bindings are represented by:

- `ExecutionPlan` holon variables
- `NavigationExecutionBindings`
- `Navigation Operation` or `Dance` result metadata
- `HolonCollection` values

### `SmartReference`

`SmartReference` remains a runtime shared type where smart-link-aware behavior is contract-significant.

Use `SmartReference` directly only when the contract surface genuinely benefits from exposing:

- smart-link identity
- smart-link-cached property access
- smart-link-specific lifecycle or navigation semantics

Otherwise, prefer the broader `HolonReference`.

---

## 3. Secondary Materialized Projection and Result Types

These remain runtime shared types, but they are secondary relative to the primary bound types.

They are used when a contract, operator, ABI, or serialization boundary requires materialized projection forms.

### `BaseValue`

`BaseValue` is the canonical scalar runtime shared type.

Use `BaseValue` for:

- scalar payloads
- parameter atoms
- single field results
- explicitly materialized scalar outputs

`BaseValue` is already the MAP runtime scalar substrate, so no additional `Value` layer is introduced here.

`BaseValue` is a runtime representation, not a value type descriptor. A
property descriptor uses a `ValueType` relationship to name the semantic value
type, and the corresponding property value is carried at runtime as a
`BaseValue` variant.

### `Row`

`Row` is a single materialized row-shaped projection keyed by projection labels serialized as strings.

Keys are not descriptor-backed property identifiers in this slice.

Use `Row` when a result or parameter shape needs multiple named scalar fields in one projection object.

A `Row` is a shared materialized projection type, not necessarily the engine's primary binding representation.

### `RowSet`

`RowSet` is an ordered collection of rows.

Use `RowSet` when a contract needs a collection of row-shaped projections.

`RowSet` preserves row order but does not imply uniqueness, schema, cursoring, streaming, or planner semantics.

A `RowSet` is a materialized projection and result type, not the same thing as a plural holon-native carrier such as `HolonCollection`.

---

## 4. Restricted Runtime Shared Type

### `Holon`

`Holon` is not a general-purpose runtime shared type for new business-level cross-surface contracts.

It remains legitimate only for narrow infrastructure-level full-state transfer, especially:

- cache hydration
- internal full-state retrieval paths whose purpose is to populate in-memory cache on a cache miss

This means:

- `Holon` remains allowed where the goal is explicit infrastructure hydration
- `Holon` should not be used as the default request or result shape for general commands, dances, or queries

When a general cross-surface contract needs to expose data, the preferred choices are:

- `HolonReference`
- `HolonCollection`
- `BaseValue`
- `Row`
- `RowSet`

---

## 5. Deferred Projection Rule

The runtime shared type family preserves deferred projection explicitly.

This means:

- intermediate execution may retain `HolonReference`-backed or `HolonCollection`-backed state
- properties and relationships should be resolved through the Reference Layer and descriptor-backed structure as needed
- `BaseValue`, `Row`, and `RowSet` should be materialized only when projection, filtering, ordering, aggregation, ABI exchange, or serialization requires those forms

So:

- `Row` is a valid runtime shared type
- `RowSet` is a valid runtime shared type
- neither implies that all intermediate execution state should be eagerly row-native

---

## 6. Specialized Type Exception Rule

Higher-level surfaces should prefer the canonical runtime shared types where appropriate, but they may retain narrower specialized types where those types encode real legality or lifecycle constraints more precisely than the broader shared family.

Examples include:

- `TransientReference`
  - appropriate when an action is valid only for transient sources
- `SmartReference`
  - appropriate when an action is valid only for smart-reference-backed version lineage or smart-link semantics
- `LocalId`
  - appropriate when a local deletion or mutation action should not force the caller to first materialize a broader holon reference

This rule preserves contract precision while still minimizing the overall runtime shared type set.

---

## 7. Relationship to Runtime Envelopes

Runtime shared types are not runtime envelopes.

Runtime envelopes remain surface-owned containers such as:

- command request and response wrappers
- dance invocation and outcome wrappers
- navigation operation, execution plan, or declarative-query wrappers where those surfaces exist
- trust-channel capsules
- guest-to-hub outbound dispatch wrappers

Those envelope types should remain documented in their corresponding surface directories.

Commands, Dances, and navigation/query-related capabilities may wrap or invoke one another, but their envelopes should not be flattened into a single generic wrapper.
For example, `MapIpcRequest` is a Commands ingress wrapper, not a Dance or Query envelope.

---

## 8. Appendix: Type Disposition Table

This appendix is intentionally limited to runtime shared types and closely
related legacy or helper types that affect the shared runtime type posture.

Surface-owned envelopes and their legacy predecessors should be classified only
in their corresponding surface documents.

| Type                                | Classification                                    | New-world status              | Allowed use in the new world                                                                           | Notes                                                                                   |
|-------------------------------------|---------------------------------------------------|-------------------------------|--------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| `HolonReference`                    | Canonical runtime shared type                     | Keep                          | General-purpose singular bound type across surfaces                                                    | Primary singular bound type                                                             |
| `HolonCollection`                   | Canonical runtime shared type                     | Keep                          | General-purpose plural holon-backed result carrier                                                     | Primary plural holon-backed type                                                        |
| `BoundHolonCollection`              | Deferred candidate runtime shared type            | Defer                         | None unless a future lifecycle or contract need cannot be represented by `HolonCollection` plus plan/session/result structure | Do not introduce for PRO3 or DAHN data-type alignment                                    |
| `SmartReference`                    | Canonical runtime shared type                     | Keep, but keep scope explicit | Use directly where smart-link-aware bound behavior is contract-significant                             | Keep as first-class only where surfaces genuinely benefit from exposing it              |
| `BaseValue`                         | Canonical runtime shared type                     | Keep                          | General-purpose scalar or projection atom                                                              | Canonical scalar runtime shared type                                                    |
| `Row`                               | Canonical runtime shared type                     | Keep                          | General-purpose materialized named projection result                                                   | Secondary projection and result type                                                    |
| `RowSet`                            | Canonical runtime shared type                     | Keep                          | General-purpose materialized collection of rows                                                        | Secondary projection and result type                                                    |
| `Record`                            | Deferred canonical runtime shared type            | Defer                         | None yet                                                                                               | Future richer result family                                                             |
| `RecordStream`                      | Deferred canonical runtime shared type            | Defer                         | None yet                                                                                               | Future streaming result family                                                          |
| `Holon`                             | Restricted canonical runtime shared type          | Keep, but narrowly            | Internal full-state transfer, especially cache hydration and tightly scoped infrastructure retrieval   | Not a general-purpose cross-surface business type                                       |
| `Vec<HolonReference>`               | Implementation helper                             | Keep internally only          | Low-level internal collection handling                                                                 | Not a canonical cross-surface runtime shared type                                       |
