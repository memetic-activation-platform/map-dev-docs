# Effective Descriptor Implementation Plan (v1.0)


## Change Log

This plan factors the EffectiveDescriptor foundation out of the Validation Implementation Plan.

Key changes:

- Treats `EffectiveDescriptor` as a Descriptor-track artifact, not a Validation-track artifact.
- Frames EffectiveDescriptors as the shared runtime semantic surface for DAHN, validation, query, import, dances, and access-control compilation.
- Moves `DefinitionHash`, `CanonicalBytes`, EffectiveDescriptor compilation, `DescriptorsCache`, and TypeActivation into the Descriptor Runtime Platform.
- Leaves PVL, Integrity validation, Nursery validation, validation receipts, and SmartLink validation to the Validation track.
- Adds DAHN consumption as an explicit downstream target.

---

# 1. Purpose

This plan defines the implementation sequence for the MAP Descriptor Runtime Platform.

The goal is to transform authored Descriptor Graphs into compact, deterministic, content-addressed `EffectiveDescriptor`s that runtime subsystems can consume efficiently.

Primary consumers include:

- DAHN
- Query Engine
- Import Pipeline
- Validation / PVL
- Nursery
- Dance runtime
- RoleAccessDescriptor compilation
- diagnostics and developer tooling

---

# 2. Delivery Principles

- The Descriptor Graph remains the authored semantic source.
- `EffectiveDescriptor` is the compiled runtime semantic surface.
- Descriptor edits create descriptor identity.
- Type activation authorizes descriptor use within a HolonSpace.
- Runtime systems should consume `EffectiveDescriptor`s rather than repeatedly traversing Descriptor Graphs.
- EffectiveDescriptors are stored as conventional `HolonNode`s.
- The compiled payload is stored as `CanonicalBytes`.
- `CompiledFrom` provides precise source provenance.
- `CompiledInto` is non-definitional for the source HolonType.
- `DescriptorsCache` improves runtime lookup but does not establish semantic authority.

---

# 3. Milestone Overview

## Milestone 1 — Descriptor Identity

Outcome:

- route-sensitive identity is separated from definitional identity
- definitional surfaces can be canonicalized
- descriptors can be compared by meaning, not by discovery path

Primary PRs:

- PR 1 — Formalize Identifier Types — 3 pts
- PR 2 — Canonical Definitional Surface — 5 pts
- PR 3 — DefinitionHash Computation — 3 pts

---

## Milestone 2 — EffectiveDescriptor Representation

Outcome:

- `CanonicalBytes` exists
- EffectiveDescriptor payload model exists
- EffectiveDescriptor holons can be stored and linked to source descriptors

Primary PRs:

- PR 4 — CanonicalBytes ValueType — 3 pts
- PR 5 — EffectiveDescriptor Payload Model — 5 pts
- PR 6 — EffectiveDescriptor Holon Model and Relationships — 3 pts

---

## Milestone 3 — EffectiveDescriptor Compilation and Cache

Outcome:

- descriptor edits compile EffectiveDescriptors
- semantic versions are assigned
- EffectiveDescriptors are cached and discoverable

Primary PRs:

- PR 7 — EffectiveDescriptor Compilation Pipeline — 8 pts
- PR 8 — DescriptorsCache in ReferenceLayer — 5 pts
- PR 9 — TypeActivation Records — 5 pts

---

## Milestone 4 — Runtime Descriptor Surface Consumption

Outcome:

- runtime APIs expose EffectiveDescriptors
- DAHN can consume EffectiveDescriptors for descriptor-aware rendering and navigation
- diagnostics can explain compiled surfaces

Primary PRs:

- PR 10 — Runtime Descriptor Surface APIs — 5 pts
- PR 11 — DAHN Consumption of EffectiveDescriptors — 5 pts
- PR 12 — EffectiveDescriptor Diagnostics and Fixtures — 5 pts

---

# 4. PR 1 — Formalize Identifier Types

Estimate: 3 pts

## Goal

Establish the identifier vocabulary needed for descriptor identity and runtime lookup.

## Deliverables

Add or formalize:

- `DefinitionHash`
- `SemanticVersion`
- `EffectiveDescriptorHash`
- `ExternalId`
- `OutboundProxyId`
- `RemoteObjectId`
- `LocalId`
- `ActionHash`-based committed holon identity
- `EntryHash`-based content identity

## Key Outcome

MAP code distinguishes route-sensitive references from path-insensitive definitional identity.

## Dependencies

None.

## Exit Criteria

- `ExternalId` is not used for descriptor equivalence.
- `DefinitionHash` exists as a distinct type.
- `ActionHash` and `EntryHash` roles are documented in code comments or docs.

---

# 5. PR 2 — Canonical Definitional Surface

Estimate: 5 pts

## Goal

Define what participates in descriptor definitional identity.

## Deliverables

- canonical serialization for definitional descriptor content
- relationship classification enum:
  - `Definitional`
  - `Operational`
  - `Contextual`
  - `Provenance`
  - `Routing`
- directional relationship classification support
- filtering rules for definitional surface extraction
- tests proving excluded metadata does not affect definitional identity

## Key Outcome

Descriptor definitional surfaces are deterministic and path-insensitive.

## Dependencies

PR 1.

## Exit Criteria

- definitional relationships can be distinguished from routing/provenance/contextual relationships
- inverse relationships are not assumed to share definitional classification
- canonical definitional surface is stable under route/provenance changes

---

# 6. PR 3 — DefinitionHash Computation

Estimate: 3 pts

## Goal

Compute DefinitionHash for descriptor-like holons.

## Deliverables

- `compute_definition_hash(descriptor)`
- optional `definition_hash` field for definitional holons where appropriate
- validation that stored hash matches canonical definitional surface, where applicable
- tests for equivalent descriptors discovered through different routes

## Key Outcome

Equivalent descriptors discovered through different TrustChannels or proxy paths share definitional identity.

## Dependencies

PR 2.

## Exit Criteria

- DefinitionHash can be computed deterministically
- route-insensitive descriptor equivalence works in tests

---

# 7. PR 4 — CanonicalBytes ValueType

Estimate: 3 pts

## Goal

Introduce a deterministic binary value type for storing compiled artifacts.

## Deliverables

- `CanonicalBytes` ValueType
- canonical byte wrapper / validation type
- serialization contract documentation
- support in property value encoding / decoding
- round-trip determinism tests

## Key Outcome

MAP can store byte-stable serialized runtime artifacts inside conventional `HolonNode`s.

## Dependencies

PR 1.

## Exit Criteria

- `CanonicalBytes` can be used as a property value.
- Encoded bytes are byte-for-byte stable.
- Storage does not depend on generic JSON ordering or formatting.

---

# 8. PR 5 — EffectiveDescriptor Payload Model

Estimate: 5 pts

## Goal

Define the deserialized EffectiveDescriptor struct that will be serialized into `CanonicalBytes`.

## Deliverables

- `EffectiveDescriptor`
- `EffectivePropertySpec`
- `EffectiveRelationshipSpec`
- `EffectiveInverseRelationshipSpec`
- `EffectiveKeyRuleSpec`
- `PvlSurface`
- `NonPvlSemantics`
- value constraint structs
- canonical serialization / deserialization implementation
- encoding version field such as `map.effective-descriptor.v1`
- deterministic serialization tests

## Key Outcome

EffectiveDescriptor exists as a canonical payload model independent of graph traversal.

## Dependencies

PR 3 and PR 4.

## Exit Criteria

- EffectiveDescriptor serializes to and deserializes from `CanonicalBytes`.
- Payload contains inheritance-compressed, relationship-compressed, and space/reference-compressed semantics.
- Payload uses keys and definition hashes rather than route-sensitive IDs.

---

# 9. PR 6 — EffectiveDescriptor Holon Model and Relationships

Estimate: 3 pts

## Goal

Represent EffectiveDescriptors as conventional MAP holons.

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

PR 2, PR 4, PR 5.

## Exit Criteria

- EffectiveDescriptor holons can be created.
- EffectiveDescriptor holons can be linked to source HolonType versions.
- `CompiledFrom` gives precise ActionHash-based provenance.
- `CompiledInto` does not affect HolonType definitional identity.

---

# 10. PR 7 — EffectiveDescriptor Compilation Pipeline

Estimate: 8 pts

## Goal

Compile descriptor edits into EffectiveDescriptor holons.

## Deliverables

- descriptor edit hook or compilation service
- inheritance flattening
- relationship compaction
- space/reference compression
- effective inverse relationship computation
- EffectiveDescriptor payload generation
- semantic version assignment
- EffectiveDescriptor holon creation flow
- `CompiledFrom` link creation
- golden tests for known descriptor graphs
- cross-space descriptor fixture proving ExternalIds are compiled away

## Key Outcome

Descriptor edits produce EffectiveDescriptor holons and semantic versions.

## Dependencies

PR 5 and PR 6.

## Exit Criteria

- descriptor semantic changes produce new EffectiveDescriptor holons
- non-definitional changes do not produce new DefinitionHashes
- semantic version assignment is tied to effective semantic change
- compiled payload does not require cross-space dereference during runtime consumption

---

# 11. PR 8 — DescriptorsCache in ReferenceLayer

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

Descriptors can be resolved by meaning rather than route.

## Dependencies

PR 5; preferably PR 7.

## Exit Criteria

- ReferenceLayer contains both `HolonsCache` and `DescriptorsCache`.
- `DescriptorsCache` is path-insensitive.
- Runtime consumers can retrieve EffectiveDescriptors without traversing the authored Descriptor Graph.

---

# 12. PR 9 — TypeActivation Records

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

A HolonSpace can authorize an EffectiveDescriptor for use.

## Dependencies

PR 7.

## Exit Criteria

- HolonSpace can activate an EffectiveDescriptor.
- activation references `EntryHash(EffectiveDescriptor HolonNode)`.
- activation does not create descriptor identity.

---

# 13. PR 10 — Runtime Descriptor Surface APIs

Estimate: 5 pts

## Goal

Expose EffectiveDescriptors through stable runtime-facing APIs.

## Deliverables

- `DescriptorSurfaceProvider`
- APIs such as:
  - `get_type_surface(type_ref)`
  - `get_active_type_surface(type_ref, space_id)`
  - `get_property_surface(type_ref, property_key)`
  - `get_relationship_surface(type_ref, relationship_key)`
- DAHN-friendly DTOs or view models where appropriate
- fallback behavior for missing activation or missing compiled surface
- tests for lookup through activation and cache paths

## Key Outcome

Runtime systems can consume EffectiveDescriptors without knowing whether the source was authored graph traversal, cache, activation, or import.

## Dependencies

PR 8 and PR 9.

## Exit Criteria

- DAHN, Query, Import, and Validation can all depend on the same runtime descriptor interface.
- Runtime consumers do not need to traverse the authored Descriptor Graph directly.

---

# 14. PR 11 — DAHN Consumption of EffectiveDescriptors

Estimate: 5 pts

## Goal

Make DAHN consume EffectiveDescriptors as its descriptor surface for the PoC.

## Deliverables

- DAHN adapter to `DescriptorSurfaceProvider`
- property list rendering from EffectiveDescriptor
- relationship affordance rendering from EffectiveDescriptor
- inherited vs declared indicators, if needed
- required/optional indicators
- basic visualizer selection from runtime surface
- DAHN PoC fixture using compiled descriptor surfaces

## Key Outcome

DAHN demonstrates runtime descriptor consumption without relying directly on authored Descriptor Graph traversal.

## Dependencies

PR 10.

## Exit Criteria

- DAHN can render and navigate using EffectiveDescriptors.
- PoC uses compiled descriptor surfaces.
- DAHN remains independent of PVL and validation implementation.

---

# 15. PR 12 — EffectiveDescriptor Diagnostics and Fixtures

Estimate: 5 pts

## Goal

Make EffectiveDescriptor behavior observable and testable.

## Deliverables

- explain DefinitionHash inputs
- explain EffectiveDescriptor compilation
- explain CanonicalBytes payload decoding
- explain inheritance compression
- explain relationship compression
- explain space/reference compression
- explain semantic version changes
- explain type activation lookup
- fixtures for:
  - core descriptors
  - domain descriptors
  - equivalent descriptors through different routes
  - cross-space descriptors compiled into local EffectiveDescriptor
  - missing EffectiveDescriptor
  - invalid payload

## Key Outcome

Developers can understand how runtime descriptor surfaces were produced and why they differ.

## Dependencies

PR 7 through PR 11.

## Exit Criteria

- EffectiveDescriptor generation is explainable.
- Regression fixtures cover major descriptor-runtime invariants.
- DAHN and later validation debugging have shared diagnostics.

---

# 16. Cross-Phase Dependency Summary

## Critical Path for DAHN PoC

1. Identifier Types
2. Canonical Definitional Surface
3. DefinitionHash
4. CanonicalBytes
5. EffectiveDescriptor Payload Model
6. EffectiveDescriptor Holon Model
7. EffectiveDescriptor Compilation
8. DescriptorsCache
9. TypeActivation
10. Runtime Descriptor Surface APIs
11. DAHN Consumption

## Downstream Validation Dependency

Validation begins consuming this platform after:

- EffectiveDescriptor Payload Model
- EffectiveDescriptor Holon Model
- TypeActivation
- Runtime Descriptor Surface APIs

Validation-specific follow-on work remains:

- PVL core crate
- Integrity Zome PVL integration
- SmartLink PVL validation
- Nursery validation
- Transaction validation lifecycle
- ValidationResults and receipts

## Downstream Trust / Access Dependency

Role-based access work begins after:

- EffectiveDescriptor Payload Model
- CanonicalBytes
- DescriptorsCache
- agreement model readiness

---

# 17. Parallel Work Guidance

## Safe Early Work

- identifier cleanup
- relationship classification
- canonical definitional surface
- DefinitionHash tests
- CanonicalBytes ValueType

## Safe Once EffectiveDescriptor Payload Exists

- EffectiveDescriptor holon model
- compilation pipeline
- DescriptorsCache
- diagnostics fixtures

## Safe Once TypeActivation Exists

- runtime descriptor APIs
- DAHN integration
- import alignment
- validation planning

## Safe Later Consumers

- PVL / Integrity validation
- Nursery validation
- Query Engine convergence
- Dance runtime convergence
- RoleAccessDescriptor compilation

---

# 18. Recommended Initial Issue Sequence

1. PR 1 — Formalize Identifier Types
2. PR 2 — Canonical Definitional Surface
3. PR 3 — DefinitionHash Computation
4. PR 4 — CanonicalBytes ValueType
5. PR 5 — EffectiveDescriptor Payload Model
6. PR 6 — EffectiveDescriptor Holon Model and Relationships
7. PR 7 — EffectiveDescriptor Compilation Pipeline
8. PR 8 — DescriptorsCache in ReferenceLayer
9. PR 9 — TypeActivation Records
10. PR 10 — Runtime Descriptor Surface APIs
11. PR 11 — DAHN Consumption of EffectiveDescriptors
12. PR 12 — EffectiveDescriptor Diagnostics and Fixtures

---

# 19. Immediate Next Step

The immediate next step is to define PR 1 and PR 2 issues together:

- formalize identifier types
- define canonical definitional surface
- establish directional relationship classification
- specify how route-sensitive references are excluded from definitional identity
- define initial tests for path-insensitive descriptor equivalence