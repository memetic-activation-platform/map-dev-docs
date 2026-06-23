# MAP Query Architecture

This document identifies the runtime architecture for MAP query execution.Its purpose is to provide a high-level overview of the major components of the MAP Query architecture and how they relate to one another.

---

## Core Runtime Position

MAP query execution is provided by a `holons_core` resident query engine that
implements the `QueryDance`.

The query engine is reached through the same canonical dance invocation seam used elsewhere in MAP.

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

The runtime architecture therefore separates:

- ingress adapters, which receive requests from particular channels
- the canonical dance execution seam, which binds and dispatches a
  `DanceInvocation`
- the query engine, which executes the `QueryDance`
- host and guest execution sites, which determine where the work runs

---

## Runtime Components

### `holons_core` Query Engine

The `holons_core` resident query engine is the canonical runtime for MAP query
execution.

Its architectural responsibility is to execute the `QueryDance` against a
`QueryDanceRequest`, producing an `ExecutionInstance` and a
`HolonCollection` result. It is the common runtime surface behind the different
ingress paths.

It owns query execution behavior. It does not own the transport envelopes used
to bring requests into the system.

### Ingress Adapters

Ingress adapters translate a particular boundary surface into the canonical
`DanceInvocation` and `QueryDanceRequest` execution seam.

They stamp or validate ingress-specific authority and envelope details, then
dispatch through the shared query engine.

Ingress adapters do not define query semantics. They are boundary-layer entry
points into the same runtime.

### Host Runtime

The host runtime is the place where canonical dance dispatch and orchestration
occur.

For query execution, the host is responsible for receiving ingress traffic,
binding a `DanceInvocation`, and dispatching the `QueryDance` through the
`holons_core` query engine.

The host is also the architectural home for cross-space orchestration, though
that larger distributed model is outside the scope of this document.

### Guest Runtime

The guest runtime is where single-space query work may execute inside one hApp /
one `HolonSpace` execution context.

Guest execution is local execution. It is not the general cross-space
coordinator. It executes query work for the current space when the host routes
that work into the guest-resident execution context.

---

## Ingress Paths

### MAP Client Via Dance Commands

One ingress path begins with a MAP client, typically through the TypeScript
experience layer.

In this path:

1. the client issues a Dance Command through the normal command ingress surface
2. the command payload carries or lowers to a `DanceInvocation`
3. the host command adapter binds that invocation
4. the host dispatches the `QueryDance` through the `holons_core` query engine

Architecturally, Commands are the client-to-host ingress adapter. They are not
the semantic home of query execution.

### TrustChannel Ingress

Another ingress path begins with TrustChannel-delivered dance traffic.

In this path:

1. a TrustChannel message delivers a Dance Capsule or equivalent trust-channel
   envelope
2. the TrustChannel ingress layer unwraps that envelope
3. the unwrapped invocation is adapted into the canonical `DanceInvocation`
   surface
4. the host dispatches the `QueryDance` through the same `holons_core` query
   engine

The important architectural point is that TrustChannel ingress is a different
transport and authority path, not a different query engine.

### hApp Guest-Resident Single-Space Execution

Single-space query graphs may execute inside the guest-resident hApp context.

In this path:

1. query work is bound to one current `HolonSpace` / hApp execution context
2. the query executes locally for that space
3. the execution remains one-space only
4. the resulting collection is returned through the same overall query model

This guest-resident path matters because MAP query execution is space-scoped at
runtime. A single step execution does not straddle multiple hApps.

---

## Architectural Boundaries

This runtime architecture depends on a few firm boundaries.

- The query engine implements `QueryDance`; ingress surfaces adapt into it.
- Commands are one ingress path; they do not define query semantics.
- TrustChannels are another ingress path; they do not define a second query
  runtime.
- Guest execution is valid for single-space query graphs; it is not the
  cross-space coordinator.
- Host runtime dispatch remains the common architectural seam across ingress
  paths.

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

