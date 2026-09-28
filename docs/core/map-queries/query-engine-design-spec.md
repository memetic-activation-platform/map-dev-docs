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

The initial operand algebra is deliberately narrow:

```text
HolonCollectionReference -> QueryExpression -> HolonCollectionReference
```

`HolonReference` and `HolonCollectionReference` preserve identity and deferred
access. Materialized scalar, projection, path, correlation, and row-like values
are introduced only where a concrete expression or compatibility surface
requires them.

## Normative Execution Model

The Query engine executes a reusable `Query` directly and has no dependency on
Dance. A direct caller supplies a focal `HolonSpace` invocation context,
optional initial `HolonCollectionReference`, and bindings without importing
Dance types. `QueryDance` is a separate descriptor-afforded adapter: it adapts
the Dance's `AffordingHolon` into the same focal-space context and forwards an
optional collection reference through the Dance layer.

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
  FocalSpace -> HolonSpace
  ExpressionExecutions -> QueryExpressionExecution*
  ExecutionResult -> HolonCollection?
```

`ExecutionInstance.FocalSpace` is transient per-invocation context, required
exactly once, and is not saved on `Query` or a `QueryExpression`. It is local
to `SeedHolons` scope in this version; it is not the future multi-space
`ExecutionDomain`.

A root expression is either source-producing or operand-consuming. A source
root receives no collection input; an operand-consuming root receives the
caller-supplied `HolonCollectionReference`. Each successful expression
execution supplies its result to the next expression in the chain. The result
of the root chain becomes `ExecutionResult`. When the caller used the Dance
adapter, it also becomes `QueryDanceResponse.ResponseBody`.

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

The first expression family includes:

- `SeedHolons`, which establishes the focal-space-owned initial collection;
- `Expand`, which follows one named relationship channel;
- `Filter`, a future predicate-evaluation expression;
- `OrderBy`, `Distinct`, `Skip`, and `Limit`, which transform a collection;
- `Project`, which is the explicit materialization boundary.

These names identify expression semantics. Concrete parameter shapes are
introduced with their expression types in the schema when implementation
requires them.

QRY2 implements only `SeedHolons` and `Expand`. It introduces an abstract
`QueryPredicate` plus optional `SeedHolons.SeedPredicate` and
`Expand.ExpansionPredicate` attachments as forward-compatible payload shapes,
but no concrete predicate form exists in QRY2. They are expression definition
state, not collection operands. QRY2 therefore performs no predicate
construction, composition, evaluation, host fallback, or storage pushdown.

### SeedHolons

`SeedHolons` is root-only. It declares no parameters and consumes no collection
operand, but may carry an optional `SeedPredicate` definition payload. It
derives its source from the current execution's required focal space and
performs exactly:

```text
Expand(ExecutionInstance.FocalSpace, Owns)
```

It is not `GetAll`, global enumeration, all-relationship expansion, or an
ambient query-definition context. A supplied collection input for a
`SeedHolons` root is a validation error. The resulting transient collection
preserves the `Owns` traversal order and duplicate occurrences.

### Expand

As a root, `Expand` is operand-consuming and requires exactly one
`HolonCollectionReference` supplied by the caller. As a non-root expression,
it consumes its predecessor result. Independently, it may carry an optional
`ExpansionPredicate` definition payload. It never treats a missing relationship
name as an instruction to expand all relationships.

For each source member, `Expand` obtains its `HolonDescriptor` and calls
`HolonDescriptor::allows_relationship(requested_name)`. That existing helper
resolves one declared-or-inverse outbound relationship or returns its ordinary
`HolonError`; `Expand` propagates that result and uses the returned relationship
for traversal. It does not preflight the whole collection, construct a separate
effective-descriptor model, or add query-specific relationship validation.

If a requested traversal is legal but has no targets, `Expand` returns an empty
collection for that input. If any input member cannot legally traverse the
requested channel, the expression fails validation. Successful expansion
preserves storage traversal order and duplicate occurrences. Explicit
`Distinct` and `OrderBy` expressions own deduplication and reordering.

### Deferred predicates, ordering, and projection

Predicate semantics are deferred until MAP defines concrete predicate forms,
unary, binary, and n-ary value operators, effective-operator lookup, and a
composition grammar. That work must make a predicate eligible for guest-side
evaluation near storage when the relevant local capability supports it, so an
expand-filter plan need not drag every candidate across the guest-host boundary.
The attachment on `Expand` does not itself define evaluation or pushdown.

Until predicate evaluation is supported, execution must refuse an attached
`SeedPredicate` or `ExpansionPredicate` with `HolonError::NotImplemented`
rather than return unfiltered members. This check applies before operator
execution at every step, including non-root expressions reached through `Next`.
Both attachment names are checked regardless of operator kind, and refusal is
based on presence rather than cardinality: a misplaced attachment or multiple
attached predicates must not bypass the unsupported-feature check. The
root-only contract for `SeedHolons` is checked first; an off-root `SeedHolons`
remains an `InvalidParameter` error even when it carries a predicate.

A refused expression's execution record is `Failed` with no `Result`; the
execution instance is `Failed` with no `ExecutionResult`. Previously completed
steps retain their `Complete` status and results. Optional predicate attachments
remain valid definition shapes; they do not imply executable filtering support.

`OrderBy` validates sortable values through value descriptors. `Distinct`,
`Skip`, and `Limit` have explicit collection semantics and do not change the
meaning of preceding expressions. `Project` selects descriptor-valid properties
and produces materialized output; it is not the default navigation carrier.

### OrderBy

`OrderBy` consumes a `HolonCollectionReference` and returns a collection of the
same holon-reference occurrences in sorted order. A root requires an explicit
input collection; a successor consumes its predecessor's result. It neither
deduplicates members nor materializes projected property values in its output.

#### Holonic ordering specification

An `OrderBy` expression has an `OrderBySpecs` declared relationship to
`OrderBySpec` with `IsOrdered = true`, minimum cardinality 1, and maximum
cardinality 5. Relationship target order determines sort precedence.
Each `OrderBySpec` is a holon with concrete members:

| Member | Contract |
| --- | --- |
| `Property` | Required singleton InstanceRelationship to the `PropertyType` descriptor of the property to sort. No property-name parsing, path syntax, or computed expression. |
| `SortDirection` | Required InstanceProperty with enum variants `Ascending` and `Descending`; default `Ascending`. |
| `NullPlacement` | Required InstanceProperty with enum variants `Missing-First` and `Missing-Last`; default `Missing-Last`, independent of direction. |

See the [OrderBySpec schema](command-dance-query-schema-tdl.md#orderby-spec-schema).
An author may construct the query, expressions, and specs as transient holons,
attach concrete values and related holons, then submit the query for execution.
Authoring does not require staging, committing, or a separate parameter-binding
wrapper. Definition state can be transient; it is distinct from execution state.
Evaluation resolves required argument values without modifying the supplied
holons. For `SortDirection` and `NullPlacement` independently, call
`property_value()` first:

- `Some(value)`: validate and use that value without resolving a default.
- `None`: invoke the shared descriptor-backed read-only default accessor,
  validate the resolved default, and use it locally without writing it back.
- A read error propagates immediately; it does not trigger default lookup.

A missing value with no applicable default is a required-value error.
Malformed explicit values fail validation rather than falling back to defaults;
descriptor-resolution and invalid-default errors propagate.

This read-only resolution is distinct from `populate_defaults()`, which
materializes values during explicit construction. Query evaluation must not
call that mutating operation on caller-supplied arguments. Ordinary property
reads retain their existing stored-value semantics; default fallback is an
explicit accessor operation. Required SortDirection and NullPlacement may
therefore be omitted on a transient OrderBySpec when their descriptor-defined
defaults resolve successfully. Neither success nor failure changes the supplied
query graph. This execution behavior does not relax staged-holon validation or
commit requirements for populated required properties.

Execution reads the attached specs without mutating them. It records status,
input, and results in separate execution records. Zero or more than five specs,
invalid Property targets/cardinality, invalid enum values, or required values
unresolved after read-only effective-value resolution are contract errors. Validate spec
shape even for empty input collections.

#### Comparison and missing values

Resolve the referenced PropertyType by descriptor identity against each
member's effective property surface, then validate its value descriptor for every
input occurrence, including singleton collections and keys that do not affect
the eventual ordering. An undeclared property, unreadable member, malformed
value, or absent required property fails execution; none is treated as a
missing optional value or silently omitted.

An absent value is sortable only when the effective property contract permits
its absence. For a given key, a missing value sorts before every present value
under `Missing-First`, and after every present value under `Missing-Last`. Two
missing values tie for that key. Direction changes only present-value order.

The supported comparison domains are descriptor-backed integer and string
values. For each key, members must resolve to the same effective value-type
descriptor identity, and that descriptor must afford supported equality and
less-than operations. This conservative compatibility rule also applies when
values are absent; matching primitive representations alone do not establish
compatibility between distinct value types. Different keys may use different
value types. Empty input has no member descriptors to validate and returns an
empty collection after specification validation.

Integer comparison is numeric. String comparison uses the value descriptor's
ordinal, case-sensitive lexicographic semantics, without locale collation,
case folding, or normalization. Descriptor validation and comparison errors
propagate. Unsupported domains, including boolean, enum, bytes, and arrays,
fail explicitly; there is no stringification or reference-identity fallback.

#### Stable ordering and execution outcomes

Compare keys lexicographically in relationship target order: the first non-tied key decides
the order. If all keys tie, preserve input occurrence order. Descending order
must preserve this stability rather than reversing a completed ascending
collection. Duplicate occurrences remain separate occurrences.

For example, keys `Name Ascending Missing-Last` followed by
`Age Descending Missing-Last` group equal names by decreasing age. Occurrences
with equal names and ages retain their input order. A missing Name follows
every present Name, regardless of Age; two missing Names are compared by Age.

Execution follows authored `Next` order. Thus `OrderBy -> Skip -> Limit` slices
the sorted result, whereas `Skip -> OrderBy` sorts only the retained input.
Ordering does not guarantee repeatable pagination across changed data or
different input ordering among fully tied values.

The expression publishes its result only after validation and sorting succeed.
A reached `OrderBy` that fails specification validation, property validation, or comparison is
`Failed` with no `Result`; its execution instance is `Failed` with no
`ExecutionResult`. Earlier completed steps retain their results. The result
remains a collection holon whose identity is passed to the next step as Input.

### Skip and Limit

`Skip` and `Limit` are concrete `QueryExpression` HolonTypes. `Skip` declares
`SkipCount` in its `InstanceProperties`; `Limit` declares `LimitCount` in its
`InstanceProperties`. Each count PropertyType has an integer ValueType and
`IsValueRequired = true`, with no default. Consequently, each `Skip` instance
must supply `SkipCount`, and each `Limit` instance must supply `LimitCount`.
Neither property is attached to the base `QueryExpression` type or required of
other expression types. See the
[pagination schema contract](command-dance-query-schema-tdl.md#skip-and-limit-schema).

Counts must be nonnegative. A missing, negative, or non-integer count is a
contract error, including for empty input. A root requires an explicit input
collection; a successor consumes its predecessor's result. `Skip` removes the
first `SkipCount` occurrences; `Limit` retains at most `LimitCount` occurrences.
Zero Skip retains all members; zero Limit returns an empty collection. A count
at or above input length returns empty for Skip and all members for Limit.
Large counts must retain these semantics without overflowing an index conversion.

Both expressions preserve relative order and duplicate occurrences among
retained members. They operate in authored `Next` order and do not require an
`OrderBy`. Results remain collection holons under the ordinary execution
identity and failure contracts.

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

### Unsupported invocation bindings

Until separate runtime binding is supported, `QueryReference::begin_execution`
rejects any nonempty invocation binding list with `HolonError::NotImplemented`
as its first operation, before root/input validation or creation of an
`ExecutionInstance` or `QueryExpressionExecution`. No execution records are
created for this rejection. Empty binding lists proceed through ordinary
execution. QueryDance forwards `RequestParameters` to this same entry point;
it does not implement an alternative binding check. Its existing Dance ingress
validation still precedes entry into QueryCore. The direct single-holon helper
also delegates binding rejection to this entry point.

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
