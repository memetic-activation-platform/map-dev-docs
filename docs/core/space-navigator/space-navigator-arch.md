# DAHN Space Navigator Architecture Specification v0.4

## Status

Draft architecture specification.

v0.4 establishes that DAHN visualizers are first-class MAP Holons. It replaces
the former parallel `VisualizerDescriptor` / `VisualizerId` semantic model with
a small DAHN schema: Visualizer Holons have durable MAP identity, concrete
Visualizer Holon Types define their compositional contracts, and executable
implementations are related realizations rather than the visualizer's identity.

## Purpose

This specification defines the DAHN architectural contracts exercised by the **Space Navigator**, the first concrete DAHN Canvas Visualizer.

The Space Navigator is intentionally being used as an architectural proving ground. The architecture defined here therefore MUST support the Space Navigator without embedding assumptions that would prevent other Canvas Visualizers, Node Visualizers, Collection Visualizers, themes, adaptive behaviors, or interaction models from emerging later.

This specification is authoritative for cross-cutting DAHN architectural responsibilities and contracts, including:

- the boundary between Rust/MAP and TypeScript/DAHN;
- MAP semantic and transaction state ownership;
- DAHN experience-state ownership;
- Visualizer Commons;
- federated visualizer discovery;
- the DAHN Selector Function;
- adaptive personalization and collective salience;
- visualizer categories and runtime resolution;
- recursive visualizer composition;
- layout ownership and layout budgets;
- theme architecture;
- action scope;
- staged transaction ownership;
- Undo and Redo;
- multi-holon Commit;
- adaptive gesture reporting.

Space Navigator-specific visual behavior, navigation geometry, editing interaction, compression behavior, and user interaction scenarios are defined in `space-navigator-design-spec.md`.

The Space Navigator is not DAHN itself.

It is the first Canvas through which the DAHN architecture is exercised end-to-end.

---

# 1. Relationship to the Space Navigator Document Set

The Space Navigator documentation is organized into distinct layers:

- `space-navigator-concept.md` explains the conceptual model and rationale.
- `space-navigator-arch.md` defines reusable architectural responsibilities and contracts.
- `space-navigator-design-spec.md` defines normative Space Navigator behavior, including editing.
- `space-navigator-impl-plan.md` decomposes the architecture and design into implementation increments.

This specification SHOULD avoid restating Space Navigator-specific UX behavior except where necessary to establish an architectural boundary.

A useful rule is:

> Architecture defines who owns a capability and the contract between layers.

> Design defines how the Space Navigator uses that capability and what the person experiences.

---

# 2. DAHN

DAHN stands for:

**Dynamic Adaptive Holon Navigator**

The name reflects two foundational properties of the architecture.

## 2.1 Dynamic

DAHN dynamically composes an experience at runtime.

It does not assume that application developers know in advance:

- which holon types will be encountered;
- which properties those holons will expose;
- which relationships will exist;
- which dances will be available;
- which specialized visualizers will exist;
- which visualizer will be most appropriate in a particular context.

The experience is composed from runtime semantic information, including:

- MAP descriptors;
- effective affordances;
- result shape and cardinality;
- available visualizers;
- Canvas context;
- user preferences;
- layout constraints.

A previously unknown holon type SHOULD remain usable through generic visualizers even if DAHN has never encountered that type before.

## 2.2 Adaptive

DAHN also adapts from accumulated use.

Adaptive state may eventually incorporate:

- individual preferences;
- prior visualizer choices;
- property ordering;
- relationship ordering;
- collection-affordance ordering;
- action ordering;
- navigation behavior;
- collective salience;
- trends;
- long-term popularity;
- visualizer maturity;
- release history;
- exploration versus exploitation preferences;
- controlled novelty or randomness.

The experience therefore evolves without requiring centralized design-time control.

---

# 3. Existing MAP Deployment Architecture

DAHN executes within the existing MAP deployment architecture.

Conceptually:

    +-------------------------------------------------------+
    | Tauri Application                                    |
    |                                                       |
    |  TypeScript Runtime                                   |
    |                                                       |
    |    DAHN Experience Layer                              |
    |      +-- Canvas Visualizers                           |
    |      +-- Node Visualizers                             |
    |      +-- Collection Visualizers                       |
    |      +-- Property Visualizers                         |
    |      +-- Value Visualizers                            |
    |      +-- Action Visualizers                           |
    |      +-- layout / composition                         |
    |      +-- theme realization                            |
    |      +-- local interaction state                      |
    |                                                       |
    |    TypeScript MAP SDK                                 |
    |                    |                                  |
    |                    | JSON IPC                         |
    |                    v                                  |
    |  Rust MAP Host                                        |
    |      +-- command decode / dispatch                    |
    |      +-- MAP command layer                            |
    |      +-- dance invocation                             |
    |      +-- Query Dance                                  |
    |      +-- DAHN visualizer discovery                    |
    |      +-- DAHN Selector Function                       |
    |      +-- adaptive state                               |
    |      +-- Nursery                                      |
    |      +-- HolonsCache                                  |
    |      +-- Transient Holon Manager                      |
    |      +-- transaction snapshots                        |
    |      +-- Undo / Redo                                  |
    |      +-- validation                                   |
    |      +-- Commit                                       |
    |      +-- receptors / persistence / DHT                |
    +-------------------------------------------------------+

The TypeScript MAP SDK exposes MAP APIs as TypeScript functions.

Those functions map to commands that cross the Tauri JSON IPC boundary and are decoded and dispatched by the Rust MAP host.

Dance invocation is exposed through this command layer. Query is itself available as a dance, giving DAHN general access to MAP query capability through the same architecture.

---

# 4. Primary Responsibility Boundary

The central architectural boundary is:

> **Rust owns MAP semantic truth, adaptive selection, and transactional truth.**

> **TypeScript owns experience realization, spatial composition, and immediate interaction.**

This boundary SHOULD remain stable as DAHN becomes more capable.

---

# 5. Rust Responsibilities

Rust SHOULD own capabilities whose correctness depends on MAP semantics, persistent state, transaction state, DHT state, or adaptive history.

These include:

- persisted holons;
- staged holons;
- transient holons;
- Nursery state;
- HolonsCache;
- Transient Holon Manager;
- transaction lifecycle;
- transaction snapshots;
- Undo state;
- Redo state;
- validation;
- Commit;
- create;
- clone;
- update;
- delete semantics;
- relationship traversal;
- projection;
- dance execution;
- query execution;
- descriptor resolution;
- inheritance resolution;
- effective affordance resolution;
- authorization-sensitive semantic decisions;
- Visualizer Commons discovery;
- candidate Visualizer Holon discovery;
- Visualizer Holon applicability evaluation;
- DAHN Visualizer Holon selection;
- personal adaptive state;
- collective salience;
- trend information;
- maturity information;
- explore/exploit selection policy.

Rust SHOULD answer semantic questions such as:

- What is this holon?
- What is its effective descriptor?
- Which properties, relationships, and dances are effective?
- What is the declared cardinality of this relationship?
- What is the declared result shape of this dance?
- Which operations are currently permitted?
- Which Visualizer Holons are reachable through the user's Visualizer Commons relationships?
- Which candidate Visualizer Holons are applicable?
- Which Visualizer Holon should be preferred?
- What adaptive ordering should initially be presented?
- What staged changes currently exist?
- Can the current transaction Undo?
- Can it Redo?
- Is the transaction valid?
- Can it Commit?

Rust SHOULD NOT decide:

- where a visualizer appears on a Canvas;
- whether a Space Navigator traversal appears horizontally or vertically;
- which visualizer occurrence is compressed;
- which tab is currently selected;
- how many pixels a child receives;
- how a selected visualizer renders its controls;
- how a theme styles the selected visualizer.

---

# 6. TypeScript Responsibilities

TypeScript SHOULD own realization of the selected experience.

These responsibilities include:

- executable Visualizer Implementations;
- Canvas, Node, Collection, Property, Value, and Action implementation modules;
- visualizer runtime resolution;
- visualizer occurrence state;
- Canvas navigation provenance;
- focus;
- selections;
- active tabs and rails;
- geometry;
- responsive composition;
- layout budgets;
- compression presentation;
- local interaction state;
- immediate drag/reorder behavior;
- theme-token realization;
- mapping gestures to semantic MAP or DAHN requests;
- determining meaningful UX boundaries for transaction snapshots.

TypeScript answers questions such as:

- How should the selected visualizer render?
- Where does this child visualizer go?
- How much space does it receive?
- What is currently expanded or compressed?
- Which affordance is active?
- Which row is selected?
- How should a semantic action be represented at the current density?
- Has a meaningful editing gesture completed such that an Undo boundary should be established?

---

# 7. MAP State Versus Experience State

DAHN MUST distinguish authoritative MAP state from TypeScript experience state.

## 7.1 MAP State

Rust-owned MAP state includes:

- committed data;
- staged data;
- transient data;
- relationship state;
- transaction state;
- transaction snapshots;
- validation state;
- persistence state;
- adaptive preference state;
- aggregate salience state.

## 7.2 Experience State

TypeScript experience state includes:

- visualizer occurrence identity;
- Canvas placement;
- traversal path;
- selected affordances;
- selected rows;
- focus;
- compression presentation;
- viewport state;
- scroll state;
- temporary interaction state;
- animation state.

TypeScript MAY retain projections and render models obtained from Rust.

Those representations MUST NOT become an independent authoritative MAP object graph.

---

# 8. IPC Boundary

The IPC boundary SHOULD exchange semantic requests, references, descriptors, projections, selection results, adaptive signals, and transaction operations.

It SHOULD NOT duplicate the MAP runtime in TypeScript.

Typical TypeScript-to-Rust operations may include:

- inspect holon;
- retrieve projection;
- retrieve effective descriptor;
- expand relationship;
- invoke dance;
- invoke Query Dance;
- request DAHN presentation context;
- request visualizer selection;
- record adaptive gesture;
- stage new version;
- stage create;
- stage clone;
- mutate staged property;
- mutate staged relationship;
- establish Undo marker;
- Undo;
- Redo;
- validate transaction;
- Commit transaction;
- stage deletion.

Typical Rust-to-TypeScript results may include:

- holon references;
- property projections;
- effective descriptors;
- relationship descriptors;
- dance descriptors;
- collections;
- staged holon references;
- validation feedback;
- transaction status;
- Undo/Redo availability;
- selected Visualizer Holon reference and compatible implementation information;
- adaptive presentation ordering;
- indication that alternate visualizers are available;
- operation results.

The boundary SHOULD remain semantic rather than visual.

For example:

    expand relationship R from holon H

is appropriate.

The following is not:

    populate Space Navigator collection tab T

That is a TypeScript composition concern.

---

# 9. Visualizers Are Holons

Every DAHN Visualizer MUST have first-class MAP semantic identity.

A Visualizer is not fundamentally a TypeScript class, package, component
registration record, or opaque runtime identifier. It is a MAP Holon described
by a concrete Visualizer Holon Type. Its semantic state and relationships
describe the visualizer's applicability, capabilities, evolution, stewardship,
and one or more executable realizations.

Executable code realizes a Visualizer Holon. It does not define that Holon's
identity.

DAHN therefore uses MAP to describe both the semantic subjects being
experienced and the visualizers through which they are experienced.

## 9.1 Visualizer Holon Types

Visualizer categories are represented by the DAHN schema's type hierarchy, not
only by TypeScript/runtime categories. `Visualizer` is an abstract architectural
anchor. Ordinary Visualizer Holons MUST be described by stabilized concrete
descendants, consistent with the MAP rule that abstract descriptors are never
ordinary runtime instance targets.

The initial hierarchy SHOULD support at least:

    Visualizer (abstract)
      |
      +-- CanvasVisualizer
      +-- NodeVisualizer
      +-- CollectionVisualizer
      +-- PropertyVisualizer
      +-- ValueVisualizer
      +-- ActionVisualizer
      +-- GraphVisualizer

These types define compositional contracts. Individual Visualizer Holons are
instances of those concrete types. For example:

    Space Navigator                    instance of CanvasVisualizer
    Generic Holon Node Visualizer       instance of NodeVisualizer
    Table Collection Visualizer         instance of CollectionVisualizer

A specialized Event Node Visualizer is likewise a Visualizer Holon, rather
than a hard-coded DAHN category.

## 9.2 Semantic Identity and Executable Realization

DAHN distinguishes:

1. the **Visualizer Holon**, whose MAP identity is the durable semantic target;
2. a **Visualizer Implementation**, which is an executable realization for a
   particular runtime or platform; and
3. a **Visualizer Occurrence**, which is one use of that visualizer for a
   subject within a Canvas experience.

Conceptually:

    Generic Holon Node Visualizer
      |
      +-- implemented_by --> TypeScript Visualizer Implementation
      |
      +-- implemented_by --> Rust Visualizer Implementation

A Visualizer may outlive, replace, or gain implementations without losing its
semantic identity or the adaptive state that refers to it.

---

# 10. Generic Versus Specialized Visualizers

DAHN SHOULD provide generic fallback visualizers wherever practical.

Examples include:

- a Generic Holon Node Visualizer capable of displaying an arbitrary holon using core affordances;
- a Table Collection Visualizer capable of displaying a homogeneous collection;
- generic Property and Value Visualizers;
- generic Action Visualizers.

Specialized visualizers may provide richer presentation for more specific types or semantic shapes.

Conceptually:

    Holon
      |
      +-- Generic Holon Node Visualizer

    Event
      |
      +-- Event Node Visualizer

    Governance Model
      |
      +-- Governance Model Node Visualizer

The DAHN Selector SHOULD be able to prefer an applicable specialized visualizer while retaining generic fallback capability.

The Space Navigator MUST NOT treat a particular generic implementation as
synonymous with a Visualizer type or a generic Visualizer Holon.

## 10.1 Static Core Visualizers

Static implementation is an acquisition optimization, not a different semantic
model. Core fallbacks—including the Space Navigator, Generic Holon Node
Visualizer, Table Collection Visualizer, and generic Property, Value, and
Action Visualizers—MUST each have a corresponding Visualizer Holon even where
their initial executable implementations are compiled into the TypeScript or
Rust client.

The Space Navigator itself is a Visualizer Holon described by a concrete
`CanvasVisualizer` type. Its pinned Canvas Action Bar and navigation grammar
remain Space Navigator design concerns; its semantic identity and executable
realizations belong to this architecture and the DAHN schema.

---

# 11. Visualizer Commons

Visualizers are drawn from a federated network of **Visualizer Commons**.

A Visualizer Commons is a stewarded, governed MAP Agent Space containing and
stewarding Visualizer Holons and their related semantic resources.

Visualizer Commons are not centrally controlled by the MAP team.

Different commons may have different:

- governance models;
- contribution policies;
- review practices;
- trust models;
- maturity expectations;
- communities;
- domain emphases;
- aesthetic philosophies.

The visualizer ecosystem is therefore open and federated.

---

# 12. Accessible Visualizer Population

The effective population of candidate visualizers is determined through relationships of the user's Space.

Conceptually:

    MySpace
       |
       +-- We-Space relationship --> Visualizer Commons A
       |
       +-- We-Space relationship --> Visualizer Commons B
       |
       +-- We-Space relationship --> Visualizer Commons C

The full complement of eligible Visualizer Holons offered through those
accessible Commons is potentially available to the DAHN Selector.

Candidate inclusion may additionally depend on:

- authorization;
- compatibility;
- trust;
- availability;
- semantic and implementation compatibility;
- runtime support;
- other applicable semantic constraints.

The candidate population MUST NOT be assumed to consist only of visualizers shipped by the MAP team or bundled with the current client.

---

# 13. Visualizer Discovery

Visualizer discovery SHOULD be implemented as a MAP/Rust-side capability.

Discovery may require:

- traversing Space relationships;
- discovering accessible Visualizer Commons;
- discovering available Visualizer Holons;
- resolving semantic applicability;
- evaluating availability;
- evaluating compatibility;
- considering trust or governance information;
- considering versions.

Conceptually, discovery proceeds through ordinary MAP semantics:

    discover reachable Visualizer Commons
      -> discover available Visualizer Holons
      -> filter by Visualizer type and semantic applicability
      -> apply contextual and adaptive selection criteria
      -> select Visualizer Holon
      -> resolve compatible executable implementation

No centralized application registry is the semantic source of the Visualizer
population. A client-side mapping may exist only after selection, to resolve a
known Visualizer Holon or implementation reference to locally available code.

The TypeScript layer SHOULD NOT need to retrieve the full federated visualizer ecosystem merely to choose a visualizer.

---

# 14. Minimal DAHN Visualizer Schema

DAHN requires a MAP-native schema defining its own semantic entities. The first
schema increment MUST be deliberately small, but it MUST be sufficient to
represent statically bundled core visualizers without introducing a parallel
non-holonic descriptor model.

At minimum it MUST define:

- the Visualizer type hierarchy in Section 9.1;
- a `VisualizerImplementation` concept or equivalent implementation reference;
- an `implemented_by` relationship from a Visualizer Holon to its realizations;
- initial applicability semantics;
- the semantic capabilities required before execution; and
- enough identity and compatibility information for safe initial resolution.

A Visualizer Holon's concrete type descriptor defines the semantic shape of
that class of visualizer. The instance carries semantic metadata and
relationships used for discovery and selection. Information that was formerly
attributed to a conceptual `VisualizerDescriptor` belongs in those ordinary MAP
properties and relationships, or in related Holons where it has independent
identity and lifecycle.

The architecture does not prescribe that every concern become a scalar property
of the base `Visualizer` type. Release history, provenance, maturity,
compatibility, and adaptive measures MAY be represented by related Holons.

## 14.1 Applicability

Applicability MUST be MAP-semantic and available to the Rust Selector. The
initial schema MAY express it simply, for example:

    Generic Holon Node Visualizer
      applicable_to_type --> Holon

    Event Node Visualizer
      applicable_to_type --> Event

The Selector can use ordinary type lineage to determine specificity. The schema
MUST remain extensible because future applicability may depend on semantic
capabilities, result shapes, property/value types, relationship affordances, or
other declared constraints—not only a subject Holon Type.

## 14.2 Capabilities

If discovery, selection, compatibility, or parent composition requires a
characteristic before an implementation is executing, that characteristic MUST
be represented semantically in MAP. Examples include read/edit support,
supported semantic shapes, compact presentation, meaningful dimensions,
preferred geometry, and runtime requirements.

Implementation-private behavior MAY remain implementation-local.

## 14.3 Version and Evolution Domains

MAP's persisted Holon version and lineage metadata remain the authority for the
exact version of a Visualizer Holon and of an implementation Holon. DAHN MUST
NOT introduce an opaque `VisualizerId` or an unqualified `visualizer_version`
that conflates those identities.

Where a semantic compatibility or release contract requires a separately named
version, it MUST be modeled explicitly and remain distinct from the exact MAP
version/lineage of both the Visualizer and its implementation. The initial
schema SHOULD avoid choosing more version machinery than implementation
resolution requires.

---

# 15. DAHN Selector Function

The DAHN Selector Function executes on the Rust side.

It selects among available, applicable Visualizer Holons discovered through the
Visualizer Commons ecosystem and any applicable core fallback Visualizer Holons.

Conceptually:

    discovered visualizers
              |
    semantic applicability
              |
    personal preference
              |
    collective salience
              |
    trend / popularity
              |
    maturity / stability
              |
    context
              |
    explore / exploit policy
              |
              v
       selected Visualizer Holon

The Selector is therefore substantially more than a local UI component lookup.

---

# 16. Selector Inputs

The DAHN Selector may eventually consider:

- required Visualizer type/category;
- subject holon type;
- type lineage;
- descriptor semantics;
- property/value type;
- result shape;
- relationship cardinality;
- Canvas type;
- read/edit mode;
- available geometry;
- environment constraints;
- personal visualizer preference;
- personal ordering preferences;
- aggregate preference;
- aggregate salience;
- trend;
- historical popularity;
- Visualizer maturity;
- release stability;
- novelty;
- controlled randomness;
- exploration/exploitation posture.

The initial Selector implementation MAY use only a subset.

Its interface SHOULD NOT assume that type specificity alone will always determine the answer.

---

# 17. Explore Versus Exploit

DAHN selection SHOULD support an exploration/exploitation spectrum.

## 17.1 Exploit-Oriented Selection

Toward the exploit end:

- personal preferences receive greater weight;
- familiar visualizers are favored;
- mature visualizers are favored;
- deterministic behavior increases;
- novelty decreases;
- consistency and task efficiency dominate.

This is suitable for predictable work in which the person does not want the experience changing unexpectedly.

## 17.2 Explore-Oriented Selection

Toward the explore end:

- collective preferences may receive greater weight;
- trending visualizers may be favored;
- less mature visualizers may be permitted;
- novelty receives more weight;
- randomness may increase;
- discovery and experimentation dominate.

The policy belongs to DAHN adaptive selection rather than to individual visualizer implementations.

---

# 18. Adaptive Salience

DAHN may treat interaction gestures as salience signals.

Examples include:

- moving a property upward;
- moving a collection affordance leftward;
- moving a singular navigation affordance upward;
- moving an action toward greater prominence;
- choosing one Visualizer Holon instead of another;
- navigating a relationship;
- repeatedly selecting a collection.

Such signals may contribute to:

- immediate personalization;
- persistent personal preference;
- aggregate salience;
- collective Visualizer Holon preference;
- future default ordering.

---

# 19. Personal and Collective Adaptation

Adaptive state operates at multiple levels.

## 19.1 Personal Adaptation

A person's own prior choices SHOULD be capable of influencing their future experience.

Examples:

- preferred property ordering for a given holon type;
- preferred relationship ordering;
- preferred action ordering;
- preferred Visualizer Holon.

## 19.2 Collective Adaptation

Individual signals MAY also contribute to aggregate measures.

Collective state may influence:

- initial ordering for people without established personal preferences;
- default visualizer selection;
- trending visualizers;
- collective salience.

Collective adaptation is not required to be a simple popularity vote.

Different aggregation rubrics may weight signals differently.

---

# 20. Gesture Handling Boundary

TypeScript owns the immediate interaction consequence of a user gesture.

Rust owns the persistent learned meaning of that gesture.

For example:

    user drags property P above property Q
                |
    TypeScript reorders immediately
                |
    semantic adaptation event
                |
    MAP SDK / IPC
                |
    Rust persists preference / salience signal

This yields:

> **TypeScript owns the immediate consequence of a gesture.**

> **Rust owns its learned meaning.**

Adaptive persistence SHOULD NOT block immediate UI response.

---

# 21. Adaptive Presentation Context

Rust MAY provide adaptive ordering or other presentation guidance without requiring TypeScript to independently reconstruct personalization logic.

A conceptual presentation context might include:

    selected_visualizer_reference
    alternatives_available

    property_order
    singular_affordance_order
    collection_affordance_order
    action_order

    transaction_context
    capability_context

This presentation context MAY be combined with the effective descriptor or exposed separately.

The exact API remains to be defined.

---

# 22. Visualizer Selection Result

A DAHN selection result SHOULD identify the selected Visualizer Holon without
exposing all of the internal selector state.

A conceptual result may include:

    selected_visualizer_reference
    selected_visualizer_type
    compatible_implementation_references
    alternatives_available
    semantic_capability_context

The selected Visualizer reference is the durable semantic answer. An
implementation reference is resolution information, not a substitute identity.
Optional diagnostic information MAY be added later.

The TypeScript runtime SHOULD not need to reproduce the Rust selection
algorithm.

---

# 23. Visualizer Acquisition and Execution

Visualizer discovery and semantic selection are MAP-native concerns.

Visualizer acquisition and execution are client-runtime concerns.

Therefore:

> **Rust discovers and chooses.**

> **TypeScript resolves and executes.**

Conceptually:

    Rust DAHN Selector
          |
          | Visualizer Holon reference
          | compatible implementation information
          v
    TypeScript Visualizer Runtime
          |
          +-- locate available implementation
          +-- acquire if necessary
          +-- instantiate
          +-- execute / render

The initial implementation MAY resolve only locally bundled visualizers.

That is an initial acquisition strategy, not the permanent definition of the visualizer ecosystem.

---

# 24. Visualizer Runtime

TypeScript SHOULD provide a runtime capable of resolving a selected Visualizer
Holon and/or compatible Visualizer Implementation reference to executable code
available in the current client.

The runtime is distinct from the semantic DAHN Selector.

Its responsibilities may eventually include:

- local implementation lookup;
- package acquisition;
- version compatibility;
- loading;
- execution isolation;
- fallback if the selected implementation cannot execute.

The initial implementation MAY be a simple local mapping from known core
Visualizer Holon or implementation references to statically bundled code. That
mapping is an implementation-resolution mechanism, not the semantic visualizer
registry.

---

# 25. Trust and Compatibility

Because visualizers may originate in open federated Commons, future architecture MUST account for:

- provenance;
- trust;
- signing;
- code integrity;
- compatibility;
- versioning;
- sandboxing;
- runtime permissions;
- dependency isolation;
- package acquisition.

These concerns are outside the initial Space Navigator implementation scope.

However:

> Semantic applicability does not automatically imply runtime executability.

The selection and runtime-resolution boundaries SHOULD preserve room for these checks.

---

# 26. Recursive Visual Composition

DAHN visual composition is hierarchical.

Conceptually:

    Canvas Visualizer Holon selected for a Canvas subject/context
      |
      +-- client resolves executable implementation
      |
      +-- Action Visualizer Holons
      |
      +-- Node Visualizer Holons
            |
            +-- Action Visualizer Holons
            |
            +-- Property Visualizer Holons
            |     |
            |     +-- Value Visualizer Holons
            |
            +-- navigation affordances
            |
            +-- Collection Visualizer Holons
                  |
                  +-- Property / Value Visualizers

Every selected Visualizer Holon is realized by an executable implementation that
composes its immediate children. A child request is semantically a request to
select an appropriate child Visualizer Holon; the client then realizes a
compatible implementation. This does not require each child request to be a
synchronous Selector round trip: batching, local cached resolution, and other
performance strategies remain implementation decisions.

The root Canvas MUST NOT control all nested presentation directly.

---

# 27. Parent-Owned Placement

The parent visualizer owns placement and layout allocation of its immediate children.

The child visualizer owns its own internal composition.

Therefore:

> **A visualizer owns its internal composition.**

> **Its parent owns its external placement.**

Examples:

- a Canvas Visualizer places Node Visualizer occurrences;
- a Node Visualizer places its immediate component visualizers;
- a Property Viewer places Property Visualizers;
- a Property Visualizer places its Value Visualizer;
- a Collection Visualizer places its member representations.

A child SHOULD NOT independently position itself in global Canvas coordinates.

---

# 28. Layout Budgets

A parent SHOULD provide each child with a layout budget.

A conceptual LayoutBudget may include:

    width
    height
    minimum_width
    minimum_height
    maximum_width
    maximum_height
    orientation
    density
    overflow_constraints

The child then decides how to compose its own content within that allocation.

This boundary is especially important because the parent may not know which concrete visualizer the DAHN Selector will choose.

---

# 29. Visualizer Layout Capabilities

A Visualizer Holon MAY expose or relate to semantic capabilities or preferences
such as:

- minimum useful width;
- minimum useful height;
- preferred dimensions;
- preferred aspect ratio;
- supported density range;
- support for compact presentation;
- support for compression;
- support for scrolling;
- alternate action presentation.

A parent MAY use these capabilities when allocating space.

The first implementation may use simpler contracts for generic Visualizer
Holons.

The architecture SHOULD leave room for richer layout negotiation later.

---

# 30. Selection Versus Layout

Visualizer selection and layout MUST remain distinct concerns.

The DAHN Selector answers:

> Which visualizer should represent this semantic subject?

The parent composition answers:

> Where should it be placed, and what layout budget should it receive?

The child answers:

> Given that budget, how should I compose myself internally?

A visualizer's geometry capabilities may inform allocation, but selection SHOULD NOT collapse into Canvas placement logic.

---

# 31. Responsive Composition

Responsive behavior SHOULD be hierarchical.

Conceptually:

1. the Canvas receives the viewport;
2. the Canvas allocates regions to immediate child visualizers;
3. each child allocates its region to its own children;
4. the process continues recursively.

A Canvas SHOULD NOT micromanage the geometry of deeply nested visualizers.

This allows independently contributed visualizers to participate in responsive composition while preserving local autonomy.

---

# 32. Theme Architecture

Themes are external to visualizer semantic logic.

Visualizers MUST avoid hard-coding stylistic decisions that properly belong to a theme.

Theme-controlled concerns may include:

- color;
- typography;
- spacing;
- border appearance;
- corner treatment;
- elevation;
- icons;
- hover state;
- focus state;
- selection state;
- error state;
- density;
- control sizing.

Visualizers SHOULD consume semantic theme tokens rather than literal stylistic constants.

Examples:

    surface.background
    surface.border
    text.primary
    text.secondary
    action.primary
    state.selected
    state.error
    spacing.small
    spacing.medium

---

# 33. Theme Versus Semantic Layout

Themes MAY influence:

- typography metrics;
- spacing;
- density;
- icon size;
- control dimensions.

Themes SHOULD NOT redefine the semantic interaction model of a Canvas.

For example, a theme may change how a navigation affordance looks.

It SHOULD NOT redefine whether an affordance represents singular or plural traversal.

Semantic layout belongs to Canvas and visualizer behavior.

Stylistic realization belongs to themes.

---

# 34. Action Architecture

Actions visible in DAHN do not all originate from the same semantic source.

The architecture SHOULD distinguish actions by scope and ownership.

Potential scopes include:

- value;
- property;
- collection;
- holon;
- visualizer;
- Canvas;
- transaction.

A useful invariant is:

> **An action belongs at the lowest common scope that semantically owns its effect.**

---

# 35. Action Sources

Action surfaces may compose operations originating from multiple sources.

## 35.1 Holon-Semantic Actions

Examples:

- dances;
- Edit;
- Clone;
- Delete;
- Create Instance where applicable.

These operate on a particular semantic holon or type.

## 35.2 Collection Actions

Examples:

- sort;
- filter;
- collection mutation;
- collection-specific commands.

## 35.3 Visualizer Actions

Examples:

- select alternate visualizer;
- collapse;
- expand;
- change visualizer-specific presentation.

## 35.4 Canvas and Transaction Actions

Examples:

- Undo;
- Redo;
- Commit;
- abandon/revert transaction;
- Canvas-level layout or navigation controls.

The Space Navigator's specific placement of these actions is defined by the Design Specification.

---

# 36. Action Visualizers

A semantic action and its visual representation are separate.

A given action might be rendered as:

- button;
- icon;
- toolbar item;
- menu item;
- overflow-menu entry;
- contextual control.

Action Visualizers allow the same semantic operation to adapt to layout and interaction context.

Action representation MAY itself be selected dynamically.

---

# 37. Canvas-Level Interaction Surface

A Canvas Visualizer owns its Canvas-level interaction surface.

The Space Navigator, for example, defines a pinned Canvas Action Bar.

Another Canvas Visualizer MAY define a different action surface.

DAHN SHOULD therefore not impose one universal top-level action bar on every Canvas.

Canvas-specific presentation belongs to the Canvas Design Specification.

The architectural contract is that a Canvas may expose actions whose scope is the Canvas session or active transaction.

---

# 38. Action Personalization

Where a Canvas or visualizer allows it, actions may be reordered or represented differently.

Such interaction may serve both immediate customization and adaptive learning.

Examples include:

- changing action order;
- promoting an action out of overflow;
- selecting a different Action Visualizer.

The same gesture-handling boundary applies:

- TypeScript updates immediate presentation;
- Rust receives durable adaptive signals.

---

# 39. Visualizer Occurrence

The architecture MUST distinguish:

1. **subject Holon**;
2. **Visualizer Holon**;
3. **Visualizer Implementation**; and
4. **Visualizer Occurrence**.

A subject Holon is the semantic entity being represented.

A Visualizer Holon is the semantic visualizer selected to represent it.

A Visualizer Implementation is reusable executable code capable of realizing a
Visualizer Holon in a particular runtime environment.

A Visualizer Occurrence is one particular placement and use of a selected
Visualizer Holon for a subject in an active Canvas experience.

A conceptual occurrence may include:

    occurrence_id
    semantic_subject_reference
    selected_visualizer_reference
    resolved_implementation_reference
    parent_occurrence
    source_affordance
    traversal_context
    layout_allocation
    interaction_mode
    local_view_state

The same subject Holon may legitimately appear in multiple Visualizer
Occurrences. Different occurrences of the same subject MAY use different
Visualizer Holons when the person chooses an applicable alternative.

Visualizer occurrence state belongs to TypeScript experience state.

---

# 40. Holon Identity Versus Occurrence Identity

Holon identity MUST NOT be used as the unique identity of a Canvas visualizer occurrence.

The same holon may appear:

- through different relationships;
- through different collections;
- through different traversal paths;
- in multiple visualizers;
- in multiple places in the same Canvas.

The semantic subject may be the same while:

- provenance;
- focus;
- selected tabs;
- layout;
- compression;
- visualizer choice;

differ between occurrences.

---

# 41. DAHN Interaction Events

Child visualizers SHOULD communicate semantic interaction events rather than directly manipulate unrelated Canvas components.

For example:

    Collection Visualizer
      emits:
        inspectHolon(H42)

A parent Canvas may then interpret that event according to its own navigation semantics.

Similarly:

    alternate visualizer control
      emits:
        chooseVisualizer(V7)

The appropriate DAHN layer then processes the semantic request.

This keeps child visualizers reusable across different Canvas types.

---

# 42. DAHN Events Versus MAP Commands

DAHN interaction events and MAP commands are separate abstractions.

For example:

    user activates a collection row
          |
    DAHN event:
      inspect semantic subject
          |
    Canvas updates experience state
          |
    semantic data is requested if needed
          |
    MAP SDK
          |
    Rust MAP command

Not every DAHN interaction requires IPC.

Examples of TypeScript-only state changes may include:

- focus;
- local selection;
- expanding already loaded presentation;
- Canvas compression;
- scrolling;
- hover;
- temporary drag state.

Semantic data mutation and persistent adaptive state SHOULD cross the appropriate MAP boundary.

---

# 43. Progressive Semantic Retrieval

DAHN SHOULD prefer progressive retrieval over eager graph materialization.

A visualizer may initially need only:

- a semantic reference;
- identifying projection;
- effective descriptor;
- adaptive presentation context.

Additional data can then be requested as required by interaction.

This supports:

- smaller IPC payloads;
- Rust-side caching;
- lazy collection retrieval;
- deferred relationship expansion;
- deferred dance invocation.

The exact Space Navigator retrieval sequence is defined in the Design Specification.

---

# 44. Effective Descriptor Boundary

Rust SHOULD provide sufficiently resolved semantic information that TypeScript does not repeatedly reconstruct MAP inheritance or authorization semantics.

Where practical, the effective descriptor or equivalent presentation context should resolve:

- inherited properties;
- inherited relationships;
- inherited dances;
- effective cardinalities;
- effective constraints;
- authorization-sensitive affordances.

This yields:

> **MAP determines what is semantically available.**

> **DAHN determines how the selected experience presents it.**

---

# 45. Property and Value Visualizers

Property and Value Visualizers are architectural extension points.

A Property Visualizer is responsible for presentation of a property in context.

A Value Visualizer is responsible for presentation and interaction appropriate to a value type.

The architecture SHOULD support both read and edit behavior through the same visualizer hierarchy.

Conceptually:

    Property Descriptor
          |
    selected Property Visualizer
          |
    Value Type Descriptor
          |
    selected Value Visualizer

A Value Visualizer may provide:

- read presentation;
- edit interaction;
- validation feedback;
- compact representation;
- specialized interaction behavior.

A Node Visualizer SHOULD NOT need hard-coded knowledge of every value type.

---

# 46. Collection Visualizers

A Collection Visualizer represents a semantic collection.

The collection's source may include:

- array-valued property;
- multi-valued relationship;
- dance result;
- another collection-producing semantic operation.

The Collection Visualizer abstraction SHOULD be based on collection semantics rather than provenance-specific UI models.

Potential implementations include:

- table;
- cards;
- timeline;
- graph;
- map;
- gallery;
- domain-specific visualizations.

The initial fallback implementation is expected to be table-based.

Space Navigator-specific collection geometry and navigation behavior belong in the Design Specification.

---

# 47. Read and Edit Architecture

Read and edit are interaction modes of the same visualizer structure.

Entering edit mode SHOULD NOT require a separate form architecture.

Conceptually:

    persisted holon
          |
        Edit
          |
    Rust creates / exposes staged state
          |
    existing visualizer structure
      presents edit interactions

TypeScript coordinates the interaction mode.

Rust owns the staged semantic state.

---

# 48. Staged State Ownership

Staged MAP data remains authoritative on the Rust side.

TypeScript MAY retain:

- staged holon references;
- indication that an occurrence is presenting staged state;
- local editor-control state;
- validation display state.

Property and relationship mutations SHOULD ultimately update Rust-owned staged state.

TypeScript MUST NOT become the authoritative store of staged holon semantics.

---

# 49. Semantic Editing Ownership

Visual containment does not imply semantic ownership.

If holon B appears inside a collection belonging to holon A:

- modifying whether B belongs in A's relationship modifies A's staged relationship state;
- modifying B's own properties modifies B.

The architecture MUST preserve this ownership distinction regardless of Canvas presentation.

The Space Navigator Design Specification defines how this distinction appears to the person.

---

# 50. Multi-Holon Transaction Scope

A MAP transaction MAY contain staged changes involving multiple holons.

A single transaction may therefore include:

- updated holon A;
- newly created holon B;
- cloned holon C;
- relationship changes involving D;
- staged deletion of E.

Conceptually:

    active transaction
      |
      +-- staged A
      +-- staged B
      +-- staged C
      +-- staged relationship changes
      +-- staged deletion

Commit applies to the transaction, not inherently to one visualizer occurrence or one holon.

This is a critical architectural distinction.

---

# 51. Commit Ownership

Commit is a transaction-scoped MAP operation.

Rust owns:

- transaction validation;
- commit semantics;
- persistence;
- resulting committed state.

TypeScript owns:

- exposing the applicable transaction action through the active Canvas;
- presenting transaction state;
- refreshing affected visualizers after the operation.

The Space Navigator Design Specification defines Commit's user-facing placement and behavior.

---

# 52. Commit Flow

Conceptually:

    user requests Commit
          |
    Canvas interaction
          |
    TypeScript MAP SDK
          |
    IPC
          |
    Rust validates transaction
          |
    Rust commits transaction
          |
       success / failure
          |
    TypeScript refreshes affected presentation

On success:

- staged transaction state becomes committed according to MAP semantics;
- affected presentation is refreshed.

On failure:

- staged state remains available;
- validation or commit errors are returned for presentation.

Commit MUST NOT depend on one particular Node Visualizer owning the transaction.

---

# 53. Create, Edit, and Clone

Create, Edit, and Clone differ in how staged state is initialized.

## Edit

    persisted holon
          |
    stage new version

## Clone

    persisted holon
          |
    create staged new holon initialized from source

## Create

    concrete type
          |
    create staged new holon

After staging, all participate in the same transaction model.

The interaction details belong to the Space Navigator Design Specification.

---

# 54. Delete

Delete is a semantic operation on a holon whose effects participate in transaction state.

Rust owns:

- deletion semantics;
- staging;
- validation;
- transaction participation;
- historical persistence behavior.

TypeScript owns the presentation and interaction through which deletion is requested.

Deletion MAY participate in the same transaction as other creates or updates.

---

# 55. Transaction Snapshots

The Rust MAP layer maintains transaction snapshots for work in flight.

These snapshots support:

- recovery;
- Undo;
- Redo.

Snapshot storage and restoration belong to Rust because the semantic transaction state lives there.

TypeScript SHOULD NOT maintain an independent semantic command history attempting to reconstruct MAP state.

---

# 56. UX Undo Boundaries

TypeScript is responsible for determining when a meaningful user interaction constitutes an Undo boundary.

Examples might include:

- completion of a property edit;
- completion of a relationship mutation;
- completion of an array mutation;
- completion of a semantically meaningful editing gesture.

TypeScript instructs Rust when such a boundary has been reached.

This yields:

> **DAHN defines the semantic boundaries of an interaction.**

> **MAP owns recoverable transaction state at those boundaries.**

---

# 57. Undo

Conceptually:

    meaningful interaction completes
              |
    TypeScript establishes Undo boundary
              |
    Rust records transaction snapshot

Later:

    user requests Undo
          |
    TypeScript
          |
    Rust restores prior transaction snapshot
          |
    TypeScript refreshes affected projections

Undo changes transaction state, not merely DOM or component state.

---

# 58. Redo

Redo follows the same ownership model.

Rust owns roll-forward through recoverable transaction snapshots.

TypeScript requests the operation and refreshes presentation afterward.

---

# 59. Transaction Status

Rust SHOULD expose sufficient transaction status for the active Canvas to present appropriate transaction controls.

Possible information includes:

- transaction active;
- staged changes present;
- can Undo;
- can Redo;
- validation status;
- Commit availability;
- current snapshot marker where required.

The exact wire contract remains to be defined.

---

# 60. Continuous Snapshotting Versus Undo Semantics

Continuous or frequent snapshotting used for work preservation is conceptually distinct from user-visible Undo boundaries.

Not every low-level recovery snapshot needs to become an Undo step.

The architecture SHOULD distinguish:

- preservation snapshots;
- meaningful interaction boundaries.

The user-facing design belongs to the Space Navigator Design Specification.

---

# 61. Adaptive Gestures and Transaction Gestures Are Distinct

Some gestures may affect experience adaptation without changing MAP domain state.

For example:

- reordering properties;
- selecting an alternate visualizer;
- changing action prominence.

Other gestures mutate staged semantic state.

For example:

- changing a property value;
- adding a relationship;
- removing an array element.

A gesture may therefore result in:

- local TypeScript experience-state update;
- persistent adaptive signal;
- staged MAP mutation;
- Undo-boundary creation;

depending on its semantics.

These concerns SHOULD remain independently represented even when triggered by one user interaction.

---

# 62. DAHN MAP Adapter

A thin TypeScript adapter MAY sit above the lower-level MAP SDK to expose DAHN-oriented semantic operations.

Conceptual operations may include:

    inspectHolon(reference)
    getEffectiveDescriptor(reference)
    getPresentationContext(reference)

    expandRelationship(reference, relationship)
    invokeDance(reference, dance, arguments)

    selectVisualizer(category, subject, context)
    recordAdaptiveGesture(event)

    stageEdit(reference)
    stageCreate(typeReference)
    stageClone(reference)
    stageDelete(reference)

    updateStagedProperty(reference, property, value)
    updateRelationship(reference, relationship, mutation)

    markUndoBoundary(context)
    undo()
    redo()

    getTransactionStatus()
    commitTransaction()

This adapter SHOULD:

- normalize asynchronous interaction;
- centralize command translation;
- centralize error normalization;
- make visualizers easier to test.

It MUST remain thin.

It MUST NOT evolve into a second MAP runtime.

---

# 63. Asynchrony

Many DAHN semantic operations may cross IPC and may ultimately interact with distributed state.

These operations SHOULD be treated as asynchronous.

Visualizers may therefore need local states such as:

- unresolved;
- loading;
- ready;
- empty;
- error.

Failure SHOULD be localized to the smallest meaningful presentation boundary.

For example:

- one collection may fail to load while the containing Node Visualizer remains usable;
- one visualizer acquisition may fail while a generic fallback remains available.

---

# 64. Error Boundaries

Errors SHOULD be surfaced near the operation or semantic object that failed.

Examples:

- value-specific error → Property or Value Visualizer;
- collection retrieval error → Collection Visualizer;
- dance failure → action/result region;
- visualizer acquisition failure → runtime-resolution boundary;
- transaction validation error → relevant visualizers plus transaction-level summary;
- Canvas-level failure → Canvas boundary.

Architecture SHOULD make it possible to recover through generic fallbacks where practical.

---

# 65. Presentation Refresh After Semantic Change

Because semantic truth resides in Rust, TypeScript SHOULD refresh affected projections or presentation context after operations that change semantic state.

Examples include:

- staged mutation;
- Undo;
- Redo;
- Commit;
- Delete;
- dance that mutates state.

The exact refresh strategy may vary.

The architectural rule is that TypeScript should not assume its pre-operation projection remains authoritative after Rust semantic state changes.

---

# 66. Multiple Occurrences of the Same Holon

Because visualizer occurrence identity is independent of holon identity, the same holon may be displayed in multiple places.

If the holon participates in staged state, all occurrences need a coherent relationship to that staged semantic state.

The exact UX synchronization policy belongs in the Design Specification.

The architectural invariant is:

> There is one authoritative semantic staged state in Rust, even if multiple TypeScript visualizer occurrences represent that subject.

TypeScript MUST avoid creating independent semantic edit copies per occurrence.

---

# 67. Space Navigator as an Architectural Proof

The Space Navigator should prove the DAHN architecture through a constrained initial implementation.

The first implementation does not need the complete future ecosystem.

It should, however, preserve the intended boundaries around:

- Rust-side visualizer selection;
- Visualizer Holon and implementation-reference runtime resolution;
- generic fallback visualizers;
- descriptor-driven composition;
- hierarchical layout;
- theme tokens;
- TypeScript occurrence state;
- Rust-owned staged state;
- transaction snapshots;
- Canvas-scoped transaction controls;
- adaptive gesture reporting.

The implementation MAY initially use only locally bundled core visualizers while keeping the interfaces compatible with future Visualizer Commons discovery.

---

# 68. Initial Architectural Modules

A possible TypeScript decomposition might include:

    dahn/
      canvas/
      visualizer-runtime/
      visualizers/
        node/
        collection/
        property/
        value/
        action/
      layout/
      theme/
      state/
      map-adapter/

A possible Rust conceptual decomposition might include:

    dahn/
      discovery/
      selector/
      adaptation/
      presentation-context/

Existing MAP transaction, cache, command, and holon infrastructure SHOULD be reused rather than duplicated into a DAHN-specific runtime.

The exact repository structure is not normative.

The responsibility boundaries are.

---

# 69. Architectural Testing Boundaries

The architecture SHOULD support testing at multiple levels.

## 69.1 Rust / MAP Tests

Test:

- descriptor resolution;
- visualizer discovery;
- visualizer applicability;
- Selector behavior;
- adaptive signal processing;
- transaction staging;
- transaction snapshots;
- Undo;
- Redo;
- validation;
- Commit;
- relationship expansion;
- dance/query execution.

## 69.2 DAHN Adapter Tests

Test:

- SDK translation;
- async behavior;
- error normalization;
- visualizer selection requests;
- adaptation-event reporting;
- transaction control.

## 69.3 Visualizer Runtime Tests

Test:

- Visualizer Holon / implementation-reference resolution;
- generic fallback;
- failure to resolve selected implementation;
- version compatibility where implemented.

## 69.4 Visualizer Tests

Given:

- semantic input;
- descriptor context;
- layout budget;
- theme;
- interaction mode;

verify:

- rendering;
- child composition;
- semantic events emitted.

## 69.5 Canvas Tests

Verify:

- visualizer occurrence management;
- layout allocation;
- navigation state;
- transaction-action state;
- composition of child visualizers.

## 69.6 Adaptive Interaction Tests

Verify:

- immediate TypeScript reordering;
- semantic adaptive event emission;
- persistent preference influence;
- alternate visualizer selection signals.

---

# 70. Architecture That Should Not Be Over-Generalized Initially

The initial Space Navigator implementation SHOULD NOT require full implementation of:

- remote visualizer package loading;
- arbitrary third-party code execution;
- production-grade sandboxing;
- sophisticated adaptive scoring;
- every salience rubric;
- every maturity model;
- decentralized package dependency resolution;
- advanced recommendation explanation;
- theme marketplaces;
- generalized layout constraint solving;
- complete cross-device adaptation;
- every visualizer category;
- every possible dance result shape.

The architecture should leave room for these capabilities without requiring them before the Space Navigator can be useful.

---

# 71. Core Architectural Invariants

## 71.1 Rust Owns Semantic Truth

Holon state, descriptors, relationships, staging, transactions, caches, validation, persistence, and adaptive history remain MAP/Rust responsibilities.

## 71.2 TypeScript Owns Experience Realization

Rendering, layout, Canvas state, focus, selection, navigation presentation, and immediate interaction remain TypeScript responsibilities.

## 71.3 Rust Owns the DAHN Selector

Visualizer discovery, applicability evaluation, personalization-informed selection, and collective adaptive selection belong on the Rust side.

## 71.4 Visualizer Discovery Is Federated

Candidate visualizers are discovered through accessible Visualizer Commons rather than through a centrally controlled application registry.

## 71.5 Visualizers Are Holons

Every DAHN Visualizer has first-class MAP semantic identity. A concrete
Visualizer Holon Type describes its compositional contract; the Visualizer
Holon, rather than a component class or registry ID, is the selector's semantic
object.

## 71.6 Visualizer Selection and Execution Are Separate

Rust chooses a Visualizer Holon.

The client runtime resolves and executes a compatible implementation.

## 71.7 Generic Fallbacks Preserve Usability

Unknown semantic types and unavailable specialized visualizers SHOULD remain usable through generic visualizers wherever practical.

## 71.8 Parent Owns Child Placement

A parent determines where and how much space a child receives.

A child determines how to compose within that space.

## 71.9 Layout Is Hierarchical

Responsive behavior emerges through recursive layout allocation.

## 71.10 Themes Are External

Visualizer implementations consume semantic theme values rather than hard-coded style constants.

## 71.11 Read and Edit Share the Same Visual Structure

Editing changes semantic staged state and interaction mode rather than requiring separate form architecture.

## 71.12 Staged State Remains in Rust

TypeScript may represent staged state but does not become its authoritative semantic owner.

## 71.13 Transactions May Span Multiple Holons

Commit is transaction-scoped rather than Node-Visualizer-scoped.

## 71.14 Undo and Redo Are Transaction-Scoped

Rust owns snapshots and restoration.

TypeScript defines meaningful interaction boundaries.

## 71.15 Subject, Visualizer, and Occurrence Are Distinct

The subject being represented, the selected Visualizer Holon, and its Canvas
occurrence are distinct identities. The same subject may appear in multiple
visual contexts without acquiring multiple semantic identities.

## 71.16 Adaptive Preferences Refer to Visualizer Holons

Personal and collective preference, salience, and usage measures that describe
the visualizer normally reference the stable Visualizer Holon. Operational
metrics specific to an executable realization MAY instead reference its
Visualizer Implementation.

## 71.17 User Gestures May Become Adaptive Signals

TypeScript handles immediate interaction.

Rust owns durable learned interpretation.

## 71.18 Action Scope Determines Ownership

Actions are associated with the lowest common semantic or experience scope that owns their effect.

## 71.19 Architecture Defines Contracts, Not Space Navigator UX

Space Navigator-specific geometry, navigation, editing interaction, and presentation belong in the Design Specification.

---

# 72. Architectural Summary

The DAHN architecture exercised by the Space Navigator consists of four cooperating domains.

## 72.1 MAP Semantic and Adaptive Layer — Rust

Owns:

- holons;
- descriptors;
- relationships;
- dances;
- queries;
- caches;
- staged state;
- transactions;
- snapshots;
- Undo/Redo;
- validation;
- Commit;
- Visualizer Commons discovery;
- Visualizer Holons and their semantic relationships;
- personalization;
- aggregate salience;
- adaptive visualizer selection.

## 72.2 DAHN Experience Layer — TypeScript

Owns:

- executable visualizers;
- runtime visualizer resolution;
- Canvas composition;
- layout;
- responsive presentation;
- visualizer occurrence state;
- focus;
- navigation presentation;
- immediate interaction;
- theme realization;
- adaptive gesture emission;
- meaningful Undo-boundary detection.

## 72.3 Visualizer Ecosystem — Federated MAP Agent Spaces

Visualizer Commons provide an open, governed source of:

- contributed visualizers;
- Visualizer Holons and their related implementation resources;
- stewardship;
- maturity information;
- community curation;
- semantic specialization.

## 72.4 Canvas Visualizers

Canvas Visualizers use these architectural capabilities to define concrete interaction environments.

The Space Navigator is the first such Canvas.

Its specific navigation grammar, geometry, Canvas Action Bar, editing behavior, compression behavior, and interaction scenarios are defined in `space-navigator-design-spec.md`.

Conceptually:

    Visualizer Commons
          |
          | federated MAP relationships
          v
    Rust / MAP
      discovers candidates
      evaluates semantic applicability
      applies adaptive state
      selects Visualizer Holons
      owns semantic and transaction truth
          |
          | semantic APIs
          | descriptors
          | projections
          | Visualizer Holon references
          | compatible implementation information
          | transaction status
          v
    TypeScript / DAHN
      resolves executable implementations
      recursively composes experience
      allocates layout
      renders
      handles immediate interaction
      reports adaptive signals
          |
          v
    Canvas-specific experience
          |
          v
    Human

The central architectural rules are:

> **MAP determines semantic truth.**

> **The federated Visualizer Commons determine the available experience ecosystem.**

> **The Rust DAHN Selector determines which applicable visualizer should be used.**

> **TypeScript resolves, composes, and renders the selected experience.**

> **The parent allocates space; the child composes within that allocation.**

> **Themes determine stylistic expression without redefining semantic behavior.**

> **User gestures can shape both personal and collective future experience.**

> **Rust preserves semantic, staged, transaction, and adaptive state.**

> **TypeScript preserves spatial, occurrence, and immediate interaction state.**

> **The Space Navigator proves these architectural contracts without defining the limits of DAHN.**
