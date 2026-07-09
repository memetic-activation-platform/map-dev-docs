# Query / Navigation Implementation Plan (v2.7)

Status: pre-`QueryExpression` pivot implementation plan.

This plan still reflects the earlier `QueryGraph` / `QueryStep` delivery
shape. The current query architecture has moved to the storage-grounded
`QueryExpression` model described in
[storage-grounded-query-architecture.md](storage-grounded-query-architecture.md).
Use this plan as delivery history and a realignment source, not as the current
implementation authority.

## Purpose

This document turns the MAP query/navigation design specs into a practical delivery sequence.

The current design pivot is:

```text
Dance command or trusted ingress
  -> QueryDance invocation
  -> QueryDanceRequest
  -> QueryGraph
  -> QueryStep execution over HolonCollection
  -> ExecutionInstance-backed runtime state
  -> future distributed execution
  -> future declarative compilation
```

`Query` is not a required runtime object for the current implementation target.
The current implementation focus is executable `QueryGraph`s and the core query
algebra used by both host and guest execution.

This is an implementation plan, not the design authority. The design authority lives in:

- [index.md](index.md)
- [query-arch.md](query-arch.md)
- [query-engine-design-spec.md](query-engine-design-spec.md)
- [command-dance-query-schema-tdl.md](command-dance-query-schema-tdl.md)
- [dist-query-concept.md](dist-query-concept.md)
- [declarative-query/query-planner-algebra.md](declarative-query/query-planner-algebra.md)

---

## Current Conclusion

The query design detour was needed to settle the shared data-type question before DAHN work hardened around the wrong result shapes.

That question is now settled enough for DAHN and for the newer execution seam:

- `HolonReference` is the primary singular holon-backed handle.
- `HolonCollection` is the primary plural holon-backed carrier.
- `BaseValue`, `Row`, and `RowSet` remain materialized projection/result types.
- `QueryDanceRequest` is the fixed-shape query execution request.
- `QueryGraph` owns symbolic query structure; `ExecutionInstance` owns runtime execution state.
- `RowSet`, paths, pair views, partitioned views, and graph-like outputs are concrete materialized result types, not foundational execution carriers.
- `BoundHolonCollection` is not required unless a future lifecycle or contract need emerges that `HolonCollection` plus surrounding plan/execution/result structure cannot represent.
- OpenCypher/GQL compatibility remains possible through later declarative compilation into `QueryGraph` and concrete compatibility-oriented result types.

This means Query PRs are no longer on the critical path to initial DAHN delivery merely to settle shared operand types.
DAHN can proceed against Commands ingress, `DanceInvocation`, `QueryDance`,
descriptor affordances, `HolonReference`, `HolonCollection`, and
projection-boundary result types.

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
- New chunks reflect the current design: query execution is a `QueryDance` over a
  `QueryGraph`, with `HolonCollection` as the primary runtime substrate.
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
| Query PRS2 - SeedHolons And Descriptor-Validated Expand Over HolonCollection | PRS                | Planned           |              8 | Yes                | Implement the first executable `QueryStepKind`s needed for DAHN: focal-space / execution-domain seeding and named-channel expansion returning `HolonCollection`, with descriptor-backed relationship legality validation in `Expand`.       |
| Query PRS3 - Filter And Projection Boundary Subset                           | PRS                | Planned           |              5 | Yes                | Add initial `Filter` and `Project` semantics as `QueryStepKind`s over `HolonCollection`, including descriptor-aware predicates and explicit projection-boundary behavior.                                                                   |
| Query PRS4 - Ordering, Distinct, And Pagination                              | PRS                | Planned           |              3 | Yes                | Add deterministic `OrderBy`, `Distinct`, `Skip`, and `Limit` semantics as host-owned `QueryStepKind`s over `HolonCollection`.                                                                                                             |
| Query PRS5 - QueryDance Response And Diagnostics Alignment                   | PRO / PRS          | Planned           |              3 | Likely             | Stabilize the `QueryDanceResponse` / result-outcome shape, diagnostics ownership, and response-body conventions without reviving retired `NavigationQueryResult` assumptions.                                                              |
| Query PRO4 - QueryStep And QueryGraph HolonType Scaffold                     | PRO                | Next              |              5 | Yes                | Introduce `QueryStep`, `QueryGraph`, declared input bindings, and declared result binding as the symbolic execution layer required by `QueryDanceRequest`.                                                                                |
| Query PRS6 - ExecutionInstance And QueryDance Runtime Coordination           | PRS                | Later             |              5 | No                 | Execute `QueryGraph` structures through an `ExecutionInstance`, maintain live execution bindings, and align runtime state ownership with the `QueryDance` execution model.                                                                 |
| Query PRS7 - Saved QueryGraph Replay                                         | PRS                | Planned           |              5 | No                 | Replay saved or constructed `QueryGraph` holons by creating or reusing an `ExecutionInstance`, with `HolonCollection`-centered results and concrete materialized result types where required.                                             |
| Query PRS8 - Distributed Host / Guest Query Execution                        | PRS                | Future            |              5 | No                 | Add host-coordinated multi-space behavior over the same `QueryDance` and `QueryGraph` model, including single-space guest execution, delegated continuation, and result merge rules.                                                       |
| Query PRS9 - Declarative Query Compilation Foundation                        | PRS                | Future            |              8 | No                 | Introduce the future declarative route that parses supported OpenCypher/GQL subsets into executable `QueryGraph` holons.                                                                                                                   |

The important correction is that the former large "Query PRO3 navigation substrate" is now split:

- a small **Query PRO3** closeout chunk for contract realignment
- the former **PRS1** slice is explicitly abandoned and should not be revived
- several **Query PRS** chunks for executable `QueryStepKind` behavior over `HolonCollection`
- an earlier symbolic execution-structure chunk for `QueryStep` / `QueryGraph`
- later execution-state and replay chunks aligned with `ExecutionInstance`

---

## Implementation Layers

Implement the navigation/query capability in layers.

### Layer 1 - `QueryDance` Execution Seam

Goal:

Land the canonical command/dance/query execution seam.

Core runtime pieces:

- `DanceInvocation`
- `QueryDance`
- `QueryDanceRequest`
- `QueryDanceResponse`
- host dispatch through the Integration Hub runtime
- execution through `holons_core::execute_dance_v2(...)`

This layer should ensure:

- Commands ingress and TrustChannel ingress both adapt into the same
  `DanceInvocation -> QueryDance` seam
- query execution is no longer framed as a standalone query envelope
- `QueryDanceRequest` is the fixed-shape request contract for query execution
- `QueryDanceResponse` carries the externally meaningful result body

Primary PR chunks:

- Query PRS5
- Query PRO4

Exit criteria:

- the canonical ingress and dispatch seam is settled
- `QueryDanceRequest` and `QueryDanceResponse` are the normative query
  request/response contracts
- the query engine is clearly owned by the `QueryDance` implementation, not by
  Commands or boundary adapters

### Layer 2 - `QueryGraph` And `QueryStep` Symbolic Structure

Goal:

Introduce the symbolic execution model required by the current spec.

Objects:

- `QueryStep`
- `QueryGraph`
- `QueryBinding`
- typed wrappers or facades as needed

Primary PR chunks:

- Query PRO4

This layer should:

1. define `QueryGraph` as the symbolic query plan
2. define `QueryStep` as the operation node in that plan
3. define declared input bindings and declared result binding
4. keep the model graph-shaped even if initial execution starts with simple chains
5. avoid turning this into planner or optimizer work prematurely

Exit criteria:

- `QueryGraph` and `QueryStep` exist as MAP-owned symbolic execution structure
- runtime execution no longer depends on ad hoc step sequences alone
- direct execution still works without declarative parsing or optimization

### Layer 3 - Initial `QueryStepKind` Execution Set

Goal:

Implement the first executable `QueryStepKind`s over `HolonCollection`.

Initial step kinds:

- `SeedHolons`
- `Expand`
- `Filter`
- `OrderBy`
- `Skip`
- `Limit`
- `Distinct`
- `Project`

This layer should be enough for DAHN to navigate and refine holon-backed
results. Immediate execution may remain naive and stepwise in this layer,
including test suites that currently rely on `GetAllHolons`-style seeding over
fixture-scale data stores.

Primary PR chunks:

- Query PRS2
- Query PRS3
- Query PRS4

Exit criteria:

- initial `QueryStepKind`s consume and produce `HolonCollection` where applicable
- `Expand` follows named relationship channels
- `Filter` can evaluate an initial descriptor-aware predicate subset
- ordering and pagination are host-owned
- operation results do not require `BoundHolonCollection`, `RowSet`, `Path`, or a graph result object as foundational carriers
- query execution remains centered on `QueryDance` + `QueryGraph`, not on
  standalone operation-dance lifecycles

### Layer 4 - `ExecutionInstance` Runtime State

Goal:

Introduce runtime execution state ownership aligned with the current spec.

Objects:

- `ExecutionInstance`
- `ExecutionBinding`

Primary PR chunks:

- Query PRS6

This layer should:

1. create one `ExecutionInstance` per execution run
2. store runtime bindings on `ExecutionInstance`
3. keep live execution state out of `QueryGraph`
4. align diagnostics ownership with the newer `QueryDanceResponse` +
   `ExecutionInstance` split

Exit criteria:

- `QueryGraph` remains the symbolic query artifact
- `ExecutionInstance` owns live execution bindings and runtime state
- runtime ownership is aligned with the spec's command/dance/query seam

### Layer 5 - Saved `QueryGraph` Replay

Goal:

Replay previously defined plans through the same execution model.

Primary PR chunk:

- Query PRS7

Exit criteria:

- a saved or constructed `QueryGraph` holon can execute against an explicit
  transaction, snapshot, or session context
- execution resolves plan variables through an `ExecutionInstance`
- results remain `HolonCollection`-centered until a projection boundary
  requires concrete materialized result types
- replay preserves descriptor-backed validation and deterministic ordering rules

### Layer 6 - Declarative Query Compilation

Goal:

Add declarative query support after the executable `QueryGraph` route is stable.

Primary PR chunk:

- Query PRS9

The future route is:

```text
Declarative query expression (OpenCypher/GQL)
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
- query execution applies predicates without becoming the semantic owner of value types

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

- `ExecutionInstance` replay tooling beyond the core execution model
- saved query replay
- declarative query compilation
- OpenCypher/GQL parsing
- `BoundHolonCollection`
- foundational `RowSet` or path execution

Initial DAHN delivery does need:

- stable Commands ingress
- `DanceInvocation` through Commands
- `QueryDance` execution through the shared host runtime
- descriptor-afforded behavior discovery
- `HolonReference`
- `HolonCollection`
- `QueryGraph` / `QueryStep` if DAHN adopts the current executable-graph path
- scalar/property projection through `BaseValue` where needed
- initial `QueryStepKind`s that let DAHN seed, expand, filter, order, and page holon-backed results

---

## Guardrails

- Do not make `RowSet` the default execution carrier.
- Do not introduce `BoundHolonCollection` unless it has a specific lifecycle or contract that `HolonCollection` cannot satisfy.
- Do not model MAP relationships as property-bearing edge instances.
- Do not put OpenCypher/GQL semantics into the initial executable `QueryStepKind` set.
- Do not make Commands, SDK, or hApp ingress layers the semantic home of navigation behavior.
- Do not introduce a generic `Query` runtime object unless a future design identifies a concrete lifecycle for it.
- Keep Commands and Dances envelopes distinct from `QueryGraph`,
  `ExecutionInstance`, and future declarative compilation lifecycles.
- Do not let early `QueryStep` / `QueryGraph` introduction silently expand into
  full declarative planning or optimizer work.
- Keep descriptor-backed structural validation separate from the runtime carrier model.
- Keep legacy query/navigation behavior working until an explicit migration step replaces it.

---

## Immediate Next Step

The immediate implementation path should return to the DAHN mainline with the data-type question settled.

If a query/navigation issue is generated next, continue with the symbolic
structure scaffold plus the first executable step-kind work:

1. **Query PRO4 - QueryStep And QueryGraph HolonType Scaffold**
2. **Query PRS2 - SeedHolons And Descriptor-Validated Expand Over HolonCollection**
3. **Query PRS5 - QueryDance Response And Diagnostics Alignment**

The preferred near-term implementation shape is:

```text
Dance ingress
  -> QueryDanceRequest
  -> QueryGraph / QueryStep scaffold
  -> initial QueryStepKind execution over HolonCollection
  -> naive stepwise execution is still acceptable initially
```

That is still not a full declarative query substrate and not an
OpenCypher-compatible execution engine.
