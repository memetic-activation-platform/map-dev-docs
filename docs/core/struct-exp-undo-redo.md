# MAP Core — Structural Pre-Commit Transaction Editing Model
## Structural Experience-Level Undo / Redo Specification

---

## 1. Purpose and Scope

This document specifies the **Structural Experience-Level Undo / Redo model for MAP Core** during pre-commit transaction editing.

This model applies only to:

- Human-initiated editing sessions
- Operations performed within an open Transaction
- Provisional (uncommitted) state

This model explicitly excludes:

- Domain-level undo after commit
- Inter-agent undo semantics
- Compensating operations across Trust Channels
- Undo history spanning transaction boundaries

Undo history is strictly **transaction-scoped** and is destroyed on commit or rollback.

---

## 2. Design Principles

The structural undo model is guided by the following principles:

1. **Human-first behavior** — Command-Z must feel predictable, immediate, and linear.
2. **Simplicity over optimization** — Avoid premature delta, replay, or compaction mechanisms.
3. **Transaction scope only** — Undo never spans transactions.
4. **Holon-only storage** — All persisted structures are representable as Holons and HolonRelationships.
5. **Openness preservation** — Command providers are not required to implement custom undo logic.
6. **Deterministic restoration** — Undo restores prior transaction state structurally, not semantically.

---

## 3. Core Model

### 3.1 Transaction as Mutable Graph

An open Transaction represents:

- A mutable staged holon graph
- Transient holons
- A strictly linear structural history

Undo and redo operate by restoring prior structural states of this graph.

---

### 3.2 Command (Structural Unit)

A Command:

- Executes atomically (all-or-nothing)
- Mutates staged and/or transient holons
- On success, produces a structural checkpoint
- On failure, produces no observable state change and no history entry

Command providers are not required to supply undo or redo logic.

Undo is handled exclusively by structural restoration.

---

### 3.3 Structural Checkpoints

After each successful undoable Command:

- MAP Core captures a full structural snapshot of the Transaction context, including:
    - All staged holons
    - All transient holons
    - Necessary transaction metadata
- The snapshot is pushed onto the undo stack
- The redo stack is cleared

Snapshots are opaque structural representations of the Transaction state.

---

## 4. Undo / Redo History Model

### 4.1 Linear History

The Transaction maintains:

- An Undo Stack of structural checkpoints
- A Redo Stack of structural checkpoints
- Optional Undo Markers (opaque positional delimiters)

History is:

- Strictly linear
- LIFO-based
- Non-branching
- Transaction-scoped

---

### 4.2 Undo Operation

`undo_last_command`:

- Fails if the undo stack is empty
- Restores the previous structural checkpoint
- Moves the current checkpoint to the redo stack

Undo is implemented purely as state restoration.

No command logic is executed during undo.

---

### 4.3 Redo Operation

`redo_last_command`:

- Fails if the redo stack is empty
- Restores the next structural checkpoint
- Moves the checkpoint back to the undo stack

Redo is implemented purely as state restoration.

---

### 4.4 Undo Markers

Undo Markers:

- Are inert positional delimiters
- May include metadata (ignored by Core)
- Are used only for navigation via marker_id
- Do not contain semantic meaning

Undo and redo operate strictly via LIFO traversal.

---

## 5. Command Metadata

Commands may optionally include metadata fields.

### 5.1 disable_undo

If `disable_undo = true`:

- No structural checkpoint is created
- The command cannot be undone
- Redo stack behavior remains consistent (cleared on success)

This is intended for:

- Bulk operations
- Regenerable imports
- Commands where structural snapshot is unnecessary

Crash recovery still persists the resulting Transaction state.

---

## 6. Crash Recovery

### 6.1 Recovery Model

During an open Transaction:

- The Transaction context (staged graph + undo/redo stacks) may be persisted locally.
- Persistence is local-only and not DHT-visible.
- Persistence may occur asynchronously.

On restart:

- The latest persisted Transaction snapshot is loaded.
- The staged graph is restored.
- Undo and redo stacks are restored.
- Editing resumes seamlessly.

---

### 6.2 Persistence Scope

Persisted snapshot includes:

- All staged holons
- All transient holons
- Undo stack
- Redo stack
- Marker positions
- Transaction metadata

Only one recovery snapshot per open Transaction is required.

Snapshots may overwrite prior persisted state.

---

### 6.3 Lifecycle

On `commit` or `rollback`:

- The in-memory Transaction context is destroyed.
- The persisted recovery snapshot is deleted.
- No undo history survives beyond transaction boundary.

Undo cannot span transactions.

---

## 7. Threading and Persistence

- Structural checkpoint creation occurs only after successful command completion.
- Persistence may be handled asynchronously in a separate thread.
- Persistence must reflect a fully consistent Transaction state.
- Partial command states must never be persisted.
- Recovery must load only the most recent consistent snapshot.

---

## 8. Holon-Only Representation

All persisted recovery state must be representable as:

- Holons
- HolonRelationships

Opaque structural snapshots may be serialized representations of holon subgraphs but must map to holon structures conceptually.

---

## 9. Loader and Bulk Operations

For large bulk commands (e.g., Holon Loader):

- `disable_undo` may be set initially.
- Structural snapshotting is not required for undo.
- Crash recovery may persist current staged state.
- Future versions may introduce custom undo strategies, but none are required in this model.

---

## 10. Guarantees

MAP Core guarantees that:

- Undo and redo are strictly structural.
- Undo is deterministic and LIFO.
- Commands are all-or-nothing.
- No failed command produces history.
- Undo history exists only during an open Transaction.
- Crash recovery restores a consistent Transaction state.
- All undo history is destroyed on commit or rollback.

---

## 11. Non-Goals

This model does not support:

- Semantic command-specific undo logic
- Replay-based undo
- Delta-based checkpointing
- Cross-transaction undo
- Domain-level reversal after commit
- Trust Channel undo semantics

Such capabilities may be introduced in future specifications but are not part of this structural model.

---

## 12. Summary

The Structural Experience-Level Undo / Redo model treats a Transaction as a mutable graph with a linear time axis.

Each successful Command advances the graph and captures a structural checkpoint.

Undo and redo move backward and forward along this structural history by restoring prior graph states.

Crash recovery persists the Transaction state locally and is cleared entirely upon commit or rollback.

This model prioritizes:

- Human predictability
- Architectural simplicity
- Openness of the Commons
- Deterministic behavior
- Minimal implementation complexity