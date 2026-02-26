# MAP Dance Interface Refactor — Architectural Foundations
*(Deterministic Structure → Navigation Algebra → Future OpenCypher)*

This document explains how the current documentation portfolio supports the refactoring of the MAP Dance Interface.

The query implementation refactor is a subset of this broader effort.

The primary objective is to introduce:

- Deterministic execution-time structural contracts
- Proper execution operands
- A stable navigation algebra
- Clean separation between ontology and execution
- A forward-compatible path toward declarative OpenCypher

The early focus is intentionally narrow:

1. Execution-Time Type Resolution
2. Navigation Algebra

The remaining documents define the evolutionary path beyond Phase 1 and ensure we are not constraining future planner and optimizer work.

---

# Refactor Context

The Dance Interface is MAP’s execution surface.

Today it mixes:

- Ontology lookups
- Structural validation
- Imperative navigation logic
- Mutation logic
- Query-like behaviors

The refactor separates concerns and introduces proper execution primitives.

The query implementation is one use case of the Dance Interface — not its definition.

---

# 1. execution-type-resolution.md
## Deterministic Structural Contracts

### Role in Dance Refactor

Defines how a committed `TypeDescriptor` becomes an immutable `ResolvedType`.

This provides:

- Flattened inheritance
- Conflict-free property contracts
- Conflict-free relationship contracts
- O(1) structural validation
- Elimination of runtime descriptor traversal

### Implementation Implications

During Dance refactor:

- Introduce `ResolvedType`
- Introduce `TypeRegistry`
- Remove ad-hoc descriptor walking
- Remove duplicated structural logic
- Eliminate Rust enums that mirror ontology

This stabilizes structural semantics for *all* dances — not just queries.

Every execution path benefits from this layer.

---

# 2. navigation-algebra.md
## Human-First Execution Layer

### Role in Dance Refactor

Defines a minimal execution algebra that becomes the structured substrate for navigation-oriented dances.

Introduces:

- `Value`
- `Row`
- `RowSet`
- `ExecutionPlan`
- `PlanNode`
- `PlanStep`

This replaces ad-hoc imperative traversal with a structured interpreter.

### Implementation Implications

During Dance refactor:

- Dances emit `ExecutionPlan` instead of direct imperative logic.
- Introduce proper operand types.
- Make navigation append-only and replayable.
- Validate `Expand` against `ResolvedType`.
- Keep plan container tree-shaped from the start.

This delivers immediate value:

- Interactive exploration
- Search
- Filter
- Projection
- Replayable navigation

No optimizer required.
No cost model required.
No join logic required.

This is Phase 1 of Dance Interface stabilization.

---

# 3. query-planner-algebra.md
## Logical Planner Layer (Future Evolution)

### Role in Portfolio

Defines the full logical algebra required for:

- Declarative OpenCypher compilation
- Logical plan construction
- Rewrite passes
- Cost-based optimization
- Correlated execution

### Why It Exists Now

It demonstrates that:

- Navigation Algebra is a strict subset.
- ExecutionPlan tree structure is future-proof.
- Operand model aligns with RecordStream abstraction.
- We are not constraining planner evolution.

This document ensures architectural continuity.

It is not Phase 1 work.

It is the evolution target.

---

# 4. cypher-operator-inventory.md
## Execution Reality Check

### Role in Portfolio

Catalogs operators observed in production Cypher engines.

This prevents theoretical drift and ensures:

- Vocabulary alignment
- Compatibility awareness
- Strategy specialization awareness
- Future explain-plan capability

It is descriptive, not prescriptive.

It grounds planner algebra in real execution systems.

---

# Refactor Priority Stack

Current implementation focus:

```
execution-type-resolution.md
        ↓
navigation-algebra.md
        ↓
Dance Interface refactor
```

Query support emerges naturally from this work.

Future evolution path:

```
navigation-algebra
        ↓
query-planner-algebra
        ↓
OpenCypher parser
        ↓
Logical rewrite engine
        ↓
Physical strategy selection
```

---

# Operand Introduction Strategy (Dance Refactor)

During refactor:

1. Introduce semantic reference types.
2. Introduce `ResolvedType`.
3. Introduce execution operands:
   - `Value`
   - `Row`
   - `RowSet`
4. Introduce `ExecutionPlan` with tree container.
5. Refactor navigation dances to emit PlanSteps.

This creates a stable execution substrate.

All higher-level query capabilities build on it.

---

# Why This Is Safe

We are not painting ourselves into a corner because:

- Navigation Algebra ⊂ Planner Algebra.
- Planner Algebra ⊂ Real Execution Operator Space.
- ExecutionPlan is tree-based from the start.
- Operand model matches future RecordStream abstraction.
- Structural validation is deterministic and cached.
- No ontology duplication exists in Rust.

The path is monotonic:

```
Imperative Dance Calls
    ↓
Structured Navigation Algebra
    ↓
Logical Planner Algebra
    ↓
Declarative Cypher Compilation
    ↓
Cost-Based Optimization
```

Each step builds on stable primitives introduced earlier.

No layer invalidates a prior one.

---

# Strategic Outcome

By prioritizing:

- Deterministic type resolution
- Minimal navigation algebra
- Proper operand introduction

We stabilize the Dance Interface first.

Query implementation improves as a consequence.

Full OpenCypher support becomes an evolutionary extension — not a redesign.

This approach delivers:

- Immediate execution clarity
- Cleaner Dance Interface semantics
- Replayable navigation
- Structural determinism
- Long-term planner compatibility

Incrementally.
Deliberately.
Without over-engineering.