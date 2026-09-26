# DAHN Space Navigator Interaction Grammar

**Version:** 0.2

## Status

Draft normative specification for **Space Navigator experience composition**.

## Change Log

### v0.2

Narrows this document to the interaction grammar owned by the Space Navigator Dancer. Rooted-navigation topology, two-dimensional grid projection, traversal, branching, viewport, compression, and overflow semantics have been removed from this document and are normatively defined by `path-inspector-grammar.md`.

### v0.1

Initial grammar. It combined Space Navigator experience composition with rooted-navigation behavior that is now owned by Path Inspector.

## Purpose and Authority

Space Navigator is a **Dancer** that composes capabilities into a coherent navigation experience. It is not itself the RootedNavigation visualizer and does not own the internal spatial grammar of rooted navigation.

This document defines only the composition-level interaction contract owned by Space Navigator:

- establishment of the active `HolonSpace` context;
- provision of a `RootedNavigation` visualizer slot rooted at that active HolonSpace;
- use of the Visualizer Selection Service to bind an applicable RootedNavigation visualizer;
- allocation of Space Navigator's received spatial budget among its top-level experience roles;
- preservation of the semantic boundary between the Dancer experience and the visualizers selected to realize its roles.

The normative grammar for the current RootedNavigation realization is `path-inspector-grammar.md`.

> **Space Navigator decides that rooted navigation is part of the experience. Path Inspector decides how rooted navigation behaves.**

---

# 1. Space Navigator Composition

## 1.1 Active HolonSpace Context

A Space Navigator experience operates in the context of an active `HolonSpace`.

The active HolonSpace supplies the semantic root for Space Navigator's RootedNavigation role. Space Navigator MAY expose other experience roles associated with that HolonSpace, but those roles are independent of the internal Path Inspector grammar.

## 1.2 RootedNavigation Role

Space Navigator MUST expose a visualizer role whose required semantic contract is `Structure / RootedNavigation`.

Conceptually:

    SpaceNavigator Dancer
        ->
    RootedNavigation slot
        subject/root = active HolonSpace
        ->
    Visualizer Selection Service
        ->
    applicable RootedNavigation visualizer

The slot expresses **what semantic role must be fulfilled**. It does not prescribe the concrete visualizer that fulfills it.

## 1.3 Visualizer Selection

Space Navigator MUST use the DAHN Visualizer Selection Service to resolve the RootedNavigation slot rather than hard-coding Path Inspector as an implementation dependency.

`PathInspector` is the current concrete RootedNavigation visualizer, but another applicable RootedNavigation visualizer MAY satisfy the same slot in the future.

Selection concerns semantic applicability. Space Navigator does not select a RootedNavigation visualizer by prescribing its internal row, column, viewport, compression, or child-layout behavior.

## 1.4 Spatial Allocation

Space Navigator receives an external spatial budget from its containing visualizer or Canvas context.

As a containing experience, Space Navigator owns allocation among its immediate top-level roles. It passes a bounded allocation to the selected RootedNavigation visualizer.

The selected RootedNavigation visualizer then owns its own internal spatial composition. Space Navigator MUST NOT reach through that boundary to control Path Inspector rows, columns, cells, viewport position, compression policy, or child visualizer geometry.

> **The containing Dancer experience allocates space to the role; the selected visualizer owns the role's internal realization.**

---

# 2. Interaction Boundary

## 2.1 Delegated Rooted Navigation

Once a RootedNavigation visualizer has been selected and mounted, interactions whose semantics belong to rooted navigation are delegated to that visualizer.

For Path Inspector, these include:

- occurrence creation and retention;
- horizontal and vertical traversal, including target-existence guards and
  destination-first transitions;
- replacement of untraversed leaves;
- retention and displacement of traversed alternatives;
- two-dimensional grid projection;
- row and column insertion;
- viewport movement;
- focus-dependent row and column allocation;
- compression and overflow;
- child spatial budgets and semantic presentation obligations.

Space Navigator MUST NOT duplicate or redefine those rules.

## 2.2 Dancer-Level Interactions

Interactions remain Space Navigator responsibilities when they change the composition or context of the Space Navigator experience itself rather than the internal rooted-navigation state of the selected visualizer.

Examples include:

- establishing or changing the active HolonSpace context;
- mounting or replacing a visualizer that fills a Space Navigator role;
- allocating top-level experience space among Space Navigator roles;
- coordinating other Dancer-level capabilities that surround RootedNavigation.

Changing the active HolonSpace MAY require a new RootedNavigation subject/root. The selected RootedNavigation visualizer determines how that new root is realized according to its own contract.

---

# 3. Ownership Invariants

Space Navigator MUST preserve these invariants:

1. Space Navigator is a Dancer experience, not a RootedNavigation visualizer.
2. The active HolonSpace supplies the root subject for Space Navigator's RootedNavigation role.
3. The RootedNavigation role is expressed as a semantic visualizer slot.
4. The Visualizer Selection Service chooses the concrete visualizer that fills that slot.
5. Space Navigator allocates external space to its immediate roles but does not own their internal geometry.
6. Rooted-navigation topology and spatial interaction semantics belong to the selected RootedNavigation visualizer.
7. Space Navigator MUST NOT duplicate Path Inspector's traversal, grid, viewport, insertion, compression, overflow, or child-layout grammar.
8. Replacing one applicable RootedNavigation visualizer with another MUST NOT require Space Navigator to understand that visualizer's internal interaction grammar.

---

# 4. Relationship to Path Inspector

`PathInspector` is the current concrete DAHN `Structure / RootedNavigation` visualizer used by Space Navigator.

Its normative interaction grammar is defined in:

    path-inspector-grammar.md

That document owns the rules for:

- rooted navigation topology;
- occurrence identity and provenance;
- horizontal and vertical traversal;
- retained-path branching;
- the two-dimensional grid;
- horizontal-path rows and vertical-path columns;
- orthogonal row/column insertion;
- sparse cells;
- the movable viewport;
- focus and spatial allocation;
- compression and overflow;
- child spatial budgets and responsive composition.

This document intentionally does not restate those rules.

---

# 5. Relationship to Adjacent Specifications

DAHN Architecture defines the general mechanisms used here, including Dancer versus Visualizer responsibility, visualizer slots, Visualizer Selection, and recursive spatial allocation.

The Space Navigator design specification should define the concrete Space Navigator experience built from those mechanisms.

The Path Inspector grammar defines the behavior of the current RootedNavigation visualizer selected into that experience.

Implementation plans MUST preserve these ownership boundaries rather than introducing a second rooted-navigation grammar at the Space Navigator layer.

---

# 6. Summary

Space Navigator composes the experience. Path Inspector realizes rooted navigation within that experience.

The governing boundary is:

> **Space Navigator owns experience composition and top-level role allocation. The selected RootedNavigation visualizer owns rooted-navigation topology and internal spatial interaction.**
