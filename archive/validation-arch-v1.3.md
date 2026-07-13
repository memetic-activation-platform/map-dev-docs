# MAP Validation Architecture (v1.3)

## NOTE: UPDATE IN PROGRESS
> this document is in the process of significant revision

## 1. Purpose and Scope

This document defines MAP validation architecture after the EffectiveDescriptor and TypeActivation split.

It owns:

- validation-layer boundaries
- the peer-validation guarantee
- the PVL execution contract
- HolonNode and SmartLink validation classes
- Integrity, Nursery, runtime recognition, and higher-layer validation responsibilities
- end-to-end validation flows

It depends on:

- `docs/core/descriptors/effective-descriptor.md` for EffectiveDescriptor artifact identity, carrier shape, payload content, and digest rules
- `docs/core/agent-spaces/type-activation-spec.md` for activation records, governance evidence, activated sets, and runtime recognition
- `docs/core/validation/validation-impl-plan.md` for delivery sequence

It does not own:

- descriptor compilation
- EffectiveDescriptor payload schema
- TypeActivation governance model
- RoleAccessDescriptor design
- TrustChannel protocol design
- social attestation or dispute resolution processes

---

## 2. Core Guarantee Model

Validation has three distinct guarantees.

### 2.1 Descriptor-Relative Validity

Integrity/PVL proves:

    This DHT op is well formed and, for ordinary holons, the HolonNode conforms to the exact EffectiveDescriptor artifact it names.

This is descriptor-relative.

PVL does not prove:

- the descriptor is activated
- the descriptor is socially legitimate
- the descriptor was correctly compiled from the authored graph
- the descriptor is globally canonical
- the holon is visible to any role
- open-world semantics are true

### 2.2 Runtime Recognition

Activation filtering proves:

    This AgentSpace currently recognizes the EffectiveDescriptor artifact named by the holon.

Activation is temporal, revocable, and governance-mediated. It must not be part of immutable peer validation.

### 2.3 Transaction-Local Semantic Validity

Nursery validation proves:

    This staged transaction satisfies the descriptor-backed and application-level checks that are bounded by the transaction and local snapshot.

Nursery validation is valuable pre-commit validation. It is not peer consensus and cannot prove global truth.

### 2.4 Composed Runtime Validity

The normal runtime guarantee is:

    PVL descriptor-relative validity
    +
    mandatory read-time activation filtering
    =
    recognized runtime validity in this AgentSpace

Unrecognized but structurally valid DHT data is expected. Normal runtime views exclude it by default and expose it only through diagnostic or quarantine APIs.

---

## 3. Validation-Relevant Identity Vocabulary

The full identity model lives in `effective-descriptor.md`. Validation uses the following roles.

| Identity | Validation Role |
|---|---|
| `TypeName` | Logical type lineage inside decoded EffectiveDescriptor payloads |
| `DescriptorRevisionId` | Authored revision identity; not part of PVL payload interpretation |
| `EffectiveDescriptorDigest` | BLAKE3 digest of canonical DAG-CBOR EffectiveDescriptor payload |
| `EffectiveDescriptorHash` | Holochain `EntryHash` of the canonical EffectiveDescriptor carrier |
| `ActionHash` | Committed action or record identity, used for ordinary holon endpoints and provenance |
| `ExternalId` | Route-sensitive foreign reference; never descriptor-content identity |

Ordinary holons bind to validation semantics by `effective_descriptor_hash`.

Graph-level `DescribedBy` relationships may exist for navigation and introspection, but PVL must not chase them. PVL derives the holon's type claim from the decoded EffectiveDescriptor payload.

EffectiveDescriptor artifacts have no `effective_descriptor_hash` dependency. They are validated through the bootstrap path defined below.

Semantic version is publication metadata. It is not part of the EffectiveDescriptor payload and does not participate in PVL interpretation.

---

## 4. Validation Layers

| Layer | Context Available | Proves | Does Not Prove |
|---|---|---|---|
| Integrity / PVL | op, action, DNA constants, bounded content-addressed dependencies | DHT admissibility and descriptor-relative structural validity | activation, global truth, agreement semantics |
| Nursery | staged transaction plus local snapshot | transaction-local semantic validity | peer consensus, global absence, social legitimacy |
| Runtime activation filtering | verified activated set and runtime reads | current AgentSpace recognition | DHT admissibility or conformance |
| Trust / Agreement | agreement, role, TrustChannel context | access and projection validity | PVL validity |
| Attestation / Social | open-world social process | social resolution or evidence | deterministic peer validation |

Rules move outward when their dependencies become less bounded.

---

## 5. PVL Specification

### 5.1 Definition

PVL is the deterministic validation kernel embedded in the Integrity Zome.

PVL validates DHT admissibility. It is not a general MAP runtime.

### 5.2 Inputs

PVL may read only:

- the DHT op/action being validated
- fixed DNA constants and supported format versions
- bounded Holochain validation context
- bounded content-addressed dependencies obtained through deterministic retrieval
- decoded EffectiveDescriptor payloads when validating ordinary holons

PVL must not read:

- ReferenceLayer APIs
- HolonsCache or DescriptorsCache
- activation sets
- live Descriptor Graphs
- coordinator state
- Nursery state
- query services
- Dance dispatch
- dynamic modules
- TrustChannel or agreement interpretation
- wall-clock time

### 5.3 Outputs

PVL returns:

    Valid
    Invalid(reason)
    UnresolvedDependencies(dependencies)

Missing content-addressed dependencies are not semantic failure. They produce `UnresolvedDependencies`.

Unsupported formats, noncanonical encodings, malformed carriers, and unsupported PVL constructs are `Invalid`.

### 5.4 Determinism Rules

PVL must be:

- deterministic
- bounded
- independently reproducible by every validating peer
- free of network calls except deterministic Holochain dependency retrieval
- free of runtime service dependencies
- free of open-world graph traversal

Unknown required semantics must be rejected. PVL must never silently ignore an unknown opcode, rule form, or EffectiveDescriptor format version.

### 5.5 Dependency Rules

PVL may use bounded deterministic dependencies.

For `EffectiveDescriptorHash`, retrieval is:

    must_get_entry(effective_descriptor_hash)

`must_get_entry` does not prove the entry was valid. PVL re-verifies the EffectiveDescriptor carrier every time it uses the payload.

Action-hash retrieval should be used only when the dependency is actually an `ActionHash`, such as checking an update's original action or validating inverse-link provenance.

Each op type must define a maximum validation dependency count.

### 5.6 Resource Bounds

Each DNA or supported PVL format version must define numeric bounds for:

- HolonNode entry size
- property count
- property-key length
- scalar value size
- nested value depth and collection length
- EffectiveDescriptor payload size
- EffectiveDescriptor payload nesting depth
- EffectiveDescriptor property and relationship rule counts
- enum value count
- pattern length, if deterministic patterns are ever PVL-supported
- SmartLink tag size
- SmartLink decoded field count
- validation dependency count per op

Bounds constrain interpretation cost, not only byte size.

### 5.7 PVL Evolution

PVL is compiled into the DNA. New required PVL opcodes or incompatible canonical encoding changes require a DNA/version migration strategy.

Initial PVL should therefore be conservative. Existing spaces cannot safely receive new integrity semantics by coordinator upgrade alone.

---

## 6. HolonNode PVL

HolonNode PVL includes Classes A through D when all inputs are bounded and content-addressed.

### 6.1 Class A: Intrinsic Envelope Checks

Class A does not require an EffectiveDescriptor.

Checks include:

- entry is the expected `HolonNode` entry type
- entry encoding is canonical
- entry size is within fixed bounds
- property map has canonical ordering and no duplicate keys
- property count is within bounds
- property names are valid and bounded
- property values use valid MAP value encodings
- scalar, collection, and nested values are bounded
- present-null semantics are fixed and deterministic
- reserved/internal fields are absent from ordinary holons unless explicitly allowed
- author/action/signature checks available from Holochain context pass
- create, update, and delete action shapes are valid under fixed lifecycle rules
- update references existing original or prior action where required

### 6.2 Class B: EffectiveDescriptor Artifact Bootstrap Checks

Class B applies when the HolonNode is an EffectiveDescriptor artifact.

An EffectiveDescriptor artifact:

- is recognized by an explicit artifact discriminant or equivalent fixed bootstrap mechanism
- has no `effective_descriptor_hash` dependency
- contains exactly the canonical carrier properties required by `effective-descriptor.md`
- contains `EffectiveDescriptorDagCbor`
- contains `EffectiveDescriptorDigest`
- contains no semantic or cosmetic carrier properties outside the canonical carrier contract
- decodes canonical DAG-CBOR
- has `EffectiveDescriptorDigest == BLAKE3(EffectiveDescriptorDagCbor)`
- uses a supported EffectiveDescriptor format version
- respects EffectiveDescriptor resource bounds
- contains only supported PVL-safe constructs

An EffectiveDescriptor artifact is immutable compiled data. A changed payload creates a new artifact.

The artifact-discriminant mechanism is an implementation decision, but it must be fixed, deterministic, and safe against ordinary holons accidentally or maliciously resembling descriptor artifacts.

### 6.3 Class C: Ordinary Holon Descriptor Binding

Class C applies to ordinary HolonNodes.

Checks include:

- ordinary HolonNode has `effective_descriptor_hash`
- `effective_descriptor_hash` is an `EffectiveDescriptorHash`, meaning a Holochain `EntryHash` of a canonical EffectiveDescriptor carrier
- Integrity retrieves the carrier with `must_get_entry`
- missing carrier returns `UnresolvedDependencies`
- retrieved carrier passes Class B bootstrap checks
- decoded payload is well formed and supported
- type claim is derived from the decoded payload
- graph-level `DescribedBy` is not chased by PVL
- ordinary HolonNode update keeps the same `effective_descriptor_hash` as the original

Retyping means creating a new holon, not updating the descriptor binding of an existing holon.

### 6.4 Class D: EffectiveDescriptor-Backed Structural Checks

Class D uses the decoded EffectiveDescriptor payload.

PVL-safe checks include:

- required property presence
- property key declaration or descriptor-defined open-property policy
- value base type checks
- enum membership
- numeric min/max checks
- string and bytes length checks
- deterministic key-shape checks
- non-instantiable or abstract type rejection, if encoded in the payload
- local type-conformance checks using `conforms_to`, where all required data is in bounded payloads

Class D excludes:

- activation checks
- semantic version or publication status checks
- Descriptor Graph traversal
- `CompiledFrom` traversal
- global uniqueness
- relationship cardinality
- required outbound or inbound relationships
- cross-holon transaction coherence
- duplicate detection
- agreement, role, or access policy
- TrustChannel interpretation
- dynamic validation Dances
- social or attestation semantics

---

## 7. SmartLink PVL

SmartLink validation is split into classes because link ops have different dependency gravity than entry ops.

### 7.1 Class A: Intrinsic Link Envelope and Anti-Graffiti Checks

Class A is descriptor-independent and belongs in PVL.

Checks include:

- link type is a recognized MAP SmartLink link type
- base address has the expected committed HolonNode action/record shape
- target address has the expected committed HolonNode action/record shape
- endpoint retrievability is checked where the DNA requires endpoint existence
- self-link policy is fixed and deterministic
- link tag uses canonical encoding
- link tag size is within bounds
- relationship key shape is valid and bounded
- forward/inverse marker shape is valid, if used
- reserved/system relationship-key namespaces are protected by fixed rules
- link delete references an existing link action
- link delete author policy is fixed and deterministic
- dependency count remains within the SmartLink PVL bound

Authorship policy is part of Class A.

Possible baseline policy:

- forward links may be authored only by the base holon author, unless the DNA defines a fixed alternate authorization mechanism
- inverse links must carry forward-link provenance and be authored by the same author as the forward link, unless the DNA defines a fixed alternate authorization mechanism

For inverse-link provenance, PVL may retrieve the forward link by `ActionHash` and verify:

- forward link exists
- forward base equals inverse target
- forward target equals inverse base
- relationship key matches
- direction markers correspond
- author policy is satisfied

Open third-party annotation is possible, but it must be an explicit fixed policy. Without a fixed rule, third-party link authorship is graph graffiti.

### 7.2 Class B: Descriptor-Backed Relationship Typing

Class B is a design choice.

It may be included in PVL only if the launch DNA accepts the dependency cost.

Potential Class B checks:

- relationship key is declared in the source EffectiveDescriptor
- target holon's EffectiveDescriptor is retrievable through bounded dependencies
- target type conforms using the decoded target payload's `conforms_to`
- attachment policy is encoded in bounded descriptor payload data
- tag-shape requirements match descriptor payload data

If Class B is not included in launch PVL, relationship typing must be enforced by Nursery and read-time/runtime filtering. In that model, edges are peer-admissible claims, not peer-validated typed facts.

Adding Class B later requires DNA migration for existing spaces.

### 7.3 Class C: Non-PVL Relationship Semantics

Class C is not PVL unless a future transaction-manifest mechanism makes a specific case bounded and peer-reconstructible.

Class C includes:

- minimum cardinality
- maximum cardinality
- exclusivity
- global ordering
- required outbound relationships
- required inbound relationships
- transaction-wide relationship coherence
- absence of other links
- global uniqueness

These belong in Nursery, runtime filtering, diagnostics, or higher layers.

---

## 8. EffectiveDescriptor Retrieval and Bootstrap Flow

For ordinary HolonNode validation:

    validate ordinary HolonNode op
      read effective_descriptor_hash
      must_get_entry(effective_descriptor_hash)
      if missing:
        return UnresolvedDependencies
      validate EffectiveDescriptor carrier with Class B bootstrap checks
      verify EffectiveDescriptorDigest == BLAKE3(EffectiveDescriptorDagCbor)
      decode canonical DAG-CBOR payload
      run Class D structural checks
      accept or reject

For EffectiveDescriptor artifact validation:

    validate EffectiveDescriptor artifact op
      require no effective_descriptor_hash dependency
      validate fixed carrier shape
      verify digest
      decode payload
      validate payload format and resource bounds
      accept or reject

PVL never resolves a TrustChannel, ReferenceLayer route, DescriptorsCache entry, or authored Descriptor Graph while validating an op.

---

## 9. Activation and Runtime Recognition

Activation is outside Integrity/PVL.

Coordinator and Nursery flows should select active descriptors before commit, but a modified coordinator can bypass that selection. Therefore, normal runtime reads must apply activation filtering.

Write-side behavior:

- honest coordinator resolves active EffectiveDescriptor through runtime descriptor APIs
- Nursery validates against that descriptor
- committed ordinary HolonNode carries `effective_descriptor_hash`

Peer-validation behavior:

- PVL checks conformance to the named EffectiveDescriptor artifact
- PVL does not check activation

Read-side behavior:

- ReferenceLayer applies mandatory activation filtering for normal reads
- unrecognized holons and edges are excluded by default
- diagnostic APIs may bypass filtering explicitly

---

## 10. Nursery Validation

Nursery validation runs before commit in coordinator space.

Nursery owns checks that are bounded by a staged transaction and local snapshot but not peer-reconstructible at op granularity.

Nursery checks include:

- relationship cardinality after transaction application
- required outbound or inbound relationships
- transaction coherence across multiple holons and links
- duplicate detection against a local snapshot
- command preconditions
- dance preconditions
- dynamic or extensible validation rules where allowed
- activation-aware write-side descriptor selection

Outcomes:

    Fail
    Valid
    Warning
    Deferred

Nursery failure should abort the transaction in honest coordinators. Warnings and deferred outcomes may be recorded as ValidationResults.

---

## 11. ValidationResults and Receipts

ValidationResults and receipts are evidence.

They are not the primary basis of peer validation.

A ValidationResult may record:

- validated input digest
- validation scope
- descriptor artifact identity
- rule set or rule id
- validation engine identity and version
- validator identity
- outcome
- signature or attestation

Integrity may verify receipt format, digest binding, validator identity, or signatures only when the receipt acceptance rule is itself PVL-safe.

Receipt verification proves that an assertion was made. It does not prove semantic correctness unless the asserted semantics are also PVL-enforceable.

---

## 12. End-to-End Flows

### 12.1 EffectiveDescriptor Artifact Commit

    compile descriptor graph
      produce canonical DAG-CBOR payload
      compute EffectiveDescriptorDigest
      construct canonical carrier
      commit EffectiveDescriptor artifact
      Integrity runs bootstrap checks
      create provenance/navigation links later
      activate artifact later

### 12.2 Ordinary Holon Commit

    coordinator selects recognized EffectiveDescriptor
      Nursery validates transaction
      commit ordinary HolonNode with effective_descriptor_hash
      Integrity retrieves and verifies EffectiveDescriptor artifact
      PVL validates descriptor-relative structure
      runtime activation filtering recognizes or hides the holon

### 12.3 SmartLink Commit

    commit SmartLink
      PVL runs Class A envelope and anti-graffiti checks
      optional PVL Class B relationship typing, if adopted by DNA
      Nursery/runtime handles Class C relationship semantics

### 12.4 Import

    import data
      provision required EffectiveDescriptor artifacts locally
      verify digests and carrier shape
      ensure activation where required by coordinator flow
      Nursery validates staged import
      commit holons and links
      PVL validates descriptor-relative admissibility
      activation filtering controls normal visibility

---

## 13. Open Decisions

The architecture leaves these decisions explicit:

- EffectiveDescriptor artifact discriminant mechanism: explicit field vs fixed carrier-shape detection
- SmartLink Class B in launch PVL vs runtime/Nursery only
- exact numeric resource-bound constants
- PVL opcode and EffectiveDescriptor format migration strategy
- whether transaction manifests will ever make selected multi-op semantics PVL-checkable
- fixed authorship policy for open annotation use cases

---

## 14. Implementation Checklist

Implementation must provide:

- ordinary HolonNode `effective_descriptor_hash`
- EffectiveDescriptor artifact bootstrap path
- deterministic `must_get_entry` retrieval for `EffectiveDescriptorHash`
- carrier digest verification
- canonical DAG-CBOR payload decoding
- PVL resource-bound constants
- unknown-format and unknown-opcode rejection
- HolonNode Class A through D checks
- SmartLink Class A checks
- explicit decision for SmartLink Class B
- Nursery checks for relationship cardinality and transaction coherence
- mandatory runtime activation filtering
- diagnostics for invalid, unresolved, unrecognized, warning, and deferred outcomes

