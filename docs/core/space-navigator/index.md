# DAHN Space Navigator

## Purpose

This section defines the **DAHN Space Navigator**: the first concrete Canvas Visualizer used to exercise and validate the broader DAHN architecture.

The Space Navigator provides a generic, descriptor-driven environment for navigating, inspecting, and editing holons within a MAP Space.

It is intentionally both:

- a useful Canvas in its own right; and
- an architectural proving ground for capabilities that will ultimately support other DAHN Canvases and visualizers.

The documents in this section are organized so that each has a distinct role and a clear scope of authority.

---

# Document Set

## [Space Navigator Concept](space-navigator-concept.md)

### Role

Explains the core idea and motivation behind the Space Navigator.

### Covers

- descriptor-driven presentation;
- Node Visualizers and Collection Visualizers;
- singular versus plural navigation;
- horizontal traversal for single-valued affordances;
- vertical traversal through collections;
- recursive exploration;
- preservation of navigation provenance;
- geometric compression of prior context;
- the Space Navigator as one DAHN Canvas rather than DAHN itself.

### Intended Audience

Readers who want to understand the experience model before encountering architectural or normative detail.

### Authority

The Concept document is **explanatory rather than normative**.

It should communicate the design clearly without duplicating detailed architectural contracts or implementation requirements.

---

## [Space Navigator Architecture](space-navigator-arch.md)

### Role

Defines the architectural responsibilities and reusable DAHN contracts exercised by the Space Navigator.

### Covers

- MAP Rust versus TypeScript responsibility boundaries;
- MAP state versus DAHN experience state;
- Tauri / IPC interaction;
- Visualizer Commons;
- federated visualizer discovery;
- the Rust-side DAHN Selector Function;
- adaptive personalization and collective salience;
- visualizer categories;
- visualizer selection and runtime resolution;
- generic fallback visualizers;
- recursive visual composition;
- parent-owned child layout;
- layout budgets and responsive composition;
- themes;
- visualizer occurrence identity;
- transaction ownership;
- staged state;
- Undo and Redo;
- multi-holon Commit;
- adaptive gesture reporting;
- action scope;
- Canvas-level versus holon-level responsibilities.

### Intended Audience

Developers and architects who need to understand how DAHN fits into MAP and how responsibilities are divided across layers.

### Authority

The Architecture specification is authoritative for **cross-cutting DAHN architectural responsibilities and contracts**.

Space Navigator-specific behavior should rely on these architectural contracts rather than redefine them.

---

## [Space Navigator Design Specification](space-navigator-design-spec.md)

### Role

Provides the single normative specification for Space Navigator behavior.

This document includes both inspection/navigation behavior and editing/staged-state behavior.

### Covers

- Space Navigator Canvas structure;
- pinned Canvas Action Bar;
- Node Visualizer behavior;
- Collection Visualizer behavior;
- Property and Value Visualizer participation;
- descriptor-to-presentation rules;
- Vertical Single-Value Tab Rail;
- Horizontal Collection Tab Bar;
- horizontal and vertical navigation;
- recursive exploration;
- navigation provenance;
- active traversal frontier;
- geometric compression;
- focus and interaction state;
- read and edit modes;
- scalar editing;
- editable arrays;
- editable relationships;
- semantic editing ownership;
- Create;
- Clone;
- Delete;
- multi-holon staged transactions;
- Canvas-level Undo;
- Canvas-level Redo;
- Canvas-level Commit;
- validation and failure behavior;
- adaptive and personalizable interactions;
- interaction scenarios;
- unresolved Space Navigator design questions.

### Intended Audience

Developers, HX designers, reviewers, and contributors who need to know exactly how the Space Navigator is expected to behave.

### Authority

The Design Specification is authoritative for **Space Navigator-specific behavior and interaction semantics**.

It should reference architectural contracts rather than restating their implementation or ownership.

---

## [Space Navigator Implementation Plan](space-navigator-impl-plan.md)

### Role

Decomposes the Architecture and Design Specifications into a sequence of small, mergeable implementation increments.

### Covers

- PR-sized delivery scopes;
- ordering and dependencies;
- acceptance criteria;
- milestone groupings;
- incremental architectural proof points;
- monotonic capability growth.

### Intended Audience

Developers implementing the Space Navigator and contributors creating or reviewing implementation issues and PRs.

### Authority

The Implementation Plan is **derivative**.

It does not define architecture or behavior independently. Each implementation increment should implement requirements established by the Architecture and Design Specifications.

---

# How the Documents Relate

The intended reading and dependency flow is:

    Concept
       |
       v
    Architecture
       |
       v
    Design Specification
       |
       v
    Implementation Plan

Each document answers a different question.

| Document | Primary Question |
| --- | --- |
| Concept | What is the Space Navigator, and why does it work this way? |
| Architecture | Which layer owns each capability, and what contracts make the experience possible? |
| Design Specification | Exactly how should the Space Navigator behave? |
| Implementation Plan | In what sequence should we build it? |

---

# Authority and Precedence

The documents intentionally overlap enough to remain understandable, but normative material should have one canonical home.

When resolving apparent overlap or inconsistency:

1. **Architecture Specification** is authoritative for cross-cutting DAHN architecture and responsibility boundaries.
2. **Design Specification** is authoritative for Space Navigator behavior and interaction semantics.
3. **Concept** explains the model but does not override either specification.
4. **Implementation Plan** derives from the specifications and MUST be updated when upstream architectural or design decisions change.

Examples:

- Whether the DAHN Selector runs in Rust is an **Architecture** decision.
- Whether a single-valued relationship opens to the right is a **Design** decision.
- Why singular and plural navigation use different spatial axes belongs primarily in the **Concept**.
- Which PR first implements horizontal traversal belongs in the **Implementation Plan**.

---

# DRY Documentation Principle

These documents should avoid independently defining the same rule.

The preferred pattern is:

> **Define once at the level that owns the decision; reference it everywhere else.**

In particular:

- MAP and DAHN responsibility boundaries belong in Architecture.
- Visualizer Commons and adaptive selection belong in Architecture.
- Rust-owned transaction and staged-state semantics belong in Architecture.
- Space Navigator interaction behavior belongs in Design.
- Editing behavior as experienced through the Space Navigator belongs in Design.
- Navigation geometry and compression belong in Design.
- Conceptual motivation belongs in Concept.
- PR decomposition belongs in the Implementation Plan.

---

# Key Architectural and Design Boundary

A useful shorthand for the overall specification set is:

> **Architecture defines who owns the capability and the contract between layers.**

> **Design defines how the Space Navigator uses that capability and what the person experiences.**

For example:

Architecture defines that:

- Rust owns adaptive visualizer selection;
- Rust owns staged transaction state;
- TypeScript owns Canvas geometry;
- TypeScript determines meaningful Undo gesture boundaries.

Design defines that:

- an alternate visualizer can be selected from the current experience;
- staged holons remain editable in their existing Node Visualizers;
- Undo and Redo appear in the pinned Canvas Action Bar;
- singular navigation extends rightward;
- plural navigation extends downward.

---

# Core Space Navigator Model

Across the document set, several concepts form the stable center of the Space Navigator.

## Descriptor-Driven Structure

> **Definitions determine structure; runtime data populates it.**

Descriptor-declared shape and cardinality determine the structural affordances presented by DAHN.

## Spatial Navigation

> **Follow one thing horizontally; choose among many things vertically.**

Single-valued traversal extends to the right.

Multi-valued traversal extends downward through a Collection Visualizer.

## Provenance

Navigation preserves how the current visual context was reached rather than replacing prior context with conventional page navigation.

## Compression

> **The Canvas allocates space toward the active traversal frontier and compresses provenance behind it.**

Compression hides presentation while preserving recoverable interaction and navigation state.

## Dynamic Visualizers

Node, Collection, Property, Value, Action, and Canvas Visualizers are roles rather than fixed implementations.

DAHN may select specialized visualizers dynamically while retaining generic fallbacks.

## Shared Read/Edit Structure

> **Read and edit are modes of the same descriptor-driven visual structure.**

Editing does not introduce a separate form architecture.

## Transaction Scope

A Space Navigator transaction may contain staged changes to multiple holons.

Undo, Redo, and Commit therefore operate at Canvas/transaction scope rather than belonging to individual Node Visualizers.

---

# Current Scope

The current specifications use the Space Navigator as the initial DAHN proving ground.

They do not attempt to fully specify:

- every future Canvas Visualizer;
- complete Visualizer Commons package distribution;
- arbitrary third-party runtime loading;
- all adaptive scoring algorithms;
- every possible specialized visualizer;
- every future theme capability;
- every responsive layout strategy.

Those capabilities should remain compatible with the architecture without being prematurely designed as part of the first Space Navigator implementation.

---

# Suggested Reading Order

For a first-time reader:

1. Start with the **Concept** to understand the mental model.
2. Read the **Architecture** to understand how DAHN and MAP support that model.
3. Read the **Design Specification** for the normative Space Navigator behavior.
4. Read the **Implementation Plan** when working on delivery, issues, or PRs.

For implementation work, the Architecture and Design Specification should be treated as the primary source material, with the Implementation Plan providing sequencing rather than independent requirements.