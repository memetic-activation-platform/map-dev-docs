# MAP Commands Cheatsheet (v0.6)

<div style="display: flex; flex-wrap: wrap; gap: 2rem;">

<div style="flex: 1 1 420px; min-width: 320px;">

### Goal

Establish:

- Canonical IPC command surface
- Explicit structural scope
- Strict wire/domain separation
- Descriptor-driven policy
- Single execution boundary

Structure first.  
Behavior remains domain-defined.

---

## 1. Execution Boundary

**All IPC flows through:**

```text
TypeScript
  → Tauri
    → Runtime::dispatch  (binding seam)
      → HolonSpaceManager
        → TransactionContext
          → HolonReference
            → Domain
```

- No string dispatch
- No session-derived authority
- No bypass paths
- No Wire types below binding seam

---

## 2. IPC Entry (Transport Only)

Only the outer envelope is visible at IPC level:

```rust
pub struct MapRequestWire {
    pub request_id: RequestId,
    pub command: MapCommandWire,
}

pub struct MapResponseWire {
    pub request_id: RequestId,
    pub result: Result<MapResultWire, HolonErrorWire>,
}
```

Everything below `Runtime::dispatch` is **domain-only**.

---

## 3. Structural Scope (Domain)

```rust
pub enum MapCommand {
    Space(SpaceCommand),
    Transaction(TransactionCommand),
    Holon(HolonCommand),
}
```

Scope is explicit.  
Scope is never inferred.

---

## 4. Space Scope

```rust
pub enum SpaceCommand {
    BeginTransaction,
}
```

**BeginTransaction**

- Opens new transaction
- Returns `TxId`
- Only space-level command in v0

</div>

<div style="flex: 1 1 420px; min-width: 320px;">

## 5. Transaction Scope (Domain)

```rust
pub struct TransactionCommand {
    pub context: TransactionContextHandle,
    pub action: TransactionAction,
}

pub enum TransactionAction {
    Commit,
    CreateTransientHolon { key: Option<MapString> },
    StageNewHolon { transient: TransientReference },
    StageNewVersion { holon: SmartReference },
    LoadHolons { bundle: HolonReference },
    Dance(DanceInvocation),
    Lookup(LookupQuery),
}
```

Runtime responsibilities:

- Resolve transaction
- Enforce lifecycle
- Enforce descriptor policy
- Delegate to `TransactionContext`

No `tx_id` strings below binding seam.

---

## 6. Holon Scope (Domain)

```rust
pub struct HolonCommand {
    pub target: HolonReference,
    pub action: HolonAction,
}

pub enum HolonAction {
    Read(ReadableHolonAction),
    Write(WritableHolonAction),
}
```

Dispatch stops at `HolonReference`.

---

## 7. ReadableHolonAction

```rust
pub enum ReadableHolonAction {
    PropertyValue { name: PropertyName },
    RelatedHolons { name: RelationshipName },
    Key,
    VersionedKey,
    IntoModel,
    AllRelatedHolons,
    EssentialContent,
    Summarize,
}
```

- Non-mutating
- Lifecycle validated via descriptor
- No snapshot

---

## 8. WritableHolonAction

```rust
pub enum WritableHolonAction {
    WithPropertyValue { name: PropertyName, value: BaseValue },
    RemovePropertyValue { name: PropertyName },
    AddRelatedHolons { name: RelationshipName, holons: Vec<HolonReference> },
    RemoveRelatedHolons { name: RelationshipName, holons: Vec<HolonReference> },
    WithDescriptor { descriptor: HolonReference },
    WithPredecessor { predecessor: Option<HolonReference> },
}
```

- Requires `Open` lifecycle
- May require commit guard
- May trigger snapshot persistence

---

## 9. Descriptor Policy

```rust
pub struct CommandDescriptor {
    pub is_mutating: bool,
    pub requires_open_tx: bool,
    pub requires_commit_guard: bool,
    pub snapshot_after: bool,
}
```

Enums define structure.  
Descriptors define behavior.

---

## 10. Runtime Boundary

```rust
pub struct Runtime {
    active_space: Arc<HolonSpaceManager>,
}
```

Responsibilities:

- Accept `MapRequestWire`
- Bind Wire → Domain
- Resolve scope
- Enforce descriptor
- Delegate execution
- Convert domain result → Wire

Below binding seam:

    No `*Wire` types exist.

---

## 11. Single IPC Entry

```rust
#[tauri::command]
fn dispatch_map_command(
    state: State<Runtime>,
    request: MapRequestWire,
) -> Result<MapResponseWire, HolonErrorWire> {
    state.dispatch(request)
}
```

Transport only.

All execution authority begins inside:

    Runtime::dispatch

</div>

</div>