# Binding Layer Foundation

This document defines the missing intermediate representational layer for MAP query execution.

`Value`, `Row`, and `RowSet` remain important shared contract and projection shapes, but they are not the primary execution-time substrate for deferred-projection query work.

The primary intermediate representational layer is the Binding Layer.

This slice is intentionally foundational. It does not finalize planner behavior, declarative compilation, predicate legality, distributed execution, or the final public `Record` / `RecordStream` model.

---

## 1. Purpose

The Binding Layer exists to make MAP query execution align with the affordances already provided by the Reference Layer and Core Shared Objects.

In particular:

- `HolonReference` already hides whether a target holon is transient, staged, or saved
- property access is already transparently deferred through `SmartReference` and `HolonsCache`
- relationship access is already transparently deferred through relationship-cache-backed traversal
- query execution therefore should not prescribe fetch points or force early field projection merely to carry intermediate state forward

The Binding Layer is the execution-time home for named intermediate bindings while projection remains deferred.

---

## 2. Core Principle

> Intermediate query execution should preserve identity-bearing holon-backed bindings as long as possible and materialize projected values or rows only when a contract, operator boundary, or serialization need requires it.

This means:

- variables should bind to holon-backed execution objects rather than to eagerly projected field maps whenever possible
- structural and value access should flow through descriptor-backed lookup and the Reference Layer
- the query runtime should reuse MAP-native lazy property and relationship access instead of inventing a second eager materialization model

---

## 3. Relationship to Shared Operands

The shared operand family foundation defines:

- `Value`
- `Row`
- `RowSet`

Those remain valid and useful.

But their role is narrower:

- they are materialized contract, projection, and serialized-result shapes
- they are not, by themselves, the canonical internal representation of intermediate query bindings

The relationship is therefore:

- Binding Layer first
- projection/materialization second

Typical flow:

```text
Holon-backed bindings
        ↓
descriptor-backed interrogation as needed
        ↓
materialized Value / Row / RowSet only at explicit projection, operator, ABI, or serialization boundaries
```

---

## 4. Binding Layer Alignment with the Reference Layer

The Binding Layer should be tuned to the real MAP substrate rather than to a generic graph-engine runtime.

### 4.1 `HolonReference` as the Base Handle

`HolonReference` is already the correct opaque handle for query-time holon identity because it:

- preserves transaction-relative behavior
- hides transient vs staged vs saved phase distinctions
- routes property access through the correct backing implementation
- avoids exposing fetch timing to call sites

The Binding Layer should build on `HolonReference`, not replace it.

### 4.2 Deferred Property Access

For saved holons:

- `SmartReference` may satisfy property reads from its own cached property subset
- if a requested property is not cached in the smart reference, it may obtain the backing holon through `HolonsCache`
- the backing holon is fetched only if not already cached

This is already deferred projection in practice.

The Binding Layer should preserve this behavior by avoiding eager projection of properties into standalone row fields unless an operator or contract explicitly requires those fields.

### 4.3 Deferred Relationship Access

Relationship access should remain compatible with MAP's relationship cache posture:

- fetched relationships are cached
- fetched relationship results are collections of `SmartReference`s
- query call sites should not hardcode fetch boundaries just to preserve intermediate navigation state

---

## 5. Primary Intermediate Units

The Binding Layer should treat bound holon-shaped objects as the primary intermediate units.

### 5.1 Singular Binding

A singular binding is a named binding to a holon-backed execution object, typically reachable through `HolonReference`.

### 5.2 Collection Binding

MAP already defines `HolonCollection` as an unbound Rust runtime container (`Vec<HolonReference>`).

The Binding Layer needs a distinct concept for a named collection binding.

Current design candidate:

- `BoundHolonCollection`

This avoids overloading the existing `HolonCollection` type name while making explicit that the collection is not just a vector, but a named query-time binding object.

---

## 6. `BoundHolonCollection`

`BoundHolonCollection` is the current candidate for the primary plural binding object.

### 6.1 High-Level Posture

A `BoundHolonCollection` should be treated as a first-class holon that:

- is itself referenced through `HolonReference`
- may be transient and execution-scoped
- may still be described by a descriptor holon
- participates in the same phase-hiding and deferred-access behavior as other holons

This gives the Binding Layer a MAP-native plural unit without inventing a second non-holonic identity system.

### 6.2 Candidate Structural Shape

Candidate structure for a `BoundHolonCollection` instance:

- optional `variable_name` instance property
- `ItemType -> HolonType` relationship pointing to the descriptor for the member holon type
- `Members -> HolonReference`-oriented membership relationship

This shape may evolve, but the architectural point is stable:

- collection bindings should remain holon-centered
- variable identity belongs to the binding object
- item-type semantics remain descriptor-aware

### 6.3 Why This Matters

If collection bindings are first-class holons, then singular and plural bindings can share the same reference-layer substrate:

- singular bound thing -> holon-backed
- plural bound thing -> collection holon-backed

This greatly reduces pressure to encode intermediate query state as projected rows.

---

## 7. Navigation Semantics

Relationship navigation from a `BoundHolonCollection` should yield another `BoundHolonCollection` when the navigated relationship is plural in effect.

Example:

- `B` is a `BoundHolonCollection` of books
- `B.ReviewedBy` yields a `BoundHolonCollection` of persons who reviewed any member of `B`

This result may denote the union of reachable reviewers while still preserving provenance implicitly, because:

- the members remain real holons reachable through `HolonReference`
- those holons still know their own relationships
- provenance is recoverable through the underlying graph rather than having to be flattened into row payloads

This is one of the major advantages of a holon-bound Binding Layer over an eagerly projected row-native intermediate model.

---

## 8. Relationship to Declarative Query Languages

MAP still intends to support OpenCypher first and then GQL.

This Binding Layer should not be read as rejecting that direction.

Instead:

- declarative languages compile into MAP query algebra
- the logical semantics remain compatible with declarative query expectations
- MAP is free to use a more substrate-aware physical/intermediate execution model beneath that logical layer

The Binding Layer is therefore a MAP-native execution substrate choice, not a rejection of declarative compatibility.

Guardrail:

- MAP should avoid letting physical binding conveniences silently redefine the logical semantics expected by OpenCypher or GQL compilation

---

## 9. Boundaries

- This document defines the primary intermediate representational layer for deferred-projection query execution.
- It does not redefine `Value`, `Row`, or `RowSet`.
- It does not require immediate replacement of the legacy query/navigation module.
- It does not finalize whether future declarative-facing logical records should be named `Record`, `BindingContext`, or `RecordStream`.
- It does not finalize every structural detail of `BoundHolonCollection`.
- It does make explicit that intermediate query execution should not be modeled as if eager row projection were the default substrate.

---

## 10. Immediate Implications

Near-term query work should read this foundation as implying:

- descriptor-backed structural access should serve holon-bound execution state first, not only projected row state
- shared operand-family shapes should be treated as projection/result forms
- navigation algebra should preserve room for holon-bound intermediate bindings
- query envelope and contract work should avoid overclaiming that `Value` / `Row` / `RowSet` are the full internal query model

---

## 11. Forward Compatibility

This foundation leaves room for later work on:

- a clearer logical record/binding-stream model for declarative compilation
- explicit projection operators that convert bound holon state into `Value`, `Row`, `RowSet`, and later `Record` / `RecordStream`
- descriptor-owned predicate evaluation over holon-bound execution state
- provenance-aware path or relationship bindings if later phases require them explicitly

The key correction introduced here is simple:

> The Binding Layer is primary.  
> Shared projected operands are secondary materialization forms.
