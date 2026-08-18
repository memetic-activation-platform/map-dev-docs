# MAP Queries

MAP query support is the design area for finding holons, navigating
relationships, filtering results, projecting output, and eventually compiling
declarative graph-query languages into executable MAP query plans.

The current design center is the storage-grounded `QueryExpression` model.
The documentation has one authority for each concern: the loadable
`map-holons/schema-src/query/schema.tdl` is Query Schema authority and
`map-holons/schema-src/query-dance/schema.tdl` is Dance adapter authority; their TDL design
companions explain the intended declarations; the query-engine design
specification defines execution semantics; the storage design
specification defines physical storage operations; and this index routes readers
to them.

The long-term intent is to support four related layers:

1. declarative query expressions, initially through OpenCypher and later GQL
2. a query optimizer that compiles declarative expressions into optimized
   `QueryTree` plans
3. an executable `QueryTree` made of algebraic `QueryExpression`s
4. distributed, multi-space query execution over MAP's topology of nested
   belonging

Initial implementation work is focused on the third layer: executable
`QueryTree`s and the core query algebra used by both host and guest execution.

---

## Design Center

The current design center is:

```text
Direct peer Rust
  -> Query with runtime input and bindings
  -> root QueryExpression definition
  -> QueryExpressionExecution runtime state
  -> HolonCollection result

Dance command or trusted ingress
  -> QueryDance adapter invocation
  -> QueryDanceRequest
  -> the same Query execution path
```

The core runtime substrate is intentionally conservative:

```text
HolonCollection -> QueryExpression -> HolonCollection
```

`Query` is the reusable query definition.
`QueryDanceRequest` is the Dance-adapter invocation request for a query run.
`QueryExpression` is the reusable executable unit in the query definition.
`QueryParameterDeclaration` is reusable definition state for accepted
parameters.
`QueryParameterBinding` is runtime state for concrete request or expression
parameter values.
`QueryExpressionExecution` is the runtime state for invoking a query expression.
`QueryTree` is the conceptual hierarchy of expression chains rooted by
`Query.RootExpression`.
`ExecutionInstance` is the runtime state for one whole-query execution.
`HolonCollection` is the primary runtime operand and result carrier.

Projection, paths, scalar values, row-like views, and compatibility surfaces may
be materialized when needed, but they are not the default execution substrate.

---

## Documentation Plan

This directory is being simplified. The current design center is captured in
[storage-grounded-query-architecture.md](storage-grounded-query-architecture.md)
and its companion execution and schema documents.

### [storage-grounded-query-architecture.md](storage-grounded-query-architecture.md)

Current architecture for storage-grounded MAP query execution.

This document defines:

- the direct `Query` execution model, Query–Dance adapter, and query tree
- `QueryExpression`
- `QueryExpressionExecution`
- `QueryParameterDeclaration`
- `QueryParameterBinding`
- `QuerySubTree`
- `QueryTree`
- concrete expression types as ordinary `QueryExpression` extensions
- composite expression execution
- Smart Link storage access-path constraints
- the current schema relationships for `Next` / `Previous` and `Subtree` /
  `Parent`

### [storage-layer-design-spec.md](../guest/storage-layer-services/storage-layer-design-spec.md)

Authoritative storage-layer and SmartLink contract.

This document defines:

- the storage/coordinator boundary
- the minimal `HolonNode` and SmartLink read algebra
- idempotent SmartLink insertion and exact deletion
- occurrence identity for duplicate-allowing relationships
- the canonical version 1 SmartLink tag format
- exact and prefix canonical-key access paths
- authoritative relationship properties and best-effort target-property caches
- typed property encoding and deterministic tag-budget packing

### [storage-layer-impl-plan.md](../guest/storage-layer-services/storage-layer-impl-plan.md)

Storage-only implementation plan for the authoritative storage and SmartLink
contract. It groups delivery into PR units for the version 1 codec and storage
algebra, exact holon retrieval, optional occurrence persistence, and retirement
of superseded persistence paths. Coordinator and reference-layer work is
explicitly excluded.

### [query-arch.md](query-arch.md)

Runtime architecture for MAP query execution.

This document should stay focused on:

- the `holons_core` resident query engine that implements the `QueryDance`
- MAP client ingress through Dance Commands
- TrustChannel ingress through Dance Capsule unwrapping and Query Dance dispatch
- hApp guest-resident execution for single-space query trees
- host-resident multi-space orchestration in the Integration Hub query engine

Detailed algebra, planner, schema, and distributed retrieval semantics belong in
the more specific docs below.

### [query-engine-design-spec.md](query-engine-design-spec.md)

Normative executable MAP query algebra and local execution semantics.

Its scope is the core execution engine shared by host and guest execution:

- `QueryExpression`
- `QueryDanceRequest`
- `ExecutionInstance`
- `HolonCollection` runtime semantics
- projection and materialization boundaries
- local execution rules

### [queries-impl-plan.md](queries-impl-plan.md)

Current delivery sequence for the storage-grounded query engine. This plan
implements the schema and execution specification in small, dependency-ordered
slices; it is not a design authority.

### [command-dance-query-schema-tdl.md](command-dance-query-schema-tdl.md)

Normative schema-design companion for the independently loadable Query Schema.

It prescribes the query-owned holon types, properties, relationships, and
inverse relationships for `Query`, `QueryExpression`,
`QueryParameterDeclaration`, `QueryParameterBinding`, `QuerySubTree`,
`ExecutionInstance`, and `QueryExpressionExecution`.

Within that package, QueryCore is the internal direct-execution module. It is
not an independently loadable schema package: executions still execute a
`Query`, and direct Rust callers enter Query rather than a generic QueryCore
API.

### [query-dance-adapter-schema-tdl.md](query-dance-adapter-schema-tdl.md)

Normative schema-design companion for the separate Query–Dance adapter. It owns
the Dance request/response surface and `HolonSpace` affordance without creating
a Core-to-Query dependency.

It depends on Dance, Query, and Core; it is a Dance implementation adapter, not
part of the Query engine. Dance extraction from the current Core package is a
follow-on boundary change.

### [dist-query-concept.md](dist-query-concept.md)

Conceptual design for distributed MAP query execution.

This document explains the distributed retrieval model that emerges from MAP's
topology of nested belonging, including focal space, query horizon, host/guest
responsibilities, delegated execution, fanout, and result merging.

### [declarative-query/query-planner-algebra.md](declarative-query/query-planner-algebra.md)

Future-facing planner algebra.

This document maps declarative query calculus concepts into algebraic MAP query
operations. Its purpose is to show how OpenCypher and later GQL can compile into
MAP `QueryTree`s without forcing the core runtime to become row-stream based.

### [declarative-query/cypher-operator-inventory.md](declarative-query/cypher-operator-inventory.md)

Comprehensive Cypher execution operator inventory.

This is a reference catalog for declarative-query compatibility and coverage
analysis. It is not MAP's execution model.
