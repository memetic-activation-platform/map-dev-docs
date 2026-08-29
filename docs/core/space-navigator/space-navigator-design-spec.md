# DAHN Space Navigator Design Specification v0.3

## Status

Draft normative design specification.

## Purpose

This specification defines the **Space Navigator**, an initial DAHN Canvas for generic, descriptor-driven exploration and manipulation of a MAP Space.

It is the single normative specification for Space Navigator behavior, including:

- inspection;
- navigation;
- visual composition;
- geometric compression;
- editing;
- Create;
- Clone;
- Delete;
- editable collections and relationships;
- multi-holon staged transactions;
- Undo;
- Redo;
- Commit;
- personalization interactions;
- interaction scenarios.

Cross-cutting DAHN architectural responsibilities are defined in `space-navigator-arch.md`.

In particular, this specification assumes the architectural contracts that:

- Rust owns MAP semantic, staged, transaction, adaptive, and selection state;
- TypeScript owns experience realization, visualizer occurrences, layout, navigation presentation, and immediate interaction;
- the DAHN Selector Function executes on the Rust side;
- visualizers may be discovered through federated Visualizer Commons;
- visualizer selection is distinct from client-side visualizer execution;
- transactions may contain staged changes to multiple holons;
- Undo, Redo, and Commit are transaction-scoped operations;
- TypeScript establishes meaningful Undo boundaries while Rust owns transaction snapshots and restoration.

This document defines how the Space Navigator uses those capabilities and what the person experiences.

---

# 1. Design Goals

## 1.1 Descriptor-Driven

The structure of the experience MUST be determined primarily from effective descriptors rather than domain-specific UI logic.

Effective semantic information determines:

- available properties;
- property shapes;
- relationships;
- relationship cardinality;
- effective dances;
- dance response shapes;
- inherited affordances;
- currently permitted affordances;
- editability.

Runtime data populates this structure but SHOULD NOT determine its structural form when descriptors already define that form.

---

## 1.2 Generic

The Space Navigator SHOULD support previously unknown holon types.

A specialized Node, Collection, Property, Value, or Action Visualizer MAY be selected when available.

Where no specialized visualizer applies, generic fallback visualizers SHOULD preserve basic usability.

The Space Navigator MUST therefore treat visualizer categories as roles rather than assume one permanently hard-coded implementation.

Unless otherwise stated, descriptions of Node and Collection behavior in this specification describe the requirements that the selected visualizer must satisfy within the Space Navigator.

The initial implementation may use:

- Generic Holon Node Visualizer;
- Table Collection Visualizer;
- generic Property Visualizers;
- generic Value Visualizers;
- generic Action Visualizers.

---

## 1.3 Shape-Oriented

Visual treatment SHOULD depend primarily on semantic shape and cardinality rather than provenance.

For example, the same Collection Visualizer category may present:

- an array-valued property;
- a multi-valued relationship target set;
- a multi-valued dance result.

Similarly, a single holon reached through either a relationship or dance result should be presented through a Node Visualizer.

---

## 1.4 Context-Preserving

Navigation SHOULD add visible or recoverable context rather than replace the current context as conventional page navigation would.

The Space Navigator should preserve:

- what is being inspected;
- how it was reached;
- which affordance produced the traversal;
- relevant prior collection or singular-navigation context.

---

## 1.5 Spatially Scalable

The Canvas MUST support sustained exploration without requiring every prior visualizer to remain at full size.

Prior context progressively compresses along the horizontal and vertical axes while remaining recoverable.

---

## 1.6 Unified Read and Edit Experience

Inspection and editing MUST use the same visual structure.

> **Read and edit are modes of the same descriptor-driven experience.**

Editing SHOULD NOT introduce a parallel form architecture.

---

## 1.7 Incrementally Implementable

The design SHOULD decompose into implementation increments that build on existing primitives rather than introducing parallel mechanisms.

---

# 2. Core Design Principles

## 2.1 Definitions Determine Structure

> **Definitions determine structure; runtime data populates it.**

For example:

- a relationship with maximum cardinality `1` is structurally singular even when it currently has no target;
- a relationship with maximum cardinality greater than `1` or unbounded is structurally plural even when it currently has zero or one target;
- a dance whose response descriptor declares a collection is structurally collection-valued before invocation.

The UI MUST NOT infer structural cardinality from runtime result count when descriptor information already defines it.

---

## 2.2 Navigation Determines Visibility

> **Navigation determines what is visible.**

Navigation state determines which visualizers and collections are currently expanded, compressed, selected, or in focus.

---

## 2.3 Descriptors Determine Editability

> **Descriptors and effective permissions determine what is editable.**

Visibility does not imply editability.

---

## 2.4 Staged State Determines What Is Being Changed

> **Staged state determines what is currently being changed.**

A visualizer may display persisted or staged semantic state while remaining in the same spatial position.

---

## 2.5 Compression Hides Presentation, Not State

> **Compression hides presentation; it does not destroy state.**

Navigation, selection, collection state, and staged edit context MUST survive compression.

---

# 3. Core Visual Roles

The Space Navigator is composed primarily from:

1. Canvas Visualizer;
2. Node Visualizers;
3. Collection Visualizers;
4. Property Visualizers;
5. Value Visualizers;
6. Action Visualizers.

The Space Navigator itself is a Canvas Visualizer.

The selected concrete visualizer for each role is resolved through DAHN architectural mechanisms.

---

# 4. Space Navigator Canvas

## 4.1 Responsibility

The Space Navigator owns Canvas-specific behavior including:

- visualizer occurrence placement;
- horizontal and vertical traversal;
- active traversal frontier;
- navigation provenance;
- Canvas geometry;
- compression and restoration;
- Canvas-level focus;
- transaction-level interaction surface;
- coordination of selected Node and Collection Visualizers.

It SHOULD NOT contain domain-specific knowledge about the holons being displayed.

---

## 4.2 Canvas Structure

The Space Navigator consists conceptually of:

1. a pinned Canvas Action Bar;
2. the navigable Canvas area containing visualizer occurrences.

Conceptually:

    +------------------------------------------------------+
    | Canvas Action Bar                                    |
    | Undo | Redo | Commit | ...                           |
    +------------------------------------------------------+
    |                                                      |
    | Space Navigator Canvas                               |
    |                                                      |
    | Node / Collection visualizer occurrences             |
    |                                                      |
    +------------------------------------------------------+

The Canvas Action Bar remains pinned while traversal occurs beneath it.

---

# 5. Canvas Action Bar

## 5.1 Purpose

The Canvas Action Bar contains actions whose semantic scope is the current Space Navigator Canvas session or active MAP transaction.

These actions SHOULD NOT be repeated in every Node Visualizer.

---

## 5.2 Transaction Actions

The Canvas Action Bar SHOULD support transaction-scoped operations such as:

- Undo;
- Redo;
- Commit;
- transaction status;
- abandon/revert transaction where supported.

Because one transaction may contain staged changes to multiple holons, Commit belongs here rather than in an individual Node Visualizer.

---

## 5.3 Canvas Actions

The Canvas Action Bar MAY additionally contain:

- Canvas view controls;
- layout controls;
- Canvas-specific navigation controls;
- Canvas visualizer controls;
- other Space-Navigator-level operations.

---

## 5.4 Personalization

The Space Navigator defines a set of Canvas-level actions and their relative semantic importance.

Where supported, the person MAY personalize:

- ordering;
- prominence;
- visible versus overflow placement;
- Action Visualizer choice.

Reordering or replacing action presentations MAY emit adaptive signals according to the architecture specification.

---

## 5.5 Action Scope Rule

Actions SHOULD appear at the lowest common scope that owns their effect.

Examples:

- value action → Value Visualizer;
- property action → Property Visualizer;
- collection action → Collection Visualizer;
- holon action → Node Visualizer;
- transaction action → Canvas Action Bar.

---

# 6. Active Traversal Frontier

At any point, the Space Navigator has an **active traversal frontier**: the visualizer occurrence currently receiving primary interaction and spatial priority.

The Canvas SHOULD preferentially allocate real estate toward this frontier.

Prior contexts progressively compress away from it.

> **The Canvas allocates space toward the active traversal frontier and compresses provenance behind it.**

---

# 7. Node Visualizer

## 7.1 Responsibility

A Node Visualizer renders one holon together with the effective affordances available for that holon.

The same Node Visualizer category is used regardless of whether the holon:

- is the initial node;
- was reached vertically;
- was reached horizontally;
- was returned from a dance;
- represents persisted state;
- represents staged edited state;
- is newly created;
- is a staged clone.

Placement and mode change.

The semantic role does not.

---

## 7.2 Selection

For each holon occurrence, the Space Navigator requests an applicable Node Visualizer through the DAHN selection architecture.

The initial fallback is the Generic Holon Node Visualizer.

A specialized Node Visualizer MAY replace it without changing the Canvas traversal model, provided it satisfies the required Space Navigator contracts.

---

## 7.3 Inputs

A Node Visualizer may require:

- semantic holon reference;
- effective descriptor or presentation context;
- required property projections;
- effective holon actions;
- selected adaptive ordering;
- current interaction mode;
- current layout budget;
- theme context.

Additional values SHOULD be retrieved lazily where practical.

---

# 8. Full Node Geometry

In its initial full state, a Node Visualizer is conceptually composed from:

1. Title Bar;
2. Node Action Bar;
3. Property Viewer Pane;
4. Vertical Single-Value Tab Rail;
5. Horizontal Collection Tab Bar.

Conceptually:

    +--------------------------------------+--+
    | Title / actions / properties         |  |
    |                                      |  |
    | Main Node Visualizer body            |  | singular
    |                                      |  | navigation
    |                                      |  | rail
    +--------------------------------------+--+
    | Collection tab bar                      |
    +-----------------------------------------+

The vertical rail and horizontal tab bar are visible before either child region is activated.

No child Node Visualizer or Collection Visualizer consumes additional space until explicitly selected.

---

# 9. Node Title Bar

The Title Bar identifies the displayed holon.

It SHOULD expose enough identity to distinguish multiple visualizer occurrences.

Initial content may include:

- display name or identifying label;
- type;
- edit/staged indicator;
- compression or restoration affordances where appropriate.

---

# 10. Node Action Bar

## 10.1 Purpose

The Node Action Bar contains actions whose semantic subject is the displayed holon.

Examples may include:

- Edit;
- Clone;
- Delete;
- type-defined dances;
- Create Instance when the displayed holon is an applicable concrete Holon Type descriptor;
- alternate Node Visualizer selection;
- Node-specific visual controls.

It SHOULD NOT contain transaction-wide Commit, Undo, or Redo.

---

## 10.2 Effective Dances

Presented dances may include:

- directly declared dances;
- inherited dances;
- dances permitted by role;
- dances allowed by other runtime policy.

Only effective available dances SHOULD be presented.

---

## 10.3 Alternate Visualizers

If alternate applicable Node Visualizers are available, the Node Visualizer SHOULD be able to advertise that fact.

The person MAY select an alternate visualizer.

Doing so:

- changes the current experience immediately;
- preserves the visualizer occurrence and traversal context where possible;
- emits an adaptive visualizer-selection signal.

---

## 10.4 Compression

When space is constrained, Node Action Bar presentation MAY compress into:

- icons;
- compact buttons;
- menus;
- overflow controls.

The semantic actions remain available according to their applicable priority and layout budget.

---

# 11. Property Viewer Pane

## 11.1 Purpose

The Property Viewer Pane presents scalar properties of the holon.

It supports both read and edit modes.

---

## 11.2 Property Visualizers

Individual properties SHOULD be delegated to applicable Property Visualizers.

Property Visualizers may in turn delegate value presentation to Value Visualizers.

Conceptually:

    Node Visualizer
        |
        +-- Property Visualizer
                |
                +-- Value Visualizer

---

## 11.3 Scalar Values

Scalar properties SHOULD initially be presented as name/value pairs.

Value rendering MUST NOT be hard-coded by the Node Visualizer for each concrete value type.

---

## 11.4 Read Mode

In read mode:

- property values are rendered for inspection;
- editable controls are not active;
- navigation and applicable actions remain available.

---

## 11.5 Edit Mode

In edit mode:

- editable scalar values become interactive through their selected Property and Value Visualizers;
- non-editable values remain read-only;
- edits update staged state through MAP operations;
- geometry remains fundamentally the same.

Possible Value Visualizer interactions include:

- text input;
- numeric input;
- date/time input;
- boolean controls;
- enumerated choices;
- structured editors;
- reference selectors.

---

## 11.6 Property Ordering

Where supported, properties MAY be reordered by the person.

For example, dragging a property upward:

- immediately changes TypeScript presentation order;
- preserves that local experience;
- emits an adaptive signal;
- may influence future personal ordering;
- may contribute to aggregate salience.

Ordering matters particularly when vertical real estate is constrained.

---

# 12. Array-Valued Properties

Array-valued properties are structurally plural.

They SHOULD NOT be rendered inline as expanded scalar fields.

They SHOULD appear in the Horizontal Collection Tab Bar and use a Collection Visualizer when activated.

In edit mode, the same Collection Visualizer MAY support array mutation operations.

---

# 13. Vertical Single-Value Tab Rail

## 13.1 Purpose

The vertical rail on the right edge of a Node Visualizer exposes affordances that resolve to a single holon.

It is the singular counterpart to the horizontal Collection Tab Bar.

---

## 13.2 Eligible Affordances

The rail may represent:

- single-valued relationships;
- single-holon dance result affordances.

Only descriptor-declared singular holon affordances belong here.

---

## 13.3 Structural Presence

A single-valued relationship remains structurally singular even if it currently has no target.

Its rail entry therefore MAY remain visible with an appropriate empty-state treatment.

---

## 13.4 Activation

Selecting an entry opens the corresponding Node Visualizer to the right.

If another singular affordance from the same source is selected, the initial implementation MAY replace the existing right-hand child rather than preserve sibling branches.

---

## 13.5 Personalization

Rail entries MAY be reordered.

Moving an item upward:

- immediately changes presentation;
- may preserve visibility under constrained height;
- emits an adaptive salience signal.

---

# 14. Editing Single-Valued Relationships

When the containing holon is staged for editing and the relationship is mutable, its singular affordance MAY additionally support:

- set target;
- replace target;
- clear target.

These actions modify staged relationship state of the source holon.

They do not edit properties of the target holon.

Editing the target holon requires entering edit mode on that target's Node Visualizer.

---

# 15. Horizontal Collection Tab Bar

## 15.1 Purpose

The bottom Collection Tab Bar exposes plural affordances of the current holon.

---

## 15.2 Eligible Affordances

A collection tab may represent:

- array-valued property;
- multi-valued relationship;
- collection-valued dance result or result affordance.

---

## 15.3 Geometry

The Collection Tab Bar MUST have the same width as its owning Node Visualizer in that visualizer's current expanded geometry.

---

## 15.4 Initial State

The tab bar is visible even when no collection is open.

No Collection Visualizer occupies vertical space until a tab is selected.

---

## 15.5 Activation

Selecting a tab:

- activates that plural affordance;
- claims space beneath the Node Visualizer;
- displays the selected Collection Visualizer.

Selecting another tab reuses the collection region.

---

## 15.6 Personalization

Collection tabs MAY be reordered.

Moving a tab leftward:

- increases immediate prominence;
- may preserve visibility when width is constrained;
- emits an adaptive salience signal.

---

# 16. Relationship Presentation

## 16.1 Cardinality Rule

Relationship presentation MUST derive from descriptor-declared cardinality.

Runtime target count MUST NOT change structural treatment.

---

## 16.2 Singular Relationship

Maximum cardinality `1`:

- appears in the Vertical Single-Value Tab Rail;
- supports horizontal navigation;
- may support set/replace/clear in edit mode.

---

## 16.3 Plural Relationship

Maximum cardinality greater than `1` or unbounded:

- appears in the Horizontal Collection Tab Bar;
- opens a Collection Visualizer;
- may support add/remove/reorder in edit mode.

A plural relationship with zero or one current target remains plural.

---

# 17. Dance Result Presentation

## 17.1 Descriptor-Based Classification

Dance result shape SHOULD be known from its response descriptor before invocation.

---

## 17.2 Single-Holon Result

A dance returning one holon converges on horizontal Node Visualizer presentation.

---

## 17.3 Holon Collection Result

A dance returning a holon collection converges on Collection Visualizer presentation.

---

## 17.4 Value Collection Result

A homogeneous collection of values also converges on Collection Visualizer presentation.

---

## 17.5 Scalar Result

The initial presentation of scalar non-holon dance results remains an open design question.

---

## 17.6 No-Result Dance

A no-result dance may remain represented in the Node Action Bar with suitable execution feedback.

---

# 18. Collection Visualizer

## 18.1 Responsibility

A Collection Visualizer renders a homogeneous multi-valued semantic result.

Its structural behavior SHOULD be independent of whether the collection originated from:

- array property;
- relationship;
- dance.

---

## 18.2 Selection

An applicable Collection Visualizer is selected through DAHN architecture.

The initial fallback is the Table Collection Visualizer.

A specialized Collection Visualizer MAY be selected without changing the Space Navigator's collection placement contract.

---

## 18.3 Geometry

An expanded Collection Visualizer MUST initially have the same width as the Node Visualizer that exposes it.

It appears directly beneath the owning Collection Tab Bar.

---

# 19. Table Collection Visualizer

## 19.1 Rows

Each collection element corresponds to one row.

For holon collections:

- one row represents one holon.

For simple value collections:

- one row represents one value.

---

## 19.2 Columns

For holon collections:

- columns correspond to exposed projected properties.

For simple scalar collections:

- the initial table normally contains one value column.

---

## 19.3 Collection Header

The Collection Visualizer SHOULD have a header distinct from column headers.

It may contain:

- collection name;
- element count;
- collection actions;
- alternate visualizer controls;
- projection information;
- state indicators.

---

## 19.4 Column Operations

Column headers SHOULD eventually support:

- sorting;
- filtering.

These may be delivered incrementally.

---

# 20. Editable Collection Visualizers

A Collection Visualizer MAY become editable when it represents staged state semantically owned by the holon being edited.

The same visualizer is used for inspection and editing.

Editing adds mutation affordances rather than replacing the collection with a separate form.

---

# 21. Editable Value Arrays

For an editable array-valued property, the Collection Visualizer MAY support:

- add value;
- remove value;
- edit value;
- reorder values where ordering is semantically meaningful and permitted.

Individual values continue to delegate editing to their applicable Value Visualizers.

Changes update Rust-owned staged state.

---

# 22. Editable Multi-Valued Relationships

For a mutable plural relationship, the Collection Visualizer MAY support:

- add target;
- remove target;
- reorder targets where allowed.

Target selection MAY initially use the simplest generic selection mechanism available.

Relationship membership editing changes the source holon's staged relationship state.

---

# 23. Dance Result Collection Editability

A collection-valued dance result is not inherently editable merely because it is shown through a Collection Visualizer.

Editability depends on:

- semantic ownership;
- available mutation affordances;
- descriptors;
- permissions.

---

# 24. Semantic Editing Ownership

The Space Navigator MUST distinguish editing a relationship or collection from editing a contained target holon.

For example, if A has a `Friends` collection containing B:

- adding or removing B from `Friends` edits A;
- changing B's `name` edits B.

Visual containment MUST NOT imply semantic editing ownership.

---

# 25. Descriptor-to-Presentation Mapping

The initial structural mapping is:

| Affordance | Declared Shape | Space Navigator Presentation |
| --- | --- | --- |
| Property | scalar | Property Viewer Pane |
| Property | homogeneous array | Collection Tab + Collection Visualizer |
| Relationship | max cardinality = 1 | Vertical Single-Value Tab |
| Relationship | max cardinality > 1 or unbounded | Collection Tab + Collection Visualizer |
| Dance | no result | Node Action Bar |
| Dance | scalar result | TBD |
| Dance | single holon result | Node Action Bar + horizontal Node Visualizer |
| Dance | holon collection result | Node Action Bar + Collection Visualizer |
| Dance | value collection result | Node Action Bar + Collection Visualizer |

This mapping is normative for the initial Space Navigator.

---

# 26. Navigation Geometry

The Space Navigator uses two spatial dimensions with distinct semantic meanings.

---

## 26.1 Horizontal Navigation: Follow One

A singular holon affordance extends the Canvas to the right.

Examples include:

- single-valued relationship;
- single-holon dance result.

Conceptually:

    Node A  ->  Node B

The right-hand child initially uses the same canonical full Node Visualizer dimensions as its source where space permits.

---

## 26.2 Vertical Navigation: Choose Among Many

A plural affordance extends downward through a Collection Visualizer.

Conceptually:

    Node A
       |
       +-- Collection C
              |
              +-- Node B

The collection retains the same width as Node A while expanded.

---

## 26.3 Navigation Invariant

> **Single-valued traversal extends horizontally.**

> **Multi-valued traversal extends vertically through a Collection Visualizer.**

The geometry encodes semantic cardinality.

---

# 27. Recursive Exploration

Every Node Visualizer can continue navigation regardless of how it was reached.

A horizontally reached node may:

- continue right;
- open a collection downward;
- descend through that collection.

A vertically reached node may likewise continue in either direction.

Conceptually:

    Space
      |
      +-- Types
             |
             +-- Person Type  ->  Schema
                    |
                    +-- Properties
                           |
                           +-- first_name  ->  Value Type

Each holon in this structure is represented by a separate visualizer occurrence.

---

# 28. Visualizer Occurrences and Provenance

The Canvas MUST distinguish:

- holon identity;
- visualizer occurrence identity.

The same holon may appear through multiple traversal paths.

Each occurrence may maintain different:

- parent occurrence;
- selected affordance;
- focus;
- visualizer choice;
- collection state;
- compression state;
- layout.

Provenance SHOULD record how each occurrence was reached.

---

# 29. Collection Interaction

## 29.1 Row Selection

The initial interaction model SHOULD distinguish row selection from navigation.

A likely convention is:

- single-click selects;
- double-click navigates.

---

## 29.2 Vertical Child

Navigating a holon row opens a child Node Visualizer beneath the collection.

The initial implementation MAY support only one active child per collection occurrence.

Selecting another row MAY replace the child while retaining the collection.

---

## 29.3 Sibling Exploration

The collection SHOULD remain accessible while inspecting its selected child so that the person can move among sibling rows without reconstructing the path.

---

# 30. Singular Interaction

Selecting a singular-navigation rail entry opens the target to the right.

The initial implementation MAY support only one right-hand child per source occurrence.

Selecting another singular affordance MAY replace the previous child.

---

# 31. Focus

The Space Navigator SHOULD track an active visualizer occurrence.

Focus is distinct from visibility.

Multiple prior occurrences may remain visible or compressed while one occurrence is active.

Focus may influence:

- keyboard interaction;
- active traversal frontier;
- layout priority;
- contextual Canvas behavior.

The exact visual treatment of focus may evolve.

---

# 32. Geometric Compression

Persistent navigation can grow in both dimensions.

The Space Navigator therefore supports two independent compression operations:

    compress-x
    compress-y

---

# 33. Full State

A full Node Visualizer shows:

- Title Bar;
- Node Action Bar;
- Property Viewer Pane;
- Vertical Single-Value Tab Rail;
- Horizontal Collection Tab Bar.

---

# 34. Horizontal Compression

Horizontal compression is used as exploration continues to the right.

A prior Node Visualizer progressively relinquishes width.

It may retain:

- compact identity;
- relevant singular-navigation context;
- compact Node actions;
- recoverable collection state.

Its main Property Viewer no longer needs full width.

Any subordinate expanded collection must also relinquish that width.

---

# 35. Progressive Horizontal Compression

Repeated traversal may evolve conceptually from:

    Full A + Full B

to:

    |A| + Full B

to:

    |A| |B| + Full C

Increasingly distant ancestors become increasingly compact.

---

# 36. Vertical Compression

Vertical compression is used as exploration proceeds downward.

A prior Node Visualizer progressively relinquishes height.

It may retain:

- compact identity;
- active Collection Tab Bar;
- immediate collection context.

Its Property Viewer and other vertically expensive regions may collapse.

---

# 37. Progressive Vertical Compression

More distant ancestors MAY compress into progressively smaller horizontal provenance bars.

The immediate collection context MAY remain expanded to support sibling inspection.

---

# 38. Combined Compression

X and Y compression are orthogonal.

An occurrence may be:

| State | Horizontal Extent | Vertical Extent |
| --- | --- | --- |
| Full | full | full |
| X-compressed | narrow | full-ish |
| Y-compressed | full-ish | short |
| XY-compressed | narrow | short |

A doubly compressed occurrence may become a compact provenance cell.

---

# 39. Compression Invariants

## 39.1 Compress Away From the Frontier

Increasing distance from the active traversal frontier SHOULD generally imply increasing compactness.

## 39.2 Preserve State

Compression MUST preserve relevant state such as:

- selected collection tab;
- selected singular affordance;
- child relationships;
- collection sort/filter state;
- selected row;
- scroll position;
- edit mode;
- staged-state reference;
- visualizer identity.

## 39.3 Restoration

Re-expanding a compressed occurrence SHOULD restore prior local context where feasible.

## 39.4 Subordinate Geometry Follows Parent Geometry

A compressed parent MUST NOT leave subordinate presentation consuming dimensions that the parent has relinquished.

---

# 40. Loading States

Structural affordances remain visible even when runtime data is not yet available.

The Space Navigator SHOULD distinguish:

- not loaded;
- loading;
- loaded empty;
- loaded with contents;
- failed.

A multi-valued relationship with zero targets remains visible as a collection affordance.

A singular relationship with no target remains structurally singular.

---

# 41. Progressive Retrieval

The Space Navigator SHOULD favor lazy retrieval.

A typical flow is:

1. obtain semantic reference;
2. obtain effective descriptor and presentation context;
3. select visualizer;
4. construct structural affordances;
5. retrieve initial scalar projection;
6. retrieve collection contents on tab activation;
7. retrieve singular target on rail activation;
8. invoke dance only on explicit action.

---

# 42. Entering Edit Mode

When the person selects **Edit** on a persisted holon:

1. MAP stages or exposes a new version of that holon;
2. the existing Node Visualizer occurrence remains in place;
3. the visualizer enters edit mode;
4. editable scalar properties become interactive;
5. editable relationship and collection affordances become mutable where allowed;
6. transaction status becomes visible at Canvas scope.

Entering edit mode is a state transition, not a navigation transition.

---

# 43. Continuous Preservation of Staged Work

In-progress staged work is preserved by MAP snapshot mechanisms.

The person SHOULD NOT need a conventional Save button merely to protect work from loss.

The design therefore distinguishes:

- preservation of staged work;
- explicit transaction Commit.

---

# 44. Multiple Holons in Edit Mode

The Space Navigator MAY contain staged changes to multiple holons in the same active transaction.

For example:

    A [editing]
      |
      C
      |
      B [editing] -> D [read-only]

A and B may both contribute staged changes to the same transaction.

This MUST NOT imply separate Commit operations for each node.

---

# 45. Staged State and Visualizer Occurrences

Visualizer occurrence state and staged semantic state are distinct.

If the same holon appears in multiple occurrences while staged:

- all occurrences ultimately reflect the same authoritative staged semantic state;
- TypeScript MUST NOT create independent semantic edit copies for each occurrence.

The exact synchronization presentation may evolve, but semantic divergence MUST NOT occur silently.

---

# 46. Editing While Navigating

Entering edit mode MUST NOT inherently disable navigation.

The person may continue to:

- inspect collections;
- navigate vertically;
- navigate horizontally;
- open other holons;
- edit additional holons.

Staged work remains intact.

---

# 47. Compressing Editable Visualizers

When an editable occurrence is compressed:

- staged data remains intact;
- edit state remains known;
- the compact representation SHOULD indicate staged changes;
- re-expansion restores editable presentation.

Compression MUST NOT:

- Commit;
- abandon;
- revert;
- discard staged changes.

---

# 48. Create

Create SHOULD use the same editable visual structure as Edit.

A preferred generic entry point is an applicable concrete Holon Type descriptor.

When **Create Instance** is invoked:

1. a new staged holon of that type is created in the active Space;
2. defaults are applied where defined;
3. a Node Visualizer presents the new staged holon in edit mode;
4. editing uses normal descriptor-driven Property, Value, Collection, and Action Visualizers;
5. the new holon participates in the active transaction.

Create does not require a separate form architecture.

---

# 49. Clone

When **Clone** is invoked:

1. MAP creates a new staged holon initialized from the source according to clone semantics;
2. the new holon receives its own semantic identity;
3. it is presented in normal edit mode;
4. it participates in the active transaction.

Clone source history is not automatically treated as Canvas traversal provenance.

After staged initialization, Clone and Create use the same editing interaction model.

---

# 50. Delete

Delete is a holon-scoped action.

When invoked:

1. the person receives any required explicit confirmation;
2. deletion is staged according to MAP semantics;
3. the staged deletion participates in the active transaction;
4. Commit later publishes it with other staged changes.

Delete MUST NOT imply physical erasure of historical committed state.

The exact post-Commit presentation of deleted holons remains a design detail to refine.

---

# 51. Commit

Commit is exposed in the pinned Canvas Action Bar.

It applies to the **entire active transaction**, which may include:

- updated holons;
- newly created holons;
- clones;
- relationship changes;
- array changes;
- staged deletions.

It is not a Node Visualizer action.

---

# 52. Commit Flow

When Commit is invoked:

1. the active staged transaction is validated;
2. applicable validation errors are returned if present;
3. if valid, MAP commits the transaction;
4. affected visualizers refresh from committed state;
5. affected staged visualizers return to read presentation;
6. navigation provenance remains intact.

Commit is a transaction-state transition, not a navigation transition.

---

# 53. Commit Failure

If validation or Commit fails:

- staged transaction state remains intact;
- affected visualizers remain in edit mode;
- the person may correct the staged state and retry;
- errors SHOULD appear as close as practical to affected visualizers;
- the Canvas MAY also display a transaction-level summary.

Failure MUST NOT silently discard staged work.

---

# 54. Undo and Redo

Undo and Redo are exposed in the pinned Canvas Action Bar.

They apply to the active transaction.

They MUST operate on Rust-owned staged semantic state rather than merely reversing TypeScript presentation.

---

# 55. Undo Boundaries

TypeScript determines when a meaningful UX interaction constitutes a new Undo boundary.

Examples may include:

- completing a property edit;
- adding/removing a relationship target;
- completing an array mutation;
- completing another semantically meaningful editing gesture.

Low-level preservation snapshots need not correspond one-to-one with user-visible Undo steps.

---

# 56. Undo Flow

Conceptually:

    edit gesture completes
          |
    meaningful Undo boundary established
          |
    later: Undo
          |
    Rust restores prior staged snapshot
          |
    affected visualizers refresh

Undo MAY therefore affect multiple visible visualizers if one interaction changed shared transaction state.

---

# 57. Redo Flow

Redo restores the next recoverable transaction snapshot and refreshes affected presentation.

Its availability SHOULD be reflected in the Canvas Action Bar.

---

# 58. Abandon or Revert Transaction

The Space Navigator SHOULD eventually provide a clear transaction-level mechanism for abandoning or reverting staged work.

The exact user-facing term and semantics remain to be finalized.

Possible semantics include:

- revert entire active transaction to its starting state;
- abandon all staged changes;
- preserve recoverable staged state for later resumption.

The behavior MUST be explicit and MUST NOT silently lose work.

---

# 59. Adaptive and Personalizable Interactions

The Space Navigator SHOULD expose personalization opportunities where useful.

Potential adaptive gestures include:

- property reorder;
- collection-tab reorder;
- singular-rail reorder;
- action reorder;
- explicit alternate visualizer selection;
- navigation choices.

Immediate presentation changes happen locally.

Persistent personal and collective learning occurs according to the architecture specification.

---

# 60. Personalization and Constrained Geometry

Ordering has practical consequences under constrained space.

For example:

- top-ranked properties remain visible longest when vertically constrained;
- leftmost collection tabs remain visible longest when horizontally constrained;
- highest singular-navigation entries remain visible longest when vertically constrained;
- prominent actions remain outside overflow longest.

Thus personalization and adaptive salience help determine graceful degradation under compression.

---

# 61. Interaction Scenarios

## 61.1 Inspect a Holon

Given a holon:

1. obtain semantic and presentation context;
2. select an applicable Node Visualizer;
3. display identity and scalar properties;
4. expose singular affordances in the right rail;
5. expose plural affordances in the bottom tab bar;
6. expose holon-level actions;
7. show no child collection or right-side Node Visualizer until selected.

---

## 61.2 Open a Multi-Valued Relationship

Given plural relationship R:

1. R appears as a Collection Tab;
2. select R;
3. load targets if required;
4. select applicable Collection Visualizer;
5. display it below the node at matching width;
6. retain the source node as context.

The same behavior applies with zero, one, or many current targets.

---

## 61.3 Navigate Through a Collection

Given Node A and Collection C:

1. select or double-click row B for navigation;
2. create a Node Visualizer occurrence for B below C;
3. preserve A and C;
4. record provenance;
5. preserve C so sibling rows remain accessible;
6. optionally compress A vertically.

---

## 61.4 Follow a Singular Relationship

Given Node A and singular relationship R:

1. R appears in the right rail;
2. activate R;
3. load target B;
4. display a Node Visualizer for B to the right;
5. preserve provenance from A through R;
6. optionally compress A horizontally.

---

## 61.5 Continue Horizontally

Given:

    A -> B

if B opens C:

- C becomes the active frontier;
- B may retain immediate singular-navigation context;
- A may compress more aggressively;
- prior subordinate geometry compresses with its owner.

Repeated horizontal traversal progressively compresses leftward provenance.

---

## 61.6 Continue Vertically

Given:

    A
      |
      C
      |
      B

if B descends again:

- lower context receives vertical allocation;
- B may vertically compress;
- distant ancestors may compress into horizontal provenance bars;
- immediate collection context remains recoverable.

---

## 61.7 Mixed Traversal

A node reached horizontally may descend through a collection.

A node reached vertically may open a singular reference.

The same rules apply recursively.

An occurrence may therefore become compressed in both axes.

---

## 61.8 Enter Edit Mode

Given persisted Node A:

1. invoke Edit from A's Node Action Bar;
2. stage A;
3. keep A in the same occurrence;
4. switch A to edit mode;
5. make permitted scalar and relationship affordances editable;
6. reflect active transaction state in the Canvas Action Bar.

---

## 61.9 Edit Scalar Property

Given staged A:

1. edit a scalar value through its Property/Value Visualizer;
2. update staged semantic state;
3. establish an Undo boundary when the interaction is complete;
4. retain navigation context.

---

## 61.10 Edit Array

Given staged A and array property P:

1. open P's Collection Tab;
2. use the Collection Visualizer;
3. add/remove/edit/reorder as permitted;
4. update staged state;
5. establish meaningful Undo boundary.

---

## 61.11 Edit Multi-Valued Relationship

Given staged A and plural relationship R:

1. open R's Collection Visualizer;
2. add or remove targets as permitted;
3. update A's staged relationship state;
4. retain ordinary collection navigation.

---

## 61.12 Edit Singular Relationship

Given staged A and singular R:

1. keep R in the right rail;
2. set/replace/clear target when permitted;
3. update A's staged relationship state;
4. continue to allow ordinary navigation to the current target.

---

## 61.13 Edit Related Holon Separately

Given staged A and related B:

1. navigate to B;
2. B initially remains read-only unless already staged;
3. invoke Edit on B;
4. B joins the active transaction;
5. A and B now contain independent semantic changes within one transaction.

---

## 61.14 Create

Given concrete type T:

1. invoke Create Instance;
2. stage new holon A;
3. display A in edit mode;
4. edit through normal visualizers;
5. A participates in the active transaction.

---

## 61.15 Clone

Given persisted A:

1. invoke Clone;
2. create staged B initialized from A;
3. display B in edit mode;
4. modify B;
5. B participates in the active transaction.

---

## 61.16 Delete

Given persisted A:

1. invoke Delete;
2. confirm if required;
3. stage semantic deletion;
4. reflect staged deletion state;
5. publish only when the Canvas transaction is committed.

---

## 61.17 Undo Across Multiple Holons

Given staged changes to A and B:

1. complete a meaningful edit gesture;
2. create Undo boundary;
3. make later edits;
4. invoke Undo from Canvas Action Bar;
5. Rust restores transaction state;
6. all affected visible occurrences refresh accordingly.

---

## 61.18 Commit Multiple Holons

Given:

    A [updated]
    B [created]
    C [relationship changed]
    D [deleted]

all staged in one transaction:

1. invoke Commit from the Canvas Action Bar;
2. validate the full transaction;
3. if valid, commit all staged state atomically according to MAP semantics;
4. refresh affected occurrences;
5. return staged visualizers to appropriate read state.

---

## 61.19 Compress While Editing

Given staged A:

1. traversal requires space;
2. A compresses normally;
3. staged state remains authoritative in Rust;
4. compact A indicates staged state;
5. re-expansion restores editing context.

---

# 62. Open Design Questions

The following remain intentionally unresolved.

## 62.1 Sibling History

When switching among singular affordances or collection rows:

- discard previous sibling;
- retain hidden history;
- preserve explicit branches?

Initial recommendation: replacement with recoverable local state.

---

## 62.2 Compression Thresholds

Exactly when should a visualizer become:

- partially compressed;
- fully compressed?

This should be informed by implementation experiments and available geometry.

---

## 62.3 Horizontal Overflow

If compression is insufficient:

- horizontal scrolling;
- panning;
- stronger ancestor collapse;
- another strategy?

---

## 62.4 Vertical Overflow

Likewise:

- vertical scrolling;
- panning;
- stronger compression?

---

## 62.5 Scalar Dance Results

Determine initial presentation and persistence semantics.

---

## 62.6 Dance Result Tabs

Should collection-valued dance affordances:

- have tabs before invocation;
- appear after invocation;
- appear in a distinct unexecuted state?

---

## 62.7 Empty Singular Relationships

Define the exact visual treatment of a singular affordance with no current target.

---

## 62.8 Branch Closing

Determine whether and how traversal branches can be explicitly pruned.

---

## 62.9 Focus Presentation

Define the visual treatment of the active frontier.

---

## 62.10 Transaction Abandon Semantics

Define exactly what happens when the person abandons or reverts an active transaction.

---

## 62.11 Multiple Occurrences of a Staged Holon

Define the precise visual synchronization behavior when one staged holon appears in multiple occurrences.

The semantic state remains singular and Rust-owned.

---

## 62.12 Relationship Target Selection

Define the generic UX used to select targets when editing relationships.

---

## 62.13 Deleted Holon Presentation

Define how staged and committed deleted holons appear within existing traversal provenance.

---

# 63. Non-Goals of the Initial Design

The initial Space Navigator does not need to fully support:

- arbitrary free-form Canvas positioning;
- draggable visualizer placement;
- graph auto-layout;
- unlimited simultaneous sibling branches;
- persistent Canvas sessions;
- collaborative Canvas state;
- complete mobile optimization;
- sophisticated animation;
- complete keyboard navigation;
- every specialized visualizer;
- production Visualizer Commons package loading;
- all adaptive scoring algorithms;
- arbitrary query construction.

These capabilities may evolve without changing the core design grammar.

---

# 64. Normative Design Invariants

## 64.1 Descriptor Semantics Over Runtime Accident

Declared cardinality and result shape determine structural presentation.

## 64.2 Visualizer Categories Are Roles

Do not equate a category such as Node Visualizer with one permanent concrete implementation.

## 64.3 Generic Fallbacks Preserve Basic Use

Previously unknown semantic types should remain usable when no specialized visualizer exists.

## 64.4 Singular Traversal Goes Right

Single-holon traversal extends horizontally.

## 64.5 Plural Traversal Goes Down

Multi-valued traversal extends vertically through a Collection Visualizer.

## 64.6 Navigation Preserves Provenance

Traversal should add or compress context rather than erase it.

## 64.7 Holon Identity Is Not Occurrence Identity

One holon may appear in multiple traversal contexts.

## 64.8 Child Content Claims Space Only When Activated

Navigation affordances may be visible before their child visualizers consume space.

## 64.9 Parent Geometry Constrains Subordinate Geometry

Compressed parents cannot leave full-size subordinate content behind.

## 64.10 Compression Preserves State

Compression changes presentation, not semantic or navigation state.

## 64.11 Read and Edit Share One Visual Grammar

Do not introduce separate browse and form architectures.

## 64.12 Staging Is Holon-Specific; Commit Is Transaction-Wide

Individual holons enter staged edit state.

The Canvas commits the active transaction.

## 64.13 Multiple Holons May Participate in One Transaction

The design MUST support concurrent staged changes to multiple holons.

## 64.14 Undo and Redo Are Canvas/Transaction Operations

They are not local Node history operations.

## 64.15 Editing Membership Is Not Editing the Target

Relationship mutation and target-holon mutation remain semantically distinct.

## 64.16 Immediate Personalization and Durable Adaptation Are Distinct

The visible experience changes immediately; persistent learning is handled through DAHN adaptive architecture.

## 64.17 Lazy Population, Early Structure

Build structural affordances from descriptors before retrieving potentially expensive contents.

---

# 65. Summary

The DAHN Space Navigator is a descriptor-driven, adaptive, two-dimensional Canvas for navigating and manipulating a MAP Space.

Its primary visual grammar is:

- **Node Visualizer** for a holon;
- **Vertical Single-Value Tab Rail** for singular holon affordances;
- **Horizontal Collection Tab Bar** for plural affordances;
- **Collection Visualizer** for homogeneous collections;
- **Canvas Action Bar** for transaction- and Canvas-scoped actions.

Its central semantic rule is:

> **Definitions determine structure; runtime data populates it.**

Its central navigation rule is:

> **Follow one thing horizontally; choose among many things vertically.**

Its central geometric rule is:

> **The Canvas allocates space toward the active traversal frontier and compresses provenance behind it.**

Its central editing rule is:

> **Read and edit are modes of the same descriptor-driven visual structure.**

Its central transaction rule is:

> **Holons are staged individually; the active transaction is committed collectively.**

Its central state rule is:

> **Compression hides presentation, not semantic, staged, or navigation state.**

Together, these rules allow the Space Navigator to support:

- unknown holon types;
- dynamically selected visualizers;
- recursive inspection;
- two-dimensional traversal;
- preserved provenance;
- adaptive personalization;
- Create;
- Edit;
- Clone;
- Delete;
- editable arrays;
- editable relationships;
- simultaneous editing of multiple holons;
- transaction-level Undo;
- transaction-level Redo;
- transaction-level Commit;

without introducing domain-specific screens or a separate editing framework.