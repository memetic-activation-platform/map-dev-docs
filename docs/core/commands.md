# MAP Commands — Rust Client Dispatch & Execution
*(Transaction-Centric Execution Model)*

**Status:** Converged (Architectural Baseline)
**Audience:** MAP Core Rust Client developers, Conductora maintainers
**Scope:** Rust-side command dispatch, execution, and enforcement

This document defines the **Rust Client responsibilities** for executing MAP Commands under the **transaction-centric 
execution model**.

It intentionally excludes:
- TypeScript SDK API design
  (see `map-ts-sdk-impl.md`)
- Undo / redo experience semantics
  (see **MAP Core — Pre-Commit Transaction Editing Model**)

---

## 1. Architectural Positioning

### 1.1 Privileged Local Boundary

MAP Commands exist only at the **privileged IPC boundary** between:

- the TypeScript MAP SDK (caller)
- the Rust Client / **Integration Hub** (executor)

They are:
- not public APIs
- not exposed over Trust Channels
- not usable by remote agents

The Integration Hub is the **sole authority** responsible for:
- transaction resolution
- command execution
- invariant enforcement
- undo enforcement (but not orchestration)

---

## 2. Framing Shift: Transactions as Execution Context

### 2.1 Historical Context (Now Deprecated)

Historically, execution was mediated through a `HolonsContextBehavior` abstraction that wrapped a `SpaceManager` and indirectly exposed:

- nursery
- transient state
- caches
- services

This indirection added complexity without enforcing correctness.

---

### 2.2 Current Model (Authoritative)

**The Transaction is the execution context.**

Each Transaction:
- belongs to exactly one Space
- is isolated from other transactions
- owns *all* provisional and session-local state

This includes:
- nursery (staged holons)
- transient holon manager
- transaction-local caches
- linear undo chain
- open / committed / rolled-back status

The Integration Hub executes **all commands relative to a Transaction**.

---

### 2.3 Experience-Layer Responsibilities (TypeScript Client)

While this document specifies Integration Hub behavior, it is important to clarify the
responsibilities of the experience layer (TypeScript client) with respect to Space
and Transaction selection.

The TypeScript client is responsible for:

- Selecting the **focal Space** from among the Spaces to which the human belongs
- Requesting the creation of a **Transaction within that Space**
- Determining which commands are executed within a given Transaction
- Determining when a Transaction is committed or rolled back

These responsibilities reflect **experience-level intent and orchestration**.
They do not imply ownership of execution state.

The TypeScript client does **not**:
- own or materialize Transactions
- manage provisional state
- resolve references
- enforce isolation or undo correctness

All execution guarantees are enforced by the Integration Hub via the HolonSpaceManager.

---

## 3. Space, HolonSpaceManager, and Transaction Responsibilities

### 3.1 Holon Space (Backing Store)

At the persistence layer, a **Holon Space** is a Holochain DHT.

- Each Holon Space has exactly one persisted **HolonSpace HolonNode**
- This holon serves as the durable, authoritative anchor for the space
- The backing store has no concept of transactions, provisional state, or undo

---

### 3.2 HolonSpaceManager (Integration Hub Runtime)

In the Integration Hub, a **HolonSpaceManager** is the long-lived runtime authority for a Holon Space.

It:
- holds an in-memory `HolonReference` to the persisted HolonSpace holon
- mediates access to persistence, caches, and dances
- owns the **set and lifecycle of Transactions** for that space

The HolonSpaceManager **does not own provisional state directly**.

Instead, it creates and manages Transactions, delegating all provisional execution state to them.

---

### 3.3 Transactions (Execution Context)

A **Transaction** is an ephemeral, space-scoped execution context created by a HolonSpaceManager.

Each Transaction owns:
- its own Nursery (staged holons)
- its own TransientHolonManager
- transaction-local cache routing
- a linear undo chain
- open / committed / rolled-back status

Transactions are the unit of:
- execution
- isolation
- undo validity

All command execution occurs relative to a Transaction.

---

## 4. Self-Resolving References (Critical Consequence)

### 4.1 Embedded Transaction Identity

All `HolonReference` variants embed their **Transaction identity**, including:

- `SmartReference`
- `StagedReference`
- `TransientReference`

This ensures:
- references are self-resolving
- cross-transaction misuse is structurally impossible
- no external “context matching” is required

Resolution chain is intrinsic:

HolonReference
→ Transaction
→ HolonSpaceManager
→ HolonSpace + services

The Integration Hub **must never attempt to reinterpret or rebind references**.

---

## 5. Command Intent Model

### 5.x Why Commands Exist (Design Rationale)

Although the TypeScript experience layer could, in principle, invoke MAP Core Rust APIs in a one-to-one fashion, 
MAP deliberately introduces a **single Command abstraction** as the *only* human-facing execution surface into the Integration Hub.

This is a **conscious architectural choice**, not an API convenience.

The Command abstraction provides a **stable and enforceable boundary** between:

- **human intent** (imperative editing gestures), and
- **core execution** (transactional domain logic)

Commands exist because they enable guarantees that direct API calls cannot provide:

- **Centralized enforcement**
  All human-initiated behavior is funneled through a single interception point where the Integration Hub can enforce 
  transaction scoping, authorization, mutation safety, and undo eligibility.

- **Explicit intent in the type system**
  By structurally distinguishing Queries from Mutations, Commands make intent explicit and enforceable without heuristics or inference.

- **Transport and host decoupling**
  MAP Core remains entirely unaware of IPC, Tauri, serialization, or UI runtimes. The Command envelope absorbs all host and transport concerns without contaminating core APIs.

- **Experience-level undo alignment**
  Commands define the atomic unit of human-observable change, which is essential for coherent experience-level undo and redo semantics.

- **Extensibility without core pollution**
  New execution patterns (such as dance invocation or orchestration) can be introduced without expanding or destabilizing the MAP Core API surface.

- **Auditability and observability**
  Commands provide a natural unit for tracing, logging, metrics, and debugging across layers.

In short:

**Commands are not a façade over MAP Core APIs.
They are the architectural control surface that preserves core purity while enabling strong guarantees at the human-facing boundary.**

### 5.1 Structural Partitioning

Commands are structurally classified by intent:

    pub enum CommandBody {
        Query(QueryCommand),
        Mutation(MutationCommand),
    }

The structural similarity to CQRS is **intentional**, but this is **not a full CQRS architecture**.

MAP maintains:
- a single execution pipeline
- a unified state model
- no separate read/write subsystems

The Query / Mutation partition exists solely to make **intent explicit in the type system**.
This enables declarative enforcement of:
- authorization
- undo and redo eligibility
- replay safety
- mutation constraints

This partition is a **classification mechanism**, not an architectural split.

---

### 5.2 Query Commands

Queries:
- do not mutate state
- may execute within a Transaction for isolation
- never participate in undo
- are safe to replay

The Integration Hub **must reject** any observable state change during query execution.

---

### 5.3 Mutation Commands

Mutations:
- mutate transaction-local state
- require an open Transaction
- are undoable *until commit or rollback*
- must execute atomically

A failed mutation:
- produces no observable state change
- produces no undo record

---

## 6. Integration Hub Execution Responsibilities

### 6.1 Transaction Resolution

The Integration Hub:
- resolves the target Transaction
- validates its open status
- executes the command relative to it

There is **no separate execution context** beyond the Transaction.

---

### 6.2 Dispatch to MAP Core APIs

Commands are dispatched to native Rust APIs:

- Holon queries → `ReadableHolon`
- Holon mutations → `WritableHolon`
- Lifecycle operations → `HolonOperationsApi`
- Dance execution → Dance dispatch

Dispatch is **purely structural** — no inference.

---

## 7. Conductora Command Envelope (Normative)

All MAP Commands are executed via a **uniform request/response envelope** managed by the **Integration Hub**.

The command envelope:

- defines the privileged IPC boundary
- provides a stable interception point for cross-cutting concerns
- carries no execution state itself

All semantics live in the `CommandBody` and the resolved `Transaction`.

---

### 7.1 MapRequest

`MapRequest` represents a single privileged command invocation.

    pub struct MapRequest {
        /// Stable identifier for routing, tracing, and observability.
        pub name: String,

        /// The Transaction in which this command must execute.
        pub transaction_id: TransactionId,

        /// The command payload to execute.
        pub command: CommandBody,
    }

#### Semantics and Invariants

- Every `MapRequest` executes **relative to exactly one open Transaction**
- The Integration Hub **must reject** requests targeting:
  - unknown Transactions
  - closed, committed, or rolled-back Transactions
- The request envelope:
  - does not carry provisional state
  - does not carry references to execution objects
  - does not imply ownership of the Transaction

The `name` field:

- has no semantic meaning
- is used exclusively for logging, tracing, and diagnostics

---

### 7.2 MapResponse

`MapResponse` is the uniform response envelope returned after command execution.

    pub struct MapResponse {
        /// Whether command execution completed successfully.
        pub success: bool,

        /// Optional typed response payload.
        pub body: Option<CommandResponse>,

        /// Zero or more execution errors or warnings.
        pub errors: Vec<HolonError>,
    }

#### Semantics and Invariants

- `success = true` indicates that the command completed without fatal error
- `errors` may be non-empty even when `success = true`
- `body` is:
  - present only when the command produces a response
  - structurally typed via `CommandResponse`
- A failed command:
  - produces no observable state change
  - produces no undo record

The response envelope:

- does not expose transaction internals
- does not expose undo history or markers
- does not expose execution artifacts

---

### 7.3 Envelope Responsibilities

The command envelope is the **single leverage point** for:

- authorization enforcement
- audit and telemetry hooks
- transaction resolution and validation
- routing decisions (local vs guest execution)
- invariant enforcement at the IPC boundary

MAP Core APIs are **never invoked directly** across this boundary.
All privileged execution flows through `MapRequest` / `MapResponse`.

---

### 7.4 Non-Goals

The command envelope does **not**:

- define TypeScript SDK ergonomics
- expose MAP Core APIs
- represent a public or federated protocol
- carry domain-level semantics
- persist execution history

Public interoperability is achieved via **Dances and Trust Channels**, not Commands.

---

### 7.5 Normative Status

This section defines the **authoritative specification** of `MapRequest` and `MapResponse`.

Earlier envelope definitions (including context-based or undo-token-based variants)
are superseded by this specification.

---

## 8. Undo and Redo Enforcement (Core-Level)

MAP Core provides **experience-level undo and redo** for provisional (uncommitted) state within an open Transaction.

This document intentionally does **not** define the full undo/redo model or interfaces.
Those are defined normatively in:

**`experience-undo-redo.md` — MAP Core Pre-Commit Transaction Editing Model**

This section summarizes the responsibilities and guarantees enforced by MAP Core.

### 8.1 Core Guarantees

At a high level:

- Undo and redo are **transaction-scoped**
- Undo and redo apply **only to uncommitted state**
- Undo and redo history is **ephemeral**
- Undo and redo history is discarded on:
  - commit
  - rollback
- Undo and redo correctness is enforced **centrally by MAP Core**

### 8.2 Responsibility Split

MAP Core is responsible for:

- maintaining the undo/redo history
- enforcing ordering, reachability, and invalidation rules
- guaranteeing correctness and safety

The experience layer (TypeScript client) is responsible for:

- deciding when to create undo markers
- deciding how far to undo or redo
- issuing undo/redo requests in sequence

The experience layer **does not** enforce correctness.
It relies on MAP Core for all invariants.

### 8.3 Normative Reference

All details of:

- undo and redo semantics
- undo/redo to marker behavior
- invariants
- failure conditions
- interface specifications

are defined in **`experience-undo-redo.md`**, which supersedes earlier exploratory designs.

---

## 9. Commit and Rollback

Transactions are explicitly terminated via commit or rollback.

### 9.1 Commit

Calling `commit()`:

- persists all staged transaction state
- invalidates all undo and redo capability
- closes the Transaction permanently

After commit:

- no further commands may execute in the Transaction
- undo and redo history is discarded

### 9.2 Rollback

Calling `rollback()`:

- discards all transaction-local state
- invalidates all undo and redo capability
- closes the Transaction permanently

Rollback has no observable effects on persisted state.

### 9.3 Post-Commit Reversal

Post-commit reversal is **not undo**.

Any reversal after commit must be expressed as:

- a new Transaction
- explicit compensating domain operations

This is outside the scope of MAP Commands.

---

## 10. Invariants Enforced by the Integration Hub

The Integration Hub guarantees:

- all execution is transaction-relative
- no mutation executes without an open Transaction
- references are never reinterpreted or rebound
- undo/redo correctness is enforced once, centrally
- no execution-state structures cross IPC boundaries

Violations of these invariants must result in command rejection.

---

## 11. Summary

This document establishes the **authoritative execution model** for MAP Commands:

- Commands are executed exclusively via a uniform request/response envelope
- Transactions are the execution context
- Spaces own Transactions; Transactions own provisional state
- References are self-resolving via embedded Transaction identity
- Undo and redo are linear, core-enforced, and experience-orchestrated
- Context indirection is obsolete

This model provides the foundation for ongoing MAP Core refactoring,
particularly in the Reference Layer and HolonSpaceManager design.