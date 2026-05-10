# Query Envelope and Contract Path

This document defines the `Query PRO2` contract path for MAP queries.

Its purpose is to stabilize the end-to-end query interface early enough for:

- TypeScript SDK convergence
- DAHN-facing API work
- Commands-layer ingress alignment
- later query, dance, and command contract reuse

without overcommitting MAP to a finished query runtime before descriptor-aware
semantic work is ready.

## Core Posture

The query contract path spans:

- the public TypeScript SDK query API
- the Commands client-to-host ingress layer
- host-side adaptation into the shared query substrate boundary
- materialized query result shapes returned to callers

This layer is intentionally narrower than the full future query engine.

It does **not** define:

- descriptor-backed structural interrogation
- predicate or operator semantics
- planner or distributed execution behavior
- the final internal execution representation

## Responsibility Boundaries

The intended responsibility split is:

- **TypeScript SDK layer**
  - owns the public query API surface exposed to TS and DAHN consumers
  - does not own query semantics or execution behavior

- **Commands ingress layer**
  - owns the client-to-host invocation path for TS callers
  - adapts query requests into the shared query substrate contract
  - does not become the architectural home of query semantics or execution

- **Shared query substrate layer**
  - is the intended long-term home of the canonical query contract below Commands
  - must remain reusable by non-TS ingress paths, including dance-initiated and trust-channel-initiated query flows
  - is where later execution and semantic work should attach

- **Boundary / wire layer**
  - owns serialization, transport-safe shapes, and binding across host/process boundaries
  - remains distinct from substrate semantics and execution logic

## Deferred Projection

`Value`, `Row`, and `RowSet` remain the shared materialized contract and
serialized shapes for MAP query-adjacent APIs.

They are **not** necessarily the interpreter's internal binding model.

Execution layers may retain richer runtime bindings, including
`HolonReference`-backed or otherwise descriptor-aware execution state, and
materialize `Value`, `Row`, or `RowSet` only when a contract or operator
actually requires those shapes.

This means:

- `Row` is a valid contract/output shape
- `RowSet` is a valid contract/result shape
- neither implies eager projection of intermediate execution state

## Current-Phase Delivery

`Query PRO2` is expected to wire the stack from the SDK through Commands to the
substrate boundary without claiming that the new substrate is already
implemented.

Near-term behavior may therefore include:

- request/result contract stabilization
- wire-shape stabilization
- adapter-path stabilization
- explicit placeholder seams below Commands

while still deferring:

- descriptor-aware structure
- predicate semantics
- navigation algebra execution
- planner and declarative evolution

## Legacy Relationship

The existing query/navigation path remains transitional:

- legacy `QueryExpression`
- `Node`
- `NodeCollection`
- `QueryPathMap`

`Query PRO2` does not require immediate cutover or removal of that path.
Instead, it establishes the new contract path in parallel so future PRS work can
attach to the right layer without making Commands or the legacy traversal model
the long-term home of MAP query behavior.
