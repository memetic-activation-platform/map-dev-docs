# Validation Implementation Plan (v1.1)
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
- PVL remains the integrity-local, bounded, peer-reproducible enforcement and verification layer
- integrity validation must not perform live descriptor graph resolution, reference-layer lookup, coordinator-cache access, or dynamic validation rule dispatch
- Nursery remains the bounded pre-commit environment for richer descriptor-backed checks and validation receipt generation
- dependency gravity determines where descriptor-defined rules may safely execute and whether their outcomes need proof-carrying evidence

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
- PVL should remain minimal, bounded, local, and reproducible
- PVL should verify descriptor-linked validation claims through local digest/signature checks rather than re-running coordinator-only work
- Nursery should absorb bounded validation that dependency gravity rejects from PVL
- validation should not finalize semantics before the relevant descriptor surfaces are real
- command, query, and dance work should reuse descriptor-defined validation semantics where appropriate

---

# 2. Phase Overview

The recommended validation implementation sequence is:

1. Structural Rule Classification and Adoption Boundary
2. Integrity PVL Substrate and Proof-Carrying Boundary
3. Nursery Bounded Descriptor Rule Integration
4. Validation Flow and Outcome Integration
5. Cross-Subsystem Semantic Convergence
6. Higher-Layer Validation Signaling and Evolution

The recommended PR segmentation is:

1. Validation PR1 — Structural Rule Classification and Adoption Boundary
2. Validation PR2 — Integrity PVL Substrate and Proof-Carrying Boundary
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
    - intrinsic PVL rules
    - artifact-backed PVL rules
    - receipt-verified coordinator rules
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
    - dynamic validation rule categories

## Why This Phase Exists

Validation cannot safely become descriptor-driven simply by moving logic into validators. The architecture requires a classification step that uses dependency gravity to decide where descriptor-defined rules may execute.

Without this phase:

- PVL risks absorbing rules that exceed its boundary
- proof-carrying validation risks being treated as an afterthought rather than the bridge between coordinator validation and integrity verification
- Nursery risks becoming an unstructured catch-all
- downstream work may harden around temporary or duplicated rule placements

## Dependencies

- Descriptor PR1 / runtime spine
- validation architecture baseline
- dependency gravity baseline

## PR Identity

- Validation PR1 / structural rule classification and adoption boundary

## Exit Criteria

- descriptor-defined rule classes are explicitly mapped to enforcement and verification layers
- the team has a clear rule-placement vocabulary grounded in dependency gravity
- no validation stream needs to guess whether a rule belongs in PVL, artifact-backed PVL, receipt-verified Nursery validation, or above

---

# 4. Phase 2 — Integrity PVL Substrate and Proof-Carrying Boundary

## Goal

Define the minimal integrity-side validation substrate and the proof-carrying boundary between coordinator validation and peer validation before adopting any descriptor-backed PVL rules.

## Major Deliverables

- Validation PR2:
    - integrity-side PVL substrate for local structure and cryptographic evidence checks
    - proof-carrying validation receipt posture
    - explicit no-live-descriptor-resolution rule for integrity validation

- minimal PVL checks for:
    - `HolonNode` / `SmartLink` well-formedness
    - descriptor identity field shape and consistency
    - validation receipt input digest, descriptor identity, rule-set identity, validator identity, and signature consistency
    - validator / rule-set / engine acceptability only where the acceptance rule is integrity-local
- definition of the safe channels through which descriptor semantics may affect integrity:
    - fixed DNA semantics
    - integrity-local PVL artifacts
    - explicit validation evidence
- guidance for when descriptor-backed rules can later be adopted as artifact-backed PVL
- tests for peer-reproducible local validation and receipt verification behavior
- explicit exclusions for:
    - live descriptor graph resolution
    - reference-layer and coordinator-cache access
    - open-world graph traversal
    - runtime plugin/module loading
    - Dance-based validation rule execution
    - non-reconstructible context

## Why This Phase Exists

The architecture says descriptors define rules, but integrity may execute only what is local, fixed, or explicitly carried. This phase makes the integrity boundary real before any descriptor-backed rule is adopted into PVL.

Without this phase, "descriptor-backed PVL" can accidentally reintroduce the original dependency-gravity problem: descriptor graph traversal pulls in reference-layer services, coordinator caches, dynamic rule engines, and eventually DHT churn.

## Dependencies

- Validation PR1 / classification boundary
- Holochain entry/link storage representation clear enough to carry descriptor identity and validation evidence
- signature/digest primitives available in integrity-safe code
- Descriptor Phase 2 / schema-backed structural descriptor surface for receipt identity binding

## PR Identity

- Validation PR2 / integrity PVL substrate and proof-carrying boundary

## Exit Criteria

- PVL validates local structure and proof-carrying evidence without live descriptor resolution
- integrity validation remains reproducible, bounded, and independent of coordinator/runtime services
- the project has an explicit adoption path for later artifact-backed descriptor PVL
- PVL has not absorbed higher-layer runtime responsibilities, dynamic rule dispatch, or reference-layer lookup

---

# 5. Phase 3 — Nursery Bounded Descriptor Rule Integration

## Goal

Make Nursery the real home of bounded descriptor-driven validation that exceeds PVL but remains meaningfully checkable before commit.

## Major Deliverables

- Validation PR3:
    - Nursery integration for bounded transaction/snapshot-aware descriptor rules
    - required / warning / deferred rule categorization in practice
    - validation receipt generation for rules whose outcomes must be bound to commits

- bounded transaction-context evaluation of descriptor-defined rules
- descriptor graph resolution and inherited descriptor flattening in coordinator/runtime context
- local snapshot-aware checks such as:
    - post-transaction cardinality
    - transaction coherence
    - duplicate detection
    - bounded query/filter-style checks
- dynamic validation rule execution where allowed by the rule-placement classification
- explicit separation of:
    - hard-fail required checks
    - warning-level advisory checks
    - deferred higher-layer outcomes
- tests for bounded pre-commit validation behavior

## Why This Phase Exists

Dependency gravity rejects many meaningful descriptor-defined checks from PVL. Nursery exists to absorb exactly that work without pulling runtime complexity downward into integrity, then bind the relevant outcome to committed data when peers need local evidence that validation occurred.

## Dependencies

- Validation PR1 / classification boundary
- Descriptor Phase 2 / structural descriptor surface
- Descriptor Phase 3 / `ValueDescriptor` semantics for value-level checks
- transaction and snapshot context available to Nursery
- Validation PR2 / validation receipt boundary

## PR Identity

- Validation PR3 / Nursery bounded descriptor rule integration

## Exit Criteria

- Nursery executes bounded descriptor-defined rules that do not belong in PVL
- required / warning / deferred validation categories are operationally meaningful
- coordinator-side validation can produce validation receipts suitable for integrity verification
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
- validation receipt handling for:
    - descriptor identity binding
    - input digest binding
    - rule-set / engine identity binding
    - validator identity and signature verification
- integration of uniqueness/conflict patterns with the layered validation model
- tests for validation flow and outcome signaling

## Why This Phase Exists

Rule placement alone is not enough. Validation outcomes must fit the real transaction and propagation flow so that descriptor-driven rules influence user and system behavior coherently. The flow must also make clear which outcomes are re-executed by integrity and which are verified as signed evidence from coordinator-side validation.

## Dependencies

- Validation PR2 / integrity PVL substrate and proof-carrying boundary
- Validation PR3 / Nursery integration
- transaction lifecycle and commit flow stable enough to consume validation outcomes

## PR Identity

- Validation PR4 / validation flow and outcome integration

## Exit Criteria

- descriptor-driven validation is integrated into the staged validation flow
- validation outcomes are explicit and consistent across layers
- validation receipts are consistently produced, carried, and verified where required
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

- Validation PR2 / integrity PVL substrate and proof-carrying boundary
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
3. Integrity PVL substrate and validation receipt boundary
4. Nursery bounded descriptor and dynamic rule integration
5. Validation flow integration
6. Cross-subsystem semantic convergence

## Key Dependency Rules

- validation should not finalize rule placement before dependency gravity classification is explicit
- PVL should not consume descriptor-defined rules until the rule is fixed, artifact-backed, or explicitly carried in a bounded context
- coordinator-only validation should produce local verification evidence when its outcome must be bound to committed data
- Nursery should not finalize value-level checks before `ValueDescriptor` semantics exist
- validation should not become the second home of operator semantics once descriptors own them
- command and dance precondition semantics should not harden outside descriptor ownership

---

# 10. Parallel Work Guidance

## Safe Earlier Work

- validation implementation sequence planning
- dependency-gravity-based rule classification
- issue definition for intrinsic PVL, artifact-backed PVL, receipt-verified, and Nursery-safe rule families
- inventory of existing validation logic that should migrate toward descriptor ownership
- validation receipt shape exploration

## Safe Once Descriptor Structural Surface Exists

- integrity-local descriptor identity binding
- artifact-backed PVL candidate evaluation
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
   - define integrity-local PVL checks and validation receipt verification
3. Validation PR3
   - integrate bounded Nursery descriptor rules and receipt generation
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
- intrinsic PVL vs artifact-backed PVL vs receipt-verified Nursery vs deferred rule-placement framework
- explicit statement of which descriptor-defined rule families are safe to adopt once Descriptor Phase 2 and Phase 3 land
- explicit statement that live descriptor graph resolution, reference-layer access, and validation Dance dispatch do not belong in integrity validation

That issue is the natural entry point for the validation track.
