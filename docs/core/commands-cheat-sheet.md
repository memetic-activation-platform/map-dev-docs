# MAP Commands Cheatsheet (v0.3)

<div style="display: flex; flex-wrap: wrap; gap: 2rem;">

<div style="flex: 1 1 420px; min-width: 320px;">

### Goal

Establish:

- Canonical IPC command surface
- Explicit structural scope
- Strict wire/domain separation (sandwich model)
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
- No Wire types below Runtime binding seam

---

## 2. IPC Envelope (Wire Layer Only)

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

Rules:

- `request_id` must round-trip
- Wire types exist only at IPC boundary
- No behavioral objects in Wire types
- No transaction context in Wire types

---

## 3. Structural Scope

### Wire Form

```rust
pub enum MapCommandWire {
    Space(SpaceCommandWire),
    Transaction(TransactionCommandWire),
    Holon(HolonCommandWire),
}
```

### Domain Form (After Binding)

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

### Wire

```rust
pub enum SpaceCommandWire {
    BeginTransaction,
}
```

### Domain

```rust
pub enum SpaceCommand {
    BeginTransaction,
}
```

**BeginTransaction**

- Opens new transaction
- Returns `TxId`
- Only space-level command in v0

---

## 5. Transaction Scope

### Wire

```rust
pub struct TransactionCommandWire {
    pub tx_id: TxId,
    pub action: TransactionActionWire,
}

pub enum TransactionActionWire {
    Commit,
    CreateTransientHolon { key: Option<MapString> },
    StageNewHolon { transient: TemporaryId },
    StageNewVersion { holon: HolonId },
    LoadHolons { bundle: HolonReferenceWire },
    Dance(DanceInvocationWire),
    Lookup(LookupQueryWire),
}
```

### Domain (After Binding)

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

Runtime MUST:

1. Resolve `tx_id`
2. Convert Wire → Domain
3. Fail if transaction missing
4. Enforce descriptor policy

No `*Wire` types below binding seam.

---

## 6. Holon Scope

### Wire

```rust
pub struct HolonCommandWire {
    pub target: HolonReferenceWire,
    pub action: HolonActionWire,
}

pub enum HolonActionWire {
    Read(ReadableHolonActionWire),
    Write(WritableHolonActionWire),
}
```

### Domain (After Binding)

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

Runtime MUST:

- Bind `HolonReferenceWire` → `HolonReference`
- Validate lifecycle
- Enforce descriptor
- Delegate to façade traits

Dispatch stops at `HolonReference`.

---

## 7. ReadableHolonAction (Domain)

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

Characteristics:

- Non-mutating
- No snapshot
- Lifecycle validated via descriptor
- Executed via HolonReference façade

---

## 8. WritableHolonAction (Domain)

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

Characteristics:

- Requires `Open` lifecycle
- May require commit guard
- May trigger snapshot persistence
- No Wire types permitted

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

Runtime responsibilities:

- Resolve descriptor
- Validate lifecycle
- Enforce commit guard
- Trigger snapshot if required

Enums define structural shape.  
Descriptors define execution behavior.

---

## 10. Runtime (v0.3)

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

Does NOT:

- Own lifecycle semantics
- Enforce TrustChannel policy
- Maintain multi-space registry (v0)

Below binding seam:  
No `*Wire` types exist.

---

## 11. Single IPC Entry

Every command enters here.

```rust
#[tauri::command]
fn dispatch_map_command(
    state: State<Runtime>,
    request: MapRequestWire,
) -> Result<MapResponseWire, String> {
    state.dispatch(request)
         .map_err(|e| e.to_string())
}
```

Transport only.

All execution authority begins inside:

    Runtime::dispatch

</div>

</div>