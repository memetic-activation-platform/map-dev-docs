# MAP Queries

MAP query support is the design area for finding holons, navigating
relationships, filtering results, projecting output, and eventually compiling
declarative graph-query languages into executable MAP query plans.

The current design center is the storage-grounded `QueryExpression` model
captured in
[storage-grounded-query-architecture.md](storage-grounded-query-architecture.md).
Older documents in this directory may still use the previous `QueryGraph` /
`QueryStep` vocabulary while they await realignment.

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
Dance command or trusted ingress
  -> QueryDance invocation
  -> QueryDanceRequest
  -> Query
  -> root QueryExpression definition
  -> QueryExpressionExecution runtime state
  -> HolonCollection result
```

The core runtime substrate is intentionally conservative:

```text
HolonCollection -> QueryExpression -> HolonCollection
```

`Query` is the reusable query definition.
`QueryDanceRequest` is the invocation request for a query run.
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

This directory is being simplified. Some existing files still reflect earlier
stages of design thinking. The current design center is captured in
[storage-grounded-query-architecture.md](storage-grounded-query-architecture.md),
and the older query-engine design spec should be realigned before
they are treated as implementation-ready.

### [storage-grounded-query-architecture.md](storage-grounded-query-architecture.md)

Current architecture for storage-grounded MAP query execution.

This document defines:

- the relationship between `Query`, `QueryDanceRequest`, and the query tree
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

Older design spec for the executable MAP query algebra and its execution engine.
This document still reflects the pre-pivot `QueryGraph` / `QueryStep` model and
needs realignment before it should be treated as canonical again.

Its scope is the core execution engine shared by host and guest execution:

- `QueryExpression`
- `QueryDanceRequest`
- `ExecutionInstance`
- `HolonCollection` runtime semantics
- projection and materialization boundaries
- local execution rules

### [command-dance-query-schema-tdl.md](command-dance-query-schema-tdl.md)

Source-of-truth TDL schema definitions that ground the MAP query engine.

This file defines the current holon types, properties, relationships, and
inverse relationships for `Query`, `QueryDanceRequest`, `QueryExpression`,
`QueryParameterDeclaration`, `QueryParameterBinding`, `QuerySubTree`,
`ExecutionInstance`, and `QueryExpressionExecution`.

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
