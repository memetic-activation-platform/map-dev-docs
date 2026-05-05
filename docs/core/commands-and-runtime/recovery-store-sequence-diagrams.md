# RecoveryStore — Use-Case Sequence Diagrams

Actors in all diagrams:

| Actor | Description |
|-------|-------------|
| **Runtime** | `Runtime::execute_command` |
| **RuntimeSession** | `RuntimeSession` — orchestrates `ClientSession` |
| **ClientSession** | `ClientSession` — owns `TransactionContext` + `LocalRecoveryReceptor` |
| **Receptor** | `LocalRecoveryReceptor` — async wrapper around the store |
| **Store** | `TransactionRecoveryStore` — synchronous SQLite operations |
| **DB** | SQLite (`recovery_session`, `recovery_checkpoint`, `experience_unit`) |

---

## 1. persist — intermediate mutation (crash-recovery only)

Command with `snapshot_after=false`, `disable_undo=false`. Writes a sentinel checkpoint at
`stack_pos=-1` so the process can restart mid-transaction, but creates no ExperienceUnit.

```mermaid
sequenceDiagram
    participant Runtime
    participant RuntimeSession
    participant ClientSession
    participant Receptor
    participant Store
    participant DB

    Runtime->>RuntimeSession: persist_success(tx_id, label, policy{snapshot_after=false})
    RuntimeSession->>ClientSession: persist(desc, disable_undo=false, snapshot_after=false, ...)
    ClientSession->>Receptor: persist(context, ...)
    Receptor->>Store: persist(context, ...) [spawn_blocking]
    Store->>DB: snapshot = TransactionSnapshot::from_context
    Store->>DB: UPSERT recovery_session SET latest_checkpoint_id=<new>
    Store->>DB: INSERT OR REPLACE recovery_checkpoint (stack_pos=-1)
    note over Store,DB: redo_stack empty? skip redo-clear
    note over Store,DB: disable_undo=false, snapshot_after=false → intermediate path
    Store->>DB: COMMIT
    Store-->>Receptor: Ok(())
    Receptor-->>ClientSession: Ok(())
    ClientSession-->>RuntimeSession: Ok(())
    RuntimeSession-->>Runtime: Ok(())
```

---

## 2. persist — EU-closing mutation (snapshot_after=true)

Command with `snapshot_after=true`, `disable_undo=false`. In addition to the crash-recovery
checkpoint, creates an `experience_unit` row and pushes the unit onto the undo stack.

```mermaid
sequenceDiagram
    participant Runtime
    participant RuntimeSession
    participant ClientSession
    participant Receptor
    participant Store
    participant DB

    Runtime->>RuntimeSession: persist_success(tx_id, label, policy{snapshot_after=true})
    RuntimeSession->>ClientSession: persist(desc, disable_undo=false, snapshot_after=true, marker_id?)
    ClientSession->>Receptor: persist(context, ...)
    Receptor->>Store: persist(context, ...) [spawn_blocking]
    Store->>DB: snapshot = TransactionSnapshot::from_context
    Store->>DB: UPSERT recovery_session SET latest_checkpoint_id=<new>
    Store->>DB: INSERT OR REPLACE recovery_checkpoint (stack_pos=-1)
    note over Store,DB: redo_stack non-empty? DELETE EU+checkpoint redo rows, clear redo_stack_json
    Store->>DB: UPDATE recovery_checkpoint SET stack_pos=<undo top>
    Store->>DB: INSERT experience_unit (stack_kind='undo', stack_pos=<top>)
    Store->>DB: UPDATE recovery_session SET undo_stack_json, redo_stack_json, latest_checkpoint_id
    Store->>DB: COMMIT
    Store-->>Receptor: Ok(())
    Receptor-->>ClientSession: Ok(())
    ClientSession-->>RuntimeSession: Ok(())
    RuntimeSession-->>Runtime: Ok(())
```

---

## 3. persist — disable_undo mutation

Command with `disable_undo=true`. Writes the crash-recovery checkpoint, clears any pending
redo stack, and permanently sets `undo_checkpointing_enabled=0` for this transaction.
No ExperienceUnit is created regardless of `snapshot_after`.

```mermaid
sequenceDiagram
    participant Runtime
    participant RuntimeSession
    participant ClientSession
    participant Receptor
    participant Store
    participant DB

    Runtime->>RuntimeSession: persist_success(tx_id, label, policy{disable_undo=true})
    RuntimeSession->>ClientSession: persist(desc, disable_undo=true, snapshot_after=*, ...)
    ClientSession->>Receptor: persist(context, ...)
    Receptor->>Store: persist(context, ...) [spawn_blocking]
    Store->>DB: snapshot = TransactionSnapshot::from_context
    Store->>DB: UPSERT recovery_session SET latest_checkpoint_id=<new>
    Store->>DB: INSERT OR REPLACE recovery_checkpoint (stack_pos=-1)
    note over Store,DB: redo_stack non-empty? DELETE EU+checkpoint redo rows, clear redo_stack_json
    Store->>DB: UPDATE recovery_session SET undo_checkpointing_enabled=0
    Store->>DB: COMMIT
    note over Store: future persist calls skip EU creation
    Store-->>Receptor: Ok(())
    Receptor-->>ClientSession: Ok(())
```

---

## 4. undo_last — mid-stack (prior snapshot exists)

```mermaid
sequenceDiagram
    participant RuntimeSession
    participant ClientSession
    participant Receptor
    participant Store
    participant DB

    RuntimeSession->>ClientSession: undo_last()
    ClientSession->>Receptor: can_undo(tx_id)
    Receptor->>Store: can_undo(tx_id)
    Store->>DB: load undo_stack_json
    Store-->>Receptor: true
    Receptor-->>ClientSession: true
    ClientSession->>Receptor: undo(tx_id)
    Receptor->>Store: undo(tx_id) [spawn_blocking]
    Store->>DB: load undo_stack + redo_stack
    Store->>DB: pop top EU → load prior EU's checkpoint snapshot
    Store->>DB: UPDATE experience_unit SET stack_kind='redo'
    Store->>DB: UPDATE recovery_checkpoint SET stack_kind='redo'
    Store->>DB: UPDATE recovery_session stacks + latest_checkpoint_id
    Store->>DB: COMMIT
    Store-->>Receptor: Ok(Some(snapshot))
    Receptor-->>ClientSession: Ok(Some(snapshot))
    ClientSession->>ClientSession: snapshot.restore_into(context)
    ClientSession-->>RuntimeSession: Ok(())
```

---

## 5. undo_last — last EU (restore to baseline)

Undoing the only remaining EU. The store pops it onto the redo stack and returns `None`
because there is no prior snapshot.

```mermaid
sequenceDiagram
    participant RuntimeSession
    participant ClientSession
    participant Receptor
    participant Store
    participant DB

    RuntimeSession->>ClientSession: undo_last()
    ClientSession->>Receptor: can_undo(tx_id)
    Receptor-->>ClientSession: true
    ClientSession->>Receptor: undo(tx_id)
    Receptor->>Store: undo(tx_id) [spawn_blocking]
    Store->>DB: pop last EU from undo_stack (stack now empty)
    Store->>DB: UPDATE EU → redo, UPDATE checkpoint → redo
    Store->>DB: UPDATE recovery_session stacks (undo=[], redo=[eu_id])
    Store->>DB: COMMIT
    Store-->>Receptor: Ok(None)  ← no prior snapshot = baseline
    Receptor-->>ClientSession: Ok(None)
    ClientSession->>ClientSession: import_staged_holons(HolonPool::new())
    ClientSession->>ClientSession: import_transient_holons(HolonPool::new())
    ClientSession-->>RuntimeSession: Ok(())
```

---

## 6. undo_last — nothing to undo (empty stack)

```mermaid
sequenceDiagram
    participant RuntimeSession
    participant ClientSession
    participant Receptor
    participant Store
    participant DB

    RuntimeSession->>ClientSession: undo_last()
    ClientSession->>Receptor: can_undo(tx_id)
    Receptor->>Store: can_undo(tx_id)
    Store->>DB: load undo_stack_json → []
    Store-->>Receptor: false
    Receptor-->>ClientSession: false
    ClientSession-->>RuntimeSession: Err(Misc("No undo snapshot available..."))
```

---

## 7. redo_last

```mermaid
sequenceDiagram
    participant RuntimeSession
    participant ClientSession
    participant Receptor
    participant Store
    participant DB

    RuntimeSession->>ClientSession: redo_last()
    ClientSession->>Receptor: redo(tx_id)
    Receptor->>Store: redo(tx_id) [spawn_blocking]
    Store->>DB: load undo_stack + redo_stack
    alt redo stack empty
        Store-->>Receptor: Ok(None)
        Receptor-->>ClientSession: Ok(None)
        ClientSession-->>RuntimeSession: Err(Misc("No redo snapshot available..."))
    else redo stack non-empty
        Store->>DB: pop top EU from redo → load its checkpoint snapshot
        Store->>DB: UPDATE EU → stack_kind='undo'
        Store->>DB: UPDATE checkpoint → stack_kind='undo'
        Store->>DB: UPDATE recovery_session stacks + latest_checkpoint_id
        Store->>DB: COMMIT
        Store-->>Receptor: Ok(Some(snapshot))
        Receptor-->>ClientSession: Ok(Some(snapshot))
        ClientSession->>ClientSession: snapshot.restore_into(context)
        ClientSession-->>RuntimeSession: Ok(())
    end
```

---

## 8. undo_to_marker

Pops all EUs from the top of the undo stack down to and including the marked EU,
moving them all to the redo stack. Restores the snapshot of the EU just below the marker.

```mermaid
sequenceDiagram
    participant RuntimeSession
    participant ClientSession
    participant Receptor
    participant Store
    participant DB

    RuntimeSession->>ClientSession: undo_to_marker(marker_id)
    ClientSession->>Receptor: undo_to_marker(tx_id, marker_id)
    Receptor->>Store: undo_to_marker(...) [spawn_blocking]
    Store->>DB: load EU stack (newest-first)
    alt marker_id not found
        Store-->>Receptor: Err(InvalidParameter)
        Receptor-->>ClientSession: Err(...)
        ClientSession-->>RuntimeSession: Err(...)
    else marker found
        note over Store: to_pop = EUs from top down to marker (inclusive)
        Store->>DB: for each popped EU: UPDATE EU → redo, UPDATE checkpoint → redo
        Store->>DB: UPDATE recovery_session stacks + latest_checkpoint_id
        Store->>DB: COMMIT
        alt marker was NOT the first EU
            Store-->>Receptor: Ok(Some(prior_snapshot))
            Receptor-->>ClientSession: Ok(Some(prior_snapshot))
            ClientSession->>ClientSession: snapshot.restore_into(context)
        else marker WAS the first EU (baseline)
            Store-->>Receptor: Ok(None)
            Receptor-->>ClientSession: Ok(None)
            ClientSession->>ClientSession: import_staged_holons(HolonPool::new())
            ClientSession->>ClientSession: import_transient_holons(HolonPool::new())
        end
        ClientSession-->>RuntimeSession: Ok(())
    end
```

---

## 9. redo_to_marker

Pops EUs from the redo stack up to and including the marked EU, restoring them to undo.
Returns the snapshot of the marked EU (the state after it was applied).

```mermaid
sequenceDiagram
    participant RuntimeSession
    participant ClientSession
    participant Receptor
    participant Store
    participant DB

    RuntimeSession->>ClientSession: redo_to_marker(marker_id)
    ClientSession->>Receptor: redo_to_marker(tx_id, marker_id)
    Receptor->>Store: redo_to_marker(...) [spawn_blocking]
    Store->>DB: load EU redo stack (newest-first on redo = oldest-first from undo perspective)
    alt marker_id not found on redo stack
        Store-->>Receptor: Err(InvalidParameter)
        Receptor-->>ClientSession: Err(...)
        ClientSession-->>RuntimeSession: Err(...)
    else marker found
        note over Store: to_restore = EUs from redo top down to marker (inclusive)
        Store->>DB: for each EU: UPDATE EU → undo, UPDATE checkpoint → undo
        Store->>DB: UPDATE recovery_session stacks + latest_checkpoint_id
        Store->>DB: COMMIT
        Store-->>Receptor: Ok(Some(marked_eu_snapshot))
        Receptor-->>ClientSession: Ok(Some(snapshot))
        ClientSession->>ClientSession: snapshot.restore_into(context)
        ClientSession-->>RuntimeSession: Ok(())
    end
```

---

## 10. recover_latest — crash recovery on startup

Called from `ClientSession::recover` when reopening a transaction after process restart.

```mermaid
sequenceDiagram
    participant RuntimeSession
    participant ClientSession
    participant Receptor
    participant Store
    participant DB

    RuntimeSession->>ClientSession: ClientSession::recover(space_manager, recovery, tx_id)
    ClientSession->>ClientSession: open_transaction_with_id(tx_id)
    ClientSession->>ClientSession: restore_from_recovery()
    ClientSession->>Receptor: recover_latest(tx_id)
    Receptor->>Store: recover_latest(tx_id)
    Store->>DB: SELECT latest_checkpoint_id FROM recovery_session WHERE tx_id=?
    alt no session row
        Store-->>Receptor: Ok(None)
        Receptor-->>ClientSession: Ok(None)
        note over ClientSession: context left at empty open state
    else checkpoint found
        Store->>DB: SELECT snapshot_blob FROM recovery_checkpoint WHERE checkpoint_id=?
        Store->>Store: snapshot.verify_integrity()
        Store-->>Receptor: Ok(Some(snapshot))
        Receptor-->>ClientSession: Ok(Some(snapshot))
        ClientSession->>ClientSession: snapshot.restore_into(context)
    end
    ClientSession-->>RuntimeSession: Ok(Self)
```

---

## 11. cleanup — on commit

Called by `RuntimeSession::commit_transaction` after `context.commit()` succeeds.
Removes all recovery state for the transaction (CASCADE deletes checkpoints + EUs).

```mermaid
sequenceDiagram
    participant RuntimeSession
    participant ClientSession
    participant Receptor
    participant Store
    participant DB

    RuntimeSession->>ClientSession: cleanup()
    ClientSession->>Receptor: cleanup(tx_id)
    Receptor->>Store: cleanup(tx_id) [spawn_blocking]
    Store->>DB: DELETE FROM recovery_session WHERE tx_id=?
    note over DB: ON DELETE CASCADE removes recovery_checkpoint + experience_unit rows
    Store->>DB: COMMIT
    Store-->>Receptor: Ok(())
    Receptor-->>ClientSession: Ok(())
    ClientSession-->>RuntimeSession: Ok(())
    RuntimeSession->>RuntimeSession: archive_transaction(tx_id)
```

---

## 12. list_open_sessions — startup recovery scan

Called by `RuntimeSession::restore_open_sessions` at process startup to find transactions
that were open when the process last crashed.

```mermaid
sequenceDiagram
    participant Host
    participant RuntimeSession
    participant Receptor
    participant Store
    participant DB

    Host->>RuntimeSession: restore_open_sessions()
    RuntimeSession->>Receptor: list_open_sessions()
    Receptor->>Store: list_open_sessions()
    Store->>DB: SELECT tx_id FROM recovery_session WHERE lifecycle_state='Open'
    Store-->>Receptor: Ok(Vec<tx_id_str>)
    Receptor-->>RuntimeSession: Ok(Vec<tx_id_str>)
    loop for each tx_id
        RuntimeSession->>RuntimeSession: ClientSession::recover(space_manager, recovery, tx_id)
        note over RuntimeSession: recover_latest called inside — restores to last checkpoint
        RuntimeSession->>RuntimeSession: register_recovered_session(session)
    end
    RuntimeSession-->>Host: Ok(restored_count)
```

---

## 13. can_undo / can_redo — stack inspection (UI query)

Lightweight reads used to determine whether undo/redo controls should be enabled.
No write to DB.

```mermaid
sequenceDiagram
    participant Caller
    participant Receptor
    participant Store
    participant DB

    Caller->>Receptor: can_undo(tx_id)
    Receptor->>Store: can_undo(tx_id)
    Store->>DB: SELECT undo_stack_json FROM recovery_session WHERE tx_id=?
    Store-->>Receptor: Ok(undo_stack.len() > 0)
    Receptor-->>Caller: Result<bool>

    Caller->>Receptor: can_redo(tx_id)
    Receptor->>Store: can_redo(tx_id)
    Store->>DB: SELECT redo_stack_json FROM recovery_session WHERE tx_id=?
    Store-->>Receptor: Ok(redo_stack.len() > 0)
    Receptor-->>Caller: Result<bool>
```

---

## 14. undo_history — undo stack label list (UI query)

Returns the description strings of all closed EUs in undo order (oldest first).

```mermaid
sequenceDiagram
    participant Caller
    participant Receptor
    participant Store
    participant DB

    Caller->>Receptor: list_undo_history(tx_id)
    Receptor->>Store: undo_history(tx_id) [spawn_blocking]
    Store->>DB: SELECT description FROM recovery_checkpoint WHERE tx_id=? AND stack_kind='undo' AND stack_pos >= 0 ORDER BY stack_pos ASC
    Store-->>Receptor: Ok(Vec<String>)
    Receptor-->>Caller: Ok(Vec<String>)
```

---

## DB schema summary (for reference)

```
recovery_session
  tx_id PK, lifecycle_state, latest_checkpoint_id FK,
  undo_stack_json, redo_stack_json,
  undo_checkpointing_enabled, format_version, updated_at_ms

recovery_checkpoint
  checkpoint_id PK, tx_id FK→session(CASCADE),
  stack_kind ('undo'|'redo'), stack_pos (-1=sentinel, ≥0=EU-linked),
  snapshot_blob, snapshot_hash, description, disable_undo, created_at_ms

experience_unit
  unit_id PK, tx_id FK→session(CASCADE),
  marker_id?, marker_label?,
  checkpoint_id FK→recovery_checkpoint,
  stack_kind ('undo'|'redo'), stack_pos, created_at_ms
```
