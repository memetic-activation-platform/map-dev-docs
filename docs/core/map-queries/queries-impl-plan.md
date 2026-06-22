# Query / Navigation Implementation Plan (v2.6)

## Purpose

This document turns the MAP query/navigation design specs into a practical delivery sequence.

The current design pivot is:

```text
Navigation operation Dances
  -> HolonCollection-centered execution
  -> optional QueryStep / QueryGraph holon capture
  -> optional ExecutionInstance-backed orchestration and replay
  -> optional saved-query replay
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
- `QueryGraph` owns symbolic query structure; `ExecutionInstance` owns runtime execution state.
- `RowSet`, paths, pair views, partitioned views, and graph-like outputs are concrete materialized result types, not foundational execution carriers.
- `BoundHolonCollection` is not required unless a future lifecycle or contract need emerges that `HolonCollection` plus surrounding plan/execution/result structure cannot represent.
- OpenCypher/GQL compatibility remains possible through later `DeclarativeQuery -> QueryGraph` holon compilation and concrete compatibility-oriented result types.

This means Query PRs are no longer on the critical path to initial DAHN delivery merely to settle shared operand types.
DAHN can proceed against Commands, Dance invocation, descriptor affordances, `HolonReference`, `HolonCollection`, and projection-boundary result types.

---

## Delivered History

PRO1 and PRO2 are already delivered. Do not rewrite their history.

Completed chunks may still imply follow-on alignment or rework work. That
rework should be tracked in new chunks or explicit follow-on notes rather than
pretending the completed chunk never happened.

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

## Delivery Tracker Alignment

The delivery tracker currently records these query chunks as already completed:

- Query PRO1 - Shared Operand Family Foundation
- Query PRO2 - Query Envelope And Contract Stabilization
- Query DS1 - Query Design Realignment Sprint
- Query PRO3 - Legacy Query Contract Removal And Navigation Algebra Reset

Those completions are real history and should remain recorded as such.

However, some of that completed work was done before the current v1.1
command/dance/query realignment fully settled. That means some completed work
may now require targeted follow-on rework or replacement slices.

The important rule is:

- do not erase or rename completed history
- do note when a completed chunk likely needs follow-on alignment work
- do create new implementation slices for that rework rather than silently
  pretending the old chunk is still perfectly aligned

The delivery tracker also records:

- Query PRS1 - Parallel Descriptor-Backed Structural Resolution = Abandoned

`PRS1` should be treated as abandoned history, not as latent planned work.
Do not revive it under the same name. Any remaining useful intent from that
abandoned slice should be captured by newer chunks such as `PRS2`, `PRS3`,
`PRO4`, or later descriptor/execution work.

---

## PR Chunk Decomposition

This implementation plan is decomposed into bite-size PR chunks for delivery tracking.

Planning rules:

- Delivered chunks are fixed history. Do not rename, re-score, or reinterpret their delivered scope as if it had not happened.
- Completed chunks may require follow-on rework; track that rework explicitly rather than reopening or rewriting the completed chunk's history.
- New chunks reflect the current design: navigation behavior is descriptor-afforded Dance behavior over `HolonCollection`.
- `PRO` chunks are contract, ABI, envelope, or lifecycle stabilization work.
- `PRS` chunks are descriptor-dependent semantic, structural, dispatch, or execution behavior.
- Dev Points are planning estimates for new or newly recognized work. Delivered PRO1/PRO2 should keep whatever actual values are already recorded in the delivery tracker.

| Chunk                                                                        | Track              | Status            |     Dev Points | DAHN Critical Path | Purpose                                                                                                                                                                                                                                    |
|------------------------------------------------------------------------------|--------------------|-------------------|---------------:|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Query PRO1 - Shared Operand Family Foundation                                | PRO                | Delivered / fixed | tracker actual | Done               | Established shared projection/result vocabulary around `BaseValue`, `Row`, and `RowSet`. May need follow-on alignment where old row-oriented assumptions leaked too far inward.                                                            |
| Query PRO2 - Query Envelope And Contract Stabilization                       | PRO                | Delivered / fixed | tracker actual | Done               | Stabilized the existing query contract path enough to preserve compatibility and avoid freezing legacy shapes as the only long-term surface. May need follow-on alignment where old query-envelope assumptions no longer match Dance-first execution. |
| Query DS1 - Query Design Realignment Sprint                                  | Design / Discovery | Delivered / fixed |              8 | Indirect           | Rebased the query/navigation design around `HolonCollection`, navigation operation Dances, symbolic query-structure holons, and projection-boundary materialized result types. This is completed design history but some conclusions have continued to sharpen afterward. |
| Query PRO3 - Query Contract Realignment Closeout                             | PRO                | Done              |              5 | Done               | Close out PRO1/PRO2 fallout: no standalone `NavigationQueryRequest` requirement, no foundational `BoundHolonCollection`, no row-stream execution assumption, and no reified `Query` object for the initial route. Some outputs may need targeted rework to match the now-sharper v1.1 command/dance/query seam. |
| Query PRS1 - Parallel Descriptor-Backed Structural Resolution                | PRS                | Abandoned         | tracker actual | No                 | Historical abandoned slice. Do not revive under this ID. Any surviving intent should be redistributed into the newer descriptor-backed navigation and query-structure chunks.                                                              |
| Query PRS2 - SeedHolons And Descriptor-Validated Expand Over HolonCollection | PRS                | Planned           |              8 | Yes                | Implement the first holon-native navigation behavior: focal-space / execution-domain seeding and named-channel expansion returning `HolonCollection`, with descriptor-backed relationship-channel legality validation built into `Expand`. |
| Query PRS3 - Filter And Projection Boundary Subset                           | PRS                | Planned           |              5 | Yes                | Add an initial descriptor-aware predicate subset and projection boundary behavior without making `RowSet` the execution carrier.                                                                                                           |
| Query PRS4 - Ordering, Distinct, And Pagination                              | PRS                | Planned           |              3 | Yes                | Add deterministic host-owned `OrderBy`, `Distinct`, `Skip`, and `Limit` semantics over `HolonCollection`.                                                                                                                                  |
| Query PRS5 - Navigation Operation Outcome And Diagnostics                    | PRO / PRS          | Planned           |              3 | Likely             | Stabilize the result/outcome shape for navigation operation Dances, including output binding, diagnostics, and references to result state without freezing the retired `NavigationQueryResult` name.                                       |
| Query PRO4 - QueryStep And QueryGraph HolonType Scaffold                     | PRO                | Next              |              5 | Likely             | Introduce `QueryStep` and `QueryGraph` as the symbolic query-structure layer early, without requiring optimizer machinery or abandoning naive per-operation execution.                                                                       |
| Query PRS6 - ExecutionInstance Orchestration And QueryGraph Replay           | PRS                | Later             |              5 | No                 | Add host-level orchestration that executes `QueryGraph` structures through an `ExecutionInstance`, maintains live execution bindings, and supports replay without becoming the normative semantic owner.                                    |
| Query PRS7 - QueryGraph Execute Dance                                        | PRS                | Planned           |              5 | No                 | Execute saved or constructed `QueryGraph` holons by creating or using an `ExecutionInstance`, with `HolonCollection`-centered results and concrete materialized result types where required.                                               |
| Query PRS8 - Distributed Seed And Expand Semantics                           | PRS                | Future            |              5 | No                 | Apply focal-space, execution-domain, Home Space, TrustChannel, and rebinding rules to distributed seed and expansion.                                                                                                                      |
| Query PRS9 - DeclarativeQuery Compilation Foundation                         | PRS                | Future            |              8 | No                 | Introduce a future `DeclarativeQuery` route that parses supported OpenCypher/GQL subsets into `QueryGraph` holons.                                                                                                                         |

The important correction is that the former large "Query PRO3 navigation substrate" is now split:

- a small **Query PRO3** closeout chunk for contract realignment
- the former **PRS1** slice is explicitly abandoned and should not be revived
- several **Query PRS** chunks for descriptor-backed navigation behavior
- an earlier symbolic query-structure chunk for `QueryStep` / `QueryGraph`
- later execution-orchestration chunks for replayable execution

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

This layer should be enough for DAHN to navigate and refine holon-backed results.
Immediate execution may remain naive and stepwise in this layer, including test suites that currently rely on `GetAllHolons`-style seeding over fixture-scale data stores.

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

### Layer 2 - Early `QueryStep` / `QueryGraph` Structure

Goal:

Introduce symbolic query structure earlier without turning the initial query layer into a planner-first system.

Objects:

- `QueryStep`
- `QueryGraph`
- lightweight typed references or facades

Primary PR chunks:

- Query PRO4

This layer should:

1. define `QueryStep` as the symbolic node for one navigation operation
2. define `QueryGraph` as the graph-shaped symbolic artifact relating those steps
3. allow an immediate Dance invocation to optionally emit or append a corresponding `QueryStep`
4. keep immediate execution naive and stepwise unless a later layer explicitly introduces richer orchestration
5. make saved queries possible earlier
6. make sub-graphs, rather than individual Dances, the natural units for later delegation and optimization

Exit criteria:

- `QueryStep` and `QueryGraph` exist as MAP-owned symbolic structure
- a simple chain is supported first, while graph shape remains allowed by the model
- direct navigation does not require declarative parsing, optimizer machinery, or a generalized planner runtime
- individual operation Dances remain the first executable behavior surface

### Layer 3 - `ExecutionInstance` Orchestration And Replay

Goal:

Introduce replay and richer execution coordination without making `QueryGraph` the executor of every operation or the owner of runtime state.

Objects:

- `QueryGraph` HolonType and query-graph holons
- `ExecutionInstance`
- optional host-level interactive orchestration object

Dance:

- host-owned orchestration and replay affordances backed by `QueryGraph` and `ExecutionInstance`

Primary PR chunks:

- Query PRS6

Execution and replay orchestration should:

1. accept a navigation operation intent
2. append a deterministic operation to the related `QueryGraph` holon when graph capture is active
3. execute immediately when requested or replay a previously saved graph
4. create or reuse an `ExecutionInstance`
5. resolve inputs through that `ExecutionInstance`'s bindings
6. store output bindings, runtime values, diagnostics, and execution status on the `ExecutionInstance`

Exit criteria:

- `QueryGraph` remains the symbolic query artifact
- `ExecutionInstance` owns live execution bindings and runtime state
- any interactive session object is host-level orchestration around `QueryGraph` plus `ExecutionInstance`, not the normative runtime state carrier
- operation append and immediate execution are coordinated by the host-level interactive affordance
- individual operation Dances do not each mutate plans as incidental side effects

### Layer 4 - `QueryGraph` Execute Dance

Goal:

Replay previously defined plans.

Dance:

- `QueryGraph.Execute`

Primary PR chunk:

- Query PRS7

Exit criteria:

- a saved or constructed `QueryGraph` holon can execute against an explicit transaction, snapshot, or session context
- execution resolves plan variables through an `ExecutionInstance`
- results remain `HolonCollection`-centered until a projection boundary requires concrete materialized result types
- replay preserves descriptor-backed validation and deterministic ordering rules

### Layer 5 - DeclarativeQuery

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
  -> QueryGraph holon
  -> Execute
```

Exit criteria:

- supported OpenCypher/GQL subsets compile into MAP `QueryGraph` holons
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

That chunk is done, but some implementation consequences of the older query
contract model may still need targeted cleanup. Treat those as new follow-on
alignment tasks rather than pretending PRO3 itself is still open.

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

- `ExecutionInstance` orchestration and replay
- host-level interactive orchestration
- `QueryGraph.Execute`
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
- `QueryStep` / `QueryGraph` only if we choose the slightly more ambitious path for early symbolic query capture
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
- Keep Commands and Dances envelopes distinct from `QueryGraph`, `ExecutionInstance`, optional host-level interactive orchestration, and `DeclarativeQuery` lifecycles.
- Do not let early `QueryStep` / `QueryGraph` introduction silently expand into full declarative planning or optimizer work.
- Keep descriptor-backed structural validation separate from the runtime carrier model.
- Keep legacy query/navigation behavior working until an explicit migration step replaces it.

---

## Immediate Next Step

The immediate implementation path should return to the DAHN mainline with the data-type question settled.

If a query/navigation issue is generated next, continue with the first behavior-bearing PRS work or the lightweight symbolic-structure scaffold:

1. **Query PRS2 - SeedHolons And Descriptor-Validated Expand Over HolonCollection**
2. **Query PRO4 - QueryStep And QueryGraph HolonType Scaffold**

The preferred near-term implementation shape is:

```text
Navigation Operation Dances over HolonCollection
  -> optional lightweight QueryStep / QueryGraph capture
  -> naive stepwise execution is still acceptable initially
```

That is still not a full declarative query substrate, not a standalone new-world query envelope, and not an OpenCypher-compatible execution engine.
