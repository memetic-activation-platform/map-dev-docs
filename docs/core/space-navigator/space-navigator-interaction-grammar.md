# DAHN Space Navigator Interaction Grammar

**Version:** 0.3

## Status

Draft normative specification for **reusable DAHN compositional obligations and Space Navigator experience composition**.

## Change Log

### v0.3

Formalizes reusable DAHN composition, Window Manager authority, surface/view separation, and context creation while retaining Path Inspector ownership of rooted-navigation rules.

### v0.2

Narrows this document to the interaction grammar owned by the Space Navigator Dancer. Rooted-navigation topology, two-dimensional grid projection, traversal, branching, viewport, compression, and overflow semantics have been removed from this document and are normatively defined by `path-inspector-grammar.md`.

### v0.1

Initial grammar. It combined Space Navigator experience composition with rooted-navigation behavior that is now owned by Path Inspector.

## Purpose and Authority

Space Navigator is a **Dancer** that composes capabilities into a coherent navigation experience. It is not itself the RootedNavigation visualizer and does not own the internal spatial grammar of rooted navigation.

This document defines reusable DAHN compositional obligations (§1.5–1.9) and their Space Navigator application. The Dancer-specific contract includes:

- establishment of the active `HolonSpace` context;
- provision of a `RootedNavigation` visualizer slot initially rooted at that active HolonSpace, with explicit anchors for new exploration contexts;
- use of the Visualizer Selection Service to bind an applicable RootedNavigation visualizer;
- allocation of Space Navigator's received spatial budget among its top-level experience roles;
- preservation of the semantic boundary between the Dancer experience and the visualizers selected to realize its roles.

The normative grammar for the current RootedNavigation realization is `path-inspector-grammar.md`.

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

The conceptual experience stack is:

    DAHN Experience
        -> Window Manager
        -> Window / Viewport (top-level experiential context)
        -> Canvas
        -> Composition / Navigation Surface
        -> Visualizer Occurrences
        -> Visualizer Slots
        -> Child Visualizers

These are authority and contract boundaries, not a requirement for one UI component per level. A Dancer composes experience roles hosted within this stack; selected visualizers may recursively own composition surfaces.

The **Window Manager** owns top-level experiential-context creation/destruction, finite display allocation, context placement and switching, and maximize/restore/minimize where supported. A conventional window is only one realization: tabs, tiles, single-context switching, multiple displays, spatial volumes, rooms, or immersive contexts MAY implement the same authority. It grants each Canvas a bounded viewport/allocation.

A **Canvas** owns composition inside its granted context: hosted-role placement, child allocations, composition-surface extent, view transformation, focus projection, and recovery of off-viewport content. It MUST NOT assume ownership of the whole DAHN display. Expansion beyond its grant is a request to the Window Manager. A selected RootedNavigation visualizer may own a nested navigation surface and its layout/view operations; Canvas authority does not permit reaching through that boundary to manipulate its geometry.

## 1.6 Surface, Layout, and View

The spatial model is:

    Navigation Topology
        -> Navigation Layout
        -> Navigation Surface
        <-> View Transform
        -> Viewport
        -> Human-visible projection

A **Composition Surface** contains a spatial realization; a **Navigation Surface** is its rooted-navigation specialization. A **Viewport** is the finite view onto that potentially larger surface. Layout determines placement and allocation. The **View Transform** determines view position and scale. Panning/scrolling and zooming MUST NOT inherently recompute layout or change allocation, compression, or topology.

**A Visualizer at 50% zoom is not a compressed Visualizer.** Compression reduces allocation and may invoke a different responsive realization; zoom preserves layout and allocation. Surface growth beyond the viewport is permitted. An uncompressed Visualizer MAY declare or negotiate its minimum useful extent. The Path Inspector application of this contract protects an open Holon Inspector from being forced below that extent solely by viewport exhaustion ([Path Inspector §4.6](path-inspector-grammar.md#46-minimum-useful-extent-and-surface-growth)). Exact dimensions remain presentation decisions.

Canvas-level `zoom-to-fit` changes only view scale and, as needed, position to fit the relevant surface extent. It MUST preserve topology, occurrence budgets, compression, and layout geometry. `focus/actual-size` returns to the normal useful scale and centers the active/open occurrence; other occurrences may then be off-viewport and reachable by pan or Zoom to Fit. For nested surfaces these requests are handled by the composition owner of that surface.

## 1.7 Parent-Owned Allocation and Maximization

Every composition host owns external allocation and placement of its immediate children and grants a budget/context through a slot. Children own internal realization, MAY report minimum/preferred extents and supported presentations, and MUST respect their granted allocation.

Three operations have distinct authority:

| Operation | Authority and effect |
| --- | --- |
| `maximize-region(occurrence, region)` / local restore | The Visualizer redistributes only its existing allocation among internal regions; restore returns its prior local composition. |
| Canvas focus / occurrence maximize | The composition host gives an occurrence dominant attention in its viewport, preserving surrounding topology; any allocation change is explicit and distinct from a view-only focus/actual-size operation. |
| Window/context maximize / restore | The Window Manager changes the context's share of the DAHN display where supported. |

A participant MAY redistribute resources it owns; expansion beyond that boundary MUST be requested from its parent authority. Requests may propagate through hosts without bypassing them. Local maximization MUST NOT silently become global maximization or topology removal.

## 1.8 Slots as Participation Contracts

A Visualizer Slot is an experiential participation contract, not merely a structural placeholder or a HolonType match. Its requirements can combine semantic role, required capabilities, supplied experiential context, allocation, and interaction obligations. Independently authored Visualizers from federated Commons must satisfy the slot/context in which they participate.

Possible contract dimensions include budget responsiveness, minimum/preferred or intrinsic sizing, compact and focus capabilities, inherited theme/design tokens, accessibility, input conventions, and state-survival obligations. This list is illustrative, not a finalized schema. Semantic capability requirements and subsequent real-estate negotiation remain distinct from selecting a Visualizer by transient pixel dimensions. The contract MUST leave room for future formalization without prescribing child internals.

## 1.9 Independent State and Experiential Authority

Topology, layout/allocation, and view are independent state dimensions. Inspect/traverse/branch/close affect topology; placement, compression, minimum and surface extents affect layout; pan, zoom, viewport and attention affect view. A semantic interaction may explicitly coordinate dimensions, but they MUST NOT be collapsed into one enumerated state machine.

Compression, focus, local maximization, off-viewport placement, or zoom MUST NOT implicitly discard occurrence/navigation state or semantic/staged state. Closing an occurrence removes its branch under the selected navigation grammar, not externally owned Nursery/transaction state. Context destruction likewise is not implicit transaction abandonment; any semantic disposal follows its owner's explicit contract.

These boundaries preserve experiential sovereignty: no Visualizer seizes global space, no Canvas commandeers its Window Manager, and inherited experiential policies remain under person/context control. **Standardize the seams, not the implementations.** This is not a universal visual design system. Infinite 2D, grid, tiling, radial, focus+context, timeline, 3D, and immersive Canvases and alternative Window Managers remain valid if they preserve these obligations.

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

Re-root means establishing a semantic anchor as the root of a new exploration context. Space Navigator routes this intent through its hosts to the Window Manager; the default is a new top-level context preserving the source topology. Window Manager policy chooses window, tab, tile, spatial volume, or another realization. Failure or refusal MUST leave the source intact. A source-disposing policy must be explicit, never inferred from re-root itself.

The new context carries the anchor and applicable experiential context, not the source occurrence's identity or an implicit transfer/discard of its transaction. Transaction sharing versus isolation requires an explicit context policy. `replace-current-root`, if offered, is a separately named operation that explicitly replaces current navigation topology while respecting semantic-state ownership.

Close branch, occurrence focus/maximize, and re-root MUST remain separate intents: remove a branch, concentrate within a context, and create a rooted context respectively. Their Path Inspector productions are defined in [its grammar](path-inspector-grammar.md#2-topology-production-rules).

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
- compression, layout overflow, and off-viewport recovery;
- child spatial budgets and responsive composition.

This document intentionally does not restate those rules.

---

# 5. Relationship to Adjacent Specifications

DAHN Architecture defines the general mechanisms used here, including Dancer versus Visualizer responsibility, visualizer slots, Visualizer Selection, and recursive spatial allocation. Sections 1.5–1.9 refine their reusable compositional interaction obligations; they do not prescribe a Window Manager implementation or final slot schema.

The Space Navigator design specification should define the concrete Space Navigator experience built from those mechanisms.

The Path Inspector grammar defines the behavior of the current RootedNavigation visualizer selected into that experience.

Implementation plans MUST preserve these ownership boundaries rather than introducing a second rooted-navigation grammar at the Space Navigator layer.

---

# 6. Deferred Presentation Decisions

Window metaphors, pan/zoom controls, focus labels/iconography, exact useful extents, responsive thresholds, and alternative Canvas layout policies remain presentation choices. The generalized slot schema and cross-context transaction sharing policy remain separate contract decisions; neither may weaken the state-survival or parent-authority rules above.

---

# 7. Summary

Space Navigator composes the experience. Path Inspector realizes rooted navigation within that experience.

The governing boundary is:

> **Space Navigator owns experience composition and top-level role allocation. The selected RootedNavigation visualizer owns rooted-navigation topology and internal spatial interaction.**
