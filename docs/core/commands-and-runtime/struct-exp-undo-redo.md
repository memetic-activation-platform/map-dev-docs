# MAP Core — Structural Pre-Commit Transaction Editing Model -- v1.2
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
2. **Experience-unit semantics** — Users undo named editing units, not internal implementation details.
3. **Simplicity over optimization** — Avoid premature delta, replay, or compaction mechanisms.
4. **Transaction scope only** — Undo never spans transactions.
5. **Holon-only storage** — All persisted structures are representable as Holons and HolonRelationships.
6. **Openness preservation** — Command providers are not required to implement custom undo logic.
7. **Deterministic restoration** — Undo restores prior transaction state structurally, not semantically.

---

## 3. Core Model

### 3.1 Transaction as Mutable Graph

An open Transaction represents:

- A mutable staged holon graph
- Transient holons
- A strictly linear editing history

Undo and redo operate by restoring prior structural states of this graph.

---

### 3.2 Command Execution

A Command:

- Executes atomically (all-or-nothing)
- Mutates staged and/or transient holons
- On failure, produces no observable state change and no history entry
- On success, may contribute to the currently active Experience Unit

Command providers are not required to supply undo or redo logic.

Undo is handled exclusively by structural restoration.

---

### 3.3 Experience Units

An **Experience Unit** is the human-facing undo/redo unit.

An Experience Unit:

- May contain one or more successfully executed Commands
- Exists entirely within a single open Transaction
- Is closed only when the experience layer signals a structural boundary
- May carry optional metadata such as:
  - `marker_id`
  - human-readable label
  - other opaque experience-layer metadata

MAP Core must not interpret Experience Unit metadata semantically.

The experience layer is responsible for determining Experience Unit boundaries.

A single user gesture may span multiple Commands and produce exactly one Experience Unit.

An Experience Unit becomes undoable only when it closes successfully and produces a Structural Checkpoint.

Commands accumulated in the currently open Experience Unit are not individually undoable until that Experience Unit is closed.

---

### 3.4 Structural Checkpoints

A **Structural Checkpoint** is an opaque snapshot of Transaction state captured at the close of an Experience Unit.

A Structural Checkpoint includes:

- All staged holons
- All transient holons
- Necessary transaction metadata
- Undo/redo history metadata required for restoration

A Structural Checkpoint is:

- A restore target
- Not itself the human-facing undoable item
- The resulting state after completion of an Experience Unit

If Experience Unit `EU_n` completes successfully and closes with a checkpoint, then:

- the checkpoint produced is the resulting state of `EU_n`
- undo of `EU_(n+1)` restores that checkpoint

Thus, Experience Units form the human-visible linear chain, while checkpoints provide the structural restore targets between them.

---

## 4. History Model

### 4.1 Linear History

Within an open Transaction, MAP Core maintains a strictly linear, non-branching history of:

- Structural Checkpoints
- Experience Units
- Optional Markers associated with Experience Units

History is:

- Strictly linear
- LIFO-based for undo/redo traversal
- Non-branching
- Transaction-scoped

---

### 4.2 Relationship Between Checkpoints and Experience Units

Conceptually, history forms a chain:

`Checkpoint_0 --(ExperienceUnit_1)--> Checkpoint_1 --(ExperienceUnit_2)--> Checkpoint_2 ...`

Where:

- `Checkpoint_0` is the initial Transaction state
- each Experience Unit transforms one checkpoint into the next
- undo of an Experience Unit restores the checkpoint immediately prior to that Experience Unit
- redo of an Experience Unit restores the checkpoint produced by that Experience Unit

UI history should therefore be expressed in terms of Experience Units, not checkpoints.

---

### 4.3 Markers

A **Marker** is an opaque identifier attached to an Experience Unit.

Properties:

- Created explicitly by the experience layer
- Bound when an Experience Unit closes successfully
- May carry optional metadata
- Metadata is never interpreted by MAP Core
- Markers are inert and non-semantic
- Markers are strictly ordered by position in the linear Experience Unit chain

Markers identify Experience Units, not checkpoints.

MAP Core must not infer marker placement.

MAP Core must not select undo/redo targets by marker label or metadata.

Only `marker_id` may be used to identify a marker.

---

## 5. Undo / Redo Operations

### 5.1 undo_last

`undo_last`:

- Fails if there is no undoable Experience Unit reachable from the current state
- Restores the checkpoint immediately preceding the most recent undoable Experience Unit
- Moves the undone Experience Unit into redo history, if redo remains valid

Undo is implemented purely as structural state restoration.

No command logic is executed during undo.

Previously created checkpoints remain reachable via undo even if later successful commands no longer produce new checkpoints.

If checkpoint creation has been disabled by later commands, undo restores the most recent reachable prior checkpoint.

---

### 5.2 redo_last

`redo_last`:

- Fails if redo history is empty
- Restores the checkpoint produced by the most recently undone Experience Unit
- Moves that Experience Unit back into undo history

Redo is implemented purely as structural state restoration.

No command logic is executed during redo.

Only previously checkpointed Experience Units may participate in redo history.

State changes from successful commands that never produced an undoable checkpoint do not become redoable Experience Units.

If an earlier checkpoint is restored, later uncheckpointed forward state is discarded unless it has been captured as valid redoable history.

---

### 5.3 undo_to_marker(marker_id)

`undo_to_marker(marker_id)`:

- Repeatedly performs `undo_last`
- Stops when the Experience Unit identified by `marker_id` has been undone
- Restores the checkpoint immediately preceding the marked Experience Unit
- Fails if the marker is not reachable via valid LIFO undo traversal

This operation is defined semantically as repeated LIFO undo.

MAP Core may optimize implementation, but observable behavior must be identical to repeated `undo_last`.

---

### 5.4 redo_to_marker(marker_id)

`redo_to_marker(marker_id)`:

- Repeatedly performs `redo_last`
- Stops when the Experience Unit identified by `marker_id` has been redone
- Restores the checkpoint produced by the marked Experience Unit
- Fails if the marker is not reachable via valid LIFO redo traversal
- Fails if redo history has been invalidated

This operation is defined semantically as repeated LIFO redo.

MAP Core may optimize implementation, but observable behavior must be identical to repeated `redo_last`.

---

### 5.5 Redo Invalidation

Any successful new command that advances Transaction state clears redo history.

This enforces a single linear history and prevents branching timelines.

---

## 6. Execution and Command Metadata

Commands and command executions may include metadata supplied by different layers of the system.

### 6.1 Execution Metadata

Execution metadata is supplied by the experience layer to describe Experience Unit boundaries and related UI-facing metadata.

Examples include:

- `snapshot_after`
- `marker_id`
- human-readable label
- other opaque experience-layer metadata

MAP Core must not interpret this metadata semantically beyond its structural role in Experience Unit formation and navigation.

---

### 6.2 snapshot_after

`snapshot_after` is an experience-layer boundary signal.

If `snapshot_after = true` and checkpointing is enabled:

- the currently active Experience Unit is closed
- a Structural Checkpoint is created after successful completion
- the new checkpoint becomes the resulting state of that Experience Unit
- redo history is cleared on successful forward progress

If `snapshot_after = false`:

- the command contributes to the currently active Experience Unit
- no new checkpoint boundary is created yet

`snapshot_after` does not ask MAP Core to choose policy.

It tells MAP Core whether the current successful command closes the current Experience Unit.

`snapshot_after` is only meaningful for successful mutable editing commands executed within an open Transaction that remains open after the command completes.

MAP Core must ignore or reject `snapshot_after` on:

- read-only commands
- `BeginTransaction`
- `Commit`
- `Rollback`
- other transaction lifecycle-boundary operations

---

### 6.3 Command Metadata

Command metadata describes structural properties or constraints of a command itself.

Examples include:

- `disable_undo`

Such metadata is distinct from execution metadata.

---

### 6.4 disable_undo

If a successful command executes with `disable_undo = true`:

- no new undo checkpoint is created for that command
- the command's resulting state must not become a newly created undoable Experience Unit boundary
- crash recovery may still persist the latest Transaction state
- redo history is cleared on successful forward progress
- `undo_checkpointing_enabled` for the Transaction becomes `false`

This is intended for:

- Bulk operations
- Regenerable imports
- Commands where structural checkpoint creation is undesirable or too expensive

---

### 6.5 undo_checkpointing_enabled

The Transaction maintains `undo_checkpointing_enabled: bool`.

Rules:

- Default is `true` for a newly opened Transaction
- It becomes `false` after any successful command with `disable_undo = true`
- While `false`, successful commands may still mutate the Transaction and may still persist crash recovery state
- While `false`, no new undoable Structural Checkpoints may be created, regardless of `snapshot_after`

This flag controls creation of new undo checkpoints.

It does **not** invalidate previously created checkpoints.

Therefore:

- previously created undo points remain valid restore targets
- users may still undo back to the most recent valid checkpoint created before checkpointing was disabled
- MAP Core must not present later uncheckpointed work as newly undoable history

Operationally, best practice for commands using `disable_undo = true` is to commit immediately after success and continue subsequent editing in a new Transaction.

---

## 7. Crash Recovery

### 7.1 Recovery Model

During an open Transaction:

- The Transaction context may be persisted locally
- Persistence is local-only and not DHT-visible
- Persistence may occur asynchronously

On restart:

- The latest persisted Transaction snapshot is loaded
- The staged graph is restored
- The transient graph is restored
- Any persisted history structures required by this model are restored
- Editing resumes from the most recently persisted consistent state

Crash recovery is a restoration mechanism, not a semantic undo system.

---

### 7.2 Persistence Scope

Persisted recovery snapshot includes the latest consistent Transaction state, including as needed:

- All staged holons
- All transient holons
- Structural history metadata required for correct recovery
- Marker positions or Experience Unit metadata if such metadata is part of recoverable state
- Transaction metadata

Only one latest recovery snapshot per open Transaction is required.

Recovery snapshots may overwrite prior persisted recovery state.

---

### 7.3 Recovery vs Undoability

Crash recovery persistence and undo checkpoint creation are distinct concerns.

A successful command may:

- persist latest crash-recoverable Transaction state
- without creating a new undoable checkpoint

This distinction is especially important when:

- `disable_undo = true`
- `undo_checkpointing_enabled = false`

Persisted recovery state answers:

- "What state should be restored after a crash?"

Undo history answers:

- "What prior Experience Units may the user navigate back to?"

These are related but not identical.

---

### 7.4 Lifecycle

On a successful transaction `commit` or `rollback`:

- The in-memory Transaction context is destroyed
- The persisted recovery snapshot is deleted
- No undo history survives beyond the Transaction boundary
- No redo history survives beyond the Transaction boundary

Undo and redo cannot span Transactions.

The cleanup responsibility for persisted recovery state belongs to the MAP Commands / runtime commands layer at the point where transaction lifecycle transitions are finalized. Concretely, for `commit`, persisted recovery state must be deleted immediately after the commit succeeds and before control returns to any generic post-command completion flow. This ensures that recovery cleanup is tied to the transaction boundary itself rather than to later generic command processing. `commit` is a lifecycle-boundary operation, not an in-transaction editing operation, and therefore must not trigger any subsequent checkpoint or recovery persistence behavior such as `snapshot_after`.


---

## 8. Threading and Persistence

- Structural checkpoint creation occurs only after successful command completion
- Recovery persistence may be handled asynchronously in a separate thread
- Persistence must reflect a fully consistent Transaction state
- Partial command states must never be persisted
- Recovery must load only the most recent consistent snapshot
- Any optimization must preserve the observable semantics defined in this specification

---

## 9. Holon-Only Representation

All persisted recovery state must be representable as:

- Holons
- HolonRelationships

Opaque structural snapshots may be serialized representations of holon subgraphs but must map conceptually to holon structures.

---

## 10. Loader and Bulk Operations

For large bulk commands (e.g. Holon Loader):

- `disable_undo` may be set
- Structural checkpointing is not required for undo
- Crash recovery may still persist the latest staged state
- Such commands should generally terminate the current undoable editing phase
- Best practice is to commit immediately after such commands and begin subsequent editing in a new Transaction

Future versions may introduce alternative strategies, but none are required in this model.

---

## 11. Guarantees

MAP Core guarantees that:

- Undo and redo are strictly structural
- Undo and redo are deterministic and linear
- Commands are all-or-nothing
- No failed command produces history
- Experience Units are the human-facing undo/redo units
- Structural Checkpoints are restore targets, not semantic commands
- History exists only during an open Transaction
- Previously created checkpoints remain valid even after checkpoint creation is later disabled
- Crash recovery restores a consistent Transaction state
- All undo/redo history is destroyed on commit or rollback

---

## 12. Non-Goals

This model does not support:

- Semantic command-specific undo logic
- Replay-based undo
- Delta-based checkpointing
- Cross-transaction undo
- Domain-level reversal after commit
- Trust Channel undo semantics
- Interpretation of marker metadata by MAP Core

Such capabilities may be introduced in future specifications but are not part of this structural model.

---

## 13. Summary

The Structural Experience-Level Undo / Redo model treats a Transaction as a mutable graph with a linear editing history.

The human-facing history is composed of Experience Units.

Each Experience Unit may contain one or more successful Commands and may close with a Structural Checkpoint when the experience layer signals `snapshot_after = true`.

Undo and redo move backward and forward across Experience Units by restoring adjacent Structural Checkpoints.

Markers identify Experience Units for navigation but remain opaque and non-semantic to MAP Core.

Crash recovery persists the latest Transaction state locally and is cleared entirely upon commit or rollback.

This model prioritizes:

- Human predictability
- Architectural simplicity
- Deterministic behavior
- Openness of the Commons
- Minimal implementation complexity
