# 🧾 MAP Transaction Model Specification

This document proposes a design for a Transaction Model used in the Memetic Activation Platform (MAP), grounding it in MAP’s architectural principles and comparing it to event sourcing, Holochain, and CRDT systems.

---

## 🔹 Overview: What Is a Transaction in MAP?

A **Transaction** in MAP is a semantically meaningful, multi-operation commit unit that:

- Encapsulates one or more staged holon or relationship updates.
- Records validation outcomes, operation logs, and possible compensating operations.
- Results in either a validated commit, an invalid provisional state, or a rollback.

Transactions serve both as:
- A **logical unit of change** (semantic granularity),
- And a **backbone for undo, validation, and resolution semantics**.

---

## 🧱 Structure of a Transaction Holon

```
{
  "type": "#TransactionType",
  "properties": {
    "transaction_id": "txn:2025-08-19T17:54Z:87af0",
    "timestamp": "2025-08-19T17:54:33Z",
    "initiated_by": "Agent:alice",
    "final_state": "CommittedWithWarnings"  // or "Validated", "Failed", "RolledBack"
  },
  "relationships": {
    "Updated": [ "$ref": "Holon:book:MAP" ],
    "HasValidationResult": [ "$ref": "#validation-too-many-tags" ],
    "HasOperationLog": [ "$ref": "#op-1", "$ref": "#op-2" ],
    "Compensates": [ "$ref": "#Transaction:txn-original" ]
  }
}
```

### Key Properties

| Property         | Description                                                              |
|------------------|--------------------------------------------------------------------------|
| `transaction_id` | Unique identifier for the transaction.                                   |
| `initiated_by`   | Agent or process that initiated the commit.                              |
| `final_state`    | Enum: `Validated`, `CommittedWithWarnings`, `Failed`, `RolledBack`, etc. |
| `timestamp`      | When the transaction was created.                                        |

### Key Relationships

| Relationship          | Target           | Purpose                                                 |
|-----------------------|------------------|---------------------------------------------------------|
| `Updated`             | Holon(s)         | All holons affected in the transaction.                 |
| `HasValidationResult` | ValidationResult | Records rule checks applied post-commit.                |
| `HasOperationLog`     | OperationLog     | Stores user-facing or compensatory operation sequences. |
| `Compensates`         | Transaction      | Links to the prior transaction being rolled back.       |

---


## 📚 Best Practices Integrated into the Transaction Model

### ✅ Event Sourcing Practices

| Event Sourced Concept           | MAP Equivalent                                                                                    |
|---------------------------------|---------------------------------------------------------------------------------------------------|
| Event stream per aggregate      | `StagedHolon` per entry                                                                           |
| Append-only log                 | `OperationLog` attached to Transaction                                                            |
| Optimistic concurrency (OCC)    | OCC applied at commit time using version check                                                    |
| Snapshot for materialized state | Materialized `StagedHolon` represents final state                                                 |
| Sagas for long transactions     | `Transaction` + `Compensates` + Agreement policies                                                |
| **Read model projection**       | **Nursery maintains a transient, fully materialized view of all holons in the Transaction scope** |

### Key Takeaway
MAP treats the Transaction Holon as the **bounded event stream unit**, aggregating property/relationship changes into a single validation and commit phase. The **Nursery** functions as an ephemeral **read model** or **projection layer**, allowing efficient access to the current state during staged editing and commit processing — much like a projection in traditional event-sourced systems.

---

## 🌀 Holochain Comparisons

| Holochain Concept                  | MAP Layer                                                     |
|------------------------------------|---------------------------------------------------------------|
| `create_entry`, `update_entry` ops | Underlying backing store for Holons                           |
| Action Hash graph                  | Reflected in `SemanticVersion` and `Updated` links            |
| DHT validation callbacks           | Wrapped into MAP’s third-pass commit validation               |
| Branching via multiple updates     | Tracked and resolved via `ValidationResult` + `ConflictsWith` |

### Key Takeaway
MAP extends Holochain’s “validation-on-each-op” model by layering **transaction-level, type-aware, and agreement-aware validation** atop the raw chain mechanics.

---

## 🔁 CRDT Perspective

| CRDT Trait                    | MAP Position                                                   |
|-------------------------------|----------------------------------------------------------------|
| Automatic conflict resolution | Not automatic — requires rule- or agreement-based merge logic  |
| Merge-on-receipt              | Delayed, semantic resolution during validation or review       |
| Convergence guarantee         | Conditional — governed by AgreementScope and policies          |
| Operation deltas              | Represented via fine-grained `OperationLog` commands           |
| Composability                 | Holon structure is the merge target, not the CRDT state itself |

### Key Takeaway
MAP’s Transaction Model **prioritizes semantic correctness over blind convergence**. It supports CRDT-style operational tracking but rejects automatic merging unless declared via policy.

---

## 🧠 Strategic Benefits of This Model

- Enables **fine-grained UX undo** without polluting the DHT.
- Supports **event sourcing patterns** while maintaining a clean, materialized model.
- Adds semantic structure on top of **Holochain’s low-level operation model**.
- Leaves room for **application- and agreement-scoped conflict resolution**, aligning with MAP’s governance-first design.

---

## 📌 Open Extensions (Future)

- `ResolutionPolicy` holons linked to `AgreementScope` and `ApplicationScope`
- `MergeResolution` holons for explicit fork merging
- Automatic detection of unresolved forks and triggering of merge workflows
- Parallel Transaction Streams per AgreementSpace

# Comparison to Event-Sourced Systems, Holochain, CRDTs, and MVCC_

---

## 🌱 The MAP Transaction Model

In the Memetic Activation Platform (MAP), every set of proposed changes to holons is staged in a local **Nursery** before being committed. A **Transaction** holon represents this unit of change. It is created at commit time and holds:

- Relationships to a set of **ValidationResult** holons
- Links to all **updated Holons** (via those results)
- State transitions such as `Unvalidated` → `Validated` → `Committed` or `RolledBack`
- Optional logging of **fine-grained operations** to support undo/redo and compensating transactions

The MAP’s layered design separates **validation** (ensuring semantic correctness and consistency) from **persistence** (recording changes in the source of truth). Validation is performed before commit using rules scoped by both application logic and shared agreements (e.g. cardinality checks, role consistency, semantic integrity, etc.).

---

## 🪵 Nursery as a Read Model (Projection Layer)

In Event Sourced systems, **projections** (also called read models) are derived views of the event stream, optimized for user interaction. The MAP **Nursery** serves this role during a transaction:

- It maintains a **materialized view** of holons after every staged change.
- Ergonomic client APIs (e.g. `with_property`, `add_relationship`) mutate this staged state.
- These lightweight operations can be **logged as Commands**, enabling undo/redo support.
- Only at commit time is the transaction finalized and written as an immutable update.

---

## 🔁 Comparison to Event Sourcing Systems

| Aspect                     | Event Sourcing                      | MAP Transaction Model                       |
|----------------------------|-------------------------------------|---------------------------------------------|
| Core Persistence Model     | Append-only event log               | Append-only holon updates (via DHT)         |
| Aggregates                 | Derived from replaying events       | Materialized holons in nursery projections  |
| Validation                 | Done before/after event persistence | Done in the nursery, before commit          |
| Transaction Representation | Often lacks explicit transaction    | Explicit `Transaction` holon                |
| Undo/Redo                  | By reversing events or snapshots    | Via logged staged operations in nursery     |
| Compensating Transactions  | Application-defined                 | Tracked via new Transaction holons          |
| Concurrency Control        | Typically OCC or snapshot isolation | MVCC + Agreement-Scoped Conflict Resolution |

---

## ⚙️ MVCC in MAP vs Other Concurrency Strategies

### ✅ MAP uses Multi-Version Concurrency Control (MVCC)

- Each holon update produces a new immutable version
- Writers do not block each other — they create **parallel branches**
- Version history is preserved and traceable
- Conflict detection is **deferred**, and resolution is semantic (not structural)

### ❌ Not Optimistic Concurrency Control (OCC)

- OCC would reject commits if the read version was outdated
- MAP instead accepts the write, creating a new fork
- This **branching behavior** supports collaborative divergence before reconciliation

---

## 🧠 Conflict Resolution Strategies: CRDTs vs Holochain vs MAP

| Feature                | CRDTs                                    | Holochain                            | MAP                                           |
|------------------------|------------------------------------------|--------------------------------------|-----------------------------------------------|
| Conflict-Free?         | Claims "conflict-free" via auto-merge    | Leaves resolution to the application | Explicitly supports semantic conflicts        |
| Merge Strategy         | Structural (e.g. last-write-wins, ORSet) | None by default                      | Application + Agreement-Scoped Semantics      |
| Determinism            | Always converges                         | No built-in convergence              | Resolution logic is pluggable per domain      |
| Lost Updates Possible? | Yes (e.g. in LWW)                        | Yes                                  | Yes — but tracked and resolvable              |
| Undo Support           | Limited                                  | Manual                               | Fine-grained undo via operation log           |
| Update Representation  | Per-property, tombstones, deltas         | Entry-level action history           | Per-holon, with ergonomic staging granularity |
| Versioning Model       | Conflict-resolution per data type        | Full action chain (via hashes)       | Holon-level branches tracked via hashes       |

> 🔍 Note: While CRDTs automatically resolve structural conflicts, they often do so at the cost of **semantic predictability**. MAP preserves all branches and delegates resolution to **shared agreements** and **application logic**.

---

## 📜 Agreement Scopes and Application Scopes

To support meaningful conflict resolution:

- **Agreement Scope**: Specifies the **participants** and **rules** (e.g. communities, working groups) that govern semantic resolution.
- **Application Scope**: Defines the **data boundaries** (e.g. all holons in a shared Space) to which resolution applies.

Resolution logic is therefore anchored in both the **social commitments** and the **data model** — ensuring that divergent updates are reconciled in a trustworthy, context-aware way.

---

## 🧩 Summary

MAP’s Transaction model offers:

- A **clear separation** of staging, validation, and commit phases
- Fine-grained operation tracking for undo/redo and compensation
- Explicit **MVCC-style version branching** with later reconciliation
- A hybrid model blending **Event Sourcing**, **Holochain DHT consistency**, and **semantic conflict resolution** that goes beyond CRDTs

This design supports both a robust technical foundation and the social contracts required for trustworthy, collaborative data stewardship.