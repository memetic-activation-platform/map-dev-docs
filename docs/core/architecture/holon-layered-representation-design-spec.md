# Holon Layered Representation Design Spec (v0.1)

## Purpose

This spec defines a cross-cutting MAP architectural pattern:

> Everything in MAP is represented as a self-describing, active holon or holon relationship.

From an implementation perspective, this means MAP should be understood as a
layered holon representation architecture rather than as a single storage model,
single runtime struct family, or single API surface.

This document is the canonical home for the layered representation pattern that
connects:

- integrity-layer persistence representations
- in-memory shared runtime objects
- reference-layer access contracts
- typed Rust wrapper structs for MAP Core holon kinds

It is intentionally cross-cutting. It does not replace the more detailed specs
that govern each layer.

## Architectural Posture

MAP does not treat holons as passive records.

A holon in MAP is:

- self-describing through descriptor relationships and schema meaning
- active in the sense that it participates in commands, dances, queries,
  transactions, validation, and runtime affordances
- representable through multiple coordinated layers without losing identity or
  semantic continuity

The same underlying holonic entity may therefore appear through different
implementation shapes depending on whether the concern is:

- persistence and integrity
- runtime mutation and staging
- read/write access and resolution
- strongly typed ergonomic APIs for core holon kinds

## Layer Model

### 1. Integrity Layer

The Integrity Layer is the persistence-oriented representation of holons and
their relationships.

Canonical examples:

- `HolonNode`
- `SmartLink`

This layer owns:

- persisted node and link representation
- integrity-facing storage identity
- durable graph persistence shape
- the storage-facing substrate consumed by higher layers

This layer does not own:

- transaction-scoped in-memory mutation posture
- uniform reference ergonomics
- type-specific developer wrapper APIs

### 2. Shared Objects Layer

The Shared Objects Layer is the in-memory, shared-state representation reused
across MAP runtime surfaces.

Canonical examples:

- `Holon` enum with `Saved`, `Staged`, and `Transient` variants
- `HolonRelationship`
- `RelationshipMap`

This layer owns:

- in-memory holon lifecycle posture
- staged vs saved vs transient runtime distinctions
- relationship mutation intent
- shared object contracts used across command, dance, query, loader, and host
  pathways

This layer does not own:

- persistence storage encoding
- reference-layer traits as the primary developer-facing access contract
- type-specific wrapper ergonomics for core holon kinds

### 3. Reference Layer

The Reference Layer provides the uniform access contract for holon-bound reads
and writes.

Canonical examples:

- `HolonReference` enum
- `SmartReference`
- `StagedReference`
- `TransientReference`
- `ReadableHolon`
- `WritableHolon`

This layer owns:

- singular holon access handles
- phase-aware read/write behavior
- the abstraction that hides backing representation differences from callers
- the narrow contract consumed by APIs, commands, dances, queries, and SDKs

This layer does not own:

- persistence encoding details
- the full in-memory object model
- type-specific core wrapper semantics beyond their reference dependency

### 4. Core Struct Layer

The Core Struct Layer provides strongly typed Rust wrappers for MAP Core holon
types.

Canonical shape:

- type-specific Rust structs that wrap `HolonReference` values for core MAP
  holon kinds

This layer owns:

- ergonomic typed APIs for core holon kinds
- core-type-specific helper methods and affordances
- stronger semantic legibility than raw generic reference access alone

This layer does not own:

- the canonical reference contract
- lifecycle-state machinery
- persistence representation

## Dependency Direction

The intended dependency direction is:

```text
Core Struct Layer
    depends on Reference Layer
Reference Layer
    depends on Shared Objects Layer and/or integrity-backed resolution services
Shared Objects Layer
    depends on integrity-backed persistence and descriptor semantics where needed
Integrity Layer
    persists the durable representation
```

Higher layers may expose narrower, more ergonomic views, but they should not
erase the core holonic invariants established below them.

## Cross-Layer Invariants

The following invariants should hold across all four layers:

1. The represented thing is still a holon.
2. Holon identity must remain semantically continuous across layers.
3. Descriptor-backed self-description remains authoritative even when hidden
   behind typed wrappers.
4. Runtime activity is expressed through holon-bound commands, dances, queries,
   validation, and transaction semantics rather than by treating holons as
   passive DTOs.
5. Layer transitions may change representation shape, but they must not invent a
   second conceptual object that competes with the holon as the primary runtime
   subject.

## Why This Layering Matters

This layering keeps several MAP goals aligned at once:

- persistence can remain durable and integrity-oriented
- runtime objects can remain mutation-aware and transaction-aware
- public APIs can stay uniform across transient, staged, and saved phases
- core MAP types can still feel strongly typed and semantically explicit to
  developers

Without this pattern, MAP documentation tends to collapse into one of two
mistakes:

- treating storage representations as if they were the whole runtime model
- treating typed wrapper structs or API handles as if they were the underlying
  semantic object

The layered representation architecture avoids both mistakes.

## Relationship To Other Specs

This spec is the architectural parent for several narrower documents:

- `type-system/map-type-system.md` defines how holons are self-describing in the
  descriptor/type-system sense
- `type-system/runtime-shared-types.md` defines cross-surface runtime-carried
  shared types such as `HolonReference` and `HolonCollection`
- `holons-shared-objects-layer-design-spec.md` defines the in-memory shared
  object model and lifecycle semantics
- `rust-api.md` explains the developer-facing reference-layer and typed API
  experience

This spec does not supersede those documents. It provides the cross-cutting
frame that tells readers how they fit together.
