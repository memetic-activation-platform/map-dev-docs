# Navigation Algebra for MAP Core
*(Human-First DAHN Navigation → Cypher-Ready Foundation)*

This document defines a deliberately constrained, imperative execution algebra designed to power interactive, gesture-driven navigation of MAP property graphs before introducing declarative Cypher compilation. It establishes a minimal operand model (Value, Row, RowSet), a lightweight execution tree structure, and a transaction-scoped interpreter that cleanly separates ontology, resolved structural projection, and instance state.

The algebra is intentionally limited to navigation-oriented operations (Seed, Expand, Filter, Project, Distinct, OrderBy, Skip, Limit) while remaining forward-compatible with future declarative OpenCypher compilation and optimization. It serves as the foundational execution layer upon which the full query planner algebra will later be built.

---

This plan defines the smallest execution algebra that can subsume:

- Current MAP imperative operations
- A powerful subset of Cypher
- Future extensibility toward declarative query compilation

It incorporates:

- Transaction-scoped execution
- Flattened `ResolvedType` runtime projection
- Strict separation of structure vs state
- Semantic newtypes for descriptor references
- No query optimization (yet)

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