# MAP Design Spec: Dances, Descriptor Affordances, and Execution Binding v1.1

**Status:** Draft  
**Author:** MAP Core / Steve Melville  
**Intent:** Specify how dances fit into the descriptor model, how dance execution binds to implementations, and how dance inputs/outputs align with MAP query/navigation data structures.  
**Scope:** Descriptor integration, dance descriptors and implementations, request/response data structures, query-algebra alignment, validation/governance, runtime dispatch, security, caching, and compatibility with existing MAP/Holochain patterns.

---

## 0) Core Synthesis

This version integrates the newer descriptor design and query design.

The main architectural synthesis is:

> Descriptors own dance affordance semantics.  
> Dance dispatch resolves through descriptor lookup.  
> Dance execution may later bind to dynamic implementations.  
> Query/navigation dances should use the same operand structures as MAP query algebra.

This changes the framing of the older dance design in three important ways:

- `HolonDescriptor` is now the primary caller-facing surface for dance discovery
- dance inheritance/lookup must follow descriptor `Extends` flattening rules
- dance request/response payloads should align with query/navigation data structures such as `Value`, `Row`, `RowSet`, and eventually `RecordStream`

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
   - Navigation and query-oriented dances should exchange payloads using MAP query operand structures where applicable.
   - Dance design should not introduce a parallel family of ad hoc tabular/query result structures.

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

| Layer | What It Owns |
|---|---|
| Descriptor affordance layer | whether a type affords a dance |
| Implementation binding layer | what executable implementation may satisfy that dance |
| Dispatch layer | how a dance request is routed to a concrete implementation |
| Query/navigation layer | what operand/result structures are exchanged |

This prevents the mistake of treating implementation binding as if it defined the existence of a dance.

### 3.2 Behavior Resolution

When the system receives a dance invocation for a target holon:

1. resolve the target holon's `HolonDescriptor`
2. resolve the effective inherited dance affordance set
3. resolve the requested `DanceDescriptor`
4. resolve the best active implementation binding for that `(descriptor, dance)` pair
5. invoke the implementation using the defined dance ABI and operand model

This keeps dance discovery descriptor-first.

---

## 4) Dance Descriptor Model

### 4.1 Core Descriptor Kinds

This design assumes or extends the following descriptor holons:

- `DanceDescriptor`
- `DanceImplementationDescriptor`
- optional `DanceRequestDescriptor`
- optional `DanceResultDescriptor`

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

- `RequestShape` -> request descriptor or request type
- `ResultShape` -> result descriptor or result type
- optional `ProducesRowSet`
- optional `ProducesValue`
- optional `ProducesSmartReferences`

### 4.3 `DanceImplementationDescriptor`

This descriptor represents a concrete executable binding for a `DanceDescriptor` on behalf of an affording type.

Suggested properties:

- `engine`
- `module_ref`
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

The older dance design used generic `DanceRequest` and `DanceResponse` envelopes but did not align them to MAP's emerging query/navigation operand model.

This version does.

### 5.1 Core Operand Family

Dance inputs and outputs should reuse the same conceptual operands used by MAP query/navigation layers where appropriate:

- `Value`
- `Row`
- `RowSet`
- future `Record`
- future `RecordStream`
- `SmartReference`

### 5.2 Guidance by Dance Category

| Dance Category | Preferred Input/Output Shapes |
|---|---|
| Scalar/transform dance | `Value` in, `Value` out |
| Holon-local action | target holon + structured parameters, result as `Value` or structured holon result |
| Navigation dance | target holon + navigation parameters, result as `RowSet` or `SmartReference` collection |
| Query dance | query expression or algebra plan, result as `RowSet`, later `RecordStream` |
| Bulk dance | list/collection input, result as `RowSet`, list, or structured batch result |

### 5.3 Why This Matters

This avoids three different result models for:

- query execution
- navigation dances
- DAHN-driven graph exploration

Instead:

- navigation-oriented dances can return `RowSet`
- query dances can grow naturally into `RecordStream`
- distributed query surfaces can still use `SmartReference`-oriented outputs where sovereignty requires it

### 5.4 Request Envelope

Representative invocation shape:

```text
DanceInvocation {
  dance_descriptor_ref
  affording_type_ref
  target_refs
  parameters
  context
}
```

Where:

- `target_refs` are holon references or smart references as appropriate
- `parameters` should be representable as descriptor-backed `Value` structures
- `context` contains transaction/space/capability metadata

### 5.5 Result Envelope

Representative result shape:

```text
DanceResult {
  status
  result_kind
  value?
  row_set?
  smart_references?
  events?
  diagnostics?
}
```

The important rule is not the exact field names, but the semantic constraint:

> Dance results should compose with MAP query/navigation data structures rather than inventing a second incompatible family.

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

- `(DanceDescriptor) -[RequestShape]-> (TypeDescriptor or ValueDescriptor-backed request shape)`
- `(DanceDescriptor) -[ResultShape]-> (TypeDescriptor or result descriptor)`

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

Given `(target, dance_name, ctx)`:

1. resolve `target.holon_descriptor()`
2. resolve `get_instance_dance_by_name(dance_name)`
3. resolve candidate active `DanceImplementationDescriptor`s for the effective affording type
4. choose one deterministically by:
   - scope precedence
   - exact version/compatibility
   - policy eligibility
   - stable tiebreaker
5. load or reuse the executable implementation
6. invoke with the dance ABI and operand model
7. validate and return a `DanceResult`

If Phase A only is implemented, step 3 collapses to a static descriptor-local dispatch table.

---

## 9) ABI

### 9.1 Goals

- stable host/implementation contract
- clear operand/result model
- deterministic execution
- compatibility across engines

### 9.2 Core Shape

The dance ABI should explicitly accommodate query-aligned operand structures.

Inputs:

- `dance_descriptor_ref`
- `affording_type_ref`
- `target_refs`
- `parameters`
- `context`

Outputs:

- `status`
- `result_kind`
- `value`
- `row_set`
- `smart_references`
- `events`
- `diagnostics`

### 9.3 ABI Constraint

The ABI should not require every dance to serialize into one opaque JSON blob when stronger MAP-native operand structures are available.

Opaque transport encoding is fine, but the semantic model should still distinguish:

- scalar values
- row-oriented result sets
- smart references
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
- `request-result-shape-consistency`
  - if a dance declares `ResultShape`, its ABI/result kind must be compatible with that shape

### 10.2 Activation-Time

- `abi-compat`
- `module-integrity`
- `policy-eligibility`
- optional request/result-shape conformance checks

### 10.3 Runtime Semantics Checks

- query/navigation dances returning `RowSet` or `SmartReference` collections should preserve the semantics promised by their declared shapes
- filter/query-oriented dances should fail on unsupported descriptor operators rather than silently reinterpret predicates

---

## 11) Security, Provenance, and Audit

No major conceptual changes here, but descriptor integration clarifies what is being audited.

Every dispatch should log at least:

- target holon
- resolved affording descriptor
- resolved `DanceDescriptor`
- resolved implementation
- module hash / builtin identity
- status
- duration / resource usage

This makes it possible to distinguish:

- semantic dance identity
- concrete executable binding

which is essential once multiple implementations can satisfy one dance affordance.

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
3. align dance request/result structures with query/navigation operands
4. introduce `DanceImplementationDescriptor` and dynamic binding later

### 13.2 With Query Architecture

Navigation and query dances should evolve toward:

- algebra-backed execution
- descriptor-aware predicate semantics
- `RowSet` / `RecordStream` compatible outputs

This lets query support emerge from the same substrate rather than from a separate query-only runtime.

---

## 14) Open Questions

- should `DanceDescriptor` request/result shapes point to `HolonType` descriptors, `ValueDescriptor` structures, or a dedicated request/result descriptor family?
- when should `RowSet` give way to `RecordStream` in public dance results?
- should distributed query dances declare `SmartReference`-only result contracts explicitly?
- how much of dance invocation should be modeled as algebra-emitting behavior versus opaque module execution?
- what minimum host-import surface is needed for query/navigation dances versus side-effecting dances?

---

## 15) Acceptance Criteria

- dances are discovered from descriptor affordances, not a global registry
- effective dance lookup is inherited and flattened through descriptor semantics
- dance invocation structures align with MAP query/navigation operand models
- query/filter semantics used by dances rely on descriptor-backed operator/value semantics
- the design supports both current static descriptor-local dispatch and later dynamic implementation binding
- implementation binding, governance, and audit semantics remain explicit and deterministic

---

## 16) Next Steps

1. align core schema names and relationships with descriptor terminology:
   - `DanceDescriptor`
   - `AffordsInstanceDance`
   - `DanceImplementationDescriptor`
2. implement descriptor-local dance lookup on `HolonDescriptor`
3. define the canonical dance invocation/result operand model
4. align navigation/query dances with `Value` / `Row` / `RowSet` and future `RecordStream`
5. defer dynamic module loading until after static descriptor-local dispatch is stable
6. add governance/activation and module-binding only after the descriptor-owned affordance layer is working end to end
