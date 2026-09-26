# DAHN Path Inspector Interaction Grammar

**Version:** 0.3

## Change Log

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

This document sits between DAHN Architecture and the concrete design and implementation specifications that realize the Path Inspector:

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

Architecture defines the available mechanisms and their ownership. This grammar defines valid topology production, focus-dependent projection, spatial allocation, compression, and responsive child composition using those mechanisms.

This document is normative for:

- Path Inspector navigation topology;
- occurrence identity, provenance, and directional lineage connectors;
- horizontal and vertical traversal semantics;
- sparse row/column projection;
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

An occurrence remains in the topology until an explicit branch-closing or re-rooting operation removes it from the current Path Inspector context.

## 1.2 Root

The **root** is the initial semantic Holon from which the current rooted navigation topology unfolds.

The Path Inspector can in principle be rooted at any Holon. A containing Dancer such as Space Navigator may choose a HolonSpace as its root, but HolonSpace is not intrinsic to the RootedNavigation grammar.

## 1.3 Occurrence

An **occurrence** is one appearance of a semantic subject within the rooted navigation topology.

A semantic Holon may appear in more than one occurrence when reached through different navigation paths. Each occurrence retains its own provenance and presentation context.

Holon identity and occurrence identity are therefore distinct.

## 1.4 Focus

The **focus** is the occurrence at the active navigation frontier.

Focus influences viewport position and the spatial allocation of rows and columns. It does not alter topology or reattach descendants. Focus is not permanently associated with any particular row or column.

## 1.5 Viewport

The **viewport** is the bounded visible region through which the Path Inspector presents part of its potentially larger two-dimensional grid.

The viewport may move horizontally and vertically over the grid as focus changes or the user scans retained navigation context. Moving the viewport does not re-root the Path Inspector, renumber occurrence identity, or rewrite traversal provenance.

The grid persists independently of the viewport:

> **The grid retains navigation structure; the viewport moves over it.**

## 1.6 Navigation Topology Versus Spatial Projection

The navigation topology records what has been unfolded and how occurrences are related.

The **spatial projection** is the current bounded realization of that topology around the focus.

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

Occurrences connected by retained vertical traversal remain in the same column unless branching requires the prior traversed path to be displaced into a newly inserted column.

Every cell in a column receives the same current width budget.

## 1.10 Row

A **row** is a horizontal grid band that preserves one horizontal traversal path.

Occurrences connected by retained horizontal traversal remain in the same row unless branching requires the prior traversed path to be displaced into a newly inserted row.

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

---

# 2. Topology Production Rules

## 2.1 Inspect

`inspect(holon)` creates or activates a Node occurrence for that Holon in the current topology.

The root inspection establishes the initial focus.

## 2.2 Horizontal Traversal

`traverse-right(occurrence, singular-affordance)` creates or activates a child Node occurrence horizontally adjacent to the navigation stage containing its source occurrence.

The affordance must be structurally singular. Runtime population does not alter its axis: an empty singular relationship remains singular.

The new child becomes the focus unless the invoking interaction explicitly specifies otherwise.

## 2.3 Vertical Traversal

`traverse-down(occurrence, plural-affordance, member)` exposes or activates the Collection occurrence associated with a structurally plural affordance and creates or activates the selected member's child Node below it.

The Collection remains the semantic mediator for sibling scanning.

Runtime population does not alter the axis: an empty or one-member plural relationship remains plural.

The selected child becomes the focus unless the invoking interaction explicitly specifies otherwise.

## 2.4 Branch

`branch(anchor, continuation)` retains an additional continuation from an existing anchor when the continuation currently occupying the canonical traversal position has already been traversed onward.

A child occurrence that remains an untraversed leaf MAY be replaced by another selection from the same anchor. Once navigation has continued through that child, the occurrence and its continuation are retained history and MUST NOT be overwritten.

When an alternative must coexist with a retained continuation:

- a **vertical** alternative remains on the anchor's current column, while the previously traversed vertical continuation is displaced into a newly inserted column to the right;
- a **horizontal** alternative remains on the anchor's current row, while the previously traversed horizontal continuation is displaced into a newly inserted row below.

Existing continuations remain attached to the occurrences that produced them. Branching MUST NOT reconstruct retained navigation as a misleading linear page history merely to make the layout denser.

> **Replace an untraversed leaf; displace and retain a traversed path.**

## 2.5 Scan

`scan(lineage, direction, focus)` changes the focus-dependent projection of an existing lineage.

Scanning does not:

- replace the topology;
- reinterpret prior occurrences as children of the newly focused occurrence;
- discard sibling context;
- change semantic provenance.

## 2.6 Restore

`restore(occurrence)` moves focus or allocation toward a previously compressed or overflowed occurrence and returns it to a more useful visible extent while retaining prior local state where feasible.

## 2.7 Re-root

`re-root(occurrence)` establishes that occurrence's semantic Holon as the new root and discards prior topology from the current Path Inspector context.

> **Traversal extends topology. Re-rooting replaces retained rooted context.**

---

## 2.8 Destination-First Transitions

Relationship navigation MUST establish that a destination exists before changing
focus, compressing the source, replacing a leaf, inserting a branch, or allocating
a destination. Verified zero targets produce local feedback without structural
navigation. Unknown or failed inspection is not evidence of emptiness. A singular
relationship with multiple targets follows existing cardinality validation/error
semantics; it MUST NOT silently become plural or choose an arbitrary target.

After existence is established, the spatial sequence MUST be:

1. apply the appropriate traversal and retention rules;
2. establish destination real estate through source compression and pan/reflow
   as required by the existing focus-dependent allocation rules;
3. occupy that real estate with a pending destination presentation;
4. replace the pending presentation with resolved content in-place.

For a fully expanded source followed horizontally, partial compression and the
opening of the right-hand destination MUST be perceptible before destination
content appears. The destination remains in the source's horizontal lineage;
this ordering does not override grid insertion or retained-path rules.

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

When the occurrence currently selected from an anchor has not itself been traversed onward, another selection from that same anchor MAY replace it in the same canonical traversal position.

Changing collection tabs or the collection being viewed inside a Node visualizer is local child state and does not itself extend Path Inspector topology. Selecting a collection member creates or activates a vertical child occurrence.

Once navigation continues through a child occurrence, that child becomes part of retained navigation history and MUST NOT be overwritten by a later alternative selection from the same anchor.

## 3.4 Vertical Alternative Insertion

A vertical traversal continues in the anchor's current column.

If the canonical vertical child position contains an untraversed leaf, a new member selection MAY replace that leaf.

If the prior vertical child has been traversed onward, the newly selected occurrence remains in the anchor's column. The previously traversed vertical continuation is displaced one column to the right. A new column is inserted for that retained path, and pre-existing columns to its right shift right as necessary.

For example:

    before:

            C1      C2      C3

    R1      H1      A       B
    R2      H2      C       D
    R3      H3      E       F

    select new collection member H4 from H1:

            C1      C2      C3      C4

    R1      H1              A       B
    R2      H4      H2      C       D
    R3              H3      E       F

The new `H1 -> H4` vertical continuation remains in C1. The retained `H2 -> H3` vertical path moves to C2. The former C2 and C3 shift to C3 and C4.

The current column focus is not changed merely because this insertion occurs.

## 3.5 Horizontal Alternative Insertion

A horizontal traversal continues in the anchor's current row.

If the canonical horizontal child position contains an untraversed leaf, a new singular selection MAY replace that leaf.

If the prior horizontal child has been traversed onward, the newly selected occurrence remains in the anchor's row. The previously traversed horizontal continuation is displaced one row downward. A new row is inserted for that retained path, and pre-existing rows below it shift downward as necessary.

The current row focus is not changed merely because this insertion occurs.

Thus branching uses the axis orthogonal to the traversal path being preserved:

> **A retained vertical alternative consumes another column. A retained horizontal alternative consumes another row.**

## 3.6 Grid-Band Insertion Preserves Identity

Row and column positions are projection properties, not occurrence identities.

Insertion may change the grid coordinates of existing occurrences, but MUST NOT change:

- occurrence identity;
- semantic Holon identity;
- the source occurrence from which an occurrence was reached;
- the affordance through which it was reached;
- traversal direction;
- descendants or retained continuation.

> **Coordinates may move; provenance does not.**

## 3.7 Sparse Cells Are Not Occurrences

A sparse cell:

- has no semantic Holon;
- has no visualizer occurrence identity;
- does not participate in selection;
- does not create navigation provenance;
- exists only to preserve truthful projection geometry.

Sparse cells may arise above, below, left, or right of occupied cells as row and column insertion reconciles the two traversal-path systems.

## 3.8 Stable Attachment

Insertion, compression, scanning, viewport movement, and focus movement MUST NOT alter the semantic attachment of a descendant.

A continuation remains attached to the occurrence that produced it even when its current row or column position changes.


## 3.9 Lineage Connectors

The Path Inspector MUST expose recorded parentage through directional lineage
connectors for horizontal and vertical traversal, including retained alternatives
and recursive mixed-axis paths. Connectors are a projection of navigation
provenance, not additional topology or semantic relationships between Holons.

Each connector MUST identify its source and target by occurrence identity and
use the recorded traversal kind. Grid adjacency, DOM order, or shared Holon
identity MUST NOT imply parentage. Sparse cells and connector crossings do not
create occurrences, edges, or junctions.

Horizontal lineage connects the source occurrence's right boundary to the target
occurrence's left boundary, with a rightward arrowhead at the target. Vertical
lineage connects the source navigation stage's lower boundary to the target
occurrence's upper boundary, with a downward arrowhead at the target; the source
Collection remains the semantic mediator recorded by vertical provenance.

Connectors MUST use a visually prominent, thick stroke with rounded joins and
ends and a clear target arrowhead. Aligned endpoints MAY use a straight segment;
displaced endpoints use orthogonal segments with rounded elbows. Exact stroke
width, color, corner treatment and spacing are theme-responsive presentation
details rather than fixed pixel values in this grammar. Routes SHOULD avoid
unrelated Node interiors and remain distinguishable where paths cross or share
part of a route; an apparent junction MUST NOT imply unrecorded parentage.

For example, a retained vertical child displaced into another column remains
connected downward from its original source through an elbow route. If that
child opens a singular target, the new edge points rightward. A retained
horizontal child displaced into another row remains connected from its original
source through an elbow route with a rightward target arrowhead. Displacement
changes routing, not the recorded traversal axis or source.

The Path Inspector owns connector routing as part of inter-child geometry.
Row/column insertion, compression, restoration and resizing MUST update endpoints
to the current occurrence allocations without changing parentage. Scrolling and
viewport movement MUST keep connectors registered with their occurrences. A
compressed occurrence retains an attachment to its compact presentation; clipping
at the viewport boundary MUST NOT imply a new endpoint or changed parentage.
Hidden lineage remains directionally discoverable and recoverable under §7.4.
Connectors MUST NOT intercept Node, Collection or viewport interaction.

A new connector MUST NOT depict a traversal before its child occurrence is
successfully installed in the topology. Failed or stale realization preserves the
previous continuation and its connectors. Replacing an eligible leaf or explicitly
removing a branch removes only the connectors for topology that was removed;
retained descendants keep their original attachment.

---

# 4. Focus-Dependent Geometry

## 4.1 Focus Determines Allocation Priority

The Path Inspector preferentially allocates space toward the current focus and its immediate exploration context while the viewport moves over the persistent grid as needed.

Prior or non-focused context may receive progressively smaller allocations while remaining visible or recoverable.

## 4.2 Column Width Is a Path Inspector Decision

The Path Inspector assigns a width to each projected column.

All cells in a column receive the same external width budget for that column.

As the viewport/focus moves horizontally, the Path Inspector may:

- allocate the focused column a useful expanded width;
- partially compress contextual columns;
- fully compress more distant columns;
- overflow columns when the bounded viewport cannot retain them visibly.

A child visualizer does not independently choose the width of its column.

## 4.3 Row Height Is a Path Inspector Decision

The Path Inspector assigns a height to each projected row.

All cells in a row receive the same external height budget for that row.

As the viewport/focus moves vertically, the Path Inspector may:

- allocate the focused row a useful expanded height;
- partially compress contextual rows;
- fully compress more distant rows;
- overflow rows when necessary.

A child visualizer does not independently choose the height of its row.

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

# 5. Parent and Child Spatial Responsibility

## 5.1 Parent Owns Inter-Child Geometry

A compositional visualizer owns the placement and external spatial budgets of its immediate children.

For the Path Inspector this means it owns:

- sparse two-dimensional grid projection;
- row and column insertion;
- row and column allocation;
- viewport positioning over the grid;
- child cell bounds;
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

## 7.4 Overflow Is Distinct

Overflow occurs when even compressed contextual rows or columns cannot remain within the Path Inspector's bounded allocation.

Overflow changes visibility or placement, not topology.

Hidden lineage MUST remain directionally discoverable and recoverable.

## 7.5 Branch-Local Overflow

Overflow SHOULD apply to the relevant lineage or branch allocation rather than indiscriminately scrolling or displacing unrelated topology.

---

# 8. State Preservation

Compression, overflow, scanning, viewport movement, focus changes, row/column insertion, and child responsive adaptation MUST NOT inherently discard:

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

The Path Inspector may produce a large number of visible configurations, but those configurations SHOULD be generated from a small set of rules rather than explicitly enumerated.

The principal inputs are:

- navigation topology;
- traversal provenance;
- focus;
- viewport position;
- available Path Inspector allocation.

The principal derivations are:

- sparse grid topology;
- vertical-path column placement;
- horizontal-path row placement;
- column widths;
- row heights;
- cell spatial budgets;
- semantic presentation obligations.

The selected children then independently derive their responsive realization.

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
7. Descendants remain attached to the occurrences that produced them.
8. An untraversed leaf may be replaced by another selection from the same anchor.
9. Once navigation continues through an occurrence, that occurrence and its continuation become retained navigation history.
10. A new vertical alternative remains in the anchor's column; the traversed prior vertical continuation is preserved by inserting a column to its right and displacing retained grid content accordingly.
11. A new horizontal alternative remains in the anchor's row; the traversed prior horizontal continuation is preserved by inserting a row below and displacing retained grid content accordingly.
12. Row or column insertion may change grid coordinates but MUST NOT change occurrence identity or navigation provenance.
13. Sparse cells are valid when required to preserve truthful horizontal and vertical traversal paths.
14. The viewport may move over the grid; focus is not anchored to a fixed row or column.
15. Branch insertion itself does not change the focused column for vertical branching or the focused row for horizontal branching.
16. Every occupied cell receives the width of its column and the height of its row.
17. Horizontal compression or expansion transforms a whole column; vertical compression or expansion transforms a whole row.
18. The Path Inspector owns grid geometry, viewport projection, and child external allocation.
19. Selected children own their internal responsive realization.
20. Semantic presentation obligations may cross the parent-child boundary; implementation-specific layout directives should not.
21. Spatial size is not, by default, a Visualizer Selection Service criterion.
22. Compression changes allocation and presentation, not semantic identity or topology.
23. Overflow is distinct from compression and hidden lineage remains discoverable.
24. The same grammar must produce coherent behavior for navigation paths that have not been explicitly mocked up.
25. Directional lineage connectors expose recorded occurrence parentage and traversal kind; displacement, compression, and viewport movement change routing without changing attachment.

---

# 11. Relationship to Space Navigator

The Path Inspector is not the Space Navigator.

**Space Navigator** is a Dancer that composes capabilities into a coherent experience.

Within that experience, Space Navigator may expose a **RootedNavigation** visualizer slot rooted at its active HolonSpace.

Conceptually:

    SpaceNavigator Dancer
        ->
    RootedNavigation slot
        subject/root = active HolonSpace
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

The Path Inspector grammar therefore belongs to the selected RootedNavigation visualizer, not to the Space Navigator Dancer itself. This document is the normative source for the rooted-navigation topology, grid, viewport, traversal, insertion, compression, and overflow semantics used by Path Inspector.

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

The Path Inspector Design Specification should define concrete interactions that invoke this grammar, including:

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
- exact row-height or column-width functions;
- whether compression is discrete, continuous, or hybrid;
- animation;
- exact controls for hidden lineage;
- exact child visualizer responsive thresholds;
- exact compact representations;
- a universal DAHN compression-state vocabulary;
- persistence of Path Inspector sessions;
- sibling-history retention beyond the topology invariants;
- advanced adaptive allocation based on salience or learned behavior.

These decisions can evolve through implementation and usage without changing the core grammar.

---

# 15. Summary

The Path Inspector is a concrete **Structure / RootedNavigation** visualizer that turns an interaction-derived navigation topology into a persistent two-dimensional grid viewed through a bounded, movable viewport.

Its central navigation rule is:

> **Follow one thing horizontally; choose among many things vertically.**

Its central topology rule is:

> **Navigation provenance persists independently of the current projection.**

Its central projection rule is:

> **Each column preserves a vertical traversal path; each row preserves a horizontal traversal path; sparse cells and orthogonal insertion keep both path systems truthful.**

Its central allocation rule is:

> **Column width and row height are Path Inspector decisions; their intersection is the spatial budget of each child cell.**

Its central composition rule is:

> **Parent visualizers own inter-child geometry. Child visualizers own intra-child adaptation.**

Its central responsive rule is:

> **Compression is a smaller semantic presentation budget, not merely a scaled-down rendering.**

Its central selection rule is:

> **Select for semantic applicability; adapt the selected visualizer to changing spatial budgets.**

Together, these rules allow a small grammar to generate a wide range of coherent navigation paths without enumerating every visible configuration as a separate state. Existing mockups become conformance examples of the grammar rather than the definition of its complete state space.
