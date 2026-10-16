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

Every operand and result collection declares exactly one `ElementType` relationship
to a `HolonType.TypeDescriptor`. Members conform to that declared type and may be
instances of its subtypes. Concrete member diversity does not give the collection
multiple query contracts.

Holonic query expressions select properties and relationship channels by name.
At execution time, resolve selectors through the declared ElementType's effective
surface, including inherited declarations, using shared descriptor facilities.
Member subtypes do not enlarge the selectable surface or replace the selected
property's ValueType, requiredness, operator, or traversal contract. A property
available only on a subtype is not selectable from a collection declared at its
ancestor type, even when every current member has that subtype.

An undeclared selector is an error; absence of a declared optional value is a
different condition. Validate selected contracts and operator applicability even
on empty collections: the declared ElementType supplies the contract without an
invented representative member. Collection membership and stored-value conformance
are responsibilities of collection construction/mutation and the established data
validation lifecycle. The query engine relies on those invariants; it does not
revalidate each member's descriptor lineage or configured value constraints.

Type admission is inheritance-aware: a holon has the required type when its
resolved describing type is that descriptor or extends it. Typed query wrappers
and executable form classification must accept extension types through supported
ancestor contracts, not require an exact local TypeName. Shared descriptor identity
and inheritance facilities own this check; unrelated same-named descriptors are
not equivalent.

Shared descriptor facilities own inheritance and member-name resolution. Query
expressions do not implement parallel duplicate-declaration rules. Selectors
remain names in reusable definitions; execution must not replace them with
resolved descriptors or write runtime bindings into those definitions.

This policy applies to Expand, Filter/ComparisonPredicate, OrderBy, and
future Project. Filter, OrderBy, Distinct, Skip, and Limit preserve the
input ElementType. Expand resolves its channel from the source ElementType and
derives the output ElementType from the resolved traversal target contract;
SeedHolons derives it from the focal HolonSpace's Owns target contract. Members
from all source occurrences are governed by that output contract; establishing
conformance belongs to the data/reference lifecycle, not a query-level scan. Projection
requires its own materialized output contract.

Selector resolution is distinct from invocation parameter binding and query
persistence. A textual front end can construct the same name-based holonic
representation without authoring-time descriptor binding. Saved-query replay
and version guarantees require their own contracts.

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

`Expand` resolves the requested channel through the source collection's declared
ElementType using shared declared-or-inverse relationship resolution. It traverses
each source reference through ordinary reference operations and derives the result
ElementType from that resolved channel's target contract. It does not resolve a
new channel contract from each member subtype. Descriptor and traversal errors
propagate unchanged.

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

A ComparisonPredicate applies an operator to the value of one named property.
The selected property's value supplies the subject; the definition supplies the
remaining operands. For fixed execution arity, its canonical forms are:

| Execution arity | Canonical predicate content |
| --- | --- |
| Unary | (property_name, operator) |
| Binary | (property_name, operator, operand_value) |
| Ternary | (property_name, operator, operand_value_1, operand_value_2) |

The uniform model is (property_name, operator, ordered_authored_operands), with
exactly arity minus one authored operands for a fixed-arity operator. The ordered
sequence is extensible; it is not an exhaustive enum of supported arities. Each
position has the type and semantic role prescribed by the operator's operand
specification. Ergonomic constructors may accept different representations of
property and operator selectors, but must produce this same canonical holonic
representation. A supplied PropertyDescriptor guides construction; the definition
retains PropertyName for resolution against the execution ElementType.

A single filter specification is a ComparisonPredicate, not a second FilterSpec.
The following declared members realize that semantic model:

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
property selector and execution resolves it against the collection's declared
ElementType. There is no separate key-only predicate syntax: selecting the canonical `Key` property
uses the same representation as selecting another scalar property.

#### Typed literal operands

LiteralOperand is a Query-owned holon representing one (declared ValueType, value)
pair. Its required OperandValue property is described by Core's existing
BaseValueValueType.ValueType, allowing scalar string, integer, Boolean, enum, and
bytes representations. Exactly one ValueType relationship identifies its declared
ValueType descriptor. ValueType is a relationship, not a property containing a
type name. Scalar BaseValue does not represent value arrays or arbitrary structured
values; those require separately specified envelopes.

ComparisonPredicate.Operands is an ordered zero-or-more relationship to
LiteralOperand. The operator's specification determines the valid count. A
transient constructor accepts Vec<HolonReference>, verifies the targets are
LiteralOperand instances or conforming extension types, and preserves vector
order in that relationship. A resolved execution slice of BaseValue values is
operational state, not a replacement authored representation.

For a literal with declared type D and operator-required type R, D must be R or
extend R by descriptor identity. Validate the value against D and R using the
shared value-validation capability for the applicable supported semantics. Schemas
used for execution must not attach effective constraints whose evaluators are
unavailable; such contracts cause validation failures. Declaring constraint types
for future support is distinct from attaching unsupported constraint instances.
Unknown or unsupported required constraints fail explicitly, never silently pass.
A broad declared type cannot satisfy a narrower
requirement merely because one value happens to fit it. Ordinary constructors
can declare R directly; specialized authors can declare a conforming subtype.
The operator's R is independent of the property's ValueType unless its operand
specification explicitly selects SameAsSubject.

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

Core owns OperandSpecification holons and the operator descriptor's ordered
OperandSpecifications relationship, exposed as an InstanceRelationship through
MetaOperatorType. Each specification carries required OperandRole and DisplayName
strings, optional Description, and required OperandValueTypeRule with these values:

| Rule | Required operand ValueType |
| --- | --- |
| SameAsSubject | The exact resolved subject ValueType, retaining all effective constraints. |
| FixedValueType | The descriptor referenced by exactly one OperandValueType relationship on the specification. |

OperandValueType must be absent for SameAsSubject and present exactly once for
FixedValueType. No inferred subject-family rule or primitive-kind fallback exists.
Specifications are ordered by relationship position, not a second index property.
For a fixed-arity operator, specification count equals Arity minus one; unary
operators therefore permit zero specifications.

Equals and LessThan each declare one SameAsSubject specification with role
ComparisonValue. Contains declares one FixedValueType specification with role
Substring, label Substring, and OperandValueType pointing to
MapStringValueType.StringValueType. Its subject is an eligible MapStringValueType
or descendant, but its substring need not satisfy the subject's specialized
constraints. Each literal still satisfies its own declared type and the required
operand type. Core metadata has no dependency on Query's LiteralOperand type.

Arity and OperatorCategory alone do not fulfill this contract. Operator categories
remain extensible beyond equality and ordering.

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
zero, one, and multiple authored operands across different operators rather than
permanently assuming `lhs, rhs`. Each invocation must match the selected operator's
total execution arity (subject plus authored operands) and its ordered operand
specifications in count and type. Contains has execution arity two and requires
exactly one authored scalar string. Zero or multiple authored operands, or an
array-valued operand, are invalid. Multiple search terms require distinct leaves
with explicit Boolean composition; they are not multiple operands to Contains.
Operator-specific constraints belong to the operator/value layer.
Security-aware operator availability and array predicate semantics are outside
this contract.

#### Scalar equality and validation lifecycle

Equals compares scalar values under the selected ValueType's equality semantics.
Operator resolution validates descriptor-backed applicability, affordance, arity,
and operand specifications. Resolved invocation checks the native representations
needed for comparison; it does not establish full value conformance or read
descriptor declarations on each comparison. This boundary also applies to binary
convenience APIs over the shared operator execution path.

For enum equality, both values must use the enum representation and their variant
tokens are compared for equality. Invocation does not check either token against
the descriptor's declared variants. Predicate definition validation must establish
authored-literal enum membership against both the declared and required ValueType
contracts. Stored enum membership belongs to the data construction and validation
lifecycle, not to filtering. An undeclared stored token therefore compares unequal
to a valid authored token; a non-enum representation is an execution error.

Callers requiring value conformance must invoke the shared validation capability
explicitly. Operator execution is not an implicit validation operation. String
Equals remains ordinal and case-sensitive, without case folding, normalization,
or locale tailoring; matching-operator policy does not change equality.

#### String matching operators

The string ValueType family affords three distinct matching operators through
the ordinary inherited `AffordsOperator` relationship. Each has a string subject,
exactly one authored scalar string operand, and a Boolean result. They belong
to the `Matching` operator category, distinct from Equality and Ordering:

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

CaseMatching is Core-owned operator metadata with enum values CaseSensitive and
UnicodeDefaultCaseFold. It is not category metadata, a Predicate property, a
Search parameter, or a change to Equals/LessThan. The Contains descriptor declares
UnicodeDefaultCaseFold as its default effective mode. A separately afforded
operator descriptor using the supported Contains ancestor contract may declare
CaseSensitive. Resolve the effective policy through shared descriptor facilities;
missing, ambiguous, unknown, or unsupported effective modes are explicit errors.

CaseSensitive performs literal substring matching on the original scalar sequence.
UnicodeDefaultCaseFold applies Unicode 17.0.0 full default case folding to both
complete strings, then performs literal substring matching on the folded strings.
Use the C and F mappings in that version's CaseFolding.txt; do not use simple-only
S mappings or Turkic T tailoring. Code points without a mapping remain unchanged.
Do not normalize, strip accents, apply locale/browser rules, or perform wildcard
or regex interpretation. Folding does not mutate stored strings or authored values.

Matching is defined over the folded scalar sequences, including expansions; it
is not constrained to original grapheme or character boundaries. For example,
Straße matches STRASSE, and a substring s also matches the folded ss contributed
by ß. Greek final sigma and ordinary sigma fold alike. Composed and decomposed
accented spellings are not guaranteed to match; canonical equivalence is not part
of this contract. Empty literals retain the substring semantics below.

The Unicode version is part of the matching contract, not an implicit property of
the compiler or selected dependency. Implementations must use those exact tables
and yield identical host/guest results. The normative mapping data is
[Unicode 17.0.0 CaseFolding.txt](https://www.unicode.org/Public/17.0.0/ucd/CaseFolding.txt).
Dependency selection must preserve this policy rather than silently substituting
std lowercasing or another Unicode release. Like and MatchesRegex must separately
define interaction with this policy; do not lowercase their patterns implicitly.

An explicitly authored Contains with an empty literal follows substring semantics
and matches every present valid string. It remains a predicate application.
A consumer wishing to express no filtering omits its predicate/filter instead.

### Shared validation and evaluation

The query engine validates supplied query definitions, including authored literal
operands. It does not validate collection membership or stored data conformance.
The declared ElementType is the authoritative input contract, including for an
empty collection. Collection construction/mutation and the established data
validation lifecycle own member conformance and stored-value constraints.

#### Predicate validation

Provide an explicit validate operation taking the predicate and declared
ElementType. It performs no candidate iteration or candidate-property reads.
For each comparison leaf it must:

1. Validate structural shape and supported Predicate capability, including a
   present string PropertyName, exactly one Operator, and an ordered operand list.
2. Resolve PropertyName on ElementType's effective available property surface,
   including inherited declarations, through shared descriptor facilities. An
   unavailable selector is an error. Retain its ValueType and requiredness.
3. Validate the subject-type requirement of the selected operator through shared
   inheritance-aware type membership. Contains requires a ValueType that has
   MapStringValueType in its type lineage. This is not a string restriction on
   all ComparisonPredicates; other operators prescribe their own subject domains.
4. Verify that the selected Operator is effectively afforded by that property's
   ValueType, including inherited affordances. Use shared effective lookup, not a
   query-local operator registry or a direct-only inverse relationship check.
5. Resolve the operator's ordered authored-operand specifications in the selected
   subject-type context. Check total execution arity equals one plus authored
   operand count and that count/order match those specifications.
6. Validate every authored literal against the ValueType required at its operand
   position, including applicable effective value constraints and operator-specific
   restrictions. The operand type is prescribed by the operator; it must not be
   assumed identical to the property's ValueType. Matching primitive representation
   alone is not full literal conformance. Validate declared-versus-required type
   compatibility as specified by the typed literal envelope.

For composition, validate shape, child cardinality, cycles, capability, and every
child definition before execution. No branch's Boolean result can exempt another
branch from definition validation. Unsupported executable forms fail explicitly;
malformed definitions and unavailable affordances are validation errors.

Validation may return an execution-local resolved predicate containing the selected
property contract, operator, and validated operands. Reuse that result for the
member sequence within its valid transaction/schema context. Do not mutate or
cache bindings in caller-owned definitions, and do not treat authoring-time
validation as a substitute for execution-time query validation.

#### Predicate execution

Execution reads selected values through ordinary bound reference access and
applies the validated operator through the shared value/operator layer. It must
not scan DescribedBy/Extends on members, call a general member-conformance validator,
or re-run configured stored-value constraints. The operator/value layer still
checks the runtime representations necessary to execute the operation safely;
an incompatible representation is an execution error, not coercion or omission.

An absent optional property makes the comparison false; an absent required
property fails execution. These are operation outcomes, not a whole-data validation
pass. Access failures propagate. Not negates the optional-absence Boolean result;
there is no implicit three-valued/null logic.

Required value access, presence, and representation checks apply to every selected
leaf and occurrence. A true AnyOf branch cannot hide a read failure, missing
required subject, or unusable runtime representation in another branch. Neither
success nor failure mutates supplied definitions. Results are published only after
execution succeeds for all required occurrences.

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
operator semantics, source-versus-target ambiguity, or a new storage search operation.
An attached predicate and a subsequent Filter remain separately authored
applications; an implementation must not accidentally apply one attachment twice.

An author can therefore express either an expansion with an attached Predicate
or an explicit `Expand -> Filter` chain. `SeedHolons` provides the focal-space
Owns expansion. The choice of attachment or expression does not change the
predicate representation supplied by a programmatic caller, agent, or UI.

### Collection Search

Collection Search is a Dance afforded by HolonCollection. Its implementation
constructs a synthetic query above the raw query engine. It is not a concrete
Search QueryExpression and has no SearchText property in the Query schema. The
Dance operates on its affording collection, accepts scalar search text, resolves
that collection's declared ElementType, and obtains its effective property
declarations through shared descriptor APIs.

Select all properties whose ValueType is MapStringValueType or a subtype. Include
inherited properties; exclude subtype-only member properties, non-string values,
arrays, and textual coercions. Each selected declaration must afford Contains and
satisfy its operand contract; unsupported properties are errors, not silently
omitted branches.

Construct one ComparisonPredicate per selected property with Contains and exactly
one authored scalar string operand carrying the search text. Relate the leaves
through a flat AnyOf and attach that predicate to an ordinary Filter expression.
The generated query enters the same direct or QueryDance execution path as any
caller-authored query. There is no trusted/internal graph marker or privileged
Search execution route. A per-property filter authors one leaf; collection Search
constructs the disjunction over the eligible declared property set.

Construction-time descriptor lookup guides authoring but does not replace runtime
validation. The engine validates selectors, operator availability, and authored operands
against the execution input's ElementType, without revalidating members or stored
value constraints. It reads values through ordinary bound references and performs
only the representation/presence checks required for execution. A match in one branch cannot hide an
unusable runtime representation, missing required property, or access failure
in another branch.
Each matching input occurrence survives once, even when several properties match;
order, multiplicity, reference identity/binding, and ElementType are preserved.

The generated predicate names an explicit property set. This contract does not
settle persistence of synthetic Search intent, regeneration, saved-query forms,
or schema replay guarantees. Such facilities may live above the raw query layer.

AnyOf requires one or more children. If no properties are eligible, construction
reports an explicit no-searchable-properties error; do not create an empty AnyOf
or silently substitute an unfiltered query. Explicit empty search text follows
Contains semantics: it matches an occurrence with at least one present valid
selected string, not one whose selected optional values are all absent. Clearing
Search means omitting the generated filter.

### Property access and optimization

Query execution reads properties through ordinary bound HolonReference operations.
The Reference Layer decides whether cached reference properties, an in-memory
holon, the holon cache, or a storage fetch supplies a value. Query evaluation must
not classify references by expected fetch cost, impose a no-fetch precondition,
or infer property absence from an incomplete collection key index.

The collection's current key-to-single-position index is not an occurrence index.
Filter, including generated Search queries, iterates the member sequence; repeated identities or keys remain
separate occurrences. Key uniqueness within a namespace, if enforced elsewhere,
does not imply occurrence uniqueness. This query contract adds no key-uniqueness
policy and requires no key/index evidence redesign or special result-insertion API.

An index may later optimize access only if it preserves declared-type validation,
value/error semantics, occurrence coverage, order, and multiplicity. A text index,
storage search operation, or pushdown is not a prerequisite for collection Search.
Reference operations remain the only storage access path.

### Authoring and consumer boundaries

A general authoring experience can expose Property, Operator, and authored
operands. A per-property filter fixes the selected property. The HolonCollection-afforded Search Dance resolves ElementType and constructs
Filter + AnyOf + Contains over eligible properties. Consumers invoke the Dance
with search text; they do not duplicate descriptor selection or comparison semantics.
The query engine executes ordinary predicates and validates their contracts.
The frontend owns text entry, clearing, and display. CollectionVisualizer exposes
the collection's Search Dance through the existing descriptor-afforded Dance
invocation mechanism. The Dance contract, affordance declarations, implementation,
and consumer binding belong above the query engine. Query owns ComparisonPredicate,
Filter, AnyOf, Contains execution, and their validation; it neither implements the
Search Dance nor depends on that consumer. The Search request/response schema
belongs to the Dance capability, not the Query expression vocabulary.

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
| `PropertyName` | Required string-valued InstanceProperty with no default. Names one property on the input collection's declared ElementType surface. No path syntax or computed expression. |
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

Read PropertyName from each spec and resolve it against the input collection's
declared ElementType. Its effective PropertyDescriptor fixes requiredness and
ValueType for every occurrence, including subtype instances. Validate the query
specifications and supported comparison domains before reading members. Execution
checks required presence and usable runtime representation for each accessed key,
including singleton collections and non-decisive keys. It does not revalidate
member lineage or configured stored-value constraints. Undeclared selectors are
query errors; read failures, required absence, or unusable representations are
execution errors.

An absent value is sortable only when that selected contract permits absence.
Missing-First places it before present values; Missing-Last places it after them.
Two missing values tie. Direction changes only present-value order.

The supported domains are descriptor-backed integer and string values affording
supported equality and less-than operations. Different sort keys may select
different ValueTypes. Member subtypes do not rebind a sort key to a different
property or value descriptor.

For empty input, validate spec shape, arguments, declared-property resolution,
and comparison-domain support using ElementType, then return an empty collection
with that ElementType. No member descriptor or invented representative is needed.

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
