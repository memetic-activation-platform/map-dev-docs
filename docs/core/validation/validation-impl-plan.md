# Validation Implementation Plan (v1.0)
## Descriptor-Driven Layered Validation Delivery Sequence

This document translates the current validation architecture into a practical implementation sequence aligned with the descriptor-driven implementation roadmap.

It is intended to:

- break validation delivery into concrete, dependency-aware phases
- distinguish rule ownership from enforcement-layer execution
- prevent premature hardening around descriptor semantics that have not yet landed
- provide a basis for issue definition, sequencing, and parallel work decisions

This plan assumes:

- descriptors own validation semantics
- validation layers own evaluation authority
- PVL remains the closed-world, bounded, peer-reproducible enforcement layer
- Nursery remains the bounded pre-commit environment for richer descriptor-backed checks
- dependency gravity determines where descriptor-defined rules may safely execute

Related references:

- `docs/core/validation/validation-arch.md`
- `docs/core/validation/dependency-gravity.md`
- `docs/core/descriptors/descriptors-design-spec.md`
- `docs/roadmap/desc-driven-impl-plan.md`

---

# 1. Delivery Principles

The implementation sequence follows these rules:

- validation must consume descriptor semantics rather than inventing a second permanent rule system
- descriptor rule ownership and enforcement-layer placement must remain distinct
- PVL should remain minimal, bounded, and reproducible
- Nursery should absorb bounded validation that dependency gravity rejects from PVL
- validation should not finalize semantics before the relevant descriptor surfaces are real
- command, query, and dance work should reuse descriptor-defined validation semantics where appropriate

---

# 2. Phase Overview

The recommended validation implementation sequence is:

1. Structural Rule Classification and Adoption Boundary
2. PVL Closed-World Descriptor Rule Integration
3. Nursery Bounded Descriptor Rule Integration
4. Validation Flow and Outcome Integration
5. Cross-Subsystem Semantic Convergence
6. Higher-Layer Validation Signaling and Evolution

The recommended PR segmentation is:

1. Validation PR1 — Structural Rule Classification and Adoption Boundary
2. Validation PR2 — PVL Closed-World Descriptor Rule Integration
3. Validation PR3 — Nursery Bounded Descriptor Rule Integration
4. Validation PR4 — Validation Flow and Outcome Integration
5. Validation PR5 — Cross-Subsystem Semantic Convergence
6. Validation PR6 — Higher-Layer Validation Signaling and Evolution

Each phase below defines:

- goal
- major deliverables
- why the phase exists
- dependencies
- exit criteria

---

# 3. Phase 1 — Structural Rule Classification and Adoption Boundary

## Goal

Classify descriptor-defined rule kinds by enforcement layer and define the adoption boundary between descriptor semantics, PVL, and Nursery.

## Major Deliverables

- Validation PR1:
    - rule classification framework grounded in dependency gravity
    - validation adoption boundary for descriptor-defined rules

- explicit classification of descriptor-defined rules into:
    - PVL-safe closed-world rules
    - Nursery-only bounded transaction/snapshot rules
    - deferred higher-layer rules
- identification of current validation logic that should migrate toward descriptor ownership
- explicit statement of what validation must not finalize before descriptor semantics land
- initial mapping of likely rule families such as:
    - property requiredness
    - enum membership
    - bounded cardinality
    - transaction coherence
    - post-transaction duplicate detection
    - command/dance precondition categories

## Why This Phase Exists

Validation cannot safely become descriptor-driven simply by moving logic into validators. The architecture requires a classification step that uses dependency gravity to decide where descriptor-defined rules may execute.

Without this phase:

- PVL risks absorbing rules that exceed its boundary
- Nursery risks becoming an unstructured catch-all
- downstream work may harden around temporary or duplicated rule placements

## Dependencies

- Descriptor PR1 / runtime spine
- validation architecture baseline
- dependency gravity baseline

## PR Identity

- Validation PR1 / structural rule classification and adoption boundary

## Exit Criteria

- descriptor-defined rule classes are explicitly mapped to enforcement layers
- the team has a clear rule-placement vocabulary grounded in dependency gravity
- no validation stream needs to guess whether a rule belongs in PVL, Nursery, or above

---

# 4. Phase 2 — PVL Closed-World Descriptor Rule Integration

## Goal

Integrate the closed-world subset of descriptor-defined rules into PVL without widening the PVL boundary.

## Major Deliverables

- Validation PR2:
    - PVL integration for closed-world descriptor-backed rules
    - bounded descriptor-resolution posture for integrity validation

- explicit PVL-side adoption of descriptor-backed structural checks where reconstructible
- integrity-safe descriptor resolution guidance and bounded lookup rules
- runtime checks for descriptor graph invalidity where PVL legitimately depends on descriptor-backed structure
- tests for peer-reproducible closed-world validation behavior
- explicit exclusions for:
    - open-world graph traversal
    - runtime plugin/module loading
    - non-reconstructible context

## Why This Phase Exists

The architecture says descriptors define rules, but PVL may execute only the closed-world subset. This phase makes that subset real without turning PVL into a general descriptor-execution runtime.

## Dependencies

- Validation PR1 / classification boundary
- Descriptor Phase 2 / schema-backed structural descriptor surface
- descriptor resolution bounded enough for PVL-safe usage

## PR Identity

- Validation PR2 / PVL closed-world descriptor rule integration

## Exit Criteria

- PVL can execute the bounded closed-world subset of descriptor-defined rules
- integrity validation remains reproducible and bounded
- PVL has not absorbed higher-layer runtime responsibilities

---

# 5. Phase 3 — Nursery Bounded Descriptor Rule Integration

## Goal

Make Nursery the real home of bounded descriptor-driven validation that exceeds PVL but remains meaningfully checkable before commit.

## Major Deliverables

- Validation PR3:
    - Nursery integration for bounded transaction/snapshot-aware descriptor rules
    - required / warning / deferred rule categorization in practice

- bounded transaction-context evaluation of descriptor-defined rules
- local snapshot-aware checks such as:
    - post-transaction cardinality
    - transaction coherence
    - duplicate detection
    - bounded query/filter-style checks
- explicit separation of:
    - hard-fail required checks
    - warning-level advisory checks
    - deferred higher-layer outcomes
- tests for bounded pre-commit validation behavior

## Why This Phase Exists

Dependency gravity rejects many meaningful descriptor-defined checks from PVL. Nursery exists to absorb exactly that work without pulling runtime complexity downward into integrity.

## Dependencies

- Validation PR1 / classification boundary
- Descriptor Phase 2 / structural descriptor surface
- Descriptor Phase 3 / `ValueDescriptor` semantics for value-level checks
- transaction and snapshot context available to Nursery

## PR Identity

- Validation PR3 / Nursery bounded descriptor rule integration

## Exit Criteria

- Nursery executes bounded descriptor-defined rules that do not belong in PVL
- required / warning / deferred validation categories are operationally meaningful
- higher-gravity validation no longer pressures PVL to expand unsafely

---

# 6. Phase 4 — Validation Flow and Outcome Integration

## Goal

Integrate descriptor-driven validation into the end-to-end validation flow across Nursery, commit, integrity validation, and conflict signaling.

## Major Deliverables

- Validation PR4:
    - staged validation flow integration
    - validation outcomes and signaling posture

- descriptor-driven validation flow across:
    - Stage 1 — Nursery
    - Stage 2 — Commit
    - Stage 3 — Integrity Validation
    - Stage 4 — Propagation
    - Stage 5 — Conflict Detection
    - Stage 6 — Resolution
- outcome handling for:
    - block
    - warn
    - defer
- integration of uniqueness/conflict patterns with the layered validation model
- tests for validation flow and outcome signaling

## Why This Phase Exists

Rule placement alone is not enough. Validation outcomes must fit the real transaction and propagation flow so that descriptor-driven rules influence user and system behavior coherently.

## Dependencies

- Validation PR2 / PVL integration
- Validation PR3 / Nursery integration
- transaction lifecycle and commit flow stable enough to consume validation outcomes

## PR Identity

- Validation PR4 / validation flow and outcome integration

## Exit Criteria

- descriptor-driven validation is integrated into the staged validation flow
- validation outcomes are explicit and consistent across layers
- conflict detection/signaling works with the layered validation posture

---

# 7. Phase 5 — Cross-Subsystem Semantic Convergence

## Goal

Converge validation semantics with query, command, and dance consumers so validation is not redefined in parallel elsewhere.

## Major Deliverables

- Validation PR5:
    - semantic convergence across validation, query, commands, and dances
    - shared descriptor-owned rule consumption posture

- explicit reuse of descriptor-backed value/operator semantics where validation overlaps with query filtering
- validation-side alignment with command and dance precondition categories
- removal or deprecation path for duplicated validation logic outside descriptor ownership
- integration guidance for DAHN-facing validation consumption without frontend semantic ownership

## Why This Phase Exists

The validation architecture is not isolated. Query, commands, dances, and DAHN all touch overlapping semantics. This phase keeps validation from becoming correct in theory while the rest of the system drifts into duplication.

## Dependencies

- Validation PR2 / PVL integration
- Validation PR3 / Nursery integration
- Descriptor Phase 3 / `ValueDescriptor` semantics
- sufficient maturity in query, command, and dance structural work

## PR Identity

- Validation PR5 / cross-subsystem semantic convergence

## Exit Criteria

- validation, query, commands, and dances are clearly consuming one descriptor-owned semantic surface where appropriate
- parallel permanent rule systems are shrinking rather than growing
- DAHN is not pressured to invent frontend-owned validation semantics

---

# 8. Phase 6 — Higher-Layer Validation Signaling and Evolution

## Goal

Clarify and evolve the layers above Nursery where validation becomes social, inter-agent, or attestation-oriented.

## Major Deliverables

- Validation PR6:
    - trust-channel and attestation evolution guidance
    - higher-layer validation signaling posture

- explicit posture for:
    - trust-channel validation
    - attestation recording
    - deferred higher-layer validation outcomes
- future-facing integration notes for richer open-world validation and interpretation
- clear boundary preservation so higher-layer validation does not leak back downward into PVL or Nursery

## Why This Phase Exists

The layered model extends beyond pre-commit correctness. Higher-layer validation remains important, but should evolve after the bounded descriptor-driven lower layers are coherent.

## Dependencies

- Validation PR4 / validation flow integration
- sufficiently stable signaling and outcome model

## PR Identity

- Validation PR6 / higher-layer validation signaling and evolution

## Exit Criteria

- higher validation layers are clearly separated from PVL and Nursery responsibilities
- deferred and social validation outcomes have an explicit architectural home
- lower-layer validation remains stable while higher layers evolve

---

# 9. Cross-Phase Dependency Summary

## Critical Path

1. Descriptor structural surface
2. Validation rule classification
3. PVL closed-world descriptor rule integration
4. Nursery bounded descriptor rule integration
5. Validation flow integration
6. Cross-subsystem semantic convergence

## Key Dependency Rules

- validation should not finalize rule placement before dependency gravity classification is explicit
- PVL should not consume descriptor-defined rules until descriptor resolution is bounded and reconstructible
- Nursery should not finalize value-level checks before `ValueDescriptor` semantics exist
- validation should not become the second home of operator semantics once descriptors own them
- command and dance precondition semantics should not harden outside descriptor ownership

---

# 10. Parallel Work Guidance

## Safe Earlier Work

- validation implementation sequence planning
- dependency-gravity-based rule classification
- issue definition for PVL-safe and Nursery-safe rule families
- inventory of existing validation logic that should migrate toward descriptor ownership

## Safe Once Descriptor Structural Surface Exists

- PVL closed-world descriptor rule integration
- Nursery structural rule integration
- descriptor graph invalidity handling
- tests for bounded structural validation behavior

## Safe Once Descriptor Value Semantics Exist

- Nursery value-level validation
- shared operator/value semantic consumption
- command/dance precondition alignment where descriptor semantics are real

## Safe Once Query / Dance Structural Work Matures

- convergence work for query/filter semantics
- alignment of dance precondition categories with validation layers

---

# 11. Recommended Initial Issue / PR Sequence

A likely issue sequence is:

1. Validation PR1
   - classify descriptor-defined rule families by enforcement layer
   - define the validation adoption boundary
2. Validation PR2
   - integrate PVL-safe closed-world descriptor rules
3. Validation PR3
   - integrate bounded Nursery descriptor rules
4. Validation PR4
   - wire descriptor-driven validation into the staged validation flow
5. Validation PR5
   - align query/command/dance consumers with descriptor-owned validation semantics
6. Validation PR6
   - evolve trust-channel and attestation signaling posture

---

# 12. Immediate Next Step

The immediate next step should be to define the first structural issue in this sequence:

- dependency-gravity-based rule classification
- PVL vs Nursery vs deferred rule-placement framework
- explicit statement of which descriptor-defined rule families are safe to adopt once Descriptor Phase 2 and Phase 3 land

That issue is the natural entry point for the validation track.
