# MAP Query Architecture - Navigation Dances, HolonCollection, and QueryGraph (v1.6)

## Core Principle

MAP query architecture keeps runtime value shapes conservative and treats concrete navigation behavior as Dances afforded by MAP types.

`Query` is a capability area, not a required runtime object for the current implementation target.
MAP should reify more specific things when they are needed:

- navigation operation Dances
- `QueryGraph` holons
- `InteractiveNavigationSession` holons
- navigation operation result holons
- later `DeclarativeQuery` holons for OpenCypher/GQL text

The key synthesis is:

> Navigation operations are Dances.
> `HolonCollection` is the primary holon-oriented runtime carrier.
> `QueryGraph` is the HolonType for symbolic query structure and replay.
> Descriptors are the semantic source of query structure and value/operator meaning.

This means MAP navigation/query support should not default to a row-stream, graph-value, generalized result-object substrate, or special query envelope.
Core holon-oriented execution should remain closed over existing MAP runtime structures wherever possible:

    HolonCollection -> Operation -> HolonCollection

Additional result views are derived only when required by an operation, dance outcome, projection surface, or output contract.
Examples include scalar collections, projection results, partitioned collections, pair views, traversal traces, path collections, and row-oriented projections for OpenCypher/GQL-compatible result surfaces.

---

## 1. Architectural Positioning

MAP query support is the host-owned capability area for graph-native read, navigation, and future declarative query behavior.

It is designed to support:

- interactive HumanAgent navigation
- DAHN-guided exploration
- descriptor-afforded navigation operation Dances
- replayable saved query graphs
- descriptor-aware filtering and traversal validation
- later declarative OpenCypher and GQL compilation
- future optimization and explainability

The current architecture has two important boundaries:

- Declarative languages are authoring and interchange surfaces, not the foundational MAP execution model.
- Runtime values remain ordinary MAP runtime values; a `QueryGraph` holon carries symbolic structure, dependencies, derivation, and correlation-sensitive semantics only when capture, replay, analysis, delegation, or optimization is needed.

---

## 2. Runtime Carrier Model

`HolonCollection` is the core runtime carrier for holon-oriented query execution.

The MAP runtime already defines a collection shape with:

- collection state
- ordered `HolonReference` members
- keyed indexing
- navigable references to full holons

Query architecture should reuse that existing carrier rather than introduce a new foundational plural holon type such as `BoundHolonCollection` or `BoundHolonSet`.

Variables are plan-level symbolic names.
They are not embedded inside `HolonCollection`.

Conceptually:

    QueryGraph holon:
      Expand {
        input: "books",
        relationship: Authors,
        output: "authors"
      }

    NavigationExecutionBindings:
      "books" -> HolonCollection
      "authors" -> HolonCollection

`NavigationExecutionBindings` maps plan variables to runtime values produced during execution.
Initially, `HolonCollection` should be sufficient for the core holon-oriented algebra.
Other runtime values should be added only when an operation or contract actually requires them.

---

## 3. `QueryGraph` Responsibilities

`QueryGraph` is a MAP `HolonType`.
A query graph instance is a `QueryGraph` holon whose symbolic content describes a sequence or graph of navigation operations.
Typed APIs may expose a graph facade or reference, but the graph's identity, lifecycle, and authoritative stored form are holon-backed.

A `QueryGraph` holon owns:

- operation dependencies
- input and output binding names
- operation-specific parameters
- source and target binding relationships
- derivation structure
- traversal provenance
- correlation-sensitive relationships between intermediate results

A `QueryGraph` holon does not contain runtime collections.
It describes how runtime values are produced and related.

The graph may begin as a simple chain for interactive navigation, but it should be allowed to become graph-shaped when needed to preserve dependencies, branching, reuse, correlation, delegation, or later optimization opportunities.

`QueryStep` and `QueryGraph` may be introduced early without turning the initial query layer into a planner-first system.
The near-term model can remain simple:

- individual navigation operation Dances remain the first executable behavior surface
- each Dance may correspond to a `QueryStep`
- a `QueryGraph` may initially be a straightforward recorded chain or small graph of those steps
- immediate execution may remain naive and stepwise even when query structure is captured

This allows MAP to gain saved-query structure and sub-graph delegation units earlier without requiring declarative query expression or full query optimization.

---

## 4. Navigation Operation Dances

Concrete navigation operations are Dances afforded by MAP types.

Collection-transforming operations are naturally afforded by `HolonCollection`, for example:

- `Expand`
- `Filter`
- `OrderBy`
- `Skip`
- `Limit`
- `Distinct`
- projection-oriented operations where a dance outcome needs a shaped view

Seed operations are different because they create an initial collection.
They may be afforded by:

- `HolonSpace`
- focal-space context
- execution-domain context
- `InteractiveNavigationSession`
- another host-defined navigation scope

This makes query/navigation behavior consistent with the broader MAP descriptor model.
Operations are not special "query methods" hidden behind a query engine; they are affordances discovered and invoked like other Dances.

---

## 5. Relationship And Correlation Model

MAP relationships are named traversal channels, not general property-bearing edge instances.

A relationship expansion is best understood as:

    Expand(source_collection, relationship_name) -> target_collection

The relationship name identifies traversal semantics.
It does not imply an independent property-bearing relationship object flowing through the algebra.

MAP already has graph-shaped relationship structures that can preserve source-to-target correlation.
`RelationshipMap` and `RelationshipCache` are the current runtime examples of this shape:

    source_holon
      -> relationship_name
        -> target_collection

For example:

    Book1
      -> Authors
        -> [AuthorA, AuthorB]

    Book2
      -> Authors
        -> [AuthorC]

This structure can support multiple derived views:

- flat collection: `[AuthorA, AuthorB, AuthorC]`
- partitioned collection: `Book1 -> [AuthorA, AuthorB]`, `Book2 -> [AuthorC]`
- pair view: `(Book1, AuthorA)`, `(Book1, AuthorB)`, `(Book2, AuthorC)`
- row-oriented projection for Cypher-compatible `RETURN b, a`

The default runtime result may stay flat when the gesture or operation only needs a target collection.
Correlation-sensitive views should be derived when query semantics require them.

When relationship-specific state is needed, MAP should model that state as an intersection `HolonType`.
State-bearing semantic things should remain holons.

For example:

    Person - HAS_MEMBERSHIP -> Membership
    Membership - MEMBER_OF -> Organization

The `Membership` holon can carry properties such as role, since, status, permissions, provenance, or lifecycle state.

---

## 6. Descriptor-Owned Semantics

Query execution should not become the semantic owner of property, relationship, or value/operator meaning.

Descriptors own semantic interpretation:

- `HolonDescriptor` owns effective structural lookup.
- `RelationshipDescriptor` owns relationship-channel meaning.
- `PropertyDescriptor` bridges property names to value semantics.
- `ValueDescriptor` owns validation and operator compatibility.

Navigation operation Dances execute operations.
Descriptors explain what those operations mean.

Examples:

- `Expand` should validate relationship-channel legality through descriptor-backed effective relationship lookup.
- `Filter` should use descriptor-backed value/operator semantics where typed values are involved.
- Inheritance flattening should come from descriptor-backed structure, not caller reconstruction.
- Relationship navigation should preserve declared and inverse relationship meaning.

This prevents a split where validation and DAHN behavior become descriptor-driven while navigation/query semantics drift into a parallel handwritten rule system.

---

## 7. Layering Toward `QueryGraph`

MAP has four useful layers. They should be implemented incrementally.

### 7.1 Navigation Operation Dances

The first layer is concrete navigation operation Dances.

This layer lets DAHN and other clients navigate, filter, order, and project holon-backed results without a reified `Query` object.
Near-term implementations may still execute naively one Dance at a time.

### 7.2 `QueryStep` And `QueryGraph`

The second layer is early symbolic query-structure capture.

`QueryStep` is the symbolic node for one navigation operation.
`QueryGraph` is the graph-shaped symbolic artifact that relates those steps.

This layer may be introduced earlier than full interactive orchestration.
It is intentionally lightweight:

- a Dance invocation may optionally emit a corresponding `QueryStep`
- a host-owned flow may append that step to a `QueryGraph`
- the resulting `QueryGraph` may remain a simple chain at first
- immediate execution may still be performed naively step by step
- saved queries become possible without waiting for declarative parsing or a general optimizer
- sub-graphs become the natural units for later delegation and optimization

At this stage, MAP can have both:

- live results produced by immediate operation execution
- a replayable `QueryGraph` holon representing the same symbolic sequence or graph

Gesture history may also be preserved as UX/provenance data, but it is distinct from the executable query graph.

### 7.3 Interactive Execution Orchestration And Replay

The third layer adds explicit runtime orchestration and replay.

At this point MAP introduces or stabilizes `ExecutionInstance` as the runtime execution state for one execution of a `QueryGraph`.
A `QueryGraph` holon can afford an `Execute` Dance that replays a previously defined query graph against a transaction, snapshot, or other execution scope.

This is distinct from early query-structure capture:

- lightweight capture records the symbolic structure of operations
- orchestration and replay manage bindings, status, diagnostics, and repeated execution of that structure

### 7.4 Declarative Route

The future declarative route starts from OpenCypher and later GQL.

In this route:

1. a `DeclarativeQuery` holon or equivalent document carries declarative text
2. the declarative query is parsed
3. descriptor-backed structure and value/operator semantics are resolved
4. the query is planned and optimized
5. the result is emitted as a semantically equivalent MAP `QueryGraph` holon

Declarative languages are compiler front ends into MAP-owned algebra.
They are not the execution engine and not the source of MAP-specific semantic authority.

### 7.5 Round-Trip Optimization Path

An interactive `QueryGraph` holon may later be lifted into declarative form when it falls within the OpenCypher/GQL-expressible subset.
That declarative representation can then be parsed, analyzed, and optimized back into a semantically equivalent `QueryGraph` holon.

This creates an eventual round-trip path:

    HumanAgent gestures
      -> faithful imperative QueryGraph holon
      -> OpenCypher/GQL expression
      -> optimized QueryGraph holon

The original gesture-built plan remains the faithful replay artifact.
The optimized plan is a derived equivalent artifact.

MAP should preserve the distinction between:

- gesture history
- original query graph
- optional declarative expression
- optimized query graph

---

## 8. Ingress And Boundary Responsibilities

MAP navigation/query behavior may be reached through multiple ingress surfaces:

- TypeScript SDK calls
- Commands dispatch through `MapIpcRequest`
- Dance invocation
- future non-TS or trust-channel-aware entrypoints
- internal system and tooling flows

Those surfaces do not collapse into a single generic query envelope.
Each layer keeps its own envelope and semantic owner.

The responsibility split is:

- **TypeScript SDK layer**
  - owns ergonomic client-facing APIs for DAHN and other TS consumers
  - calls Commands and Dance invocation surfaces
  - does not own navigation semantics or execution behavior

- **Commands ingress layer**
  - owns client-to-host invocation for TS callers
  - uses `MapIpcRequest` for Commands ingress only
  - can carry a Dance invocation
  - does not become the architectural home of navigation/query behavior

- **Dance layer**
  - owns invocation of descriptor-afforded behavior
  - includes navigation operation Dances and later `InteractiveNavigationSession.ApplyOperation`
  - keeps Dance envelopes distinct from Commands and query-graph/declarative artifacts

- **QueryGraph layer**
  - owns the `QueryGraph` HolonType and query-graph holons
  - can afford `Execute`
  - executes against a supplied transaction, snapshot, or session context
  - is not required for every immediate navigation operation

- **Boundary / wire layer**
  - owns serialization, transport-safe shapes, and binding across process or host boundaries
  - remains distinct from semantics and execution logic

- **hApp graph access**
  - may provide storage and graph-access primitives
  - does not own logical query semantics, ordering, pagination, projection, or optimization semantics

---

## 9. Delegable Sub-Graphs

MAP should reason about pushdown and delegation in terms of equivalent query sub-graphs rather than isolated navigation operations.

A delegable sub-graph is a connected fragment of a `QueryGraph` or immediate navigation sequence whose semantics remain MAP-owned even if a lower layer performs the physical execution.

The ownership split is:

- MAP descriptors, navigation algebra, and execution planning own the meaning of the sub-graph
- the host decides whether a sub-graph is delegated, partially delegated, or executed locally
- a guest, storage adapter, or graph-access layer may execute an equivalent fragment without becoming the semantic authority

This preserves the core rule that hApp graph access and other lower layers may provide graph-access primitives, but do not redefine MAP relationship meaning, predicate meaning, ordering rules, pagination semantics, projection semantics, or optimization semantics.

### 9.1 Delegation Criteria

A sub-graph is delegable only when the host can establish that the lower layer can execute an equivalent fragment while preserving MAP semantics.

Typical criteria include:

- descriptor-backed relationship legality is preserved for every delegated `Expand`
- descriptor-backed property and value/operator semantics are preserved for every delegated `Filter`
- the lower layer can preserve the required `HolonCollection`-centered result shape or another explicitly authorized boundary result shape
- any required ordering, distinctness, skip, or limit behavior is either preserved exactly or retained in the host-owned remainder of the plan
- the delegated fragment preserves the required transaction, snapshot, execution-domain, and trust-boundary context
- the host can retain enough provenance, diagnostics, and correlation information to explain and continue execution of the remaining plan

### 9.2 Guardrails

Delegation should not be treated as semantic transfer.

The following guardrails apply:

- do not delegate a fragment if the lower layer would need to reinterpret descriptor semantics instead of applying them faithfully
- do not delegate a fragment if the only available lower-layer behavior is similar but not equivalent to MAP's declared relationship or predicate semantics
- do not force row-oriented, graph-valued, or relationship-object foundational carriers merely to make delegation possible
- do not treat storage-local execution as authority for MAP ordering, pagination, projection, or optimization rules unless exact equivalence has been established
- do not let boundary transport shapes become the semantic model of the algebra
- keep the original host-visible sub-graph and the delegated equivalent fragment distinguishable for provenance, explanation, and fallback execution

### 9.3 Worked Example

Consider the navigation sequence:

```text
SeedHolons
  -> Filter(type = Book AND title contains "Emerging World")
  -> Expand(Authors, Outgoing)
```

The host should treat this as a candidate delegable sub-graph rather than as three unrelated operations.

The naive physical plan would be:

```text
host:
  SeedHolons(all holons in scope)
  -> materialize large HolonCollection
  -> Filter(...)
  -> Expand(Authors, Outgoing)
```

That plan may move far more data than necessary into the host.

If the host can prove semantic equivalence, it may instead delegate an equivalent fragment downward:

```text
host-owned logical sub-graph:
  SeedHolons
    -> Filter(type = Book AND title contains "Emerging World")
    -> Expand(Authors, Outgoing)

delegated physical fragment:
  lower layer executes an equivalent seed/filter/expand fragment
  -> returns the resulting author HolonCollection
  -> plus any required references, diagnostics, or provenance handles
```

The meaning of the operations still comes from MAP:

- `SeedHolons` still means seeding within the host-supplied execution domain
- `Filter` still means MAP descriptor-backed predicate evaluation
- `Expand(Authors, Outgoing)` still means MAP descriptor-validated traversal of the named relationship channel

The lower layer is only the execution site for an equivalent fragment.
If equivalence cannot be established, the host must execute all or part of the sub-graph itself.

---

## 10. Derived Views And Output Contracts

The core runtime should not default to:

    RowSet -> Operation -> RowSet

It should default to:

    HolonCollection -> Operation -> HolonCollection

Derived views are introduced only where required.

Examples:

- scalar values for counts and aggregations
- scalar collections for projected property values
- partitioned collections for grouped navigation results
- pair views for source-target correlation
- traversal traces for provenance and visualization
- path collections for OpenCypher path variables
- row-oriented projections for tabular or Cypher-compatible result surfaces

This lets MAP remain graph-native internally while still producing row-observable or path-observable results when a query surface requires them.

Derived views should preserve snapshot or transaction context where recomputation would otherwise be ambiguous.

---

## 11. OpenCypher And GQL Compatibility

OpenCypher remains the initial declarative compatibility target.
GQL is the later standards-aligned target.

Compatibility means MAP must be able to produce the correct observable semantics for supported query surfaces.
It does not mean MAP must adopt Cypher's row stream or property-bearing relationship variable model as its foundational runtime substrate.

For example:

    MATCH (b:Book)-[:AUTHORED_BY]->(a:Author)
    RETURN b, a

This requires a row-observable result associating each book with its author.
MAP may derive that view from:

- `QueryGraph` topology
- relationship cache structures
- traversal provenance
- partitioned collection overlays
- pair projections

OpenCypher and GQL analysis belongs primarily in appendix/reference documents until MAP begins implementing the declarative planner.

---

## 12. Design Consequences

This architecture has several consequences:

- `HolonCollection` remains the core holon-oriented runtime carrier.
- A new foundational `BoundHolonCollection`, `RowSet`, `RecordStream`, or `GraphValue` is not introduced for the initial query substrate.
- concrete navigation behavior is implemented as Dances afforded by MAP types.
- `QueryGraph` is a HolonType whose holons carry symbolic structure, dependency, derivation, delegation, and replay semantics when those are needed.
- lightweight `QueryStep` / `QueryGraph` capture may be introduced before full orchestration or optimization.
- `InteractiveNavigationSession` may later layer richer session behavior on top of operation Dances and query-graph capture.
- A reified `Query` object is not required for the current implementation target.
- Relationship traversal remains named-channel traversal.
- Relationship-specific state is modeled with holons, not property-bearing edge instances.
- Row, path, pair, partitioned, scalar, and graph-like outputs are derived views.
- Descriptor-backed semantics govern structure, relationship meaning, and value/operator meaning.
- OpenCypher/GQL support remains possible through compilation and projection boundaries.

---

## Summary

MAP should treat navigation operation Dances as the first executable layer, `HolonCollection` as the primary holon-oriented runtime carrier, `QueryGraph` as the HolonType for symbolic query structure and replay, and descriptors as the semantic authority.

The query architecture should remain small, graph-native, and faithful to existing MAP runtime structures while preserving a path toward interactive sessions, saved query graphs, and richer declarative query compatibility.
