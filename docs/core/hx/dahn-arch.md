# DAHN Architecture Specification v0.6

## Status

Draft architecture specification. This is the canonical successor to the former
Space Navigator architecture document. It defines reusable subsystem authority,
not the internal experiential grammar of any Dancer or Visualizer.

## Change Log

### v0.6

Delegates adaptive concepts and reporting contracts to the DAHN design
specification; preserves Rust interpretation, local presentation response,
and governed personal/collective state authority.

### v0.5

Moves shared architecture to DAHN; separates semantic identity, executable
realization, and usage; delegates selection and composition mechanisms to the
DAHN design specification and kind-specific promises to the Visualizer families.

### v0.4

Established Visualizers as first-class MAP Holons, distinct from executable
implementations and non-semantic runtime registry identifiers.

## Purpose

DAHN architecture assigns responsibility across MAP/Rust, the TypeScript runtime,
composition owners, and federated Visualizer Commons. The
[DAHN Design Specification](dahn-design-spec.md) owns shared composition,
selection, allocation, materialization, and runtime contracts. Architecture
summaries delegate those mechanisms rather than defining a second rule set.

# 1. Relationship to the Specification Family

- [DAHN design](dahn-design-spec.md) defines the grammar of composition.
- [Visualizer kinds](visualizers/index.md) classify semantic subject shape;
  owner-defined slots add local participation requirements and subject bindings.
- [Space Navigator](../space-navigator/space-navigator-design-spec.md) owns its
  Dancer roles and local HolonSpace coupling.
- [Path Inspector grammar](visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md) owns
  that Visualizer's topology and spatial productions.
- Other concrete Visualizer specs own their internal realization.
- [Delivery planning](../space-navigator/space-navigator-impl-plan.md) sequences
  implementation without changing these authorities.

The MAP Application Launcher owns startup and home-Dancer selection. Canvas
hosts the resulting experience; neither Launcher nor Canvas requires Space
Navigator as its permanent implementation choice.

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
- Canvas and Dancer context;
- user preferences;
- layout constraints.

A previously unknown holon type SHOULD remain usable through generic visualizers even if DAHN has never encountered that type before.

## 2.2 Adaptive

DAHN adapts to evolving subjects, Visualizers, environmental circumstances, and
accumulated experience. The [adaptive human-experience contract](dahn-design-spec.md#48-adaptive-human-experience)
defines the dimensions, salience and affinity, agent control, and contextual
policy inheritance. Adaptation is a target architectural capability; the
presence of an input below does not imply an implemented learning service.

Adaptive state also draws on accumulated use.

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
    |      +-- Canvas-hosted Dancer experience realizations |
    |      +-- Node Visualizers                             |
    |      +-- Collection Visualizers                       |
    |      +-- PropertyMap Visualizers                         |
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

TypeScript MUST NOT select a semantic Visualizer Holon, choose between that
Visualizer's implementations, or substitute a generic fallback when the
supplied implementation is unavailable. Those are Rust Selector
responsibilities.

Space Navigator supplies visualization context and realizes the Selector's
result. It does not select a Theme or MetaDesignSystem, and it does not bind an
application to a Visualizer. The selected Theme establishes the effective MDS;
the DAHN Selector uses the MDS-guaranteed DesignToken subset to choose a
Visualizer whose declared token dependencies are satisfied at runtime.

These responsibilities include:

- executable Visualizer Implementations;
- Dancer top-level, Node, Collection, Property, Value, and Action implementation modules;
- visualizer runtime resolution;
- visualizer occurrence state;
- Space Navigator navigation provenance;
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

Rust also owns selected Visualizer semantic identity, executable implementation
resolution and authorization, and artifact verification. These decisions do not
move to TypeScript merely because it holds a reference or cached projection.

## 7.2 Experience State

TypeScript experience state includes:

- visualizer occurrence identity;
- Dancer-experience placement within the Canvas;
- traversal path;
- selected affordances;
- selected rows;
- focus;
- compression presentation;
- viewport state;
- scroll state;
- temporary interaction state;
- selected tabs and local expansion;
- transient hover state;
- component-local layout and client DOM state;
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
- selected Visualizer Holon reference and selected implementation information;
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
      +-- NodeVisualizer
      +-- CollectionVisualizer
      +-- PropertyMapVisualizer
      +-- ValueVisualizer
      +-- ActionVisualizer
      +-- StructureVisualizer
            |
            +-- GraphVisualizer
            +-- RootedNavigationVisualizer
            +-- GeospatialVisualizer

These types classify semantic capabilities. Each owner-defined slot adds its
required contract, subject binding, and participation constraints; kind membership
alone does not guarantee applicability to that slot. Individual Visualizer Holons are
instances of those concrete types. For example:

    Generic Holon Node Visualizer       instance of NodeVisualizer
    Table Collection Visualizer         instance of CollectionVisualizer
    Rooted Navigation Visualizer        instance of RootedNavigationVisualizer

A specialized Event Node Visualizer is likewise a Visualizer Holon, rather
than a hard-coded DAHN category.

## 9.2 Semantic Identity and Executable Realization

DAHN distinguishes:

1. the **Visualizer Holon**, whose MAP identity is the durable semantic target;
2. a **Visualizer Implementation**, which is an executable realization for a
   particular runtime or platform; and
3. a **Visualizer Occurrence**, which is a runtime presentation occurrence for
   a bound subject within a composition; and
4. **VisualizerUsage**, the agent-relative use/configuration relationship defined
   by [DAHN design](dahn-design-spec.md#111-visualizerusage), distinct from the
   occurrence, shared Visualizer, and slot contract.

Conceptually:

    Generic Holon Node Visualizer
      |
      +-- implemented_by --> TypeScript Visualizer Implementation
      |
      +-- implemented_by --> Rust Visualizer Implementation

A Visualizer may outlive, replace, or gain implementations without losing its
semantic identity or the adaptive state that refers to it.

For a given realization request, Rust supplies the selected Visualizer Holon
and one implementation identity selected for the target runtime. TypeScript
maps that supplied implementation to executable local code. If it cannot do
so, it reports a realization failure; it does not traverse `ImplementedBy` or
make another semantic or implementation-selection decision.

---

# 10. Generic Versus Specialized Visualizers

DAHN should make broadly applicable Visualizers available as ordinary candidates.
Selection follows the [shared policy](dahn-design-spec.md#1421-slot-directed-descriptor-selection);
no candidate may bypass conformance and absence remains an explicit error.

Examples include:

- a Generic Holon Node Visualizer capable of displaying an arbitrary holon using core affordances;
- a Table Collection Visualizer capable of displaying a homogeneous collection;
- generic PropertyMap and Value Visualizers;
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

Rust evaluates specialized and generic candidates through the shared selection
policy. An implementation availability failure is reported explicitly; any
reselection remains a Rust decision under that same policy.

A composition owner MUST NOT treat a particular generic implementation as
synonymous with a Visualizer type or a generic Visualizer Holon.

## 10.1 Static Core Visualizers

Static implementation is an acquisition optimization, not a different semantic
model. Bundled candidates—including the Generic Holon Node Visualizer, Table
Collection Visualizer, and generic PropertyMap, Value, Action,
and Rooted Navigation Visualizers—MUST each have a corresponding Visualizer
Holon even where their initial executable implementations are compiled into the
TypeScript or Rust client. A Dancer such as Space Navigator remains a Dancer
Holon, not a Visualizer Holon.

Space Navigator is a Dancer, not a Visualizer Holon. It composes the roles that
make a `HolonSpace` experience coherent: the space Holon itself, Dancers
afforded by it, and navigation rooted at it. Its navigation role may select a
generic `RootedNavigationVisualizer`, a Structure Visualizer rooted at the
`HolonSpace`. Holons `OwnedBy` that `HolonSpace` form an initial heterogeneous
ownership structure; the interaction-derived navigation topology may extend
beyond those directly owned Holons as relationships are traversed. Its pinned
Space Navigator Action Bar remains a
Dancer concern; the concrete rooted-navigation grammar belongs to the
Path Inspector grammar; selected Visualizers retain their own semantic identities
and executable realizations. Neither Space Navigator nor Rooted Navigation is
the Canvas.

A future `AgentSpace` may extend `HolonSpace` with agent, social, governance,
membership, LifeCode, We-space, or related affordances. Such affordances may
add Space Navigator roles; they are not prerequisites of its current design.

---

# 11. Visualizer Commons

Visualizers are drawn from a federated network of **Visualizer Commons**.

A Visualizer Commons is a stewarded, governed MAP Agent Space containing and
stewarding Visualizer Holons and their related semantic resources, including
independently contributed MetaDesignSystems and Themes. A Human Agent selects
an offered Theme; its MDS guarantees the DesignToken set against which the
DAHN Selector evaluates Visualizer dependencies.

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

# 15. DAHN Visualizer Selection Service

The [DAHN design contract](dahn-design-spec.md#14-dahn-visualizer-selection-service) is authoritative for
this mechanism. Composition, selection, and execution responsibilities remain
separate across the Rust, runtime, and local composition-owner boundaries.

---

# 16. Selector Inputs

The [DAHN design contract](dahn-design-spec.md#12-visualization-requests) is authoritative for
this mechanism. Composition, selection, and execution responsibilities remain
separate across the Rust, runtime, and local composition-owner boundaries.

---

# 17. Explore Versus Exploit

The [adaptive human-experience contract](dahn-design-spec.md#48-adaptive-human-experience)
defines agent-controlled stability and discovery, policy dimensions, and
inheritance. Rust resolves selection policy; Canvas, Dancers, and Visualizers
supply the applicable explicit request context without becoming selectors.

## 17.1 Exploit-Oriented Selection

Predictable reuse favors familiar eligible choices and established configuration.
Explicit protected choices retain their declared scope.

## 17.2 Explore-Oriented Selection

Discovery may consider novel eligible alternatives and governed collective
signals. It cannot waive eligibility or silently displace protected choices.

---

# 18. Adaptive Salience

[Salience and affinity](dahn-design-spec.md#salience-and-affinity) express
contextual importance and association/preference. Concrete Visualizer specs own
their gestures; Rust interprets learned meaning. Presentation signals do not
change descriptor structure, authorization, or semantic availability.

---

# 19. Personal and Collective Adaptation

## 19.1 Personal Adaptation

Rust services own persistent preference interpretation and usage matching;
TypeScript owns immediate presentation response and occurrence state.
[Personal and collective feedback](dahn-design-spec.md#personal-and-collective-feedback)
distinguishes explicit choices, inferred evidence, and persistence scope.

## 19.2 Collective Adaptation

Governed Rust services automatically accumulate and aggregate permitted
interaction evidence under established agent settings and Agent Space
participation policies. Aggregation can span community-specific or broader,
potentially MAP-wide populations through federated spaces. Personalization does
not require sharing, and collective signals remain advisory. Global reach does
not imply centralized storage of raw behavioral data. Consent, disclosure, and
retention follow the shared adaptive contract; the protocol remains open.

---

# 20. Gesture Handling Boundary

[Adaptive interaction reporting](dahn-design-spec.md#148-adaptive-interaction-reporting)
defines semantic events and the distinction between choice, authorization,
realization, persistence, and contribution. Reporting goes through the public
MAP SDK/IPC boundary. Visualizers report meaning; Rust interprets adaptive
signals without requiring preference persistence to block local UI response.

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

The [DAHN design contract](dahn-design-spec.md#142-selector-signatures) is authoritative for
this mechanism. Composition, selection, and execution responsibilities remain
separate across the Rust, runtime, and local composition-owner boundaries.

---

## 22.1 Visualizer Materialization

See [materialization](dahn-design-spec.md#401-materialization-and-client-caching).

---

# 23. Visualizer Acquisition and Execution

The [DAHN design contract](dahn-design-spec.md#40-visualizer-artifact-loading) is authoritative for
this mechanism. Composition, selection, and execution responsibilities remain
separate across the Rust, runtime, and local composition-owner boundaries.

---

# 24. Visualizer Runtime

The [DAHN design contract](dahn-design-spec.md#33-visualizer-runtime-contract) is authoritative for
this mechanism. Composition, selection, and execution responsibilities remain
separate across the Rust, runtime, and local composition-owner boundaries.

---

# 25. Trust and Compatibility

The [DAHN design contract](dahn-design-spec.md#34-visualizer-runtime-security-boundary) is authoritative for
this mechanism. Composition, selection, and execution responsibilities remain
separate across the Rust, runtime, and local composition-owner boundaries.

---

# 26. Recursive Visual Composition

The [DAHN design contract](dahn-design-spec.md#15-visualizer-composition) is authoritative for
this mechanism. Composition, selection, and execution responsibilities remain
separate across the Rust, runtime, and local composition-owner boundaries.

---

# 27. Parent-Owned Placement

The [DAHN design contract](dahn-design-spec.md#30-parent-owned-allocation) is authoritative for
this mechanism. Composition, selection, and execution responsibilities remain
separate across the Rust, runtime, and local composition-owner boundaries.

---

# 28. Layout Budgets

The [DAHN design contract](dahn-design-spec.md#301-layout-budgets-and-participation) is authoritative for
this mechanism. Composition, selection, and execution responsibilities remain
separate across the Rust, runtime, and local composition-owner boundaries.

---

# 29. Visualizer Layout Capabilities

The [DAHN design contract](dahn-design-spec.md#301-layout-budgets-and-participation) is authoritative for
this mechanism. Composition, selection, and execution responsibilities remain
separate across the Rust, runtime, and local composition-owner boundaries.

---

# 30. Selection Versus Layout

The [DAHN design contract](dahn-design-spec.md#30-parent-owned-allocation) is authoritative for
this mechanism. Composition, selection, and execution responsibilities remain
separate across the Rust, runtime, and local composition-owner boundaries.

---

# 31. Responsive Composition

The [DAHN design contract](dahn-design-spec.md#30-parent-owned-allocation) is authoritative for
this mechanism. Composition, selection, and execution responsibilities remain
separate across the Rust, runtime, and local composition-owner boundaries.

---

# 32. Theme Architecture

The [DAHN design contract](dahn-design-spec.md#45-design-tokens-meta-design-systems-and-theme-ownership) is authoritative for
this mechanism. Composition, selection, and execution responsibilities remain
separate across the Rust, runtime, and local composition-owner boundaries.

---

# 33. Theme Versus Semantic Layout

The [DAHN design contract](dahn-design-spec.md#45-design-tokens-meta-design-systems-and-theme-ownership) is authoritative for
this mechanism. Composition, selection, and execution responsibilities remain
separate across the Rust, runtime, and local composition-owner boundaries.

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

## 35.4 Canvas Actions and Dancer Transaction Actions

Canvas actions govern the desktop-like composition environment, for example:

- launch a Dancer in an existing window;
- launch a Dancer in a new window;
- tile, focus, switch, or close hosted Dancer windows;
- Canvas-level layout or navigation controls.

Dancer transaction actions govern the active Dancer experience, for example:

- Undo;
- Redo;
- Commit;
- abandon/revert transaction;

Undo and Redo MUST NOT be offered as Canvas actions. The Space Navigator's
specific placement of its Dancer transaction actions is defined by the Design
Specification.

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

# 37. Dancer and Canvas Interaction Surfaces

A Canvas owns interaction whose scope crosses hosted Dancers, including
desktop-like window launch and placement. A Dancer owns the interaction surface
for its experience, including its transaction actions, and realizes that surface
through its selected visualizer roles.

The Space Navigator, for example, defines a pinned Space Navigator Action Bar.
Another Dancer MAY define a different top-level action surface.

DAHN SHOULD therefore not impose one universal action bar on every Canvas or
every Dancer. Canvas-specific presentation belongs to the Canvas design;
Dancer-specific presentation belongs to the Dancer's design specification.

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
Visualizer Holon for a subject in an active Dancer experience.

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

Holon identity MUST NOT be used as the unique identity of a visualizer occurrence.

The same holon may appear:

- through different relationships;
- through different collections;
- through different traversal paths;
- in multiple visualizers;
- in multiple places in the same Dancer experience.

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

Child visualizers SHOULD communicate semantic interaction events rather than directly manipulate unrelated Dancer or Canvas components.

For example:

    Collection Visualizer
      emits:
        inspectHolon(H42)

A parent Visualizer may then interpret that event according to its Dancer's navigation semantics.

Similarly:

    alternate visualizer control
      emits:
        chooseVisualizer(V7)

The appropriate DAHN layer then processes the semantic request.

This keeps child visualizers reusable across different Dancer experiences.

---

# 42. DAHN Events Versus MAP Commands

DAHN interaction events and MAP commands are separate abstractions.

For example:

    user activates a collection row
          |
    DAHN event:
      inspect semantic subject
          |
    Dancer experience updates experience state
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
- Dancer-experience compression;
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

Relationship definitions and runtime population are distinct semantic inputs.
Rust/MAP remains authoritative for relationship semantics and target information;
TypeScript coordinates asynchronous inspection and presentation through that
boundary. Discovery MUST NOT require eager materialization of every relationship
before a holon's initial display. Background relationship inspection uses bounded
concurrency; the limit is configurable or implementation-defined.

Navigation establishes destination topology before presenting destination content
and does not structurally navigate toward a relationship known to have no target.
The selected RootedNavigation visualizer owns these internal transitions and
coordinates pending destination presentation with its child visualizers; the
Space Navigator Dancer does not take ownership of their geometry. A temporary
presentation does not replace Visualizer Selection or grant TypeScript authority
to choose a different semantic visualizer after a realization failure.

The exact Space Navigator retrieval sequence and browse-mode visibility rules
are defined in the Design Specification; spatial ordering is defined in the
[Path Inspector grammar](visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md#28-destination-first-transitions).

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

# 45. PropertyMap and Value Visualizers

[PropertyMap](visualizers/property-map/kind-spec.md) and
[Value](visualizers/value/kind-spec.md) define the independent semantic families.
PropertyMap owns set-level composition and can select String label and typed
value children directly. There is no intervening Property VisualizerKind.
The Node parent need not hard-code renderers for value types.

---

# 46. Collection Visualizers

The [Collection kind](visualizers/collection/kind-spec.md) defines homogeneous
collection subjects independently of their source. Concrete table behavior
belongs to the [Table Collection specification](visualizers/collection/table/design-spec.md)
and its current detailed source. Semantic topology instead belongs to the
[Structure family](visualizers/structure/kind-spec.md); a drawing's geometry
alone does not decide its kind.

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

The architecture MUST preserve this ownership distinction regardless of Canvas-hosted Dancer presentation.

The owning Dancer and selected Visualizer specifications define how this
semantic distinction appears to the person.

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

- exposing the applicable transaction action through the active Dancer experience;
- presenting transaction state;
- refreshing affected visualizers after the operation.

The Space Navigator Design Specification defines Commit's user-facing placement and behavior.

---

# 52. Commit Flow

Conceptually:

    user requests Commit
          |
    Dancer experience interaction
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

Rust SHOULD expose sufficient transaction status for the active Dancer experience to present appropriate transaction controls.

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
- one visualizer realization may fail, after which the Selector may be asked
  to reselect a locally realizable Visualizer.

---

# 64. Error Boundaries

Errors SHOULD be surfaced near the operation or semantic object that failed.

Examples:

- value-specific error → Property or Value Visualizer;
- collection retrieval error → Collection Visualizer;
- dance failure → action/result region;
- visualizer acquisition failure → runtime-resolution boundary;
- transaction validation error → relevant visualizers plus transaction-level summary;
- Dancer-experience-level failure → root experience-realization boundary.

The Selector may evaluate compatible generic candidates under ordinary policy;
if none qualifies it returns an explicit error. The TypeScript runtime does not perform that
recovery itself.

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

This delivery guidance is retained in the
[implementation-plan source notes](dahn-docs-refactor-impl-plan.md#architecture-delivery-guidance-retained-for-doc5).

---

# 68. Initial Architectural Modules

This delivery guidance is retained in the
[implementation-plan source notes](dahn-docs-refactor-impl-plan.md#architecture-delivery-guidance-retained-for-doc5).

---

# 69. Architectural Testing Boundaries

This delivery guidance is retained in the
[implementation-plan source notes](dahn-docs-refactor-impl-plan.md#architecture-delivery-guidance-retained-for-doc5).

---

# 70. Architecture That Should Not Be Over-Generalized Initially

This delivery guidance is retained in the
[implementation-plan source notes](dahn-docs-refactor-impl-plan.md#architecture-delivery-guidance-retained-for-doc5).

---

# 71. Core Architectural Invariants

## 71.1 Rust Owns Semantic Truth

Holon state, descriptors, relationships, staging, transactions, caches, validation, persistence, and adaptive history remain MAP/Rust responsibilities.

## 71.2 TypeScript Owns Experience Realization

Rendering, layout, Dancer experience state, focus, selection, navigation presentation, and immediate interaction remain TypeScript responsibilities.

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

Rust chooses a Visualizer Holon and the implementation identity to realize for
the target runtime.

The client runtime resolves and executes that supplied implementation. It
reports an explicit realization failure when it is unavailable and does not
select an alternative Visualizer or implementation.

## 71.7 Generic Fallbacks Preserve Usability

Generic Visualizers are ordinary applicable candidates under the
[selection policy](dahn-design-spec.md#1421-slot-directed-descriptor-selection).
Their absence produces an explicit error, not permission to bypass the slot
contract or silently substitute an implementation.

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

The subject being represented, the selected Visualizer Holon, and its
Visualizer Occurrence are distinct identities. The same subject may appear in multiple
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

Architecture assigns responsibility. DAHN design defines reusable composition
mechanisms. The selected Visualizer owns experiential grammar; Space Navigator
owns its direct Dancer roles and subject coupling. Detailed behavior delegates
to the corresponding owner, not to a universal Space Navigator hierarchy.

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
- Canvas composition and Dancer-internal visualizer composition;
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

## 72.4 Canvas-Hosted Dancer Experiences

The Canvas uses these architectural capabilities to host concrete Dancer
experiences. A Dancer defines its experience's internal interaction environment
by composing visualizer roles.

The Space Navigator is the first such Dancer.

Its Dancer interactions are defined in the
[Space Navigator grammar](../space-navigator/space-navigator-interaction-grammar.md).
Spatial transformations belong to the selected RootedNavigation Visualizer.
Dancer action and coordination behavior belongs to the
[Space Navigator design](../space-navigator/space-navigator-design-spec.md).

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
          | selected implementation information
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
    Canvas-hosted Dancer experience
          |
          v
    Human

The central architectural rules are:

> **MAP determines semantic truth.**

> **The federated Visualizer Commons determine the available experience ecosystem.**

> **The Rust DAHN Selector determines which applicable visualizer should be used.**

> **TypeScript resolves, composes, and renders the selected experience.**

> **The Canvas allocates real estate to a Dancer's root experience realization; every
> visualizer then allocates space to its children and composes within its own
> allocation.**

> **Themes determine stylistic expression without redefining semantic behavior.**

> **User gestures can shape both personal and collective future experience.**

> **Rust preserves semantic, staged, transaction, and adaptive state.**

> **TypeScript preserves spatial, occurrence, and immediate interaction state.**

> **The Space Navigator proves these architectural contracts without defining the limits of DAHN.**
