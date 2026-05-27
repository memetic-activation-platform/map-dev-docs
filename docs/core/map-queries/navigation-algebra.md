# MAP Navigation Algebra - Initial Navigation Operation Dance Spec (v2.2)

## Purpose

This document defines the first concrete MAP navigation operation contract for HumanAgent and DAHN navigation.

The initial target is:

- implement concrete navigation operations as descriptor-afforded Dances
- carry runtime results primarily as `HolonCollection`s
- allow those same operations to be captured into an `ExecutionPlan` holon later
- preserve enough operation structure and traversal context to derive richer views when needed
- keep Commands, SDK, hApps, and external dances outside navigation/query semantic ownership

This is the concrete initial operation spec for the navigation layers described in `query-arch.md`.
It is not an OpenCypher planner spec and not a catalog of all future query operators.

---

## 1. Core Model

The initial navigation algebra is built from four pieces:

- Navigation operation Dances
  - executable descriptor-afforded behaviors such as `Expand` and `Filter`
  - can run without a saved plan or reified query object

- `ExecutionPlan` HolonType
  - MAP HolonType for optional static, serializable symbolic operation structure
  - owns variables, dependencies, operation parameters, derivation, and replay structure

- `NavigationExecutionBindings`
  - transaction-, snapshot-, or session-scoped plan binding set
  - maps plan variables to runtime values

- `HolonCollection`
  - primary runtime carrier for holon-oriented execution
  - reused from the existing MAP runtime

The default execution shape is:

    HolonCollection -> Operation -> HolonCollection

Derived views are introduced only when an operation or output contract requires them.

`Query` is not required as a reified runtime object for this initial model.

---

## 2. ExecutionPlan

`ExecutionPlan` is a MAP `HolonType`.
An `ExecutionPlan` holon has ordered, append-friendly symbolic content: operations with named inputs and outputs.

It is the replay and analysis layer, not the first thing required to execute a navigation operation Dance.

Initial shape:

    ExecutionPlan holon {
      operations: Vec<PlanOperation>
    }

    PlanOperation {
      id: OperationId,
      inputs: Vec<VariableName>,
      outputs: Vec<VariableName>,
      kind: PlanOperationKind
    }

The operation list in the plan holon supports the interactive route because gestures are append-oriented.
Because every operation declares named inputs and outputs, the same representation can later be interpreted as a dependency graph when branching, reuse, optimization, or derived correlation views require it.

The plan holon does not contain runtime collections.
It contains symbolic variables, operation parameters, and enough derivation structure to replay or analyze how runtime values were produced.

---

## 3. NavigationExecutionBindings

`NavigationExecutionBindings` is the narrow binding set for a navigation `ExecutionPlan` holon.
It is used while capturing, replaying, or interactively executing that plan.
It maps plan variables to values produced by plan operations.

For direct navigation operation Dance execution, the host may supply an equivalent operation-local binding set.
`NavigationExecutionBindings` becomes authoritative when operations are being captured or replayed through `InteractiveNavigationSession` or an `ExecutionPlan` holon.

Initial shape:

    NavigationExecutionBindings {
      transaction_or_snapshot: ExecutionScope,
      bindings: Map<VariableName, NavigationExecutionValue>
    }

    NavigationExecutionValue {
      Holons(HolonCollection)
      Derived(DerivedView)
    }

`Holons(HolonCollection)` is the default and primary runtime value.
`Derived(DerivedView)` is non-foundational and appears only when a projection, correlation-sensitive gesture, compatibility surface, or output contract requires it.

Examples of derived views include:

- scalar values
- scalar collections
- partitioned collections
- source-target pair views
- traversal traces
- path collections
- row-oriented projections

The binding set is scoped to the transaction or snapshot used for execution.
Derived views that depend on recomputation must preserve or reference that scope.

---

## 4. Variables

Variables are symbolic names in the `ExecutionPlan` holon.
They are not embedded in `HolonCollection`.

Example:

    Expand {
      input: "books",
      relationship: Authors,
      output: "authors"
    }

At runtime:

    NavigationExecutionBindings["books"] -> HolonCollection
    NavigationExecutionBindings["authors"] -> HolonCollection

This separation supports:

- interactive construction
- replay
- variable renaming
- plan analysis
- operation fusion
- future optimization
- later OpenCypher/GQL compilation

---

## 5. Runtime Layers

Navigation execution distinguishes three layers.

### 5.1 Ontology Layer

Persistent holonic schema and data.

Includes:

- type descriptors
- property descriptors
- relationship descriptors
- `Extends`
- instance properties
- instance relationships

Schema meaning remains ontology-as-data.
Rust enums or query-local rule systems should not duplicate ontology concepts.

### 5.2 Runtime Structural Layer

Ephemeral host-side structural support for validation and lookup.

Examples:

- descriptor-backed effective property lookup
- descriptor-backed effective relationship lookup
- internal caches such as `ResolvedType`

This layer is an execution aid.
It is not the caller-facing semantic facade.

### 5.3 Instance State Layer

Transaction-scoped mutable holon state.

Includes:

- staged holons
- transient holons
- committed holon references
- property maps
- relationship maps
- relationship caches

Navigation algebra operates relative to this layer and must preserve transaction lifecycle invariants.

---

## 6. Initial Navigation Operation Dance Set

The initial operation set is intentionally small.
It supports DAHN and HumanAgent navigation while leaving planner, declarative, join, aggregation, and subquery work for later specs.

Collection-transforming operations such as `Expand`, `Filter`, `OrderBy`, `Skip`, `Limit`, and `Distinct` are naturally afforded by `HolonCollection`.
Seed operations may be afforded by a space, execution domain, session, or other host-defined navigation scope because they create an initial collection.

### 6.1 SeedHolons

    SeedHolons {
      output: VariableName,
      scope: SeedScope,
      holon_type: Option<TypeDescriptorReference>
    }

Produces a `HolonCollection`.

`SeedScope` may represent:

- focal space
- current selection
- explicit seed references
- execution domain
- another host-defined navigation scope

`Focal Space` is the shared runtime-context term for the current default `HolonSpace`.
It is defined in [runtime-shared-types.md](../type-system/runtime-shared-types.md).

When `SeedScope` is `FocalSpace`, seed selection is equivalent to expanding the focal space's `OWNS` relationship:

    SeedHolons(scope: FocalSpace)

means:

    Expand(FocalSpace, OWNS) -> owned_holons

and then, if `holon_type` is present, filtering the owned holons by descriptor-backed type conformance.

When `SeedScope` is an `ExecutionDomain`, seed selection applies the same rule to each space in the domain:

    SeedHolons(scope: ExecutionDomain([space_a, space_b, ...]))

means:

    Expand(space_a, OWNS) -> owned_holons_a
    Expand(space_b, OWNS) -> owned_holons_b
    ...
    merge authorized results

For local spaces, this can produce all holons owned by that space in the current transaction or snapshot.
For remote spaces, the result is limited by TrustChannel authorization and boundary projection rules.

If `holon_type` is present, the host validates and filters using descriptor-backed type conformance.

Common gesture:

    "Show all Books in my I-Space"

can be represented as:

    SeedHolons {
      output: "books",
      scope: FocalSpace,
      holon_type: Book
    }

### 6.2 Expand

    Expand {
      input: VariableName,
      relationship: RelationshipName,
      direction: Direction,
      output: VariableName
    }

Consumes a `HolonCollection`, follows a named relationship channel, and produces a target `HolonCollection`.

The relationship name is an operation parameter.
It is not a property-bearing edge object flowing through the algebra.

Validation:

- outgoing expansion requires the relationship channel to be legal for the source holon types
- incoming expansion must preserve declared and inverse relationship meaning
- descriptor-backed effective relationship lookup is the semantic authority

Runtime behavior:

- the default output is a flat target `HolonCollection`
- source-to-target correlation may be preserved or recovered through `ExecutionPlan` holon topology, `RelationshipMap`, `RelationshipCache`, and traversal provenance
- correlation-sensitive derived views are materialized only when required

### 6.3 Filter

    Filter {
      input: VariableName,
      predicate: Predicate,
      output: VariableName
    }

Consumes a `HolonCollection` and produces a filtered `HolonCollection`.

Predicates initially evaluate each holon in the input collection.
Predicate semantics are host-owned and descriptor-backed where typed values are involved.

False or null-like predicate outcomes are rejected.

### 6.4 OrderBy

    OrderBy {
      input: VariableName,
      keys: Vec<SortKey>,
      output: VariableName
    }

Consumes a `HolonCollection` and produces an ordered `HolonCollection`.

Ordering is host-owned.
hApp graph access does not own ordering semantics.

Sort keys may reference descriptor-backed properties or host-defined stable identity keys.
If pagination occurs without explicit ordering, the host should apply a deterministic default order.

### 6.5 Skip

    Skip {
      input: VariableName,
      count: usize,
      output: VariableName
    }

Consumes a `HolonCollection` and drops the first `count` members according to the collection's current ordering.

### 6.6 Limit

    Limit {
      input: VariableName,
      count: usize,
      output: VariableName
    }

Consumes a `HolonCollection` and keeps at most `count` members according to the collection's current ordering.

### 6.7 Distinct

    Distinct {
      input: VariableName,
      output: VariableName
    }

Consumes a `HolonCollection` and produces a collection with duplicate holon references removed according to host identity semantics.

If a later query surface requires duplicate-preserving row-observable semantics, that belongs in a derived view or planner-level compatibility layer rather than in the foundational collection carrier.

### 6.8 Project

    Project {
      input: VariableName,
      items: Vec<ProjectItem>,
      output: VariableName
    }

Consumes a runtime value and produces a derived view.

`Project` is the boundary where the algebra may materialize:

- scalar values
- scalar collections
- property projections
- source-target pair views
- partitioned collection views
- path or traversal trace views
- row-oriented projections for tabular or OpenCypher-compatible output

`Project` should not make row-oriented output the default execution substrate.
It is a derived-view operation.

---

## 7. Expression And Predicate Model

The initial expression model is intentionally limited.

Initial expressions:

- `CurrentHolon`
- `Property(PropertyName)`
- `Literal(BaseValue)`
- `Variable(VariableName)` where a derived view or project item needs to name an existing binding

Initial predicates:

- `Eq`
- `Neq`
- `Gt`
- `Gte`
- `Lt`
- `Lte`
- `And`
- `Or`
- `Not`
- `Exists(PropertyName)`
- `ConformsTo(TypeDescriptorReference)`

`ConformsTo` is evaluated through descriptor-backed structural support.
For a `ResolvedType`-like execution aid, the conceptual check is:

    resolved_type.descriptor == T
      OR resolved_type.extends_closure.contains(T)

The semantic authority remains the descriptor layer.
The runtime cache is only an execution aid.

---

## 8. Relationship And Path Semantics

MAP relationships are named traversal channels.
They are not foundational property-bearing edge values.

When relationship-specific state is needed, the model should introduce an intersection holon type.

Example:

    Person - HAS_MEMBERSHIP -> Membership
    Membership - MEMBER_OF -> Organization

Paths are derived traversal traces.
They are not primitive runtime carriers in the initial algebra.

A path-like derived view may be materialized for:

- visualization
- provenance
- replay explanation
- OpenCypher path variables
- export

Relationship variables, if needed for Cypher-like compatibility, should initially be interpreted as symbolic traversal provenance:

- source binding
- relationship name
- target binding
- operation identity

They should not force MAP Core to adopt a property-graph edge-instance model.

---

## 9. Correlation-Sensitive Views

The default output of `Expand` may be a flat target `HolonCollection`.
For many interactive gestures, that is sufficient.

Example:

    books
      Expand(Authors)
    authors

If a later gesture or query surface asks for grouped or pairwise results, the host may derive a correlation-sensitive view from:

- `ExecutionPlan` holon topology
- operation input and output variables
- `RelationshipMap`
- `RelationshipCache`
- traversal provenance
- transaction or snapshot state

Supported derived view categories may include:

- partitioned collection: `Book -> [Authors]`
- pair projection: `(Book, Author)`
- path collection
- row-oriented projection

The derived view must preserve the transaction or snapshot context needed to make the view deterministic.

---

## 10. Host/hApp Graph Access Boundary

Navigation Algebra is host-owned.
hApps may provide bounded graph access primitives.

The hApp may perform:

- seed retrieval
- adjacency expansion
- holon fetch
- property fetch
- smartlink or relationship-cache access

The hApp does not own:

- logical plan structure
- predicate semantics
- descriptor semantics
- ordering semantics
- pagination semantics
- projection semantics
- optimization semantics

Illustrative graph access shape:

    GraphAccess {
      seed_holons(scope, holon_type) -> HolonCollection
      expand(input, relationship, direction) -> HolonCollection
      fetch_properties(input, properties) -> PropertyValues
    }

Actual host/hApp APIs may differ.
The boundary rule is the authority.

---

## 11. Predicate Pushdown

The host may push safe predicate subsets into graph access calls.

This is a physical optimization, not a semantic transfer.

Logical plan:

    Expand
    Filter

Possible physical execution:

    expand_with_predicate(pushdown_subset)
    host_filter(full_predicate)

Safe pushdown candidates may include:

- property equality
- simple range comparisons
- simple conjunctions
- relationship-channel constraints
- type filters when the hApp can evaluate them correctly

Unsafe pushdown candidates include:

- cross-variable predicates
- computed expressions
- aggregation-dependent predicates
- complex disjunctions
- host-only functions
- ordering
- pagination
- joins
- subqueries

The host remains semantic authority and must retain the full predicate.

---

## 12. Interactive Plan Construction

Interactive construction layers `InteractiveNavigationSession` on top of navigation operation Dances.

Each `ApplyOperation` Dance:

1. identifies the current input variable or navigation focus
2. appends one or more deterministic operations to the `ExecutionPlan` holon
3. executes those operations immediately in the current `NavigationExecutionBindings`
4. records the resulting output variable and runtime value

Examples:

- Search: `SeedHolons`
- Navigate: `Expand`
- Refine: `Filter`
- Sort: `OrderBy`
- Page: `Skip` / `Limit`
- Shape output: `Project`

The accumulated `ExecutionPlan` holon is the executable replay artifact.
The gesture history may be retained separately for UX or provenance.

Direct execution of individual navigation operation Dances can be implemented before `InteractiveNavigationSession`.
That incremental order supports DAHN delivery without waiting for saved-plan infrastructure.

---

## 13. Save And Replay

A saved navigation session should save the `ExecutionPlan` holon.

The saved plan should preserve:

- operation order
- operation identities
- input and output variables
- operation parameters
- descriptor references required for stable semantics
- enough scope identity to replay against the intended transaction, snapshot, or current-space context

Future saved-plan variants may also retain:

- the original gesture history
- derived explanation data
- an OpenCypher/GQL expression when representable
- an optimized equivalent `ExecutionPlan` holon

The original gesture-built plan remains the faithful replay artifact.

---

## 14. Non-Goals

This initial algebra spec does not define:

- full OpenCypher parsing
- GQL support
- planner algebra
- cost-based optimization
- joins
- apply
- optional match
- aggregation
- subqueries
- mutation plans
- property-bearing relationship variables
- a row-stream execution substrate
- a graph-value execution substrate
- final TS SDK API shape
- final IPC schema

These belong to later specs or appendix/reference documents.

---

## Summary

The initial MAP Navigation Algebra is a small, host-owned set of navigation operation Dances over `HolonCollection`.

It keeps the runtime carrier simple while allowing later `ExecutionPlan` holon and `InteractiveNavigationSession` layers to preserve symbolic structure, derivation, replay, and correlation-sensitive semantics.
Derived views provide the escape hatch for projections, path traces, pair views, partitioned results, and future OpenCypher/GQL-compatible row-observable outputs.
