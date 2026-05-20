# MAP Query Support Portfolio — Descriptor-Synthesized Foundations
*(Descriptor Semantics → Query Algebra → Declarative Query Evolution)*

This document explains how the MAP query support documentation set should now be read in light of the descriptor design.

The primary shift is:

> Query execution remains algebra-first, but query semantics should increasingly be descriptor-owned.

`BaseValue`, `Row`, and `RowSet` remain the shared materialized contract vocabulary used across query, dance, command, SDK, and DAHN surfaces.
They should not be read as forcing MAP's internal execution model to be eagerly row-native.

That means this portfolio is no longer just about deterministic structure and navigation algebra. It is also about aligning query semantics with:

- `HolonDescriptor` structural lookup
- `PropertyDescriptor` to `ValueDescriptor` semantic bridging
- `RelationshipDescriptor` navigation semantics
- `ValueDescriptor` operator semantics

The goal is to avoid a split where:

- descriptors own validation semantics
- queries own a different, parallel semantic system

---

## Portfolio Context

This section of the docs is concerned with specifying MAP query support: the runtime shared type posture, deferred-projection binding posture, structural resolution posture, navigation algebra, planner evolution, and distributed query boundaries.

The descriptor work sharpens that target architecture.

Today, MAP query-related code and designs risk mixing:

- descriptor lookup
- structural projection
- imperative navigation logic
- query predicate semantics
- mutation/query boundary behavior

The descriptor synthesis suggests a cleaner split:

- descriptors own structural and value semantics
- algebra owns execution
- planners own rewrite/optimization
- declarative languages compile into descriptor-aware algebra
- Commands act as a TypeScript ingress adapter onto the shared query substrate rather than as the semantic home of query behavior

For `Query PRO2`, the contract path that should now be read across this portfolio is:

- TS SDK-facing query API
- Commands-ingress query shape
- wire/binding seam
- substrate-facing query request envelope
- substrate-facing query result envelope

This slice is about stabilizing that path early without overcommitting to the final internal execution representation.

---

## 1. Runtime Shared Types

### Role in Query Architecture

The canonical home for cross-surface runtime shared types now lives in `docs/core/type-system/runtime-shared-types.md`.

Its role is to make explicit that:

- the runtime shared type family remains a first-order architectural objective
- bound holon-native types are primary
- materialized projection types remain shared, but are secondary

### Updated Interpretation

This runtime shared type foundation should be read as the primary shared-type foundation for MAP query work.

In particular:

- it positions `HolonReference` and `BoundHolonCollection` as primary runtime shared types
- it keeps `BaseValue`, `Row`, and `RowSet` as shared types while assigning them a secondary projection/result role
- it keeps MAP aligned with eventual OpenCypher and GQL support by distinguishing logical declarative semantics from the physical/intermediate execution substrate

This is the architectural correction that was missing when scalar and row-shaped materializations were read too centrally.

---

## 2. `query-arch.md`
## Architecture Synthesis

### Role in Query Architecture

This is now the main normative architecture doc for the section.

Its role is to define:

- the descriptor-versus-algebra split
- the query contract path from SDK ingress down to the shared substrate boundary
- deferred-projection posture at architecture level
- the responsibility boundaries between SDK, Commands ingress, wire/binding, and the shared substrate

### Updated Interpretation

This should be read as the architectural frame for all other query docs.

In particular:

- it explains why query semantics should increasingly be descriptor-owned
- it incorporates the query contract-path posture directly rather than splitting it into a separate standalone file
- it preserves bound-first execution posture without reintroducing a second shared-type foundation

---

## 3. `exec-time-type-resolution.md`
## Descriptor-Backed Structural Resolution

### Role in Query Architecture

This document should now be read as a bridge document, not the final semantic home of structure.

Its role is to define:

- deterministic runtime structural projection
- caching/runtime lookup support
- effective inherited property and relationship availability

But descriptor wrappers are now the preferred semantic facade for this structure.

### Updated Interpretation

During query refactor:

- runtime caches may still materialize effective structural views
- but query callers should increasingly use descriptor wrappers rather than a standalone `ResolvedType` semantic layer
- flattened inheritance must remain core-provided, not caller-reconstructed

This document stabilizes query structure, but the long-term semantic owner is the descriptor layer.

---

## 4. `navigation-algebra.md`
## Human-First Execution Layer

### Role in Query Architecture

This remains the minimal execution substrate for:

- interactive navigation
- DAHN-guided exploration
- filtered traversal
- replayable user-driven graph movement

### Updated Interpretation

The algebra still matters, but it should no longer define value/operator semantics independently.

Instead:

- `Expand` should navigate through descriptor-backed relationship semantics
- `Filter` should evaluate descriptor-backed operator semantics where value types are involved
- structural checks should rely on descriptor-provided effective lookups

The algebra is execution. Descriptors are meaning.

`Query PRO2` should therefore stop short of defining this algebra's final runtime semantics and instead focus on the contract path that leads into the shared substrate.

---

## 5. `query-planner-algebra.md`
## Full Logical Planner Layer

### Role in Portfolio

This remains the future-facing logical algebra for:

- declarative OpenCypher compilation
- planner construction
- rewrite passes
- cost-based optimization
- distributed query planning

### Updated Interpretation

The planner algebra should now be treated as descriptor-aware from the beginning:

- predicates should be typed by descriptor-backed value semantics
- navigation should preserve relationship descriptor meaning
- explain plans can eventually surface descriptor/operator provenance

This prevents the planner layer from becoming a second semantic authority.

---

## 6. `cypher-operator-inventory.md`
## Reference-Only Execution Reality Check

### Role in Portfolio

This document remains descriptive rather than prescriptive and is not part of the normative MAP query core.

It still helps with:

- vocabulary alignment
- engine-reality awareness
- future explain-plan capability

### Updated Interpretation

The operator inventory is not MAP’s semantic source of truth.

It is:

- a reference catalog of physical/logical operator families
- a reality check for planning and execution work

MAP-specific operator meaning, especially for value predicates, should come from descriptors.

---

## 7. `distributed-query-semantics.md`
## Federated Query Boundaries

This remains the authority on:

- sovereignty
- execution domain
- home-space expansion
- trust-channel mediation
- canonical identity and rebinding

The descriptor synthesis does not replace these rules.

It adds one important constraint:

- distributed query execution must preserve descriptor meaning across spaces where that meaning is required for filtering, navigation, and interpretation

---

## Current Core

The current normative MAP query core is:

- `query-arch.md`
- `exec-time-type-resolution.md`
- `navigation-algebra.md`
- `query-planner-algebra.md`
- `distributed-query-semantics.md`

Reference-only companion:

- `cypher-operator-inventory.md`
```

But all of that should now assume descriptor-owned semantics.

---

## Why This Matters

This synthesis prevents a likely architectural split where:

- validation becomes descriptor-driven
- DAHN becomes descriptor-driven
- but query semantics remain ad hoc

That split would create duplicated logic around:

- operator support
- property/value typing
- relationship meaning
- inheritance flattening

This portfolio should instead converge those concerns under the descriptor layer while preserving algebra-first execution.

---

## Summary

The MAP query portfolio now supports a stronger architectural posture:

- descriptors own semantics
- query algebra executes plans
- planners optimize plans
- declarative languages compile into descriptor-aware algebra
- distributed semantics still govern where and how queries run

That is the path toward a query system that is both structurally coherent and aligned with the broader descriptor-driven MAP design.
