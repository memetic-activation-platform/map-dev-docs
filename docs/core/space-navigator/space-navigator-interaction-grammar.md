# DAHN Space Navigator Interaction Grammar

**Version:** 0.4

## Status

Draft normative specification for **Space Navigator experience composition**. Shared DAHN composition contracts are defined in the DAHN design specification.

## Change Log

### v0.4

Delegates reusable composition, allocation, surface/view, and state-survival
contracts to the DAHN design specification; retains Dancer-owned application.

### v0.3

Formalizes reusable DAHN composition, Window Manager authority, surface/view separation, and context creation while retaining Path Inspector ownership of rooted-navigation rules.

### v0.2

Narrows this document to the interaction grammar owned by the Space Navigator Dancer. Rooted-navigation topology, two-dimensional grid projection, traversal, branching, viewport, compression, and overflow semantics have been removed from this document and are normatively defined by `path-inspector-grammar.md`.

### v0.1

Initial grammar. It combined Space Navigator experience composition with rooted-navigation behavior that is now owned by Path Inspector.

## Purpose and Authority

Space Navigator is a **Dancer** that composes capabilities into a coherent navigation experience. It is not itself the RootedNavigation visualizer and does not own the internal spatial grammar of rooted navigation.

This document defines Space Navigator's application of the shared
[DAHN composition contracts](../hx/dahn-design-spec.md#29-canvas-dancer-and-rooted-navigation-responsibilities). The Dancer-specific contract includes:

- establishment of the active `HolonSpace` context;
- provision of a `RootedNavigation` visualizer slot initially rooted at that active HolonSpace, with explicit anchors for new exploration contexts;
- use of the Visualizer Selection Service to bind an applicable RootedNavigation visualizer;
- allocation of Space Navigator's received spatial budget among its top-level experience roles;
- preservation of the semantic boundary between the Dancer experience and the visualizers selected to realize its roles.

The normative grammar for the initial RootedNavigation realization is the
[Path Inspector grammar](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md).

> **Space Navigator decides that rooted navigation is part of the experience. Path Inspector decides how rooted navigation behaves.**

---

# 1. Space Navigator Composition

## 1.1 Active HolonSpace Context

A Space Navigator experience operates in the context of an active `HolonSpace`.

The active HolonSpace supplies the initial semantic root for Space Navigator's RootedNavigation role. A newly requested exploration context MAY instead carry an explicit Holon anchor while retaining its applicable HolonSpace context. Changing the navigation anchor does not change the active HolonSpace or confer ownership of that Holon on it. Roots and centers are contextual/perspectival, not ontologically privileged. Space Navigator MAY expose other experience roles associated with that HolonSpace, but those roles are independent of the internal Path Inspector grammar.

## 1.2 RootedNavigation Role

Space Navigator MUST expose a visualizer role whose required semantic contract is `Structure / RootedNavigation`.

Conceptually:

    SpaceNavigator Dancer
        ->
    RootedNavigation slot
        subject/root = active HolonSpace or explicit new-context anchor
        ->
    Visualizer Selection Service
        ->
    applicable RootedNavigation visualizer

The slot expresses **what semantic role must be fulfilled**. It does not prescribe the concrete visualizer that fulfills it.

## 1.3 Visualizer Selection

Space Navigator MUST use the DAHN Visualizer Selection Service to resolve the RootedNavigation slot rather than hard-coding Path Inspector as an implementation dependency.

`PathInspector` is the current concrete RootedNavigation visualizer, but another applicable RootedNavigation visualizer MAY satisfy the same slot in the future.

Selection concerns semantic applicability and the participation requirements of the slot (§1.8). Space Navigator does not select a RootedNavigation visualizer by prescribing its internal row, column, viewport, compression, or child-layout behavior.

## 1.4 Spatial Allocation

Space Navigator receives an external spatial budget from its containing visualizer or Canvas context.

As a containing experience, Space Navigator owns allocation among its immediate top-level roles. It passes a bounded allocation to the selected RootedNavigation visualizer.

The selected RootedNavigation visualizer then owns its own internal spatial composition. Space Navigator MUST NOT reach through that boundary to control Path Inspector rows, columns, cells, viewport position, compression policy, or child visualizer geometry.

> **The containing Dancer experience allocates space to the role; the selected visualizer owns the role's internal realization.**

## 1.5 DAHN Composition Authorities

The [shared DAHN contract](../hx/dahn-design-spec.md#291-dahn-composition-authorities)
is authoritative. Space Navigator applies it at its direct role boundaries;
it does not own selected Visualizers' internal realization.

## 1.6 Surface, Layout, and View

The [shared DAHN contract](../hx/dahn-design-spec.md#292-surface-layout-and-view)
is authoritative. Space Navigator applies it at its direct role boundaries;
it does not own selected Visualizers' internal realization.

## 1.7 Parent-Owned Allocation and Maximization

The [shared DAHN contract](../hx/dahn-design-spec.md#30-parent-owned-allocation)
is authoritative. Space Navigator applies it at its direct role boundaries;
it does not own selected Visualizers' internal realization.

## 1.8 Slots as Participation Contracts

The [shared DAHN contract](../hx/dahn-design-spec.md#301-layout-budgets-and-participation)
is authoritative. Space Navigator applies it at its direct role boundaries;
it does not own selected Visualizers' internal realization.

## 1.9 Independent State and Experiential Authority

The [shared DAHN contract](../hx/dahn-design-spec.md#311-independent-state-and-experiential-authority)
is authoritative. Space Navigator applies it at its direct role boundaries;
it does not own selected Visualizers' internal realization.

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
- compression, layout overflow, and off-viewport recovery;
- branch closing and re-root requests;
- child spatial budgets and semantic presentation obligations.

Space Navigator MUST NOT duplicate or redefine those rules.

## 2.2 Dancer-Level Interactions

Interactions remain Space Navigator responsibilities when they change the composition or context of the Space Navigator experience itself rather than the internal rooted-navigation state of the selected visualizer.

Examples include:

- establishing or changing the active HolonSpace context;
- mounting or replacing a visualizer that fills a Space Navigator role;
- allocating top-level experience space among Space Navigator roles;
- coordinating other Dancer-level capabilities that surround RootedNavigation.

Changing the active HolonSpace is distinct from re-rooting at a Holon within that space and MAY require a new RootedNavigation subject/root. The selected RootedNavigation visualizer determines how that new root is realized according to its own contract.

## 2.3 New Exploration Context Requests

Re-root means establishing a semantic anchor as the root of an additional exploration tab within the same Space Navigator experience. Space Navigator owns the tabs and their RootedNavigation slots. The first tab is rooted at the active HolonSpace; a new tab may be rooted at any compatible reached Holon. Each selected RootedNavigation Visualizer owns its internal navigation geometry. These exploration tabs are not Window Manager top-level contexts: the enclosing Canvas and Window Manager context remain in place. Failure or refusal MUST leave the source intact.

The new tab receives an explicit semantic anchor separately from the applicable HolonSpace and inherits the Space Navigator experience's Dancer identity, Theme, and agent/runtime context. The action need only identify the anchor; the owning experience supplies inherited context. Each tab creates fresh occurrence identities and independently retains topology, provenance, selections, focus, and view transform. Switching tabs preserves those states. Closing a tab releases its presentation resources without closing sibling explorations.

Space Navigator is the shared experience owner of the read transaction used by its read-only exploration tabs. Tabs reuse that transaction's bound references and semantic cache rather than creating a transaction or duplicating cached semantic data for each viewport. Unloaded data may still require retrieval. Read transactions remain segregated from write transactions; request coordination follows the shared transaction's execution constraints. Tab creation, switching, and closure neither dispose the shared transaction nor transfer or abandon staged work. Editing across tabs requires a separate explicit transaction policy before it is enabled.

`replace-current-root`, if offered, is a separately named operation that explicitly replaces current navigation topology while respecting semantic-state ownership.

### Activation and realization outcomes

An exploration request immediately presents a pending tab indicator while keeping
the source active. The destination becomes ready when its root exploration is
usable; readiness does not require loading every lazy relationship. Creating a
container or displaying a realization-error placeholder does not establish readiness.

On readiness, Space Navigator activates the destination unless the user has
switched tabs while it was pending. After such a switch, completion marks the
destination ready without stealing focus; the user chooses when to activate it.

Failure or refusal removes the pending destination, releases its incomplete
presentation resources, and presents a dismissible error with Retry in Space
Navigator. The source exploration and shared read transaction remain intact.
Cancellation or teardown prevents late completion from attaching or activating
disposed content.

Close branch, occurrence focus/maximize, and re-root MUST remain separate intents: remove a branch, concentrate within a context, and create a rooted exploration tab respectively. Their Path Inspector productions are defined in [its grammar](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md#2-topology-production-rules).

---

# 3. Ownership Invariants

Space Navigator MUST preserve these invariants:

1. Space Navigator is a Dancer experience, not a RootedNavigation visualizer.
2. The active HolonSpace supplies the initial root; an explicitly requested exploration context may supply another Holon anchor.
3. The RootedNavigation role is expressed as a semantic visualizer slot.
4. The Visualizer Selection Service chooses the concrete visualizer that fills that slot.
5. Space Navigator allocates external space to its immediate roles but does not own their internal geometry.
6. Rooted-navigation topology and spatial interaction semantics belong to the selected RootedNavigation visualizer.
7. Space Navigator MUST NOT duplicate Path Inspector's traversal, grid, viewport, insertion, compression, overflow, or child-layout grammar.
8. Window Manager display allocation, Canvas composition, and Visualizer-local realization have separate parent-bounded authority.
9. Surface extent, occurrence allocation, and view scale remain distinct; zoom never implicitly compresses.
10. Re-root preserves the source by default; branch closure does not abandon staged work.
11. Replacing one applicable RootedNavigation visualizer with another MUST NOT require Space Navigator to understand that visualizer's internal interaction grammar.

---

# 4. Relationship to Path Inspector

`PathInspector` is the current concrete DAHN `Structure / RootedNavigation` visualizer used by Space Navigator.

Its normative interaction grammar is the
[Path Inspector grammar](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md).

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
- compression, layout overflow, and off-viewport recovery;
- child spatial budgets and responsive composition.

This document intentionally does not restate those rules.

---

# 5. Relationship to Adjacent Specifications

DAHN Architecture defines the general mechanisms used here, including Dancer versus Visualizer responsibility, visualizer slots, Visualizer Selection, and recursive spatial allocation. Sections 1.5–1.9 link to the canonical shared contracts; they do not define another Window Manager implementation or slot schema.

The Space Navigator design specification should define the concrete Space Navigator experience built from those mechanisms.

The Path Inspector grammar defines the behavior of the current RootedNavigation visualizer selected into that experience.

Implementation plans MUST preserve these ownership boundaries rather than introducing a second rooted-navigation grammar at the Space Navigator layer.

---

# 6. Deferred Presentation Decisions

Window metaphors, pan/zoom controls, focus labels/iconography, exact useful extents, responsive thresholds, and alternative Canvas layout policies remain presentation choices. The generalized slot schema and editing-transaction policy across exploration tabs remain separate contract decisions; neither may weaken the state-survival or parent-authority rules above.

---

# 7. Summary

Space Navigator composes the experience. Path Inspector realizes rooted navigation within that experience.

The governing boundary is:

> **Space Navigator owns experience composition and top-level role allocation. The selected RootedNavigation visualizer owns rooted-navigation topology and internal spatial interaction.**
