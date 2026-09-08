# Space Navigator: Conceptual Overview, Compositional Structure, Generative Grammar, and Visual Affordances

## 1. Conceptual Overview

The **Space Navigator** is a DAHN Canvas Visualizer for dynamically exploring, inspecting, and manipulating a MAP Space.

It does not present a sequence of pre-designed screens. Instead, it incrementally constructs a two-dimensional experience from:

- the Holons encountered;
- their descriptors;
- their scalar properties;
- their single-valued and multi-valued relationships;
- their dances and dance results;
- the Visualizer Holons selected by DAHN;
- the person's navigation and interaction choices.

The Space Navigator grows through interaction.

Each navigation operation adds to a persistent **navigation topology**. The Canvas presents a bounded viewport onto that topology, continuously reallocating space around the person's current focus rather than discarding prior context.

The central conceptual model is:

> **The navigation topology persists; the viewport shows a focus-dependent projection of it.**

Prior context may:

- remain expanded;
- become partially compressed;
- become fully compressed;
- overflow outside the current viewport;

but it remains part of the navigation topology until explicitly discarded or the Canvas is re-rooted.

---

# 2. Core Spatial Semantics

The Space Navigator assigns different semantic meaning to its two primary axes.

## 2.1 Horizontal Lineage

Horizontal navigation represents a lineage of directly related Holons connected through **single-valued Holon relationships or equivalent single-Holon results**.

Conceptually:

    H2 -> H2b -> H2c -> H2d

This is a relatively strong lineage.

Each step follows one semantic target to one semantic target.

The horizontal dimension therefore means:

> **Follow one thing.**

A horizontal lineage behaves as an accordion-like sequence. One member receives the useful expanded layout budget while surrounding lineage members progressively compress.

As the lineage grows beyond the available horizontal viewport, fully compressed members can move beyond the viewport boundary rather than continually shrinking the active Node Visualizer.

---

## 2.2 Vertical Lineage

Vertical navigation represents a weaker, collection-mediated lineage.

Conceptually:

    H1
     |
     +-- Collection C1
             |
             +-- selected H2
                     |
                     +-- Collection C2
                             |
                             +-- selected H3
                                     |
                                     +-- Collection C3
                                             |
                                             +-- selected H4

The semantic transition is:

> Holon -> Collection -> selected member -> Holon

The vertical dimension therefore means:

> **Choose among many things.**

The Collection Visualizer remains meaningful because it records the set through which the next Holon was reached and allows sibling exploration.

---

# 3. Navigation Topology Versus Visible Projection

The Space Navigator MUST distinguish the actual accumulated navigation topology from what happens to be visible in the viewport.

For example, suppose the initial vertical lineage is:

    H1
     |
    H2
     |
    H3
     |
    H4

and H2 develops a horizontal lineage:

    H2 -> H2b -> H2c -> H2d

The topology is:

        H1
         |
        H2 ---- H2b ---- H2c ---- H2d
         |
        H3
         |
        H4

As horizontal focus moves toward H2d, the original H1/H2/H3/H4 stack remains spatially intact.

It is not rewritten as:

    H1
    H2c
    H3
    H4

Instead, the viewport moves across a stable two-dimensional topology.

The H1/H2/H3/H4 vertical lineage may progressively move outside the left viewport boundary while H2c or H2d occupies the active horizontal working region.

This yields the invariant:

> **Lineages maintain their geometry as focus moves across them.**

---

# 4. Branching

Navigation is not limited to one linear path.

A lineage can branch when the person selects a different target from an earlier collection or follows another semantic continuation from an existing occurrence.

For example:

           H2
          /  \
        H3    H9

The common H2 occurrence should not be duplicated merely to make both branches visible.

Instead, its compressed representation may act as a **spanner** over the visible extent of its child branches.

For vertical branching, a compressed common parent may become a horizontal bar spanning the visible horizontal envelope of its children.

Conceptually:

              H2
        ----------------
          H3          H9

Likewise, when branching occurs along the horizontal dimension, a compressed common parent may become a vertical bar spanning the visible vertical envelope of its children.

This gives branching a general geometric rule:

> **A compressed common ancestor spans the visible cross-axis envelope of the branches it semantically anchors.**

Its thickness reflects its compression state.

Its length reflects the currently visible extent of the descendant branches.

Hidden off-screen descendants do not force the visible spanner to consume their full theoretical extent.

---

# 5. Stable Attachment

Each continuation remains spatially attached to the occurrence from which it was produced.

For example:

        H1
         |
        H2 ---- H2b ---- H2c ---- H2d
         |                         |
        H3                        H5
         |
        H4

H3/H4 remain part of the vertical lineage through H2.

H5 is a vertical continuation rooted at H2d.

As the horizontal viewport moves, these structures do not get reassigned to whichever horizontal node is currently in focus.

They remain attached to their semantic anchors.

This gives the Space Navigator a stable topology rather than a continuously reconstructed page layout.

---

# 6. Bounded Viewport

The Space Navigator Canvas operates within a bounded viewport.

Navigation does not cause the overall application window to grow indefinitely.

Instead:

- compression initially absorbs navigation pressure;
- the active occurrence receives a useful layout budget;
- fully compressed historical context can overflow outside the viewport;
- directional affordances indicate that recoverable lineage exists beyond the visible boundary.

The Canvas Title Bar remains pinned.

The navigation topology moves beneath it.

This avoids awkward blank regions created solely by retaining entire compressed bars as historical indicators.

The rule is:

> **Prior lineage need not remain physically visible merely to prove that it exists. Its existence and recoverability must remain perceptible.**

A lightweight affordance may indicate:

- more lineage exists left;
- more lineage exists right;
- more lineage exists above;
- more lineage exists below.

The exact visual treatment is intentionally deferred.

---

# 7. Node Visualizer Layout States

A Node Visualizer has three meaningful extents independently on each axis.

## 7.1 Width States

### Expanded Width

The Node Visualizer receives its full useful horizontal budget.

Conceptually this includes:

    +---------------------------+------+
    |                           |      |
    | Property Viewer           | Rail |
    |                           |      |
    +---------------------------+------+

Both:

- Property Viewer;
- Vertical Single-Value Rail;

are available.

### Partially Compressed Width

The Property Viewer is suppressed while the Vertical Single-Value Rail remains available.

Conceptually:

    +------+
    |      |
    | Rail |
    |      |
    +------+

This is not merely historical compression.

The remaining rail is an **active navigation surface**.

The person can scan among single-valued links and see different Holons realized to the right.

### Fully Compressed Width

The Node Visualizer is reduced to its minimum horizontal lineage representation.

It preserves:

- occurrence identity;
- navigation topology;
- recoverability;

but no longer needs to expose the active vertical rail.

Once fully compressed, it may be moved completely outside the current branch viewport.

---

# 8. Node Visualizer Height States

The same three-state model applies vertically.

## 8.1 Expanded Height

The full Node Visualizer is available, including its main content and collection affordances.

## 8.2 Partially Compressed Height

The vertically expensive upper Node content is suppressed while the collection-oriented navigation context remains usable.

This can preserve:

- Collection Tab Bar;
- active Collection Visualizer;
- collection row selection/navigation.

The remaining collection surface is still functionally active.

The person can:

- select another collection tab;
- inspect another collection;
- select another row;
- replace the vertically expanded child.

## 8.3 Fully Compressed Height

The occurrence is reduced to its minimum horizontal lineage representation.

It preserves topology and recoverability but no longer needs to consume viewport height.

Once fully compressed, it may overflow beyond the top or bottom viewport boundary.

---

# 9. Compression Versus Overflow

Compression and overflow are separate concepts.

A Visualizer controls its own presentation under:

- expanded;
- partially compressed;
- fully compressed;

layout budgets.

The Canvas controls whether that compressed occurrence is currently within the visible branch viewport.

Thus the progression may be:

    Expanded
        ->
    Partially Compressed
        ->
    Fully Compressed
        ->
    Overflowed

`Overflowed` is not a fourth Visualizer layout mode.

It is a Canvas placement state applied to an already compressed occurrence.

This preserves the architecture:

> **The parent controls external allocation and placement; the child controls its internal realization within that allocation.**

---

# 10. Lineage Cross-Axis Consistency

A useful geometric invariant applies to each lineage.

## 10.1 Vertical Lineage Width

The width of a vertical lineage follows the width of the Node occurrence at the lineage intersection.

If H2 changes horizontally from:

    expanded
        ->
    partially compressed
        ->
    fully compressed

then the H1/H2/H3/H4 vertical lineage associated with H2 adopts the corresponding width.

The vertical lineage therefore remains geometrically coherent.

---

## 10.2 Horizontal Lineage Height

Likewise, the height of a horizontal lineage follows the height of the Node occurrence at the lineage intersection.

If a Node becomes partially vertically compressed because its Collection Visualizer and selected child need more space, the horizontally attached lineage adopts the corresponding height.

Thus:

> **Vertical lineages share the current width of their intersection occurrence.**

> **Horizontal lineages share the current height of their intersection occurrence.**

---

# 11. Node Visualizer Compositional Structure

The initial Generic Holon Node Visualizer is conceptually composed from:

1. Title Bar
2. Node Action Bar
3. Property Viewer
4. Vertical Single-Value Rail
5. Horizontal Collection Tab Bar
6. Optional expanded Collection Visualizer

Conceptually:

    +--------------------------------------+------+
    | Title / Actions                      |      |
    +--------------------------------------+      |
    |                                      |      |
    | Property Viewer                      | Rail |
    |                                      |      |
    +--------------------------------------+------+
    | Collection Tabs                             |
    +---------------------------------------------+
    | Optional Collection Visualizer              |
    +---------------------------------------------+

The exact rendering may vary by selected Visualizer Holon.

The structural role is what matters.

---

# 12. Property Composition

Scalar properties appear through Property Visualizers and Value Visualizers.

Conceptually:

    Node Visualizer
        |
        +-- Property Visualizer
                 |
                 +-- Value Visualizer

The Node Visualizer does not need concrete knowledge of every Value Type.

The descriptor determines the property's semantic structure.

DAHN selects an applicable Property/Value Visualizer.

The theme determines presentation expression.

---

# 13. Single-Valued Affordances

Single-valued Holon relationships and equivalent single-Holon dance results populate the Vertical Single-Value Rail.

Selecting one creates or replaces a Node Visualizer to the right.

Thus:

    Node
        |
        +-- single-valued affordance
                |
                v
           rightward Node

The Vertical Rail remains visible during partial horizontal compression specifically because it remains useful for scanning the horizontal lineage.

---

# 14. Multi-Valued Affordances

Array-valued properties, multi-valued relationships, and collection-valued dance results populate the Collection Tab Bar.

Selecting a tab exposes its Collection Visualizer below the owning Node.

Conceptually:

    Node
      |
      +-- collection tab
              |
              v
         Collection
              |
         selected row
              |
              v
            Node

The Collection Visualizer may remain present as the parent Node compresses vertically so that sibling exploration remains efficient.

---

# 15. Collection Visualizer

The generic Collection Visualizer operates on a homogeneous collection independent of provenance.

A collection may originate from:

- array-valued property;
- multi-valued relationship;
- dance result;
- query result.

The initial generic implementation is table-oriented:

- one row per member;
- columns for projected properties;
- a collection-level header;
- column-level controls such as sorting/filtering.

For scalar collections, the table may contain a single value column.

---

# 16. Descriptor-Driven Generative Grammar

The Space Navigator derives structure from descriptors.

The core mapping is:

| Semantic Shape | Space Navigator Structure |
| --- | --- |
| Scalar property | Property Viewer |
| Array-valued property | Collection Tab + Collection Visualizer |
| Relationship with max cardinality 1 | Vertical Single-Value Rail |
| Relationship with max cardinality many | Collection Tab + Collection Visualizer |
| Dance returning one Holon | horizontal Node continuation |
| Dance returning a Holon collection | Collection Visualizer |
| Dance returning value collection | Collection Visualizer |
| No-result dance | Action surface |
| Scalar dance result | presentation still to be finalized |

The structural rule is:

> **Definitions determine structure; runtime values populate it.**

A relationship declared multi-valued remains structurally plural even when it currently has zero or one target.

A singular relationship remains singular even when it currently has no target.

---

# 17. Space Navigator Generative Grammar

The emerging spatial grammar can be described as a small set of operations.

## 17.1 Inspect

Create or activate a Node Visualizer occurrence for a Holon.

## 17.2 Traverse Right

Follow a single-valued Holon affordance.

Result:

    H1 -> H2

## 17.3 Traverse Down

Expose a collection, choose a member, and continue vertically.

Result:

    H1
     |
     C
     |
    H2

## 17.4 Branch

Select a different continuation from an existing point without duplicating the common parent.

## 17.5 Scan Lineage

Move focus along a horizontal or vertical lineage.

The newly focused member receives the expanded or useful layout budget while surrounding lineage members compress or overflow.

## 17.6 Partially Compress

Suppress expensive content while preserving an active axis-specific navigation surface.

Horizontal partial compression preserves the Vertical Single-Value Rail.

Vertical partial compression preserves collection-oriented navigation/context.

## 17.7 Fully Compress

Reduce an occurrence to minimal lineage representation while preserving topology.

## 17.8 Overflow

Move fully compressed lineage context beyond the bounded branch viewport.

## 17.9 Restore

Bring compressed or overflowed lineage back into the visible working projection.

## 17.10 Re-root

Choose an existing Node occurrence and make its Holon the new root/focal point of the Space Navigator.

The prior accumulated navigation topology is discarded from this Canvas.

Conceptually:

    accumulated topology
           |
       select H9
           |
       "re-root here"
           v
          H9

Re-rooting differs from ordinary navigation:

> Navigation extends the topology. Re-rooting replaces its retained root/context.

## 17.11 Maximize Region

Give one internal region of a Visualizer most or all of the real estate already allocated to that Visualizer.

Examples:

- maximize Property Viewer;
- maximize Collection Visualizer;
- maximize another internal pane.

This does not escape the parent's allocation.

Thus:

> **Maximization redistributes internal allocation; it does not change navigation topology or global Canvas geometry.**

## 17.12 Restore Region

Return from maximized internal presentation to the Visualizer's ordinary composition.

---

# 18. Compression, Maximization, and Re-rooting Are Distinct

These operations must not be conflated.

## Compression

Occurs because the parent supplies a smaller layout budget as navigation pressure grows.

It changes presentation while preserving topology.

## Maximization

Is an intentional attention operation within an existing allocation.

It redistributes internal space without changing topology.

## Re-rooting

Changes the retained navigation topology itself.

A useful shorthand is:

> **Compression is allocation pressure from outside.**

> **Maximization is attention applied from inside.**

> **Re-rooting changes the navigation context itself.**

---

# 19. Visual Affordance Families

The exact visual language remains intentionally open, but the Space Navigator requires semantic affordances for several classes of operation.

## 19.1 Holon Actions

At Node scope:

- Edit
- Clone
- Delete
- dances
- Create Instance where applicable
- alternate Visualizer selection
- re-root from here
- local maximize/restore operations where applicable

## 19.2 Canvas Actions

At Space Navigator scope:

- Undo
- Redo
- Commit
- transaction status
- Canvas-level controls

These remain pinned outside the scrolling navigation topology.

## 19.3 Collection Actions

Potentially:

- sort
- filter
- add/remove members when editable
- alternate Collection Visualizer
- maximize/restore collection region

## 19.4 Navigation Affordances

The Canvas needs mechanisms to:

- activate singular links;
- activate collection tabs;
- select collection rows;
- navigate a selected row;
- scan backward/forward through lineage;
- reveal hidden lineage beyond viewport boundaries;
- restore compressed context;
- re-root.

The specific widgets—arrows, gestures, buttons, fades, chevrons, hover controls, etc.—are deliberately not prescribed by the geometric grammar.

---

# 20. Hidden-Lineage Affordances

Fully compressed lineage may move completely outside the visible viewport.

The Canvas therefore needs lightweight edge affordances communicating that recoverable topology exists outside the current projection.

Conceptually:

    more left
    more right
    more above
    more below

These affordances may eventually communicate:

- direction;
- amount/count;
- lineage identity;
- scrollability.

The important design requirement is:

> **Hidden lineage must remain discoverable without requiring entire historical bars to consume viewport space.**

---

# 21. Re-rooting as Cognitive Reset

Accumulated topology can eventually become cognitively unnecessary even if it remains geometrically manageable.

The person therefore needs a deliberate operation equivalent to:

> **Make this Holon my new starting point.**

Re-rooting:

- preserves the selected semantic Holon;
- creates a fresh Canvas navigation root;
- removes prior navigation topology from the current Canvas;
- restores a full initial layout budget around the new focal occurrence.

This gives the person explicit control over accumulated context rather than requiring the Space Navigator to guess when history has become irrelevant.

---

# 22. Internal Focus / Maximize

Within any Visualizer's allocated rectangle, internal regions may compete for attention.

A region can therefore support an operation conceptually equivalent to:

> **Use this Visualizer's available allocation for this region.**

For example:

    ordinary Node

    +---------------------------+
    | title                     |
    +--------------------+------+
    | properties         | rail |
    +--------------------+------+
    | tabs                      |
    +---------------------------+
    | collection                |
    +---------------------------+

may become:

    focused collection

    +---------------------------+
    | title                     |
    +---------------------------+
    |                           |
    |       collection          |
    |                           |
    +---------------------------+

The title or a minimal restoration control may remain.

Action surfaces may eventually auto-hide or appear contextually.

Those details remain presentation decisions.

The invariant is:

> **A child may maximize within the allocation of its owning Visualizer, but it may not claim space outside that allocation.**

---

# 23. Query Composition Correspondence

The same structural grammar has a natural correspondence to a future Query Language Visualizer.

In ordinary Space Navigator interaction, a Collection Visualizer supports manual selection:

    Collection C
        |
        | choose row H
        v
       Holon H

In query composition, the same collection can instead be transformed by a predicate:

    Collection C0
        |
        | filter rule
        v
    Collection C1
        |
        | filter rule
        v
    Collection C2

The predicate vocabulary can be descriptor-driven.

For a selected property:

1. inspect its Property Type;
2. resolve its Value Type;
3. expose operators afforded by that Value Type;
4. render an appropriate Value Visualizer for the comparison value.

Examples may include:

- equals;
- not equals;
- less than;
- greater than;
- between;
- contains;
- before;
- after;

depending entirely on the Value Type's afforded operator space.

This allows the Query Language Visualizer to reuse:

- Collection Visualizers;
- Property Visualizers;
- Value Visualizers;
- lineage geometry;
- branching;
- compression;
- re-rooting;
- maximization;
- descriptor-driven affordances.

The difference is semantic:

> **The Space Navigator accumulates a navigation topology.**

> **The Query Language Visualizer accumulates a query derivation/execution topology.**

A saved query can preserve the sequence/composition of operations rather than merely the currently materialized results.

This reuse is evidence that the spatial grammar is broader than one Canvas implementation.

---

# 24. Relationship to DAHN Composition

The Space Navigator is one Canvas Visualizer implementing this grammar.

Its internal experience is itself composed from selected Visualizer Holons.

Conceptually:

    Space Navigator Canvas Visualizer
        |
        +-- Node Visualizer
        |     |
        |     +-- Property Visualizers
        |     |      |
        |     |      +-- Value Visualizers
        |     |
        |     +-- Action Visualizers
        |     |
        |     +-- Collection Visualizer
        |
        +-- Canvas Action Visualizers

The DAHN schema increasingly carries the semantic composition structure.

Visualizers are Holons.

Layouts are semantic Holons.

Visualizer Slots describe accepted child Visualizer roles.

Executable TypeScript implementations realize those semantic definitions within the layout allocation supplied by the parent.

---

# 25. Composition, Layout, and Theme

The architecture should preserve three distinct concepts.

## Composition

Defines:

> What structurally belongs here?

Examples:

- Title
- Actions
- Properties
- Singular Navigation
- Collection Navigation

## Layout

Defines:

> How do those components occupy the allocation supplied to this Visualizer?

Examples eventually include:

- vertical flow;
- horizontal flow;
- grid;
- stack;
- intrinsic sizing;
- fill;
- min/max constraints;
- partial/full compression variants.

## Theme

Defines:

> How are these semantic roles visually expressed?

Examples:

- font;
- size;
- weight;
- color;
- spacing;
- borders;
- buttons;
- state treatment.

Visualizers should not hard-code theme-owned decisions in TypeScript or CSS.

---

# 26. Core Geometric Invariants

The Space Navigator's current geometry can be summarized by the following invariants.

## 26.1 Bounded Canvas

The Canvas viewport remains bounded.

Navigation topology may extend beyond it.

## 26.2 Pinned Canvas Chrome

Canvas-level title/action regions remain fixed while navigation topology moves beneath them.

## 26.3 Stable Topology

Existing lineage is not rewritten merely because another occurrence receives focus.

## 26.4 Axis Semantics

Single-valued traversal extends horizontally.

Collection-mediated traversal extends vertically.

## 26.5 Three Extents Per Axis

Each Node Visualizer supports:

- expanded;
- partially compressed;
- fully compressed;

extent independently in width and height.

## 26.6 Partial Compression Preserves Active Scanning

Partial horizontal compression preserves singular-navigation capability.

Partial vertical compression preserves collection-navigation capability.

## 26.7 Full Compression Preserves Topology

Fully compressed context need not remain inside the visible viewport.

## 26.8 Overflow Is Branch-Local

Overflow affects the relevant lineage/branch allocation rather than scrolling the entire Canvas indiscriminately.

## 26.9 Cross-Axis Lineage Consistency

Vertical lineages share the width of their intersection occurrence.

Horizontal lineages share the height of their intersection occurrence.

## 26.10 Common Ancestors Span Branches

Compressed common ancestors span the visible cross-axis envelope of branches they anchor.

## 26.11 Parent Owns Allocation

A parent determines a child's external allocation.

The child composes within that allocation.

## 26.12 State Survives Projection Changes

Compression, overflow, scrolling, and maximization do not inherently destroy semantic or navigation state.

---

# 27. Compact Generative Model

The Space Navigator can therefore be understood as a small generative system.

Start with:

    Root Holon

Apply repeatedly:

    Inspect Holon
    Follow singular affordance -> extend right
    Open plural affordance -> expose collection below
    Select member -> extend downward
    Select alternate child -> branch
    Scan lineage -> redistribute expanded allocation
    Compress -> preserve topology under pressure
    Overflow -> hide fully compressed context beyond viewport
    Restore -> recover hidden context
    Maximize -> redistribute internal visualizer allocation
    Re-root -> establish a fresh navigation topology

The result is a continuously evolving two-dimensional navigation structure.

The Canvas does not attempt to display that entire structure at full fidelity.

Instead:

> **Space Navigator continuously projects an arbitrarily growing semantic navigation topology into a finite two-dimensional viewport around the person's current focus.**

That is the central geometric and compositional idea.