# Descriptor-Driven MAP Implementation Milestone Plan (v1.3)

This document is the synthesized cross-component implementation roadmap for the current descriptor-driven MAP architecture.

Its purpose is to translate several component-level design specs and implementation plans into one dependency-aware execution sequence, so that work across descriptors, validation, queries, dances, commands, TypeScript surfaces, and DAHN can proceed without duplicated semantics, premature hardening, or avoidable rework.

In particular, this plan synthesizes across:

- the descriptor design and descriptor implementation plan
- the validation architecture and dependency gravity model
- the query architecture and query implementation plan
- the dance design and dance implementation plan
- the DAHN specs, blueprint, and implementation plan

Rather than replacing those component documents, this plan coordinates them. It identifies which capabilities are foundational, which downstream streams can begin safely in parallel, and which work must wait until descriptor-owned structure or semantics are real.

The guiding principle is:

- descriptors are the semantic root
- validation, queries, dances, and DAHN should consume descriptor semantics rather than invent parallel systems
- implementation should separate structural foundations from semantic behavior and from TS / UX integration
- within the query stream, the Binding Layer is the primary intermediate representational layer for deferred-projection execution
- `BaseValue` / `Row` / `RowSet` should be read primarily as shared materialized contract and projection shapes rather than as the full internal query substrate

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
| Wave 1 — Schema-Backed Descriptor Surface                   |            18 | 15-22 | Medium-Low | Now also carries early `Query PRO1/PRO2` and `Dance PRO1` prep alongside Descriptor PR2 and DAHN PR3a.                         |
| Wave 2 — Descriptor-Owned Value Semantics                   |            20 | 15-24 | Low        | Now also carries early `Query PRO3` and `Dance PRO2/PRO3` prep in addition to descriptor semantic work.                        |
| Wave 3 — Validation Integration                             |            13 | 10-16 | Low-Medium | Validation layering is conceptually clear, but implementation depends heavily on what Descriptor Phase 3 actually delivers.     |
| Wave 4 — Query Contract Stabilization and Structural Semantics |         20 | 16-24 | Low-Medium | Broader than before because it now includes both `PRO` contract work and `PRS` semantic work, but the split reduces ambiguity. |
| Wave 5 — Dance Contract Stabilization and Descriptor Affordances |       20 | 15-23 | Low-Medium | Still substantial, but clearer now that envelope/ABI stabilization is separated from descriptor-dependent dance semantics.      |
| Wave 6 — Command Descriptor Anchoring and Routing           |            13 |  8-16 | Low        | Smaller than Waves 4-5 overall, but still contract-heavy and sensitive to descriptor-shape decisions.                           |
| Wave 7 — TypeScript Interface Realignment                   |            21 | 16-26 | Low        | This is the major Rust-to-TS contract bridge and is likely to surface integration friction not yet visible.                     |
| Wave 8 — Real DAHN Integration                              |            18 | 13-21 | Low        | Depends on TS descriptor surfaces and multiple prior DAHN PRs, so scope is visible but not yet stable.                          |
| Wave 9 — Dynamic Dance Binding and Advanced Query Evolution |            22 | 17-30 | Low        | Still high-risk, but somewhat narrower now that earlier operand/envelope and contract work is no longer implicitly deferred.    |

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
| Query `PRO` contract work                                  | unit tests, operand tests, envelope/contract tests, compatibility tests      | descriptor-semantic, planner, or declarative integration tests before the contract substrate stabilizes |
| Query `PRS` semantic work                                  | unit tests, descriptor-aware execution tests, semantic seam tests            | declarative/planner integration tests before navigation algebra and predicate semantics stabilize |
| Dance `PRO` contract work                                  | unit tests, envelope tests, ABI/contract tests, operand-alignment tests      | broad dance-framework integration tests before dispatch and descriptor semantics are in scope     |
| Dance `PRS` semantic / dispatch work                       | unit tests, lookup tests, dispatch seam tests                                | broad runtime-binding or end-to-end dynamic execution tests before those contracts are in scope   |
| DAHN shell / adapter seams                                 | seam tests, adapter-boundary tests, registry/loader tests                    | semantic rendering tests before TS descriptor surfaces are ready                                  |
| Dynamic binding / advanced runtime work                    | targeted integration tests, runtime contract tests, end-to-end binding tests | none once those runtime contracts are intentionally in scope                                      |

### Dance-Specific Guidance

For the dance track, testing should generally tighten in this order:

- Dance PRO1 / Phase 1:
  - unit tests
  - invocation/result envelope tests
  - no dance-framework integration tests yet

- Dance PRO2 / Phase 2:
  - unit tests
  - operand-alignment tests
  - ABI/contract tests

- Dance PRO3 / Phase 2:
  - cross-surface contract tests
  - SDK-facing contract compatibility tests where appropriate

- Dance PRS1 / Phase 3:
  - unit tests
  - descriptor-affordance lookup tests
  - inheritance/effective-lookup tests
  - no broad dance-framework integration tests yet

- Dance PRS2 / Phase 4:
  - unit tests
  - targeted static dispatch-path tests
  - narrow integration tests only where static descriptor-local dispatch is the intended contract

- Dance PRS3 / Phase 5:
  - add semantic integration tests where descriptor-owned validation/operator behavior is now in scope

- Dance PRS4+:
  - integration and end-to-end runtime tests become required because binding, governance, and runtime behavior are now part of the contract

### Query-Specific Guidance

For the query track, testing should generally tighten in this order:

- Query PRO1:
  - unit tests
  - operand family tests
  - result-shape normalization tests
  - projection-shape boundary tests confirming that shared operands are not overread as the full intermediate binding model

- Query PRO2:
  - envelope/contract tests
  - compatibility tests for new query request/result shapes
  - contract-path tests preserving a clean seam between materialized request/result shapes and the internal binding substrate

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
- Query binding-layer foundation prep

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
| Query binding-layer foundation prep                              | during Wave 1       | none           |
| Query PRO1 prep — Shared Operand Family Foundation               | during Wave 1       | none           |
| Query PRO2 prep — Query Envelope and Contract Stabilization      | during Wave 1       | Query PRO1     |
| Dance PRO1 prep — Shared Invocation / Result Envelope Foundation | during Wave 1       | none           |
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
| Dance PRO2 prep — Shared Operand and ABI Alignment                      | during Wave 2                     | Dance PRO1, Query PRO1             |
| Dance PRO3 prep — Cross-Surface Contract Stabilization                  | during Wave 2                     | Dance PRO2                         |
| Dance PRS3 prep — Descriptor-Semantic Validation and Operator Alignment | during Wave 2                     | Descriptor Phase 2                 |
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

## Wave 4 — Query Contract Stabilization and Structural Semantics

### Goal
Stabilize the new query operand/envelope contracts and execution substrate while continuing the descriptor-dependent structural and semantic query work.

### Major Deliverables
- Query binding-layer foundation:
    - primary intermediate representation posture for deferred-projection query execution
    - alignment to `HolonReference`, `SmartReference`, and relationship-cache affordances
    - `BoundHolonCollection` direction for named plural bindings
- Query PRO2 / Phase 2 — Query Envelope and Contract Stabilization:
    - query envelope and contract posture for the new query substrate
    - long-term query result-shape direction distinct from the legacy path
- Query PRO3 / Phase 3 — Navigation Algebra Contract Stabilization:
    - navigation/query operand stabilization above the Binding Layer:
        - `Value`
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

- a primary holon-bound Binding Layer for deferred-projection execution
- an earlier-stabilizing contract shape for operands, envelopes, and execution substrate
- descriptor-backed structural and predicate semantics that keep query meaning aligned with the descriptor model

This wave makes sure:

- algebra remains the execution substrate
- descriptors remain the semantic source
- the Binding Layer is the primary intermediate representation
- operand models are ready for reuse in dance refactor and DAHN as materialized contract/projection forms

| Work Item                                     | Can Start           | Blocked By         |
|-----------------------------------------------|---------------------|--------------------|
| Query binding-layer foundation                | after Wave 1 starts | none               |
| Query PRO2 / Phase 2 — Query Envelope and Contract Stabilization | after Wave 1 starts | Query PRO1 |
| Query PRO3 / Phase 3 — Navigation Algebra Contract Stabilization | after Wave 1 starts | Query PRO1, Query binding-layer foundation, Query PRS1 / Phase 2, Descriptor Phase 2 |
| Query PRS1 / Phase 2 — Parallel Descriptor-Backed Structural Resolution | after Wave 1 starts | Descriptor Phase 2 |
| Query PRS2 / Phase 4 — Descriptor-Owned Predicate and Operator Alignment | after Wave 2 starts | Query PRS1 / Phase 2, Query PRO3 / Phase 3, Descriptor Phase 3 |
| Query PRS3 / Phase 5 — Distributed Descriptor-Consistent Query Semantics | during Wave 4 | Query PRO3 / Phase 3, Query PRS2 / Phase 4 |
| Query PRS4 prep / Phase 5 — Planner Algebra Foundation | during Wave 4 | Query PRO3 / Phase 3, Query PRS2 / Phase 4 |

### Exit Criteria
- query execution no longer owns value semantics independently
- descriptor-aware algebra is the clear direction
- the Binding Layer is established as the primary intermediate representation
- query operand family is stable enough for dance reuse as materialized contract/projection forms

---

## Wave 5 — Dance Contract Stabilization and Descriptor Affordances

### Goal
Stabilize dance invocation/result contracts and shared operand/ABI posture while continuing the descriptor-dependent dance affordance and dispatch work.

### Major Deliverables
- Dance PRO1 / Phase 1 — Shared Invocation / Result Envelope Foundation:
    - canonical dance invocation envelope foundation
    - canonical dance result envelope foundation
- Dance PRO2 / Phase 2 — Shared Operand and ABI Alignment:
    - dance IO aligned with:
        - `Value`
        - `Row`
        - `RowSet`
        - `SmartReference`
        - later `RecordStream`
    - ABI-facing payload posture
- Dance PRO3 / Phase 2 — Cross-Surface Contract Stabilization:
    - query/dance/command envelope convergence posture
    - TS/SDK-facing contract stabilization direction
- Dance PRS1 / Phase 3 — Structural Descriptor-Affordance Surface:
    - descriptor-afforded dance discovery on `HolonDescriptor`
    - effective inherited dance lookup through flattened `Extends`
    - no global dance registry
- Dance PRS2 / Phase 4 — Static Descriptor-Local Dispatch Alignment:
    - static descriptor-local dance dispatch as the first execution posture
    - no conflation of dance existence with execution binding
- Dance PRS3 / Phase 5 — Descriptor-Semantic Validation and Operator Alignment:
    - no dance-local reinvention of validation/operator semantics

### Why This Wave Exists
Dance work now has two partially separable fronts:

- earlier contract stabilization for envelopes, operands, and ABI shape
- later descriptor-backed affordance, dispatch, and semantic alignment

That means this wave should carry both the earlier `PRO` contract work and the descriptor-dependent `PRS` work, without forcing them into one dependency bucket.

| Work Item                                       | Can Start           | Blocked By                                                |
|-------------------------------------------------|---------------------|-----------------------------------------------------------|
| Dance PRO1 / Phase 1 — Shared Invocation / Result Envelope Foundation         | after Wave 1 starts | none                                                      |
| Dance PRO2 / Phase 2 — Shared Operand and ABI Alignment                         | after Wave 2 starts | Dance PRO1 / Phase 1, Query PRO1                          |
| Dance PRO3 / Phase 2 — Cross-Surface Contract Stabilization                     | after Wave 2 starts | Dance PRO2 / Phase 2                                      |
| Dance PRS1 / Phase 3 — Structural Descriptor-Affordance Surface                 | after Wave 1 starts | Descriptor Phase 2                                        |
| Dance PRS2 / Phase 4 — Static Descriptor-Local Dispatch Alignment               | after Wave 1 starts | Descriptor PR1, Descriptor Phase 2, Dance PRS1 / Phase 3  |
| Dance PRS3 / Phase 5 — Descriptor-Semantic Validation and Operator Alignment    | after Wave 2 starts | Descriptor Phase 3, Dance PRO2 / Phase 2                  |
| Dance PRS4 prep / Phase 6 — Dynamic Implementation Binding                      | during Wave 5       | Dance PRS2 / Phase 4, Dance PRO2 / Phase 2                |

### Exit Criteria
- dances are semantically discovered from descriptors
- dance IO does not diverge from query/navigation structures
- dance code is not a second semantic home for filtering or validation

---

## Wave 6 — Command Descriptor Anchoring and Routing

### Goal
Bring commands into the same descriptor-owned behavior model.

### Major Deliverables
- Descriptors Phase 4:
    - `CommandDescriptor`
    - `AffordsCommand`
- Descriptors Phase 5:
    - descriptor-bound command routing
- Descriptors Phase 6:
    - dispatch redistribution away from central dispatch

### Why This Wave Exists
Commands are less critical than value semantics for validation/query coherence, but they matter for:

- runtime consistency
- DAHN affordance surfaces
- future TS API alignment
- keeping behavior discovery uniform

| Work Item                                   | Can Start                               | Blocked By                                      |
|---------------------------------------------|-----------------------------------------|-------------------------------------------------|
| Command schema anchor                       | after Wave 1                            | Descriptor Phase 2                              |
| Descriptor-bound command routing            | after command anchor exists             | Descriptor Phase 4                              |
| Dispatch redistribution                     | after routing is real                   | Descriptor Phase 5                              |
| DAHN affordance menu expansion for commands | after command descriptor surface exists | Descriptor command routing, TS realignment prep |

### Exit Criteria
- commands have descriptor ownership
- central dispatch is shrinking or gone
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
| TS implementation realignment    | after descriptor/core semantics are stable enough | Descriptor Phases 2-6                      |
| DAHN real adapter implementation | after TS realignment begins                       | TS descriptor surfaces                     |
| Query-builder TS/API design      | after TS realignment begins                       | TS descriptor surfaces, Descriptor Phase 3 |

### Exit Criteria
- TS no longer needs to guess descriptor meaning
- DAHN and other clients can consume thin descriptor handles directly
- no TS-side inheritance or operator semantics are invented

---

## Wave 8 — Real DAHN Integration

### Goal
Turn the DAHN shell into a genuinely descriptor-driven experience layer.

### Major Deliverables
- DAHN PR 3:
    - SDK-backed adapter seam
- DAHN PR 5:
    - affordance hierarchy and action menu
- DAHN PR 6:
    - generic `HolonNodeVisualizer`
- DAHN PR 7:
    - host UI mount and bring-up
- DAHN PR 8:
    - full hardening and boundary tests

### Why This Wave Exists
Earlier DAHN work can land as scaffolding, but real descriptor-driven rendering and affordance presentation should wait until TS descriptor surfaces exist.

| Work Item                    | Can Start                       | Blocked By                                        |
|------------------------------|---------------------------------|---------------------------------------------------|
| DAHN PR3                     | after Wave 7 begins             | TS descriptor surfaces                            |
| DAHN PR5 UI shell            | earlier as scaffold             | none                                              |
| DAHN PR5 semantic completion | later                           | Descriptor command/dance surfaces, TS realignment |
| DAHN PR6                     | after Wave 7 begins             | TS descriptor surfaces, Descriptor Phase 2        |
| DAHN PR7                     | after PR3 and PR6 are real      | DAHN PR3, DAHN PR6                                |
| DAHN PR8 full                | after semantic DAHN seams exist | DAHN PR3-7                                        |

### Exit Criteria
- DAHN can render real descriptor-defined properties, relationships, and affordances
- property presentation is value-type-aware
- affordance surfaces reflect descriptor-discovered commands and dances
- no internal SDK leakage into DAHN

---

## Wave 9 — Dynamic Dance Binding and Advanced Query Evolution

### Goal
Layer in the later dance implementation phases and the more ambitious query/runtime features after the semantic foundations are stable.

### Major Deliverables
- Dance PRS4 / Phase 6 — Dynamic Implementation Binding:
    - dynamic dance implementation binding
    - executable binding metadata and selection posture
- Dance PRS5 / Phase 6 — Governance, Activation, and Advanced Runtime Evolution:
    - governance activation flows for dance implementations
    - active implementation resolution posture
- WASM / engine loading
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
- stable operand models
- stable dispatch ownership
- stable TS/UX surfaces

| Work Item                            | Can Start                      | Blocked By                                         |
|--------------------------------------|--------------------------------|----------------------------------------------------|
| Dance PRS4 / Phase 6 — Dynamic Implementation Binding | after Wave 5 semantic refactor | Dance PRS2 / Phase 4, Dance PRS3 / Phase 5, Dance PRO2 / Phase 2 |
| Dance PRS5 / Phase 6 — Governance, Activation, and Advanced Runtime Evolution | after dynamic model is defined | Dance PRS4 / Phase 6                                |
| Query PRS4 / Phase 5 — Planner Algebra Foundation | after Wave 4 | Query PRO3 / Phase 3, Query PRS2 / Phase 4, Query PRS3 / Phase 5 |
| Query PRS5 / Phase 6 — Declarative Compilation and Optimization Evolution | after planner substrate exists | Query PRS4 / Phase 5 |
| Schema-backed operator metadata      | after Descriptor Phase 3       | Descriptor operator runtime                        |
| Richer command metadata              | after Descriptor Phase 6       | Command descriptor routing                         |

### Exit Criteria
- dynamic behavior loading sits on top of descriptor affordances instead of replacing them
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
6. Dance PRO1-PRO3 + PRS1-PRS3
7. TypeScript interface realignment
8. Real DAHN integration

## Key Semantic Dependency Rules
- Validation PR2 / Phase 2 should not finalize before descriptor resolution is bounded and reconstructible enough for PVL-safe use.
- Validation PR3 / Phase 3 should not finalize before `ValueDescriptor` semantics exist.
- Query PRS2 / Phase 4 should not finalize before `ValueDescriptor` operators exist.
- Query PRS4 / Phase 5 should not harden before navigation algebra contracts and descriptor-aware predicate semantics are stable.
- Dances should not finalize request/result structures before query operand structures stabilize.
- Dance PRS3 / Phase 5 should not finalize before `ValueDescriptor` semantics exist.
- DAHN should not finalize real adapter/visualizer semantics before TS descriptor surfaces exist.
- Dynamic dance binding should not start before Dance PRS2 / Phase 4 static descriptor-local dispatch is real.

---

# Parallel Work Summary

## Safely Parallel Early
- Descriptor PR1
- DAHN PR1, PR2, PR4
- Validation PR1 / Phase 1 classification prep
- Query PRO1 issue definition
- Query PRO2 issue definition
- Query PRO1 / shared operand family foundation
- Query PRO2 / envelope and contract stabilization
- Query PRS1 issue definition
- Dance PRO1 issue definition
- dance design refactor
- DAHN PR8 boundary-only subset

## Parallel Once Descriptor Structure Exists
- Validation PR1 / Phase 1 classification work
- Validation PR2 / Phase 2 PVL integration
- Query PRS1 / parallel structural resolution
- Query PRO3 / navigation algebra contract work
- Dance PRO1 / envelope foundation
- Dance PRS1 / structural affordance work
- Dance PRS2 / static dispatch alignment prep
- command descriptor modeling
- TS descriptor client design

## Parallel Once TS Realignment Starts
- DAHN PR3
- DAHN PR6
- query-builder/client API design
- affordance UI work for DAHN

---

# Recommended Execution Order

## Recommended Named Waves
1. Structural Groundwork
2. Schema-Backed Descriptor Surface
3. Descriptor-Owned Value Semantics
4. Validation Integration
5. Query Structural and Operand Alignment
6. Dance Refactor onto Descriptor Affordances
7. Command Descriptor Anchoring and Routing
8. TypeScript Interface Realignment
9. Real DAHN Integration
10. Dynamic Dance Binding and Advanced Query Evolution

## Short Practical Reading
If we want the fewest reversals and the least duplicated logic, the safest sequence is:

`Descriptors 1-3 -> Validation PR1-PR4 + Query PRO/PRS early tracks -> Dance PRO/PRS early tracks -> Commands -> TS realignment -> DAHN -> Dance PRS4-PRS5 + Query PRS4-PRS5`

That sequence keeps semantic ownership centralized and lets each later wave consume real descriptor behavior rather than speculative placeholders.
