## TypeScript MAP SDK — Core Specification

### Purpose

The **TypeScript MAP SDK** provides an **ergonomic, strongly-typed interface** for interacting with the MAP Core from human-facing runtime layers, primarily:

- **DAHN (Distributed Agentic Human Narratives)**
- **Visualizers**
- Other host-side experience orchestration components

The SDK is **not** a Suite API and is **not** intended for Suite authors.  
Suites expose **Dances**; the SDK exposes **MAP Core interaction capabilities**.

This document specifies the **architectural role, scope, and layering** of the TypeScript MAP SDK for MAP implementers.

---

### Audience

**Primary consumers**
- DAHN developers
- Visualizer developers
- Host-side experience and orchestration logic

**Secondary consumers**
- MAP core maintainers (for parity and evolution)

**Explicitly not for**
- Suite authors
- Guest-side (WASM) code
- Direct domain mutation outside MAP Core

---

### Position in the MAP Stack

The TypeScript MAP SDK sits at the **top of the MAP interaction stack**, translating human-intent–level operations into structured MAP Core Commands.

```
Human Interaction
   ↓
DAHN / Visualizers
   ↓
TypeScript MAP SDK
   ↓
Command Protocol (MapRequest / MapResponse)
   ↓
Rust Host (Conductora)
   ↓
MAP Core / Holons / Transactions
```

The SDK is **experience-facing**, not domain-facing.

---

### Core Responsibilities

The TypeScript MAP SDK is responsible for:

- Providing **ergonomic, object-oriented facades** over MAP Core capabilities
- Preserving **Rust–TypeScript parity** in naming, structure, and semantics
- Grouping operations at **human-action granularity**
- Managing **presentation-level undo/redo**
- Constructing and issuing **Command requests** to the Rust Host
- Decoding structured responses into typed objects

The SDK is **not responsible** for:

- Authorization or policy enforcement
- Transaction execution
- Persistence
- Domain invariants
- TrustChannel enforcement

---

### Architectural Principles

#### 1. Ergonomics without semantic leakage

The SDK exposes method-style APIs (e.g. `ReadableHolon.property_value`) even though MAP Core operates on Commands.  
This is a **developer convenience**, not a semantic abstraction leak.

#### 2. Strong parity with Rust Core

Wherever possible:

- Method names mirror Rust traits and APIs
- Types preserve structural shape (e.g. `HolonReference`, `PropertyMap`)
- Case conventions are enforced:
    - `PascalCase` for types
    - `snake_case` for properties
    - `SCREAMING_SNAKE_CASE` for relationships

#### 3. Experience-level undo only

Undo/redo in the SDK:
- Operates at the **UI / experience layer**
- Is scoped to **pre-commit transactions**
- Does **not** attempt to undo committed MAP state

After commit, reversal is expressed only through **explicit compensating actions**, not undo.

---

### High-Level API Surface

The SDK exposes **three primary surfaces**:

1. **Holon Facades**
2. **Holon Operations**
3. **Client & Transport**

---

## 1. Holon Facades

Holon facades provide **method-based access** to MAP state via references.  
They do not materialize Holons.

### ReadableHolon

A façade over a `HolonReference` that exposes **query-only** operations.

Examples:
- `property_value(name)`
- `essential_content()`
- `all_related_holons()`
- `predecessor()`

Characteristics:
- Non-mutating
- Idempotent
- Safe to invoke repeatedly
- Often drive **screen state updates**

Readable operations **do not participate in MAP undo**, but may be tracked by the UI for presentation rollback.

---

### WritableHolon

Extends `ReadableHolon` with **mutation operations**.

Examples:
- `with_property_value(name, value)`
- `remove_property_value(name)`
- `add_related_holons(relationship, holons)`
- `with_predecessor(predecessor)`

Characteristics:
- Always routed as **Mutation Commands**
- Always executed **within a transaction**
- May return **undo capabilities**
- Represent **human-initiated actions**

Writable operations define **undo boundaries** at the experience layer.

---

## 2. Holon Operations

Holon Operations are **standalone, high-level actions** that do not conceptually belong to a single Holon instance.

Examples:
- `new_holon`
- `stage_new_holon`
- `stage_new_version`
- `commit`
- `delete_holon`
- `summarize`
- `staged_count`
- `transient_count`

Characteristics:
- Map 1:1 to Rust `holon_operations_api`
- Often mutate global transaction state
- Always routed through Command dispatch
- May return undo capabilities

Holon Operations are the **primary way DAHN drives structural change**.

---

## 3. Client and Transport

### MapClient

`MapClient` is the **single entry point** into MAP Core from TypeScript.

Responsibilities:
- Issue Commands
- Construct typed references
- Abstract transport details
- Maintain parity across runtimes

The client does **not**:
- Maintain MAP state
- Perform authorization
- Enforce transactions

---

### Transport Abstraction

The SDK defines a minimal `Transport` interface:

- No runtime assumptions
- No hard dependency on Tauri
- Supports testing and alternate runtimes

Example implementations:
- `TauriTransport`
- `MockTransport`
- `IdEncodingTransport` (decorator)

---

### ID Encoding Boundary

Binary identifiers (`LocalId`, `HolonId`, etc.) are:

- Represented as structured types in memory
- Encoded/decoded at the JSON boundary
- Never manipulated manually by SDK consumers

This preserves correctness and Rust parity.

---

## Undo and Transactions (SDK Perspective)

### Undo Scope

The SDK manages **presentation undo**, not domain undo.

- Undo groups correspond to **human actions**
- Undo applies only to **uncommitted changes**
- Undo reverts:
    - UI state
    - provisional MAP changes via undo tokens

### Transaction Boundary

A **transaction marks the end of undoability**.

After `commit`:
- Undo is no longer available
- Returned undo capabilities are invalid
- Reversal requires **new compensating actions**

This aligns UI semantics with MAP Core invariants.

---

## Relationship to Suites and Suite Agents

- The SDK does **not** expose Suite internals
- The SDK does **not** depend on Suite code
- Suites expose **Dances**
- The SDK invokes Dances only indirectly, via MAP Core

DAHN and Visualizers:
- Select which Dances to invoke
- Orchestrate human experience
- Use the SDK as their **sole MAP interaction surface**

---

## Non-Goals

The TypeScript MAP SDK explicitly does **not** aim to:

- Be a general RPC client
- Provide direct access to storage
- Expose TrustChannels
- Replace the Command Protocol
- Encode Suite-specific logic

---

## Stability and Evolution

The SDK is expected to evolve, but must preserve:

- Semantic parity with MAP Core
- Clear separation between experience and domain
- Explicit transaction and undo boundaries

Breaking changes must be driven by **core architectural shifts**, not convenience.

---

### Summary

The TypeScript MAP SDK is:

- **Experience-facing**
- **Command-backed**
- **Transaction-aware**
- **Undo-conscious**
- **Suite-agnostic**

It exists to let humans interact with MAP **without leaking domain complexity**, while preserving the integrity and invariants of the MAP Core.