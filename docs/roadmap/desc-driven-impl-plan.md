# Descriptor-Driven MAP Implementation Milestone Plan

This milestone plan turns the current cross-doc dependency picture into concrete implementation waves.

The guiding principle is:

- descriptors are the semantic root
- validation, queries, dances, and DAHN should consume descriptor semantics rather than invent parallel systems
- implementation should separate structural foundations from semantic behavior and from TS / UX integration

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

| Work Item | Can Start | Blocked By |
|---|---|---|
| Descriptor PR1 | immediately | none |
| DAHN PR1 | immediately | none |
| DAHN PR2 | immediately | none |
| DAHN PR4 | immediately | none |
| DAHN PR8 (boundary-only subset) | immediately | none |

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

### Why This Wave Exists
Wave 0 gives wrappers and traversal. Wave 1 gives real usable structure.

This is the point where downstream systems can stop saying “in principle descriptors will provide this” and start depending on:
- property lookup
- relationship lookup
- inverse relationship lookup
- effective flattened structural access

| Work Item | Can Start | Blocked By |
|---|---|---|
| Descriptor Phase 2 | after Wave 0 starts | Descriptor PR1 |
| Query structural alignment work | during Wave 1 | Descriptor PR1 |
| Dance affordance modeling prep | during Wave 1 | Descriptor PR1 |
| DAHN adapter design refinement | during Wave 1 | Descriptor PR1 |

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

| Work Item | Can Start | Blocked By |
|---|---|---|
| Descriptor Phase 3 | after Wave 1 is sufficiently real | Descriptor PR1, Descriptor Phase 2 |
| Validation runtime alignment | during Wave 2 | Descriptor Phase 2 |
| Query predicate/operator alignment | during Wave 2 | Descriptor Phase 2 |
| Dance request/result semantic alignment | during Wave 2 | Descriptor Phase 2 |
| DAHN property presentation heuristics | during Wave 2 | Descriptor Phase 2 |

### Exit Criteria
- `ValueDescriptor` is the accepted home of value semantics
- validation and query streams can both target one semantic source
- no new freestanding operator subsystem is needed elsewhere

---

## Wave 3 — Validation Integration

### Goal
Make validation consume descriptor semantics while preserving PVL / Nursery boundaries.

### Major Deliverables
- structural and bounded validation rules routed through descriptors where appropriate
- explicit classification of which descriptor-defined rules live in:
    - PVL
    - Nursery
    - higher layers
- runtime checks for descriptor graph invalidity
- descriptor-driven validation adoption plan at commit/runtime boundaries

### Why This Wave Exists
The updated validation architecture says:
- descriptors own semantics
- validation layers own evaluation authority

So validation should start consuming descriptors as soon as Waves 1 and 2 make that possible.

| Work Item | Can Start | Blocked By |
|---|---|---|
| Descriptor-driven validation integration | after Wave 2 starts | Descriptor Phase 2, Descriptor Phase 3 |
| PVL classification work | during Wave 3 | Descriptor Phase 2 |
| Nursery-side bounded semantic checks | during Wave 3 | Descriptor Phase 3 |
| Validation test refactors | during Wave 3 | Descriptor Phase 3 |

### Exit Criteria
- validation no longer trends toward a separate permanent semantic rule system
- descriptor-owned rules are classified by evaluation layer
- bounded vs open-world enforcement boundaries remain explicit

---

## Wave 4 — Query Structural and Operand Alignment

### Goal
Align query execution and dance/query data structures around descriptor-aware structure and common operands.

### Major Deliverables
- query runtime alignment around descriptor-backed structure
- `ResolvedType` / structural projection reframed as internal support, not caller-facing semantic truth
- navigation/query operand stabilization:
    - `Value`
    - `Row`
    - `RowSet`
    - path toward `Record` / `RecordStream`
- descriptor-aware navigation/filter execution rules

### Why This Wave Exists
Queries now depend on descriptors semantically, but still need their own execution substrate.

This wave makes sure:
- algebra remains the execution substrate
- descriptors remain the semantic source
- operand models are ready for reuse in dance refactor and DAHN

| Work Item | Can Start | Blocked By |
|---|---|---|
| Query structural refactor | after Wave 1 starts | Descriptor Phase 2 |
| Query predicate/operator integration | after Wave 2 starts | Descriptor Phase 3 |
| Navigation algebra implementation work | during Wave 4 | Descriptor Phase 2 |
| Query result structure stabilization | during Wave 4 | Descriptor Phase 2 |
| Distributed query descriptor-consistency work | during Wave 4 | Descriptor Phase 2 |

### Exit Criteria
- query execution no longer owns value semantics independently
- descriptor-aware algebra is the clear direction
- query operand family is stable enough for dance reuse

---

## Wave 5 — Dance Refactor onto Descriptor Affordances

### Goal
Move dances onto descriptor affordances and align dance IO with query/navigation operand structures.

### Major Deliverables
- descriptor-afforded dance discovery on `HolonDescriptor`
- static descriptor-local dance dispatch as the first execution posture
- dance request/result model aligned with:
    - `Value`
    - `Row`
    - `RowSet`
    - `SmartReference`
    - later `RecordStream`
- no global dance registry
- no dance-local reinvention of validation/operator semantics

### Why This Wave Exists
The new dance spec depends on both:
- descriptor affordances
- query-aligned data structures

That makes Wave 5 downstream of both the descriptor foundation and the query operand work.

| Work Item | Can Start | Blocked By |
|---|---|---|
| Dance affordance lookup refactor | after Wave 1 starts | Descriptor Phase 2 |
| Static dance dispatch refactor | after Wave 1 starts | Descriptor PR1, Descriptor Phase 2 |
| Query-aligned dance IO refactor | after Wave 4 starts | Query structural/operand alignment |
| Dance-side descriptor validation/operator usage | after Wave 2 starts | Descriptor Phase 3 |
| Dynamic implementation binding design | during Wave 5 | Descriptor dance affordance model, static dispatch design |

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

| Work Item | Can Start | Blocked By |
|---|---|---|
| Command schema anchor | after Wave 1 | Descriptor Phase 2 |
| Descriptor-bound command routing | after command anchor exists | Descriptor Phase 4 |
| Dispatch redistribution | after routing is real | Descriptor Phase 5 |
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

| Work Item | Can Start | Blocked By |
|---|---|---|
| TS descriptor client design | during Wave 6 | Descriptor Phase 2 |
| TS implementation realignment | after descriptor/core semantics are stable enough | Descriptor Phases 2-6 |
| DAHN real adapter implementation | after TS realignment begins | TS descriptor surfaces |
| Query-builder TS/API design | after TS realignment begins | TS descriptor surfaces, Descriptor Phase 3 |

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

| Work Item | Can Start | Blocked By |
|---|---|---|
| DAHN PR3 | after Wave 7 begins | TS descriptor surfaces |
| DAHN PR5 UI shell | earlier as scaffold | none |
| DAHN PR5 semantic completion | later | Descriptor command/dance surfaces, TS realignment |
| DAHN PR6 | after Wave 7 begins | TS descriptor surfaces, Descriptor Phase 2 |
| DAHN PR7 | after PR3 and PR6 are real | DAHN PR3, DAHN PR6 |
| DAHN PR8 full | after semantic DAHN seams exist | DAHN PR3-7 |

### Exit Criteria
- DAHN can render real descriptor-defined properties, relationships, and affordances
- property presentation is value-type-aware
- affordance surfaces reflect descriptor-discovered commands and dances
- no internal SDK leakage into DAHN

---

## Wave 9 — Dynamic Dance Binding and Advanced Query Evolution

### Goal
Layer in the more ambitious dynamic/runtime features after the semantic foundations are stable.

### Major Deliverables
- dynamic dance implementation binding
- governance activation flows for dance implementations
- WASM / engine loading
- query planner algebra expansion
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

| Work Item | Can Start | Blocked By |
|---|---|---|
| Dynamic dance binding runtime | after Wave 5 semantic refactor | Static dance refactor, descriptor affordance model |
| Dance governance/activation | after dynamic model is defined | Dynamic dance binding design |
| Query planner algebra implementation | after Wave 4 | Query structural alignment |
| Declarative query compilation | after planner substrate exists | Planner algebra implementation |
| Schema-backed operator metadata | after Descriptor Phase 3 | Descriptor operator runtime |
| Richer command metadata | after Descriptor Phase 6 | Command descriptor routing |

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
4. Query structural/operand alignment
5. Dance refactor onto descriptor affordances
6. TypeScript interface realignment
7. Real DAHN integration

## Key Semantic Dependency Rules
- Validation cannot become properly descriptor-driven before `ValueDescriptor` semantics exist.
- Queries should not finalize predicate semantics before `ValueDescriptor` operators exist.
- Dances should not finalize request/result structures before query operand structures stabilize.
- DAHN should not finalize real adapter/visualizer semantics before TS descriptor surfaces exist.
- Dynamic dance binding should not start before static descriptor-afforded dance lookup is real.

---

# Parallel Work Summary

## Safely Parallel Early
- Descriptor PR1
- DAHN PR1, PR2, PR4
- validation architecture clarification
- query architecture/doc refactor
- dance design refactor
- DAHN PR8 boundary-only subset

## Parallel Once Descriptor Structure Exists
- validation integration planning
- query structural/runtime implementation
- dance affordance refactor
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

`Descriptors 1-3 -> Validation + Query structural alignment -> Dance refactor -> Commands -> TS realignment -> DAHN -> Dynamic binding + declarative query expansion`

That sequence keeps semantic ownership centralized and lets each later wave consume real descriptor behavior rather than speculative placeholders.
