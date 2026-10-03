# DAHN Path Inspector Interaction Grammar

**Version:** 0.11

## Change Log

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

Each new vertical group anchor uses the source column and moves older groups rightward. Later members append rightward within their traversal group; later groups may move rightward as units. Connector geometry preserves the source-axis attachment of displaced groups.

Every cell in a column receives the same current width budget.

## 1.10 Row

A **row** is a horizontal grid band that preserves one horizontal traversal path.

Each new horizontal group anchor uses the source row and moves older groups downward. Later members append downward within their traversal group; later groups may move downward as units. Connector geometry preserves the source-axis attachment of displaced groups.

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

For horizontal traversal, members of a traversal group occupy contiguous rows at the target side of the source. For vertical traversal, members occupy contiguous columns beneath the source stage.

Group membership derives from the recorded traversal operation and its semantically relevant qualifiers, not from semantic target identity, visual adjacency, or primary label text alone. In particular, an unfiltered expansion and a Predicate-qualified expansion MUST NOT be merged solely because they expand the same relationship, and distinct Dance traversals MUST NOT be merged solely because their rendered labels happen to match.

Within a group, retained members preserve insertion order. The **group anchor** is its first retained member and source-axis connector attachment. **Terminal insertion** appends a new retained member at the bottom-most edge of a horizontal group or right-most edge of a vertical group, including the space needed by retained descendant branches.

The **canonical traversal position** is the source-aligned cell immediately right of the source or below the source stage. Each new group takes that cell and displaces older groups outward, preserving their relative order. Subsequent members append within their existing group; they do not promote it. Growth of a spatially earlier group may displace later anchors outward without changing their provenance or relative order.

**Outward reflow** displaces retained branches down and/or right. **Monotonic expansion** means topology-producing traversal never moves retained occurrences up or left to accommodate newer navigation. It is a layout invariant; explicit close compaction and view transformations are separate operations.

## 1.17 Traversal Channel

A **traversal channel** is the inter-child spatial region through which a lineage connector runs between a source and its target or target group.

The channel is Path Inspector geometry. It may be wider or taller than a minimal grid gap so that the connector, its traversal label, and any compact qualifier remain legible. Channel allocation is coordinated with row/column allocation and compression; it is not a child-owned region or an independent semantic occurrence.

---

# 2. Topology Production Rules

## 2.1 Inspect

`inspect(holon)` creates or activates a Node occurrence for that Holon in the current topology.

The root inspection establishes the initial focus.

## 2.2 Horizontal Traversal

`traverse-right(occurrence, singular-affordance)` creates or activates a child Node occurrence to the right of its source, using the canonical position for a new group anchor or the derived outward group position under §2.4.

The affordance must be structurally singular. Runtime population does not alter its axis: an empty singular relationship remains singular.

The new child becomes the focus unless the invoking interaction explicitly specifies otherwise.

## 2.3 Vertical Traversal

`traverse-down(occurrence, plural-affordance, member)` exposes or activates the Collection occurrence associated with a structurally plural affordance and creates or activates the selected member's child Node below the source stage, using the canonical position for a new group anchor or the derived outward group position under §2.4.

The Collection remains the semantic mediator for sibling scanning.

Runtime population does not alter the axis: an empty or one-member plural relationship remains plural.

The selected child becomes the focus unless the invoking interaction explicitly specifies otherwise.

## 2.4 Branch and Retained Alternative Insertion

`branch(anchor, continuation)` retains an additional continuation from an existing anchor when the continuation currently selected from that anchor has already been traversed onward.

An untraversed leaf MAY be replaced by another selection from the same anchor. Once navigation has continued through that child, the occurrence and its continuation are retained history and MUST NOT be overwritten.

Retained alternatives satisfy **monotonic expansion**, **traversal-group ordering**, and **terminal insertion**:

- a new horizontal group anchor takes the canonical right-hand, source-row cell and shifts older groups downward;
- a new vertical group anchor takes the canonical lower, source-column cell and shifts older groups rightward;
- older groups preserve their relative spatial order when a new group is inserted before them;
- equivalent traversal provenance groups sibling targets from the same source; visible label text is not grouping identity;
- a new member of an existing horizontal group appends below its existing members and retained branch footprint;
- a new member of an existing vertical group appends to the right of its existing members and retained branch footprint;
- earlier same-group members remain in place when a member appends; later groups move down/right only as needed to make room;
- every displaced branch carries its descendants, preserving its internal geometry where possible, identity, insertion order and attachment.

Topology-producing traversal MUST NOT move retained occurrences or branches upward or left solely to accommodate newer navigation. Mixed-axis collision resolution also proceeds outward; it must not use a later coordinate normalization to hide an inward move. Sparse cells and surface growth are preferable to false lineage or inward repacking.

The first occurrence inserts a group nearest the source axis; older groups retain their relative order. Here, “later groups” means spatially later, not more recently opened. Later members join that group instead of appearing after unrelated groups. Restoring an existing occurrence does not append or reorder it. Connector geometry preserves source attachment even when a later member or group anchor is not directly source-axis aligned.

> **Replace an eligible leaf; otherwise retain the group anchor, append at the group's outward terminal edge, and move later branches only down/right.**

## 2.5 Scan

`scan(lineage, direction, focus)` changes the focus-dependent projection of an existing lineage.

Scanning does not:

- replace the topology;
- reinterpret prior occurrences as children of the newly focused occurrence;
- discard sibling context;
- change semantic provenance.

## 2.6 Restore

`restore(occurrence)` moves focus or allocation toward a previously compressed, layout-overflowed, or off-viewport occurrence and returns it to a more useful visible extent while retaining prior local state where feasible. Merely recovering an off-viewport occurrence requires a view change, not an allocation change.

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

1. apply the appropriate traversal and retention rules and derive the final destination: the canonical cell for a new group anchor, or the outward group/terminal position for retained alternatives;
2. establish destination real estate through source/context compression, traversal-channel allocation, and pan/reflow
   as required by the existing focus-dependent allocation rules;
3. occupy that real estate with a pending destination presentation;
4. replace the pending presentation with resolved content in-place.

For a fully expanded source followed horizontally, partial compression and the
opening of the derived right-hand destination MUST be perceptible before content
appears. A later group member is reserved at its final terminal position, never
first shown on the source row and then relocated. The vertical rule is symmetric.
This ordering preserves group attachment and does not override monotonic expansion.

Opening a relationship collection similarly establishes its region beneath the
source before presenting its contents. Switching collections in an already-open
region MUST retain that region and transition its contents in-place. This reuse
does not discard traversed occurrences or their descendants: existing retention
and stable-attachment rules still apply. Selecting a member remains a separate
vertical traversal and uses the same destination-first ordering for its Node.

An explicit edit or inspection interaction MAY expose an empty collection;
normal relationship browsing MUST NOT allocate a region solely to show emptiness.
Transitions MUST preserve spatial continuity. Reduced-motion presentation may
omit motion but MUST preserve destination ordering and localized pending feedback.
Concrete messages and discovery states are defined in the design specification.

After deriving final destination geometry and applying contextual allocation, the Path Inspector MUST adjust the viewport within surface bounds to reveal the active destination and its immediate source context before presenting pending destination content. Materialization fills that same region; once the selected target reports its useful extent, the viewport follows that final extent without moving the target to a temporary cell or resizing the experience.

---

## 2.9 Close Branch

`close(occurrence)` removes that occurrence and all its descendant occurrences from this topology. It MUST preserve shared ancestors and unrelated branches, including other occurrences of the same semantic Holon. For `A -> B -> C -> D`, closing C leaves `A -> B`; if B also has `E -> F`, that branch remains intact.

In collection-mediated navigation, closing a descendant removes only its lineage; closing the Collection occurrence removes the exploration descended through it. Removal follows recorded occurrence parentage, not grid adjacency or semantic identity. Closing the root leaves an empty navigation topology; it does not itself destroy the top-level context.

If focus was removed, the nearest surviving ancestor becomes navigation focus, or focus is cleared if none survives. Layout may reclaim vacated space without rewriting remaining provenance. When a horizontal child branch closes, surviving sibling branches compact into the vacated space while retaining traversal-group contiguity, group order, sibling insertion order, and each branch's internal geometry. The symmetric rule applies to vertical sibling groups. This includes promoting a surviving alternative into a vacant canonical child position beside or beneath the parent when consistent with group-anchor attachment and group-order rules; removing wholly empty global rows or columns alone is insufficient. Compaction MUST avoid occupied cells of unrelated branches and preserve pending destinations attached to surviving branches. This explicit close compaction is distinct from topology-producing traversal and may reclaim space toward the origin; monotonic expansion does not redesign close semantics. Closing MUST NOT discard externally owned staged edits, Nursery state, transaction participation, or Undo history. Occurrence-local presentation may be released; semantic disposal requires a separate operation by its owner.

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

When the occurrence currently selected from an anchor has not itself been traversed onward, another selection from that same anchor MAY replace it in its established traversal position, subject to group ordering.

Changing collection tabs or the collection being viewed inside a Node visualizer is local child state and does not itself extend Path Inspector topology. Selecting a collection member creates or activates a vertical child occurrence.

Once navigation continues through a child occurrence, that child becomes part of retained navigation history and MUST NOT be overwritten by a later alternative selection from the same anchor.

## 3.4 Vertical Alternative Insertion and Grouping

Vertical traversal opens below the source stage. A new group anchor occupies the canonical position in the source column and displaces older groups rightward. Subsequent members of equivalent traversal provenance append at that group's right-most terminal edge; they do not take ownership of the source column.

For an existing group:

1. retain the anchor and earlier members in their existing columns;
2. derive the new member's position just beyond the group's retained branch footprint;
3. shift later groups rightward as units only where necessary;
4. move retained descendants with each displaced branch root; and
5. establish the final destination before showing pending content there.

For a new group, insert its anchor at the canonical cell and move older groups outward, preserving their relative order. Repeated traversal does not reorder groups. Mixed-axis collisions may require additional outward reflow, never leftward/upward displacement. The Collection remains the semantic mediator regardless of whether the selected member is directly source-column aligned.

## 3.5 Horizontal Alternative Insertion and Grouping

Horizontal traversal opens to the right of the source. A new group anchor occupies the canonical position in the source row and displaces older groups downward. Subsequent members of equivalent traversal provenance append at that group's bottom-most terminal edge; they do not take ownership of the source row.

For an existing group:

1. retain the anchor and earlier members in their existing rows;
2. derive the new member's position just beyond the group's retained branch footprint;
3. shift later groups downward as units only where necessary;
4. move retained descendants with each displaced branch root; and
5. establish the final destination before showing pending content there.

For a new group, insert its anchor at the canonical cell and move older groups outward, preserving their relative order. Repeated traversal does not reorder groups. Mixed-axis collisions may require additional outward reflow, never upward/leftward displacement.

Given `H1 --R1--> H1.1 --R2--> X` followed by `H1 --R3--> H1.2 --Rn--> Y`, a later `H1 --R1--> H1.3` produces:

                 R3
    H1 ----------+----> H1.2 ----Rn----> Y

                 R1
                 +----> H1.1 ----R2----> X
                 +----> H1.3

Opening R3 placed H1.2 on H1's row and moved the older R1 branch downward. Repeating R1 leaves H1.1 in that displaced anchor row and appends H1.3 below its retained footprint. R3 stays in place above R1. A subsequent retained R3 member appends below H1.2 and pushes the entire R1 group downward as necessary, including X and H1.3. No traversal moves any retained occurrence upward or left. The vertical counterpart inserts new groups at the source column and appends repeated members rightward.

> **The first member anchors its traversal group; later members append at its outward terminal edge. Horizontal sibling groups consume rows; vertical sibling groups consume columns.**

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

Topology-producing reflow MUST be monotonic down/right. Earlier groups are never pulled up/left when a later group changes. Traversal groups MUST remain contiguous after reflow. Descendant branches move with their displaced root occurrence; they MUST NOT be detached or independently compacted merely to reduce movement.

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

For a group anchor in the canonical source-aligned position, the connector SHOULD use the most direct orthogonal segment available. Later group members and displaced group anchors use branching or elbow routing through the traversal channel; direct source-axis alignment is not required for every member. Source, target, direction, group attachment, and label association MUST remain unambiguous.

Traversal-group growth moves later horizontal groups downward or later vertical groups rightward. It MUST NOT move retained members upward or left to make room for the newest target. Its connector remains attached to the original source and target occurrence and is rerouted through the traversal channel. Displacement changes routing, not recorded traversal direction, provenance, or source.

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

The Node Inspector slot offers three independent vertical states (`full-height`,
`partial-height`, `minimal-height`) and three horizontal states (`full-width`,
`partial-width`, `minimal-width`). These are slot participation states, not a
universal vocabulary imposed on every DAHN visualizer.

A conforming selected visualizer MUST report useful unscaled extents for each
axis state and accept the allocated dimensions together with both selected
states. Extents MUST be positive and ordered minimal <= partial <= full. The
Path Inspector chooses states for whole rows and columns, allocates the maximum
reported extent required by participating cells, and delivers each cell's two
states and budget. It MUST NOT inspect child DOM or know child sub-slot names to
make those decisions. Pending/error presentations use the same slot geometry.

Full extents are stable content allocations, not the viewport's remaining space.
Ordinary traversal MUST apply discrete contextual compression, allocate legible traversal channels, and extend the surface by the resulting band extents and gaps. Adding context MUST NOT shrink the active target below its useful expanded extent merely to preserve distant provenance.

Traversal coordinates topology, allocation and view as distinct operations. Once final destination geometry is established, the viewport follows the active inspector within the real surface bounds. “Center of attention” does not require literal centering: the view MUST NOT add leading padding, translate retained geometry, or move a first-column inspector away from the left edge to center it. When the immediate source and target composition fits, retain both in view using the smallest necessary scroll. A vertical traversal therefore preserves horizontal alignment; the orthogonal rule applies to horizontal traversal. Earlier, more distant history may scroll above or to the left. View movement MUST NOT change topology, retained geometry, group ordering or band dimensions.

The initial usable Actual Size allocation SHOULD simultaneously support:

- width >= partial source width + horizontal traversal-channel width + full target useful width;
- height >= partial source height + vertical traversal-channel height + full target useful height.

Derive these dimensions from the selected participants' extent contracts, not a percentage of the available viewport. For the Holon Inspector, downward compression retains its title bar, collection tabs, and Collection Viewer; it suppresses the actions/properties body. The Collection Viewer allocation includes its controls, column header, and five data rows. Additional rows scroll within that allocation. Compression MUST preserve this collection allocation.

Initial total height is the Path Actions Bar plus the retained source title/tabs/Collection Viewer, the vertical channel, and the full target (title, actions/properties body, tabs and Collection Viewer), including all framing and gaps. Initial width includes one compressed vertical source rail, one horizontal channel and one full target, plus framing. Reserve collection space even before a collection is selected. After reserving both title/tabs/five-row collection allocations and the channel, the actions/properties body receives the remaining initial usable height, up to its normal preferred height. Freeze that body grant for ordinary traversal; properties scroll internally. Title tracks MUST remain intrinsic and MUST NOT absorb surplus band height. The selected Collection owns its measured five-row report; the Holon Inspector adds its own regions and chrome, and the Path Inspector consumes only Node extents. Before a selected Collection reports, use a theme-derived initial estimate rather than an available-space cap. Materialized participants may refine their measured extents.

Each immediate composition owner adds its own framing, scrollbars, tabs or toolbar; Canvas and enclosing experience chrome are accounted for outside the usable Path Inspector viewport. The application/window owner honors the composed initial report. Path Inspector MUST NOT imperatively resize its parent window. Ordinary traversal MUST NOT trigger experience resizing; the basic first traversal requires at most view movement.

A physically constrained display or externally allocated embedding may prevent the full two-stage composition from fitting. Preserve the active target's useful allocation, show as much immediate context as possible, and retain pan and Zoom to Fit for recovery. Do not silently shrink the active Node or alter topology to fit. Deep navigation may move distant history wholly off-viewport; initial allocation need not fit an unbounded path. Explicit pan, zoom, restoration and actual-size recovery remain available.

The selected visualizer exclusively owns sub-region and sub-slot allocation for
all nine axis combinations. Path Inspector supplies participation states and
budgets; it must not implement child-private region retention or suppression.
For the current Holon Inspector realization, see its
[responsive composition](../../../node/holon-inspector/design-spec.md#responsive-realization-under-path-inspector).

### PropertyMap sub-slot content extent

This is a Holon Inspector child-composition concern. Its authoritative contract
is [PropertyMap content extent](../../../node/holon-inspector/design-spec.md#propertymap-sub-slot-content-extent),
not a Path Inspector requirement on a Node's private sub-slots.

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

An uncompressed child MAY declare or negotiate a minimum useful extent. An open Holon Inspector MUST NOT be forced below that extent solely because the viewport is exhausted. Existing context may be compressed under the established whole-row/whole-column rules; when required geometry exceeds the viewport, the Navigation Surface grows and pan/scroll makes the remaining geometry reachable. Minimum useful extents constrain the row/column budget; they do not authorize a child to seize parent space. No pixel threshold is normative here.

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

Although pixel dimensions do not ordinarily participate in selection, a slot MAY require semantic capabilities needed by the containing visualizer.

For example, a Path Inspector Node slot may require that a selected Node visualizer be capable of preserving:

- recognizable occurrence identity;
- required navigation affordances;
- recoverability under contextual presentation.

The Visualizer Selection Service may use such semantic requirements as applicability constraints.

It SHOULD NOT select based on assumptions about a particular child implementation's internal geometry.

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

The Path Inspector may accompany a reduced spatial budget with semantic presentation obligations appropriate to the occurrence's role.

For a contextual Node occurrence these may include:

- preserve recognizable identity;
- preserve singular-navigation capability;
- preserve evidence of staged state where applicable;
- remain recoverable.

The child determines how those obligations are realized.

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

The Path Inspector MAY use categories such as partially compressed and fully compressed when useful for its own allocation policy.

Those categories describe Path Inspector allocation policy, not universal child visualizer states.

A child remains free to define its own responsive realization for the actual budget received.

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
7. A new horizontal group anchor takes the canonical right-hand cell in the source row and shifts older groups downward while preserving their relative order.
8. A new vertical group anchor takes the canonical lower cell in the source column and shifts older groups rightward while preserving their relative order.
9. Descendants remain attached to the occurrences that produced them and move with those occurrences during reflow.
10. An untraversed leaf may be replaced by another selection from the same anchor.
11. Once navigation continues through an occurrence, that occurrence and its continuation become retained navigation history.
12. Retained sibling targets from the same source and equivalent traversal provenance form a contiguous traversal group; matching primary label text alone is insufficient.
13. A new retained horizontal member appends at the bottom of its traversal group. Earlier same-group members stay in place; later groups may move downward.
14. A new retained vertical member appends at the right edge of its traversal group. Earlier same-group members stay in place; later groups may move rightward.
15. Traversal-group reflow may change grid coordinates but MUST NOT change occurrence identity, traversal provenance, group membership, insertion order within a group, or descendant attachment.
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
39. Topology-producing traversal MUST NOT move retained occurrences or branches upward or left solely to accommodate newer navigation; reflow proceeds downward and/or rightward.
40. The pending destination occupies the final derived canonical or terminal group position before content is resolved; it never appears source-aligned merely to move to a terminal position afterward.
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
- exact row-height, column-width, or traversal-channel dimension functions;
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

> **Retained siblings are grouped by equivalent traversal provenance; the first member anchors each group and subsequent members append at its outward terminal edge. Later groups move only down/right as space is required.**

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


Collection-viewer space is lent to the Properties body while no collection is open; collection tabs remain visible. Opening a collection transfers its five-row viewer allocation from Properties within the stable full Inspector height. It does not resize that Inspector merely because a measured Collection height replaces an estimate. Properties remain scrollable and show a visible directional overflow cue independently of operating-system scrollbar visibility. The Properties maximize control uses a compact icon row.
