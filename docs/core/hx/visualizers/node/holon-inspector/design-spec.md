# Holon Inspector Design Specification

## Status and current authority

Draft normative specification for this concrete Node Visualizer. Shared kind
and DAHN contracts retain their own authority. This document owns its private
composition, descriptor projection, responsive realization, and editing presentation.

## Purpose and authority

Holon Inspector is a concrete Visualizer in the
[Node family](../kind-spec.md). Its specification owns the experiential
realization behind the slot contract it fulfills.

## Contract fulfillment and semantic subject

One Active Holon and its effective descriptor-derived affordances.

The selecting parent's slot establishes the required contract and participation
constraints. DAHN selection resolves that boundary. Classification as Node
is not a claim that this implementation satisfies every conceivable Node slot.

## Direct child roles and subject bindings

These six slots describe this implementation, not every Node Visualizer.
Each actual child request supplies its owner-declared slot, bound subject, and
context to [DAHN selection](../../../dahn-design-spec.md#1421-slot-directed-descriptor-selection).
The slot filters accepted Visualizer types; subject applicability and selection
policy resolve a candidate. Neither this inventory nor kind membership supplies
an undeclared accepted type or permits a hard-coded implementation.

| Role | Subject or binding context | Boundary |
| --- | --- | --- |
| NodeTitleBarSlot | Bound Holon identity/title context | Title/header realization; accepted type descriptor remains unspecified. |
| ActionBarSlot | Applicable executable affordances and invocation context | Action-bar composition; accepted bar type remains unspecified. Individual actions are separate Action requests. |
| VerticalRailSlot | Singular relationship and navigational Dance affordances of the bound Holon | Singular affordance presentation; accepted rail type remains unspecified. |
| PropertyMapSlot | Property facet of the bound Holon, derived from its effective descriptor | [PropertyMap](../../property-map/kind-spec.md) owns set-level composition, including label/value pairing; no intervening Property Visualizer. |
| CollectionTabsSlot | Collection-shaped affordances of the bound Holon | Affordance index, not the resulting collection; accepted tab-index type remains unspecified. |
| CollectionViewerSlot | The active collection exposed by the chosen affordance | Collection family; active collection is the subject, source affordance supplies provenance. |

Exact accepted type descriptors for the title, action bar, rail, and tab index
remain open design details. No new kinds or runtime contract schema are implied.
PropertyMap selection is anchored at the bound owner Holon’s HolonType; Collection
selection follows DAHN’s dedicated collection-subject contract. Child loading
errors remain explicit; they do not authorize renderer substitution.

## Internal behavior and state

Internal information architecture, affordance projection, local loading/editing presentation, and responsive allocation among its own children. Navigation topology and outer allocation remain with its parent.

Authoritative MAP data and staged transaction state remain with MAP/Rust.
This Visualizer's presentation state does not become a second semantic model.

## Parent and child boundaries

The parent owns the external allocation and requirements at its slot boundary.
This Visualizer owns internal realization and directly defined child slots.
It does not prescribe the private composition of selected children. Agent-specific
configuration and usage belong to VisualizerUsage; the Visualizer fulfills the
slot contract.

## Concrete presentation

The following Node-specific behavior describes Holon Inspector. References to
rails, panes, tabs, and compression realizations are its private grammar. Parent
navigation effects refer to Path Inspector's participation context, not every
possible parent. MAP remains the authority for semantic edit operations.

## Node Visualizer

### Responsibility

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

### Selection

A composition owner requests a Node Visualizer through DAHN selection.
Holon Inspector is an ordinary generic candidate, not a hard-coded fallback.
Selection/materialization follows the canonical DAHN contract. A conforming
substitute may replace it if it satisfies the parent's slot requirements;
it need not reproduce Holon Inspector's private composition.

### Inputs

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

## Full Node Geometry

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

## Node Title Bar

The Title Bar identifies the displayed holon.

It SHOULD expose enough identity to distinguish multiple visualizer occurrences.

Initial content may include:

- display name or identifying label;
- type;
- edit/staged indicator;
- compression or restoration affordances where appropriate.

## Node Action Bar

### Purpose

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

### Effective Dances

Presented dances may include:

- directly declared dances;
- inherited dances;
- dances permitted by role;
- dances allowed by other runtime policy.

Only effective available dances SHOULD be presented.

---

### Alternate Visualizers

If alternate applicable Node Visualizers are available, the Node Visualizer SHOULD be able to advertise that fact.

The person MAY select an alternate visualizer.

Doing so:

- changes the current experience immediately;
- preserves the visualizer occurrence and traversal context where possible;
- emits an adaptive visualizer-selection signal.

---

### Compression

When space is constrained, Node Action Bar presentation MAY compress into:

- icons;
- compact buttons;
- menus;
- overflow controls.

The semantic actions remain available according to their applicable priority and layout budget.

## Property Viewer Pane

### Purpose

The Property Viewer Pane presents scalar properties of the holon.

It supports both read and edit modes.

---

### PropertyMap and Value Visualizers

The [PropertyMap kind](../../property-map/kind-spec.md) owns set-level
property composition and may select String labels and typed Value Visualizers
directly. The [DAHN selection contract](../../../dahn-design-spec.md#14-dahn-visualizer-selection-service)
is authoritative. No intervening Property Visualizer is selected.

---

### Scalar Values

Scalar properties SHOULD initially be presented as name/value pairs.

Value rendering MUST NOT be hard-coded by the Node Visualizer for each concrete value type.

---

### Read Mode

In read mode:

- property values are rendered for inspection;
- editable controls are not active;
- navigation and applicable actions remain available.

---

### Edit Mode

In edit mode:

- editable scalar values become interactive through their selected PropertyMap and Value Visualizers;
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

### Property Ordering

Where supported, properties MAY be reordered by the person.

For example, dragging a property upward:

- immediately changes TypeScript presentation order;
- preserves that local experience;
- emits an adaptive signal;
- may influence future personal ordering;
- may contribute to aggregate salience.

Ordering matters particularly when vertical real estate is constrained.

## Array-Valued Properties

Array-valued properties are structurally plural.

They SHOULD NOT be rendered inline as expanded scalar fields.

They SHOULD appear in the Horizontal Collection Tab Bar and use a Collection Visualizer when activated.

In edit mode, the same Collection Visualizer MAY support array mutation operations.

## Vertical Single-Value Tab Rail

### Purpose

The vertical rail on the right edge of a Node Visualizer exposes affordances that resolve to a single holon.

It is the singular counterpart to the horizontal Collection Tab Bar.

---

### Eligible Affordances

The rail may represent:

- single-valued relationships;
- single-holon dance result affordances.

Only descriptor-declared singular holon affordances belong here.

---

### Structural Presence

A single-valued relationship remains structurally singular even if it currently has no target.

Its rail entry appears in normal browsing only once runtime inspection establishes
a target exists ([Progressive Relationship Affordances](design-spec.md#progressive-relationship-affordances)). Edit, schema-inspection, and diagnostic modes MAY expose
the empty relationship with an appropriate treatment.

---

### Activation

Selecting a relationship entry first establishes target existence ([Loading States](../../structure/rooted-navigation/path-inspector/design-spec.md#loading-states)); zero
targets produce local feedback without compression or destination allocation.
For a valid target, destination-first presentation precedes actual content.
Selecting an entry invokes horizontal traversal under the authoritative
[Path Inspector Interaction Grammar](../../structure/rooted-navigation/path-inspector/interaction-grammar.md), especially
§§2.2–2.4 and §§3.3–3.8. The corresponding Node occurrence opens to the right
in its source occurrence's row and becomes the focus unless the invoking
interaction explicitly specifies otherwise.

Selecting another singular affordance from the same source MAY replace the
canonical right-hand child only while that child remains an untraversed leaf.
Once navigation has continued through that child, horizontally or vertically,
the child and its continuation MUST be retained.

The new horizontal alternative remains in the anchor's current row. The prior
traversed horizontal continuation is displaced into a newly inserted row
immediately below, and pre-existing rows below shift downward as necessary.
Insertion preserves occurrence identity, Holon identity, source and affordance
provenance, traversal direction, local navigation context, and descendant
attachment. It does not itself change the current row focus.

Rows preserve horizontal traversal paths and columns preserve vertical traversal
paths; sparse cells are valid where required to keep both truthful. Retained
occurrences remain available for restoration and further traversal. Local
presentation changes do not make a traversed occurrence replaceable again.

---

### Personalization

Rail entries MAY be reordered.

Moving an item upward:

- immediately changes presentation;
- may preserve visibility under constrained height;
- emits an adaptive salience signal.

## Editing Single-Valued Relationships

When the containing holon is staged for editing and the relationship is mutable, its singular affordance MAY additionally support:

- set target;
- replace target;
- clear target.

These actions modify staged relationship state of the source holon.

They do not edit properties of the target holon.

Editing the target holon requires entering edit mode on that target's Node Visualizer.

## Horizontal Collection Tab Bar

### Purpose

The bottom Collection Tab Bar exposes plural affordances of the current holon.

---

### Eligible Affordances

A collection tab may represent:

- array-valued property;
- multi-valued relationship;
- collection-valued dance result or result affordance.

---

### Geometry

The Collection Tab Bar MUST have the same width as its owning Node Visualizer in that visualizer's current expanded geometry.

---

### Initial State

The tab bar is visible even when no collection is open.

No Collection Visualizer occupies vertical space until a tab is selected.

---

### Activation

Selecting a relationship tab first establishes that it is non-empty. If empty,
provide local feedback and preserve the current layout and collection selection.
For a populated relationship, open the region beneath the Node, show pending
feedback there, then materialize and replace it with the Collection Visualizer
in-place ([Loading States](../../structure/rooted-navigation/path-inspector/design-spec.md#loading-states)). Array and explicitly invoked Dance result tabs retain their own
activation semantics, including meaningful empty results.

Selecting another populated collection reuses the existing region without
collapsing and reopening it. Transition out or de-emphasize the previous content,
show pending feedback identifying the newly requested collection, then replace
that feedback in-place. Preserve retained navigation paths under the Path
Inspector grammar.

---

### Personalization

Collection tabs MAY be reordered.

Moving a tab leftward:

- increases immediate prominence;
- may preserve visibility when width is constrained;
- emits an adaptive salience signal.

## Relationship Presentation

### Cardinality Rule

Relationship presentation MUST derive from descriptor-declared cardinality.

Runtime target count MUST NOT change singular/plural classification. It gates
normal browsing visibility and navigation readiness, not descriptor semantics.

---

### Singular Relationship

Maximum cardinality `1`:

- when exposed under [Progressive Relationship Affordances](design-spec.md#progressive-relationship-affordances), appears in the Vertical Single-Value Tab Rail;
- supports horizontal navigation;
- may support set/replace/clear in edit mode.

---

### Plural Relationship

Maximum cardinality greater than `1` or unbounded:

- when exposed under [Progressive Relationship Affordances](design-spec.md#progressive-relationship-affordances), appears in the Horizontal Collection Tab Bar;
- opens a Collection Visualizer;
- may support add/remove/reorder in edit mode.

A plural relationship with zero or one current target remains plural.

---

### Progressive Relationship Affordances

Normal browsing MUST withhold relationship navigation affordances until runtime
inspection establishes at least one target. Verified empty relationships remain
in descriptor knowledge but are absent from the normal rail and collection tabs.
Unknown, pending, and failed inspection MUST NOT be represented as verified zero.
Discovery failures SHOULD have local diagnostic/retry feedback without presenting
an unverified relationship as a populated navigation destination.

Relationship discovery MUST NOT block initial identity and scalar presentation.
Inspect relationships asynchronously through bounded concurrency and progressively
reveal populated affordances. Preserve descriptor/adaptive/user ordering as results
arrive; completion order does not determine salience. Existence evidence may
precede an exact count: show known collection counts when available, but do not
label a non-empty result as an exact count of one. A singular count can remain
implicit in the rail while its runtime cardinality is retained internally.

Edit mode MUST retain access to mutable empty relationships so a first target can
be set or added. Schema inspection and diagnostics MAY expose defined empty
relationships explicitly. This visibility rule does not apply to array-valued
properties or require speculative Dance invocation.

Automatic discovery and known-count display are the normal browsing defaults;
`Show Counts` and `Hide Empty` controls are not prerequisites. Specialized modes
may retain such controls where useful.

## Dance Result Presentation

### Descriptor-Based Classification

Dance result shape SHOULD be known from its response descriptor before invocation.

---

### Single-Holon Result

A dance returning one holon converges on horizontal Node Visualizer presentation.

---

### Holon Collection Result

A dance returning a holon collection converges on Collection Visualizer presentation.

---

### Value Collection Result

A homogeneous collection of values also converges on Collection Visualizer presentation.

---

### Scalar Result

The initial presentation of scalar non-holon dance results remains an open design question.

---

### No-Result Dance

A no-result dance may remain represented in the Node Action Bar with suitable execution feedback.

## Descriptor-to-Presentation Mapping

The [effective descriptor projection](#effective-descriptor-projection) below
is authoritative for this implementation. Descriptors classify affordances;
Holon Inspector chooses their regions and the parent realizes navigation intents.

## Focus and Concrete Extent Realization

Outer focus and allocation belong to Path Inspector or another composition
owner. Holon Inspector realizes the received extent within that boundary.

In a Path Inspector composition, its [axis participation protocol](../../structure/rooted-navigation/path-inspector/interaction-grammar.md#441-node-inspector-slot-compression-contract)
defines valid outer states. The [responsive realization](#responsive-realization-under-path-inspector)
below defines exact private retention/suppression behavior. In overview:

- an expanded Node presents its Title Bar, Node Action Bar, Property Viewer,
  Vertical Single-Value Rail, and Collection Tab Bar;
- partial horizontal compression retains the singular-navigation context needed
  to scan the horizontal lineage while allowing the Property Viewer to yield
  width;
- partial vertical compression retains collection-navigation context needed for
  sibling exploration while vertically expensive content yields height;
- a full or overflowed occurrence remains recoverable through the Grammar's
  hidden-lineage and restoration rules.

Exact thresholds, animation durations and styling, compact rendering, and edge controls remain open
presentation decisions. A compressed parent MUST apply its reduced allocation
to subordinate presentation; it cannot leave an expanded child consuming space
the parent has relinquished.

## Progressive Retrieval

Holon Inspector SHOULD favor lazy retrieval.

A typical flow is:

1. obtain semantic reference;
2. obtain effective descriptor and presentation context;
3. select visualizer;
4. classify affordances from descriptors without exposing unverified relationships;
5. retrieve/display initial scalar projection;
6. discover relationship population asynchronously with bounded concurrency,
   revealing populated affordances and known counts progressively;
7. on activation, establish target existence, allocate the destination, show its
   pending presentation, then retrieve/materialize content in-place;
8. invoke dance only on explicit action.

Use the least expensive available inspection sufficient to establish existence
or count; discovery does not require loading every target visualizer or full
collection. The concurrency limit is implementation-defined or configurable.
Scope results to the source and semantic context; invalidate or refresh them
when relationship state changes, including staged edits. Cancel or ignore obsolete
work when the source/context is replaced. Discovery MUST NOT mutate navigation
selection or topology.

## Entering Edit Mode

When the person selects **Edit** on a persisted holon:

1. MAP stages or exposes a new version of that holon;
2. the existing Node Visualizer occurrence remains in place;
3. the visualizer enters edit mode;
4. editable scalar properties become interactive;
5. editable relationship and collection affordances become mutable where allowed;
6. transaction status becomes visible at Space Navigator scope.

Entering edit mode is a state transition, not a navigation transition.

## Compressing Editable Visualizers

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

## Create

Create SHOULD use the same editable visual structure as Edit.

A preferred generic entry point is an applicable concrete Holon Type descriptor.

When **Create Instance** is invoked:

1. a new staged holon of that type is created in the active Space;
2. defaults are applied where defined;
3. a Node Visualizer presents the new staged holon in edit mode;
4. editing uses normal descriptor-driven PropertyMap, Value, Collection, and Action Visualizers;
5. the new holon participates in the active transaction.

Create does not require a separate form architecture.

## Clone

When **Clone** is invoked:

1. MAP creates a new staged holon initialized from the source according to clone semantics;
2. the new holon receives its own semantic identity;
3. it is presented in normal edit mode;
4. it participates in the active transaction.

Clone source history is not automatically treated as Space Navigator traversal provenance.

After staged initialization, Clone and Create use the same editing interaction model.

## Delete

Delete is a holon-scoped action.

When invoked:

1. the person receives any required explicit confirmation;
2. deletion is staged according to MAP semantics;
3. the staged deletion participates in the active transaction;
4. Commit later publishes it with other staged changes.

Delete MUST NOT imply physical erasure of historical committed state.

The exact post-Commit presentation of deleted holons remains a design detail to refine.

## Adaptive and Personalizable Interactions

Holon Inspector SHOULD expose personalization opportunities where useful.

Potential adaptive gestures include:

- property reorder;
- collection-tab reorder;
- singular-rail reorder;
- action reorder;
- explicit alternate visualizer selection;
- navigation choices.

Immediate presentation changes happen locally.

Persistent personal and collective learning occurs according to the architecture specification.

## Personalization and Constrained Geometry

Ordering has practical consequences under constrained space.

For example:

- top-ranked properties remain visible longest when vertically constrained;
- leftmost collection tabs remain visible longest when horizontally constrained;
- highest singular-navigation entries remain visible longest when vertically constrained;
- prominent actions remain outside overflow longest.

Thus personalization and adaptive salience help determine graceful degradation under compression.

## Responsive realization under Path Inspector

The selected visualizer exclusively owns sub-region and sub-slot allocation for
all nine axis combinations. In the Holon Inspector realization, partial-height
removes actions/properties while preserving the existing collection region's
height; minimal-height retains recognizable identity. Horizontal realization is
likewise child-owned. The Holon Inspector partial-width presentation MUST suppress
the entire multi-valued collection navigation region, including tabs and viewer;
only singular horizontal navigation remains available. Suppression preserves the
selected collection and its local state for restoration at full width. The Path Inspector MUST NOT implement those internal rules.

## Local region Maximize and Restore

Holon Inspector implements `maximize-region(occurrence, region)` by
redistributing its existing grant among its internal regions. A collection
viewer or property pane is an example of a region that may receive this local
emphasis; supported targets and exact controls remain presentation decisions.
This operation MUST NOT enlarge the Holon Inspector occurrence's external grant,
change sibling or ancestor allocation, modify navigation topology, or implicitly
invoke Canvas attention or context maximize.

Before maximization, Holon Inspector retains enough occurrence-local composition
state to restore the prior arrangement. Maximize and Restore MUST preserve the
occurrence identity and mounted child state, including the active collection,
selected tab/rail affordance, table sort/filter/selection, edit mode, and staged
state references. Regions yielding space remain recoverable; maximization is
not dismissal or replacement of their selected Visualizers.

Restore recovers the prior arrangement subject to the **current** parent grant
and participation states. If the parent changed the grant during maximization,
Holon Inspector reapplies that arrangement within the new bounds rather than
reinstating stale dimensions or overriding its parent's compression states.
The existing responsive rules and child extent obligations continue to apply.

Requests for space beyond the occurrence grant must go to the immediate parent
and follow the [shared request and restoration contract](../../../dahn-design-spec.md#independent-restoration-and-request-outcomes).
A refusal preserves usable presentation and the local restore information.
Local Restore does not also restore Canvas attention or the host allocation.
Specific icons, shortcuts, button placement, and animations remain open; the
operation's semantics do not depend on a particular control design.

## PropertyMap sub-slot content extent

A PropertyMap participant may report its preferred content height at its allocated
width and notify its immediate parent when that report changes. This is an
intrinsic content measurement, not a request to resize an ancestor. The Holon
Inspector may use it to reclaim unused property-pane height for an open collection
viewer, respecting its actions, relationship rail and pane chrome. This local
redistribution MUST preserve the Node's outer allocation, axis states, and Path
Inspector row geometry. Reports MUST be independent of the height granted in
response, and unchanged reports MUST NOT trigger repeated negotiation.



## Interaction scenarios

### Inspect a Holon

Given a holon:

1. obtain semantic and presentation context;
2. select an applicable Node Visualizer;
3. display identity and scalar properties;
4. progressively expose verified populated singular relationships in the right rail;
5. progressively expose verified populated plural relationships, with known counts,
   in the bottom tab bar; expose other affordances according to their contracts;
6. expose holon-level actions;
7. show no child collection or right-side Node Visualizer until selected.

### Open a Multi-Valued Relationship

Given plural relationship R:

1. discovery establishes that R is populated and reveals its Collection Tab;
2. select R and establish current target existence;
3. open or retain the collection region below the node at matching width;
4. show `Opening R…` in that region;
5. load targets and select/materialize the Collection Visualizer in-place;
6. retain the source node as context.

One or many targets use the same plural structure. Zero targets produce local
feedback without allocating a region, except in explicit empty inspection/edit flows.

### Enter Edit Mode

Given persisted Node A:

1. invoke Edit from A's Node Action Bar;
2. stage A;
3. keep A in the same occurrence;
4. switch A to edit mode;
5. make permitted scalar and relationship affordances editable;
6. reflect active transaction state in the Space Navigator Action Bar.

### Edit Scalar Property

Given staged A:

1. edit a scalar value through its Value Visualizer within the PropertyMap composition;
2. update staged semantic state;
3. establish an Undo boundary when the interaction is complete;
4. retain navigation context.

### Edit Array

Given staged A and array property P:

1. open P's Collection Tab;
2. use the Collection Visualizer;
3. add/remove/edit/reorder as permitted;
4. update staged state;
5. establish meaningful Undo boundary.

### Edit Multi-Valued Relationship

Given staged A and plural relationship R:

1. open R's Collection Visualizer;
2. add or remove targets as permitted;
3. update A's staged relationship state;
4. retain ordinary collection navigation.

### Edit Singular Relationship

Given staged A and singular R:

1. keep R in the right rail;
2. set/replace/clear target when permitted;
3. update A's staged relationship state;
4. continue to allow ordinary navigation to the current target.

### Edit Related Holon Separately

Given staged A and related B:

1. navigate to B;
2. B initially remains read-only unless already staged;
3. invoke Edit on B;
4. B joins the active transaction;
5. A and B now contain independent semantic changes within one transaction.

### Create

Given concrete type T:

1. invoke Create Instance;
2. stage new holon A;
3. display A in edit mode;
4. edit through normal visualizers;
5. A participates in the active transaction.

### Clone

Given persisted A:

1. invoke Clone;
2. create staged B initialized from A;
3. display B in edit mode;
4. modify B;
5. B participates in the active transaction.

### Delete

Given persisted A:

1. invoke Delete;
2. confirm if required;
3. stage semantic deletion;
4. reflect staged deletion state;
5. publish only when the Space Navigator transaction is committed.

## Open design questions

### Scalar Dance Results

Determine initial presentation and persistence semantics.

### Dance Result Tabs

Should collection-valued dance affordances:

- have tabs before invocation;
- appear after invocation;
- appear in a distinct unexecuted state?

### Empty Singular Relationships

Normal browsing suppresses verified empty relationships ([Progressive Relationship Affordances](design-spec.md#progressive-relationship-affordances)). The exact visual
treatment in edit, schema-inspection, and diagnostic modes remains open.

### Multiple Occurrences of a Staged Holon

Define the precise visual synchronization behavior when one staged holon appears in multiple occurrences.

The semantic state remains singular and Rust-owned.

### Relationship Target Selection

Define the generic UX used to select targets when editing relationships.

### Deleted Holon Presentation

Define how staged and committed deleted holons appear within existing traversal provenance.

## Presentation invariants

### Child Content Claims Space Only When Activated

Navigation affordances may be visible before their child visualizers consume space.

### Read and Edit Share One Visual Grammar

Do not introduce separate browse and form architectures.

### Lazy Population, Early Structure

Classify structural affordances from descriptors before retrieving expensive
contents. Progressively expose populated relationships in normal browsing.
Establish existence before structural navigation and destination real estate
before destination content; pending and final content occupy the same region.


## Effective descriptor projection

The Holon Inspector Visualizer binds to an Active Holon and evaluates its effective descriptor.

It projects the Holon's semantic affordances into its Slots according to the following rules.

---

### Scalar Properties

A Property whose `ValueType` is not `ValueArray` is projected into the Property Viewer Pane.

    Property
        WHERE ValueType != ValueArray
            ->
        PropertyMapViewer

The number of rows is determined dynamically from the bound Holon's descriptor.

No compile-time knowledge of the Holon Type is required.

---

### ValueArray Properties

A Property whose `ValueType` is `ValueArray` is projected into Collection Tabs.

    Property
        WHERE ValueType == ValueArray
            ->
        CollectionTabs

Activating the tab exposes its values through the Collection Viewer.

A ValueArray does not inherently imply navigation to another Holon.

---

### Singular Relationships

A Relationship whose structural maximum cardinality is one is projected into the Vertical Rail.

    Relationship
        WHERE max_cardinality <= 1
            ->
        VerticalRail

Activation emits a singular navigation intent; Path Inspector realizes it horizontally.

An empty singular relationship remains structurally singular.

---

### Plural Relationships

A Relationship whose structural maximum cardinality is greater than one is projected into Collection Tabs.

    Relationship
        WHERE max_cardinality > 1
            ->
        CollectionTabs

Selecting that tab exposes a Collection.

Selecting a Holon member emits a member-navigation intent; Path Inspector realizes it vertically.

A zero- or one-member runtime result remains structurally plural.

---

### Singular Navigational Dances

A navigational Dance whose response is structurally capable of producing no more than one Holon is projected into the Vertical Rail.

    navigational Dance
        AND response cardinality <= 1 Holon
            ->
        VerticalRail

Activation emits a singular navigation intent; Path Inspector realizes it horizontally.

---

### Plural Navigational Dances

A navigational Dance whose response may produce more than one Holon is projected into Collection Tabs.

    navigational Dance
        AND response cardinality > 1 Holon
            ->
        CollectionTabs

The Dance is invoked when required, its result is exposed as a Collection, and selection of a Holon result emits a member-navigation intent to the parent.

---

### Other Dances

Other applicable Dances are projected into the Action Bar.

Examples include:

- commands;
- mutators;
- create/delete operations;
- other non-navigational behaviors.

Conceptually:

    non-navigational applicable Dance
        ->
    ActionBar

The Dance Descriptor must provide sufficient semantics to support this classification.

## Action child selection

Applicable non-navigational Dances populate the Action Bar. Its realization may
request a separately selected Action Visualizer for each affordance, carrying
the bound owner Holon, Dance Descriptor, and invocation context. Action selection
uses the owner Holon’s HolonType as descriptor anchor. A button or menu item may
be an ordinary bootstrap candidate; the bar does not permanently bind every
action to one implementation. Richer Action Visualizers remain possible.

## Collection child activation and allocation

CollectionTabsSlot indexes plural relationships, ValueArray properties, and
plural navigational Dances, preserving the source affordance’s semantic origin.
CollectionViewerSlot binds the active result. Descriptor discovery alone does
not eagerly expand relationships or invoke Dances: activation resolves or invokes
the affordance, obtains the collection, and requests its selected Visualizer.

The expanded collection region initially spans the Node’s width beneath the
Collection Tab Bar. Holon Inspector supplies that allocation to any compatible
Collection child; the child owns layout inside it. This is Holon Inspector’s
placement rule, not a Collection-kind or Space Navigator requirement.

## Initial rendering example

Consider a `Book` Holon whose effective descriptor exposes:

    PropertyMap
        title : String
        subtitle : String
        publicationDate : Date
        keywords : ValueArray<String>

    Relationships
        publisher : 0..1 Publisher
        authors : 0..* Person

    Dances
        findRelatedBooks -> 0..* Book
        openPrimaryEdition -> 0..1 Book
        deleteBook -> mutation result

The illustrative visualization flow is:

    Book Active Holon -> selected Holon Inspector
        +-- PropertyMap slot -> selected PropertyMap Visualizer
        |     +-- title label / value -> String / applicable Value Visualizers
        |     +-- subtitle label / value -> String / applicable Value Visualizers
        |     +-- publicationDate label / value -> String / applicable Value Visualizers
        +-- keywords / authors / findRelatedBooks -> collection affordances
        +-- publisher / openPrimaryEdition -> singular affordances
        +-- deleteBook -> selected Action Visualizer

The PropertyMap child controls label/value pairing. These concrete Holon
Inspector projections are illustrative here; their complete behavior belongs
to that Visualizer's design, not to DAHN's universal composition contract.

The Holon has not defined any of this UI.

Its descriptors define semantic affordances.

`HolonInspectorVisualizer` defines the projection grammar.

The Visualizer Selection Service selects each semantic Visualizer; Rust resolves
its authorized implementation.

---
