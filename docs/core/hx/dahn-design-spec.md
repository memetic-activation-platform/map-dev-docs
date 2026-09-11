# DAHN Design Specification v2.0

## Status

Draft replacement for `dahn-phase-0-design-spec.md` v1.4.

This version re-baselines the DAHN design around the architecture that has emerged through the Space Navigator, Dancer, Selector Function, self-describing Active Holon, and dynamic Visualizer work.

It supersedes the Phase-0-specific visualizer selection, canvas, affordance hierarchy, and dynamic-loading models in v1.4 while preserving still-valid MAP/DAHN boundary decisions.

## Change Log

### v2.0

Major architectural re-baseline of the DAHN design specification.

This version supersedes the Phase-0-specific visualizer, selector, canvas, affordance, and dynamic-loading model in v1.4 while preserving the still-valid MAP/DAHN boundary decisions.

Key changes:

- moves final Visualizer selection authority fully into Rust;
- removes the prior split between Rust-side semantic recommendation and TypeScript-side final resolution;
- replaces selector output as a Canvas mount plan with recursive per-request Visualizer selection;
- introduces `VisualizerKind` as the DAHN-wide categorization used for discovery, selection, compatibility, stewardship, and eventual Commons organization;
- introduces `VisualizerSlot` as a Visualizer-local composition contract;
- distinguishes Visualizer kinds from local visualizer Slots;
- establishes recursive-but-centralized selection: Visualizers may create child visualization requests, but concrete child implementations are always selected by the DAHN Selector Function;
- generalizes selector input beyond `Holon` subjects so Node, Collection, Property, Value, Action, Canvas, and future Visualizer kinds can participate in the same selection architecture;
- establishes self-describing Active Holons as the semantic input to Visualizers through effective Properties, Relationships, and Dances;
- removes the preconstructed DAHN-global `AffordanceNode[]` presentation model as the primary Active Holon abstraction;
- makes descriptor-to-presentation projection the responsibility of the selected Visualizer;
- renames the current Node presentation strategy from `HolonNodeVisualizer` to `HolonInspectorVisualizer`;
- defines the six current `HolonInspectorVisualizer` Slots:
    - `NodeTitleBarSlot`
    - `ActionBarSlot`
    - `VerticalRailSlot`
    - `PropertiesViewerSlot`
    - `CollectionTabsSlot`
    - `CollectionViewerSlot`
- defines the `HolonInspectorVisualizer` projection grammar:
    - scalar Properties -> Properties Viewer
    - `ValueArray` Properties -> Collection Tabs
    - singular Relationships -> Vertical Rail
    - plural Relationships -> Collection Tabs
    - singular navigational Dances -> Vertical Rail
    - plural navigational Dances -> Collection Tabs
    - other applicable Dances -> Action Bar
- establishes structural cardinality, rather than runtime result count, as the basis for singular versus plural navigation semantics;
- aligns singular and plural navigation with the Space Navigator Interaction Grammar:
    - singular navigation -> horizontal lineage
    - plural Holon navigation -> collection-mediated vertical lineage
- introduces Property visualization as a first-class selection boundary;
- establishes `PropertiesVisualizer` selection separately from `ValueVisualizer` selection;
- introduces `ValueViewerSlot` as a typical child Slot of a Property Visualizer;
- makes `ValueType` a selector input rather than a direct renderer mapping;
- introduces Action visualization as a first-class selection boundary;
- allows each projected action/Dance affordance to select an `ActionVisualizer`;
- formalizes Collection visualization as a first-class Visualizer kind and selector boundary;
- replaces the prior minimal one-region scrolling Canvas model with the Space Navigator topology and projection model;
- clarifies the division between:
    - Canvas-owned navigation topology and external allocation;
    - Visualizer-owned internal composition and layout;
- establishes that compression, overflow, scanning, maximization, and restore ordinarily preserve selected Visualizer identity rather than trigger reselection;
- preserves parent-owned external allocation and child-owned internal composition;
- incorporates the dynamic Visualizer artifact architecture:
    - content-addressed executable identity;
    - separation of artifact stewardship from artifact transport;
    - Rust-side implementation resolution;
    - Rust-side digest/signature verification;
    - immutable local caching;
    - DAHN-controlled module materialization;
    - TypeScript-side instantiation only after authorization;
- removes browser URL/origin as the conceptual identity of a Visualizer implementation;
- aligns Visualizer executable artifacts with the broader MAP executable-artifact model also used for dynamic Dance WASM;
- distinguishes executable provenance from runtime safety;
- introduces the Visualizer Runtime Protocol as both an interoperability contract and a future capability/security boundary;
- preserves Web Components and dynamic import as possible implementation mechanisms without making them the architectural source of Visualizer identity or authority;
- preserves the public MAP SDK as the sole TypeScript-facing MAP boundary;
- preserves Rust as the authoritative holder of Holon/model semantic state;
- preserves reference-centered TypeScript access and avoids establishing a second authoritative TypeScript Holon model;
- preserves Rust-side effective descriptor flattening rather than TypeScript-side inheritance reconstruction;
- adds explicit architectural invariants covering Selector authority, Slots, recursive composition, navigation shape, artifact identity, verification, and bootstrap-selection behavior;
- treats deterministic bootstrap selection as ordinary policy rather than permanent one-Visualizer-per-kind mappings;
- adds explicit near-term design priorities for Selector requests, Slots, Dance semantics, Property/Value/Action visualization, dynamic artifact loading, and the Visualizer Runtime Protocol.

### v1.4

- aligned Phase 0 with the TypeScript MAP SDK implementation spec v1.3;
- recorded `BoundHolonCollection` as an abandoned design branch and removed it from the DAHN-facing target posture;
- treated public plural holon-backed traversal and relationship results as `HolonCollection`;
- treated query/navigation-like DAHN behavior as descriptor-afforded Dances invoked through the public SDK rather than through a command-owned query envelope;
- treated new-world Dance results as response-holon handles rather than standalone `DanceOutcome` objects;
- clarified that DAHN or other above-SDK caller layers own `RequestOptions` decisions such as `snapshot_after`, `gesture_id`, and `gesture_label`.

### v1.3

- captured an intermediate bound-first Dance/query contract posture;
- superseded by v1.4 for current `HolonCollection`, Dance-response, and query/navigation guidance.

---

# 1. Purpose

DAHN is the experiential layer through which people inspect, navigate, act upon, and eventually edit the self-describing active holons of the MAP.

This specification defines the DAHN runtime architecture required to support:

- self-describing Active Holons;
- Visualizers as open-ended, dynamically selectable presentation implementations;
- recursive Visualizer composition through Slots;
- centralized visualizer selection through the DAHN Selector Function;
- descriptor-driven projection of Properties, Relationships, and Dances;
- Space Navigator topology and allocation semantics;
- dynamic loading of Visualizer implementation artifacts;
- the public MAP SDK as the sole TypeScript-facing MAP boundary;
- Rust as the authoritative holder of MAP semantic state and DAHN selection state.

The specification intentionally separates:

- semantic description from presentation;
- Visualizer composition from Visualizer selection;
- Visualizer selection from implementation loading;
- navigation topology from Visualizer layout;
- executable artifact identity from artifact transport;
- artifact provenance from runtime authority.

---

# 2. Relationship to Adjacent Specifications

The DAHN specification hierarchy is:

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

The DAHN Architecture defines major subsystem ownership and boundaries.

The Space Navigator Interaction Grammar defines valid:

- navigation topology;
- horizontal and vertical lineage;
- branching;
- compression;
- overflow;
- re-rooting;
- allocation semantics.

This Design Specification defines the concrete DAHN mechanisms that realize those architectural and grammatical rules, including:

- Visualizer kinds;
- Visualizer Slots;
- Selector Function requests;
- Visualizer composition;
- descriptor-to-presentation projection;
- Holon Inspector visualization;
- Property, Value, Collection, and Action visualization;
- Visualizer loading and activation.

Implementation plans sequence this design into deliverable work.

---

# 3. Core Architectural Principles

## 3.1 MAP semantics remain authoritative

DAHN does not create a second semantic model of MAP data.

Authoritative Holon state, descriptors, relationships, Dances, transaction state, and other MAP semantics remain in Rust/MAP runtime layers.

TypeScript operates primarily through reference-backed public SDK objects and small derived presentation state.

---

## 3.2 Holons describe affordances, not UI

An Active Holon exposes what it is and what it affords through effective descriptors.

At minimum, DAHN must be able to discover:

    Properties
    Relationships
    Dances

Those semantic affordances do not prescribe how they are rendered.

The selected Visualizer determines how those affordances are projected into presentation.

---

## 3.3 Visualizers define presentation grammar

A Visualizer defines:

- its internal layout;
- its Slots;
- how semantic affordances populate those Slots;
- what child visualization requests it creates;
- how it realizes itself within the allocation assigned by its parent.

Different Visualizers may project the same Active Holon differently.

---

## 3.4 Visualizer selection is centralized

Concrete Visualizer implementations are selected exclusively through the DAHN Selector Function.

A Visualizer may request another Visualizer for one of its Slots, but it must not directly choose that child implementation.

Therefore:

> Selection is recursive and compositional, but centralized.

---

## 3.5 Visualizer composition and selection are separate

A parent Visualizer determines:

> A visualization of kind X is required here.

The Selector Function determines:

> Which available Visualizer of kind X should fulfill that request?

A Slot expresses the first question.

The Selector Function answers the second.

---

## 3.6 Navigation topology and Visualizer composition are separate

The Space Navigator owns occurrence topology and external allocation.

The selected Visualizer owns its internal realization within that allocation.

Compression, overflow, scanning, maximization, and other projection changes do not ordinarily cause Visualizer reselection.

---

# 4. Public MAP SDK Boundary

DAHN consumes MAP exclusively through the public TypeScript MAP SDK.

DAHN must not depend on:

- command-wire types;
- IPC envelopes;
- internal request metadata;
- private SDK command builders;
- transport implementation details;
- transitional bridge payloads;
- legacy query envelopes.

DAHN may consume public:

- `MapClient`;
- `MapTransaction`;
- `HolonReference`;
- `HolonCollection`;
- descriptor handles;
- Dance invocation handles;
- Dance response handles;
- public request-option surfaces.

The public SDK remains the semantic boundary between DAHN TypeScript and MAP runtime functionality.

---

# 5. State Ownership

## 5.1 Rust-owned state

Rust should remain authoritative for:

- Holon state;
- effective descriptors;
- transaction and staged mutation state;
- Holon references and caches;
- Selector Function policy and selection;
- selected Visualizer identity;
- Visualizer implementation resolution;
- artifact verification;
- other MAP semantic state.

---

## 5.2 TypeScript-owned state

TypeScript may own ephemeral presentation state such as:

- currently selected tab;
- local expansion state;
- transient hover/focus state;
- component-local layout state;
- temporary render projections;
- client-side DOM state.

Such state must not become an alternate source of truth for MAP semantics.

---

# 6. Active Holon Model

For DAHN purposes, an Active Holon is a Holon together with its effective semantic affordances.

Conceptually:

    ActiveHolon
        identity
        effective descriptor
            Properties
            Relationships
            Dances

The effective descriptor must already reflect the MAP descriptor semantics required for DAHN consumption.

TypeScript must not reconstruct descriptor inheritance independently.

---

# 7. Descriptor Requirements for DAHN

DAHN depends upon sufficiently expressive effective descriptors.

## 7.1 Property Descriptor

A Property Descriptor must provide enough information to determine at minimum:

- Property identity;
- Property label/description where available;
- associated ValueType;
- structural value semantics;
- constraints required for presentation;
- whether its value is scalar or collection-shaped.

---

## 7.2 Relationship Descriptor

A Relationship Descriptor must provide enough information to determine:

- relationship identity;
- target Holon Type;
- minimum cardinality;
- maximum cardinality;
- declared versus inverse relationship semantics;
- other presentation-relevant relationship metadata.

Navigation axis is based on structural cardinality.

Runtime result count must not change whether the affordance is treated as singular or plural.

---

## 7.3 Dance Descriptor

A Dance Descriptor must expose sufficient declarative semantics for a Visualizer to classify the Dance without:

- inspecting its implementation;
- relying on naming conventions;
- hard-coding knowledge of individual Dances.

At minimum, DAHN requires information sufficient to distinguish:

- navigational behavior;
- non-navigational actions such as commands and mutators.

It must also expose the structural shape of the Dance response.

Relevant dimensions may eventually include concepts such as:

    interaction intent
        navigation
        command
        edit
        create
        delete
        invoke
        ...

    effect semantics
        read-only
        mutating
        ...

    response shape
        none
        scalar
        0..1 Holon
        1 Holon
        0..* Holon
        1..* Holon
        structured result
        ...

These dimensions should remain declarative and should not dictate presentation.

---

# 8. Visualizer Model

## 8.1 AbstractVisualizer

`AbstractVisualizer` is the common semantic base for DAHN Visualizers.

A Visualizer describes a presentation implementation capable of fulfilling a visualization request.

An Abstract Visualizer may define zero or more Slots.

Conceptually:

    AbstractVisualizer
        Slots -> VisualizerSlot [0..*]

Visualizers are ultimately intended to be MAP-stewarded holons rather than permanently hard-coded application metadata.

---

# 9. VisualizerKind

`VisualizerKind` is a DAHN-wide classification.

It identifies the general kind of visualization provided by a Visualizer.

Initial kinds include:

    Canvas
    Node
    Collection
    Properties
    Value
    Action

Additional kinds may emerge as DAHN evolves.

`VisualizerKind` is expected eventually to participate in:

- Visualizer discovery;
- Visualizer Commons;
- stewardship;
- candidate filtering;
- compatibility constraints;
- Selector Function policy.

`VisualizerKind` must not be confused with the internal Slots of a particular Visualizer.

For example:

    PropertiesViewerSlot

is not automatically a DAHN-wide VisualizerKind.

---

# 10. VisualizerSlot

A `VisualizerSlot` is a composition contract owned by a Visualizer.

A Slot represents a semantic visualization role within its parent Visualizer's
composition. It is not a geometric region or an independently selected layout.

A Slot may define:

- semantic role;
- required `VisualizerKind`;
- cardinality;
- parent-supplied context;
- constraints on compatible child Visualizers.

A Slot does not select a concrete Visualizer implementation.
It does not encode pixel position, grid coordinates, responsive breakpoints,
direction, padding, gaps, or compression thresholds. The parent supplies a
bounded allocation; the selected Visualizer determines its own responsive
internal composition within that allocation.

Conceptually:

    Visualizer
        |
        | defines
        v
    VisualizerSlot
        |
        | is fulfilled through
        v
    VisualizerUsage
        |
        | uses
        v
    selected Visualizer

The distinction is fundamental:

> A Slot declares a visualization need.
> A VisualizerKind constrains the class of Visualizer that can satisfy it.
> The DAHN Selector Function chooses the actual Visualizer.

## 10.1 VisualizerUsage

`VisualizerUsage` is the context-owned holonic binding through which a Slot is
fulfilled. It establishes the required indirection:

    VisualizerSlot
        -> VisualizerUsage
        -> UsesVisualizer
        -> Visualizer

The shared Visualizer remains a capability stewarded by its provider or
Commons. A Usage belongs where use occurs, such as an I-Space or We-Space, so
future configuration, circumstance, and selection-history data need not write
to the shared Visualizer. PR 3 establishes only the structural bindings; it
does not define configuration, circumstance matching, analytics, or adaptive
selection. A Usage binds a selected Visualizer to a Slot under a circumstance;
it does not define the Slot or the Visualizer's internal layout policy.

---

# 11. Visualization Requests

The Selector Function operates on a visualization request rather than a simple category lookup.

Conceptually:

    VisualizerSelectionRequest
        subject
        requested_visualizer_kind
        slot / semantic role
        visualization context
        human agent
        applicable runtime constraints

The exact implementation types may evolve.

The contract must support richer selection than:

    select_visualizer(category)

---

# 12. Visualization Subject

The subject of a visualization request varies by VisualizerKind.

Examples:

    Node
        -> Active Holon

    Collection
        -> Collection or plural affordance result

    Properties
        -> set of Property Descriptors in the context of a bound Holon

    Value
        -> Value + ValueType + Property context

    Action
        -> Dance Descriptor / active action affordance

    Canvas
        -> navigation or experiential context

The selector must therefore not assume that every visualization subject is simply a Holon.

---

# 13. DAHN Selector Function

## 13.1 Responsibility

The DAHN Selector Function chooses the Visualizer that should fulfill a visualization request.

It may eventually consider:

- subject semantics;
- VisualizerKind;
- Slot role;
- Holon Type;
- Property semantics;
- ValueType;
- Dance semantics;
- current visualization context;
- human-agent preferences;
- collective preferences;
- prior interaction usefulness;
- trusted stewardship;
- available Visualizers;
- runtime compatibility;
- device/context constraints.

---

## 13.2 Rust ownership

Visualizer selection belongs in Rust.

TypeScript must not independently resolve:

    HolonType -> NodeVisualizer

or:

    Properties -> PropertiesVisualizer

or:

    ValueType -> ValueVisualizer

or:

    Dance -> ActionVisualizer

TypeScript submits or triggers visualization requests and instantiates the implementation selected by Rust.

There must not be separate Rust and TypeScript selection authorities.

---

## 13.3 Initial deterministic bootstrap policy

Early implementation may deterministically select the currently bundled
least-specialized applicable Visualizer. It is ordinary candidate selection,
not a separate exceptional mechanism.

For example:

    Node
        -> HolonInspectorVisualizer

    Collection
        -> TableVisualizer

If later selection considers increasingly specific circumstances, a Node
Visualizer applicable to `Holon` naturally remains the root candidate after
more-specific candidates are exhausted. If no applicable Visualizer exists,
selection fails explicitly because the visualization environment is incomplete.

The bootstrap policy must not be encoded as a permanent one-Visualizer-per-kind
ontology.

---

## 13.4 Recursive selection

Selection occurs recursively throughout a Visualizer composition tree.

Example:

    Active Holon
        |
        | Node request
        v
    Selector
        |
        v
    HolonInspectorVisualizer
        |
        | Properties request
        v
    Selector
        |
        v
    PropertiesVisualizer
        |
        | Value request
        v
    Selector
        |
        v
    ValueVisualizer

The same Selector Function participates at every boundary.

---

# 14. Visualizer Composition

A selected Visualizer determines its internal composition.

Its responsibilities include:

- defining Slots;
- assigning internal geometry;
- determining which semantic affordances populate each Slot;
- creating child visualization requests;
- responding to parent allocation changes.

The parent Visualizer determines composition.

The child Selector determines implementations.

---

# 15. HolonInspectorVisualizer

`HolonInspectorVisualizer` is the current least-specialized Node presentation strategy.

For the current implementation:

    kind = Node
        ->
    HolonInspectorVisualizer

for every Active Holon.

This is deterministic bootstrap policy, not a permanent architectural mapping.

---

# 16. HolonInspectorVisualizer Slots

The current Holon Inspector Visualizer defines six principal Slots:

    NodeTitleBarSlot
    ActionBarSlot
    VerticalRailSlot
    PropertiesViewerSlot
    CollectionTabsSlot
    CollectionViewerSlot

These Slots define the internal topology of this particular Node Visualizer.

Other Node Visualizers may define completely different compositions.

---

# 17. HolonInspectorVisualizer Descriptor Projection

The Holon Inspector Visualizer binds to an Active Holon and evaluates its effective descriptor.

It projects the Holon's semantic affordances into its Slots according to the following rules.

---

## 17.1 Scalar Properties

A Property whose `ValueType` is not `ValueArray` is projected into the Properties Viewer.

    Property
        WHERE ValueType != ValueArray
            ->
        PropertiesViewer

The number of rows is determined dynamically from the bound Holon's descriptor.

No compile-time knowledge of the Holon Type is required.

---

## 17.2 ValueArray Properties

A Property whose `ValueType` is `ValueArray` is projected into Collection Tabs.

    Property
        WHERE ValueType == ValueArray
            ->
        CollectionTabs

Activating the tab exposes its values through the Collection Viewer.

A ValueArray does not inherently imply navigation to another Holon.

---

## 17.3 Singular Relationships

A Relationship whose structural maximum cardinality is one is projected into the Vertical Rail.

    Relationship
        WHERE max_cardinality <= 1
            ->
        VerticalRail

Activation produces horizontal traversal in the Space Navigator.

An empty singular relationship remains structurally singular.

---

## 17.4 Plural Relationships

A Relationship whose structural maximum cardinality is greater than one is projected into Collection Tabs.

    Relationship
        WHERE max_cardinality > 1
            ->
        CollectionTabs

Selecting that tab exposes a Collection.

Selecting a Holon member produces collection-mediated vertical traversal.

A zero- or one-member runtime result remains structurally plural.

---

## 17.5 Singular Navigational Dances

A navigational Dance whose response is structurally capable of producing no more than one Holon is projected into the Vertical Rail.

    navigational Dance
        AND response cardinality <= 1 Holon
            ->
        VerticalRail

Activation produces horizontal continuation.

---

## 17.6 Plural Navigational Dances

A navigational Dance whose response may produce more than one Holon is projected into Collection Tabs.

    navigational Dance
        AND response cardinality > 1 Holon
            ->
        CollectionTabs

The Dance is invoked when required, its result is exposed as a Collection, and selection of a Holon result produces vertical traversal.

---

## 17.7 Other Dances

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

---

# 18. Structural Cardinality Invariant

Navigation axis is derived from the structural shape of an affordance, not the cardinality of a particular runtime result.

Therefore:

    singular relationship returning zero
        -> remains horizontal

    plural relationship returning one
        -> remains collection-mediated vertical

    plural navigational Dance returning one result
        -> remains collection-mediated vertical

This preserves spatial consistency and conforms to the Space Navigator Interaction Grammar.

---

# 19. Properties Viewer

The `PropertiesViewerSlot` is local to `HolonInspectorVisualizer`.

The Properties Viewer is not responsible for directly rendering arbitrary
Properties. It creates a Properties visualization request for the dynamic set
of scalar Property Descriptors, then asks the DAHN Selector Function to select
a `PropertiesVisualizer`.

Conceptually:

    PropertiesViewer
        |
        +-- scalar Property set
                ->
            Selector(kind = Properties)

The Properties Viewer owns the name/value-column composition.

The selected Properties Visualizer owns set-level presentation such as layout,
ordering, grouping, salience, and responsive thresholds. It may recursively
select Value Visualizers for the values it contains.

---

# 20. PropertiesVisualizer

`PropertiesVisualizer` is a DAHN-wide VisualizerKind.

A Properties Visualizer presents a set of Properties as semantic Properties,
rather than merely displaying raw values. It may organize labels, metadata,
validation state, editing affordances, constraints, help, ordering, grouping,
and responsive layout. A typical Properties Visualizer defines one or more
`ValueViewerSlot`s.

---

# 21. ValueViewerSlot

A Properties Visualizer may define:

    ValueViewerSlot
        required VisualizerKind = Value

The Properties Visualizer determines the layout and context of the slot.

It does not choose the concrete Value Visualizer.

Instead it creates another DAHN Selector request.

---

# 22. ValueVisualizer

`ValueVisualizer` is a DAHN-wide VisualizerKind.

Value selection may consider:

- ValueType;
- Property Descriptor;
- actual value;
- view/edit mode;
- parent Property Visualizer;
- Holon context;
- agent preferences;
- specialized Visualizers available in Commons.

Example:

    publicationDate Property
        |
        v
    PropertiesVisualizer
        |
        v
    ValueViewerSlot
        |
        v
    Selector
        kind = Value
        ValueType = Date
        |
        v
    DateValueVisualizer

Properties and Value visualization are therefore distinct selection boundaries.

---

# 23. Action Bar and ActionVisualizer

The Holon Inspector Visualizer projects applicable non-navigational Dances into its Action Bar.

The Action Bar should not permanently own one rendering implementation for every action.

For each action affordance it may create an Action visualization request:

    Dance Descriptor
        |
        v
    ActionBar
        |
        v
    Selector
        kind = Action
        |
        v
    selected ActionVisualizer

`ActionVisualizer` is therefore a DAHN-wide VisualizerKind.

A simple button or menu item may serve as an initial deterministic bootstrap selection.

Specialized Action Visualizers may eventually exist for richer behaviors.

---

# 24. Collection Tabs

The `CollectionTabsSlot` is the Holon Inspector Visualizer's index of collection-shaped affordances.

It may contain tabs corresponding to:

- plural Relationships;
- ValueArray Properties;
- plural navigational Dances.

These sources have different semantics but share a useful information shape:

> Activating this affordance exposes a Collection.

The tab itself should preserve the semantic origin of the Collection.

---

# 25. Collection Viewer

The `CollectionViewerSlot` presents the active Collection selected through Collection Tabs.

The Collection need not be eagerly loaded merely because its descriptor is visible.

The intended sequence is:

    inspect descriptors
        ->
    derive CollectionTabs
        ->
    user activates tab
        ->
    resolve/invoke plural affordance
        ->
    obtain Collection
        ->
    select a Collection Visualizer
        ->
    render Collection

This preserves lazy traversal and avoids unnecessary relationship expansion or Dance invocation.

---

# 26. Collection Visualizers

`Collection` is a DAHN-wide VisualizerKind. Concrete Collection Visualizers
are named for presentation strategy, such as `TableVisualizer`,
`GalleryVisualizer`, `ListVisualizer`, `GraphVisualizer`, or
`TimelineVisualizer`.

Different collection shapes may eventually select different Visualizers based on:

- member type;
- source affordance;
- schema;
- cardinality;
- available columns;
- context;
- agent preference.

The initial Space Navigator may use a generic tabular Collection Visualizer.

---

# 27. Node Navigation Semantics

The Holon Inspector Visualizer realizes the Space Navigator Interaction Grammar as follows.

## Singular navigation

    Vertical Rail
        ->
    horizontal lineage

Typical sources:

- singular Relationships;
- singular navigational Dances.

## Plural navigation

    Collection Tab
        ->
    Collection Viewer
        ->
    selected Holon
        ->
    vertical lineage

Typical sources:

- plural Relationships;
- plural navigational Dances.

ValueArray Collections may use the same Collection Viewer surface without necessarily producing Holon navigation.

---

# 28. Canvas and Space Navigator Responsibilities

The Canvas owns navigation topology and the external allocation of Visualizer occurrences.

The Canvas is responsible for:

- occurrence placement;
- topology retention;
- horizontal lineage;
- vertical lineage;
- branching;
- compression allocation;
- overflow;
- focus projection;
- re-rooting;
- discoverability of hidden lineage.

The Canvas does not dictate the internal composition of a Visualizer.

---

# 29. Parent-Owned Allocation

The parent Canvas or parent Visualizer owns each child's external allocation.

A child Visualizer owns internal composition within that allocation.

Conceptually:

    Parent
        assigns:
            x
            y
            width
            height

    Child Visualizer
        determines:
            internal layout
            visible Slots
            compact realization

A child must not independently claim Canvas space outside the allocation supplied by its parent.

---

# 30. Compression and Visualizer Identity

The selected Visualizer identity survives:

- partial compression;
- full compression;
- scanning;
- overflow;
- maximization;
- restore.

The Selector Function should not ordinarily select separate Visualizers such as:

    FullNodeVisualizer
    RailOnlyNodeVisualizer
    CollectionsOnlyNodeVisualizer
    CompressedNodeVisualizer

for projection-state changes.

Instead:

    HolonInspectorVisualizer
        +
    current allocation
        ->
    appropriate internal realization

Another Node Visualizer may realize the same allocation states differently.

---

# 31. HolonInspectorVisualizer Extent Realization

The Holon Inspector Visualizer may define concrete realizations for Space Navigator allocation states such as:

    X expanded + Y expanded
        -> Full Node

    X partially compressed
        -> singular-navigation / rail-oriented realization

    X fully compressed
        -> horizontal compact identity realization

    Y partially compressed
        -> collection-navigation-oriented realization

    Y fully compressed
        -> vertical compact identity realization

Exact region retention, geometry, thresholds, and rendering remain design details of `HolonInspectorVisualizer`.

The interaction grammar defines the required semantics; the Visualizer defines their concrete realization.

---

# 32. Visualizer Runtime Contract

A dynamically instantiated Visualizer requires a stable DAHN runtime contract.

The exact TypeScript API may evolve, but it should provide only the capabilities required by the Visualizer.

Possible capabilities include:

    read descriptor
    read value
    traverse relationship
    invoke Dance
    request navigation
    stage edit
    request child visualization
    report interaction
    request local layout change

The runtime protocol should avoid exposing unrestricted host capabilities.

---

# 33. Visualizer Runtime Security Boundary

Artifact provenance establishes what code is executing.

It does not establish that the code is safe.

Therefore contributed Visualizers should eventually execute through constrained DAHN capabilities rather than automatically receiving unrestricted access to:

- filesystem;
- shell;
- arbitrary networking;
- arbitrary Tauri commands;
- conductor internals;
- unrestricted MAP APIs.

The Visualizer Runtime Protocol is therefore both:

- an interoperability contract;
- an execution-authority boundary.

---

# 34. Visualizer Definition and Stewardship

Visualizer definitions should be treated as semantic MAP resources rather than permanently as compile-time TypeScript objects.

A Visualizer definition may eventually include:

    identity
    version
    VisualizerKind
    Slots
    applicability
    Visualizer protocol version
    implementation artifact
    steward
    signatures
    compatibility metadata

Early implementations may bootstrap these definitions locally.

That bootstrap representation must not become the permanent architecture.

---

# 35. Visualizer Commons

Visualizers are expected eventually to be stewarded in federated Commons.

Commons can provide:

- Visualizer discovery;
- descriptions;
- versions;
- VisualizerKind;
- applicability;
- stewardship;
- provenance;
- endorsements;
- implementation metadata;
- artifact locations.

The Selector Function may use such information when choosing among candidate Visualizers.

---

# 36. Visualizer Implementation Artifacts

A Visualizer implementation should be treated as an immutable executable artifact.

Its durable identity should be content-based, not URL-based.

Conceptually:

    Visualizer
        implementation
            artifact digest
            artifact format
            entry point
            protocol version
            signer
            signature
            artifact locations

A URL answers:

> Where might these bytes currently be obtained?

It does not answer:

> What executable artifact is this?

---

# 37. Content-Addressed Identity

Visualizer implementation artifacts should be identified by digest.

For example:

    SHA-256 = abc123...

Any source returning bytes matching that digest has supplied the same immutable artifact.

Changing the executable produces a new artifact identity.

This allows:

- deterministic caching;
- mirroring;
- distributed acquisition;
- offline reuse;
- transport independence.

---

# 38. Distribution Does Not Imply Authority

Artifact stewardship and artifact transport are separate concerns.

A Visualizer artifact may be available from:

- local cache;
- MAP artifact provider;
- steward-hosted service;
- mirror;
- HTTPS;
- content-addressed storage;
- other future transports.

An untrusted mirror can safely distribute an artifact if the runtime verifies that the bytes match the selected digest.

Authority comes from MAP identity, stewardship, signatures, and policy.

Transport supplies bytes.

---

# 39. Visualizer Artifact Loading

The intended loading flow is:

    visualization request
        |
        v
    Rust Selector Function
        |
        v
    selected Visualizer
        |
        v
    implementation resolution
        |
        v
    artifact acquisition
        |
        v
    digest/signature verification
        |
        v
    immutable local cache
        |
        v
    DAHN-controlled runtime module handle
        |
        v
    TypeScript dynamic import / activation
        |
        v
    Visualizer Protocol validation
        |
        v
    Visualizer instantiation

TypeScript does not independently discover or authorize implementation artifacts.

---

# 40. DAHN-Controlled Module Materialization

A verified Visualizer artifact may be exposed to the WebView through a DAHN-controlled local or custom protocol.

Conceptually:

    map-visualizer://sha256/abc123/index.js

Such a URL is a runtime handle, not the Visualizer's semantic identity.

Its meaning is approximately:

> DAHN has resolved and verified the artifact having this content identity and made it available for frontend execution.

---

# 41. Visualizer Protocol Compatibility

A dynamically loaded Visualizer must declare the Visualizer Protocol version it implements.

The DAHN runtime must reject incompatible implementations.

A standard module entry point should be defined.

Conceptually:

    createVisualizer(context)

The exact contract belongs to implementation-level refinement.

---

# 42. Relationship to Dynamic Dance Implementations

Dynamic Dance implementations and Visualizer implementations share a common higher-level executable-artifact model.

    MAP executable artifact semantics
                |
        +-------+-------+
        |               |
      Dance          Visualizer
      WASM               JS
        |               |
    sandbox         UI runtime
        |               |
    Dance Protocol  Visualizer Protocol

Common principles include:

- immutable artifact identity;
- content addressing;
- agent stewardship;
- digital signatures;
- provenance;
- runtime policy;
- constrained execution protocols.

The runtime technologies differ, but the MAP trust and artifact model can remain coherent.

---

# 43. Initial Bootstrap Visualizers

The initial DAHN implementation should provide deterministic bootstrap
Visualizers sufficient to prove the architecture. The current Node strategy is
`HolonInspectorVisualizer`; the current Collection strategy is
`TableVisualizer`. Future candidates participate in the same selection space,
with increasingly general applicability considered only as selection policy.

Exact implementation sequencing belongs in implementation plans. If no
applicable and runnable Visualizer remains after policy evaluates the available
candidates, selection fails explicitly.

---

# 45. Design Tokens, Meta Design Systems, and Theme Ownership

DAHN presentation is grounded in a three-part model:

    DesignToken
        -> reusable named semantic presentation decision
    MetaDesignSystem
        -> versioned contract defining a complete token vocabulary
    Theme
        -> user-selectable complete typed value assignment for one MDS

## 45.1 Design Tokens

A DesignToken names what presentation decision is requested, not how a
component implements it. Examples include `Surface`, `Text`, `Focus`, and
`Space`; its identity is neither a CSS property nor a Theme value.

Every DesignToken has exactly one `DesignTokenType`. The initial types are
`Color`, `Dimension`, `FontFamily`, `FontWeight`, and `StrokeStyle`. They are
narrowly aligned with the equivalent DTCG token-type concepts. `DesignTokenType`
is MAP's first-class value classification, not a claim of complete DTCG
vocabulary or DTCG serialization conformance.

Design Tokens belong to a reusable vocabulary package with no dependency on
Themes or Meta Design Systems. A token may consequently be defined by many
MDSs; MDS membership does not establish token ownership.

## 45.2 Meta Design System Contract

A MetaDesignSystem (MDS) is a versioned semantic presentation contract. Its
`DefinesDesignToken` relationships identify the full set of token roles
available to its Canvases, Themes, and supporting Visualizers. A change in the
meaning of an existing role requires a new MDS version rather than a silent
reinterpretation.

MDS is MAP-native composition vocabulary. DTCG standardizes design-token
concepts and interchange formats, but does not standardize a MetaDesignSystem
entity.

Each Canvas is bound to exactly one MDS through `UsesMetaDesignSystem`. A Canvas may contain only Visualizers
that support that MDS. A Visualizer may support one or more MDSs and may consume
only a small subset of the MDS's tokens; its `ConsumesDesignToken` declarations
make that dependency explicit.

## 45.3 Themes and Complete Assignment

A Theme realizes exactly one MDS through `ForMetaDesignSystem`. It owns
`ThemeTokenAssignment` intersection holons, each of which binds exactly one
Theme, one DesignToken, and a concrete `PresentationValue`. The assignment's
semantic identity is the ordered `(Theme, DesignToken)` pair.

A Theme is valid for its MDS when, and only when, it has exactly one assignment
for every DesignToken defined by that MDS, and no assignments for other tokens.
Each assigned value must conform to that token's DesignTokenType. These are
schema validation rules, not optional runtime fallbacks.

This direct Theme-to-MDS dependency is intentional: it states the compatibility
contract explicitly and permits independent evolution of token vocabulary,
MDSs, and Themes without binding a Theme to a Dancer.

## 45.4 Theme Selection and Runtime Projection

Theme selection is person- and space-driven, orthogonal to Dancer choice. A
HolonSpace may `OffersTheme` to make Themes available; Themes are not supplied
by Dancers and do not have their own synthetic HolonSpace. The initial POC uses
the sole Theme offered by the active HolonSpace. A future space with several
offered Themes presents a choice to the person; personal-preference persistence
is deliberately outside this initial model.

On Canvas initialization, the runtime resolves the applicable Theme and invokes
the Theme wrapper's single projection operation to generate the fixed CSS
custom-property representation. That Theme graph is resolved once, not on every
Visualizer render. It refreshes only after an explicit Theme change or version
refresh. Visualizers consume these semantic token values and may derive their
internal presentation from them, preserving compatibility with independently
developed Visualizers.

---

# 46. DAHN Runtime Orchestration

The DAHN runtime coordinates:

1. obtaining a semantic subject;
2. creating a visualization request;
3. invoking the DAHN Selector Function;
4. resolving the selected Visualizer;
5. ensuring its implementation is available and verified;
6. instantiating the Visualizer;
7. binding the semantic subject and runtime context;
8. assigning external allocation;
9. allowing the Visualizer to recursively request child Visualizers.

A Visualizer should not independently recreate these host responsibilities.

---

# 47. Holon Access

DAHN should remain reference-centered.

The default posture is:

- authoritative Holon state in Rust;
- transaction-bound public `HolonReference` objects in TypeScript;
- plural results represented through `HolonCollection`;
- functional reads when required;
- small derived TypeScript presentation state;
- no eager full-Holon snapshot as the primary DAHN model.

Descriptor access should likewise remain reference-backed or use deliberately bounded presentational projections.

---

# 48. Lazy Semantic Expansion

Rendering an Active Holon's descriptor must not require eagerly traversing all semantic affordances.

For example:

- discovering a plural Relationship may create a Collection Tab without loading its members;
- discovering a plural navigational Dance may create a Collection Tab without invoking the Dance;
- Collection contents are resolved when the user activates the affordance.

This preserves scalability and aligns with the Space Navigator's inspect-then-navigate interaction model.

---

# 49. Commands and Dances

DAHN should treat active behavior primarily through descriptor-afforded Dances.

Legacy or separate command abstractions should not force the presentation layer into a permanent split if command behavior is represented through the Dance model.

Where Commands remain exposed as distinct MAP concepts, DAHN should normalize presentation through declarative affordance semantics rather than maintain independent hard-coded UI paths.

The design goal is that the Holon Inspector Visualizer can classify behavior from descriptors without understanding implementation dispatch.

---

# 50. Editing and Staged State

Editing is not fully specified here, but the architecture must preserve the established ownership model:

- authoritative staged mutation state belongs in Rust;
- Visualizers expose edit affordances through MAP operations;
- multiple Holons may participate in a transaction;
- undo/redo and snapshot semantics are host/runtime concerns;
- TypeScript Visualizers do not become authoritative mutable Holon stores.

Property and Value Visualizer separation should support future view/edit-specific Visualizer selection.

---

# 51. Interaction Reporting and Future Selector Learning

The Selector Function is expected eventually to evolve beyond deterministic bootstrap selection.

DAHN should therefore preserve a path for reporting interaction outcomes such as:

- Visualizer selected;
- context;
- user choice;
- dwell/use;
- explicit preference;
- repeated substitutions;
- task success;
- decision usefulness.

Such signals may later contribute to:

- individual preferences;
- collective preferences;
- affinity models;
- adaptive Selector Function behavior.

This learning architecture is outside the initial implementation scope but should not require changing the fundamental visualization-request model.

---

# 52. Architectural Invariants

The following are normative design constraints.

## INV-1 — Public SDK boundary

DAHN TypeScript depends only on the public MAP SDK.

## INV-2 — Rust model authority

Authoritative Holon and MAP semantic state remains in Rust.

## INV-3 — Active Holons describe semantics, not UI

Properties, Relationships, Dances, cardinalities, ValueTypes, and response shapes form semantic affordances.

## INV-4 — Visualizers own presentation grammar

The selected Visualizer determines how semantic affordances map into its Slots.

## INV-5 — VisualizerKind is DAHN-wide

Kinds classify Visualizers for discovery, selection, and eventual Commons stewardship.

## INV-6 — Slots are Visualizer-local

A Slot expresses a composition role defined by its parent Visualizer.

## INV-7 — Slots do not choose implementations

Child implementation selection always goes through the DAHN Selector Function.

## INV-8 — Selection is recursive and centralized

Visualizers may create additional visualization requests, but only the Selector Function chooses concrete Visualizers.

## INV-9 — Selector authority resides in Rust

TypeScript does not independently perform final Visualizer selection.

## INV-10 — Selection is richer than category lookup

Selection operates on semantic subject, requested kind, role/context, agent, and other relevant inputs.

## INV-11 — Properties and Value visualization are distinct

PropertiesVisualizer and ValueVisualizer are independent Visualizer kinds and selector boundaries.

## INV-12 — Actions are independently visualizable

Dance affordances may be rendered through selected ActionVisualizers.

## INV-13 — Structural cardinality determines navigation shape

Runtime result population does not alter singular versus plural interaction semantics.

## INV-14 — Singular navigation is horizontal

Structurally singular navigational affordances extend horizontal lineage.

## INV-15 — Plural Holon navigation is collection-mediated vertical

Structurally plural navigational affordances expose a Collection before selected-member traversal.

## INV-16 — Allocation does not ordinarily cause reselection

Compression, overflow, and local layout changes alter Visualizer realization rather than Visualizer identity.

## INV-17 — Parents own external allocation

Children compose only within the space assigned by their parent.

## INV-18 — Visualizer identity is independent of artifact location

Executable implementation identity is content-based.

## INV-19 — Verification precedes execution

External implementation artifacts must be verified before frontend execution.

## INV-20 — Distribution does not imply authority

Artifact transport and artifact stewardship are independent.

## INV-21 — Provenance does not imply safety

Signed code still requires constrained runtime authority.

## INV-22 — Visualizer loading is origin-agnostic

The architecture must not depend on browser URL/DNS semantics as the permanent delivery model.

## INV-23 — Bootstrap selection is policy, not ontology

Initial deterministic bootstrap selection must not encode permanent
one-Visualizer-per-kind assumptions.

---

# 53. Initial Holon Inspector Rendering Example

Consider a `Book` Holon whose effective descriptor exposes:

    Properties
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

The visualization flow is:

    Book Active Holon
        |
        | request kind = Node
        v
    DAHN Selector
        |
        v
    HolonInspectorVisualizer
        |
        +-- title
        |      -> PropertiesViewer
        |      -> select PropertiesVisualizer
        |      -> ValueViewerSlot
        |      -> select String ValueVisualizer
        |
        +-- subtitle
        |      -> PropertiesViewer
        |      -> PropertiesVisualizer
        |      -> String ValueVisualizer
        |
        +-- publicationDate
        |      -> PropertiesViewer
        |      -> PropertiesVisualizer
        |      -> Date ValueVisualizer
        |
        +-- keywords
        |      -> CollectionTabs
        |
        +-- publisher
        |      -> VerticalRail
        |
        +-- authors
        |      -> CollectionTabs
        |
        +-- openPrimaryEdition
        |      -> VerticalRail
        |
        +-- findRelatedBooks
        |      -> CollectionTabs
        |
        +-- deleteBook
               -> ActionBar
               -> select ActionVisualizer

The Holon has not defined any of this UI.

Its descriptors define semantic affordances.

`HolonInspectorVisualizer` defines the projection grammar.

The Selector Function selects each Visualizer implementation.

---

# 54. Implementation Posture

The implementation should evolve toward this architecture incrementally.

Early PRs may use:

- deterministic bootstrap Visualizer selection;
- local Visualizer descriptors;
- bundled implementations;
- local fixture artifacts;
- deterministic selector rules.

Those simplifications are acceptable only when clearly treated as bootstrap policy.

They must not establish incompatible architectural assumptions such as:

- TypeScript final selection;
- one Visualizer per VisualizerKind;
- direct child Visualizer selection by parent Visualizers;
- ValueType-to-renderer mappings outside the Selector;
- URL-as-Visualizer-identity;
- eager relationship traversal;
- monolithic Holon Inspector rendering of all child semantics.

---

# 55. Near-Term Design Priorities

The next design and implementation work should converge on:

1. formal `VisualizerKind` representation;
2. `AbstractVisualizer -> Slots -> VisualizerSlot -> VisualizerUsage -> Visualizer` ontology;
3. visualization-request / Selector Function contract;
4. Rust-owned Selector Function API;
5. HolonInspectorVisualizer Slot model;
6. effective Active Holon descriptor surface required by Node projection;
7. Dance Descriptor interaction semantics;
8. PropertiesVisualizer contract;
9. ValueViewerSlot and ValueVisualizer contract;
10. ActionVisualizer contract;
11. Collection Visualizer selection;
12. verified dynamic Visualizer implementation loading;
13. constrained Visualizer Runtime Protocol.

---

# 56. Superseded v1.4 Concepts

The following v1.4 concepts are explicitly superseded.

## TS-owned final Visualizer resolution

Superseded by:

> Rust owns final Visualizer selection.

---

## SelectorOutput as a Canvas mount plan

Superseded by:

> The Selector Function resolves individual visualization requests recursively; Canvas orchestration and Visualizer composition are separate concerns.

---

## One default Node Visualizer plus one default Action Menu as the selector model

Superseded by:

> Node, Collection, Property, Value, Action, Canvas, and future Visualizer kinds all participate in the same recursive Selector Function architecture.

---

## Property visualization directly driven by ValueType

Superseded by:

    Property
        ->
    PropertiesVisualizer selection
        ->
    ValueViewerSlot
        ->
    ValueVisualizer selection

ValueType remains a critical selector input but does not collapse Property and Value visualization into one layer.

---

## Generic preconstructed `AffordanceNode[]` as the Active Holon presentation model

Superseded by:

> The Active Holon exposes effective Properties, Relationships, and Dances; the selected Visualizer applies its own descriptor-to-presentation projection grammar.

Presentation grouping should not be prematurely imposed upstream of the selected Visualizer.

---

## Minimal one-region scrolling Canvas as the DAHN Canvas model

Superseded by the Space Navigator topology and projection architecture, including:

- occurrence-based navigation;
- horizontal lineage;
- vertical lineage;
- branching;
- independent axis compression;
- overflow;
- re-rooting;
- parent-owned allocation.

---

# 57. Result

This design establishes DAHN as a recursively compositional, self-describing visualization environment for the MAP.

The central runtime pattern is:

    semantic subject
        |
        v
    visualization request
        |
        v
    DAHN Selector Function
        |
        v
    selected Visualizer
        |
        +-- owns layout
        +-- owns Slots
        +-- interprets semantic affordances
        |
        +-- creates child visualization requests
                |
                v
            DAHN Selector Function
                |
                v
            selected child Visualizers

For Holons specifically:

    Active Holon
        |
        | effective descriptors
        v
    selected Node Visualizer
        |
        | Visualizer-specific projection grammar
        v
    Properties / Relationships / Dances
        |
        +-- Property Visualizers
        |       |
        |       +-- Value Visualizers
        |
        +-- Collection Visualizers
        |
        +-- Action Visualizers
        |
        +-- navigational continuation

The MAP provides semantic self-description.

Visualizers provide open-ended presentation strategies.

The Selector Function mediates between them.

The Space Navigator supplies persistent experiential topology.

Together, these mechanisms allow DAHN to remain generic enough to visualize Holon Types and behaviors that did not exist when DAHN itself was compiled, while preserving centralized selection, MAP stewardship, recursive composition, and runtime trust boundaries.
