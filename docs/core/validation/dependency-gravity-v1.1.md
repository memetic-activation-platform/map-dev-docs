# Dependency Gravity (Reframed) — v2

## 1. Purpose

This document reframes **dependency gravity** in light of the evolved MAP validation architecture.

Originally, dependency gravity described the tendency for validation logic to pull increasingly rich runtime dependencies (reference layer, graph traversal, coordinator services) into the integrity layer, creating architectural instability.

Through this design exploration, we arrive at a clearer and more stable conclusion:

> **Dependency gravity is not merely a problem to be mitigated — it is a signal that validation concerns belong in different architectural layers.**

---

## 2. Core Insight

### Original Framing

Dependency gravity arises when:

- validation requires descriptor resolution
- descriptor resolution requires graph traversal
- graph traversal requires reference-layer services
- reference-layer services require coordinator-level infrastructure

Result:

> The integrity layer becomes entangled with runtime concerns it cannot safely support.

---

### Revised Framing

> Dependency gravity is the consequence of attempting to enforce **open-world, semantic constraints** within a **closed, bounded, deterministic validation environment**.

---

## 3. Resolution: Layered Validation Model

The resolution is not to eliminate dependency gravity, but to **respect its boundary**.

MAP adopts a layered validation model:

| Layer | Responsibility | Validation Type |
|------|----------------|----------------|
| Integrity (DHT) | Structural integrity | Peer-reproducible (PVL) |
| Nursery (Coordinator) | Transaction coherence | Local, pre-commit |
| Trust Channel | Agreement enforcement | Inter-agent |
| Attestation | Social validation | Post-commit |

---

## 4. Peer Validation Language (PVL)

### Definition

> The Peer Validation Language (PVL) is the set of Core Schema constraints enforceable by all peers during op-level validation.

### Properties

PVL is:

- deterministic
- bounded
- local (closed-world)
- independent of runtime services
- fixed per DHT (via Core Schema)

### Expressiveness

PVL includes:

- type conformance
- property presence
- value type validation
- enum membership
- key rules
- relationship typing
- bounded cardinality
- referential integrity
- lifecycle transitions

PVL may also include:

- **transaction-scoped constraints**, if:
    - the transaction explicitly enumerates all relevant holons
    - validation is bounded and reconstructible

---

### Boundary

> PVL is limited to constraints that can be evaluated over a **closed, explicitly defined set of data**.

PVL cannot include:

- unbounded graph traversal
- dynamic rule dispatch
- temporal logic
- external state dependencies
- open-world queries
- agreement interpretation

---

## 5. Dependency Gravity Reinterpreted

### Key Principle

> **Dependency gravity occurs when a validation rule requires data or computation outside PVL’s closed-world boundary.**

Instead of pulling those dependencies inward:

> **We move the rule outward to the appropriate layer.**

---

## 6. Nursery: The Anti-Gravity Layer

The Nursery exists to absorb validation complexity that cannot safely exist in integrity.

### Role

> The Nursery is the only environment where full transaction context is available.

It enables:

- multi-holon validation
- transaction-scoped invariants
- coordinated updates
- snapshot-based checks
- semantic rule evaluation

---

### Constraint

Nursery validation is:

- locally consistent
- snapshot-dependent
- not globally authoritative

---

### Outcome

> The Nursery reduces invalid writes but does not eliminate global conflicts.

---

## 7. Uniqueness as a Case Study

Uniqueness illustrates dependency gravity clearly.

### Structural Layer (PVL)

- enforce claim structure
- ensure deterministic key derivation
- allow multiple claims
- no global exclusivity enforcement

---

### Index Layer (Paths + Links)

- deterministic path per normalized value
- bounded conflict surface
- efficient conflict discovery

> Absence of links ≠ uniqueness

---

### Nursery Layer

- best-effort duplicate detection
- transaction-scoped uniqueness enforcement
- prevent obvious conflicts

---

### Trust / Social Layers

- resolve conflicts
- enforce agreements
- establish canonical claims

---

### Conclusion

> Uniqueness is not a storage invariant.  
> It is a coordination property.

---

## 8. Conflict Model

### Detection

Conflicts are detected when:

- multiple claims exist under the same deterministic path

Detection is:

- eventual
- partial
- monotonic

---

### Signaling

Conflicts may be signaled via:

- relationships (`ConflictsWith`)
- conflict holons
- validation results
- attestations

---

### Resolution

Occurs via:

- transactions
- trust channels
- attestation consensus

---

## 9. Transaction vs Op Validation

### Problem

Holochain validates at **op granularity**  
MAP semantics exist at **transaction granularity**

---

### Solution

> Use the Nursery for transaction validation  
> Use PVL for structural validation

---

### Key Rule

> A constraint may be enforced in PVL only if it can be evaluated from:
- the op
- the transaction (if explicitly referenced)
- bounded local context

---

## 10. Validation Classification

### Required (Hard Fail — Nursery)

- transaction-internal invariants
- bounded cardinality after transaction
- direct referential consistency
- required claim presence

---

### Optional (Warning — Nursery)

- likely duplicates (snapshot-based)
- advisory semantic checks
- quality rules

---

### Deferred (Post-commit)

- global uniqueness
- cross-agent semantics
- agreement-level rules
- open-world constraints

---

## 11. Final Principle

> Dependency gravity defines the boundary of peer-reproducible validation.

Instead of resisting it:

- PVL defines the **closed-world boundary**
- Nursery handles **bounded open-world approximation**
- Trust Channels handle **inter-agent semantics**
- Attestations handle **social truth**

---

## 12. Architectural Summary

- PVL remains minimal, stable, and safe
- Nursery absorbs semantic complexity pre-write
- DHT ensures structural integrity only
- Paths + Links bound conflict detection
- Conflicts are inevitable but manageable
- Resolution is external to storage

---

## 13. Guiding Rule

> If a validation rule requires knowledge beyond a bounded, explicitly defined context, it does not belong in PVL.

---

## 14. Closing Insight

> **MAP is structurally consistent, but semantically pluralistic.**

Dependency gravity is the force that keeps those two truths properly separated.