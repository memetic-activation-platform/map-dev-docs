# MAP Commands Specification (v0.3)

---

## 1. Purpose and Design Intent

This specification defines the canonical IPC command architecture for the Memetic Activation Platform (MAP).

It establishes a stable structural contract between:

- The TypeScript Experience Layer
- The Rust Integration Hub

All stateful execution occurs inside the Integration Hub. The Experience Layer performs no domain mutation and holds no holon state.

This specification formalizes:

- A single structural dispatch boundary
- An explicit scope model
- A strict wire/domain separation ("sandwich model")
- Descriptor-driven execution policy
- Deterministic lifecycle enforcement

This document is normative for the MAP IPC layer.

---

## 2. Architectural Context

This specification defines the MAP Command architecture within the **Conductora Tauri container**, as shown in the MAP Deployment Architecture.

![MAP Deployment Archi - v1.2 -- Detailed View.jpg](media/MAP%20Deployment%20Archi%20-%20v1.2%20--%20Detailed%20View.jpg)

MAP Commands form the structural IPC contract between the TypeScript Experience Layer and the Rust Integration Hub.

They exist exclusively within the Conductora container.

---

### 2.1 IPC Entry Point

All MAP Commands enter the system through a single Tauri IPC function:

```
dispatch_map_command
```

Call flow begins:

```
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

MAP Commands strictly separate transport types (“bread”) from behavioral domain types (“filling”).

#### Bread (Wire Types)

Wire types exist only:

- In the Tauri entrypoint
- Inside `Runtime::dispatch` during binding
- When constructing the response

Examples:

- `MapRequestWire`
- `MapResponseWire`
- `MapCommandWire`
- `HolonReferenceWire`
- `HolonErrorWire`

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

_**After binding completes no *Wire types remain.**_

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

The following function is the **single normative IPC ingress** into MAP domain execution:

```
#[tauri::command]
fn dispatch_map_command(
    state: State<Runtime>,
    request: MapRequestWire,
) -> Result<MapResponseWire, HolonErrorWire> {
    state.dispatch(request)
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

### 4.1 MapRequestWire

```
pub struct MapRequestWire {
    pub request_id: RequestId,
    pub command: MapCommandWire,
}
```

### 4.2 MapResponseWire

```
pub struct MapResponseWire {
    pub request_id: RequestId,
    pub result: Result<MapResultWire, HolonErrorWire>,
}
```

Wire types:

- Are serializable
- Contain identifiers only
- Contain no behavioral objects
- Must not cross below the binding seam

---

## 5. Domain Command Surface (Post-Binding)

These types exist only below the binding seam.

### 5.1 MapCommand

```
pub enum MapCommand {
    Space(SpaceCommand),
    Transaction(TransactionCommand),
    Holon(HolonCommand),
}
```

Scope is explicit and structural.

---

### 5.2 SpaceCommand

```
pub enum SpaceCommand {
    BeginTransaction,
}
```

---

### 5.3 TransactionCommand

```
pub struct TransactionCommand {
    pub context: TransactionContextHandle,
    pub action: TransactionAction,
}

pub enum TransactionAction {
    Commit,
    CreateTransientHolon { key: Option<MapString> },
    StageNewHolon { source: TransientReference },
    StageNewVersion { holon: SmartReference },
    LoadHolons { bundle: HolonReference },
    Dance(DanceInvocation),
    Lookup(LookupQuery),
}
```

No `tx_id` strings exist below binding.

---

### 5.4 HolonCommand

```
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

## 6. Runtime Structure and Dispatch

```
pub struct Runtime {
    active_space: Arc<HolonSpaceManager>,
}
```

Responsibilities:

- Bind Wire → Domain
- Resolve transaction context
- Enforce descriptor policy
- Delegate execution
- Convert domain result → Wire

---

### 6.1 Domain Dispatch

```
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

---

## 7. Scope Execution Sequences

### 7.1 Space Scope

```
MapRequestWire(Space)
  → bind
  → dispatch_space
  → open_transaction
  → MapResponseWire
```

---

### 7.2 Transaction Scope

```
MapRequestWire(Transaction)
  → bind (tx_id → TransactionContextHandle)
  → dispatch_transaction
  → TransactionContext
  → MapResponseWire
```

---

### 7.3 Holon Scope

```
MapRequestWire(Holon)
  → bind (HolonReferenceWire → HolonReference)
  → dispatch_holon
  → HolonReference.method()
  → MapResponseWire
```

---

## 8. Descriptor Enforcement Model

```
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

Policy derives from descriptor metadata, not enum branching.

---

## 9. Error Model

Domain error:

```
HolonError
```

Wire error:

```
HolonErrorWire
```

Conversion occurs only at the binding seam.

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