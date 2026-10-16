# Holon Inspector Design Specification

## Status and current authority

Draft normative specification for this concrete Node Visualizer. Shared kind
and DAHN contracts retain their own authority. This document owns its private
composition, descriptor projection, responsive realization, and editing presentation.

## Purpose and authority

Holon Inspector is a concrete Visualizer in the
[Node family](../kind-spec.md). Its specification owns the experiential
realization behind the slot contract it fulfills.

## Slot contract obligations fulfilled

Holon Inspector fulfills an owner-defined Node Inspector slot for one Active Holon
and its effective descriptor-derived affordances. The [Node kind](../kind-spec.md)
classifies its subject; the selecting slot supplies the actual required contract.
Path Inspector's [Node Inspector slot](../../structure/rooted-navigation/path-inspector/design-spec.md#node-inspector-slot-declaration)
is the concrete requiring boundary for the presentation obligations below.

| Obligation at the containing Node slot | Holon Inspector's fulfillment |
| --- | --- |
| Subject/context | Preserve the bound Holon, effective descriptor, semantic edits and actual reference ownership; presentation augmentation does not replace the subject |
| Explicit presentation participation | Offer the required Node presentation Operator, validate complete assignments and honor the supported profile before being eligible for selection |
| Allocated dimensions | Allocate its own immediate child regions within the grant; respond through modes, wrapping and owned scrolling, with no rendered-content feedback into ancestor sizing |
| Inspect | Start in Properties; thereafter use the occurrence's remembered Properties or Collection view |
| Singular-navigation context | Enter Relationship mode with usable singular navigation, identity and Restore |
| Collection-navigation context | Enter Collection mode retaining active content; permit local Properties/Collection switching in the same allocation, without changing outer focus or tracks |
| Compact identity | Preserve recognizable identity and operable Restore regardless of shared-track aspect ratio; additional space does not imply Inspect |
| Allocation updates and restoration | Preserve permitted local choice on resizing/unrelated navigation; after a parent Restore grant, recover the remembered full-content view and meaningful child state |
| Upward interactions | Emit occurrence-bound traversal, Restore, attention, closure, exploration and inspection requests through supplied owner capabilities; do not manipulate the parent's topology or claim another occurrence's authority |
| Child state, accessibility and lifecycle | Preserve selected children, references, edits and meaningful view state while hidden; make hidden content inert; revoke/release owned realizations through the shared lifecycle |
| Failure | Refuse invalid input explicitly while preserving the last valid view; report failure on a valid promise locally with recovery, without implicit reselection |

These promises do not require the containing owner to know Holon Inspector's private
pane layout. Its four modes are its realization of the incoming contract. It then
defines the outgoing child-slot contracts below; its children do not automatically
inherit Path Inspector's occurrence contract.

## Alternating slot and Visualizer structure

    owner's Node Inspector slot
      <- Holon Inspector
        -> Title Bar slot <- selected Title Bar
        -> one ActionBar slot <- selected ActionBar (owns Action components)
        -> PropertyMap slot <- selected PropertyMap -> its declared children
        -> singular-navigation role <- selected navigation presentation
        -> collection-tabs role <- selected affordance-index presentation
        -> CollectionViewer slot <- selected Collection -> its declared children

This is target experiential composition. Concrete children own their further slots.
The Node owns one ActionBar slot combining its supplied actions; the Title Bar does
not declare a second action bar. ActionBar is the substitution boundary. Individual
Actions are components rendered by the bar, not required child Visualizer slots.
Membership and invocation bindings belong to the containing composition; the bar
uses the source-independent PresentActions contract. Exact physical placement of
the one bar remains responsive Node composition within its grant. Unmigrated role
declarations and bindings are tracked separately in the implementation plan.

## Immediate child slot contracts declared

These six slots describe this implementation, not every Node Visualizer.
Each actual child request supplies its owner-declared slot, bound subject, and
context to [DAHN selection](../../../dahn-design-spec.md#1421-slot-directed-descriptor-selection).
The slot filters accepted Visualizer types; subject applicability and selection
policy resolve a candidate. Neither this inventory nor kind membership supplies
an undeclared accepted type or permits a hard-coded implementation.

| Role | Subject or binding context | Contractual obligations |
| --- | --- | --- |
| NodeTitleBarSlot | Bound Holon identity/title context | Accept TitleBar; preserve the Holon as semantic subject, recognizable identity/restore access, accessibility and lifecycle within the allocated title band; fulfill the [Title Bar contract](#node-title-bar). |
| ActionBarSlot | Applicable executable affordances and invocation context | Accept ActionBar under the common PresentActions contract; present supplied actions and their availability within the allocation using its own Action components and supplied activation capabilities. The bar does not discover membership from the action source or subject. |
| VerticalRailSlot | Singular relationship and navigational Dance affordances of the bound Holon | Present eligible singular navigation, availability and empty/discovery feedback; emit bound navigation intents; obey the rail grant and retain state while hidden. Exact accepted descriptor remains to be grounded. |
| PropertyMapSlot | Property facet of the bound Holon, derived from its effective descriptor | Accept [PropertyMap](../../property-map/kind-spec.md); own set-level label/value composition, preserve edit/value bindings, and use assigned space with local scrolling; no intervening Property Visualizer. |
| CollectionTabsSlot | Collection-shaped affordances of the bound Holon | Present and select collection-shaped affordances, counts/availability and discovery feedback within the tabs grant; selection requests local Collection activation. Exact accepted descriptor remains to be grounded. |
| CollectionViewerSlot | The active collection exposed by the chosen affordance | Accept Collection; present supplied membership and actions within its region, preserve selection/sort/filter/scroll, and emit member-navigation intents with source provenance. Do not allocate destination Nodes or resize Path tracks. |

The Title Bar and ActionBar roles use their established type contracts; the
rail/tab-index accepted descriptors and migration remain explicit grounding work.
No new kind follows merely from the role name. Each required/optional realization
is bound and allocated by Holon Inspector; inactive optional roles need not appear
in the realized slot tree. No child owns a sibling's allocation or may demand an
ancestor resize from measured contents.
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

Ordinary Holon Inspector and Load Holons Inspector each own a Title Bar slot
with the same role contract. The selected Title Bar is an independently selected
Visualizer occurrence; sharing its implementation is optional. The Node grants a
bounded title band from its current allocation and composes its other regions
below it. Title measurements never determine Path tracks or the Node's external
grant. The Title Bar does not prescribe the containing Node's internal layout.

The semantic subject is the same bound Holon shown by the Node. Augmentation MUST
NOT change that subject. The selected Title Bar presents identity and its declared
identity/restore interactions. It does not require its own ActionBar or one selected
Visualizer per Action.

Occurrence-local display identity, permitted identifying text, staged indicator,
Theme and identity/restore state are supplied as title presentation context.
This does not rebind the Holon or add occurrence IDs to persisted usage matching.
The containing Node owns the Title Bar slot and supplies the actual slot/owner to
Rust. Its separate ActionBar fulfills the [shared membership and binding contract](#standard-membership-and-bound-activation).

The slot requires an identity-bound `ApplyTitlePresentation` Operator. Its contract
accepts one coherent bounded width/height assignment together with required
identity/restore access and relevant identity presentation state. It validates
and synchronously accepts or explicitly refuses the complete assignment, retaining
the last valid presentation on refusal; browser paint is not promised. It does
not receive Path axis states or return measured preferred dimensions. Applying it
does not invoke Dances, perform semantic discovery, reselect, or enlarge a parent.
Title wrapping, ellipsis, menus, local measurement and recoverable full-identity
disclosure remain implementation choices within the grant.

Occurrence actions route through the Node's supplied owner-bound request
capabilities. The ActionBar and Title Bar do not directly resize the Node, invoke
host-window APIs or modify topology. Identity/Restore must remain reachable even
under compact allocation, including a bound clickable identity where appropriate.
Menus and overlays follow the shared containment contract.

The standard Show Visualizer Action is explicitly bound to the containing Node's
actual inspection target. It does not inspect the Title Bar or ActionBar merely
because the control is rendered nearby. Those selected Visualizers have their own
actual inspection targets. Individual Action components do not acquire fictional
Visualizer identities or per-Action v controls; diagnostic Action metadata may be
shown clearly as component information. Every v targets one actual inspectable
Visualizer occurrence.

Replacing only the Title Bar preserves the containing Node/subject, transaction
edits, rail and collection selections and pending work. The Node owns preparation,
admission, publication and disposal of that child using ordinary replacement rules.
A failed candidate leaves the current valid title usable; initial failure retains
explicit slot-local feedback and an owner-provided restoration/closure path, not
a hard-coded alternative selection. Event handlers from replaced occurrences are
revoked. Child usage and successful-use capture follow the existing slot/descriptor
matching policy; no new persistence context dimension is introduced.

A text-led title with inline actions and a compact identity title with an
accessible action menu are examples of meaningfully different realizations of
this same contract. Neither requires the other's private layout. Title policy
must remain usable under the supported Node allocation profiles and text scales.

It SHOULD expose enough identity to distinguish multiple visualizer occurrences.

Initial content may include:

- display name or identifying label;
- type;
- edit/staged indicator;
- compression or restoration affordances where appropriate.

## Node Action Bar

### Purpose

The Node has one ActionBar presenting both centrally declared occurrence actions
and applicable actions associated with the displayed Holon. Their sources and
activation targets are resolved by the containing composition, not by the bar.

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

### Standard membership and bound activation

Explore-from-here, Close, Expand/Restore and Show Visualizer are standard occurrence
actions. They are centrally declared once in the shared Node action-membership
contract, independently of subject type. Shared composition supplies them together
with applicable subject actions to the Node's single ActionBar. Node implementations
reference that declaration rather than copying a list or manually remembering each
action. The title remains independently selectable and its semantic subject remains
the Holon; supplying occurrence actions does not rebind it.

The selected ActionBar implements PresentActions and renders each supplied Action
as a component. The owner supplies identity, label, optional independently defined
icon, availability/reason and authorized activation binding. Icon definition/reuse
does not require an Action Visualizer or a new Icon Visualizer slot. Responsive
arrangement may use icons, labels, grouping or overflow; none changes membership or
execution semantics. Presentation-afforded actions invoke their supplied local
Operator bindings; subject-afforded Dances retain their own execution bindings.
The bar does not need to know either source or target semantics to present them.

Updating the shared standard membership changes required Actions for participating
Nodes through composition, without redefining that set in individual renderers.
Existing title-specific schema records require migration to this common Node
composition; this specification does not select replacement executable key names.

Participation checks MUST reject missing required roles or action bindings
explicitly. A Node or ActionBar implementation cannot silently omit a standard
action because its developer did not manually register it. Shared realization
resolves required membership from the contract, rather than another handwritten
list in each renderer. Structural admission can verify declarations and bindings;
behavioral conformance must additionally verify that the selected presentation
makes the required actions accessible. A matching declaration alone does not
prove arbitrary rendering behavior. Legitimate operation availability remains
owned by the relevant occurrence/composition authority.


Standard action membership is independent of current availability. The owning
occurrence/composition authority supplies an explicit available/unavailable state
and an explanation for an unavailable action. For example, protected roots or
active workflows may prevent closure without removing Close from the shared set.
The selected ActionBar preserves discoverability of that state and
reason through an accessible presentation, which need not be a permanent icon.
This does not override the separate responsive policy for direct v display or
recursive inspection access. A declared action binding that reports legitimate
unavailability is conforming; omitting a required binding is an admission failure.


Specialized Node Visualizers MAY declare additional actions through an
explicit extension of the shared role contract. Extensions add to the canonical
set; they MUST NOT remove, replace or redefine standard action identities or their
semantics. Shared composition combines standard membership with declared additions
and validates the required occurrence-bound operation bindings. This does not
permit a second copied definition of the standard set in a specialized renderer.
### Common ActionBar slot participation

ActionBar has one source-independent role contract, `PresentActions`. It presents
supplied actions within the assigned region. The containing composition determines
membership, ordering and any applicable grouping, and supplies action descriptors,
current presentation/availability state and occurrence-bound activation capabilities.
The bar owns responsive arrangement and renders individual Action components;
per-Action Visualizer selection is not required.
It does not discover actions from a Holon, identify a title/subject category, or
choose a different interface according to the source of the actions.

Presenting actions does not apply or execute them. Applying layout, refreshing
availability or rearranging overflow must not invoke actions. An explicit agent
activation uses the supplied binding of the Action component, preserving its actual
authority and target. The bar need not know that target's semantics to present it.
Domain-specific execution remains outside ActionBar's presentation contract.

Canonical standard occurrence-action membership remains declared once in the
shared Node action contract and supplied through composition. The same ActionBar
contract can present that supplied membership or another owner's supplied actions;
no dedicated title-action bar behavior is required. Parent-specific membership
constraints do not become separate ActionBar contracts.

`ApplyTitleActions` and `ApplySubjectActions` are superseded target vocabulary.
The contract is `PresentActions`, with one coherent input shape for all uses.
Migration must normalize the supplied inputs and preserve Action state and bound
activation authority while removing required per-Action selection; simply renaming two incompatible call signatures
would not establish a shared contract. Eligibility remains Rust-owned and verifies
that common contract, with callable admission and explicit selection policy where
multiple conforming implementations exist. Do not resolve ambiguity through an
incumbent-specific name check or artificial title-versus-subject Operator split.

Holon Inspector has one ActionBar slot. Its allocated placement is Node-owned;
combining action membership does not require the bar to interpret membership sources.
The Title Bar has no second mandatory ActionBar child. Independently defined icons
are presentation metadata/assets, not a requirement for individual Action Visualizers.

### Effective Dances

Presented dances may include:

- directly declared dances;
- inherited dances;
- dances permitted by role;
- dances allowed by other runtime policy.

Only effective available dances SHOULD be presented.

### Holon-level Action Initiation

The displayed holon remains the semantic owner and affording subject of its
Dance actions. HolonInspector presents those actions through its action bar;
the enclosing Dancer does not acquire their semantic ownership by hosting them.
For example, `LoadHolons.DanceType` is initiated from the action bar of the
HolonSpace that affords it.

Semantic availability and execution readiness are distinct. An effective Dance
may be displayed disabled while its interaction or invocation support is not
implemented. A disabled control exposes its reason; presentation alone does not
grant execution authority.

Action activation carries the explicitly bound affording holon, selected Dance
identity, and originating occurrence context through a reusable interaction
contract. It does not infer its target from a later navigation root or current
selection. Generic action-bar code delegates Dance-specific request preparation
to an applicable interaction rather than implementing source pickers or other
domain-specific forms itself.

Activation may begin request preparation before invocation. For Load Holons,
source selection and review precede explicit Submit; cancelling preparation
does not invoke the Dance. Invocation uses the canonical public MAP SDK boundary
and remains subject to MAP authority. The action interaction reports readiness,
pending execution, and terminal outcomes and prevents duplicate submission.

HolonInspector or a selected child Visualizer owns the presentation slots it
actually composes for request interaction and results. The affording holon is
their semantic context, not a Visualizer or presentation-slot owner. Feedback
and results retain the originating holon and Dance as provenance. Navigation or
presentation disposal does not silently retarget execution, cancel a submitted
Dance, or abandon externally owned transaction state.

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
Holon Inspector emits a singular-navigation intent identifying the source
occurrence, activated affordance, and resolved target. The containing navigation
Visualizer owns the resulting destination placement, focus, and treatment of
existing continuations; Holon Inspector does not manipulate that owner's grid.

When composed under Path Inspector, the intent follows its authoritative
[horizontal traversal](../../structure/rooted-navigation/path-inspector/interaction-grammar.md#22-horizontal-traversal),
[branch retention](../../structure/rooted-navigation/path-inspector/interaction-grammar.md#24-branch),
and [horizontal alternative insertion](../../structure/rooted-navigation/path-inspector/interaction-grammar.md#35-horizontal-alternative-insertion)
rules. Those rules own replacement eligibility, row displacement, identity
preservation, and attachment of retained paths.

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

Outer focus and allocation belong to Path Inspector or another immediate owner.
Holon Inspector realizes the received intent and dimensions within that boundary.
Its [four-mode realization](#responsive-realization-under-path-inspector) separates
presentation from track geometry. Properties and Collection share a main content
region; Relationship retains singular context; Compact identity retains identity
and Restore. Each mode responds to dimensions without resizing ancestor tracks.
A larger shared row/column does not force richer presentation. Compression applies
the reduced grant to child slots rather than leaving children at stale extents.

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

Persistent interpretation follows [adaptive interaction reporting](../../../dahn-design-spec.md#148-adaptive-interaction-reporting)
and [personal/collective feedback](../../../dahn-design-spec.md#personal-and-collective-feedback).
Reorder, visibility, and prominence changes may provide salience evidence;
choosing a representation may provide preference-affinity evidence. Incidental
navigation is not automatically a durable preference. Occurrence-local changes,
remembered settings, pins, and consent to collective contribution remain distinct.
Shared Visualizer definitions and semantic Holon state are not modified by
presentation personalization.

## Personalization and Constrained Geometry

Ordering has practical consequences under constrained space.

For example:

- top-ranked properties remain visible longest when vertically constrained;
- leftmost collection tabs remain visible longest when horizontally constrained;
- highest singular-navigation entries remain visible longest when vertically constrained;
- prominent actions remain outside overflow longest.

Thus personalization and adaptive salience help determine graceful degradation under compression.

## Responsive realization under Path Inspector

Holon Inspector participates in the explicit Node-slot presentation Operator
required by [Path's contract](../../structure/rooted-navigation/path-inspector/interaction-grammar.md#441-node-inspector-slot-compression-contract).
It receives dimensions and coherent presentation requirements, not independently
mutable axis states. Path owns track allocation; Holon Inspector owns its internal
regions. Neither dimensions nor shared track states determine its private mode.

Holon Inspector has four modes:

| Mode | Presentation priorities |
| --- | --- |
| Properties | Identity/actions, properties pane, singular rail and collection tabs; no collection viewer |
| Collection | Identity/actions, Properties return header, tabs, collection actions and active viewer; no properties pane or singular rail |
| Relationship | Usable singular navigation, identity and Restore; no properties, collection tabs or viewer |
| Compact identity | Recognizable identity and Restore, responsive to the granted aspect ratio |

Wide/shallow and narrow/tall are realizations of Compact identity, not additional
modes. Additional space may expose identity details or actions without changing
mode. Responsive wrapping, internal measurement and owned scrolling are allowed;
rendered-content reports MUST NOT determine ancestor track sizes.

Properties and Collection share the available main content region. Selecting a
collection tab enters Collection. A shallow, full-width **Properties** header above
the collection tabs remains visible in Collection mode; activating it returns to
Properties. This is always local, including in a vertical source's contextual
allocation. It does not request parent restoration, change Path focus or resize
tracks. The properties pane uses the available budget rather than demanding enough
height to show every property. Collection mode gives that budget to its viewer.

Each occurrence remembers its last full-content view, Properties or Collection.
Local switching updates that memory. Relationship and Compact identity do not.
New ordinary and loader inspectors start in Properties; the loader presents its
authoritative outcome and available diagnostics there. Restore requests expanded
allocation through the immediate parent, then restores the remembered full-content
view and its meaningful state after the grant. Refusal leaves the valid presentation
intact. Memory is per occurrence, not globally per semantic Holon.

Horizontal traversal enters Relationship context. Vertical traversal originates in
Collection and retains it under the contextual budget without an extra transition
to expose content. A subsequent Properties/Collection switch is permitted locally.
Resizing and unrelated navigation preserve that local choice; a new traversal
from the occurrence may establish context again. Allocation reapplication MUST NOT
replay context entry. The slot's contract distinguishes these operations explicitly.

Hiding a region preserves selected child identity, bound references, membership,
selected tab, selection, sort/filter, scroll and edits. Hide/show alone does not
refetch or reconstruct content. Hidden regions are inert and absent from keyboard
navigation. Identity and reachable Restore survive every mode. Local application
of geometry does not invoke Dances or discover content merely to size regions.

The singular rail is capped at its normal Theme-informed policy width and aligned
right; surplus width remains left of it. Narrower grants cause responsive adaptation
inside that budget. Buttons do not stretch merely to fill a shared wide column.
A substitute participant fulfills semantic slot intents without reproducing these
private regions or modes.

### Shared inspector composition

Generic and specialized response inspectors share region allocation, responsive
navigation, compression, expansion/restore, and Operator participation through
composition. They do not copy geometry because their data bindings differ.
A specialized binding supplies semantic properties, result collections, actions,
and navigation targets to the shared implementation. Properties remain a selected
PropertyMap presentation; a chips realization is not a separately copied Node
shell. Collection actions and content remain owned by selected Collection
Visualizers, not a table-only layout contract.

Subject-type applicability inheritance is independent of code reuse. A specialized
Node may retain its semantic identity and binding logic while composing the same
layout helper. Compression and restore preserve selected identities. This does
not prescribe an implementation inheritance hierarchy. The Title Bar is selected
through its declared slot for agent substitution; shared geometry remains private
machinery. Rail/tab delegation is a separate component migration and does not
justify copying region geometry in the meantime.

### Compressed title identity

The default selected Title Bar serves Holon Inspector and Load Holons Inspector
with the following compressed identity behavior. Alternatives fulfill the same
identity/restore obligations within their own assigned band.
Minimal-height titles use the ordinary canvas font size and allow up to two lines
of the Holon key. Both-axis compression retains the key rather than replacing it
with initials. Their preferred minimal extents are 96 px wide and 64 px high;
these are concrete Visualizer requests, not universal Node-kind thresholds.
Minimal-width titles with non-minimal height use vertical text and reserve a
separate closure-control row so controls do not consume the text column. The
Visualizer-information control is suppressed in either minimal axis state and
returns when restored. Closure and title restoration remain available. Full
identity remains in the title tooltip and accessible label when text overflows.
Compressed title measurements must not replace the normal internal title policy; compressed measurements do not size ancestor tracks.

## Local region Maximize and Restore

Properties and Collection switch ownership of the same main content region.
They are not simultaneous small panes with a separate region-maximization state.
The visible Properties header and collection tabs provide local switching without
ancestor space requests. Both views use the current grant, with owned scrolling
and meaningful state retained while hidden.

Occurrence Restore is distinct from local Properties/Collection switching. From
Relationship or Compact identity, request expanded allocation through the immediate
parent and restore the last full-content view after a grant. Never reset to the
initial default or restore saved pixel dimensions. Clicking a Properties return
header in Collection mode does not invoke occurrence Restore.

Path attention and host maximize/restore retain their own ownership. They do not
supply an implicit reason to discard or reset the local full-content view.

## PropertyMap sub-slot content extent

PropertyMap may measure internally to wrap controls or manage scrolling within its
assigned pane. Holon Inspector allocates the Properties region from its own grant;
it does not negotiate ancestor tracks from reported PropertyMap height. Properties
and the collection viewer do not compete through preferred-height redistribution:
they occupy the main content region in different local modes. No rendered row
count or content extent determines Path allocation.

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

## Action components and presentation

Applicable non-navigational Dances and the centrally declared occurrence actions
supply the single ActionBar's membership through containing composition. The
[shared ActionBar contract](../../../dahn-design-spec.md#action-selection-and-activation-boundary)
requires PresentActions. ActionBar renders Action components with supplied labels,
optional independently defined icons, availability, grouping and activation bindings.
It does not select a Visualizer for each Action or derive membership from the
subject Holon. Grouping and responsive overflow preserve access and invocation
authority without executing an action merely to arrange it.

ActionBar is independently selected through Rust. Its Action components are not
semantic Visualizer children in the inspection tree. Replacing the bar preserves
Node/subject state and meaningful action/workflow state through the containing
owner's lifecycle. Workflow execution remains separate from control rendering.

## Collection child activation and allocation

CollectionTabsSlot indexes plural relationships, ValueArray properties, and
plural navigational Dances, preserving the source affordance’s semantic origin.
CollectionViewerSlot binds the active result. Descriptor discovery alone does
not eagerly expand relationships or invoke Dances: activation resolves or invokes
the affordance, obtains the collection, and requests its selected Visualizer.

Holon Inspector establishes its collection region before showing loading or
resolved content. Switching collections reuses that internal region and preserves
retained child/local state as applicable. This internal transition does not remove
previously navigated Path occurrences. Only activation of a Holon member sends
Path a semantic navigation intent; Path then owns that destination Node's
transition. This rule does not prescribe another Node realization's placement.

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
        +-- ActionBar slot -> selected ActionBar
              +-- deleteBook Action component (supplied activation binding)

The PropertyMap child controls label/value pairing. These concrete Holon
Inspector projections are illustrative here; their complete behavior belongs
to that Visualizer's design, not to DAHN's universal composition contract.

The Holon has not defined any of this UI.

Its descriptors define semantic affordances.

`HolonInspectorVisualizer` defines the projection grammar.

The Visualizer Selection Service selects each semantic Visualizer; Rust resolves
its authorized implementation.

---


### Initial body allocation and scrolling

Properties is the initial full-content mode. The Node allocates title/actions,
properties with singular rail, and collection tabs within its grant. No viewer is
shown until a collection is selected. In Collection mode, the full-width Properties
return header and tabs precede collection actions/content; properties and the
singular rail are hidden. The active main region consumes useful surplus height.
No Path row change accompanies a local mode switch.

Typography stays stable; shrinking fonts is not the primary fitting mechanism.
Property and collection regions provide keyboard-accessible owned scrolling and
visible overflow cues independent of operating-system scrollbar visibility.
Show Empty Relationships remains part of the appropriate singular-navigation
presentation; switching modes does not alter discovery semantics.

### Internal containment and constrained grants

Allocate finite title, actions, navigation and main-content regions before laying
out their children. Respect the current mode and grant, with optional detail
yielding before required capabilities. Content MUST NOT paint into sibling regions
when intrinsic size exceeds the assigned region. Positioned controls follow the
owner's bounds/overlay contract. Resize recomputes internal regions without
resetting local mode or retaining stale placement styles.

The parent's supported participation profile must permit both local full-content
views where switching is allowed. A smaller Collection-source budget does not
block switching to Properties; it may require more scrolling within the same
rectangle. No child requests larger Path tracks merely to show every field or row.

### Navigation capability retention in partial context

Relationship context retains singular navigation. Collection-context entry retains
the active collection and its navigation, but permits a subsequent local Properties
choice. Track intersections never impose both obligations simultaneously. Retained
alternatives outside the focused ancestry do not add obligations; restoring the
source gives access to the other direction. Subjects, selected children, local
full-content memory and semantic state survive contextual changes.

### Minimal identity and unconditional restoration

Minimal context may suppress direct navigation until restored. Every minimal
presentation retains recognizable subject identity and an operable, keyboard-
accessible Restore affordance. Compression, reduced allocation or suppression of
an inspection icon must never remove the final restoration path for a live cell.
The selected Title Bar/Actions composition fulfills this shared obligation; it
cannot depend on each specialized Node manually remembering a Restore callback.
Off-viewport placement preserves recoverability through the containing surface
and actual occurrence inspection. Restore result semantics follow Path Inspector.
