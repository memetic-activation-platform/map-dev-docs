# DAHN Path Inspector Interaction Grammar

**Version:** 0.13

## Change Log

### v0.14

Uses the four-experience Node slot contract and V2 presentation assignment.
Separates per-occurrence intent from shared-track allocation. Restore preserves
retained downstream presentations; fixed-reference budgets, topology productions,
provenance and whole-band placement remain under their existing owners.


### v0.13

Uses whole-band insertion for first-time destinations, source-adjacent placement
for new selections regardless of traversal group, branch-position swapping for
source-driven retained-target reactivation, and placement-preserving direct Restore.
Retains untraversed-destination replacement and explored-branch retention.
Supersedes terminal append and first-member spatial anchoring from v0.8–v0.12.


### v0.12

Replaces rendered child-extent negotiation with explicit Path policy profiles.
Defines the nine-state retention policy, capability-only Node assignment,
shared-track aggregation, bounded preferred viewport, and reduced-budget fallback.
Historical sizing rules below describe superseded revisions.


### v0.11

Initial allocation is content-first: retain the source title, tabs and five collection data rows with their controls/header, then add the channel and full target. This supersedes v0.10 capacity-based negotiation; collection height MUST NOT be capped by a viewport percentage.

### v0.10

Bounds viewpoint movement to the real navigation surface: attention MUST NOT introduce artificial leading margins or shift a first-column inspector away from the left edge. Initial two-stage capacity is negotiated with Node participants so immediate collection context and the full useful target fit together without traversal-time resize. This refines v0.9's literal centering rule.

### v0.9

Makes active-frontier visibility part of traversal: after final allocation, the viewport follows the target by centering the active inspector, preserving immediate source context where the surrounding view permits. Initial Actual Size allocation is derived from the contextual-source, channel, and full-target composition on both axes. This supersedes historical upper-left viewport anchoring; retained geometry still grows only down/right.

### v0.8

Restores **monotonic expansion**: topology-producing traversal moves retained geometry only down and/or right. The first retained member anchors its traversal group; subsequent members append at its outward terminal edge. Later groups move outward when an earlier group grows. A newly opened group takes the source-aligned canonical cell and moves older groups outward, preserving their relative order. Repeated traversal appends within its existing group without promoting that group.

Preserves v0.7 traversal provenance, labels, qualifiers, Predicate-qualified Expand, navigational Dance semantics, destination-first presentation, branch retention, compression, surface/view separation, close, and re-root. Existing band and channel dimensions survive displacement independently of explicit allocation changes. Earlier change-log entries describe historical behavior superseded by this revision.

### v0.7

Generalizes lineage presentation from relationship-oriented labels to traversal-oriented provenance so future navigation operations can use the same spatial grammar without implying that every connector represents a stored semantic relationship.

- Defines **Traversal Provenance** as the recorded operation by which a target occurrence was reached.
- Defines a **Traversal Label** as the compact human-readable projection of that provenance rather than necessarily a relationship name.
- Treats relationship expansion as one traversal form: the relationship predicate/name remains the primary label.
- Allows relationship expansion to carry an optional **Predicate**, consisting of Filters; the Predicate is recorded as part of traversal provenance.
- Allows a Predicate-qualified Expand to be signaled compactly on the connector label, for example with a funnel icon, without rendering the full Predicate on the connector.
- Treats a navigational Dance as another traversal form; the Dance name becomes the primary traversal label.
- Generalizes traversal grouping from “same relationship” to equivalent traversal provenance for grouping purposes, preventing differently constrained expansions or different Dance traversals from being collapsed merely because their visible labels resemble one another.
- Reaffirms that connector labels and qualifiers describe **how the occurrence was reached**; they do not assert a new semantic relationship between source and target Holons.
- Leaves exact qualifier iconography, Predicate inspection interaction, Dance-specific styling, and richer traversal-detail presentation intentionally deferred.

### v0.6

Historical note: v0.7 generalizes the relationship-oriented terminology introduced here into traversal provenance, labels, qualifiers, and traversal groups.

Refines retained-alternative layout into relationship-grouped traversal channels while preserving the Path Inspector's two-axis navigation grammar.

- Widens horizontal and vertical traversal channels so lineage connectors can carry small, subordinate labels naming the relationship or navigational affordance traversed.
- Establishes **source-target axis alignment**: every newly opened horizontal target is immediately to the right of and in the same row as its source; every newly opened vertical target is immediately below and in the same column as its source.
- Groups retained sibling targets from the same source by traversal affordance. Horizontal relationship groups are contiguous vertically; vertical relationship groups are contiguous horizontally.
- Appends a new member of an existing relationship group at that group's terminal position: bottom-most for horizontal traversal groups and right-most for vertical traversal groups.
- Reflows existing same-relationship members toward the opposite side of the source axis as needed so the new target can remain source-aligned while occupying the group's terminal position. Later relationship groups are displaced outward as groups.
- Requires descendants to move with a displaced target branch, preserving branch geometry, occurrence identity, and provenance.
- Allows sibling connectors for the same source and traversal affordance to share one relationship label where the routing remains unambiguous.
- Preserves compression semantics: traversal real estate is obtained jointly through source/context compression and traversal-channel allocation rather than channel growth alone.
- Replaces the earlier fixed "prior continuation moves one row down / one column right" rule with semantic relationship-group insertion and reflow.

### v0.5

Places the grammar with Path Inspector; distinguishes its Node participation
requirements from Holon Inspector private realization and delegates shared DAHN
mechanisms to their canonical specification.

### v0.4

Separates topology, navigation layout/surface, and view transformation; defines branch closing and non-destructive re-root requests; reconciles minimum useful extent, layout overflow, and off-viewport recovery with reusable DAHN composition authority.

### v0.3

Adds target-existence guards and destination-first structural transitions while preserving traversal axes, retained paths, and parent-owned geometry.

### v0.2

Refines the Path Inspector's two-dimensional grid projection and retained-path branching semantics.

- Makes this document the authoritative grammar for RootedNavigation behavior realized by Path Inspector.
- Establishes that each **column preserves a vertical traversal path** and each **row preserves a horizontal traversal path**.
- Clarifies that the viewport moves over the persistent grid; focus is not anchored to a fixed row or column.
- Establishes orthogonal insertion for retained alternatives: a new vertical alternative preserves the current column and displaces the traversed prior vertical path into a newly inserted column to the right; a new horizontal alternative preserves the current row and displaces the traversed prior horizontal path into a newly inserted row below.
- Clarifies that insertion shifts the affected retained path and the grid bands beyond it while preserving occurrence identity and provenance.
- Retains whole-column width and whole-row height allocation: all cells in a column share its width and all cells in a row share its height.
- Removes the earlier asymmetry in which only columns carried semantic lineage while rows were treated primarily as geometric alignment.
- Reaffirms that sparse cells are valid when required to preserve truthful horizontal and vertical traversal paths.
- Defines directional lineage connectors for both axes, preserving recorded parentage across retained alternatives, sparse projection, compression, and viewport movement.

### v0.1

Initial Path Inspector interaction grammar establishing occurrence-based rooted navigation, horizontal and vertical traversal, sparse projection, focus-dependent allocation, compression and overflow, recursive spatial allocation, and responsive child composition.

## Status

Draft normative specification for the **Path Inspector** spatial interaction model.

## Purpose and Authority

This document defines the small set of spatial and compositional rules that generate valid **Path Inspector** interaction.

The Path Inspector is a concrete DAHN **Structure / RootedNavigation** visualizer. It realizes an interaction-derived navigation topology rooted at a Holon. It may be composed into a larger Dancer experience such as Space Navigator, but its interaction grammar is not specific to Space Navigator.

The [DAHN architecture](../../../../dahn-arch.md) assigns shared responsibility;
[DAHN design](../../../../dahn-design-spec.md) defines reusable composition
mechanisms. This grammar owns Path Inspector's spatial productions. Its
[design specification](design-spec.md) describes subject/slot binding and the
concrete interactions that invoke those productions.

This document is normative for:

- Path Inspector navigation topology;
- occurrence identity, traversal provenance, directional lineage connectors, traversal labels, and traversal qualifiers;
- horizontal and vertical traversal semantics;
- sparse row/column projection and relationship-grouped sibling placement;
- focus-dependent row and column allocation;
- compression and overflow;
- child spatial budgets;
- semantic presentation obligations passed to child visualizers;
- restoration and re-rooting.

It does not prescribe:

- a particular Node visualizer implementation;
- the internal regions of a Node visualizer;
- exact pixel dimensions or thresholds;
- concrete compact representations;
- theme or styling;
- descriptor-to-presentation mapping;
- concrete loading presentation or retrieval implementation;
- editing flows.

The central distinction is:

> **The Path Inspector owns the topology and inter-child geometry. Selected child visualizers own their internal responsive realization within the spatial budgets and semantic obligations they receive.**

---

# 1. Vocabulary

## 1.1 Rooted Navigation Topology

The **rooted navigation topology** is the persistent, occurrence-based structure accumulated by inspection and traversal from a root Holon.

It records:

- the semantic anchor of each occurrence;
- the occurrence from which it was reached;
- the affordance through which it was reached;
- whether the traversal was singular or collection-mediated;
- retained branches and local navigation context.

It is not a page stack and it is not equivalent to the currently rendered layout.

Retained occurrences remain in the topology until explicit branch closing or `replace-current-root` removes them (the untraversed-leaf replacement rule in §2.4 still applies). Re-root does not itself remove source occurrences.

## 1.2 Root

The **root** is the initial semantic Holon from which the current rooted navigation topology unfolds.

Roots and centers are contextual/perspectival, not ontologically privileged. The Path Inspector can in principle be rooted at any Holon. A containing Dancer such as Space Navigator may choose a HolonSpace as its root, but HolonSpace is not intrinsic to the RootedNavigation grammar.

## 1.3 Occurrence

An **occurrence** is one appearance of a semantic subject within the rooted navigation topology.

A semantic Holon may appear in more than one occurrence when reached through different navigation paths. Each occurrence retains its own provenance and presentation context.

Holon identity and occurrence identity are therefore distinct.

## 1.4 Focus

The **focus** is the occurrence at the active navigation frontier.

Navigation focus may coordinate viewport position with explicit row/column allocation changes. View-only focus/actual-size or Canvas attention does not inherently invoke that allocation policy. It does not alter topology or reattach descendants. Focus is not permanently associated with any particular row or column.

## 1.5 Viewport

The **viewport** is the bounded visible region through which the Path Inspector presents part of its potentially larger two-dimensional grid.

The viewport may present different horizontal and vertical portions of the grid as focus changes or the user pans. Its view transform records position and scale; panning and zooming alone MUST NOT recompute layout or compression. Moving the viewport does not re-root the Path Inspector, renumber occurrence identity, or rewrite traversal provenance.

The grid persists independently of the viewport:

> **The grid retains navigation structure; the viewport moves over it.**

## 1.6 Navigation Topology Versus Spatial Projection

The navigation topology records what has been unfolded and how occurrences are related.

The **Navigation Layout** derives row/column placement and allocations from topology and allocation policy. The **Navigation Surface** contains that geometry and may exceed the finite viewport. The human-visible **spatial projection** is the view of this surface through the current view transform and viewport, not a second layout constrained to fit the screen.

> **Topology persists; geometry is derived.**

Changes in focus, compression, viewport size, or child responsive realization do not by themselves change the navigation topology.

## 1.7 Horizontal Traversal

A **horizontal traversal** follows a structurally singular affordance from one occurrence to one target occurrence.

Conceptually:

    A -> B -> C

Horizontal traversal means:

> **Follow one thing.**

A single-valued relationship or equivalent single-Holon result may produce horizontal traversal.

## 1.8 Vertical Traversal

A **vertical traversal** follows a structurally plural affordance through a Collection occurrence and selects one member for deeper inspection.

Conceptually:

    A
     |
     Collection
     |
     selected B

Vertical traversal means:

> **Choose among many things.**

The Collection occurrence remains the semantic mediator that preserves sibling context.

## 1.9 Column

A **column** is a vertical grid band that preserves one vertical traversal path.

First-time rightward traversal inserts a whole column immediately right of its source.
Vertical traversal preserves its source column. Retained alternatives and branch
reactivation follow §2.4; traversal groups do not impose terminal column placement.

Every cell in a column receives the same current width budget.

## 1.10 Row

A **row** is a horizontal grid band that preserves one horizontal traversal path.

First-time downward traversal inserts a whole row immediately below its source stage.
Horizontal traversal preserves its source row. Retained alternatives and branch
reactivation follow §2.4; traversal groups do not impose terminal row placement.

Every cell in a row receives the same current height budget.

The governing symmetry is:

> **Columns preserve vertical traversal paths. Rows preserve horizontal traversal paths.**

## 1.11 Sparse Cell

A **sparse cell** is an intentionally unoccupied row/column intersection.

Sparse cells are legitimate structural elements of the projection. They preserve truthful alignment when a horizontal expansion originates from a lower row and therefore requires a distinct adjacent column.

Whitespace may therefore carry structural information.

## 1.12 Spatial Budget

A **spatial budget** is the external width and height allocation a parent visualizer gives a child visualizer.

The parent owns the budget. The child owns its internal composition within that budget.

## 1.13 Semantic Presentation Obligations

**Semantic presentation obligations** are requirements a parent may impose on a child realization without prescribing the child's concrete internal layout.

Examples may include:

- preserve recognizable identity;
- preserve the ability to continue singular navigation;
- preserve recoverability;
- indicate staged state where required.

An obligation states **what semantic capability must remain available**, not which internal widget, rail, panel, icon, or region must implement it.

## 1.14 Traversal Provenance

**Traversal provenance** records how a target occurrence was reached from its source occurrence.

At minimum it identifies the traversal kind and the navigational operation that produced the target. Supported and anticipated forms include:

- expansion of a relationship;
- expansion of a relationship qualified by an optional Predicate consisting of Filters;
- invocation of a navigational Dance.

Traversal provenance belongs to the navigation occurrence edge. It does not create or modify a semantic relationship between the source and target Holons.

A filtered relationship expansion still traverses the named relationship. The Predicate constrains the result of that traversal and is therefore recorded as a traversal qualifier, not as a new RelationshipType.

A navigational Dance may derive its result through behavior more complex than expansion of one stored relationship. Its provenance therefore records the Dance rather than fabricating a relationship predicate.

## 1.15 Traversal Label and Qualifier

A **traversal label** is the compact human-readable projection of traversal provenance shown on or with a lineage connector.

The primary label SHOULD identify the operation in the vocabulary natural to that operation:

- for relationship expansion, the relationship predicate/name is the primary label;
- for a navigational Dance, the Dance name is the primary label.

A **traversal qualifier** is a compact signal that additional traversal semantics apply beyond the primary label. For an Expand qualified by a Predicate, the label MAY carry a funnel icon or equivalent compact filter indicator.

The compact connector presentation need not render the full Predicate, its Filters, Dance parameters, or other detailed provenance. Such detail MAY be exposed through a richer inspection interaction outside the core spatial grammar.

Visible label text alone MUST NOT be treated as the authoritative traversal identity.

## 1.16 Traversal Group

A **traversal group** is the ordered set of retained sibling target occurrences reached from the same source occurrence through equivalent traversal provenance for grouping purposes.

Group membership derives from the recorded traversal operation and its semantically
relevant qualifiers, not target identity, adjacency or label text alone. Unfiltered
and Predicate-qualified expansions, or distinct Dance traversals, are not merged
merely because their visible labels match.

Grouping preserves semantic provenance and chronological history; it does not
require spatial contiguity or reserve a canonical cell for the first member.
Source-adjacent selection, whole-band insertion, retained-branch exchange and
Restore follow §2.4–§2.6. Connector routing keeps the source, target and provenance
unambiguous when retained alternatives occupy displaced bands.

New-destination creation displaces retained history outward. Explicit source-driven
reactivation can move an existing incoming branch inward. Direct Restore changes
focus/allocation/view without changing placement. These operations must not be
conflated under one blanket monotonic-movement rule.

## 1.17 Traversal Channel

A **traversal channel** is the inter-child spatial region through which a lineage connector runs between a source and its target or target group.

The channel is Path Inspector geometry. It may be wider or taller than a minimal grid gap so that the connector, its traversal label, and any compact qualifier remain legible. Channel allocation is coordinated with row/column allocation and compression; it is not a child-owned region or an independent semantic occurrence.

---

# 2. Topology Production Rules

## 2.1 Inspect

`inspect(holon)` creates or activates a Node occurrence for that Holon in the current topology.

The root inspection establishes the initial focus.

## 2.2 Horizontal Traversal

`traverse-right(occurrence, singular-affordance)` creates or activates a child Node occurrence to the right of its source, using the source-adjacent position and insertion/retention rules under §2.4.

The affordance must be structurally singular. Runtime population does not alter its axis: an empty singular relationship remains singular.

The new child becomes the focus unless the invoking interaction explicitly specifies otherwise.

## 2.3 Vertical Traversal

`traverse-down(occurrence, plural-affordance, member)` exposes or activates the Collection occurrence associated with a structurally plural affordance and creates or activates the selected member's child Node below the source stage, using the source-adjacent position and insertion/retention rules under §2.4.

The Collection remains the semantic mediator for sibling scanning.

Runtime population does not alter the axis: an empty or one-member plural relationship remains plural.

The selected child becomes the focus unless the invoking interaction explicitly specifies otherwise.

## 2.4 Branch and Retained Alternative Insertion

`branch(anchor, continuation)` retains an additional continuation from an existing anchor when the continuation currently selected from that anchor has already been traversed onward.

A new destination selection from the same source replaces its current untraversed
destination, subject to the existing dismissal and state-safety guards. Once
navigation has continued through that destination, the occurrence and its
continuation are retained history and MUST NOT be overwritten by another selection
from the source. Retain that destination with its descendants as an alternative.
Restoring an already retained destination is distinct from creating a replacement.

### Whole-band insertion for first-time destinations

When establishing a source's rightward destination for the first time, insert a
whole column immediately right of the source. Shift all existing columns at or
beyond the insertion point rightward, across every row, then place the destination
in the new column at the source row. Establishing its downward destination for
the first time inserts a whole row immediately below the source stage: shift all
existing rows at or beyond that point downward, across every column, and place
the destination in the new row at the source column.

Insert the band even when the target intersection in an existing band is empty.
An empty intersection does not authorize reuse of that band. Preserve occurrence
identity and provenance as whole-band coordinates shift. A replaced untraversed
destination reuses its established cell. Retained-alternative displacement and
source-driven branch reactivation follow the rules below, rather than allocating
a new forward band for every repeated selection.

For A→B with an older A↓X, first B↓C inserts a row immediately below A/B.
C occupies the new row under B; X's entire row moves down. C and X do not share
a row merely because they could fit at different column intersections.

### Source-adjacent placement of a new destination

Every newly created destination takes the source-adjacent canonical position:
immediately right of its source in the source row for horizontal traversal, or
immediately below its source stage in the source column for vertical traversal.
This applies even to another selection through the same relationship or equivalent
traversal provenance. A traversal group does not reserve that position for its
first member or force a new destination to a terminal append position.

If the previous destination is untraversed, replace it under the state-safety
rule above. If it has been traversed onward, retain its occurrence and descendants
as an alternative. Move the retained horizontal continuation downward, or the
retained vertical continuation rightward, as needed to free the canonical position.
Preserve branch identity, provenance, contracted state and internal relative
geometry. Existing retained alternatives keep their relative order during that
outward displacement. Grouping records semantic provenance; it must not override
source-adjacent placement of a new destination.

For A→B→C, selecting a new D from A places D immediately right of A and moves
the retained B→C continuation down intact. The vertical counterpart moves an
explored prior continuation rightward while the new destination takes the cell
immediately below the source stage. New destination creation never pulls retained
history upward or left to manufacture room. Whole-band insertion and direct occurrence restoration follow their explicit
rules here and in §2.6.

### Selecting a retained destination through its source

When a source selects an already-retained destination, reuse that occurrence and
its retained continuation rather than creating a duplicate or reinitializing its
state. Bring that continuation back to the source-adjacent canonical position.
If the currently selected destination is untraversed, replace it under the ordinary
safety rule. If it has been traversed onward, exchange the two continuations'
branch positions: the outgoing branch takes the alternative position vacated by
the incoming branch. It does not move above or left of the source.

A branch-position exchange is not a promise of identical rectangular footprints.
Unequal footprints may require outward reflow to preserve a valid non-overlapping
grid. Preserve each branch's occurrence identity, provenance, meaningful state and
internal structure. This explicit reactivation can move the incoming retained
branch inward; it is distinct from new-destination creation, whose retained-history
displacement remains outward.

Selecting a destination through its source is distinct from directly restoring
an occurrence in its existing region. Direct Restore preserves topology and
row/column placement; it changes focus, allocation and view as needed to reveal
and expand the occurrence where it already sits. It does not promote a retained
branch or change its source's selected continuation.

This rule supersedes terminal-append and first-member spatial anchoring.
Chronological group membership remains provenance, not a placement override.

> **Replace an eligible leaf; otherwise retain its explored continuation and give
> the new destination the source-adjacent position.**


## 2.5 Scan

`scan(lineage, direction, focus)` changes the focus-dependent projection of an existing lineage.

Scanning does not:

- replace the topology;
- reinterpret prior occurrences as children of the newly focused occurrence;
- discard sibling context;
- change semantic provenance.

## 2.6 Restore

Direct occurrence Restore preserves topology and row/column placement. It grants
usable inspection allocation and reveals the occurrence in place; the child resumes
its remembered Properties or Collection view. It does not swap branches, change
the source's selected continuation, or restore stale pixel dimensions.

Restore changes only the requested occurrence's presentation requirement. Retained
downstream occurrences keep their existing presentations and meaningful state.
A shared-column expansion changes all occupants' widths coherently, but does not
itself restore or compact those occupants. Navigation, source-driven branch
reactivation, and ancestry-changing Close have their own explicit reassignment rules;
a generic render or allocation pass must not undo Restore.

For A↓B→C, the initial assignment is A:Relationship, B:Relationship, C:Properties,
with A remembering its prior Collection. Restoring A resumes that Collection and
expands A/B's shared column. B stays Relationship and C stays Properties. Their
rectangles may change under the shared-track rules; presentation and allocation
remain separate. The same column width is supplied to both A and B before and
after Restore. Preserving downstream presentations does not require equal widths
between unrelated columns.

An offscreen occurrence can also be revealed by a view-only pan without changing
its presentation or allocation. Direct Restore is distinct from that view operation.

### Reclaiming bands after explicit branch closure

Explicit Close removes the selected occurrence branch subject to existing workflow
and state-safety guards. Afterwards reclaim only rows or columns that are wholly
empty across the retained surface, shifting subsequent bands together. Preserve
partially occupied bands and legitimate sparse cells; do not repack unrelated
surviving Nodes independently into holes. Reclamation preserves surviving occurrence
identity, provenance, descendant attachment and meaningful state. This explicit
removal may move subsequent bands upward/left, unlike new-destination insertion.

## 2.7 Re-root

`re-root(occurrence)` requests a new exploration context rooted at the occurrence's semantic Holon. In Space Navigator, the owning Dancer creates another exploration tab under the [composition contract](../../../../../space-navigator/space-navigator-interaction-grammar.md#23-new-exploration-context-requests), within the same enclosing Canvas and Window Manager context. The source occurrence and its descendants remain in the source topology by default; the new context creates its own root occurrence identity.

For `A -> B -> C -> D`, re-rooting C leaves that path intact and establishes a separate context rooted at C. In Space Navigator, this is a second tab sharing the experience-owned read transaction while retaining independent navigation state. Refusal/failure leaves the source unchanged; re-root does not dispose the source.

If offered, `replace-current-root(holon)` explicitly replaces the current topology and is a distinct operation, not an alias for re-root. Neither operation implicitly transfers or abandons semantic/staged state.

> **Traversal extends topology. Re-root establishes another rooted context.**

---

## 2.8 Destination-First Transitions

Relationship navigation MUST establish that a destination exists before changing
focus, compressing the source, replacing a leaf, inserting a branch, or allocating
a destination. Verified zero targets produce local feedback without structural
navigation. Unknown or failed inspection is not evidence of emptiness. A singular
relationship with multiple targets follows existing cardinality validation/error
semantics; it MUST NOT silently become plural or choose an arbitrary target.

After existence is established, the spatial sequence MUST be:

1. apply whole-band insertion, replacement/retention or retained-branch reactivation under §2.4 and derive the final source-adjacent destination;
2. establish destination real estate through source/context compression, traversal-channel allocation, and pan/reflow
   as required by the existing focus-dependent allocation rules;
3. occupy that real estate with a pending destination presentation;
4. replace the pending presentation with resolved content in-place.

For a fully expanded source followed horizontally, partial compression and the
opening of the derived right-hand destination MUST be perceptible before content
appears. Reserve the destination at its final source-adjacent position, never
show it temporarily elsewhere before relocating it. The vertical rule is symmetric.
This ordering preserves provenance and the operation-specific placement rules.

The selected Node owns exposing, loading, allocating, and switching its internal
collection presentation under its own child contracts. Path Inspector receives
the semantic intent to navigate a selected Holon member and establishes that
member's destination Node through the sequence above. Opening or switching a
collection alone does not allocate a Path destination or discard previously
traversed occurrences. Internal placement is not required to be beneath the
source for every substitute Node. See [Holon Inspector collection activation](../../../node/holon-inspector/design-spec.md#42-local-properties-and-collection-switching)
for that concrete realization's collection-region behavior.

Reduced-motion presentation may omit motion but MUST preserve Path-owned
destination ordering and localized pending feedback. An empty collection supplies
no member-navigation intent; its internal empty-state treatment belongs to its
owning Node/Collection contract, not Path geometry.

After deriving final destination geometry and applying contextual allocation, the Path Inspector MUST adjust the viewport within surface bounds to reveal the active destination and its immediate source context before presenting pending destination content. Materialization fills that same policy-allocated region; selected child content does not revise track extents or relocate the destination. Pending and failed realizations retain the same geometry.

---

## 2.9 Close Branch

`close(occurrence)` removes that occurrence and all its descendant occurrences from this topology. It MUST preserve shared ancestors and unrelated branches, including other occurrences of the same semantic Holon. For `A -> B -> C -> D`, closing C leaves `A -> B`; if B also has `E -> F`, that branch remains intact.

In collection-mediated navigation, closing a descendant removes only its lineage; closing the Collection occurrence removes the exploration descended through it. Removal follows recorded occurrence parentage, not grid adjacency or semantic identity. Closing the root leaves an empty navigation topology; it does not itself destroy the top-level context.

If focus was removed, the nearest surviving ancestor becomes navigation focus,
or focus is cleared if none survives. Reclaim only wholly empty rows/columns as
specified in §2.6; do not compact surviving siblings individually or promote one
merely to fill a sparse canonical cell. If the source needs another selected
continuation, that is an explicit source-driven selection under §2.4. Preserve
pending destinations attached to surviving branches and their state-safety guards.
Closing MUST NOT discard externally owned staged edits, Nursery state, transaction
participation or Undo history. Occurrence-local presentation may be released;
semantic disposal requires a separate operation by its owner.

---

# 3. Two-Dimensional Grid Projection

## 3.1 Projection as a Derived Grid

The Path Inspector projects its rooted navigation topology into a sparse two-dimensional grid of rows and columns.

The grid is not the semantic source of truth. It is a geometric realization derived from:

- retained navigation topology;
- traversal provenance;
- current focus;
- available Path Inspector allocation.

The grid may grow as retained alternatives require additional rows or columns. The viewport remains bounded and moves over this potentially larger grid.

## 3.2 Traversal-Path Integrity

The Path Inspector MUST preserve both traversal axes:

> **Each column preserves a vertical traversal path. Each row preserves a horizontal traversal path.**

A projection MUST NOT compact occurrences in a way that falsely joins unrelated vertical paths within a column or unrelated horizontal paths within a row.

Whitespace and sparse cells are therefore valid structural consequences of preserving both path systems simultaneously.

## 3.3 Replaceable Leaves

When the occurrence currently selected from an anchor has not itself been traversed onward, another destination selection from that same anchor replaces it in its established
traversal position, subject to the state-safety rules in §2.4.

Changing collection tabs or the collection being viewed inside a Node visualizer is local child state and does not itself extend Path Inspector topology. Selecting a collection member creates or activates a vertical child occurrence.

Once navigation continues through a child occurrence, that child becomes part of retained navigation history and MUST NOT be overwritten by a later alternative selection from the same anchor.

<a id="34-vertical-alternative-insertion-and-grouping"></a>

## 3.4 Vertical Destination Insertion and Alternatives

Vertical traversal follows §2.4. A first-time destination inserts a whole row
below the source stage. Later new selections use the source-adjacent destination
cell, replacing an untraversed destination or moving an explored continuation
rightward intact. Traversal provenance does not change these placement rules.
Selecting an already-retained destination reuses and promotes it, exchanging
branch positions if the outgoing continuation must also be retained.

<a id="35-horizontal-alternative-insertion-and-grouping"></a>

## 3.5 Horizontal Destination Insertion and Alternatives

Horizontal traversal follows the symmetric rule in §2.4. A first-time destination
inserts a whole column right of the source. Later new selections use that
source-adjacent cell, replacing an untraversed destination or moving an explored
continuation downward intact. Retained-target selection reuses/promotes and,
where necessary, exchanges branch positions. Direct Restore leaves placement alone.

For H1→H1.1→X, selecting a new H1.2 from H1 gives:

    H1 → H1.2
         H1.1 → X

If H1.2 has also been explored, selecting H1.1 again through H1 promotes H1.1→X
and moves H1.2's intact branch to the vacated alternative position. If H1.2 is
untraversed, replace it. Merely restoring H1.1 where displayed does not exchange
these positions. Connector routing continues to identify their true source H1.


## 3.6 Grid-Band Reflow Preserves Identity and Group Order

Row and column positions are projection properties, not occurrence identities.

Insertion and relationship-group reflow may change the grid coordinates of existing occurrences, but MUST NOT change:

- occurrence identity;
- semantic Holon identity;
- the source occurrence from which an occurrence was reached;
- the affordance through which it was reached;
- traversal direction;
- traversal-group membership;
- relative insertion order within a traversal group;
- descendants or retained continuation.

New-destination insertion displaces existing bands/retained alternatives outward.
Source-driven retained-target reactivation may promote/exchange branches; explicit
Close reclaims whole-empty bands. Direct Restore and Pan do not change placement.
Preserve descendant attachment and meaningful branch structure under each operation;
semantic provenance grouping does not require spatial contiguity.

> **Coordinates may move; provenance, grouping, and attachment do not.**

## 3.7 Sparse Cells Are Not Occurrences

A sparse cell:

- has no semantic Holon;
- has no visualizer occurrence identity;
- does not participate in selection;
- does not create navigation provenance;
- exists only to preserve truthful projection geometry.

Sparse cells may arise above, below, left, or right of occupied cells as row and column insertion reconciles the two traversal-path systems.

## 3.8 Stable Attachment

Insertion, traversal-group reflow, compression, scanning, viewport movement, and focus movement MUST NOT alter the semantic attachment of a descendant.

A continuation remains attached to the occurrence that produced it even when its current row or column position changes.


## 3.9 Lineage Connectors, Channels, Labels, and Qualifiers

The Path Inspector MUST expose recorded parentage through directional lineage connectors for horizontal and vertical traversal, including retained alternatives and recursive mixed-axis paths. Connectors are a projection of navigation provenance, not additional topology or semantic relationships between Holons.

Each connector MUST identify its source and target by occurrence identity and use the recorded traversal kind and traversal provenance. Grid adjacency, DOM order, shared Holon identity, membership in a visual group, or matching label text MUST NOT imply parentage or traversal equivalence. Sparse cells and connector crossings do not create occurrences, edges, or junctions.

Horizontal lineage connects the source occurrence's right boundary to the target occurrence's left boundary, with a rightward arrowhead at the target. Vertical lineage connects the source navigation stage's lower boundary to the target occurrence's upper boundary, with a downward arrowhead at the target; where traversal is collection-mediated, the source Collection remains the semantic mediator recorded by vertical provenance.

The inter-inspector traversal channel MUST provide sufficient width for horizontal lineage and sufficient height for vertical lineage to render the connector, its primary traversal label, and any compact traversal qualifier legibly.

The primary traversal label describes the navigational operation that produced the target:

- a relationship expansion uses the relationship predicate/name;
- a navigational Dance uses the Dance name.

When relationship expansion is qualified by a Predicate consisting of Filters, the connector MAY add a compact funnel icon or equivalent filter qualifier beside the relationship label. The qualifier indicates that the displayed result was constrained during traversal; it MUST NOT imply a new RelationshipType or alter the semantic meaning of the underlying relationship.

The connector is intentionally a compact projection of provenance. It is not required to display the full Predicate, individual Filters, Dance parameters, or other operation detail. Exact interaction for inspecting that richer provenance is outside this grammar.

Sibling targets reached from the same source through equivalent traversal provenance MAY share one traversal label and qualifier presentation when their connector routing makes the shared meaning unambiguous. Traversals with materially different provenance or qualifiers MUST remain distinguishable and MUST NOT share a label merely because their primary label text matches. Label sharing is a projection optimization; each target retains its own recorded traversal provenance.

For the source-adjacent selected destination, the connector SHOULD use the most
direct orthogonal segment available. Retained alternatives use branching or elbow
routing through the traversal channel; grouping does not reserve a spatial anchor. Source, target, direction, group attachment, and label association MUST remain unambiguous.

Insertion, retained-branch exchange and empty-band reclamation follow their
operation-specific movement rules. A connector remains attached to the original
source and target occurrence and is rerouted through the actual traversal channel.
Displacement changes routing, not recorded traversal direction, provenance or source.

Path Inspector owns lineage routing, traversal-channel geometry, traversal-label placement, and compact qualifier placement as inter-child geometry. A child Node visualizer MUST NOT be required to draw or reserve its own external connector.

Connectors, labels, and qualifiers are presentation geometry. They MUST NOT intercept or reinterpret child interactions, create semantic relationships, or change topology. Exact typography, iconography, channel dimensions, stroke width, color, corner treatment, and spacing are theme-responsive presentation details rather than fixed pixel values in this grammar.

---

# 4. Focus-Dependent Geometry

## 4.1 Navigation Focus Determines Allocation Priority

The Path Inspector preferentially allocates space toward the current focus and its immediate exploration context while the viewport moves over the persistent grid as needed.

Prior or non-focused context may receive progressively smaller allocations while remaining visible or recoverable.

## 4.2 Column Width Is a Path Inspector Decision

The Path Inspector assigns a width to each projected column.

All cells in a column receive the same external width budget for that column.

When navigation focus or allocation policy changes (not merely when the view pans or zooms), the Path Inspector may:

- allocate the focused column a useful expanded width;
- partially compress contextual columns;
- fully compress more distant columns;
- grow the surface so columns outside the viewport remain reachable;
- apply explicit layout-overflow policy where applicable (§7.4).

Displacing columns MUST preserve their existing widths and inter-column channel widths; only a separate explicit allocation decision may resize them.

Column allocation MUST also account for required vertical traversal-channel width where the column participates in downward lineage. A child visualizer does not independently choose the width of its column or the traversal channel.

## 4.3 Row Height Is a Path Inspector Decision

The Path Inspector assigns a height to each projected row.

All cells in a row receive the same external height budget for that row.

When navigation focus or allocation policy changes (not merely when the view pans or zooms), the Path Inspector may:

- allocate the focused row a useful expanded height;
- partially compress contextual rows;
- fully compress more distant rows;
- grow the surface so off-viewport rows remain reachable;
- apply explicit layout-overflow policy where applicable (§7.4).

Displacing rows MUST preserve their existing heights and inter-row channel heights; only a separate explicit allocation decision may resize them. Compression is not permission to move retained grid positions upward or left.

Row allocation MUST also account for required horizontal traversal-channel height where the row participates in rightward lineage. A child visualizer does not independently choose the height of its row or the traversal channel.

## 4.4 Cell Budget Is Derived

The external spatial budget of a cell is the intersection of its column width and row height:

    cell width  = allocated width of its column
    cell height = allocated height of its row

Thus a cell may naturally receive:

- expanded width and expanded height;
- compressed width and expanded height;
- expanded width and compressed height;
- compressed width and compressed height.

These combinations need not be modeled as named Path Inspector states.

## 4.4.1 Node Inspector Slot Compression Contract

The [Node Inspector Slot Contract](design-spec.md#3-child-slots-and-their-contracts)
defines four experiences independently of a concrete Node's private widgets:
Properties, Collection, Relationship, and Compact identity. Path supplies dimensions
and an optional explicit presentation request through
`ApplyNodePresentationV2.VisualizerOperator`. The old required-capability-set input
and nine-state capability matrix do not define this contract.

The request identities are `inspect`, `collection-context`, `relationship`, and
`compact`. Inspect resumes the remembered Properties or Collection view; it does
not introduce a fifth mode. Collection context also permits local full-content
switching without changing Path focus or requesting larger tracks. Relationship
and Compact retain that memory. Omitted presentation means dimensions-only delivery,
which preserves the current view. Identity and accessible Restore are unconditional.

### ApplyNodePresentation invocation and completion

The slot requires the declared V2 Operator, admitted against the selected Node.
A single assignment supplies whole CSS-pixel width/height and any explicit request.
Validate the full input before publication; acceptance is synchronous and explicit,
not a browser-paint guarantee. A valid grant that a selected child cannot apply is
a contract violation, with owner-provided recovery. Do not query child content for
a minimum, resize siblings, silently reselect, or invoke a Dance to apply geometry.
Pending, failed and materialized destinations occupy the same allocated rectangle.

### Contextual presentation and shared-track allocation

On successful navigation, retain the latest singular source as Relationship and
latest collection-member source in its full-content view under collection-context.
Older sources become Compact. Off-ancestry retained alternatives keep their state
without accumulating contextual grants. Compute explicit assignments for navigation,
source-driven reactivation, and ancestry-changing Close; resizing, rendering, pan,
and local Properties/Collection switching do not recompute presentation choices.

For A→B↓C, A receives Relationship, B collection-context, and C Inspect. For A↓B→C,
Path explicitly assigns Relationship to both A and B and Inspect to C, compressing
A/B's shared column. A's remembered Collection remains intact; its hidden full-content
minimum does not constrain the Relationship grant. Traversal axis and provenance
remain unchanged. A later shared-track resize alone cannot change a sibling's mode.

Track geometry and presentation are separate. Derive each column/row grant from
the strongest currently assigned requirement of its occupants, rather than deriving
child capabilities from the track intersection. A Compact occurrence stays Compact
in a wide column or tall row. Root, repeated subject, and retained occurrence
identity do not merge their local view memory.

### Explicit policy profiles and useful limits

The immediate slot owner owns the participation profile: minimum/preferred widths
and heights for Compact, contextual and inspection allocation, plus connector
channels. Theme/MDS inputs scale useful budgets without making descendants size
ancestor tracks. Each eligible participant promises the required range before
selection. Numeric defaults are tested policy data, not universal mode constants.

### Preferred viewport and reduced-budget fallback

Path requests the fixed reference footprint on each axis: Compact + context +
inspection + two labeled connector channels, including its framing once. That
request is not the bounding span of all retained history and is not a host-window
resize command. Actual grants flow through immediate owners.

### Stable dimensions and viewport recovery

For unchanged viewport, Theme and profile, dimensions assigned to each allocation
state remain stable through history growth, navigation and branch exchange.
Offscreen history remains on the retained surface. Below useful minima, retain
usable dimensions and allow pan/scroll instead of shrinking typography or fitting
all history. Reveal an oversized target at its top so identity/Restore remain
reachable. Zoom to Fit changes view only.

### Common-factor reduction from a fixed profile reference

Resolve one factor per axis from the fixed minimal + contextual + inspection
reference and two channels, independent of retained track count or positions.
With preferred total P, minimum total M, usable budget B and framing F:

    f = clamp((B - F - M) / (P - M), 0, 1)  when P > M
    f = 1                                  when P = M
    resolved_i = m_i + f * (p_i - m_i)

Apply the same resolved state/channel dimensions throughout the surface. Resolve
to whole CSS pixels within the profile bounds for V2 assignments. Count framing
once. At f=0 use minima and overflow; no child row count, prior-band maximum cache,
adaptive weighting or context-first reduction determines the factor.

### Attention projection

Occurrence attention is an immediate-owner operation distinct from direct Restore,
local Properties/Collection switching, view-only fit, and native-window maximize.
It may temporarily hide/inert ordinary-grid presentations while retaining mounted
participants, topology and stored tracks. It creates no fifth Node mode and does
not dispose semantic state. Restore uses the current grant, not stored old pixels.

### PropertyMap sub-slot content extent

A selected PropertyMap can wrap and scroll within its own allocation. Its rendered
rows and content height do not determine Node or Path tracks or compete with an
active Collection for a simultaneous properties pane.

## 4.5 Geometry Emerges From Topology and Focus

The Path Inspector SHOULD avoid enumerating every visually possible compression combination as a separate interaction state.

Instead:

    retained topology
        +
    current focus
        +
    Path Inspector spatial budget
        ->
    sparse row/column projection
        ->
    row heights + column widths
        ->
    per-cell spatial budgets

The mockup states are therefore best treated as **conformance examples produced by the grammar**, not as an exhaustive state machine.

This allows previously unmocked navigation paths to produce coherent geometry from the same rules.

---

## 4.6 Minimum Useful Extent and Surface Growth

The explicit Path policy profile establishes useful lower bounds, not rendered child measurements. Nodes MUST NOT be forced below those bounds solely because the viewport is exhausted. Whole-track compression follows navigation policy; when useful geometry exceeds the viewport, the Navigation Surface grows and pan/scroll makes it reachable. Lower bounds do not authorize a child to seize parent space. No universal pixel threshold is normative here.

## 4.7 View Operations and Pinned Chrome

`zoom-to-fit` adjusts scale and, as needed, position so the relevant surface extent fits the viewport. It MUST NOT change topology, occurrence allocation, compression, or layout geometry. `focus/actual-size` returns to the normal useful scale and reveals the active/open occurrence within real surface bounds. Compressed ancestors, siblings, and branches may remain off-viewport, reachable by pan or Zoom to Fit.

The view transform belongs to the owner of this navigation surface. Canvas-level requests directed to this nested surface are delegated through the composition boundary. Outer Canvas or Dancer pinned chrome stays within its own allocation and outside the navigation transform; it does not scale or pan with navigation content.

---

# 5. Parent and Child Spatial Responsibility

## 5.1 Parent Owns Inter-Child Geometry

The reusable [DAHN parent-owned allocation rule](../../../../dahn-design-spec.md#30-parent-owned-allocation) applies here: a compositional visualizer owns placement and external budgets of its immediate children within its own grant. Path Inspector does not own the containing Canvas or Window Manager allocation.

For the Path Inspector this means it owns:

- sparse two-dimensional grid projection;
- row and column insertion;
- row and column allocation;
- viewport positioning over the grid;
- child cell bounds;
- traversal-channel geometry, connector routing, traversal labels, and traversal qualifiers;
- traversal-group reflow;
- focus-dependent compression;
- branch-local overflow.

## 5.2 Child Owns Intra-Child Adaptation

A selected child visualizer owns its internal realization within the spatial budget assigned by the Path Inspector.

The Path Inspector MUST NOT require knowledge of implementation-specific internal regions such as:

- a Property Viewer Pane;
- a vertical relationship rail;
- a title bar;
- a Collection Tab Bar;
- a particular action control.

A concrete child such as HolonInspector may use those regions, but another valid Node visualizer may realize the same semantic obligations differently.

## 5.3 Recursive Spatial Allocation

The same ownership rule applies recursively.

Conceptually:

    parent allocation
        ->
    Path Inspector
        ->
    row/column cell allocation
        ->
    selected Node visualizer
        ->
    its own slot allocations
        ->
    selected subordinate visualizers
        ->
    their internal allocations

> **Parent visualizers own inter-child geometry. Child visualizers own intra-child adaptation.**

## 5.4 Budget Changes Do Not Trigger Reselection by Default

Spatial dimensions and compression thresholds are not, by default, criteria for the Visualizer Selection Service.

Once a visualizer has been selected for a slot, changes in the spatial budget SHOULD ordinarily cause that visualizer to adapt rather than cause the parent to request a different visualizer.

This preserves a clean distinction:

    selection
        -> which visualizer satisfies the semantic slot?

    allocation
        -> how much space does the selected visualizer receive now?

    responsiveness
        -> how does that visualizer realize itself within that space?

## 5.5 Semantic Capability May Constrain Selection

For this Path Inspector, the Node slot requires `ApplyNodePresentation` and
its contract in [§4.4.1](#441-node-inspector-slot-compression-contract). Rust-owned
selection MUST check declared Operator compatibility; runtime admission verifies
promised bindings under the [DAHN mechanism](../../../../dahn-design-spec.md#visualizer-operators-and-operations).
Participation is not optional. Before selection, a candidate must promise the
complete required capability/allocation contract across its supported input range,
not just the currently expanded case. Rust checks that required-contract promise
as eligibility. Path then issues contract-bound directives with the expectation
that they can always be honored. A child reporting it cannot comply with a valid
directive is a contract violation; Path must not reconsider selection or restore
rendered-content negotiation in response. Selection does not infer child-private
geometry or reselect based on transient pixel budgets. The historical heading is retained
for reference continuity; the general possibility of slot requirements does not
weaken this slot's specific requirement.

---

# 6. Responsive Child Realization

## 6.1 Responsive Realization Belongs to the Child

Each selected visualizer is responsible for responding gracefully to the spatial budget it receives.

A visualizer may define its own:

- responsive thresholds;
- internal presentation modes;
- slot visibility choices;
- prioritization of semantic content;
- compact controls;
- iconographic or textual substitutions.

DAHN does not require one universal compression-state vocabulary for all visualizers.

## 6.2 Compression Is Not Scaling

Compression MUST NOT be interpreted merely as shrinking a full rendering until it becomes unreadable.

A compressed visualizer should make deliberate semantic choices about what remains perceptible and actionable.

Possible realizations include:

- preserving a Holon's name while suppressing lower-salience detail;
- preserving a type indicator where useful;
- reducing a Person representation to initials;
- reducing a music player to current-item identity plus play/pause;
- preserving only those navigation affordances required by the containing context.

These examples are illustrative, not normative.

## 6.3 Semantic Obligations Survive Compression

Path Inspector delivers dimensions and any explicit V2 presentation request in
one assignment under [§4.4.1](#441-node-inspector-slot-compression-contract).
Recognizable identity and Restore access are unconditional. Other obligations
follow the requested experience; dimensions-only delivery retains the current
presentation. The child realizes these requirements while preserving semantic
and staged state. It cannot suppress a required behavior as a private responsive
choice or infer a new presentation merely from a wider shared track.

## 6.4 Responsive Thresholds Belong to the Visualizer

The visualizer itself is best positioned to know when its current realization no longer works within its assigned budget.

Therefore exact thresholds between its internal responsive modes SHOULD belong to the concrete visualizer rather than to the Path Inspector or Visualizer Selection Service.

---

# 7. Compression and Overflow

## 7.1 Compression Is Allocation Change

Compression changes the external spatial budget assigned by the Path Inspector.

Traversal may deliberately compress the source or contextual rows/columns to help fund the real estate needed by a new target and its labeled traversal channel. Compression remains an allocation change, not a topology change.

It does not inherently:

- change topology;
- discard semantic state;
- change occurrence identity;
- change selected visualizer identity;
- erase provenance.

## 7.2 Independent Axis Compression

Width and height allocations vary independently because they are derived from independent column and row allocations.

Two-axis compression therefore emerges naturally from row/column geometry rather than requiring a combinatorial state model.

## 7.3 Partial and Full Compression

Expanded, contextual and Compact budgets are internal allocation states of this
Path policy. Selected Nodes receive dimensions and an optional explicit V2
presentation request. Their experience does not follow from a track intersection
or nine-state capability table. Topology, allocation, presentation requirements,
and view retain their separate ownership and transitions.

## 7.4 Layout Overflow Versus Off-Viewport

Earlier versions used overflow for contextual rows/columns that could not remain visible in a bounded allocation. With a larger navigation surface, that description conflates two conditions. **Off-viewport** now names geometry lying partially or wholly outside the current view purely because of viewport extent, pan, or zoom. It retains topology, layout, and allocation; it is neither compression nor, by itself, layout overflow.

**Layout overflow** remains available for an explicit allocation policy that cannot include content in a particular layout region and provides an alternate recoverable placement/presentation. It is not inferred from viewport clipping. Existing `overflowed` state that only records clipping must be interpreted as off-viewport; actual overflow policy remains a distinct allocation concern.

Hidden lineage MUST remain directionally discoverable and recoverable in either condition. Panning or Zoom to Fit recovers surface content; layout overflow additionally requires its policy's recovery path.

## 7.5 Branch-Local Overflow

Layout overflow SHOULD apply to the relevant lineage or branch allocation rather than indiscriminately scrolling or displacing unrelated topology.

---

# 8. State Preservation

Compression, layout overflow, off-viewport placement, zoom, scanning, viewport movement, focus changes, local maximization, row/column insertion, traversal-group reflow, and child responsive adaptation MUST NOT inherently discard:

- semantic or staged state;
- occurrence identity;
- provenance;
- selected affordances;
- child links;
- local collection context;
- navigation context;
- selected visualizer identity.

Compression hides or simplifies presentation. It does not destroy semantic or navigation state.

Where practical, restoring an occurrence SHOULD restore its prior useful local context rather than reconstructing it from scratch.

---

# 9. Derived Rather Than Enumerated Interaction

## 9.1 Small Grammar, Large State Space

Keep three independent dimensions: topology (inspection, traversal, branches, collection mediation, closure and context roots), layout/allocation (placement, expanded/partial/full compression, minimum and surface extents), and view (pan, zoom, viewport and attention). Coordinated navigation transitions may change more than one dimension explicitly; a monolithic state machine enumerating their combinations is not the model.

| Transformation | Required distinction |
| --- | --- |
| Compress | Retain topology; reduce allocation/presentation budget. |
| Off-viewport | Retain topology and layout; the current view excludes the occurrence. |
| Close | Remove the occurrence branch, preserving externally owned semantic state. |
| Focus / maximize | Concentrate attention inside parent authority, without inherently changing topology. |
| Re-root | Create a rooted context, preserving the source by default. |

Visualizer-local `maximize-region(occurrence, region)`, Canvas occurrence focus, and Window/context maximize follow the distinct authority levels in the [DAHN composition contract](../../../../dahn-design-spec.md#30-parent-owned-allocation).

The Path Inspector may produce a large number of visible configurations, but those configurations SHOULD be generated from a small set of rules rather than explicitly enumerated.

The principal inputs are:

- navigation topology;
- traversal provenance;
- focus;
- view position and scale;
- available Path Inspector allocation.

The principal derivations are:

- sparse grid topology;
- vertical-path column placement;
- horizontal-path row placement;
- traversal-group ordering and reflow;
- traversal-channel geometry and labels;
- column widths;
- row heights;
- cell spatial budgets;
- semantic presentation obligations.

Layout derivation excludes view position and scale; those determine only the visible projection of the resulting surface. The selected children then independently derive their responsive realization from their allocation and obligations, not from zoom scale.

## 9.2 Mockups as Conformance Examples

Existing Path Inspector mockups showing combinations of:

- fully expanded cells;
- horizontal compression;
- vertical compression;
- two-axis compression;
- retained navigation surfaces;

SHOULD be interpreted as examples against which the grammar can be tested.

They SHOULD NOT automatically become separately encoded Path Inspector states.

A useful conformance test is:

> Given this retained navigation topology, this focus, and this available Path Inspector allocation, do the grammar rules derive geometry consistent with the mockup?

A separate child-visualizer test is:

> Given this spatial budget and these semantic presentation obligations, does the selected visualizer produce an acceptable responsive realization?

## 9.3 Unmocked Paths Must Remain Coherent

The grammar is successful when navigation paths not explicitly represented in the mockups still produce semantically truthful and spatially coherent projections.

The Path Inspector should not require special-case layout code for each possible sequence of horizontal and vertical traversal.

---

# 10. Grammar Invariants

The Path Inspector MUST preserve these invariants:

1. The rooted navigation topology persists independently of its current spatial projection and viewport.
2. Holon identity, occurrence identity, and grid position remain distinct.
3. Single-valued traversal extends horizontally.
4. Collection-mediated traversal extends vertically.
5. Each column preserves one vertical traversal path.
6. Each row preserves one horizontal traversal path.
7. First-time rightward destination placement inserts a whole column right of its source, shifting existing columns across every row.
8. First-time downward destination placement inserts a whole row below its source stage, shifting existing rows across every column.
9. Descendants remain attached to the occurrences that produced them and move with those occurrences during reflow.
10. An untraversed leaf may be replaced by another selection from the same anchor.
11. Once navigation continues through an occurrence, that occurrence and its continuation become retained navigation history.
12. Equivalent traversal provenance groups retained siblings semantically, without requiring spatial contiguity or a first-member position; matching label text alone is insufficient.
13. A new horizontal destination takes the source-adjacent cell; an explored outgoing continuation moves downward intact.
14. A new vertical destination takes the source-adjacent cell; an explored outgoing continuation moves rightward intact.
15. Source-driven retained-target reactivation promotes/reuses that branch and exchanges branch positions when the outgoing branch is explored; direct Restore leaves logical placement unchanged. Preserve identity, provenance, chronological history and descendant attachment.
16. Sparse cells are valid when required to preserve truthful horizontal and vertical traversal paths.
17. The viewport may move over the grid; focus is not anchored to a fixed row or column.
18. Branch insertion and reflow do not alter semantic parentage merely because rows or columns move.
19. Every occupied cell receives the width of its column and the height of its row.
20. Horizontal compression or expansion transforms a whole column; vertical compression or expansion transforms a whole row.
21. Traversal channels are Path Inspector geometry and MUST provide sufficient room for directional connectors and legible subordinate traversal labels.
22. Sibling connectors from the same source with equivalent traversal provenance may share a label and qualifier presentation only when the shared meaning remains unambiguous.
23. Traversal real estate SHOULD be obtained jointly through source/context compression and channel allocation; labeled channels do not replace existing compression semantics.
24. The Path Inspector owns grid geometry, traversal-group reflow, traversal channels, connector routing, viewport projection, and child external allocation.
25. Selected children own their internal responsive realization.
26. Semantic presentation obligations may cross the parent-child boundary; implementation-specific layout directives should not.
27. Spatial size is not, by default, a Visualizer Selection Service criterion.
28. Compression changes allocation and presentation, not semantic identity or topology.
29. Layout overflow, compression, and off-viewport placement are distinct; hidden lineage remains discoverable.
30. The same grammar must produce coherent behavior for navigation paths that have not been explicitly mocked up.
31. Pan, zoom, and Zoom to Fit preserve layout and allocation; a Visualizer at 50% zoom is not compressed.
32. Surface growth preserves the minimum useful uncompressed extent of an open Holon Inspector.
33. Close removes only the selected occurrence branch, never externally owned staged state.
34. Re-root requests another context and preserves source topology by default; roots are contextual.
35. Directional lineage connectors expose recorded occurrence parentage and traversal provenance; the primary label names the relationship predicate for Expand or the Dance name for navigational Dance, while compact qualifiers such as a funnel may signal an optional Predicate. Displacement, compression, group reflow, and viewport movement change routing without changing attachment.
36. A Predicate-qualified relationship expansion remains an expansion of that relationship; its Predicate constrains traversal results and MUST NOT be represented as a new semantic relationship.
37. A navigational Dance traversal records and labels the Dance that produced the target; the grammar MUST NOT fabricate a relationship predicate for a Dance-derived result.
38. Traversal labels and qualifiers are compact projections of provenance; visible text or iconography MUST NOT replace the underlying recorded traversal provenance as the source of truth.
39. New-destination insertion displaces history outward. Explicit retained-target reactivation may promote/exchange branches, and Close may reclaim empty bands; neither is ordinary new-destination insertion.
40. The pending destination occupies its final source-adjacent cell after required band insertion/displacement, before content resolves; materialization does not move it to a terminal group position.
41. Displacement preserves existing column widths, row heights and inter-band channel dimensions independently of explicit allocation changes. Compression preserves topology and provenance and cannot justify inward reflow.

---

# 11. Relationship to Space Navigator

The Path Inspector is not the Space Navigator.

**Space Navigator** is a Dancer that composes capabilities into a coherent experience.

Within that experience, Space Navigator defines a **RootedNavigation** visualizer
slot initially rooted at its local HolonSpace. The following composition is an
illustration using Path Inspector, not a mandatory Dancer implementation.

Conceptually:

    SpaceNavigator Dancer
        ->
    RootedNavigation slot
        subject/root = active HolonSpace or explicit new-context anchor
        ->
    Visualizer Selection Service
        ->
    PathInspector
        ->
    Node visualizer slots
        ->
    Visualizer Selection Service
        ->
    applicable Node visualizers

The reusable composition, Window Manager, slot participation, and view-transform obligations are defined by the [DAHN composition contract](../../../../dahn-design-spec.md#29-canvas-dancer-and-rooted-navigation-responsibilities). The Path Inspector grammar therefore belongs to the selected RootedNavigation visualizer, not to the Space Navigator Dancer itself. This document is the normative source for the rooted-navigation topology, grid, viewport, traversal, insertion, compression, and overflow semantics used by Path Inspector.

Another Dancer could use the same Path Inspector with a different root or surrounding experience.

---

# 12. Relationship to Visualizer Selection

The Visualizer Selection Service selects a visualizer that satisfies the semantic contract of a slot.

For Path Inspector child Node slots, selection may consider:

- required Visualizer Kind;
- subject type and type lineage;
- slot semantic capability requirements;
- theme or available Visualizer population;
- specialization and preference policy.

The Path Inspector SHOULD NOT require selection to consider the current pixel width or height of the cell.

After selection, the Path Inspector may repeatedly change the child's spatial budget as focus and projection change. The selected child is responsible for adapting.

This boundary deliberately leaves room for future experimentation. If usage demonstrates that spatial constraints must participate in selection, that can be introduced explicitly rather than being assumed by the initial grammar.

---

# 13. Relationship to Adjacent Specifications

DAHN Architecture defines:

- Dancer versus Visualizer responsibility;
- Visualizer Kind and Subkind;
- slot and selection mechanisms;
- occurrence identity;
- recursive spatial allocation;
- theme ownership;
- Rust/TypeScript responsibility boundaries.

This interaction grammar defines the spatial and topological behavior of the concrete **Path Inspector**, a **Structure / RootedNavigation** visualizer.

The [Path Inspector Design Specification](design-spec.md) defines concrete interactions that invoke this grammar, including:

- which Node affordances invoke horizontal traversal;
- which collection interactions invoke vertical traversal;
- focus transitions;
- scanning and restoration controls;
- hidden-lineage recovery;
- concrete Path Inspector allocation policies.

Concrete Node visualizer specifications, such as HolonInspector, should independently define how those visualizers respond to:

- assigned spatial budgets;
- semantic presentation obligations;
- their own internal slots and layout;
- their own responsive thresholds.

The Implementation Plan sequences those requirements into deliverable increments. It MUST NOT introduce alternate topology, provenance, compression, or allocation semantics.

---

# 14. Intentionally Deferred Decisions

This grammar deliberately does not prescribe:

- exact expanded, partial, or fully compressed pixel dimensions;
- future replacements for the specified fixed-reference common-factor allocation policy;
- future alternatives to the currently specified discrete Node-slot compression protocol;
- animation;
- exact controls for hidden lineage, pan/zoom, Zoom to Fit, and focus/actual-size;
- exact child visualizer responsive thresholds;
- exact compact representations;
- exact traversal-label typography and connector styling;
- a universal DAHN compression-state vocabulary;
- persistence of Path Inspector sessions;
- sibling-history retention beyond the topology invariants;
- advanced adaptive allocation based on salience or learned behavior;
- exact traversal-qualifier iconography and styling;
- interaction for inspecting the full Predicate, its Filters, Dance parameters, or other detailed traversal provenance;
- additional future traversal-operation kinds and their compact label conventions.

These decisions can evolve through implementation and usage without changing the core grammar.

---

# 15. Summary

The Path Inspector is a concrete **Structure / RootedNavigation** visualizer that turns an interaction-derived navigation topology into a persistent two-dimensional grid viewed through a bounded, movable viewport.

Its central navigation rule is:

> **Follow one thing horizontally; choose among many things vertically.**

Its central topology rule is:

> **Navigation provenance persists independently of the current projection.**

Its central projection rule is:

> **Each column preserves a vertical traversal path; each row preserves a horizontal traversal path; group anchors, outward reflow and sparse cells keep both path systems truthful without pulling retained history toward the upper-left.**

Its central traversal-group rule is:

> **Traversal provenance groups history; new destinations take source-adjacent cells. First-time placement inserts whole bands, retained-target selection promotes/exchanges branches, and direct Restore preserves placement.**

Its central lineage-presentation rule is:

> **Traversal channels make provenance legible: connectors name the operation that produced the traversal, compact qualifiers signal additional constraints, and equivalent traversals may share a label.**

Its central traversal-presentation rule is:

> **A relationship Expand is labeled by its relationship predicate; a Predicate-qualified Expand may add a filter qualifier; a navigational Dance is labeled by its Dance name.**

Its central allocation rule is:

> **Column width, row height, traversal-channel geometry, and source/context compression are coordinated Path Inspector decisions; row/column intersection remains the spatial budget of each child cell.**

Its central composition rule is:

> **Parent visualizers own inter-child geometry. Child visualizers own intra-child adaptation.**

Its central responsive rule is:

> **Compression is a smaller semantic presentation budget, not merely a scaled-down rendering.**

Its central selection rule is:

> **Select for semantic applicability; adapt the selected visualizer to changing spatial budgets.**

Together, these rules allow a small grammar to generate a wide range of coherent navigation paths without enumerating every visible configuration as a separate state. Existing mockups become conformance examples of the grammar rather than the definition of its complete state space.


Internal property and collection allocation belongs to the selected Node; see [Holon Inspector responsive composition](../../../node/holon-inspector/design-spec.md#44-responsive-internal-allocation).
