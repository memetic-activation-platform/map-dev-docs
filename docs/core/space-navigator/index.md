# DAHN Space Navigator

## Purpose

The Space Navigator is the first concrete DAHN Canvas Visualizer: a generic,
descriptor-driven environment for navigating, inspecting, and editing holons in
a MAP Space. This section defines its progressive specification hierarchy.

The Navigator is both a useful Canvas and an architectural proving ground. Its
documents must therefore remain DRY: each rule has one canonical home and each
lower layer elaborates, but does not redefine, the layer above it.

---

# Specification Hierarchy

    Concept
        ->
    Architecture
        ->
    Interaction Grammar
        ->
    Design Specification
        ->
    Implementation Plan
        ->
    Code

| Layer | Canonical question | Authority |
| --- | --- | --- |
| [Concept](space-navigator-concept.md) | What is the Space Navigator, and why does this model exist? | Explanatory mental model. |
| [Architecture](space-navigator-arch.md) | What structural and ownership boundaries constrain it? | DAHN/MAP contracts and responsibility boundaries. |
| [Interaction Grammar](space-navigator-interaction-grammar.md) | What spatial and compositional transformations are valid? | Normative topology, lineage, projection, compression, overflow, allocation, and re-rooting rules. |
| [Design Specification](space-navigator-design-spec.md) | Exactly how should the Space Navigator behave? | Normative concrete Canvas, visualizer, navigation, editing, and action behavior. |
| [Implementation Plan](space-navigator-impl-plan.md) | In what incremental sequence should the behavior be delivered? | Derivative PR sequencing, estimates, dependencies, and delivery criteria. |

If a lower layer reveals a missing upstream decision, resolve that decision in
the upstream document rather than silently introducing a conflicting rule.

---

# Document Responsibilities

## Concept

The Concept explains descriptor-driven exploration, the high-level distinction
between following one thing and choosing among many, preserved provenance, and
why the Navigator is one DAHN Canvas rather than DAHN itself. It does not own
detailed geometry, compression states, responsibility boundaries, or delivery
sequence.

## Architecture

The Architecture owns Rust versus TypeScript responsibility boundaries, MAP
versus experience state, visualizer and implementation semantics, Rust-side
selection, Visualizer Commons, adaptive state, layout/slot contracts, themes,
occurrence identity, transactions, and semantic interaction events. It does not
specify the Navigator's lineage or overflow behavior.

## Interaction Grammar

The Interaction Grammar owns the generative spatial model: topology versus
viewport projection; horizontal and vertical lineages; collection-mediated
traversal; stable attachment; branching; scanning; extent and compression;
overflow and hidden-lineage recovery; cross-axis sizing; common-parent spans;
local maximization; and re-rooting.

## Design Specification

The Design Specification applies the Architecture and Grammar to concrete
behavior: Canvas chrome, Node and Collection Visualizers, descriptor mapping,
loading and error states, editing, transaction actions, Create/Clone/Delete,
and interaction scenarios. It references grammar rules instead of redefining
their invariants.

## Implementation Plan

The Implementation Plan is derivative. It contains PR sequence, dependencies,
Dev Point estimates, milestones, and implementation acceptance criteria. It
does not establish new architecture or interaction semantics.

---

# Authority and Precedence

1. Concept establishes the mental model but is not normative.
2. Architecture is authoritative for cross-cutting DAHN/MAP contracts and
   ownership.
3. Interaction Grammar is authoritative for valid Space Navigator spatial and
   compositional transformations.
4. Design Specification is authoritative for concrete Space Navigator behavior.
5. Implementation Plan derives from all upstream specifications.

Examples:

- Rust-owned visualizer selection is an Architecture decision.
- Horizontal lineage, compression, and re-rooting semantics are Grammar rules.
- A rail activation that invokes horizontal traversal is Design behavior.
- The PR that first delivers that traversal is an Implementation Plan decision.

---

# Stable Center

- **Definitions determine structure; runtime data populates it.**
- **Follow one thing horizontally; choose among many things vertically.**
- Navigation topology persists while the bounded viewport projects it around
  current focus.
- Read and edit are modes of the same descriptor-driven visual structure.
- Rust owns MAP semantic and transaction state; TypeScript owns Canvas
  occurrence and immediate experience state.
- A parent owns a child's external allocation; a child composes within it.

---

# Reading Order

1. Read the Concept for the mental model.
2. Read the Architecture for contracts and ownership.
3. Read the Interaction Grammar for valid spatial transformations.
4. Read the Design Specification for concrete behavior.
5. Read the Implementation Plan when defining implementation work.

The former standalone editing specification is archived. Editing and staged
state behavior are part of the Design Specification.
