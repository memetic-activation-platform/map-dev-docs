# MAP Commands — Integration Hub Command Envelope
*(Conductora Host · Transaction-Centric Execution Model)*

**Status:** Converged (Architectural Baseline)  
**Audience:** MAP Core Rust developers, Integration Hub maintainers  
**Scope:** Human-facing command dispatch, execution, and enforcement within Conductora

This document defines the **authoritative specification** for the **command envelope and command taxonomy** exposed by the **MAP Integration Hub** (historically labeled *Rust Client*) and hosted inside the **Conductora Tauri Container**.

It specifies **only** the subset of Integration Hub behavior that is exposed to the **Human Agent** via a **privileged local command envelope**.

It intentionally excludes:

- TypeScript SDK API design  
  (see `map-ts-sdk-impl.md`)
- TrustChannel / inter-agent protocols and dances
- Undo / redo experience semantics  
  (see `experience-undo-redo.md`)

---

## 1. Architectural Positioning

### 1.1 Conductora Host Context

All MAP Commands execute within a **Conductora Tauri Container**, which is the single-process host runtime embedding:

- the TypeScript experience layer
- the MAP Integration Hub (host-side authority)
- MAP Core (domain engine)
- the Rust Holons Guest (WASM sandbox)
- networking and storage adapters

The Conductora host provides:

- a privileged local IPC boundary
- component wiring and lifecycle
- no domain semantics of its own

---

### 1.2 MAP Integration Hub (Rust Client)

The **MAP Integration Hub** is the privileged, host-side authority responsible for:

- receiving and validating MAP Commands
- resolving the target Transaction
- enforcing command invariants
- dispatching execution into MAP Core
- mediating access to adapters and guests

The term **“Rust Client”** appears only as a historical alias for continuity with earlier diagrams.

MAP Core itself remains transport-agnostic and command-unaware.

---

### 1.3 Human-Facing vs Agent-Facing Surfaces

The Integration Hub exposes multiple behavioral surfaces:

- **Human-facing (this document):**

  - privileged local commands
  - imperative editing semantics
  - experience-level undo/redo

- **Agent-facing (out of scope):**

  - TrustChannels
  - negotiated dances
  - inter-agent protocols
  - no undo guarantees

This document specifies **only the human-facing command surface**.

---

## 2. Execution Model: Transactions as Context

### 2.1 Transaction-Centric Execution

All MAP Commands execute **relative to exactly one Transaction**.

A Transaction:

- belongs to exactly one Holon Space
- is isolated from other Transactions
- owns all provisional and session-local state

Including:

- Nursery (staged holons)
- Transient holon manager
- transaction-local caches
- linear undo/redo history
- open / committed / rolled-back status

There is **no separate execution context** beyond the Transaction.

---

### 2.2 Experience-Layer Responsibilities

The experience layer (TypeScript client) is responsible for:

- selecting the **focal Space** for the human
- requesting creation of a Transaction within that Space
- choosing which commands execute within that Transaction
- deciding when to commit or roll back

The experience layer does **not**:

- own Transactions
- resolve references
- manage provisional state
- enforce undo correctness

All execution guarantees are enforced by the Integration Hub and MAP Core.

---

## 3. Space, Manager, and Transaction Responsibilities

### 3.1 Holon Space (Backing Store)

At the persistence layer, a **Holon Space** is a Holochain DHT.

- Each Holon Space has exactly one persisted HolonSpace holon
- The backing store has no concept of Transactions or undo

---

### 3.2 HolonSpaceManager (Host Runtime)

Within MAP Core, a **HolonSpaceManager** is the long-lived runtime authority for a Space.

It:

- holds an in-memory reference to the HolonSpace holon
- owns the lifecycle of Transactions for that Space

It does **not** own provisional state directly.

---

### 3.3 Transactions (Execution Context)

A **Transaction** is an ephemeral, space-scoped execution context created by a HolonSpaceManager.

Each Transaction owns:

- its own Nursery
- its own TransientHolonManager
- transaction-local cache routing
- a linear undo/redo chain

Transactions are the unit of:

- execution
- isolation
- undo validity

---

## 4. Self-Resolving References

### 4.1 Embedded Transaction Identity

All `HolonReference` variants embed their **Transaction identity**, including:

- SmartReference
- StagedReference
- TransientReference

This ensures:

- references are self-resolving
- cross-transaction misuse is structurally impossible
- no external context matching is required

Resolution chain:

HolonReference → Transaction → Space → HolonSpace + services

The Integration Hub **must never reinterpret or rebind references**.

---

## 5. Command Intent Model

Although the TypeScript experience layer could, in principle, invoke MAP Core Rust APIs in a one-to-one fashion, MAP deliberately introduces a **single Command abstraction** as the *only* human-facing execution surface into the Integration Hub.

This is a **conscious architectural choice**, not an API convenience.

The Command abstraction provides a **stable and enforceable boundary** between:

- **human intent** (imperative editing gestures), and
- **core execution** (transactional domain logic)

Commands exist because they enable guarantees that direct API calls cannot provide:

- **Centralized enforcement**  
  All human-initiated behavior is funneled through a single interception point where the Integration Hub can enforce transaction scoping, authorization, mutation safety, and undo eligibility.

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


### 5.1 Structural Partitioning

Commands are structurally classified by intent:

    pub enum CommandBody {
        Query(QueryCommand),
        Mutation(MutationCommand),
    }

The structural similarity to CQRS is intentional, but this is **not a full CQRS architecture**.

MAP maintains:
- a single execution pipeline
- a unified state model
- no separate read/write subsystems

The Query / Mutation partition exists solely to make **intent explicit in the type system**, enabling declarative enforcement of:
- authorization
- undo and redo eligibility
- replay safety
- mutation constraints

This partition is a classification mechanism, not an architectural split.

---

### 5.2 Query Commands

Queries:
- do not mutate state
- may execute within a Transaction for isolation
- never participate in undo/redo
- are safe to replay

Any observable state mutation during a Query is a violation.

---

### 5.3 Mutation Commands

Mutations:
- mutate transaction-local state
- require an open Transaction
- are undoable until commit or rollback
- must execute atomically

A failed mutation:
- produces no observable state change
- produces no undo record

---

## 6. Integration Hub Execution Responsibilities

### 6.1 Transaction Resolution

For every command, the Integration Hub must:

- resolve the referenced Transaction
- verify it is open
- reject commands targeting unknown or closed Transactions

---

### 6.2 Dispatch to MAP Core APIs

Commands are dispatched structurally to native Rust APIs:

- Holon queries → ReadableHolon
- Holon mutations → WritableHolon
- Lifecycle operations → HolonOperationsApi
- Dance execution → Dance caller

No semantic inference occurs at the Integration Hub layer.

---

## 7. Conductora Command Envelope (Normative)

All MAP Commands are executed via a **uniform request/response envelope** managed by the Integration Hub.

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

**Semantics and Invariants**

- Every MapRequest executes relative to exactly one open Transaction
- The Integration Hub must reject requests targeting:
  - unknown Transactions
  - committed or rolled-back Transactions
- The request envelope:
  - does not carry provisional state
  - does not carry references to execution objects
  - does not imply ownership of the Transaction

---

### 7.2 MapResponse

`MapResponse` is the uniform response envelope.

    pub struct MapResponse {
        pub success: bool,
        pub body: Option<CommandResponse>,
        pub errors: Vec<HolonError>,
    }

Notes:
- No HTTP semantics
- Errors may accompany successful responses
- Partial success is allowed

---

## 7.3 Command Taxonomy (Normative)

### Query Commands

    pub enum QueryCommand {
        Holon(HolonQuery),
        Operations(OperationsQuery),
    }

    pub struct HolonQuery {
        pub target: HolonReference,
        pub action: HolonQueryAction,
    }

    pub enum HolonQueryAction {
        CloneHolon,
        EssentialContent,
        HolonId,
        Predecessor,
        Key,
        VersionedKey,
        AllRelatedHolons,
        GetPropertyValue { property: PropertyName },
        GetRelatedHolons { relationship: RelationshipName },
    }

    pub enum OperationsQuery {
        GetAll,
        Summarize,
        StagedCount,
        TransientCount,
    }

---

### Mutation Commands

    pub enum MutationCommand {
        Holon(HolonMutation),
        Operations(OperationsMutation),
        ExecuteDance(ExecuteDanceCommand),
    }

    pub struct HolonMutation {
        pub target: HolonReference,
        pub action: HolonMutationAction,
    }

    pub enum HolonMutationAction {
        AddRelatedHolons { relationship: RelationshipName, holons: Vec<HolonReference> },
        RemoveRelatedHolons { relationship: RelationshipName, holons: Vec<HolonReference> },
        WithPropertyValue { property: PropertyName, value: BaseValue },
        RemovePropertyValue { property: PropertyName },
        WithPredecessor { predecessor: Option<HolonReference> },
        WithDescriptor { descriptor: HolonReference },
    }

    pub enum OperationsMutation {
        NewHolon { key: String },
        DeleteHolon { target: HolonReference },
        StageNewHolon { type_name: TypeName, properties: PropertyMap },
        StageNewVersion { source: HolonReference, properties: PropertyMap },
        StageFromClone { source: HolonReference },
        Commit,
    }

    pub struct ExecuteDanceCommand {
        pub dance_name: String,
        pub request: DanceRequestBody,
    }

Dance invocation is modeled as a mutation by default.
Undo behavior (if any) is the responsibility of the Dance implementation.

---

### 7.4 CommandResponse

    pub enum CommandResponse {
        HolonReference { reference: HolonReference },
        EssentialHolonContent { content: EssentialHolonContent },
        PropertyValue { value: Option<BaseValue> },
        RelationshipMap { relationships: RelationshipMap },
        HolonCollection { members: Vec<HolonReference> },
        StringValue { value: Option<String> },
        Summary { summary: SummarizeResponse },
        Count { count: usize },
        HolonReferenceList { holons: Vec<HolonReference> },
        CommitResult { committed: usize },
        DanceResult { response: DanceResponseBody },
    }

Some commands may return no body.

---

## 8. Undo and Redo Enforcement (Summary)

Undo and redo apply only to **uncommitted state within an open Transaction**.

- Undo/redo history is transaction-scoped and ephemeral
- All correctness is enforced by MAP Core
- Grouping and navigation are orchestrated by the experience layer

The full model and interfaces are defined normatively in:

**experience-undo-redo.md — MAP Core Pre-Commit Transaction Editing Model**

---

## 9. Commit and Rollback

- Commit persists transaction state, invalidates undo/redo, and closes the Transaction
- Rollback discards transaction-local state and closes the Transaction

Post-commit reversal requires new compensating Transactions.

---

## 10. Invariants Enforced by the Integration Hub

The Integration Hub guarantees:

- all execution is transaction-relative
- no mutation executes without an open Transaction
- references are never reinterpreted
- undo/redo correctness is enforced centrally
- no execution-state structures cross IPC boundaries

Violations must result in command rejection.

---

## 11. Summary

This document defines the **authoritative Conductora-hosted command envelope**:

- Commands are the human-facing imperative surface
- Transactions are the execution context
- Spaces own Transactions; Transactions own provisional state
- References are self-resolving
- Undo/redo is linear, core-enforced, and experience-orchestrated

This specification provides the stable foundation for MAP Core evolution and Integration Hub implementation.