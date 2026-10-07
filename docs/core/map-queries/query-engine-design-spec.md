# MAP Descriptor-Aware Query Engine Design Specification

Status: normative execution semantics for the storage-grounded query model.

This specification describes the target design for collection-based query
execution, including shared scalar predicates and filtering. Delivery stages,
implementation status, and transitional limitations belong to the
[implementation plan](queries-impl-plan.md).

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

## Name selection and execution-time descriptor resolution

Holonic query expressions select properties and relationship channels by name.
The expression definition represents the query before schema binding. During
execution, each expression's Rust implementation resolves its selectors against
the actual input holon's effective type surface through shared descriptor
facilities, then uses the resolved descriptors to validate and execute the
operation. A textual front end, including a future GQL or OpenCypher front end,
can construct the same holonic representation as direct holonic authoring
without first binding names to schema descriptor identities.

Name resolution is descriptor-backed: it does not read arbitrary stored fields
or bypass declaration, requiredness, value-type, operator, or traversal checks.
Duplicate property names within a holon type's effective property surface are
rejected during type-definition validation. Query expressions rely on that
invariant and propagate descriptor-resolution errors; they do not introduce a
parallel duplicate-declaration validator or choose arbitrarily among matches.
An undeclared name is an error, distinct from an absent optional value.

Independently valid holon types may declare the same property name using
different PropertyType descriptors. Selector resolution accepts those distinct
property identities; each operation still enforces its own compatibility rules.
For example, Book and Film may each declare a distinct `Title` PropertyType.
An OrderBy selector `Title` applies to both when their resolved value descriptors
satisfy the ordering compatibility contract. Neither type contains duplicate
property names. Shared primitive representations alone do not establish
semantic comparison compatibility.

This policy applies to Expand relationship selectors, OrderBy property selectors,
ComparisonPredicate property selectors, and future Project definitions.
Filter must resolve selected operands before validating applicable operators;
Project must resolve selected properties before materializing their values and
type information. Predicate compatibility and missing-value semantics are defined
below; Project's concrete shape remains separately defined. Skip and
Limit are positional transformations and perform no member-property selection.

Resolution belongs to the execution in its transaction context. It must not
replace names with descriptor references in caller-owned query definitions.
Shared descriptor facilities own lookup and inheritance semantics rather than
individual expressions implementing competing resolution rules. Names reduce
coupling to particular declaration versions, but do not guarantee that every
schema revision remains semantically compatible.

Selector resolution is distinct from invocation parameter binding and from
query persistence. Constructing a name-based query does not require a parameter
binder, and saving a definition does not by itself specify when its selectors
are bound. Saved forms, any bound form, and replay/version guarantees require
separate contracts; execution-time resolution does not settle those choices.

## Initial Expression Set

The first expression family includes:

- `SeedHolons`, which establishes the focal-space-owned initial collection;
- `Expand`, which follows one named relationship channel;
- `Filter`, which retains collection members satisfying a shared Predicate;
- `OrderBy`, `Distinct`, `Skip`, and `Limit`, which transform a collection;
- `Project`, which is the explicit materialization boundary.

These names identify expression semantics. Concrete expression types declare
their parameter contracts in the schema. `SeedHolons.SeedPredicate` and
`Expand.ExpansionPredicate` are optional relationships to `QueryPredicate`.
They carry expression definition state, not collection operands.

### SeedHolons

`SeedHolons` is root-only. It declares no parameters and consumes no collection
operand, but may carry an optional `SeedPredicate` definition payload. It
derives its source from the current execution's required focal space and
establishes its unfiltered candidates by:

```text
Expand(ExecutionInstance.FocalSpace, Owns)
```

It is not `GetAll`, global enumeration, all-relationship expansion, or an
ambient query-definition context. A supplied collection input for a
`SeedHolons` root is a validation error. The resulting transient collection
preserves the `Owns` traversal order and duplicate occurrences.
When `SeedPredicate` is present, the shared predicate evaluator filters those
candidates under the same semantics as a subsequent `Filter` expression.

### Expand

As a root, `Expand` is operand-consuming and requires exactly one
`HolonCollectionReference` supplied by the caller. As a non-root expression,
it consumes its predecessor result. Independently, it may carry an optional
`ExpansionPredicate` definition payload. It never treats a missing relationship
name as an instruction to expand all relationships.

For each source member, `Expand` obtains its `HolonDescriptor` and calls
`HolonDescriptor::resolve_available_relationship(requested_name)`. That existing helper
resolves one declared-or-inverse outbound relationship or returns its ordinary
`HolonError`; `Expand` propagates that result and uses the returned relationship
for traversal. It does not preflight the whole collection, construct a separate
effective-descriptor model, or add query-specific relationship validation.

If a requested traversal is legal but has no targets, `Expand` returns an empty
collection for that input. If any input member cannot legally traverse the
requested channel, the expression fails validation. Successful expansion
preserves storage traversal order and duplicate occurrences. Explicit
`Distinct` and `OrderBy` expressions own deduplication and reordering.
When `ExpansionPredicate` is present, it evaluates against the expanded target
holons, not the source holons. It has the same meaning as filtering the expanded
collection with that Predicate. It does not filter relationship descriptors or
SmartLink payloads as though they were candidate holons.

### Shared Predicate model and schema contract

**Predicate semantics are standardized; Predicate authoring experiences are
plural.** Query, Space Navigator, agents, and saved definitions use the same
representation, validation, and evaluation. A consumer may expose a restricted
subset without creating its own predicate language or comparison semantics.

`QueryPredicate` remains the existing abstract schema anchor for the shared
Predicate model. Its name does not give Query exclusive ownership of Predicate
semantics. The concrete forms are:

```text
QueryPredicate (abstract)
  ComparisonPredicate
  Not
  AllOf
  AnyOf
```

Ordinary MAP typing identifies each concrete schema form. A Predicate
is definition state and evaluates against one candidate to produce a Boolean;
it is neither a collection operand nor a `QueryExpression` continuation.

#### ComparisonPredicate: one filter specification

A single filter specification is a `ComparisonPredicate`, not a second
`FilterSpec` representation. Its declared semantic members are:

| Member | Contract |
| --- | --- |
| `PropertyName` | One required string-valued property selector, using the existing name-selection contract. No path syntax, computed expression, or Search-specific selector. |
| `Operator` | Exactly one relationship to an `OperatorType` descriptor. The selected descriptor must be effectively afforded by the resolved property's ValueType. |
| `Operands` | An ordered relationship to authored operand-value holons. Each carries a typed literal value; its position corresponds to the operator's authored-operand specification. Zero, one, or multiple operands are permitted as required by that operator. |

The operand-value envelope uses MAP value representations and ValueType
validation; it is not an untyped string bag or a consumer-specific JSON AST.
The selected property's value supplies the subject operand. Authored values
remain definition state, not `QueryParameterBinding` instances. Invocation
parameter binding is a separate capability.

For example, the semantic content of `Age GreaterThan 30` is property selector
`Age`, the afforded GreaterThan operator descriptor, and one authored integer
operand. Examples name operators by their semantic labels.

Selectors remain names in reusable definitions. An authoring context may supply
a PropertyDescriptor to guide construction, but the predicate retains the
property selector and execution resolves it against each candidate. There is
no separate key-only predicate syntax: selecting the canonical `Key` property
uses the same representation as selecting another scalar property.

#### Recursive logical composition

`Not` declares exactly one `Predicate` child relationship to `QueryPredicate`.
`AllOf` and `AnyOf` each declare an ordered `Predicates` relationship to
`QueryPredicate`, with one or more children. Children may themselves be leaves
or composites. Empty groups, missing children, and cycles are invalid; the
absence of a filter is represented by omitting the filter, not an empty group.

- `Not` returns the Boolean negation of its child.
- `AllOf` returns true exactly when every child returns true.
- `AnyOf` returns true exactly when at least one child returns true.

For example:

```text
AllOf(
  GreaterThan(Age, 30),
  AnyOf(Equals(Status, Active), Equals(Status, Pending))
)
```

Composition scope is explicit regardless of the author's presentation. Predicate
child relationships are not `Next`; `Next` remains collection-expression
continuation. Shared validation rejects malformed or unsupported branches even
when another branch's Boolean value would determine the outcome. An evaluator
may short-circuit Boolean combination only after required validation and value
access checks; it must not use short-circuiting to hide an invalid candidate,
unsupported operator, or unreadable property.

### Operator and authored-operand contracts

Operators belong to ValueTypes. Predicate execution and authoring reuse
`OperatorType`, `MetaOperatorType`, `Arity`, `OperatorCategory`, inherited
`AffordsOperator`, and the shared effective-operator lookup. They must not
introduce a filtering-specific operator registry or comparison implementation.

Execution arity and authored operand count are different. Equals has two input
values but one authored operand when the property supplies its subject;
Between has a subject plus two authored bounds. An authorable operator exposes
an ordered set of operand specifications, each identifying its semantic role,
required ValueType, and human-facing label where needed. The contract must
resolve those ValueTypes for the selected subject ValueType; inherited generic
operators must not lose the subject's semantic type constraints. Controls must
not be inferred from `Arity` alone.

`Arity` and `OperatorCategory` metadata alone do not fulfill this
authored-operand contract. The operand-specification relationship and value
envelope require concrete declarations in the Query/Operator schema companions;
their storage details must preserve the semantic members and ordering above.
Operator categories remain extensible beyond equality and ordering.

Operator descriptors provide human-facing labels/descriptions and sufficient
operand metadata for generic authoring. ValueTypes own value validation and
value-authoring semantics. An editor discovers:

```text
Property -> ValueType -> effective AffordsOperator
         -> authored-operand specifications -> ValueType-driven value authoring
```

The shared invocation contract accommodates a subject value and an ordered
operand sequence, conceptually `apply_operator(operator, subject, operands[])`.
The exact Rust API is an implementation choice; its semantic model must support
zero, one, and multiple authored operands rather than permanently assuming
`lhs, rhs`. Operator-specific constraints belong to the operator/value layer.
Security-aware operator availability and array predicate semantics are outside
this contract.

#### String matching operators

The string ValueType family affords three distinct matching operators through
the ordinary inherited `AffordsOperator` relationship. Each has a string subject,
one authored string operand, and a Boolean result:

| Operator | Authored operand | Meaning |
| --- | --- | --- |
| `Contains` | Literal text | The subject contains the supplied text as a literal substring. Pattern metacharacters have no special meaning. |
| `Like` | Wildcard pattern | The subject matches a wildcard pattern under the operator's declared wildcard and escaping rules. This is not regex syntax. |
| `MatchesRegex` | Regular expression | The subject matches a regular expression under the operator's declared regex dialect, flags, and match-scope rules. |

These are distinct string-family affordances. The detailed pattern contracts
remain open design decisions: Like requires a wildcard alphabet, escaping,
and whole-value versus partial-match rules; MatchesRegex requires a dialect,
flags, match scope, and invalid-pattern/resource-limit error behavior. No
caller may infer those rules from its local programming language.

The operators may share execution machinery, but their semantic contracts remain
distinct. A regex-backed Contains implementation must treat its operand as
literal text and preserve containment semantics; it must not interpolate raw
input into a pattern or expose regex behavior to its caller. Unsupported Like
or MatchesRegex execution fails explicitly rather than falling back to Contains.

Case handling belongs to the generic operator/value matching policy, not Query
or an authoring experience. The contract must support case-insensitive
containment and identify the effective policy reproducibly; it must not depend
on the executing browser's locale or change existing Equals/LessThan semantics.
The policy's schema placement and exact Unicode case-folding/normalization
rules remain an explicit ValueType/operator design decision. They must be
defined before case-insensitive evaluation is considered specified completely.
This is not a Search-specific property, operand, or invocation shape.
Like and MatchesRegex must declare how their pattern rules interact with this
policy; a case-insensitive literal policy is not permission to rewrite regex
or wildcard syntax by lowercasing the pattern.

An explicitly authored Contains with an empty literal follows substring semantics
and matches every present valid string. It remains a predicate application.
A consumer wishing to express no filtering omits its predicate/filter instead.

### Shared validation and evaluation

Validate predicate shape, child cardinalities, operator descriptors, authored
operand counts and values, and supported capabilities before publishing a
result, including for an empty collection. Empty input provides no candidate
descriptor for property resolution; candidate-dependent checks apply when
candidates exist, not against an invented representative type.

For every candidate and comparison leaf, the shared layer:

1. Resolves `PropertyName` through the candidate's effective property surface.
2. Obtains that PropertyDescriptor's effective ValueType and requiredness.
3. Resolves and verifies the selected operator's effective affordance.
4. Resolves its authored-operand specifications and validates operand values
   and operator-specific constraints.
5. Obtains the subject value through a valid access path and validates it.
6. Invokes the value/operator machinery and combines Boolean results according
   to the predicate structure.

An undeclared property, incompatible candidate type, unavailable or unafforded
operator, incorrect operand count, malformed value, or failed access is an
explicit error. No implicit stringification, conversion fallback, or silent
omission is permitted. Distinct PropertyDescriptors with the same selected
name are allowed; each must independently satisfy the operator and operand
contracts. A shared primitive representation alone does not prove compatibility.

For the initial scalar comparison contract, an absent optional property makes
the comparison false; an absent required property fails execution. Operator
and operand validation still applies when the optional value is absent. `Not`
negates that Boolean result, so it can include a candidate whose optional
property is absent. There is no implicit three-valued/null logic. Future
presence-testing operators require their own explicit missing-subject contract.

Validation and evaluation are shared capabilities. Consumers may guide authors
away from invalid combinations, but execution does not trust UI validation as
a substitute for the semantic checks above. Neither success nor failure mutates
the supplied predicate or query definition.

### Filter and predicate-bearing expansion

`Filter` is a concrete `QueryExpression` with exactly one `Predicate`
relationship to `QueryPredicate`. A root Filter requires one explicit
`HolonCollectionReference`; a successor consumes its predecessor's result.
It retains precisely those candidate occurrences for which the Predicate is
true, preserving their relative order, duplicate occurrences, reference identity,
and transaction binding. The output is an ordinary collection holon, including
when empty, and supplies the next expression's Input through `Next`.

Filtering does not mutate the input or the underlying relationship. Source
cardinality and result cardinality are distinct facts. A Predicate that happens
to match every member is still evaluated; it is not equivalent definition or
execution state to an absent Predicate.

The optional `SeedPredicate` and `ExpansionPredicate` relationships accept the
same `QueryPredicate` forms and invoke the same evaluator as Filter. Their
meaning is expansion followed by filtering. They do not introduce different
operator semantics, source-versus-target ambiguity, or a new Search operation.
An attached predicate and a subsequent Filter remain separately authored
applications; an implementation must not accidentally apply one attachment twice.

An author can therefore express either an expansion with an attached Predicate
or an explicit `Expand -> Filter` chain. `SeedHolons` provides the focal-space
Owns expansion. The choice of attachment or expression does not change the
predicate representation supplied by a programmatic caller, agent, or UI.

### Indexed property access

The evaluator may obtain a selected property from complete, valid collection
index evidence rather than dereference each candidate. This is an access-path
choice below Predicate syntax, not a special operand or operator. It must
preserve descriptor validation, value semantics, candidate coverage, order,
and multiplicity.

For a fully materialized collection with a complete member-key index, a
comparison selecting Key evaluates against those indexed values. Matching and
result construction must not retrieve every target merely to read or rebuild
its key. Retain known key/reference associations through expansion and filtering
and adjust result positions from that evidence. Scanning the complete local
index is sufficient for substring containment; an exact or prefix lookup is
not a substitute for Contains.

Index completeness includes occurrence coverage and valid absent-value evidence
where applicable. A key-to-single-position map does not by itself cover duplicate
occurrences or prove that an unindexed member lacks an optional property.
Preserve sufficient collection evidence or reject an index-only execution that
cannot meet this contract; never silently drop uncovered members. General
evaluation may use ordinary property reads where indexed evidence is unavailable,
but an execution constrained to a complete materialized index must fail rather
than silently switch to per-target fetching. Descriptor evidence may be reused
only within its valid transaction/schema context.

Index-backed execution does not change the storage boundary. Substring matching
over an already materialized collection does not require a new storage search
operation. Future guest-side evaluation or pushdown must preserve the same
validation, errors, and results and state its fallback/failure contract explicitly.

### Authoring and consumer boundaries

A general authoring experience can expose Property, Operator, and authored
operands. A pre-scoped experience may fix any of them while producing the same
complete Predicate. A search field can fix Key and Contains and supply a single
literal; the backend sees an ordinary ComparisonPredicate. A column filter can
fix the selected property. Neither teaches Space Navigator operator semantics.

Predicate Editors may expose groups, sentence-oriented conditions, visual trees,
or constrained forms. Their model includes `Not`, `AllOf`, and `AnyOf` even when
a particular experience exposes only a single leaf. Operator metadata enables
new operators to participate without changes to a generic editor.

The authoring architecture proposes a `PredicateEditor` VisualizerKind and
a `PredicateAuthoringContext` carrying candidate-type context, a pre-scoped
property, an existing predicate, editability, and permitted operator/composition
subsets. Their concrete DAHN schema and slot contracts are separate HX design
work, subject to the current
[slot-directed Visualizer selection architecture](../hx/dahn-design-spec.md#1421-slot-directed-descriptor-selection).
Query execution depends on none of those visualizers. ValueTypes describe
operand values; operators describe required operands; HX designers choose how
to present their authoring. These remain independent extension points.

### Unsupported predicates and execution outcomes

A runtime lacking a concrete Predicate form, operator, or predicate-bearing
expression must fail explicitly with `HolonError::NotImplemented`, never return
unfiltered members. Misplaced or multiple attachments must not bypass
validation. The root-only contract for SeedHolons takes precedence: an off-root
SeedHolons remains an `InvalidParameter` error even with a predicate.

A reached expression that fails validation or evaluation is `Failed` with no
`Result`; its execution instance is `Failed` with no `ExecutionResult`. Earlier
completed steps retain their results. No partially filtered output is published
as success. A runtime may support a subset of the full Predicate model, but its
capability boundary must be explicit and must not redefine the shared grammar.

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
| `PropertyName` | Required string-valued InstanceProperty with no default. Names one property on each input holon's effective property surface. No path syntax or computed expression. |
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
missing or non-string PropertyName values, invalid enum values, or required values
unresolved after read-only effective-value resolution are contract errors. Validate spec
shape even for empty input collections.

#### Comparison and missing values

Read the required `PropertyName` from each spec and resolve that name against
each member's effective property surface using the shared property-descriptor
lookup. Use each resolved PropertyDescriptor's requiredness and effective
ValueType; do not select one member's PropertyDescriptor as the declaration for
all other members. Validate every input occurrence, including singleton
collections and keys that do not affect the eventual ordering. An undeclared
property, unreadable member, malformed value, or absent required property fails execution; none is treated as a
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
compatibility between distinct value types. Distinct PropertyType identities
with the selected name are permitted when they resolve to that same effective
ValueType identity. Different keys may use different value types. Requiredness
is checked against each member's own resolved property declaration.

Empty input has no member descriptors against which to resolve PropertyName or
validate comparison domains. It returns an empty collection after validating
spec cardinality, the required string-valued PropertyName, and the effective
enum arguments. It does not require an authoring-time property descriptor.

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

### Distinct

`Distinct` is a concrete `QueryExpression` HolonType that removes repeated holon
identities from a collection. It consumes a `HolonCollectionReference` and
returns a new collection holon containing the first occurrence of each identity,
in input order. A root requires an explicit input collection; a successor
consumes its predecessor's result. See the
[Distinct schema contract](command-dance-query-schema-tdl.md#distinct-schema).

`Distinct` is parameter-free. It declares no additional InstanceProperties or
InstanceRelationships, no predicate attachment, and no operator-specific
runtime bindings. Identity is not configurable per expression; there is no
selector, key specification, or comparison option.

#### Duplicate identity

Two occurrences are duplicates exactly when their `HolonReference` values are
equal under the existing reference-layer equality contract. `Distinct`
introduces no new concept of equality, normalization, or identity resolution.
Any optimized duplicate detection must produce the same duplicate decisions as
pairwise reference equality.

| Reference phase | Equality contract |
| --- | --- |
| Saved (`SmartReference`) | Existing `SmartReference` equality: equal `HolonId` values; local IDs also require the same Space Manager instance. |
| Staged (`StagedReference`) | Same transaction ID and temporary ID. |
| Transient (`TransientReference`) | Same transaction ID and temporary ID. |

References in different phases are unequal, even when they share a lineage.
`Distinct` does not resolve, reload, or normalize references to compare across
phases. Local and external `HolonId` variants are never equal under reference
equality. Within a runtime session, there is one Space Manager instance;
local-space identity is that instance, as used by the reference layer.

External references participate through existing reference equality without
dereferencing them. ExternalId routing and resolution semantics are outside
the `Distinct` contract; duplicate detection makes no claim about whether
unequal references could resolve to the same target.

Holon content and presentation do not establish equality. Property values,
cached property hints, descriptors, keys, versioned keys, and diagnostic or
summary strings do not participate. Different identities with equal stored
values remain distinct. Reference identity remains owned by the reference
layer rather than by individual query expressions.

Property/value-based distinctness is a separate capability requiring its own
selector and comparison contract.

#### Survivor and order

The first occurrence of each identity survives; every later occurrence is
removed. Each survivor retains the original reference value of that occurrence,
including its phase and transaction binding. Retained occurrences preserve
their relative input order.

For example, `[A, B, A, C, B]` produces `[A, B, C]`. Empty input produces an
empty collection. Input with no repeated identity preserves all reference
occurrences and their order. Successful executions always produce a new
collection holon and never reuse the input collection holon.

#### Composition and execution outcomes

`Distinct` operates in authored `Next` order and does not change the meaning of
preceding expressions. Its position is significant. If `Expand(AuthoredBy)`
produces `[P1, P2, P1, P2, P1]`:

- `Expand -> Distinct` yields `[P1, P2]`.
- `Expand -> Skip(1) -> Distinct` yields `[P2, P1]`.
- `Expand -> Distinct -> Skip(1)` yields `[P2]`.
- `Expand -> Limit(1) -> Distinct` yields `[P1]`.
- `Expand -> Distinct -> Limit(1)` yields `[P1]`.

`OrderBy -> Distinct` retains sorted order among survivors. `Distinct` neither
sorts nor reorders and does not require a preceding `OrderBy`.

`Distinct` has no operator-specific argument values to validate. Ordinary query
structure/type validation, unsupported-feature checks, collection access, and
result construction retain their existing contracts. A root without input is a
contract error. Invocation bindings remain governed by the query-wide
[parameter contract](#parameters).

Execution does not mutate the input collection, its members, or the query
definition. The expression publishes its new result collection only after
successful execution, under the ordinary execution identity and failure
contracts. A reached `Distinct` that fails is `Failed` with no `Result`; its
execution instance is `Failed` with no `ExecutionResult`. Earlier completed
steps retain their status and results.

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
