# MAP Commands Specification (v1.0.0)

---

## 1. Purpose and Design Intent

This specification defines the canonical IPC command architecture for the Memetic Activation Platform (MAP).
MAP Commands define the **IPC contract between the TypeScript client (Experience Layer) and the Conductora host runtime (Rust Integration Hub)**. They provide a strongly typed interface through which the client invokes MAP domain operations inside the IntegrationHub runtime. All stateful execution occurs inside the Integration Hub. The Experience Layer performs no domain mutation and holds no holon state.

MAP Commands are NOT intended to serve as a universal protocol for all MAP communication channels. Other subsystems (such as Trust Channels, host–guest bridges, or storage replay mechanisms) may use different transport formats and adapters.

This specification formalizes the MAP IPC command architecture, including:

- A single structural dispatch boundary
- A split host adapter / runtime execution model
- An explicit scope model
- A strict wire/domain separation ("sandwich model")
- Descriptor-driven execution policy
- Deterministic lifecycle enforcement

This document is normative for the MAP IPC layer.

---

## 2. Architectural Context

This specification defines the MAP Command architecture within the Conductora Tauri container, as shown in the MAP Deployment Architecture.

![MAP Deployment Archi - v1.2 -- Detailed View.jpg](../media/MAP%20Deployment%20Archi%20-%20v1.2%20--%20Detailed%20View.jpg)

MAP Commands form the structural IPC contract between the TypeScript Experience Layer and the Rust Integration Hub.

They exist exclusively within the Conductora container.

The current implementation is split across three crates with strict dependency direction:

- `map_commands_contract`
  - owns domain contract types
  - `MapCommand`, `SpaceCommand`, `TransactionCommand`, `HolonCommand`
  - `MapResult`
  - `CommandDescriptor`
- `map_commands_wire`
  - owns IPC transport and wire types
  - `MapIpcRequest`, `MapIpcResponse`
  - `MapCommandWire`
  - `MapResultWire`
  - `*Wire` variants
- `map_commands_runtime`
  - owns runtime execution
  - `Runtime`
  - `RuntimeSession`
  - scope-specific handlers
  - lifecycle enforcement

Dependency direction:

- `map_commands_wire` depends on `map_commands_contract`
- `map_commands_runtime` depends on `map_commands_contract`
- `map_commands_runtime` does not depend on `map_commands_wire`

---

### 2.1 IPC Entry Point

All MAP Commands enter the system through a single Tauri IPC function:

`dispatch_map_command`

Call flow begins:

```text
TypeScript
  → Tauri invoke("dispatch_map_command")
    → dispatch_map_command
    → bind wire → domain
    → Runtime::execute_command
    → domain result → wire result
```

The Tauri entrypoint is the single IPC ingress.

It:

- Accepts wire types
- Owns IPC envelope handling
- Performs wire-to-domain binding
- Delegates bound commands to Runtime
- Maps domain results back into wire results
- Must not execute domain behavior directly

The Tauri adapter layer is not the domain execution boundary.

`dispatch_map_command` remains the only IPC entrypoint for MAP command execution.

---

### 2.2 Runtime Boundary

`Runtime` is the single domain execution and policy boundary for bound MAP commands.

It is responsible for:

- Accepting bound domain commands
- Enforcing descriptor policy
- Delegating to scope-specific handlers
- Returning domain results

It is not responsible for:

- owning the IPC envelope
- parsing `MapIpcRequest`
- constructing `MapIpcResponse`
- holding `*Wire` types

No bound command may bypass Runtime.

---

### 2.3 The Sandwich Model (Wire vs Domain)

MAP Commands strictly separate transport types ("bread") from behavioral domain types ("filling").

#### Bread (Wire Types)

Wire types exist only:

- In the Tauri entrypoint
- In the host-side MAP command adapter during binding
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
- `Arc<TransactionContext>`
- `HolonError`

Domain types:

- Contain behavior
- Contain transaction-bound references
- Must not depend on serialization
- Must not reference any `*Wire` types

The sandwich is now split across two host-side layers:

- Tauri adapter layer
  - owns IPC envelope handling
  - performs wire-to-domain binding
  - performs domain-to-wire result mapping
- Runtime layer
  - owns lifecycle enforcement
  - routes bound domain commands to handlers
  - executes domain behavior

Wire-to-domain binding occurs exclusively inside the host-side MAP command adapter layer before runtime execution begins.

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
type RuntimeState = RwLock<Option<Runtime>>;

#[tauri::command]
async fn dispatch_map_command(
    request: MapIpcRequest,
    runtime_state: State<'_, RuntimeState>,
) -> Result<MapIpcResponse, HolonError> {
    // adapter logic:
    // 1. acquire initialized Runtime
    // 2. bind wire -> domain
    // 3. call Runtime::execute_command
    // 4. map MapResult -> MapResultWire
}
```

Normative requirements:

- This MUST be the only IPC command that initiates MAP domain execution.
- It MUST accept only wire-layer types.
- It MUST fail if runtime state is not initialized.
- It MUST perform wire-to-domain binding before runtime execution begins.
- It MUST delegate bound commands to runtime execution.
- It MUST convert domain results into wire results.
- It MUST perform no scope inference.
- It MUST perform no domain behavior directly.

All domain execution authority begins inside `Runtime::execute_command`.

---

## 4. IPC Envelope (Wire Layer)

### 4.1 MapIpcRequest

```rust
pub struct MapIpcRequest {
    pub request_id: RequestId,
    pub command: MapCommandWire,
    pub options: RequestOptions,
}

pub struct RequestOptions {
    pub gesture_id: Option<GestureId>,
    pub gesture_label: Option<String>,
    pub snapshot_after: bool,
}
```

`RequestId` is currently a `MapInteger` wrapper, not a plain integer.

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
    pub context: Arc<TransactionContext>,
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
        Query(QueryExpression),
        GetAllHolons,
        GetStagedHolonByBaseKey { key: MapString },
        GetStagedHolonsByBaseKey { key: MapString },
        GetStagedHolonByVersionedKey { key: MapString },
        GetTransientHolonByBaseKey { key: MapString },
        GetTransientHolonByVersionedKey { key: MapString },
        StagedCount,
        TransientCount,
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

- `Query(QueryExpression)`
  Executes a query expression against transaction-visible state.

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
    pub context: Arc<TransactionContext>,
    pub target: HolonReference,
    pub action: HolonAction,
}

pub enum HolonAction {
    Read(ReadableHolonAction),
    Write(WritableHolonAction),
}
```

Holon commands carry both:

- a bound transaction context for lifecycle and mutation-policy enforcement
- a bound holon target for holon-local behavior

Dispatch routing does not stop at `HolonReference` alone; runtime policy evaluation still depends on command context.

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

---

## 6. Runtime Structure and Dispatch

```rust
pub struct Runtime {
    session: Arc<RuntimeSession>,
}
```

Responsibilities:

- Accept bound domain commands
- Enforce descriptor policy
- Route to scope-specific handlers
- Execute domain behavior
- Return domain results

### 6.1 Runtime Boundary Signature

```
impl Runtime {
    pub async fn execute_command(
        &self,
        command: MapCommand,
    ) -> Result<MapResult, HolonError>;
}
```

`Runtime::execute_command` is the normative runtime API.

It accepts already-bound domain commands.

IPC envelope handling and wire conversion occur in the host adapter layer, not in runtime.

### 6.2 Runtime Session

```rust
pub struct RuntimeSession {
    // owns runtime-visible session and transaction state
}
```

`RuntimeSession` is the runtime-owned session and transaction layer.

It is responsible for:

- transaction resolution during binding support
- active runtime session state
- access to transaction-scoped execution objects

### 6.3 Scope-Specific Handlers

```rust
impl Runtime {
    fn execute_command_internal(
        &self,
        command: MapCommand,
    ) -> Result<MapResult, HolonError> {
        match command {
            MapCommand::Space(cmd) => self.handle_space(cmd),
            MapCommand::Transaction(cmd) => self.handle_transaction(cmd),
            MapCommand::Holon(cmd) => self.handle_holon(cmd),
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
  → bind in Tauri adapter
  → Runtime::execute_command
  → handle_space
  → MapResult
  → wire response mapping
```

---

### 7.2 Transaction Scope

```text
MapIpcRequest(Transaction)
  → bind in Tauri adapter (tx_id → Arc<TransactionContext>)
  → Runtime::execute_command
  → handle_transaction
  → TransactionContext
  → MapResult
  → wire response mapping
```

---

### 7.3 Holon Scope

```text
MapIpcRequest(Holon)
  → bind in Tauri adapter (HolonReferenceWire + tx context → HolonCommand)
  → Runtime::execute_command
  → handle_holon
  → HolonReference.method()
  → MapResult
  → wire response mapping
```

---

## 8. Descriptor Enforcement Model

```rust
pub struct CommandDescriptor {
    pub mutation: MutationClassification,
    pub requires_open_tx: bool,
    pub requires_commit_guard: bool,
}

pub enum MutationClassification {
    ReadOnly,
    Mutating,
    RuntimeDetected,
}
```

Runtime MUST:

1. Resolve descriptor
2. Validate lifecycle
3. Enforce commit guard if required

Policy derives from descriptor metadata, not command enum branching.

Lifecycle semantics are scope-sensitive:

- Transaction-scoped read-only commands still require an open transaction.
- Holon-scoped read-only commands do not necessarily require an open transaction, because committed-transaction references may remain readable.
- Mutating commands remain subject to open-transaction and commit-guard requirements as described by their descriptor.

`snapshot_after` is not currently part of `CommandDescriptor`.

If snapshot behavior is requested, it is carried in `RequestOptions` as request metadata at the IPC layer rather than as descriptor metadata in the current implementation.

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
- Runtime as the sole domain execution boundary for bound commands
- No wire leakage below binding seam
