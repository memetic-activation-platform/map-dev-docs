# DAHN Space Navigator Design Specification v0.10

## Status

Draft normative design specification.

## Change Log

| Version | Changes from prior version |
| --- | --- |
| v0.10 | Adds a Space Navigator-owned collapsible auxiliary information region, custom Visualizer definition inspection, occurrence-bound targeting, and responsive hosting. |
| v0.9 | Keeps Load Holons with its affording HolonSpace and initiation in HolonInspector's action bar; Space Navigator supplies the enclosing exploration context. |
| v0.8 | Separates Dancer roles and subject bindings from launch, Path Inspector, Holon Inspector, and Table Collection authority. |
| v0.7 | Replaces default visibility of empty relationships with progressive population-gated browsing; defines destination-first pending presentation and stable collection switching. |
| v0.6 | Defines column-oriented sorting semantics separately from table-level default row ordering, including descriptor-backed Sequence and Key defaults and occurrence-local restoration. |
| v0.5 | Defines the bounded DAHN Launch Experience: its narrative, application-shell boundary, readiness and handoff behavior, accessibility, observational-imagery provenance, and MVP deferrals. |
| v0.4 | Adds `LoadHolons` as a Space Navigator Action Bar operation, invoked as the canonical Dance through the active `HolonSpace`; defines Space-Navigator-scoped feedback and makes host source selection ingress rather than a second semantic loading protocol. |
| v0.3 | Baseline normative Space Navigator design specification. |

## Purpose

Space Navigator is a Dancer for exploring and manipulating the local MAP Space.
It owns experience roles, their semantic subject bindings, coordination, and
Space/transaction-scoped interaction. Canvas hosts the experience.

Its top-level RootedNavigation slot initially binds the local `HolonSpace`.
DAHN selection chooses a conforming Visualizer; Space Navigator does not require
Path Inspector's two-axis grammar. Selected Visualizers own their recursive child
composition. Node, PropertyMap, Value, and Collection roles beneath them are not
therefore direct Space Navigator responsibilities.

[DAHN architecture](../hx/dahn-arch.md) owns subsystem and semantic-state
boundaries. The [Space Navigator grammar](space-navigator-interaction-grammar.md)
owns Dancer interactions. Concrete navigation belongs to the selected
RootedNavigation Visualizer; the current [Path Inspector design](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md)
and its grammar are independent authorities.

---

# 1. Design Goals

## 1.1 Descriptor-Driven

Space Navigator obtains semantic subjects and effective affordances through MAP.
Its role composition remains descriptor-driven rather than hard-coded to known
domain types. Selected Visualizers interpret the properties, relationships,
Dances, cardinality, permissions, and editability supplied by those descriptors.

---

## 1.2 Generic

Space Navigator supports previously unknown Holon types by requesting applicable
Visualizers through the [DAHN selection policy](../hx/dahn-design-spec.md#14-dahn-visualizer-selection-service).
It does not choose a fallback implementation when selection or realization fails.
A selected RootedNavigation Visualizer may recursively compose specialized Node,
Collection, PropertyMap, Value, or Action Visualizers; those are its descendants,
not an additional list of direct Dancer slots.

---

## 1.3 Shape-Oriented

Semantic subject shape informs slot requirements and applicability through the
[Visualizer kinds](../hx/visualizers/index.md). The selected Visualizer decides
how it realizes those semantics. Space Navigator does not assign an axis or
presentation region from relationship cardinality.

---

## 1.4 Context-Preserving

The navigation role must preserve meaningful exploration context: the inspected
subject, how it was reached, the producing affordance, and relevant prior
navigation context. The selected Visualizer chooses how that context remains
visible or recoverable; Space Navigator does not prescribe lineage geometry.

---

## 1.5 Spatially Scalable

The navigation role must support sustained exploration within the host-provided
allocation while keeping prior context recoverable. Axis-specific compression
is Path Inspector's strategy, not a requirement on every RootedNavigation
substitute.

---

## 1.6 Unified Read and Edit Experience

The experience supports inspection and permitted editing without requiring a
separate application. Selected Visualizers own their view/edit presentation;
MAP owns staged semantics and the Dancer coordinates transaction interaction.

---

## 1.7 Incrementally Implementable

Delivery sequencing is defined in the [implementation plan](space-navigator-impl-plan.md).
Incremental delivery preserves the same composition boundaries.

---

## 1.8 DAHN Launch Experience

<a id="181-narrative-and-scenes"></a>
<a id="182-application-shell-boundary"></a>
<a id="183-readiness-handoff-and-control"></a>
<a id="184-observational-imagery-and-provenance"></a>

The [DAHN Launch Experience](../hx/dahn-launch-experience-design-spec.md) is an
application-shell presentation. It coordinates readiness and handoff without
becoming a Space Navigator-owned Visualizer or Dancer-selection mechanism.

---

# 2. Core Design Principles

## 2.1 Definitions Determine Structure

[Descriptor semantics](../hx/dahn-design-spec.md#8-descriptor-requirements-for-dahn)
distinguish declared cardinality from runtime population. Visualizers use those
inputs without turning them into a universal spatial grammar.

## 2.2 Navigation Determines Visibility

Visibility, focus, and navigation layout belong to the selected RootedNavigation
Visualizer. Space Navigator owns its direct experience-role allocation.

## 2.3 Descriptors Determine Editability

Descriptors and effective permissions determine editability; visibility does
not confer permission to mutate a subject.

## 2.4 Staged State Determines What Is Being Changed

The [architecture state boundary](../hx/dahn-arch.md#7-map-state-versus-experience-state)
distinguishes presentation state from authoritative staged semantics.

## 2.5 Compression Hides Presentation, Not State

Space Navigator preserves the [shared state-survival contract](../hx/dahn-design-spec.md#311-independent-state-and-experiential-authority)
when coordinating its roles. It does not define a child's compression strategy.

---

<a id="3-core-visual-roles"></a>

# 3. Direct Experience Roles

| Direct role | Subject / context binding | Required capability and ownership |
| --- | --- | --- |
| Space context | Local HolonSpace | Presents the space itself; when visual, requests a compatible Node realization through DAHN. |
| Afforded Dancers | Dancer affordances exposed by that HolonSpace | Composes access to the afforded Dancers; no concrete visual contract beyond established source behavior is presumed. |
| Rooted navigation | Initially the local HolonSpace; explicit new-context anchor where requested | RootedNavigation with recoverable context and bounded participation, specified below. |
| Space Navigator Action Bar | Space Navigator experience session and active MAP transaction | Coordinates Space/transaction-scoped actions, with selectable action presentations where supported. |

For each visual slot actually defined, Space Navigator supplies the slot,
accepted Visualizer contract/types, semantic subject, and applicable context to
DAHN selection. These role descriptions do not introduce schema relationships
or formal slot names beyond the existing design.

A future AgentSpace may extend HolonSpace with agent, social, governance,
membership, LifeCode, or We-Space affordances. Such roles are not prerequisites
of the current Space Navigator.

---

# 4. Space Navigator Experience Composition

## 4.1 Responsibility

The Space Navigator Dancer owns `HolonSpace`-specific orchestration, including:

- representing the `HolonSpace` and its afforded Dancers as experience concerns;
- selecting the navigation role rooted at that `HolonSpace`;
- using Holons `OwnedBy` the `HolonSpace` as initial heterogeneous semantic
  context;
- transaction-level interaction surface;
- coordination of selected role realizations.

The ownership topology (`HolonSpace` -> `OwnedBy` Holons) is semantic context,
not the complete navigation topology. Rooted Navigation unfolds its distinct,
interaction-derived topology through relationships traversed from the root and
may therefore extend beyond directly owned Holons.

The selected RootedNavigation Visualizer owns navigation realization and its
child roles. Space Navigator neither assigns those children nor dictates their
geometry. The local HolonSpace is a subject binding, not an implementation
dependency on HolonSpace inside the selected generic Visualizer.

---

## 4.2 Experience Structure

The Space Navigator consists conceptually of:

1. a pinned Space Navigator Action Bar;
2. the navigable Space Navigator area containing visualizer occurrences.

Conceptually:

    +------------------------------------------------------+
    | Space Navigator Action Bar                           |
    | Undo | Redo | Commit | ...                           |
    +------------------------------------------------------+
    |                                                      |
    | Rooted Navigation Visualizer                          |
    |                                                      |
    | Internal realization belongs to selected Visualizer  |
    |                                                      |
    +------------------------------------------------------+

The Space Navigator Action Bar remains pinned while traversal occurs beneath
it. It is Dancer chrome, not Canvas chrome.

---


## 4.3 RootedNavigation Slot Boundary

The slot requires the [RootedNavigation semantic capability](../hx/visualizers/structure/rooted-navigation/kind-spec.md),
rooted exploration through applicable Holon affordances, inspection of reached
subjects, recoverable navigation context, and participation within its supplied
allocation. Space Navigator supplies the initial local HolonSpace, effective
Theme and runtime context, and relevant agent/experience context. DAHN selection
resolves the slot under its normal compatibility and choice policy.

No contract here requires two axes, horizontal singular traversal, vertical
plural traversal, table placement, a sidebar, or Path Inspector's Node
compression states. Those choices belong to the selected realization and its
own slots. Path Inspector is the current conforming realization, not the slot's
permanent implementation identity.

## 4.4 New Exploration Contexts

The [Dancer interaction grammar](space-navigator-interaction-grammar.md#23-new-exploration-context-requests)
owns routing an explicit Holon anchor to a new exploration tab within the same
Space Navigator experience. Space Navigator owns the tab collection and each
tab's RootedNavigation slot; the selected Visualizer owns navigation within it.
The first tab is rooted at the local HolonSpace; an additional tab may bind a
different compatible anchor while retaining the same HolonSpace, Dancer, Theme,
and agent/runtime context. The enclosing Canvas and Window Manager context do
not change. Each tab retains independent occurrence topology and view state.

Read-only tabs share the Space Navigator-owned read transaction, bound references,
and semantic cache. Closing a tab disposes its presentation, not that transaction
or sibling tabs. Read and write transactions remain segregated; editing across
tabs requires an explicit policy before it is enabled. Re-root, branch close,
and focus are distinct intents. Failure or refusal preserves the source.

A future presentation option may detach an exploration tab into its own window.
Space Navigator remains the shared experience and read-transaction owner; the
Window Manager supplies the additional top-level context and display allocation.
Detachment moves the existing exploration presentation while preserving its
navigation state; it does not imply a new Dancer session, semantic copy, or
transaction. Window closure and reattachment behavior require a separate design.

## 4.5 Auxiliary Information Region

Space Navigator's experience composition owns a collapsible auxiliary region
outside its selected RootedNavigation Visualizer. The region has a stable desktop
location. While open, its width remains stable across focus changes, inspection
targets, and content updates. Opening or closing the region is an explicit layout
action that changes the allocation supplied to RootedNavigation; the selected
Visualizer continues to own layout within that allocation.

The first consumer is a custom Visualizer for shared Visualizer definition
holons, selected through a dedicated experience slot under DAHN's normal selection
policy. It leads with the selected Visualizer's display name and a plain-language description
of what it helps the user do. Built-in definitions supply purpose descriptions
through their holonic property contract. Internal identifiers, captured occurrence
provenance, slot name and accepted kind(s), properties, applicability, composition,
implementation, and token relationships remain accessible inside one initially
closed “Technical details” disclosure. Accepted kind labels come from the captured
slot's AcceptsVisualizerType declarations. The initial view does not ask users to
choose a Visualizer; eligible-alternative discovery and choice remain in later slices.
Definition
information remains distinct from VisualizerUsage configuration and history.

Each presented slot selection exposes a small lowercase circled v with the
selected Visualizer display name in its tooltip. Invoking that control captures the presentation occurrence, containing context,
actual slot and owner, presented subject, and selected Visualizer. Focus changes
and exploration-tab switches do not retarget an open inspection. A new explicit
v invocation can replace the current inspection session. While the information view
is visible, its live invoking v is highlighted as selected; replacing, hiding, or
dismissing the view clears the previous highlight. Initially there is one
information session for the Space Navigator experience; independent retained
sessions per exploration tab are not required. The view identifies its captured
subject and occurrence so that its binding stays clear across tab switches.

The definition heading offers the standard “Explore from here” icon. Explicit
activation opens the captured Visualizer holon as the root of a new exploration
using the ordinary RootedNavigation tab lifecycle. Reading information alone
does not navigate.

An initially closed “Presentation structure” disclosure exposes the live parts
of this presentation, distinguishing selected child Visualizers from regions
implemented by their containing Visualizer. It permits inspection of those parts;
it does not list candidates or change selection. In Table, its column entries
identify the Value Visualizer shared by every cell in the respective column.
Declared composition slots remain in Technical details. The consumed Theme token
list identifies the active Theme and shows the PresentationValue supplied by its
ThemeTokenAssignment for each exact DesignToken version. These are the validated
assignment values projected with the active Theme, not inferred CSS values.
Tokens not consumed by this Visualizer are omitted; an unavailable assignment is
identified explicitly rather than substituted from another Theme or token version.

Closing the inspected occurrence dismisses its information view and restores
focus to an appropriate surviving control. Explicit dismissal restores focus to
the live invoker where possible. Late asynchronous results must not populate a
closed or superseded inspection. Desktop target closure may leave the auxiliary
region open for another tool or inspection.

On narrow displays, the same region is presented as a full-width overlay within
the experience instead of reserving sidebar width. Its keyboard focus is contained
while open; closing it restores navigation and an appropriate focus target.
Exploration state and semantic targeting survive presentation changes.

Read-only inspection does not change the inspected definition, occurrence
selection, usage, or staged editing state. Realizing the custom presentation may
create transient invocation/projection holons through the established materialization
pipeline; it does not authorize staging or committing semantic changes.

Later choice slices may present Rust-authorized alternatives and support explicit
selection in this information experience. An alternatives list contains only other
Visualizers satisfying every selection criterion for the captured slot, owner, and
subject; it is never a global Visualizer catalog and may be empty. Discovery, usage selection, and safe
occurrence replacement remain governed by their separate contracts. Future tools
such as annotations or comments may share the auxiliary region, but each must
state whether its target is captured or follows focus.

# 5. Space Navigator Action Bar

## 5.1 Purpose

The Space Navigator Action Bar contains actions whose semantic scope is the
current Space Navigator experience session or active MAP transaction. A Canvas
may separately provide desktop-manager actions that launch, tile, focus, or
switch Dancer windows; it MUST NOT offer the Space Navigator's Undo or Redo.

These actions SHOULD NOT be repeated in every Node Visualizer.

---

## 5.2 Transaction Actions

The Space Navigator Action Bar SHOULD support transaction-scoped operations such as:

- Undo;
- Redo;
- Commit;
- transaction status;
- abandon/revert transaction where supported.

Because one transaction may contain staged changes to multiple holons, Commit belongs here rather than in an individual Node Visualizer.

---

## 5.3 Space Navigator Actions

The Space Navigator Action Bar MAY additionally contain:

- Space Navigator view controls;
- layout controls;
- Space Navigator-specific navigation controls;
- Space Navigator experience-visualization controls;
- other Space-Navigator-level operations.

`LoadHolons` belongs to its affording `HolonSpace` and is initiated through that
holon's [HolonInspector action bar](../hx/visualizers/node/holon-inspector/design-spec.md#holon-level-action-initiation).
Space Navigator supplies the enclosing exploration context. Source selection,
request preparation, and result presentation participate in the holon-level
action interaction; host ingress does not define a second semantic loading
protocol. Normal inspection reflects committed results through MAP-backed reads.

---

## 5.4 Personalization

The Space Navigator defines a set of Dancer-level actions and their relative semantic importance.

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
- property action → owning PropertyMap or Value Visualizer, according to its effect;
- collection action → Collection Visualizer;
- holon action → Node Visualizer;
- transaction action → Space Navigator Action Bar.

---

# 6. Active Traversal Frontier

See [Active Traversal Frontier](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md#active-traversal-frontier).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 7. Node Visualizer

<a id="71-responsibility"></a>
<a id="72-selection"></a>
<a id="73-inputs"></a>

See [Node Visualizer](../hx/visualizers/node/holon-inspector/design-spec.md#node-visualizer).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 8. Full Node Geometry

See [Full Node Geometry](../hx/visualizers/node/holon-inspector/design-spec.md#full-node-geometry).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 9. Node Title Bar

See [Node Title Bar](../hx/visualizers/node/holon-inspector/design-spec.md#node-title-bar).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 10. Node Action Bar

<a id="101-purpose"></a>
<a id="102-effective-dances"></a>
<a id="103-alternate-visualizers"></a>
<a id="104-compression"></a>

See [Node Action Bar](../hx/visualizers/node/holon-inspector/design-spec.md#node-action-bar).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 11. Property Viewer Pane

<a id="111-purpose"></a>
<a id="112-propertymap-and-value-visualizers"></a>
<a id="113-scalar-values"></a>
<a id="114-read-mode"></a>
<a id="115-edit-mode"></a>
<a id="116-property-ordering"></a>

See [Property Viewer Pane](../hx/visualizers/node/holon-inspector/design-spec.md#property-viewer-pane).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 12. Array-Valued Properties

See [Array-Valued Properties](../hx/visualizers/node/holon-inspector/design-spec.md#array-valued-properties).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 13. Vertical Single-Value Tab Rail

<a id="131-purpose"></a>
<a id="132-eligible-affordances"></a>
<a id="133-structural-presence"></a>
<a id="134-activation"></a>
<a id="135-personalization"></a>

See [Vertical Single-Value Tab Rail](../hx/visualizers/node/holon-inspector/design-spec.md#vertical-single-value-tab-rail).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 14. Editing Single-Valued Relationships

See [Editing Single-Valued Relationships](../hx/visualizers/node/holon-inspector/design-spec.md#editing-single-valued-relationships).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 15. Horizontal Collection Tab Bar

<a id="151-purpose"></a>
<a id="152-eligible-affordances"></a>
<a id="153-geometry"></a>
<a id="154-initial-state"></a>
<a id="155-activation"></a>
<a id="156-personalization"></a>

See [Horizontal Collection Tab Bar](../hx/visualizers/node/holon-inspector/design-spec.md#horizontal-collection-tab-bar).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 16. Relationship Presentation

<a id="161-cardinality-rule"></a>
<a id="162-singular-relationship"></a>
<a id="163-plural-relationship"></a>
<a id="164-progressive-relationship-affordances"></a>

See [Relationship Presentation](../hx/visualizers/node/holon-inspector/design-spec.md#relationship-presentation).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 17. Dance Result Presentation

<a id="171-descriptor-based-classification"></a>
<a id="172-single-holon-result"></a>
<a id="173-holon-collection-result"></a>
<a id="174-value-collection-result"></a>
<a id="175-scalar-result"></a>
<a id="176-no-result-dance"></a>

See [Dance Result Presentation](../hx/visualizers/node/holon-inspector/design-spec.md#dance-result-presentation).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 18. Collection Visualizer

<a id="181-responsibility"></a>
<a id="182-selection"></a>
<a id="183-geometry"></a>

See [Collection Visualizer](../hx/visualizers/collection/table/design-spec.md#collection-visualizer).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 19. Table Collection Visualizer

<a id="191-rows"></a>
<a id="192-columns"></a>
<a id="193-collection-header"></a>
<a id="194-column-operations"></a>
<a id="1941-column-oriented-sorting-semantics"></a>
<a id="1942-sort-state-lifetime"></a>
<a id="195-sequence-column"></a>
<a id="196-table-level-default-row-ordering"></a>

See [Table Collection Visualizer](../hx/visualizers/collection/table/design-spec.md#table-collection-visualizer).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 20. Editable Collection Visualizers

See [Editable Collection Visualizers](../hx/visualizers/collection/table/design-spec.md#editable-collection-visualizers).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 21. Editable Value Arrays

See [Editable Value Arrays](../hx/visualizers/collection/table/design-spec.md#editable-value-arrays).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 22. Editable Multi-Valued Relationships

See [Editable Multi-Valued Relationships](../hx/visualizers/collection/table/design-spec.md#editable-multi-valued-relationships).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 23. Dance Result Collection Editability

See [Dance Result Collection Editability](../hx/visualizers/collection/table/design-spec.md#dance-result-collection-editability).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 24. Semantic Editing Ownership

The Space Navigator MUST distinguish editing a relationship or collection from editing a contained target holon.

For example, if A has a `Friends` collection containing B:

- adding or removing B from `Friends` edits A;
- changing B's `name` edits B.

Visual containment MUST NOT imply semantic editing ownership.

---

# 25. Descriptor-to-Presentation Mapping

See [Descriptor-to-Presentation Mapping](../hx/visualizers/node/holon-inspector/design-spec.md#descriptor-to-presentation-mapping).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 26. Applying the Interaction Grammar

<a id="261-horizontal-navigation"></a>
<a id="262-vertical-navigation"></a>
<a id="263-recursive-exploration-and-provenance"></a>

See [Applying the Interaction Grammar](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md#applying-the-interaction-grammar).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 27. Focus and Concrete Extent Realization

See [Focus and Concrete Extent Realization](../hx/visualizers/node/holon-inspector/design-spec.md#focus-and-concrete-extent-realization).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 28. Compression and Editing

See [Compression and Editing](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md#compression-and-editing).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 29. Loading States

See [Loading States](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md#loading-states).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 30. Progressive Retrieval

See [Progressive Retrieval](../hx/visualizers/node/holon-inspector/design-spec.md#progressive-retrieval).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 31. Entering Edit Mode

See [Entering Edit Mode](../hx/visualizers/node/holon-inspector/design-spec.md#entering-edit-mode).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 32. Continuous Preservation of Staged Work

In-progress staged work is preserved by MAP snapshot mechanisms.

The person SHOULD NOT need a conventional Save button merely to protect work from loss.

The design therefore distinguishes:

- preservation of staged work;
- explicit transaction Commit.

---

# 33. Multiple Holons in Edit Mode

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

# 34. Staged State and Visualizer Occurrences

Visualizer occurrence state and staged semantic state are distinct.

If the same holon appears in multiple occurrences while staged:

- all occurrences ultimately reflect the same authoritative staged semantic state;
- TypeScript MUST NOT create independent semantic edit copies for each occurrence.

The exact synchronization presentation may evolve, but semantic divergence MUST NOT occur silently.

---

# 35. Editing While Navigating

See [Editing While Navigating](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md#editing-while-navigating).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 36. Compressing Editable Visualizers

See [Compressing Editable Visualizers](../hx/visualizers/node/holon-inspector/design-spec.md#compressing-editable-visualizers).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 37. Create

See [Create](../hx/visualizers/node/holon-inspector/design-spec.md#create).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 38. Clone

See [Clone](../hx/visualizers/node/holon-inspector/design-spec.md#clone).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 39. Delete

See [Delete](../hx/visualizers/node/holon-inspector/design-spec.md#delete).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 40. Commit

Commit is exposed in the pinned Space Navigator Action Bar.

It applies to the **entire active transaction**, which may include:

- updated holons;
- newly created holons;
- clones;
- relationship changes;
- array changes;
- staged deletions.

It is not a Node Visualizer action.

---

# 41. Commit Flow

When Commit is invoked:

1. the active staged transaction is validated;
2. applicable validation errors are returned if present;
3. if valid, MAP commits the transaction;
4. affected visualizers refresh from committed state;
5. affected staged visualizers return to read presentation;
6. navigation provenance remains intact.

Commit is a transaction-state transition, not a navigation transition.

---

# 42. Commit Failure

If validation or Commit fails:

- staged transaction state remains intact;
- affected visualizers remain in edit mode;
- the person may correct the staged state and retry;
- errors SHOULD appear as close as practical to affected visualizers;
- the Space Navigator MAY also display a transaction-level summary.

Failure MUST NOT silently discard staged work.

---

# 43. Undo and Redo

Undo and Redo are exposed in the pinned Space Navigator Action Bar.

They apply to the active transaction.

They MUST operate on Rust-owned staged semantic state rather than merely reversing TypeScript presentation.

---

# 44. Undo Boundaries

TypeScript determines when a meaningful UX interaction constitutes a new Undo boundary.

Examples may include:

- completing a property edit;
- adding/removing a relationship target;
- completing an array mutation;
- completing another semantically meaningful editing gesture.

Low-level preservation snapshots need not correspond one-to-one with user-visible Undo steps.

---

# 45. Undo Flow

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

# 46. Redo Flow

Redo restores the next recoverable transaction snapshot and refreshes affected presentation.

Its availability SHOULD be reflected in the Space Navigator Action Bar.

---

# 47. Abandon or Revert Transaction

The Space Navigator SHOULD eventually provide a clear transaction-level mechanism for abandoning or reverting staged work.

The exact user-facing term and semantics remain to be finalized.

Possible semantics include:

- revert entire active transaction to its starting state;
- abandon all staged changes;
- preserve recoverable staged state for later resumption.

The behavior MUST be explicit and MUST NOT silently lose work.

---

# 48. Adaptive and Personalizable Interactions

See [Adaptive and Personalizable Interactions](../hx/visualizers/node/holon-inspector/design-spec.md#adaptive-and-personalizable-interactions).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 49. Personalization and Constrained Geometry

See [Personalization and Constrained Geometry](../hx/visualizers/node/holon-inspector/design-spec.md#personalization-and-constrained-geometry).
This behavior belongs to the selected Visualizer, not to the Space Navigator Dancer.

---

---

# 50. Interaction Scenarios

## 50.1 Inspect a Holon

See [Inspect a Holon](../hx/visualizers/node/holon-inspector/design-spec.md#inspect-a-holon).

## 50.2 Open a Multi-Valued Relationship

See [Open a Multi-Valued Relationship](../hx/visualizers/node/holon-inspector/design-spec.md#open-a-multi-valued-relationship).

## 50.3 Navigate Through a Collection

See [Navigate Through a Collection](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md#navigate-through-a-collection).

## 50.4 Follow a Singular Relationship

See [Follow a Singular Relationship](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md#follow-a-singular-relationship).

## 50.5 Continue Horizontally

See [Continue Horizontally](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md#continue-horizontally).

## 50.6 Continue Vertically

See [Continue Vertically](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md#continue-vertically).

## 50.7 Mixed Traversal

See [Mixed Traversal](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md#mixed-traversal).

## 50.8 Enter Edit Mode

See [Enter Edit Mode](../hx/visualizers/node/holon-inspector/design-spec.md#enter-edit-mode).

## 50.9 Edit Scalar Property

See [Edit Scalar Property](../hx/visualizers/node/holon-inspector/design-spec.md#edit-scalar-property).

## 50.10 Edit Array

See [Edit Array](../hx/visualizers/node/holon-inspector/design-spec.md#edit-array).

## 50.11 Edit Multi-Valued Relationship

See [Edit Multi-Valued Relationship](../hx/visualizers/node/holon-inspector/design-spec.md#edit-multi-valued-relationship).

## 50.12 Edit Singular Relationship

See [Edit Singular Relationship](../hx/visualizers/node/holon-inspector/design-spec.md#edit-singular-relationship).

## 50.13 Edit Related Holon Separately

See [Edit Related Holon Separately](../hx/visualizers/node/holon-inspector/design-spec.md#edit-related-holon-separately).

## 50.14 Create

See [Create](../hx/visualizers/node/holon-inspector/design-spec.md#create).

## 50.15 Clone

See [Clone](../hx/visualizers/node/holon-inspector/design-spec.md#clone).

## 50.16 Delete

See [Delete](../hx/visualizers/node/holon-inspector/design-spec.md#delete).

## 50.17 Undo Across Multiple Holons

Given staged changes to A and B:

1. complete a meaningful edit gesture;
2. create Undo boundary;
3. make later edits;
4. invoke Undo from Space Navigator Action Bar;
5. Rust restores transaction state;
6. all affected visible occurrences refresh accordingly.

---

## 50.18 Commit Multiple Holons

Given:

    A [updated]
    B [created]
    C [relationship changed]
    D [deleted]

all staged in one transaction:

1. invoke Commit from the Space Navigator Action Bar;
2. validate the full transaction;
3. if valid, commit all staged state atomically according to MAP semantics;
4. refresh affected occurrences;
5. return staged visualizers to appropriate read state.

---

## 50.19 Compress While Editing

See [Compress While Editing](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md#compress-while-editing).

---

# 51. Open Design Questions

## 51.1 Sibling History

See [Sibling History](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md#sibling-history).

## 51.2 Compression Thresholds

See [Compression Thresholds](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md#compression-thresholds).

## 51.3 Horizontal Overflow

See [Horizontal Overflow](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md#horizontal-overflow).

## 51.4 Vertical Overflow

See [Vertical Overflow](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md#vertical-overflow).

## 51.5 Scalar Dance Results

See [Scalar Dance Results](../hx/visualizers/node/holon-inspector/design-spec.md#scalar-dance-results).

## 51.6 Dance Result Tabs

See [Dance Result Tabs](../hx/visualizers/node/holon-inspector/design-spec.md#dance-result-tabs).

## 51.7 Empty Singular Relationships

See [Empty Singular Relationships](../hx/visualizers/node/holon-inspector/design-spec.md#empty-singular-relationships).

## 51.8 Branch Closing

See [Branch Closing](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md#branch-closing).

## 51.9 Focus Presentation

See [Focus Presentation](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md#focus-presentation).

## 51.10 Transaction Abandon Semantics

Define exactly what happens when the person abandons or reverts an active transaction.

---

## 51.11 Multiple Occurrences of a Staged Holon

See [Multiple Occurrences of a Staged Holon](../hx/visualizers/node/holon-inspector/design-spec.md#multiple-occurrences-of-a-staged-holon).

## 51.12 Relationship Target Selection

See [Relationship Target Selection](../hx/visualizers/node/holon-inspector/design-spec.md#relationship-target-selection).

## 51.13 Deleted Holon Presentation

See [Deleted Holon Presentation](../hx/visualizers/node/holon-inspector/design-spec.md#deleted-holon-presentation).

---

# 52. Non-Goals of the Initial Design

The initial integrated delivery may defer the following capabilities. Items
concerning a Visualizer are delivery limits on that realization, not requirements
that Space Navigator imposes on every substitute:

- arbitrary free-form positioning within the Canvas;
- draggable visualizer placement;
- graph auto-layout;
- unlimited simultaneous sibling branches;
- persistent Space Navigator sessions;
- collaborative Space Navigator state;
- complete mobile optimization;
- sophisticated animation;
- complete keyboard navigation;
- every specialized visualizer;
- production Visualizer Commons package loading;
- all adaptive scoring algorithms;
- arbitrary query construction.

These capabilities may evolve within their owning components without changing
Space Navigator's direct-role contract.

---

# 53. Normative Design Invariants

## 53.1 Descriptor Semantics Over Runtime Accident

Declared cardinality and result shape determine structural presentation.

## 53.2 Visualizer Categories Are Roles

Do not equate a category such as Node Visualizer with one permanent concrete implementation.

<a id="533-generic-fallbacks-preserve-basic-use"></a>

## 53.3 Generic Candidates Preserve Basic Use

Generic candidates obey the [DAHN selection policy](../hx/dahn-design-spec.md#14-dahn-visualizer-selection-service).
Absence is an explicit error; neither this Dancer nor its client chooses a
hard-coded fallback.

## 53.4 Singular Traversal Goes Right

See [Singular Traversal Goes Right](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md#10-grammar-invariants).

## 53.5 Plural Traversal Goes Down

See [Plural Traversal Goes Down](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md#10-grammar-invariants).

## 53.6 Navigation Preserves Provenance

See [Navigation Preserves Provenance](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md#10-grammar-invariants).

## 53.7 Holon Identity Is Not Occurrence Identity

See [Holon Identity Is Not Occurrence Identity](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md#10-grammar-invariants).

## 53.8 Child Content Claims Space Only When Activated

See [Child Content Claims Space Only When Activated](../hx/visualizers/node/holon-inspector/design-spec.md#child-content-claims-space-only-when-activated).

## 53.9 Parent Geometry Constrains Subordinate Geometry

See [Parent Geometry Constrains Subordinate Geometry](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md#10-grammar-invariants).

## 53.10 Compression Preserves State

See [Compression Preserves State](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md#10-grammar-invariants).

## 53.11 Read and Edit Share One Visual Grammar

See [Read and Edit Share One Visual Grammar](../hx/visualizers/node/holon-inspector/design-spec.md#read-and-edit-share-one-visual-grammar).

## 53.12 Staging Is Holon-Specific; Commit Is Transaction-Wide

Individual holons enter staged edit state.

The Space Navigator commits the active transaction.

## 53.13 Multiple Holons May Participate in One Transaction

The design MUST support concurrent staged changes to multiple holons.

## 53.14 Undo and Redo Are Space Navigator/Transaction Operations

They are not local Node history operations.

## 53.15 Editing Membership Is Not Editing the Target

Relationship mutation and target-holon mutation remain semantically distinct.

## 53.16 Immediate Personalization and Durable Adaptation Are Distinct

The visible experience changes immediately; persistent learning is handled through DAHN adaptive architecture.

## 53.17 Lazy Population, Early Structure

See [Lazy Population, Early Structure](../hx/visualizers/node/holon-inspector/design-spec.md#lazy-population-early-structure).

---

# 54. Summary

Space Navigator binds the local HolonSpace to a RootedNavigation role and
coordinates its direct experience roles and transaction-level actions.
It can host a conforming alternative with a different navigation layout without
adopting that Visualizer's internal grammar. MAP owns semantic and staged state;
selected Visualizers own their experiential realization and recursive children.

Inspection, Create, Clone, Delete, property/relationship editing, and navigation
remain available through the composed experience. Their concrete controls belong
to the appropriate selected Visualizer; Commit, Undo, and Redo remain scoped to
the active transaction and exposed by the Dancer.

<a id="slot-directed-selection-alignment"></a>

## Selection authority

Direct Dancer roles and recursively requested children use the
[DAHN slot-directed selection policy](../hx/dahn-design-spec.md#1421-slot-directed-descriptor-selection).
Each slot narrows eligible candidates; subject applicability and selection policy
resolve the selected Visualizer within that boundary.
