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
[unsupported predicate contract](query-engine-design-spec.md#unsupported-predicates-and-execution-outcomes).
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

Until separate runtime binding is supported, `QueryReference::begin_execution`
rejects any nonempty invocation binding list with `HolonError::NotImplemented`
as its first operation, before root/input validation or creation of an
`ExecutionInstance` or `QueryExpressionExecution`. No execution records are
created for this rejection. Empty binding lists proceed through ordinary
execution. QueryDance forwards `RequestParameters` to this same entry point;
it does not implement an alternative binding check. Its Dance ingress validation
still precedes entry into QueryCore. The direct single-holon helper also delegates
binding rejection to this entry point. QRY6 replaces this transitional refusal
with the target binding contract.

### QRY4a — Transient query authoring, ordering, and pagination

Author `Query` and concrete `QueryExpression` holons as transient definitions,
attach concrete holonic arguments, and execute through direct QueryCore and
QueryDance without staging or committing the query graph. Keep execution
status, input, and results on separate runtime execution records.

- `Expand` retains its existing concrete relationship-name argument.
- `OrderBy` relates directly to one through five `OrderBySpec` holons through
  an ordered relationship. Each spec carries a required string-valued
  `PropertyName` with no default and required enum properties with
  descriptor-defined defaults. Resolve the selected name against each input
  holon's effective property surface at execution time.
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
or separate invocation parameter binding. Selector-name resolution is part of
expression execution and is not the deferred parameter binder. Keep unsupported
predicate attachments rejected. `Distinct` and `Project` remain separate follow-ons.

### Selector-resolution adjustment — 2026-10-01

OrderBySpec selects a property by required string-valued PropertyName rather
than a Property relationship to a particular descriptor. Align the executable
TDL and regenerate loader artifacts; update authoring helpers and both Direct
and QueryDance fixtures. This follows the authoritative
[name-selection policy](query-engine-design-spec.md#name-selection-and-execution-time-descriptor-resolution)
and does not introduce invocation parameter binding or decide saved-query forms.

Cover independently valid types declaring distinct same-named PropertyTypes:
accept them when they resolve to the same effective ValueType identity, and
reject incompatible value descriptors even when values are absent. Retain
undeclared-name rejection, per-member requiredness and value validation,
including singleton and non-decisive keys, and unchanged-definition assertions.
Cover missing/non-string PropertyName arguments on empty input, valid five-spec
and invalid zero/six-spec boundaries, and read-only enum-default failure paths.
A former same-name/different-PropertyType-identity rejection test is superseded
by these name-resolution and value-compatibility tests.

### QRY4b — Identity-based distinctness

Implement the [Distinct contract](query-engine-design-spec.md#distinct) and its
[parameter-free schema](command-dance-query-schema-tdl.md#distinct-schema).
Duplicate detection uses the existing `HolonReference` equality contract; no
query-specific equality or identity normalization is introduced. The first
occurrence of each identity survives as its original reference value, retained
occurrences preserve input order, and the result is a new collection holon.
Any optimized duplicate detection must agree with reference equality. Do not
substitute content equality or a diagnostic-string identity key.
Property/value-based distinctness is outside this delivery.

Add `Distinct` to the executable Query TDL and regenerate canonical loader
artifacts through map-schema. Recognize and dispatch it through the existing
QueryCore transformation lifecycle on both direct and QueryDance routes,
preserving caller-owned definitions and reference bindings.

Cover empty, singleton, all-unique, adjacent and separated repetitions,
all-identical input, equal-value/different-identity members, and composition
with Expand, OrderBy, Skip, and Limit. Verify first-occurrence reference
retention, stable order, new result-collection identity, required root input,
and ordinary execution failure attribution. Cover the reference equality
boundaries for phases, transactions, and owning spaces; use unit tests for
identity combinations that runtime collections cannot legitimately contain.
Follow the singleton Space Manager and definitional space-ownership contracts
rather than introducing alternative identity semantics for unsupported cases.

QRY4b also carries two regression tests deferred from the QRY4a OrderBy
delivery in PR #767. They are coverage gaps, not demonstrated runtime defects:

- The read-only effective-value accessor propagates an authored-value read
  error even when a usable descriptor default exists. Where the fixture permits,
  verify that default resolution is not attempted after the read error.
- An OrderBySpec type declares a valid required string-valued `PropertyName`
  and supplies its value, but omits the `SortDirection` declaration. Other
  fixture prerequisites are valid. Assert `DescriptorDeclarationNotFound`
  identifies `SortDirection`, rather than accepting a failure on `PropertyName`
  or silently using an ascending default.

### QRY4c — Projection specification and materialization

Define the projection specification and materialized output structure, then
implement `Project` with a concrete holonic projection specification attached
to the transient expression. Settle
selected property naming, materialized property values and their type
information, missing-value behavior, retained source identity if any, and how
the output fits the collection-based execution contract before implementation.

Resolve property-name selections at execution time through shared descriptor
facilities, following the query-wide name-selection policy. Treat `Project` as explicit
materialization, not as a replacement for `HolonCollection` navigation.

### Delivery-boundary adjustment — 2026-09-27

The initial proposal to combine QRY3 binding with QRY4a is superseded:
**QRY4a** now delivers transient authoring, ordering, and pagination;
**QRY3's runtime binding work moves to QRY6**, alongside saving and replay.
QRY4b retains identity-based distinctness and QRY4c retains projection.
QRY5–QRY8 retain their identifiers. These are intended PR boundaries; only
QRY4a's issue is currently requested. Retain original tracker estimates and
use dated adjustment rows for any later re-estimation.

### Filtering delivery adjustment — 2026-10-06

Restore the full Predicate design while delivering executable support in small
increments. This replaces the earlier requirement to finish every operator
arity and Boolean composition form before delivering useful filtering.
The [shared Predicate model](query-engine-design-spec.md#shared-predicate-model-and-schema-contract)
is the semantic foundation for every increment; implementation deferral does
not remove a form from that model or permit a competing representation.

Use `QRY-F1` onward for the filtering sequence below without renumbering
QRY0–QRY8. These are planned delivery boundaries, not claims of completed work
or assigned GitHub issues. Ground each issue against current code before
implementation. Planned estimates are recorded below; no tracking-sheet values
are changed by this plan.

The first slice establishes generic construction, validation, evaluation, and
query integration with Contains. Subsequent slices mostly add operators through
that machinery; recursive Boolean evaluation is one separate extension.
Neither a generic Predicate Editor nor Space Navigator UI is a backend
prerequisite. Guest/storage pushdown is also a later optimization, not a gate
on correct local evaluation over a materialized collection.

#### Planned Dev Points — 2026-10-06

Estimated with the repository's `estimate-dev-points` rubric against this plan
and the query-engine design specification. These are Planned PR-chunk estimates,
not issue-grounded Defined estimates or delivered actuals. Re-estimate when each
issue is grounded; retain this dated baseline when recording adjustments.

| Unit | Lifecycle phase | Estimate | Rationale | Re-estimation trigger |
| --- | --- | ---: | --- | --- |
| QRY-F1 — Shared scalar filtering with Contains | Planned | 8 | Cross-cutting foundation: operand schema/metadata, generalized invocation, leaf evaluation, three query entry forms, and index-preserving collection execution. Operand representation, Unicode policy, and occurrence coverage remain uncertain. | Grounding reveals an independent collection/index redesign, broad compatibility migration, or SDK/UI scope; decompose before implementation if these cannot remain one coherent PR. |
| QRY-F2 — Equality through the Predicate path | Planned | 3 | Reuses existing equality execution, but adapts metadata and validates typed operands across several scalar domains through the new predicate path. | F1 does not provide reusable typed operand dispatch, or equality expands beyond currently supported scalar domains. |
| QRY-F3 — Recursive Boolean composition | Planned | 3 | One cohesive schema/evaluator extension with recursive construction, structural validation, and nontrivial error/short-circuit tests. | Composition requires a broader graph-validation framework, depth/resource policies, or changes to the specified validation semantics. |
| QRY-F4 — Ordered scalar comparisons | Planned | 3 | Reuses ordering primitives while adding three related comparison operators, affordances, metadata, and boundary/type tests. | New ordering domains, coercion, locale collation, or incompatible descriptor behavior enter scope. |
| QRY-F5 — Multiple authored operands with Between | Planned | 3 | Exercises two ordered typed operands and cross-operand validation through the existing general invocation contract; bound semantics still need resolution. | F1's operand model needs redesign, or open/unbounded ranges and additional interval policies are included. |
| QRY-F6 — Additional string operators | Planned | 2 | StartsWith and EndsWith follow the Contains pattern and reuse its settled text policy; focused metadata and semantic tests. | Prefix/suffix matching cannot reuse the text policy or requires new normalization/index behavior. |
| QRY-F7 — Wildcard matching with Like | Planned | 3 | A bounded new pattern contract and matcher with escaping, match-scope, Unicode, and error tests; predicate integration is reused. | Wildcard syntax grows into a richer pattern language, or execution requires a new shared pattern runtime. |
| QRY-F8 — Regular-expression matching with MatchesRegex | Planned | 5 | Requires regex dependency/runtime compatibility decisions, dialect and flag contracts, execution bounds, and error mapping in addition to operator integration. | No suitable engine supports the required host/guest targets, or requested dialect features require custom execution/isolation. |

**Roll-up: 30 Dev Points**, the sum of the eight proposed PR chunks. This is not
a separate track-level estimate or a calendar forecast.

Assumptions: QRY-F1 supplies genuinely reusable schema, operand invocation,
validation, and query integration; later chunks do not repay that foundation.
Existing descriptor/equality/ordering facilities are reused. Each operator
increment includes its necessary schema artifacts, focused documentation, and
unit/integration validation. SDK/DAHN integration, Predicate Editor UI, saving,
parameter binding, and storage/distributed optimization remain excluded.
MatchesRegex assumes reuse of a suitable regex engine rather than implementing
one. The unresolved matching policies are included as bounded design work.

QRY-F1 receives 8 rather than a routine 5 because its contracts and index path
are not yet fully grounded. Its scope is one coherent backend capability, but
it is the primary decomposition risk. If grounding exposes independently
shippable infrastructure changes, split them into named PR chunks and estimate
those separately; do not treat 8 as a cap on an oversized bundle.

#### QRY-F1 — Shared scalar filtering with Contains

**Depends on:** the existing Query execution/Next scaffold, SeedHolons/Expand,
descriptor property resolution, ValueType operator affordances, and transient
definition construction. Reuse delivered QRY4a construction facilities where
available; sorting, pagination, projection, saving, and parameter binding are
not semantic prerequisites for filtering.

**Deliver:** a standard ComparisonPredicate selecting a scalar property, an
operator descriptor, and authored operands, evaluated through both Filter and
the existing expansion predicate attachments. Contains is the first supported
predicate operator. Key is an ordinary PropertyName selection, not a special
predicate form or Search argument.

Work within this slice proceeds in dependency order:

1. Finalize the concrete operand-value envelope and ordered operator operand
   specifications in the schema companions and executable TDL. Preserve the
   distinction between total execution arity and authored operand count. The
   invocation shape accepts an operand sequence even though Contains needs one
   authored value. Existing binary callers retain their behavior.
2. Declare ComparisonPredicate and Filter using the shared schema anchor and
   contracts. Supply narrow programmatic construction helpers for transient
   definitions and fixtures. Keep unsupported composition forms explicit;
   runtime support for every form is not required in this slice.
3. Add the Contains descriptor, string ValueType affordances, authored-operand
   metadata, validation, and literal substring evaluation through the existing
   value/operator layer. Settle the generic case policy, its default, and exact
   Unicode behavior in the normative operator contract before implementing
   case-insensitive execution. No browser-locale or DAHN-specific semantics.
   Record Like and MatchesRegex as distinct intended string-family affordances;
   their runtime implementation is deferred to QRY-F7/F8. If their descriptors
   are declared early, discovery must not imply executable support and invocation
   must fail explicitly. Do not substitute Contains for either operator.
4. Implement shared leaf validation/evaluation, including descriptor-backed
   property resolution, optional/required missing values, empty input, operand
   compatibility, and explicit errors. Support eligible scalar string
   properties generally, not only Key; unsupported operators fail explicitly.
5. Integrate the same evaluator into Filter, SeedPredicate, and
   ExpansionPredicate. Preserve root/input rules, Next chaining, execution
   records, unchanged definitions, and ordinary collection results. Replace
   blanket attachment refusal only for supported, correctly placed predicates.
6. Preserve complete key/index evidence through materialized expansion and
   filtering. Execute Key comparisons and construct indexed results without
   per-target key reads. Validate occurrence coverage; do not lose duplicate
   occurrences or infer absence from an incomplete single-position index.

**Delivery proof:** programmatically authored direct and QueryDance invocations
exercise attached expansion predicates and an explicit Expand/SeedHolons →
Filter chain. Both routes return equivalent membership for the same predicate.
Also exercise Filter as a root over a retained collection. Cover another
declared string property to prove the predicate is not key-specific, and
instrument the complete-key-index path to prohibit matching/result-construction
key fetches. Verify literal metacharacters, substring and case behavior,
non-matches, absent optional values, invalid inputs, duplicate occurrences,
empty results, and failure records. A no-predicate expansion remains distinct
from Contains with an explicitly empty literal.

**Consumer handoff:** this is the backend dependency for Space Navigator Search.
The frontend owns text entry, clearing, occurrence state, and result display.
Its required SDK/command adapter must carry ordinary query/predicate definitions
and collections; it may be delivered with that integration without introducing
a Search endpoint. Search fixes PropertyName to Key and the operator to Contains;
the backend syntax remains general.

#### QRY-F2 — Equality through the Predicate path

**Depends on:** QRY-F1.

Expose existing Equals execution through the shared predicate invocation and
authored-operand metadata. Start with scalar domains already supported by
ValueDescriptor and their declared affordances; do not expand to arrays or
silently coerce incompatible values. This is primarily integration of an
existing operator, not another equality implementation.

**Delivery proof:** equality predicates execute through the same construction,
validation, Filter, and attachment paths across supported scalar ValueTypes.
Cover semantic type compatibility, enum constraints where supported, missing
values, and rejection of unafforded operators. Preserve existing string
equality semantics independently of Contains's matching policy.

#### QRY-F3 — Recursive Boolean composition

**Depends on:** QRY-F1; use QRY-F2 when equality leaves are needed by fixtures.

Complete concrete Not, AllOf, and AnyOf schema/construction support and shared
recursive validation/evaluation. Preserve explicit child scope and distinguish
predicate children from expression Next links. Apply the normative rules for
cardinality, cycles, unsupported branches, missing values, and short-circuiting.
No Predicate Editor or logical-grouping UI belongs in this slice.

**Delivery proof:** nested mixed-operator predicates work identically through
Filter and expansion attachments. Negation of an absent optional value follows
the specified Boolean semantics. Malformed or unsupported branches fail even
when another branch would determine the Boolean result.

#### QRY-F4 — Ordered scalar comparisons

**Depends on:** QRY-F1. QRY-F3 is useful for combinations, not required to execute
an individual comparison.

Expose existing LessThan semantics through Predicate metadata/evaluation, then
add GreaterThan, LessThanOrEqual, and GreaterThanOrEqual as separately afforded
operators where their ValueTypes define the required ordering. Reuse the
value/operator comparison machinery rather than copying OrderBy comparisons
into predicates. Specify each new operator's contract before implementing it.
These additions may become separate issues when grounded scope warrants it.

**Delivery proof:** strict and inclusive boundary cases, supported integer/string
domains, incompatible types, and inherited affordances. A new operator requires
metadata and value/operator execution changes, not Filter dispatch branches or
consumer changes. Do not infer ordering for enums or other domains merely from
their primitive representation.

#### QRY-F5 — Multiple authored operands with Between

**Depends on:** QRY-F1 and the relevant ordered ValueType support from QRY-F4.

Add Between to exercise the already general subject-plus-operands contract.
Declare ordered lower/upper operand roles and their ValueTypes. Define bound
inclusivity, reversed-bound behavior, and cross-operand constraints in the
operator design before implementation. Keep those semantics in the operator
layer; Filter must not acquire special handling for bounds.

**Delivery proof:** operand ordering, exact-boundary behavior, missing/extra
operands, invalid bounds, and type constraints work through the unchanged
predicate/query paths. Metadata can describe two authored values without
operator-specific knowledge in an authoring consumer.

#### QRY-F6 — Additional string operators

**Depends on:** QRY-F1.

Add StartsWith and EndsWith with their own affordances, metadata, and shared
value/operator evaluation. Reuse the generic text policy defined for Contains.
Each operator can ship
independently of Boolean composition and ordered-comparison work.

**Delivery proof:** literal prefix/suffix behavior, empty operands, case policy,
Unicode rules, and invalid operand types. The same ComparisonPredicate shape
and query integration work without frontend or Filter changes.

#### QRY-F7 — Wildcard matching with Like

**Depends on:** QRY-F1; QRY-F6 is not required.

Define Like's wildcard alphabet, literal escaping, match scope, empty-pattern
behavior, and interaction with the generic text policy in the operator contract.
Then add its string-family affordance, authored-pattern metadata, validation,
and value/operator execution. Reuse any earlier descriptor declaration rather
than creating a second operator. Like consumes a wildcard pattern, not literal
Contains text and not a regex.

**Delivery proof:** wildcard and escaped-literal cases, match scope, empty and
invalid patterns, case policy, and Unicode behavior through the unchanged
ComparisonPredicate/Filter path. Identical operand text can intentionally have
different meaning under Contains and Like; neither is silently reinterpreted.

#### QRY-F8 — Regular-expression matching with MatchesRegex

**Depends on:** QRY-F1; QRY-F7 is not required.

Define the regex dialect, flags, whole-value versus partial matching, empty
patterns, Unicode behavior, and invalid-pattern/resource-limit errors before
implementation. Add the string-family affordance, authored-pattern metadata,
validation, and value/operator execution using that explicit contract. Reuse
any earlier descriptor declaration. Pattern validation and execution belong to
the operator layer, with no regex-specific branches in Filter or DAHN.

**Delivery proof:** ordinary and metacharacter patterns, match scope, flags,
invalid syntax, bounded-execution failures, and separation from literal Contains
and wildcard Like semantics. Results and errors follow the existing shared
Predicate/query contracts.

#### Extension rule and deferred capabilities

For each subsequent operator: define semantics, declare affordances and ordered
operand metadata, implement ValueType-owned validation/evaluation, and prove it
through the existing Predicate/query path. Zero-authored-operand operators can
extend the same invocation contract when a concrete need justifies them; any
presence-testing operator first needs an explicit missing-subject contract.

The suggested progression is F1 → F2 → F3 → F4 → F5 → F6 → F7 → F8, but the dependencies
above allow independent operator additions after F1. It is not necessary to
finish the entire operator inventory before a consumer uses filtering.

Keep generic Predicate Editor visualizers, column-filter UI, saved predicates,
runtime parameter binding, arrays, security-aware operator availability, and
distributed/pushed-down execution in separate work. Future access-path
optimizations must preserve the same semantics and expose fallback/failure
behavior; they must not change the Predicate authored by a consumer.

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

The next filtering issue to ground is **QRY-F1 — Shared scalar filtering with
Contains**, using the restored Predicate design and the current QueryCore,
QueryDance adapter, collection index, Query schema, and descriptor/operator
implementation. Reconcile existing QRY4a construction support during grounding;
the former recommendation to create QRY4a here is not a fresh delivery-status
assessment. QRY4b and QRY4c remain separate follow-ons and do not belong in the
first filtering issue. Space Navigator Search is a separate consumer enhancement
depending on QRY-F1's execution contract.
