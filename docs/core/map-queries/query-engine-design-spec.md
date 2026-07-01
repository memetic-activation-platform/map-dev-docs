# MAP Graph Query Engine v1.1

## Changelog

### v1.1

- sharpens the seam between `Command`, `Dance`, and `Query`
- treats query execution as a `QueryDance`, invoked through `DanceInvocation`
- makes the `QueryDanceRequest` a fixed-shape holon rather than a projection-shaped payload
- makes `QueryGraph` the symbolic query plan and `ExecutionInstance` the runtime execution state
- makes `HolonCollection` the primary runtime query operand and result substrate
- simplifies `QueryStep` so normal step input flows through `StepDependsOn`
- reserves explicit input binding use for root steps through `UsesInitialBinding`
- replaces string-expression placeholders for filter and ordering with structural rule holons
- replaces free-form projection-expression placeholders with `PropertyNameList`
- incorporates the distributed retrieval model from `dist-query-concept.md`
- aligns the design more closely with `query-algebra-design-spec.md`
- folds in the remaining algebra-spec invariants around descriptor-governed
  semantics, relationship normalization, projection boundaries, and
  non-foundational result views
- adds a companion Rust wrapper-layer design grounded in typed holon wrappers

### v1.0

- framed the graph query engine primarily as a coarse-grained dancer executing a `QueryGraph`
- treated step input/output binding structure more generically
- allowed broader result-shape drift away from the `HolonCollection -> Operation -> HolonCollection` algebra

## Purpose

This document is the v1.1 design-spec narrative for MAP's graph query engine.

It captures the intended architecture of query execution in MAP, using the
authoritative schema names currently grounded in the generated core-schema and
the intended semantics grounded in the query algebra design.

The companion precise schema artifact is:

- [command-dance-query-schema-dsl.md](/Users/stevemelville/dev/map-dev-docs/docs/core/map-queries/command-dance-query-schema-dsl.md)

That DSL is the precise type-and-relationship companion to this narrative spec.
This document is the more readable architectural explanation.

The distributed-retrieval concept note that informs the distributed execution
section is:

- [dist-query-concept.md](/Users/stevemelville/dev/map-dev-docs/docs/core/map-queries/dist-query-concept.md)

That concept document is exploratory and forward-looking. It is the current
home where fuller multi-space query-execution design is being worked through.
This v1.1 spec remains focused on the stable query-model seam needed for
Commands, Dances, and near-term single-space query execution.

## Core Position

The key design rule is:

```text
Command = ingress envelope and lifecycle policy.
Dance = descriptor-afforded executable behavior.
Query = request payload supplied to a Query Dance.
```

This is the seam that v1.1 is meant to sharpen.

A query is not itself a command.

A query is not itself a dance.

A query is the structured payload carried by a query dance invocation.

## Query Engine as Dance

MAP provides graph query execution as a dance.

That means the graph query engine is not modeled as a standalone, magical
runtime subsystem floating outside MAP's normal type-and-affordance model. It is
modeled as a concrete dance implementation of a `QueryDance`.

In the general dance model, any holon instance may serve as the affording holon
for a `DanceInvocation`, so long as that instance's type affords the dance
being invoked.

Conceptually:

```text
SomeHolonType
  Affords -> QueryDance.DanceType

QueryDance.DanceType
  HasImplementation -> GraphQueryEngine.DanceImplementation
```

This preserves MAP's extensibility requirement. Different spaces may eventually
afford different query dances or different implementations with different
optimizers, capabilities, and execution strategies.

In the current distributed query design, `HolonSpace` is the ordinary affording
holon for query execution. That is an important deployment convention, but it
should not be encoded as a narrowing of the base `DanceInvocation` schema.

## Implementation Placement

The canonical query engine core should live in a shared crate rather than being
owned by the host runtime alone.

That shared engine owns:

- query-step semantics
- binding flow
- descriptor-governed validation
- result-binding selection
- packaging of pushdown-capable execution segments
- detection that execution has reached a distributed delegation boundary

The shared engine must remain safe for single-space guest execution.

That means it should not own:

- cross-space trust-channel dispatch
- host-side async fanout
- host-only task orchestration
- branch tracking across spaces

Instead, the runtime split is:

- the shared query engine, which owns common execution semantics
- a local single-space executor, which may run in host or guest
- a coordinating host adapter, which handles distributed delegation and branch
  orchestration when work must continue in several spaces

So the shared engine may determine that a distributed continuation is required,
but it returns that need to the host adapter rather than trying to perform
parallel dispatch itself.

## Canonical Execution Path

The canonical v1.1 execution path is:

```text
Transaction.HolonType
  AffordsCommand -> Dance.CommandType

Dance.CommandType
  payload -> DanceInvocation.HolonType

DanceInvocation.HolonType
  InvokesDance    -> QueryDance.DanceType
  AffordingHolon  -> HolonType
  Request         -> QueryDanceRequest.HolonType

QueryDanceRequest.HolonType
  QueryGraph      -> QueryGraph.HolonType
  InitialBindings -> ExecutionBinding.HolonType

ExecutionInstance.HolonType
  ExecutesRequest   -> QueryDanceRequest.HolonType
  ExecutionBindings -> ExecutionBinding.HolonType
  ExecutionResult   -> HolonCollection.HolonType

QueryDanceResponse.DanceResponseType
  ResponseBody -> HolonCollection.HolonType
```

Narratively, this means:

- the command layer gets the request into the system
- the dance layer identifies the executable behavior being invoked
- the affording holon must be an instance whose type affords that dance
- the query layer provides the symbolic plan plus named starting bindings
- the execution layer creates a run-specific `ExecutionInstance`
- the runtime result is a `HolonCollection`

## Vocabulary

The important v1.1 terms are:

- `Dance.CommandType`: the command surface for dance execution
- `DanceInvocation.HolonType`: the typed invocation holon carried as the dance command payload
- `AffordingHolon`: the holon affording the dance, not merely a "target";
  the referenced instance must afford the dance named by `InvokesDance`
- `QueryDance.DanceType`: the concrete dance type for query execution
- `QueryDanceRequest.HolonType`: the fixed-shape request holon for query execution
- `QueryGraph.HolonType`: the symbolic query plan
- `QueryStep.HolonType`: an operation node in that plan
- `QueryBinding.HolonType`: a symbolic variable name used by the plan
- `ExecutionBinding.HolonType`: a runtime binding from query variable to `HolonCollection`
- `ExecutionInstance.HolonType`: one ephemeral execution run of one request
- `QueryDanceResponse.DanceResponseType`: the dance response carrying the final result collection

## Query Architecture Overview

The externally visible query affordance is no longer best described as a bare:

```text
GraphQueryEngine(QueryGraphReference) -> QueryResultReference
```

That old framing was too coarse and hid the important seam between command,
dance, request, plan, and execution state.

The v1.1 architecture should instead be understood as:

```text
Dance.CommandType
  payload -> DanceInvocation

DanceInvocation
  invokes -> QueryDance
  request -> QueryDanceRequest

QueryDanceRequest
  query_graph      -> QueryGraph
  initial_bindings -> ExecutionBinding*

QueryDance
  response -> QueryDanceResponse

QueryDanceResponse
  response_body -> HolonCollection
```

The query language evolves through `QueryGraph`, `QueryStep`, `QueryStepKind`,
parameter projections, and rule holons. It does not evolve by proliferating
algebra-specific dances.

## QueryGraph

A `QueryGraph` is the symbolic query plan.

It is the reusable, saveable, replayable MAP artifact that describes what the
query means without carrying any live execution state.

In v1.1 it owns:

- human-facing identity through `QueryName` and `QueryDescription`
- the query's `QuerySteps`
- the query's declared external input names
- the query's declared exported result name

Through its `QueryStep`s and dependency relationships, a `QueryGraph` also owns
the symbolic execution topology, operation parameters, relationship traversal
provenance, and explanation topology for the query.

Conceptually:

```text
QueryGraph
  QuerySteps            -> QueryStep*
  DeclaredInputBindings -> QueryBinding*
  DeclaredResultBinding -> QueryBinding
```

### DeclaredInputBindings

`DeclaredInputBindings` defines the query's external input contract.

These are symbolic binding names that the plan is allowed to expect from a
caller. They are not runtime collections themselves. They are just the names the
plan is written against.

For example, a graph may declare that it expects a binding named `books` or
`starting_spaces`. The actual runtime values for those names arrive through
`QueryDanceRequest.InitialBindings`.

So:

- `DeclaredInputBindings` lives on the symbolic plan
- `InitialBindings` lives on the concrete request
- `ExecutionBindings` lives on the runtime execution instance

### DeclaredResultBinding

`DeclaredResultBinding` defines the query's exported output contract.

A query may produce several intermediate named bindings internally, but exactly
one symbolic binding is designated as the graph's externally meaningful result.

That is the binding whose runtime `HolonCollection` should be treated as the
result of the query when execution completes.

So, in plain terms:

- `DeclaredInputBindings` = the named inputs the query accepts
- `DeclaredResultBinding` = the named output the query promises
- `QuerySteps` = the transformations in between

## QueryDanceRequest

`QueryDanceRequest` is the fixed-shape input contract for query execution.

It contains:

- `QueryGraph -> QueryGraph.HolonType`
- `InitialBindings -> ExecutionBinding.HolonType`

This keeps the request explicit:

- what symbolic plan is being executed
- what named runtime collections the plan starts from

The request is intentionally simple. It does not carry runtime execution state.

For the first executable vertical slice, root query input should come from
`InitialBindings`.

The affording holon scopes execution, authority, and locality, but it is not
the query's starting data. A root step should name the request-supplied
starting collection through `UsesInitialBinding`.

## ExecutionInstance

`ExecutionInstance` represents one execution run of one `QueryDanceRequest`.

It is an ephemeral runtime holon, not a reusable query-plan artifact.

It owns:

- the request it is executing
- the live runtime bindings for that execution
- execution status
- the final result collection

Conceptually:

```text
ExecutionInstance
  ExecutesRequest   -> QueryDanceRequest
  ExecutionBindings -> ExecutionBinding*
  ExecutionResult   -> HolonCollection?
```

This separation matters because the same `QueryGraph` may be executed multiple
times with different initial bindings, different scopes, or concurrently, and
none of that should contaminate the symbolic plan.

In the intended runtime posture, `ExecutionInstance` is not merely an internal
host-side helper struct. It is a transient holon-backed execution artifact.

Likewise, `ExecutionBinding` should be understood as explicit runtime binding
state maintained during execution rather than as something projected onto a
holon only after the run completes.

Those transient execution artifacts may remain alive for the life of the
surrounding transaction so they can be inspected, debugged, or explained
without becoming persisted domain state.

## HolonCollection as Query Substrate

`HolonCollection` is the primary runtime operand and result substrate for query
execution.

The core algebraic bias remains:

```text
HolonCollection -> Operation -> HolonCollection
```

This is one of the key simplifications restored in v1.1.

Even projection-producing steps remain collection-oriented at the runtime
substrate level. A `Project` step produces a `HolonCollection` of projection
references rather than leaving the collection substrate entirely.

A `HolonCollection` contains holon references and collection semantics. It does
not contain variable bindings, relationship provenance, execution provenance, or
query-plan metadata. Those belong to `QueryGraph`, `QueryStep`, and
`ExecutionInstance`.

`HolonReference` preserves holon identity and may defer state access. Callers may
read through the reference surface exposed by MAP's holon APIs, but deferred
materialization does not change the query substrate: operations still consume
and produce collections of references.

The core query engine must not introduce foundational runtime carriers such as
`RowSet`, `Expansion`, `RelationshipMap`, or `GraphValue` in order to execute
ordinary navigation. Concrete row-like, path-like, graph-like, or scalar result
surfaces may be materialized at explicit boundaries when a caller or
compatibility surface requires them.

## QueryStep

A `QueryStep` is an operation node in a `QueryGraph`.

The v1.1 `QueryStep` model is intentionally smaller and more chain-oriented than
the v1.0 draft.

Each step identifies:

- its operation kind
- its operation parameters
- its predecessor steps
- optionally, a request-supplied initial binding for root steps
- optionally, a symbolic output binding name

Conceptually:

```text
QueryStep
  StepKind          -> QueryStepKind
  StepParameters    -> HolonType?
  StepDependsOn     -> QueryStep*
  UsesInitialBinding -> QueryBinding?
  StepOutputBinding -> QueryBinding?
```

### StepDependsOn

`StepDependsOn` is the normal structural flow mechanism.

Non-root steps consume the output of predecessor steps through dependency
relationships. That means the common step-to-step execution chain does not need
a generic explicit input-binding field on every step.

### UsesInitialBinding

`UsesInitialBinding` exists only so a root step can explicitly name which
request-supplied starting binding it consumes.

This keeps explicit binding references where they are needed, without forcing
every step in the graph to carry them.

For the first executable slice, the intended shape is deliberately narrow:

- exactly one root `SeedHolons` step
- that root consumes one request-supplied `InitialBinding`
- downstream steps follow one predecessor chain through `StepDependsOn`
- no multi-root execution, branch fan-in, or general graph scheduling is
  required in that first slice

### StepOutputBinding

`StepOutputBinding` is optional.

Not every intermediate step result needs a stable symbolic name. A step may
simply feed successor steps structurally through the dependency chain. A named
binding becomes useful when a result needs to be:

- designated as the final query result
- reused by more than one successor
- inspected or explained
- referenced externally

Relationship names, operation identities, and traversal provenance belong to the
step that performs the work. They are not embedded into the `HolonCollection`
produced by the step.

## QueryStepKind

`QueryStepKind` remains an abstract holon type describing a family of query-step
operations.

In v1.1 its common semantic contract is deliberately small:

- `StepInputType -> HolonCollection.HolonType`
- `StepResultType -> HolonCollection.HolonType`
- `StepParameterType -> Projection.HolonType?`

This matches the initial algebra more closely than the earlier, driftier design.

## Descriptor-Owned Semantics

Descriptors are the semantic source for query validation and interpretation.

The query engine should use descriptor-backed structure to validate relationship
traversal, property access, projection property names, and operation
applicability. It should use descriptor-backed value and operator semantics to
interpret filter and ordering rules.

This keeps query execution aligned with MAP's type-and-affordance model:

- holon types define the available structural surface
- relationship descriptors define legal traversal channels and inverse names
- property and value descriptors define what may be projected, compared, sorted,
  or filtered
- step kinds define the executable operation contract

The query engine is therefore descriptor-governed graph navigation over MAP
holons, not a separate property-graph database runtime hidden inside
`holons_core`.

## Initial Operation Set

The v1.1 initial step kinds are:

- `SeedHolonsQueryStepType`
- `ExpandQueryStepType`
- `FilterQueryStepType`
- `OrderByQueryStepType`
- `SkipQueryStepType`
- `LimitQueryStepType`
- `DistinctQueryStepType`
- `ProjectQueryStepType`

This is intentionally close to the initial operation set from
`query-algebra-design-spec.md`.

## Parameter Modeling

The parameter side of the design is also narrower and more structural in v1.1.

### Expand

`ExpandParameters` carries a `RelationshipName` property.

`Expand` consumes a `HolonCollection`, follows a named MAP relationship channel,
and produces a target `HolonCollection`.

MAP relationships are named traversal channels, not foundational
property-bearing edge instances. Each semantic relationship has:

- a declared relationship name
- an inverse relationship name
- a declared source endpoint type
- a declared target endpoint type

Those names and endpoint roles describe one semantic relationship pair, not two
separate edge kinds.

For example, for a semantic relationship:

```text
(A)-[R]->(B)
```

with inverse name `Rinv`, a declarative surface may express the same semantic
relationship through equivalent surface forms such as:

```text
(A)-[R]->(B)
(A)<-[Rinv]-(B)
(B)-[Rinv]->(A)
(B)<-[R]-(A)
```

The executable query step should normalize that surface intent onto the one
semantic relationship pair before execution. Validation must not be reduced to a
naive check that the requested relationship name is directly declared on the
current source type.

In the current v1.1 schema, the narrow `ExpandParameters` shape carries
`RelationshipName`. Declarative authoring surfaces that distinguish traversal
direction must compile that direction into the chosen declared or inverse
relationship name, or into a future structural direction field if the schema is
extended. Either way, execution-time validation must determine:

- which semantic relationship pair the requested name refers to
- whether the current source holon type is a legal endpoint for the traversal
- whether the requested surface intent is compatible with the declared/inverse
  relationship semantics

If the traversal is legal but there are no matching runtime targets, `Expand`
returns an empty `HolonCollection`.

If no legal normalization exists for the requested relationship name, source
type, and traversal intent, `Expand` returns a validation error rather than an
empty collection.

If relationship-specific state is needed, MAP should model that state using
holons, typically through an intersection `HolonType`, rather than treating
relationships themselves as property-bearing runtime edges. Manually ordered
collections may keep sequence information as collection-organization metadata,
but that does not make relationship state a general schema-level edge payload.

For the first executable slice:

- `Expand` should validate descriptor legality rather than behaving as a
  permissive name-only traversal
- if any input member does not legally afford the requested traversal channel,
  the step should fail rather than silently skipping invalid members
- successful `Expand` preserves traversal order and duplicates
- deduplication and ordering remain the job of later explicit `Distinct` and
  `OrderBy` steps

`ExpandAll`, if introduced by an authoring surface or planner, is planning sugar
over multiple `Expand` steps. It is not a distinct runtime result shape.

### Filter

`FilterParameters` no longer relies on a placeholder string expression.

Instead it points structurally to one or more `FilterRule` holons:

```text
FilterParameters
  FilterRules -> FilterRule*
```

This keeps room for filter semantics to become a proper structural mini-model.

`Filter` remains a standalone `QueryStep` in the query model even when an
execution runtime can evaluate it together with an adjacent `Expand`.

That distinction matters because MAP should not mutate its semantic query
vocabulary just to represent one common optimization pattern.

### OrderBy

`OrderByParameters` no longer relies on a placeholder string expression.

Instead it points structurally to one or more `OrderByRule` holons:

```text
OrderByParameters
  OrderByRules -> OrderByRule*
```

### Project

`ProjectParameters` does not use a free-form projection expression string in
v1.1.

Instead it uses `PropertyNameList.PropertyType`, intended as a value-array of
`PropertyName` values.

That means projection is expressed as an explicit list of requested property
names rather than as an opaque mini-language.

`Project` is the explicit materialization boundary of the executable algebra.
Before projection, execution should generally preserve deferred access through
`HolonReference`, `HolonCollection`, `QueryGraph`, and `ExecutionInstance`.

A projection is a materialized, self-describing holon-shaped value described by
a derived `HolonType`. Projection types may be anonymous and inline or reusable
content-addressed descriptors assembled from existing schema elements such as
property, value, and relationship types.

Projection values may implement the same readable holon-facing surface as other
holons, but they remain materialized selected state. References preserve
identity and defer materialization; projections contain selected state.

## Query Results

The external result of query execution is simply a `HolonCollection`.

The older `QueryResult` wrapper framing is intentionally dropped from the core
v1.1 model.

That does not mean the engine cannot internally track diagnostics or richer
execution state. It means the externally meaningful result payload of the query
dance is the result collection itself:

```text
QueryDanceResponse
  ResponseBody -> HolonCollection
```

Diagnostics belong to the dance-response layer.

Live state belongs to `ExecutionInstance`.

The symbolic result designation belongs to `QueryGraph.DeclaredResultBinding`.

Scalar extraction is not the default query-result shape. If a caller needs
scalar values from projected holons, that should be modeled as an explicit
materialization or command surface rather than changing ordinary query execution
into scalar-stream execution.

Path-like and explanation views are also materialized views over the
`QueryGraph`, `QueryStep` identities, relationship-channel names, execution
topology, and execution bindings. They are useful for explanation, provenance,
visualization, export, or declarative-query compatibility, but they are not
primitive runtime carriers.

## Distributed Execution

Distributed query execution in MAP emerges from nested space topology.

This section is intentionally limited in scope.

Its purpose is to state the conceptual boundary between single-space query
execution and possible future multi-space query execution, so that the
Command/Dance/Query seam can be landed cleanly now.

It does not attempt to fully specify the runtime coordination machinery for
multi-space execution. The current exploratory home for that design work is:

- [dist-query-concept.md](/Users/stevemelville/dev/map-dev-docs/docs/core/map-queries/dist-query-concept.md)

A `HolonSpace` is not merely another data object. It is also:

- a social boundary
- a trust boundary
- a storage boundary
- an execution boundary
- a Holochain app/DHT boundary

That means MAP's social topology and execution topology are intentionally
aligned. Queries follow belonging relationships and may cross from one
execution domain into another when the query reaches another space.

### Coordinator And Local Executor

This document is about execution of an already-formed `QueryGraph`, not about
query-graph generation.

So the important distributed-runtime distinction is:

- a coordinating host, which owns cross-space orchestration
- a local executor, which evaluates query steps inside one `HolonSpace` / hApp

The local executor always runs within exactly one space-scoped execution
context.

An individual step execution never straddles multiple hApps.

If work must continue in several spaces, that is not one distributed step. It
is a coordination event in which the host creates one delegated execution per
participating space.

The exact mechanics of that coordination event are not yet specified in this
document.

### Focal Space And Query Horizon

The focal space is the place from which a query is authorized, interpreted, and
presented.

The query horizon is the permission-filtered set of spaces that may participate
in answering the query.

These are not the same thing.

For example, a query may originate from Frank's I-Space while its query horizon
includes multiple spaces Frank shares with Mary. The focal space determines the
standpoint and authority. The query horizon determines where execution may fan
out.

### HolonSpace As Execution Boundary

`HolonSpace` is a first-class execution boundary.

The basic rule is:

```text
Each step executes inside one current HolonSpace / hApp.

If a step produces a collection whose members are HolonSpaces,
and the next work must execute inside those spaces,
the coordinating host splits execution into one delegated branch per space.
```

This is reasonable because `HolonSpace` is infrastructure, not just ordinary
data. It marks a boundary of storage, trust, host/guest execution, and Holochain
app/DHT locality.

In v1.1 this rule does not require a new core schema type. It is host/executor
behavior over the existing `QueryGraph`, `QueryDanceRequest`,
`ExecutionInstance`, and `HolonCollection` model.

The fuller execution-coordination design for how this behavior would be
realized across spaces remains exploratory at this stage.

### Detecting Fanout

Static analysis may reveal that a step kind can produce `HolonSpace`
references, but it cannot know in advance which spaces, or how many, for a
particular execution.

Therefore fanout is fundamentally a runtime discovery.

The coordinating host detects fanout when all of the following are true at
execution time:

- a step finishes in the current space
- its output is a `HolonCollection`
- one or more members of that collection are `HolonSpace` references
- the next step or continuation requires local execution against those spaces

The signal is therefore not a separate schema object. It is the combination of:

- the current execution scope
- the actual output collection
- the next continuation to be executed

Until fanout is detected, execution is simply the ordinary walk of the
`QueryGraph` through its `QueryStep` dependencies.

When fanout is detected, the host does not invent a new algebraic structure. It
continues the same `QueryGraph` execution separately in each discovered target
space, beginning from the next eligible step and using the branch-local
bindings/context for that space.

For the near-term execution posture, that delegated continuation should be
understood as the remaining contiguous linear suffix of the current query
chain, not as an arbitrary graph fragment.

The shared engine may therefore package:

- one entry binding
- one ordered contiguous continuation segment
- one exported result binding

and return that delegation requirement to the coordinating host.

### No Mandatory Fanout Operation

v1.1 does not require a distinct `FanoutQueryStepType`.

Fanout is an execution rule, not part of the core algebra.

That keeps the query graph simpler:

- `Expand`, `Filter`, `OrderBy`, `Limit`, and related operations remain the algebra
- crossing from one space to many spaces is handled by the coordinating host
- the symbolic query graph does not need a special distributed-control node just
  to express "continue this query in each resulting space"

An explicit fanout operation could still be introduced later if MAP needs:

- user-visible control over delegation points
- explicit explain plans for distribution boundaries
- alternative merge policies as first-class query semantics

But it is not required for the v1.1 execution model.

If MAP later needs a more explicit distributed-control surface, that should be
specified in a future coordination-oriented design document rather than
prematurely hardened here.

### Delegation And Reference Resolution

MAP has two distinct cross-space retrieval mechanisms.

Delegated execution happens when already-executing query work discovers that
continuation must occur in one or more other spaces. For example:

```text
Expand(BelongsTo) -> [SpaceA, SpaceB, SpaceC]
then Expand(Members)
```

The host evaluates `Expand(BelongsTo)` in the current space, sees that the
result collection contains `HolonSpace` references, and then dispatches
`Expand(Members)` into each target space. This is coarse-grained federation:
move the query toward the data.

Resolution-driven distribution happens when ordinary execution encounters
unresolved references. A `HolonCollection` contains references, not necessarily
materialized holons. Later, when code asks for state that is not already present
in a SmartReference or SmartLink, the Holon Cache Manager resolves the reference
through cache and fetch behavior. This is demand-driven retrieval: move the data
toward the query only when needed.

These mechanisms should remain separate:

- delegated execution reasons about spaces, execution domains, and query continuation
- reference resolution reasons about cache hits, cache misses, and fetches
- the coordinator should not become a cache-miss engine
- the cache manager should not become a distributed query coordinator

### Host And Guest Responsibilities

Guests execute within one space/app/DHT.

Hosts coordinate across spaces.

A guest may evaluate local query work using:

- local holons
- SmartLink values
- SmartReference property-map values
- local cache state

But a guest should not initiate external trust-channel calls. Cross-space
coordination belongs to the host, which can route dance requests, dispatch
eligible query work to other spaces, and merge results.

### Asynchronous Delegation

Delegated cross-space execution will likely require asynchronous invocation.

Once the coordinating host detects fanout, it may issue one `QueryDance`
invocation per participating space without blocking local execution on serial
round-trips.

Conceptually:

```text
for each target space S:
  invoke QueryDance asynchronously in S
  with the delegated continuation and delegated bindings
```

The host would then need to track outstanding delegated executions until they
complete, timeout, fail, or are cancelled.

The shared query engine does not itself spawn those parallel branches. It only
returns the need for delegation plus the delegated continuation. The host
adapter owns the actual asynchronous dispatch.

This document does not specify a particular Rust async shape or a particular
schema-level child-execution model.

What is normative is the responsibility split:

- local execution is single-space
- cross-space invocation is host-coordinated
- delegated invocations may eventually run concurrently
- result handling must tolerate partial completion and failure

### Expand Returns References

Relationship expansion returns a `HolonCollection`.

That collection contains references. It does not imply every referenced holon
has been materialized.

This matters for distributed execution because a collection may contain:

- local references
- external references
- references into several spaces
- references with enough embedded smart data for some operations
- references requiring later materialization

The expand step itself should not chase every link. Resolution happens only
when later work needs state that is not already available.

External reference resolution is not itself part of query execution.

This document therefore treats the responsibilities for:

- resolving external references
- fetching missing remote state
- cache hit/miss behavior
- trust-channel retrieval behavior

as out of scope for the graph-query-engine spec.

The intended design home for those responsibilities is a future Holons Cache
Manager design spec.

That document has not yet been authored, so the authoritative specification
home for external reference resolution is currently TBD.

Until then, [dist-query-concept.md](/Users/stevemelville/dev/map-dev-docs/docs/core/map-queries/dist-query-concept.md)
remains the active exploratory discussion of how these concerns may interact
with distributed query execution.

### Expand-Filter Pushdown

`Expand` and `Filter` often form a useful dyad.

Instead of expanding all members of a space and filtering centrally, the
coordinating host should often delegate the paired work into the target space:

```text
Expand(Members)
Filter(criteria)
```

This lets each social organism filter near storage and return only matching
references.

For example, from an I-Space:

```text
Expand(BelongsTo) -> [GroupA, GroupB, GroupC]

For each group:
  Expand(Members)
  Filter(name contains "Mary")
```

Each group evaluates locally and returns matches. The host combines, ranks,
streams, or otherwise merges the results.

This minimizes data movement while preserving space sovereignty.

The important modeling rule is that this dyad remains normalized in the query
graph:

- `Expand` is still `Expand`
- `Filter` is still `Filter`

Pushdown is an execution-time optimization over adjacent steps, not a
query-model-level `ExpandWithFilter` primitive.

The shared engine may package an adjacent `Expand -> Filter` pair as one
contiguous execution segment when the runtime can evaluate that segment near
storage.

### Result Merge Semantics

When delegated branches complete, the coordinating host would need to merge
their branch results into one `HolonCollection` for the downstream
continuation.

Here "merge" should be understood carefully.

The default distributed merge is not implicit duplicate elimination. It is
combination of branch collections into one logical result collection.

So for design purposes in v1.1:

- branch results are combined into one `HolonCollection`
- duplicate elimination is performed only by an explicit `Distinct` step
- ordering across asynchronous branches is not guaranteed unless an explicit
  later `OrderBy` step establishes it

In that sense, earlier uses of the word "union" in this document should be read
as "combined result set" rather than "mathematical set union with automatic
deduplication."

### Natural Parallelism

Nested belonging provides natural partitioning and parallelism.

If a person belongs to ten spaces, a query over those spaces can become ten
parallel subqueries. If they belong to many more spaces, the same rule still
applies, with later optimizations for prioritization, streaming, batching,
backpressure, ranking, and caching.

The foundational model does not change as these optimizations are added.

### Relationship To Recursive QueryGraph Execution

The older v1.0 narrative leaned heavily on `QueryGraphStepType` and nested query
graphs as the central mechanism for distributed execution and graph rewriting.

v1.1 deliberately steps back from making that recursive-subgraph mechanism
normative in the core schema.

The important v1.1 point is more precise:

- a query dance is invoked against some affording holon whose type affords that dance
- query execution is therefore naturally space-scoped
- `HolonCollection` remains the runtime substrate
- `ExecutionInstance` carries run-specific state
- each step execution is local to one `HolonSpace` / hApp
- fanout is runtime-discovered when step results reveal downstream space branches
- hosts coordinate across spaces; guests execute locally within a space
- delegated distributed execution and demand-driven reference resolution remain separate

Distributed rewriting, grouped subgraphs, and recursive query-graph execution
remain valid execution strategies. They are no longer the schema foundation of
the core query-engine design.

Those strategies are currently better understood as part of the exploratory
multi-space design space than as settled v1.1 execution machinery.

### Distributed Design Rules

The distributed execution model follows these rules:

- focal space is not the same thing as search scope
- `HolonSpace` is a distributed execution boundary
- each concrete step execution is single-space
- fanout is detected at runtime from actual step results
- v1.1 does not require an explicit fanout operation
- guests execute locally
- hosts coordinate across spaces
- delegated query-dance invocations may run concurrently
- branch results are merged into one `HolonCollection`
- deduplication requires an explicit `Distinct`
- `Expand` returns references, not materialized holons
- SmartReferences resolve state only when needed
- expand-filter dyads should be delegated when the target space can evaluate them
- predicates should move near storage whenever possible
- distributed delegation and cache resolution remain distinct
- batching, pulsing, prefetching, streaming, and prioritization are optimizations, not semantic requirements

These rules are included to keep the current query design from painting later
multi-space work into a corner. They should not be read as a complete runtime
specification for distributed query execution.

## Rust Intent Layer

The Rust layer should use thin typed wrappers around `HolonReference` so callers
can express intent without mirroring holon state into Rust structs.

Examples:

- `QueryGraphHolon`
- `QueryStepHolon`
- `QueryBindingHolon`
- `ExecutionInstanceHolon`
- `ExecutionBindingHolon`
- `HolonCollectionReference`

The important pattern is:

- keep the wrapped `HolonReference` private
- provide typed read-through accessor methods
- use helper patterns similar to `accessor_helpers.rs`
- use collection-oriented helpers like `single_member()`,
  `optional_single_member()`, and `members()` where callers expect a collection

The detailed wrapper sketch lives in the companion DSL document.

## Suggested Core-Schema Source Changes

The design above is grounded in the currently generated schema names, but it
also implies several source-of-truth Airtable refinements that are not yet
reflected in generated schema JSON.

The most important ones are:

- `DanceType.HolonType` should use `DanceInput -> HolonType` instead of
  `InputParameters -> Projection.HolonType`
- `DanceInvocation.HolonType` should use `AffordingHolon -> HolonType` instead
  of `Target -> HolonType`
- the full query schema described here should be introduced as an explicit
  schema-layer model

Those changes should be made in the Airtable source and then regenerated into
schema JSON. This document does not propose editing generated JSON directly.

## Summary

The v1.1 foundation is:

```text
Dance.CommandType
  payload -> DanceInvocation

DanceInvocation
  invokes -> QueryDance
  request -> QueryDanceRequest

QueryDanceRequest
  query_graph      -> QueryGraph
  initial_bindings -> ExecutionBinding*

QueryGraph
  query_steps             -> QueryStep*
  declared_input_bindings -> QueryBinding*
  declared_result_binding -> QueryBinding

ExecutionInstance
  executes_request   -> QueryDanceRequest
  execution_bindings -> ExecutionBinding*
  execution_result   -> HolonCollection?

QueryDanceResponse
  response_body -> HolonCollection
```

This gives MAP:

- a sharper Command/Dance/Query seam
- a symbolic query plan separated cleanly from runtime execution state
- `HolonCollection` as the stable runtime query substrate
- a smaller and more legible `QueryStep`
- structural parameter modeling for filter, order-by, and project
- a shared query engine core with host-only distributed orchestration around it
- normalized query steps with execution-time segment fusion where beneficial
- room for typed Rust wrappers that convey intent cleanly

That is the intended v1.1 design center.
