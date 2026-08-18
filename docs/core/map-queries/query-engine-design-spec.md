# MAP Descriptor-Aware Query Engine Design Specification

Status: normative execution semantics for the storage-grounded query model.

This specification defines how MAP executes a saved query definition. The
independently loadable Query Schema is
`map-holons/schema-src/query/schema.tdl`; its Dance adapter is
`map-holons/schema-src/query-dance/schema.tdl`.
The [query schema design companion](command-dance-query-schema-tdl.md) and
[adapter design companion](query-dance-adapter-schema-tdl.md) prescribe their
respective declarations. The
[storage-grounded query architecture](storage-grounded-query-architecture.md)
defines query-tree topology and the boundary to the storage algebra. The
[storage-layer design specification](../guest/storage-layer-services/storage-layer-design-spec.md)
is authoritative for SmartLink encoding and storage operations.

## Purpose

MAP query execution is descriptor-aware graph navigation over holons. It is not
a separate property-graph engine, and it does not make a row stream its default
runtime carrier.

The initial execution algebra is deliberately narrow:

```text
HolonCollection -> QueryExpression -> HolonCollection
```

`HolonReference` preserves identity and deferred access. Materialized scalar,
projection, path, correlation, and row-like values are introduced only where a
concrete expression or compatibility surface requires them.

## Normative Execution Model

The Query engine executes a reusable `Query` directly. A peer Rust caller may
supply its initial `HolonCollection` and invocation bindings without importing
Dance types. `QueryDance` is a separate descriptor-afforded adapter: its
`QueryDanceRequest` selects the same `Query` and supplies the same runtime
inputs through the Dance layer.

QueryCore is the internal direct-execution submodule of `map-query-schema`. It
owns the execution contract and lifecycle beneath the `Query` entry point; it
is not a separately loadable schema package or a generic direct-caller API.
Extract it only if another independently loadable consumer needs that contract
without Query definitions, or it needs independent versioning.

For every invocation, the engine creates one `ExecutionInstance`. It creates a
`QueryExpressionExecution` for each expression invocation. Runtime input,
output, status, and resolved bindings belong exclusively to these execution
holons; they must not be written onto the reusable query definition.

```text
Query
  RootExpression -> QueryExpression

ExecutionInstance
  ExecutesQuery -> Query
  ExpressionExecutions -> QueryExpressionExecution*
  ExecutionResult -> HolonCollection?
```

The first root-expression execution consumes the caller-supplied input. Each
successful expression execution supplies its result to the next expression in
the chain. The result of the root chain becomes `ExecutionResult`. When the
caller used the Dance adapter, it also becomes `QueryDanceResponse.ResponseBody`.

## Expression Semantics

Every executable operator is a concrete holon type extending `QueryExpression`.
Ordinary MAP typing classifies an expression; no separate expression-kind or
expression-type relationship exists.

`Next` is the only declared sequential-continuation relationship. `Previous`
is its inverse. `QuerySubTree.Subtree` is implementation containment, not
continuation. A query tree is consequently a hierarchy of linear chains, not a
general DAG. Cycles and shared expression nodes are invalid.

A composite expression receives a collection, executes its contained subtree,
applies the merge or selection semantics of its concrete type to the subtree
exits, then continues at its own `Next` expression. Child expressions must not
reference the parent continuation.

## Descriptor Ownership

Descriptors, rather than query-specific metadata, own query meaning:

- holon-type descriptors determine the structural surface available to an input
  holon;
- relationship descriptors determine legal channels, endpoint roles, and
  inverse names;
- property and value descriptors determine projection, comparison, ordering,
  and predicate legality;
- concrete expression descriptors determine their parameter contracts and
  execution behavior.

An engine must reject an expression whose descriptor-backed contract cannot be
satisfied. It must not silently omit invalid input members or treat invalid
structure as an empty result.

## Initial Expression Set

The first executable expression types are:

- `SeedHolons`, which establishes a descriptor-governed initial collection;
- `Expand`, which follows one named relationship channel;
- `Filter`, which applies descriptor-valid predicates above storage;
- `OrderBy`, `Distinct`, `Skip`, and `Limit`, which transform a collection;
- `Project`, which is the explicit materialization boundary.

These names identify expression semantics. Concrete parameter shapes are
introduced with their expression types in the schema when implementation
requires them.

### Expand

`Expand` resolves the requested relationship name against the effective
descriptor of every input member. It must normalize declared and inverse names
onto one semantic relationship pair, validate endpoint legality, and then use
the corresponding storage access path.

If a requested traversal is legal but has no targets, `Expand` returns an empty
collection for that input. If any input member cannot legally traverse the
requested channel, the expression fails validation. Successful expansion
preserves storage traversal order and duplicate occurrences. Explicit
`Distinct` and `OrderBy` expressions own deduplication and reordering.

### Filter, ordering, and projection

General property predicates execute above storage through `SmartReference`
accessors. Cached SmartLink target properties may avoid a fetch but never alter
predicate truth or plan validity. `Filter` validates property access and
operator compatibility through descriptors before evaluation.

`OrderBy` validates sortable values through value descriptors. `Distinct`,
`Skip`, and `Limit` have explicit collection semantics and do not change the
meaning of preceding expressions. `Project` selects descriptor-valid properties
and produces materialized output; it is not the default navigation carrier.

## Storage Boundary

The engine delegates storage access only to the storage algebra. The relevant
version 1 operations are source expansion, relationship selection, and exact
or prefix canonical-key selection. They return decoded SmartLinks. The query
coordination layer materializes those links as `SmartReference` values before
continuing the expression pipeline.

The engine must not invent target lookup, reverse lookup, or arbitrary property
search beneath this boundary. Reverse traversal uses the persisted inverse
SmartLink. General filtering remains above storage unless a later complete,
explicitly maintained access path is added.

## Parameters

`QueryParameterDeclaration` is reusable definition state. It names an accepted
parameter and identifies the concrete `QueryParameterBinding` type. A binding
is runtime state and must reference its declaration. A direct caller supplies
bindings to the engine; Dance-mediated bindings belong to `QueryDanceRequest`.
Expression-local resolved bindings belong to `QueryExpressionExecution`.

Expression types must validate that each received binding matches a declared
parameter and its expected binding type before execution.

## Execution Outcomes

An execution is pending, running, complete, or failed as defined by
`QueryExecutionStatus`. A complete execution has an `ExecutionResult`; a failed
execution does not return a partial collection as if it were a successful one.
Diagnostics belong to the dance and execution outcome contracts, not to saved
query or expression definitions.

## Distributed Boundary

The shared engine is valid in a single `HolonSpace` and may identify an
expression boundary that requires distributed continuation. It does not perform
cross-space dispatch, trust-channel coordination, host task orchestration, or
branch merging. Those are host-coordinator responsibilities defined by
[dist-query-concept.md](dist-query-concept.md).

## Non-goals

This specification does not define an OpenCypher/GQL parser, optimizer,
row-stream runtime, generic relationship-edge payloads, or arbitrary graph
search. Declarative compatibility is a later compiler that produces the same
`Query` and `QueryExpression` model.
