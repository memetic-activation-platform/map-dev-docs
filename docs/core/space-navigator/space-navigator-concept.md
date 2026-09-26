# DAHN Space Navigator — Concept

## What It Is

The **Space Navigator** is a DAHN **Dancer** for exploring, inspecting, and
eventually editing a MAP Space through its holons and their effective
affordances. It composes `HolonSpace`-specific experience roles, including a
generic Rooted Navigation Visualizer rooted at that `HolonSpace`.
Canvas hosts the resulting experience without making either Space Navigator or
Rooted Navigation a Canvas kind.

It is not a succession of domain-specific screens. It is a generic,
descriptor-driven experience that can present previously unknown holon types
through selected Node, Collection, Property, Value, and Action Visualizers.

The Navigator is not a Canvas and is not DAHN itself. A Canvas may host the
Space Navigator alongside other Dancers, switch among them, or compose them.

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

# Entering DAHN

Before the initial Space Navigator is exposed, DAHN may offer a short **DAHN
Launch Experience**: an entry ritual rather than a splash screen. Its movement
from cosmos to stellar light, living Earth, living place, and finally I-Space
locates the person as a participating local center within progressively larger
wholes:

> **cosmogenesis → planetary emergence → life → place → participation**

The initial narrative is **NGC 346 → stellar-light transition → Earth →
Okavango Delta → I-Space / Space Navigator**. It must suggest continuity
across those scales, not simulate literal travel or claim that a star in NGC
346 is the Sun. The intended meaning of the arrival is: *here, within all of
this, is the local center from which you participate*—not an isolated ego or
avatar.

This first Navigator is deliberately a proto-experience: a practical opening
of MAP's visual layer, not its definitive visual expression. Richer
visualizations and alternative experience designs remain possible through the
Visualizer Commons. A future descent to a person's actual bioregion or
locality is a design north star, not an MVP commitment.

The launch experience is constrained by the Space Navigator architecture but
is not a MAP visualizer or a Visualizer Commons contribution. Its observable
behavior, accessibility, provenance, and application-shell boundary are
defined in the [Design Specification](space-navigator-design-spec.md); its
delivery slice is defined in the implementation plan.

---

# Descriptor-Driven Experience

The essential principle is:

> **Definitions determine structure; runtime data populates it.**

Descriptors determine which relationships are defined and their structural
shape. A singular relationship remains singular when empty; a plural
relationship remains plural with one target. Runtime discovery determines
which of these relationships currently offer somewhere to navigate. Normal
browsing progressively reveals populated relationships; editing and schema
inspection can also expose empty ones.

Navigation establishes topology before content: first determine that a
destination exists, then make room for it, communicate what is opening there,
and populate that same space. This preserves the visible connection between
action, destination, and result.

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
[Path Inspector Interaction Grammar](path-inspector-grammar.md).

---

# Reusable Visual Roles

The initial experience composes reusable roles:

- a **space role** for the `HolonSpace` Holon itself, realized through an
  appropriate Node Visualizer;
- an **afforded-Dancers role** for Dancers afforded by that `HolonSpace`;
- a **Rooted Navigation Visualizer** for the evolving navigation structure
  anchored at that `HolonSpace`;

- a **Node Visualizer** for one holon and its affordances;
- a **Collection Visualizer** for a homogeneous plural result;
- **Property** and **Value Visualizers** for scalar presentation; and
- **Action Visualizers** for available actions.

A table is an initial Collection Visualizer, not the permanent definition of a
collection. Likewise, generic fallback visualizers preserve usability when no
specialized visualizer applies.

Holons `OwnedBy` the `HolonSpace` form an initial heterogeneous ownership
structure. It gives the experience meaningful current context, but is distinct
from the interaction-derived navigation topology that Rooted Navigation
progressively unfolds through traversal.

A future `AgentSpace` may extend `HolonSpace` with additional agent, social,
or governance affordances. That could add roles to Space Navigator without
specializing the generic Rooted Navigation Visualizer.

---

# Context, Provenance, and Scale

Each inspected holon appears as a visualizer occurrence with its own provenance.
The same semantic holon may appear in more than one occurrence when reached by
different paths.

As exploration grows, the Rooted Navigation Visualizer need not keep every
occurrence fully expanded. It preserves recoverable context while allocating
its Canvas-provided real-estate budget toward the current area of work. This is
why the experience remains a navigable space rather than an ever-growing page
or a history that must be discarded.

---

# Read and Edit Are One Experience

The Navigator is intended to inspect and manipulate MAP state through the same
descriptor-driven visual structure. Editing is a mode of an existing
occurrence, not a second form-oriented application. MAP retains ownership of
semantic and staged state while the Space Navigator retains its experience and
occurrence state within the Canvas-provided allocation.

The Architecture and Design Specification define those responsibilities and
concrete behavior respectively.

---

# Relationship to the Rest of the Specification

This document explains the mental model. It does not define architectural
ownership, spatial transformation invariants, concrete UI behavior, or delivery
sequence.

Read next:

1. [Architecture](space-navigator-arch.md) for DAHN and MAP boundaries.
2. [Space Navigator Interaction Grammar](space-navigator-interaction-grammar.md)
   for composition and [Path Inspector Interaction Grammar](path-inspector-grammar.md)
   for the normative spatial model.
3. [Design Specification](space-navigator-design-spec.md) for concrete
   Space Navigator behavior.
4. [Implementation Plan](space-navigator-impl-plan.md) for delivery order.
