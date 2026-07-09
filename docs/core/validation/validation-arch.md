# MAP Validation Architecture — v1.3

## Change Log from v1.2

v1.3 brings the validation architecture into alignment with the broader MAP Architecture Spec.

Key changes:

- Replaces the prior “validation receipt / proof-carrying” emphasis with the stronger peer-validation path based on content-addressed `EffectiveDescriptor` artifacts.
- Clarifies that descriptor edits, not type activation, trigger `EffectiveDescriptor` compilation, `DefinitionHash` computation, and semantic version assignment.
- Removes the need for a separate `ValidationDescriptor` concept unless later design work identifies a meaningful distinction. PVL evaluates the integrity-enforceable subset of the `EffectiveDescriptor`.
- Clarifies that MAP currently uses `ActionHash` as the primary `LocalId` for committed holons.
- Clarifies that `EntryHash(HolonNode)` is not sufficient for semantic equivalence, while `EntryHash(EffectiveDescriptor)` can serve as a definitional content identity for the compiled descriptor surface.
- Introduces type activation as the mechanism by which a HolonSpace authorizes an `EffectiveDescriptor` for use in that DHT.
- Defines `HolonNode.effective_descriptor_hash` as the content-addressed dependency used by peer validation.
- Clarifies use of Holochain `must_get_valid_record` to retrieve the required `EffectiveDescriptor` during integrity validation.
- Adds `DescriptorsCache` as a ReferenceLayer responsibility for lookup by `DefinitionHash`, distinct from route-sensitive `HolonsCache`.
- Repositions validation receipts as useful higher-layer evidence, not the primary mechanism for preserving Holochain-style peer validation.
- Strengthens the boundary between PVL and coordinator/runtime layers: PVL may interpret bounded `EffectiveDescriptor` data, but may not invoke descriptor graph traversal, caches, Dance dispatch, dynamic rule execution, or agreement interpretation.

---

## 1. Purpose

This document defines the MAP validation architecture after incorporating:

- the layered validation model from the original validation design
- the dependency gravity reframing
- PVL (Peer Validation Language)
- the Nursery / coordinator role
- transaction-vs-op validation distinctions
- descriptor-driven validation
- `DefinitionHash`
- `EffectiveDescriptor`
- type activation
- Holochain `must_get_valid_record`
- ReferenceLayer descriptor caching
- the MAP one-home-space principle
- the Holochain integrity zome immutability constraint

The key synthesis is:

> **Descriptors own validation semantics. Validation layers own evaluation authority.**

MAP should not treat validation rules as freestanding logic scattered across validators, queries, commands, dances, and coordinators. Instead, descriptors define the structural and semantic rules that apply to holons, properties, relationships, and values. The validation architecture determines which subset of those descriptor-defined rules may be evaluated in which layer.

Corollary:

> **Descriptor-owned does not mean integrity-resolved.**

The Holochain integrity zome is compiled into the DNA and effectively fixed for a DHT. It must stay small, stable, deterministic, and free of coordinator/runtime dependencies. Descriptor semantics may influence peer validation only when they have been reduced to a bounded, content-addressed `EffectiveDescriptor` that every validating peer can retrieve and interpret deterministically.

Integrity validation must not resolve the live descriptor graph through coordinator services.

---

## 2. Core Principles

### 2.1 Structural vs Semantic Validation

MAP distinguishes between broad kinds of validity:

| Type | Meaning | Typical Enforcement Layer |
|------|---------|----------------------------|
| Storage Envelope Validity | Safe, canonical, well-formed entry/link data | Integrity / PVL |
| Descriptor Structural Validity | Schema conformance under descriptor-defined structure | PVL when backed by an activated `EffectiveDescriptor`; otherwise Nursery |
| Transactional Semantic Validity | Correctness over a bounded transaction and local snapshot | Nursery / Validation Engine |
| Agreement / Trust Validity | Correctness under roles, trust channels, and agreements | Trust Channels / Agreements |
| Social Validity | Ambiguous, contested, or open-world meaning | Attestation / social resolution |

This distinction remains important, but descriptors refine it:

- descriptors define both structural and semantic rule surfaces
- `EffectiveDescriptor`s provide the flattened runtime descriptor surface
- PVL evaluates only the peer-reproducible subset
- Nursery evaluates bounded transaction/snapshot semantics
- higher layers evaluate agreement-, trust-, and interpretation-dependent semantics

---

### 2.2 Closed vs Open World

| Domain | World Model |
|--------|-------------|
| Integrity / PVL | Closed over the op, action, DNA, and content-addressed dependencies retrievable by hash |
| Nursery | Locally closed over a transaction plus local snapshot |
| Trust / Social | Open, evolving, agreement-mediated |

---

### 2.3 Validation is Layered

Validation is not a single mechanism. It is a layered architecture in which:

- descriptors provide the semantic rule definitions
- `EffectiveDescriptor`s provide canonical runtime descriptor surfaces
- each validation layer applies only the rules it can evaluate safely
- rules move outward when they exceed a layer's boundedness constraints
- peer validation remains deterministic, bounded, and independently reproducible

---

### 2.4 Rule Ownership vs Enforcement Location

Rule ownership and rule execution must not be conflated.

Examples:

- `ValueDescriptor` owns value-validation semantics and operator semantics
- `PropertyDescriptor` owns requiredness and value-type linkage
- `RelationshipDescriptor` owns relationship typing and bounded cardinality semantics
- `HolonDescriptor` owns inherited structural lookup and type-level affordance lookup

But ownership does not imply that every layer may execute every rule.

- Integrity may execute only storage-envelope rules and `EffectiveDescriptor` rules that are PVL-safe.
- Nursery may execute richer transaction- and snapshot-aware descriptor rules.
- Trust and agreement layers may execute role-, access-, and interpretation-dependent rules.
- Attestation layers may resolve ambiguity and contested meaning.

---

## 3. Identity and Descriptor Artifacts

### 3.1 Routable Identity

Foreign holons are accessed by reference, not replication.

For holons stewarded in another Home Space, access is mediated through:

    ExternalId = OutboundProxyId + RemoteObjectId

ExternalIds are:

- path-sensitive
- authority-sensitive
- route-dependent
- TrustChannel-mediated
- steward-mediated

ExternalIds are used for dereferencing stewarded holons.

They are not used for definitional equivalence.

---

### 3.2 Definitional Identity

Descriptors and other definition-like holons require path-insensitive identity.

    DefinitionHash = hash(canonical_definitional_surface)

A `DefinitionHash` is independent of:

- TrustChannel
- proxy route
- remote steward path
- local database identity
- incidental provenance
- `ExternalId`

It is used for:

- descriptor equivalence
- descriptor caching
- recognizing equivalent definitions discovered through different routes
- determining whether descriptor edits changed meaning

Only definitional content participates in a `DefinitionHash`.

Included:

- definitional properties
- definitional relationships
- constraints
- value type references
- declared property references
- declared relationship references
- structural semantics required to determine equivalence

Excluded:

- routing relationships
- TrustChannel relationships
- provenance relationships
- operational/cache metadata
- local IDs
- external IDs
- agreement-specific access paths

---

### 3.3 Storage Identity

MAP currently uses `ActionHash` as the primary local identifier for committed holons.

For example, `SmartLink` source and target references identify holons by their `ActionHash`.

`EntryHash` identifies the content of a stored entry.

For ordinary `HolonNode` entries, the `EntryHash` should not be treated as full semantic or definitional equivalence, because important meaning may be carried by associated `SmartLink`s rather than by the entry body itself.

Compiled descriptor artifacts such as `EffectiveDescriptor`s are intentionally different. An `EffectiveDescriptor` materializes the flattened definitional surface, including inherited and definitional relationship semantics, into a canonical entry representation. Therefore, the `EntryHash` of an `EffectiveDescriptor` may be used as a content-based identifier for definitional equivalence of that compiled surface.

In short:

- `ActionHash` identifies a committed holon record/version.
- `EntryHash` identifies entry content.
- `EntryHash(HolonNode)` is not generally sufficient for semantic equivalence.
- `EntryHash(EffectiveDescriptor)` may be sufficient for definitional equivalence if the `EffectiveDescriptor` entry contains the canonical flattened definitional surface.
- `DefinitionHash` remains useful as a path-insensitive hash of an authored descriptor’s canonical definitional surface, especially before or outside DHT storage.

---

## 4. Descriptor Architecture

### 4.1 Descriptor Graph

The Descriptor Graph is MAP's semantic source of truth.

It contains:

- TypeDescriptors
- PropertyDescriptors
- RelationshipDescriptors
- ValueDescriptors
- KeyRules
- Extends relationships
- validation semantics
- affordance semantics
- metadata

The Descriptor Graph is optimized for:

- authoring
- governance
- inheritance
- introspection
- visualization
- documentation
- evolution

It is not the preferred peer-validation runtime surface.

---

### 4.2 EffectiveDescriptor

An `EffectiveDescriptor` is the canonical runtime descriptor surface produced from the Descriptor Graph.

It materializes:

- inherited properties
- declared properties
- inherited relationships
- declared relationships
- inverse relationship surfaces
- value constraints
- key rules
- relevant structural validation semantics
- other flattened definitional relationships needed for runtime interpretation

The `EffectiveDescriptor` is deterministic, compact, and content-addressable.

It is the primary descriptor artifact used by both:

- PVL, for peer-reproducible structural validation
- Nursery / Validation Engine, for richer transaction-local validation

---

### 4.3 Descriptor Edit Lifecycle

Descriptor edits trigger compilation.

    Descriptor edit
        → canonical definitional surface
        → DefinitionHash
        → EffectiveDescriptor
        → EntryHash(EffectiveDescriptor)
        → semantic version assignment

Any descriptor edit that changes the effective semantic surface produces:

- a new `DefinitionHash`
- a new `EffectiveDescriptor`
- a new `EntryHash(EffectiveDescriptor)`
- a new semantic version

Type activation does not create descriptor identity.

Type activation authorizes use of an already-defined descriptor surface within a HolonSpace.

---

### 4.4 Relationship Classification

Relationships should be classified conceptually into:

- definitional relationships
- operational relationships
- contextual relationships
- provenance/routing relationships

Only definitional relationships participate in:

- `DefinitionHash`
- `EffectiveDescriptor`
- `EntryHash(EffectiveDescriptor)` as definitional content identity

---

## 5. Type Activation

### 5.1 Purpose

A HolonSpace is a long-lived agent relationship context, not an application container.

New holon types must be introducible into an existing HolonSpace without requiring the creation of a new DHT or DNA.

Type activation is the mechanism by which a HolonSpace recognizes an `EffectiveDescriptor` as valid for use within that space.

---

### 5.2 Activation Boundary

Activation answers:

> Which descriptor surfaces does this HolonSpace recognize for use?

It does not answer:

> What does this descriptor mean?

Meaning is established by the descriptor and its `EffectiveDescriptor`.

Activation is a space-governance decision.

Descriptor identity is a definitional decision.

---

### 5.3 Activation Record

A type activation record should identify, at minimum:

- the HolonSpace
- the semantic type identity
- the `DefinitionHash`
- the semantic version
- the `EntryHash(EffectiveDescriptor)`
- activation status
- activation authority / governance evidence, where required

Activation status may include:

- Proposed
- Active
- Disabled
- Deprecated

---

## 6. HolonNode Descriptor Binding

### 6.1 Committed Descriptor Reference

Committed `HolonNode`s should carry an explicit reference to the activated effective descriptor used for peer validation.

Conceptually:

    HolonNode {
        local_id: ActionHash-derived identity after commit
        described_by: TypeDescriptor identity
        effective_descriptor_hash: EntryHash(EffectiveDescriptor)
        properties: PropertyMap
        ...
    }

The exact field names may vary, but the committed representation must give peer validation direct access to the content-addressed descriptor artifact required for PVL.

A `DescribedBy` relationship may still exist in the MAP graph, but peer validation must not depend on chasing a `SmartLink` in order to discover the descriptor surface needed for validation.

---

### 6.2 Meaning of the Descriptor Binding

The fields answer different questions:

- `described_by` answers: What type does this holon claim to instantiate?
- `effective_descriptor_hash` answers: Which content-addressed runtime descriptor surface validates this holon?
- Type activation answers: Is this effective descriptor authorized for use in this HolonSpace?

---

## 7. Peer Validation Language (PVL)

### 7.1 Definition

PVL is the deterministic validation substrate embedded in the Integrity Zome.

PVL evaluates:

- storage-envelope constraints
- cryptographic/canonical-form checks
- the peer-reproducible subset of descriptor semantics expressed in an `EffectiveDescriptor`

PVL is an interpreter for a bounded descriptor surface, not a general MAP runtime.

---

### 7.2 Properties

PVL must be:

- deterministic
- bounded
- local to a closed validation context
- reconstructible by peers
- independent of coordinator/runtime services
- independent of ReferenceLayer lookup
- independent of caches
- independent of Dance dispatch
- independent of agreement interpretation

---

### 7.3 PVL Constructs

PVL always includes storage-envelope rules such as:

- `HolonNode` and `SmartLink` well-formedness
- canonical serialization and hash consistency
- author/action/signature checks available to Holochain validation
- lifecycle transition checks that can be evaluated from the op's bounded context
- key and path derivation checks that require no lookup beyond explicit inputs

PVL may also include `EffectiveDescriptor`-backed rules such as:

- type conformance
- required property presence
- value type validation
- enum membership
- relationship typing
- bounded cardinality where reconstructible
- referential integrity where dependencies are content-addressed and retrievable

These rules are PVL-safe only because the descriptor context has already been flattened into a bounded `EffectiveDescriptor`.

---

### 7.4 PVL Boundary

PVL excludes:

- live descriptor graph traversal
- inheritance computation
- `EffectiveDescriptor` generation
- ReferenceLayer APIs
- coordinator managers
- HolonsCache
- DescriptorsCache
- dynamic rule dispatch
- validation Dances
- runtime plugin/module loading
- temporal logic
- external dependencies
- TrustChannel evaluation
- agreement semantics
- role-based access interpretation
- global uniqueness
- open-world graph traversal
- semantic conflict resolution

---

## 8. Integrity Layer

### 8.1 Scope

Scope: op-level validation  
Guarantee: peer-reproducible  
Language: PVL

The Integrity Layer owns DHT admissibility.

It does not own full semantic truth.

---

### 8.2 Responsibilities

The Integrity Layer is responsible for:

- validating `HolonNode` storage envelope
- validating `SmartLink` storage envelope
- retrieving required `EffectiveDescriptor` records by hash
- validating that retrieved `EffectiveDescriptor`s are themselves valid DHT records
- verifying that a `HolonNode`'s descriptor binding is internally consistent
- running PVL over `HolonNode + EffectiveDescriptor`
- running PVL over `SmartLink + relevant EffectiveDescriptor context`
- returning valid / invalid / unresolved dependency outcomes

---

### 8.3 Retrieval of EffectiveDescriptors

When validating a `HolonNode`, the Integrity Zome reads the `effective_descriptor_hash` from the committed representation and retrieves the corresponding record using Holochain deterministic dependency retrieval.

Conceptually:

    validate(HolonNode op)
        read holon.effective_descriptor_hash
        must_get_valid_record(effective_descriptor_hash)
        if unavailable:
            return UnresolvedDependencies
        decode EffectiveDescriptor
        confirm it applies to holon.described_by
        run PVL checks
        accept or reject

This handles propagation-order latency.

A peer need not already possess the `EffectiveDescriptor` locally. It must be able to retrieve it by hash from the same DHT.

---

### 8.4 Validation of EffectiveDescriptor Writes

`EffectiveDescriptor` writes require a bootstrap validation path.

An `EffectiveDescriptor` cannot be validated by the `EffectiveDescriptor` it introduces.

Therefore, `EffectiveDescriptor` entries are validated by fixed core PVL rules embedded in the Integrity Zome / DNA.

Integrity validation of an `EffectiveDescriptor` should check:

- canonical encoding
- well-formed `EffectiveDescriptor` structure
- supported constraint opcodes / PVL constructs
- boundedness of all referenced structural elements
- hash consistency
- declared type identity shape
- declared semantic version shape
- declared source definition hash shape

Integrity validation does not necessarily prove that the `EffectiveDescriptor` was correctly compiled from the Descriptor Graph unless the compiler proof is itself PVL-checkable.

Compilation correctness may be established by:

- deterministic coordinator compiler
- tests
- governance
- activation records
- attestations
- future reproducible compiler receipts

---

## 9. Nursery Validation

### 9.1 Role

The Nursery is the primary execution environment for descriptor-driven validation that exceeds PVL's boundary but is still meaningfully checkable before commit.

It owns staged local state and transaction-local semantic coherence.

---

### 9.2 Capabilities

The Nursery can enforce:

- multi-holon invariants
- transaction-scoped constraints
- snapshot-based checks
- bounded semantic rule evaluation
- descriptor-backed query/filter checks over transaction plus local snapshot
- dynamic or extensible validation rule execution when allowed
- validation result generation
- warning and deferred-work classification

---

### 9.3 Limitations

The Nursery:

- operates on a partial DHT view
- cannot guarantee global correctness
- remains subject to race conditions
- must not be mistaken for peer consensus
- must not be treated as a substitute for Integrity validation

---

### 9.4 Validation Categories

#### Required / Hard Fail

- transaction-internal invariants
- bounded cardinality after transaction application
- direct referential consistency
- required claim presence
- descriptor-backed rules whose evaluation is bounded and mandatory for local correctness

#### Warning

- likely duplicates based on snapshot inspection
- advisory semantic rules
- quality checks
- descriptor-backed heuristics that are useful but not authoritative

#### Deferred

- global uniqueness
- cross-agent constraints
- agreement-level validation
- socially resolved semantic disputes
- open-world consistency checks

---

### 9.5 Outcomes

- Fail → abort transaction
- Valid → proceed to commit
- Warn → commit with warnings
- Defer → commit and surface follow-up work

Validation results may be recorded as holons where useful, but they are not the primary basis of peer validation.

---

## 10. Transactions

### 10.1 Role

Transactions are the unit of semantic coherence.

They group staged holon and relationship changes into a meaningful commit boundary.

---

### 10.2 Properties

Transactions:

- explicitly enumerate affected holons and links
- form a bounded validation context
- support pre-commit validation
- may carry validation results
- support lifecycle states:
  - Provisional
  - Validated
  - Committed
  - CommittedWithWarnings
  - Failed

---

### 10.3 Relationship to Descriptor-Driven Validation

Transactions matter because many descriptor-defined rules are not meaningful at single-op granularity.

Examples:

- post-update relationship cardinality
- coherence across multiple coordinated writes
- command preconditions spanning several holons
- dance execution preconditions
- batch import consistency

These belong in the Nursery / Validation Engine unless the complete relevant context is bounded and peer-reconstructible.

---

## 11. Validation Receipts and ValidationResults

A validation receipt is attributable evidence that a validation process evaluated a specific input under a specific rule surface and produced a specific outcome. Receipts may be persisted as `ValidationResult` holons, linked from Transactions, or included in transaction metadata.

Receipts are not the primary basis of peer validation. Peer validation should recompute PVL-safe rules against content-addressed `EffectiveDescriptor`s wherever possible.

Receipts remain useful for Nursery validation, warnings, deferred checks, dynamic validation rule outcomes, TrustChannel validation, audit trails, attestations, and conflict resolution.

A receipt should identify:

- validated input digest
- validation scope
- descriptor identity or `EntryHash(EffectiveDescriptor)`
- rule set or rule ids
- validation engine identity and version, where applicable
- validator identity
- outcome: failed, valid, warning, deferred
- signature or attestation, where applicable

Integrity may verify a receipt only when the receipt acceptance rule is itself PVL-safe. Integrity verification may check receipt format, digest binding, descriptor identity, validator identity, and signature. This verifies an asserted validation outcome; it does not prove semantic correctness unless the relevant semantics are themselves PVL-enforceable.

---

## 12. ReferenceLayer Caching

### 12.1 HolonsCache

`HolonsCache` caches stewarded holon state for convenience and performance.

Lookup identity:

- `HolonId`
- `ExternalId`

The identity regime is route-sensitive.

Cached foreign holons are disposable and do not violate the One Home Space principle.

---

### 12.2 DescriptorsCache

`DescriptorsCache` is a separate ReferenceLayer cache for descriptor artifacts.

Lookup identity:

- `DefinitionHash`
- `EntryHash(EffectiveDescriptor)`
- semantic version, where mapped
- route-to-definition equivalence mappings

The identity regime is path-insensitive and semantic.

Possible cached artifacts include:

- descriptor surfaces
- `EffectiveDescriptor`s
- descriptor equivalence mappings
- compiled descriptor-derived surfaces

The `DescriptorsCache` allows equivalent descriptors discovered through different TrustChannels or proxy paths to share cache entries.

It is not part of peer validation correctness.

Integrity/PVL must not depend on `DescriptorsCache`.

---

## 13. Trust Channels, Agreements, and RoleAccessDescriptors

### 13.1 One Home Space Principle

Every holon has exactly one Home Space.

Use outside that Home Space occurs by reference.

Foreign access is mediated by TrustChannels and represented through `ExternalId`s.

---

### 13.2 RoleAccessDescriptor

A `RoleAccessDescriptor` is a compiled access-control surface generated from:

    EffectiveDescriptor
    + Role
    + Information Access Agreement

It may specify:

- allowed properties
- allowed outbound relationships
- allowed target types
- traversal permissions
- redaction rules
- projection constraints

A `RoleAccessDescriptor` is not the same as an `EffectiveDescriptor`.

It is not used for peer validation.

It is used for agreement-mediated access and projection.

---

### 13.3 Local Persistence of Compiled Surfaces

Local persistence of `EffectiveDescriptor`s and `RoleAccessDescriptor`s is an allowable exception to the no-replication principle because these artifacts are:

- deterministic
- content-addressed
- reproducible
- disposable
- non-authoritative derivatives

They are compiled semantic surfaces, not replicated stewarded holon state.

---

## 14. Uniqueness and Claims

### 14.1 Principle

Uniqueness is not universally enforceable as an integrity invariant.

It is detected, coordinated, and resolved across layers.

---

### 14.2 Claim Holon Pattern

A claim represents ownership of a normalized value.

- deterministic key: `hash(normalized_value)`
- linked to claimant
- includes lifecycle state

---

### 14.3 Path Index

A deterministic path acts as an index:

    claims.<domain>.<hash>

Links:

    Path -> ClaimHolon

---

### 14.4 Conflict Set

All claims linked from a path form a conflict set.

---

### 14.5 Key Insight

- conflicts are detectable
- absence of conflict is not proof of uniqueness

---

## 15. Conflict Detection and Signaling

### 15.1 Detection

Conflicts may be detected:

- during Nursery validation as a best-effort local check
- during DHT integration as an eventual observation
- during reads and queries
- during background reconciliation

---

### 15.2 Signaling

Conflicts may be signaled via:

- `ConflictsWith` relationships
- conflict holons
- validation results
- attestations

---

### 15.3 Resolution

Resolution occurs outside integrity:

- transaction updates
- trust channel enforcement
- attestation consensus
- agreement processes
- human/social review

---

## 16. Links as Validation Ops

### 16.1 Principle

Link creation is a DHT op and must pass PVL validation.

---

### 16.2 Implication

Links cannot enforce:

- absence of other links
- global uniqueness
- exclusivity

---

### 16.3 Role

Links publish entries into conflict sets.

They do not by themselves prove semantic correctness.

---

## 17. Validation Flow

### Stage 1 — Descriptor Edit

- author or update Descriptor Graph
- compute canonical definitional surface
- compute `DefinitionHash`
- compile `EffectiveDescriptor`
- assign semantic version
- commit descriptor artifacts as appropriate

---

### Stage 2 — Type Activation

- HolonSpace governance activates an `EffectiveDescriptor`
- activation record identifies `EntryHash(EffectiveDescriptor)`
- activated descriptor becomes eligible for use by holons in that HolonSpace

---

### Stage 3 — Nursery

- build transaction
- resolve active `EffectiveDescriptor`s
- evaluate required, warning, and deferred descriptor-backed rules
- evaluate transaction-local semantic constraints
- fail, warn, defer, or proceed

---

### Stage 4 — Commit

- write holons and links
- committed `HolonNode`s carry `effective_descriptor_hash`
- generate DHT ops

---

### Stage 5 — Integrity Validation

- validate local storage envelope
- retrieve `EffectiveDescriptor` by `must_get_valid_record`
- return unresolved dependency if descriptor is not yet available
- run PVL over `HolonNode + EffectiveDescriptor`
- validate `SmartLink` structure and bounded relationship semantics
- accept or reject

---

### Stage 6 — Propagation

- valid data spreads across the DHT
- missing descriptor dependencies resolve through normal DHT retrieval and retry

---

### Stage 7 — Conflict Detection

- detect conflicts through links, paths, reads, queries, and reconciliation

---

### Stage 8 — Resolution

- resolve through higher coordination layers:
  - new transactions
  - TrustChannels
  - Agreements
  - Attestations
  - human/social processes

---

## 18. Component Responsibility Summary

### Descriptors Component

Owns:

- Descriptor Graph
- semantic definition
- `DefinitionHash`
- `EffectiveDescriptor` generation
- semantic versioning
- inheritance flattening

Does not own:

- peer validation execution
- agreement interpretation
- dynamic behavior execution

---

### Knowledge Graph Persistence Layer / Integrity Zome

Owns:

- DHT admissibility
- PVL interpreter
- `HolonNode` and `SmartLink` storage-envelope validation
- `must_get_valid_record` retrieval of `EffectiveDescriptor`
- peer-reproducible structural validity

Does not own:

- descriptor graph traversal
- `EffectiveDescriptor` generation
- ReferenceLayer access
- caches
- Dance execution
- agreement semantics
- open-world validation

---

### Nursery

Owns:

- staged state
- transaction-local materialization
- pre-commit validation
- bounded semantic checks
- warning/deferred outcomes

Does not own:

- peer consensus
- global truth
- DHT admissibility

---

### Validation Engine

Owns:

- rich coordinator-side validation
- descriptor interpretation above PVL
- transaction-level validation
- validation result generation

Does not own:

- Integrity validation authority

---

### Transaction Manager

Owns:

- semantic commit boundary
- transaction lifecycle
- commit orchestration
- validation state transitions

---

### Space Manager

Owns:

- type activation
- descriptor-use authorization within a HolonSpace
- activation lifecycle

Does not own:

- descriptor identity

---

### ReferenceLayer

Owns:

- `HolonsCache`
- `DescriptorsCache`
- local reference resolution
- route-sensitive and definition-sensitive cache support

Does not own:

- peer validation correctness

---

### Trust Channels and Agreements

Own:

- inter-space mediation
- ExternalId dereference authorization
- role interpretation
- Information Access Agreements
- RoleAccessDescriptor generation and use

Do not own:

- DHT structural validity

---

### Graph Query Engine

Owns:

- graph traversal
- descriptor-aware queries
- conflict discovery
- duplicate detection
- projections

Does not own:

- DHT validity

---

### Dance Dispatcher

Owns:

- behavior execution
- affordance dispatch
- Dance request/result handling

Does not own:

- PVL
- peer validation

---

## 19. Design Consequences

This architecture has several practical consequences:

- validation rules should be authored once in descriptor semantics
- descriptor edits produce `EffectiveDescriptor`s and semantic versions
- type activation authorizes descriptor use within a HolonSpace
- committed holons must carry the content-addressed `EffectiveDescriptor` needed for validation
- peer validation retrieves descriptor artifacts by hash, not by live graph traversal
- PVL interprets `EffectiveDescriptor`s but never calls MAP runtime services
- `DescriptorsCache` improves coordinator performance but is not part of integrity correctness
- query, command, and dance systems should reuse descriptor semantics rather than duplicate validation rules
- agreement-based access control compiles into separate access surfaces such as `RoleAccessDescriptor`
- semantic conflicts are expected and resolved above integrity

---

## 20. Final Principles

- structural integrity is universal
- semantic validity is contextual
- descriptors are the semantic source of validation rules
- `EffectiveDescriptor`s are the canonical runtime descriptor surface
- PVL is the peer-reproducible subset of descriptor interpretation
- Nursery is the bounded pre-commit layer for richer descriptor-driven checks
- type activation authorizes descriptor use without creating descriptor identity
- `ActionHash` identifies committed holon records
- `EntryHash(EffectiveDescriptor)` can identify compiled definitional equivalence
- `DefinitionHash` supports path-insensitive descriptor equivalence
- conflicts are inevitable
- detection is eventual
- resolution is external

---

## 21. Closing Statement

MAP should become descriptor-driven without collapsing all validation into one layer.

Descriptors define what the rules are.

`EffectiveDescriptor`s provide the canonical flattened runtime surface of those rules.

PVL defines what every peer can independently enforce from bounded, content-addressed context.

The Nursery defines which richer rules can be checked before commit.

Trust Channels, Agreements, and Attestations define how open-world meaning, access, and social truth are coordinated afterward.

This preserves Holochain's peer-validation promise while allowing MAP's ontology and applications to evolve inside stable, long-lived AgentSpaces.

# Appendices

