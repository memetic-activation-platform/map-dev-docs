# Effective Descriptor Implementation Plan — v2.0
## Descriptor Runtime Platform Delivery Sequence

# 1. Purpose

This plan defines the implementation sequence for the MAP Descriptor Runtime Platform.

The goal is to transform authored Descriptor Graphs into compact, deterministic, content-addressed `EffectiveDescriptor` artifacts that runtime subsystems can consume without repeatedly traversing inheritance hierarchies, resolving descriptor relationships, or dereferencing cross-space descriptor references.

`EffectiveDescriptor` is not primarily a validation artifact. It is the shared compiled runtime semantic surface consumed by:

- DAHN
- Query Engine
- Import Pipeline
- Validation / PVL
- Nursery
- Dance runtime
- `RoleAccessDescriptor` compilation
- ReferenceLayer descriptor lookup
- diagnostics and developer tooling

The Descriptor Graph remains the authored semantic source.

The `EffectiveDescriptor` is its compiled runtime representation.

---

# 2. Delivery Principles

- The Descriptor Graph is optimized for authoring, evolution, inheritance, composition, and semantic navigation.
- `EffectiveDescriptor` is optimized for deterministic runtime interpretation, caching, transport, and validation.
- Runtime systems should consume `EffectiveDescriptor`s rather than repeatedly traversing authored Descriptor Graphs.
- `EffectiveDescriptor` compilation performs three compressions:
  - inheritance compression
  - definitional relationship compression
  - space/reference compression
- `TypeName` identifies the continuing logical type lineage.
- `DescriptorRevisionId` identifies one authored `TypeDescriptor` revision before save.
- `SemanticVersion` classifies an accepted or published revision after ordering, merge, or governance approval.
- Semantic version is publication metadata, not compiled runtime semantic content.
- `EffectiveDescriptorDigest` identifies the canonical DAG-CBOR payload independently of storage substrate.
- `EffectiveDescriptorHash` identifies the locally stored Holochain carrier entry.
- `ExternalId` and `OutboundProxyId` remain route-sensitive identifiers and must not be used as descriptor-content identity.
- EffectiveDescriptors are represented as conventional MAP holons rather than a new Holochain `EntryType`.
- The compiled payload is stored using a `DagCbor` ValueType.
- The payload digest is stored using a `Blake3Digest` ValueType.
- The outer EffectiveDescriptor carrier must remain minimal and deterministic.
- `CompiledFrom` provides source provenance and navigation.
- `CompiledInto` is non-definitional for the source `HolonType`.
- Type activation authorizes an exact EffectiveDescriptor artifact for use in an AgentSpace.
- Activation does not create descriptor identity.
- Activation is revocable and therefore is enforced through runtime recognition and filtering, not immutable peer validation.
- `DescriptorsCache` improves runtime performance but does not establish semantic authority.
- Cross-space persistence of EffectiveDescriptor artifacts is an allowed exception to the one-home-space rule because the artifacts are deterministic, derived, non-authoritative runtime surfaces.
- Validation, TrustChannel policy, and social attestation remain separate downstream concerns.

---

# 3. Identity Model

The Descriptor Runtime Platform uses distinct identity regimes.

## 3.1 `TypeName`

`TypeName` is the key of a `TypeDescriptor` and identifies the continuing logical type.

Examples:

    Person
    Book
    Organization

`TypeName` remains stable across compatible revisions.

It does not identify:

- a specific semantic version
- a specific compiled payload
- a specific Holochain entry
- a specific committed descriptor record

---

## 3.2 `DescriptorRevisionId`

`DescriptorRevisionId` identifies one authored `TypeDescriptor` revision before it is saved.

It is opaque, immutable, collision-resistant, and independent of semantic version, commit hash, wall-clock time, author identity, and compiled digest.

The authored graph can key a `TypeDescriptor` revision by:

    TypeName + DescriptorRevisionId

This allows concurrent draft, branch, rejected, or merge-input revisions to exist before any governance process assigns a semantic version.

`DescriptorRevisionId` does not participate in the canonical `EffectiveDescriptor` payload because multiple authored revisions may compile into the same runtime semantic artifact.

---

## 3.3 `SemanticVersion`

`SemanticVersion` identifies an accepted or published revision of a logical type.

Conceptually:

    TypeName: Person
    SemanticVersion: 2.1.0

`SemanticVersion` is represented as MAP data rather than as a scalar identifier.

It is attached to a saved `TypeDescriptor` revision through non-definitional `Version` / `VersionFor` relationships.

It does not participate in:

- `TypeDescriptor` definitional identity
- `EffectiveDescriptor` canonical payloads
- `EffectiveDescriptorDigest`
- PVL interpretation of compiled descriptor artifacts

Runtime consumers that need version metadata obtain it from publication, activation, or provenance context.

---

## 3.4 `EffectiveDescriptorDigest`

`EffectiveDescriptorDigest` identifies the exact canonical compiled payload.

It is calculated as:

    EffectiveDescriptorDigest =
      BLAKE3(canonical DAG-CBOR EffectiveDescriptor bytes)

The digest is calculated after:

- inheritance flattening
- definitional relationship embedding
- space/reference resolution

It is not a hash of the authored Descriptor Graph.

It is storage-substrate independent and may later support:

- TrustChannel exchange
- non-Holochain AgentSpaces
- portable artifact comparison
- cache integrity verification
- exact payload equivalence

---

## 3.5 `EffectiveDescriptorHash`

`EffectiveDescriptorHash` identifies the EffectiveDescriptor carrier stored in a Holochain DHT.

It is:

    EffectiveDescriptorHash =
      Holochain EntryHash(canonical EffectiveDescriptor carrier HolonNode)

It is used for:

- `must_get_entry`
- local EffectiveDescriptor retrieval
- Holochain-local TypeActivation bindings
- PVL dependency resolution
- local cache lookup
- ordinary holons binding to the compiled descriptor used for validation

It is distinct from `EffectiveDescriptorDigest`.

---

## 3.6 `ActionHash` / `LocalId`

`ActionHash` identifies a particular committed record or record version.

It remains appropriate for:

- SmartLink source and target endpoints
- precise provenance
- exact committed-version references
- `CompiledFrom` / `CompiledInto` navigation

It does not identify the canonical EffectiveDescriptor payload.

---

## 3.7 `ExternalId`

`ExternalId` identifies a route to a stewarded foreign object.

The intended form is:

    ExternalId =
      OutboundProxyId
      + RemoteObjectId

`RemoteObjectId` is opaque and interpreted by the remote steward.

`ExternalId` is route-sensitive and must not be used as:

- EffectiveDescriptor equivalence identity
- payload identity
- stable logical type identity

---

# 4. Milestone Overview

## Milestone 1 — Identifier, Revision, and Version Foundations

Outcome:

- route-sensitive and content-addressed identities are explicitly separated
- `TypeName` is documented as the stable logical type identity
- `DescriptorRevisionId` is available before save for authored type revision identity
- EffectiveDescriptor digest and storage identities have distinct types
- semantic versioning is represented as non-definitional MAP publication metadata
- relationship definitional classification is explicit

Primary PRs:

- PR 1 — Identifier, Revision, and Semantic-Version Schema — 5 pts
- PR 2 — Definitional Relationship Classification and Compilation Boundary — 5 pts

---

## Milestone 2 — Canonical Payload Representation

Outcome:

- DAG-CBOR can be stored as a MAP property value
- BLAKE3 digests can be stored and validated
- the EffectiveDescriptor payload model is defined
- canonical serialization and digest computation are deterministic

Primary PRs:

- PR 3 — DAG-CBOR and BLAKE3 ValueTypes — 5 pts
- PR 4 — EffectiveDescriptor Payload Model — 5 pts
- PR 5 — Canonical DAG-CBOR Serialization and Digest Computation — 5 pts

---

## Milestone 3 — EffectiveDescriptor Carrier and Compilation

Outcome:

- EffectiveDescriptors are conventional MAP holons
- descriptor edits can produce compiled runtime artifacts
- source provenance is retained
- cross-space references are compiled away

Primary PRs:

- PR 6 — EffectiveDescriptor Holon Model and Relationships — 5 pts
- PR 7 — EffectiveDescriptor Compilation Pipeline — 8 pts

---

## Milestone 4 — Cache, Provisioning, and Activation

Outcome:

- EffectiveDescriptors can be cached by digest and local entry hash
- foreign EffectiveDescriptors can be provisioned locally
- AgentSpaces can activate exact descriptor artifacts
- activation state is available consistently to runtime consumers

Primary PRs:

- PR 8 — DescriptorsCache in ReferenceLayer — 5 pts
- PR 9 — Cross-Space EffectiveDescriptor Provisioning — 5 pts
- PR 10 — TypeActivation Schema and Lifecycle — 5 pts
- PR 11 — Activated Descriptor Set and Recognition Filtering — 8 pts

---

## Milestone 5 — Runtime Descriptor Consumption

Outcome:

- stable runtime APIs expose activated EffectiveDescriptors
- DAHN consumes compiled descriptor surfaces
- diagnostics explain descriptor compilation, activation, and identity

Primary PRs:

- PR 12 — Runtime Descriptor Surface APIs — 5 pts
- PR 13 — DAHN Consumption of EffectiveDescriptors — 5 pts
- PR 14 — EffectiveDescriptor Diagnostics and Fixtures — 5 pts

---

# 5. PR 1 — Identifier, Revision, and Semantic-Version Schema

Estimate: 5 pts

## Goal

Establish the identifier vocabulary, authored revision identity, and semantic-version schema needed by later EffectiveDescriptor work.

## Deliverables

### Identifier vocabulary

Add or formalize:

- `DescriptorRevisionId`
- `EffectiveDescriptorDigest`
- `EffectiveDescriptorHash`
- `RemoteObjectId`
- `CommittedHolonId`, if a distinct role type provides meaningful value
- `TypeName` documentation and type guarantees
- `LocalId` compatibility-role documentation
- `ExternalId = OutboundProxyId + RemoteObjectId`

Clarify:

- `TypeName` identifies the continuing logical type
- `DescriptorRevisionId` identifies one authored type revision before save
- `TypeName + DescriptorRevisionId` keys authored `TypeDescriptor` revisions
- `SemanticVersion` classifies accepted or published revisions and is not basic revision identity
- `EffectiveDescriptorDigest` identifies canonical DAG-CBOR payload content
- `EffectiveDescriptorHash` identifies the local Holochain carrier entry
- `ActionHash` identifies a committed record/version
- `ExternalId` identifies a route to a stewarded object

### DescriptorRevisionId schema

Add:

- `DescriptorRevisionId` ValueType
- `DescriptorRevisionId` PropertyType on `TypeDescriptor`

Required semantics:

    TypeDescriptor.DescriptorRevisionId
      ValueType: DescriptorRevisionId
      Cardinality: 1..1
      Required: true
      Definitional: true

Constraints:

- `DescriptorRevisionId` is generated before save
- `DescriptorRevisionId` is opaque and collision-resistant
- `DescriptorRevisionId` is immutable after save
- `DescriptorRevisionId` is not derived from semantic version, `ActionHash`, wall-clock time, author identity, or `EffectiveDescriptorDigest`
- `TypeName + DescriptorRevisionId` uniquely identifies an authored `TypeDescriptor` revision within the logical type lineage

### SemanticVersion core schema

Add:

- `SemanticVersion` HolonType
- `Major` PropertyType
- `Minor` PropertyType
- `Patch` PropertyType
- `Version` RelationshipType
- `VersionFor` RelationshipType

Required relationship semantics:

    TypeDescriptor --Version--> SemanticVersion

    SemanticVersion --VersionFor--> TypeDescriptor

Constraints:

- `Version` cardinality: `0..1`
- `VersionFor` cardinality: `1..1`
- `Version` is non-definitional
- `Version` uses `deletion_semantic Cascade`
- one `SemanticVersion` cannot be shared by multiple `TypeDescriptor`s
- draft, branch, rejected, unresolved, and merge-input `TypeDescriptor` revisions may have no semantic version

Remove:

- legacy `DanceImplementation.Version` property

### Rust facade

Add a holon-backed `SemanticVersion` facade in `holons_core`.

The facade should provide typed access to:

- `Major`
- `Minor`
- `Patch`
- `VersionFor`

## Dependencies

None.

## Exit Criteria

- the identifier regimes are distinct in code
- no `SemanticTypeId` is introduced
- `TypeName` is explicitly documented as the continuing logical type identity
- `DescriptorRevisionId` exists and is usable before a `TypeDescriptor` revision is saved
- `ExternalId` uses `RemoteObjectId`
- `EffectiveDescriptorDigest` and `EffectiveDescriptorHash` cannot be interchanged
- `SemanticVersion` is non-definitional publication metadata, not a compiled payload field
- `Version` cardinality permits unversioned draft, branch, rejected, unresolved, and merge-input revisions
- semantic-version schema exists in both AirTable and the TDL source
- semantic-version schema tests pass
- canonical encoding changes caused by `ExternalId` migration are versioned and tested

---

# 6. PR 2 — Definitional Relationship Classification and Compilation Boundary

Estimate: 5 pts

## Goal

Define which authored descriptor relationships contribute to the compiled EffectiveDescriptor and how directional definitional classification works.

## Deliverables

Add or formalize relationship classifications:

- `Definitional`
- `Operational`
- `Contextual`
- `Provenance`
- `Routing`

Support directional classification so an inverse relationship is not assumed to share the same definitional status.

Examples:

- `CompiledFrom` may be definitional or provenance-relevant from the EffectiveDescriptor side
- `CompiledInto` is non-definitional from the `HolonType` side
- routing and TrustChannel relationships do not participate in the compiled semantic surface
- authoring provenance does not participate in runtime semantic equivalence

Define compilation-boundary rules for:

- inherited properties
- inherited relationships
- value constraints
- key rules
- inverse relationships
- type conformance
- dances and affordances
- operational metadata
- routing/provenance metadata

Define the source inputs for each of the three compressions:

### Inheritance compression

- flatten `Extends`
- resolve inherited properties
- resolve inherited relationships
- resolve inherited constraints
- resolve inherited affordances where included

### Relationship compression

- embed definitional property and relationship specifications
- replace live descriptor links with compiled specifications
- compute effective inverse relationship surfaces

### Space/reference compression

- dereference foreign descriptor dependencies
- remove `ExternalId`, proxy, TrustChannel, and routing identities from the runtime payload
- retain only runtime semantic identities such as `TypeName` and compiled specifications

## Dependencies

PR 1.

## Exit Criteria

- directional relationship classification is explicit
- routing and provenance changes do not change the compiled runtime surface
- the three compression boundaries are documented and testable
- later compilation work has an explicit inclusion/exclusion contract

---

# 7. PR 3 — DAG-CBOR and BLAKE3 ValueTypes

Estimate: 5 pts

## Goal

Add the reusable MAP value primitives required to store canonical EffectiveDescriptor payloads and their digests.

## Core Schema Deliverables

### `DagCbor` ValueType

Add:

    ValueType: DagCbor
    Base representation: Bytes

The ValueType represents a canonical DAG-CBOR payload.

Validation requirements should include:

- valid DAG-CBOR decoding
- canonical encoding
- no unsupported CBOR tags
- deterministic map-key ordering
- bounded nesting depth
- bounded payload size
- explicit numeric restrictions
- no ambiguous alternate representations

### `Blake3Digest` ValueType

Add:

    ValueType: Blake3Digest
    Base representation: Bytes
    Length: exactly 32 bytes

The ValueType stores a BLAKE3-256 digest.

## Runtime Deliverables

- property-value encoding and decoding
- serde support
- byte access
- validation errors
- fixed-length digest checks
- DAG-CBOR canonicality checks
- size and nesting limits
- round-trip tests
- malformed-value tests

## Dependencies

PR 1.

## Exit Criteria

- `DagCbor` can be used as a MAP property value
- `Blake3Digest` can be used as a MAP property value
- DAG-CBOR values are validated as canonical
- BLAKE3 digest values must be exactly 32 bytes
- all value-type tests pass

---

# 8. PR 4 — EffectiveDescriptor Payload Model

Estimate: 5 pts

## Goal

Define the deserialized EffectiveDescriptor runtime semantic surface.

## Deliverables

Define structures such as:

- `EffectiveDescriptor`
- `EffectivePropertySpec`
- `EffectiveRelationshipSpec`
- `EffectiveInverseRelationshipSpec`
- `EffectiveKeyRuleSpec`
- `EffectiveDanceSpec` or an explicit deferral of `EffectiveDanceSet`
- PVL-safe structural rule surface
- Nursery-only semantic rule surface
- value constraint structures
- type-conformance structures

Define the relationship between the payload and the canonical carrier:

- the payload is the canonical DAG-CBOR value stored in `EffectiveDescriptorDagCbor`
- the carrier stores the payload digest in `EffectiveDescriptorDigest`
- the digest is BLAKE3 over the exact canonical DAG-CBOR payload
- carrier properties, provenance links, activation links, and local storage IDs are outside the payload

The payload should include at minimum:

- `type_name`
- EffectiveDescriptor format version
- canonical encoding identifier
- transitive `conforms_to` closure
- effective properties
- effective relationships
- effective inverse relationships
- effective key rule
- effective value constraints
- PVL-safe rule surface
- Nursery-only constraints
- any required dependency declarations

The payload must exclude:

- `DescriptorRevisionId`
- semantic version
- semantic-version ranges
- authored revision graph relationships
- publication metadata

### Type conformance

`conforms_to` should use:

- `TypeName`

Relationship target typing should normally use:

- target `TypeName`

Exact digest or hash pinning should be reserved for cases requiring exact artifact identity.

### Relationship-rule separation

The payload must distinguish:

#### PVL-safe relationship rules

Potentially:

- relationship key declaration
- source/target type requirements
- inverse compatibility
- attachment-policy metadata
- tag-shape requirements

#### Nursery-only relationship rules

- minimum cardinality
- maximum cardinality
- exclusivity
- global ordering
- transaction-level coherence

### Pattern constraints

Choose one:

- include only a deterministic, linear-time restricted pattern language
- classify general pattern checks as Nursery-only

## Dependencies

PR 2 and PR 3.

## Exit Criteria

- the payload contains all three compressed semantic surfaces
- no routing identifiers remain in the compiled payload
- semantic version and `DescriptorRevisionId` do not appear in the compiled payload
- carrier-local fields are excluded from the payload model
- `TypeName` is used instead of a separate semantic-type identifier
- subtype checks can be performed from `conforms_to`
- cardinality and global ordering are not incorrectly classified as PVL-safe
- EffectiveDanceSet inclusion or deferral is explicit

---

# 9. PR 5 — Canonical DAG-CBOR Serialization and Digest Computation

Estimate: 5 pts

## Goal

Define and implement the deterministic serialization contract for EffectiveDescriptor payloads.

## Deliverables

- canonical carrier schema constraints relevant to serialization and digest verification
- canonical DAG-CBOR serialization
- canonical DAG-CBOR deserialization
- format/version contract
- deterministic map ordering
- explicit absent/null semantics
- deterministic enum representation
- deterministic integer representation
- string-normalization policy
- no floating-point ambiguity
- bounded collection sizes and nesting
- `EffectiveDescriptorDigest` computation:

      EffectiveDescriptorDigest =
        BLAKE3(canonical DAG-CBOR EffectiveDescriptor bytes)

- digest verification helper
- resource-limit enforcement during canonical decode
- golden byte fixtures
- cross-run determinism tests
- round-trip tests
- over-limit rejection tests
- mutation tests proving semantic changes alter the digest
- tests proving route/provenance changes do not alter the digest

## Dependencies

PR 3 and PR 4.

## Exit Criteria

- equivalent payload structures serialize to identical bytes
- canonical bytes produce stable BLAKE3 digests
- semantic changes produce different digests
- excluded route and provenance changes do not alter the payload or digest
- malformed or noncanonical DAG-CBOR is rejected
- over-limit payloads are rejected before interpretation can become expensive

---

# 10. PR 6 — EffectiveDescriptor Holon Model and Relationships

Estimate: 5 pts

## Goal

Represent EffectiveDescriptors as conventional MAP holons with a minimal deterministic carrier shape.

## Core Schema Deliverables

### `EffectiveDescriptor` HolonType

Add a concrete `EffectiveDescriptor` HolonType.

It should:

- permit no incidental properties
- contain exactly the required artifact properties
- be treated as immutable compiled data
- reject updates to an existing carrier
- remain distinct from the authored `HolonType`

### `EffectiveDescriptorDagCbor` PropertyType

Add:

    PropertyType: EffectiveDescriptorDagCbor
    ValueType: DagCbor
    Cardinality: 1..1
    Required: true
    Definitional: true

### `EffectiveDescriptorDigest` PropertyType

Add:

    PropertyType: EffectiveDescriptorDigest
    ValueType: Blake3Digest
    Cardinality: 1..1
    Required: true
    Definitional: true

The stored digest must equal:

    BLAKE3(EffectiveDescriptorDagCbor)

### `CompiledFrom` RelationshipType

Add:

    EffectiveDescriptor --CompiledFrom--> HolonType

Recommended cardinality:

- `EffectiveDescriptor` side: `1..1`
- `HolonType` target side: `0..*`

Purpose:

- exact committed source provenance
- navigation
- diagnostics
- recompilation analysis

The target is an ActionHash-identified committed `HolonType` version.

PVL must not depend on traversing this relationship.

### `CompiledInto` RelationshipType

Add:

    HolonType --CompiledInto--> EffectiveDescriptor

Characteristics:

- inverse of `CompiledFrom`
- source-side cardinality: `0..*`
- non-definitional for `HolonType`

### Carrier canonicality

The carrier must not contain:

- timestamps
- display labels
- notes
- route-specific IDs
- author-dependent values
- arbitrary additional properties
- mutable operational metadata

The carrier must enforce:

- exactly one `EffectiveDescriptorDagCbor`
- exactly one `EffectiveDescriptorDigest`
- no additional semantic or cosmetic properties
- no in-place payload updates
- source-independent payload generation
- reuse of an existing canonical carrier when the same payload is already present

### Loader and bootstrap ordering

Descriptor bootstrap fixtures and loaders must preserve this order:

1. commit EffectiveDescriptor artifacts
2. create provenance/navigation links
3. activate descriptors
4. commit ordinary holons that bind to activated descriptors

## Dependencies

PR 3, PR 4, and PR 5.

## Exit Criteria

- EffectiveDescriptor holons can be constructed using only the two required properties
- digest correspondence is validated
- `CompiledFrom` and `CompiledInto` are present with correct directionality
- `CompiledInto` does not alter the `HolonType` definitional surface
- the outer carrier is deterministic and minimal
- updates to existing carrier payloads are rejected
- bootstrap fixtures exercise the required ordering
- no new Holochain `EntryType` is introduced

---

# 11. PR 7 — EffectiveDescriptor Compilation Pipeline

Estimate: 8 pts

## Goal

Compile authored Descriptor Graphs into stored EffectiveDescriptor holons.

## Deliverables

- compilation service or descriptor-commit hook
- inheritance flattening
- definitional relationship compaction
- space/reference compression
- `conforms_to` closure computation
- effective inverse relationship computation
- key-rule compilation
- `effective_dances` generation
- declarative dance-contract generation
- inheritance flattening for dance affordances
- ambiguity detection for inherited or conflicting dances
- effective value-constraint compilation
- PVL-safe versus Nursery-only rule classification
- exclusion of semantic-version and authored-revision metadata from the canonical payload
- canonical DAG-CBOR generation
- `EffectiveDescriptorDigest` calculation
- EffectiveDescriptor holon creation
- `CompiledFrom` / `CompiledInto` creation
- local `EffectiveDescriptorHash` capture after commit
- idempotent compilation when the authored graph has not changed semantically
- no duplicate carrier creation when the identical canonical carrier already exists
- canonical carrier reuse across equivalent compilation inputs
- golden tests for known descriptor graphs
- cross-space fixtures proving `ExternalId`s are compiled away

## Revision and semantic-version behavior

The compiler should distinguish:

- effective semantic change
- non-definitional metadata change
- compiler/format change
- no-op recompilation

Semantic-version assignment is not a compiler responsibility.

The compiler should:

- accept authored `TypeDescriptor` revisions that may or may not have semantic versions
- compile only effective semantic content
- exclude `DescriptorRevisionId`, `SemanticVersion`, `Version`, and `VersionFor` from the canonical payload
- permit different authored revisions to compile into the same `EffectiveDescriptorDigest`
- permit an accepted revision to receive semantic version metadata after compilation without changing the digest
- leave version assignment and version-policy checks to governance, publication, activation, and diagnostics layers

## Dependencies

PR 6.

## Exit Criteria

- authored descriptor graphs compile into deterministic EffectiveDescriptor payloads
- descriptor edits that alter effective semantics produce new digests
- non-definitional edits do not alter the digest
- assigning or changing semantic version metadata does not alter the digest
- route and steward-access paths do not appear in the payload
- identical canonical carriers produce the same Holochain `EntryHash`
- repeated compilation can reuse the existing canonical artifact
- source provenance is available through `CompiledFrom`
- runtime consumers no longer need authored-graph traversal for compiled semantics

---

# 12. PR 8 — DescriptorsCache in ReferenceLayer

Estimate: 5 pts

## Goal

Add a descriptor-specific cache beside `HolonsCache`.

## Deliverables

Add `DescriptorsCache` with lookup support for:

- `EffectiveDescriptorDigest`
- `EffectiveDescriptorHash`
- `TypeName`
- `TypeName + DescriptorRevisionId`, for authored revision mappings where available
- semantic version, via publication or activation metadata
- route-sensitive references mapped to resolved runtime artifacts
- decoded EffectiveDescriptor payloads

Potential mappings:

    EffectiveDescriptorDigest
      -> decoded EffectiveDescriptor

    EffectiveDescriptorHash
      -> EffectiveDescriptor carrier and decoded payload

    TypeName
      -> one or more EffectiveDescriptorHash values

    TypeName + DescriptorRevisionId
      -> one or more EffectiveDescriptorHash values, where provenance is available

    TypeName + SemanticVersion
      -> one or more EffectiveDescriptorHash values, via publication or activation metadata only

    ExternalId
      -> published artifact address or local EffectiveDescriptorHash

Define:

- cache insertion
- cache eviction
- digest verification on insertion
- stale-entry handling
- duplicate-route convergence
- local provisioning integration
- clear separation from `HolonsCache`

## Key Principle

The cache is an optimization.

It must not become:

- a source of peer-validation authority
- a substitute for activation
- a substitute for content-address verification
- an Integrity Zome dependency

## Dependencies

PR 5 and PR 6; preferably PR 7.

## Exit Criteria

- the ReferenceLayer contains both `HolonsCache` and `DescriptorsCache`
- different routes resolving to the same digest converge on one decoded cache entry
- Holochain-local retrieval works by `EffectiveDescriptorHash`
- cache insertion verifies payload digest
- Integrity/PVL has no dependency on the cache

---

# 13. PR 9 — Cross-Space EffectiveDescriptor Provisioning

Estimate: 5 pts

## Goal

Enable a consuming AgentSpace to obtain and locally persist an EffectiveDescriptor stewarded elsewhere.

## Deliverables

Define and implement the provisioning flow:

    discover foreign HolonType
        ↓
    dereference through TrustChannel
        ↓
    obtain steward-published EffectiveDescriptor artifact
        ↓
    verify steward authenticity
        ↓
    verify EffectiveDescriptorDigest
        ↓
    validate supported DAG-CBOR and payload format
        ↓
    create canonical local EffectiveDescriptor carrier
        ↓
    commit carrier into local DHT
        ↓
    obtain local EffectiveDescriptorHash
        ↓
    make artifact eligible for activation

Support:

- Holochain-to-Holochain provisioning
- preservation of published digest
- local carrier creation
- route-to-local-artifact mapping
- repeated provisioning idempotence
- provenance retention where available

Do not require:

- recompilation by the consuming space
- reproduction of the steward’s authored Descriptor Graph
- identical storage identifiers across different substrates

## Dependencies

PR 7 and PR 8.

## Exit Criteria

- foreign EffectiveDescriptor artifacts can be verified and stored locally
- repeated provisioning of the same canonical artifact does not create divergent carriers
- published digest and local Holochain EntryHash remain distinct concepts
- the consuming space does not acquire stewardship of the authored HolonType
- provisioned artifacts are not automatically activated

---

# 14. PR 10 — TypeActivation Schema and Lifecycle

Estimate: 5 pts

## Goal

Model the revocable governance binding between an EffectiveDescriptor artifact and an AgentSpace’s recognized runtime ontology.

## Core Schema Deliverables

### `TypeActivation` HolonType

Add a core `TypeActivation` HolonType.

### `ActivationStatus` ValueType

Add enum values:

- `Proposed`
- `Active`
- `Deprecated`
- `Disabled`
- `Superseded`

### `ActivationStatus` PropertyType

Add:

    TypeActivation.ActivationStatus
      ValueType: ActivationStatus
      Cardinality: 1..1
      Required: true

### Activation relationships

Add relationships conceptually equivalent to:

    AgentSpace --ActivatesType--> TypeActivation

    TypeActivation --ActivatedBySpace--> AgentSpace

    TypeActivation --ActivatesDescriptor--> EffectiveDescriptor

    EffectiveDescriptor --ActivatedThrough--> TypeActivation

    TypeActivation --Supersedes--> TypeActivation

    TypeActivation --SupersededBy--> TypeActivation

TypeActivation should bind to the exact EffectiveDescriptor artifact rather than merely a `TypeName`.

`TypeName` should normally be derived from the EffectiveDescriptor payload unless duplication has a specific indexing or verification purpose.

Semantic version, when relevant, should be obtained from publication, activation, or provenance context. It is not part of the EffectiveDescriptor payload.

### Governance evidence

Define an extensible relationship boundary for activation authority, but do not prematurely fix one governance model.

A future relationship may resemble:

    TypeActivation --AuthorizedBy--> GovernanceDecision

The durable requirement is:

> Readers must be able to verify that activation was authorized by the governance authority recognized by the AgentSpace.

## Lifecycle Deliverables

Implement or model:

- proposal
- evaluation
- authorization
- activation
- deprecation
- disablement
- supersession

## Dependencies

PR 7 and PR 9.

## Exit Criteria

- an AgentSpace can activate an exact EffectiveDescriptor artifact
- activation does not create descriptor identity
- activation state is revocable
- activation history remains available
- multiple versions may coexist when policy permits
- governance evidence has an explicit architectural attachment point

---

# 15. PR 11 — Activated Descriptor Set and Recognition Filtering

Estimate: 8 pts

## Goal

Make activation recognition mandatory and consistent across ordinary runtime reads.

## Deliverables

Add an `ActivatedDescriptorSet` maintained by the ReferenceLayer or Space Manager.

The set should support lookup by:

- local `EffectiveDescriptorHash`
- `EffectiveDescriptorDigest`
- `TypeName`
- semantic version, where activation or publication metadata provides it
- activation status

Apply activation filtering at every normal read ingress:

- direct holon fetch
- collection resolution
- query results
- SmartLink traversal
- reverse relationship traversal
- DAHN navigation
- Dance operand resolution
- command target resolution
- import reference resolution

Recognition outcomes should distinguish:

- structurally invalid
- structurally valid but unrecognized
- recognized and valid
- recognized with warnings or deferred semantic concerns

Default behavior:

- exclude unrecognized holons from normal semantic results
- drop or flag edges to unrecognized holons
- provide explicit diagnostic/quarantine APIs that bypass filtering
- invalidate activation caches when activation records change

## Key Principle

PVL proves:

    holon conforms to the EffectiveDescriptor it names

Activation filtering proves:

    the AgentSpace currently recognizes that EffectiveDescriptor

Together they provide:

    recognized runtime validity within the AgentSpace

## Dependencies

PR 8 and PR 10.

## Exit Criteria

- activation filtering is centralized rather than consumer-specific
- all normal read paths apply the same recognition rule
- unrecognized data remains available through diagnostic APIs
- disabling an activation changes runtime recognition without retroactively changing DHT validity
- DAHN and Query Engine receive only recognized data by default

---

# 16. PR 12 — Runtime Descriptor Surface APIs

Estimate: 5 pts

## Goal

Expose EffectiveDescriptors and activation state through stable runtime-facing APIs.

## Deliverables

Add or formalize a provider such as:

    DescriptorSurfaceProvider

Potential APIs:

    get_effective_descriptor_by_hash(hash)

    get_effective_descriptor_by_digest(digest)

    get_type_surface(type_name)

    get_type_surface_for_revision(type_name, descriptor_revision_id)

    get_published_type_surface(type_name, semantic_version)

    get_active_type_surface(type_name, space_id)

    get_property_surface(type_name, property_key)

    get_relationship_surface(type_name, relationship_key)

    get_conformance_surface(type_name)

    list_active_types(space_id)

    get_unrecognized_descriptor_status(hash)

Support:

- cache-backed lookup
- activation-aware lookup
- diagnostic bypass
- local and provisioned artifacts
- DAHN-friendly DTOs or view models where appropriate
- missing-artifact and inactive-artifact errors
- deprecated and superseded status information

## Dependencies

PR 8, PR 10, and PR 11.

## Exit Criteria

- runtime consumers do not traverse authored Descriptor Graphs for compiled semantics
- activation-aware and diagnostic APIs are clearly separated
- DAHN, Query, Import, and Validation can consume the same runtime descriptor interfaces
- lookup behavior is deterministic and testable

---

# 17. PR 13 — DAHN Consumption of EffectiveDescriptors

Estimate: 5 pts

## Goal

Make DAHN consume activated EffectiveDescriptors as its runtime descriptor surface for the PoC.

## Deliverables

- DAHN adapter to `DescriptorSurfaceProvider`
- active-type discovery
- property rendering from EffectiveDescriptor
- relationship-affordance rendering
- inherited-versus-declared indicators where useful
- required/optional indicators
- conformance display
- semantic-version display from publication or activation metadata
- deprecated/superseded status display
- basic visualizer selection from the runtime surface
- hidden-by-default unrecognized data
- optional diagnostic/quarantine view
- PoC fixtures using compiled and activated descriptor surfaces

## Dependencies

PR 12.

## Exit Criteria

- DAHN renders and navigates using EffectiveDescriptors
- the PoC does not depend on direct authored Descriptor Graph traversal
- DAHN respects activation filtering
- DAHN remains independent of PVL implementation
- deprecated and unrecognized surfaces are handled explicitly

---

# 18. PR 14 — EffectiveDescriptor Diagnostics and Fixtures

Estimate: 5 pts

## Goal

Make EffectiveDescriptor identity, compilation, provisioning, activation, and consumption observable and testable.

## Deliverables

Diagnostics should explain:

- EffectiveDescriptorDigest inputs
- DAG-CBOR payload decoding
- BLAKE3 digest verification
- local EffectiveDescriptorHash
- inheritance compression
- relationship compression
- space/reference compression
- `conforms_to`
- authored revision and semantic-version metadata, where available outside the payload
- source `CompiledFrom` provenance
- cache resolution
- route-to-artifact convergence
- cross-space provisioning
- activation lookup
- recognition filtering
- missing artifact
- inactive artifact
- disabled or superseded activation
- malformed or noncanonical payload

Fixtures should cover:

- core descriptors
- domain descriptors
- equivalent routes resolving to one artifact
- cross-space descriptor provisioning
- different payloads under the same `TypeName`
- multiple authored revisions and semantic-version publications for the same `TypeName`
- subtype conformance
- invalid digest
- malformed DAG-CBOR
- missing local artifact
- proposed but inactive descriptor
- disabled descriptor
- superseded descriptor
- unrecognized holon
- DAHN consumption

## Dependencies

PR 7 through PR 13.

## Exit Criteria

- EffectiveDescriptor generation and identity are explainable
- activation and recognition decisions are inspectable
- regression fixtures cover the main runtime descriptor invariants
- DAHN and later validation debugging share the same diagnostic foundation

---

# 19. Core Schema Change Summary

## PR 1

### ValueTypes

- `DescriptorRevisionId`

### HolonTypes

- `SemanticVersion`

### PropertyTypes

- `DescriptorRevisionId`
- `Major`
- `Minor`
- `Patch`

### RelationshipTypes

- `Version`
- `VersionFor`

### Removals

- `DanceImplementation.Version`

---

## PR 3

### ValueTypes

- `DagCbor`
- `Blake3Digest`

---

## PR 6

### HolonTypes

- `EffectiveDescriptor`

### PropertyTypes

- `EffectiveDescriptorDagCbor`
- `EffectiveDescriptorDigest`

### RelationshipTypes

- `CompiledFrom`
- `CompiledInto`

---

## PR 10

### HolonTypes

- `TypeActivation`

### ValueTypes

- `ActivationStatus`

### PropertyTypes

- `ActivationStatus`

### RelationshipTypes

- `ActivatesType`
- `ActivatedBySpace`
- `ActivatesDescriptor`
- `ActivatedThrough`
- `Supersedes`
- `SupersededBy`

Governance-evidence relationships are deferred until the governance model is sufficiently concrete.

---

# 20. Native HolonNode Changes Owned Outside This Plan

The following are required by validation but are not ordinary core-schema additions and remain in the Validation Implementation Plan:

- native `HolonNode` artifact discriminant or equivalent bootstrap mechanism
- native `HolonNode.effective_descriptor_hash`
- EffectiveDescriptor bootstrap handling
- immutable EffectiveDescriptor binding across ordinary holon updates
- Integrity Zome retrieval using `must_get_entry`
- PVL interpretation of EffectiveDescriptor payloads

The Descriptor Runtime Platform provides the artifact.

The Validation track defines how Integrity consumes it.

---

# 21. Cross-Phase Dependency Summary

## Critical Path for DAHN PoC

1. Identifier, Revision, and Semantic-Version Schema
2. Definitional Relationship Classification
3. DAG-CBOR and BLAKE3 ValueTypes
4. EffectiveDescriptor Payload Model
5. Canonical Serialization and Digest Computation
6. EffectiveDescriptor Holon Model
7. EffectiveDescriptor Compilation
8. DescriptorsCache
9. TypeActivation
10. Activated Descriptor Set and Filtering
11. Runtime Descriptor APIs
12. DAHN Consumption

---

## Downstream Validation Dependency

Validation begins consuming this platform after:

- PR 3 — DAG-CBOR and BLAKE3 ValueTypes
- PR 4 — EffectiveDescriptor Payload Model
- PR 5 — Canonical Serialization and Digest Computation
- PR 6 — EffectiveDescriptor Holon Model
- PR 7 — EffectiveDescriptor Compilation

Activation-aware runtime validation additionally depends on:

- PR 10 — TypeActivation
- PR 11 — Activated Descriptor Set
- PR 12 — Runtime Descriptor Surface APIs

Validation-specific work remains:

- native HolonNode EffectiveDescriptor binding
- PVL core crate
- Integrity Zome integration
- SmartLink validation
- Nursery validation
- transaction lifecycle
- ValidationResults and receipts

---

## Downstream Trust and Access Dependency

TrustChannel and role-based access work depends on:

- EffectiveDescriptor payload model
- canonical digest
- cross-space provisioning
- DescriptorsCache
- TypeActivation
- agreement-model readiness

Future cross-substrate interoperability may add a protocol wrapper such as:

    ContentAddress {
        scheme
        hash_algorithm
        encoding
        version
        digest
    }

That wrapper is intentionally deferred until TrustChannel interoperability requires it.

---

# 22. Parallel Work Guidance

## Safe Early Work

- PR 1 identifier, revision, and semantic-version schema
- PR 2 relationship classification
- PR 3 DAG-CBOR and BLAKE3 ValueTypes
- initial payload design
- canonical serialization research
- test-fixture preparation

## Safe Once Payload Model Exists

- canonical serialization
- digest computation
- EffectiveDescriptor carrier schema
- compilation pipeline scaffolding
- cache interfaces
- diagnostics fixtures

## Safe Once Compilation Exists

- DescriptorsCache
- cross-space provisioning
- TypeActivation
- runtime descriptor APIs
- DAHN integration
- validation planning

## Safe Once Activation Exists

- recognition filtering
- active-type listing
- DAHN active ontology views
- import alignment
- query integration

## Safe Later Consumers

- PVL / Integrity validation
- Nursery validation
- Query Engine convergence
- Dance runtime convergence
- `RoleAccessDescriptor` compilation
- TrustChannel enforcement

---

# 23. Recommended Initial Issue Sequence

1. PR 1 — Identifier, Revision, and Semantic-Version Schema
2. PR 2 — Definitional Relationship Classification and Compilation Boundary
3. PR 3 — DAG-CBOR and BLAKE3 ValueTypes
4. PR 4 — EffectiveDescriptor Payload Model
5. PR 5 — Canonical DAG-CBOR Serialization and Digest Computation
6. PR 6 — EffectiveDescriptor Holon Model and Relationships
7. PR 7 — EffectiveDescriptor Compilation Pipeline
8. PR 8 — DescriptorsCache in ReferenceLayer
9. PR 9 — Cross-Space EffectiveDescriptor Provisioning
10. PR 10 — TypeActivation Schema and Lifecycle
11. PR 11 — Activated Descriptor Set and Recognition Filtering
12. PR 12 — Runtime Descriptor Surface APIs
13. PR 13 — DAHN Consumption of EffectiveDescriptors
14. PR 14 — EffectiveDescriptor Diagnostics and Fixtures

---

# 24. Immediate Next Step

The immediate next step is to finalize and implement PR 1:

- formalize `EffectiveDescriptorDigest`
- formalize `EffectiveDescriptorHash`
- add `DescriptorRevisionId`
- add `RemoteObjectId`
- reshape `ExternalId`
- document `TypeName` as the stable logical type identity
- clarify `LocalId` / ActionHash identity
- add the `SemanticVersion` core schema
- add the `SemanticVersion` Rust facade
- remove `DanceImplementation.Version`

PR 2 can proceed in parallel at the design level by finalizing:

- directional definitional relationship classification
- the exact inputs to the three compression stages
- the exclusion of routing, contextual, and provenance data from the compiled runtime surface
