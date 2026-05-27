# Query Design Pivot: Journey and Findings

This is not so much a discussion as a journal entry recording the motivation and result of a deep-dive I did into MAP Query Design.

## Summary

During the DAHN-oriented design work, we paused to clarify whether Query design would materially affect the shared operand/result types exposed through MAP Commands, the MAP SDK, and the initial DAHN implementation.

The investigation began with the assumption that Queries might require special algebraic data types such as `BoundHolonCollection`, `BoundRelationshipCollection`, `Row`, `RowSet`, and `Path`, especially because of the longer-term OpenCypher target.

The current conclusion is different:

> Queries do not appear to require a special foundational runtime category or special query-specific operand types.

Instead:

> Query-like behavior is best understood as ordinary Dance behavior afforded by HolonTypes, with `HolonCollection` serving as the primary shared data type.

This substantially reduces the likelihood that Query PRs are on the critical path to DAHN delivery.

## Context

The larger implementation plan is a description-driven implementation path toward the initial DAHN.

The dependency chain is currently understood as:

- DAHN depends on the TypeScript API exposed through the MAP SDK.
- The MAP SDK wraps MAP Commands.
- MAP Commands include:
    - built-in commands afforded by MAP Core,
    - a Dance command that allows any Dance to be invoked through the Command surface.
- Earlier design work assumed Queries were a special kind of Dance.
- The Query deep-dive was motivated by the risk that query-specific result and operand types might need to be shared across Commands, Dances, SDK APIs, and DAHN.

The key architectural question was therefore:

> Do Queries introduce foundational operand/result types that must be stabilized before DAHN work proceeds?

## Initial Assumption

The earlier assumption was that Query support, especially OpenCypher support, might require a distinct query algebra with dedicated data types.

Candidate query-specific types included:

- `BoundHolonCollection`
- `BoundRelationshipCollection`
- `Row`
- `RowSet`
- `Path`
- query-specific projection/result structures
- interactive navigation session structures

This suggested that Query design might be on the DAHN critical path because the SDK operand surface could be affected by these types.

## Deeper Question

The design exploration then raised a more fundamental question:

> Is "Query" even a thing in the MAP ontology?

This reframed the inquiry.

Rather than asking what HolonType grounds Queries, we asked whether Query is a first-class MAP concept at all.

The emerging answer is:

> "Query" may be a human-facing label for a family of navigation-oriented Dances, not a foundational runtime category.

## Key Decomposition

The deeper decomposition separates several concerns that were previously bundled together under "Query":

| Concern | Current Interpretation |
|---|---|
| OpenCypher text | A declarative serialization or authoring language |
| Query operations such as Seed, Expand, Filter, Project | Dances afforded by relevant HolonTypes |
| ExecutionPlan | A durable executable choreography, likely represented as a Holon later |
| ExecutePlan | A Dance afforded by an ExecutionPlan Holon |
| InteractiveNavigationSession | A later stateful authoring/session layer over ExecutionPlan |
| Query | A convenient human-facing term, not necessarily a primitive |

## Core Insight

The central insight is:

> Query Operations are not special because they are "query" operations. They are ordinary Dances that operate over collections.

Examples:

- `Seed` produces a collection.
- `Expand` transforms a collection by traversing relationships.
- `Filter` narrows a collection.
- `Project` shapes or extracts from a collection.
- `Aggregate` summarizes a collection.
- `Join` combines collections.

This makes `HolonCollection` the natural primary operand.

## HolonCollection as the Primary Data Type

The most important design pivot is that `HolonCollection` appears to be the correct foundational shared data type.

A navigation-oriented operation can be understood as a transformation over collections:

    HolonCollection -> HolonCollection

or, in some cases:

    HolonCollection -> scalar/result value

or:

    HolonCollection x HolonCollection -> HolonCollection

This substantially reduces the need for query-specific foundational types.

## What Affords QueryOperation Dances?

The current hypothesis is:

> QueryOperation Dances are afforded by `HolonCollection` or closely related collection-oriented HolonTypes.

This is a cleaner grounding than saying they are afforded by a special Query type.

In this framing:

- HolonSpace affords visibility, scope, and membrane-constrained access.
- HolonCollection affords navigation and collection transformation operations.
- RelationshipTypes describe traversal semantics.
- ExecutionPlan choreographs operations.
- Dance invokes behavior.
- Command exposes invocation through the SDK-facing command surface.

## Revised Architectural Stack

A more stable stack now appears to be:

| Layer | Role |
|---|---|
| Holon | Primary semantic entity |
| HolonCollection | Primary navigation operand and result carrier |
| RelationshipMap | Relationship-name-indexed exposure of target collections |
| Dance | Executable behavior |
| Command | Invocation surface |
| QueryOperation / NavigationOperation | Collection-oriented Dance |
| ExecutionPlan | Later durable choreography graph |
| InteractiveNavigationSession | Later stateful plan-authoring layer |
| OpenCypher | Later declarative authoring syntax lowered into ExecutionPlan |

## Consequence for OpenCypher

OpenCypher no longer needs to define the foundational runtime shape.

Instead:

> OpenCypher can be treated as one possible authoring syntax that is parsed, normalized, and optimized into an ExecutionPlan.

Possible future flow:

    OpenCypher text
      -> ParseOpenCypher Dance
      -> Normalize / Type Inference / Planning Dances
      -> ExecutionPlan Holon
      -> ExecutePlan Dance
      -> HolonCollection or other result

This lets OpenCypher remain an important target without forcing Cypher-specific abstractions into the early SDK surface.

## Consequence for ExecutionPlan

ExecutionPlan becomes a later layer rather than a DAHN-blocking primitive.

An ExecutionPlan may eventually represent a choreography such as:

    Seed
      -> Expand
      -> Filter
      -> Project

But the early shared type system does not need to expose the full plan algebra.

ExecutionPlan can layer on top of HolonCollection after the DAHN-critical command and SDK surfaces are stable.

## Consequence for InteractiveNavigationSession

InteractiveNavigationSession is also no longer foundational.

It can be understood as a later stateful authoring or plan-building layer that sits above ExecutionPlan.

Possible future layering:

    HolonCollection
      -> ExecutionPlan
      -> InteractiveNavigationSession
      -> OpenCypher / visual navigation / AI-assisted plan construction

This allows interactive navigation to evolve incrementally without blocking the first DAHN implementation.

## Types That May Be Deferred

The following types should not currently be treated as required foundational SDK operand types:

- `BoundHolonCollection`
- `BoundRelationshipCollection`
- `Row`
- `RowSet`
- `Path`
- OpenCypher-specific result structures
- Interactive navigation session state
- Query-specific algebra structures

These may still become useful later as planner internals, projection formats, UI presentation types, or OpenCypher compatibility layers.

But they do not appear necessary as core shared operand types for the initial DAHN path.

## Types That Remain Central

The types that remain central are:

- `Holon`
- `HolonCollection`
- `RelationshipMap`
- Dance request/response structures
- Command request/response structures
- shared MAP operand/result envelopes used by Commands and Dances

The most important design constraint is that these types should remain general enough to support later ExecutionPlan and OpenCypher layers without prematurely importing query-specific assumptions.

## Impact on DAHN Critical Path

The main practical outcome is:

> Query PRs may no longer be on the critical path to DAHN delivery.

The reason is that the original risk has been substantially reduced.

Originally, the concern was:

> If Query requires special operand/result types, then DAHN-facing SDK types might need to wait for Query design to stabilize.

The current finding is:

> Query-like behavior can be grounded in ordinary Dances over HolonCollection, so the shared operand type question is sufficiently settled for DAHN to proceed.

Therefore, the DAHN path can likely continue through:

    MAP Core Commands
      -> Dance invocation through Command
      -> TypeScript SDK stabilization
      -> DAHN implementation

while Query design proceeds in parallel or later through:

    map-queries design spec updates
      -> query-impl-plan update
      -> ExecutionPlan design
      -> InteractiveNavigationSession design
      -> OpenCypher lowering

## Required Documentation Updates

The next step is to capture this pivot explicitly in the MAP Query design materials.

Suggested updates:

- Update `map-queries` design specs to explain that Query is not currently treated as a foundational runtime primitive.
- Clarify that QueryOperation-like behavior is modeled as ordinary Dances afforded by HolonTypes, especially collection-oriented types such as `HolonCollection`.
- Clarify that `HolonCollection` is the primary shared navigation operand.
- Reclassify `Row`, `RowSet`, `Path`, and bound collection structures as deferred or non-foundational.
- Describe ExecutionPlan as a later durable choreography layer.
- Describe InteractiveNavigationSession as a later stateful layer over ExecutionPlan.
- Describe OpenCypher as a future authoring language that lowers into ExecutionPlan, not as the source of the core operand model.
- Update `query-impl-plan` to remove or reduce Query PRs from the DAHN critical path unless they are needed for some other immediate reason.

## Proposed Design Principle

A useful design principle to capture:

> Do not introduce a special Query abstraction unless and until a concrete need emerges that cannot be satisfied by Dances over HolonCollection and later ExecutionPlan choreography.

A stronger version:

> In MAP Core, navigation is collection-oriented Dance behavior. "Query" is a language-level or user-facing interpretation, not a required foundational runtime category.

## Working Decision

For current planning purposes:

- Treat `HolonCollection` as the primary shared operand/result type for navigation-oriented behavior.
- Treat QueryOperation concepts such as `Seed`, `Expand`, `Filter`, and `Project` as Dances.
- Treat ExecutionPlan as a later HolonType that can choreograph those Dances.
- Treat OpenCypher as a later declarative source language that can compile into ExecutionPlan.
- Do not block DAHN implementation on Query PRs unless a specific DAHN requirement reintroduces a concrete dependency.

## Open Questions

The following questions remain open but are no longer DAHN-blocking:

- Should `HolonCollection` itself afford all core navigation operations, or should more specific collection HolonTypes afford specialized operations?
- How should relationship traversal semantics be declared on RelationshipTypes?
- What is the minimal shape of ExecutionPlan when introduced?
- Are ExecutionPlan steps Holons, embedded structures, or both?
- How should OpenCypher paths be represented when OpenCypher compatibility requires path-shaped results?
- Should `Row` and `RowSet` exist only as projection/presentation structures?
- How should interactive navigation sessions persist partially constructed plans?
- How should membrane visibility and promise constraints be represented inside future ExecutionPlans?

## Bottom Line

The Query deep-dive appears to have achieved its purpose.

It clarified that Query design does not need to force special algebraic result types into the initial shared MAP operand model.

The foundational pivot is:

> From query-specific algebra types to collection-oriented Dance behavior.

That means the DAHN-critical type surface can remain smaller, cleaner, and more MAP-native.