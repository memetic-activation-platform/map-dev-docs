# Storage-Grounded Query Architecture

Status: current architecture narrative.

The source of truth for query state is
[command-dance-query-schema-tdl.md](command-dance-query-schema-tdl.md). This
document explains the architecture and execution semantics that the TDL
prescribes.

Older query documents in this directory may still use the previous
`QueryGraph`, `QueryStep`, and `QueryStepKind` vocabulary. Treat this document
and the companion TDL file as the current terminology and topology source until
those documents are realigned.

---

## Core Position

The MAP query system separates reusable query definition from runtime
execution.

`Query` is the reusable definition holon. It owns the root `QueryExpression` of
the query tree.

`QueryDanceRequest` is a concrete invocation request submitted to `QueryDance`.
It identifies:

- the reusable `Query`
- the initial input `HolonCollection`
- invocation-level `QueryParameterBinding` holons

`ExecutionInstance` is the runtime state for the whole query invocation.

`QueryExpressionExecution` is the runtime state for one execution of one
`QueryExpression`.

Conceptually:

```text
DanceInvocation
  Request -> QueryDanceRequest

QueryDanceRequest
  RequestedQuery    -> Query
  InitialInput      -> HolonCollection
  RequestParameters -> QueryParameterBinding*

Query
  RootExpression -> QueryExpression

ExecutionInstance
  ExecutesRequest      -> QueryDanceRequest
  ExpressionExecutions -> QueryExpressionExecution*
  ExecutionResult      -> HolonCollection?

QueryExpressionExecution
  ExecutesExpression -> QueryExpression
  Input              -> HolonCollection
  Result             -> HolonCollection?
  RuntimeParameters  -> QueryParameterBinding*
```

This separation keeps saved query definitions reusable. Runtime inputs, results,
and parameter bindings belong to execution state, not to the query definition.

---

## QueryExpression

`QueryExpression` is the fundamental executable unit of a query.

Every query root, subquery, logical operator, physical operator, and
storage-specific implementation expression is a holon described by
`QueryExpression` or by a concrete holon type that extends `QueryExpression`.

TDL defines the current state shape:

```text
QueryExpression
  ExpressionParameters -> QueryParameterDeclaration*
  Next                 -> QueryExpression?

QueryExpression
  Previous             -> QueryExpression?  # inverse of Next
```

`Next` is the declared relationship for sequential execution. `Previous` is
only its inverse relationship.

There is no separate `ExpressionType` relationship. Expression classification is
ordinary MAP typing: the expression holon is described by its concrete
`QueryExpression`-derived holon type, and descriptor instance discovery uses
the normal inverse relationship for that typing link.

`ExpressionParameters` points to zero or more parameter declaration holons.
Parameter binding types belong to those declarations and to the concrete
binding holon types, not to a separate expression-type relationship.

`ExpressionParameters` is definition state. It points to
`QueryParameterDeclaration` holons that name accepted parameters and identify
the concrete `QueryParameterBinding` type expected at runtime.

Runtime parameter values and resolved parameter bindings belong to
`QueryDanceRequest.RequestParameters` or
`QueryExpressionExecution.RuntimeParameters`. Those relationships point to
`QueryParameterBinding` instances. Concrete binding types extend
`QueryParameterBinding` and declare the value-bearing properties or
relationships for the specific parameter kind.

The runtime operand and result type is `HolonCollection`. Optional, singleton,
and multi-valued cases are represented by collection membership rather than by
separate execution carriers.

Runtime `Input` and `Result` relationships are declared by
`QueryExpressionExecution`, not by `QueryExpression`, because a single saved
expression may execute many times with different inputs and results.

---

## Concrete Expression Types

Concrete operators should be modeled as holon types that extend
`QueryExpression`.

Examples may eventually include:

- `Expand`
- `ExpandWhere`
- `Filter`
- `Project`
- `GetLinks`
- `GetLinksByPrefix`
- `HydrateTargets`

Layer identity is deliberately not a base relationship yet. Logical, physical,
and storage-specific expression type extensions should be introduced only when
a layer has concrete properties, relationships, or dances of its own.

---

## QueryTree Topology

The query shape is a `QueryTree`.

`QueryTree` is a conceptual name, not a separate holon type. It means:

- the root is `Query.RootExpression`
- each chain advances through `QueryExpression.Next`
- implementation containment is represented by `QuerySubTree.Subtree`
- `Previous` and `Parent` are inverse relationships

A `QueryTree` is a hierarchy of linear expression chains, not an arbitrary DAG.

Topology rules:

- `Next` defines sequential execution within a chain.
- `Previous` is the inverse of `Next`.
- `Subtree` defines implementation containment.
- `Parent` is the inverse of `Subtree`.
- Child expressions do not point to the parent's continuation.
- Cycles are invalid.
- Shared expression nodes are invalid unless a later design explicitly adds
  sharing semantics.

The ordinary execution path is chain-shaped. The overall query is tree-shaped
because expressions may contain implementation subtrees.

---

## Composite Expressions

`QuerySubTree` extends `QueryExpression` and adds the `Subtree` declared
relationship.

TDL defines the containment shape:

```text
QuerySubTree extends QueryExpression
  Subtree -> QueryExpression*

QueryExpression
  Parent -> QuerySubTree?  # inverse of Subtree
```

`Subtree` represents implementation containment. It does not represent the
next step of execution.

Composite execution follows this lifecycle:

1. the parent expression receives an input `HolonCollection`
2. the parent delegates execution to the first ordered expression in `Subtree`
3. the subtree executes as one or more independent linear chains
4. each terminal expression with no `Next` is an exit
5. the parent expression receives the subtree result
6. execution resumes at the parent's `Next` expression

Multiple exits are permitted. The merge or selection rule for multiple exits is
part of the parent expression's concrete type semantics.

No child expression is required to reference the parent's continuation.

---

## Uniform Representation

The same `QueryExpression` base structure represents every abstraction level:

- root expression
- logical operator
- physical operator
- storage-specific implementation expression
- subquery

Concrete type extensions should be introduced only when a layer or operator has
its own properties, relationships, or dances. Until then, layer identity remains
an open design point rather than a required base relationship.

---

## Compilation Pipeline

A query progresses through successive representations:

1. semantic query intent
2. logical query tree
3. optimized logical query tree
4. physical query tree
5. executable storage plan

Each stage remains a tree of `QueryExpression` holons.

Compilation is expressed by replacing or extending higher-level expressions
with implementation subtrees composed of lower-level expressions.

---

## Logical Query Algebra

The logical algebra defines the meaning of a query independently of storage
implementation.

Logical operations express intent rather than execution strategy.

Examples include:

- `Expand`
- `ExpandWhere`
- `Filter`
- `Project`
- `Aggregate`
- `Join`
- `TraversePath`
- `LookupByKey`

Versioned-key lookup is deliberately not a logical query operation. A
versioned key is a reference-layer disambiguator for transient and staged
holons: clone/version operations retain the logical `Key`, so multiple
transaction-local holons may share that base key and receive an appended
version suffix for Nursery or transient-pool lookup.

That mechanism does not identify versions of persisted SmartLink endpoints.
Persisted endpoints are already exact because their `HolonId`s are based on
action identity.

Logical operators may intentionally combine primitive concepts when doing so
preserves optimization opportunities.

For example, `ExpandWhere` preserves the semantic association between traversal
and filtering. The initial correctness-first planner may implement it as
expansion followed by filtering through `SmartReference` accessors; future
optimization may use that association without changing semantics, but only
through a complete access path or a correctness-preserving fallback.

---

## Physical Query Algebra

The physical algebra represents executable storage-oriented operations.

Representative operations include:

- `ExpandAllFromSource`
- `ExpandFromSource`
- `ExpandFromSourceByKey(Exact)`
- `ExpandFromSourceByKey(StartsWith)`
- `GetPathChildren`
- `GetRelated`
- `GetRelated(Predecessor)`
- `GetRelated(Successor)`
- `Union`
- `ForEach`

The three `Expand*` operations are the concrete storage surface. They return
decoded SmartLinks, not `HolonCollection` results. Coordination materializes
those links as `SmartReference` values before the query-expression pipeline
continues.

General property filtering and target-property access execute above the
storage boundary through `SmartReference`. Canonical-key exact and prefix
selection are storage operations because every version 1 SmartLink contains a
canonical-key segment, including an empty segment for a keyless target.

SmartLink source and target identifiers refer to exact holon versions. Version
lineage is therefore ordinary traversal over the `Predecessor` relationship and
its `Successor` inverse, not a selection step during storage lookup.

The initial planner compiles logical expressions through a direct,
correctness-preserving implementation. Future planners may choose among
additional access paths when those paths have explicit completeness contracts.

The design does not yet require physical algebra and storage operations to be
separate layers. That split should wait until the implementation needs a real
distinction.

---

## Storage Access Paths

Smart Link tag encoding defines the available storage access paths.

The encoding is therefore part of the query architecture rather than merely an
implementation detail. The exact encoding and storage operation contracts are
defined by the
[Storage Layer and SmartLink Design Specification](../guest/storage-layer-services/storage-layer-design-spec.md)
and are not re-specified here.

The ordering of encoded path segments determines which predicates can be
executed efficiently.

Typical capabilities include:

- exact source identity
- exact relationship selection from that source
- exact canonical-key selection within that relationship
- canonical-key prefix selection within that relationship

The initial planner uses those structural access paths and evaluates general
property predicates above storage. A generic exact-target or reverse-link
lookup is not part of the initial storage algebra. Reverse navigation uses the
persisted inverse SmartLink.

---

## Smart Link Constraints

Smart Links are implemented using Holochain links.

The storage layer exposes prefix-based lookup over link tags.

Consequently:

- exact source, exact relationship, exact canonical-key, and canonical-key
  prefix predicates are storage operations
- general property predicates are evaluated above storage through
  `SmartReference` accessors
- arbitrary substring and regular-expression search are not native SmartLink
  retrieval predicates
- best-effort cached property presence never determines plan validity

The smart property map may avoid target-holon retrieval while an upper-layer
predicate is evaluated, but that is reference-layer execution transparency,
not storage predicate pushdown.

---

## Access Path Selection

The initial planner does not choose among access paths for performance. It uses
the direct storage operation for source expansion, relationship expansion, or
canonical-key selection and leaves general property filtering above storage.

Other property predicates continue to use expansion followed by reference-layer
filtering unless a complete, explicitly maintained secondary access path is
introduced.

---

## Index Design

Smart Link encoding constitutes index design.

The ordering of encoded path components determines which lookup patterns are
efficient.

Additional Smart Link structures may be introduced as secondary indexes to
support lookup requirements that are not naturally served by relationship
traversal.

Relationship traversal and indexed lookup are distinct concerns, even when
implemented using the same underlying Holochain link mechanism.

---

## Execution Model

Execution is modeled as a pipeline over `HolonCollection`.

The root expression's first execution consumes `QueryDanceRequest.InitialInput`.

Each `QueryExpressionExecution` consumes an input `HolonCollection` through
`Input` and may produce a result `HolonCollection` through `Result`.

The result of one expression execution becomes the input to the next expression
execution.

Composite expressions execute by delegating to their implementation subtree and
returning the subtree's result before continuing along the parent execution
chain.

`ExecutionInstance` records whole-query runtime status and the final
`ExecutionResult -> HolonCollection`. `QueryExpressionExecution` records
per-expression runtime state, including the input and result collections for
that expression invocation.
