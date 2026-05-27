# MAP Commands Cheatsheet (v1.2)

## ChangeLog

### v1.2

- aligns the cheat sheet with the Query design pivot and Issue 508 contract delta
- removes `TransactionAction::Query` from the target command surface
- clarifies that navigation/query-like behavior enters Commands as Dance invocation
- re-centers plural holon-backed command and navigation results on `HolonCollection`
- marks retained old-world query traversal artifacts as deprecated compatibility only

### v1.1

- aligns the cheat sheet with the canonical runtime shared type family
- preserves narrower specialized types where they encode real legality or lifecycle constraints
- clarifies that `DanceRequest` and `QueryExpression` remain transitional bridge payloads
- adds a command-local appendix for deprecated bridge payloads and legacy contract-adjacent forms

### v1.0.0

- established the baseline quick reference for the MAP Commands IPC architecture

See the [full specification](commands.md) for details.

## Goal

Establish:

- Canonical IPC command surface
- Split host adapter / runtime execution model
- Explicit structural scope
- Strict wire/domain separation
- Descriptor-driven policy
- No command-owned Query envelope

Structure first. Behavior remains domain-defined.

---

## 1. Single IPC Entry

    type RuntimeState = RwLock<Option<Runtime>>;

    #[tauri::command]
    async fn dispatch_map_command(
        request: MapIpcRequest,
        runtime_state: State<'_, RuntimeState>,
    ) -> Result<MapIpcResponse, HolonError>

**Invariants**

- This is the only IPC entrypoint for MAP domain execution.
- It accepts wire types only.
- It may fail if runtime is not initialized.
- It performs wire-to-domain binding before runtime execution.
- It delegates bound commands to `Runtime::execute_command`.
- It performs no domain behavior directly.

---

## 2. Crate Split

- `map_commands_contract`
  - owns domain contract types
  - `MapCommand`, `MapResult`, `CommandDescriptor`
- `map_commands_wire`
  - owns IPC transport and wire types
  - `MapIpcRequest`, `MapIpcResponse`, `MapCommandWire`, `MapResultWire`
- `map_commands_runtime`
  - owns runtime execution
  - `Runtime`, `RuntimeSession`, scope-specific handlers

**Dependency Rules**

- `wire` depends on `contract`
- `runtime` depends on `contract`
- `runtime` does not depend on `wire`

---

## 3. IPC Envelope (Wire Layer Only)

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

    pub struct MapIpcResponse {
        pub request_id: RequestId,
        pub result: Result<MapResultWire, HolonError>,
    }

**Wire Layer Rules**

- Wire types are serializable transport structures.
- Wire types contain identifiers and request metadata only.
- `RequestId` is currently a `MapInteger` wrapper.
- Wire types contain no behavioral objects.
- Wire types must not cross below the binding seam.

---

## 4. Runtime Boundary

    pub struct Runtime {
        session: Arc<RuntimeSession>,
    }

    impl Runtime {
        pub async fn execute_command(
            &self,
            command: MapCommand,
        ) -> Result<MapResult, HolonError>;
    }

`Runtime` is the single domain execution and policy boundary for bound commands.

**Runtime Responsibilities**

- Accept bound domain commands
- Enforce descriptor policy
- Route to scope-specific handlers
- Execute domain behavior
- Return domain results

Below the binding seam:

    No *Wire types exist.

---

## 5. Structural Scope (Domain)

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

## 6. Space Scope

    pub enum SpaceCommand {
        BeginTransaction,
    }

- Opens a new transaction.
- Returns a transaction result in domain form, later mapped to wire form.
- Only space-level command in v0.

---

## 7. Transaction Scope (Domain)

    pub struct TransactionCommand {
        pub context: Arc<TransactionContext>,
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
        DanceV2(DanceInvocation),
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
- `Arc<TransactionContext>` exists only in domain form.
- Transaction-scoped commands are bound before runtime execution.
- Transaction-scoped read-only commands still require an open transaction.
- No string identifiers exist below binding.
- General command payloads and results should converge on the runtime shared type family:
  - `HolonReference`
  - `HolonCollection`
  - `BaseValue`
- Narrower specialized operand types are preserved where they encode real invariants:
  - `TransientReference` for `StageNewHolon`
  - `SmartReference` for `StageNewVersion`
  - `LocalId` for `DeleteHolon`
- `DanceRequest` remains a transitional bridge payload rather than the long-term canonical dance-facing substrate.
- `DanceV2(DanceInvocation)` is the explicit parallel new-world command path for dance invocation during transition.
- `TransactionAction::Query` is not part of the target Commands API.
- Navigation/query-like behavior should enter Commands through Dance invocation, not a first-class Query command envelope.
- `QueryExpression`, `NodeCollection`, and `QueryPathMap` remain only as deprecated compatibility payloads inside retained old-world query dance flows.
- Projected records should be transient holons, and projected record sets should be `HolonCollection`s.

---

## 8. Holon Scope (Domain)

    pub struct HolonCommand {
        pub context: Arc<TransactionContext>,
        pub target: HolonReference,
        pub action: HolonAction,
    }

    pub enum HolonAction {
        Read(ReadableHolonAction),
        Write(WritableHolonAction),
    }

**Holon Invariants**

- Holon commands carry both transaction context and holon target.
- Context exists for lifecycle and mutation-policy enforcement.
- Holon references remain self-resolving for their own operations.
- Holon-scoped read-only commands do not necessarily require an open transaction.
- Full `Holon` payloads are not a general command result shape; they are restricted to narrow infrastructure-level transfer such as cache hydration.

---

## 9. ReadableHolonAction

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
- Readability rules differ from transaction-scope reads.
- `PropertyValue` remains scalar-valued through `BaseValue`.
- `RelatedHolons` should use `HolonCollection` as the canonical plural holon-backed contract result.

Not part of the MAP Commands API surface in v0:

- `is_accessible`
- `get_all_related_holons`
- `into_model`

---

## 10. WritableHolonAction

    pub enum WritableHolonAction {
        WithPropertyValue { name: PropertyName, value: BaseValue },
        RemovePropertyValue { name: PropertyName },
        AddRelatedHolons { name: RelationshipName, holons: HolonCollection },
        RemoveRelatedHolons { name: RelationshipName, holons: HolonCollection },
        WithDescriptor { descriptor: HolonReference },
    }

- Requires lifecycle validation.
- May require commit guard.
- Mutation semantics are descriptor-driven.
- Plural relationship operands should converge on `HolonCollection`; lower-level vector forms may remain as implementation helpers during migration.

---

## Appendix A. Command Bridge-Type Disposition

| Type | Classification | New-world status | Allowed use in the new world | Notes |
|---|---|---|---|---|
| `DanceRequest` | Deprecated legacy bridge | Deprecate | Legacy runtime and adapter compatibility only | Commands should converge on the canonical dance invocation and outcome surface |
| `DanceInvocation` carried by `DanceV2` | Canonical surface-owned envelope usage | Keep | New-world canonical dance invocation path through Commands | Explicit parallel path during transition |
| `QueryExpression` | Deprecated compatibility payload | Deprecate | Legacy old-world query dance compatibility only | Retained only inside old-world `DanceRequest` / query-method dance flows |
| `Node`, `NodeCollection`, `QueryPathMap`, `DanceType::QueryMethod(NodeCollection)` | Deprecated compatibility payload family | Deprecate | Legacy `query_relationships` and `fetch_all_related_holons` compatibility only | Retained after Issue 508 because current flows still require them |
| `HolonCollection` | Canonical runtime shared type | Keep | General-purpose plural holon-backed command, dance, and navigation result carrier | Primary plural runtime carrier |
| `BoundHolonCollection` | Deferred candidate / removed target posture | Defer | None in the current command target contract | Do not introduce unless a future lifecycle or contract need cannot be represented by `HolonCollection` plus surrounding structure |
| `Row` | Removed query/command contract artifact | Remove | None in the current command target contract | Projected records should be transient holons, not row-shaped command contracts |
| `RowSet` | Removed query/command contract artifact | Remove | None in the current command target contract | Projected record sets should be `HolonCollection`s |
| `QueryRequest`, `QueryResult`, `QueryResultData`, `QueryDiagnostic` | Removed standalone Query contracts | Remove | None | Commands do not own a first-class query request/result contract |
| `Vec<HolonReference>` as a command contract operand | Implementation helper | Keep internally only | Low-level internal collection handling | May remain internally but should not remain the command contract center |
| direct full `Holon` payloads in general command contracts | Restricted infrastructure pattern | Restrict | Infrastructure-level full-state transfer only | Legitimate for narrow cache-hydration or internal retrieval paths, not as the general command result posture |

---

## 11. Descriptor Policy

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

**Policy Rules**

- Every command is described by a `CommandDescriptor`.
- Structural enums define command shape.
- Descriptors define execution behavior.
- Runtime enforces descriptor metadata.
- `snapshot_after` is request metadata in `RequestOptions`, not descriptor metadata.

---

## 12. Execution Shape

Space:

    MapIpcRequest(Space)
      → bind in Tauri adapter
      → Runtime::execute_command
      → handle_space
      → MapResult
      → wire response mapping

Transaction:

    MapIpcRequest(Transaction)
      → bind in Tauri adapter (tx_id → Arc<TransactionContext>)
      → Runtime::execute_command
      → handle_transaction
      → TransactionContext operations
      → MapResult
      → wire response mapping

Holon:

    MapIpcRequest(Holon)
      → bind in Tauri adapter (HolonReferenceWire + tx context → HolonCommand)
      → Runtime::execute_command
      → handle_holon
      → HolonReference method execution
      → MapResult
      → wire response mapping

---

## Core Architectural Invariants

- Exactly one IPC entrypoint: `dispatch_map_command`.
- Runtime is the only domain execution boundary for bound commands.
- No `*Wire` types exist below the binding seam.
- Scope is explicit: `Space | Transaction | Holon`.
- Commands execute in host, not in WASM.
- Descriptor metadata drives execution policy.
- No session-derived authority.
- No string-based dispatch.
- No command-owned Query envelope.
- Navigation behavior is descriptor-afforded Dance behavior over `HolonCollection`.
- Future replayable navigation structure belongs in `ExecutionPlan` holons, not command variants.

This cheat sheet captures structural invariants only.  
Detailed execution semantics are defined in the [full specification](commands.md).
