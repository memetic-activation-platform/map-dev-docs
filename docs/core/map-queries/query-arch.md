# MAP Query Architecture

This document identifies the concrete runtime architecture for MAP query
execution.

Its purpose is to name the actual runtime components, show how they relate, and
explain the ingress and execution path for MAP queries at the architectural
layer.

It does not define the query algebra, planner semantics, distributed fanout
rules, or schema details. Those belong in:

- [query-engine-design-spec.md](/Users/stevemelville/dev/map-dev-docs/docs/core/map-queries/query-engine-design-spec.md)
- [command-dance-query-schema-dsl.md](/Users/stevemelville/dev/map-dev-docs/docs/core/map-queries/command-dance-query-schema-dsl.md)
- [dist-query-concept.md](/Users/stevemelville/dev/map-dev-docs/docs/core/map-queries/dist-query-concept.md)

---

## Core Runtime Position

MAP query execution is provided by a `holons_core` resident query engine that
implements the `QueryDance`.

The query engine is not a separate query-only subsystem. It is reached through
the same canonical dance execution seam used elsewhere in MAP.

The core rule is:

```text
Command = ingress envelope and lifecycle policy.
Dance = descriptor-afforded executable behavior.
Query = request payload supplied to a Query Dance.
```

For query execution, that becomes:

```text
DanceInvocation
  -> QueryDance
  -> QueryDanceRequest
  -> QueryGraph
  -> ExecutionInstance
  -> HolonCollection result
```

At the architectural level, the concrete runtime path is:

```text
MAP client or TrustChannel peer
  -> ingress adapter
  -> DanceInvocation
  -> Integration Hub host runtime
  -> holons_core::execute_dance_v2(...)
  -> QueryDance implementation
  -> single-space execution in one HolonSpace / hApp context
  -> HolonCollection result
```

---

## Runtime Components

### TypeScript Experience Layer

The TypeScript experience layer is one caller of MAP query execution.

It may initiate a query through the Commands IPC surface, but it does not own
query execution semantics and it does not execute query logic locally.

### Tauri IPC Entry Point

For command-based ingress, the first concrete runtime component is the Tauri IPC
entry point:

```rust
dispatch_map_command(request: MapIpcRequest, ...)
```

This is the single IPC ingress for MAP Commands. It receives `MapIpcRequest`
from the client side and passes control into the host-side command adapter.

### Host-Side MAP Command Adapter

The host-side MAP command adapter binds wire-safe IPC payloads into host-side
runtime values inside the Integration Hub.

For query execution through Commands, it is responsible for:

- parsing `MapIpcRequest`
- binding the request into host/runtime shapes
- handling the `TransactionAction::DanceV2` command path
- carrying or resolving the `HolonReference` to a `DanceInvocation`

This is still an ingress component. It is not the query engine itself.

### `DanceInvocation`

`DanceInvocation` is the canonical execution request record shared across query
ingress paths.

It identifies:

- the invoked `DanceType`
- the `AffordingHolon`
- the request holon
- the ingress source

For query execution, the request holon is a `QueryDanceRequest`, which points to
the `QueryGraph` and its initial bindings.

### Integration Hub Host Runtime

Commands execute entirely within the Rust Integration Hub host runtime.

This is the canonical dispatch site for MAP query execution. It receives a bound
`DanceInvocation`, resolves the local dance contract, and invokes the canonical
dance executor.

This host runtime is also the architectural home for cross-space orchestration,
though the distributed model itself is outside the scope of this document.

### `holons_core` Dance Executor

The canonical dance execution seam is `holons_core::execute_dance_v2(...)`.

This is the key shared runtime component behind both Commands ingress and
TrustChannel ingress. Different ingress adapters feed into the same executor.

The executor:

- reads the `DanceInvocation`
- resolves `DanceInvocation.DanceName` to the local `DanceType`
- validates the invocation and request contract
- binds the invocation into a `BoundDanceInvocation` or equivalent resolved form
- selects the `DanceImplementation`
- executes it and returns the dance response

### `QueryDance` Implementation

The `QueryDance` implementation is the query engine proper.

It accepts a `QueryDanceRequest`, executes the `QueryGraph`, creates an
`ExecutionInstance`, and produces the final `HolonCollection`.

Architecturally, query execution is therefore an ordinary dance executed through
the common `holons_core` dance runtime.

### Guest-Side hApp / `HolonSpace` Execution Context

Single-space query work may execute inside one guest-resident hApp / one
`HolonSpace` execution context.

This is the local execution site for one space-scoped branch of query work. It
is not the general cross-space coordinator.

---

## Ingress Paths

### MAP Client Via Dance Commands

One ingress path begins with a MAP client, typically through the TypeScript
experience layer.

The concrete flow is:

1. the experience layer issues a command request
2. the request enters `dispatch_map_command(...)`
3. the host-side MAP command adapter binds `MapIpcRequest` into host runtime
   values
4. query dance invocation is carried through `TransactionAction::DanceV2`
5. the Integration Hub host runtime dispatches the bound `DanceInvocation`
6. the host calls `holons_core::execute_dance_v2(...)`
7. the executor resolves and runs the `QueryDance`

Commands are therefore the client-to-host ingress adapter. They are not the
semantic home of query execution.

### TrustChannel Ingress

Another ingress path begins with TrustChannel-delivered dance traffic.

The concrete flow is:

1. a TrustChannel message delivers a Dance Capsule or equivalent trust-channel
   envelope
2. the TrustChannel ingress layer validates that channel's authority
3. the ingress layer unwraps the capsule into the canonical `DanceInvocation`
   surface
4. the Integration Hub host runtime dispatches that invocation
5. the host calls the same `holons_core::execute_dance_v2(...)` seam
6. the executor resolves and runs the same `QueryDance`

TrustChannel ingress is a different transport and authority path, not a
different query engine.

### hApp Guest-Resident Single-Space Execution

Single-space query graphs may execute inside the guest-resident hApp context.

The concrete execution rule is:

1. the current query work is bound to one `HolonSpace`
2. that space corresponds to one hApp execution context
3. query execution runs locally for that one space
4. a step execution does not straddle multiple hApps
5. the local result is returned through the same `QueryDance` execution model

This guest-resident path matters because MAP query execution is space-scoped at
runtime.

---

## How The Components Relate

The concrete relationship between components is:

- The experience layer calls the Tauri IPC entry point when query ingress comes
  from a client.
- The Tauri IPC entry point forwards to the host-side MAP command adapter.
- The command adapter binds `MapIpcRequest` into
  `TransactionAction::DanceV2` carrying a `DanceInvocation`.
- The Integration Hub host runtime dispatches that invocation.
- The host calls `holons_core::execute_dance_v2(...)`.
- The `holons_core` executor resolves and runs the `QueryDance`.
- The `QueryDance` executes the query against one current `HolonSpace` / hApp
  context at a time.

TrustChannel ingress differs only in its outer adapter:

- TrustChannel transport and capsule handling replace Tauri IPC and
  `MapIpcRequest`.
- After unwrapping, it rejoins the same
  `DanceInvocation -> execute_dance_v2 -> QueryDance` path.

---

## Architectural Boundaries

This runtime architecture depends on a few firm boundaries.

- The query engine lives in the `QueryDance` implementation executed through
  `holons_core`.
- `dispatch_map_command(...)` and `MapIpcRequest` are command ingress
  components, not query-semantic components.
- `DanceInvocation` is the common execution request surface shared across
  ingress paths.
- The Integration Hub host runtime is the canonical dispatch site.
- TrustChannel ingress is a different adapter into the same host and executor
  seam.
- Guest-side hApp execution is valid for single-space query graphs, but it is
  not the cross-space coordinator.

---

## Out Of Scope

This document does not attempt to specify:

- the `QueryGraph` and `QueryStep` execution model in detail
- query algebra operators and validation semantics
- projection, path, scalar, or explanation result modeling
- distributed fanout, delegated execution, and result merge rules
- planner algebra or declarative OpenCypher / GQL compilation
- core schema relationship and property definitions

Those concerns belong in the query engine design spec, schema DSL, and
distributed query concept documents.

