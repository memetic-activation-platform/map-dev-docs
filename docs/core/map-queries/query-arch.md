# MAP Query Architecture — Algebra-First, Descriptor-Synthesized (v1.1)

## Core Principle

Decouple declarative graph query languages from graph execution by introducing a MAP-native Graph Algebra as the stable internal IR, while making descriptor semantics the authoritative source of query meaning.

The key synthesis is:

> Graph Algebra is the execution substrate.  
> Descriptors are the semantic source of query structure and value/operator meaning.

This means MAP query architecture should no longer treat type resolution, predicate semantics, and operator support as freestanding query concerns. Those semantics should increasingly come from descriptor wrappers, especially:

- `HolonDescriptor` for effective structural lookup
- `RelationshipDescriptor` for relationship semantics
- `PropertyDescriptor` for property-to-value bridging
- `ValueDescriptor` for validation and operator semantics

---

## 1. Holons Core: Graph Algebra Execution Layer

- MAP Holons Core implements graph algebra operations as the execution IR.
- Operations are composable, imperative, and deterministic.
- This algebra is exposed through APIs and the TypeScript SDK for:
  - programmatic graph navigation
  - internal system use
  - tooling and UX layers

Illustrative ops:

- `matchNode`
- `matchEdge`
- `traverse`
- `filter`
- `project`
- `join`
- `group`
- `aggregate`
- `sort`
- `limit`

This layer is:

- language-agnostic
- optimizable
- the execution substrate of MAP query behavior

But it is not the semantic owner of query meaning. Algebra executes plans; descriptors define what properties, relationships, commands, dances, and value operators mean.

---

## 2. Descriptor-Semantic Query Model

The descriptor design changes the architecture of query semantics in three important ways.

### 2.1 Structural Resolution is Descriptor-Driven

Query planning and execution should resolve structural meaning through descriptor wrappers rather than through ad hoc type/relationship rule logic.

Examples:

- property lookup by name should come from effective descriptor lookup
- relationship lookup should preserve declared vs inverse semantics
- inheritance flattening should come from descriptor `Extends` handling in core
- callers should not reconstruct effective structure manually

### 2.2 Value Semantics are Descriptor-Owned

Predicate semantics should come from `ValueDescriptor` rather than from a freestanding query-operator subsystem.

That includes:

- support for `=`, `<`, `>`, `contains`, range-like predicates, and similar comparators
- operator discovery for query-building UIs
- compatibility checks between a value type and an operator
- actual operator application during filter evaluation

### 2.3 Query Semantics and Validation Semantics Converge

The same descriptor-owned value semantics should increasingly support both:

- validation-oriented checks
- query/filter predicates

They are not identical in purpose, but they should not live in separate semantic systems if they are evaluating the same value-type meaning.

---

## 3. Declarative Query Engine

- OpenCypher remains the initial declarative language.
- It remains a stepping stone toward ISO GQL.
- The query engine:
  - parses declarative syntax
  - transforms it into MAP Graph Algebra
  - does not execute directly

This continues to preserve:

- standards alignment
- long-term GQL compatibility
- freedom to evolve execution and optimization independently

The new constraint is:

> Declarative compilation must target algebra plus descriptor-backed semantics, not algebra plus a parallel handwritten query-semantic layer.

---

## 4. Descriptor-Aware Query Compilation

Compilation from OpenCypher/GQL-like syntax into algebra should explicitly account for descriptor context.

Important compilation steps:

1. resolve the relevant holon/type descriptor context
2. resolve effective properties and relationships through descriptor flattening
3. resolve value semantics through `PropertyDescriptor -> ValueDescriptor`
4. resolve supported operators through `ValueDescriptor`
5. emit algebra whose filters reference descriptor-backed semantics

This keeps parsing separate from execution while also preventing semantic drift between:

- query code
- validation code
- SDK helper code
- future DAHN/query-builder surfaces

---

## 5. Optimization Surface

Graph Algebra remains the optimization IR.

Optimization may still include:

- predicate pushdown
- operation reordering
- cost-based planning
- lazy evaluation
- distributed execution

But optimization must respect descriptor semantics.

For example:

- pushed-down predicates must remain valid for the relevant `ValueDescriptor`
- relationship-navigation rewrites must preserve declared vs inverse relationship meaning
- value comparisons must preserve descriptor-defined operator compatibility

---

## 6. Algebra Command Log

Executed algebra operations may still be recorded as a command log representing:

- user-guided navigation
- programmatic exploration
- system-driven query execution

Properties:

- serializable
- replayable
- deterministic, within the relevant execution context

The synthesis added here is:

- replay should preserve descriptor references or sufficient descriptor identity to keep semantics stable
- logs should not rely on TS-side or UI-side reconstruction of query semantics

---

## 7. Algebra to Declarative Translation

Algebra command logs may still be translated back into OpenCypher and later GQL for:

- replay
- sharing
- explainability
- AI-assisted authoring

But round-tripping must account for descriptor-backed semantics.

In particular:

- value predicates should serialize using operators actually supported by the underlying value descriptors
- structural paths should reflect effective descriptor structure, not accidental runtime shortcuts

---

## 8. Design Consequences

This descriptor synthesis changes the query architecture in several concrete ways:

- query execution should stop owning value-operator semantics independently
- type resolution should evolve toward descriptor-local lookup rather than a standalone semantic layer
- query-builder surfaces can discover valid operators from descriptors rather than hardcoded client inventories
- relationship-navigation semantics should flow from relationship descriptors
- distributed query planning still remains a separate concern, but descriptor meaning travels with the query

---

## 9. Strategic Outcomes

- clean separation of concerns:
  - language != execution
  - execution != semantic ownership
- future-proofing:
  - OpenCypher today
  - GQL tomorrow
  - descriptor-driven semantics throughout
- rich UX possibilities:
  - explainable navigation
  - descriptor-aware query builders
  - AI-assisted query authoring constrained by real descriptor/operator affordances

---

## Summary

MAP should treat Graph Algebra as the execution truth and descriptors as the semantic truth.

Declarative query languages are:

- compilers into algebra
- not execution engines
- not the semantic home of property, relationship, or operator meaning

This architecture enables:

- standards compliance
- optimization
- replayability
- convergence between query and validation semantics
- long-term evolvability of the platform
