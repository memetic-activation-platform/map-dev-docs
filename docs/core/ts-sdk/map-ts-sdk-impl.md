# TypeScript MAP SDK — Implementation Specification v1.3

## Change Log

### v1.3

- aligns the SDK implementation spec with Commands v1.2, Dances v2.0, and the current query/navigation design pivot
- re-centers plural holon-backed SDK operands and results on `HolonCollection`
- records `BoundHolonCollection` as an abandoned design branch and removes it from the SDK target posture
- removes command-owned `QueryRequest`, `QueryResult`, `TransactionAction::Query`, and `legacyQuery` assumptions
- treats query/navigation behavior as descriptor-afforded Dances invoked through `DanceV2(DanceInvocation)`
- replaces standalone `DanceOutcome` guidance with response-holon handling through `DanceResponseHandle` or equivalent thin response references
- clarifies that projected record sets are `HolonCollection`s of projection-described holons, not row-shaped SDK results

### v1.2

- captured an intermediate bound-first dance/query contract posture
- superseded by v1.3 for current `HolonCollection`, dance-response, and query/navigation guidance

### v1.1

- aligned the SDK draft with the MAP Commands v1.1 structure and descriptor-oriented public surfaces

## 1. Overview

This document defines the implementation specification for the TypeScript MAP SDK.

It is intended for MAP Core developers responsible for:

- implementing and maintaining the SDK
- keeping the SDK aligned with the canonical MAP Commands surface
- implementing the TypeScript-side command construction layer
- implementing and testing the TS ↔ Rust IPC boundary

This document is normative for the TypeScript implementation.

It is subordinate to [commands.md](../commands-and-runtime/commands.md) for command architecture, [commands-cheat-sheet.md](../commands-and-runtime/commands-cheat-sheet.md) for the condensed structural reference, and [commands-impl-plan.md](../commands-and-runtime/commands-impl-plan.md) for command delivery sequencing.

It is also informed by the descriptor design work under `docs/core/descriptors/`, the runtime shared type foundation under `docs/core/type-system/runtime-shared-types.md`, the current query/navigation design under `docs/core/map-queries/`, and the current Dances design under `docs/core/dances/dances-design-spec.md`.

## 2. Design Goal

The TypeScript side is composed of two distinct layers:

1. A public SDK layer that exposes ergonomic TypeScript APIs to MAP client developers.
2. An internal command layer that constructs TypeScript command objects and wire types, then invokes the single MAP IPC entrypoint.

The public SDK layer MUST NOT expose wire types.

The internal command layer MUST mirror the current MAP Commands structure closely enough that each SDK method maps to exactly one MAP command.

This version adds an additional design constraint:

- the public SDK should move toward a descriptor-oriented surface over time
- descriptor wrappers should become the semantic home for validation, operator discovery, command lookup, and dance lookup
- the internal command layer remains structural and transport-facing
- public SDK results should prefer `HolonReference` and `HolonCollection` when the result remains holon-backed
- materialized projection/result shapes should appear only when a command, dance, ABI, or serialization boundary actually requires them
- query/navigation behavior should enter through descriptor-afforded Dances rather than through a command-owned query envelope

## 3. Architectural Position

```text
DAHN / Visualizers / other TS clients
  -> Public TS SDK
  -> Internal TS Command Layer
  -> MapIpcRequest / MapIpcResponse
  -> Tauri invoke("dispatch_map_command")
  -> host adapter binds wire -> domain
  -> Runtime::execute_command
  -> MAP Core APIs
```

Key rule:

- The public SDK is ergonomic.
- The internal command layer is structural.
- The wire layer is transport-only.

## 4. Layer Definitions

### 4.1 Layer A: Public TS SDK

This is the API consumed by TypeScript application developers.

It:

- exposes domain-meaningful functions and objects
- hides all `*Wire` types
- hides IPC transport details
- hides Tauri invocation details
- maps each public method to exactly one MAP command

It MUST NOT:

- expose `MapIpcRequest`, `MapIpcResponse`, or any `*Wire` types
- expose string-based command names
- perform multi-command orchestration implicitly
- invent new lifecycle semantics

### 4.2 Layer B: Internal TS Command Layer

This is the implementation layer used by the public SDK.

It:

- constructs TypeScript representations of MAP command structures
- constructs `MapIpcRequest`
- attaches `RequestOptions`
- invokes `dispatch_map_command`
- parses `MapIpcResponse`
- converts wire results into public SDK return values

It MUST:

- structurally mirror the current MAP Commands architecture from `commands.md`
- preserve explicit scope: `Space | Transaction | Holon`
- respect the host adapter / runtime split
- preserve the single IPC boundary
- keep wire types internal to the SDK package

## 5. Alignment with MAP Commands

The TypeScript implementation MUST align with the current command specification:

- single IPC entrypoint: `dispatch_map_command`
- wire envelope: `MapIpcRequest` / `MapIpcResponse`
- request metadata: `RequestOptions`
- structural command scopes: `Space`, `Transaction`, `Holon`
- flattened transaction lookup actions
- host adapter performs wire binding before `Runtime::execute_command`
- new-world dance ingress: `DanceV2(DanceInvocation)`
- no command-owned `TransactionAction::Query`, `QueryRequest`, `QueryResult`, `Row`, `RowSet`, or alternate plural collection target surface
- transitional bridge payloads: `DanceRequest` and old-world query traversal payloads only inside legacy dance compatibility paths

The TypeScript implementation SHOULD also reflect the current crate split conceptually:

- contract-facing command/result shapes
- wire-facing IPC envelope shapes
- runtime-facing execution boundary

The TypeScript SDK does not need to replicate the Rust crate layout literally.

It does need to preserve the same separation of concerns.

## 5.1 Alignment with Runtime Shared Types

The SDK must align with the canonical runtime shared type family.

For public TypeScript contracts, this means:

- `HolonReference` is the default singular bound holon handle
- `HolonCollection` is the default plural holon-backed result or operand when a result remains holon-backed
- `SmartReference` remains explicit where smart-link-aware lifecycle semantics are contract-significant
- `BaseValue` is the scalar materialized value shape
- projected records are holons described by concrete extensions of `Projection`
- projected record sets are `HolonCollection`s whose members are projection-described holons
- `Row`, `RowSet`, and standalone record-stream shapes are not target command, dance, query, or SDK contracts in the current design

Compatibility interpretation:

- `HolonReference[]` may be accepted by convenience helpers only if it is adapted into the canonical command contract shape before IPC
- `DanceRequest` is legacy dance ingress; new public dance APIs should target `DanceInvocation`
- `QueryExpression`, `NodeCollection`, and `QueryPathMap` are legacy old-world query dance payloads, not public SDK query substrate
- the SDK should not define standalone `QueryRequest` or `QueryResult` contracts for the current target design
- the SDK should not force eager row-shaped results where `HolonReference`, `HolonCollection`, or a projection-described response body is the more faithful contract

## 5.2 Alignment with MAP Descriptors

The SDK must now also align with the descriptor architecture.

That means the SDK should increasingly expose:

- holon descriptor access
- property descriptor access
- relationship descriptor access
- value descriptor access
- descriptor-afforded command and dance discovery
- value-type-driven operator discovery

The key rule is:

> SDK ergonomics may group behavior for developers, but SDK semantics should come from descriptors rather than from duplicated TS-side rule systems.

Consequences:

- the SDK must not re-implement `Extends` flattening in TypeScript
- descriptor inheritance and effective lookup should be resolved by the Rust/core layer
- TS descriptor handles should stay thin and reference-backed
- frontend consumers such as DAHN should use those public SDK descriptor-oriented surfaces rather than declaring parallel local descriptor handle APIs
- validation/query/operator semantics exposed to TS should derive from descriptor meaning, not from ad hoc client helpers

## 6. Public SDK Surface

This section defines the intended public TypeScript API surface.

The public API is grouped by developer-facing concepts. Internally, each method maps to a structural MAP command.

### 6.1 MapClient

`MapClient` is the root SDK object for a bound MAP space.

Unlike the previous draft, `MapClient` MUST NOT be specified as carrying both `contextId` and `transactionId`.

The current commands architecture only requires:

- space-scoped command construction for `BeginTransaction`
- transaction-scoped command construction using transaction identity in wire form
- holon-scoped command construction using a holon target

Accordingly, the TypeScript SDK should treat transaction identity as an internal implementation detail of transaction-bound objects, not as a public architectural primitive on every client object.

`MapClient` responsibilities:

- begin a transaction
- manufacture transaction-scoped helper objects
- avoid exposing wire-layer identifiers unless separately justified by the SDK design

#### Public methods

| Function Signature | Emits | Notes |
|---|---|---|
| `beginTransaction(): Promise<MapTransaction>` | `MapCommandWire.Space(BeginTransaction)` | Only public space-scoped SDK command in v0. Returns a transaction-bound SDK object. |

### 6.2 MapTransaction

`MapTransaction` is the public transaction-bound execution context.

It represents an open transaction from the perspective of the TypeScript developer.

It is the object through which transaction-scoped and holon-scoped work is initiated.

`MapTransaction` MUST encapsulate the transaction identity required by the wire layer.

#### Public methods

| Function Signature                                                                       | Emits                                                                 | Notes                                                                                                                                                                                    |
|------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `commit(): Promise<void>`                                                                | `MapCommandWire.Transaction(Commit)`                                  | Ends the transaction. The SDK spec should not invent a return payload unless the wire/result spec defines one.                                                                           |
| `newHolon(key?: string): Promise<TransientHolonReference>`                               | `MapCommandWire.Transaction(NewHolon { key })`                        | Creates a new transient holon.                                                                                                                                                           |
| `stageNewHolon(source: TransientHolonReference): Promise<HolonReference>`                | `MapCommandWire.Transaction(StageNewHolon { source })`                | Stages a new holon from a transient source.                                                                                                                                              |
| `stageNewFromClone(original: HolonReference, newKey: string): Promise<HolonReference>`   | `MapCommandWire.Transaction(StageNewFromClone { original, new_key })` | Stages a clone with a new base key.                                                                                                                                                      |
| `stageNewVersion(currentVersion: SmartReference): Promise<HolonReference>`               | `MapCommandWire.Transaction(StageNewVersion { current_version })`     | Stages a new version from a smart reference.                                                                                                                                             |
| `stageNewVersionFromId(holonId: HolonId): Promise<HolonReference>`                       | `MapCommandWire.Transaction(StageNewVersionFromId { holon_id })`      | Present in current commands spec and was missing from the prior SDK draft.                                                                                                               |
| `deleteHolon(localId: LocalId): Promise<void>`                                           | `MapCommandWire.Transaction(DeleteHolon { local_id })`                | Deletes a local holon within the active transaction.                                                                                                                                     |
| `loadHolons(bundle: HolonReference): Promise<void>`                                      | `MapCommandWire.Transaction(LoadHolons { bundle })`                   | Current commands spec uses `HolonReference` for `bundle`; prior SDK draft was out of sync.                                                                                               |
| `dance(invocation: DanceInvocationHandle): Promise<DanceResponseHandle>`                 | `MapCommandWire.Transaction(DanceV2(invocation.reference))`           | New-world dance ingress. The handle points to a `DanceInvocation` holon; the response handle points to a holon whose descriptor extends `DanceResponseType`.                             |
| `legacyDance(request: DanceRequest): Promise<LegacyDanceResponse>`                       | `MapCommandWire.Transaction(Dance(request))`                          | Compatibility-only bridge. Keep internal or clearly deprecated if exported.                                                                                                              |
| `getAllHolons(): Promise<HolonCollection>`                                               | `MapCommandWire.Transaction(GetAllHolons)`                            | Transaction-scoped lookup.                                                                                                                                                               |
| `getStagedHolonByBaseKey(key: string): Promise<HolonReference \| null>`                  | `MapCommandWire.Transaction(GetStagedHolonByBaseKey { key })`         |                                                                                                                                                                                          |
| `getStagedHolonsByBaseKey(key: string): Promise<HolonCollection>`                        | `MapCommandWire.Transaction(GetStagedHolonsByBaseKey { key })`        |                                                                                                                                                                                          |
| `getStagedHolonByVersionedKey(key: string): Promise<HolonReference \| null>`             | `MapCommandWire.Transaction(GetStagedHolonByVersionedKey { key })`    |                                                                                                                                                                                          |
| `getTransientHolonByBaseKey(key: string): Promise<TransientHolonReference \| null>`      | `MapCommandWire.Transaction(GetTransientHolonByBaseKey { key })`      |                                                                                                                                                                                          |
| `getTransientHolonByVersionedKey(key: string): Promise<TransientHolonReference \| null>` | `MapCommandWire.Transaction(GetTransientHolonByVersionedKey { key })` |                                                                                                                                                                                          |
| `stagedCount(): Promise<number>`                                                         | `MapCommandWire.Transaction(StagedCount)`                             |                                                                                                                                                                                          |
| `transientCount(): Promise<number>`                                                      | `MapCommandWire.Transaction(TransientCount)`                          |                                                                                                                                                                                          |

The SDK MUST NOT expose a public `query(request: QueryRequest)` method backed by `TransactionAction::Query` for the current target design.

Navigation/query-like SDK helpers may be added as ergonomic conveniences, but they must construct or target descriptor-afforded navigation Dances. Such helpers return `DanceResponseHandle`, `HolonCollection`, or projection-specific handles according to the invoked dance contract. They must not introduce standalone `QueryRequest`, `QueryResult`, `QueryExpression`, `Row`, or `RowSet` as the public substrate.

### 6.3 ReadableHolon

`ReadableHolon` is the public read-only facade for a holon target.

Each method emits a holon-scoped command targeting the bound holon reference.

This surface should be treated as transitional rather than final. Over time, the SDK should grow a descriptor-oriented API that sits alongside these command-aligned reads.

#### Public methods

| Function Signature | Emits | Notes |
|---|---|---|
| `cloneHolon(): Promise<TransientHolonReference>` | `MapCommandWire.Holon(Read(CloneHolon))` | Present in current commands spec; missing from prior SDK draft. |
| `essentialContent(): Promise<EssentialHolonContent>` | `MapCommandWire.Holon(Read(EssentialContent))` | |
| `summarize(): Promise<string>` | `MapCommandWire.Holon(Read(Summarize))` | Present in current commands spec; missing from prior SDK draft. |
| `holonId(): Promise<HolonId>` | `MapCommandWire.Holon(Read(HolonId))` | Present in current commands spec; missing from prior SDK draft. |
| `predecessor(): Promise<HolonReference \| null>` | `MapCommandWire.Holon(Read(Predecessor))` | |
| `key(): Promise<string \| null>` | `MapCommandWire.Holon(Read(Key))` | |
| `versionedKey(): Promise<string>` | `MapCommandWire.Holon(Read(VersionedKey))` | |
| `propertyValue(propertyName: PropertyName): Promise<BaseValue \| null>` | `MapCommandWire.Holon(Read(PropertyValue { name }))` | |
| `relatedHolons(relationshipName: RelationshipName): Promise<HolonCollection>` | `MapCommandWire.Holon(Read(RelatedHolons { name }))` | |

### 6.3.1 Descriptor-Oriented Additions

To support DAHN and other descriptor-driven clients, the public SDK SHOULD introduce thin descriptor-facing APIs as the command/runtime surface allows.

Representative additions:

| Function Signature | Role |
|---|---|
| `holonDescriptor(): Promise<HolonDescriptorHandle>` | Main descriptor entrypoint for a holon instance. |
| `availableCommands(): Promise<CommandDescriptorHandle[]>` | Effective inherited descriptor-afforded commands. |
| `availableDances(): Promise<DanceDescriptorHandle[]>` | Effective inherited descriptor-afforded dances. |

These additions do not change the one-command-per-method rule. They define the intended semantic direction of the public SDK.

DAHN and other frontend consumers should treat this public SDK layer as the source of truth for descriptor-oriented TypeScript access rather than defining duplicate raw descriptor handle contracts locally.

The following read APIs MUST NOT appear in the public SDK surface for v0 because they are explicitly not part of the MAP Commands API surface:

- `allRelatedHolons()`
- `isAccessible()`
- `intoModel()`

### 6.4 WritableHolon

`WritableHolon` extends `ReadableHolon` with mutating operations.

These methods require an open transaction in the runtime, but the TypeScript SDK SHOULD model that by only manufacturing writable holon facades from a `MapTransaction`.

#### Public methods

| Function Signature | Emits | Notes |
|---|---|---|
| `withPropertyValue(propertyName: PropertyName, value: BaseValue): Promise<void>` | `MapCommandWire.Holon(Write(WithPropertyValue { name, value }))` | |
| `removePropertyValue(propertyName: PropertyName): Promise<void>` | `MapCommandWire.Holon(Write(RemovePropertyValue { name }))` | |
| `addRelatedHolons(relationshipName: RelationshipName, holons: HolonCollection): Promise<void>` | `MapCommandWire.Holon(Write(AddRelatedHolons { name, holons }))` | |
| `removeRelatedHolons(relationshipName: RelationshipName, holons: HolonCollection): Promise<void>` | `MapCommandWire.Holon(Write(RemoveRelatedHolons { name, holons }))` | |
| `withDescriptor(descriptor: HolonReference): Promise<void>` | `MapCommandWire.Holon(Write(WithDescriptor { descriptor }))` | |

SDK convenience helpers may later accept `HolonReference[]` or `Iterable<HolonReference>`, but those helpers must adapt into the command contract's `HolonCollection` posture before IPC and must not make vector-shaped collections the architectural center.

### 6.5 Descriptor Handles

The SDK should treat descriptor-facing objects as thin, reference-backed handles rather than materialized TS-side schema mirrors.

Representative handles:

- `HolonDescriptorHandle`
- `PropertyDescriptorHandle`
- `RelationshipDescriptorHandle`
- `ValueDescriptorHandle`
- `CommandDescriptorHandle`
- `DanceDescriptorHandle`
- `DanceInvocationHandle`
- `DanceResponseHandle`
- `OperatorDescriptorHandle`

Descriptor handle rules:

- no duplicated ontology state
- no TS-side inheritance merging
- no client-side semantic shadow model
- direct accessors should reflect schema-backed/runtime-backed descriptor structure
- dance invocation and response handles are holon-backed references, not embedded request or response payload objects
- response body access should follow `ResponseBody` relationships from a `DanceResponseType`-derived response holon

### 6.6 Descriptor-Semantic Affordances

The public SDK should expose descriptor-backed semantics in ways that help clients like DAHN without forcing them to interpret raw commands.

Key examples:

- value validation should be accessible through `ValueDescriptor`-oriented APIs
- supported query/filter operators should be discoverable from value descriptors
- commands and dances should be discoverable as descriptor affordances, not only as standalone invocation surfaces

The SDK must not blur enforcement layers:

- descriptor semantics may be surfaced publicly
- PVL vs Nursery vs higher-layer enforcement remains a runtime architecture concern
- the TS SDK should not imply that every descriptor-defined rule can be authoritatively enforced on the client

## 7. Explicitly Removed from the Prior Draft

The following items from the prior `map-ts-sdk-impl.md` draft are not aligned with current MAP Commands and MUST be removed from the implementation spec:

- `MapRequest` / `MapResponse`
- Tauri endpoint name `map_request`
- command families `QueryCommand.*`, `MutationCommand.*`, `OperationsMutation.*`, `OperationsQuery.*`
- `allRelatedHolons()` as a command-backed SDK method
- `rollback()` as a command-backed SDK method
- `undo()` as a command-backed SDK method
- `withPredecessor()` as a command-backed SDK method
- assumptions that every SDK operation hangs off a client carrying both `contextId` and `transactionId`
- assumptions about `commit()` returning `TransientReference`
- nested `Lookup(...)` transaction command construction
- `DanceRequest` as the canonical public dance invocation shape
- `DanceOutcome` as a standalone public result object detached from response holons
- `TransactionAction::Query` as an SDK command target
- `query(request: QueryRequest)` and `legacyQuery(expression: QueryExpression)` as command-backed public SDK methods
- `QueryRequest`, `QueryResult`, `QueryExpression`, `Row`, and `RowSet` as canonical public query substrate

## 8. Internal TypeScript Command Layer

This layer is not part of the public developer-facing SDK, but it is mandatory for implementation.

It SHOULD be implemented with TypeScript types that structurally mirror the MAP commands specification.

### 8.1 Internal Structural Types

The internal command layer SHOULD define TypeScript structures equivalent in role to:

- `MapIpcRequest`
- `MapIpcResponse`
- `RequestOptions`
- `MapCommandWire`
- `SpaceCommandWire`
- `TransactionCommandWire`
- `TransactionActionWire`
- `HolonCommandWire`
- `HolonActionWire`
- `ReadableHolonActionWire`
- `WritableHolonActionWire`
- result wire variants needed to decode `MapResultWire`

The exact TypeScript syntax is implementation-defined.

The structure is not.

### 8.2 Internal Builder Responsibility

For each public SDK method, the internal command layer MUST:

1. choose the correct structural scope
2. construct the matching command object
3. attach required wire-layer identifiers such as `request_id`, transaction identity, and `RequestOptions`
4. wrap the command in `MapIpcRequest`
5. invoke `dispatch_map_command`
6. decode `MapIpcResponse`
7. convert the result into the public SDK return type

The internal TypeScript command layer corresponds to the host adapter side of the Rust implementation.

It owns:

- wire-envelope construction
- request metadata attachment
- wire-result decoding

It does not own runtime policy evaluation.

### 8.3 Transaction Identity Handling

`tx_id` exists only at the wire layer in the commands specification.

Therefore:

- public SDK APIs SHOULD NOT be specified in terms of raw `tx_id` values unless there is a separate product need
- internal transaction-bound SDK objects MUST retain whatever wire-layer transaction identity is needed to build transaction commands
- no domain-facing public API should pretend that TypeScript owns an `Arc<TransactionContext>` or any equivalent runtime domain context object

### 8.4 Request Identity Handling

Every IPC call MUST carry a `request_id` via `MapIpcRequest`.

The implementation spec therefore requires:

- request id generation in the internal command layer
- response/request correlation checks in the transport layer
- clear failure behavior if a malformed or mismatched response is returned

The prior draft did not specify this and was incomplete.

### 8.5 Request Options Handling

Every IPC call MUST also carry `RequestOptions`.

`RequestOptions` decisions are owned by the layer above the TypeScript SDK.

The TypeScript SDK MUST NOT decide:

- whether a given command should set `snapshot_after`
- what `gesture_id` should be attached
- what `gesture_label` should be attached

Those choices belong to DAHN, visualizers, gesture controllers, command
orchestration code, or other caller layers that know the user interaction and
snapshot policy.

The SDK's responsibility is mechanical:

- accept `RequestOptions` from the caller layer through an explicit per-call
  option, transaction/client-scoped option context, or injected
  `RequestOptions` provider
- attach the supplied `RequestOptions` to the `MapIpcRequest`
- validate that required wire fields are present and serializable
- preserve `snapshot_after`, `gesture_id`, and `gesture_label` exactly as
  supplied

If public SDK methods do not expose `RequestOptions` directly, the SDK
implementation MUST still define an explicit above-SDK source for them.

The internal command layer may apply only transport-shape defaults that are
defined by that source, such as an absent gesture id or label. It must not infer
snapshot or gesture behavior from command type, result type, transaction state,
or SDK convenience method name.

## 9. Transport Boundary

The command transport boundary collapses to one internal function.

### 9.1 Required function

| Function Signature | Notes |
|---|---|
| `invokeMapCommand(request: MapIpcRequest): Promise<MapIpcResponse>` | Internal only. Single IPC boundary. |

### 9.2 Responsibilities

`invokeMapCommand` MUST:

- accept a fully formed `MapIpcRequest`
- invoke Tauri with `dispatch_map_command`
- return `MapIpcResponse` verbatim on successful transport
- reject on transport or IPC failure

`invokeMapCommand` MUST NOT:

- infer scope
- construct commands
- perform business logic
- batch commands
- implement undo or rollback semantics

## 10. Result Mapping Requirements

For this document to drive implementation, each SDK command must have a defined public return shape and a defined wire-result decoding path.

At minimum, the implementation MUST specify result mapping for:

- transaction creation result -> `MapTransaction`
- reference-returning commands -> `HolonReference`, `TransientHolonReference`, or `SmartReference` wrappers as appropriate
- scalar-returning commands -> `string`, `number`, `null`
- plural holon-backed commands -> `HolonCollection`
- scalar property or parameter results -> `BaseValue`
- projection-producing dance response bodies -> projection-described holon handles or `HolonCollection` values whose members are projection-described holons
- dance execution results -> `DanceResponseHandle` or an equivalent thin wrapper over the returned response holon reference
- other structure-returning commands -> `EssentialHolonContent`
- void-returning commands -> successful completion with no public payload

If `MapResultWire` requires multiple variants, the TypeScript command layer MUST define a total decoder over the variants used by the SDK.

A future revision of this document may split this section into a dedicated command-result matrix. Until then, no SDK method may be implemented without an explicit result-decoding rule in code.

Because runtime now accepts bound domain commands on the Rust side, the TypeScript implementation MUST treat result decoding as part of the host adapter contract, not as a runtime concern.

Descriptor-backed result mapping must follow the same rule:

- descriptor lookup results decode into thin public descriptor handles
- the host adapter decodes wire/domain results, but it does not become the semantic owner of descriptor behavior

Holon-backed result mapping must follow the same rule:

- plural holon-backed results decode into public `HolonCollection` values or thin handles preserving the `HolonCollection` contract
- response-body references decode through the response holon's `ResponseBody` relationship rather than through a dance-specific result union
- row-shaped results must not be introduced for new command, dance, or query/navigation contracts
- lower-level vector forms may remain implementation helpers, but the public SDK boundary should preserve the `HolonCollection` contract

## 11. Error Semantics

The TypeScript SDK MUST distinguish:

- transport failure
- malformed response failure
- domain failure returned as `HolonError`

The public SDK MAY normalize these into a TS error hierarchy, but the implementation MUST preserve enough information to distinguish them in tests.

The prior draft's blanket use of "throw synchronously" was too broad and not precise enough.

Required clarification:

- SDK argument validation may fail synchronously.
- transport and runtime failures are asynchronous promise rejections.
- domain errors returned by the Rust side are asynchronous promise rejections after response decoding.

The SDK spec MUST also distinguish:

- adapter-layer failures such as malformed request construction or response mismatch
- runtime-layer domain failures returned as `HolonError`

## 12. Testing Requirements

This specification is intended to be complete enough to drive implementation and tests.

The implementation MUST include tests covering:

- one-to-one mapping from each public SDK method to exactly one internal MAP command
- correct structural scope selection
- correct `request_id` population
- correct transaction identity propagation for transaction-scoped commands
- correct holon target propagation for holon-scoped commands
- correct result decoding for every public SDK method
- correct `HolonCollection` decoding for plural command results and operands
- correct `DanceV2` decoding into response-holon handles
- failure decoding for `HolonError`
- absence of wire-type leakage from public exports
- absence of public `TransactionAction::Query`, `QueryRequest`, `QueryResult`, `Row`, `RowSet`, and alternate plural collection target contracts

## 13. Implementation Guarantees

- Every SDK method maps to exactly one MAP command.
- The public SDK exposes no wire types.
- The internal command layer mirrors the current structural command architecture.
- The SDK uses exactly one IPC entrypoint: `dispatch_map_command`.
- Descriptor-facing public APIs remain thin and reference-backed.
- The SDK does not re-implement descriptor inheritance flattening in TypeScript.
- Descriptor-owned semantics are surfaced without duplicating runtime rule systems in TS.
- Public plural holon-backed results and operands converge on `HolonCollection`.
- New-world direct dance invocation uses a holon-backed `DanceInvocation` handle through `DanceV2`.
- New-world dance results return response holon handles whose descriptors extend `DanceResponseType`.
- Navigation/query-like SDK helpers invoke descriptor-afforded Dances and do not introduce a command-owned query envelope.
- No command families from the older draft remain in the implementation spec.
- No SDK method is specified for commands explicitly excluded from the MAP Commands API surface.
- No undo or rollback command behavior is specified unless and until those commands are added to `commands.md`.

## 14. Final Note

This document is the authoritative implementation specification for the TypeScript MAP SDK as aligned to the current MAP Commands, Dances, and query/navigation designs.

If the commands specification changes, this document MUST be updated by preserving the same layering model:

- ergonomic public SDK
- structural internal command layer
- transport-only wire boundary
