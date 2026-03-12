# MAP Commands Specification (v1.0.0)

---

## 1. Purpose and Design Intent

This specification defines the canonical IPC command architecture for the Memetic Activation Platform (MAP).
MAP Commands define the **IPC contract between the TypeScript client (Experience Layer) and the Conductora host runtime (Rust Integration Hub)**. They provide a strongly typed interface through which the client invokes MAP domain operations inside the IntegrationHub runtime. All stateful execution occurs inside the Integration Hub. The Experience Layer performs no domain mutation and holds no holon state.

MAP Commands are NOT intended to serve as a universal protocol for all MAP communication channels. Other subsystems (such as Trust Channels, host–guest bridges, or storage replay mechanisms) may use different transport formats and adapters.

This specification formalizes the MAP IPC command architecture, including:

- A single structural dispatch boundary
- An explicit scope model
- A strict wire/domain separation ("sandwich model")
- Descriptor-driven execution policy
- Deterministic lifecycle enforcement

This document is normative for the MAP IPC layer.

---

## 2. Architectural Context

This specification defines the MAP Command architecture within the Conductora Tauri container, as shown in the MAP Deployment Architecture.

![MAP Deployment Archi - v1.2 -- Detailed View.jpg](media/MAP%20Deployment%20Archi%20-%20v1.2%20--%20Detailed%20View.jpg)

MAP Commands form the structural IPC contract between the TypeScript Experience Layer and the Rust Integration Hub.

They exist exclusively within the Conductora container.

---

### 2.1 IPC Entry Point

All MAP Commands enter the system through a single Tauri IPC function:

`dispatch_map_command`

Call flow begins:

```text
TypeScript
  → Tauri invoke("dispatch_map_command")
    → dispatch_map_command
    → Runtime::dispatch
```

The Tauri entrypoint is transport-only.

It:

- Accepts wire types
- Delegates immediately to Runtime
- Performs no binding
- Performs no lifecycle enforcement
- Performs no descriptor evaluation

All execution authority begins inside Runtime.

---

### 2.2 Runtime Boundary

`Runtime::dispatch` is the single structural execution boundary for MAP Commands.

It is responsible for:

- Binding wire types to domain types
- Resolving transaction context
- Enforcing descriptor policy
- Delegating scope-specific execution
- Converting domain results back to wire form

No command may bypass Runtime.

---

### 2.3 The Sandwich Model (Wire vs Domain)

MAP Commands strictly separate transport types ("bread") from behavioral domain types ("filling").

#### Bread (Wire Types)

Wire types exist only:

- In the Tauri entrypoint
- Inside `Runtime::dispatch` during binding
- When constructing the response

Examples:

- `MapIpcRequest`
- `MapIpcResponse`
- `MapCommandWire`
- `HolonReferenceWire`
- `HolonError`

Wire types:

- Are serializable
- Contain identifiers
- Contain no behavioral objects
- Must not cross into domain execution

#### Filling (Domain Types)

Domain types exist only below the binding seam.

Examples:

- `MapCommand`
- `SpaceCommand`
- `TransactionCommand`
- `HolonCommand`
- `HolonReference`
- `TransactionContextHandle`
- `HolonError`

Domain types:

- Contain behavior
- Contain transaction-bound references
- Must not depend on serialization
- Must not reference any `*Wire` types

Binding occurs exclusively inside `Runtime::dispatch`.

After binding completes, no `*Wire` types remain.

---

### 2.4 Host / Guest Demarcation

MAP Commands are a host-side construct.

They execute entirely within the Integration Hub (Rust client layer).

They do not:

- Execute inside the Holochain Conductor
- Execute inside the Rust Holons Guest (WASM)
- Cross into other conductors as command structures

The guest exposes domain capabilities.  
The host interprets and dispatches commands.

This separation is fundamental to the sandwich model.

---

## 3. Normative IPC Dispatch Definition

The following function is the single normative IPC ingress into MAP domain execution:

```rust
#[tauri::command]
async fn dispatch_map_command(
    state: State<'_, Runtime>,
    request: MapIpcRequest,
) -> Result<MapIpcResponse, HolonError> {
    state.dispatch(request).await
}
```

Normative requirements:

- This MUST be the only IPC command that initiates MAP domain execution.
- It MUST accept only wire-layer types.
- It MUST delegate immediately to `Runtime::dispatch`.
- It MUST perform no scope inference.
- It MUST perform no lifecycle enforcement.
- It MUST perform no descriptor evaluation.
- It MUST not construct domain objects directly.

All execution authority begins inside `Runtime::dispatch`.

---

## 4. IPC Envelope (Wire Layer)

### 4.1 MapIpcRequest

```rust
pub struct MapIpcRequest {
    pub request_id: RequestId,
    pub command: MapCommandWire,
}
```

### 4.2 MapIpcResponse

```rust
pub struct MapIpcResponse {
    pub request_id: RequestId,
    pub result: Result<MapResultWire, HolonError>,
}
```

Wire types:

- Are serializable
- Contain identifiers only
- Contain no behavioral objects
- Must not cross below the binding seam

---

## 5. Domain Command Surface (Post-Binding)

Command identity is determined exclusively by the structural variant of `MapCommandWire`.

MAP Commands do not use string-based command routing. Scope and command identity must be derived solely from the
structural command variant. These types exist only below the binding seam.

### 5.1 MapCommand

```rust
pub enum MapCommand {
    Space(SpaceCommand),
    Transaction(TransactionCommand),
    Holon(HolonCommand),
}
```

Scope is explicit and structural.

---

### 5.2 SpaceCommand

```rust
pub enum SpaceCommand {
    BeginTransaction,
}
```

---

### 5.3 TransactionCommand

```rust
pub struct TransactionCommand {
    pub context: TransactionContextHandle,
    pub action: TransactionAction,
}
```

No `tx_id` strings exist below binding.

### 5.3.1 TransactionAction

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

`TransactionAction` defines the complete transaction-scoped command surface exposed by the MAP Commands API in v0.

Discrete actions:

- `Commit`
  Finalizes the active transaction.

- `NewHolon { key }`
  Creates a new transient holon, optionally with a base key.

- `StageNewHolon { source }`
  Stages a new holon from a transient source reference.

- `StageNewFromClone { original, new_key }`
  Stages a new holon cloned from an existing holon reference with a new key.

- `StageNewVersion { current_version }`
  Stages a new version from an existing smart reference.

- `StageNewVersionFromId { holon_id }`
  Stages a new version from an existing holon id.

- `DeleteHolon { local_id }`
  Deletes the holon identified by the given local id within the active transaction.

- `LoadHolons { bundle }`
  Loads holons from an existing holon reference bundle into the active transaction.

- `Dance(DanceRequest)`
  Executes a DANCE request within the active transaction context.

- `Lookup(LookupAction)`
  Executes a transaction-scoped lookup action.

- `Query(QueryExpression)`
  Executes a query expression against transaction-visible state.

#### 5.3.1.1 LookupAction

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

`LookupAction` is the definitive list of transaction-scoped lookup actions.

Discrete actions:

- `GetAllHolons`
  Returns all holons visible in the active transaction.

- `GetStagedHolonByBaseKey { key }`
  Returns the staged holon matching the given base key.

- `GetStagedHolonsByBaseKey { key }`
  Returns all staged holons matching the given base key.

- `GetStagedHolonByVersionedKey { key }`
  Returns the staged holon matching the given versioned key.

- `GetTransientHolonByBaseKey { key }`
  Returns the transient holon matching the given base key.

- `GetTransientHolonByVersionedKey { key }`
  Returns the transient holon matching the given versioned key.

- `StagedCount`
  Returns the number of staged holons in the active transaction.

- `TransientCount`
  Returns the number of transient holons in the active transaction.

---

### 5.4 HolonCommand

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

### 5.4.1 HolonAction

    pub enum HolonAction {
        Read(ReadableHolonAction),
        Write(WritableHolonAction),
    }

`HolonAction` defines the complete holon-targeted command surface exposed by the MAP Commands API in v0.

Discrete actions:

- `Read(ReadableHolonAction)`
  Executes a non-mutating action against a bound holon reference.

- `Write(WritableHolonAction)`
  Executes a mutating action against a bound holon reference.

#### 5.4.1.1 ReadableHolonAction

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

`ReadableHolonAction` is the definitive list of read-only holon actions exposed through the MAP Commands API.

Discrete actions:

- `CloneHolon`
  Clones the target holon and returns a transient reference.

- `EssentialContent`
  Returns the essential content of the target holon.

- `Summarize`
  Returns a summary string for the target holon.

- `HolonId`
  Returns the holon id of the target holon.

- `Predecessor`
  Returns the predecessor reference of the target holon, if any.

- `Key`
  Returns the base key of the target holon, if any.

- `VersionedKey`
  Returns the versioned key of the target holon.

- `PropertyValue { name }`
  Returns the value of the named property on the target holon.

- `RelatedHolons { name }`
  Returns the holons related to the target holon by the named relationship.

The following `ReadableHolon` trait methods are explicitly not part of the MAP Commands API surface in v0:

- `is_accessible`
- `get_all_related_holons`
- `into_model`

These may remain available as internal/runtime APIs without becoming command-level actions.

#### 5.4.1.2 WritableHolonAction

    pub enum WritableHolonAction {
        WithPropertyValue { name: PropertyName, value: BaseValue },
        RemovePropertyValue { name: PropertyName },
        AddRelatedHolons { name: RelationshipName, holons: Vec<HolonReference> },
        RemoveRelatedHolons { name: RelationshipName, holons: Vec<HolonReference> },
        WithDescriptor { descriptor: HolonReference },
        WithPredecessor { predecessor: Option<HolonReference> },
    }

`WritableHolonAction` is the definitive list of mutating holon actions exposed through the MAP Commands API.

Discrete actions:

- `WithPropertyValue { name, value }`
  Sets or replaces a property value on the target holon.

- `RemovePropertyValue { name }`
  Removes a property value from the target holon.

- `AddRelatedHolons { name, holons }`
  Adds one or more related holon references under the named relationship.

- `RemoveRelatedHolons { name, holons }`
  Removes one or more related holon references from the named relationship.

- `WithDescriptor { descriptor }`
  Sets the descriptor reference of the target holon.

- `WithPredecessor { predecessor }`
  Sets or clears the predecessor reference of the target holon.

---

## 6. Runtime Structure and Dispatch

```rust
pub struct Runtime {
    active_space: Arc<HolonSpaceManager>,
}
```

Responsibilities:

- Bind Wire -> Domain
- Resolve transaction context
- Enforce descriptor policy
- Delegate execution
- Convert domain result -> Wire

### 6.1 Runtime Boundary Signature

```
impl Runtime {
    async fn dispatch(
        &self,
        request: MapIpcRequest,
    ) -> Result<MapIpcResponse, HolonError>;
}
```

`Runtime::dispatch` is the full sandwich boundary (ingress bread + filling delegation + egress bread).

### 6.2 Domain Dispatch

```rust
impl Runtime {
    fn dispatch_command(
        &self,
        command: MapCommand,
    ) -> Result<MapResult, HolonError> {
        match command {
            MapCommand::Space(cmd) => self.dispatch_space(cmd),
            MapCommand::Transaction(cmd) => self.dispatch_transaction(cmd),
            MapCommand::Holon(cmd) => self.dispatch_holon(cmd),
        }
    }
}
```

No `*Wire` types appear below binding.

Scope branching is structural routing only.  
Lifecycle and policy decisions are derived from descriptors.

---

## 7. Scope Execution Sequences

### 7.1 Space Scope

```text
MapIpcRequest(Space)
  → bind
  → dispatch_space
  → open_transaction
  → MapIpcResponse
```

---

### 7.2 Transaction Scope

```text
MapIpcRequest(Transaction)
  → bind (tx_id → TransactionContextHandle)
  → dispatch_transaction
  → TransactionContext
  → MapIpcResponse
```

---

### 7.3 Holon Scope

```text
MapIpcRequest(Holon)
  → bind (HolonReferenceWire → HolonReference)
  → dispatch_holon
  → HolonReference.method()
  → MapIpcResponse
```

---

## 8. Descriptor Enforcement Model

```rust
pub struct CommandDescriptor {
    pub is_mutating: bool,
    pub requires_open_tx: bool,
    pub requires_commit_guard: bool,
    pub snapshot_after: bool,
}
```

Runtime MUST:

1. Resolve descriptor
2. Validate lifecycle
3. Enforce commit guard if required
4. Trigger snapshot if required

Policy derives from descriptor metadata, not command enum branching.

---

## 9. Error Model

Domain error: `HolonError`

Error conversion occurs only at IPC seams using existing (default) Serialize and Deserialize.

---

## 10. Non-Goals

This specification does not:

- Introduce multi-space routing
- Define cross-space execution
- Redesign TrustChannel authority
- Replace transaction lifecycle semantics
- Implement undo/redo
- Define query optimization

---

## 11. Forward Evolution

Future extensions must preserve:

- Single IPC entrypoint
- Strict wire/domain separation
- Explicit structural scope
- Descriptor-driven policy
- Runtime as the sole execution boundary
- No wire leakage below binding seam
