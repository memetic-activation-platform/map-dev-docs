# MAP Design Spec: Dances, Descriptor Affordances, and Execution Binding v1.3

## ChangeLog

### v1.3

- incorporates the Issue 508 reset by removing row-shaped query contracts and the first-class query command seam from the target dance/query posture
- re-centers navigation and query-oriented dances on `HolonCollection`, transient projection holons, `BaseValue`, and MAP-native descriptor-backed structures
- reframes `DanceInvocation`, `DanceOutcome`, and `DanceDiagnostic` as canonical holonic contract types rather than standalone dance-specific wire envelopes
- introduces abstract `Parameter` holons and `DanceType.ParameterType` as the preferred way to specify dance-specific parameter shapes
- makes `DanceOutcome` relate back to its invocation through `OutcomeOf` and relate to produced state through `Result`
- clarifies that dance results are carried across runtime/API boundaries as `HolonReference`; produced state remains owned by `Nursery`, `TransientHolonManager`, or `HolonsCache`
- defers `DanceEvent` until a concrete event consumer, outbox, subscription surface, audit stream, or projection invalidation mechanism is specified
- documents retained old-world request/response and query traversal artifacts as deprecated compatibility surfaces only

---

**Status:** Draft  
**Author:** MAP Core / Steve Melville  
**Intent:** Specify how dances fit into the descriptor model, how dance execution binds to implementations, and how dance inputs/outputs align with MAP query/navigation data structures.  
**Scope:** Descriptor integration, dance descriptors and implementations, request/response data structures, query-algebra alignment, validation/governance, runtime dispatch, security, caching, and compatibility with existing MAP/Holochain patterns.

---

## 0) Core Synthesis

This version integrates the newer descriptor design and query design.
Version 1.3 incorporates the Issue 508 reset: row-shaped query contracts and
the first-class query command seam are removed, while a small set of old-world
relationship traversal artifacts remains only as deprecated compatibility.

The main architectural synthesis is:

> Descriptors own dance affordance semantics.  
> Dance dispatch resolves through descriptor lookup.  
> Dance execution may later bind to dynamic implementations.  
> Query/navigation dances should reuse the same `HolonCollection`-centered substrate as MAP query algebra, without introducing a new dance/query operand family.

This changes the framing of the older dance design in three important ways:

- `HolonDescriptor` is now the primary caller-facing surface for dance discovery
- dance inheritance/lookup must follow descriptor `Extends` flattening rules
- dance request/response payloads should align with the MAP-native navigation model: `HolonReference` is the primary singular holon-backed handle, `HolonCollection` is the primary plural holon-backed carrier, scalar/property values remain `BaseValue`, and projected records are transient holons described by transient or generated `HolonDescriptor`s

This doc therefore extends the descriptor design rather than competing with it.

---

## 1) Relationship to the Descriptor Design

The descriptor design already establishes:

- `InstanceDance` as a behavior family afforded by `HolonType` descriptors
- flattened inherited affordance lookup across `Extends`
- no override and no deletion
- `HolonDescriptor` as the primary instance-facing lookup surface
- static descriptor-local dispatch in the current phase

This dance design adds the next layer:

- richer dance descriptor metadata
- runtime binding of dance affordances to executable implementations
- governance and activation for executable implementations
- request/response structures for invocation

Interpretation rule:

- the descriptor design is authoritative for the existence and lookup semantics of dances
- this dance design is authoritative for how those descriptor-afforded dances are bound and invoked

That means this document must not reintroduce:

- a second global dance registry
- caller-side inheritance reconstruction
- freestanding dance semantics detached from descriptors

---

## 2) Foundational Assumptions

1. **Self-describing types**
    - All MAP types are holons described by descriptor holons.
    - Descriptor wrappers are thin typed views over `HolonReference`.
    - Structural and behavior affordances should be discovered from descriptors, not hardcoded registries.

2. **Dance ownership**
    - Dances are instance behaviors afforded by `HolonType` descriptors.
    - Effective dance lookup is inherited and flattened through descriptor `Extends`.

3. **Descriptor-local meaning**
    - `HolonDescriptor` owns effective dance discovery for a holon instance.
    - Query/operator semantics remain owned by `ValueDescriptor`, not by dance-specific code.

4. **Execution layering**
    - The current descriptor design stops at static dispatch surfaces.
    - Dynamic dance implementation loading is a future extension layer built on top of descriptor affordances.

5. **Query-algebra compatibility**
    - Navigation and query-oriented dances should exchange payloads using existing MAP runtime shared types and query/navigation binding structures where applicable.
    - The current canonical plural holon-backed carrier is `HolonCollection`.
    - `ExecutionPlan` remains a future MAP `HolonType` for replayable symbolic plans.
    - `NavigationExecutionBindings` remains a future narrow plan/session binding set.
    - Projected records should be transient holons, projected record sets should be `HolonCollection`s, and projection shape should be described by transient or generated `HolonDescriptor`s.
    - `Value`, `Row`, `RowSet`, `BoundHolonCollection`, broad query `RuntimeValue`, and standalone `Query` runtime contracts are not part of the target dance/query alignment model.
    - Dance design should not introduce a parallel family of ad hoc tabular/query result structures or new query operands.
    - Dances should invoke shared navigation/query capabilities rather than depend on a Commands-owned query runtime.

---

## 3) Conceptual Model

At the semantic level, dances are descriptor-afforded instance behaviors:

```text
(HolonTypeDescriptor) -[AffordsInstanceDance]-> (DanceDescriptor)
```

At the execution-binding level, dance affordances may be associated with executable implementations:

```text
(HolonTypeDescriptor) -[ImplementsDance]-> (DanceImplementationDescriptor)
(DanceImplementationDescriptor) -[ForDance]-> (DanceDescriptor)
```

### 3.1 Semantic vs Execution Layers

These layers must remain distinct:

| Layer                        | What It Owns                                               |
|------------------------------|------------------------------------------------------------|
| Descriptor affordance layer  | whether a type affords a dance                             |
| Implementation binding layer | what executable implementation may satisfy that dance      |
| Dispatch layer               | how a dance request is routed to a concrete implementation |
| Query/navigation layer       | what runtime carriers, future bindings, and holon-backed projection structures are exchanged |

This prevents the mistake of treating implementation binding as if it defined the existence of a dance.

### 3.2 Behavior Resolution

When the system receives a dance invocation for a target holon:

1. resolve the target holon's `HolonDescriptor`
2. resolve the effective inherited dance affordance set
3. resolve the requested `DanceDescriptor`
4. resolve the best active implementation binding for that `(descriptor, dance)` pair
5. invoke the implementation using the defined dance ABI and MAP runtime value model

This keeps dance discovery descriptor-first.

---

## 4) Dance Descriptor Model

### 4.1 Core Descriptor and Contract Holons

This design assumes or extends the following descriptor and contract holons:

- `DanceDescriptor`
- `DanceImplementationDescriptor`
- `DanceInvocation`
- `DanceOutcome`
- `DanceDiagnostic`
- abstract `Parameter`

### 4.2 `DanceDescriptor`

`DanceDescriptor` is the semantic descriptor for a single instance behavior.

It should be treated as the dance counterpart to the other descriptor wrappers in the descriptor design.

Minimal metadata:

- `dance_name`
- `display_name`
- `description`
- optional `category`
- optional `stability`

Relationships:

- `ParameterType` -> concrete `Parameter` type descriptor
- optional `ResultShape` -> `HolonType` descriptor for the result holon shape
- optional `ProducesHolonReference`
- optional `ProducesHolonCollection`
- optional `ProducesBaseValue`
- optional `ProducesSmartReferences`

Result-class markers should refer to existing MAP-native types or holon-backed projection patterns.
They should not introduce dance-specific operand categories, row-shaped result families, or a standalone query result model.

`ParameterType` is the preferred holonic replacement for a generic request
shape. Dance inputs should be represented by parameter holons rather than by a
separate dance request payload family.

### 4.3 `DanceImplementationDescriptor`

This descriptor represents a concrete executable binding for a `DanceDescriptor` on behalf of an affording type.

Suggested properties:

- `engine`
- `module`
- `entrypoint`
- `abi`
- `version`
- `compat_range`
- `activation_status`
- `scope`
- `module_hash`

Relationships:

- `ForDance` -> `DanceDescriptor`
- `ForAffordingType` -> `HolonTypeDescriptor`

---

## 5) Query-Aligned Dance Data Structures

This is the most important integration with `map-queries`.

The older dance design used generic `DanceRequest` and `DanceResponse` envelopes but did not align them to MAP's emerging query/navigation runtime carrier model.

This version does.

### 5.1 MAP-Native Runtime Alignment, Not New Operands

Dance inputs and outputs should reuse existing MAP runtime structures where appropriate.
The dance layer should not introduce a new operand family, row-shaped result family, or standalone query runtime contract for query alignment.

The relevant canonical definitions live in:

- `docs/core/type-system/runtime-shared-types.md`
- `docs/core/map-queries/simple-algebra-binding-model.md`
- `docs/core/map-queries/navigation-algebra.md`

Interpretation rule:

- `HolonReference` is the primary singular holon-backed handle
- `HolonCollection` is the primary plural holon-backed runtime carrier for current navigation/query execution
- `BaseValue` remains the scalar/property value family
- MAP-native projected records are transient holons
- MAP-native projected record sets are `HolonCollection`s
- projection shape is described by transient or generated `HolonDescriptor`s
- `ExecutionPlan` remains a future MAP `HolonType` for replayable symbolic plans
- `NavigationExecutionBindings` remains a future narrow plan/session binding set
- `Value`, `Row`, `RowSet`, `BoundHolonCollection`, broad query `RuntimeValue`, and standalone `Query` runtime contracts are removed from the target dance/query alignment model
- `SmartReference` remains appropriate where smart-link-aware behavior is contract-significant, but should not become the default plural result carrier
- this dance spec does not redefine their shape constraints
- alignment here is about contract compatibility, not about forcing one internal execution representation
- query-aligned dance execution should remain `HolonCollection`-centered where possible and materialize projected records as transient holons only when a contract, ABI, or operator requires them

### 5.2 Guidance by Dance Category

This table describes the target query-aligned posture.
The PRO1 outcome holon in section 5.6 returns results by relationship and
`HolonReference`; the table describes the state represented behind parameters
and results, not a separate dance-specific wire payload.

| Dance Category             | Preferred Input/Output Shapes                                                                                                                                                    |
|----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Scalar/transform dance     | parameter holon with `BaseValue` properties, result holon with `BaseValue` properties                                                                                            |
| Holon-local action         | `DanceInvocation.Target` + structured parameter holon, result relationship to a staged, transient, or saved holon                                                                |
| Navigation operation dance | target or parameter holon carrying `HolonReference` or `HolonCollection` state, result relationship primarily to a `HolonCollection` holon                                      |
| Projection-boundary dance  | `HolonCollection` input, projected transient holons as output, result relationship to a `HolonCollection`, projection shape described by transient or generated `HolonDescriptor` |
| Plan/session dance         | future `ExecutionPlan` or `InteractiveNavigationSession` holons where applicable, with runtime results still centered on `HolonCollection`                                      |
| Bulk dance                 | parameter holon carrying collection or list input, result relationship to `HolonCollection`, scalar-result holon, or structured holon-backed batch result according to the contract |

### 5.3 Why This Matters

This avoids three different result models for:

- query execution
- navigation dances
- DAHN-driven graph exploration

Instead:

- navigation-oriented dances can remain `HolonCollection`-centered
- projection-oriented dances can produce transient projection holons and return a `HolonCollection`
- future plan/session dances can use `NavigationExecutionBindings` and `ExecutionPlan` holons when plan-scoped binding or replay semantics are needed
- distributed query surfaces can still use `SmartReference`-oriented outputs where sovereignty requires it

It also preserves room for deferred projection:

- a dance may internally retain `HolonReference`- or `HolonCollection`-backed state
- it may materialize `BaseValue` or transient projection holons only when the ABI, result contract, or an operator boundary requires those shapes

### 5.4 Canonical Invocation and Outcome Holons (PRO1 Foundation)

The first contract-track dance slice should stabilize the canonical dance
invocation and outcome posture before descriptor-backed lookup,
dispatch-routing, runtime value alignment, and ABI finalization are fully
defined.

This PRO1 foundation owns the role boundaries between:

- dance identity
- target selection
- structured parameters
- invocation source
- structured successful results
- diagnostics
- failure reporting

The canonical dance execution posture in PRO1 is:

```text
DanceExecutionResult = Result<DanceOutcome, HolonError>
```

Interpretation rules:

- invocation failure is represented through `HolonError`
- successful execution returns `DanceOutcome`
- non-fatal diagnostics are returned with a successful outcome
- HTTP-like response status codes are not part of the canonical PRO1 contract

The canonical posture is holonic, not a new family of dance-specific wire
payloads:

- `DanceInvocation`, `DanceOutcome`, and `DanceDiagnostic` are `HolonType`s
- dance-specific parameter shapes extend the abstract `Parameter` `HolonType`
- typed Rust structs may wrap the backing `HolonReference` and provide behavior
  over the holonic state
- cross-boundary transport should reuse existing MAP holon serialization and
  deserialization rather than introduce new dance request/result wire types

### 5.5 Canonical Invocation Holon

The canonical invocation model in PRO1 is:

```text
HolonType: DanceInvocation

Properties:
  dance_name: String
  invocation_source: InvocationSource

Relationships:
  InvokesDance -> DanceType [1..1]
  Target -> HolonType [0..1]
  Parameters -> Parameter [0..1]
```

`DanceInvocation` records the fact that a dance was requested. The
relationship to `DanceType` is the authoritative executable identity; the
`dance_name` property preserves the caller-facing name for lookup,
compatibility, readability, and audit.

#### 5.5.1 Dance Identity

```text
InvokesDance -> DanceType [1..1]
dance_name: String
```

Interpretation rules:

- `InvokesDance` points to the resolved dance descriptor holon
- the relationship target type is `DanceType`, the core schema type for dance
  descriptor holons
- `dance_name` is a property on the invocation, not a replacement for the
  `InvokesDance` relationship
- executable invocation requires `InvokesDance`; pre-resolution compatibility
  ingress may still begin from a name-only request and materialize a canonical
  `DanceInvocation` before execution

#### 5.5.2 Dance Target

```text
Target -> HolonType [0..1]
```

Interpretation rules:

- target selection is distinct from dance identity
- target selection is distinct from structured parameters
- PRO1 defines only no-target and single-target posture
- multi-target invocation posture is deferred
- `HolonType` is an abstract relationship target constraint here; the
  relationship may point to any holon whose concrete descriptor extends
  `HolonType`
- the relationship does not point to an instance of abstract `HolonType`

#### 5.5.3 Dance Parameters

```text
Abstract HolonType: Parameter

DanceInvocation:
  Parameters -> Parameter [0..1]

DanceType:
  ParameterType -> Parameter [0..1]
```

Interpretation rules:

- structured dance parameters are conveyed through a parameter holon
- each concrete dance-specific parameter shape should extend `Parameter`
- `DanceType.ParameterType` declares the parameter shape expected by that dance
- if a `DanceType` declares `ParameterType`, the invocation's `Parameters`
  relationship must point to a holon described by that parameter type or an
  allowed descendant
- if a `DanceType` does not declare `ParameterType`, the invocation must not
  provide `Parameters`
- parameters are distinct from target selection
- parameter holons are normally transient or staged invocation-local state
- PRO1 does not yet define later `HolonCollection` or projected-transient-holon
  payload expansion as direct parameter payloads

#### 5.5.4 Invocation Source

```text
EnumValueType: InvocationSource

InvocationSource =
  | ClientCommand
  | TrustChannel
  | Internal
```

Interpretation rules:

- `invocation_source` distinguishes the ingress posture of the invocation
- `invocation_source` is an invocation property, not a nested context envelope
- capability, provenance, and authorization artifacts are not part of the PRO1
  `DanceInvocation` shape
- the affording type used during descriptor resolution is dispatch or audit
  metadata, not caller-supplied invocation state

Commands-originated invocation and TrustChannel-originated invocation should
both converge on this same canonical `DanceInvocation` shape.

Transition posture:

- old-world command ingress may continue using `TransactionAction::Dance(DanceRequest)`
- new-world command ingress should use `TransactionAction::DanceV2(DanceInvocation)`
  where `DanceInvocation` is a typed wrapper around holonic state rather than a
  standalone wire envelope
- this explicit dual-path posture preserves old-world and new-world isolation during transition
- after cutover, naming may be simplified again, but the transition design should not treat `DanceRequest` as if it were already the canonical new-world invocation envelope

### 5.6 Canonical Successful Outcome Holon

The canonical successful outcome model in PRO1 is:

```text
HolonType: DanceOutcome

Relationships:
  OutcomeOf -> DanceInvocation [1..1]
  Result -> HolonType [0..1]
  Diagnostics -> DanceDiagnostic [0..*]
```

#### 5.6.1 Structured Success Result

```text
Result -> HolonType [0..1]
```

Interpretation rules:

- `DanceOutcome` records which `DanceInvocation` produced it through
  `OutcomeOf`
- `Result` points to the holon that represents the successful result, if any
- across runtime/API boundaries, the result is represented by `HolonReference`
- `DanceOutcome` does not embed or own holon state directly
- produced state must live in the appropriate MAP state manager:
    - `Nursery` for staged holons
    - `TransientHolonManager` for transient holons
    - `HolonsCache` for saved holons
- full `Holon` state transfer remains an infrastructure concern such as
  guest/host synchronization or cache hydration, not the dance result contract
- `HolonType` is an abstract relationship target constraint here; `Result` may
  point to any holon whose concrete descriptor extends `HolonType`
- there is no canonical `DanceResult` payload union; any transitional helper
  named `DanceResult` should carry only the `HolonReference` for
  `DanceOutcome.Result`
- PRO1 does not require a dedicated `DanceResult` `HolonType`
- PRO1 does not retain `NodeCollection` as a canonical dance result family, though Issue 508 retained it temporarily as a deprecated compatibility surface
- PRO1 does not define `Value`, `Row`, `RowSet`, `BoundHolonCollection`, `Record`, or `RecordStream` as canonical dance result families
- collection-bearing and query-aligned result convergence is deferred to later
  work, and should reuse existing `HolonCollection` rather than introduce a new
  plural operand or row-shaped result family

#### 5.6.2 Diagnostics

```text
HolonType: DanceDiagnostic

Properties:
  severity: DanceDiagnosticSeverity
  code: String
  message: String
```

```text
EnumValueType: DanceDiagnosticSeverity

DanceDiagnosticSeverity =
  | Info
  | Warning
```

Interpretation rules:

- diagnostics are non-fatal execution notes
- diagnostics are returned only within successful outcomes
- diagnostics do not replace `HolonError`
- diagnostics should remain lightweight and machine-identifiable
- diagnostics are related to the successful outcome through
  `DanceOutcome.Diagnostics`

#### 5.6.3 Events Deferred

```text
PRO1 does not define DanceEvent.
```

Interpretation rules:

- event-like artifacts should not be added to the canonical outcome until there
  is a specified consumer, such as an outbox, subscription surface, audit
  stream, or projection invalidation mechanism
- if future work introduces dance events, they should be modeled as holons and
  related explicitly to the invocation or outcome they describe

### 5.7 Failure Reporting

Failure reporting remains `HolonError`-based.

Interpretation rules:

- `Err(HolonError)` indicates invocation failure
- `Ok(DanceOutcome)` indicates invocation success, with optional diagnostics and
  an optional result relationship
- new `HolonError` additions should remain minimal and precise
- existing general `HolonError` variants should be reused where they preserve
  sufficient meaning without undue ambiguity

### 5.8 Post-PRO1 Result Expansion

PRO1 intentionally does not finalize the canonical multi-result or query-aligned
result family.

When later dance work expands beyond PRO1's minimal success result, it should
converge on:

- `HolonCollection` for plural holon-backed results
- transient holons for projected records
- `HolonCollection` for projected record sets
- transient or generated `HolonDescriptor`s for projected record shape
- `BaseValue` for scalar/property values
- result holons that are reached through `DanceOutcome.Result`, not embedded
  payloads on `DanceOutcome`

It should not add `Value`, `Row`, `RowSet`, `BoundHolonCollection`,
`Record`, `RecordStream`, or another query-specific result union as the
new-world dance/query result family.

The important semantic constraint remains:

> Dance results should converge with MAP query/navigation runtime carriers,
> future plan/session bindings, and holon-backed projection structures rather
> than hardening a second incompatible family.

---

## 6) Validation and Query Semantics Inside Dances

The new descriptor and query designs imply a strong boundary:

- dances do not own value/operator semantics
- `ValueDescriptor` owns value validation and operator application

So if a dance needs to:

- validate input values
- apply filters
- compare values
- interpret query predicates

it should rely on descriptor-backed value semantics rather than custom per-dance logic wherever possible.

Examples:

- a search dance should use `ValueDescriptor.supports_operator()` and `apply_operator(...)`
- an edit dance should use descriptor-driven validation for candidate values
- a navigation/filter dance should compile or execute against descriptor-aware algebra rather than handwritten property predicate code

This keeps dance logic from becoming a semantic dumping ground.

---

## 7) Import and Schema Additions

### 7.1 Descriptor Relationships

The canonical relationships should align with descriptor terminology:

- `(HolonTypeDescriptor) -[AffordsInstanceDance]-> (DanceDescriptor)`
- `(HolonTypeDescriptor) -[ImplementsDance]-> (DanceImplementationDescriptor)`
- `(DanceImplementationDescriptor) -[ForDance]-> (DanceDescriptor)`

Optional:

- `(DanceDescriptor) -[ParameterType]-> (Parameter HolonType descriptor)`
- `(DanceDescriptor) -[ResultShape]-> (HolonType descriptor for the result holon)`

Canonical invocation/outcome relationships:

- `(DanceInvocation) -[InvokesDance]-> (DanceType)`
- `(DanceInvocation) -[Target]-> (HolonType abstract target constraint)`
- `(DanceInvocation) -[Parameters]-> (Parameter)`
- `(DanceOutcome) -[OutcomeOf]-> (DanceInvocation)`
- `(DanceOutcome) -[Result]-> (HolonType abstract target constraint)`
- `(DanceOutcome) -[Diagnostics]-> (DanceDiagnostic)`

### 7.2 Descriptor Inheritance Rules

Dance affordances must follow the same inheritance rules as other descriptor affordances:

- flatten across `Extends`
- no override
- no deletion
- duplicate redeclaration is invalid

This is inherited from the descriptor design and should not be restated differently elsewhere.

---

## 8) Runtime Binding and Dispatch

### 8.1 Current-Phase Compatibility

The descriptor design currently promises static, descriptor-local dispatch.

Therefore this dance design should be interpreted in two phases:

#### Phase A: Static Descriptor-Local Dispatch

- dance affordances are discovered from `HolonDescriptor`
- dispatch goes to handwritten Rust implementations
- no dynamic module loading is required

#### Phase B: Dynamic Implementation Binding

- descriptor-afforded dances are resolved to `DanceImplementationDescriptor`s
- implementations may be loaded dynamically through WASM/WASI or other engines
- governance and activation determine which implementations are active

This preserves compatibility with the current descriptor roadmap while keeping the larger dance vision intact.

### 8.2 Dispatch Algorithm

Given a canonical `DanceInvocation` holon:

1. load the `DanceInvocation` wrapper from its backing `HolonReference`
2. read `InvokesDance`, `Target`, `Parameters`, and `invocation_source`
3. if `Target` is present, resolve `target.holon_descriptor()`
4. verify that the resolved dance is effectively afforded by the target
   descriptor when target-based affordance applies
5. validate `Parameters` against the invoked `DanceType.ParameterType`
6. resolve candidate active `DanceImplementationDescriptor`s for the effective affording type
7. choose one deterministically by:
    - scope precedence
    - exact version/compatibility
    - policy eligibility
    - stable tiebreaker
8. load or reuse the executable implementation
9. invoke with the dance ABI and MAP runtime value model
10. create a `DanceOutcome` holon with `OutcomeOf`, optional `Result`, and
    optional `Diagnostics`
11. validate and return a `DanceExecutionResult`

If Phase A only is implemented, implementation resolution collapses to a
static descriptor-local dispatch table.

---

## 9) ABI

### 9.1 Goals

- stable host/implementation contract
- clear runtime value/result model
- deterministic execution
- compatibility across engines

### 9.2 Core Shape

The dance ABI should explicitly accommodate the canonical invocation and
outcome holons defined in PRO1, while preserving room for later query-aligned
`HolonCollection` and projected-transient-holon result expansion.

Inputs:

- `DanceInvocation` wrapper or `HolonReference`
- related holon state available through existing MAP state managers and
  serialization rules

Outputs:

- `Result<DanceOutcome, HolonError>`
- optional `Result` relationship from `DanceOutcome`
- optional `Diagnostics` relationships from `DanceOutcome`

Where:

- PRO1 canonical success results are represented by `DanceOutcome.Result`
- runtime/API boundaries carry the result as `HolonReference`
- `DanceOutcome` never embeds full `Holon` state
- later `HolonCollection` and projected-transient-holon expansion remains a
  subsequent layer represented by result holons

### 9.3 ABI Constraint

The ABI should not require every dance to serialize into one opaque JSON blob when stronger MAP-native runtime structures are available.

Opaque transport encoding is fine, but the semantic model should still distinguish:

- invocation failure versus successful outcome
- dance identity, target selection, parameters, and invocation source
- result relationships versus later query-aligned `HolonCollection` and projected-transient-holon result forms
- structured diagnostic outcomes

---

## 10) Validation Rules

### 10.1 Import-Time / Schema-Time

- `impl-consistency`
    - if `(T ImplementsDance impl)` then `(impl ForDance)` must refer to a dance effectively afforded by `T`
- `single-active-impl`
    - at most one active implementation for a deterministic `(affording type, dance, scope, version resolution path)` slot
- `engine-fields-required`
    - required fields vary by engine
- `descriptor-inheritance-consistency`
    - duplicate inherited dance redeclarations are invalid
- `parameter-result-shape-consistency`
    - if a dance declares `ParameterType`, invocation parameters must conform to that type
    - if a dance declares `ResultShape`, the `DanceOutcome.Result` holon must be compatible with that shape

### 10.2 Activation-Time

- `abi-compat`
- `module-integrity`
- `policy-eligibility`
- optional parameter/result-shape conformance checks

### 10.3 Runtime Semantics Checks

- query/navigation dances returning `HolonCollection` or smart-reference-bearing results should preserve the semantics promised by their declared shapes
- projected-record outputs should be represented as transient holons in a `HolonCollection`, with shape described by transient or generated `HolonDescriptor`s
- smart-reference-bearing results should appear only when the declared contract needs smart-link-aware behavior
- filter/query-oriented dances should fail on unsupported descriptor operators rather than silently reinterpret predicates
- `DanceInvocation.Parameters` must conform to `DanceType.ParameterType`
- `DanceOutcome.Result` must be a relationship to holon state owned by
  `Nursery`, `TransientHolonManager`, or `HolonsCache`, not an embedded full
  `Holon` payload

---

## 11) Security, Provenance, and Audit

The holonic invocation/outcome model means MAP does not need a separate audit
record shape just to observe dance execution. If durable audit is needed, the
runtime can retain the `DanceInvocation` and `DanceOutcome` holons, with
`DanceOutcome.OutcomeOf` linking the outcome back to the invocation that
produced it.

Every dispatch audit record, whether represented by retained holons or by a
separate operational log, should be able to recover at least:

- invocation holon
- target holon, if any
- resolved affording descriptor
- resolved `DanceDescriptor`
- resolved implementation
- module hash / builtin identity
- outcome / failure classification
- duration / resource usage

This makes it possible to distinguish:

- semantic dance identity
- concrete executable binding
- retained invocation/outcome history

which is essential once multiple implementations can satisfy one dance affordance.

Capability, provenance, and authorization models should be specified in their
own security design and then related to invocation/outcome holons explicitly.
They should not be smuggled into the PRO1 `DanceInvocation` shape as generic
optional fields.

---

## 12) Performance and Caching

Separate caches should exist for:

- holon state
- descriptor lookup/effective affordance lookup
- query/navigation runtime structures such as `ResolvedType` or planner artifacts where still used
- executable modules/instances

Important integration rule:

- dance execution caches must not obscure descriptor changes that alter effective affordances or request/result semantics

---

## 13) Compatibility and Migration

### 13.1 With the Current Descriptor Plan

Near-term rollout should be:

1. land descriptor-local dance affordance lookup on `HolonDescriptor`
2. keep execution static and Rust-local first
3. add canonical `DanceInvocation`, `DanceOutcome`, `DanceDiagnostic`, and
   abstract `Parameter` holon types
4. expose typed Rust wrappers that wrap `HolonReference` and offer behavior over
   the holonic state
5. align dance parameters and results with `HolonReference`, `HolonCollection`,
   `BaseValue`, and projected-transient-holon result patterns through parameter
   and result holons
6. introduce `DanceImplementationDescriptor` and dynamic binding later

### 13.2 With Query Architecture

Navigation and query dances should evolve toward:

- algebra-backed execution
- descriptor-aware predicate semantics
- `HolonCollection`-centered runtime behavior
- projected records as transient holons and projected record sets as `HolonCollection`s
- transient or generated `HolonDescriptor`s for projected record shape
- future `NavigationExecutionBindings` only where plan/session execution is involved
- no new foundational dance/query operand types
- shared query substrate reuse across TS invocation, trust-channel flows, and dance-initiated execution

This lets query support emerge from the same substrate rather than from a Commands-owned or query-only runtime.

---

## 14) Open Questions

- how should result-shape declarations constrain scalar-result holons,
  `HolonCollection` result holons, and projection-result holons?
- how should projected-transient-holon descriptors be generated, cached, authorized, and named at ABI boundaries?
- what is the explicit removal path for deprecated Issue 508 compatibility surfaces such as `NodeCollection`, `QueryExpression`, and `DanceType::QueryMethod`?
- should distributed query dances declare `SmartReference`-only result contracts explicitly?
- how much of dance invocation should be modeled as algebra-emitting behavior versus opaque module execution?
- what minimum host-import surface is needed for query/navigation dances versus side-effecting dances?
- what concrete event consumer would justify introducing a future `DanceEvent`
  holon type?
- what retention policy should decide when invocation/outcome holons remain
  transient, staged, or saved?

---

## 15) Acceptance Criteria

- dances are discovered from descriptor affordances, not a global registry
- effective dance lookup is inherited and flattened through descriptor semantics
- dance invocation and outcome are modeled as holons, not new standalone wire envelopes
- typed Rust dance structs wrap `HolonReference` and provide behavior over holonic state
- dance parameter/result structures align with existing MAP runtime shared types and MAP query/navigation carrier, future binding, and projected-transient-holon models
- query/filter semantics used by dances rely on descriptor-backed operator/value semantics
- dances can consume the shared query substrate without depending on Commands as the semantic owner
- dance/query alignment does not introduce a new foundational operand family
- dance outcomes relate to result holons and do not embed full `Holon` state
- new dance/query alignment does not use `Value`, `Row`, `RowSet`, `BoundHolonCollection`, broad query `RuntimeValue`, or standalone `Query` runtime contracts
- the design supports both current static descriptor-local dispatch and later dynamic implementation binding
- implementation binding, governance, and audit semantics remain explicit and deterministic

---

## 16) Next Steps

1. align core schema names and relationships with descriptor terminology:
    - `DanceDescriptor`
    - `AffordsInstanceDance`
    - `DanceImplementationDescriptor`
    - `DanceInvocation`
    - `DanceOutcome`
    - `DanceDiagnostic`
    - `Parameter`
2. implement descriptor-local dance lookup on `HolonDescriptor`
3. define the canonical dance invocation/outcome holon model and wrappers
4. align navigation/query dances with `HolonReference`, `HolonCollection`, `BaseValue`, projected transient holons, generated/transient projection descriptors, and future `NavigationExecutionBindings` where needed
5. defer dynamic module loading until after static descriptor-local dispatch is stable
6. add governance/activation and module-binding only after the descriptor-owned affordance layer is working end to end

---

## Appendix A) Dance Legacy Envelope Disposition

This appendix records the dance-specific subset of the broader runtime shared
type disposition posture.

These legacy dance envelope and payload types may remain in code during
migration and test preservation, but they are not part of the target
new-world dance contract design. The target design represents invocation and
outcome as holons and uses existing holon serialization/deserialization for
cross-boundary transport.

| Type | Classification | New-world status | Allowed use in the new world | Notes |
|---|---|---|---|---|
| `DanceInvocation` | Canonical holonic contract wrapper | Keep | New-world canonical dance invocation holon | During transition, `TransactionAction::DanceV2(DanceInvocation)` should mean a typed wrapper around holonic state, not a standalone wire envelope |
| `DanceRequest` | Deprecated legacy bridge | Deprecate | Legacy runtime and adapter compatibility only | Keep during migration, but do not preserve as the new-world dance request center |
| `DanceResponse` | Deprecated legacy bridge | Deprecate | Legacy runtime and adapter compatibility only | Keep during migration, but do not preserve as the new-world dance response center |
| `RequestBody` | Deprecated legacy bridge | Deprecate | Legacy dance payload compatibility only | Old request payload family |
| `ResponseBody` | Deprecated legacy bridge | Deprecate | Legacy dance payload compatibility only | Old response payload family |
| `HolonCollection` as a dance response body payload | Legacy envelope usage of a canonical runtime shared type | Replace envelope use | Legacy `ResponseBody` compatibility only; `HolonCollection` itself remains the canonical plural holon-backed runtime carrier | New-world query/navigation result expansion should reuse `HolonCollection` as the holon reached through `DanceOutcome.Result`; do not introduce `BoundHolonCollection` |
| `Holons(Vec<Holon>)` style response payloads | Deprecated legacy bridge | Deprecate | Legacy response compatibility only | New-world plural dance results should use `HolonCollection` or projected transient holons in a `HolonCollection` |
| `Node` | Deprecated Issue 508 compatibility surface | Retain temporarily | Existing old-world query relationship traversal flows only | Do not use for new navigation work |
| `NodeCollection` | Deprecated Issue 508 compatibility surface | Retain temporarily | Existing `query_relationships` / `fetch_all_related_holons` flows only | Not a canonical dance/query result family |
| `QueryPathMap` | Deprecated Issue 508 compatibility surface | Retain temporarily | Existing old-world query relationship traversal flows only | Not a foundation for descriptor-backed navigation |
| `QueryExpression` | Deprecated Issue 508 compatibility surface | Retain temporarily | Existing old-world query relationship traversal flows only | Do not use as the new navigation request model |
| `DanceType::QueryMethod(NodeCollection)` | Deprecated Issue 508 compatibility surface | Retain temporarily | Existing old-world query relationship traversal flows only | New navigation Dances should be descriptor-backed operations over `HolonCollection` |
| `RequestBody::QueryExpression` | Deprecated Issue 508 compatibility surface | Retain temporarily | Existing old-world query relationship traversal flows only | Do not add new callers |
| `ResponseBody::NodeCollection` | Deprecated Issue 508 compatibility surface | Retain temporarily | Existing old-world query relationship traversal flows only | Do not treat as aligned public result shape |
| `NodeWire`, `NodeCollectionWire`, `QueryPathMapWire` | Deprecated Issue 508 compatibility wire surfaces | Retain temporarily | Existing client, guest, boundary, SDK, and sweettest compatibility only | Remove when old-world relationship traversal is replaced |
| `query_relationships` / `fetch_all_related_holons` | Deprecated Issue 508 compatibility dances | Retain temporarily | Existing client, guest, boundary, builder, SDK, and sweettest flows only | New relationship navigation should be implemented as descriptor-backed Dances over `HolonCollection` |
| `Value` query-layer alias | Removed query contract artifact | Do not use | None | Use `BaseValue` for scalar/property values; do not reintroduce a query-specific `Value` operand |
| `Row` / `RowSet` | Removed query contract artifacts | Do not use | None | Projected records are transient holons; projected record sets are `HolonCollection`s |
| `BoundHolonCollection` | Removed from current dance/query alignment | Do not use | None | `HolonCollection` is the primary plural holon-backed carrier |
| broad query `RuntimeValue` / `RuntimeContext` | Removed query runtime posture | Do not use | None | Future plan/session execution should use narrow `NavigationExecutionBindings` only where needed |
