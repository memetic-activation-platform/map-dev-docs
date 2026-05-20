# MAP Runtime Shared Types (v1.0)

## ChangeLog

### v1.0

- establishes the canonical runtime shared type family reused across commands, dances, queries, and related pathways
- distinguishes runtime shared types from descriptors and runtime envelopes
- defines bound-first runtime shared types centered on `HolonReference` and `BoundHolonCollection`
- defines materialized projection and result types centered on `BaseValue`, `Row`, and `RowSet`
- narrows direct `Holon` usage to infrastructure-level full-state transfer such as cache hydration
- classifies legacy bridge and implementation-helper types in an Appendix disposition table

This document defines the canonical runtime shared types reused across higher-level MAP surfaces.

These types are shared across surfaces such as:

- commands
- dances
- queries
- SDK-facing result shapes where appropriate

They are not the same thing as:

- descriptor types
- surface-owned runtime envelopes

---

## 1. Core Posture

MAP runtime shared types have two coordinated subfamilies:

- primary bound runtime shared types
- secondary materialized projection and result types

The key rule is:

> Runtime shared types should be holon-bound first and projection-shaped second.

This means:

- intermediate execution should preserve identity-bearing holon-backed types as long as possible
- projection should be deferred until a contract, operator boundary, or serialization need requires it
- materialized scalar and row-shaped types remain important, but they are secondary relative to the bound side of the family

---

## 2. Primary Bound Runtime Shared Types

Primary bound runtime shared types are the main intermediate runtime-carried types shared across commands, dances, and queries.

They are:

- identity-bearing
- reference-layer-aligned
- projection-deferred by default

### `HolonReference`

`HolonReference` is the foundational singular bound runtime shared type.

It is the correct opaque handle for holon-bound execution because it:

- preserves transaction-relative behavior
- hides transient vs staged vs saved distinctions
- routes reads through the correct backing implementation
- avoids exposing fetch timing to call sites

Use `HolonReference` when a runtime shared type needs to refer to a singular holon-bound object without forcing property projection.

### `BoundHolonCollection`

MAP already defines `HolonCollection` as an unbound Rust runtime container (`Vec<HolonReference>`).

The runtime shared type family needs a distinct type for a named plural binding.

Current design candidate:

- `BoundHolonCollection`

`BoundHolonCollection` is the canonical plural bound runtime shared type.

High-level posture:

- it should be treated as a first-class holon
- it should itself be referenced through `HolonReference`
- it may be transient and execution-scoped
- it may still be described by a descriptor holon
- it should participate in the same phase-hiding and deferred-access behavior as other holons

Candidate structure:

- optional `variable_name` instance property
- `ItemType -> HolonType` relationship pointing to the descriptor for the member holon type
- `Members -> HolonReference`-oriented membership relationship

Use `BoundHolonCollection` when a runtime shared type needs to carry a named plural holon-bound result without collapsing it into projected rows.

### `SmartReference`

`SmartReference` remains a runtime shared type where smart-link-aware behavior is contract-significant.

Use `SmartReference` directly only when the contract surface genuinely benefits from exposing:

- smart-link identity
- smart-link-cached property access
- smart-link-specific lifecycle or navigation semantics

Otherwise, prefer the broader `HolonReference`.

---

## 3. Secondary Materialized Projection and Result Types

These remain runtime shared types, but they are secondary relative to the primary bound types.

They are used when a contract, operator, ABI, or serialization boundary requires materialized projection forms.

### `BaseValue`

`BaseValue` is the canonical scalar runtime shared type.

Use `BaseValue` for:

- scalar payloads
- parameter atoms
- single field results
- explicitly materialized scalar outputs

`BaseValue` is already the MAP runtime scalar substrate, so no additional `Value` layer is introduced here.

### `Row`

`Row` is a single materialized row-shaped projection keyed by projection labels serialized as strings.

Keys are not descriptor-backed property identifiers in this slice.

Use `Row` when a result or parameter shape needs multiple named scalar fields in one projection object.

A `Row` is a shared materialized projection type, not necessarily the engine's primary binding representation.

### `RowSet`

`RowSet` is an ordered collection of rows.

Use `RowSet` when a contract needs a collection of row-shaped projections.

`RowSet` preserves row order but does not imply uniqueness, schema, cursoring, streaming, or planner semantics.

A `RowSet` is a materialized projection and result type, not the same thing as a plural bound holon-native type such as `BoundHolonCollection`.

---

## 4. Restricted Runtime Shared Type

### `Holon`

`Holon` is not a general-purpose runtime shared type for new business-level cross-surface contracts.

It remains legitimate only for narrow infrastructure-level full-state transfer, especially:

- cache hydration
- internal full-state retrieval paths whose purpose is to populate in-memory cache on a cache miss

This means:

- `Holon` remains allowed where the goal is explicit infrastructure hydration
- `Holon` should not be used as the default request or result shape for general commands, dances, or queries

When a general cross-surface contract needs to expose data, the preferred choices are:

- `HolonReference`
- `BoundHolonCollection`
- `BaseValue`
- `Row`
- `RowSet`

---

## 5. Deferred Projection Rule

The runtime shared type family preserves deferred projection explicitly.

This means:

- intermediate execution may retain `HolonReference`-backed or `BoundHolonCollection`-backed state
- properties and relationships should be resolved through the Reference Layer and descriptor-backed structure as needed
- `BaseValue`, `Row`, and `RowSet` should be materialized only when projection, filtering, ordering, aggregation, ABI exchange, or serialization requires those forms

So:

- `Row` is a valid runtime shared type
- `RowSet` is a valid runtime shared type
- neither implies that all intermediate execution state should be eagerly row-native

---

## 6. Specialized Type Exception Rule

Higher-level surfaces should prefer the canonical runtime shared types where appropriate, but they may retain narrower specialized types where those types encode real legality or lifecycle constraints more precisely than the broader shared family.

Examples include:

- `TransientReference`
  - appropriate when an action is valid only for transient sources
- `SmartReference`
  - appropriate when an action is valid only for smart-reference-backed version lineage or smart-link semantics
- `LocalId`
  - appropriate when a local deletion or mutation action should not force the caller to first materialize a broader holon reference

This rule preserves contract precision while still minimizing the overall runtime shared type set.

---

## 7. Relationship to Runtime Envelopes

Runtime shared types are not runtime envelopes.

Runtime envelopes remain surface-owned containers such as:

- command request and response wrappers
- dance invocation and outcome wrappers
- query request and result wrappers
- trust-channel capsules
- guest-to-hub outbound dispatch wrappers

Those envelope types should remain documented in their corresponding surface directories.

---

## 8. Appendix: Type Disposition Table

This appendix is intentionally limited to runtime shared types and closely
related legacy or helper types that affect the shared runtime type posture.

Surface-owned envelopes and their legacy predecessors should be classified only
in their corresponding surface documents.

| Type                                | Classification                                    | New-world status              | Allowed use in the new world                                                                           | Notes                                                                                   |
|-------------------------------------|---------------------------------------------------|-------------------------------|--------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| `HolonReference`                    | Canonical runtime shared type                     | Keep                          | General-purpose singular bound type across surfaces                                                    | Primary singular bound type                                                             |
| `BoundHolonCollection`              | Canonical runtime shared type                     | Keep                          | General-purpose plural bound type across surfaces                                                      | Primary plural bound type                                                               |
| `SmartReference`                    | Canonical runtime shared type                     | Keep, but keep scope explicit | Use directly where smart-link-aware bound behavior is contract-significant                             | Keep as first-class only where surfaces genuinely benefit from exposing it              |
| `BaseValue`                         | Canonical runtime shared type                     | Keep                          | General-purpose scalar or projection atom                                                              | Canonical scalar runtime shared type                                                    |
| `Row`                               | Canonical runtime shared type                     | Keep                          | General-purpose materialized named projection result                                                   | Secondary projection and result type                                                    |
| `RowSet`                            | Canonical runtime shared type                     | Keep                          | General-purpose materialized collection of rows                                                        | Secondary projection and result type                                                    |
| `Record`                            | Deferred canonical runtime shared type            | Defer                         | None yet                                                                                               | Future richer result family                                                             |
| `RecordStream`                      | Deferred canonical runtime shared type            | Defer                         | None yet                                                                                               | Future streaming result family                                                          |
| `Holon`                             | Restricted canonical runtime shared type          | Keep, but narrowly            | Internal full-state transfer, especially cache hydration and tightly scoped infrastructure retrieval   | Not a general-purpose cross-surface business type                                       |
| `HolonCollection`                   | Deprecated legacy bridge or implementation helper | Deprecate                     | Existing runtime compatibility only, unless retained internally as a low-level helper during migration | Canonical plural type should be `BoundHolonCollection`                                  |
| `Vec<HolonReference>`               | Implementation helper                             | Keep internally only          | Low-level internal collection handling                                                                 | Not a canonical cross-surface runtime shared type                                       |
