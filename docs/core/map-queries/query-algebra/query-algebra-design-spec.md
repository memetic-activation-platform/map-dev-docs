# MAP Query Algebra Design Spec

## Purpose

This document is the canonical design spec for MAP-native query algebra.

It consolidates the core runtime model, execution model, binding model, navigation operation set, execution-time structural validation, materialized projection model, and distributed execution semantics for query algebra in MAP.

This spec defines the MAP-owned execution model for graph-native read and navigation.
Declarative query languages such as OpenCypher and GQL are separate authoring and compatibility surfaces and are not the subject of this document.

---

## 1. Core Position

MAP query algebra keeps runtime value shapes conservative and treats concrete navigation behavior as Dances afforded by MAP types.

The key design position is:

- `HolonCollection` is the primary runtime carrier for holon-oriented query execution.
- Navigation operations are Dances, not special query-engine methods.
- `ExecutionPlan` is a first-class MAP artifact that captures symbolic execution structure.
- `ExecutionInstance` is the runtime execution state for a specific execution of an `ExecutionPlan`.
- Variables are symbolic plan-level bindings, not fields embedded in runtime collections.
- Relationship traversal provenance belongs to `ExecutionStep`, not to runtime result objects.
- Relationships are named traversal channels, not foundational property-bearing edge instances.
- Descriptors are the semantic source of structure, relationship meaning, and value/operator meaning.
- `Project` is the explicit materialization boundary of the navigation algebra.
- `Projection` is the primary materialized holon-shaped result.
- Non-collection outputs use concrete result types rather than a generic derived-view abstraction.

The default execution shape is:

    HolonCollection -> Operation -> HolonCollection

The default runtime substrate is not:

    RowSet -> Operation -> RowSet

---

## 2. Scope And Boundaries

This design spec covers:

- direct MAP-native navigation operations
- interactive navigation built from HumanAgent gestures
- replayable saved execution plans
- descriptor-backed structural and value validation
- distributed execution across sovereign MAP spaces

This design spec does not define:

- declarative query syntax
- planner-specific logical operators such as `Apply`, `Optional`, or `Join`
- mutation semantics for declarative query languages
- a generalized row-stream execution engine
- foundational graph-valued runtime carriers
- a generic derived-view runtime abstraction

Declarative query support must compile into this algebra rather than replace it.

---

## 3. Runtime Model

### 3.1 `HolonCollection`

`HolonCollection` is the primary runtime result for holon-oriented query execution.

It provides:

- collection state
- ordered `HolonReference` members
- keyed lookup
- navigable references to full holons

A `HolonCollection` contains only holon references and collection semantics.

It does not contain:

- variable bindings
- relationship provenance
- execution provenance
- query-plan metadata

MAP should not introduce separate foundational carriers such as:

- `BoundHolonCollection`
- `Expansion`
- `GraphValue`
- `RelationshipMap`
- `RowSet`

unless a real lifecycle or semantic distinction emerges that `HolonCollection` cannot represent.

### 3.2 `HolonReference` And `ReadableHolon`

`HolonReference` exposes the `ReadableHolon` interface directly.

Call sites do not need to explicitly perform resolution in order to read holon properties, relationships, or descriptor information.

This preserves a clean caller-facing read surface while retaining deferred materialization.

The distinction is:

- `HolonReference` preserves identity and defers state access.
- `HolonCollection` groups references without projecting them.
- `Projection` materializes selected state.

### 3.3 Variables

Variables belong to the `ExecutionPlan`.
They do not belong inside runtime collections.

Conceptually:

    Expand {
      input: "books",
      relationship: Authors,
      direction: Outgoing,
      output: "authors"
    }

### 3.4 `ExecutionPlan`

`ExecutionPlan` is a first-class MAP artifact.

It represents symbolic execution structure rather than runtime state.

An `ExecutionPlan` owns:

- execution topology
- operation dependencies
- input and output binding names
- operation-specific parameters
- relationship provenance
- traversal provenance
- derivation structure
- explanation structure

An `ExecutionPlan` is graph-shaped.

The initial implementation may be tree-shaped, but the model must support graph-shaped plans when branching, reuse, correlation, or optimization require it.

A linear chain is a special case.

Conceptually:

    SeedBooks
        ├── Expand(Authors, Outgoing)
        └── Expand(Publisher, Outgoing)

`ExecutionStep` is the semantic owner of:

- variable names
- relationship names
- symbolic producer/consumer relationships
- operation identity

`ExecutionPlan` remains reusable, saveable, replayable, inspectable, explainable, and shareable.

It must not own execution-specific runtime values.

### 3.5 `ExecutionInstance`

`ExecutionInstance` represents one execution of an `ExecutionPlan`.

It owns runtime execution state, including:

- plan reference
- execution scope
- current bindings
- diagnostics
- execution status
- transient runtime results

Conceptually:

    ExecutionInstance {
      plan_ref: ExecutionPlan,
      bindings: Map<VariableName, ExecutionValue>
    }

An `ExecutionPlan` may have zero or more associated execution instances.

This separation allows the same plan to be:

- replayed
- shared
- executed concurrently
- executed in different execution scopes

without contaminating the plan with runtime state.

### 3.6 Execution Values

Execution values are runtime values bound within an `ExecutionInstance`.

Conceptually:

    ExecutionValue {
      Holons(HolonCollection)
      Projection(Projection)
      Projections(ProjectionCollection)
      Scalar(ScalarValue)
      Scalars(ScalarCollection)
    }

`Holons(HolonCollection)` is the default runtime value.

Other variants are introduced only when an operation intentionally leaves the holon-navigation substrate.

### 3.7 Hybrid Execution Model

MAP query algebra uses a hybrid execution model:

- `ExecutionPlan` carries symbolic execution structure
- `ExecutionInstance` carries runtime execution state

This separation supports:

- replay
- optimization
- explanation
- provenance reconstruction
- concurrent execution
- graph-shaped dependency analysis

without embedding execution state into the plan.

---

## 4. Runtime Layers

No substantive changes.

---

## 5. Descriptor-Owned Semantics

No substantive changes.

---

## 6. Execution-Time Structural Resolution

No substantive changes.

---

## 7. Relationship Model And Correlation

MAP relationships are named traversal channels.

They are not foundational property-bearing edge instances.

Conceptually:

    Expand(source_collection, relationship_name, traversal_direction)
      -> target_collection

The relationship name and traversal direction are operation parameters carried by the corresponding `Expand` step.

They are not runtime values flowing through the algebra.

Each semantic MAP relationship has:

- a declared relationship name
- an inverse relationship name
- a declared source endpoint type
- a declared target endpoint type

These names and endpoint roles describe one semantic relationship pair.
They do not describe separate foundational edge kinds.

For a semantic relationship:

    (A)-[R]->(B)

with inverse name `Rinv`, the same underlying relationship may be expressed in four equivalent surface forms:

    (A)-[R]->(B)
    (A)<-[Rinv]-(B)
    (B)-[Rinv]->(A)
    (B)<-[R]-(A)

All four surface forms normalize to the same semantic relationship pair.
What changes is:

- which endpoint is the current source of the traversal
- which surface relationship name is used
- whether the surface syntax is written in the declared or inverse direction

`Expand` validation must therefore normalize the requested surface form onto the underlying semantic relationship pair before execution.
Validation must not be reduced to a naive check that the requested relationship name is directly declared on the source type.

Concretely, `Expand` validation must determine:

- which semantic relationship pair the requested name refers to
- whether the current source holon type is a legal endpoint for the requested traversal
- whether the requested surface direction is compatible with the declared/inverse relationship semantics

If no legal normalization exists for the requested relationship name, source type, and traversal direction, `Expand` is invalid.

The default runtime result of expansion is:

    HolonCollection

not:

    RelationshipMap
    Expansion
    GraphValue

Relationship-specific provenance belongs to the `Expand` operation recorded in the `ExecutionPlan`.

Correlation-sensitive structures may be produced when required by semantics, explanation, visualization, compatibility surfaces, or output contracts.

Such structures should be concrete result types rather than foundational algebraic carriers.

If relationship-specific state is needed, MAP should model that state using holons, typically through an intersection `HolonType`.

One internal exception exists for manually ordered collections: sequence information may be stored internally on the relationship.

This is collection-organization metadata rather than schema-level relationship state.

`ExpandAll` is planning sugar rather than a distinct runtime result shape.

Conceptually:

    ExpandAll
      ├── Expand(RelA)
      ├── Expand(RelB)
      └── Expand(RelC)

Each child `ExpandStep` produces a `HolonCollection`.

Graph-shaped expansion views may be reconstructed from:

- the `ExecutionPlan`
- the execution topology
- operation identities
- execution bindings

when required for explanation or visualization.

---

## 8. Projection And Materialized Results

### 8.1 Projection Boundary

`Project` is the explicit materialization boundary of the navigation algebra.

Before projection, navigation should generally preserve deferred access through:

- `HolonReference`
- `HolonCollection`
- `ExecutionPlan`
- `ExecutionInstance`

### 8.2 `Projection`

A `Projection` is:

- the result of a `Project` operation
- a materialized, self-describing holon-shaped value
- described by a derived `HolonType`
- ephemeral by default
- state-bearing directly within the projection
- not resolved through `TransientReference`
- not managed through `TransientHolonManager`

A `Projection` may implement `ReadableHolon`, but it remains distinct from the reference layer.

The distinction is:

- references preserve identity and defer materialization
- projections contain materialized selected state

### 8.3 Projection Type

A projection type may be anonymous and inline, or may be represented by a reusable content-addressed descriptor.

Projection types are assembled from existing schema elements such as:

- `PropertyType`
- `ValueType`
- `RelationshipType`

A projection type may be ephemeral, but it is not semantically ad hoc.

### 8.4 Projection Collections

When projection is applied to a collection, the result may be a `ProjectionCollection`.

A `ProjectionCollection` is a collection of projection values.

It is distinct from `HolonCollection`, whose members are references.

### 8.5 Scalars And Scalar Collections

Scalar extraction and aggregation use concrete scalar result types such as:

- `ScalarValue`
- `ScalarCollection`

These are not foundational graph-navigation carriers.

### 8.6 Paths And Explanation Views

Paths are materialized traversal traces rather than primitive runtime carriers.

Conceptually:

    holon -> relationship_name, direction -> holon -> relationship_name, direction -> holon

Path-like views may be materialized for:

- explanation
- provenance
- replay analysis
- visualization
- export
- compatibility surfaces

These should be modeled as concrete result types when needed.

---

## 9. Initial Navigation Operation Set

The initial MAP query algebra is intentionally small.

It supports HumanAgent and DAHN navigation while deferring declarative-planner-only constructs to the declarative query layer.

### 9.1 `SeedHolons`

Produces a `HolonCollection`.

### 9.2 `Expand`

Consumes a `HolonCollection`, follows a named relationship channel in a requested traversal direction, and produces a target `HolonCollection`.

The relationship name remains part of execution provenance rather than runtime result structure.

`Expand` is validated against descriptor-backed effective relationship structure.

It must support traversal through either the declared relationship name or the inverse relationship name when the requested surface form legally normalizes to the same semantic relationship pair.

If the requested traversal is legal for the source holon type and there are no matching runtime targets, `Expand` returns an empty `HolonCollection`.

If the requested traversal is not legal for the source holon type under declared/inverse normalization semantics, `Expand` returns a validation error rather than an empty `HolonCollection`.

### 9.3 `Filter`

Consumes a `HolonCollection` and produces a filtered `HolonCollection`.

### 9.4 `OrderBy`

Consumes a `HolonCollection` and produces an ordered `HolonCollection`.

### 9.5 `Skip`

Consumes a `HolonCollection` and produces a `HolonCollection`.

### 9.6 `Limit`

Consumes a `HolonCollection` and produces a `HolonCollection`.

### 9.7 `Distinct`

Consumes a `HolonCollection` and produces a `HolonCollection`.

### 9.8 `Project`

`Project` is the explicit materialization boundary.

It may produce:

- `Projection`
- `ProjectionCollection`
- `ScalarValue`
- `ScalarCollection`
- path traces
- explanation views
- compatibility-oriented result surfaces

without changing the foundational navigation substrate.

---

## 10. Initial Expression And Predicate Model

Unchanged.

---

## 11. Distributed Query Algebra Semantics

No substantive changes except:

- distributed execution operates through `ExecutionInstance`
- distributed execution must not force row-oriented or graph-valued foundational carriers

Authorized boundary exchange may include:

- references
- projections
- path views
- scalar results
- other concrete result types required by contract

---

## 12. Correlation In Distributed Execution

Correlation may be derived from:

- execution topology
- operation identities
- delegated expansion provenance
- relationship-channel names
- execution scope

Distributed correlation must not force:

- `RowSet`
- `RelationshipMap`
- `Expansion`
- `GraphValue`

to become foundational runtime carriers.

---

## 13. Layering And Adoption Path

Unchanged.

---

## 14. Responsibility Split

The core responsibility split is:

- `ExecutionPlan` owns symbolic execution structure, dependencies, relationship provenance, and explanation topology.
- `ExecutionInstance` owns runtime execution state and bindings.
- `HolonReference` owns deferred holon identity and exposes `ReadableHolon`.
- `HolonCollection` remains the primary runtime carrier for navigation results.
- `Projection` is the primary materialized holon-shaped result.
- Concrete scalar, path, explanation, or compatibility result types are introduced only when required.
- Relationship provenance belongs to `ExecutionStep`, not to runtime result objects.

This split is normative for MAP query algebra.

---

## 15. Out Of Scope

The following concerns are intentionally outside this design spec:

- declarative query syntax and planning vocabulary
- planner-only operators
- mutation operators
- foundational expansion graph carriers
- foundational graph-valued runtime results
- embedding execution state into `ExecutionPlan`
- embedding execution provenance into runtime collections
- generic derived-view abstractions

---

## Summary

MAP query algebra is a holon-centered, descriptor-governed, sovereignty-preserving execution model for graph-native navigation.

Its core commitments are:

- `HolonCollection` as the primary runtime carrier
- `ExecutionPlan` as a graph-shaped symbolic execution artifact
- `ExecutionInstance` as runtime execution state
- relationship provenance owned by execution steps
- named relationship-channel traversal
- `Project` as the explicit materialization boundary
- `Projection` as the primary materialized holon-shaped result
- concrete non-collection result types instead of generic derived-view abstractions
- descriptor-owned structure and value semantics
- delegated distributed expansion across sovereign spaces

Declarative query support must target this model rather than replace it.
