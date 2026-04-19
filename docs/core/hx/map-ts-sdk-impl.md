# TypeScript MAP SDK — Implementation Specification

## 1. Overview

This document defines the implementation specification for the TypeScript MAP SDK.

It is intended for MAP Core developers responsible for:

- implementing and maintaining the SDK
- keeping the SDK aligned with the canonical MAP Commands surface
- implementing the TypeScript-side command construction layer
- implementing and testing the TS ↔ Rust IPC boundary

This document is normative for the TypeScript implementation.

It is subordinate to [commands.md](../commands-and-runtime/commands.md) for command architecture and [commands-cheat-sheet.md](../commands-and-runtime/commands-cheat-sheet.md) for the condensed structural reference.

## 2. Design Goal

The TypeScript side is composed of two distinct layers:

1. A public SDK layer that exposes ergonomic TypeScript APIs to MAP client developers.
2. An internal command layer that constructs TypeScript command objects and wire types, then invokes the single MAP IPC entrypoint.

The public SDK layer MUST NOT expose wire types.

The internal command layer MUST mirror the current MAP Commands structure closely enough that each SDK method maps to exactly one MAP command.

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

The TypeScript implementation SHOULD also reflect the current crate split conceptually:

- contract-facing command/result shapes
- wire-facing IPC envelope shapes
- runtime-facing execution boundary

The TypeScript SDK does not need to replicate the Rust crate layout literally.

It does need to preserve the same separation of concerns.

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

| Function Signature | Emits | Notes |
|---|---|---|
| `commit(): Promise<void>` | `MapCommandWire.Transaction(Commit)` | Ends the transaction. The SDK spec should not invent a return payload unless the wire/result spec defines one. |
| `newHolon(key?: string): Promise<TransientHolonReference>` | `MapCommandWire.Transaction(NewHolon { key })` | Creates a new transient holon. |
| `stageNewHolon(source: TransientHolonReference): Promise<HolonReference>` | `MapCommandWire.Transaction(StageNewHolon { source })` | Stages a new holon from a transient source. |
| `stageNewFromClone(original: HolonReference, newKey: string): Promise<HolonReference>` | `MapCommandWire.Transaction(StageNewFromClone { original, new_key })` | Stages a clone with a new base key. |
| `stageNewVersion(currentVersion: SmartReference): Promise<HolonReference>` | `MapCommandWire.Transaction(StageNewVersion { current_version })` | Stages a new version from a smart reference. |
| `stageNewVersionFromId(holonId: HolonId): Promise<HolonReference>` | `MapCommandWire.Transaction(StageNewVersionFromId { holon_id })` | Present in current commands spec and was missing from the prior SDK draft. |
| `deleteHolon(localId: LocalId): Promise<void>` | `MapCommandWire.Transaction(DeleteHolon { local_id })` | Deletes a local holon within the active transaction. |
| `loadHolons(bundle: HolonReference): Promise<void>` | `MapCommandWire.Transaction(LoadHolons { bundle })` | Current commands spec uses `HolonReference` for `bundle`; prior SDK draft was out of sync. |
| `dance(request: DanceRequest): Promise<DanceResult>` | `MapCommandWire.Transaction(Dance(request))` | Public only if the TS SDK intends to surface DANCE directly; if not, mark as internal-only in package exports, but the implementation spec must still account for it. |
| `query(expression: QueryExpression): Promise<QueryResult>` | `MapCommandWire.Transaction(Query(expression))` | Public only if query execution is part of the SDK promise; otherwise retain as internal but specified. |
| `getAllHolons(): Promise<HolonCollection>` | `MapCommandWire.Transaction(GetAllHolons)` | Transaction-scoped lookup. |
| `getStagedHolonByBaseKey(key: string): Promise<HolonReference \| null>` | `MapCommandWire.Transaction(GetStagedHolonByBaseKey { key })` | |
| `getStagedHolonsByBaseKey(key: string): Promise<HolonCollection>` | `MapCommandWire.Transaction(GetStagedHolonsByBaseKey { key })` | |
| `getStagedHolonByVersionedKey(key: string): Promise<HolonReference \| null>` | `MapCommandWire.Transaction(GetStagedHolonByVersionedKey { key })` | |
| `getTransientHolonByBaseKey(key: string): Promise<TransientHolonReference \| null>` | `MapCommandWire.Transaction(GetTransientHolonByBaseKey { key })` | |
| `getTransientHolonByVersionedKey(key: string): Promise<TransientHolonReference \| null>` | `MapCommandWire.Transaction(GetTransientHolonByVersionedKey { key })` | |
| `stagedCount(): Promise<number>` | `MapCommandWire.Transaction(StagedCount)` | |
| `transientCount(): Promise<number>` | `MapCommandWire.Transaction(TransientCount)` | |

### 6.3 ReadableHolon

`ReadableHolon` is the public read-only facade for a holon target.

Each method emits a holon-scoped command targeting the bound holon reference.

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
| `addRelatedHolons(relationshipName: RelationshipName, holons: HolonReference[]): Promise<void>` | `MapCommandWire.Holon(Write(AddRelatedHolons { name, holons }))` | |
| `removeRelatedHolons(relationshipName: RelationshipName, holons: HolonReference[]): Promise<void>` | `MapCommandWire.Holon(Write(RemoveRelatedHolons { name, holons }))` | |
| `withDescriptor(descriptor: HolonReference): Promise<void>` | `MapCommandWire.Holon(Write(WithDescriptor { descriptor }))` | |

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

The implementation spec therefore requires explicit SDK behavior for:

- defaulting `snapshot_after`
- passing through `gesture_id` when available
- passing through `gesture_label` when available

If public SDK methods do not expose these values directly, the internal command layer MUST still define how they are sourced or defaulted.

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
- structure-returning commands -> `EssentialHolonContent`, `HolonCollection`, `DanceResult`, `QueryResult`
- void-returning commands -> successful completion with no public payload

If `MapResultWire` requires multiple variants, the TypeScript command layer MUST define a total decoder over the variants used by the SDK.

A future revision of this document may split this section into a dedicated command-result matrix. Until then, no SDK method may be implemented without an explicit result-decoding rule in code.

Because runtime now accepts bound domain commands on the Rust side, the TypeScript implementation MUST treat result decoding as part of the host adapter contract, not as a runtime concern.

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
- failure decoding for `HolonError`
- absence of wire-type leakage from public exports

## 13. Implementation Guarantees

- Every SDK method maps to exactly one MAP command.
- The public SDK exposes no wire types.
- The internal command layer mirrors the current structural command architecture.
- The SDK uses exactly one IPC entrypoint: `dispatch_map_command`.
- No command families from the older draft remain in the implementation spec.
- No SDK method is specified for commands explicitly excluded from the MAP Commands API surface.
- No undo or rollback command behavior is specified unless and until those commands are added to `commands.md`.

## 14. Final Note

This document is the authoritative implementation specification for the TypeScript MAP SDK as aligned to the current MAP Commands design.

If the commands specification changes, this document MUST be updated by preserving the same layering model:

- ergonomic public SDK
- structural internal command layer
- transport-only wire boundary
