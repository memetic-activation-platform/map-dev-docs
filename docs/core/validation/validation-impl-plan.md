# Validation Implementation Plan — v1.3
## Descriptor Identity, EffectiveDescriptors, CanonicalBytes, PVL, Caches, and Layered Validation Delivery Sequence

### Change Log from v1.2

v1.3 updates the implementation plan to reflect the latest EffectiveDescriptor representation decisions.

Key changes:

- Clarifies that `EffectiveDescriptor` remains represented as a conventional MAP holon, not a new Holochain `EntryType`.
- Adds `CanonicalBytes` as the storage value type for the serialized `EffectiveDescriptor` payload.
- Clarifies that `EntryHash(EffectiveDescriptor HolonNode)` can serve as the content-addressed identity of the compiled effective surface because the full compiled payload is stored inside the `HolonNode` entry.
- Adds `effective_descriptor_bytes: CanonicalBytes` as the core payload property of the EffectiveDescriptor holon.
- Adds explicit serialization/deserialization work for the `EffectiveDescriptor` struct.
- Adds `CompiledFrom` / `CompiledInto` relationship modeling:
  - `CompiledFrom` is definitional for `EffectiveDescriptor`.
  - `CompiledInto` is non-definitional for `HolonType`.
- Clarifies that `EffectiveDescriptor` performs three compressions:
  - inheritance compression
  - relationship compression
  - space/reference compression
- Updates PVL integration so integrity retrieves an EffectiveDescriptor holon via `must_get_valid_record`, extracts `CanonicalBytes`, deserializes the effective surface, and validates against it.
- Adds point estimates for each PR chunk using the requested heuristic.

### Change Log from v1.1

v1.2 synthesizes the prior validation implementation plan with the newer architecture work around descriptor identity, EffectiveDescriptors, type activation, PVL, and ReferenceLayer caches.

Key changes:

- Adds `DefinitionHash`, `EffectiveDescriptor`, and `EntryHash(EffectiveDescriptor)` as first-class implementation concerns.
- Clarifies that descriptor edits, not type activation, trigger EffectiveDescriptor compilation and semantic version assignment.
- Replaces the earlier primary emphasis on proof-carrying validation receipts with a stronger peer-validation path based on `HolonNode.effective_descriptor_hash` and Holochain `must_get_valid_record`.
- Retains validation receipts as higher-layer evidence for Nursery, warning, deferred, audit, attestation, and non-PVL validation outcomes.
- Adds `DescriptorsCache` beside `HolonsCache` in the ReferenceLayer, with lookup by `DefinitionHash` and `EntryHash(EffectiveDescriptor)`.
- Adds type activation as the Space Manager responsibility that authorizes an EffectiveDescriptor for use in a HolonSpace.
- Adds explicit PRs for HolonNode descriptor binding, PVL core crate, Integrity Zome PVL integration, and SmartLink PVL validation.
- Preserves the v1.1 rule-classification work so descriptor-defined rules are assigned to the proper enforcement layer before implementation hardens.
- Preserves cross-subsystem semantic convergence across validation, query, commands, dances, and DAHN.
- Preserves higher-layer validation signaling for conflicts, attestations, deferred outcomes, and social/open-world validation.
- Adds an audit/migration step for existing validation logic that should move toward descriptor ownership.


---

# 1. Purpose

This document translates the current MAP validation and descriptor architecture into a dependency-aware implementation sequence.

It is intended to:

- break validation delivery into concrete, reviewable pull requests
- honor dependencies between descriptor identity, EffectiveDescriptors, CanonicalBytes, PVL, Nursery validation, and TrustChannel mediation
- distinguish descriptor rule ownership from enforcement-layer execution
- prevent PVL from absorbing runtime/coordinator responsibilities
- ensure validation, query, command, and dance semantics converge on descriptor-owned definitions
- provide a basis for issue definition, sequencing, and parallel work decisions

This plan assumes:

- descriptors own validation semantics
- validation layers own evaluation authority
- EffectiveDescriptors are the canonical flattened runtime descriptor surface
- descriptor edits produce DefinitionHashes, EffectiveDescriptors, and semantic versions
- EffectiveDescriptors are stored as normal `HolonNode`s with a canonical serialized payload
- type activation authorizes EffectiveDescriptors for use within a HolonSpace
- committed HolonNodes carry the content-addressed EffectiveDescriptor required for peer validation
- PVL remains the bounded, deterministic, peer-reproducible validation layer
- integrity validation must not perform live descriptor graph traversal, ReferenceLayer lookup, coordinator-cache access, Dance dispatch, dynamic rule loading, or agreement interpretation
- Nursery remains the bounded pre-commit environment for richer descriptor-backed validation
- validation receipts remain useful as evidence, but are not the primary mechanism for preserving Holochain-style peer validation

---

# 2. Delivery Principles

The implementation sequence follows these rules:

- validation must consume descriptor semantics rather than invent a second permanent rule system
- descriptor identity and descriptor use authorization must remain distinct
- descriptor edits create descriptor identity; type activation authorizes use in a HolonSpace
- PVL validates against bounded, content-addressed EffectiveDescriptor holons, not the live Descriptor Graph
- PVL extracts a canonical serialized EffectiveDescriptor payload from `CanonicalBytes`
- PVL remains minimal, bounded, local, deterministic, and reproducible
- Nursery absorbs bounded validation that dependency gravity rejects from PVL
- validation receipts support non-PVL validation evidence, audit, warnings, deferred checks, and attestations
- ReferenceLayer caches improve performance but must not become part of peer validation correctness
- command, query, and dance work should reuse descriptor-owned validation semantics where appropriate
- higher-layer trust and attestation semantics must not leak downward into PVL

---

# 3. Milestone Overview

## Milestone 1 — Rule Placement and Descriptor Identity

Outcome:

- descriptor-defined rule families are classified by enforcement layer
- routable identity is separated from definitional identity
- DefinitionHash is implemented
- descriptor surfaces can be compared by meaning, not route

Primary PRs:

- PR 0 — Validation Rule Classification and Adoption Boundary — 3 pts
- PR 1 — Formalize Identifier Types — 3 pts
- PR 2 — Canonical Definitional Surface — 5 pts
- PR 3 — DefinitionHash Computation for Descriptors — 3 pts
- PR 4 — Existing Validation Logic Migration Audit — 3 pts

---

## Milestone 2 — EffectiveDescriptors, CanonicalBytes, and Descriptor Cache

Outcome:

- EffectiveDescriptors are first-class runtime artifacts
- CanonicalBytes can store deterministic serialized payloads
- descriptor edits compile effective surfaces
- semantic versions are assigned on descriptor semantic change
- DescriptorsCache supports lookup by definitional identity

Primary PRs:

- PR 5 — CanonicalBytes ValueType — 3 pts
- PR 6 — EffectiveDescriptor Payload Model — 5 pts
- PR 7 — EffectiveDescriptor Holon Model and Relationships — 3 pts
- PR 8 — EffectiveDescriptor Compilation Pipeline — 8 pts
- PR 9 — DescriptorsCache in ReferenceLayer — 5 pts

---

## Milestone 3 — Space Activation and Peer Validation

Outcome:

- HolonSpaces activate descriptor surfaces
- HolonNodes bind directly to activated EffectiveDescriptor holons
- PVL validates HolonNodes and SmartLinks against content-addressed EffectiveDescriptors

Primary PRs:

- PR 10 — Space Type Activation Records — 5 pts
- PR 11 — HolonNode References Active EffectiveDescriptor — 3 pts
- PR 12 — PVL Core Crate — 5 pts
- PR 13 — Integrity Zome PVL Integration — 8 pts
- PR 14 — SmartLink PVL Validation — 5 pts

---

## Milestone 4 — Nursery, Transactions, and Validation Outcomes

Outcome:

- Nursery uses EffectiveDescriptors for richer validation
- Transaction Manager enforces validation lifecycle
- fail / warn / defer outcomes are operational
- ValidationResult / receipt evidence is recorded where useful

Primary PRs:

- PR 15 — Nursery Validation Uses EffectiveDescriptors — 5 pts
- PR 16 — Transaction Manager Integration — 5 pts
- PR 17 — Validation Outcomes and ValidationResult Receipts — 3 pts

---

## Milestone 5 — Cross-Subsystem Convergence

Outcome:

- validation, query, commands, dances, and DAHN consume descriptor-owned semantics consistently
- duplicated rule systems are reduced or deprecated

Primary PRs:

- PR 18 — Cross-Subsystem Semantic Convergence — 8 pts

---

## Milestone 6 — Trust Mediation and Role-Based Access

Outcome:

- RoleAccessDescriptors support agreement-mediated access
- TrustChannels mediate foreign holon access without replicating stewarded state

Primary PRs:

- PR 19 — RoleAccessDescriptor Model — 5 pts
- PR 20 — RoleAccessDescriptor Compilation — 8 pts
- PR 21 — TrustChannel / ExternalId Resolution Integration — 8 pts

---

## Milestone 7 — Import, Diagnostics, and Higher-Layer Signaling

Outcome:

- import flows respect descriptor identity, activation, and validation
- developers can explain validation failures and descriptor identity decisions
- deferred and social validation outcomes have a clear signaling posture

Primary PRs:

- PR 22 — Import Pipeline Integration — 8 pts
- PR 23 — Developer Diagnostics and Test Fixtures — 5 pts
- PR 24 — Higher-Layer Validation Signaling and Evolution — 5 pts

---

# 4. PR 0 — Validation Rule Classification and Adoption Boundary

Estimate: 3 pts

## Goal

Classify descriptor-defined rule kinds by enforcement layer before implementation hardens.

## Deliverables

- dependency-gravity-based rule classification framework
- explicit classification of descriptor-defined rules into:
  - intrinsic PVL rules
  - EffectiveDescriptor-backed PVL rules
  - Nursery-only bounded transaction/snapshot rules
  - receipt/evidence-backed coordinator rules
  - deferred higher-layer rules
- initial mapping of rule families:
  - property requiredness
  - enum membership
  - value type validation
  - bounded cardinality
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

## Dependencies

- validation architecture baseline
- dependency gravity baseline

## Exit Criteria

- rule placement vocabulary is explicit
- no validation stream needs to guess whether a rule belongs in PVL, Nursery, TrustChannel, or Attestation
- downstream PVL work has a clear adoption boundary

---

# 5. PR 1 — Formalize Identifier Types

Estimate: 3 pts

## Goal

Establish the identity vocabulary before behavior changes.

## Deliverables

Add or formalize types such as:

- `DefinitionHash`
- `SemanticVersion`
- `EffectiveDescriptorHash`
- `RoutableHolonReference`
- `ExternalId`
- `OutboundProxyId`
- `RemoteObjectId`
- `LocalId`
- `ActionHash`-based committed holon identity
- `EntryHash`-based content identity

## Key Outcome

Routable identity is separated from definitional identity in code.

## Dependencies

- none

## Exit Criteria

- type-level distinction exists between route-sensitive references and path-insensitive definition hashes
- APIs stop overloading `ExternalId` with equivalence semantics

---

# 6. PR 2 — Canonical Definitional Surface

Estimate: 5 pts

## Goal

Define what participates in a descriptor's content identity.

## Deliverables

- canonical serialization for definitional descriptor content
- relationship classification enum:
  - `Definitional`
  - `Operational`
  - `Contextual`
  - `Provenance`
  - `Routing`
- directional relationship classification support
- filtering rules for DefinitionHash computation
- tests proving excluded metadata does not affect definitional identity

## Key Outcome

The canonical definitional surface is deterministic and path-insensitive.

## Dependencies

- PR 1

## Exit Criteria

- definitional relationships are distinguishable from routing/provenance/contextual relationships
- canonical definitional surface is stable under route/provenance changes
- inverse relationships are not assumed to share definitional classification automatically

---

# 7. PR 3 — DefinitionHash Computation for Descriptors

Estimate: 3 pts

## Goal

Compute and store DefinitionHash for descriptor-like holons.

## Deliverables

- `compute_definition_hash(descriptor)`
- optional `definition_hash` field on definitional HolonNodes where appropriate
- validation that stored hash matches canonical definitional surface, where applicable
- tests for descriptors discovered through different ExternalIds producing the same DefinitionHash

## Key Outcome

Equivalent descriptors discovered through different routes share identity.

## Dependencies

- PR 2

## Exit Criteria

- DefinitionHash can be computed deterministically
- path-insensitive descriptor equivalence works in tests

---

# 8. PR 4 — Existing Validation Logic Migration Audit

Estimate: 3 pts

## Goal

Inventory current validation logic and decide which subsystem should own each rule.

## Deliverables

- list of existing validation checks
- classification of each rule under PR 0 categories
- migration recommendations:
  - keep in PVL
  - move to EffectiveDescriptor-backed PVL
  - move to Nursery
  - move to TrustChannel / Agreement
  - move to Attestation / conflict signaling
  - deprecate duplicate logic
- issue list for follow-up migrations

## Dependencies

- PR 0

## Exit Criteria

- current validation logic has an owner
- duplicate rule systems are identified
- implementation can proceed without preserving accidental rule placement

---

# 9. PR 5 — CanonicalBytes ValueType

Estimate: 3 pts

## Goal

Introduce a deterministic binary value type suitable for storing compiled artifacts.

## Deliverables

- `CanonicalBytes` ValueType
- canonical byte wrapper / validation type
- serialization contract documentation
- support in property value encoding/decoding
- tests for round-trip determinism

## Key Outcome

MAP can store deterministic serialized payloads inside conventional `HolonNode`s.

## Dependencies

- PR 1
- existing BaseValue / ValueType infrastructure

## Exit Criteria

- `CanonicalBytes` can be used as a property value
- encoded bytes are byte-for-byte stable
- storage does not depend on generic JSON ordering or formatting

---

# 10. PR 6 — EffectiveDescriptor Payload Model

Estimate: 5 pts

## Goal

Define the deserialized EffectiveDescriptor struct that will be serialized into CanonicalBytes.

## Deliverables

- `EffectiveDescriptor`
- `EffectivePropertySpec`
- `EffectiveRelationshipSpec`
- `EffectiveInverseRelationshipSpec`
- `EffectiveKeyRuleSpec`
- `PvlSurface`
- `NonPvlSemantics`
- value constraint structs
- canonical serialization/deserialization implementation
- encoding version field such as `map.effective-descriptor.v1`
- tests for deterministic serialization

## Key Outcome

EffectiveDescriptor exists as a canonical payload model independent of graph traversal.

## Dependencies

- PR 5
- PR 3
- existing descriptor model

## Exit Criteria

- EffectiveDescriptor can be serialized to and deserialized from `CanonicalBytes`
- canonical payload contains inheritance-compressed, relationship-compressed, and space/reference-compressed semantics
- payload uses keys and definition hashes rather than route-sensitive IDs

---

# 11. PR 7 — EffectiveDescriptor Holon Model and Relationships

Estimate: 3 pts

## Goal

Represent EffectiveDescriptors as conventional MAP holons, not a new Holochain EntryType.

## Deliverables

- `EffectiveDescriptorType`
- required property:
  - `effective_descriptor_bytes: CanonicalBytes`
- relationship:
  - `CompiledFrom`
- inverse relationship:
  - `CompiledInto`
- directional classification:
  - `CompiledFrom` is definitional for `EffectiveDescriptor`
  - `CompiledInto` is non-definitional for `HolonType`
- graph/query support for locating EffectiveDescriptors from source descriptors

## Key Outcome

EffectiveDescriptors are graph-addressable MAP holons with compact compiled payloads.

## Dependencies

- PR 5
- PR 6
- PR 2

## Exit Criteria

- EffectiveDescriptor holons can be created and linked to source HolonType versions
- `CompiledFrom` gives precise ActionHash-based provenance
- `CompiledInto` does not affect HolonType definitional identity

---

# 12. PR 8 — EffectiveDescriptor Compilation Pipeline

Estimate: 8 pts

## Goal

Compile descriptor edits into EffectiveDescriptor holons.

## Deliverables

- descriptor edit hook or service
- inheritance flattening
- relationship compaction
- space/reference compression
- effective inverse relationship computation
- EffectiveDescriptor payload generation
- semantic version assignment
- EffectiveDescriptor holon creation/update flow
- `CompiledFrom` link creation
- golden tests for known descriptor graphs
- cross-space descriptor fixture proving ExternalIds are compiled away

## Key Outcome

Descriptor edits produce EffectiveDescriptor holons and semantic versions.

## Dependencies

- PR 6
- PR 7

## Exit Criteria

- descriptor semantic changes produce new EffectiveDescriptor holons
- non-definitional changes do not produce new DefinitionHashes
- semantic version assignment is tied to effective semantic change
- compiled payload does not require cross-space dereference during validation

---

# 13. PR 9 — DescriptorsCache in ReferenceLayer

Estimate: 5 pts

## Goal

Add a semantic descriptor cache beside HolonsCache.

## Deliverables

- `DescriptorsCache`
- lookup by `DefinitionHash`
- lookup by `EntryHash(EffectiveDescriptor HolonNode)`
- route-to-definition equivalence mapping
- semantic version to DefinitionHash mapping where known
- cache insertion and eviction policy
- ReferenceLayer APIs for descriptor and EffectiveDescriptor lookup

## Key Outcome

Descriptors can be resolved by meaning, not route.

## Dependencies

- PR 6
- preferably PR 8

## Exit Criteria

- ReferenceLayer contains both HolonsCache and DescriptorsCache
- DescriptorsCache is path-insensitive
- Integrity/PVL has no dependency on DescriptorsCache

---

# 14. PR 10 — Space Type Activation Records

Estimate: 5 pts

## Goal

Distinguish descriptor identity from use authorization.

## Deliverables

- `TypeActivation` holon/type
- links from HolonSpace to activated EffectiveDescriptor
- activation status lifecycle:
  - Proposed
  - Active
  - Disabled
  - Deprecated
- lookup API:
  - `get_active_effective_descriptor(type_id, space_id)`
- activation governance placeholders

## Key Outcome

Space Manager can authorize EffectiveDescriptor holons for use.

## Dependencies

- PR 8

## Exit Criteria

- HolonSpace can activate an EffectiveDescriptor
- activation references `EntryHash(EffectiveDescriptor HolonNode)`
- activation does not create descriptor identity

---

# 15. PR 11 — HolonNode References Active EffectiveDescriptor

Estimate: 3 pts

## Goal

Prepare committed holons for peer validation.

## Deliverables

- add committed field such as:
  - `described_by`
  - `effective_descriptor_hash`
- update builders/importers to populate from active type activation
- verify the selected EffectiveDescriptor is active in the current HolonSpace before commit
- migration/default behavior for core holons
- clarify that normal `DescribedBy` SmartLinks remain part of the MAP graph

## Key Outcome

Every committed holon carries the content-addressed EffectiveDescriptor holon needed for validation.

## Dependencies

- PR 10

## Exit Criteria

- HolonNode contains direct descriptor binding for peer validation
- peer validation does not need to chase `DescribedBy` SmartLinks to discover its descriptor surface
- semantic graph still preserves `DescribedBy`

---

# 16. PR 12 — PVL Core Crate

Estimate: 5 pts

## Goal

Create the small deterministic validation kernel shared by coordinator and integrity.

## Deliverables

- `map_pvl_core`
- canonical decoding of EffectiveDescriptor payload
- supported PVL constraint types
- HolonNode envelope checks
- SmartLink envelope checks
- property presence checks
- value type checks
- enum checks
- key rule checks
- relationship typing checks where bounded
- no dependency on:
  - ReferenceLayer
  - Nursery
  - HolonsCache
  - DescriptorsCache
  - DanceService
  - query engine
  - TrustChannels

## Key Outcome

Shared deterministic validation logic exists for PVL-safe rules.

## Dependencies

- PR 6
- PR 0

## Exit Criteria

- PVL kernel can validate a HolonNode against a deserialized EffectiveDescriptor
- dependency graph confirms no coordinator/runtime imports

---

# 17. PR 13 — Integrity Zome PVL Integration

Estimate: 8 pts

## Goal

Use EffectiveDescriptor holons during peer validation.

## Deliverables

- read `effective_descriptor_hash` from HolonNode
- retrieve EffectiveDescriptor HolonNode with `must_get_valid_record`
- return unresolved dependency if missing
- decode EffectiveDescriptor HolonNode
- extract `effective_descriptor_bytes: CanonicalBytes`
- deserialize EffectiveDescriptor payload
- verify it applies to `HolonNode.described_by`
- run `map_pvl_core`
- tests for:
  - valid descriptor dependency
  - missing descriptor dependency
  - invalid descriptor binding
  - malformed HolonNode
  - malformed EffectiveDescriptor payload

## Key Outcome

Peers independently validate HolonNodes against content-addressed EffectiveDescriptor holons.

## Dependencies

- PR 11
- PR 12

## Exit Criteria

- Integrity validation uses Holochain deterministic dependency retrieval
- no live descriptor graph traversal occurs in integrity
- HolonNode validation is peer-reproducible

---

# 18. PR 14 — SmartLink PVL Validation

Estimate: 5 pts

## Goal

Bring relationships into peer validation.

## Deliverables

- SmartLink structural validation
- relationship lookup from bounded EffectiveDescriptor context
- source/target type conformance using keys and definition hashes
- bounded cardinality where reconstructible
- unresolved dependency handling
- tests for valid and invalid SmartLinks

## Key Outcome

SmartLinks are peer-validated without open descriptor traversal.

## Dependencies

- PR 13

## Exit Criteria

- SmartLinks pass through PVL validation
- link validation does not enforce global absence/exclusivity
- unresolved dependencies are handled correctly

---

# 19. PR 15 — Nursery Validation Uses EffectiveDescriptors

Estimate: 5 pts

## Goal

Align coordinator validation with descriptor semantics.

## Deliverables

- Nursery loads active EffectiveDescriptors
- Nursery deserializes EffectiveDescriptor payloads from CanonicalBytes
- transaction-local validation
- multi-holon consistency checks
- required / warning / deferred classification
- bounded snapshot checks
- optional dynamic rule execution above PVL where allowed
- tests for bounded pre-commit validation behavior

## Key Outcome

Richer validation uses the same descriptor surface as PVL.

## Dependencies

- PR 10
- PR 12
- PR 13

## Exit Criteria

- Nursery executes bounded descriptor-defined rules that do not belong in PVL
- higher-gravity validation no longer pressures PVL to expand unsafely

---

# 20. PR 16 — Transaction Manager Integration

Estimate: 5 pts

## Goal

Make validation part of the commit lifecycle.

## Deliverables

- transaction states:
  - Provisional
  - Validated
  - Failed
  - Committed
  - CommittedWithWarnings
- enforce required Nursery validation before commit
- attach ValidationResults where useful
- preserve warnings and deferred checks
- commit only HolonNodes with active EffectiveDescriptor bindings

## Key Outcome

Semantic commit boundaries are explicit.

## Dependencies

- PR 15

## Exit Criteria

- validation state transitions are part of commit flow
- invalid transactions fail before DHT write
- warnings/deferred outcomes can be preserved

---

# 21. PR 17 — Validation Outcomes and ValidationResult Receipts

Estimate: 3 pts

## Goal

Retain validation evidence for non-PVL and higher-layer validation outcomes.

## Deliverables

- `ValidationResult` / receipt model
- outcome categories:
  - Fail
  - Valid
  - Warning
  - Deferred
- optional digest binding to transaction or committed data
- descriptor identity binding
- validator identity and signature where useful
- linkage from Transaction to ValidationResults
- audit-friendly representation

## Key Outcome

Validation receipts remain available as evidence without replacing peer validation.

## Dependencies

- PR 15
- PR 16

## Exit Criteria

- Nursery and Transaction Manager can record validation outcomes
- receipts are not treated as primary PVL proof unless explicitly adopted by PVL-safe rules
- warnings and deferred checks have durable representation

---

# 22. PR 18 — Cross-Subsystem Semantic Convergence

Estimate: 8 pts

## Goal

Ensure validation semantics converge with query, command, dance, and DAHN consumers.

## Deliverables

- shared descriptor-owned value/operator semantics where validation overlaps with query filtering
- alignment with command preconditions
- alignment with dance preconditions
- deprecation plan for duplicated validation logic
- guidance for DAHN-facing validation display without frontend semantic ownership

## Key Outcome

Validation, query, commands, dances, and DAHN consume one descriptor-owned semantic surface where appropriate.

## Dependencies

- PR 15
- descriptor value semantics maturity
- query/command/dance structural readiness

## Exit Criteria

- permanent parallel rule systems are shrinking
- descriptor semantics are reused across subsystems
- DAHN does not invent its own validation semantics

---

# 23. PR 19 — RoleAccessDescriptor Model

Estimate: 5 pts

## Goal

Introduce agreement-derived compiled access surfaces.

## Deliverables

- `RoleAccessDescriptor`
- allowed properties
- allowed outbound relationships
- allowed target types
- traversal constraints
- source hashes:
  - EffectiveDescriptorHash
  - RoleHash
  - AgreementHash
- canonical serialization and content hash
- decide whether RoleAccessDescriptor also uses `CanonicalBytes` storage

## Key Outcome

Role-based access surfaces become explicit artifacts.

## Dependencies

- PR 6
- agreement model readiness

## Exit Criteria

- RoleAccessDescriptor can represent agreement-derived access surface
- RoleAccessDescriptor is distinct from EffectiveDescriptor and PVL

---

# 24. PR 20 — RoleAccessDescriptor Compilation

Estimate: 8 pts

## Goal

Compile access surfaces from agreements.

## Deliverables

- compiler:
  - EffectiveDescriptor + Role + InformationAccessAgreement → RoleAccessDescriptor
- cache by content hash
- invalidation/recompile on agreement change
- integration with TrustChannel access checks

## Key Outcome

Access control becomes compact, deterministic, and cacheable.

## Dependencies

- PR 19

## Exit Criteria

- RoleAccessDescriptors can be generated deterministically
- role access logic no longer requires repeated interpretation of full agreement plus descriptor graph

---

# 25. PR 21 — TrustChannel / ExternalId Resolution Integration

Estimate: 8 pts

## Goal

Connect route-sensitive access with role-based compiled surfaces.

## Deliverables

- ExternalId dereference through OutboundProxyId
- TrustChannel role resolution
- RoleAccessDescriptor lookup
- property filtering
- outbound relationship filtering
- projection/redaction behavior for returned holons

## Key Outcome

Foreign holons remain referenced, while access is mediated by compiled agreement surfaces.

## Dependencies

- PR 20

## Exit Criteria

- inter-space access obeys TrustChannel agreements
- stewarded state is not replicated
- RoleAccessDescriptor controls exposed surface

---

# 26. PR 22 — Import Pipeline Integration

Estimate: 8 pts

## Goal

Make JSON/import flows respect the new architecture.

## Deliverables

- descriptor import computes DefinitionHash
- descriptor import compiles EffectiveDescriptors
- EffectiveDescriptor HolonNode import/export support
- CanonicalBytes import/export support
- type activation import support
- holon import resolves active EffectiveDescriptor
- pre-commit validation before DHT write
- import-time errors for inactive or missing descriptor bindings

## Key Outcome

Imports no longer bypass descriptor activation or validation.

## Dependencies

- PR 16

## Exit Criteria

- import pipeline creates or resolves descriptor identity correctly
- imported holons carry active EffectiveDescriptor bindings
- imports participate in Nursery and PVL validation flow

---

# 27. PR 23 — Developer Diagnostics and Test Fixtures

Estimate: 5 pts

## Goal

Make the model observable and debuggable.

## Deliverables

- explain DefinitionHash inputs
- explain EffectiveDescriptor compilation
- explain CanonicalBytes payload decoding
- explain inheritance / relationship / space-reference compression
- explain semantic version changes
- explain type activation lookup
- explain PVL validation failure
- explain unresolved descriptor dependencies
- fixtures for:
  - core descriptors
  - domain descriptors
  - equivalent descriptors through different routes
  - cross-space descriptors compiled into local EffectiveDescriptor
  - missing EffectiveDescriptor dependency
  - invalid SmartLink
  - warning/deferred validation outcomes

## Key Outcome

Developers can understand why validation passed, failed, warned, deferred, or could not resolve dependencies.

## Dependencies

- PR 13 through PR 22

## Exit Criteria

- validation failures are explainable
- descriptor identity and activation decisions are inspectable
- regression fixtures cover major architectural invariants

---

# 28. PR 24 — Higher-Layer Validation Signaling and Evolution

Estimate: 5 pts

## Goal

Clarify and evolve the layers above Nursery where validation becomes social, inter-agent, or attestation-oriented.

## Deliverables

- posture for TrustChannel validation
- posture for attestation recording
- deferred validation signaling
- conflict signaling through:
  - ConflictsWith links
  - conflict holons
  - ValidationResults
  - attestations
- explicit boundary preservation so higher-layer validation does not leak into PVL or Nursery

## Key Outcome

Open-world and social validation outcomes have an architectural home.

## Dependencies

- PR 17
- PR 21
- PR 23

## Exit Criteria

- deferred and social validation outcomes are represented coherently
- lower-layer validation remains stable while higher layers evolve
- conflict detection and resolution are not confused with DHT admissibility

---

# 29. Cross-Phase Dependency Summary

## Critical Path

1. Rule classification
2. Identifier types
3. Canonical definitional surface
4. DefinitionHash
5. CanonicalBytes
6. EffectiveDescriptor payload model
7. EffectiveDescriptor holon model
8. EffectiveDescriptor compilation
9. Type activation
10. HolonNode effective descriptor binding
11. PVL core
12. Integrity PVL integration
13. Nursery validation
14. Transaction integration
15. Validation outcomes
16. Import and diagnostics

## Trust Mediation Path

1. EffectiveDescriptor payload model
2. RoleAccessDescriptor model
3. RoleAccessDescriptor compilation
4. TrustChannel / ExternalId resolution integration
5. Higher-layer validation signaling

## Semantic Convergence Path

1. Rule classification
2. EffectiveDescriptor payload model
3. Nursery validation
4. descriptor value/operator semantics
5. query / command / dance alignment
6. DAHN-facing diagnostics

---

# 30. Parallel Work Guidance

## Safe Earlier Work

- rule classification
- issue definition for intrinsic PVL, EffectiveDescriptor-backed PVL, Nursery-safe, and deferred rule families
- identifier type cleanup
- existing validation logic audit
- validation outcome vocabulary

## Safe Once Descriptor Structural Surface Exists

- DefinitionHash computation
- CanonicalBytes ValueType
- EffectiveDescriptor payload model
- EffectiveDescriptor holon model
- DescriptorsCache
- type activation

## Safe Once EffectiveDescriptors Exist

- HolonNode descriptor binding
- PVL core validation against deserialized EffectiveDescriptor
- Integrity Zome `must_get_valid_record` integration
- SmartLink PVL validation
- Nursery structural validation

## Safe Once Transaction Flow Is Stable

- Transaction Manager validation lifecycle
- ValidationResult receipt model
- warnings/deferred outcomes
- import pipeline integration

## Safe Once Agreement Model Is Ready

- RoleAccessDescriptor model
- RoleAccessDescriptor compilation
- TrustChannel access mediation

## Safe Once Query / Dance Structural Work Matures

- cross-subsystem semantic convergence
- query/filter semantic reuse
- command/dance precondition alignment
- DAHN-facing validation presentation

---

# 31. Recommended Initial Issue Sequence

A likely initial issue sequence is:

1. PR 0 — classify descriptor-defined rule families by enforcement layer
2. PR 1 — formalize identifier types
3. PR 2 — define canonical definitional surface
4. PR 3 — compute DefinitionHash
5. PR 4 — audit existing validation logic
6. PR 5 — add CanonicalBytes ValueType
7. PR 6 — define EffectiveDescriptor payload model
8. PR 7 — define EffectiveDescriptor holon model and relationships
9. PR 8 — implement EffectiveDescriptor compilation
10. PR 9 — add DescriptorsCache
11. PR 10 — define TypeActivation records
12. PR 11 — add HolonNode EffectiveDescriptor binding
13. PR 12 — create PVL core crate
14. PR 13 — integrate PVL into Integrity Zome

---

# 32. Immediate Next Step

The immediate next step should be to define the first structural issue:

- dependency-gravity-based rule classification
- intrinsic PVL vs EffectiveDescriptor-backed PVL vs Nursery-only vs deferred rule-placement framework
- explicit rule families to classify
- explicit exclusions from PVL
- relationship between EffectiveDescriptor-backed validation and non-PVL ValidationResults

This issue is the natural entry point because it prevents later implementation work from accidentally pulling descriptor graph traversal, ReferenceLayer access, dynamic validation rule dispatch, or agreement interpretation into integrity validation.