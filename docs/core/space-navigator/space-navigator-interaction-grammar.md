# DAHN Space Navigator Interaction Grammar

## Status

Draft normative specification for the Space Navigator spatial interaction
model.

## Purpose and Authority

This document defines the small set of spatial and compositional rules that
generate valid Space Navigator interaction. It sits between the DAHN
Architecture and the Space Navigator Design Specification:

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

Architecture defines the available mechanisms and their ownership. This grammar
defines valid spatial transformations using those mechanisms. The Design
Specification defines the concrete Node, Collection, action, and editing
interactions that invoke those transformations.

This document is normative for Space Navigator topology, projection, lineage,
compression, overflow, re-rooting, and allocation semantics. It does not
specify concrete widgets, Node-region composition, descriptor-to-presentation
mapping, loading behavior, or editing flows.

---

# 1. Vocabulary

## 1.1 Navigation Topology

The **navigation topology** is the persistent, occurrence-based structure
accumulated by inspection and traversal. It records semantic anchors and how
each occurrence was reached. It is not a page stack and it is not equivalent to
the currently rendered layout.

An occurrence remains in the topology until an explicit branch-closing or
re-rooting operation removes it from the current Canvas context.

## 1.2 Viewport Projection

The **viewport projection** is the bounded visible realization of the topology
around the current focus. It may expand, partially compress, fully compress, or
overflow occurrences without changing their semantic identity, provenance, or
topological attachment.

> The navigation topology persists; the viewport shows a focus-dependent
> projection of it.

## 1.3 Semantic Anchor and Occurrence

Every descendant remains attached to the visualizer occurrence that produced
it. A semantic holon may appear in more than one occurrence, each with its own
provenance and presentation state. Focus does not reattach descendants to a
different occurrence.

## 1.4 Horizontal Lineage

A **horizontal lineage** is a sequence of direct, single-valued continuation:

    A -> B -> C

It means **follow one thing**. A single-valued relationship or an equivalent
single-holon result may extend this lineage.

## 1.5 Vertical Lineage

A **vertical lineage** is collection-mediated continuation:

    A
     |
     Collection
     |
     selected B

It means **choose among many things**. The Collection occurrence is retained as
the mediator that preserves sibling context.

## 1.6 Branch

A **branch** occurs when more than one continuation is retained from a common
occurrence. The common occurrence is not duplicated merely to make branches
visible.

---

# 2. Topology Production Rules

The grammar generates topology through the following operations.

## 2.1 Inspect

`inspect(holon)` creates or activates a Node occurrence for that holon in the
current topology.

## 2.2 Horizontal Traversal

`traverse-right(occurrence, singular-affordance)` creates or activates a child
Node occurrence to the right of its source occurrence.

The affordance must be structurally singular. Runtime population does not alter
its axis: an empty singular relationship remains singular.

## 2.3 Vertical Traversal

`traverse-down(occurrence, plural-affordance, member)` first exposes the
Collection occurrence associated with a structurally plural affordance, then
creates or activates the selected member's child Node beneath it.

The Collection remains the semantic mediator for sibling scanning. Runtime
population does not alter its axis: a one-member or empty plural relationship
remains plural.

## 2.4 Branch

`branch(anchor, continuation)` retains an additional continuation from an
existing anchor. It must preserve the anchor and existing branches rather than
reconstruct a linear page history.

## 2.5 Scan Lineage

`scan(lineage, direction, focus)` changes the focus-dependent projection of an
existing lineage. It does not replace the topology or reinterpret prior
occurrences as children of the newly focused occurrence.

## 2.6 Restore

`restore(occurrence)` returns a compressed or overflowed occurrence to a more
useful visible extent while retaining its prior local state where feasible.

## 2.7 Re-root

`re-root(occurrence)` establishes that occurrence's semantic holon as the new
Canvas root and discards prior topology from this Canvas context.

Re-rooting is deliberately different from traversal:

> Traversal extends topology. Re-rooting replaces retained context.

---

# 3. Projection and Extent Rules

## 3.1 Bounded Viewport and Pinned Chrome

The Canvas viewport is bounded. Navigation topology may grow beyond it.
Canvas-level chrome remains pinned relative to the viewport while the topology
is projected beneath it.

The viewport must not grow indefinitely merely to retain all history at full
size.

## 3.2 Independent Axis Extents

Each occurrence has independently selected width and height extents:

| Extent | Meaning |
| --- | --- |
| Expanded | Receives a useful full allocation on that axis. |
| Partially compressed | Suppresses expensive presentation while preserving the axis-relevant active navigation context. |
| Fully compressed | Preserves minimal identity, topology, and recoverability. |

An occurrence can therefore be expanded, X-compressed, Y-compressed, or
compressed on both axes. Exact visual realization belongs to the selected
Visualizer and the Design Specification.

## 3.3 Partial Compression Preserves Scanning

Partial compression is not merely historical decoration. It must retain the
active surface needed to scan the relevant lineage:

- partial horizontal compression preserves singular-navigation context;
- partial vertical compression preserves collection-navigation context.

## 3.4 Full Compression Preserves Topology

Fully compressed occurrences preserve occurrence identity, semantic anchor,
provenance, child links, and recoverability. Compression changes projection; it
does not discard navigation state or semantic state.

## 3.5 Compression and Overflow Are Distinct

Compression is a Visualizer realization under a smaller allocation. Overflow is
a Canvas placement decision that may move an already fully compressed occurrence
outside the visible branch viewport.

The valid progression is:

    expanded -> partially compressed -> fully compressed -> overflowed

`overflowed` is not a fourth child layout mode.

## 3.6 Hidden-Lineage Discoverability

When lineage overflows, the Canvas must provide a lightweight directional means
to discover and recover it. The grammar requires discoverability and direction;
the Design Specification chooses the concrete affordance.

Historical context need not remain physically visible merely to prove that it
exists.

---

# 4. Lineage Geometry and Branching

## 4.1 Stable Attachment

A continuation remains attached to the occurrence that produced it. If an
occurrence has both vertical and horizontal descendants, moving the focus along
one lineage must not move the other lineage to the currently focused sibling.

## 4.2 Cross-Axis Consistency

At a lineage intersection:

- the vertical lineage shares the current width of its intersection occurrence;
- the horizontal lineage shares the current height of its intersection
  occurrence.

This keeps the topology geometrically coherent as allocation changes.

## 4.3 Common-Parent Spanning

A compressed common ancestor spans the visible cross-axis envelope of branches
it semantically anchors:

- a vertically branching parent may span visible child width;
- a horizontally branching parent may span visible child height.

The span reflects the visible descendant envelope only. Off-screen descendants
do not force it to consume their theoretical extent.

## 4.4 Branch-Local Overflow

Overflow applies to the relevant lineage or branch allocation, not as
indiscriminate scrolling of the whole Canvas. Unrelated branches retain their
own topology and allocation context.

---

# 5. Allocation, Maximization, and State

## 5.1 Parent-Owned External Allocation

The parent Canvas or Visualizer owns a child's external allocation and
placement. The child chooses its internal composition within that allocation.

This rule applies recursively and prevents a child from claiming Canvas space
outside the region assigned by its parent.

## 5.2 Local Maximize and Restore

`maximize-region(occurrence, region)` redistributes only the allocation already
owned by that occurrence. It does not change navigation topology, overflow,
the Canvas viewport, or a sibling's allocation.

`restore-region` returns to the ordinary internal composition.

## 5.3 Distinct Transformations

The following operations must not be conflated:

| Operation | Changes topology? | Changes external allocation? | Changes internal allocation? |
| --- | --- | --- | --- |
| Compression | No | Yes | May require a compact realization. |
| Overflow | No | Placement only | No. |
| Maximize | No | No | Yes. |
| Re-root | Yes | Establishes a new root projection | May restore the new root's useful extent. |

## 5.4 State Survival

Compression, overflow, scanning, and maximization must not inherently discard:

- semantic or staged state;
- occurrence identity and provenance;
- selected affordances and child links;
- local collection and navigation context;
- selected Visualizer identity.

The Architecture assigns ownership of these state classes; the Design
Specification defines their concrete presentation and recovery behavior.

---

# 6. Grammar Invariants

The Space Navigator MUST preserve these invariants:

1. The viewport is bounded while topology may grow.
2. Canvas chrome is pinned relative to the viewport, not embedded in scrolling
   topology.
3. Single-valued traversal extends horizontal lineage; collection-mediated
   traversal extends vertical lineage.
4. Existing lineage remains stably attached as focus changes.
5. Independent width and height compression are representable.
6. Partial compression retains the relevant active scanning context.
7. Full compression preserves topology and recoverability.
8. Overflow is branch-local and hidden lineage remains discoverable.
9. Cross-axis lineage sizing follows the intersection occurrence.
10. A compressed common ancestor spans the visible envelope of its branches.
11. Parents own external child allocation; children compose locally.
12. Compression, overflow, maximization, and re-rooting have distinct
    semantics.

---

# 7. Relationship to Adjacent Specifications

The Architecture defines the Rust/TypeScript ownership boundary, occurrence
identity model, layout/slot contracts, theme ownership, and transaction state
ownership used by this grammar.

The Design Specification applies this grammar to concrete interactions. For
example, it specifies which rail activation invokes horizontal traversal, how a
collection row invokes vertical traversal, which Node regions remain available
at a given extent, and how editing and loading state appear.

The Implementation Plan sequences those requirements into PRs. It must not
introduce alternate topology, compression, or allocation semantics.

## Intentionally Deferred Presentation Decisions

This grammar does not prescribe:

- exact edge controls for hidden lineage;
- pixel dimensions, animation, or compression thresholds;
- the concrete rendering of a compact occurrence;
- the widget used for local maximize/restore;
- sibling-history retention policy beyond the topology invariants.

Those decisions belong in the Design Specification when they become necessary.
