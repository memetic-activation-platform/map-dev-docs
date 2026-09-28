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
Direct: Query + focal HolonSpace + optional collection reference/bindings -> QueryExpression
  -> QueryExpressionExecution -> HolonCollection

Dance adapter: DanceInvocation -> QueryDanceRequest -> Query
  -> the same direct execution path
```

Collection holons are the default operand and result carrier, passed as
`HolonCollectionReference` at execution boundaries and viewed as a runtime
`HolonCollection` only when members must be inspected. Query definitions are
reusable; all focal-space context, input, result, status, and resolved-binding
state is runtime state. Storage is accessed only through the published storage
algebra.

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
operator behavior is added. It must preserve `InitialInput` collection-holon
identity through QueryCore rather than unpacking members into a replacement
carrier, and record the Dance `AffordingHolon` as the execution focal space.

### QRY2 — Descriptor-validated seed and expand

Status: delivered, including linear `Next` chaining.

Implement `SeedHolons` and `Expand` as concrete `QueryExpression` types.
`SeedHolons` is a root-only, parameterless source expression: it derives the
execution focal `HolonSpace` and performs `Expand(FocalSpace, Owns)`, preserving
traversal order and duplicates. A root `Expand` instead requires an explicit
`HolonCollectionReference`; non-root `Expand` receives its predecessor result.
QRY2 declares abstract `QueryPredicate` plus optional
`SeedHolons.SeedPredicate` and `Expand.ExpansionPredicate` as forward-compatible
payload hooks, but provides no concrete predicate form or predicate evaluation.
They are definition payloads, not collection inputs. Until predicate evaluation
is supported, each expression reached through the root or `Next` must reject
attached `SeedPredicate` or `ExpansionPredicate` payloads with
`HolonError::NotImplemented`, rather than silently return unfiltered members.
Check both attachment names by presence regardless of operator kind or attachment
count, after enforcing the root-only `SeedHolons` contract. The refused step and
instance fail without a step result or execution result; previously completed
steps retain their status and results. See the
[deferred predicate contract](query-engine-design-spec.md#deferred-predicates-ordering-and-projection).
For each source member,
`Expand` calls the existing
`HolonDescriptor::allows_relationship(requested_name)` helper, then calls the
storage-layer expansion operation using the relationship it returns. It
propagates the helper's ordinary errors rather than adding a query-specific
descriptor-validation phase, and converts decoded SmartLinks into
`SmartReference` collection members. It preserves duplicate occurrences and
traversal order.

### QRY3 — Parameter binding deferred to QRY6

Retain this identifier for tracking history. Separate parameter declarations,
invocation binding resolution, and bound/unbound saved-query behavior are now
QRY6 scope, not prerequisites for transient query authoring.

### QRY4a — Transient query authoring, ordering, and pagination

Author `Query` and concrete `QueryExpression` holons as transient definitions,
attach concrete holonic arguments, and execute through direct QueryCore and
QueryDance without staging or committing the query graph. Keep execution
status, input, and results on separate runtime execution records.

- `Expand` retains its existing concrete relationship-name argument.
- `OrderBy` relates directly to one through five `OrderBySpec` holons through
  an ordered relationship. Each spec references a `PropertyType` descriptor
  and supplies required enum properties with descriptor-defined defaults.
- `Skip` and `Limit` carry concrete nonnegative count properties on their
  expression holons, applied to the current collection's occurrence sequence.

Implement the [OrderBy contract](query-engine-design-spec.md#orderby) and
[holonic schema](command-dance-query-schema-tdl.md#orderby-spec-schema).
Use existing descriptor-backed integer/string comparison support and loaded
schema affordances; reject unsupported domains. Preserve stable ordering,
duplicate occurrences, authored chain order, collection-reference identity
between steps, and the existing failure contract.

Provide the narrowly scoped construction support needed to assemble these
transient graphs. Implement the [concrete count schema](command-dance-query-schema-tdl.md#skip-and-limit-schema)
and [pagination boundary semantics](query-engine-design-spec.md#skip-and-limit). No concrete-syntax parser or custom non-holonic
argument carrier is required.

The delivery proof is an authored transient `Expand -> OrderBy -> Skip -> Limit`
query producing expected collections through both execution routes. Cover
multiple authored argument configurations without requiring query persistence
or separate runtime binding resolution. Keep unsupported predicate attachments
rejected. `Distinct` and `Project` remain separate follow-ons.

### QRY4b — Identity-based distinctness

Implement `Distinct` over holon identity. Define duplicate identity and which
occurrence survives, preserving the relative order of retained occurrences.
Do not introduce an artificial runtime parameter where none is needed.
Property/value-based distinctness is outside this initial delivery.

### QRY4c — Projection specification and materialization

Define the projection specification and materialized output structure, then
implement `Project` with a concrete holonic projection specification attached
to the transient expression. Settle
selected property naming, materialized property values and their type
information, missing-value behavior, retained source identity if any, and how
the output fits the collection-based execution contract before implementation.

Validate property selections through descriptors. Treat `Project` as explicit
materialization, not as a replacement for `HolonCollection` navigation.

### Delivery-boundary adjustment — 2026-09-27

The initial proposal to combine QRY3 binding with QRY4a is superseded:
**QRY4a** now delivers transient authoring, ordering, and pagination;
**QRY3's runtime binding work moves to QRY6**, alongside saving and replay.
QRY4b retains identity-based distinctness and QRY4c retains projection.
QRY5–QRY8 retain their identifiers. These are intended PR boundaries; only
QRY4a's issue is currently requested. Retain original tracker estimates and
use dated adjustment rows for any later re-estimation.

### Predicate and operator foundation — Separate follow-on track

Define the operator schema and implementation before query filtering: concrete
unary, binary, and n-ary operators; effective-operator lookup from a value
type; concrete `QueryPredicate` leaves; and explicit `AllOf`, `AnyOf`, and
`Not` composition. This track also supplies programmatic construction support
for fixtures and saved query definitions.

Only after that foundation exists should query work implement predicate
evaluation and the `Filter` expression. Its planner should push eligible
expand-filter work into the guest/storage locality when possible, with an
explicit fallback or failure contract when it is not. A security-aware
`available operators` layer is later work; the initial operator API is
effective-only.

### QRY5 — Composite expressions and diagnostics

Implement `QuerySubTree` execution, exit merge/selection behavior owned by the
concrete parent expression, failure propagation, and stable dance diagnostics.
Ensure invalid descriptors and invalid topology produce failures rather than
empty successful results.

### QRY6 — Query saving, runtime parameter binding, and replay

Deliver saving of query definitions, including bound and unbound forms, and
separate runtime parameter binding formerly assigned to QRY3. Define and
implement declaration-to-binding resolution for unbound arguments without
mutating saved definitions. Reconcile concrete argument cardinalities with
valid unbound definitions and execution-ready arguments in the design/schema
contracts. Complete saved-query replay, execution-status behavior, and runtime
record inspection; preserve already delivered linear chain execution.

A saved bound query retains concrete arguments; an unbound query requires
execution-time bindings. Saving and binding are independent of authoring a
transient query with concrete arguments. Repeated execution must not add
invocation state to a saved definition.

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

## Next Implementation Issue

With QRY2 delivered, the next implementation issue is **QRY4a — Transient query
authoring, ordering, and pagination**. Ground it against the current
QueryCore, QueryDance adapter, Query schema, and descriptor comparison support.
Create QRY4b and QRY4c issues separately when requested; neither belongs in the
first issue's delivery scope.
