# Navigation Algebra for MAP Core (v1.1)
*(Human-First DAHN Navigation → Cypher-Ready Foundation)*

This document defines a deliberately constrained, imperative execution algebra designed to power interactive, gesture-driven navigation of MAP property graphs before introducing declarative Cypher compilation.

It establishes:

- A minimal execution operand model
- A lightweight execution tree structure
- A transaction-scoped host interpreter
- A clean host/hApp graph-access boundary
- A forward-compatible path toward OpenCypher support

The algebra is intentionally limited to navigation-oriented operations while remaining compatible with the fuller query-planner algebra that may later support OpenCypher compilation, logical rewrites, joins, aggregation, and cost-based optimization.

---

# 1. Architectural Positioning

Navigation Algebra is part of the broader MAP Dance API refactor, which itself sits within the Commands / TypeScript SDK deployment roadmap.

Its role is narrow and concrete:

- Provide immediate support for human-first DAHN navigation
- Introduce proper execution operands
- Support replayable navigation plans
- Preserve a path to full graph query planning
- Avoid exposing query semantics to external dance implementations

This is not a Cypher-only interface.

This is not the full Dance dispatch architecture.

This is the host-owned execution substrate for graph navigation.

---

# 2. Core Decision: Host-Owned Algebra

MAP adopts the following boundary:

> The navigation/query algebra is owned by the host.

This means:

- `ExecutionPlan`, `PlanNode`, `PlanStep`, `Value`, `Row`, and `RowSet` are host-side execution structures.
- hApp code does not own or execute the logical algebra.
- hApp may provide graph-access primitives such as scan, expand, and fetch.
- External dance implementations do not receive or execute algebra plans.
- Query semantics remain host-controlled.

This preserves a clean separation between:

- Host-owned execution semantics
- hApp-owned storage access and validation
- Dance-owned behavioral affordances

---

# 3. Relationship to the Dance API

Navigation/query behavior may be exposed as Dances, especially as Builtin dances, but execution remains host-native.

For example:

- Search
- Navigate
- Expand
- Filter
- ExecuteQuery
- SaveQuery

These may be modeled as DanceTypes, but their implementation is host-owned.

External dance implementations are not responsible for graph algebra execution.

---

# 4. Relationship to Commands

The Commands layer provides the uniform request/response container.

Navigation Algebra is one execution substrate that can sit behind Commands.

The intended flow is:

    TS client code
      → TS SDK
      → TS Command Dispatch
      → serialization
      → IPC
      → deserialization
      → transaction binding
      → Rust Commands Dispatcher
      → TransactionContext
      → host Navigation Algebra interpreter
      → hApp graph-access primitives as needed

Commands remain the transport and dispatch surface.

Navigation Algebra is the internal execution model for graph-native read/navigation commands.

---

# 5. Three Runtime Layers

Before introducing graph execution, MAP distinguishes three layers.

## 5.1 Ontology Layer

Persistent, holonic schema/data layer.

Includes:

- `TypeDescriptor`
- `Extends`
- `InstanceProperties`
- `InstanceRelationships`
- RelationshipType descriptors
- PropertyType descriptors

All schema semantics remain ontology-as-data.

No Rust enum should duplicate ontology concepts that are already represented as committed holons.

---

## 5.2 Runtime Structural Layer

Ephemeral host-side projection of ontology structure.

Core type:

    ResolvedType {
        descriptor: TypeDescriptorReference,
        extends_closure: HashSet<TypeDescriptorReference>,
        effective_property_types: BTreeMap<PropertyName, PropertyTypeReference>,
        effective_relationship_types: HashMap<RelationshipName, RelationshipTypeReference>,
    }

Properties:

- Built from committed schema holons
- Cached in the host `TypeRegistry`
- Immutable
- Deterministic
- Conflict-intolerant
- Not persisted
- Not IPC-visible

This layer allows constant-time structural validation during execution.

---

## 5.3 Instance State Layer

Transaction-scoped mutable state.

Includes:

- Property maps
- Relationship maps
- staged holons
- transient holons
- committed references
- undo-aware mutation state later

Navigation Algebra operates transaction-relatively and must respect transaction lifecycle invariants.

---

# 6. Semantic Reference Types

Introduce semantic newtypes over existing holon references where they clarify execution roles.

Examples:

    TypeDescriptorReference(HolonReference)
    PropertyTypeReference(HolonReference)
    RelationshipTypeReference(HolonReference)
    InstanceHolonReference(HolonReference)

Purpose:

- Compile-time role distinction
- Cleaner API signatures
- Safer validation
- Better alignment with future query compilation

These wrappers encode roles, not ontology rules.

Ontology rules remain data-driven.

---

# 7. Minimal Operand Model

The Navigation Algebra introduces a small operand set.

## 7.1 Value

    enum Value {
        Scalar(BaseValue),
        Holon(InstanceHolonReference),
        Relationship(HolonRelationshipReference),
        List(Vec<Value>),
        Map(BTreeMap<MapString, Value>),
        Null,
    }

Phase 1 may omit relationship, map, or advanced scalar support if not needed immediately.

The important point is that `Value` becomes the uniform internal value domain for query/navigation execution.

---

## 7.2 Row

    struct Row {
        bindings: BTreeMap<VariableName, Value>
    }

A row is an in-memory binding of variables to values.

Rows are:

- transaction-scoped
- host-only
- not persisted
- not necessarily IPC-visible

---

## 7.3 RowSet

    type RowSet = Vec<Row>;

`RowSet` is materialized in early phases.

Streaming may be introduced later without changing logical operator semantics.

---

# 8. Minimal Expression and Predicate Model

Expressions are host-owned and evaluated against rows.

## 8.1 Expressions

Initial expression forms:

- `Var(name)`
- `Literal(Value)`
- `Property(var, PropertyName)`

Optional later:

- list expressions
- map expressions
- path expressions
- function calls
- computed projections

---

## 8.2 Predicates

Initial predicate forms:

- `Eq`
- `Neq`
- `Gt`
- `Gte`
- `Lt`
- `Lte`
- `And`
- `Or`
- `Not`
- `Exists(Property(...))`
- `ConformsTo(var, TypeDescriptorReference)`

Optional later:

- `StartsWith`
- `Contains`
- `In`
- path existence predicates
- pattern predicates

---

## 8.3 ConformsTo

`ConformsTo(var, T)` is evaluated using `ResolvedType`.

Conceptually:

    resolved_type.extends_closure.contains(T)
      OR resolved_type.descriptor == T

This avoids recursive inheritance traversal during execution.

---

# 9. ExecutionPlan Tree

Even though early navigation is linear, plans should be represented as a tree from the start.

This avoids later migration when adding:

- Union
- Optional
- Apply
- Exists
- Aggregation
- Subqueries
- Cypher compilation

Initial shape:

    struct ExecutionPlan {
        root: PlanNode
    }

    enum PlanNode {
        Pipeline(Vec<PlanStep>)
    }

Phase 1 supports only `Pipeline`.

Future variants may include:

    Union {
        left: Box<PlanNode>,
        right: Box<PlanNode>,
        distinct: bool,
    }

    Apply {
        left: Box<PlanNode>,
        right: Box<PlanNode>,
    }

    Optional {
        input: Box<PlanNode>,
        optional: Box<PlanNode>,
    }

    Aggregate {
        input: Box<PlanNode>,
        keys: Vec<Expression>,
        aggregations: Vec<AggregationSpec>,
    }

The tree is structural preparation, not premature implementation.

---

# 10. Minimal PlanStep Set

Within `PlanNode::Pipeline`, Phase 1 supports a small set of steps.

## 10.1 SeedSpace

    SeedSpace { as: VariableName }

Seeds the current space into the row stream.

Used as the canonical starting point for space-scoped navigation.

---

## 10.2 SeedHolon

    SeedHolon {
        reference: InstanceHolonReference,
        as: VariableName
    }

Seeds a known holon into the row stream.

Used when navigation begins from an already-selected holon.

---

## 10.3 Expand

    Expand {
        from: VariableName,
        relationship: RelationshipName,
        direction: Direction,
        to: VariableName,
        bind_relationship: Option<VariableName>,
    }

Traverses from a bound holon across a named relationship.

Direction values:

- outgoing
- incoming
- either

Logical responsibility:

- Produce rows binding the target holon
- Optionally bind the relationship/smartlink

Validation:

- Outgoing expansion requires the relationship to exist in the source type’s effective relationship contract.
- Incoming expansion may require resolving inverse relationship metadata.

---

## 10.4 Filter

    Filter {
        predicate: Predicate
    }

Keeps only rows where predicate evaluates to true.

False or null are rejected.

---

## 10.5 Project

    Project {
        items: Vec<ProjectItem>
    }

Computes output bindings and controls result shape.

Example item:

    ProjectItem {
        expression: Expression,
        as: VariableName
    }

---

## 10.6 Distinct

    Distinct {
        keys: Option<Vec<Expression>>
    }

Removes duplicate rows.

If keys are omitted, all visible bindings are considered.

---

## 10.7 OrderBy

    OrderBy {
        keys: Vec<SortKey>
    }

Sorts rows according to host-owned ordering semantics.

Sort key:

    SortKey {
        expression: Expression,
        direction: Asc | Desc,
        null_order: NullsFirst | NullsLast
    }

Ordering is host-owned.

hApp does not own ordering semantics.

---

## 10.8 Skip

    Skip {
        count: usize
    }

Drops the first N rows.

---

## 10.9 Limit

    Limit {
        count: usize
    }

Keeps at most N rows.

---

# 11. Canonical Root Scan via OWNS

Human “search” starts from the current space.

Canonical pattern:

1. `SeedSpace`
2. `Expand (space)-[:OWNS]->(h)`
3. `Filter ConformsTo(h, T)`
4. `Filter property predicates`
5. `OrderBy`
6. `Skip`
7. `Limit`
8. `Project`

This models the common Cypher shape:

    MATCH (h:T)
    WHERE ...
    RETURN ...
    ORDER BY ...
    SKIP ...
    LIMIT ...

without requiring label scan primitives in the initial algebra.

Type filtering is handled through `ResolvedType`.

---

# 12. Host/hApp Graph Access Boundary

Navigation Algebra is host-owned, but the hApp may provide graph access primitives.

The hApp may execute bounded retrieval segments such as:

- seed space-owned holons
- expand adjacency
- fetch holons
- fetch properties
- fetch smartlinks

The hApp does not own:

- logical plan structure
- predicate semantics
- ordering semantics
- pagination semantics
- joins
- aggregation
- query optimization

---

# 13. GraphAccess Primitives

The host interpreter may depend on a narrow `GraphAccess` interface.

Illustrative shape:

    trait GraphAccess {
        fn seed_space_owns(space: SpaceReference)
            -> Result<Vec<InstanceHolonReference>, HolonError>;

        fn expand(
            from: Vec<InstanceHolonReference>,
            relationship: RelationshipName,
            direction: Direction
        ) -> Result<Vec<GraphEdge>, HolonError>;

        fn fetch_holons(
            refs: Vec<InstanceHolonReference>
        ) -> Result<Vec<Holon>, HolonError>;
    }

`GraphEdge` may contain:

    GraphEdge {
        from: InstanceHolonReference,
        relationship: Option<HolonRelationshipReference>,
        to: InstanceHolonReference,
    }

The exact representation can evolve.

The boundary principle is more important than the initial type names.

---

# 14. Predicate Pushdown

To avoid excessive host/hApp data transfer, the host may push safe predicate subsets into hApp graph access calls.

This is a physical execution optimization, not a semantic transfer.

Logical plan remains:

    Expand
    Filter

Physical execution may become:

    expand_with_predicate(pushdown_subset)
    host_filter(full_predicate)

## 14.1 Safe Pushdown Candidates

Examples:

- property equality
- property range comparisons
- simple conjunctions
- relationship name/type constraints
- possibly type filters if efficiently available

## 14.2 Unsafe Pushdown Candidates

Examples:

- cross-variable predicates
- computed expressions
- aggregation-dependent predicates
- complex disjunctions
- host-only functions
- ordering
- pagination
- joins
- subqueries

## 14.3 Correctness Rule

The host remains semantic authority.

The host must retain the full predicate and be able to evaluate it independently.

Debug or strict modes may re-check pushed-down results.

---

# 15. Ordering and Pagination

Ordering, skip, and limit are host-owned.

Even when scan or expand occurs in hApp, result shaping remains in host.

This enables stable pagination and avoids re-retrieval.

## 15.1 Stable Ordering

If a query uses pagination without explicit `OrderBy`, the host should apply a deterministic default order.

Possible default:

- HolonId
- relationship/smartlink order if defined
- canonical key order if available

Nondeterministic pagination should be avoided.

---

## 15.2 Pagination Cache

The host may maintain a pagination cache keyed by:

- normalized plan hash
- parameters
- space
- transaction id or snapshot id
- possibly user/session context

Cache value:

    CachedResultSet {
        ordered_refs: Vec<InstanceHolonReference>,
        created_at: Timestamp,
        snapshot_id: SnapshotId,
    }

First page execution:

1. scan/expand/fetch as needed
2. filter
3. sort
4. cache ordered refs
5. return requested page

Subsequent page execution:

1. look up cached ordered refs
2. slice
3. fetch only needed holons
4. return page

This avoids repeated expansion and sorting.

---

# 16. Interactive Query Building

Interactive navigation is append-oriented.

Each human gesture adds structure to the plan.

Examples:

- Search → SeedSpace + Expand OWNS + Filter
- Navigate → Expand
- Refine → Filter
- Sort → OrderBy
- Page → Skip/Limit
- Shape → Project

Even though the plan is tree-shaped, early interaction will mostly build a single pipeline.

The plan remains:

- serializable
- replayable
- explainable
- persistable later
- translatable to declarative OpenCypher later

---

# 17. Save Query

A saved navigation session may be represented as an `ExecutionPlan`.

Future options:

1. Save the host plan directly.
2. Reverse-engineer an equivalent OpenCypher expression.
3. Store both.
4. Store the original gesture sequence plus the derived plan.

Initial recommendation:

- Save the host-owned plan representation for replay.
- Add Cypher serialization later.

This delivers early value without requiring a Cypher compiler.

---

# 18. Command Integration

Navigation Algebra is invoked through the Commands layer.

Potential command shape:

    QueryCommand::ExecutePlan {
        plan: ExecutionPlan,
        page: Option<PageSpec>
    }

However, early Phase 2 may expose smaller commands before arbitrary plans are public.

Examples:

    QueryCommand::GetHolon
    QueryCommand::GetRelated
    QueryCommand::ListOwned
    QueryCommand::SearchOwned

These can be implemented internally using the same execution substrate.

---

# 19. Dance Integration

Query/navigation commands may also be exposed as Builtin Dances.

Examples:

- `Search.DanceType`
- `Navigate.DanceType`
- `ExecuteQuery.DanceType`
- `SaveQuery.DanceType`

These Dances are host-native.

They may be declared through the Dance schema and discovered as affordances, but their implementation uses the host execution substrate.

External dance implementations do not execute the algebra.

---

# 20. Relationship to Query Planner Algebra

Navigation Algebra is a subset of the fuller Query Planner Algebra.

Containment relationship:

    Navigation Algebra ⊂ Query Planner Algebra ⊂ Cypher Operator Space

Navigation Algebra intentionally omits:

- joins
- apply
- optional match
- aggregation
- subqueries
- cost-based optimization
- full path semantics
- physical operator selection
- external implementation ABI

This is a scope decision, not a limitation of the architecture.

---

# 21. Future Evolution Toward OpenCypher

The system can evolve as follows:

    Imperative DAHN gestures
      → Navigation Algebra plan
      → Saved/replayable plan
      → OpenCypher serialization
      → OpenCypher parsing
      → Query Planner Algebra
      → logical rewrites
      → cost-based optimization
      → physical execution strategies

No operand redesign should be required if the early operand model is disciplined.

---

# 22. Non-Goals

This document does not define:

- full OpenCypher parsing
- GQL support
- external dance implementation ABI
- dynamic dispatch resolution
- cost-based optimizer
- joins or Apply
- aggregation
- mutation plans
- rollback or undo semantics
- TypeScript SDK surface
- final IPC schema

These belong to adjacent roadmap documents.

---

# 23. Phase-Oriented Implementation

## Phase A — Structural Foundation

Implement or integrate:

- `ResolvedType`
- `TypeRegistry`
- semantic reference wrappers
- constant-time property and relationship contract checks

This underpins all later execution validation.

---

## Phase B — Operand Definitions

Introduce host-side:

- `Value`
- `Row`
- `RowSet`
- `Expression`
- `Predicate`
- `SortSpec`
- `PageSpec`

These may later gain wire counterparts for Commands.

Keep runtime and wire representations distinct.

---

## Phase C — ExecutionPlan Tree

Introduce:

- `ExecutionPlan`
- `PlanNode`
- `PlanStep`
- `PlanNode::Pipeline`

Even if only linear pipelines execute initially.

---

## Phase D — Interpreter

Implement host-side execution for:

- SeedSpace
- SeedHolon
- Expand
- Filter
- Project
- Distinct
- OrderBy
- Skip
- Limit

Use materialized `RowSet`.

---

## Phase E — GraphAccess Boundary

Define host/hApp access primitives.

Implement:

- OWNS scan
- adjacency expansion
- holon fetch

Keep this layer narrow.

---

## Phase F — Minimal Query Commands

Introduce command-level wrappers.

Possible initial commands:

- `GetHolon`
- `GetRelated`
- `ListOwned`
- `SearchOwned`
- `ExecutePlan` later

Mutation Commands can proceed independently.

---

## Phase G — Pagination Cache

Implement host-owned cache for stable ordered result sets.

Support:

- deterministic page slices
- no re-expand on cache hit
- transaction/snapshot-bound invalidation

---

## Phase H — Predicate Pushdown

Add safe pushdown classification.

Allow hApp to apply safe filter subsets during scan/expand.

Retain host semantic authority.

---

## Phase I — Save Query

Persist or serialize navigation plans.

Initial saved form may be the `ExecutionPlan`.

Cypher serialization can come later.

---

## Phase J — OpenCypher Evolution

Add:

- Cypher parser
- compilation to Query Planner Algebra
- logical rewrites
- cost model
- physical plan selection

This is explicitly future work.

---

# 24. Acceptance Criteria for Initial Navigation Algebra

The initial implementation is successful when:

- Interactive navigation can be represented as an `ExecutionPlan`.
- Basic space search can be represented as SeedSpace → Expand OWNS → Filter → Project.
- Expansion validates against `ResolvedType`.
- Property predicates evaluate in host.
- Ordering and pagination are host-owned.
- hApp is used only for graph access primitives.
- Existing mutation commands remain independent.
- No external dance implementation depends on query algebra.
- The design remains compatible with future OpenCypher compilation.

---

# 25. Architectural Summary

Navigation Algebra gives MAP an immediate, human-first graph navigation substrate while preserving a clean path to full query planning.

It introduces the minimal execution model needed for DAHN-style interaction:

- values
- rows
- row sets
- expressions
- predicates
- plan steps
- plan trees
- host interpretation

It does this while preserving the host/hApp split:

- host owns semantics
- hApp provides graph access
- external dances remain outside query algebra

The result is an incremental, safe, and future-compatible foundation for MAP Commands, Dance integration, and eventual OpenCypher support.