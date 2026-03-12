# MAP Commands Cheatsheet (v1.0.0)

See the [full specification](commands.md) for details.

## Goal

Establish:

- Canonical IPC command surface
- Explicit structural scope
- Strict wire/domain separation
- Descriptor-driven policy
- Single execution boundary

Structure first. Behavior remains domain-defined.

---

## 1. Single IPC Entry

    #[tauri::command]
    async fn dispatch_map_command(
        state: State<'_, Runtime>,
        request: MapIpcRequest,
    ) -> Result<MapIpcResponse, HolonError> {
        state.dispatch(request).await
    }

**Invariants**

- This is the only IPC entrypoint for MAP domain execution.
- It accepts wire types only.
- It delegates immediately to `Runtime::dispatch`.
- It performs no binding, lifecycle enforcement, or policy branching.

---

## 2. IPC Envelope (Wire Layer Only)

    pub struct MapIpcRequest {
        pub request_id: RequestId,
        pub command: MapCommandWire,
    }

    pub struct MapIpcResponse {
        pub request_id: RequestId,
        pub result: Result<MapResultWire, HolonError>,
    }

**Wire Layer Rules**

- Wire types are serializable transport structures.
- Wire types contain identifiers only.
- Wire types contain no behavioral objects.
- Wire types must not cross below the binding seam.

---

## 3. Runtime Boundary (Binding Seam)

    pub struct Runtime {
        active_space: Arc<HolonSpaceManager>,
    }

`Runtime::dispatch` is the single structural execution boundary.

**Runtime Responsibilities**

- Bind Wire → Domain types
- Resolve structural scope
- Resolve transaction context when required
- Enforce descriptor policy
- Delegate execution to domain layer
- Convert domain result → Wire

Below the binding seam:

    No *Wire types exist.

---

## 4. Structural Scope (Domain)

    pub enum MapCommand {
        Space(SpaceCommand),
        Transaction(TransactionCommand),
        Holon(HolonCommand),
    }

**Scope Rules**

- Scope is explicit and structural.
- Scope is never inferred from session state.
- Scope determines binding requirements.
- Structural enums define shape only, not policy.

---

## 5. Space Scope

    pub enum SpaceCommand {
        BeginTransaction,
    }

- Opens a new transaction.
- Returns `TxId`.
- Only space-level command in v0.

---

## 6. Transaction Scope (Domain)

    pub struct TransactionCommand {
        pub context: TransactionContextHandle,
        pub action: TransactionAction,
    }

    pub enum TransactionAction {
        Commit,
        NewHolon { key: Option<MapString> },
        StageNewHolon { source: TransientReference },
        StageNewFromClone {
            original: HolonReference,
            new_key: MapString,
        },
        StageNewVersion { current_version: SmartReference },
        StageNewVersionFromId { holon_id: HolonId },
        DeleteHolon { local_id: LocalId },
        LoadHolons { bundle: HolonReference },
        Dance(DanceRequest),
        Lookup(LookupAction),
        Query(QueryExpression),
    }

    pub enum LookupAction {
        GetAllHolons,
        GetStagedHolonByBaseKey { key: MapString },
        GetStagedHolonsByBaseKey { key: MapString },
        GetStagedHolonByVersionedKey { key: MapString },
        GetTransientHolonByBaseKey { key: MapString },
        GetTransientHolonByVersionedKey { key: MapString },
        StagedCount,
        TransientCount,
    }

**Transaction Invariants**

- `tx_id` exists only in wire form.
- `TransactionContextHandle` exists only in domain form.
- Lifecycle enforcement occurs in Runtime, driven by descriptor.
- No string identifiers below binding seam.

---

## 7. Holon Scope (Domain)

    pub struct HolonCommand {
        pub target: HolonReference,
        pub action: HolonAction,
    }

    pub enum HolonAction {
        Read(ReadableHolonAction),
        Write(WritableHolonAction),
    }

**Holon Invariants**

- Holon commands are self-resolving.
- Action does not include `tx_id` or `TransactionContext`.
- Dispatch stops at `HolonReference`.
- Domain behavior resides in reference-layer traits.

---

## 8. ReadableHolonAction

    pub enum ReadableHolonAction {
        CloneHolon,
        EssentialContent,
        Summarize,
        HolonId,
        Predecessor,
        Key,
        VersionedKey,
        PropertyValue { name: PropertyName },
        RelatedHolons { name: RelationshipName },
    }

- Non-mutating.
- Lifecycle validated via descriptor.
- Does not trigger snapshot persistence.

Not part of the MAP Commands API surface in v0:

- `is_accessible`
- `get_all_related_holons`
- `into_model`

---

## 9. WritableHolonAction

    pub enum WritableHolonAction {
        WithPropertyValue { name: PropertyName, value: BaseValue },
        RemovePropertyValue { name: PropertyName },
        AddRelatedHolons { name: RelationshipName, holons: Vec<HolonReference> },
        RemoveRelatedHolons { name: RelationshipName, holons: Vec<HolonReference> },
        WithDescriptor { descriptor: HolonReference },
        WithPredecessor { predecessor: Option<HolonReference> },
    }

- Requires `Open` lifecycle.
- May require commit guard.
- May trigger snapshot persistence, descriptor-driven.

---

## 10. Descriptor Policy

    pub struct CommandDescriptor {
        pub is_mutating: bool,
        pub requires_open_tx: bool,
        pub requires_commit_guard: bool,
        pub snapshot_after: bool,
    }

**Policy Rules**

- Every command is described by a `CommandDescriptor`.
- Structural enums define command shape.
- Descriptors define execution behavior.
- Runtime enforces descriptor metadata.

---

## Core Architectural Invariants

- Exactly one IPC entrypoint.
- Runtime is the only execution boundary.
- No `*Wire` types below the binding seam.
- Scope is explicit: `Space | Transaction | Holon`.
- Commands execute in host, not in WASM.
- Descriptor metadata drives execution policy.
- No session-derived authority.
- No string-based dispatch.

This cheat sheet captures structural invariants only.  
Detailed execution semantics are defined in the [full specification](commands.md).

