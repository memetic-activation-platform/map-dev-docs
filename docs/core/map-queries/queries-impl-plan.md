# Storage-Grounded Query Engine Implementation Plan

Status: current implementation plan.

This plan delivers the descriptor-aware `QueryExpression` engine on top of the
completed storage-layer algebra. It implements the normative design in
[query-engine-design-spec.md](query-engine-design-spec.md), the schema in
[command-dance-query-schema-tdl.md](command-dance-query-schema-tdl.md), and the
storage boundary in
[storage-grounded-query-architecture.md](storage-grounded-query-architecture.md).

The loadable schema sources are not in this documentation repository. They are
owned by the corresponding package directories under
`map-holons/schema-src/`.

The previous query-plan model has been superseded. Its completed work remains
delivery history, but no new implementation should target its retired types.

## Delivery Rule

Each slice preserves this end-to-end model:

```text
Direct: Query + runtime input/bindings -> QueryExpression
  -> QueryExpressionExecution -> HolonCollection

Dance adapter: DanceInvocation -> QueryDanceRequest -> Query
  -> the same direct execution path
```

`HolonCollection` is the default operand and result carrier. Query definitions
are reusable; all input, result, status, and resolved-binding state is runtime
state. Storage is accessed only through the published storage algebra.

## Tracking Convention

Estimated Points are append-only; scope changes are dated adjustment rows.
When a planned slice is retired, superseded, or re-estimated, retain its
original tracker estimate and append a dated positive or negative adjustment
row. This preserves historical weekly estimates while making the current scope
change explicit.

## Delivery Sequence

### QRY0 — Delivered query schema extraction

QRY0 established `query/schema.tdl` and `query-dance/schema.tdl` in the
ownership-based `map-holons/schema-src/` layout. They replace the retired
Core-owned query schema source.

The new schema must use the current TDL 2.0 declaration style and depend on the
current Core schema: `MAP Query Schema-v0.0.2` depends only on
`MAP Core Schema-v0.0.7`, while Core has no dependency on Query.
It defines `Query`, `QueryExpression`, `QuerySubTree`, query parameter
declarations and bindings, `ExecutionInstance`, and
`QueryExpressionExecution`. The separate `MAP Query Dance Adapter Schema-v0.1.0`
depends on Dance, Query, and Core, and defines `QueryDance`,
`QueryDanceRequest`, and `QueryDanceResponse` using Dance's generic
`AffordsDance` / `DanceAffordedBy` affordance pair. QueryCore remains an
internal direct-execution module of `map-query-schema`; it is not a QRY0 schema
package or a public direct-caller API.

Package verification loads Core and Query in separate committed transactions;
QueryDance is then loaded after Core, Dance, and Query have each committed.
This slice did not implement query execution behavior.

### QRY1 — Query definition and runtime-state scaffold

Introduce the direct query-execution seam over the TDL-backed `Query`,
`QueryExpression`, `QuerySubTree`, `ExecutionInstance`, and
`QueryExpressionExecution` types and relationships. The Query–Dance adapter
then maps `QueryDanceRequest` into that seam and returns a `HolonCollection`
response without making the engine depend on Dance types.

This establishes the reusable-definition/runtime-execution boundary before
operator behavior is added.

### QRY2 — Descriptor-validated seed and expand

Implement `SeedHolons` and `Expand` as concrete `QueryExpression` types.
`Expand` resolves declared and inverse relationship names through effective
descriptors, validates every input endpoint, calls the storage-layer expansion
operations, and converts decoded SmartLinks into `SmartReference` collection
members. It preserves duplicate occurrences and traversal order.

### QRY3 — Parameter binding and filter

Implement reusable parameter declarations, concrete runtime bindings, and
descriptor-aware `Filter`. Validate property access, value types, and supported
operators before evaluating filters through `SmartReference` accessors.

### QRY4 — Collection transformations and projection

Implement `OrderBy`, `Distinct`, `Skip`, `Limit`, and `Project`. Keep ordering
and duplicate semantics explicit. Treat `Project` as materialization, not as a
replacement for `HolonCollection` navigation.

### QRY5 — Composite expressions and diagnostics

Implement `QuerySubTree` execution, exit merge/selection behavior owned by the
concrete parent expression, failure propagation, and stable dance diagnostics.
Ensure invalid descriptors and invalid topology produce failures rather than
empty successful results.

### QRY6 — Local execution completion and saved-query replay

Complete root-chain execution, saved-query reuse, execution-status transitions,
and runtime-record inspection. A saved query must execute repeatedly without
acquiring invocation state.

### QRY7 — Distributed coordination

Add host-coordinated continuation across `HolonSpace` boundaries while retaining
the local engine unchanged. This includes delegation, fanout tracking, and
result merge rules.

### QRY8 — Declarative compilation

Compile supported OpenCypher/GQL subsets into `Query` definitions and
`QueryExpression` trees. Add optimizer work only when it has a
correctness-preserving physical implementation.

## Guardrails

- Do not reintroduce the retired query-plan model.
- Do not place runtime state on `Query` or `QueryExpression` definitions.
- Do not bypass descriptor validation for relationship, property, value, or
  operator meaning.
- Do not bypass the storage algebra or infer unsupported access paths.
- Do not make `RowSet`, path values, or materialized projections the default
  execution carrier.
- Do not implement cross-space coordination in the shared local engine.
- Do not introduce OpenCypher/GQL semantics before the executable expression
  route is stable.

## First Implementation Issue

The next implementation issue is **QRY0 — Authoritative query schema
extraction**. QRY1 begins only after both packages load with no Core-to-Query
dependency and no Query-to-Dance dependency.

Dance is currently physically packaged by Core. Extracting it into a standalone
Dance schema package that depends on Core, removing Dance from Core bootstrap,
and updating QueryDance to import that package is a deliberate follow-on
boundary change. It is not hidden scope within QRY0.
