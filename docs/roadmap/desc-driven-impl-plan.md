# Descriptor-Driven MAP Implementation Milestone Plan (v1.6)

## Change Log

### v1.6

- rebases the dance portions of the synthesized roadmap onto `dances-impl-plan.md` v2.0
- treats Dance `PRO1` as delivered baseline and removes abandoned Dance `PRO2` / `PRO3` / `PRS1`-`PRS5` planning items
- replaces the old split dance posture with the revised Wave 5 sequence: `Dance PR2` through `Dance PR8`
- removes deferred dance dynamic-binding work from Wave 9 because it is now scoped inside the revised Wave 5 dance plan

### v1.5

- adds a status correction after the query/navigation design pivot
- treats `HolonCollection`, not `BoundHolonCollection`, as the current plural holon-backed carrier
- clarifies that Query PRs are no longer on the DAHN critical path merely to settle shared operand types
- points readers to `runtime-shared-types.md` v1.2 and `queries-impl-plan.md` v2.1 for the current navigation/query posture

### v1.4

- aligns the synthesized roadmap with the updated component implementation plans for queries, dances, commands, the TypeScript SDK, and DAHN Phase 0
- treats the runtime shared type foundation as a cross-surface baseline rather than a query-local operand effort
- makes bound-first `HolonReference` / `BoundHolonCollection` contracts the primary query/dance/command/SDK/DAHN posture
- clarifies `BaseValue`, `Row`, `RowSet`, and later `Record` / `RecordStream` as secondary materialized projection/result shapes
- incorporates the new Commands implementation plan and its `PRO` / `PRS` split
- updates TS and DAHN sequencing around public SDK descriptor handles, `DanceV2(DanceInvocation)`, `BoundHolonCollection`, and bridge-payload migration
- preserves descriptor ownership of semantics while narrowing Commands to IPC ingress, adapter, lifecycle policy, and descriptor-bound routing

This document is the synthesized cross-component implementation roadmap for the current descriptor-driven MAP architecture.

> Status note:
> This roadmap still contains older wave-level references to `BoundHolonCollection`, Query PRO2 envelopes, and Query PRO3 as part of the DAHN dependency chain.
> The current design source of truth is now [runtime-shared-types.md](../core/type-system/runtime-shared-types.md) v1.2 and [queries-impl-plan.md](../core/map-queries/queries-impl-plan.md) v2.1.
> Until this roadmap is fully rebaselined, read `HolonCollection` as the current plural holon-backed carrier and do not treat saved-plan or declarative-query work as blocking initial DAHN delivery.

Its purpose is to translate several component-level design specs and implementation plans into one dependency-aware execution sequence, so that work across descriptors, validation, queries, dances, commands, TypeScript surfaces, and DAHN can proceed without duplicated semantics, premature hardening, or avoidable rework.

In particular, this plan synthesizes across:

- the descriptor design and descriptor implementation plan
- the validation architecture and dependency gravity model
- the query architecture and query implementation plan
- the dance design and dance implementation plan
- the commands specification and commands implementation plan
- the runtime shared types foundation
- the TypeScript MAP SDK implementation specification
- the DAHN specs, blueprint, and implementation plan

Rather than replacing those component documents, this plan coordinates them. It identifies which capabilities are foundational, which downstream streams can begin safely in parallel, and which work must wait until descriptor-owned structure or semantics are real.

The guiding principle is:

- descriptors are the semantic root
- validation, queries, dances, commands, TS SDK surfaces, and DAHN should consume descriptor semantics rather than invent parallel systems
- implementation should separate structural foundations from semantic behavior and from TS / UX integration
- runtime shared types are the cross-surface contract vocabulary reused by commands, queries, dances, SDKs, and DAHN
- `HolonReference` and `HolonCollection` are the current primary holon-backed runtime shared types for holon-backed execution and results
- `BaseValue` / `Row` / `RowSet` should be read primarily as shared materialized contract and projection shapes rather than as the full internal execution substrate
- Commands own IPC ingress, wire/domain binding, structural scope, and lifecycle policy; they do not own query, dance, or descriptor semantics

---

## Provisional Effort Estimates

These estimates use the lightweight implementation-point scale:

- `1` = tightly bounded
- `2` = small
- `3` = medium
- `5` = large
- `8` = unusually uncertain or cross-cutting

Wave totals below are provisional rollups of likely issue/PR slices rather than commitments.  
Confidence reflects how much of the wave is already issue-defined and how stable its dependency surface currently looks.

| Wave                                                        | Best Estimate | Range | Confidence | Notes                                                                                                                           |
|-------------------------------------------------------------|--------------:|------:|------------|---------------------------------------------------------------------------------------------------------------------------------|
| Wave 0 — Structural Groundwork                              |            22 | 20-24 | High       | Retrospective calibration from delivered foundational work.                                                                     |
| Wave 1 — Schema-Backed Descriptor Surface                   |            18 | 15-22 | Medium-Low | Carries early `Query PRO1/PRO2`, `Dance PRO1`, command contract inventory, and DAHN adapter refinement alongside Descriptor PR2. |
| Wave 2 — Descriptor-Owned Value Semantics                   |            20 | 15-24 | Low        | Carries early `Query PRO3`, dance semantic-validation prep, command runtime shared type adoption, and descriptor semantic work. |
| Wave 3 — Validation Integration                             |            13 | 10-16 | Low-Medium | Validation layering is conceptually clear, but implementation depends heavily on what Descriptor Phase 3 actually delivers.     |
| Wave 4 — Query Runtime Shared Type, Contract, and Structural Semantics |  20 | 16-24 | Low-Medium | Broader than before because it now includes runtime shared type, contract, and descriptor-semantic work, but the split reduces ambiguity. |
| Wave 5 — Dance Holonic Contract and Execution Alignment     |            32 | 26-38 | Medium     | Now reflects the revised post-`PRO1` sequence from `Dance PR2` through `Dance PR8`, including schema alignment, ingress, query/navigation dances, activation, and test migration. |
| Wave 6 — Command IPC Contract, Descriptor Anchoring, and Routing |        16 | 11-20 | Low        | Expanded now that Commands has an explicit PRO/PRS implementation plan and bridge-payload migration obligations.                |
| Wave 7 — TypeScript Interface Realignment                   |            22 | 17-27 | Low        | Now includes bound-first SDK result mapping, descriptor handles, `DanceInvocation`, and query bridge migration.                 |
| Wave 8 — Real DAHN Integration                              |            18 | 13-21 | Low        | Depends on TS descriptor/bound-reference surfaces and multiple prior DAHN PRs, so scope is visible but not yet stable.          |
| Wave 9 — Advanced Query Evolution                           |            13 | 10-18 | Low        | Now focused on planner and declarative query evolution after the revised dance activation/binding work moves into Wave 5.        |

Practical interpretation:

- high confidence means the estimate is useful for planning and calibration
- medium confidence means the estimate is directionally useful but should be revisited as issues are defined
- low confidence means the estimate is mainly a placeholder for wave-scale comparison and should not be treated as a commitment

Recommended practice:

- re-estimate each wave after its major issues/PR slices are defined
- treat these totals as planning aids, not performance commitments
- prefer estimating issue/PR slices directly once a wave becomes active

---

## Testing Posture by Wave / PR

Implementation sequencing should be matched by test sequencing.

The main rule is:

- introduce the strongest tests only when the corresponding runtime contract is actually intended to stabilize

That means:

- early structural work should prefer unit tests and narrow seam/boundary tests
- semantic convergence work should add richer contract tests once descriptor-owned meaning is in scope
- integration tests should be introduced when a cross-module execution contract is part of the intended deliverable
- end-to-end or framework-backed tests should not be used to harden provisional semantics too early

### Testing Guidance by Work Type

| Work Type                                                  | Preferred Tests                                                              | Avoid Too Early                                                                                   |
|------------------------------------------------------------|------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| Structural descriptor surfaces                             | unit tests, schema-backed lookup tests, inheritance/effective-access tests   | broad integration tests that assume later semantic behavior                                       |
| Validation layer classification / PVL / Nursery boundaries | unit tests, classification tests, bounded seam tests                         | end-to-end semantic validation flows before descriptor semantics are real                         |
| Query `PRO` contract work                                  | unit tests, runtime-shared-type tests, envelope/contract tests, compatibility tests | descriptor-semantic, planner, or declarative integration tests before the contract substrate stabilizes |
| Query `PRS` semantic work                                  | unit tests, descriptor-aware execution tests, semantic seam tests            | declarative/planner integration tests before navigation algebra and predicate semantics stabilize |
| Dance contract / discovery / execution-alignment work      | unit tests, schema/wrapper tests, lookup tests, dispatch seam tests          | broad runtime-binding or end-to-end execution tests before activation and semantic validation are in scope |
| Dance semantic / activation / migration work               | semantic integration tests, targeted activation tests, migration/regression tests | broad dynamic-loading or end-to-end runtime tests before the static execution posture is stable   |
| Command `PRO` contract work                                | wire/domain seam tests, result mapping tests, runtime-shared-type adoption tests | descriptor-bound routing tests before command descriptor anchoring exists                         |
| Command `PRS` descriptor/routing work                      | command descriptor lookup tests, lifecycle policy tests, static routing tests | dynamic command implementation tests; Commands should not absorb query/dance semantics            |
| TS SDK realignment                                         | public/internal boundary tests, result-decoder tests, descriptor-handle tests | DAHN-owned duplicate descriptor APIs or direct SDK-internal imports                               |
| DAHN shell / adapter seams                                 | seam tests, adapter-boundary tests, registry/loader tests                    | semantic rendering tests before TS descriptor/bound-reference surfaces are ready                  |
| Dynamic binding / advanced runtime work                    | targeted integration tests, runtime contract tests, end-to-end binding tests | none once those runtime contracts are intentionally in scope                                      |

### Dance-Specific Guidance

For the dance track, testing should generally tighten in this order:

- Dance PRO1 / delivered baseline:
  - preserve the already-delivered invocation/result envelope coverage
  - do not reopen its scope merely to absorb later design simplifications

- Dance PR2:
  - schema import tests
  - wrapper/contract tests
  - request/response relationship-shape tests
  - no broad execution-framework integration tests yet

- Dance PR3:
  - descriptor-affordance lookup tests
  - inherited/effective lookup tests
  - request/response metadata discovery tests

- Dance PR4:
  - `DanceInvocation` ingress tests
  - static execution-path seam tests
  - narrow integration tests where static host-local execution is the intended contract

- Dance PR5:
  - query/navigation dance contract tests
  - projection/result-shape tests
  - targeted common-runtime-path integration tests

- Dance PR6:
  - descriptor-semantic validation tests
  - operator/validation alignment tests
  - no dance-local semantic reinvention tests

- Dance PR7:
  - targeted activation/selection tests
  - runtime contract tests for implementation loading and eligibility

- Dance PR8:
  - migration/regression tests
  - old-world/new-world coexistence tests where temporary parallel buildout still exists

### Query-Specific Guidance

For the query track, testing should generally tighten in this order:

- Query PRO1:
  - unit tests
  - runtime shared type family tests
  - result-shape normalization tests
  - projection-shape boundary tests confirming that `BaseValue` / `Row` / `RowSet` are not overread as the full intermediate execution model
  - bound-first tests around `HolonReference` and `BoundHolonCollection`

- Query PRO2:
  - envelope/contract tests
  - compatibility tests for new query request/result shapes
  - contract-path tests preserving a clean seam between materialized request/result shapes and bound-first internal execution state

- Query PRO3:
  - navigation algebra contract tests
  - operand flow tests
  - narrow interpreter/substrate tests

- Query PRS1:
  - descriptor-backed structural lookup tests
  - declared/inverse relationship distinction tests
  - seam tests around `ResolvedType` as internal support only

- Query PRS2:
  - descriptor-backed predicate/operator tests
  - unsupported-operator error tests

- Query PRS3+:
  - progressively richer distributed, planner, and declarative integration tests only once those contracts are intentionally in scope

### Command-Specific Guidance

For the command track, testing should generally tighten in this order:

- Command PRO1:
  - unit tests
  - payload/result disposition tests
  - `BoundHolonCollection` result/operand posture tests
  - compatibility tests for bridge forms such as `DanceRequest`, `QueryExpression`, and `HolonCollection`

- Command PRO2:
  - wire/domain binding tests
  - result mapping tests
  - dependency-boundary tests proving `map_commands_runtime` does not depend on `map_commands_wire`
  - no descriptor-routing tests yet

- Command PRS1:
  - command schema anchor tests
  - `CommandDescriptor` wrapper tests
  - `CommandLifecyclePolicy` rename and metadata tests

- Command PRS2:
  - `HolonDescriptor` / `TransactionDescriptor` command lookup tests
  - inherited/effective affordance lookup tests

- Command PRS3+:
  - descriptor-bound routing tests
  - lifecycle policy enforcement tests
  - TS/DAHN affordance compatibility tests once descriptor-discovered commands are intended to be executable

### Issue-Level Rule

Each issue / PR spec should explicitly state:

- whether unit tests are sufficient
- whether seam/boundary tests are required
- whether integration tests are required
- whether framework-backed integration tests are appropriate yet
- what dependencies must land before stronger integration tests should be added

This prevents teams from using tests to harden behavior that the roadmap still intends to keep provisional.

---

## Wave 0 — Structural Groundwork

### Goal
Establish the minimum structural substrate that everything else can safely build on.

### Major Deliverables
- Descriptor PR1 / Issue 453:
    - runtime descriptor wrappers
    - `Descriptor` trait
    - `TypeHeader`
    - `ReadableHolon::holon_descriptor()`
    - inheritance traversal helpers
- DAHN PR 1:
    - contracts and skeleton
- DAHN PR 2:
    - visualizer registry and minimal canvas
- DAHN PR 4:
    - trivial selector
- DAHN PR 8 (partial):
    - boundary and seam tests that do not require real descriptor semantics

### Why This Wave Exists
This wave prevents downstream work from hardcoding:

- inheritance flattening
- structural lookup
- transport leakage into TS
- UX/runtime seams that will later fight the descriptor model

| Work Item                       | Can Start   | Blocked By |
|---------------------------------|-------------|------------|
| Descriptor PR1                  | immediately | none       |
| DAHN PR1                        | immediately | none       |
| DAHN PR2                        | immediately | none       |
| DAHN PR4                        | immediately | none       |
| DAHN PR8 (boundary-only subset) | immediately | none       |

### Exit Criteria
- thin runtime descriptor wrappers exist
- flattened structural traversal exists
- no downstream stream needs to invent its own structural lookup foundation
- DAHN shell work exists without semantic coupling

---

## Wave 1 — Schema-Backed Descriptor Surface

### Goal
Make descriptor structure real and consumable rather than merely wrapped.

### Major Deliverables
- Descriptors Phase 2:
    - schema-backed accessors for `HolonDescriptor`, `PropertyDescriptor`, `RelationshipDescriptor`
    - declared/inverse relationship accessors
- tests against authoritative core schema
- explicit handling of current-schema deficiencies
- Query runtime shared type and envelope prep
- command contract inventory and bridge-type disposition prep

### Why This Wave Exists
Wave 0 gives wrappers and traversal. Wave 1 gives real usable structure.

This is the point where downstream systems can stop saying “in principle descriptors will provide this” and start depending on:

- property lookup
- relationship lookup
- inverse relationship lookup
- effective flattened structural access

| Work Item                                                        | Can Start           | Blocked By     |
|------------------------------------------------------------------|---------------------|----------------|
| Descriptor Phase 2                                               | after Wave 0 starts | Descriptor PR1 |
| Query PRO1 prep — Runtime Shared Types Foundation Alignment      | during Wave 1       | none           |
| Query PRO2 prep — Query Envelope and Contract Stabilization      | during Wave 1       | Query PRO1     |
| Dance PRO1 prep — Shared Invocation / Result Envelope Foundation | during Wave 1       | none           |
| Command PRO1 prep — IPC Contract and Runtime Shared Type Alignment | during Wave 1     | runtime shared type foundation |
| Command PRO2 prep — Wire / Domain Binding and Result Mapping Stabilization | during Wave 1 | Command PRO1 |
| DAHN adapter design refinement                                   | during Wave 1       | Descriptor PR1 |

### Exit Criteria
- effective structural descriptor access is real
- schema-backed descriptor surface is test-backed
- downstream consumers can target descriptors as an actual API surface

---

## Wave 2 — Descriptor-Owned Value Semantics

### Goal
Move the first real semantics into descriptors through `ValueDescriptor`.

### Major Deliverables
- Descriptors Phase 3:
    - `is_valid()`
    - `supports_operator()`
    - `apply_operator()`
- initial operator semantics implemented in Rust
- no global operator registry
- compatibility with future schema-backed operators

### Why This Wave Exists
This is the semantic keystone for:  

- validation
- query predicates
- query-builder affordances
- dance input checking and filter-like behavior
- DAHN property rendering and future editing hints

Without this wave, every other stream risks inventing its own:  

- value validation logic
- operator support logic
- comparison semantics

| Work Item                                                               | Can Start                         | Blocked By                         |
|-------------------------------------------------------------------------|-----------------------------------|------------------------------------|
| Descriptor Phase 3                                                      | after Wave 1 is sufficiently real | Descriptor PR1, Descriptor Phase 2 |
| Validation PR3 prep — Nursery Bounded Descriptor Rule Integration       | during Wave 2                     | Descriptor Phase 2                 |
| Query PRO3 prep — Navigation Algebra Contract Stabilization             | during Wave 2                     | Query PRO1, Descriptor Phase 2     |
| Query PRS2 prep — Descriptor-Owned Predicate and Operator Alignment     | during Wave 2                     | Descriptor Phase 2                 |
| Dance PR2 prep — Core Schema and Contract Alignment                     | during Wave 2                     | Dance PRO1, core schema governance |
| Dance PR6 prep — Descriptor-Semantic Validation                        | during Wave 2                     | Descriptor Phase 2                 |
| Command PRS1 prep — Command Descriptor Schema Anchoring                 | during Wave 2                     | Descriptor Phase 2                 |
| Command PRS2 prep — Descriptor-Afforded Command Discovery               | during Wave 2                     | Command PRS1                       |
| DAHN property presentation heuristics                                   | during Wave 2                     | Descriptor Phase 2                 |

### Exit Criteria
- `ValueDescriptor` is the accepted home of value semantics
- validation and query streams can both target one semantic source
- no new freestanding operator subsystem is needed elsewhere

---

## Wave 3 — Validation Integration

### Goal
Make validation consume descriptor semantics while preserving PVL / Nursery boundaries.

### Major Deliverables
- Validation PR1 / Phase 1 — Structural Rule Classification and Adoption Boundary:
    - explicit classification of which descriptor-defined rules live in:
        - PVL
        - Nursery
        - higher layers
    - descriptor-driven validation adoption boundary
- Validation PR2 / Phase 2 — PVL Closed-World Descriptor Rule Integration:
    - structural descriptor-backed rules routed into PVL where bounded and reconstructible
    - runtime checks for descriptor graph invalidity where PVL legitimately depends on descriptor-backed structure
- Validation PR3 / Phase 3 — Nursery Bounded Descriptor Rule Integration:
    - bounded descriptor-driven validation in Nursery
    - required / warning / deferred categorization in practice
- Validation PR4 / Phase 4 — Validation Flow and Outcome Integration:
    - descriptor-driven validation adoption plan at commit/runtime boundaries

### Why This Wave Exists
The updated validation architecture says:  

- descriptors own semantics
- validation layers own evaluation authority

So validation should start consuming descriptors as soon as Waves 1 and 2 make that possible.

| Work Item                                | Can Start           | Blocked By                             |
|------------------------------------------|---------------------|----------------------------------------|
| Validation PR1 / Phase 1 — Structural Rule Classification and Adoption Boundary | during Wave 3 | Descriptor Phase 2 |
| Validation PR2 / Phase 2 — PVL Closed-World Descriptor Rule Integration | after Wave 1 starts | Validation PR1 / Phase 1, Descriptor Phase 2 |
| Validation PR3 / Phase 3 — Nursery Bounded Descriptor Rule Integration | after Wave 2 starts | Validation PR1 / Phase 1, Descriptor Phase 2, Descriptor Phase 3 |
| Validation PR4 / Phase 4 — Validation Flow and Outcome Integration | after Wave 2 starts | Validation PR2 / Phase 2, Validation PR3 / Phase 3 |
| Validation PR5 prep / Phase 5 — Cross-Subsystem Semantic Convergence | during Wave 3 | Validation PR2 / Phase 2, Validation PR3 / Phase 3 |

### Exit Criteria
- validation no longer trends toward a separate permanent semantic rule system
- descriptor-owned rules are classified by evaluation layer
- bounded vs open-world enforcement boundaries remain explicit

---

## Wave 4 — Query Runtime Shared Type, Contract, and Structural Semantics

### Goal
Stabilize the new query runtime shared type, envelope, and execution substrate posture while continuing the descriptor-dependent structural and semantic query work.

### Major Deliverables
- Query PRO1 / Phase 1 — Runtime Shared Types and Envelope Foundation:
    - query adoption of the canonical runtime shared type family
    - primary bound posture around `HolonReference`, `BoundHolonCollection`, and contract-significant `SmartReference`
    - secondary materialized projection posture around `BaseValue`, `Row`, `RowSet`, and later `Record` / `RecordStream`
    - explicit normalization away from legacy `Node` / `NodeCollection` / `QueryPathMap`
- Query PRO2 / Phase 2 — Query Envelope and Contract Stabilization:
    - query envelope and contract posture for the new query substrate
    - long-term query result-shape direction distinct from the legacy path
    - end-to-end contract path from TS through Commands to the shared substrate boundary
- Query PRO3 / Phase 3 — Navigation Algebra Contract Stabilization:
    - navigation/query contract stabilization over bound-first execution:
        - `HolonReference`
        - `BoundHolonCollection`
        - `BaseValue`
        - `Row`
        - `RowSet`
        - path toward `Record` / `RecordStream`
    - minimal navigation algebra as the execution substrate
- Query PRS1 / Phase 2 — Parallel Descriptor-Backed Structural Resolution:
    - query runtime alignment around descriptor-backed structure
    - `ResolvedType` / structural projection reframed as internal support, not caller-facing semantic truth
- Query PRS2 / Phase 4 — Descriptor-Owned Predicate and Operator Alignment:
    - descriptor-aware navigation/filter execution rules
    - no query-owned permanent operator semantic subsystem
- Query PRS3 / Phase 5 — Distributed Descriptor-Consistent Query Semantics:
    - distributed query behavior that preserves descriptor meaning under sovereignty constraints

### Why This Wave Exists
Queries need two things in parallel:

- a primary holon-bound runtime shared type posture for deferred-projection execution
- an earlier-stabilizing contract shape for runtime shared types, envelopes, and execution substrate
- descriptor-backed structural and predicate semantics that keep query meaning aligned with the descriptor model

This wave makes sure:

- algebra remains the execution substrate
- descriptors remain the semantic source
- bound-first execution remains the primary intermediate representation
- materialized projection models are ready for reuse in dance refactor, SDKs, and DAHN without becoming the full internal execution model

| Work Item                                     | Can Start           | Blocked By         |
|-----------------------------------------------|---------------------|--------------------|
| Query PRO1 / Phase 1 — Runtime Shared Types and Envelope Foundation | after Wave 1 starts | runtime shared type foundation |
| Query PRO2 / Phase 2 — Query Envelope and Contract Stabilization | after Wave 1 starts | Query PRO1 |
| Query PRO3 / Phase 3 — Navigation Algebra Contract Stabilization | after Wave 1 starts | Query PRO1, Query PRO2, Query PRS1 / Phase 2, Descriptor Phase 2 |
| Query PRS1 / Phase 2 — Parallel Descriptor-Backed Structural Resolution | after Wave 1 starts | Descriptor Phase 2 |
| Query PRS2 / Phase 4 — Descriptor-Owned Predicate and Operator Alignment | after Wave 2 starts | Query PRS1 / Phase 2, Query PRO3 / Phase 3, Descriptor Phase 3 |
| Query PRS3 / Phase 5 — Distributed Descriptor-Consistent Query Semantics | during Wave 4 | Query PRO3 / Phase 3, Query PRS2 / Phase 4 |
| Query PRS4 prep / Phase 5 — Planner Algebra Foundation | during Wave 4 | Query PRO3 / Phase 3, Query PRS2 / Phase 4 |

### Exit Criteria
- query execution no longer owns value semantics independently
- descriptor-aware algebra is the clear direction
- bound-first runtime shared type posture is established as the primary intermediate representation
- query contract shapes are stable enough for command, dance, SDK, and DAHN reuse
- materialized projection forms are available without forcing eager row-shaped internal execution

---

## Wave 5 — Dance Holonic Contract and Execution Alignment

### Goal
Bring the post-`PRO1` dance implementation into conformance with the revised holonic design, from schema alignment through static execution, query/navigation dances, activation, and old-world drawdown.

### Major Deliverables
- Dance PRO1 / delivered baseline:
    - early `DanceInvocation` / dance-envelope foundation remains delivered and fixed in scope
- Dance PR2 — Core Schema and Contract Alignment:
    - `DanceType.RequestType -> HolonType`
    - `DanceInvocation.Request -> HolonType`
    - `DanceResponseType.ResponseBody -> HolonType`
    - `Projection` as the shell for value-shaped request/response/projection records
    - old-world dance schema surfaces retained only as deprecated descriptors during parallel buildout
- Dance PR3 — Descriptor-Afforded Dance Discovery:
    - dance lookup through `HolonDescriptor`
    - inherited/effective dance affordances through flattened `Extends`
    - no second dance registry
- Dance PR4 — Command Ingress and Static Execution Alignment:
    - `DanceV2` ingress through `DanceInvocation`
    - `ForDance`-based implementation binding
    - static host-local execution posture over the common runtime surface
- Dance PR5 — Query and Navigation Dances:
    - query/navigation operations delivered as ordinary dances
    - `Projection` / transient projection-shape posture for value-based request or result bodies
    - common runtime surface for query-like and side-effecting dances
- Dance PR6 — Descriptor-Semantic Validation:
    - descriptor-owned validation/operator semantics consumed by dances
    - no dance-local semantic duplication
- Dance PR7 — Dynamic Implementation Activation and Selection:
    - dynamic activation/loading posture
    - ABI-compat, integrity, and policy-eligibility checks
    - implementation selection by dance, not by target-type-specific method dispatch
- Dance PR8 — Test Migration and Old-World Drawdown:
    - convert tests to the new-world dance model as support becomes real
    - keep temporary old-world surfaces only where still needed for parallel buildout

### Why This Wave Exists
The revised dance design simplified the model substantially:

- `DanceInvocation` and successful dance responses are ordinary transient holons
- request and response bodies are reached by holon reference
- descriptor-backed affordance lookup owns dance discovery
- query/navigation operations are ordinary dances
- old-world/new-world coexistence is handled by parallel buildout and test migration, not runtime translation

That simplification removes the old `PRO2` / `PRO3` / `PRS` split. The remaining work is better represented as one post-`PRO1` delivery sequence whose middle phases depend on descriptors, commands, and query/runtime shared types, but whose target design is now one coherent holonic contract.

| Work Item                                       | Can Start           | Blocked By                                                |
|-------------------------------------------------|---------------------|-----------------------------------------------------------|
| Dance PRO1 / delivered baseline                                  | complete            | none                                                      |
| Dance PR2 — Core Schema and Contract Alignment                   | after Wave 1 starts | Dance PRO1, core schema governance                        |
| Dance PR3 — Descriptor-Afforded Dance Discovery                  | after Wave 1 starts | Dance PR2, Descriptor Phase 2                             |
| Dance PR4 — Command Ingress and Static Execution Alignment       | after Wave 1 starts | Dance PR2, Dance PR3, Command PRO2                        |
| Dance PR5 — Query and Navigation Dances                          | after Wave 4 starts | Dance PR2, Dance PR3, Dance PR4, Query PRO3, Query PRS1 / Phase 2 |
| Dance PR6 — Descriptor-Semantic Validation                       | after Wave 2 starts | Dance PR2, Dance PR3, Descriptor Phase 3, Validation PR3 / Phase 3 |
| Dance PR7 — Dynamic Implementation Activation and Selection      | after Wave 5 core phases stabilize | Dance PR4, Dance PR5, Dance PR6                |
| Dance PR8 — Test Migration and Old-World Drawdown                | after Wave 5 core phases stabilize | Dance PR4, Dance PR5, Dance PR6, Dance PR7     |

### Exit Criteria
- new-world dance schema and wrappers match the revised holonic contract
- dances are discovered from descriptors through `HolonDescriptor`
- `DanceInvocation` and the `DanceV2` ingress path are aligned
- query/navigation operations can execute as ordinary dances
- dance code is not a second semantic home for filtering or validation
- dynamic activation/selection is available without reintroducing target-type-specific dispatch
- test posture is migrating away from old-world dance surfaces

---

## Wave 6 — Command IPC Contract, Descriptor Anchoring, and Routing

### Goal
Align the MAP Commands IPC contract with runtime shared types, then bring commands into the descriptor-owned behavior model without making Commands the semantic home of query or dance behavior.

### Major Deliverables
- Command PRO1 — IPC Contract and Runtime Shared Type Alignment:
    - command payload/result disposition
    - plural command result convergence on `BoundHolonCollection`
    - bridge-type classification for `DanceRequest`, `QueryExpression`, `HolonCollection`, and direct `Holon`
- Command PRO2 — Wire / Domain Binding and Result Mapping Stabilization:
    - adapter-owned wire-to-domain binding
    - domain-to-wire result mapping
    - no `*Wire` leakage below the binding seam
- Command PRS1 — Command Descriptor Schema Anchoring:
    - `CommandType`
    - schema-backed `CommandDescriptor`
    - `AffordsCommand`
    - `CommandLifecyclePolicy` rename for lifecycle metadata
- Command PRS2 — Descriptor-Afforded Command Discovery:
    - `HolonDescriptor`, `HolonSpaceDescriptor`, and `TransactionDescriptor` command lookup
    - effective inherited command affordance discovery
- Command PRS3 — Descriptor-Bound Runtime Routing and Policy Enforcement:
    - lifecycle policy enforcement through descriptor-resolved command metadata
    - static Rust-local command dispatch anchored in descriptor lookup
- Command PRO3 — Query and Dance Ingress Contract Convergence:
    - `DanceV2(DanceInvocation)` as new-world dance ingress
    - `QueryExpression` scoped as transitional query bridge payload
- Command PRS4 — Dispatch Redistribution and TS / DAHN Readiness:
    - central dispatch shrinks where descriptor-local static routing is ready
    - command affordances become consumable by TS and DAHN

### Why This Wave Exists
Commands are less critical than value semantics for validation/query coherence, but they matter for:

- runtime consistency
- DAHN affordance surfaces
- future TS API alignment
- keeping behavior discovery uniform
- preserving the single IPC ingress and wire/domain sandwich model while descriptor-owned behavior discovery expands

| Work Item                                           | Can Start                   | Blocked By                                      |
|-----------------------------------------------------|-----------------------------|-------------------------------------------------|
| Command PRO1 / runtime shared type alignment        | after Wave 1 starts         | runtime shared type foundation                  |
| Command PRO2 / wire-domain binding and result mapping | after Command PRO1 starts | Command PRO1                                    |
| Command PRS1 / command descriptor schema anchoring  | after Wave 1                | Descriptor Phase 2                              |
| Command PRS2 / descriptor-afforded command discovery | after Command PRS1         | Command PRS1, descriptor inherited lookup       |
| Command PRS3 / descriptor-bound routing and policy  | after Command PRS2          | Command PRO2, Command PRS2                      |
| Command PRO3 / query and dance ingress convergence  | after relevant query/dance contract work | Query PRO2, Dance PR4, Command PRO2 |
| Command PRS4 / dispatch redistribution and TS / DAHN readiness | after Command PRS3 | Command PRS3, TS descriptor client planning     |
| DAHN affordance menu expansion for commands         | after command descriptor surface exists | Descriptor command routing, TS realignment prep |

### Exit Criteria
- commands have descriptor ownership
- command payloads and results align with runtime shared types
- wire/domain separation remains intact
- bridge payloads are isolated and migration-scoped
- central dispatch is shrinking where descriptor-local routing is ready
- behavior discovery becomes more uniform across commands and dances

---

## Wave 7 — TypeScript Interface Realignment

### Goal
Expose descriptor-oriented surfaces to TS so DAHN and other clients can consume the real model.

### Major Deliverables
- Descriptors Phase 7:
    - TS descriptor clients
    - descriptor-oriented public SDK shape
- thin descriptor handles
- public SDK `HolonReference` and `BoundHolonCollection` contract surfaces
- `DanceInvocation` / `DanceV2` public SDK path
- query API aligned toward the Query PRO2 contract rather than legacy `QueryExpression`
- command result decoding aligned with runtime shared type posture
- no TS-side inheritance flattening
- no TS semantic shadow model

### Why This Wave Exists
Until this wave lands, TS/DAHN can only partially align with the descriptor model.

This is the real bridge from core semantics to:

- DAHN
- SDK consumers
- future query builders
- UX surfaces

| Work Item                        | Can Start                                         | Blocked By                                 |
|----------------------------------|---------------------------------------------------|--------------------------------------------|
| TS descriptor client design      | during Wave 6                                     | Descriptor Phase 2                         |
| TS runtime shared type / result mapping realignment | during Wave 6                    | Command PRO1, Command PRO2, runtime shared type foundation |
| TS implementation realignment    | after descriptor/core semantics are stable enough | Descriptor Phases 2-6, Command PRO/PRS early tracks |
| DAHN real adapter implementation | after TS realignment begins                       | TS descriptor surfaces, bound-reference SDK surfaces |
| Query-builder TS/API design      | after TS realignment begins                       | TS descriptor surfaces, Descriptor Phase 3 |

### Exit Criteria
- TS no longer needs to guess descriptor meaning
- DAHN and other clients can consume thin descriptor handles directly
- public SDK plural holon-backed results converge on `BoundHolonCollection`
- legacy bridge payloads such as `DanceRequest` and `QueryExpression` are not the long-term public SDK center
- no TS-side inheritance or operator semantics are invented

---

## Wave 8 — Real DAHN Integration

### Goal
Turn the DAHN shell into a genuinely descriptor-driven experience layer.

### Major Deliverables
- DAHN PR 3:
    - SDK-backed adapter seam
    - public SDK `HolonReference` / `BoundHolonCollection` consumption
- DAHN PR 5:
    - affordance hierarchy and action menu
    - `AffordanceNode[]` built from command and dance descriptor handles
- DAHN PR 6:
    - generic `HolonNodeVisualizer`
- DAHN PR 7:
    - host UI mount and bring-up
- DAHN PR 8:
    - full hardening and boundary tests

### Why This Wave Exists
Earlier DAHN work can land as scaffolding, but real descriptor-driven rendering and affordance presentation should wait until TS descriptor and bound-reference surfaces exist.

| Work Item                    | Can Start                       | Blocked By                                        |
|------------------------------|---------------------------------|---------------------------------------------------|
| DAHN PR3                     | after Wave 7 begins             | TS descriptor surfaces, bound-reference SDK surfaces |
| DAHN PR5 UI shell            | earlier as scaffold             | none                                              |
| DAHN PR5 semantic completion | later                           | Descriptor command/dance surfaces, TS realignment |
| DAHN PR6                     | after Wave 7 begins             | TS descriptor surfaces, Descriptor Phase 2        |
| DAHN PR7                     | after PR3 and PR6 are real      | DAHN PR3, DAHN PR6                                |
| DAHN PR8 full                | after semantic DAHN seams exist | DAHN PR3-7                                        |

### Exit Criteria
- DAHN can render real descriptor-defined properties, relationships, and affordances
- property presentation is value-type-aware
- affordance surfaces reflect descriptor-discovered commands and dances
- DAHN's default data posture is bound references and bound collections, not materialized query rows
- no internal SDK leakage into DAHN

---

## Wave 9 — Advanced Query Evolution

### Goal
Layer in the more ambitious query/runtime features after the semantic foundations are stable.

### Major Deliverables
- Query PRS4 / Phase 5 — Planner Algebra Foundation:
    - query planner algebra expansion
    - descriptor-aware logical operator posture
- Query PRS5 / Phase 6 — Declarative Compilation and Optimization Evolution:
    - declarative OpenCypher/GQL compilation
    - physical planning and optimization
- schema-backed operator metadata
- richer command metadata

### Why This Wave Exists
These are important, but they should not be allowed to destabilize the semantic base.

They depend on having:

- descriptor-owned semantics
- stable query/runtime shared type and envelope models
- stable TS/UX surfaces

| Work Item                            | Can Start                      | Blocked By                                         |
|--------------------------------------|--------------------------------|----------------------------------------------------|
| Query PRS4 / Phase 5 — Planner Algebra Foundation | after Wave 4 | Query PRO3 / Phase 3, Query PRS2 / Phase 4, Query PRS3 / Phase 5 |
| Query PRS5 / Phase 6 — Declarative Compilation and Optimization Evolution | after planner substrate exists | Query PRS4 / Phase 5 |
| Schema-backed operator metadata      | after Descriptor Phase 3       | Descriptor operator runtime                        |
| Richer command metadata              | after Descriptor Phase 6       | Command descriptor routing                         |

### Exit Criteria
- declarative query evolution builds on descriptor-aware algebra rather than reintroducing semantic duplication
- advanced runtime features no longer pressure teams to invent parallel models

---

# Cross-Wave Critical Dependencies

## Absolute Critical Path
1. Descriptor PR1
2. Descriptor Phase 2
3. Descriptor Phase 3
4. Validation PR1-PR4 / Phases 1-4
5. Query PRO1-PRO3 + PRS1-PRS3
6. Dance PR2-PR8
7. Command PRO/PRS early tracks
8. TypeScript interface realignment
9. Real DAHN integration

## Key Semantic Dependency Rules
- Validation PR2 / Phase 2 should not finalize before descriptor resolution is bounded and reconstructible enough for PVL-safe use.
- Validation PR3 / Phase 3 should not finalize before `ValueDescriptor` semantics exist.
- Query PRS2 / Phase 4 should not finalize before `ValueDescriptor` operators exist.
- Query PRS4 / Phase 5 should not harden before navigation algebra contracts and descriptor-aware predicate semantics are stable.
- Dances should not finalize request/result structures before the runtime shared type foundation and query contract posture stabilize.
- Dance PR6 should not finalize before `ValueDescriptor` semantics exist.
- Commands should not make `DanceRequest`, `QueryExpression`, or `HolonCollection` the long-term public contract center.
- TS SDK work should not expose internal command builders, wire types, or DAHN-local descriptor mirrors.
- DAHN should not finalize real adapter/visualizer semantics before TS descriptor and bound-reference surfaces exist.
- Dance PR7 should not start before Dance PR4 static execution alignment and Dance PR6 semantic validation are real.

---

# Parallel Work Summary

## Safely Parallel Early
- Descriptor PR1
- DAHN PR1, PR2, PR4
- Validation PR1 / Phase 1 classification prep
- Query PRO1 issue definition
- Query PRO2 issue definition
- Query PRO1 / runtime shared type foundation alignment
- Query PRO2 / envelope and contract stabilization
- Query PRS1 issue definition
- Dance PR2 issue definition
- Command PRO1 / command runtime shared type adoption
- Command PRO2 / wire-domain seam stabilization
- dance design sprint follow-through
- DAHN PR8 boundary-only subset

## Parallel Once Descriptor Structure Exists
- Validation PR1 / Phase 1 classification work
- Validation PR2 / Phase 2 PVL integration
- Query PRS1 / parallel structural resolution
- Query PRO3 / navigation algebra contract work
- Dance PR3 / descriptor-afforded discovery work
- Dance PR4 / static execution alignment prep
- Dance PR6 / semantic validation prep
- Command PRS1 / command descriptor schema anchoring
- Command PRS2 / descriptor-afforded command discovery
- TS descriptor client design

## Parallel Once TS Realignment Starts
- DAHN PR3
- DAHN PR6
- query-builder/client API design
- DAHN affordance hierarchy work using `AffordanceNode[]`

---

# Recommended Execution Order

## Recommended Named Waves
1. Structural Groundwork
2. Schema-Backed Descriptor Surface
3. Descriptor-Owned Value Semantics
4. Validation Integration
5. Query Runtime Shared Type, Contract, and Structural Semantics
6. Dance Holonic Contract and Execution Alignment
7. Command IPC Contract, Descriptor Anchoring, and Routing
8. TypeScript Interface Realignment
9. Real DAHN Integration
10. Advanced Query Evolution

## Short Practical Reading
If we want the fewest reversals and the least duplicated logic, the safest sequence is:

`Descriptors 1-3 -> Validation PR1-PR4 + Query PRO/PRS early tracks -> Dance PR2-PR6 + Command PRO/PRS early tracks -> TS realignment -> DAHN -> Dance PR7-PR8 + Query PRS4-PRS5`

That sequence keeps semantic ownership centralized and lets each later wave consume real descriptor behavior rather than speculative placeholders.
