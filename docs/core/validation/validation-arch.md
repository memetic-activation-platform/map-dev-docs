# MAP Validation Architecture — v1.1

## 1. Purpose

This document defines the MAP validation architecture after incorporating:

- the layered validation model from the original validation design
- the dependency gravity reframing
- PVL (Peer Validation Language)
- the Nursery / coordinator role
- transaction-vs-op validation distinctions
- the emerging descriptor architecture

The key synthesis is:

> **Descriptors own validation semantics. Validation layers own evaluation authority.**

MAP should not treat validation rules as freestanding logic scattered across validators, queries, commands, and coordinators. Instead, descriptors define the structural and semantic rules that apply to holons, properties, relationships, and values. The validation architecture determines which subset of those descriptor-defined rules may be evaluated in which layer.

---

## 2. Core Principles

### 2.1 Structural vs Semantic Validation

MAP distinguishes between two broad kinds of validity:

| Type | Meaning | Typical Enforcement Layer |
|------|--------|----------------------------|
| Structural Validity | Safe, well-formed, schema-conformant data | Integrity (PVL) |
| Semantic Validity | Correctness under richer rules, agreements, and context | Nursery, Trust Channels, Attestations |

This distinction remains important, but descriptors now refine it:

- descriptors define both structural and semantic rule surfaces
- PVL evaluates the closed-world, peer-reproducible subset
- Nursery evaluates the bounded transaction/snapshot subset
- higher layers evaluate agreement- and trust-dependent subsets

### 2.2 Closed vs Open World

| Domain | World Model |
|--------|------------|
| Integrity / PVL | Closed, bounded |
| Nursery | Locally closed over a transaction plus snapshot |
| Trust / Social | Open, evolving |

### 2.3 Validation is Layered

Validation is not a single mechanism. It is a layered architecture in which:

- descriptors provide the rule definitions
- each layer applies only the rules it can evaluate safely
- rules move outward when they exceed a layer's boundedness constraints

### 2.4 Rule Ownership vs Enforcement Location

This is the main update prompted by the descriptor design work.

Rule ownership and rule execution should not be conflated:

- `ValueDescriptor` owns value-validation semantics and operator semantics
- `PropertyDescriptor` owns requiredness and value-type linkage
- `RelationshipDescriptor` owns relationship typing and bounded cardinality semantics
- `HolonDescriptor` owns inherited structural lookup and type-level affordance lookup

But ownership does not imply that every layer may execute every rule:

- integrity may execute only deterministic, bounded, reconstructible descriptor rules
- Nursery may execute richer transaction- and snapshot-aware descriptor rules
- trust/social layers may execute agreement- and interpretation-dependent rules

---

## 3. Validation Layers

### 3.1 Integrity Layer (DHT / PVL)

**Scope:** op-level validation  
**Guarantee:** peer-reproducible  
**Language:** PVL

Responsibilities:

- enforce structural correctness
- reject malformed data
- evaluate the closed-world subset of descriptor-defined rules

Integrity validation is intentionally narrow. It is not the home for general-purpose descriptor execution, dynamic dispatch, open-world graph queries, or coordinator-dependent semantics.

### 3.2 Nursery (Coordinator Pre-Commit)

**Scope:** transaction-level validation  
**Guarantee:** local pre-commit correctness  
**Context:** full transaction plus bounded snapshot

Responsibilities:

- enforce transaction coherence
- prevent avoidable invalid writes
- evaluate descriptor-defined rules that require full transaction context
- evaluate bounded semantic and query-style checks that do not belong in PVL

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

- descriptor-backed validation is valid in PVL only when descriptor resolution stays within the PVL boundary
- descriptor-backed validation belongs in Nursery when evaluating it requires richer runtime context, open-ended traversal, or coordinator services

### 4.3 Descriptor Rule Classes

Descriptor-defined rules naturally fall into three classes:

| Rule Class | Example | Enforceable In |
|-----------|---------|----------------|
| Pure closed-world structural rule | property requiredness, enum membership, bounded cardinality | PVL |
| Bounded transaction/snapshot rule | post-transaction cardinality, transaction coherence, duplicate detection | Nursery |
| Open-world / social rule | global uniqueness, agreement interpretation, trust assertions | Trust / Attestation |

---

## 5. Peer Validation Language (PVL)

### 5.1 Definition

PVL is the set of descriptor-backed and core-schema-backed constraints enforceable by all peers during integrity validation.

### 5.2 Properties

PVL must be:

- deterministic
- bounded
- local to a closed validation context
- reconstructible by peers
- fixed per DHT for any schema/descriptor knowledge it depends on

### 5.3 PVL Constructs

PVL includes the closed-world subset of descriptor-defined rules, including:

- type conformance (`DescribedBy`)
- property presence / requiredness
- value type validation
- enum membership
- key rules
- relationship typing
- bounded cardinality
- referential integrity
- lifecycle transitions

When these rules are descriptor-backed, peers are still evaluating them as PVL because the evaluation remains bounded and reproducible.

### 5.4 Transaction-Scoped PVL

PVL may include transaction-level constraints if:

- all relevant holons are explicitly enumerated
- validation remains bounded and reconstructible
- no external or open-world state is required

This is still not a license for general transaction semantics in integrity. It is only the bounded subset.

### 5.5 PVL Boundary

PVL excludes:

- unbounded graph traversal
- dynamic rule dispatch
- runtime plugin/module loading
- temporal logic
- external dependencies
- agreement semantics
- global uniqueness
- any descriptor evaluation that requires non-reconstructible runtime context

---

## 6. Nursery Validation

### 6.1 Role

The Nursery is the primary execution environment for descriptor-driven validation that exceeds PVL's boundary but is still meaningfully checkable before commit.

### 6.2 Capabilities

The Nursery can enforce:

- multi-holon invariants
- transaction-scoped constraints
- snapshot-based checks
- bounded semantic rule evaluation
- descriptor-backed query/filter style checks over the transaction plus local snapshot

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
- Warn → commit with warnings
- Defer → commit and surface follow-up work

---

## 7. Transactions

### 7.1 Role

Transactions are the unit of semantic coherence.

### 7.2 Properties

- explicitly enumerate affected holons
- form a bounded validation context
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
- fail, warn, or proceed

### Stage 2 — Commit

- write holons and links
- generate ops

### Stage 3 — Integrity Validation

- evaluate PVL constraints
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
- query operators and validation operators should converge where they share value semantics
- commands and dances should not become alternate homes for duplicated validation logic
- command/dance execution may use descriptor lookup and descriptor-owned preconditions, but their richer semantics will usually live above PVL
- dependency gravity should be evaluated against runtime evaluation context, not against the mere existence of descriptors

---

## 13. Final Principles

- structural integrity is universal
- semantic validity is contextual
- descriptors are the semantic source of validation rules
- PVL is the closed-world subset of descriptor-driven validation
- Nursery is the bounded pre-commit layer for richer descriptor-driven checks
- conflicts are inevitable
- detection is eventual
- resolution is external

---

## 14. Closing Statement

MAP should become descriptor-driven without collapsing all validation into one layer.

Descriptors define what the rules are.  
PVL defines which rules every peer can enforce.  
The Nursery defines which richer rules can be checked before commit.  
Trust and attestation define how open-world meaning is coordinated afterward.
