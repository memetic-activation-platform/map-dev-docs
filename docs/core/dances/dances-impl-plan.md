# Dance Implementation Plan (v1.0)
## Descriptor-Afforded Behavior Delivery Sequence

This document translates the current dance design into a practical implementation sequence aligned with the descriptor-driven implementation roadmap.

It is intended to:

- break dance delivery into concrete, dependency-aware phases
- distinguish structural affordance work from semantic alignment and runtime binding
- prevent premature hardening around query, validation, or DAHN assumptions
- provide a basis for issue definition, sequencing, and parallel work decisions

This plan assumes:

- the descriptor design is authoritative for dance existence and lookup semantics
- `HolonDescriptor` is the primary caller-facing surface for dance discovery
- effective dance lookup is inherited and flattened through descriptor `Extends`
- query/navigation operand structures should be reused rather than reinvented
- dynamic implementation binding is a later layer built on top of descriptor-afforded static dispatch

Related references:

- `docs/core/dances-design-v1.1.md`
- `docs/core/descriptors/descriptors-design-spec.md`
- `docs/roadmap/desc-driven-impl-plan.md`

---

# 1. Delivery Principles

The implementation sequence follows these rules:

- descriptors own dance affordance semantics
- dance work must not invent a second global registry or caller-side lookup model
- structural affordance delivery should come before semantic request/result alignment
- static descriptor-local dispatch should come before dynamic implementation binding
- dance-side validation and operator usage should consume descriptor semantics rather than define parallel rule systems
- dance IO should converge on query/navigation operand structures rather than inventing a second result family

---

# 2. Phase Overview

The recommended dance implementation sequence is:

1. Structural Descriptor-Affordance Surface
2. Static Descriptor-Local Dispatch Alignment
3. Request/Result Operand Alignment
4. Descriptor-Semantic Validation and Operator Alignment
5. Dynamic Implementation Binding
6. Governance, Activation, and Advanced Runtime Evolution

The recommended PR segmentation is:

1. Dance PR1 — Structural Descriptor-Affordance Surface
2. Dance PR2 — Static Descriptor-Local Dispatch Alignment
3. Dance PR3 — Request/Result Operand Alignment
4. Dance PR4 — Descriptor-Semantic Validation and Operator Alignment
5. Dance PR5 — Dynamic Implementation Binding
6. Dance PR6 — Governance, Activation, and Advanced Runtime Evolution

Each phase below defines:

- goal
- major deliverables
- why the phase exists
- dependencies
- exit criteria

---

# 3. Phase 1 — Structural Descriptor-Affordance Surface

## Goal

Make descriptor-backed dance discovery real through `HolonDescriptor` and related structural runtime surfaces.

## Major Deliverables

- Dance PR1:
    - structural descriptor-affordance surface for dances
    - schema-backed dance lookup entrypoints

- descriptor-local dance lookup on `HolonDescriptor`
- effective inherited dance affordance lookup through flattened `Extends`
- runtime wrapper/access patterns for dance affordances
- explicit handling of absent or unsupported schema-backed dance surfaces
- no global dance registry as the caller-facing source of truth

## Why This Phase Exists

This is the first point where downstream systems can stop treating descriptor-afforded dances as a future concept and begin treating them as real structural runtime access.

Without this phase:

- DAHN cannot safely consume descriptor-afforded dances
- static dispatch remains weakly anchored
- callers risk accumulating ad hoc dance lookup logic

## Dependencies

- Descriptor PR1 / runtime spine
- Descriptor PR2 / schema-backed structural descriptor surface

## PR Identity

- Dance PR1 / structural dance affordance lookup

## Exit Criteria

- dances are discoverable through descriptor-backed lookup
- effective inherited dance lookup is flattened and caller-facing
- no caller needs a second lookup mechanism for dance existence

---

# 4. Phase 2 — Static Descriptor-Local Dispatch Alignment

## Goal

Align dance invocation with descriptor-local static dispatch as the current implementation posture.

## Major Deliverables

- Dance PR2:
    - static descriptor-local dispatch alignment
    - dispatch routing keyed by descriptor-afforded dance lookup

- static descriptor-local dispatch rules
- dispatch path keyed by descriptor-afforded dance lookup
- no execution binding model beyond current static Rust-local implementations
- explicit separation between:
    - dance affordance existence
    - dispatch routing
    - future implementation binding

## Why This Phase Exists

The design already distinguishes semantic dance existence from execution binding. This phase delivers the current-phase compatible execution posture without prematurely introducing dynamic loading, governance, or runtime binding complexity.

## Dependencies

- Phase 1 structural affordance lookup
- current runtime dispatch posture from MAP core

## PR Identity

- Dance PR2 / static descriptor-local dispatch alignment

## Exit Criteria

- static dispatch is clearly anchored in descriptor-afforded dance lookup
- dance discovery and dance execution are no longer conflated
- current implementation remains compatible with later dynamic binding

---

# 5. Phase 3 — Request/Result Operand Alignment

## Goal

Align dance request and result structures with MAP query/navigation operand models.

## Major Deliverables

- Dance PR3:
    - canonical dance invocation envelope
    - canonical dance result envelope
    - query-aligned operand/result model for dance IO

- canonical dance invocation envelope
- canonical dance result envelope
- convergence on:
    - `Value`
    - `Row`
    - `RowSet`
    - `SmartReference`
    - later `Record` / `RecordStream`
- dance category guidance for preferred input/output shapes
- removal or deprecation path for ad hoc dance-local result families

## Why This Phase Exists

Dance IO must not become a separate structural island. Navigation dances, query dances, and DAHN-driven exploration all benefit from shared operand/result structures.

## Dependencies

- Phase 1 structural affordance lookup
- query structural and operand work sufficiently mature to provide stable target shapes

## PR Identity

- Dance PR3 / query-aligned dance request-result operand model

## Exit Criteria

- dance request/result structures have a clear canonical direction
- dance IO is aligned with query/navigation operands
- no second incompatible result family is being reinforced

---

# 6. Phase 4 — Descriptor-Semantic Validation and Operator Alignment

## Goal

Make dance-side validation and filter/operator behavior consume descriptor-owned semantics.

## Major Deliverables

- Dance PR4:
    - descriptor-semantic dance validation/operator alignment
    - no dance-local permanent rule system

- dance request/value checking via descriptor-backed value semantics
- use of descriptor-owned operator support where dances evaluate filters or comparisons
- explicit rejection of handwritten dance-local predicate semantics where descriptor semantics exist
- clarified boundary between dance orchestration and validation authority

## Why This Phase Exists

Once dances accept structured inputs and may perform navigation/filter-like behavior, they must not become a second home for validation and operator semantics.

## Dependencies

- Descriptor Phase 3 / `ValueDescriptor` semantics
- validation architecture alignment
- Phase 3 operand alignment where relevant

## PR Identity

- Dance PR4 / descriptor-semantic validation and operator alignment

## Exit Criteria

- dance-side checks consume descriptor semantics rather than custom rule systems
- operator behavior is descriptor-backed where applicable
- dance logic no longer trends toward semantic duplication

---

# 7. Phase 5 — Dynamic Implementation Binding

## Goal

Add the binding layer that allows descriptor-afforded dances to resolve to executable implementations.

## Major Deliverables

- Dance PR5:
    - `DanceImplementationDescriptor`
    - implementation binding model
    - compatibility posture for static and dynamic execution

- `DanceImplementationDescriptor`
- implementation binding relationships such as:
    - `ForDance`
    - `ForAffordingType`
- implementation selection rules
- engine/module/entrypoint metadata
- compatibility model for static and dynamic execution postures

## Why This Phase Exists

Dynamic loading and multi-implementation resolution are important, but they should sit on top of already-stable descriptor affordance semantics and dispatch ownership.

## Dependencies

- Phase 2 static dispatch alignment
- sufficiently stable descriptor-afforded dance model
- clear ABI and operand/result posture

## PR Identity

- Dance PR5 / dynamic implementation binding

## Exit Criteria

- dynamic binding is layered on top of descriptor affordances rather than replacing them
- implementation binding does not redefine dance existence
- static and dynamic models remain conceptually compatible

---

# 8. Phase 6 — Governance, Activation, and Advanced Runtime Evolution

## Goal

Layer in activation policy, governance control, and more advanced runtime behavior after the binding model is stable.

## Major Deliverables

- Dance PR6:
    - governance and activation posture
    - advanced runtime evolution for executable dance implementations

- governance and activation rules for dance implementations
- active implementation resolution policy
- audit/provenance expectations
- runtime loading lifecycle guidance
- later support for WASM/WASI or other execution engines

## Why This Phase Exists

Governance and runtime evolution are real requirements, but they should not destabilize the core dance affordance and dispatch model.

## Dependencies

- Phase 5 implementation binding
- broader runtime/module-loading readiness

## PR Identity

- Dance PR6 / governance, activation, and advanced runtime evolution

## Exit Criteria

- active implementation resolution is explicit and deterministic
- governance does not redefine descriptor affordance semantics
- runtime evolution remains layered and auditable

---

# 9. Cross-Phase Dependency Summary

## Critical Path

1. Descriptor structural surface
2. Dance structural affordance lookup
3. Static descriptor-local dispatch alignment
4. Query/dance operand alignment
5. Descriptor-owned semantic alignment
6. Dynamic implementation binding
7. Governance/activation evolution

## Key Dependency Rules

- dance discovery must be descriptor-first before dispatch work hardens
- static descriptor-local dispatch should land before dynamic binding
- dance request/result structures should not finalize before query operand structures stabilize
- dance-side validation and operator behavior should not finalize before descriptor value semantics exist
- governance and activation should not begin before implementation binding is real

---

# 10. Parallel Work Guidance

## Safe Earlier Work

- dance implementation sequence planning
- schema terminology alignment analysis
- issue definition for structural affordance work
- dispatch boundary clarification
- inventory of current dance-local request/result structures

## Safe Once Descriptor Structural Surface Exists

- descriptor-local dance lookup work
- static dispatch refactor prep
- DAHN-facing dance affordance consumption planning
- tests for inherited affordance lookup behavior

## Safe Once Descriptor Value Semantics Exist

- dance-side validation alignment
- operator-backed filter/comparison alignment
- richer request parameter semantics

## Safe Once Query Operand Shapes Stabilize

- canonical dance request/result operand convergence
- query-aligned navigation and bulk dance result models

---

# 11. Recommended Initial Issue / PR Sequence

A likely issue sequence is:

1. Dance PR1
   - expose descriptor-local dance lookup on `HolonDescriptor`
   - define and test effective inherited dance affordance lookup
2. Dance PR2
   - refactor static dance dispatch to route through descriptor-afforded lookup
3. Dance PR3
   - define canonical dance invocation/result operand model
4. Dance PR4
   - align dance-side validation/operator usage with descriptor semantics
5. Dance PR5
   - introduce `DanceImplementationDescriptor`
6. Dance PR6
   - add governance/activation and dynamic binding rules

---

# 12. Immediate Next Step

The immediate next step should be to define the first structural issue in this sequence:

- descriptor-local dance affordance lookup
- inherited/flattened effective dance discovery
- explicit current-schema handling
- no execution-binding expansion yet

That issue is the natural Wave 1 entry point for the dance track.
