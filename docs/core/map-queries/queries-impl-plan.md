# Query / Navigation Implementation Plan (v2.4)

## Purpose

This document turns the MAP query/navigation design specs into a practical delivery sequence.

The current design pivot is:

```text
Navigation operation Dances
  -> HolonCollection-centered execution
  -> optional ExecutionPlan holon capture
  -> optional ExecutionInstance-backed interactive orchestration
  -> optional saved-plan execution
  -> future DeclarativeQuery compilation
```

`Query` is not a required runtime object for the current implementation target.
Concrete navigation behavior should be implemented as Dances afforded by MAP types, especially `HolonCollection`.

This is an implementation plan, not the design authority. The design authority lives in:

- [query-algebra/query-algebra-design-spec.md](query-algebra/query-algebra-design-spec.md)
- [index.md](index.md)
- [query-arch.md](query-arch.md)
- [simple-algebra-binding-model.md](simple-algebra-binding-model.md)
- [navigation-algebra.md](navigation-algebra.md)
- [exec-time-type-resolution.md](exec-time-type-resolution.md)
- [distributed-query-semantics.md](distributed-query-semantics.md)
- [query-planner-algebra.md](query-planner-algebra.md)

---

## Current Conclusion

The query design detour was needed to settle the shared data-type question before DAHN work hardened around the wrong result shapes.

That question is now settled enough for DAHN:

- `HolonReference` is the primary singular holon-backed handle.
- `HolonCollection` is the primary plural holon-backed carrier.
- `BaseValue`, `Row`, and `RowSet` remain materialized projection/result types.
- `ExecutionPlan` owns symbolic execution structure; `ExecutionInstance` owns runtime execution state.
- `RowSet`, paths, pair views, partitioned views, and graph-like outputs are concrete materialized result types, not foundational execution carriers.
- `BoundHolonCollection` is not required unless a future lifecycle or contract need emerges that `HolonCollection` plus surrounding plan/execution/result structure cannot represent.
- OpenCypher/GQL compatibility remains possible through later `DeclarativeQuery -> ExecutionPlan` holon compilation and concrete compatibility-oriented result types.

This means Query PRs are no longer on the critical path to initial DAHN delivery merely to settle shared operand types.
DAHN can proceed against Commands, Dance invocation, descriptor affordances, `HolonReference`, `HolonCollection`, and projection-boundary result types.

---

## Delivered History

PRO1 and PRO2 are already delivered. Do not rewrite their history.

### Query PRO1 - Shared Operand Family Foundation

Delivered intent:

- define the shared operand family around `Value` / `BaseValue`, `Row`, and `RowSet`
- provide common projection/result vocabulary across query, command, SDK, dance, and related surfaces

Current interpretation:

- `BaseValue`, `Row`, and `RowSet` remain useful shared projection/result concepts
- they should not be treated as the foundational navigation/query execution substrate
- any implementation or documentation that made `RowSet` central to internal execution should be corrected in the next alignment pass

### Query PRO2 - Query Envelope And Contract Stabilization

Delivered intent:

- prepare query request/result envelopes on top of the shared operand family
- stabilize the client-to-host-to-substrate query contract path

Current interpretation:

- the envelope work should not force a reified `Query` object or standalone new-world query request path
- navigation operation execution should flow through Dance invocation
- Commands keep `MapIpcRequest` as a Commands-only ingress envelope
- Dances keep their own invocation/outcome envelopes
- plan/session/declarative layers should introduce concrete envelopes only when those layers are implemented

---

## PR Chunk Decomposition

This implementation plan is decomposed into bite-size PR chunks for delivery tracking.

Planning rules:

- Delivered chunks are fixed history. Do not rename, re-score, or reinterpret their delivered scope as if it had not happened.
- New chunks reflect the current design: navigation behavior is descriptor-afforded Dance behavior over `HolonCollection`.
- `PRO` chunks are contract, ABI, envelope, or lifecycle stabilization work.
- `PRS` chunks are descriptor-dependent semantic, structural, dispatch, or execution behavior.
- Dev Points are planning estimates for new or newly recognized work. Delivered PRO1/PRO2 should keep whatever actual values are already recorded in the delivery tracker.

| Chunk                                                                        | Track              | Status            |     Dev Points | DAHN Critical Path | Purpose                                                                                                                                                                                                                                    |
|------------------------------------------------------------------------------|--------------------|-------------------|---------------:|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Query PRO1 - Shared Operand Family Foundation                                | PRO                | Delivered / fixed | tracker actual | Done               | Established shared projection/result vocabulary around `BaseValue`, `Row`, and `RowSet`.                                                                                                                                                   |
| Query PRO2 - Query Envelope And Contract Stabilization                       | PRO                | Delivered / fixed | tracker actual | Done               | Stabilized the existing query contract path enough to preserve compatibility and avoid freezing legacy shapes as the only long-term surface.                                                                                               |
| Query DS1 - Query Design Realignment Sprint                                  | Design / Discovery | Delivered / fixed |              8 | Indirect           | Rebased the query/navigation design around `HolonCollection`, navigation operation Dances, `ExecutionPlan` holons, and projection-boundary materialized result types.                                                                      |
| Query PRO3 - Query Contract Realignment Closeout                             | PRO                | Done              |              2 | Done               | Close out PRO1/PRO2 fallout: no standalone `NavigationQueryRequest` requirement, no foundational `BoundHolonCollection`, no row-stream execution assumption, and no reified `Query` object for the initial route.                          |
| Query PRS2 - SeedHolons And Descriptor-Validated Expand Over HolonCollection | PRS                | Next              |              8 | Yes                | Implement the first holon-native navigation behavior: focal-space / execution-domain seeding and named-channel expansion returning `HolonCollection`, with descriptor-backed relationship-channel legality validation built into `Expand`. |
| Query PRS3 - Filter And Projection Boundary Subset                           | PRS                | Planned           |              5 | Yes                | Add an initial descriptor-aware predicate subset and projection boundary behavior without making `RowSet` the execution carrier.                                                                                                           |
| Query PRS4 - Ordering, Distinct, And Pagination                              | PRS                | Planned           |              3 | Yes                | Add deterministic host-owned `OrderBy`, `Distinct`, `Skip`, and `Limit` semantics over `HolonCollection`.                                                                                                                                  |
| Query PRS5 - Navigation Operation Outcome And Diagnostics                    | PRO / PRS          | Planned           |              3 | Likely             | Stabilize the result/outcome shape for navigation operation Dances, including output binding, diagnostics, and references to result state without freezing the retired `NavigationQueryResult` name.                                       |
| Query PRO4 - ExecutionPlan HolonType Scaffold                                | PRO                | Later             |              5 | No                 | Introduce the `ExecutionPlan` HolonType, plan holons, operation structure, and typed references/facades without making saved-plan execution mandatory for direct navigation.                                                               |
| Query PRS6 - Interactive Execution Orchestration                             | PRS                | Later             |              5 | No                 | Add host-level interactive orchestration that appends operations to an `ExecutionPlan`, executes them through an `ExecutionInstance`, and maintains live execution bindings without becoming the normative runtime state model.            |
| Query PRS7 - ExecutionPlan Execute Dance                                     | PRS                | Later             |              5 | No                 | Execute saved or constructed `ExecutionPlan` holons by creating or using an `ExecutionInstance`, with `HolonCollection`-centered results and concrete materialized result types where required.                                            |
| Query PRS8 - Distributed Seed And Expand Semantics                           | PRS                | Future            |              5 | No                 | Apply focal-space, execution-domain, Home Space, TrustChannel, and rebinding rules to distributed seed and expansion.                                                                                                                      |
| Query PRS9 - DeclarativeQuery Compilation Foundation                         | PRS                | Future            |              8 | No                 | Introduce a future `DeclarativeQuery` route that parses supported OpenCypher/GQL subsets into `ExecutionPlan` holons.                                                                                                                      |

The important correction is that the former large "Query PRO3 navigation substrate" is now split:

- a small **Query PRO3** closeout chunk for contract realignment
- several **Query PRS** chunks for descriptor-backed navigation behavior
- later plan/execution-orchestration chunks for replayable execution

---

## Implementation Layers

Implement the navigation/query capability in layers.

### Layer 1 - Navigation Operation Dances

Goal:

Implement concrete navigation behavior as Dances afforded by MAP types.

Primary affordance target:

- `HolonCollection`

Initial Dances:

- `Expand`
- `Filter`
- `OrderBy`
- `Skip`
- `Limit`
- `Distinct`
- `Project`

Seed operations are separate because they create the initial collection.
They may be afforded by:

- `HolonSpace`
- focal-space context
- execution-domain context
- another host-defined navigation scope

This layer should be enough for DAHN to navigate and refine holon-backed results without waiting for saved-plan infrastructure.

Primary PR chunks:

- Query PRS2
- Query PRS3
- Query PRS4
- Query PRS5, if DAHN needs stable operation result holons or diagnostics before the session layer

Exit criteria:

- navigation operation Dances consume and produce `HolonCollection` where applicable
- `Expand` follows named relationship channels
- `Filter` can evaluate an initial descriptor-aware predicate subset
- ordering and pagination are host-owned
- operation results do not require `BoundHolonCollection`, `RowSet`, `Path`, or a graph result object as foundational carriers
- Dance invocation remains distinct from Commands ingress

### Layer 2 - ExecutionPlan And ExecutionInstance-Backed Interactive Orchestration

Goal:

Introduce replayable operation capture and immediate interactive execution without making `ExecutionPlan` the executor of every operation or the owner of runtime state.

Objects:

- `ExecutionPlan` HolonType and plan holons
- `PlanOperation`
- `ExecutionInstance`
- optional host-level interactive orchestration object

Dance:

- host-owned interactive apply-operation affordance backed by `ExecutionPlan` and `ExecutionInstance`

Primary PR chunks:

- Query PRO4
- Query PRS6

Interactive apply-operation should:

1. accept a navigation operation intent
2. append a deterministic operation to the related `ExecutionPlan` holon
3. execute immediately when requested
4. create or reuse an `ExecutionInstance`
5. resolve inputs through that `ExecutionInstance`'s bindings
6. store output bindings, runtime values, diagnostics, and execution status on the `ExecutionInstance`

Exit criteria:

- `ExecutionPlan` remains the symbolic execution artifact
- `ExecutionInstance` owns live execution bindings and runtime state
- any interactive session object is host-level orchestration around `ExecutionPlan` plus `ExecutionInstance`, not the normative runtime state carrier
- operation append and immediate execution are coordinated by the host-level interactive affordance
- individual operation Dances do not each mutate plans as incidental side effects

### Layer 3 - ExecutionPlan Execute Dance

Goal:

Replay previously defined plans.

Dance:

- `ExecutionPlan.Execute`

Primary PR chunk:

- Query PRS7

Exit criteria:

- a saved or constructed `ExecutionPlan` holon can execute against an explicit transaction, snapshot, or session context
- execution resolves plan variables through an `ExecutionInstance`
- results remain `HolonCollection`-centered until a projection boundary requires concrete materialized result types
- replay preserves descriptor-backed validation and deterministic ordering rules

### Layer 4 - DeclarativeQuery

Goal:

Add declarative query support after imperative navigation is stable.

Object:

- `DeclarativeQuery`

Primary PR chunk:

- Query PRS9

The future route is:

```text
DeclarativeQuery(OpenCypher/GQL text)
  -> parse
  -> descriptor-aware semantic validation
  -> plan/optimize
  -> ExecutionPlan holon
  -> Execute
```

Exit criteria:

- supported OpenCypher/GQL subsets compile into MAP `ExecutionPlan` holons
- row-observable, path-observable, optional, grouped, or duplicate-preserving semantics are produced through concrete materialized result types and compatibility-oriented result surfaces
- declarative support does not replace the HolonCollection-centered runtime model

---

## Descriptor Validation Track

Descriptor-backed validation remains important, but it can progress alongside the layers above.

Primary PR chunks:

- Query PRS2 for `Expand` relationship-channel legality
- Query PRS3 for predicate and projection value semantics
- Query PRS8 for distributed descriptor-consistent execution

### Structural Validation

`Expand` should validate relationship-channel legality through descriptor-backed effective relationship lookup.

Requirements:

- outgoing expansion validates that the relationship channel exists for the source holon type
- incoming expansion preserves declared vs inverse relationship meaning
- inheritance flattening comes from descriptor-backed structure
- relationship-channel validation does not imply property-bearing edge instances

### Predicate And Operator Alignment

`Filter` and `Project` should use descriptor-owned value/operator semantics where typed values are involved.

Requirements:

- property references resolve through descriptor-backed structure
- operator compatibility is owned by descriptors/value semantics
- navigation operation Dances execute predicates without becoming the semantic owner of value types

---

## PRO1 / PRO2 Alignment Work

Query PRO3 is the delivered closeout chunk for this alignment pass.

It should:

- keep `BaseValue`, `Row`, and `RowSet` as projection/result vocabulary
- remove or demote any assumption that internal execution is row-oriented
- remove or defer `BoundHolonCollection` unless a concrete lifecycle or contract need is identified
- stop treating standalone `NavigationQueryRequest` / `NavigationQuerySpec` as required PRO3 runtime objects
- rename or defer query-specific result names such as `NavigationQueryResult` if the result is really a navigation operation or dance outcome result holon
- align execution-state language and contracts with `ExecutionInstance` as the normative runtime state owner
- preserve legacy query surfaces through adapters where needed
- keep old-world `Node`, `NodeCollection`, `QueryPathMap`, and `QueryExpression` compatibility until an explicit migration removes them

---

## DAHN Critical Path

Initial DAHN delivery should not wait for:

- `ExecutionPlan` HolonType and plan holons
- host-level interactive orchestration
- `ExecutionPlan.Execute`
- `DeclarativeQuery`
- OpenCypher/GQL parsing
- `BoundHolonCollection`
- foundational `RowSet` or path execution

Initial DAHN delivery does need:

- stable Commands ingress
- Dance invocation through Commands
- descriptor-afforded behavior discovery
- `HolonReference`
- `HolonCollection`
- scalar/property projection through `BaseValue` where needed
- navigation operation Dances that let DAHN expand, filter, order, and page holon-backed results

---

## Guardrails

- Do not make `RowSet` the default execution carrier.
- Do not introduce `BoundHolonCollection` unless it has a specific lifecycle or contract that `HolonCollection` cannot satisfy.
- Do not model MAP relationships as property-bearing edge instances.
- Do not put OpenCypher/GQL semantics into the initial navigation operation Dances.
- Do not make Commands, SDK, or hApp ingress layers the semantic home of navigation behavior.
- Do not introduce a generic `Query` runtime object unless a future design identifies a concrete lifecycle for it.
- Keep Commands and Dances envelopes distinct from `ExecutionPlan`, `ExecutionInstance`, optional host-level interactive orchestration, and `DeclarativeQuery` lifecycles.
- Keep descriptor-backed structural validation separate from the runtime carrier model.
- Keep legacy query/navigation behavior working until an explicit migration step replaces it.

---

## Immediate Next Step

The immediate implementation path should return to the DAHN mainline with the data-type question settled.

If a query/navigation issue is generated next, continue with the first behavior-bearing PRS work:

1. **Query PRS2 - SeedHolons And Descriptor-Validated Expand Over HolonCollection**

The first behavior-bearing implementation slice should be:

```text
Navigation Operation Dances over HolonCollection
```

That is PRS work, not a full query substrate, not a standalone new-world query envelope, and not an OpenCypher-compatible execution engine.
