# MAP Commands Specification (Phase 2.1 – v0.2)

## 1. Purpose and Design Intent

Phase 2.1 defines the canonical IPC command API for the Memetic Activation Platform (MAP).

This specification introduces, for the first time, a stable, structural command contract between the TypeScript experience layer and the Rust Integration Hub. The commands defined here are new at the IPC boundary. While many underlying domain operations already exist inside the Integration Hub (e.g., transaction mutation, holon reads and writes, lifecycle transitions), they were not previously expressed as a formal, structural IPC API surface.

Historically, IPC dispatch relied on string-based routing, mixed dispatch heuristics, implicit scope reconstruction, and execution authority inferred from session state. Policy logic was distributed across execution surfaces rather than centralized. Phase 2.1 replaces that model with a single, explicit command architecture.

This document defines:

- The canonical `MapCommand` structure
- The structural scope model (Space, Transaction, Holon)
- The authoritative execution boundary (`Runtime::dispatch`)
- The binding model for transactions and holon references
- Descriptor-driven execution policy
- Normative lifecycle enforcement responsibilities

This specification supersedes prior string-dispatch patterns and becomes the definitive IPC command surface for MAP.

---

## 2. Core Architectural Principles

Phase 2.1 is guided by the following principles.

### 2.1 Structural Authority

All execution authority MUST be structural and explicit.

Authority MUST NOT be inferred from:

- Transport metadata
- Session envelopes
- Implicit focal space
- Payload shape heuristics

Authority derives exclusively from:

- The structural `MapCommand`
- The resolved `TransactionContext`
- Descriptor-defined execution policy

---

### 2.2 Single Execution Boundary

All IPC execution MUST pass through a single boundary:

Tauri → Runtime → HolonSpaceManager → TransactionContext → HolonReference → Domain

The `Runtime` formalizes the execution root that previously existed only implicitly.

No command may bypass `Runtime`.

This ensures:

- A single authority gate
- A single descriptor enforcement point
- A single binding location
- No alternate dispatch paths

---

### 2.3 Descriptor-Driven Semantics

Command structure defines shape.

Command descriptors define policy.

Execution semantics such as:

- Whether a command mutates state
- Whether it requires an open transaction
- Whether commit guards must be enforced
- Whether snapshot persistence should occur

MUST derive from `CommandDescriptor`.

Structural enums describe scope and shape only. They MUST NOT embed policy logic.

---

### 2.4 Explicit Scope Model

Scope is first-class and structural.

Commands MUST declare their scope explicitly as one of:

- Space
- Transaction
- Holon

Scope MUST NOT be inferred from payload content, envelope metadata, or session state.

---

## 3. Architectural Boundary

All IPC execution MUST pass through:

```rust
Runtime::dispatch(request: MapRequest) -> MapResponse
```

This boundary is responsible for:

1. Scope resolution
2. Transaction resolution
3. Descriptor enforcement
4. Reference binding
5. Delegation to domain execution surfaces

The Runtime does not implement domain logic, reimplement lifecycle semantics, enforce trust authority, or maintain cross-space registries in v0.

It is a structural execution boundary, not a business object.

---

## 4. Runtime (v0)

### 4.1 Conceptual Role

`Runtime` is the canonical execution boundary for IPC commands.

It makes explicit what was previously distributed across Tauri handlers, receptor logic, session reconstruction paths, and transaction binding helpers.

### 4.2 Structure

```rust
pub struct Runtime {
    active_space: Arc<HolonSpaceManager>,
}
```

### 4.3 Invariants (v0)

- Exactly one active space exists per process.
- Runtime does not maintain a global space registry.
- Runtime does not perform cross-space routing.
- Runtime does not embed lifecycle logic.
- Runtime does not embed trust validation.

Future phases MAY extend these constraints, but Phase 2.1 intentionally keeps Runtime minimal.

---

## 5. IPC Envelope

### 5.1 MapRequest

```rust
pub struct MapRequest {
    pub request_id: RequestId,
    pub command: MapCommand,
}
```

The envelope is deliberately minimal.

It contains:

- A stable request identifier
- A fully structural command

It does not contain session-derived authority, implicit space context, or string-based dispatch keys.

### 5.2 MapResponse

```rust
pub struct MapResponse {
    pub request_id: RequestId,
    pub result: Result<MapResult, MapError>,
}
```

The response mirrors the request identifier and carries a deterministic result.

Errors MUST be serializable and MUST NOT leak internal implementation details.

---

---

## 6. Structural Scope Model

Scope is first-class and encoded structurally in `MapCommand`.

```rust
pub enum MapCommand {
    Space(SpaceCommand),
    Transaction(TransactionCommand),
    Holon(HolonCommand),
}
```

Scope MUST NOT be inferred from:

- Payload shape
- Envelope metadata
- Session state
- Implicit focal space

Each command belongs to exactly one scope.

---

## 7. Space Scope

```rust
pub enum SpaceCommand {
    BeginTransaction,
}
```

### 7.1 BeginTransaction

**Behavior**

- Calls `active_space.get_transaction_manager().open_default_transaction(...)`
- Returns a new `TxId`

**Rationale**

Opening a transaction is a space-level act. No transaction exists yet, therefore the command cannot be transaction-scoped.

**Constraints (v0)**

- Only one active space exists per process.
- `space_id` is not required.
- Multi-space resolution is deferred to future phases.

---

## 8. Transaction Scope

```rust
pub struct TransactionCommand {
    pub tx_id: TxId,
    pub action: TransactionAction,
}
```

Transaction scope represents execution authority bound to a specific transaction lifecycle.

### 8.1 Transaction Resolution

Runtime MUST:

1. Resolve `tx_id` using `TransactionManager::get_transaction`.
2. Return an error if the transaction does not exist.
3. Enforce descriptor lifecycle requirements.
4. Delegate execution to `TransactionContext` or its facades.

Runtime MUST NOT reimplement lifecycle logic.

---

### 8.2 TransactionAction (v0)

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

These actions correspond to transaction-level operations that are not bound to a single holon reference.

Lifecycle semantics remain defined by `TransactionContext`.

---

## 9. Holon Scope

```rust
pub struct HolonCommand {
    pub target: HolonReferenceWire,
    pub action: HolonAction,
}
```

Holon scope binds execution to a specific holon reference.

### 9.1 Holon Binding

Runtime MUST:

1. Resolve `HolonReferenceWire` into a runtime `HolonReference`.
2. Ensure the reference is associated with a valid `TransactionContext`.
3. Enforce descriptor requirements prior to execution.
4. Delegate to the corresponding façade method.

Holon scope ensures:

- The TypeScript layer never holds holon state.
- IntegrationHub remains the sole holder of HolonState.
- All state interaction crosses the IPC boundary.

---

## 10. HolonAction

HolonAction mirrors the public domain façade traits.

```rust
pub enum HolonAction {
    Read(ReadableHolonAction),
    Write(WritableHolonAction),
}
```

This preserves alignment between:

- Domain façade traits
- IPC command surface
- Descriptor-driven policy

---

## 11. ReadableHolonAction

ReadableHolonAction corresponds directly to methods on the `ReadableHolon` façade.

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

### Requirements

Readable actions:

- MUST NOT mutate state.
- MUST NOT trigger snapshot persistence.
- MUST respect transaction lifecycle requirements.
- MUST resolve through the bound `TransactionContext`.

Readable actions may still require lifecycle state validation depending on descriptor policy.

---

## 12. WritableHolonAction

WritableHolonAction corresponds directly to methods on the `WritableHolon` façade.

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

### Requirements

Writable actions:

- MUST require `TransactionLifecycleState::Open`.
- MUST respect host commit ingress guard if active.
- MUST trigger snapshot persistence if descriptor requires.
- MUST perform all mutation through `TransactionContext`-bound references.

Runtime MUST enforce descriptor policy before delegating to the façade.

---

## 13. CommandDescriptor

Command execution policy MUST derive from descriptor metadata.

```rust
pub struct CommandDescriptor {
    pub is_mutating: bool,
    pub requires_open_tx: bool,
    pub requires_commit_guard: bool,
    pub snapshot_after: bool,
}
```

### 13.1 Enforcement Model

Runtime MUST:

1. Resolve descriptor from `MapCommand`.
2. Enforce lifecycle constraints.
3. Enforce commit guard requirements.
4. Trigger snapshot persistence when `snapshot_after = true`.

Structural enums define scope and shape only.  
Policy MUST NOT be embedded directly in enum branching logic.

---

## 14. Binding Model

Binding occurs in two explicit phases.

### 14.1 Scope Binding

Resolve:

- Space authority
- Transaction context

This attaches execution authority to the command.

### 14.2 Reference Binding

Convert wire forms into runtime references:

- `HolonReferenceWire`
- `TransientReferenceWire`
- Other transaction-bound wire types

No domain execution may occur before both binding phases complete.

---

## 15. SessionStateWire Clarification

`SessionStateWire` MUST NOT:

- Carry execution authority
- Determine focal space
- Implicitly bind transaction scope

Session state MAY carry transport-level data only.

Execution authority MUST derive exclusively from `MapCommand`.

---

## 16. Error Conditions

Runtime MUST return deterministic errors for:

- Unknown transaction
- Invalid lifecycle state
- Commit in progress
- Descriptor policy violation
- Invalid holon binding

Errors MUST:

- Be serializable
- Avoid leaking internal implementation details
- Preserve request_id correlation

---

## 17. Tauri Integration

There MUST be exactly one IPC entrypoint:

```rust
#[tauri::command]
fn dispatch_map_command(
    state: State<Runtime>,
    request: MapRequest,
) -> Result<MapResponse, String>
```

All IPC commands MUST flow through this function.

Legacy string-dispatch entrypoints are deprecated.

---

## 18. Migration Requirements

Migration to Phase 2.1 MUST:

1. Introduce `MapCommand`.
2. Route all Tauri entrypoints through `Runtime::dispatch`.
3. Remove string-based dispatch.
4. Remove authority derivation from session state.
5. Centralize descriptor enforcement inside Runtime.

---

## 19. Non-Goals (v0)

This specification does not:

- Introduce multi-space routing.
- Define cross-space execution.
- Redesign TrustChannel authority.
- Implement undo/redo semantics.
- Replace transaction lifecycle semantics.
- Define graph query optimization.

Phase 2.1 clarifies structure and authority boundaries only.

---

## 20. Future Extensions

Future phases MAY introduce:

- Multi-space resolution.
- FocalSpaceResolver.
- Cross-space command propagation.
- Authorization descriptors.
- Snapshot and undo/redo integration.
- Query unification.

All future evolution MUST preserve:

- Structural scope clarity
- Descriptor-driven policy
- Runtime as the single execution boundary

---

End of Specification (Phase 2.1 – v0.2)