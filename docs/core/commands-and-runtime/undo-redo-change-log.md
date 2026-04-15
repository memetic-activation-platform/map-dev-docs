# Structural Undo/Redo Spec Change Log

This document highlights the changes made to the Undo/Redo Spec since v1.0

---

# What's Changed in v1.2

This revision tightens the v1.1 model by resolving several remaining ambiguities around Experience Unit closure, metadata ownership, `snapshot_after` eligibility, and redo behavior after non-checkpointed work.

### 1. Clarifies when an Experience Unit becomes undoable

v1.1 introduced Experience Units, but did not explicitly say when they become undoable.

v1.2 now states that:

- an Experience Unit becomes undoable only when it closes successfully
- closure requires creation of a Structural Checkpoint
- commands accumulated in an open Experience Unit are not individually undoable until that boundary closes

This makes the model more precise and aligns it with the intended human experience.

---

### 2. Clarifies marker binding semantics

v1.1 restored the marker concept, but did not state exactly when a marker becomes attached.

v1.2 now specifies that:

- a marker is bound when an Experience Unit closes successfully
- the marker identifies that Experience Unit in the linear history

This makes marker placement consistent with checkpoint creation and Experience Unit closure.

---

### 3. Separates execution metadata from command metadata

v1.1 grouped `snapshot_after` and `disable_undo` together under “Command / Request Metadata,” which still blurred their responsibility boundaries.

v1.2 now distinguishes:

- **Execution Metadata**
    - `snapshot_after`
    - `marker_id`
    - label and other experience-layer metadata
- **Command Metadata**
    - `disable_undo`

This reflects the clarified architecture:

- the experience layer decides boundaries
- command metadata expresses structural constraints of the command itself

---

### 4. Adds explicit eligibility rules for `snapshot_after`

This is one of the most important clarifications in v1.2.

v1.1 explained what `snapshot_after` means, but did not explicitly limit where it is valid. That left room for invalid uses such as applying it to transaction lifecycle commands.

v1.2 now states that `snapshot_after` is only meaningful for:

- successful mutable editing commands
- executed within an open Transaction
- where the Transaction remains open after the command completes

It also explicitly states that MAP Core must ignore or reject `snapshot_after` on:

- read-only commands
- `BeginTransaction`
- `Commit`
- `Rollback`
- other lifecycle-boundary operations

This closes an important semantic gap and aligns the spec with the design insight that `snapshot_after` is a boundary signal, not a general post-success hook.

---

### 5. Strengthens undo behavior after checkpointing has been disabled

v1.1 said that previously created checkpoints remain valid after `undo_checkpointing_enabled` becomes `false`, but it did not clearly state the resulting operational behavior.

v1.2 now makes explicit that:

- previously created checkpoints remain reachable via undo
- undo restores the most recent reachable prior checkpoint
- this remains true even if later successful commands did not create new checkpoints

This captures the important nuance that disabling creation of new checkpoints does not invalidate older restore points.

---

### 6. Defines redo behavior for uncheckpointed forward state

This was the largest remaining gap in v1.1.

v1.2 now states that:

- only previously checkpointed Experience Units may participate in redo history
- state changes from commands that never produced an undoable checkpoint do not become redoable Experience Units
- restoring an earlier checkpoint discards later uncheckpointed forward state unless it was captured as valid redoable history

This clarifies the relationship between undo, redo, and later non-checkpointed edits, and prevents the model from implying redo behavior it cannot honestly provide.

---

### 7. Tightens overall semantic consistency

v1.2 does not change the core snapshot-based model introduced in v1.1. Instead, it sharpens the spec so that all major concepts now line up more cleanly:

- Experience Units are the human-facing history objects
- Structural Checkpoints are restore targets
- markers identify Experience Units
- `snapshot_after` is a closure signal, not a policy toggle
- `disable_undo` affects future checkpoint creation, not validity of prior checkpoints
- redo only applies to actual checkpointed Experience Units

Overall, v1.2 improves completeness and internal consistency without changing the fundamental architectural direction established in v1.1.

---

---

# What's Changed in v1.1

This revision clarifies and strengthens the structural undo/redo model in several important ways.

### 1. Introduces **Experience Units** as the human-facing undo/redo abstraction

The prior draft treated successful commands as if they directly corresponded to undoable history entries. This revision makes the model more precise:

- Users undo and redo **Experience Units**, not raw commands and not checkpoints
- An Experience Unit may contain one or more successful commands
- Experience Unit boundaries are determined by the experience layer

This better reflects real UI behavior, where a single user gesture may span multiple commands but should feel like one undoable action.

---

### 2. Repositions **Structural Checkpoints** as restore targets, not history items

The prior draft implicitly treated checkpoints as the undoable units. This revision distinguishes clearly between:

- **Experience Units** — the human-visible units of undo/redo
- **Structural Checkpoints** — the structural states restored during undo/redo

This resolves a key semantic confusion: a checkpoint created after one Experience Unit becomes the restore target for undoing the next Experience Unit.

---

### 3. Restores and clarifies the role of **Markers**

The revised spec restores the marker concept more explicitly:

- Markers identify **Experience Units**
- Markers are opaque and non-semantic
- Only `marker_id` may be used for undo/redo targeting
- `undo_to_marker(marker_id)` and `redo_to_marker(marker_id)` are explicitly defined

This preserves the intended human-navigation model while remaining compatible with snapshot-based implementation.

---

### 4. Clarifies `snapshot_after`

The prior draft risked making `snapshot_after` sound like an implementation “policy” switch. This revision clarifies that:

- `snapshot_after` is an **experience-layer boundary signal**
- It tells MAP Core whether the current successful command closes the active Experience Unit
- It does not ask MAP Core to decide behavior heuristically

This aligns the spec with the actual intended architecture: the client determines gesture boundaries.

---

### 5. Clarifies `disable_undo` under the snapshot model

The prior draft left ambiguity around how `disable_undo` interacts with later commands and later checkpoints.

This revision now specifies that:

- `disable_undo = true` prevents creation of a new undoable checkpoint for that state
- crash recovery may still persist the latest Transaction state
- redo is still invalidated on successful forward progress
- the Transaction tracks `undo_checkpointing_enabled`

This separates two concerns that had become blurred:
- crash recovery persistence
- creation of new undoable checkpoints

---

### 6. Introduces `undo_checkpointing_enabled`

To resolve ambiguity introduced by `disable_undo`, this revision adds the explicit Transaction-level concept:

- `undo_checkpointing_enabled: bool`

Rules are defined for when it is set, what it blocks, and what it does **not** block.

Importantly:

- previously created checkpoints remain valid
- users may still undo back to the last valid checkpoint
- no new undoable checkpoints may be created once checkpointing is disabled

This preserves honest and predictable human behavior.

---

### 7. Distinguishes **crash recovery** from **undoability**

The revised spec now explicitly states that:

- a state may be crash-recoverable
- without becoming a new undoable checkpoint

This is a major clarification and is especially important for bulk or loader-style operations.

---

### 8. Refines terminology and semantics throughout

Several terms were updated to better reflect intended behavior:

- `undo_last_command` -> `undo_last`
- `redo_last_command` -> `redo_last`
- history is described in terms of Experience Units and adjacent checkpoints
- UI-visible history is explicitly tied to Experience Units, not internal snapshots

This makes the model more faithful to human editing expectations and to applications like document editors.

---

### 9. Adds best-practice guidance for bulk operations

The revised spec now makes explicit that commands using `disable_undo = true` should generally:

- terminate the current undoable editing phase
- be followed by `commit`
- continue further editing in a new Transaction

This keeps the undo model predictable and prevents misleading navigation behavior.

---

Overall, this revision preserves the snapshot-based structural undo model while restoring the missing human-experience semantics around unit boundaries, markers, restore targets, and honest undo/redo behavior.
