# DAHN Path Inspector Interaction Grammar

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
- occurrence identity and provenance;
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
- loading behavior;
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

Focus influences the viewport projection and the spatial allocation of rows and columns. It does not alter topology or reattach descendants.

## 1.5 Navigation Topology Versus Spatial Projection

The navigation topology records what has been unfolded and how occurrences are related.

The **spatial projection** is the current bounded realization of that topology around the focus.

> **Topology persists; geometry is derived.**

Changes in focus, compression, viewport size, or child responsive realization do not by themselves change the navigation topology.

## 1.6 Horizontal Traversal

A **horizontal traversal** follows a structurally singular affordance from one occurrence to one target occurrence.

Conceptually:

    A -> B -> C

Horizontal traversal means:

> **Follow one thing.**

A single-valued relationship or equivalent single-Holon result may produce horizontal traversal.

## 1.7 Vertical Traversal

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

## 1.8 Column

A **column** is a Path Inspector layout band representing a coherent horizontal navigation stage.

Columns have stronger semantic integrity than rows: horizontal descendants must remain spatially associated with the occurrence from which their horizontal traversal originated.

## 1.9 Row

A **row** is a Path Inspector layout band used to align vertical unfolding and assign a common height budget to cells at that vertical position.

Rows provide geometric integrity. They do not require the same semantic lineage invariant as columns.

## 1.10 Sparse Cell

A **sparse cell** is an intentionally unoccupied row/column intersection.

Sparse cells are legitimate structural elements of the projection. They preserve truthful alignment when a horizontal expansion originates from a lower row and therefore requires a distinct adjacent column.

Whitespace may therefore carry structural information.

## 1.11 Spatial Budget

A **spatial budget** is the external width and height allocation a parent visualizer gives a child visualizer.

The parent owns the budget. The child owns its internal composition within that budget.

## 1.12 Semantic Presentation Obligations

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

`branch(anchor, continuation)` retains an additional continuation from an existing anchor.

Existing continuations remain attached to the occurrences that produced them. A branch must not be reconstructed as a misleading linear page history merely to make the layout denser.

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

# 3. Sparse Matrix Projection

## 3.1 Projection as a Derived Matrix

The Path Inspector projects its rooted navigation topology into a sparse matrix of rows and columns.

The matrix is not the semantic source of truth. It is a geometric realization derived from:

- retained navigation topology;
- traversal provenance;
- current focus;
- available Path Inspector allocation.

## 3.2 Column Integrity

The Path Inspector MUST preserve horizontal navigation provenance when assigning occurrences to columns.

A column must not combine horizontal descendants whose placement would imply a false common horizontal parentage.

For example, given:

    A   B
    C

where `B` was reached horizontally from `A`, a new horizontal traversal from `C` must not simply place the new child beneath `B` if doing so would imply that the two cells belong to the same horizontal navigation stage.

Instead, the Path Inspector may insert a new adjacent column:

    A   .   B
    C   D

where `D` was reached horizontally from `C`.

The sparse cell above `D` preserves the integrity of the geometry.

> **Never compact the projection in a way that implies false navigation ancestry.**

## 3.3 Column Insertion

When a horizontal traversal requires a new navigation stage between existing projected stages, the Path Inspector inserts a column and shifts subsequent columns as necessary.

Existing occurrence provenance does not change when columns shift.

Column position is therefore a projection property, not occurrence identity.

## 3.4 Row Geometric Integrity

Rows MUST maintain coherent height allocation across their occupied cells so the Path Inspector can resize or compress a row as a unit.

Rows do not require the same semantic lineage integrity as columns.

The governing asymmetry is:

> **Columns preserve horizontal navigation lineage. Rows preserve geometric alignment.**

## 3.5 Sparse Cells Are Not Occurrences

A sparse cell:

- has no semantic Holon;
- has no visualizer occurrence identity;
- does not participate in selection;
- does not create navigation provenance;
- exists only to preserve truthful projection geometry.

## 3.6 Stable Attachment

Insertion, compression, scanning, and focus movement MUST NOT alter the semantic attachment of a descendant.

A continuation remains attached to the occurrence that produced it even when its current row or column position changes.

---

# 4. Focus-Dependent Geometry

## 4.1 Focus Determines Allocation Priority

The Path Inspector preferentially allocates space toward the current focus and its immediate exploration context.

Prior or non-focused context may receive progressively smaller allocations while remaining visible or recoverable.

## 4.2 Column Width Is a Path Inspector Decision

The Path Inspector assigns a width to each projected column.

All cells in a column receive the same external width budget for that column.

When focus moves horizontally, the Path Inspector may:

- allocate the focused column a useful expanded width;
- partially compress contextual columns;
- fully compress more distant columns;
- overflow columns when the bounded viewport cannot retain them visibly.

A child visualizer does not independently choose the width of its column.

## 4.3 Row Height Is a Path Inspector Decision

The Path Inspector assigns a height to each projected row.

All cells in a row receive the same external height budget for that row.

When focus moves vertically, the Path Inspector may:

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

- sparse row/column projection;
- column insertion;
- row and column allocation;
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

Compression, overflow, scanning, focus changes, row/column insertion, and child responsive adaptation MUST NOT inherently discard:

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
- available Path Inspector allocation.

The principal derivations are:

- sparse matrix topology;
- column placement;
- row placement;
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

1. The rooted navigation topology persists independently of its current spatial projection.
2. Holon identity and visualizer occurrence identity remain distinct.
3. Single-valued traversal extends horizontally.
4. Collection-mediated traversal extends vertically.
5. Descendants remain attached to the occurrences that produced them.
6. Focus changes projection and allocation; it does not rewrite provenance.
7. Horizontal navigation provenance is preserved through column integrity.
8. Rows provide common geometric height allocation without requiring equivalent semantic lineage integrity.
9. Sparse cells are valid when needed to preserve truthful geometry.
10. Column insertion may shift projection positions without changing topology.
11. Every occupied cell receives the width of its column and the height of its row.
12. The Path Inspector owns row/column geometry and child external allocation.
13. Selected children own their internal responsive realization.
14. Semantic presentation obligations may cross the parent-child boundary; implementation-specific layout directives should not.
15. Spatial size is not, by default, a Visualizer Selection Service criterion.
16. Slot semantic capability requirements may constrain visualizer applicability.
17. Compression changes allocation and presentation, not semantic identity or topology.
18. Independent width and height compression emerge from row/column allocation rather than requiring combinatorial Path Inspector states.
19. Overflow is distinct from compression and hidden lineage remains discoverable.
20. The same grammar must produce coherent behavior for navigation paths that have not been explicitly mocked up.

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

The Path Inspector grammar therefore belongs to the selected RootedNavigation visualizer, not to the Space Navigator Dancer itself.

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

The Path Inspector is a concrete **Structure / RootedNavigation** visualizer that turns an interaction-derived navigation topology into a bounded, focus-dependent spatial projection.

Its central navigation rule is:

> **Follow one thing horizontally; choose among many things vertically.**

Its central topology rule is:

> **Navigation provenance persists independently of the current projection.**

Its central projection rule is:

> **Preserve horizontal lineage through column integrity; preserve vertical alignment through row geometry; allow sparse cells when needed to keep the geometry truthful.**

Its central allocation rule is:

> **Column width and row height are Path Inspector decisions; their intersection is the spatial budget of each child cell.**

Its central composition rule is:

> **Parent visualizers own inter-child geometry. Child visualizers own intra-child adaptation.**

Its central responsive rule is:

> **Compression is a smaller semantic presentation budget, not merely a scaled-down rendering.**

Its central selection rule is:

> **Select for semantic applicability; adapt the selected visualizer to changing spatial budgets.**

Together, these rules allow a small grammar to generate a wide range of coherent navigation paths without enumerating every visible configuration as a separate state. Existing mockups become conformance examples of the grammar rather than the definition of its complete state space.
