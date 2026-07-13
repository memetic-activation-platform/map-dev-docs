# Dependency Gravity — v3.0

## 1. Purpose

This document defines **dependency gravity** as an architectural principle for deciding where MAP validation and semantic logic may safely execute.

The original concern remains:

> Validation logic tends to pull richer runtime dependencies downward into layers that cannot safely support them.

This concern is especially acute in Holochain because the Integrity Zome is compiled into the DNA. Changing Integrity behavior changes the immutable peer-validation contract for that DHT.

MAP therefore treats the Peer Validation Layer as a small, deterministic, descriptor-independent validation floor rather than as the execution environment for evolving descriptor, rule, query, command, Dance, agreement, or social semantics.

The current synthesis is:

> **Descriptors and ValidationRules own semantics. Dependency gravity determines where those semantics may safely execute.**

Dependency gravity does not argue against descriptor-driven semantics. It prevents those semantics from pulling live descriptor resolution, coordinator services, dynamic dispatch, or open-world state into the Integrity boundary.

---

## 2. Core Insight

Dependency gravity appears when evaluating a rule requires a richer world than the current execution layer can reproduce safely.

That richer world may include:

- descriptor lookup
- descriptor inheritance
- EffectiveDescriptor interpretation
- reference-layer traversal
- caches
- transaction state
- query execution
- command preconditions
- Dance dispatch
- dynamic validation implementations
- agreement interpretation
- TrustChannel state
- external systems
- social judgment
- open-world graph state

The architectural rule is:

> If evaluating a rule requires data, traversal, services, or authority outside a layer's bounded context, the rule belongs in a higher layer.

The important question is not:

> Is this rule descriptor-driven?

The important question is:

> Can every validator in this layer evaluate the rule deterministically from the context explicitly available to that layer?

If the answer is no, dependency gravity has identified a layer violation.

---

## 3. Rule Ownership and Execution Placement

MAP separates two concerns.

### 3.1 Rule Ownership

Rule ownership identifies where the meaning of a rule is defined.

Examples:

- a `PropertyTypeDescriptor` defines whether a property is required
- a String ValueType descriptor defines string constraints
- a RelationshipType descriptor defines source and target expectations
- a `ValidationRule` holon defines a reusable semantic check
- an agreement defines role and access obligations

### 3.2 Execution Placement

Execution placement identifies where the rule can safely be evaluated.

Examples:

- native size limits execute in PVL
- required-property validation executes in the shared descriptor-aware validator
- transaction cardinality executes in Nursery
- activation checks execute at runtime
- agreement access checks execute in TrustChannel or agreement context
- social legitimacy executes through attestation or governance

Rule ownership does not imply that the rule may execute in the lowest architectural layer.

---

## 4. Validation Layers

| Layer | Available Context | Primary Responsibility |
|---|---|---|
| Peer Validation Layer | DHT op, action, fixed DNA constants, bounded deterministic dependencies | Descriptor-independent admissibility and resource safety |
| Shared Validation Framework | Supplied holon, descriptor, operation, level-specific context | Reusable descriptor-aware validation |
| Nursery | Staged transaction, local snapshot, descriptor runtime, coordinator services | Transaction-local semantic validity |
| Runtime Recognition | Activated descriptor set and runtime reads | Current AgentSpace recognition |
| Application | Workflow, command, Dance, and domain context | Application-specific validity |
| Trust and Agreement | Agreement, role, capability, TrustChannel context | Access and policy validity |
| Attestation and Social | Agents, governance, review, evidence, disputes | Social interpretation and resolution |

Rules move outward as their dependencies become less bounded, more contextual, more temporal, or more social.

---

## 5. Peer Validation Layer

## 5.1 Definition

The Peer Validation Layer is the deterministic validation kernel executed by every peer inside the Integrity Zome.

The current PVL design is intentionally **descriptor-independent**.

PVL does not resolve or interpret:

- authored Descriptor Graphs
- `TypeDescriptor`s
- `EffectiveDescriptor`s
- descriptor caches
- type activation
- coordinator state
- dynamic ValidationRules
- Dance implementations
- TrustChannel or agreement state

The authoritative rules, limits, error model, dependency handling, and callback behavior are defined in the **MAP Descriptor-Independent PVL Design Specification**.

## 5.2 PVL Guarantee

Descriptor-independent PVL proves:

> A submitted MAP entry or link is structurally well formed, uses supported native representations, remains within fixed resource bounds, and obeys the descriptor-independent create, update, delete, authorship, and provenance rules of the DNA.

It does not prove:

- that a property is declared
- that a required property is present
- that a value satisfies descriptor-defined constraints
- that an enum value is descriptor-valid
- that a relationship is declared
- that source or target types conform to a relationship descriptor
- that relationship cardinality holds
- that uniqueness holds
- that a descriptor is activated
- that an agreement permits the operation

## 5.3 PVL Includes

Descriptor-independent PVL includes rules such as:

- native `HolonNode` shape
- native `SmartLink` shape
- canonical native representations
- serialized size limits
- property count limits
- property-name representation limits
- native scalar and collection limits
- identifier validation
- update target validation
- delete target validation
- immutable native field checks
- SmartLink endpoint validation
- fixed SmartLink authorship rules
- inverse-link provenance
- validation dependency budgets
- deterministic unresolved-dependency handling

## 5.4 PVL Excludes

PVL must not include:

- live descriptor resolution
- descriptor inheritance traversal
- `ReferenceLayer` access
- `HolonsCache` or `DescriptorsCache`
- Nursery state
- coordinator services
- open-ended queries
- dynamic ValidationRule dispatch
- validation Dances
- runtime module loading
- activation checks
- temporal logic
- agreement interpretation
- social attestation
- global uniqueness
- open-world absence checks
- unbounded graph traversal

## 5.5 PVL and the Shared Validation Framework

The shared validation framework has no implementation dependency on PVL.

PVL may reuse selected pure, Integrity-safe components such as:

- structured result or error types
- rule traits
- narrow validation helpers
- naming-validation helpers
- native value-validation helpers
- shared create, update, delete, and SmartLink entry-point patterns

PVL-specific concerns remain owned by the PVL implementation:

- fixed resource limits
- `PvlViolation`
- stable PVL error codes
- dependency budgets
- Holochain callback mapping
- unresolved dependency results
- Integrity logging policy

The shared validation framework must not be distorted into a Holochain-specific API merely to accommodate PVL.

---

## 6. Shared Descriptor-Aware Validation

The shared validation framework evaluates descriptor-defined structure when the caller supplies the required descriptor context.

It includes validators for:

- holons
- properties
- generic values
- specific ValueTypes
- relationships
- transactions

The framework does not own descriptor retrieval.

Its callers may include:

- Holon Data Loader
- Nursery
- coordinator preflight
- import tools
- diagnostics
- runtime services

The validator hierarchy may include:

    HolonValidator
        PropertyValidator
            ValueValidator
                StringValueValidator
                IntegerValueValidator
                BooleanValueValidator
                EnumValueValidator
                BytesValueValidator
        RelationshipValidator

This framework is richer than descriptor-independent PVL because it may evaluate rules such as:

- required properties
- undescribed properties
- ValueType conformance
- descriptor-defined string limits
- numeric ranges
- legal enum variants
- relationship declaration
- source and target type conformance

These rules remain reusable and pure where practical, but they require descriptor context unavailable to descriptor-independent PVL.

---

## 7. Nursery as the Anti-Gravity Layer

The Nursery absorbs validation work that dependency gravity rejects from PVL.

It provides a bounded pre-commit environment with access to:

- staged holons
- staged relationships
- transaction scope
- a local snapshot
- descriptor runtime services
- activation state
- coordinator APIs
- dynamic validation engines where allowed

Nursery validation may evaluate:

- descriptor-aware holon validation
- multi-holon coherence
- required relationships
- relationship cardinality
- transaction-wide invariants
- duplicate detection against a snapshot
- command preconditions
- Dance preconditions
- activation-aware descriptor selection
- dynamic ValidationRules
- import-batch consistency

Nursery validation is:

- stronger than PVL in semantic scope
- bounded by transaction and snapshot context
- authoritative for honest coordinators
- not peer consensus
- not proof of global absence or uniqueness

The Nursery reduces invalid commits without pretending that local snapshot validation establishes universal truth.

---

## 8. Declarative Validation and Dependency Gravity

MAP's validation architecture is intended to become declarative and extensible.

Validation rules may eventually be represented as first-class holons:

- `ValidationRule`
- `ValidationImplementation`
- `ValidationRuleSet`
- `ValidationResult`

Type descriptors may declare rules through a relationship such as:

    <TypeDescriptor> —InstanceValidations→ <ValidationRule>

Meta-types may contribute starter validations for their type kind. Concrete descriptors may inherit and add rules.

Dependency gravity constrains how these rules execute.

### Built-In Rust Execution

Initial validation uses:

- Rust traits
- level-specific validation contexts
- built-in rule implementations
- hard-coded invocation
- no dynamic dispatch

This is suitable for the Proof of Concept.

### Descriptor-Driven Built-In Dispatch

A later stage may:

1. read rule identities from descriptors
2. resolve those identities through a built-in registry
3. instantiate Rust implementations
4. execute them with the appropriate validation context

This remains coordinator-side or runtime behavior unless a rule is separately adopted into PVL as fixed Integrity logic.

### Dance-Based Validation

Nursery and higher layers may eventually execute validation through Dances.

This may require:

- rule discovery
- implementation activation
- ABI resolution
- module loading
- capability checks
- sandboxing
- runtime context
- TrustChannel or policy evaluation

These dependencies make general Dance-based validation unsuitable for PVL.

---

## 9. Validation Rules as a Gravity Classifier

A rule may be classified by the strongest context it requires.

### Class 1 — Native Structural Rules

Inputs:

- current entry or link
- fixed constants
- canonical native types

Examples:

- entry size
- property count
- property-name length
- native string size
- SmartLink tag size

Placement:

- PVL
- coordinator preflight

### Class 2 — Bounded Dependency Rules

Inputs:

- current operation
- a fixed number of content-addressed dependencies

Examples:

- update target shape
- delete target shape
- inverse-link provenance
- fixed authorship validation

Placement:

- PVL
- coordinator preflight

### Class 3 — Descriptor-Aware Local Rules

Inputs:

- target holon
- supplied descriptor
- bounded descriptor-owned constraints

Examples:

- required properties
- undescribed properties
- ValueType match
- string range
- integer range
- enum membership
- relationship typing

Placement:

- shared validation framework
- Holon Data Loader
- Nursery
- runtime diagnostics

Not part of descriptor-independent PVL.

### Class 4 — Transaction and Snapshot Rules

Inputs:

- staged transaction
- bounded local snapshot
- related holons and links

Examples:

- cardinality after transaction application
- required outbound relationships
- duplicate detection
- cross-holon coherence
- command preconditions
- Dance preconditions

Placement:

- Nursery

### Class 5 — Runtime Recognition Rules

Inputs:

- current activation state
- AgentSpace governance state
- runtime reads

Examples:

- active descriptor recognition
- quarantine classification
- current publication state

Placement:

- runtime recognition layer

### Class 6 — Agreement and Trust Rules

Inputs:

- agreements
- roles
- capabilities
- TrustChannels
- projection policies

Examples:

- access validity
- disclosure permissions
- exfiltration policy
- role-bound operation permission

Placement:

- Trust and Agreement layer

### Class 7 — Social and Open-World Rules

Inputs:

- attestations
- governance decisions
- dispute processes
- open-world evidence

Examples:

- canonical claim recognition
- social legitimacy
- conflict resolution
- steward approval

Placement:

- Attestation and Social layer

---

## 10. Query, Commands, and Dances

Dependency gravity applies beyond validation code.

## 10.1 Queries

Query and validation operators may share descriptor-owned value semantics.

That reuse is desirable.

However:

- pure comparison helpers may be shared
- bounded filtering over explicit values may be reused
- open-ended graph traversal is not PVL-safe
- query-engine dependencies must not enter Integrity

## 10.2 Commands

Commands often combine:

- lookup
- authorization
- preconditions
- side effects
- multi-holon changes
- transaction coordination

Only native structural validation of the resulting operations belongs in PVL.

Command preconditions generally belong in Nursery or application context.

## 10.3 Dances

Dances are intended to be extensible and behavior-rich.

Dance execution may depend on:

- affordance resolution
- implementation lookup
- ABI compatibility
- dynamic modules
- external capabilities
- social or agreement context

Dance execution is therefore ordinarily outside PVL.

A validation Dance may contribute to Nursery or higher-layer validation, but it must not become an Integrity dependency.

---

## 11. SmartLinks as a Boundary Example

SmartLinks illustrate how dependency gravity separates native validity from semantic validity.

### PVL May Validate

- native tag shape
- tag size
- relationship-name representation
- endpoint representation
- link authorship
- delete target
- inverse-link provenance
- dependency budget

### Shared Descriptor-Aware Validation May Validate

- relationship declaration
- source type conformance
- target type conformance
- descriptor-defined tag constraints

### Nursery May Validate

- minimum cardinality
- maximum cardinality
- required relationships
- exclusivity within transaction scope
- transaction-wide relationship coherence

### Runtime or Social Layers May Validate

- global uniqueness
- absence of conflicting links
- agreement legitimacy
- canonical relationship claims

This separation avoids forcing open-world relationship semantics into op-level peer validation.

---

## 12. Uniqueness as a Case Study

Uniqueness remains a useful example of dependency gravity.

### PVL

PVL may validate:

- deterministic claim shape
- key representation
- native identifier form

PVL cannot prove global absence of competing claims.

### Nursery

Nursery may perform:

- best-effort duplicate detection
- transaction-local uniqueness
- snapshot-based conflict checks

### Runtime

Runtime may surface:

- competing claims
- ambiguity
- unrecognized or stale claims

### Trust and Social Layers

Higher layers may establish:

- accepted canonical claim
- steward resolution
- agreement-based ownership
- conflict adjudication

Therefore:

> Uniqueness is not a descriptor-independent peer-validation invariant. It is a coordination property evaluated across layers.

---

## 13. Transaction Semantics and Op Validation

Holochain validates at operation granularity.

MAP semantics often span a transaction.

This mismatch must not be resolved by pulling transaction semantics into Integrity.

Instead:

- PVL validates each operation's native admissibility
- shared validators evaluate supplied descriptors
- Nursery validates staged transaction semantics
- runtime applies recognition state
- higher layers handle agreement and social meaning

A transaction-level rule belongs in PVL only if a future design makes every required input:

- explicit
- bounded
- deterministic
- reconstructible by every peer

Until then, transaction semantics remain outside PVL.

---

## 14. Receipts and Validation Evidence

ValidationResults and receipts are useful evidence for coordinator, runtime, trust, and social processes.

They may record:

- target digest
- descriptor identity
- rule identity
- implementation identity
- validator identity
- outcome
- signature
- attestation

They are not part of descriptor-independent PVL's normal validity model.

PVL failures do not create:

- ValidationResult holons
- receipts
- conflict holons
- audit entries

Integrity cannot safely trigger compensating DHT writes for invalid operations.

A receipt proves that a validation assertion was made. It does not prove that every peer could independently reproduce the asserted semantics.

If a future PVL design accepts a receipt as a hard gate, the receipt-verification rule and accepted validator identity must themselves be fixed, bounded, deterministic, and independently reproducible.

---

## 15. Dependency Direction Between Validation and PVL

The shared validation implementation plan does not depend on the PVL implementation plan.

The preferred dependency direction is:

    shared validation foundation
        ↓
    descriptor-independent PVL helpers and adapters
        ↓
    Integrity Zome integration

PVL may depend on selected validation-plan tasks such as:

- validation foundation types
- validation rule traits and contexts
- pure native value helpers
- relationship validation abstractions
- shared validation entry-point patterns
- diagnostics and fixture conventions

The shared validation plan must not wait for:

- PVL limits
- PVL error codes
- dependency-budget implementation
- Holochain callback integration
- SmartLink authorship policy
- PVL benchmarks

The only reverse pressure is architectural:

- shared components reused by PVL must remain Integrity-safe
- PVL-specific concerns must not leak into general validator APIs
- coordinator dependencies must remain outside Integrity-safe crates

These are boundary constraints, not implementation dependencies.

---

## 16. Practical Decision Test

Before placing a rule, ask the following questions in order.

### 1. Can it be evaluated from the current entry or link and fixed DNA constants?

If yes, it may belong in PVL.

### 2. Does it require only a fixed, bounded number of deterministic dependencies?

If yes, it may still belong in PVL.

### 3. Does it require a supplied descriptor but no runtime services?

If yes, it belongs in the shared descriptor-aware validation framework.

### 4. Does it require staged transaction or snapshot context?

If yes, it belongs in Nursery.

### 5. Does it depend on current activation or runtime recognition?

If yes, it belongs in runtime validation.

### 6. Does it depend on roles, agreements, capabilities, or TrustChannels?

If yes, it belongs in the Trust and Agreement layer.

### 7. Does it depend on global absence, social judgment, governance, or dispute resolution?

If yes, it belongs in Attestation or Social validation.

When uncertain, place the rule in the higher layer until its dependency boundary is proven safe.

---

## 17. Final Model

Dependency gravity defines the execution boundary for MAP semantics.

- ValidationRules and descriptors define semantic commitments.
- The shared validation framework evaluates descriptor-aware local rules.
- PVL enforces descriptor-independent native admissibility.
- Nursery evaluates bounded transaction and snapshot semantics.
- Runtime recognition evaluates current activation state.
- Trust and Agreement layers evaluate policy and access.
- Attestation and Social layers evaluate open-world meaning.

This architecture allows MAP to preserve both:

- a small, stable, deterministic Integrity kernel
- an open-ended, declarative, extensible semantic system

The two are compatible because dependency gravity prevents richer runtime semantics from collapsing into the peer-validation boundary.

---

## 18. Closing Statement

Dependency gravity is not an obstacle to descriptor-driven or rule-driven MAP validation.

It is the architectural discipline that tells us where each rule can safely run.

If a rule fits inside the descriptor-independent, bounded, deterministic PVL context, it may execute in Integrity.

If it requires a supplied descriptor, it belongs in the shared validation framework.

If it requires transaction or snapshot context, it belongs in Nursery.

If it requires activation, agreement, trust, or social interpretation, it belongs higher still.

MAP should move rules outward as their dependencies grow rather than pulling the runtime inward.