# Validation Implementation Plan — v2.0
## Descriptor-Driven Layered Validation Delivery Sequence

## 1. Purpose

This document defines the implementation plan for MAP validation after extracting the EffectiveDescriptor foundation into the Descriptor Runtime Platform track.

Validation now consumes the runtime descriptor platform rather than owning it.

This plan focuses on:

- rule placement and validation-layer boundaries
- PVL validation against published EffectiveDescriptors
- Integrity Zome integration
- SmartLink validation
- Nursery validation
- transaction validation lifecycle
- ValidationResult / receipt evidence
- cross-subsystem semantic convergence
- higher-layer validation signaling
- import and diagnostics integration

This plan assumes the EffectiveDescriptor Implementation Plan owns:

- `EffectiveDescriptorDigest`
- `EffectiveDescriptorHash`
- canonical DAG-CBOR payloads
- BLAKE3 digest verification
- `EffectiveDescriptor` payloads
- `EffectiveDescriptor` holons
- `CompiledFrom` / `CompiledInto`
- EffectiveDescriptor compilation
- `DescriptorsCache`
- TypeActivation and activated descriptor sets
- runtime descriptor surface APIs

---

## 2. Delivery Principles

- Validation consumes descriptor semantics; it does not invent a parallel rule system.
- Validation does not compile EffectiveDescriptors.
- PVL validates against bounded, content-addressed EffectiveDescriptor holons.
- PVL must not traverse live Descriptor Graphs.
- PVL must not depend on ReferenceLayer caches, Nursery, query services, Dance dispatch, or TrustChannel interpretation.
- Nursery owns richer transaction-local validation that exceeds PVL’s boundedness.
- ValidationResults / receipts remain evidence for non-PVL validation, warnings, deferred checks, audit, trust, and attestation.
- Structural validity is enforced by Integrity / PVL.
- Semantic validity is contextual and layered.
- Higher-layer trust and attestation semantics must not leak downward into PVL.

---

## 3. External Dependencies

This plan depends on the EffectiveDescriptor Implementation Plan.

### Required before PVL integration

- EffectiveDescriptor Payload Model
- EffectiveDescriptor Holon Model and Relationships
- EffectiveDescriptor Compilation Pipeline
- DAG-CBOR and BLAKE3 ValueTypes

### Required before Nursery validation

- Runtime Descriptor Surface APIs
- EffectiveDescriptor lookup via TypeActivation
- EffectiveDescriptor deserialization from `EffectiveDescriptorDagCbor`

### Required before Import validation

- Runtime Descriptor Surface APIs
- TypeActivation support
- EffectiveDescriptor diagnostics and fixtures

### Required before Trust / Agreement validation

- RoleAccessDescriptor model
- RoleAccessDescriptor compilation
- TrustChannel / ExternalId resolution integration

---

## 4. Milestone Overview

### Milestone 1 — Validation Rule Placement

Outcome:

- descriptor-defined rule families are assigned to the correct validation layer
- PVL boundaries are explicit
- Nursery, TrustChannel, and Attestation responsibilities are clear

Primary PR:

- PR 0 — Validation Rule Classification and Adoption Boundary — 3 pts

---

### Milestone 2 — PVL Foundation

Outcome:

- committed holons bind to exact EffectiveDescriptor artifacts selected through activation-aware coordinator flows
- PVL can validate HolonNodes against EffectiveDescriptors
- Integrity validation retrieves EffectiveDescriptors through deterministic Holochain dependency lookup
- SmartLinks receive bounded structural validation

Primary PRs:

- PR 1 — HolonNode EffectiveDescriptor Binding — 3 pts
- PR 2 — PVL Core Crate — 5 pts
- PR 3 — Integrity Zome PVL Integration — 8 pts
- PR 4 — SmartLink PVL Validation — 5 pts

---

### Milestone 3 — Nursery and Transaction Validation

Outcome:

- Nursery validates staged transactions using EffectiveDescriptors
- transaction lifecycle incorporates validation outcomes
- ValidationResults / receipts preserve warning, deferred, and non-PVL validation evidence

Primary PRs:

- PR 5 — Nursery Validation Uses EffectiveDescriptors — 5 pts
- PR 6 — Transaction Manager Integration — 5 pts
- PR 7 — Validation Outcomes and ValidationResult Receipts — 3 pts

---

### Milestone 4 — Cross-Subsystem Semantic Convergence

Outcome:

- validation, query, commands, dances, and DAHN consume descriptor-owned semantics consistently
- duplicated validation logic is reduced or deprecated

Primary PR:

- PR 8 — Cross-Subsystem Semantic Convergence — 8 pts

---

### Milestone 5 — Trust and Agreement Validation

Outcome:

- validation integrates with agreement-mediated access and trust interpretation without collapsing those semantics into PVL

Primary PRs:

- PR 9 — Validation Integration with RoleAccessDescriptors — 5 pts
- PR 10 — Higher-Layer Validation Signaling — 5 pts

---

### Milestone 6 — Import and Diagnostics

Outcome:

- import flows respect descriptor activation and validation
- validation failures, warnings, deferred outcomes, and unresolved dependencies are explainable

Primary PRs:

- PR 11 — Import Pipeline Validation Integration — 5 pts
- PR 12 — Validation Diagnostics and Fixtures — 5 pts

---

## 5. PR 0 — Validation Rule Classification and Adoption Boundary

Estimate: 3 pts

### Goal

Classify descriptor-defined rule kinds by enforcement layer before implementation hardens.

### Deliverables

- dependency-gravity-based rule classification framework
- explicit classification of descriptor-defined rules into:
  - intrinsic PVL rules
  - EffectiveDescriptor-backed PVL rules
  - Nursery-only bounded transaction/snapshot rules
  - receipt/evidence-backed coordinator rules
  - TrustChannel / Agreement rules
  - Attestation / social resolution rules
  - deferred higher-layer rules
- initial mapping of rule families:
  - property requiredness
  - enum membership
  - value type validation
  - bounded cardinality
  - referential integrity
  - lifecycle transitions
  - transaction coherence
  - post-transaction duplicate detection
  - command preconditions
  - dance preconditions
  - dynamic validation rule categories
  - agreement-level rules
  - social/open-world rules
- explicit statement of what must not enter PVL:
  - live descriptor graph traversal
  - ReferenceLayer access
  - HolonsCache / DescriptorsCache access
  - dynamic rule dispatch
  - Dance execution
  - agreement interpretation
  - global uniqueness
  - open-world graph traversal

### Dependencies

- validation architecture baseline
- dependency gravity baseline
- EffectiveDescriptor design baseline

### Exit Criteria

- rule placement vocabulary is explicit
- downstream PVL work has a clear adoption boundary
- no validation stream needs to guess whether a rule belongs in PVL, Nursery, TrustChannel, or Attestation

---

## 6. PR 1 — HolonNode EffectiveDescriptor Binding

Estimate: 3 pts

### Goal

Ensure committed holons carry the content-addressed EffectiveDescriptor needed for validation.

### Deliverables

- add committed `effective_descriptor_hash` field for ordinary HolonNodes
- update HolonNode builders to populate `effective_descriptor_hash` from active TypeActivation
- verify selected EffectiveDescriptor is active in the current AgentSpace before commit
- preserve normal `DescribedBy` SmartLinks for graph semantics and introspection
- tests for:
  - missing EffectiveDescriptor binding
  - inactive EffectiveDescriptor
  - malformed or non-EffectiveDescriptor binding
  - valid active binding

### Key Outcome

Peer validation does not need to chase `DescribedBy` SmartLinks to discover the descriptor surface.

### Dependencies

EffectiveDescriptor track:

- TypeActivation Schema and Lifecycle
- Activated Descriptor Set and Recognition Filtering
- Runtime Descriptor Surface APIs
- EffectiveDescriptor Holon Model and Relationships

### Exit Criteria

- HolonNode contains direct descriptor binding for peer validation
- graph-level `DescribedBy` remains intact
- commit path rejects missing or inactive EffectiveDescriptor bindings where required

---

## 7. PR 2 — PVL Core Crate

Estimate: 5 pts

### Goal

Create the small deterministic validation kernel shared by coordinator and integrity.

### Deliverables

- `map_pvl_core`
- canonical decoding of EffectiveDescriptor payload
- supported PVL constraint types
- HolonNode Class A intrinsic envelope checks
- EffectiveDescriptor artifact bootstrap checks
- HolonNode Class C descriptor binding checks
- HolonNode Class D EffectiveDescriptor-backed structural checks
- SmartLink Class A intrinsic envelope and anti-graffiti checks
- property presence checks
- value type checks
- enum checks
- key rule checks
- optional SmartLink Class B relationship typing checks if adopted by the launch DNA
- resource-bound enforcement
- unknown format, opcode, and required-rule rejection
- PVL error model
- tests for PVL-safe rule evaluation
- dependency guardrails ensuring no dependency on:
  - ReferenceLayer
  - Nursery
  - HolonsCache
  - DescriptorsCache
  - DanceService
  - Query Engine
  - TrustChannels
  - Agreements

### Key Outcome

A deterministic PVL kernel exists for rules that every peer can independently evaluate.

### Dependencies

EffectiveDescriptor track:

- EffectiveDescriptor Payload Model
- DAG-CBOR and BLAKE3 ValueTypes

Validation track:

- PR 0

### Exit Criteria

- PVL kernel can validate a HolonNode against a deserialized EffectiveDescriptor
- PVL kernel can bootstrap-validate an EffectiveDescriptor artifact
- dependency graph confirms no coordinator/runtime imports
- PVL constraints are limited to PR 0-approved rule families

---

## 8. PR 3 — Integrity Zome PVL Integration

Estimate: 8 pts

### Goal

Integrate PVL into the Integrity Zome so peers independently validate HolonNodes against EffectiveDescriptors.

### Deliverables

- read `effective_descriptor_hash` from HolonNode
- retrieve EffectiveDescriptor carrier with deterministic Holochain dependency lookup
- return unresolved dependency if EffectiveDescriptor is unavailable
- bootstrap-validate the EffectiveDescriptor carrier
- extract `EffectiveDescriptorDagCbor`
- verify `EffectiveDescriptorDigest == BLAKE3(EffectiveDescriptorDagCbor)`
- deserialize EffectiveDescriptor payload from canonical DAG-CBOR
- derive the HolonNode type claim from the decoded EffectiveDescriptor payload
- run `map_pvl_core`
- tests for:
  - valid descriptor dependency
  - missing descriptor dependency
  - invalid descriptor binding
  - malformed HolonNode
  - malformed EffectiveDescriptor carrier
  - malformed EffectiveDescriptor payload
  - unsupported PVL construct
  - unresolved dependency retry behavior where testable

### Key Outcome

HolonNode peer validation is deterministic, bounded, and descriptor-aware without live descriptor graph traversal.

### Dependencies

EffectiveDescriptor track:

- EffectiveDescriptor Payload Model
- EffectiveDescriptor Holon Model and Relationships
- EffectiveDescriptor Compilation Pipeline
- DAG-CBOR and BLAKE3 ValueTypes

Validation track:

- PR 1
- PR 2

### Exit Criteria

- Integrity validation uses Holochain deterministic dependency retrieval
- EffectiveDescriptor retrieval uses entry-hash retrieval and re-verifies carrier validity locally
- no live descriptor graph traversal occurs in integrity
- no ReferenceLayer or cache access occurs in integrity
- malformed or mismatched EffectiveDescriptor bindings fail validation
- missing EffectiveDescriptors produce unresolved dependency rather than false invalidity

---

## 9. PR 4 — SmartLink PVL Validation

Estimate: 5 pts

### Goal

Bring relationship operations into bounded peer validation without treating open-world relationship semantics as DHT admissibility.

### Deliverables

- SmartLink Class A intrinsic envelope and anti-graffiti validation
- fixed endpoint-shape and authorship-policy validation
- canonical link-tag and relationship-key validation
- link delete shape validation
- inverse-link provenance validation where adopted by fixed DNA policy
- optional SmartLink Class B relationship typing decision:
  - relationship lookup from bounded EffectiveDescriptor context
  - source/target type conformance using decoded EffectiveDescriptor payloads
  - descriptor-defined tag-shape requirements
- unresolved dependency handling
- explicit exclusions for:
  - relationship cardinality, unless a future transaction-manifest mechanism makes the specific case PVL-bounded
  - global absence
  - exclusivity
  - global uniqueness
  - open-world relationship constraints
- tests for:
  - valid SmartLink
  - invalid link tag encoding
  - invalid relationship key shape
  - invalid endpoint shape
  - unauthorized third-party link authorship under fixed DNA policy
  - invalid inverse-link provenance where inverse links are adopted
  - optional Class B invalid relationship key or target type, if Class B is adopted
  - relationship semantics that must defer to Nursery or higher layers

### Key Outcome

SmartLinks are peer-admissible only when their intrinsic link shape and fixed authorship rules are valid. Optional descriptor-backed relationship typing is a conscious DNA-level decision.

### Dependencies

Validation track:

- PR 3

EffectiveDescriptor track:

- EffectiveDescriptor Payload Model includes relationship surfaces

### Exit Criteria

- SmartLinks pass through PVL validation
- SmartLink Class A is implemented independently of descriptor graph traversal
- SmartLink Class B is explicitly adopted or deferred
- link validation does not enforce global absence/exclusivity
- unresolved dependencies are handled correctly

---

## 10. PR 5 — Nursery Validation Uses EffectiveDescriptors

Estimate: 5 pts

### Goal

Align coordinator-side validation with the same EffectiveDescriptor surface used by PVL.

### Deliverables

- Nursery loads active EffectiveDescriptors through Runtime Descriptor Surface APIs
- Nursery deserializes EffectiveDescriptor payloads from `EffectiveDescriptorDagCbor`
- transaction-local validation
- multi-holon consistency checks
- required / warning / deferred classification
- bounded snapshot checks
- optional dynamic rule execution above PVL where allowed
- tests for bounded pre-commit validation behavior

### Key Outcome

Richer validation uses the same descriptor surface as PVL without forcing those rules into integrity.

### Dependencies

EffectiveDescriptor track:

- Runtime Descriptor Surface APIs
- TypeActivation Schema and Lifecycle
- Activated Descriptor Set and Recognition Filtering

Validation track:

- PR 0
- PR 2

### Exit Criteria

- Nursery executes bounded descriptor-defined rules that do not belong in PVL
- validation outcomes are classified as fail, warning, or deferred
- higher-gravity validation no longer pressures PVL to expand unsafely

---

## 11. PR 6 — Transaction Manager Integration

Estimate: 5 pts

### Goal

Make validation part of the transaction commit lifecycle.

### Deliverables

- transaction states:
  - Provisional
  - Validated
  - Failed
  - Committed
  - CommittedWithWarnings
- enforce required Nursery validation before commit
- preserve warnings and deferred checks
- attach ValidationResults where useful
- commit only HolonNodes with active EffectiveDescriptor bindings where required
- tests for:
  - valid transaction commit
  - hard-fail validation abort
  - commit with warnings
  - deferred validation outcome
  - missing descriptor binding

### Key Outcome

Semantic commit boundaries are explicit and validation-aware.

### Dependencies

Validation track:

- PR 5

Transaction infrastructure baseline.

### Exit Criteria

- validation state transitions are part of commit flow
- invalid transactions fail before DHT write
- warnings/deferred outcomes can be preserved and surfaced

---

## 12. PR 7 — Validation Outcomes and ValidationResult Receipts

Estimate: 3 pts

### Goal

Retain validation evidence for non-PVL and higher-layer validation outcomes.

### Deliverables

- `ValidationResult` / receipt model
- outcome categories:
  - Fail
  - Valid
  - Warning
  - Deferred
- optional digest binding to transaction or committed data
- descriptor identity binding
- rule-set or rule identity where applicable
- validator identity and signature where useful
- linkage from Transaction to ValidationResults
- audit-friendly representation
- tests for ValidationResult creation and linkage

### Key Outcome

Validation receipts remain available as evidence without replacing peer validation.

### Dependencies

Validation track:

- PR 5
- PR 6

### Exit Criteria

- Nursery and Transaction Manager can record validation outcomes
- receipts are not treated as primary PVL proof unless explicitly adopted by PVL-safe rules
- warnings and deferred checks have durable representation

---

## 13. PR 8 — Cross-Subsystem Semantic Convergence

Estimate: 8 pts

### Goal

Ensure validation semantics converge with query, command, dance, and DAHN consumers.

### Deliverables

- shared descriptor-owned value/operator semantics where validation overlaps with query filtering
- alignment with command preconditions
- alignment with dance preconditions
- deprecation plan for duplicated validation logic
- guidance for DAHN-facing validation display without frontend semantic ownership
- documented shared use of Runtime Descriptor Surface APIs
- tests or fixtures showing common descriptor semantics consumed by multiple subsystems

### Key Outcome

Validation, query, commands, dances, and DAHN consume one descriptor-owned semantic surface where appropriate.

### Dependencies

EffectiveDescriptor track:

- Runtime Descriptor Surface APIs
- DAHN Consumption of EffectiveDescriptors, where applicable

Validation track:

- PR 5

Other tracks:

- query/command/dance structural readiness

### Exit Criteria

- permanent parallel rule systems are shrinking
- descriptor semantics are reused across subsystems
- DAHN does not invent its own validation semantics

---

## 14. PR 9 — Validation Integration with RoleAccessDescriptors

Estimate: 5 pts

### Goal

Clarify how validation interacts with agreement-derived access surfaces without collapsing access policy into PVL.

### Deliverables

- validation posture for RoleAccessDescriptors
- checks that access-related validation belongs to TrustChannel / Agreement layer unless explicitly PVL-safe
- integration points for:
  - role-based read access
  - projection validation
  - outbound relationship filtering
  - agreement-mediated visibility
- tests for:
  - access-surface validation as higher-layer concern
  - no PVL dependency on RoleAccessDescriptor interpretation

### Key Outcome

Validation integrates with access-control surfaces while preserving validation-layer boundaries.

### Dependencies

EffectiveDescriptor / Access track:

- RoleAccessDescriptor Model
- RoleAccessDescriptor Compilation
- TrustChannel / ExternalId Resolution Integration

Validation track:

- PR 0
- PR 7

### Exit Criteria

- RoleAccessDescriptor is not confused with EffectiveDescriptor
- access validation remains above PVL unless specifically classified otherwise
- TrustChannel validation has clear handoff points from ValidationResults and deferred outcomes

---

## 15. PR 10 — Higher-Layer Validation Signaling

Estimate: 5 pts

### Goal

Clarify and evolve the layers above Nursery where validation becomes social, inter-agent, or attestation-oriented.

### Deliverables

- posture for TrustChannel validation
- posture for attestation recording
- deferred validation signaling
- conflict signaling through:
  - `ConflictsWith` links
  - conflict holons
  - ValidationResults
  - attestations
- explicit boundary preservation so higher-layer validation does not leak into PVL or Nursery
- tests or fixtures for deferred validation signaling

### Key Outcome

Open-world and social validation outcomes have an architectural home.

### Dependencies

Validation track:

- PR 7
- PR 9

Trust / Attestation readiness.

### Exit Criteria

- deferred and social validation outcomes are represented coherently
- lower-layer validation remains stable while higher layers evolve
- conflict detection and resolution are not confused with DHT admissibility

---

## 16. PR 11 — Import Pipeline Validation Integration

Estimate: 5 pts

### Goal

Make JSON/import flows respect descriptor activation and validation.

### Deliverables

- imported holons resolve active EffectiveDescriptors
- import path populates `effective_descriptor_hash`
- import path runs Nursery validation before DHT write
- import-time errors for inactive or missing descriptor bindings
- ValidationResults for import warnings/deferred outcomes
- tests for:
  - valid import
  - missing type activation
  - invalid EffectiveDescriptor binding
  - warning/deferred import checks

### Key Outcome

Imports no longer bypass descriptor activation or validation.

### Dependencies

EffectiveDescriptor track:

- Runtime Descriptor Surface APIs
- TypeActivation Schema and Lifecycle
- Activated Descriptor Set and Recognition Filtering
- EffectiveDescriptor Diagnostics and Fixtures

Validation track:

- PR 6
- PR 7

### Exit Criteria

- import pipeline participates in Nursery and PVL validation flow
- imported holons carry active EffectiveDescriptor bindings
- import errors are explainable

---

## 17. PR 12 — Validation Diagnostics and Fixtures

Estimate: 5 pts

### Goal

Make validation behavior observable and debuggable.

### Deliverables

- explain PVL validation failure
- explain unresolved descriptor dependencies
- explain EffectiveDescriptor binding mismatch
- explain unrecognized but structurally valid data hidden by activation filtering
- explain Nursery validation failures
- explain warning/deferred outcomes
- explain receipt / ValidationResult linkage
- fixtures for:
  - valid HolonNode validation
  - invalid HolonNode validation
  - missing EffectiveDescriptor dependency
  - malformed EffectiveDescriptor payload
  - invalid SmartLink
  - warning outcome
  - deferred outcome
  - TrustChannel/deferred validation signaling

### Key Outcome

Developers can understand why validation passed, failed, warned, deferred, or could not resolve dependencies.

### Dependencies

Validation track:

- PR 3 through PR 11

EffectiveDescriptor track:

- EffectiveDescriptor Diagnostics and Fixtures

### Exit Criteria

- validation failures are explainable
- regression fixtures cover major validation invariants
- diagnostics distinguish PVL failure, Nursery failure, deferred checks, and unresolved dependencies

---

## 18. Cross-Phase Dependency Summary

### Critical Validation Path

1. Validation Rule Classification
2. HolonNode EffectiveDescriptor Binding
3. PVL Core Crate
4. Integrity Zome PVL Integration
5. SmartLink PVL Validation
6. Nursery Validation
7. Transaction Manager Integration
8. Validation Outcomes / ValidationResults
9. Import Validation
10. Diagnostics

### External Descriptor Runtime Dependencies

From the EffectiveDescriptor track:

1. EffectiveDescriptor Payload Model
2. EffectiveDescriptor Holon Model and Relationships
3. EffectiveDescriptor Compilation Pipeline
4. DAG-CBOR and BLAKE3 ValueTypes
5. TypeActivation Schema and Lifecycle
6. Activated Descriptor Set and Recognition Filtering
7. Runtime Descriptor Surface APIs
8. EffectiveDescriptor Diagnostics and Fixtures

### Trust / Access Dependencies

From Trust and Access tracks:

1. RoleAccessDescriptor Model
2. RoleAccessDescriptor Compilation
3. TrustChannel / ExternalId Resolution Integration
4. Attestation support, where applicable

---

## 19. Parallel Work Guidance

### Safe Early Validation Work

- PR 0 rule classification
- validation logic audit
- PVL boundary documentation
- validation outcome vocabulary
- ValidationResult model sketching

### Safe Once EffectiveDescriptor Payload Exists

- PVL core crate
- validation fixtures around deserialized EffectiveDescriptor payloads

### Safe Once TypeActivation Exists

- HolonNode EffectiveDescriptor binding
- import validation planning
- Nursery lookup planning

### Safe Once Runtime Descriptor APIs Exist

- Nursery validation
- import pipeline validation
- cross-subsystem convergence

### Safe Once Integrity Binding Exists

- Integrity Zome PVL integration
- SmartLink PVL validation
- PVL diagnostics

### Safe Once Trust / Access Work Exists

- RoleAccessDescriptor validation integration
- higher-layer validation signaling
- deferred TrustChannel validation workflows

---

## 20. Recommended Initial Issue Sequence

A likely initial issue sequence is:

1. PR 0 — Validation Rule Classification and Adoption Boundary
2. PR 1 — HolonNode EffectiveDescriptor Binding
3. PR 2 — PVL Core Crate
4. PR 3 — Integrity Zome PVL Integration
5. PR 4 — SmartLink PVL Validation
6. PR 5 — Nursery Validation Uses EffectiveDescriptors
7. PR 6 — Transaction Manager Integration
8. PR 7 — Validation Outcomes and ValidationResult Receipts
9. PR 11 — Import Pipeline Validation Integration
10. PR 12 — Validation Diagnostics and Fixtures

PRs 8–10 should be scheduled when query, command, dance, DAHN, TrustChannel, RoleAccessDescriptor, and Attestation tracks are sufficiently mature.

---

## 21. Immediate Next Step

The immediate next step is to define PR 0:

- dependency-gravity-based rule classification
- intrinsic PVL vs EffectiveDescriptor-backed PVL vs Nursery-only vs deferred rule-placement framework
- explicit rule families to classify
- explicit exclusions from PVL
- relationship between EffectiveDescriptor-backed validation and non-PVL ValidationResults

This issue remains the natural validation entry point because it prevents implementation work from accidentally pulling descriptor graph traversal, ReferenceLayer access, dynamic validation rule dispatch, or agreement interpretation into integrity validation.
