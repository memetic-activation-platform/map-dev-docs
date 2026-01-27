# MAP Query Architecture — Algebra-First Approach (DRAFT)

## Core Principle
Decouple **declarative graph query languages** from **graph execution** by introducing a MAP-native **Graph Algebra** as the stable internal intermediate representation (IR).

---

## 1. Holons Core: Graph Algebra Execution Layer

- MAP Holons Core implements a set of **graph algebra operations** (IR).
- Operations are **composable, imperative, and deterministic**.
- Exposed via **API / TypeScript SDK** for:

    - Programmatic graph navigation
    - Internal system use
    - Tooling and UX layers

**Examples of algebraic ops (illustrative):**

- `matchNode`, `matchEdge`
- `traverse`
- `filter`
- `project`
- `join`
- `group`, `aggregate`
- `sort`, `limit`

This layer is:

- Language-agnostic
- Optimizable
- The true execution substrate of MAP

---

## 2. Declarative Query Engine (Front-End)
- **OpenCypher** is the initial declarative query language.
- Chosen as a **stepping stone toward ISO GQL**.
- The Query Engine:

    - Parses OpenCypher
    - Transforms it into **MAP Graph Algebra**
    - Does *not* execute queries directly

This preserves:

- Standards alignment
- Long-term GQL compatibility
- Freedom to evolve execution semantics independently

---

## 3. Design Space for Query Optimization
- Graph Algebra acts as an **IR suitable for optimization**:

    - Reordering operations
    - Predicate pushdown
    - Cost-based planning
    - Lazy or distributed execution (future)

Optimization occurs **between parsing and execution**, not in the language layer.

---

## 4. Algebra Command Log
- Executed algebra operations are recorded as a **command log**.
- The log represents:

    - User-guided graph navigation
    - Programmatic exploration paths
    - System-driven query execution

Properties:

- Serializable
- Replayable
- Deterministic

---

## 5. Algebra → Declarative Translation (Replay & Sharing)
- Algebra command logs can be **translated back into OpenCypher**:

    - Save user navigation as declarative queries
    - Enable later replay
    - Support sharing and reproducibility
- Over time, the same logs can target **ISO GQL**.

This creates a reversible loop:

- Declarative → Algebra → Execution
- Imperative navigation → Algebra → Declarative

---

## 6. Strategic Outcomes
- Clean separation of concerns:

    - Language ≠ Execution
- Future-proofing:

    - OpenCypher today
    - ISO GQL tomorrow
- Rich UX possibilities:

    - Explainable navigation
    - AI-assisted query generation
    - Shareable graph workflows

---

## Summary
MAP treats **Graph Algebra as the truth**.

Declarative query languages are:

- Compilers *into* algebra
- Not execution engines themselves

This architecture enables:

- Standards compliance
- Optimization
- Replayability
- Long-term evolvability of the platform