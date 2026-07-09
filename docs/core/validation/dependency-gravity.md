# Dependency Gravity (Reframed) — v2.1

## 1. Purpose

This document reframes dependency gravity in light of the evolved MAP validation architecture and the new descriptor design work.

The original concern still stands: validation logic tends to pull richer runtime dependencies downward into layers that cannot safely support them.

The concern is especially acute in Holochain because the integrity zome is compiled into the DNA. A change to integrity validation changes the DNA boundary for a DHT. MAP therefore treats integrity validation as a small, stable, peer-reproducible kernel rather than as the place where evolving descriptor and rule semantics execute.

The descriptor work sharpens that concern rather than invalidating it.

> **Dependency gravity is not caused by descriptors themselves. It is caused by trying to evaluate descriptor-defined semantics in a layer whose validation boundary is too small.**

That leads to a more precise synthesis:

> **Descriptors own semantics. Dependency gravity determines where those semantics may be executed.**

---

## 2. Core Insight

### 2.1 Original Framing

Dependency gravity arises when:

- validation requires descriptor resolution
- descriptor resolution requires graph traversal
- graph traversal requires reference-layer services
- those services require coordinator/runtime infrastructure
- dynamic validation rules require Dance dispatch or pluggable execution engines

Result:

> The integrity layer becomes entangled with runtime concerns it cannot safely support.

### 2.2 Revised Framing

The deeper issue is not "descriptors are dangerous." The issue is:

> Dependency gravity appears when a rule needs data, traversal, or runtime services beyond a layer's closed validation boundary.

That boundary problem may be triggered by:

- descriptor lookup
- query execution
- command precondition evaluation
- dance affordance resolution
- dynamic validation rule dispatch
- snapshot inspection
- agreement interpretation

So the real lesson is architectural:

> If evaluating a rule requires a richer world than the current layer can reproduce, the rule belongs in a higher layer.

---

## 3. Layered Resolution

MAP resolves dependency gravity by separating rule ownership from enforcement layer.

| Layer | Responsibility | What It May Safely Evaluate |
|------|----------------|-----------------------------|
| Integrity (PVL) | Storage-envelope integrity | Local structure, fixed PVL artifacts, and validation receipt checks |
| Nursery | Transaction coherence | Descriptor graph resolution, dynamic rule execution, bounded transaction/snapshot-aware descriptor-backed rules |
| Trust Channel | Agreement enforcement | Policy and agreement semantics |
| Attestation | Social validation | Open-world interpretation and canonicalization |

This layered model means MAP does not need to choose between:

- descriptor-driven semantics
- safe bounded validation

It can have both, as long as the rules are evaluated in the right place.

---

## 4. Descriptor-Sensitive Dependency Gravity

### 4.1 What the Descriptor Design Changes

The descriptor architecture introduces a strong semantic center:

- `ValueDescriptor` owns value-validation and operator semantics
- `PropertyDescriptor` owns requiredness and value-type linkage
- `RelationshipDescriptor` owns relationship structure and bounded cardinality semantics
- `HolonDescriptor` owns inherited structural lookup and behavior affordance lookup

This is good architectural pressure. It reduces duplicated logic across validators, query code, commands, and other helpers.

### 4.2 What It Does Not Change

Descriptor ownership does not imply universal evaluability.

For example:

- a value-range check may belong in PVL only when its descriptor context is fixed, compiled, or explicitly carried
- a post-transaction relationship-cardinality check may belong in Nursery
- a command precondition spanning several holons may belong in Nursery
- a dance's social legitimacy may belong in trust/attestation layers

Dependency gravity therefore acts as a classifier:

- if the descriptor-defined rule is closed-world and already integrity-local, keep it in PVL
- if the rule can be reduced to a fixed PVL artifact for this DNA, it may be adopted into PVL
- if it needs bounded transaction/snapshot context, move it to Nursery
- if it can be checked by the coordinator but not re-executed by peers, bind the result to the commit with a validation receipt
- if it needs open-world or social context, move it higher

### 4.3 The Real Boundary

The important question is not:

> "Is this rule descriptor-driven?"

The important question is:

> "Can every validator evaluate this rule from a bounded, explicitly defined context?"

If the answer is no, dependency gravity has already told us the rule does not belong in PVL.

A second question then matters:

> "Can every validator at least verify the validation claim from local cryptographic evidence?"

If yes, the rule may be enforced pre-commit in the Nursery and represented in integrity by a validation receipt. If no, the outcome belongs to trust, attestation, reconciliation, or another higher layer.

---

## 5. Peer Validation Language (PVL)

### Definition

PVL is the set of constraints enforceable by all peers during op-level validation using only a closed, bounded, reconstructible validation context.

With descriptors in view, that means:

> PVL is the integrity-local subset of descriptor-driven validation plus verification of proof-carrying validation evidence.

### Properties

PVL is:

- deterministic
- bounded
- local to a closed validation context
- independent of coordinator/runtime services
- fixed per DHT for any schema/descriptor knowledge it depends on

### Includes

PVL always includes storage-envelope and receipt checks such as:

- key rules
- lifecycle transitions
- HolonNode and SmartLink shape
- descriptor identity field shape
- validation receipt digest/signature consistency

PVL may include artifact-backed or explicitly carried descriptor-backed rules such as:

- type conformance
- property presence / requiredness
- value type validation
- enum membership
- relationship typing
- bounded cardinality
- referential integrity

These rules may run in PVL only when their descriptor context is fixed in the DNA, compiled into an integrity-local artifact, or explicitly carried in the op's bounded validation context. PVL must not fetch or interpret the live descriptor graph through coordinator services.

It may also include transaction-scoped checks if:

- the relevant holons are explicitly enumerated
- the evaluation remains bounded and reconstructible

### Excludes

PVL cannot include:

- unbounded graph traversal
- live descriptor graph resolution
- reference-layer or coordinator-cache access
- dynamic rule dispatch
- Dance-based validation rule execution
- runtime plugin/module loading
- open-world query evaluation
- temporal logic
- external state dependencies
- agreement interpretation
- global uniqueness
- descriptor evaluation that depends on non-reconstructible runtime context

---

## 6. Nursery as the Anti-Gravity Layer

The Nursery exists to absorb the validation work that dependency gravity rejects from integrity.

### Role

The Nursery is the bounded pre-commit environment where MAP can safely evaluate richer descriptor-backed rules.

It enables:

- multi-holon validation
- descriptor graph traversal and inheritance flattening
- transaction-scoped invariants
- post-transaction cardinality checks
- coordinated updates
- snapshot-based duplicate detection
- command/dance precondition checks where bounded and meaningful
- descriptor-backed query/filter style checks over transaction plus snapshot
- dynamic validation rule execution where the rule engine is available in coordinator/runtime context
- generation of validation receipts bound to committed data

### Constraint

Nursery validation is:

- locally consistent
- snapshot-dependent
- not globally authoritative

### Outcome

The Nursery reduces invalid writes, but it does not eliminate races, ambiguity, or global conflicts.

When Nursery validation is stronger than what PVL can re-execute, it should produce proof-carrying evidence instead of pulling its dependencies downward. A validation receipt can bind the validated entry/link/transaction digest to the descriptor identity, rule-set identity, validation engine identity, outcome, validator identity, and signature. Integrity can verify that evidence locally without resolving descriptors or executing dynamic rules.

A receipt proves binding and provenance, not universal trust. If integrity treats a receipt as a hard gate, the acceptable validator, rule-set, or engine identity must itself be fixed or reconstructible inside the PVL boundary.

---

## 7. Query, Commands, and Dances

The descriptor design broadens the dependency-gravity discussion beyond classic "validation code."

### 7.1 Query Operators

Query operators and validation operators increasingly share the same value semantics.

That is desirable, but it has a boundary:

- descriptor-owned operator semantics are fine
- open-world query execution is not automatically PVL-safe

Closed-world filtering over explicit transaction data may be acceptable in bounded contexts. Open-ended graph querying is not.

### 7.2 Commands

Commands should gain descriptor ownership rather than remain freestanding dispatch targets.

But command execution often bundles:

- lookup
- authorization
- preconditions
- side effects
- multi-holon coordination

Only a narrow structural subset of command-related checks belongs in PVL. Most meaningful command validation belongs in Nursery or above.

### 7.3 Dances

Dances are even less likely than commands to fit into PVL because they are intended to be domain-extensible and behavior-rich.

Descriptor-afforded dance lookup is structurally useful.

Dance execution semantics are usually coordinator- or social-layer concerns unless reduced to a bounded structural check. Validation Dances in particular must not become an integrity-zome dependency; their outcomes can be pre-commit validation inputs and, where useful, validation receipts.

---

## 8. Uniqueness as a Case Study

Uniqueness still illustrates dependency gravity clearly.

### Structural Layer (PVL)

- enforce claim structure
- ensure deterministic key derivation
- allow multiple claims
- reject malformed claim shapes

### Index Layer (Paths + Links)

- deterministic path per normalized value
- bounded conflict surface
- efficient conflict discovery

Absence of links is not proof of uniqueness.

### Nursery Layer

- best-effort duplicate detection
- transaction-scoped uniqueness heuristics
- prevention of obvious local conflicts

### Trust / Social Layers

- conflict resolution
- agreement enforcement
- canonical claim establishment

### Conclusion

> Uniqueness is not a peer-enforceable storage invariant.  
> It is a coordination property evaluated across layers.

---

## 9. Transaction vs Op Validation

Holochain validates at op granularity.  
MAP semantics often live at transaction granularity.

That mismatch becomes more visible once descriptors become the semantic home of rules.

The correct response is not to force transaction semantics into integrity. It is:

- use PVL for local structure, fixed artifacts, and receipt verification
- use Nursery for bounded transaction semantics and descriptor/rule execution
- use higher layers for open-world semantics

Key rule:

> A rule may be enforced in PVL only if every validator can evaluate it from the op plus a bounded, explicitly defined context.

If not, dependency gravity has identified a higher-layer concern.

---

## 10. Final Model

Dependency gravity now defines the execution boundary for descriptor-driven semantics.

- descriptors define the rules
- PVL defines the integrity-local execution and verification boundary
- Nursery handles bounded pre-commit validation and receipt generation
- trust and attestation handle open-world meaning

This keeps the architecture stable because:

- PVL remains minimal, safe, and reproducible
- descriptors remain the semantic source of truth
- queries, commands, and dances do not need parallel rule systems
- dynamic validation does not force DHT churn by expanding the integrity zome
- richer validation complexity is absorbed upward instead of destabilizing integrity

---

## 11. Closing Statement

Dependency gravity is not an obstacle to descriptor-driven MAP.

It is the mechanism that tells us where descriptor-defined rules can safely run.

If a rule fits inside an integrity-local, bounded, reconstructible context, it may live in PVL.

If it can be checked before commit but not re-executed by peers, MAP should bind the result to the commit with local verification evidence.

If neither is true, MAP should move the rule outward rather than pulling the runtime inward.
