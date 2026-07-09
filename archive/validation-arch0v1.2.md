# MAP Validation Architecture — v1.2

## 1. Purpose

This document defines the MAP validation architecture after incorporating:

- the layered validation model from the original validation design
- the dependency gravity reframing
- PVL (Peer Validation Language)
- the Nursery / coordinator role
- transaction-vs-op validation distinctions
- the emerging descriptor architecture
- the integrity zome immutability constraint and proof-carrying validation posture

The key synthesis is:

> **Descriptors own validation semantics. Validation layers own evaluation authority.**

MAP should not treat validation rules as freestanding logic scattered across validators, queries, commands, and coordinators. Instead, descriptors define the structural and semantic rules that apply to holons, properties, relationships, and values. The validation architecture determines which subset of those descriptor-defined rules may be evaluated in which layer.

Corollary:

> **Descriptor-owned does not mean integrity-resolved.**

The Holochain integrity zome is compiled into the DNA and effectively fixed for a DHT. It must stay small, stable, deterministic, and free of coordinator/runtime dependencies. Descriptor semantics may influence peer validation only when they have been reduced to an integrity-local PVL artifact, carried explicitly in the op's bounded validation context, or represented by a locally verifiable validation receipt. Integrity validation must not resolve the live descriptor graph through coordinator services.

---

## 2. Core Principles

### 2.1 Structural vs Semantic Validation

MAP distinguishes between two broad kinds of validity:

| Type | Meaning | Typical Enforcement Layer |
|------|--------|----------------------------|
| Storage Envelope Validity | Safe, canonical, well-formed entry/link data | Integrity (PVL) |
| Descriptor Structural Validity | Schema conformance under descriptor-defined structure | PVL only when integrity-local; otherwise Nursery plus receipt |
| Semantic Validity | Correctness under richer rules, agreements, and context | Nursery, Trust Channels, Attestations |

This distinction remains important, but descriptors now refine it:

- descriptors define both structural and semantic rule surfaces
- PVL evaluates only the integrity-local, peer-reproducible subset
- Nursery evaluates descriptor graph and dynamic rule semantics before commit
- Nursery evaluates the bounded transaction/snapshot subset
- higher layers evaluate agreement- and trust-dependent subsets

### 2.2 Closed vs Open World

| Domain | World Model |
|--------|------------|
| Integrity / PVL | Closed over the op, action, fixed DNA artifacts, and explicitly carried validation evidence |
| Nursery | Locally closed over a transaction plus snapshot |
| Trust / Social | Open, evolving |

### 2.3 Validation is Layered

Validation is not a single mechanism. It is a layered architecture in which:

- descriptors provide the rule definitions
- each layer applies only the rules it can evaluate safely
- rules move outward when they exceed a layer's boundedness constraints
- coordinator-side validation may record proof-carrying evidence that integrity can verify without repeating the richer computation

### 2.4 Rule Ownership vs Enforcement Location

This is the main update prompted by the descriptor design work.

Rule ownership and rule execution should not be conflated:

- `ValueDescriptor` owns value-validation semantics and operator semantics
- `PropertyDescriptor` owns requiredness and value-type linkage
- `RelationshipDescriptor` owns relationship typing and bounded cardinality semantics
- `HolonDescriptor` owns inherited structural lookup and type-level affordance lookup

But ownership does not imply that every layer may execute every rule:

- integrity may execute only intrinsic storage-envelope rules and optional descriptor rules that have been made integrity-local
- integrity may verify validation receipts by checking hashes, signatures, descriptor identities, and declared validation inputs
- Nursery may execute richer transaction- and snapshot-aware descriptor rules
- trust/social layers may execute agreement- and interpretation-dependent rules

---

## 3. Validation Layers

### 3.1 Integrity Layer (DHT / PVL)

**Scope:** op-level validation  
**Guarantee:** peer-reproducible  
**Language:** PVL

Responsibilities:

- enforce storage-envelope correctness
- reject malformed data
- verify local cryptographic and canonical-form invariants
- verify descriptor identity and validation receipts when they are required by the entry/link format
- execute only PVL rules available from the op, fixed DNA artifacts, or other explicitly bounded integrity-local context

Integrity validation is intentionally narrow. It is not the home for live descriptor graph resolution, reference-layer access, general-purpose descriptor execution, dynamic dispatch, open-world graph queries, validation Dances, or coordinator-dependent semantics.

### 3.2 Nursery (Coordinator Pre-Commit)

**Scope:** transaction-level validation  
**Guarantee:** local pre-commit correctness  
**Context:** full transaction plus bounded snapshot

Responsibilities:

- enforce transaction coherence
- prevent avoidable invalid writes
- resolve descriptor graphs and inherited descriptor structure
- evaluate descriptor-defined rules that require full transaction context
- evaluate bounded semantic and query-style checks that do not belong in PVL
- produce validation outcomes or receipts that can be bound to committed data

### 3.3 Trust Channel Layer

**Scope:** inter-agent validation  
**Guarantee:** agreement conformance

Responsibilities:

- enforce agreements at membrane boundaries
- validate message flows
- apply policy, authorization, and protocol interpretation

### 3.4 Attestation Layer

**Scope:** social validation  
**Guarantee:** trust-weighted truth

Responsibilities:

- record validation outcomes
- establish canonical interpretations
- resolve ambiguity and conflict socially

---

## 4. Descriptors as the Validation Semantic Source

The descriptor architecture changes how MAP should think about validation.

### 4.1 Descriptor-Driven Validation

Validation semantics should be descriptor-driven rather than validator-driven.

Examples:

- value min/max/length/enum constraints come from `ValueDescriptor`
- property requiredness comes from `PropertyDescriptor`
- relationship typing and bounded cardinality come from `RelationshipDescriptor`
- inherited rules are resolved through descriptor `Extends` flattening rather than caller-side traversal

This means:

- validation, query filtering, and command/dance preconditions should converge on the same descriptor-defined semantic surface where appropriate
- MAP should avoid parallel handwritten rule definitions in multiple subsystems
- the validation architecture should classify descriptor-defined rules by where they may be enforced, not redefine them per layer

### 4.2 Descriptor Resolution Boundary

Descriptors do not automatically belong in PVL just because validation semantics now live there.

What matters is whether the relevant descriptor context is:

- deterministic
- bounded
- locally reconstructible
- fixed or explicitly enumerated for all validators

Therefore:

- descriptor-backed validation is valid in PVL only when descriptor resolution has already been reduced to an integrity-local artifact or explicitly carried bounded context
- descriptor-backed validation belongs in Nursery when evaluating it requires richer runtime context, open-ended traversal, or coordinator services
- integrity must not call coordinator descriptor wrappers, reference-layer managers, caches, networked lookup services, or dynamic rule dispatch in order to validate an op

### 4.3 Descriptor Rule Classes

Descriptor-defined rules naturally fall into three classes:

| Rule Class | Example | Enforceable In |
|-----------|---------|----------------|
| Integrity-local structural rule | HolonNode shape, SmartLink shape, descriptor-id field shape, validation-receipt digest/signature checks | PVL |
| Compiled or explicitly carried descriptor structural rule | property requiredness, enum membership, bounded cardinality with fixed descriptor context | PVL when artifact-backed; otherwise Nursery plus receipt |
| Bounded transaction/snapshot rule | post-transaction cardinality, transaction coherence, duplicate detection | Nursery |
| Open-world / social rule | global uniqueness, agreement interpretation, trust assertions | Trust / Attestation |

---

## 5. Peer Validation Language (PVL)

### 5.1 Definition

PVL is the set of storage-envelope constraints, cryptographic validation-evidence checks, and integrity-local descriptor constraints enforceable by all peers during integrity validation.

### 5.2 Properties

PVL must be:

- deterministic
- bounded
- local to a closed validation context
- reconstructible by peers
- fixed per DHT for any schema/descriptor knowledge it depends on
- independent of coordinator/runtime services and reference-layer lookup

### 5.3 PVL Constructs

PVL always includes local storage-envelope rules such as:

- `HolonNode` and `SmartLink` well-formedness
- canonical serialization and hash consistency
- author/action/signature checks available to Holochain validation
- descriptor identity field shape and consistency when the entry format requires it
- validation receipt shape, input digest, descriptor identity, rule-set identity, validator identity, and signature checks when receipts are present or required
- lifecycle transition checks that can be evaluated from the op's bounded context
- key and path derivation checks that require no lookup beyond the op's explicit inputs

PVL may also include artifact-backed or explicitly carried descriptor-defined rules, such as:

- type conformance against a fixed descriptor identity
- property presence / requiredness
- value type validation
- enum membership
- relationship typing
- bounded cardinality
- referential integrity

These rules are PVL-safe only when their descriptor context is fixed in the DNA, compiled into an integrity-local artifact, or explicitly carried in a bounded validation context that every peer can reconstruct.

When these rules are descriptor-backed, peers are still evaluating them as PVL only because the evaluation no longer requires live descriptor graph traversal.

### 5.4 Transaction-Scoped PVL

PVL may include transaction-level constraints if:

- all relevant holons are explicitly enumerated
- validation remains bounded and reconstructible
- no external or open-world state is required

This is still not a license for general transaction semantics in integrity. It is only the bounded subset.

### 5.5 PVL Boundary

PVL excludes:

- unbounded graph traversal
- live descriptor graph resolution
- reference-layer APIs, coordinator managers, caches, and networked descriptor lookup
- dynamic rule dispatch
- validation rule-set execution through Dances
- runtime plugin/module loading
- temporal logic
- external dependencies
- agreement semantics
- global uniqueness
- any descriptor evaluation that requires non-reconstructible runtime context

### 5.6 Integrity-Side PVL Execution Substrate

Descriptor semantics may reach integrity validation through only three safe channels:

1. **Fixed DNA semantics** — rules hardcoded or generated into the integrity zome for the current DNA.
2. **Integrity-local PVL artifacts** — deterministic lookup tables, compiled constraint enums, schema snapshots, or manifests bundled with the DNA and addressable without coordinator services.
3. **Explicit validation evidence** — validation receipts bound to the committed entry/link by digest, descriptor identity, rule-set identity, and signature.

The third channel does not make the integrity zome re-run descriptor validation. It lets integrity verify that the committed data is exactly the data that a coordinator-side validation process claimed to evaluate.

This distinction is critical: a validation receipt is peer-verifiable evidence of a claim, not proof that arbitrary descriptor semantics are universally enforceable in PVL.

---

## 6. Nursery Validation

### 6.1 Role

The Nursery is the primary execution environment for descriptor-driven validation that exceeds PVL's boundary but is still meaningfully checkable before commit.

It is also the default home for live descriptor graph resolution, inherited descriptor flattening, dynamic validation-rule collection, and validation Dance dispatch.

### 6.2 Capabilities

The Nursery can enforce:

- multi-holon invariants
- transaction-scoped constraints
- snapshot-based checks
- bounded semantic rule evaluation
- descriptor-backed query/filter style checks over the transaction plus local snapshot
- dynamic or extensible validation rule execution
- validation receipt generation

This is the natural home for many checks that are descriptor-owned but not peer-reproducible.

### 6.3 Limitations

- operates on a partial DHT view
- cannot guarantee global correctness
- remains subject to race conditions
- must not be mistaken for universal truth

### 6.4 Validation Categories

#### Required (Hard Fail)

- transaction-internal invariants
- bounded cardinality after transaction application
- direct referential consistency
- required claim presence
- descriptor-backed rules whose evaluation is bounded and mandatory for local correctness

#### Optional (Warning)

- likely duplicates based on snapshot inspection
- advisory semantic rules
- quality checks
- descriptor-backed heuristics that are useful but not authoritative

#### Deferred (Post-Commit / Higher Layer)

- global uniqueness
- cross-agent constraints
- agreement-level validation
- socially resolved semantic disputes

### 6.5 Outcomes

- Fail → abort transaction
- Valid → commit with validation receipt when required
- Warn → commit with warnings and receipt metadata
- Defer → commit and surface follow-up work

---

## 7. Transactions

### 7.1 Role

Transactions are the unit of semantic coherence.

### 7.2 Properties

- explicitly enumerate affected holons
- form a bounded validation context
- carry or produce validation receipts for committed holons and links where required
- support lifecycle states:
    - Provisional
    - Validated
    - Committed
    - CommittedWithWarnings
    - Failed

### 7.3 Relationship to Descriptor-Driven Validation

Transactions matter because many descriptor-defined rules are not meaningful at single-op granularity.

Examples:

- post-update relationship cardinality
- coherence across multiple coordinated writes
- command preconditions that span several holons
- dance execution preconditions when those are later descriptor-afforded

These should be evaluated in the Nursery when bounded, not pushed down into PVL merely because the rules are descriptor-defined.

### 7.4 Proof-Carrying Validation Receipts

When descriptor-aware validation cannot be executed inside integrity, the commit path should bind the coordinator-side validation result to the committed data.

A validation receipt, which may be represented as a `ValidationResult` when persisted as MAP data, should identify, at minimum:

- the digest of the entry, link, or transaction input that was validated
- the descriptor identity, descriptor version, or descriptor hash used for validation
- the rule-set identity, validation engine identity, or code/version hash when applicable
- the validation outcome and category
- the validator identity and signature

The integrity zome may then verify:

- the receipt is structurally well formed
- the signed digest matches the committed data
- the descriptor identity in the receipt matches the descriptor identity carried by the entry/link
- the signature is valid for the declared validator
- the declared validator or rule-set identity is acceptable, but only if that acceptance rule is itself integrity-local

The integrity zome does not thereby prove that the validator was trustworthy or that all semantic checks were socially sufficient. Trust in validators, rule sets, and cross-agent interpretation belongs to trust-channel and attestation layers unless the relevant rule has been adopted into PVL.

If a validation receipt is used as a hard PVL gate, the rule that says which validators, rule sets, or engine identities are acceptable must also be fixed in the DNA, carried in an explicitly bounded context, or otherwise reconstructible by every peer. Otherwise, the receipt is evidence for higher-layer interpretation, not a peer-enforceable proof of semantic correctness.

For holon validation, the descriptor identity needed for receipt verification should be available directly from the `HolonNode`'s committed representation or another explicitly bounded validation input. A `DescribedBy` relationship may still exist as part of the MAP graph, but peer validation must not depend on chasing a `SmartLink` in order to discover which descriptor was supposedly used.

---

## 8. Uniqueness and Claims

### 8.1 Principle

Uniqueness is not universally enforceable as an integrity invariant. It is detected, coordinated, and resolved across layers.

### 8.2 Claim Holon Pattern

A claim represents ownership of a normalized value.

- deterministic key: `hash(normalized_value)`
- linked to claimant
- includes lifecycle state

### 8.3 Path Index

A deterministic path acts as an index:

`claims.<domain>.<hash>`

Links:

`Path -> ClaimHolon`

### 8.4 Conflict Set

All claims linked from a path form a conflict set.

### 8.5 Key Insight

- conflicts are detectable
- absence of conflict is not proof of uniqueness

---

## 9. Conflict Detection and Signaling

### 9.1 Detection

Conflicts may be detected:

- during Nursery validation as a best-effort local check
- during DHT integration as an eventual observation
- during reads and queries
- during background reconciliation

### 9.2 Signaling

Conflicts may be signaled via:

- `ConflictsWith` relationships
- conflict holons
- validation results
- attestations

### 9.3 Resolution

Resolution occurs outside integrity:

- transaction updates
- trust channel enforcement
- attestation consensus

---

## 10. Links as Validation Ops

### 10.1 Principle

Link creation is an op and must pass PVL validation.

### 10.2 Implication

Links cannot enforce:

- absence of other links
- global uniqueness
- exclusivity

### 10.3 Role

Links publish entries into conflict sets; they do not by themselves prove semantic correctness.

---

## 11. Validation Flow

### Stage 1 — Nursery

- build transaction
- resolve the bounded descriptor context needed for validation
- evaluate required, optional, and deferred descriptor-backed rules
- collect and execute applicable dynamic validation rules when they are allowed in this layer
- produce validation receipts for committed data when required
- fail, warn, or proceed

### Stage 2 — Commit

- write holons and links
- carry descriptor identities and validation receipts in the committed representation or an explicitly bounded validation input
- generate ops

### Stage 3 — Integrity Validation

- evaluate local PVL constraints
- verify validation receipt digest/signature/descriptor consistency when required
- reject malformed or structurally invalid ops

### Stage 4 — Propagation

- data spreads across the DHT

### Stage 5 — Conflict Detection

- detect conflicts through links, paths, reads, and reconciliation

### Stage 6 — Resolution

- resolve through higher coordination layers

---

## 12. Design Consequences

This synthesis has several practical consequences for the broader MAP design:

- validation rules should be authored once in descriptor semantics, then classified by enforcement layer
- descriptor-owned rules must not force integrity to import descriptor runtime or reference-layer code
- descriptor-backed PVL requires a fixed artifact or explicit bounded context; otherwise the coordinator validates and records a receipt
- query operators and validation operators should converge where they share value semantics
- commands and dances should not become alternate homes for duplicated validation logic
- command/dance execution may use descriptor lookup and descriptor-owned preconditions, but their richer semantics will usually live above PVL
- dependency gravity should be evaluated against runtime evaluation context, not against the mere existence of descriptors

---

## 13. Final Principles

- structural integrity is universal
- semantic validity is contextual
- descriptors are the semantic source of validation rules
- PVL is the integrity-local subset of validation plus verification of proof-carrying validation evidence
- Nursery is the bounded pre-commit layer for richer descriptor-driven checks
- validation receipts bridge coordinator validation to integrity validation without pulling coordinator dependencies into the integrity zome
- conflicts are inevitable
- detection is eventual
- resolution is external

---

## 14. Closing Statement

MAP should become descriptor-driven without collapsing all validation into one layer.

Descriptors define what the rules are.

PVL defines what every peer can enforce or verify from an integrity-local context.

The Nursery defines which richer rules can be checked before commit and bound to committed data as validation evidence.

Trust and attestation define how open-world meaning is coordinated afterward.
