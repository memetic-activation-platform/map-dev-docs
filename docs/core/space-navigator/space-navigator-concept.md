# DAHN Space Navigator — Concept

## What It Is

The **Space Navigator** is a DAHN Canvas for exploring, inspecting, and
eventually editing a MAP Space through its holons and their effective
affordances.

It is not a succession of domain-specific screens. It is a generic,
descriptor-driven experience that can present previously unknown holon types
through selected Node, Collection, Property, Value, and Action Visualizers.

The Navigator is one Canvas in the broader DAHN architecture, not DAHN itself.

---

# Why This Model Exists

Ordinary page navigation tends to replace context as a person follows a path.
The Space Navigator instead treats exploration as spatial accumulation:

- a person can see what they are inspecting;
- the route by which they reached it remains available;
- collections retain the sibling context from which a member was selected; and
- prior context can become compact without becoming semantically lost.

This makes MAP's graph-like, descriptor-defined structure legible without
requiring a custom application screen for every holon type.

---

# Descriptor-Driven Experience

The essential principle is:

> **Definitions determine structure; runtime data populates it.**

Descriptors determine which structural affordances exist and what shape they
have. For example, a relationship declared singular remains a singular
affordance even when it is empty, while a relationship declared plural remains
a collection affordance even when it currently contains one target.

The same posture applies to Dance result shapes. The Navigator can determine
the applicable class of presentation from a Dance's declared response contract
before invoking it.

This enables generic presentation rather than a growing family of
type-specific screens.

---

# Two Complementary Ways to Explore

The Navigator gives distinct spatial meaning to two kinds of exploration:

- **Follow one thing.** A direct, singular continuation extends horizontally.
- **Choose among many things.** A plural affordance first exposes a collection,
  from which a selected member extends vertically.

The distinction is semantic, not merely visual. Direct continuation preserves a
lineage of one-to-one choices; a collection preserves the set and sibling
context through which a member was reached.

The detailed rules for topology, projection, compression, overflow, and
recovery are normative in the
[Interaction Grammar](space-navigator-interaction-grammar.md).

---

# Reusable Visual Roles

The initial experience is built from reusable roles:

- a **Node Visualizer** for one holon and its affordances;
- a **Collection Visualizer** for a homogeneous plural result;
- **Property** and **Value Visualizers** for scalar presentation; and
- **Action Visualizers** for available actions.

A table is an initial Collection Visualizer, not the permanent definition of a
collection. Likewise, generic fallback visualizers preserve usability when no
specialized visualizer applies.

---

# Context, Provenance, and Scale

Each inspected holon appears as a visualizer occurrence with its own provenance.
The same semantic holon may appear in more than one occurrence when reached by
different paths.

As exploration grows, the Canvas need not keep every occurrence fully expanded.
It preserves recoverable context while allocating useful attention to the
current area of work. This is why the experience remains a navigable space
rather than an ever-growing page or a history that must be discarded.

---

# Read and Edit Are One Experience

The Navigator is intended to inspect and manipulate MAP state through the same
descriptor-driven visual structure. Editing is a mode of an existing
occurrence, not a second form-oriented application. MAP retains ownership of
semantic and staged state while the Canvas retains experience and occurrence
state.

The Architecture and Design Specification define those responsibilities and
concrete behavior respectively.

---

# Relationship to the Rest of the Specification

This document explains the mental model. It does not define architectural
ownership, spatial transformation invariants, concrete UI behavior, or delivery
sequence.

Read next:

1. [Architecture](space-navigator-arch.md) for DAHN and MAP boundaries.
2. [Interaction Grammar](space-navigator-interaction-grammar.md) for the
   normative spatial model.
3. [Design Specification](space-navigator-design-spec.md) for concrete
   Space Navigator behavior.
