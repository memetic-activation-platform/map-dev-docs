# MAP Commands Specification (v0.3)

---

## 1. Purpose and Design Intent

This specification defines the canonical IPC command architecture for the Memetic Activation Platform (MAP).

It establishes a stable structural contract between:

- The TypeScript experience layer
- The Rust Integration Hub

All stateful execution occurs inside the Integration Hub. The experience layer performs no domain mutation and holds no holon state.

This specification formalizes:

- A single structural dispatch boundary
- An explicit scope model
- A strict wire/domain separation ("sandwich model")
- Descriptor-driven execution policy
- Deterministic lifecycle enforcement

This document is normative for the MAP IPC layer.

---

## 2. Architectural Context

The MAP IPC boundary sits between:

- The TypeScript experience layer
- The Rust Integration Hub

All IPC commands must pass through exactly one execution boundary:

    Runtime::dispatch

The core reference layer (HolonReference, StagedReference, SmartReference, TransientReference) is self-resolving. Holon references are transaction-bound and carry their own execution context internally.

The IPC layer does not inject transaction context into reference methods.

No command may bypass Runtime.

---

## 3. The Sandwich Model: Wire vs Domain

MAP IPC strictly separates transport types (bread) from behavioral domain types (filling).

### 3.1 Bread: Wire Types

Wire types exist only at the IPC boundary.

Examples:

- MapRequestWire
- MapResponseWire
- MapCommandWire
- HolonReferenceWire
- HolonErrorWire

Wire types:

- Are serializable
- Contain identifiers (tx_id, holon_id, etc.)
- Do not contain behavioral objects
- Do not contain TransactionContextHandle
- Do not contain HolonReference
- Must not cross into domain execution

Wire types exist only:

- In the Tauri entrypoint
- Inside Runtime::dispatch during binding
- When constructing the response

They must not appear below the binding seam.

---

### 3.2 Filling: Domain Types

Domain types are behavioral objects.

Examples:

- MapCommand
- SpaceCommand
- TransactionCommand
- HolonCommand
- HolonReference
- TransactionContextHandle
- HolonError

Domain types:

- Contain behavior
- Contain transaction-bound references
- Contain context handles
- Must not depend on serialization
- Must not reference any Wire types

Below the binding seam, no Wire types may exist.

---

### 3.3 The Binding Seam

Binding occurs exclusively inside:

    Runtime::dispatch

Binding responsibilities:

- Convert MapCommandWire → MapCommand
- Resolve tx_id → TransactionContextHandle
- Convert HolonReferenceWire → HolonReference
- Validate structural integrity
- Prepare domain objects for execution

After binding completes:

    No *Wire types remain.

---

## 4. IPC Envelope (Wire Layer)

The IPC envelope defines the transport structure only.

### 4.1 MapRequestWire

    pub struct MapRequestWire {
        pub request_id: RequestId,
        pub command: MapCommandWire,
    }

The envelope contains:

- A correlation identifier
- A structural wire command

It contains no implicit authority and no lifecycle hints.

---

### 4.2 MapResponseWire

    pub struct MapResponseWire {
        pub request_id: RequestId,
        pub result: Result<MapResultWire, HolonErrorWire>,
    }

Responses must:

- Mirror request_id
- Return deterministic results
- Serialize domain errors into HolonErrorWire
- Avoid leaking internal implementation details

---

## 5. Domain Command Surface (Post-Binding)

The following types are domain-level command types. They are not serialized over IPC.

### 5.1 MapCommand (Domain)

    pub enum MapCommand {
        Space(SpaceCommand),
        Transaction(TransactionCommand),
        Holon(HolonCommand),
    }

Scope is explicit and structural.

No scope may be inferred from session state.

---

### 5.2 Space Commands

    pub enum SpaceCommand {
        BeginTransaction,
    }

Opening a transaction is space-scoped because no transaction exists yet.

---

### 5.3 Transaction Commands

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

TransactionCommand contains a resolved TransactionContextHandle.

No tx_id strings exist below binding.

---

### 5.4 Holon Commands

    pub struct HolonCommand {
        pub target: HolonReference,
        pub action: HolonAction,
    }

    pub enum HolonAction {
        Read(ReadableHolonAction),
        Write(WritableHolonAction),
    }

HolonReference is transaction-bound and self-resolving.

Dispatch stops at HolonReference.

---

## 6. Runtime and Tauri Integration

There is exactly one IPC entrypoint.

All execution flows through Runtime.

---

### 6.1 Tauri Entrypoint (Bread)

    use tauri::State;

    #[tauri::command]
    fn dispatch_map_command(
        state: State<Runtime>,
        request: MapRequestWire,
    ) -> Result<MapResponseWire, String> {
        state.dispatch(request)
             .map_err(|e| e.to_string())
    }

This function:

- Accepts only wire types
- Delegates immediately to Runtime
- Performs no scope inference
- Performs no lifecycle enforcement
- Performs no descriptor policy branching

It is transport only.

---

### 6.2 Runtime as Binding + Execution Boundary

    pub struct Runtime {
        active_space: Arc<HolonSpaceManager>,
    }

    impl Runtime {
        pub fn dispatch(
            &self,
            request: MapRequestWire,
        ) -> Result<MapResponseWire, HolonErrorWire> {

            // 1. Bind wire → domain
            let command = self.bind_command(request.command)?;

            // 2. Execute domain command
            let result = self.dispatch_command(command)?;

            // 3. Convert domain result → wire
            Ok(MapResponseWire {
                request_id: request.request_id,
                result: Ok(MapResultWire::from(result)),
            })
        }
    }

Runtime is the sandwich seam.

Below bind_command:

    No Wire types may exist.

---

### 6.3 Dispatch Structure (Domain Layer)

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

        fn dispatch_space(
            &self,
            cmd: SpaceCommand,
        ) -> Result<MapResult, HolonError> {
            unimplemented!()
        }

        fn dispatch_transaction(
            &self,
            cmd: TransactionCommand,
        ) -> Result<MapResult, HolonError> {
            unimplemented!()
        }

        fn dispatch_holon(
            &self,
            cmd: HolonCommand,
        ) -> Result<MapResult, HolonError> {
            unimplemented!()
        }
    }

All dispatch functions operate strictly on domain types.

No *Wire types appear here.

---

### 6.4 Execution Invariant

All IPC execution follows:

    TypeScript
      → Tauri
        → dispatch_map_command
          → Runtime::dispatch (binding seam)
            → dispatch_command (domain)
              → scope-specific execution
            → result conversion
          → MapResponseWire

Runtime is the single structural execution boundary.

---

## 7. Scope-Specific Dispatch Sequences

This section defines domain execution flow after binding.

---

### 7.1 Space Scope

    TypeScript
      → MapRequestWire(Space)
      → Runtime::dispatch
        → bind_command
        → dispatch_space
          → HolonSpaceManager
            → TransactionManager::open_transaction
        → MapResponseWire

Space scope does not bind a transaction prior to execution.

---

### 7.2 Transaction Scope

    TypeScript
      → MapRequestWire(Transaction)
      → Runtime::dispatch
        → bind_command
            tx_id → TransactionContextHandle
        → dispatch_transaction
            → TransactionContext
              → execute action
        → MapResponseWire

Lifecycle validation derives from descriptor policy.

---

### 7.3 Holon Scope

    TypeScript
      → MapRequestWire(Holon)
      → Runtime::dispatch
        → bind_command
            HolonReferenceWire → HolonReference
        → dispatch_holon
            → HolonReference.method()
                (self-resolving)
        → MapResponseWire

Dispatch stops at HolonReference.

HolonReference delegates internally to Smart, Staged, or Transient implementations.

Runtime does not inject transaction context into reference methods.

---

## 8. Descriptor Enforcement Model

Command execution policy derives exclusively from CommandDescriptor.

    pub struct CommandDescriptor {
        pub is_mutating: bool,
        pub requires_open_tx: bool,
        pub requires_commit_guard: bool,
        pub snapshot_after: bool,
    }

Runtime must:

1. Resolve descriptor
2. Validate lifecycle state
3. Enforce commit guard if required
4. Trigger snapshot if required

Structural enums define shape only.

Policy is not embedded in branching logic.

---

## 9. Error Model

Domain error type:

    HolonError

IPC error type:

    HolonErrorWire

Conversion occurs only at the binding boundary.

Runtime must return deterministic errors for:

- Unknown transaction
- Invalid lifecycle state
- Commit in progress
- Descriptor violation
- Invalid holon binding

Errors must be correlated by request_id.

No alternate error hierarchy is permitted.

---

## 10. Migration Requirements

Migration to this architecture requires:

1. Replacing string-based routing with MapCommandWire
2. Routing all IPC through Runtime::dispatch
3. Removing session-derived authority
4. Enforcing the sandwich model
5. Ensuring no Wire types cross into domain execution

---

## 11. Non-Goals

This specification does not:

- Introduce multi-space routing
- Define cross-space execution
- Redesign TrustChannel authority
- Replace transaction lifecycle semantics
- Implement undo/redo
- Define query optimization

---

## 12. Forward Evolution

Future extensions may introduce:

- Multi-space focal space resolution
- Cross-space routing
- Authorization descriptors
- Undo/redo integration
- Unified query command surface

All future extensions must preserve:

- Explicit structural scope
- Strict wire/domain separation
- Descriptor-driven execution
- Runtime as the single execution boundary
- No Wire leakage below binding seam

---