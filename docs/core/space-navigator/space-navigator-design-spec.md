# DAHN Space Navigator Design Specification v0.7

## Status

Draft normative design specification.

## Change Log

| Version | Changes from prior version |
| --- | --- |
| v0.7 | Replaces default visibility of empty relationships with progressive population-gated browsing; defines destination-first pending presentation and stable collection switching. |
| v0.6 | Defines column-oriented sorting semantics separately from table-level default row ordering, including descriptor-backed Sequence and Key defaults and occurrence-local restoration. |
| v0.5 | Defines the bounded DAHN Launch Experience: its narrative, application-shell boundary, readiness and handoff behavior, accessibility, observational-imagery provenance, and MVP deferrals. |
| v0.4 | Adds `LoadHolons` as a Space Navigator Action Bar operation, invoked as the canonical Dance through the active `HolonSpace`; defines Space-Navigator-scoped feedback and makes host source selection ingress rather than a second semantic loading protocol. |
| v0.3 | Baseline normative Space Navigator design specification. |

## Purpose

This specification defines the **Space Navigator**, an initial DAHN Dancer for
generic, descriptor-driven exploration and manipulation of a MAP Space. Its
experience realization is hosted by a Canvas; it is not itself the Canvas.

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

The normative spatial and compositional transformations that this specification
applies are defined in `space-navigator-interaction-grammar.md`.

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

Where no specialized visualizer applies, the Rust DAHN Selector searches for
an applicable default through the nearest subject TKD, inclusive. No compatible
candidate at that boundary is an explicit selection error. TypeScript realizes
the selected implementation only; it MUST report an unavailable implementation
rather than choosing a generic fallback itself.

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

The Rooted Navigation Visualizer selected for the Space Navigator navigation
role MUST support sustained exploration within its Canvas-provided allocation
without requiring every prior visualizer to remain at full size.

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

## 1.8 DAHN Launch Experience

Before the initial Space Navigator becomes visible, DAHN SHOULD present a
brief, evocative launch experience. It is an entry ritual into DAHN, not a
splash screen, cinematic sequence, or substitute for the Navigator. The
sequence frames the person as a locally situated participant in nested wholes
and frames this first Navigator as an early visual expression that future
Visualizer Commons contributors may deepen.

### 1.8.1 Narrative and scenes

The MVP scene order is:

1. **Cosmos** — observational imagery of NGC 346 begins somewhat unresolved
   and comes into focus.
2. **Stellar transition** — the view moves toward a luminous point in the
   nebula; increasing brightness may bridge the scene into Earth's solar
   context without representing that star as literally the Sun.
3. **Living Earth** — a whole-Earth NASA DSCOVR / EPIC observation becomes the
   visual center.
4. **Living place** — Earth yields to observational imagery of the Okavango
   Delta, selected for its visibly nested relationships among water, land,
   vegetation, species, and changing conditions.
5. **I-Space** — the terrestrial scene recedes as the initialized Space
   Navigator emerges, so the handoff reads as arrival rather than screen
   replacement.

The sequence MUST suggest semantic continuity across scales rather than
simulate astrophysically literal travel. It SHOULD use restrained full-screen
still-image treatment—zoom, focal translation, blur/focus, opacity,
brightness, crossfade, and easing—rather than video, 3D simulation, or text
that competes with the imagery. Any textual framing is optional, sparse, and
provisional.

### 1.8.2 Application-shell boundary

The MVP launch experience is an **application-shell concern**. It is not a MAP
Visualizer, MAP media ValueType, media Holon, or Visualizer Commons feature.
Its imagery may be bundled as ordinary application assets. It MUST NOT put MAP
media infrastructure, dynamic visualizer acquisition, generalized animation
grammar, WebGL/Three.js, GIS, geolocation, personalized locality, or external
media streaming on the critical path.

A future experience may descend from Earth into the user's actual locality or
bioregion. That possibility makes local-first participation visually literal,
but it is explicitly deferred and creates no MVP requirement for location
services, map tiles, or geospatial data.

### 1.8.3 Readiness, handoff, and control

DAHN initialization and the narrative sequence are independent timelines.
Initialization begins immediately beneath the launch experience. If readiness
arrives early, the sequence completes normally. If it arrives late, the final
terrestrial scene enters a subtle holding state until the initial Space
Navigator can render; the experience MUST NOT expose incomplete UI.

A Skip control MUST become available after a short initial interval. Skipping
before readiness advances to that holding state; skipping after readiness
hands off promptly. The final handoff SHOULD retain subtle local movement while
the Navigator canvas emerges through or beneath the terrestrial scene.

The launch MUST provide a reduced-motion treatment that substantially removes
travel motion while preserving the semantic progression where practical, or
transitions directly to the final state. It MUST avoid flashing or rapid
luminosity changes, keep controls keyboard-accessible, fail gracefully when an
asset cannot load, and never prevent eventual access to the application.

### 1.8.4 Observational imagery and provenance

The launch uses authentic **observational imagery of the actual universe and
Earth**, not AI-generated or invented artwork. “Observational” deliberately
includes instrumentally captured and scientifically processed imagery,
including assigned-color processing; it does not imply ordinary visible-light
photography.

Provenance is part of the experience, not legal boilerplate. An unobtrusive,
keyboard-accessible **Image credits** affordance MUST expose each incorporated
asset's title/subject, mission or instrument, complete supplied credit line,
authoritative source URL, applicable usage information, and optional short
explanation that it derives from scientific observation rather than AI
artwork. The full source credit MUST NOT be reduced to merely “NASA.”

The preferred starting set is JWST NGC 346 imagery (NASA / ESA / CSA, retaining
the complete supplied credit), NASA DSCOVR / EPIC whole-Earth imagery, and
NASA Earth Observatory or other verified NASA observational imagery of the
Okavango Delta. Exact asset, crop, and source-provided attribution remain
implementation-time selections.

Bundled derivatives MUST be appropriately sized and efficiently encoded for
startup, require no network connection, and avoid expensive runtime image
processing. Original source references and provenance metadata remain retained
alongside the optimized derivatives.

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

The Space Navigator Dancer composes primarily:

1. a `HolonSpace` context role that represents the space Holon itself through
   an appropriate Node Visualizer;
2. an afforded-Dancers role for Dancers afforded by that `HolonSpace`;
3. a Rooted Navigation Visualizer role rooted at that `HolonSpace`;
4. Node Visualizers;
5. Collection Visualizers;
6. Property Visualizers;
7. Value Visualizers; and
8. Action Visualizers.

Space Navigator is not itself a Visualizer. It selects a generic Rooted
Navigation Visualizer to realize the evolving structure unfolded from its
`HolonSpace`. Canvas hosts the Dancer experience and may also host other
Dancers. A future `AgentSpace` may add affordances and therefore additional
Space Navigator roles, but is not part of the current ontology.

The selected concrete visualizer for each role is resolved through DAHN architectural mechanisms.

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

The Rooted Navigation Visualizer owns occurrence placement, topology, lineage,
compression, overflow, focus, and internal geometry for the navigation
structure. It SHOULD NOT require `HolonSpace`-specific or future
`AgentSpace`-specific semantics.

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
    | Node / Collection visualizer occurrences             |
    |                                                      |
    +------------------------------------------------------+

The Space Navigator Action Bar remains pinned while traversal occurs beneath
it. It is Dancer chrome, not Canvas chrome.

---

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

- Load Holons;
- Space Navigator view controls;
- layout controls;
- Space Navigator-specific navigation controls;
- Space Navigator experience-visualization controls;
- other Space-Navigator-level operations.

`LoadHolons` is Space-Navigator-scoped because it affects the active HolonSpace
rather than an individual displayed holon. The Space Navigator Action Bar initiates the
canonical `LoadHolons` Dance through the active `HolonSpace`; any file or
other source-selection interface is host ingress for that Dance, not a
separate semantic loading protocol. The Space Navigator MUST present loading
and failure feedback at Space Navigator scope and refresh normal inspection after a
successful load.

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
- property action → Property Visualizer;
- collection action → Collection Visualizer;
- holon action → Node Visualizer;
- transaction action → Space Navigator Action Bar.

---

# 6. Active Traversal Frontier

At any point, the Space Navigator has an **active traversal frontier**: the visualizer occurrence currently receiving primary interaction and spatial priority.

The Rooted Navigation Visualizer SHOULD preferentially allocate its
Canvas-provided real estate toward this frontier.

Prior contexts progressively compress away from it.

> **The Rooted Navigation Visualizer allocates its Canvas-provided
> space toward the active traversal frontier and compresses provenance behind it.**

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

For each holon occurrence, the Space Navigator requests an applicable Node
Visualizer through the Rust DAHN selection architecture.

The initial Selector fallback is the Generic Holon Node Visualizer.

The selection result is the selected Visualizer Holon reference. TypeScript
checks its materialization cache for that identity and, on a cache miss,
requests the Visualizer's Rust-owned `Materialize` Dance. Materialize returns
the executable realization payload from the configured Rust-side artifact
backend; the initial backend may be local filesystem artifacts.

If materialization or loading fails, TypeScript reports a realization error and
does not replace the selected Visualizer.

A specialized Node Visualizer MAY replace it without changing the Space
Navigator traversal model, provided it satisfies the required Space Navigator
contracts.

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

Its rail entry appears in normal browsing only once runtime inspection establishes
a target exists (§16.4). Edit, schema-inspection, and diagnostic modes MAY expose
the empty relationship with an appropriate treatment.

---

## 13.4 Activation

Selecting a relationship entry first establishes target existence (§29); zero
targets produce local feedback without compression or destination allocation.
For a valid target, destination-first presentation precedes actual content.
Selecting an entry invokes horizontal traversal under the authoritative
[Path Inspector Interaction Grammar](path-inspector-grammar.md), especially
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

Selecting a relationship tab first establishes that it is non-empty. If empty,
provide local feedback and preserve the current layout and collection selection.
For a populated relationship, open the region beneath the Node, show pending
feedback there, then materialize and replace it with the Collection Visualizer
in-place (§29). Array and explicitly invoked Dance result tabs retain their own
activation semantics, including meaningful empty results.

Selecting another populated collection reuses the existing region without
collapsing and reopening it. Transition out or de-emphasize the previous content,
show pending feedback identifying the newly requested collection, then replace
that feedback in-place. Preserve retained navigation paths under the Path
Inspector grammar.

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

Runtime target count MUST NOT change singular/plural classification. It gates
normal browsing visibility and navigation readiness, not descriptor semantics.

---

## 16.2 Singular Relationship

Maximum cardinality `1`:

- when exposed under §16.4, appears in the Vertical Single-Value Tab Rail;
- supports horizontal navigation;
- may support set/replace/clear in edit mode.

---

## 16.3 Plural Relationship

Maximum cardinality greater than `1` or unbounded:

- when exposed under §16.4, appears in the Horizontal Collection Tab Bar;
- opens a Collection Visualizer;
- may support add/remove/reorder in edit mode.

A plural relationship with zero or one current target remains plural.

---

## 16.4 Progressive Relationship Affordances

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

An applicable Collection Visualizer is selected through Rust DAHN architecture.

The initial Selector fallback is the Table Collection Visualizer.

The TypeScript runtime resolves only the implementation supplied with the
selection result. If that implementation is unavailable locally, it reports a
realization error and does not replace the selected Visualizer.

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

Column headers support sorting of eligible columns. Filtering is a separate
collection-view operation and may be delivered incrementally.

### 19.4.1 Column-Oriented Sorting Semantics

A column sort orders complete rows by the values in one active column. It MUST
preserve row identity, cell alignment, member-reference binding, and selection
identity. Sorting MUST NOT mutate semantic collection membership, cardinality,
relationship sequence positions, or navigation topology.

The initial column-oriented sorting contract is:

| Concern | Semantics |
| --- | --- |
| Eligible property value kinds | `StringValue`, `IntegerValue`, and `BooleanValue` |
| Strings | Deterministic, case-sensitive lexicographic ordering; no locale-dependent collation or case folding |
| Integers | Numeric ordering, not ordering of formatted strings |
| Booleans | `false` before `true` in ascending order |
| Sequence | Order by authoritative `SequencePosition` semantics; see §19.5 |
| Missing values | `null` sorts last in both directions |
| Equal values | Preserve their relative order in the supplied collection projection, including for descending sorts |
| First activation of a column with no active sort | Ascending |
| Activation of the active sort column | Toggle ascending/descending |
| Activation of a different eligible column | Ascending on the newly selected column |
| Number of active sort columns | One |

`EnumValue`, `BytesValue`, and mixed `AnyBaseValue` columns are not initially
sortable. Their displayed labels MUST NOT be used to invent semantic ordering
or a cross-type comparison policy. A future authoritative ordering contract may
extend eligibility.

Sorting compares typed values rather than rendered cell text. The sort MUST
leave the supplied input unchanged and retain a stable association between each
row and its original member occurrence. Header activation MUST NOT select or
inspect a member. Row keyboard navigation follows the displayed row order.

The active sort column and direction MUST be visible and available to assistive
technology. Header controls MUST expose visible ascending and descending choices, be
keyboard-operable, and expose appropriate `aria-sort` state. The active
direction MUST be visibly distinguished. If responsive column fitting hides the active header, the
collection MUST retain a discoverable sort indicator within its allocation.

### 19.4.2 Sort State Lifetime

The active sort belongs to the Collection Visualizer occurrence, not to the
semantic holon, column display label, or Path Inspector grid position. Different
occurrences of the same collection MAY have different sorts.

Tab switching and returning, compression on either or both axes, overflow,
viewport movement, focus changes, and retained-path insertion MUST preserve the
occurrence's sort. Sorting another column MUST leave Sequence values attached to
their original member occurrences.

A valid saved sort takes precedence over the table default in §19.6 and is
reapplied after fresh membership projection. If its column disappears or becomes
ineligible, the table MUST return to the applicable table default and update its
sort indicator. Restoring view state MUST NOT substitute stale membership for a
fresh collection read.

## 19.5 Sequence Column

For a relationship collection, the originating relationship descriptor's
`IsOrdered` property (display name `isOrdered`) is the authoritative indicator
that member order is significant. The applicable declared or inverse descriptor
supplies this policy. No separate manual-order flag is required.

When `IsOrdered` is true, the table MUST expose a read-only **Sequence** column
whose values come from authoritative relationship-occurrence `SequencePosition`
metadata. These values belong to member occurrences, not to properties of the
target holon. Repeated targets, where allowed, retain distinct occurrence identity
and sequence metadata.

Sequence MUST NOT be generated from the current display index or incidental
retrieval order, and sorting MUST NOT renumber it. Ascending Sequence restores
manual order; descending Sequence reverses that order as a view operation only.
Unordered collections MUST NOT acquire a synthetic Sequence column. A target
property with the same display name remains a distinct column identity.

The table consumes ordering policy and occurrence metadata through the public
reference/SDK boundary. It MUST NOT access storage links directly or infer
ordering policy from observed membership order. Missing authoritative metadata
must remain an explicit unavailable/error condition, not fabricated sequence
values.

See [effective collection policy](../type-system/descriptor-semantics-rules.md#36-effective-collection-policy)
and [storage ordering boundaries](../guest/storage-layer-services/storage-layer-design-spec.md#11-filtering-ordering-and-limiting).

## 19.6 Table-Level Default Row Ordering

The table's default ordering is distinct from the semantics of sorting an
individual column. It applies on initial presentation when no valid saved sort
exists, and as the fallback described in §19.4.2.

Apply the following precedence:

1. **Manually ordered relationship collection (`IsOrdered = true`):** Sequence
   ascending, whether or not the target HolonType defines a key.
2. **Otherwise, a holon collection whose declared element HolonType or concrete
   member HolonTypes define instance keys:** Key ascending, using the
   column-oriented string comparison semantics.
3. **Otherwise:** preserve the supplied collection order without asserting that
   this order has semantic significance. This includes keyless holon collections
   and scalar collections without an applicable ordering contract.

A broad declared target such as `HolonType.TypeDescriptor` may select a keyless
baseline while concrete members have keyed types. This is the case for `Owns`.
When the declared type does not establish keyedness, inspect the concrete
members' describing HolonTypes. If a concrete member type defines keys, use the
Key default; keyless members retain missing Key values and sort last. A broad
keyless target alone MUST NOT suppress this default. Empty collections use the
declared type's policy.

Whether a HolonType defines a key is descriptor-governed: use its
effective `InstanceKeyRule`; `NoneRule.KeyRuleType` denotes explicit keylessness.
Do not infer keyedness from a nonempty sample, an arbitrary property named Key,
or a fallback identity label. Key ordering uses the actual semantic member keys,
not versioned-key or display-label substitutes. Missing key values follow the
column sort's missing-value rule and do not change type-level keyedness.

Sequence and Key defaults MUST expose their active ascending sort indicators.
A user may override either default by selecting another eligible column. A valid
user-selected sort is preserved across ordinary occurrence restoration rather
than being overwritten by the default.

See [instance key rules and explicit keylessness](../type-system/schema-design-spec.md#92-explicit-keylessness).

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

# 26. Applying the Interaction Grammar

The [Path Inspector Interaction Grammar](path-inspector-grammar.md) is
authoritative for rooted-navigation topology, horizontal and vertical lineage,
lineage connectors, topology versus viewport projection, compression, overflow,
stable attachment, and allocation. This section specifies how concrete Space
Navigator interactions invoke that grammar through the selected RootedNavigation
visualizer.

The [Space Navigator Interaction Grammar](space-navigator-interaction-grammar.md)
owns Dancer-level experience composition and allocation to the RootedNavigation
role; it does not own that visualizer's internal navigation geometry.

## 26.1 Horizontal Navigation

Activating a structurally singular rail entry invokes the Grammar's horizontal
traversal rule. The target Node opens to the right of the source occurrence.
Switching eligible rail entries follows §13.4: an untraversed leaf MAY be
replaced; a traversed child and its continuation MUST be displaced and retained
through horizontal alternative insertion under the Path Inspector grammar.

## 26.2 Vertical Navigation

Activating a structurally plural affordance exposes its Collection Visualizer.
Navigating a holon row invokes the Grammar's vertical traversal rule and opens
the child Node beneath that Collection. The Collection keeps sibling context
available; the initial implementation MAY retain one active child per
Collection occurrence.

## 26.3 Recursive Exploration and Provenance

Every reached Node may invoke either traversal rule. The Space Navigator MUST distinguish
semantic holon identity from visualizer occurrence identity, and provenance
SHOULD record how each occurrence was reached. The same holon may appear in
multiple occurrences with different local selection, focus, visualizer, and
collection state.

---

# 27. Focus and Concrete Extent Realization

The Space Navigator tracks an active visualizer occurrence. Focus is distinct
from visibility and may determine the active traversal frontier, keyboard
target, layout priority, and contextual Space Navigator behavior.

The Grammar defines the valid extent states and their invariants. This Design
Specification applies them as follows:

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

---

# 28. Compression and Editing

Compression applies only to projection and presentation. It MUST NOT discard
the selected collection tab, selected rail affordance, child links, sort/filter
state, selected row, edit mode, staged-state reference, or selected Visualizer
identity. Re-expansion SHOULD restore prior local context where feasible.

The Grammar's parent-owned allocation rule applies while editing: visualizer
content may maximize locally within its allocation, but neither editing nor
maximization changes navigation topology or claims sibling space.

---

# 29. Loading States

Descriptor knowledge remains available internally before population is known;
relationship affordance visibility follows §16.4.

The Space Navigator SHOULD distinguish:

- not loaded;
- loading;
- loaded empty;
- loaded with contents;
- failed.

Discovery state and destination realization state are distinct. Before structural
navigation, use current existence evidence or inspect the relationship. If the
result is zero, indicate locally that it has no targets, refresh its browse
visibility, and leave source extent, focus, and existing destination unchanged.
An invalid singular cardinality follows validation/error semantics.

For a valid destination, establish its region first under Path Inspector §2.8.
A lightweight temporary presentation MUST occupy the final destination region
before the actual visualizer appears. For example, show `Opening DescribedBy…`
in the right-hand Node slot or `Opening Orders…` in the collection region. This
communicates destination and intent; it need not expose technical progress or
be a separately named Visualizer Commons role.

Resolve/load the destination and select/materialize its visualizer, then replace
the pending presentation in-place without relocating the destination. Cached or
prefetched data MUST NOT bypass the visible structural ordering; no fixed delay
is required. Source compression, region opening, and pan/reflow should communicate
the navigation topology without abrupt title/content swaps. Respect reduced motion
while retaining the sequence and localized feedback.

After allocation, realization failure is shown in that destination with retry
feedback under the existing selection/error contract. If a target disappears
during resolution, show the changed/empty outcome there and refresh discovery;
do not fabricate a target. This race differs from knowingly opening an empty
relationship. Superseded requests MUST NOT overwrite a newer destination or
restore stale counts after context changes.

---

# 30. Progressive Retrieval

The Space Navigator SHOULD favor lazy retrieval.

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

---

# 31. Entering Edit Mode

When the person selects **Edit** on a persisted holon:

1. MAP stages or exposes a new version of that holon;
2. the existing Node Visualizer occurrence remains in place;
3. the visualizer enters edit mode;
4. editable scalar properties become interactive;
5. editable relationship and collection affordances become mutable where allowed;
6. transaction status becomes visible at Space Navigator scope.

Entering edit mode is a state transition, not a navigation transition.

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

Entering edit mode MUST NOT inherently disable navigation.

The person may continue to:

- inspect collections;
- navigate vertically;
- navigate horizontally;
- open other holons;
- edit additional holons.

Staged work remains intact.

---

# 36. Compressing Editable Visualizers

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

# 37. Create

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

# 38. Clone

When **Clone** is invoked:

1. MAP creates a new staged holon initialized from the source according to clone semantics;
2. the new holon receives its own semantic identity;
3. it is presented in normal edit mode;
4. it participates in the active transaction.

Clone source history is not automatically treated as Space Navigator traversal provenance.

After staged initialization, Clone and Create use the same editing interaction model.

---

# 39. Delete

Delete is a holon-scoped action.

When invoked:

1. the person receives any required explicit confirmation;
2. deletion is staged according to MAP semantics;
3. the staged deletion participates in the active transaction;
4. Commit later publishes it with other staged changes.

Delete MUST NOT imply physical erasure of historical committed state.

The exact post-Commit presentation of deleted holons remains a design detail to refine.

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

# 49. Personalization and Constrained Geometry

Ordering has practical consequences under constrained space.

For example:

- top-ranked properties remain visible longest when vertically constrained;
- leftmost collection tabs remain visible longest when horizontally constrained;
- highest singular-navigation entries remain visible longest when vertically constrained;
- prominent actions remain outside overflow longest.

Thus personalization and adaptive salience help determine graceful degradation under compression.

---

# 50. Interaction Scenarios

## 50.1 Inspect a Holon

Given a holon:

1. obtain semantic and presentation context;
2. select an applicable Node Visualizer;
3. display identity and scalar properties;
4. progressively expose verified populated singular relationships in the right rail;
5. progressively expose verified populated plural relationships, with known counts,
   in the bottom tab bar; expose other affordances according to their contracts;
6. expose holon-level actions;
7. show no child collection or right-side Node Visualizer until selected.

---

## 50.2 Open a Multi-Valued Relationship

Given plural relationship R:

1. discovery establishes that R is populated and reveals its Collection Tab;
2. select R and establish current target existence;
3. open or retain the collection region below the node at matching width;
4. show `Opening R…` in that region;
5. load targets and select/materialize the Collection Visualizer in-place;
6. retain the source node as context.

One or many targets use the same plural structure. Zero targets produce local
feedback without allocating a region, except in explicit empty inspection/edit flows.

---

## 50.3 Navigate Through a Collection

Given Node A and Collection C:

1. select or double-click row B for navigation;
2. create a Node Visualizer occurrence for B below C;
3. preserve A and C;
4. record provenance;
5. preserve C so sibling rows remain accessible;
6. optionally compress A vertically.

---

## 50.4 Follow a Singular Relationship

Given Node A and singular relationship R:

1. discovery establishes R has a target and reveals it in the right rail;
2. activate R and establish valid target existence;
3. partially compress expanded A and allocate the right-hand destination;
4. show `Opening R…` in that slot;
5. resolve B and select/materialize its Node Visualizer in-place;
6. preserve provenance from A through R and the grammar's focus/retention rules.

---

## 50.5 Continue Horizontally

Given:

    A -> B

if B opens C:

- C becomes the active frontier;
- B may retain immediate singular-navigation context;
- A may compress more aggressively;
- prior subordinate geometry compresses with its owner.

Repeated horizontal traversal progressively compresses leftward provenance.

---

## 50.6 Continue Vertically

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

## 50.7 Mixed Traversal

A node reached horizontally may descend through a collection.

A node reached vertically may open a singular reference.

The same rules apply recursively.

An occurrence may therefore become compressed in both axes.

---

## 50.8 Enter Edit Mode

Given persisted Node A:

1. invoke Edit from A's Node Action Bar;
2. stage A;
3. keep A in the same occurrence;
4. switch A to edit mode;
5. make permitted scalar and relationship affordances editable;
6. reflect active transaction state in the Space Navigator Action Bar.

---

## 50.9 Edit Scalar Property

Given staged A:

1. edit a scalar value through its Property/Value Visualizer;
2. update staged semantic state;
3. establish an Undo boundary when the interaction is complete;
4. retain navigation context.

---

## 50.10 Edit Array

Given staged A and array property P:

1. open P's Collection Tab;
2. use the Collection Visualizer;
3. add/remove/edit/reorder as permitted;
4. update staged state;
5. establish meaningful Undo boundary.

---

## 50.11 Edit Multi-Valued Relationship

Given staged A and plural relationship R:

1. open R's Collection Visualizer;
2. add or remove targets as permitted;
3. update A's staged relationship state;
4. retain ordinary collection navigation.

---

## 50.12 Edit Singular Relationship

Given staged A and singular R:

1. keep R in the right rail;
2. set/replace/clear target when permitted;
3. update A's staged relationship state;
4. continue to allow ordinary navigation to the current target.

---

## 50.13 Edit Related Holon Separately

Given staged A and related B:

1. navigate to B;
2. B initially remains read-only unless already staged;
3. invoke Edit on B;
4. B joins the active transaction;
5. A and B now contain independent semantic changes within one transaction.

---

## 50.14 Create

Given concrete type T:

1. invoke Create Instance;
2. stage new holon A;
3. display A in edit mode;
4. edit through normal visualizers;
5. A participates in the active transaction.

---

## 50.15 Clone

Given persisted A:

1. invoke Clone;
2. create staged B initialized from A;
3. display B in edit mode;
4. modify B;
5. B participates in the active transaction.

---

## 50.16 Delete

Given persisted A:

1. invoke Delete;
2. confirm if required;
3. stage semantic deletion;
4. reflect staged deletion state;
5. publish only when the Space Navigator transaction is committed.

---

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

Given staged A:

1. traversal requires space;
2. A compresses normally;
3. staged state remains authoritative in Rust;
4. compact A indicates staged state;
5. re-expansion restores editing context.

---

# 51. Open Design Questions

The following remain intentionally unresolved.

## 51.1 Sibling History

When switching among singular affordances or collection rows:

- discard previous sibling;
- retain hidden history;
- preserve explicit branches?

Initial recommendation: replacement with recoverable local state.

---

## 51.2 Compression Thresholds

Exactly when should a visualizer become:

- partially compressed;
- fully compressed?

This should be informed by implementation experiments and available geometry.

---

## 51.3 Horizontal Overflow

If compression is insufficient:

- horizontal scrolling;
- panning;
- stronger ancestor collapse;
- another strategy?

---

## 51.4 Vertical Overflow

Likewise:

- vertical scrolling;
- panning;
- stronger compression?

---

## 51.5 Scalar Dance Results

Determine initial presentation and persistence semantics.

---

## 51.6 Dance Result Tabs

Should collection-valued dance affordances:

- have tabs before invocation;
- appear after invocation;
- appear in a distinct unexecuted state?

---

## 51.7 Empty Singular Relationships

Normal browsing suppresses verified empty relationships (§16.4). The exact visual
treatment in edit, schema-inspection, and diagnostic modes remains open.

---

## 51.8 Branch Closing

Determine whether and how traversal branches can be explicitly pruned.

---

## 51.9 Focus Presentation

Define the visual treatment of the active frontier.

---

## 51.10 Transaction Abandon Semantics

Define exactly what happens when the person abandons or reverts an active transaction.

---

## 51.11 Multiple Occurrences of a Staged Holon

Define the precise visual synchronization behavior when one staged holon appears in multiple occurrences.

The semantic state remains singular and Rust-owned.

---

## 51.12 Relationship Target Selection

Define the generic UX used to select targets when editing relationships.

---

## 51.13 Deleted Holon Presentation

Define how staged and committed deleted holons appear within existing traversal provenance.

---

# 52. Non-Goals of the Initial Design

The initial Space Navigator does not need to fully support:

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

These capabilities may evolve without changing the core design grammar.

---

# 53. Normative Design Invariants

## 53.1 Descriptor Semantics Over Runtime Accident

Declared cardinality and result shape determine structural presentation.

## 53.2 Visualizer Categories Are Roles

Do not equate a category such as Node Visualizer with one permanent concrete implementation.

## 53.3 Generic Fallbacks Preserve Basic Use

Previously unknown semantic types should remain usable when no specialized
visualizer exists. The Rust DAHN Selector selects the generic fallback; the
TypeScript runtime realizes the implementation it is supplied.

## 53.4 Singular Traversal Goes Right

Single-holon traversal extends horizontally.

## 53.5 Plural Traversal Goes Down

Multi-valued traversal extends vertically through a Collection Visualizer.

## 53.6 Navigation Preserves Provenance

Traversal should add or compress context rather than erase it.

## 53.7 Holon Identity Is Not Occurrence Identity

One holon may appear in multiple traversal contexts.

## 53.8 Child Content Claims Space Only When Activated

Navigation affordances may be visible before their child visualizers consume space.

## 53.9 Parent Geometry Constrains Subordinate Geometry

Compressed parents cannot leave full-size subordinate content behind.

## 53.10 Compression Preserves State

Compression changes presentation, not semantic or navigation state.

## 53.11 Read and Edit Share One Visual Grammar

Do not introduce separate browse and form architectures.

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

Classify structural affordances from descriptors before retrieving expensive
contents. Progressively expose populated relationships in normal browsing.
Establish existence before structural navigation and destination real estate
before destination content; pending and final content occupy the same region.

---

# 54. Summary

The DAHN Space Navigator is a descriptor-driven, adaptive, two-dimensional
Dancer experience for navigating and manipulating a MAP Space.

Its primary visual grammar is:

- **Node Visualizer** for a holon;
- **Vertical Single-Value Tab Rail** for singular holon affordances;
- **Horizontal Collection Tab Bar** for plural affordances;
- **Collection Visualizer** for homogeneous collections;
- **Space Navigator Action Bar** for transaction- and Space-Navigator-scoped actions.

Its central semantic rule is:

> **Definitions determine structure; runtime data populates it.**

Its central navigation rule is:

> **Follow one thing horizontally; choose among many things vertically.**

Its central geometric rule is:

> **The Rooted Navigation Visualizer allocates its Canvas-provided
> space toward the active traversal frontier and compresses provenance behind it.**

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


## Slot-directed selection alignment

Child selection follows DAHN §13.2.1: supply the actual composition slot, match
its accepted Visualizer types, and search the subject descriptor self-first only
through its nearest TKD. No compatible candidate at that boundary is an error.
A default is an ordinary applicable Visualizer, not a client-side fallback.
The Node's PropertyMapSlot accepts PropertyMapVisualizer; the default renderer is
DefaultPropertyMapVisualizer.PropertyMapVisualizer. Its PropertySlot accepts a
single PropertyVisualizer per name/value pair. HasSlot defines composition and
AcceptsVisualizerType is definitional. Multiple-candidate ranking remains deferred.
