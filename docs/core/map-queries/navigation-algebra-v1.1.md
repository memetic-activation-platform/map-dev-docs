# Navigation Algebra for MAP Core v1.1
*(Human-First DAHN Navigation → Cypher-Ready Foundation)*

This document defines a deliberately constrained, imperative execution algebra designed to power interactive, gesture-driven navigation of MAP property graphs before introducing declarative Cypher compilation. It establishes a minimal operand model (Value, Row, RowSet), a lightweight execution tree structure, and a transaction-scoped interpreter that cleanly separates ontology, resolved structural projection, and instance state.

The algebra is intentionally limited to navigation-oriented operations (Seed, Expand, Filter, Project, Distinct, OrderBy, Skip, Limit) while remaining forward-compatible with future declarative OpenCypher compilation and optimization. It serves as the foundational execution layer upon which the full query planner algebra will later be built.

---

This plan defines the smallest execution algebra that can subsume:

- Current MAP imperative operations
- A powerful subset of Cypher
- Future extensibility toward declarative query compilation

Execution interpretation rules in v1.1:

- `Expand` should be validated against effective descriptor-backed relationship semantics
- `Filter` should rely on descriptor-backed value/operator semantics where predicates touch typed values
- `Project` may reshape bindings freely, but it should not invent structural meaning that descriptors do not support

It incorporates:

- Transaction-scoped execution
- Flattened `ResolvedType` runtime projection
- Strict separation of structure vs state
- Semantic newtypes for descriptor references
- No query optimization (yet)

This version incorporates descriptor synthesis:

- descriptor wrappers are the semantic owner of effective structure
- `ValueDescriptor` is the semantic owner of value/operator behavior
- navigation algebra remains the execution substrate, not the semantic source

---

# Step 1 — Stabilize the Three-Layer Architecture

Before introducing algebra, explicitly formalize three runtime layers:

## 1. Ontology Layer (Persistent, Holonic)

- `TypeDescriptor`
- `Extends`
- `InstanceProperties`
- `InstanceRelationships`
- All schema semantics remain declarative

---

## 2. Runtime Structural Layer (Ephemeral Projection)

Introduce immutable:

Descriptor synthesis note:

- this runtime structural layer may still use a projected/resolved form for execution efficiency
- but callers should increasingly experience structure through descriptor wrappers and effective descriptor lookups
- this layer should not become a long-lived second semantic system beside descriptors
