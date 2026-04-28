# Query Implementation Plan (v1.2)
## Parallel Descriptor-Aware Query Foundation Delivery Sequence

This document translates the current MAP query portfolio into a practical implementation sequence aligned with the descriptor-driven implementation roadmap.

It is intended to:

- break query delivery into concrete, dependency-aware phases
- distinguish descriptor-owned semantics from algebra-owned execution
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
- this plan should therefore be read as a parallel foundation-and-migration sequence, not as a light semantic realignment of an already-mature query layer and not as an immediate destructive replacement of the legacy path

This plan assumes:

- descriptors are the semantic source of query structure and value/operator meaning
- query algebra remains the execution substrate
- `ResolvedType`-like structures are execution aids rather than the long-term caller-facing semantic facade
- planner algebra, declarative compilation, and distributed query evolution should build on descriptor-aware execution rather than inventing a parallel semantic system
- sovereignty and trust-channel rules remain authoritative for distributed query behavior

Related references:

- `docs/core/map-queries/index-v1.1.md`
- `docs/core/map-queries/query-arch-v1.1.md`
- `docs/core/map-queries/exec-time-type-resolution-v1.1.md`
- `docs/core/map-queries/navigation-algebra-v1.1.md`
- `docs/core/map-queries/query-planner-algebra-v1.1.md`
- `docs/core/map-queries/distributed-query-semantics-v1.1.md`
- `docs/core/map-queries/cypher-operator-inventory-v1.1.md`
- `docs/roadmap/desc-driven-impl-plan.md`

---

# 1. Delivery Principles

The implementation sequence follows these rules:

- descriptors own structural and value/operator semantics
- the current primitive relationship-name traversal model should be treated as transitional rather than as the future query foundation
- early query PRs should introduce the new substrate in parallel rather than forcing immediate cutover from the legacy query/navigation module
- query execution must not become the second semantic home of property, relationship, or operator meaning
- runtime structural projection may exist for execution efficiency, but should remain subordinate to descriptor-facing APIs
- navigation algebra should stabilize before planner or declarative work hardens
- distributed query behavior must preserve descriptor meaning without violating sovereignty or trust-channel rules
- planner and declarative layers should compile into descriptor-aware algebra rather than into a handwritten parallel semantic runtime

---

# 2. Phase Overview

The recommended query implementation sequence is:

1. Parallel Descriptor-Backed Structural Resolution Foundation
2. Navigation Algebra Execution Substrate
3. Descriptor-Owned Predicate and Operator Alignment
4. Distributed Descriptor-Consistent Query Semantics
5. Planner Algebra Foundation
6. Declarative Compilation and Optimization Evolution
7. Legacy Migration and Cutover

The recommended PR segmentation is:

1. Query PR1 — Parallel Descriptor-Backed Structural Resolution Foundation
2. Query PR2 — Navigation Algebra Execution Substrate
3. Query PR3 — Descriptor-Owned Predicate and Operator Alignment
4. Query PR4 — Distributed Descriptor-Consistent Query Semantics
5. Query PR5 — Planner Algebra Foundation
6. Query PR6 — Declarative Compilation and Optimization Evolution
7. Query PR7 — Legacy Migration and Cutover

Each phase below defines:

- goal
- major deliverables
- why the phase exists
- dependencies
- exit criteria

---

# 3. Phase 1 — Parallel Descriptor-Backed Structural Resolution Foundation

## Goal

Introduce a descriptor-backed structural resolution foundation in parallel with the legacy query/navigation module so later query execution work can build on the new substrate without breaking existing behavior or tests.

## Major Deliverables

- Query PR1:
    - parallel descriptor-backed structural foundation for query consumers
    - descriptor-backed structural resolution for query consumers
    - bounded runtime structural projection posture

- explicit parallel-introduction posture for the new descriptor-backed structural layer
- query-side consumption of effective descriptor-backed property and relationship lookup
- explicit interpretation of `ResolvedType`-like structures as internal execution aids
- bounded runtime caches for effective structural projection where useful
- no caller-side reconstruction of `Extends` flattening
- preservation of declared vs inverse relationship meaning in structural lookup
- no immediate cutover requirement for the legacy `Node` / `NodeCollection` / `QueryPathMap` path
- tests for deterministic structural resolution and conflict handling

## Why This Phase Exists

The query portfolio makes clear that structural meaning should increasingly come from descriptors, not from standalone query-owned structural logic. But the current implementation state is even earlier than that: MAP still has only a primitive one-hop traversal helper rather than a real descriptor-aware query substrate.

Without this phase:

- query callers will continue hardcoding relationship-name traversal logic
- the primitive `Node` / `NodeCollection` model will harden as if it were the intended architectural direction
- there will be no safe place to begin new query work without destabilizing the legacy path
- `ResolvedType` risks becoming a second semantic authority
- later navigation and predicate work will stabilize on the wrong abstraction

## Dependencies

- Descriptor PR1 / runtime spine
- Descriptor PR2 / schema-backed structural descriptor surface

## PR Identity

- Query PR1 / parallel descriptor-backed structural resolution foundation

## Exit Criteria

- query consumers can obtain effective structure through descriptor-backed surfaces
- the legacy query/navigation module remains intact while the new descriptor-backed structural substrate exists in parallel
- runtime structural projection remains an internal execution aid rather than a caller-facing semantic layer
- no query caller needs to reconstruct inheritance flattening manually

---

# 4. Phase 2 — Navigation Algebra Execution Substrate

## Goal

Stabilize the minimal navigation algebra as the execution substrate for interactive navigation and filtered traversal.

## Major Deliverables

- Query PR2:
    - navigation algebra execution substrate
    - minimal operand family for execution

- stabilized operand model:
    - `Value`
    - `Row`
    - `RowSet`
- initial navigation-oriented operations such as:
    - `Seed`
    - `Expand`
    - `Filter`
    - `Project`
    - `Distinct`
    - `OrderBy`
    - `Skip`
    - `Limit`
- transaction-scoped interpreter posture
- strict separation between:
    - ontology layer
    - runtime structural layer
    - instance state
- tests for deterministic navigation execution behavior

## Why This Phase Exists

The query portfolio treats navigation algebra as the near-term execution foundation for human-first exploration, DAHN-guided traversal, and future planner work. This layer must stabilize before more advanced planner or declarative work begins to harden.

## Dependencies

- Query PR1 / descriptor-backed structural resolution
- navigation algebra baseline

## PR Identity

- Query PR2 / navigation algebra execution substrate

## Exit Criteria

- a minimal, replayable navigation algebra exists as the execution substrate
- operand shapes are stable enough for dance and DAHN reuse
- execution remains algebra-first without claiming semantic ownership

---

# 5. Phase 3 — Descriptor-Owned Predicate and Operator Alignment

## Goal

Make filters and typed predicates consume descriptor-owned value/operator semantics rather than a freestanding query-operator subsystem.

## Major Deliverables

- Query PR3:
    - descriptor-owned predicate and operator alignment
    - no freestanding query semantic operator system

- `Filter` semantics backed by `ValueDescriptor` where typed values are involved
- operator compatibility checks driven by descriptor-backed value semantics
- relationship-navigation checks grounded in relationship descriptor meaning
- alignment between query predicate semantics and validation semantics where they share value-type meaning
- tests for descriptor-backed predicate behavior and unsupported-operator failure

## Why This Phase Exists

The architecture synthesis is explicit: query execution should stop owning value-operator semantics independently. This phase is where query semantics and descriptor semantics actually converge.

## Dependencies

- Query PR1 / descriptor-backed structural resolution
- Query PR2 / navigation algebra execution substrate
- Descriptor Phase 3 / `ValueDescriptor` semantics

## PR Identity

- Query PR3 / descriptor-owned predicate and operator alignment

## Exit Criteria

- query filters no longer depend on a parallel query-owned operator semantic system
- typed predicate behavior is descriptor-backed
- relationship navigation preserves descriptor-defined meaning

---

# 6. Phase 4 — Distributed Descriptor-Consistent Query Semantics

## Goal

Align distributed and federated query behavior with descriptor meaning while preserving sovereignty, execution-domain, and trust-channel constraints.

## Major Deliverables

- Query PR4:
    - distributed descriptor-consistent query semantics
    - sovereignty-preserving execution-domain and expansion rules

- explicit distributed execution-domain posture for rootless queries
- home-space expansion rule integration
- descriptor-consistent filtering and interpretation across SmartReference-based execution
- canonical space identity and rebinding posture
- no global-graph illusion in distributed execution
- tests or conformance scenarios for cross-space descriptor-consistent filtering/navigation

## Why This Phase Exists

Distributed query behavior remains sovereignty-first, but descriptor meaning must still travel with the query where filtering and interpretation depend on it. This phase prevents distributed semantics from drifting away from descriptor-owned meaning.

## Dependencies

- Query PR2 / navigation algebra execution substrate
- Query PR3 / descriptor-owned predicate and operator alignment
- distributed query semantics baseline

## PR Identity

- Query PR4 / distributed descriptor-consistent query semantics

## Exit Criteria

- distributed query behavior preserves descriptor meaning where required
- sovereignty and trust-channel rules remain authoritative
- no distributed query path relies on client-side reinterpretation of descriptor-backed predicates

---

# 7. Phase 5 — Planner Algebra Foundation

## Goal

Introduce the logical planner layer as a descriptor-aware future-facing foundation for broader declarative query evolution.

## Major Deliverables

- Query PR5:
    - planner algebra foundation
    - descriptor-aware logical operator posture

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
- planner algebra typed with descriptor-aware structural and value semantics
- compatibility posture between navigation algebra and planner algebra
- no cost-based planning requirement yet

## Why This Phase Exists

The planner layer is not near-term execution-critical, but it must be designed as descriptor-aware from the beginning so it does not become a second semantic authority.

## Dependencies

- Query PR2 / navigation algebra execution substrate
- Query PR3 / descriptor-owned predicate and operator alignment
- planner algebra baseline

## PR Identity

- Query PR5 / planner algebra foundation

## Exit Criteria

- a descriptor-aware planner algebra foundation exists
- logical operator evolution does not invent a parallel semantic layer
- planner work is clearly separated from immediate navigation execution work

---

# 8. Phase 6 — Declarative Compilation and Optimization Evolution

## Goal

Layer in declarative query compilation, round-tripping, and optimization on top of descriptor-aware algebra.

## Major Deliverables

- Query PR6:
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

- Query PR5 / planner algebra foundation
- Query PR3 / descriptor-owned predicate and operator alignment
- sufficient execution maturity for replay/round-tripping and optimization work

## PR Identity

- Query PR6 / declarative compilation and optimization evolution

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

- Query PR1 / parallel descriptor-backed structural resolution foundation
- Query PR2 / navigation algebra execution substrate
- Query PR3 / descriptor-owned predicate and operator alignment
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
2. Parallel descriptor-backed structural foundation
3. Navigation algebra execution substrate
4. Descriptor-owned predicate and operator alignment
5. Distributed descriptor-consistent semantics
6. Planner algebra foundation
7. Declarative compilation and optimization evolution
8. Legacy migration and cutover

## Key Dependency Rules

- the current primitive one-hop traversal helper should not be allowed to harden into the long-term query foundation
- the legacy query/navigation module should remain intact until an explicit later migration/cutover phase is reached
- query callers should not finalize around `ResolvedType` as the semantic facade once descriptor-backed lookup is available
- navigation algebra should stabilize before planner or declarative work hardens
- query predicate semantics should not finalize before `ValueDescriptor` semantics exist
- distributed query execution must preserve descriptor meaning without violating sovereignty and trust-channel boundaries
- planner and declarative layers should compile into descriptor-aware algebra rather than inventing a second query-semantic runtime

---

# 11. Parallel Work Guidance

## Safe Earlier Work

- query implementation sequence planning
- issue definition for parallel descriptor-backed structural resolution
- operand-model clarification
- inventory of current query-side semantic duplication

## Safe Once Descriptor Structural Surface Exists

- Query PR1 / parallel descriptor-backed structural resolution
- Query PR2 / navigation algebra execution substrate
- tests for relationship-descriptor-consistent navigation

## Safe Once Descriptor Value Semantics Exist

- Query PR3 / descriptor-owned predicate and operator alignment
- alignment with validation semantics where value-type meaning overlaps

## Safe Once Navigation Algebra Stabilizes

- Query PR4 / distributed semantics integration
- Query PR5 / planner algebra foundation

## Safe Once Planner Foundation Exists

- Query PR6 / declarative compilation and optimization evolution

## Safe Once New Substrate Is Proven Enough For Adopters

- Query PR7 / legacy migration and cutover

---

# 12. Recommended Initial Issue / PR Sequence

A likely issue sequence is:

1. Query PR1
   - introduce the new structural foundation in parallel with the legacy path
   - expose descriptor-backed structural lookup to query consumers
   - define the bounded role of runtime structural projection
2. Query PR2
   - stabilize the navigation algebra operand family and execution substrate
3. Query PR3
   - align filters and predicate semantics with `ValueDescriptor`
4. Query PR4
   - integrate distributed descriptor-consistent filtering and navigation semantics
5. Query PR5
   - introduce the descriptor-aware planner algebra foundation
6. Query PR6
   - evolve declarative compilation and optimization on top of descriptor-aware algebra
7. Query PR7
   - migrate adopters and tests from the legacy path once the new substrate is actually ready

---

# 13. Immediate Next Step

The immediate next step should be to define the first structural issue in this sequence:

- parallel introduction posture for the new substrate
- descriptor-backed query structural resolution
- explicit caller-facing shift from standalone `ResolvedType` semantics toward descriptor-facing lookup
- preservation of runtime structural projection only as an execution aid

That issue is the natural entry point for the query track.
