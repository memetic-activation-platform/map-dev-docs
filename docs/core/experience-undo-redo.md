# MAP Core — Pre-Commit Transaction Editing Model
## Undo / Redo Design Specification (Experience-Level Undo)

**Status:** Draft (Converged)  
**Scope:** **MAP Core Pre-Commit Transaction Editing Model**  
**Audience:** MAP Core developers, SDK implementers  
**Non-goals:** Domain-level (post-commit) undo, SDK ergonomics, UI behavior, Trust Channel semantics

---

## 1. Purpose and Scope

This document specifies the **Undo / Redo model for MAP Core during pre-commit transaction editing**, also referred to as **Experience-Level Undo**.

This model applies **only** to:

- Human-driven editing sessions
- Operations performed within an **open Transaction**
- Provisional (uncommitted) state

This document **explicitly excludes**:

- Domain-level undo after commit
- Inter-agent undo semantics
- Compensating operations across Trust Channels
- Long-lived or persisted undo history

> **Important distinction:**  
> Pre-commit undo is an *editing capability*.  
> Post-commit reversal is a *domain-level concern* and, if required, must be modeled explicitly (e.g., via compensating Holochain operations). That design space is intentionally out of scope here.

---

## 2. Core Concepts

### 2.1 Transaction

A **Transaction** is the sole execution context for experience-level undoable work.

- Undo/Redo exists **only** while a transaction is open
- The transaction owns:
    - all provisional holon state
    - the complete undo/redo history
- On `commit` or `rollback`, the transaction and its entire undo history are discarded

Undo history is **ephemeral** and **never persisted**.

---

### 2.2 Command (Smallest Undoable Unit)

A **Command** is the **smallest undoable and redoable unit** in MAP Core.

Properties:

- A command may perform multiple internal mutations
- A command executes **all-or-nothing**
- A successfully completed command produces **exactly one command edit record**
- A failed command produces:
    - no observable state change
    - no undo or redo capability

Undo and redo operate **only at command granularity**.

---

### 2.3 Undo Markers

An **Undo Marker** is an **opaque, transaction-scoped positional terminator** in the undo log.

Properties:

- Created explicitly by the experience layer (e.g. TypeScript SDK)
- May carry optional metadata (e.g. a human-readable label)
- Metadata is never interpreted by MAP Core
- Markers are inert and non-semantic
- Markers are strictly ordered by position in the undo log

Markers exist solely to delimit **lists of undoable commands** for human navigation.

---

## 3. Undo / Redo History Model

### 3.1 Linear History

The transaction maintains a **strictly linear history** consisting of:

- Undo Markers
- Command Edit Records

There is:

- no branching
- no random access
- no persistence
- no replay across sessions

---

### 3.2 Command Edit Records

For each successfully completed command, the command provider supplies a **Command Edit Record**.

Conceptually, a command edit record provides two opaque capabilities:

- **Undo capability** — reverses the effects of the command
- **Redo capability** — reapplies the effects of the command

MAP Core treats command edit records as opaque, atomic units.

> **Important:**  
> MAP Core does **not** assume that redo can be derived from undo.  
> Undo and redo are **peer responsibilities** supplied by the command provider.

---

### 3.3 Undo Stack and Redo Stack

Conceptually, the transaction maintains:

- an **Undo Stack** of completed command edit records
- a **Redo Stack** of undone command edit records

Undo and redo move command edit records between these stacks.

Markers remain fixed as positional references and are never undone or redone.

---

## 4. Command Execution and Reversibility Responsibilities

### 4.1 All-or-Nothing Command Requirement (Normative)

Every command executed within a transaction **must be all-or-nothing with respect to undoability**.

This is a **behavioral requirement**, not an implementation prescription.

Specifically:

- A successfully completed command **must be fully reversible** as a single undo step and fully re-applicable as a single redo step.
- A failed command **must not produce any observable state change** and **must not produce a command edit record**.
- Undo and redo operate **only at command granularity**.

MAP Core relies on this guarantee to provide correct undo/redo orchestration.

---

### 4.2 Responsibility for Undo and Redo Implementation

Responsibility for implementing reversible command behavior lies with the **command provider** (including Dance providers).

MAP Core **does not prescribe** how undo or redo capabilities are implemented.

Valid implementation strategies include, but are not limited to:

- Recording reversible deltas
- Capturing before/after snapshots
- Storing explicit inverse operations
- Replaying original command logic
- Using transactional sub-structures internal to the command

MAP Core treats each command as an opaque, atomic unit with respect to undo and redo.

---

### 4.3 Core Enforcement Role

MAP Core is responsible for:

- Defining command boundaries
- Enforcing all-or-nothing command semantics
- Managing undo and redo ordering
- Enforcing strict LIFO history
- Enforcing transaction scope and lifetime rules
- Clearing redo history on new successful commands

MAP Core is **not responsible** for:

- Inspecting internal command logic
- Deriving redo from undo
- Interpreting how reversibility is achieved
- Managing command-internal state

---

## 5. Undo Operations

The MAP Core may provide the following undo operations.

### 5.1 undo_last_command

Performs **LIFO reversal** of the most recent successfully completed command.

Rules:

- Fails if no undoable command exists
- Reverses exactly one command via its undo capability
- Moves the command edit record to the redo stack

---

### 5.2 undo_to_marker(marker_id)

Repeatedly performs `undo_last_command` until the specified marker position is reached.

Rules:

- `marker_id` is the only admissible selector
- Marker labels and metadata must not be used
- Undo proceeds strictly LIFO
- No skipping, batching, or reordering is permitted
- Fails if the marker is not reachable via undo

---

## 6. Redo Operations

Redo re-applies commands that were previously undone.

Redo is valid **only** while:

- the transaction is open
- no new successful command has been executed since the undo

---

### 6.1 redo_last_command

Reapplies the most recently undone command.

Rules:

- Fails if the redo stack is empty
- Reapplies the command’s redo capability
- Moves the command edit record back to the undo stack

Redo must be deterministic within the transaction. Failure indicates a violation of command guarantees and should invalidate the transaction.

---

### 6.2 redo_to_marker(marker_id)

Repeatedly performs `redo_last_command` until the specified marker position is reached.

Rules:

- Defined exclusively as repeated LIFO redo
- Must not bypass, batch, reorder, or selectively apply commands
- Fails if the marker is not reachable via redo
- Fails if redo history has been invalidated

---

### 6.3 Redo Invalidation

Any successful new command **clears the redo stack**.

This enforces a single linear history and prevents branching timelines.

---

## 7. Marker Invariants (Normative)

Undo markers are governed by the following invariants:

- Markers are opaque positional terminators
- The core must not interpret marker metadata
- The core must not infer marker placement
- The core must not provide undo or redo operations based on marker labels or semantics
- Only `marker_id` may be used to select undo/redo termination
- All undo and redo operations proceed exclusively via LIFO command reversal or reapplication

---

## 8. Lifetime and Scope

- Undo/Redo history exists only while a transaction is open
- The entire undo log (commands and markers) is discarded on:
    - `commit`
    - `rollback`
- Undo/Redo history is never persisted
- Undo/Redo history is never replayed across sessions

---

## 9. Relationship to Domain-Level Undo (Out of Scope)

This specification does **not** define domain-level undo after commit.

Post-commit reversal, if required, must be modeled explicitly at the domain layer, for example via:

- compensating Holochain operations
- inverse domain commands
- higher-level consistency protocols to ensure commit atomicity

Such mechanisms are **semantically and architecturally distinct** from experience-level undo and are intentionally excluded from this model.

---

## 10. Trust Channels and Agents

Experience-level undo applies **only** to human-agent editing sessions.

- Trust Channel–invoked dances do not promise undo
- Undo/Redo is not part of inter-agent contracts
- Any reversal across agents must be expressed as a new transaction with explicit domain semantics

---

## 11. Summary of Guarantees

MAP Core guarantees that:

- Every successful command supplies both undo and redo capabilities as a single atomic unit
- No failed command produces observable state or undo/redo history
- Undo and redo are strictly linear and deterministic
- Marker-based navigation is safe, opaque, and centrally enforced
- All undo/redo correctness is enforced once, in core
- Pre-commit editing undo is cleanly separated from domain-level rollback

---

**This specification defines the complete Pre-Commit Transaction Editing (Experience-Level Undo) model for MAP Core.**