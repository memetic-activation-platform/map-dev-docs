# MAP Query Support

MAP query support is the design area for finding holons, navigating relationships, filtering results, projecting output, replaying navigation, and later compiling declarative query languages into MAP execution plans.

In the current design, `Query` is not a required runtime object.
Concrete navigation behavior is implemented as descriptor-afforded Dances over MAP types such as `HolonCollection`.

The query layer exists for three practical reasons:

- A HumanAgent needs to turn interactive gestures into immediate results.
- MAP clients need a stable way to ask for data without knowing storage internals.
- Saved navigation needs an executable representation that can be replayed, inspected, optimized, or eventually generated from declarative query languages.

The first implementation target is simpler than a full query runtime:

1. implement concrete navigation operation Dances such as `Expand` and `Filter`
2. layer the `ExecutionPlan` HolonType and `ExecutionInstance`-backed interactive orchestration on top for append-and-execute interaction
3. add saved-plan execution
4. add declarative OpenCypher/GQL support later

Example:

```text
show all Books in my I-Space
  -> SeedHolons navigation operation Dance

get all authors of those Books
  -> Expand navigation operation Dance
```

Once interactive orchestration exists, those gestures can also produce:

- runtime results that can be displayed immediately
- an `ExecutionPlan` holon that can replay the same sequence later

---

## How It Works

The core runtime carrier is `HolonCollection`.

Most collection-transforming navigation operation Dances should take a `HolonCollection` and produce another `HolonCollection`:

```text
HolonCollection -> Operation -> HolonCollection
```

When an operation is captured into an `ExecutionPlan` holon, the plan names intermediate results with variables:

```text
books   -> HolonCollection
authors -> HolonCollection
```

Those names live in the `ExecutionPlan` holon, not inside the collections themselves.
During plan execution, `ExecutionInstance` maps each plan variable to its current runtime value.

Relationship traversal uses named relationship channels:

```text
Expand(input: books, relationship: Authors, direction: Outgoing, output: authors)
```

The result can be a flat author collection for ordinary navigation. If a later operation needs book-author pairs, authors grouped by book, a path trace, or a compatibility-oriented row-shaped result, MAP materializes that result type from the plan structure, relationship semantics, and execution context.

The important rule is simple:

```text
Keep runtime values small and MAP-native.
Implement concrete navigation as Dances.
Put derivation, dependency, and replay structure in an ExecutionPlan holon only when replay or analysis is needed.
Use concrete materialized result types only when an output surface needs them.
```

---

## Core Concepts

### `HolonCollection`

The primary runtime result for holon-oriented query execution.

A collection contains ordered `HolonReference`s and gives MAP enough information to continue navigating, filtering, ordering, and displaying holons.

### `ExecutionPlan`

The MAP HolonType for symbolic, replayable navigation/query workflows.

An `ExecutionPlan` holon records the operations, input variables, output variables, relationship names, predicates, ordering, limits, projections, and derivation structure needed to replay or analyze the query.

### `ExecutionInstance`

The runtime execution state for one execution of an `ExecutionPlan`.

It owns live bindings, diagnostics, execution status, and transient runtime results without embedding runtime state into the `ExecutionPlan`.

### Navigation Operation Dances

Concrete navigation behaviors afforded by MAP types.

For example, `HolonCollection` can afford collection-transforming Dances such as `Expand`, `Filter`, `OrderBy`, `Skip`, `Limit`, and `Distinct`.
Seed operations may be afforded by a space, execution domain, session, or other host-defined navigation scope.

### Relationship Channels

MAP relationships are named traversal channels, not property-bearing edge objects.

Traversal is validated by relationship name plus traversal direction, normalized onto one semantic declared/inverse relationship pair.

If relationship-specific state is needed, MAP models that state as a holon, usually through an intersection `HolonType`.

### Materialized Result Types

Rows, paths, pair views, grouped views, scalar results, and graph-like result objects are concrete materialized result types.

They are useful at projection boundaries, for correlation-sensitive gestures, for exports, and for future OpenCypher/GQL compatibility. They are not the default execution substrate.

### Descriptors

Descriptors define the legal structure and meaning of holons, properties, relationships, and value operations.

The query layer should use descriptor-backed structure to validate operations such as `Expand` and descriptor-backed value semantics to interpret filters and projections.

---

## Read The Docs In This Order

### 1. [query-arch.md](query-arch.md)

Start here for the overall architecture.

This document explains how navigation/query capabilities relate to HumanAgent gestures, Dances, Commands ingress, MAP runtime values, descriptor-owned semantics, DAHN delivery, and future declarative query surfaces.

Read it when you need to understand the big picture before touching code.

### 2. [query-algebra/query-algebra-design-spec.md](query-algebra/query-algebra-design-spec.md)

Read this next for the canonical MAP-native query algebra design.

It consolidates:

- the runtime carrier and execution model
- the initial navigation operation set
- descriptor-backed structural validation
- relationship and correlation semantics
- distributed execution rules

Read it when you need the authoritative design center for MAP query algebra.

### 3. [queries-impl-plan.md](queries-impl-plan.md)

Read this for implementation sequencing.

This is a planning document, not the design authority. Use it to translate the design specs into delivery phases and issue slices.

### 4. [declarative-query/query-planner-algebra.md](declarative-query/query-planner-algebra.md)

Read this for future declarative planner compatibility.

It explains how OpenCypher and later GQL can compile into MAP `ExecutionPlan` holons, and where richer correlation, optional matching, aggregation, union, path variables, and row-observable semantics become necessary.

This is future-facing appendix material unless you are working on declarative query compilation.

### 5. [declarative-query/cypher-operator-inventory.md](declarative-query/cypher-operator-inventory.md)

Read this as a reference catalog of OpenCypher implementation vocabulary.

It is useful for compatibility checks and future explain-plan work. It is not MAP's execution model.

---

## Mental Model

For the initial MAP query/navigation design, keep this model in your head:

```text
HumanAgent gesture or client request
  -> Command ingress where needed
  -> DanceInvocation
  -> descriptor-validated navigation operation Dance
  -> HolonCollection input where applicable
  -> HolonCollection output
  -> optional ExecutionPlan holon capture
  -> optional concrete materialized result type
```

The query layer should feel like descriptor-afforded graph navigation over MAP holons, not a property-graph database engine hidden inside MAP Core.

The long-term path still leaves room for OpenCypher and GQL. Those languages can become declarative surfaces that compile into `ExecutionPlan` holons. They do not require MAP's initial runtime to become row-stream based.

The current query doc set is intentionally small:

- [query-arch.md](query-arch.md) for the architecture overview
- [query-algebra/query-algebra-design-spec.md](query-algebra/query-algebra-design-spec.md) for the authoritative MAP-native algebra
- [queries-impl-plan.md](queries-impl-plan.md) for implementation sequencing
- `declarative-query/` for future-facing compatibility material
