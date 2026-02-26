# MAP Commands Cheatsheet (v0)

<div style="display: flex; flex-wrap: wrap; gap: 2rem;">

<div style="flex: 1 1 420px; min-width: 320px;">

### Goal

Establish:

- Canonical IPC command surface
- Explicit structural scope
- Descriptor-driven policy
- Single execution boundary

Structure first.  
Behavior remains domain-defined.

---

## 1. Execution Boundary

**All IPC flows through:**

```text
Tauri
  → Runtime::dispatch
    → HolonSpaceManager
      → TransactionContext
        → HolonReference
          → Domain
```

- No string dispatch
- No session-derived authority
- No bypass paths

---

## 2. IPC Envelope

```rust
pub struct MapRequest {
    pub request_id: RequestId,
    pub command: MapCommand,
}

pub struct MapResponse {
    pub request_id: RequestId,
    pub result: Result<MapResult, MapError>,
}
```

Rules:

- `request_id` must round-trip
- `MapCommand` fully structural
- No execution authority in session state

---

## 3. Structural Scope

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

---

## 5. Transaction Scope

```rust
pub struct TransactionCommand {
    pub tx_id: TxId,
    pub action: TransactionAction,
}
```

Runtime MUST:

1. Resolve `tx_id`
2. Fail if missing
3. Enforce descriptor policy

### TransactionAction (v0)

```rust
pub enum TransactionAction {
    Commit,
    CreateTransientHolon { key: Option<MapString> },
    StageNewHolon { transient: TemporaryId },
    StageNewVersion { holon: HolonId },
    LoadHolons { bundle: HolonReferenceWire },
    Dance(DanceInvocation),
    Lookup(LookupQuery),
}
```

</div>

<div style="flex: 1 1 420px; min-width: 320px;">

## 6. Holon Scope

```rust
pub struct HolonCommand {
    pub target: HolonReferenceWire,
    pub action: HolonAction,
}
```

Runtime MUST:

- Bind `HolonReferenceWire`
- Validate transaction
- Enforce descriptor
- Delegate to façade

---

## 7. HolonAction

```rust
pub enum HolonAction {
    Read(ReadableHolonAction),
    Write(WritableHolonAction),
}
```

Aligned directly with domain traits.

---

## 8. ReadableHolonAction

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

---

## 9. WritableHolonAction

```rust
pub enum WritableHolonAction {
    WithPropertyValue { name: PropertyName, value: BaseValue },
    RemovePropertyValue { name: PropertyName },
    AddRelatedHolons { name: RelationshipName, holons: Vec<HolonReferenceWire> },
    RemoveRelatedHolons { name: RelationshipName, holons: Vec<HolonReferenceWire> },
    WithDescriptor { descriptor: HolonReferenceWire },
    WithPredecessor { predecessor: Option<HolonReferenceWire> },
}
```

Characteristics:

- Requires `Open` lifecycle
- May require commit guard
- May trigger snapshot persistence

---

## 10. Descriptor Policy

```rust
pub struct CommandDescriptor {
    pub is_mutating: bool,
    pub requires_open_tx: bool,
    pub requires_commit_guard: bool,
    pub snapshot_after: bool,
}
```

Runtime responsibilities:

- Validate lifecycle
- Enforce commit guard
- Trigger snapshot if required

Enums define shape.  
Descriptors define behavior.

---

## 11. Runtime (v0)

```rust
pub struct Runtime {
    active_space: Arc<HolonSpaceManager>,
}
```

Responsibilities:

- Accept `MapRequest`
- Resolve scope
- Bind transaction + references
- Enforce descriptor
- Delegate execution

Does NOT:

- Own lifecycle logic
- Enforce TrustChannel rules
- Maintain multi-space registry (v0)

---

## 12. Single IPC Entry

Every command enters here.

```rust
#[tauri::command]
fn dispatch_map_command(
    state: State<Runtime>,
    request: MapRequest,
) -> Result<MapResponse, String> {
    todo!()
}
```

</div>

</div>
