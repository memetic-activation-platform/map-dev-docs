# Editing and Staged State

## Purpose

The Space Navigator MUST support editing as a state of the same descriptor-driven visual structure used for inspection and navigation.

Editing SHOULD NOT introduce a separate form system or a separate class of editing screens.

Instead:

> Read and edit are modes of the same descriptor-driven visual structure.

The same Node Visualizers, Collection Visualizers, Property Visualizers, and Value Type Visualizers used for read-only presentation SHOULD become editable when operating against staged state and when the applicable descriptors and permissions allow mutation.

A second governing principle is:

> Navigation determines what is visible; descriptors determine what is editable; staged state determines what is currently being changed.

---

## Staged Editing Model

Editing an existing persisted holon SHOULD create or expose a staged new version of that holon.

The Node Visualizer remains in place and transitions from read-only mode to edit mode.

Conceptually:

    persisted holon
          |
        Edit
          |
    staged new version
          |
    editable Node Visualizer
          |
       Commit
       /    \
    success  failure
       |       |
    new       staged state
    persisted remains editable
    head

The visualizer SHOULD preserve its navigation context while entering and leaving edit mode.

Editing SHOULD therefore be understood as a state transition of a visualizer occurrence, not as navigation to a different screen.

---

## Continuous Snapshotting

DAHN assumes continuous snapshotting of staged work.

The user SHOULD NOT need to invoke an explicit Save operation merely to prevent loss of in-progress edits.

Changes made while editing SHOULD be continuously preserved in staged state according to the underlying snapshotting mechanism.

Because of this, the operation that publishes staged changes SHOULD be treated semantically as **Commit**, not merely Save.

A Commit represents a significant transition:

- staged state is validated;
- the new state is committed to the Space;
- committed data becomes part of the durable shared history;
- the resulting committed version is immutable according to MAP semantics.

The exact user-facing label MAY later be refined, but the underlying semantic boundary is a commit boundary rather than a save boundary.

---

## Entering Edit Mode

When the user selects **Edit** for a persisted holon:

1. DAHN SHOULD stage a new version of the current holon.
2. The existing Node Visualizer occurrence SHOULD transition into edit mode.
3. The Property Viewer Pane SHOULD become editable.
4. Editable relationships and collections SHOULD expose their applicable mutation affordances.
5. Existing navigation context SHOULD remain intact.

The visual geometry SHOULD remain fundamentally the same.

The user is editing the holon they were already inspecting rather than opening a separate editing experience.

---

## Property Editing

The Node Visualizer SHOULD delegate rendering and interaction for individual property values to the appropriate Property Visualizer and Value Type Visualizer.

This delegation applies in both read and edit modes.

Conceptually:

    Property Descriptor
          |
    Value Type Descriptor
          |
    Applicable Visualizer
          |
      +---+---+
      |       |
    Read     Edit
    mode     mode

In read mode, the visualizer presents the value.

In edit mode, the same descriptor-driven visualizer SHOULD expose the interaction model appropriate to that value type.

Examples may include:

- text entry;
- numeric input;
- date selection;
- enumeration selection;
- boolean controls;
- structured value editors;
- reference selectors.

The Node Visualizer SHOULD NOT contain type-specific editing logic for individual value types.

---

## Editable State Is Descriptor-Driven

A value being visible does not imply that it is editable.

Editability SHOULD be determined from applicable descriptors, policies, roles, permissions, and structural semantics.

The visualizer SHOULD therefore distinguish between:

- visible and editable;
- visible but read-only;
- unavailable due to permissions;
- structurally immutable.

The same principle applies to properties, relationships, collections, and dances.

---

## Commit

An editable Node Visualizer SHOULD expose a Commit affordance.

When Commit is invoked:

1. staged state SHOULD be validated;
2. all applicable staged changes SHOULD be prepared for commit;
3. the underlying commit operation SHOULD execute;
4. success or failure SHOULD be reported to the visualizer.

On successful commit:

- the resulting committed version becomes the current persisted state;
- the Node Visualizer SHOULD return to read-only mode;
- the visualizer SHOULD display the newly committed state;
- navigation provenance SHOULD remain intact.

The user SHOULD remain in the same location within the Space Navigator.

A successful commit is therefore a state transition, not a navigation transition.

---

## Commit Failure

If validation or commit fails:

- the Node Visualizer SHOULD remain in edit mode;
- staged changes SHOULD remain available;
- the user SHOULD be able to correct the problem and attempt Commit again;
- the failure SHOULD NOT discard staged work.

Validation feedback SHOULD eventually be presented as close as practical to the affected property, relationship, or collection element.

Global validation failures MAY also be surfaced at the Node Visualizer level.

---

## Cancel or Abandon Editing

The design SHOULD eventually provide an explicit way to stop editing without committing the staged changes.

The exact user-facing terminology remains open.

Possible semantics include:

- abandon staged changes;
- revert to the persisted version;
- close the current editing session while retaining recoverable staged state.

Because continuous snapshotting is in use, "Cancel" requires more careful semantics than in a conventional transient form.

The initial implementation SHOULD define explicitly whether leaving edit mode:

- destroys staged state;
- preserves staged state for later recovery;
- or requires the user to choose.

---

## Clone

The Action Bar MAY expose a **Clone** operation for holons where cloning is permitted.

Clone SHOULD:

1. create a new staged holon initialized from the current holon;
2. preserve applicable values according to clone semantics;
3. assign the new holon its own identity;
4. present the new staged holon in an editable Node Visualizer.

After initialization, editing a clone SHOULD use the same interaction model as editing any other staged holon.

Conceptually:

    persisted holon A
          |
        Clone
          |
    staged holon B
          |
    editable Node Visualizer
          |
       Commit
          |
    persisted holon B

The Node Visualizer SHOULD NOT require a special clone-editing mode.

Clone is simply another way of initializing staged state.

The source holon MAY remain known internally for provenance or audit purposes, but cloning SHOULD NOT automatically create Space Navigator traversal provenance between the source and clone merely because the clone operation occurred.

---

## Create

Creation SHOULD converge on the same staged editing model.

A preferred generic entry point is a concrete Holon Type descriptor.

When viewing an applicable concrete type descriptor, the Action Bar MAY expose **Create Instance**.

Invoking Create Instance SHOULD:

1. create a new staged holon of the selected type;
2. create it within the currently active Space;
3. initialize any applicable defaults;
4. present the new holon in an editable Node Visualizer;
5. allow the user to populate its editable values;
6. Commit it using the same commit flow used for Edit and Clone.

Conceptually:

    Concrete Holon Type
          |
    Create Instance
          |
    staged new holon
          |
    editable Node Visualizer
          |
       Commit
          |
    persisted new holon

Create, Clone, and Edit therefore converge after staged state has been initialized.

---

## Unified Editable Node State

The implementation SHOULD avoid separate editing components for Edit, Clone, and Create.

Once staged state exists, all three SHOULD use the same editable Node Visualizer.

| Operation | Staged state initialized from | Resulting UI |
| --- | --- | --- |
| Edit | Current persisted holon | Editable Node Visualizer |
| Clone | Copy of current holon | Editable Node Visualizer |
| Create | Concrete type descriptor | Editable Node Visualizer |

The distinction between these operations belongs primarily to staged-state initialization and eventual commit semantics, not to the editing UI.

---

## Delete

The Action Bar MAY expose a **Delete** operation where deletion is permitted.

Delete SHOULD follow MAP deletion semantics.

It SHOULD NOT imply physical erasure of historical data.

Instead, deletion SHOULD stage or create the appropriate deleted state and commit it according to the underlying MAP model.

Because deletion affects shared durable state, the UI SHOULD require an explicit user action appropriate to the consequence.

After successful deletion, the Node Visualizer SHOULD transition to an appropriate read-only representation indicating that the holon is deleted or no longer active.

Exact post-delete navigation behavior remains to be specified.

---

## Editable Collections

Collection Visualizers SHOULD support edit mode when the collection represents editable state belonging to the holon being edited.

The Collection Visualizer SHOULD remain the same visual component used in read-only mode.

Editing SHOULD add mutation affordances appropriate to the semantic source of the collection.

### Value Arrays

For an editable array-valued property, the Collection Visualizer MAY support operations such as:

- add value;
- remove value;
- edit value;
- reorder values where ordering is semantically meaningful and permitted.

Each value SHOULD continue to delegate presentation and editing to the appropriate Value Type Visualizer.

### Multi-Valued Relationships

For an editable multi-valued relationship, the Collection Visualizer MAY support:

- add relationship target;
- remove relationship target;
- reorder targets where ordering semantics allow it.

Adding or removing relationship targets modifies the staged relationship state of the holon being edited.

### Dance Result Collections

A collection produced as a dance result is not inherently editable merely because it is displayed by a Collection Visualizer.

Its editability depends on the semantics of the result and any associated mutation affordances.

The Collection Visualizer SHOULD therefore distinguish collection presentation from ownership of editable state.

---

## Single-Valued Relationship Editing

Single-valued relationships SHOULD follow the same principle as collection-valued relationships.

When permitted, edit mode MAY expose operations such as:

- set target;
- replace target;
- clear target.

These operations modify the staged relationship state of the holon being edited.

The relationship remains structurally single-valued based on its descriptor regardless of whether its current target is present.

---

## Semantic Ownership Boundary

The Space Navigator MUST distinguish between:

- editing the structure or relationships of the holon currently in edit mode;
- editing another holon that happens to be visible through one of its relationships or collections.

For example, if Person A is being edited and Person B appears as a row in A's `Friends` relationship collection:

- adding B to or removing B from A's `Friends` collection is an edit to A's relationship state;
- changing B's `name` property is an edit to B.

Editing B's properties SHOULD therefore require entering edit mode on B's own Node Visualizer.

Visibility within an editable collection does not transfer ownership of the target holon's properties to the containing holon.

The edit boundary SHOULD follow semantic ownership rather than visual containment.

---

## Editing Across the Visualizer Hierarchy

An editable Node Visualizer SHOULD coordinate the editability of its constituent visualizers.

Conceptually:

    Editable Node Visualizer
        |
        +-- editable scalar Property Visualizers
        |
        +-- editable Value Type Visualizers
        |
        +-- editable single-valued relationship affordances
        |
        +-- editable Collection Visualizers
                |
                +-- editable values
                |
                +-- editable relationship membership

This editability is recursive in presentation but bounded by semantic ownership.

---

## Navigation While Editing

Entering edit mode SHOULD NOT inherently disable navigation.

The user MAY continue to inspect related holons and collections while staged changes exist.

The Space Navigator SHOULD preserve the distinction between:

- navigation state;
- staged editing state.

A Node Visualizer occurrence MAY therefore remain part of a traversal path while also containing staged changes.

The implementation SHOULD eventually define behavior for cases such as:

- navigating away from a node with uncommitted staged changes;
- collapsing a node while it is being edited;
- opening multiple visualizer occurrences for the same holon while one occurrence has staged edits;
- encountering the staged holon elsewhere in the same Canvas.

These cases SHOULD preserve staged work and MUST NOT silently discard it.

---

## Collapsing Editable Visualizers

Compression and collapse SHOULD hide presentation without destroying staged editing state.

If an editable Node Visualizer is compressed:

- its staged values SHOULD remain intact;
- its edit mode SHOULD remain known;
- its collapsed representation SHOULD indicate that staged changes exist;
- restoring the visualizer SHOULD restore the editable state.

Similarly, if an editable Collection Visualizer is compressed, its staged collection modifications SHOULD remain intact.

This follows the broader Space Navigator principle:

> Compression hides presentation, not state.

---

## Staged State and Visualizer Occurrences

Staged state and visualizer occurrence state SHOULD remain conceptually distinct.

A visualizer occurrence records presentation and navigation concerns such as:

- location;
- provenance;
- expansion state;
- selected tabs;
- focus.

Staged state records changes to MAP data.

The implementation SHOULD avoid coupling staged data identity directly to a particular visualizer occurrence.

This matters because the same holon MAY appear in multiple visualizer occurrences while participating in one staged editing context.

The exact synchronization model for multiple occurrences remains to be specified.

---

## Initial Editing Invariants

The implementation SHOULD preserve the following invariants.

### Same Visualizer, Different Mode

Read-only and editable presentation SHOULD use the same Node and Collection Visualizer abstractions.

### Staging Before Mutation

User edits SHOULD apply to staged state rather than directly mutating committed state.

### Commit Is Explicit

Continuous snapshotting protects work, but durable publication to the Space requires an explicit Commit.

### Commit Does Not Navigate

A successful Commit SHOULD update the current visualizer state rather than replace it with a new navigation context.

### Descriptor-Driven Interaction

Property and value descriptors SHOULD determine both read presentation and edit interaction.

### Collection Editing Reuses Collection Visualizers

Array and relationship editing SHOULD extend the Collection Visualizer rather than introduce separate list-editing forms.

### Semantic Ownership Governs Mutation

Editing a collection member's own properties is distinct from editing its membership in the containing collection.

### Compression Preserves Staged State

Collapsing or compressing visualizers MUST NOT discard staged changes.

---

## Initial Editing Scenarios

### Edit an Existing Holon

Given a persisted holon displayed in a Node Visualizer:

1. The user invokes Edit.
2. A staged new version is created.
3. The existing Node Visualizer enters edit mode.
4. Editable property values become interactive.
5. Applicable relationship mutation affordances become available.
6. Changes are continuously snapshotted.
7. The user invokes Commit.
8. Validation and commit execute.
9. On success, the visualizer returns to read-only mode displaying the newly committed version.

---

### Clone a Holon

Given a persisted holon:

1. The user invokes Clone.
2. A new staged holon is initialized from the source.
3. The new holon is displayed in an editable Node Visualizer.
4. The user modifies values as needed.
5. The user commits.
6. A new persisted holon is created.

---

### Create an Instance

Given a concrete Holon Type descriptor:

1. The user invokes Create Instance.
2. A new staged holon of that type is created in the active Space.
3. The new holon is displayed in an editable Node Visualizer.
4. Descriptor-driven property visualizers provide the appropriate editing interactions.
5. The user commits.
6. The new holon becomes persisted.

---

### Edit a Value Array

Given an editable holon with an array-valued property:

1. The user enters Edit mode.
2. The array's Collection Tab exposes its Collection Visualizer.
3. The user adds, removes, edits, or reorders values as permitted.
4. Changes modify the holon's staged state.
5. Commit persists the resulting new holon version.

---

### Edit a Multi-Valued Relationship

Given an editable holon with a multi-valued relationship:

1. The relationship remains represented by its Collection Visualizer.
2. Edit mode exposes add/remove target affordances.
3. The user modifies relationship membership.
4. Those modifications become part of staged state.
5. Commit publishes the resulting relationship changes.

---

### Edit a Collection Member Holon

Given an editable holon A and a collection containing holon B:

1. The user may modify whether B participates in A's collection if permitted.
2. The user does not edit B's own properties through A's collection editing state.
3. To edit B itself, the user navigates to B's Node Visualizer.
4. The user explicitly enters edit mode for B.

---

## Open Editing Questions

The following questions remain to be resolved through further design and implementation experience:

- What exact user-facing term should represent Commit?
- What are the semantics of Cancel or Abandon in the presence of continuous snapshotting?
- How are staged edits represented when the same holon appears in multiple visualizer occurrences?
- Can more than one holon be in edit mode simultaneously within a Space Navigator?
- Does Commit operate on one staged holon, the entire transaction, or a broader staged change set?
- How should validation errors be presented across properties, relationships, and collections?
- How should deleted holons remain represented in an existing traversal path?
- How should creation be initiated when the user does not begin from a type descriptor?
- How are selectors presented when setting or adding relationship targets?
- Which collection operations are determined by descriptor semantics versus visualizer capability?
- How should editing indicators survive horizontal and vertical compression?

These questions SHOULD remain explicit rather than forcing premature assumptions into the initial implementation.