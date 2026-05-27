# MAP Query Architecture - Navigation Dances, HolonCollection, and ExecutionPlan (v1.5)

## Core Principle

MAP query architecture keeps runtime value shapes conservative and treats concrete navigation behavior as Dances afforded by MAP types.

`Query` is a capability area, not a required runtime object for the current implementation target.
MAP should reify more specific things when they are needed:

- navigation operation Dances
- `ExecutionPlan` holons
- `InteractiveNavigationSession` holons
- navigation operation result holons
- later `DeclarativeQuery` holons for OpenCypher/GQL text

The key synthesis is:

> Navigation operations are Dances.
> `HolonCollection` is the primary holon-oriented runtime carrier.
> `ExecutionPlan` is the HolonType for replay structure.
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
- replayable saved query plans
- descriptor-aware filtering and traversal validation
- later declarative OpenCypher and GQL compilation
- future optimization and explainability

The current architecture has two important boundaries:

- Declarative languages are authoring and interchange surfaces, not the foundational MAP execution model.
- Runtime values remain ordinary MAP runtime values; an `ExecutionPlan` holon carries symbolic structure, dependencies, derivation, and correlation-sensitive semantics only when replay, analysis, or optimization is needed.

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

    ExecutionPlan holon:
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

## 3. `ExecutionPlan` Responsibilities

`ExecutionPlan` is a MAP `HolonType`.
An execution plan instance is an `ExecutionPlan` holon whose symbolic content describes a sequence or graph of navigation operations.
Typed APIs may expose a plan facade or reference, but the plan's identity, lifecycle, and authoritative stored form are holon-backed.

An `ExecutionPlan` holon owns:

- operation dependencies
- input and output binding names
- operation-specific parameters
- source and target binding relationships
- derivation structure
- traversal provenance
- correlation-sensitive relationships between intermediate results

The plan holon itself does not contain runtime collections.
It describes how runtime values are produced and related.

The plan may begin as a simple chain for interactive navigation, but it should be allowed to become graph-shaped when needed to preserve dependencies, branching, reuse, correlation, or later optimization opportunities.

The `ExecutionPlan` HolonType is not required for the first implementation of individual navigation operation Dances.
It layers on top when MAP needs append-friendly interaction, saved-plan replay, explanation, or declarative compilation.

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

## 7. Layering Toward `ExecutionPlan`

MAP has four useful layers. They should be implemented incrementally.

### 7.1 Navigation Operation Dances

The first layer is concrete navigation operation Dances.

This layer lets DAHN and other clients navigate, filter, order, and project holon-backed results without a reified `Query` object and without waiting for saved-plan infrastructure.

### 7.2 InteractiveNavigationSession

The second layer is interactive plan construction.

`InteractiveNavigationSession` is a host-owned session holon.
It owns the live `NavigationExecutionBindings` for the session's plan execution, relates to an accumulating `ExecutionPlan` holon, and affords an `ApplyOperation` Dance.

`ApplyOperation`:

1. accepts a navigation operation intent
2. appends the corresponding operation to the session's `ExecutionPlan` holon
3. optionally executes it immediately against the session's `NavigationExecutionBindings`
4. records the output binding, result, and diagnostics

By the end of the session, MAP has both:

- live results produced by gesture-initiated operations
- a replayable `ExecutionPlan` holon representing the executed sequence

The HumanAgent may save the accumulated `ExecutionPlan` holon for later replay.
Gesture history may also be preserved as UX/provenance data, but it is distinct from the executable plan.

### 7.3 ExecutionPlan Execute Dance

The third layer is saved-plan execution.

An `ExecutionPlan` holon can afford an `Execute` Dance that replays a previously defined plan against a transaction, snapshot, or other execution scope.

This is distinct from interactive plan construction:

- interactive sessions build and optionally execute the next operation
- execution plans replay a previously defined operation structure

### 7.4 Declarative Route

The future declarative route starts from OpenCypher and later GQL.

In this route:

1. a `DeclarativeQuery` holon or equivalent document carries declarative text
2. the declarative query is parsed
3. descriptor-backed structure and value/operator semantics are resolved
4. the query is planned and optimized
5. the result is emitted as a semantically equivalent MAP `ExecutionPlan` holon

Declarative languages are compiler front ends into MAP-owned algebra.
They are not the execution engine and not the source of MAP-specific semantic authority.

### 7.5 Round-Trip Optimization Path

An interactive `ExecutionPlan` holon may later be lifted into declarative form when it falls within the OpenCypher/GQL-expressible subset.
That declarative representation can then be parsed, analyzed, and optimized back into a semantically equivalent `ExecutionPlan` holon.

This creates an eventual round-trip path:

    HumanAgent gestures
      -> faithful imperative ExecutionPlan holon
      -> OpenCypher/GQL expression
      -> optimized ExecutionPlan holon

The original gesture-built plan remains the faithful replay artifact.
The optimized plan is a derived equivalent artifact.

MAP should preserve the distinction between:

- gesture history
- original execution plan
- optional declarative expression
- optimized execution plan

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
  - keeps Dance envelopes distinct from Commands and plan/declarative artifacts

- **ExecutionPlan layer**
  - owns the `ExecutionPlan` HolonType and plan holons
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

## 9. Derived Views And Output Contracts

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

## 10. OpenCypher And GQL Compatibility

OpenCypher remains the initial declarative compatibility target.
GQL is the later standards-aligned target.

Compatibility means MAP must be able to produce the correct observable semantics for supported query surfaces.
It does not mean MAP must adopt Cypher's row stream or property-bearing relationship variable model as its foundational runtime substrate.

For example:

    MATCH (b:Book)-[:AUTHORED_BY]->(a:Author)
    RETURN b, a

This requires a row-observable result associating each book with its author.
MAP may derive that view from:

- `ExecutionPlan` topology
- relationship cache structures
- traversal provenance
- partitioned collection overlays
- pair projections

OpenCypher and GQL analysis belongs primarily in appendix/reference documents until MAP begins implementing the declarative planner.

---

## 11. Design Consequences

This architecture has several consequences:

- `HolonCollection` remains the core holon-oriented runtime carrier.
- A new foundational `BoundHolonCollection`, `RowSet`, `RecordStream`, or `GraphValue` is not introduced for the initial query substrate.
- concrete navigation behavior is implemented as Dances afforded by MAP types.
- `ExecutionPlan` is a HolonType whose holons carry symbolic structure, dependency, derivation, and replay semantics when those are needed.
- `InteractiveNavigationSession` layers immediate execution and plan append behavior on top of operation Dances.
- A reified `Query` object is not required for the current implementation target.
- Relationship traversal remains named-channel traversal.
- Relationship-specific state is modeled with holons, not property-bearing edge instances.
- Row, path, pair, partitioned, scalar, and graph-like outputs are derived views.
- Descriptor-backed semantics govern structure, relationship meaning, and value/operator meaning.
- OpenCypher/GQL support remains possible through compilation and projection boundaries.

---

## Summary

MAP should treat navigation operation Dances as the first executable layer, `HolonCollection` as the primary holon-oriented runtime carrier, `ExecutionPlan` as the HolonType for replay structure, and descriptors as the semantic authority.

The query architecture should remain small, graph-native, and faithful to existing MAP runtime structures while preserving a path toward interactive sessions, saved plans, and richer declarative query compatibility.
