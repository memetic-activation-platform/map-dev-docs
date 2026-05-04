# MAP Query Support Portfolio — Descriptor-Synthesized Foundations
*(Descriptor Semantics → Query Algebra → Declarative Query Evolution)*

This document explains how the MAP query support documentation set should now be read in light of the descriptor design.

The primary shift is:

> Query execution remains algebra-first, but query semantics should increasingly be descriptor-owned.

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

This section of the docs is concerned with specifying MAP query support: shared operand vocabulary, structural resolution posture, navigation algebra, planner evolution, and distributed query boundaries.

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

---

## 1. `shared-operand-family-foundation.md`
## Shared Contract-Shape Vocabulary

### Role in Query Architecture

This document defines the narrow, shared operand-shape vocabulary used by query-adjacent contracts:

- `Value`
- `Row`
- `RowSet`

Its role is intentionally limited:

- stabilize serialized/result shape language
- distinguish scalar vs row vs rowset payloads
- preserve a common contract vocabulary across query, dance, and adjacent APIs

### Updated Interpretation

This document should be read as a contract-shape foundation, not as the semantic or execution model of MAP queries.

In particular:

- it does not make descriptors the semantic source of query meaning
- it does not define planner or distributed behavior
- it does not require eager projection as the internal execution model
- execution may retain richer bindings, including `HolonReference`-backed bindings, and materialize `Row`/`RowSet` only when a contract or operator requires those shapes

This gives the rest of the portfolio a stable operand vocabulary without forcing query execution to collapse early into string-keyed projections.

---

## 2. `exec-time-type-resolution-v1.1.md`
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

## 3. `navigation-algebra-v1.1.md`
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

---

## 4. `query-planner-algebra-v1.1.md`
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

## 5. `cypher-operator-inventory-v1.1.md`
## Execution Reality Check

### Role in Portfolio

This document remains descriptive rather than prescriptive.

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

## 6. `query-arch-v1.1.md`
## Architecture Synthesis

This is now the main place where the portfolio states:

- algebra is the execution IR
- descriptors are the semantic source
- declarative languages compile into descriptor-aware algebra

It is the key synthesis doc for the portfolio.

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

## Refactor Priority Stack

Near-term focus should now be read as:

```text
shared operand family foundation
        ↓
descriptor runtime + schema-backed accessors
        ↓
descriptor-aware structural resolution
        ↓
navigation algebra
        ↓
query execution / dance refactor
```

Future evolution remains:

```text
navigation algebra
        ↓
query planner algebra
        ↓
OpenCypher parser
        ↓
logical rewrite engine
        ↓
physical strategy selection
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
