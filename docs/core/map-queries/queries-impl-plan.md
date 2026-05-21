# Query Implementation Plan (v1.4)
## Parallel Descriptor-Aware Query Foundation Delivery Sequence

## Change Log

### v1.4

- updates the plan after the runtime shared types and bound-first dance/query contract refactor
- treats `docs/core/type-system/runtime-shared-types.md` as the canonical shared type foundation for query contracts
- makes bound-first `HolonReference` / `BoundHolonCollection` execution state the primary query posture
- clarifies `BaseValue`, `Row`, `RowSet`, and later `Record` / `RecordStream` as secondary materialized projection/result shapes
- keeps legacy `Node` / `NodeCollection` / `QueryPathMap` shapes explicitly transitional
- narrows remaining PRO work to query-specific envelope, contract, and substrate-boundary stabilization rather than rediscovering shared runtime types
- aligns query contract work with downstream dance, command, SDK, and DAHN convergence

This document translates the current MAP query portfolio into a practical implementation sequence aligned with the descriptor-driven implementation roadmap.

It is intended to:

- break query delivery into concrete, dependency-aware phases
- distinguish runtime-shared-type and envelope stabilization from descriptor-dependent semantics
- preserve a single phase sequence while allowing multiple PR tracks within that sequence
- prevent premature hardening around planners, declarative syntax, or distributed execution before the execution substrate is stable
- provide a basis for issue definition, sequencing, and parallel work decisions

This plan is based on the latest query documents in `docs/core/map-queries`, prioritizing the newest versioned files where multiple versions exist.

Current implementation reality:

- MAP does not currently have a mature query runtime aligned to the portfolio architecture
- the existing implementation is still a primitive one-hop traversal helper rooted in:
    - tx-bound `HolonReference`s
    - `RelationshipName`-driven expansion
    - `Node` / `NodeCollection` / `QueryPathMap`-style result shaping
- that implementation is useful as a starting point, but it is architecturally obsolete relative to the descriptor-synthesized query direction
- the legacy query/navigation module should remain intact and functioning while the new descriptor-aware substrate is introduced in parallel

This plan assumes:

- descriptors are the semantic source of query structure and value/operator meaning
- query algebra remains the execution substrate
- bound-first holon-backed execution state is the primary intermediate representational layer for deferred-projection execution
- the runtime shared type foundation now exists as a cross-surface baseline
- runtime-shared-type reuse and envelope stabilization can begin earlier than full descriptor interrogation
- `BaseValue` / `Row` / `RowSet` are materialized contract and projection shapes rather than the full internal execution model
- `HolonReference`, `BoundHolonCollection`, and contract-significant `SmartReference` usage are the primary bound side of the shared query contract posture
- `ResolvedType`-like structures are execution aids rather than the long-term caller-facing semantic facade
- planner algebra, declarative compilation, and distributed query evolution should build on descriptor-aware execution rather than inventing a parallel semantic system
- sovereignty and trust-channel rules remain authoritative for distributed query behavior

Related references:

- `docs/core/map-queries/index.md`
- `docs/core/type-system/runtime-shared-types.md`
- `docs/core/map-queries/query-arch.md`
- `docs/core/map-queries/exec-time-type-resolution.md`
- `docs/core/map-queries/navigation-algebra.md`
- `docs/core/map-queries/query-planner-algebra.md`
- `docs/core/map-queries/distributed-query-semantics.md`
- `docs/core/map-queries/cypher-operator-inventory.md`
- `docs/roadmap/desc-driven-impl-plan.md`

---

# 1. Delivery Principles

The implementation sequence follows these rules:

- descriptors own structural and value/operator semantics
- the current primitive relationship-name traversal model should be treated as transitional rather than as the future query foundation
- early query PRs should introduce the new substrate in parallel rather than forcing immediate cutover from the legacy query/navigation module
- runtime shared type reuse and envelope shape may stabilize before descriptor-backed semantic interrogation is available
- query contracts should prefer bound-first shapes and defer materialized projection where possible
- query execution must not become the second semantic home of property, relationship, or operator meaning
- runtime structural projection may exist for execution efficiency, but should remain subordinate to descriptor-facing APIs
- navigation algebra should stabilize before planner or declarative work hardens
- distributed query behavior must preserve descriptor meaning without violating sovereignty or trust-channel rules
- planner and declarative layers should compile into descriptor-aware algebra rather than into a handwritten parallel semantic runtime

---

# 2. Phase Overview

The recommended query implementation sequence is:

1. Runtime Shared Types and Envelope Foundation
2. Query Envelope and Contract Stabilization
3. Parallel Descriptor-Backed Structural Resolution and Navigation Algebra Contract Stabilization
4. Descriptor-Owned Predicate and Operator Alignment
5. Distributed and Planner Evolution
6. Declarative Compilation and Optimization Evolution
7. Legacy Migration and Cutover

The recommended PR segmentation uses two tracks:

- `PRO` = runtime-shared-type / envelope / contract track
- `PRS` = semantic / descriptor-dependent track

Recommended query PRs:

1. Query PRO1 — Runtime Shared Types Foundation
2. Query PRO2 — Query Envelope and Contract Stabilization
3. Query PRO3 — Navigation Algebra Contract Stabilization
4. Query PRS1 — Parallel Descriptor-Backed Structural Resolution
5. Query PRS2 — Descriptor-Owned Predicate and Operator Alignment
6. Query PRS3 — Distributed Descriptor-Consistent Query Semantics
7. Query PRS4 — Planner Algebra Foundation
8. Query PRS5 — Declarative Compilation and Optimization Evolution
9. Query PR7 — Legacy Migration and Cutover

Each phase below defines:

- goal
- major deliverables
- why the phase exists
- dependencies
- exit criteria

---

# 3. Phase 1 — Runtime Shared Types and Envelope Foundation

## Goal

Adopt the canonical runtime shared type family and baseline query envelope posture so interface shape can stabilize before full descriptor-backed semantic interrogation is available.

## Major Deliverables

- Query PRO1:
    - runtime shared types foundation alignment
    - baseline result-shape normalization

- primary bound runtime shared types for query contracts and intermediate execution:
    - `HolonReference`
    - `BoundHolonCollection`
    - `SmartReference` where smart-link-aware behavior is contract-significant
- secondary materialized projection/result types:
    - `BaseValue`
    - `Row`
    - `RowSet`
- explicit posture for later `Record` / `RecordStream` evolution
- initial normalization away from legacy `Node` / `NodeCollection` as the long-term architectural result model
- runtime-shared-type guidance for reuse by dance, command, and SDK work

## Why This Phase Exists

The shape of query inputs and outputs has ripple effects across dance invocation, command parameters, and the TypeScript SDK. That shape should stabilize earlier than descriptor-driven semantic interrogation so downstream consumers can minimize churn.

Updated interpretation:

- this phase now adopts the cross-surface runtime shared type foundation rather than defining a query-only type family
- it stabilizes shared projection and contract shapes beneath a primary bound-first execution posture
- it must not be read as proving that `BaseValue` / `Row` / `RowSet` are the intended canonical intermediate execution substrate

Without this phase:

- SDK-facing and API-facing work will continue to depend on the obsolete legacy query shape
- dance/query/command contract convergence will happen too late
- interface stabilization will remain coupled to semantic interrogation work that is blocked on descriptors

## Dependencies

- none beyond acceptance of the architectural direction

## PR Identity

- Query PRO1 / runtime shared types foundation

## Exit Criteria

- query contracts align with the canonical runtime shared type family
- bound-first versus projection/result type roles are explicit
- legacy query result shapes are no longer treated as the long-term target model
- downstream work can begin converging on `HolonReference`, `BoundHolonCollection`, `BaseValue`, `Row`, and `RowSet` according to their distinct roles

---

# 4. Phase 2 — Query Envelope and Contract Stabilization

## Goal

Stabilize the query envelope and contract posture as soon as the runtime shared type family exists, without waiting for descriptor-backed structural resolution that is not strictly required for this shape-level work.

This phase is specifically about the end-to-end contract path:

- TypeScript SDK-facing query API shape
- Commands ingress shape for TS client-to-host invocation
- host-side binding/adaptation posture
- substrate-facing query request envelope
- substrate-facing query result envelope

It should wire that path through the real ingress stack while remaining intentionally shape-level.
It should not yet define descriptor-backed interrogation, predicate semantics, planner behavior, distributed behavior, or the final internal execution representation.

## Major Deliverables

- Query PRO2:
    - query envelope and contract stabilization
    - execution/result envelope posture for new query work
    - explicit layer-by-layer contract path from TS through Commands to the substrate boundary

- canonical TS SDK-facing query API direction
- canonical Commands-ingress query shape for client-to-host invocation
- canonical host-side adapter/binding seam from Commands into the shared query substrate
- canonical substrate-facing query request envelope direction
- canonical substrate-facing query result envelope direction
- navigation/query envelope conventions
- explicit structural roles for runtime-shared-type members inside request/result contracts
- explicit distinction between:
    - TS-facing API
    - Commands ingress
    - wire/binding boundary
    - substrate-facing contracts
    - internal execution representation
- stabilization of the new query contract direction in parallel with the legacy path
- no immediate cutover requirement for the legacy `Node` / `NodeCollection` / `QueryPathMap` path
- explicit preservation of deferred projection:
    - `BaseValue`, `Row`, and `RowSet` remain shared contract/output shapes
    - they do not require intermediate execution state to be stored as eager rows
    - richer holon-bound or descriptor-aware bindings may remain internal until a contract or operator requires projection

## Why This Phase Exists

Some query work is truly descriptor-dependent, but not all of it is. Once `Query PRO1` has aligned query contracts with the runtime shared type family, the next fully unblocked step is to stabilize the query envelope and contract posture.

Without this phase:

- request/result shape will remain underspecified longer than necessary
- downstream dance/command/SDK convergence will wait on descriptor-dependent work that is not actually required for envelope stabilization
- later query execution work will continue to inherit unnecessary contract churn
- Commands risk becoming the accidental architectural home of query behavior rather than a thin ingress adapter
- the runtime shared type family risks being overread as an eager internal row model instead of a shared contract vocabulary

## Dependencies

- Query PRO1 / runtime shared types foundation
- runtime shared types foundation

Explicitly not required yet:

- descriptor-backed structural interrogation
- value/operator legality or execution semantics
- navigation algebra runtime behavior
- planner algebra
- distributed query behavior
- declarative compilation

## PR Identity

- Query PRO2 / query envelope and contract stabilization

## Exit Criteria

- the TS SDK-facing query contract direction is explicitly defined
- the Commands-ingress query contract direction is explicitly defined
- the substrate-facing request/result envelope direction is explicitly defined
- the host-side adapter/binding seam is explicitly defined
- the end-to-end contract path from TS through Commands to the substrate boundary is wired
- the new query request/result contract shape is explicitly defined
- the contract clearly builds on the `Query PRO1` runtime shared types foundation
- request, response, adapter, substrate-boundary, and execution-facing structural roles are clearly separated
- the contract explicitly preserves deferred projection and richer internal bindings
- the contract does not force eager row-shaped execution where bound-first state is sufficient
- later query, dance, command, and SDK work can target a stable query envelope direction

---

# 5. Phase 3 — Parallel Descriptor-Backed Structural Resolution and Navigation Algebra Contract Stabilization

## Goal

Introduce the descriptor-backed structural substrate in parallel with the legacy query/navigation module and stabilize the navigation algebra contract once the work is fully unblocked.

## Major Deliverables

- Query PRS1:
    - parallel descriptor-backed structural foundation for query consumers
    - descriptor-backed structural resolution for query consumers
    - bounded runtime structural projection posture

- Query PRO3:
    - navigation algebra contract stabilization
    - transaction-scoped execution posture

- query-side consumption of effective descriptor-backed property and relationship lookup
- preservation of declared vs inverse relationship meaning in structural access
- explicit interpretation of `ResolvedType`-like structures as internal execution aids
- explicit parallel-introduction posture for the new descriptor-backed structural layer
- navigation/query envelope conventions
- stabilized navigation-oriented operations such as:
    - `Seed`
    - `Expand`
    - `Filter`
    - `Project`
    - `Distinct`
    - `OrderBy`
    - `Skip`
    - `Limit`
- strict separation between:
    - ontology layer
    - runtime structural layer
    - instance state
- contract-ready runtime-shared-type usage around:
    - bound `HolonReference` / `BoundHolonCollection` state
    - materialized `BaseValue` / `Row` / `RowSet` projections

## Why This Phase Exists

The query portfolio treats navigation algebra as the near-term execution foundation for human-first exploration, DAHN-guided traversal, and future planner work. After the bound-first refactor, that algebra should preserve holon-bound execution state until a projection, operator, ABI, or serialization boundary requires materialization.

Unlike `Query PRO2`, `Query PRO3` is not fully unblocked until descriptor-backed structural resolution is in place, so it should remain paired with that dependency rather than being pulled earlier by phase numbering alone.

## Dependencies

- Descriptor PR1 / runtime spine
- Descriptor PR2 / schema-backed structural descriptor surface
- Query PRO1 / runtime shared types foundation

## PR Identity

- Query PRS1 / parallel descriptor-backed structural resolution
- Query PRO3 / navigation algebra contract stabilization

## Exit Criteria

- query consumers can obtain effective structure through descriptor-backed surfaces
- the legacy query/navigation module remains intact while the new descriptor-backed structural substrate exists in parallel
- runtime structural projection remains an internal execution aid rather than a caller-facing semantic layer
- no query caller needs to reconstruct inheritance flattening manually
- a minimal, replayable navigation algebra contract exists as the execution substrate
- runtime-shared-type and envelope shapes are stable enough for dance and SDK reuse
- bound-first execution posture remains compatible with materialized projection/result outputs
- execution remains algebra-first without claiming semantic ownership

---

# 6. Phase 4 — Descriptor-Owned Predicate and Operator Alignment

## Goal

Make filters and typed predicates consume descriptor-owned value/operator semantics rather than a freestanding query-operator subsystem.

## Major Deliverables

- Query PRS2:
    - descriptor-owned predicate and operator alignment
    - no freestanding query semantic operator system

- `Filter` semantics backed by `ValueDescriptor` where typed values are involved
- operator compatibility checks driven by descriptor-backed value semantics
- relationship-navigation checks grounded in relationship descriptor meaning
- alignment between query predicate semantics and validation semantics where they share value-type meaning

## Why This Phase Exists

The architecture synthesis is explicit: query execution should stop owning value-operator semantics independently. This phase is where query semantics and descriptor semantics actually converge.

## Dependencies

- Query PRS1 / parallel descriptor-backed structural resolution
- Query PRO3 / navigation algebra contract stabilization
- Descriptor Phase 3 / `ValueDescriptor` semantics

## PR Identity

- Query PRS2 / descriptor-owned predicate and operator alignment

## Exit Criteria

- query filters no longer depend on a parallel query-owned operator semantic system
- typed predicate behavior is descriptor-backed
- relationship navigation preserves descriptor-defined meaning

---

# 7. Phase 5 — Distributed and Planner Evolution

## Goal

Advance distributed query semantics and planner foundations only after the local execution substrate and descriptor-aware predicate posture are stable enough to support them.

## Major Deliverables

- Query PRS3:
    - distributed descriptor-consistent query semantics
    - sovereignty-preserving execution-domain and expansion rules

- Query PRS4:
    - planner algebra foundation
    - descriptor-aware logical operator posture

- explicit distributed execution-domain posture for rootless queries
- home-space expansion rule integration
- descriptor-consistent filtering and interpretation across SmartReference-based execution
- canonical space identity and rebinding posture
- initial logical operator subset informed by planner priorities, such as:
    - node scans / seeks
    - `Expand`
    - `Filter`
    - `Project`
    - `Aggregate`
    - `Sort` / `Limit`
    - `Apply`
    - `Optional`
    - `SemiApply`
    - `UnionAll`

## Why This Phase Exists

Distributed query behavior remains sovereignty-first, but descriptor meaning must still travel with the query where filtering and interpretation depend on it. Likewise, planner work should begin only after the substrate and predicate contracts are clear enough to prevent a second semantic authority from forming.

## Dependencies

- Query PRO3 / navigation algebra contract stabilization
- Query PRS2 / descriptor-owned predicate and operator alignment
- distributed query semantics baseline
- planner algebra baseline

## PR Identity

- Query PRS3 / distributed descriptor-consistent query semantics
- Query PRS4 / planner algebra foundation

## Exit Criteria

- distributed query behavior preserves descriptor meaning where required
- sovereignty and trust-channel rules remain authoritative
- a descriptor-aware planner algebra foundation exists without inventing a parallel semantic layer

---

# 8. Phase 6 — Declarative Compilation and Optimization Evolution

## Goal

Layer in declarative query compilation, round-tripping, and optimization on top of descriptor-aware algebra.

## Major Deliverables

- Query PRS5:
    - declarative compilation and optimization evolution
    - descriptor-aware compilation posture

- OpenCypher/GQL compilation into descriptor-aware algebra
- descriptor-aware explainability / round-tripping posture
- replay and command-log preservation of descriptor identity where needed
- optimization work that respects descriptor semantics, such as:
    - predicate pushdown
    - operation reordering
    - cost-based planning when statistics exist
    - lazy/distributed execution evolution

## Why This Phase Exists

Declarative syntax and optimization are important, but they should sit on top of already-stable descriptor-aware execution and planner foundations rather than forcing those foundations prematurely.

## Dependencies

- Query PRS4 / planner algebra foundation
- Query PRS2 / descriptor-owned predicate and operator alignment
- sufficient execution maturity for replay/round-tripping and optimization work

## PR Identity

- Query PRS5 / declarative compilation and optimization evolution

## Exit Criteria

- declarative compilation targets descriptor-aware algebra rather than a parallel semantic runtime
- round-tripping and explainability preserve descriptor-backed meaning
- optimization work respects descriptor-defined structural and operator semantics

---

# 9. Phase 7 — Legacy Migration and Cutover

## Goal

Migrate adopters from the legacy query/navigation module to the new descriptor-aware query substrate only after the new foundation is stable enough to replace it safely.

## Major Deliverables

- Query PR7:
    - explicit migration and cutover plan
    - legacy query/navigation deprecation posture

- migration guidance from the legacy `Node` / `NodeCollection` / `QueryPathMap` path
- explicit cutover criteria for adopters and tests
- deprecation/removal posture for legacy query/navigation APIs
- regression coverage proving that the new substrate can safely replace the old path where intended

## Why This Phase Exists

Keeping the legacy path intact early reduces delivery risk, but it also means migration must be handled deliberately later rather than by drift or accidental abandonment.

## Dependencies

- Query PRS1 / parallel descriptor-backed structural resolution
- Query PRO3 / navigation algebra contract stabilization
- Query PRS2 / descriptor-owned predicate and operator alignment
- sufficient stability in whichever later query layers are required for intended adopters

## PR Identity

- Query PR7 / legacy migration and cutover

## Exit Criteria

- migration from the legacy query/navigation path is explicit rather than accidental
- cutover happens only where the new substrate is actually ready
- legacy deprecation posture is documented and test-backed

---

# 10. Cross-Phase Dependency Summary

## Critical Path

1. Descriptor structural surface
2. Runtime shared types foundation
3. Query envelope and contract stabilization
4. Parallel descriptor-backed structural foundation
5. Navigation algebra contract stabilization
6. Descriptor-owned predicate and operator alignment
7. Distributed descriptor-consistent semantics
8. Planner algebra foundation
9. Declarative compilation and optimization evolution
10. Legacy migration and cutover

## Key Dependency Rules

- the current primitive one-hop traversal helper should not be allowed to harden into the long-term query foundation
- the legacy query/navigation module should remain intact until an explicit later migration/cutover phase is reached
- runtime shared type reuse and envelope stabilization may move earlier than descriptor-backed semantic interrogation
- bound-first query/dance contract posture is already the baseline and should not be reopened in query-specific work
- query callers should not finalize around `ResolvedType` as the semantic facade once descriptor-backed lookup is available
- navigation algebra should stabilize before planner or declarative work hardens
- query predicate semantics should not finalize before `ValueDescriptor` semantics exist
- distributed query execution must preserve descriptor meaning without violating sovereignty and trust-channel boundaries
- planner and declarative layers should compile into descriptor-aware algebra rather than inventing a second query-semantic runtime

---

# 11. Parallel Work Guidance

## Safe Earlier Work

- query implementation sequence planning
- issue definition for query-specific runtime shared type adoption and envelope stabilization
- issue definition for parallel descriptor-backed structural resolution
- inventory of current query-side semantic duplication
- Query PRO1 / runtime shared types foundation
- Query PRO2 / envelope and contract stabilization

## Safe Once Descriptor Structural Surface Exists

- Query PRS1 / parallel descriptor-backed structural resolution
- Query PRO3 / navigation algebra contract stabilization

## Safe Once Descriptor-Owned Scalar Semantics Exist

- Query PRS2 / descriptor-owned predicate and operator alignment
- alignment with validation semantics where value-type meaning overlaps

## Safe Once Navigation Algebra Stabilizes

- Query PRS3 / distributed semantics integration
- Query PRS4 / planner algebra foundation

## Safe Once Planner Foundation Exists

- Query PRS5 / declarative compilation and optimization evolution

## Safe Once New Substrate Is Proven Enough For Adopters

- Query PR7 / legacy migration and cutover

---

# 12. Recommended Initial Issue / PR Sequence

A likely issue sequence is:

1. Query PRO1
   - align query contracts with the canonical runtime shared type family
   - normalize the long-term result-shape direction around bound-first execution and deferred projection
2. Query PRO2
   - stabilize query envelopes and contract posture
3. Query PRS1
   - introduce the new structural foundation in parallel with the legacy path
   - expose descriptor-backed structural lookup to query consumers
   - define the bounded role of runtime structural projection
4. Query PRO3
   - stabilize the navigation algebra runtime shared type posture and execution contract
   - preserve bound-first intermediate state while allowing materialized projection outputs
5. Query PRS2
   - align filters and predicate semantics with `ValueDescriptor`
6. Query PRS3
   - integrate distributed descriptor-consistent filtering and navigation semantics
7. Query PRS4
   - introduce the descriptor-aware planner algebra foundation
8. Query PRS5
   - evolve declarative compilation and optimization on top of descriptor-aware algebra
9. Query PR7
   - migrate adopters and tests from the legacy path once the new substrate is actually ready

---

# 13. Immediate Next Step

The immediate next step should be to define the first issue in each early track:

- Query PRO1:
  - query adoption of the runtime shared types foundation
  - bound-first execution and contract posture
  - long-term result-shape normalization posture

- Query PRS1:
  - parallel introduction posture for the new substrate
  - descriptor-backed query structural resolution
  - explicit caller-facing shift from standalone `ResolvedType` semantics toward descriptor-facing lookup
  - preservation of runtime structural projection only as an execution aid

Those issues are the natural entry points for the query track.
