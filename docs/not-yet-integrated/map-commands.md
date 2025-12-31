## MAP Commands — Specification
*(Privileged TypeScript SDK ↔ Rust Client Interface)*

---

### Purpose

This document specifies the **MAP Commands interface**: a **privileged, local transport protocol** used by the **TypeScript MAP SDK** to convey requests to the **Rust Client**.

This interface exists to:

- provide a **single leverage point** for cross-cutting concerns (authorization gates, audit, telemetry, undo capability, transaction selection, routing)
- decouple **TypeScript ergonomics** from **Rust API structure**
- avoid exposing internal Rust objects (Holon pools, transactions, services) across the IPC boundary
- keep the TypeScript layer lightweight by exchanging only **serializable request/response envelopes** and **opaque capabilities**

**MAP Core developers do not use the Commands interface.**  
MAP Core developers use the **native Rust MAP Core API** directly (e.g., `ReadableHolon`, `WritableHolon`, `HolonOperationsApi`, etc.). The Commands interface is solely the **TS ↔ Rust client transport boundary**.

---

### Audience

- **TypeScript MAP SDK maintainers** (DAHN and Visualizer-facing SDK)
- **Rust Client implementers** (Conductora dispatch + Rust Client integration)
- MAP implementers working on the TS↔Rust boundary and associated cross-cutting concerns

Not intended for:
- MAP Core API authors working purely in Rust
- Suite authors
- TrustChannel / public Dance interface consumers

---

## 1. Architectural Positioning

### 1.1 Local Privileged Boundary

The Commands interface is used only within the privileged, co-located environment where:

- TypeScript runs in the UI/webview environment
- Rust Client runs in the Tauri host environment
- Communication is via **IPC** (not a network protocol)

```
DAHN / Visualizers
      ↓
TypeScript MAP SDK (ergonomic API)
      ↓
MAP Commands (MapRequest/MapResponse over IPC)
      ↓
Rust Client Command Dispatcher
      ↓
MAP Core Rust API (ReadableHolon, WritableHolon, HolonOperationsApi, etc.)
      ↓
Rust Client ↔ Holochain Guest (when needed)
```

### 1.2 Not a Public Interface

MAP Commands are not exposed:
- over TrustChannels
- to remote AgentSpaces
- to external clients

Public interoperability is achieved through:
- **Dances** (and TrustChannels), not Commands

**Invariant**  
MAP Commands MUST remain a privileged local IPC interface.

---

## 2. Core Design Goals

1. **Preserve Rust-native API quality**  
   Rust Core APIs stay idiomatic and do not contort around transport constraints.

2. **Enable ergonomic TypeScript SDKs**  
   TypeScript sees method-like APIs (ReadableHolon, WritableHolon, etc.) while the SDK internally emits commands.

3. **Prevent state ping-pong**  
   Transaction internals (Holon pools, undo registries, staged/transient structures) never cross the boundary.

4. **Centralize cross-cutting concerns**  
   A single dispatch path provides a natural interception point for:
    - authorization checks (local policy gates)
    - telemetry/audit
    - undo capability issuance
    - transaction scoping and isolation
    - routing decisions (local vs guest execution)

---

## 3. Execution Scoping

### 3.1 Context Selection (TS → Rust)

Each command executes relative to a **Context** resolved inside the Rust Client.

- TypeScript provides an opaque `ContextId`
- Rust resolves `ContextId` to a `HolonsContextBehavior` implementation
- From that context, Rust can access:
    - `HolonSpaceManagerBehavior`
    - the LocalHolonSpace (indirectly)
    - services and routing policy
    - transaction resolution (if applicable)

TypeScript never receives context internals.

### 3.2 Transaction Selection (TS → Rust)

TypeScript must be able to specify **which transaction scope** a command executes within.

- TypeScript provides an opaque `TransactionId`
- Rust resolves it within the selected context
- Both **queries and mutations** execute within transaction scope when `transaction_id` is provided
- Transaction scoping is required for correct resolution of `HolonReference`s and isolation

TypeScript never receives:
- StagedHolonPool
- TransientHolonPool
- UndoRegistry
- Transaction state objects of any kind

**Invariant**  
TypeScript may select transaction scope, but the Rust Client owns and materializes all transaction state.

---

## 4. Command Classification

### 4.1 Query vs Mutation

Commands are structurally partitioned into:

- **Query Commands**
    - non-mutating
    - may execute within a transaction scope to preserve isolation and reference resolution
    - never produce undo capability

- **Mutation Commands**
    - mutate MAP state within a transaction
    - require `transaction_id`
    - may produce undo capability (pre-commit only)

---

## 5. Transport Protocol

### 5.1 MapRequest

`MapRequest` is the IPC payload sent from TypeScript to Rust.

```rust
pub struct MapRequest {
    /// Unique identifier for dispatch/tracing on the Rust side.
    pub name: String,

    /// Query or Mutation classification.
    pub command_kind: CommandKind,

    /// Command payload.
    pub body: CommandBody,

    /// Execution context selector (resolved by Rust Client).
    pub context: ContextId,

    /// Optional transaction selector (resolved by Rust Client).
    /// Required for mutations; optional for queries.
    pub transaction_id: Option<TransactionId>,
}
```

```rust
pub enum CommandKind {
    Query,
    Mutation,
}
```

### 5.2 CommandBody

```rust
pub enum CommandBody {
    Query(QueryCommand),
    Mutation(MutationCommand),
}
```

This spec defines the canonical command taxonomy used by the TS SDK.

---

## 6. Command Taxonomy

The CommandBody taxonomy mirrors the *conceptual* TS SDK surface:

- **Holon Commands** (reference-scoped; “methods on a HolonReference”)
- **Operations Commands** (standalone; “HolonOperationsApi-like”)
- **Dance Commands** (generic dance invocation)

### 6.1 HolonQuery (reference-scoped)

```rust
pub enum HolonQuery {
    GetPropertyValue { target: HolonReference, property_name: PropertyName },
    GetRelatedHolons { target: HolonReference, relationship_name: RelationshipName },
    EssentialContent { target: HolonReference },
    Key { target: HolonReference },
    VersionedKey { target: HolonReference },
    Predecessor { target: HolonReference },
    AllRelatedHolons { target: HolonReference },
}
```

### 6.2 HolonMutation (reference-scoped)

```rust
pub enum HolonMutation {
    WithPropertyValue { target: HolonReference, property_name: PropertyName, value: BaseValue },
    RemovePropertyValue { target: HolonReference, property_name: PropertyName },
    AddRelatedHolons { target: HolonReference, relationship_name: RelationshipName, holons: Vec<HolonReference> },
    RemoveRelatedHolons { target: HolonReference, relationship_name: RelationshipName, holons: Vec<HolonReference> },
    WithPredecessor { target: HolonReference, predecessor: Option<HolonReference> },
    WithDescriptor { target: HolonReference, descriptor: HolonReference },
}
```

### 6.3 OperationsQuery (standalone)

```rust
pub enum OperationsQuery {
    GetAllHolons,
    StagedCount,
    TransientCount,
    SummarizeHolons { holons: Vec<HolonReference> },
    GetStagedHolonByBaseKey { key: MapString },
    GetStagedHolonByVersionedKey { key: MapString },
    GetTransientHolonByBaseKey { key: MapString },
    GetTransientHolonByVersionedKey { key: MapString },
}
```

### 6.4 OperationsMutation (standalone)

```rust
pub enum OperationsMutation {
    NewHolon { key: Option<MapString> },
    StageNewHolon { transient: TransientReference },
    StageNewFromClone { original: HolonReference, new_key: MapString },
    StageNewVersion { current_version: SmartReference },
    DeleteHolon { local_id: LocalId },
    LoadHolons { bundle: TransientReference },
    Commit,
    Rollback,
    Undo { token: UndoToken },
}
```

### 6.5 Dance Commands (generic invocation)

Dance invocation is included as a command category to support extensibility.

```rust
pub enum DanceCommand {
    InvokeDance { dance_name: String, request: BaseValue /* or structured holon ref */ },
}
```

Exact dance request/response encoding is defined in the Dances spec; the Commands layer provides a local transport wrapper.

---

## 7. MapResponse

`MapResponse` is the IPC response sent from Rust to TypeScript.

```rust
pub struct MapResponse {
    pub name: String,
    pub command_kind: CommandKind,
    pub status: CommandStatus,
    pub body: Option<CommandResponse>,
    pub errors: Vec<HolonError>,
    pub undo: Option<UndoToken>,
}
```

```rust
pub enum CommandStatus {
    Ok,
    Error,
}
```

**Invariants**
- `undo` MUST be `None` for all Query commands
- `undo` MAY be present for successful Mutation commands
- failed Mutation commands MUST NOT return undo capability

### 7.1 CommandResponse

```rust
pub enum CommandResponse {
    Query(QueryResponse),
    Mutation(MutationResponse),
}
```

```rust
pub enum QueryResponse {
    BaseValue(Option<BaseValue>),
    HolonCollection(HolonCollection),
    EssentialContent(EssentialHolonContent),
    Reference(Option<HolonReference>),
    References(Vec<HolonReference>),
    Count(i64),
    Summary(String),
}
```

```rust
pub enum MutationResponse {
    Reference(HolonReference),
    References(Vec<HolonReference>),
    CommitResponse(TransientReference),
    Unit,
}
```

---

## 8. Undo Capability Semantics (Transport-Level)

Undo at this layer is a **capability**, not a state replication mechanism.

- Rust may return an opaque `UndoToken` after successful mutations
- TypeScript may store and order tokens as part of UI undo/redo orchestration
- Undo tokens are:
    - transaction-scoped
    - single-use
    - invalid after commit

Undo execution is performed by sending `OperationsMutation::Undo { token }`.

Post-commit reversal is not “undo”; it is modeled as compensating transactions and is out of scope for this transport spec.

---

## 9. TypeScript Binding Requirements

The TypeScript SDK must:

- expose ergonomic, method-like APIs
- compile those calls into `MapRequest` objects
- preserve structural parity of command payload shapes
- select `context` and `transaction_id` explicitly
- never materialize or depend on Rust execution objects

The TypeScript SDK must not:

- receive or manipulate transaction state
- receive Holon pools or undo registries
- infer execution scope implicitly

---

## 10. Rust Client Responsibilities

The Rust Client command dispatcher must:

- resolve `ContextId` to a `HolonsContextBehavior`
- resolve `TransactionId` (if present) within that context
- enforce Query vs Mutation invariants
- execute the command by calling the Rust-native MAP Core APIs
- return typed responses and errors
- optionally issue undo capability tokens for successful mutations
- ensure no execution-state structures cross the IPC boundary

---

## Summary

The MAP Commands interface is:

- a **privileged IPC transport** between the TypeScript MAP SDK and the Rust Client
- not used by MAP Core developers (who use the Rust APIs directly)
- context-resolved and transaction-scoped
- strictly separated into Query and Mutation commands
- designed to avoid state ping-pong while preserving isolation and correctness
- the single leverage point for cross-cutting host-side concerns at the TS↔Rust boundary