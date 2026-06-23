# MAP Queries

MAP query support is the design area for finding holons, navigating
relationships, filtering results, projecting output, and eventually compiling
declarative graph-query languages into executable MAP query plans.

The long-term intent is to support four related layers:

1. declarative query expressions, initially through OpenCypher and later GQL
2. a query optimizer that compiles declarative expressions into optimized
   `QueryGraph` plans
3. an executable `QueryGraph` made of algebraic `QueryStep`s
4. distributed, multi-space query execution over MAP's topology of nested
   belonging

Initial implementation work is focused on the third layer: executable
`QueryGraph`s and the core query algebra used by both host and guest execution.

---

## Design Center

The current design center is:

```text
Dance command or trusted ingress
  -> QueryDance invocation
  -> QueryDanceRequest
  -> QueryGraph
  -> QueryStep execution
  -> HolonCollection result
```

The core runtime substrate is intentionally conservative:

```text
HolonCollection -> QueryStep -> HolonCollection
```

`QueryGraph` is the symbolic plan.
`ExecutionInstance` is the runtime state for one execution.
`HolonCollection` is the primary runtime operand and result carrier.

Projection, paths, scalar values, row-like views, and compatibility surfaces may
be materialized when needed, but they are not the default execution substrate.

---

## Documentation Plan

This directory is being simplified. Some existing files still reflect earlier
stages of design thinking. The most recent design center is currently captured
in [graph-query-engine.md](query-engine-design-spec.md), and that thinking should be
folded into the smaller documentation set below.

### [query-arch.md](query-arch.md)

Runtime architecture for MAP query execution.

This document should stay focused on:

- the `holons_core` resident query engine that implements the `QueryDance`
- MAP client ingress through Dance Commands
- TrustChannel ingress through Dance Capsule unwrapping and Query Dance dispatch
- hApp guest-resident execution for single-space query graphs
- host-resident multi-space orchestration in the Integration Hub query engine

Detailed algebra, planner, schema, and distributed retrieval semantics belong in
the more specific docs below.

### [query-engine-design-spec.md](query-engine-design-spec.md)

Canonical design spec for the executable MAP query algebra and its execution engine.

Its scope is the core execution engine shared by host and guest execution:

- `QueryGraph`
- `QueryStep`
- `QueryStepKind`
- `QueryDanceRequest`
- `ExecutionInstance`
- `ExecutionBinding`
- `HolonCollection` runtime semantics
- projection and materialization boundaries
- local execution rules

### [command-dance-query-schema-dsl.md](command-dance-query-schema-dsl.md)

Core schema definitions that ground the MAP query engine.

This is the precise schema companion for the command, dance, query request,
query graph, query step, execution instance, and result types used by the query
runtime.

### [dist-query-concept.md](dist-query-concept.md)

Conceptual design for distributed MAP query execution.

This document explains the distributed retrieval model that emerges from MAP's
topology of nested belonging, including focal space, query horizon, host/guest
responsibilities, delegated execution, fanout, and result merging.

### [declarative-query/query-planner-algebra.md](declarative-query/query-planner-algebra.md)

Future-facing planner algebra.

This document maps declarative query calculus concepts into algebraic MAP query
operations. Its purpose is to show how OpenCypher and later GQL can compile into
MAP `QueryGraph`s without forcing the core runtime to become row-stream based.

### [declarative-query/cypher-operator-inventory.md](declarative-query/cypher-operator-inventory.md)

Comprehensive Cypher execution operator inventory.

This is a reference catalog for declarative-query compatibility and coverage
analysis. It is not MAP's execution model.

