# MAP Navigation Runtime Binding Model (v1.2)

## Purpose

This document is the canonical runtime/binding model spec for MAP navigation/query support.

It defines why `HolonCollection` is the primary runtime carrier, how an `ExecutionPlan` holon names runtime values when plan capture or replay is needed, how `NavigationExecutionBindings` stores those plan-scoped values during execution, and how richer correlation or projection views are derived without becoming foundational runtime types.

---

## 1. Design Position

MAP navigation/query support keeps runtime value shapes conservative and puts concrete behavior in descriptor-afforded navigation operation Dances.
The `ExecutionPlan` HolonType adds replay and analysis structure when that structure is needed.

The core position is:

- `HolonCollection` is the primary runtime carrier for holon-oriented query execution.
- concrete navigation operations are Dances, not special query-engine methods.
- Variables are symbolic plan-level bindings, not fields embedded in runtime collections.
- `NavigationExecutionBindings` is the plan-scoped binding set that maps plan variables to runtime values.
- Relationship traversal is named-channel traversal.
- `RelationshipMap` and `RelationshipCache` provide graph-shaped correlation structures.
- Row-oriented, path-oriented, pair, partitioned, scalar, and graph-like views are derived only when query semantics or output contracts require them.

The default execution shape is:

    HolonCollection -> Operation -> HolonCollection

The default runtime substrate is not:

    RowSet -> Operation -> RowSet

---

## 2. ExecutionPlan Bindings

`ExecutionPlan` is a MAP `HolonType`.
An `ExecutionPlan` holon has serializable symbolic content describing algebraic operations.

It is not required for every direct navigation operation Dance.
It becomes relevant when MAP needs to capture, replay, inspect, optimize, or compile a workflow.

Each operation declares:

- input variable names
- output variable names
- operation-specific parameters

Example:

    SeedHolons {
      output: "people",
      holon_type: Person
    }

    Expand {
      input: "people",
      relationship: KNOWS,
      output: "friends"
    }

    Filter {
      input: "friends",
      predicate: age > 30,
      output: "adult_friends"
    }

The plan does not contain runtime collections.
It defines the symbolic dataflow and derivation structure that runtime execution follows.

Variables are symbolic names for operation input and output slots.
They support:

- serializable plans
- replayable plans
- interactive construction
- variable renaming
- operation fusion
- plan analysis
- query optimization
- future OpenCypher/GQL compilation

---

## 3. NavigationExecutionBindings

`NavigationExecutionBindings` holds the plan-scoped values produced while executing or replaying a navigation `ExecutionPlan` holon.
It is deliberately narrower than MAP's general runtime context vocabulary.

Conceptually:

    NavigationExecutionBindings {
      execution_scope: ExecutionScope,
      bindings: Map<VariableName, NavigationExecutionValue>
    }

    NavigationExecutionValue {
      Holons(HolonCollection)
      Derived(DerivedView)
    }

`execution_scope` identifies the transaction, snapshot, space, or other host-defined context needed to make runtime values and derived views meaningful.

`Holons(HolonCollection)` is the default runtime value for the core algebra.

`Derived(DerivedView)` is non-foundational. It is introduced only when required by:

- projection
- aggregation
- correlation-sensitive gestures
- OpenCypher/GQL-compatible output semantics
- tabular or object-shaped API output
- visualization, provenance, or explanation

---

## 4. HolonCollection

The existing MAP runtime already defines `HolonCollection`:

    pub struct HolonCollection {
        state: CollectionState,
        members: Vec<HolonReference>,
        keyed_index: BTreeMap<MapString, usize>,
    }

This type provides the essential runtime shape for holon-oriented query execution:

- collection state
- ordered membership
- holon references
- keyed lookup
- navigable references to full holons

`HolonCollection` should therefore be treated as the primary runtime result type for initial query algebra operations.

A separate foundational plural carrier such as `BoundHolonCollection` or `BoundHolonSet` should not be introduced unless a real lifecycle, contract, or semantic distinction emerges that `HolonCollection` cannot represent.

---

## 5. Variables Are Not Runtime Fields

Variables belong to the `ExecutionPlan` holon.
They should not be embedded in `HolonCollection`.

Example:

    ExecutionPlan holon declares:
      "friends" is the output of Expand

    NavigationExecutionBindings records:
      "friends" -> HolonCollection

This is the binding model:

- the plan names the value
- the context stores the value
- the collection remains an ordinary MAP runtime collection

The same `HolonCollection` value can be named differently by different plans, by different optimization stages, or by different replay contexts.

---

## 6. Operation Closure

Core holon-oriented navigation operation Dances should stay closed over `HolonCollection` wherever possible.

Examples:

- `SeedHolons`
- `Expand`
- `Filter`
- `OrderBy`
- `Skip`
- `Limit`
- `Distinct`

These operations should generally follow:

    HolonCollection -> HolonCollection

Operations that need non-collection output should produce derived views:

    Project:   HolonCollection -> DerivedView
    Count:     HolonCollection -> DerivedView
    Aggregate: HolonCollection -> DerivedView
    Explain:   ExecutionPlan holon -> DerivedView

This keeps the core execution pipeline holon-centered while preserving room for richer query surfaces.

---

## 7. Relationship Channels

MAP relationships are named traversal channels.
They are not foundational property-bearing edge instances.

An expansion is conceptually:

    Expand(source_collection, relationship_name) -> target_collection

The relationship name is an operation parameter.
It is not a separate runtime carrier flowing through the algebra.

At runtime:

    NavigationExecutionBindings["people"] -> HolonCollection
    Execute Expand(KNOWS)
    NavigationExecutionBindings["friends"] -> HolonCollection

Relationship-channel legality is validated through descriptor-backed effective structure.

---

## 8. Correlation Recovery

A flat expansion may produce:

    Expand(books, Authors) -> authors

where `authors` is a flat `HolonCollection`.
For many interactive gestures, that flat view is sufficient.

Some semantics require preserving or recovering correlation, such as:

- returning `(book, author)` pairs
- grouping authors by book
- filtering on both source and target variables
- preserving duplicate path semantics
- compiling richer OpenCypher/GQL patterns faithfully

The core response should not be to make `RowSet` foundational.

MAP can recover or derive correlation from:

- `ExecutionPlan` holon topology
- operation identities
- input and output variables
- relationship-channel names
- `RelationshipMap`
- `RelationshipCache`
- traversal provenance
- transaction or snapshot state

The derived view must carry or reference the execution scope needed to make that correlation deterministic.

---

## 9. RelationshipMap And RelationshipCache

The existing MAP relationship structures already resemble a graph-shaped correlation layer.

A `RelationshipMap` maps a relationship name to a target collection:

    pub struct RelationshipMap {
        map: HashMap<RelationshipName, Arc<RwLock<HolonCollection>>>,
    }

A `RelationshipCache` indexes relationship maps by source holon:

    pub struct RelationshipCache {
        cache: Arc<RwLock<HashMap<HolonId, RelationshipMap>>>,
    }

Conceptually:

    source_holon
      -> relationship_name
        -> target_collection

This can support multiple derived views:

Flat collection:

    [AuthorA, AuthorB, AuthorC]

Partitioned collection:

    Book1 -> [AuthorA, AuthorB]
    Book2 -> [AuthorC]

Pair view:

    (Book1, AuthorA)
    (Book1, AuthorB)
    (Book2, AuthorC)

Row-oriented projection:

    { book: Book1, author: AuthorA }
    { book: Book1, author: AuthorB }
    { book: Book2, author: AuthorC }

All of these are views over relationship-derived correlation.
None of them needs to become the default runtime carrier.

---

## 10. Derived Views

A `DerivedView` is any non-foundational runtime result created from a `HolonCollection`, `ExecutionPlan` holon, relationship structure, or another derived view.

Initial categories include:

- scalar values
- scalar collections
- property projections
- partitioned collections
- pair projections
- traversal traces
- path collections
- row-oriented projections
- explanation or provenance views

Derived views are introduced only when required by:

- output contracts
- project operations
- aggregation
- correlation-sensitive gestures
- OpenCypher/GQL-compatible result semantics
- visualization or explanation

Derived views should not be used to force the entire algebra into a row-, path-, or graph-value-shaped runtime substrate.

---

## 11. RowSet Status

`Row` and `RowSet` remain useful semantic concepts for tabular and declarative-query-compatible output.

They are not foundational runtime carriers for the initial MAP QueryAlgebra.

A row-oriented projection may be materialized when needed for:

- tabular output
- multi-variable projection
- Cypher-compatible `RETURN` semantics
- aggregation over correlated variables
- interoperability with row-oriented APIs

The default core execution model remains:

    HolonCollection -> Operation -> HolonCollection

not:

    RowSet -> Operation -> RowSet

---

## 12. Path Status

Paths are derived traversal traces.
They are not primitive runtime carriers in the initial algebra.

A path-like derived view may be materialized when needed for:

- OpenCypher path variables
- visual explanation
- provenance
- replay analysis
- graph traversal display
- query result export

Conceptually, a path is an ordered trace:

    holon -> relationship_name -> holon -> relationship_name -> holon

This trace can be reconstructed or materialized from the `ExecutionPlan` holon, relationship channels, operation identities, and transaction/snapshot state when query semantics require it.

---

## 13. Relationship Variables

In OpenCypher, a relationship variable may denote a materialized edge instance.
MAP does not model relationships as general property-bearing edge instances in the initial algebra.

Therefore, relationship variables should not be treated as foundational runtime carriers.

If needed for compatibility, provenance, or explanation, a relationship variable can be interpreted as a symbolic traversal handle containing:

- source binding
- relationship name
- target binding
- traversal operation identity

This supports Cypher-like authoring and result surfaces without forcing MAP Core into a property-graph edge-instance model.

---

## 14. Relationship-Specific State

When relationship-specific state is needed, MAP should model that state using an intersection `HolonType`.

Example:

    Person - HAS_MEMBERSHIP -> Membership
    Membership - MEMBER_OF -> Organization

The `Membership` holon can carry properties such as:

- role
- since
- status
- permissions
- provenance
- lifecycle state

This preserves the MAP principle that state-bearing semantic things are holons.

One internal exception exists for manually ordered collections: sequence information may be stored internally on the relationship.
This is collection-organization metadata, not schema-level relationship state.

---

## 15. OpenCypher And GQL Compatibility

OpenCypher and later GQL are declarative authoring, interchange, and compatibility surfaces.
They do not define MAP's foundational runtime carrier.

The future declarative route is:

    OpenCypher/GQL
      -> DeclarativeQuery holon or equivalent document
      -> logical query representation
      -> descriptor-aware MAP planning
      -> ExecutionPlan holon
      -> HolonCollection-centered execution plus derived views where required

The direct navigation route is:

    HumanAgent or DAHN gesture
      -> navigation operation Dance
      -> HolonCollection-centered execution

The interactive plan-building route is:

    HumanAgent gestures
      -> InteractiveNavigationSession.ApplyOperation
      -> deterministic algebra operation sequence
      -> ExecutionPlan holon
      -> HolonCollection-centered execution

Direct navigation does not need to converge on an `ExecutionPlan` holon.
Interactive plan-building, saved-plan replay, and declarative compilation converge on `ExecutionPlan` holons.

Declarative query surfaces may require observable row semantics, path semantics, null extension, grouping, or duplicate preservation.
MAP should satisfy those semantics by deriving the required view rather than adopting those views as the foundational runtime substrate.

---

## Summary

MAP query support is a capability area, not a required runtime object.

At the direct navigation layer, operation Dances consume and produce MAP runtime values, primarily `HolonCollection`s.
At the plan layer, an `ExecutionPlan` holon names intermediate results using variables, and runtime execution maps those variables to `HolonCollection`s and derived values.

The core algebra remains holon-centered for as many operations as possible, while derived views provide the path to richer projections, correlation-sensitive results, and future OpenCypher/GQL compatibility.
