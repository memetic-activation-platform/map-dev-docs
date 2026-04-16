# 🧾 MAP Transaction Model Specification — v2

This document defines the Transaction Model used in the Memetic Activation Platform (MAP), refined to incorporate:

- the layered validation architecture (PVL, Nursery, Trust Channels, Attestations)
- the dependency gravity boundary
- the distinction between structural, semantic, and social validity
- conflict detection via deterministic indexing (paths + links)
- the limits of local validation under eventual consistency

This version preserves the original model while clarifying scope, guarantees, and boundaries.

---

## 🔹 Overview: What Is a Transaction in MAP?

A **Transaction** in MAP is a semantically meaningful, multi-operation commit unit that:

- Encapsulates one or more staged holon or relationship updates.
- Records validation outcomes, operation logs, and possible compensating operations.
- Results in a locally validated commit, a failed transaction, or a rollback.

Transactions serve as:

- A **logical unit of change** (semantic granularity within an Agent),
- A **validation boundary** (closed, transaction-scoped context),
- A **record of validation outcomes and intent**.

---

## 🔑 Important Clarification

> A Transaction guarantees **local semantic coherence**, not global correctness.

It does NOT guarantee:

- global uniqueness
- absence of concurrent conflicting writes
- agreement conformance across agents

---

## 🧱 Structure of a Transaction Holon

```
{
  "type": "#TransactionType",
  "properties": {
    "transaction_id": "txn:2025-08-19T17:54Z:87af0",
    "timestamp": "2025-08-19T17:54:33Z",
    "initiated_by": "Agent:alice",
    "final_state": "CommittedWithWarnings"
  },
  "relationships": {
    "Updated": [ "$ref": "Holon:book:MAP" ],
    "HasValidationResult": [ "$ref": "#validation-too-many-tags" ],
    "HasOperationLog": [ "$ref": "#op-1", "$ref": "#op-2" ],
    "Compensates": [ "$ref": "#Transaction:txn-original" ]
  }
}
```

---

### Key Properties

| Property         | Description |
|------------------|------------|
| `transaction_id` | Unique identifier |
| `initiated_by`   | Agent initiating the transaction |
| `final_state`    | `Validated`, `Committed`, `CommittedWithWarnings`, `Failed`, `RolledBack` |
| `timestamp`      | Creation time |

---

### Key Relationships

| Relationship          | Target           | Purpose |
|-----------------------|------------------|--------|
| `Updated`             | Holon(s)         | All affected holons |
| `HasValidationResult` | ValidationResult | Records validation outcomes |
| `HasOperationLog`     | OperationLog     | Fine-grained command history |
| `Compensates`         | Transaction      | Links rollback / corrective transaction |

---

## 🧠 Transaction Context and the Nursery

### 🌱 The Nursery

The **Nursery** is a transient, in-memory projection of the transaction scope.

It acts as:

- a **materialized read model**
- a **closed validation environment**
- the **primary locus of semantic validation**

---

### 🪵 Nursery Responsibilities

- maintain a fully materialized view of staged changes
- allow ergonomic mutation APIs
- support undo/redo via operation logs
- evaluate validation rules before commit

---

### ⚠️ Constraint

The Nursery operates on:

- a **partial, local snapshot** of the DHT
- no guarantee of global visibility

Therefore:

> Nursery validation is strong but not globally authoritative.

---

## 📚 Best Practices Integrated into the Transaction Model

### ✅ Event Sourcing Practices

| Event Sourced Concept           | MAP Equivalent |
|---------------------------------|---------------|
| Event stream per aggregate      | `StagedHolon` per entry |
| Append-only log                 | `OperationLog` |
| Snapshot                        | Nursery projection |
| Sagas                           | `Transaction` + `Compensates` |
| Read model                      | Nursery |

---

### Key Takeaway

The Transaction is the **bounded semantic unit**, while the Nursery is the **projection layer** enabling validation.

---

## 🌀 Holochain Comparisons (Refined)

| Holochain Concept                  | MAP Layer |
|------------------------------------|----------|
| Entry / link ops                   | Holon persistence |
| DHT validation callbacks           | PVL (integrity layer) |
| Action graph                       | Versioning via hashes |
| Branching updates                  | MVCC-style divergence |

---

### Updated Key Takeaway

MAP does NOT extend Holochain validation into full semantic reproduction.

Instead:

- **Holochain integrity validation → PVL (structural only)**
- **MAP transaction validation → Nursery (semantic, local)**

---

## 🔁 CRDT Perspective (Refined)

| CRDT Trait                    | MAP Position |
|-------------------------------|-------------|
| Automatic merge               | ❌ No |
| Convergence guarantee         | Conditional |
| Conflict handling             | Explicit and semantic |
| Merge logic                   | Agreement + application |

---

### Key Takeaway

MAP prioritizes:

> **semantic correctness over automatic convergence**

---

## ⚙️ MVCC in MAP

MAP uses MVCC:

- multiple concurrent versions allowed
- no write blocking
- conflicts detected later
- resolution is semantic

---

### Important Refinement

> MVCC enables divergence; it does not guarantee correctness.

---

## 🧪 Validation Model

### 🔹 Structural Validation (PVL)

Performed in integrity:

- type correctness
- property validation
- relationship constraints
- lifecycle rules

---

### 🔹 Transaction Validation (Nursery)

Performed pre-commit:

- multi-holon invariants
- cardinality constraints
- referential coherence
- derived consistency

---

### 🔹 Validation Categories

#### Required (Hard Fail)

- transaction-internal invariants
- bounded cardinality
- required claim presence
- direct reference consistency

---

#### Optional (Warning)

- snapshot-based duplicate detection
- advisory rules
- quality checks

---

#### Deferred

- global uniqueness
- cross-agent semantics
- agreement constraints

---

### 🔹 Validation Outcomes

- Fail → abort
- Warn → commit with warnings
- Defer → commit, unresolved

---

## 🔗 Uniqueness and Claims

### 🔹 Claim Holon Pattern

Uniqueness is represented via **Claim Holons**:

- deterministic key = hash(normalized_value)
- linked to claimant

---

### 🔹 Path Index

Paths act as deterministic indexes:

claims.<domain>.<hash>

Links:

Path → ClaimHolon

---

### 🔹 Conflict Set

All claims linked to the same path form a conflict set.

---

### 🔹 Critical Insight

> Absence of conflict ≠ uniqueness

---

### 🔹 Transaction Role

Transactions:

- check local snapshot
- prevent obvious duplicates
- cannot guarantee global uniqueness

---

## ⚠️ Conflict Detection

Conflicts are detected:

- during Nursery validation (best effort)
- on DHT integration
- during reads

Detection rule:

multiple links from same path → conflict

---

### Properties

- eventual
- partial
- monotonic

---

## 🔔 Conflict Signaling

Conflicts may be recorded via:

- `ConflictsWith` relationships
- conflict holons
- validation results
- attestations

---

## 🔁 Conflict Resolution

Occurs outside transactions:

- follow-up transactions
- trust channel enforcement
- attestation consensus

---

## 📜 Agreement Scope vs Transaction Scope

### 🔹 Key Distinction

| Concept | Scope |
|--------|------|
| Transaction | Intra-agent |
| Agreement | Inter-agent |

---

### 🔹 Implication

Transaction validation does NOT enforce:

- agreement rules
- inter-agent policies

Those belong to:

- Trust Channels
- Attestation layer

---

## 🧾 Validation Results (Refined)

Validation results should distinguish:

- structural (PVL)
- semantic (Nursery)
- deferred
- social (attestation-derived)

---

## 🧩 Summary

MAP Transactions provide:

- bounded semantic units of change
- strong local validation via Nursery
- explicit validation records
- MVCC-based divergence
- compatibility with eventual consistency

---

## 🧭 Final Principles

- Transactions ensure **local coherence**
- Integrity ensures **structural correctness**
- Trust Channels enforce **agreements**
- Attestations establish **truth**
- Conflicts are **detected, not prevented**

---

## 🧠 Closing Statement

MAP Transactions allow Agents to construct coherent local state,  
while the broader system ensures that this state can be challenged,  
validated, and reconciled through decentralized interaction and shared meaning.