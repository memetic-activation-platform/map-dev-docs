# TypeScript MAP SDK — Implementation Specification

## 1. Overview

This document defines the **implementation specification** for the **TypeScript MAP SDK**, intended for **MAP Core developers** who are responsible for:

- implementing and maintaining the SDK
- ensuring parity with the MAP Core Rust APIs
- implementing the Rust-side command dispatcher
- writing unit, integration, and contract tests across the TS ↔ Rust boundary

### 1.1 Architectural Position

The TypeScript MAP SDK is a **privileged, experience-facing interface** used by DAHN and Visualizers to interact with MAP Core.

It transforms ergonomic, object-oriented method calls into **structured MAP Commands** that are executed by the Rust client.

```Human Interaction  
↓  
DAHN / Visualizers  
↓  
TypeScript MAP SDK  
↓  
MapRequest / MapResponse  
↓  
Rust Client (Conductora)  
↓  
MAP Core APIs (Holons, Transactions)
```

---

## 2. SDK API Surface — Implementers Reference Tables

This section provides **implementation-ready reference tables** for each SDK surface.

Each table enumerates:
- the full **function signature**
- the **exact MAP Command** emitted
- **notes and invariants** required for correctness and test construction

These tables are the **authoritative checklist** for SDK implementation.

---

## 2.1 MapClient (Client-Side Execution Context)

### Purpose and Role

`MapClient` is the **client-side execution context object** for the TypeScript MAP SDK.

It represents the **minimum authority and identity bundle** required to issue MAP Commands from the TypeScript runtime into the Rust host. Every SDK operation—query or mutation—executes *relative to* a `MapClient` instance.

`MapClient` is **not** an API root, service façade, or global singleton. It is a **scoped, capability-bearing context handle**, intentionally analogous to Rust’s `HolonsContextBehavior`.

---

### Conceptual Analogy (Rust ↔ TypeScript)

| Rust (MAP Core)               | TypeScript (MAP SDK)                 |
|-------------------------------|--------------------------------------|
| `HolonsContextBehavior`       | `MapClient`                          |
| Holds Space + Transaction     | Holds `contextId` + `transactionId`  |
| Passed into every API call    | Attached to every `MapRequest`       |
| Evolves without breaking APIs | Evolves without breaking SDK surface |

The SDK never materializes, inspects, or mutates the Rust context.  
It merely supplies the **identifiers** required for the Rust host to resolve the correct execution environment.

---

### What a MapClient *Is*

A `MapClient` instance:

- Identifies **which AgentSpace** the request targets (via `contextId`)
- Identifies **which transaction** the request executes within
- Carries **no domain state**
- Carries **no HolonPools**
- Carries **no undo stack**
- Carries **no authorization logic**

All stateful behavior lives exclusively in the Rust host, behind the Commands interface.

---

### What a MapClient *Is Not*

`MapClient` does **not**:

- Materialize Holons
- Expose MAP Core internals
- Perform authorization or TrustChannel checks
- Maintain transaction state
- Implicitly create transactions
- Act as a long-lived global handle

---

### Transaction Binding Model

A `MapClient` is always in exactly **one of two states**:

1. **Unbound** — no transaction
2. **Transaction-bound** — associated with a specific `transactionId`

Only a **transaction-bound** `MapClient` may issue SDK operations.

All SDK functions MUST synchronously reject execution if invoked on an unbound client.

---

### Derivation and Immutability

`MapClient` instances are **immutable**.

Operations such as `beginTransaction()` return a **new derived `MapClient`**, leaving the original instance unchanged and unbound.

This mirrors Rust’s pattern of passing context objects by reference rather than mutating them in place.

---

### Lifecycle Summary

- A base `MapClient` is created by the host runtime (e.g., DAHN bootstrap)
- `beginTransaction()` derives a transaction-bound client
- All SDK operations execute through that client
- `commit()` or `rollback()` invalidates the transaction-bound client
- Invalid clients MUST reject further calls synchronously

---

## 2.2 ReadableHolon (Query Facade)

| Function Signature                                                            | Command                               | Notes                                                                                        |
|-------------------------------------------------------------------------------|---------------------------------------|----------------------------------------------------------------------------------------------|
| `propertyValue(propertyName: PropertyName): Promise<BaseValue \| null>`       | `QueryCommand.Holon.GetPropertyValue` | Executes within transaction scope if present. Must resolve via transaction-local HolonPools. |
| `relatedHolons(relationshipName: RelationshipName): Promise<HolonCollection>` | `QueryCommand.Holon.GetRelatedHolons` | Returns collection of `HolonReference`s; no materialization.                                 |
| `essentialContent(): Promise<EssentialHolonContent>`                          | `QueryCommand.Holon.EssentialContent` | Includes descriptor, key, properties.                                                        |
| `key(): Promise<string \| null>`                                              | `QueryCommand.Holon.Key`              | Base key only; versioned key separate.                                                       |
| `versionedKey(): Promise<string>`                                             | `QueryCommand.Holon.VersionedKey`     | Always present for valid Holon.                                                              |
| `predecessor(): Promise<HolonReference \| null>`                              | `QueryCommand.Holon.Predecessor`      | Null if no lineage.                                                                          |
| `allRelatedHolons(): Promise<Record<RelationshipName, HolonCollection>>`      | `QueryCommand.Holon.AllRelatedHolons` | Aggregated relationship traversal; may be heavy.                                             |

---

## 2.3 WritableHolon (Mutation Facade)

**Precondition for all functions**  
A `transactionId` MUST be present on the `MapClient`.  
The SDK MUST throw synchronously if absent.

| Function Signature                                                                                 | Command                                     | Notes                                  |
|----------------------------------------------------------------------------------------------------|---------------------------------------------|----------------------------------------|
| `withPropertyValue(propertyName: PropertyName, value: BaseValue): Promise<void>`                   | `MutationCommand.Holon.WithPropertyValue`   | Produces `UndoToken`.                  |
| `removePropertyValue(propertyName: PropertyName): Promise<void>`                                   | `MutationCommand.Holon.RemovePropertyValue` | Produces `UndoToken`.                  |
| `addRelatedHolons(relationshipName: RelationshipName, holons: HolonReference[]): Promise<void>`    | `MutationCommand.Holon.AddRelatedHolons`    | Batch add; order not guaranteed.       |
| `removeRelatedHolons(relationshipName: RelationshipName, holons: HolonReference[]): Promise<void>` | `MutationCommand.Holon.RemoveRelatedHolons` | No-op if not present.                  |
| `withPredecessor(predecessor: HolonReference \| null): Promise<void>`                              | `MutationCommand.Holon.WithPredecessor`     | Lineage mutation; undoable pre-commit. |
| `withDescriptor(descriptor: HolonReference): Promise<void>`                                        | `MutationCommand.Holon.WithDescriptor`      | Descriptor change affects validation.  |

---

## 2.4 HolonOperations (Standalone Commands)

| Function Signature | Command | Notes |
|-------------------|---------|-------|
| `newHolon(key?: string): Promise<HolonReference>` | `OperationsMutation.NewHolon` | Creates TransientHolon; undoable. |
| `stageNewHolon(transient: TransientReference): Promise<HolonReference>` | `OperationsMutation.StageNewHolon` | Moves transient → staged. |
| `stageNewFromClone(original: HolonReference, newKey: string): Promise<HolonReference>` | `OperationsMutation.StageNewFromClone` | Clone without lineage. |
| `stageNewVersion(current: SmartReference): Promise<HolonReference>` | `OperationsMutation.StageNewVersion` | Clone with predecessor. |
| `deleteHolon(localId: LocalId): Promise<void>` | `OperationsMutation.DeleteHolon` | Only local holons allowed. |
| `loadHolons(bundle: TransientReference): Promise<TransientReference>` | `OperationsMutation.LoadHolons` | Host-side bulk load. |
| `commit(): Promise<TransientReference>` | `OperationsMutation.Commit` | Ends transaction; invalidates undo tokens. |
| `rollback(): Promise<void>` | `OperationsMutation.Rollback` | Transaction-scoped rollback only. |
| `stagedCount(): Promise<number>` | `OperationsQuery.StagedCount` | Observes transaction-local state. |
| `transientCount(): Promise<number>` | `OperationsQuery.TransientCount` | Observes transaction-local state. |

---

## 2.5 Undo (SDK-Orchestrated)

| Function Signature | Command | Notes |
|-------------------|---------|-------|
| `undo(): Promise<void>` | `OperationsMutation.Undo` | Uses stored `UndoToken`; valid only pre-commit. |

---

## 3. Command Transport Boundary

The **Command Transport** is intentionally minimal and collapses to **a single function**.

This is by design.

### 3.1 invokeMapCommand

| Function Signature | Command | Notes |
|-------------------|---------|-------|
| `invokeMapCommand(request: MapRequest): Promise<MapResponse>` | — | Single IPC boundary; all SDK logic stops here. |

### 3.2 Semantics

- This function is **internal** to the SDK implementation
- It is the **only place** where:
    - Tauri JSON IPC is invoked
    - serialization and deserialization occurs
- It performs **no business logic**

### 3.3 Responsibilities

`invokeMapCommand` MUST:
- accept a fully-formed `MapRequest`
- invoke the Tauri command endpoint (`map_request`)
- return the resulting `MapResponse` verbatim
- reject the Promise on IPC or transport failure

`invokeMapCommand` MUST NOT:
- construct commands
- interpret responses
- perform retries
- apply undo logic
- mutate SDK state

---

## 4. Implementation Guarantees

- Every SDK function maps to **exactly one** MAP Command
- No SDK function batches or chains commands implicitly
- Transaction scope is explicit and enforced
- Undo is capability-based, not state-based
- Queries are idempotent and transaction-aware
- Transport logic is centralized and minimal

---

## 5. Final Note

This document is the **authoritative implementers’ specification** for the TypeScript MAP SDK.

If a function is not listed here:
- it is not part of the SDK
- it must not emit MAP Commands
- or it belongs in a different layer (Suite, DAHN, Visualizer)

The SDK exists to translate **human-scale intent** into **MAP-correct execution** — no more, no less.