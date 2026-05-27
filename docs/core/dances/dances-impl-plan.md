# Dance Implementation Plan (v1.4)
## Parallel Descriptor-Afforded Behavior Delivery Sequence

## Change Log

### v1.4

- updates the plan after Issue 508 removed row-shaped query contracts and reset the navigation algebra
- removes `Value`, `Row`, `RowSet`, `BoundHolonCollection`, broad query `RuntimeValue`, and standalone `Query` runtime contracts from the Dance PRO2 target model
- re-centers Dance PRO2 on `HolonReference`, `HolonCollection`, `BaseValue`, projected transient holons, and transient/generated projection descriptors
- treats `ExecutionPlan` and `NavigationExecutionBindings` as future plan/session work, not Dance PRO2 deliverables
- marks old-world `Node`, `NodeCollection`, `QueryPathMap`, `QueryExpression`, and query-method dance paths as deprecated compatibility only

### v1.3

Superseded by v1.4 for Issue 508 query-contract removal.

- retired intermediate alignment pass between the original shared-type framing and the Issue 508 reset
- replaced by v1.4 as the authoritative Dance PRO2 posture

### v1.2

Superseded by v1.3, then by v1.4 for Issue 508 query-contract removal.

- retired historical version from the older runtime-shared-type framing
- retained only to explain document history; do not use as current implementation guidance

This document translates the current dance design into a practical implementation sequence aligned with the descriptor-driven implementation roadmap.

It is intended to:

- break dance delivery into concrete, dependency-aware phases
- distinguish runtime value / binding / envelope / ABI stabilization from descriptor-dependent semantics and dispatch
- preserve a single phase sequence while allowing multiple PR tracks within that sequence
- prevent premature hardening around query, validation, DAHN, or dynamic runtime assumptions
- provide a basis for issue definition, sequencing, and parallel work decisions

This plan assumes:

- the descriptor design is authoritative for dance existence and lookup semantics
- `HolonDescriptor` is the primary caller-facing surface for dance discovery
- effective dance lookup is inherited and flattened through descriptor `Extends`
- the runtime shared type foundation now exists as a cross-surface baseline
- `HolonReference` is the primary singular holon-backed handle
- `HolonCollection` is the primary plural holon-backed runtime carrier
- `BaseValue` remains the scalar/property value family
- projected records are transient holons
- projected record sets are `HolonCollection`s
- projection shape is described by transient or generated `HolonDescriptor`s
- `ExecutionPlan` and `NavigationExecutionBindings` are future plan/session work, not required for Dance PRO2
- `Value`, `Row`, `RowSet`, `BoundHolonCollection`, broad query `RuntimeValue`, and standalone `Query` runtime contracts are removed from the target dance/query model
- dynamic implementation binding is a later layer built on top of descriptor-afforded static dispatch

Related references:

- `docs/core/dances/dances-design-spec.md`
- `docs/core/descriptors/descriptors-design-spec.md`
- `docs/core/type-system/runtime-shared-types.md`
- `docs/core/map-queries/simple-algebra-binding-model.md`
- `docs/core/map-queries/navigation-algebra.md`
- `docs/core/map-queries/queries-impl-plan.md`
- `docs/core/commands-and-runtime/commands.md`
- `docs/roadmap/desc-driven-impl-plan.md`

---

# 1. Delivery Principles

The implementation sequence follows these rules:

- descriptors own dance affordance semantics
- dance work must not invent a second global registry or caller-side lookup model
- runtime shared type reuse, envelope posture, and ABI shape may stabilize before descriptor-backed affordance interrogation is available
- structural affordance delivery should come before semantic request/result interrogation
- static descriptor-local dispatch should come before dynamic implementation binding
- dance-side validation and operator usage should consume descriptor semantics rather than define parallel rule systems
- dance IO should consume existing MAP-native runtime structures rather than inventing a second result family
- dance contracts should prefer `HolonReference`, `HolonCollection`, `BaseValue`, and projected transient holons
- dance/query alignment should not introduce a new operand family
- retained old-world query traversal artifacts should remain deprecated compatibility surfaces only

---

# 2. Phase Overview

The recommended dance implementation sequence is:

1. Shared Invocation / Result Envelope Foundation
2. MAP-Native Runtime Value and ABI Alignment
3. Descriptor-Afforded Dance Structural Semantics
4. Static Descriptor-Local Dispatch Alignment
5. Descriptor-Semantic Validation and Operator Alignment
6. Dynamic Binding and Runtime Evolution

The recommended PR segmentation uses two tracks:

- `PRO` = runtime value / envelope / ABI / contract track
- `PRS` = semantic / descriptor-dependent / dispatch track

Recommended dance PRs:

1. Dance PRO1 — Shared Invocation / Result Envelope Foundation
2. Dance PRO2 — MAP-Native Runtime Value and ABI Alignment
3. Dance PRO3 — Cross-Surface Contract Stabilization
4. Dance PRS1 — Descriptor-Afforded Dance Structural Semantics
5. Dance PRS2 — Static Descriptor-Local Dispatch Alignment
6. Dance PRS3 — Descriptor-Semantic Validation and Operator Alignment
7. Dance PRS4 — Dynamic Implementation Binding
8. Dance PRS5 — Governance, Activation, and Advanced Runtime Evolution

Each phase below defines:

- goal
- major deliverables
- why the phase exists
- dependencies
- exit criteria

---

# 3. Phase 1 — Shared Invocation / Result Envelope Foundation

## Goal

Define the canonical dance invocation and result envelope posture on top of the shared runtime type foundation so interface shape can stabilize before full descriptor-backed dance interrogation is available.

## Major Deliverables

- Dance PRO1:
    - canonical invocation envelope foundation
    - canonical result envelope foundation

- initial dance invocation envelope posture
- initial dance result envelope posture
- explicit use of the new-world `DanceInvocation` envelope as the dance-facing contract center
- explicit distinction between:
    - target selection
    - structured parameters
    - execution context
    - structured results
    - diagnostics/events
- contract guidance for reuse by query, command, SDK, and DAHN work

## Why This Phase Exists

Dance invocation and result shape has ripple effects on command parameters, query-aligned IO, and the TypeScript SDK. That shape should stabilize earlier than descriptor-backed dance discovery so downstream consumers can reduce churn.

The runtime shared type refactor means this phase no longer needs to prove the shared type family itself. It should instead define the dance-owned envelope around that family and make clear where `DanceInvocation` sits relative to Commands, ABI payloads, and runtime execution.

Without this phase:

- dance-related interface shape will remain coupled to later semantic interrogation work
- SDK and client-facing contract stabilization will happen too late
- query/dance/command contract convergence will be harder to manage

## Dependencies

- runtime shared types foundation
- commands posture for transitional `Dance(DanceRequest)` and new-world `DanceV2(DanceInvocation)` ingress

## PR Identity

- Dance PRO1 / shared invocation and result envelope foundation

## Exit Criteria

- canonical dance invocation/result envelope direction exists and is centered on `DanceInvocation`
- downstream work can begin converging on a shared dance envelope posture
- dance IO no longer defaults to ad hoc result-shape growth
- old-world `DanceRequest` is clearly treated as transitional command ingress rather than the future dance contract

---

# 4. Phase 2 — MAP-Native Runtime Value and ABI Alignment

## Goal

Align dance IO to the MAP-native runtime value model and the ABI-facing contract posture without waiting for full descriptor-backed affordance semantics.

## Major Deliverables

- Dance PRO2:
    - MAP-native runtime value alignment for dance IO
    - ABI-facing payload posture
    - deprecated compatibility posture for retained old-world query traversal surfaces

- Dance PRO3:
    - cross-surface contract stabilization
    - query/dance/command envelope convergence posture

- convergence on:
    - primary holon-backed runtime values:
        - `HolonReference`
        - `HolonCollection`
        - `BaseValue`
    - projected record model:
        - transient holons for projected records
        - `HolonCollection` for projected record sets
        - transient or generated `HolonDescriptor`s for projection shape
    - contract-significant specialized types:
        - `SmartReference` where appropriate
    - future plan/session concepts that must remain out of the PRO2 implementation surface:
        - `ExecutionPlan` holons
        - `NavigationExecutionBindings`
    - deprecated compatibility surfaces retained after Issue 508:
        - `Node`
        - `NodeCollection`
        - `QueryPathMap`
        - `QueryExpression`
        - `DanceType::QueryMethod(NodeCollection)`
- explicit removal from the target Dance PRO2 model:
    - `Value`
    - `Row`
    - `RowSet`
    - `BoundHolonCollection`
    - broad query `RuntimeValue`
    - standalone `Query` runtime contracts
- explicit distinction between:
    - primary holon-backed runtime carriers
    - scalar/property values
    - projected transient holons
    - deprecated compatibility-only old-world query traversal payloads
- dance category guidance for preferred input/output shapes
- ABI-facing payload contract posture for dance invocation/execution
- explicit "no new operand family" guidance for dance/query alignment
- explicit transitional command-ingress split:
    - old-world `TransactionAction::Dance(DanceRequest)`
    - new-world `TransactionAction::DanceV2(DanceInvocation)`
- contract guidance for TS SDK and DAHN reuse

## Why This Phase Exists

Dance IO must not become a separate structural island. Runtime value and ABI shape should stabilize early enough to reduce churn for SDK consumers and to align with the query model before full semantic interrogation is available.

After Issue 508, this phase should be read as dance-specific adoption of the MAP-native runtime model. It must avoid reintroducing deleted row-shaped query contracts, `BoundHolonCollection`, broad query runtime values, or a standalone query contract.

The intent is:

- `HolonReference` for singular holon-backed results
- `HolonCollection` for plural holon-backed results
- `BaseValue` for scalar/property values
- transient holons for projected records
- `HolonCollection` for projected record sets
- transient or generated `HolonDescriptor`s for projection shape
- retained old-world query traversal surfaces treated as deprecated compatibility only
- a clear old-world/new-world command-ingress split while dance transition is underway
- ABI materialization only where an execution boundary actually requires it

## Dependencies

- Dance PRO1 / shared invocation and result envelope foundation
- runtime shared types foundation
- Issue 508 / query contract removal and navigation algebra reset
- retained `HolonReference`, `HolonCollection`, and `BaseValue`
- query/dance contract stabilization where cross-surface shapes touch Commands and SDK contracts

## PR Identity

- Dance PRO2 / MAP-native runtime value and ABI alignment
- Dance PRO3 / cross-surface contract stabilization

## Exit Criteria

- dance IO is aligned with `HolonReference`, `HolonCollection`, `BaseValue`, and projected transient holon result patterns
- projected records and projected record sets use the MAP-native holon model rather than row-shaped DTOs
- retained old-world query traversal artifacts are explicitly compatibility-only
- `Value`, `Row`, `RowSet`, `BoundHolonCollection`, broad query `RuntimeValue`, and standalone `Query` contracts are not introduced as part of dance/query alignment
- ABI-facing payload posture is explicit
- old-world `DanceRequest` ingress and new-world `DanceInvocation` ingress are explicitly separated
- command/dance/query contract convergence has a stable direction
- ABI or SDK projection does not recreate row-shaped query contracts

---

# 5. Phase 3 — Descriptor-Afforded Dance Structural Semantics

## Goal

Make descriptor-backed dance discovery real through `HolonDescriptor` and related structural runtime surfaces.

## Major Deliverables

- Dance PRS1:
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

- Dance PRS1 / structural dance affordance semantics

## Exit Criteria

- dances are discoverable through descriptor-backed lookup
- effective inherited dance lookup is flattened and caller-facing
- no caller needs a second lookup mechanism for dance existence

---

# 6. Phase 4 — Static Descriptor-Local Dispatch Alignment

## Goal

Align dance invocation with descriptor-local static dispatch as the current implementation posture.

## Major Deliverables

- Dance PRS2:
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

- Dance PRS1 / structural dance affordance semantics

## PR Identity

- Dance PRS2 / static descriptor-local dispatch alignment

## Exit Criteria

- static dispatch is clearly anchored in descriptor-afforded dance lookup
- dance discovery and dance execution are no longer conflated
- current implementation remains compatible with later dynamic binding

---

# 7. Phase 5 — Descriptor-Semantic Validation and Operator Alignment

## Goal

Make dance-side validation and filter/operator behavior consume descriptor-owned semantics.

## Major Deliverables

- Dance PRS3:
    - descriptor-semantic dance validation/operator alignment
    - no dance-local permanent rule system

- dance request/value checking via descriptor-backed value semantics
- use of descriptor-owned operator support where dances evaluate filters or comparisons
- explicit rejection of handwritten dance-local predicate semantics where descriptor semantics exist
- clarified boundary between dance orchestration and validation authority

## Why This Phase Exists

Once dances accept structured inputs and may perform navigation/filter-like behavior, they must not become a second home for validation and operator semantics.

## Dependencies

- Dance PRO2 / MAP-native runtime value and ABI alignment
- Descriptor Phase 3 / `ValueDescriptor` semantics
- validation architecture alignment

## PR Identity

- Dance PRS3 / descriptor-semantic validation and operator alignment

## Exit Criteria

- dance-side checks consume descriptor semantics rather than custom rule systems
- operator behavior is descriptor-backed where applicable
- dance logic no longer trends toward semantic duplication

---

# 8. Phase 6 — Dynamic Binding and Runtime Evolution

## Goal

Layer in dynamic implementation binding, governance, activation, and advanced runtime evolution only after descriptor-afforded semantics and static dispatch are stable.

## Major Deliverables

- Dance PRS4:
    - `DanceImplementationDescriptor`
    - implementation binding model
    - compatibility posture for static and dynamic execution

- Dance PRS5:
    - governance and activation posture
    - advanced runtime evolution for executable dance implementations

- implementation binding relationships such as:
    - `ForDance`
    - `ForAffordingType`
- implementation selection rules
- engine/module/entrypoint metadata
- active implementation resolution policy
- audit/provenance expectations
- runtime loading lifecycle guidance
- later support for WASM/WASI or other execution engines

## Why This Phase Exists

Dynamic loading and runtime evolution are important, but they should sit on top of already-stable dance affordance semantics, MAP-native runtime value / ABI posture, and dispatch ownership.

## Dependencies

- Dance PRS2 / static descriptor-local dispatch alignment
- Dance PRS3 / descriptor-semantic validation and operator alignment
- Dance PRO2 / MAP-native runtime value and ABI alignment

## PR Identity

- Dance PRS4 / dynamic implementation binding
- Dance PRS5 / governance, activation, and advanced runtime evolution

## Exit Criteria

- dynamic binding is layered on top of descriptor affordances rather than replacing them
- implementation binding does not redefine dance existence
- active implementation resolution is explicit and deterministic
- runtime evolution remains layered and auditable

---

# 9. Cross-Phase Dependency Summary

## Critical Path

1. Shared dance invocation/result envelope foundation
2. Shared dance MAP-native runtime value and ABI alignment
3. Descriptor-backed dance affordance semantics
4. Static descriptor-local dispatch alignment
5. Descriptor-semantic validation and operator alignment
6. Dynamic implementation binding
7. Governance/activation evolution

## Key Dependency Rules

- MAP-native runtime value and envelope stabilization may move earlier than descriptor-backed dance interrogation
- dance discovery must be descriptor-first before dispatch work hardens
- static descriptor-local dispatch should land before dynamic binding
- dance-side validation and operator behavior should not finalize before descriptor value semantics exist
- dynamic runtime evolution should not begin before implementation binding is real
- `HolonCollection`-centered dance/query contract posture is already the baseline and should not be reopened in dance-specific work
- `Value`, `Row`, `RowSet`, `BoundHolonCollection`, broad query `RuntimeValue`, standalone `Query` contracts, and other new foundational operands should not be introduced by dance-specific work
- retained old-world query traversal artifacts should stay deprecated compatibility surfaces until replaced by descriptor-backed navigation Dances

---

# 10. Parallel Work Guidance

## Safe Earlier Work

- dance implementation sequence planning
- shared invocation/result envelope work
- dance-specific adoption of the MAP-native runtime value model
- ABI alignment work
- issue definition for descriptor-affordance work
- dispatch boundary clarification
- cross-surface contract review against query, command, SDK, and DAHN callers

## Safe Once Descriptor Structural Surface Exists

- Dance PRS1 / structural dance affordance semantics
- Dance PRS2 / static dispatch alignment prep
- DAHN-facing dance affordance consumption planning
- tests for inherited affordance lookup behavior

## Safe Once Descriptor Value Semantics Exist

- Dance PRS3 / dance-side validation alignment
- operator-backed filter/comparison alignment

## Safe Once Static Dispatch and ABI Posture Stabilize

- Dance PRS4 / dynamic implementation binding
- Dance PRS5 / governance and runtime evolution

---

# 11. Recommended Initial Issue / PR Sequence

A likely issue sequence is:

1. Dance PRO1
   - define canonical `DanceInvocation` and result envelope foundations
   - separate old-world `DanceRequest` ingress from the new-world dance contract
2. Dance PRO2
   - adopt `HolonReference`, `HolonCollection`, and `BaseValue` for dance IO
   - define projected-record posture as transient holons in `HolonCollection`
   - define ABI compatibility for retained old-world query traversal payloads
   - keep `Value`, `Row`, `RowSet`, `BoundHolonCollection`, broad query `RuntimeValue`, and standalone `Query` contracts out of the current alignment work
3. Dance PRO3
   - stabilize cross-surface contract convergence with query/command work
4. Dance PRS1
   - expose descriptor-local dance lookup on `HolonDescriptor`
   - define and test effective inherited dance affordance lookup
5. Dance PRS2
   - refactor static dance dispatch to route through descriptor-afforded lookup
6. Dance PRS3
   - align dance-side validation/operator usage with descriptor semantics
7. Dance PRS4
   - introduce `DanceImplementationDescriptor`
8. Dance PRS5
   - add governance/activation and advanced runtime evolution rules

---

# 12. Immediate Next Step

The immediate next step should be to define the first issue in each early track:

- Dance PRO1:
  - canonical `DanceInvocation` envelope foundation
  - canonical result envelope foundation
  - explicit transition posture for legacy `DanceRequest`

- Dance PRS1:
  - descriptor-local dance affordance lookup
  - inherited/flattened effective dance discovery
  - explicit current-schema handling
  - no execution-binding expansion yet

Those issues are the natural entry points for the dance track.
