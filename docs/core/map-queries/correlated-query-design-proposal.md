# Correlated Query Composition — Design Proposal

**Status:** Proposed normative extension; not an assertion of implemented functionality.  
**Scope:** MAP's executable, descriptor-aware query algebra.  
**Primary design constraint:** Every intermediate and final query expression result remains a `HolonCollectionReference` containing holon references.

## 1. What and why (plain English)

A query can follow relationships from one holon to another, but a flat list of destinations does not tell us which starting holon led to which destination. For example, if two books share an author who lives in Rome, finding the cities of all their authors may return Rome twice without retaining which book and author belong to each occurrence. This becomes a problem when we want an output containing the book title, author name, and city name together.

**Correlated query composition** preserves those associations as a query proceeds through multiple steps. Each surviving match retains the holons associated with named variables such as `book`, `author`, and `city`. Subsequent steps can navigate from any bound variable, filter matches, and construct output holons using values from several sources. Duplicate matches remain distinct unless an explicit operator removes them.

## 2. Proposal in brief

1. **Preserve the existing algebraic boundary:** `HolonCollectionReference → QueryExpression → HolonCollectionReference`. Do not introduce a generalized `QueryResult` carrier or a parallel `Bindings` result overlay.
2. **Introduce transient `BindingRecord` holons** representing one complete assignment of named variables to holon references. A collection of BindingRecord references is an ordinary `HolonCollection`.
3. **Introduce `Bind` and `ExtendBindings` expressions.** `Bind` wraps each incoming holon occurrence in a one-variable record. `ExtendBindings` navigates from a named variable and emits one extended record per qualifying relationship-target occurrence.
4. **Extend `Project`** to accept binding records and emit projection holons containing values read from named bound sources. Ordinary single-source projection remains supported.
5. **Keep existing collection operators collection-oriented.** Their input members are BindingRecords when operating on a binding collection. Extend selector/predicate semantics explicitly where variable-qualified access is required; do not silently reinterpret an unqualified selector.
6. **Describe binding shape with query-local, descriptor-backed schema metadata.** The initial implementation materializes transient holons with a concrete, execution-scoped BindingRecord descriptor whose variable-named relationships have declared target types. Do not register a new durable global type for each query stage.
7. **Retain physical optimization freedom.** Expression boundaries expose holon-reference collections. Internal batching, shared reads, or future factorization may optimize execution without changing observable collection and binding semantics.

## 3. Extension of the current implementation and design

The current normative query design uses `Query` and `QueryExpression` holons, `Next` for sequential continuation, `QuerySubTree.Subtree` for composite containment, and separate `ExecutionInstance` / `QueryExpressionExecution` holons for runtime state. A successful expression supplies its `HolonCollectionReference` result to its successor. Direct Query invocation and the `QueryDance` adapter share this engine. These contracts remain unchanged.

The current descriptor contract also remains: each operand/result collection declares **exactly one `ElementType`**, members conform to that type or subtypes, and name-based selectors resolve against the declared element type's effective surface, not opportunistically against individual member subtypes. A binding collection therefore declares the concrete binding descriptor for its stage as its single `ElementType`.

Existing flat `Expand` continues to traverse a named channel and return a flat collection of targets, preserving occurrence multiplicity and traversal order. `SeedHolons`, existing predicate composition, `Filter`, `OrderBy`, `Distinct`, `Skip`, and `Limit` retain their existing contracts unless an explicit extension below applies. The new correlated expressions are **additional concrete `QueryExpression` types**, not a replacement executor, a change to `Next`, or a new row-stream subsystem.

This proposal extends the target design described in `query-engine-design-spec.md`; individual components, including multi-source `Project` and selected-property materialization support, may not yet be implemented. Verify implementation status before planning changes.

## 4. Normative data model

### 4.1 BindingRecord

Declare an abstract `BindingRecord` holon type for correlation artifacts. A concrete query-stage binding descriptor extends `BindingRecord` and declares exactly one **single-valued, required, variable-named relationship** for each variable in scope. The target contract of each relationship is the declared `HolonType` for that variable. Bindings in this first increment contain **holon references only**; scalar and null-valued variables are out of scope.

Illustrative effective surfaces:

```text
BookBinding extends BindingRecord
  book   -> Book [1..1]

BookAuthorBinding extends BindingRecord
  book   -> Book   [1..1]
  author -> Person [1..1]

BookAuthorCityBinding extends BindingRecord
  book   -> Book   [1..1]
  author -> Person [1..1]
  city   -> City   [1..1]
```

The names above identify *query-local generated descriptors*, not permanent domain types. Each BindingRecord instance is a transient holon with its own reference identity. Its bound relationships point to the **original** domain holons; no cloning of books, authors, or cities occurs. Binding creation and filtering must not mutate source holons.

**Occurrence rule:** One incoming collection occurrence can yield one or more distinct BindingRecord occurrences. Two records may contain identical assignments and must remain distinct until explicitly deduplicated. Never key the result solely by the identity of a bound domain holon.

### 4.2 Binding schema and descriptor lifecycle

A query-stage **binding schema** is the ordered mapping `variable name → declared target HolonType`, plus a stable query-stage identity. It is definition-derived metadata, not execution bindings. The concrete descriptor implementing that schema is resolved or constructed in a **query-local/transient descriptor scope**, with the following requirements:

- Derive the schema from the upstream declared collection `ElementType` and the `Bind`/`ExtendBindings` definitions, not by examining the first runtime member.
- Create or resolve a concrete descriptor even for an empty result, so downstream selector validation remains possible.
- Use normal descriptor inheritance and effective-relationship resolution; do not create a parallel ad hoc property/relationship registry.
- Preserve inherited variable relationships when extending a stage; the new descriptor adds exactly the new variable relationship.
- Require unique, valid variable names within a binding schema. Reject rebinding an existing name in this initial increment.
- Scope generated descriptors to the query definition/stage and compatible descriptor versions. Reuse a stage descriptor across invocations when safe; do not globally publish it or persist it as an ordinary domain schema artifact.
- Retain descriptors for as long as a result collection or its records can be referenced. An execution result must never contain references whose descriptors have already been discarded.
- Reject incompatible descriptor evolution rather than silently interpreting saved queries against a different variable surface.

**Implementation note:** Query-local descriptor registration and lifetime management are proposed extensions, not verified existing facilities. If the current descriptor subsystem cannot represent transient concrete descriptors and their relationships, implement that capability as a bounded prerequisite; do **not** bypass the descriptor rules with untyped variable maps.

### 4.3 Variable relationship resolution

A variable name is a **relationship selector on the binding collection's declared ElementType**. Resolve it using the shared effective-relationship facilities, including inherited declarations, and validate that it is a required, single-valued relationship with the declared target type. Resolve it **once per expression contract**, not separately by guessing from each record's concrete contents.

For a given BindingRecord, obtain the variable's target through ordinary holon/reference relationship access. Validate exactly one target and its conformance to the declared target type. Missing, multiply valued, inaccessible, or incompatible bindings are errors, not implicit empty matches. This is distinct from a *valid relationship expansion* that finds no targets, which may drop a binding as specified below.

A variable-qualified property selector is a structured pair `(VariableName, PropertyName)`, **not** a dotted string interpreted by a special parser. Resolve the variable relationship from the binding descriptor, then resolve the property from the variable's declared target type's effective property surface. This works even when the result collection is empty. Ordinary unqualified `PropertyName` continues to mean a property on the collection's actual element type.

## 5. Expression contracts

### 5.1 Bind

`Bind` is a concrete `QueryExpression` that consumes a non-binding holon collection and produces a BindingRecord collection.

Definition parameters:

| Parameter | Requirement |
|---|---|
| `BindingName` | Required, unique variable name. |
| `BindingElementType` | Derived from the incoming collection's declared `ElementType`; do not require authors to invent a concrete binding descriptor. |

For each incoming occurrence, construct a distinct transient BindingRecord whose named relationship targets that occurrence's holon reference. Preserve input order and multiplicity. Empty input produces an empty collection with a valid generated binding `ElementType`. Reject binding an input already declared as a BindingRecord collection; use `ExtendBindings` for extension.

### 5.2 ExtendBindings

`ExtendBindings` is a concrete `QueryExpression` that consumes a BindingRecord collection and produces a collection of extended BindingRecords.

Definition parameters:

| Parameter | Requirement |
|---|---|
| `SourceBindingName` | Required; must resolve to a declared variable in the input binding schema. |
| `ExpansionRelationshipName` | Required; resolve against the source variable's declared target type using existing declared-or-inverse channel resolution. |
| `TargetBindingName` | Required; must not already exist in the input schema. |
| `ExpansionPredicate` | Optional shared `QueryPredicate` evaluated against each candidate **target holon** using existing predicate semantics. |
| `MissingMatchPolicy` | `Drop` in this increment; optional/null-producing expansion is deferred. |

Derive the new variable's declared type from the resolved relationship target contract. Validate the full expansion and predicate contract before processing members, including when input is empty.

For each incoming BindingRecord occurrence, resolve the source variable, traverse the named relationship, apply the optional target predicate, and emit **one new BindingRecord per qualifying target occurrence**. Each emitted record retains all previous variable assignments and adds the new variable. If no targets qualify, emit no record for that input occurrence. Preserve input-binding order and each source traversal's target order; do not deduplicate. Propagate structural, descriptor, authorization, and retrieval errors rather than treating them as no-match.

A single invocation processes the whole input collection. Implementations should batch or cache repeated source relationship reads where execution context and freshness permit. Reusing Bob's `LIVES_IN` read must **not** collapse separate book–Bob bindings.

The existing flat `Expand` remains unchanged; it does not implicitly switch to `ExtendBindings` on seeing BindingRecords.

### 5.3 Project

Extend `Project` with an explicit binding-source form. `Project` consumes a BindingRecord collection and produces a collection of transient projection holons, one per incoming binding occurrence, in input order. Projection fields declare:

| Field | Requirement |
|---|---|
| `OutputName` | Unique property name on the projection result. |
| `SourceBindingName` | Required name of a variable declared by the input binding schema. |
| `PropertyName` | Required property on that variable's declared target type. |

For each field, resolve the variable relationship and property descriptor from declared types, verify value compatibility with the output projection descriptor, read the bound source via ordinary `HolonReference` operations, and populate the output holon's `PropertyMap`. The output collection declares exactly one projection `ElementType`, valid even when there are zero matches; its members remain accessed through `HolonReference`.

Preserve references throughout query evaluation. Binding construction, navigation, filtering, and ordering retain source references and use ordinary property reads when needed; they do not eagerly materialize source holons or copy their property maps. `Project` is an explicit value-materialization boundary, normally the final query step, rather than a reason to replace references with materialized holons at preceding stages.

The proposed `ReadableHolon::project_property_values` convenience method accepts selected property names using the same per-name ergonomics as `property_value` and returns a `PropertyMap` using those reads' existing semantics. Use it when selected values actually need materialization: at the final projection boundary, or in DAHN when populating a form containing most or all properties of a referenced holon. It is not a general query-evaluation primitive or an instruction to prefetch full property maps. Its implementation status must be verified before use.

A missing required source binding is an error. Handling optional source properties follows existing property/value requiredness and projection rules; do not invent nulls or silently omit required output properties. Projection does not deduplicate equal-valued outputs. Do not mutate input bindings or domain holons.

The binding-source form must be explicit. Preserve existing single-source `Project` behavior and avoid inferring the mode from runtime member types.

## 6. Existing operator interaction

**Default rule:** Existing collection operators operate on the **actual members** of their input `HolonCollection`. For a binding collection, those members are BindingRecord holons. No parallel collection of current-output domain references exists, and no implicit current-output variable is introduced.

| Operator | Binding collection behavior |
|---|---|
| `Filter` | An unqualified predicate evaluates properties on the BindingRecord descriptor itself. A variable-qualified predicate evaluates a declared property of the named bound holon. Retain or drop the entire binding occurrence. |
| `OrderBy` | An unqualified selector orders by a BindingRecord property; a variable-qualified selector orders by a property of a named bound holon. Preserve stable occurrence order for equal keys, subject to the existing ordering contract. |
| `Skip`, `Limit` | Skip or retain **binding occurrences**, not distinct bound domain holons. Preserve the binding collection's declared `ElementType`. |
| `Distinct` | Preserve existing identity-based distinctness unless an explicit assignment-value distinct mode is requested; do not silently equate two different BindingRecord holons. |
| `Expand` | Remains a flat expansion from its input element's declared relationship surface; it does not implicitly navigate from a named variable or preserve bindings. Use `ExtendBindings` for correlated navigation. |
| `Project` | Explicit binding-source mode resolves fields from named variables and emits projection holons. |

### 6.1 Variable-qualified selectors and predicates

Extend shared selector resolution with an **optional structured source-variable qualifier**. For a predicate comparison leaf, retain the existing `PropertyName`, `Operator`, and ordered `Operands` semantics, and add optional `SourceBindingName`. With no qualifier, resolve against the collection's declared `ElementType` exactly as today. With a qualifier, require a binding collection and resolve through its declared variable relationship to the target type's property descriptor.

The same qualifier concept applies to `OrderBy` selection and any future property-selector-consuming expression, using shared descriptor resolution rather than duplicating variable lookup logic. `Not`, `AllOf`, and `AnyOf` continue composing predicates without changing their Boolean semantics. Operators remain those afforded by the resolved property's ValueType; no binding-specific operator registry is introduced.

For `ExtendBindings.ExpansionPredicate`, the evaluation subject is the candidate target holon. In this increment its predicate remains **target-local**; comparisons involving other bound variables or two dynamically read property values are deferred to an explicit future cross-variable predicate contract. A downstream binding-aware `Filter` can already filter a property on any one named variable against authored literals.

### 6.2 Distinctness

Do **not** redefine existing `Distinct` globally. A separate, explicit `DistinctBindings` expression is recommended when assignment-value deduplication is needed. Its equality key is the ordered tuple of bound reference identities for all variables declared by the input binding schema; its output keeps the first matching occurrence and preserves the input `ElementType`. It must not compare transient BindingRecord identity when computing assignment equality. An eventual subset-of-variables key may be added explicitly, but is not part of this increment.

This separation makes duplicate match preservation testable and avoids accidentally changing existing reference-identity semantics.

## 7. End-to-end example

**Intent:** Find books and their authors' cities with population greater than one million, returning a projection per surviving book–author–city association.

```text
SeedBooks
  Next -> BindBooks
             BindingName: book
  Next -> ExtendAuthors
             SourceBindingName: book
             ExpansionRelationshipName: AUTHORED_BY
             TargetBindingName: author
             MissingMatchPolicy: Drop
  Next -> ExtendCities
             SourceBindingName: author
             ExpansionRelationshipName: LIVES_IN
             TargetBindingName: city
             ExpansionPredicate: Population GreaterThan 1000000
             MissingMatchPolicy: Drop
  Next -> ProjectBookAuthorCity
             SourceMode: Bindings
             Fields:
               BookTitle  <- (book, Title)
               AuthorName <- (author, Name)
               CityName   <- (city, Name)
```

Here `Next` means the sequential continuation from each expression to the following expression; the layout above is shorthand, not a new containment grammar.

Data:

```text
Book A -> Alice, Bob       Alice -> Paris, Lyon
Book B -> Bob              Bob   -> Rome
Paris.Population = 2,000,000
Lyon.Population  =   500,000
Rome.Population  = 2,800,000
```

Intermediate assignments:

```text
{book: A, author: Alice, city: Paris}
{book: A, author: Bob,   city: Rome}
{book: B, author: Bob,   city: Rome}
```

Expected projected rows (each row is a **separate projection holon reference**):

| BookTitle | AuthorName | CityName |
|---|---|---|
| Book A | Alice | Paris |
| Book A | Bob | Rome |
| Book B | Bob | Rome |

Bob and Rome may be read once per suitable cache scope but must still participate in two separate bindings. No implicit `Distinct` occurs.

## 8. Validation, lifecycle, and execution constraints

1. **Validate before publication:** Validate expression parameters, variable names, stage schemas, selected relationship/property contracts, predicate operators and operands, and output descriptor compatibility even for empty input collections.
2. **Conformance:** Validate that each BindingRecord conforms to the input collection's single declared binding `ElementType`; validate each variable relationship and its bound target.
3. **Errors versus no match:** A valid traversal with no qualifying targets drops the binding under `MissingMatchPolicy: Drop`. Invalid selectors, missing required bindings, unauthorized reads, incompatible types, and retrieval errors fail the expression.
4. **Occurrence and order:** Preserve multiplicity and defined iteration order through `Bind`, `ExtendBindings`, `Filter`, and `Project`; only explicit ordering/deduplication/limit expressions alter those properties.
5. **Execution isolation:** Do not write resolved variable values or generated binding instances onto reusable `QueryExpression` definitions. Binding instances belong to invocation execution state and are transient.
6. **Lifetime:** Keep transient BindingRecords, projection holons, collections, and required descriptors readable through the lifetime of any returned reference. Release them only when no live execution/result references require them.
7. **Security:** All bound-variable reads and traversals go through the ordinary reference layer and its authorization/trust boundaries; binding holons do not bypass checks or grant new access.
8. **Physical optimizations:** Permit batching, shared reference reads, and internal compact representations only when every exposed expression result remains a valid holon-reference collection with identical observable assignments and occurrence semantics.
9. **No persistence side effects:** Constructing, pruning, or projecting transient results must not commit or mutate domain holons or DHT state.

## 9. Proposed implementation sequence and acceptance tests

**Phase 1 — Descriptor-backed binding infrastructure.** Add abstract `BindingRecord`, query-local stage schema/descriptor construction and retention, and shared variable relationship resolution. Test empty-input descriptor validation, inherited variable declarations, duplicate names, missing/multiple bindings, and descriptor lifetime.

**Phase 2 — `Bind` and `ExtendBindings`.** Implement both as concrete QueryExpression types through the existing execution lifecycle. Test occurrence multiplicity, ordering, missing matches, descriptor errors, repeated source read reuse, and unchanged flat `Expand` behavior.

**Phase 3 — Variable-qualified selectors.** Add optional structured source-variable qualification to shared comparison predicates and `OrderBy`. Test qualifier validation against declared target types even on empty collections; confirm that unqualified behavior and operator affordance resolution remain unchanged.

**Phase 4 — Multi-source `Project`.** Implement binding-source projection and its output descriptor contract. Verify one output holon per binding occurrence, shared source reads, required/optional property handling, and correct output `ElementType`.

**Phase 5 — Explicit assignment distinctness.** Implement `DistinctBindings` without changing existing `Distinct` semantics. Verify two different BindingRecords with identical assignments collapse only under this explicit operator.

**Required integration tests:**

- Book–author–city example yields exactly the three expected projections.
- Two distinct book–Bob–Rome matches survive even when Bob's city relationship is fetched once.
- An author with only nonqualifying cities produces no binding; a book with no surviving authors produces no projection.
- Empty collections still have valid binding/projection descriptors and reject invalid selectors.
- `Limit 1` on a binding collection retains one **assignment occurrence**, not all records sharing its city.
- A variable-qualified filter can select `author.Name` while the binding record also contains `book` and `city`.
- Existing ordinary `SeedHolons → Expand → Filter → OrderBy → Limit` results are unchanged.
- Direct Query execution and `QueryDance` produce equivalent results for the same definition and invocation context.

## 10. Explicitly deferred extensions

Do not include the following in the first correlated-query increment: optional/null bindings; scalar, list, or map-valued binding variables; rebinding or shadowing variable names; cross-variable value comparisons and equality joins; independent-branch joins; aggregation/grouping; variable scope removal or aliases; factorized execution; persistence of binding artifacts; a Cypher parser or planner; generalized `QueryResult` carriers; or a parallel execution-owned `Bindings` collection. These may be added without changing the core collection-of-holon-references invariant.

## Appendix A — Rationale and alternatives considered

### A.1 Why explicit BindingRecords

A binding is a first-class, inspectable holon whose variable relationships use MAP's existing descriptor and reference facilities. It preserves complete associations across navigation steps, supports duplicate occurrences, and lets multi-source projection resolve sources by name. It extends the existing query expression vocabulary rather than replacing its execution boundary.

### A.2 Nested result graphs

Nested wrappers naturally represent grouped navigation and can avoid some eager combination enumeration. However, their semantics depend on traversal scopes, wrapper construction, upward pruning, and emission locations. Independent branches, joins, and arbitrary graph patterns require additional combination rules. Retain nested/factorized structures as potential future physical optimizations or grouped-output forms, not the initial logical correlation contract.

### A.3 Separate `Result` plus `Bindings` overlay

A parallel execution-owned binding collection risks mismatched cardinality, ambiguous occurrence correspondence, and unclear `Limit`/`Distinct` semantics. Keeping the binding records **inside the one authoritative result collection** removes synchronization ambiguity.

### A.4 Generalized QueryResult or row-stream execution

A generalized carrier could eventually represent scalar rows and aggregates directly, but it changes the fundamental execution boundary and duplicates the holonic collection/reference abstractions. It is unnecessary for reference-valued correlated composition and conflicts with the chosen invariant that every intermediate result is a collection of holon references.

### A.5 Eager versus compact binding materialization

One transient holon per assignment is the clearest initial implementation, but may become costly for high-cardinality queries. Do not treat eager per-match construction as an irreversible physical requirement. Future executors may batch, share, or factorize internal state, provided expression-boundary results satisfy the same holonic contract.

## Appendix B — Design sources and implementation verification

This proposal is based on:

- `correlated-query-composition.md` — the exploratory comparison and book–author–city example.
- `query-engine-design-spec.md` — normative query execution, descriptor resolution, collection occurrence, predicate, and operator contracts.
- `query-arch.md` — concrete QueryCore, direct Query, and QueryDance execution architecture.

**Verification caveat:** These files describe target architecture and proposal semantics; they are not proof that every proposed API or schema capability exists in the current repository. Before implementation, inspect the current query schema, descriptor subsystem, transient holon/reference lifecycle, and operator implementations. Preserve existing implemented contracts and document any prerequisite facilities that are missing.
