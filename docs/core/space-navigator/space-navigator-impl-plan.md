# DAHN Space Navigator Implementation Plan v1.0

## Status

Draft implementation plan derived from:

- `space-navigator-arch.md` v0.4
- `space-navigator-interaction-grammar.md`
- `space-navigator-design-spec.md`

This plan supersedes the earlier Space Navigator implementation plan.

## Change Log

| Version | Changes from prior version |
| --- | --- |
| v1.0 | Adds the Dancer-neutral MAP Application Launcher foundation before PR 5.a, retains PR 5.a as the generic Canvas shell, and adds the HolonSpace home-Dancer mount after the reusable Node shell. The Launcher never hard-codes Space Navigator. |
| v0.9 | Recasts PR 5.a as the generic DAHN Canvas Visualizer and application-launch seam. Canvas selection follows Human Agent Theme selection; a mock launch driver makes the one-Theme/one-Canvas bootstrap path observable. Space Navigator remains a hosted Dancer, not a Canvas. |
| v0.8 | Inserts PR 5.c, the bounded DAHN Launch Experience application-shell slice, after the initial Canvas and Node shell can render. |
| v0.7 | Inserts PR 5.b, a user-visible generic Node shell, before PR 6. Properties and Value visualization now fills that established Node-owned Property Viewer Pane rather than preceding its host. |
| v0.6 | Clarifies that PR 6 establishes Properties and Value visualization contracts only; they first become user-visible inside the full Node Visualizer in PR 8. |
| v0.5 | Inserts Canvas-first PR 5.a after the delivered PR 5, preserving Phase 2-and-later PR identifiers; adds the set-level `PropertyMapVisualizer` / Property Viewer Pane; establishes Action Visualizers as incremental composition within the PR that introduces each action; adds PR 40.a for the Canvas-scoped `LoadHolons` Dance and retirement of the separate Load Holons app. |
| v0.4 | Baseline implementation plan. |

## Purpose

This plan decomposes the Space Navigator into a sequence of small, mergeable PRs that monotonically increase capability while proving the DAHN architecture incrementally.

Each PR should:

- leave the system in a working state;
- introduce one primary behavioral or architectural capability;
- be independently reviewable and testable;
- reuse previously established abstractions;
- avoid introducing speculative infrastructure significantly ahead of its first use;
- be small enough for a single developer working with Codex to understand, implement, validate, and merge confidently.

The implementation plan is derivative.

Architectural decisions belong in `space-navigator-arch.md`.

Normative spatial and compositional rules belong in
`space-navigator-interaction-grammar.md`.

Normative concrete Space Navigator behavior belongs in
`space-navigator-design-spec.md`.

If this plan conflicts with an upstream specification, the upstream
specification wins and this plan should be updated. The plan MUST NOT introduce
an alternate topology, compression, overflow, allocation, or re-rooting rule.

---

# 1. Delivery Strategy

The implementation should progress through working vertical slices rather than attempting to build the complete DAHN framework before any experience is visible.

At the same time, early implementation MUST preserve several architectural seams that would otherwise become expensive to retrofit:

- Visualizer Holon Types and instances versus concrete Visualizer Implementations;
- a DAHN schema definition before visualizer runtime resolution or Selector work;
- Rust-side DAHN Visualizer Selection Service boundary;
- Visualizer Holon / implementation-reference TypeScript runtime resolution;
- explicit no-selection errors when no compatible Visualizer exists;
- Rust-owned MAP and staged state;
- TypeScript-owned visualizer occurrence and Canvas state;
- parent-owned layout allocation;
- theme-token-based styling;
- Dancer-experience-scoped transaction controls;
- semantic interaction events rather than direct cross-component manipulation.

The initial implementations behind these seams MAY be deliberately simple.

For example:

- the initial Rust Visualizer Selection Service may deterministically select the
  sole compatible bootstrap candidate, while returning an explicit error when
  no compatible candidate exists;
- the initial TypeScript Visualizer Runtime may resolve only locally bundled
  implementations for a Visualizer Implementation reference selected by Rust;
- the initial theme may provide only one token set;
- the initial Canvas layout may use fixed canonical Node dimensions.

The seam matters before the sophisticated implementation behind it does.

---

# 2. PR Sizing Rule

A PR should normally introduce one primary capability.

A useful test is:

> Can the PR be described by one primary behavioral or architectural change and demonstrated independently?

If not, it is probably too large.

Another useful test is:

> Could this PR be reverted without requiring the previous PR to be reverted?

If not, the PR may contain too many intertwined changes.

Split a PR when it begins to combine multiple significant new concerns, for example:

- visualizer selection plus remote visualizer acquisition;
- collection row interaction plus Canvas traversal plus compression;
- staging plus Undo plus Commit;
- relationship editing plus a sophisticated target-search UX;
- adaptive gesture recording plus collective salience aggregation.

## 2.1 Planned Dev Point Estimates

Each PR below has a planned estimate using the MAP Dev Points rubric:
`1` tightly bounded, `2` small, `3` medium, `5` large, and `8` unusually
uncertain or cross-cutting. These are planning estimates, not delivered actuals.
Re-estimate a PR when its GitHub issue grounds a materially different contract,
dependency, or test surface.

---

# 3. Phase 0 — DAHN Runtime Seams

The goal of this phase is not to build generalized infrastructure.

It is to establish the minimum architectural boundaries required before the first reusable visualizers are built.

---

## PR 1 — DAHN TypeScript MAP Adapter

**Planned Dev Points:** 3

### Goal

Introduce a thin DAHN-facing semantic adapter above the existing TypeScript MAP SDK.

### Scope

Provide the initial adapter boundary for operations needed by the first read-only Space Navigator slices.

Initial operations may include:

- inspect or resolve a holon reference;
- retrieve identifying/scalar projections;
- retrieve effective descriptor information;
- expand a relationship.

The adapter SHOULD:

- normalize async behavior;
- centralize command/SDK translation;
- normalize errors;
- remain independent of Space Navigator geometry.

### Non-Goals

Do not:

- duplicate MAP semantic state in TypeScript;
- introduce a TypeScript holon cache as an authoritative source;
- implement staging or transactions yet;
- implement visualizer selection yet.

### Acceptance Criteria

- Visualizers do not need to call low-level command serialization directly.
- MAP references remain Rust-backed semantic references.
- Adapter tests can run against mocked SDK operations.
- The adapter contains no Canvas placement or rendering decisions.

---

## Schema Task S1 — First-Cut DAHN Visualizer Schema Definition

**Planned Dev Points:** 5

### Goal

Define the minimal MAP-native DAHN schema in `map-holons` before the Space
Navigator introduces runtime visualizer resolution or Rust-side selection.

### Scope

Author the schema source of truth and its bootstrap resources for:

- the abstract `Visualizer` type-family anchor;
- concrete `CanvasVisualizer`, `NodeVisualizer`, `CollectionVisualizer`,
  `PropertyMapVisualizer`, `PropertyVisualizer`, `ValueVisualizer`,
  `ActionVisualizer`, `StructureVisualizer`, `GraphVisualizer`,
  `RootedNavigationVisualizer`, and `GeospatialVisualizer` Holon Types;
- a `VisualizerImplementation` semantic entity or the closest
  schema-native equivalent;
- a Visualizer-to-Implementation relationship;
- initial MAP-semantic applicability.

The Space Navigator Dancer and any HolonSpace-oriented experience artifacts
belong to the separately loadable Space Navigator House Troupe package, not
the Core Schema bootstrap bundle.

The schema MUST use concrete, stabilized descriptors for ordinary runtime
Visualizer Holons. It MUST keep Visualizer semantic identity distinct from
executable implementation identity and from MAP version/lineage metadata.

### Non-Goals

Do not implement:

- remote package acquisition or arbitrary executable-code loading;
- sandboxing, signing, or dependency isolation;
- full Visualizer Commons governance;
- adaptive preference, salience, affinity, or embedding schemas; or
- a parallel `VisualizerDescriptor` model or semantic `VisualizerId`.

### Acceptance Criteria

- The map-holons schema source defines the minimal DAHN Visualizer model and
  passes its schema validation workflow.
- Core Visualizer Holons are representable through concrete Visualizer types.
- A Visualizer Holon can relate to one or more executable implementations.
- Initial applicability is available through MAP semantics before implementation
  execution.
- The generic DAHN schema is available to dependent runtime work without
  requiring Space Navigator-specific semantic resources at Core bootstrap.

### Dependency

PRs 2 and 3 depend on this task. The Space Navigator documentation references
the accepted schema; it does not become a competing schema source of truth.

---

## PR 2 — Visualizer Implementation Runtime Resolution

**Planned Dev Points:** 3

### Goal

Resolve an already-selected Visualizer Holon together with one
Rust-selected Visualizer Implementation reference to locally available
TypeScript executable code.

### Scope

Introduce a minimal TypeScript Visualizer Runtime with:

- resolution from the selected Visualizer Holon and one supplied
  Visualizer Implementation reference;
- locally bundled implementation-key-to-definition mappings; and
- failure handling when a selected implementation is unavailable.

The implementation key indexes executable definitions. A local definition ID
may support registry loading, but it is implementation-private and remains
distinct from the Visualizer Holon, VisualizerImplementation Holon, and stable
implementation key.

Initial registrations may include placeholders for:

- Generic Holon Node Visualizer;
- Table Collection Visualizer;
- generic Properties Visualizer;
- generic scalar Value Visualizers.

For this runtime slice, a placeholder need only be a loadable executable
definition. Canvas mounting, composition, and rendering behavior remain out of
scope.

### Non-Goals

Do not implement:

- Visualizer Commons discovery;
- remote packages;
- version acquisition;
- sandboxing;
- adaptive selection.

### Acceptance Criteria

- TypeScript can resolve a selected Visualizer Holon plus the one
  Rust-selected implementation reference into an executable local
  implementation.
- Visualizer Holon identity is distinct from implementation identity.
- TypeScript does not traverse `ImplementedBy`, choose between implementation
  candidates, evaluate applicability, or select a Visualizer.
- The stable implementation key maps to a locally executable definition without
  making that definition's registry ID a semantic identity.
- An unavailable local implementation produces an explicit realization error
  containing the supplied Visualizer and implementation identity where
  available. Rust may make a new selection request through ordinary Service
  policy; it must not apply a fallback.
- No Canvas needs to instantiate a concrete visualizer by hard-coded implementation class where the runtime boundary should apply.

---

## PR 3 — Rust DAHN Selector Boundary

**Planned Dev Points:** 3

### Goal

Establish the architectural boundary in which Rust chooses a Visualizer Holon.

This PR also introduces the smallest Dancer activation seam required to keep
Space Navigator outside Core: generic Core Dancer semantics, a separately
packaged `SpaceNavigator.Dancer` House Troupe resource, and an idempotent
host-side activation path that loads that package's local semantic resources
on demand. This is an incremental activation implementation, not the target
Dynamic Dancer Runtime or generalized Dance extensibility architecture.

### Scope

Introduce the minimum Rust-side selector command/API needed to answer a request such as:

    select visualizer for category + semantic subject/context

After Space Navigator activation, the initial implementation MAY
deterministically return the appropriate package-provided fallback Visualizer
Holon.

Return the semantic selection result, such as:

- selected Visualizer Holon reference;
- required Visualizer type/category;
- optional indication that alternatives exist.

Define the first Visualizer-afforded `Materialize` Dance as a separate
operation. Given the selected Visualizer Holon reference, Materialize retrieves
the executable JavaScript realization through Rust and returns a typed module
payload. The initial materializer MAY read local filesystem artifacts. The
TypeScript registry is a cache of materialized modules, not an authority for
selection or artifact retrieval.

Preserve the existing DanceV2 execution behavior while introducing an
invocation-aware implementation-resolution seam. The executor resolves an
already available implementation from the bound invocation, and initially
delegates to the existing exactly-one static candidate policy. Dance execution
does not activate a Dancer; activation makes its semantic package and bundled
implementation available beforehand.

The Host dispatches the resolved implementation identity, not a Dance name.
For the initial local Visualizer materializer, filesystem access remains inside
that Host-native implementation; the shared DanceV2 pipeline continues to own
binding, semantic validation, static resolution, and descriptor-driven
response construction.

### Non-Goals

Do not implement:

- federated Visualizer Commons discovery;
- adaptive scoring;
- personal preference;
- collective salience;
- trend or maturity scoring.
- federated or remote artifact acquisition, signing, verification, or
  sandboxing.
- WebAssembly Components, a Dancer sidecar, dynamic artifact acquisition, or
  generalized Dance implementation extensibility.

### Acceptance Criteria

- TypeScript requests selection rather than selecting semantic visualizers itself.
- The decision crosses the existing MAP command/IPC boundary.
- Rust returns a stable Visualizer Holon reference rather than an opaque
  application identifier.
- Selection and Materialize are distinct: selection returns the Visualizer
  reference; Materialize returns executable realization payload.
- TypeScript caches a materialized module by the selected Visualizer identity
  and requests Materialize only on cache miss.
- TypeScript does not select a Visualizer, choose an implementation, or
  retrieve artifacts directly.
- Core bootstrap does not load Space Navigator-specific schemas or instances.
- Activating `SpaceNavigator.Dancer` loads its locally bundled semantic package
  on demand, is idempotent, and fails explicitly when that package cannot be
  resolved or loaded.
- DanceV2 resolves implementations through a bound-invocation seam while
  preserving the current exactly-one static candidate policy and
  descriptor-driven response construction.
- Dance execution does not implicitly activate a Dancer.
- Tests unrelated to Space Navigator do not require its semantic resources.
- The fallback-only implementation proves the correct architectural direction.

---

## PR 4 — Theme Token Foundation

**Planned Dev Points:** 2

### Goal

Prevent the first visualizers from embedding visual style constants that later need to be removed.

### Scope

Introduce the minimum semantic theme-token mechanism required by initial visualizers.

Initial tokens may cover:

- surfaces;
- text;
- borders;
- spacing;
- selected/focus states;
- action treatment.

Provide one locally bundled Visualizer Commons Theme contribution for the
demonstration. The Theme realizes an independently contributed MDS and is
offered by the active HolonSpace for Human Agent selection; it is not owned by
Space Navigator or Core bootstrap.

### Non-Goals

Do not implement:

- theme marketplace;
- multiple sophisticated themes;
- adaptive theme selection.

### Acceptance Criteria

- Initial visualizers consume semantic tokens for theme-owned styling.
- Core visualizer code does not hard-code theme-specific colors or equivalent styling decisions.
- A different token set could later change stylistic expression without changing visualizer semantics.
- The DAHN Selector can retain only Visualizer candidates whose declared
  DesignToken dependencies are included in the MDS established by the selected
  Theme, without making Space Navigator own that MDS or Theme.

---

# 4. Phase 1 — Canvas-First Read-Only Experience

Phase 1 delivers visible experience before it expands reusable components.
PR 5, the Table Collection Visualizer, was delivered before this sequencing
change and remains a useful mounted component once collection exploration
begins. It does not need to be revisited or renumbered. PR 5.a-pre establishes
the Dancer-neutral application session required by Canvas. PR 5.a then inserts
the Canvas immediately after it, and PR 5.b inserts its first generic Node
shell. PR 5.b.1 selects and mounts the active HolonSpace's home Dancer.
Existing identifiers from Phase 2 onward remain unchanged; future insertions
use a dotted identifier such as `PR 10.a` rather than renumbering a later
planned PR. The Canvas is visible in PR 5.a; component contracts that require a
Node-owned slot need not be independently visible before the Node arrives in
PR 5.b. PR 5.c then adds the launch experience once application startup,
readiness observation, and a selected home-Dancer state are all available.

`PropertyMapVisualizer` is the set-level visualizer for the scalar Property
Viewer Pane. It owns property-set presentation (for example layout, grouping,
ordering, and responsive treatment); it is not a synonym for an individual
`PropertyVisualizer`. Individual Property and Value Visualizers remain
available as composition boundaries within that pane.

---

## PR 5 — Static Table Collection Visualizer

**Planned Dev Points:** 3

### Goal

Introduce the first concrete generic Collection Visualizer.

### Scope

Implement the Table Collection Visualizer with:

- homogeneous collection input;
- collection header;
- column headers;
- one row per element;
- scalar value collections;
- holon collections using an explicitly supplied property projection.

The visualizer MUST remain independent of collection provenance.

It should not care whether its input came from:

- array property;
- relationship;
- dance result.

### Non-Goals

Do not implement:

- sorting;
- filtering;
- row navigation;
- editing;
- adaptive ordering.

### Acceptance Criteria

- A scalar collection can render as one value column.
- A holon collection can render projected properties as columns.
- One collection implementation works independent of collection origin.
- The visualizer is selected/resolved through the visualizer runtime boundary.

---

## PR 5.a-pre — MAP Application Launcher Foundation

**Planned Dev Points:** 5

### Goal

Establish the Rust/Tauri application-startup seam that opens one local active
HolonSpace and makes a MAP-bound ApplicationSession available to Canvas work.

### Scope

Implement the Launcher foundation defined by
`docs/dahn/map-application-launcher-design-spec.md`:

- Tauri startup coordination and MAP host/command-runtime readiness;
- open or create one local active HolonSpace;
- idempotent intrinsic Core Schema bootstrap through the statically available
  bootstrap adapter;
- activation of the base packages needed by generic Canvas selection;
- observable startup stages and recoverable stage-specific failure; and
- a typed ApplicationSession/readiness result consumed by the Canvas shell.

The foundation MUST NOT start the legacy Holon Data Loader application or route
startup through `HolonsClient`, `MultiplexService.dance()`, `map_request`, or
the deprecated Holochain receptor.

### Non-Goals

Do not select or mount Canvas, select a Dancer, name Space Navigator, create a
long-lived write transaction, present a space chooser, or implement window
placement policy. Canvas and Dancer realization follow in later slices.

### Acceptance Criteria

- `npm start` reaches an ApplicationSession with one active local HolonSpace
  without launching the legacy Loader surface.
- Core is the only intrinsically loaded package; ordinary post-bootstrap loads
  use the normal MAP command/SDK path.
- Repeated startup recognizes completed bootstrap and failure exposes the
  failed stage without treating uncertain bootstrap as complete.
- The Launcher has no static Space Navigator or other Dancer dependency.

---

## PR 5.a — DAHN Canvas Visualizer

**Planned Dev Points:** 3

### Goal

Introduce the generic DAHN Canvas Visualizer and mount it from the MAP-bound
ApplicationSession produced by PR 5.a-pre.

### Scope

Create:

- an initial Canvas Holon loaded with bootstrap schema resources and a runtime
  `CanvasVisualizer` holonic wrapper for the selected Canvas;
- generic Canvas chrome and a distinct hosted-Dancer allocation region;
- Canvas-owned Theme projection, applied once for all future hosted Dancers;
- Canvas-local empty-host, realizing, mounted, and realization-error states;
- selection of a Theme-compatible Canvas from the ApplicationSession's active
  HolonSpace; and
- a visible application host for that selected Canvas without requiring a
  Dancer or the separately defined pre-launch visual experience.

The Human Agent selects a preferred Theme. The DAHN Visualizer Selection
Service then selects a compatible Canvas. The first bootstrap path is
deterministic because it has one candidate at each step, not because either
selector has a hard-coded fallback. A missing Theme or compatible Canvas is an
explicit selection error.

Canvas chrome governs only Canvas-level hosting/composition concerns. It MUST
NOT introduce transaction controls, which belong to the hosted Dancer
experience.

### Non-Goals

Do not implement the Space Navigator Dancer, its Rooted Navigation Visualizer, Node, property,
collection, transaction, home-Dancer selection, window-tiling policy, or the
pre-launch visual experience defined for PR 5.c.

### Acceptance Criteria

- The bootstrap Canvas Holon and its `RuntimeCanvasVisualizer` wrapper are
  selected through the Canvas Selector after Theme selection.
- The generic Canvas exists independently of Space Navigator and has distinct
  Canvas chrome and hosted-Dancer allocation regions.
- The selected Theme is projected once at Canvas initialization and is the
  shared themed environment for future hosted Dancers.
- Canvas mounts through the ApplicationSession established by PR 5.a-pre; no
  mock launch driver or legacy Loader ingress is introduced.
- No-selection and realization failures are explicit; neither the launcher,
  Canvas, Dancer, nor TypeScript runtime applies a fallback.
- A developer can mount the Canvas and observe its awaiting-home-Dancer and
  realization states without waiting for a Space Navigator-specific UI.

---

## PR 5.b — Basic Generic Holon Node Shell

**Planned Dev Points:** 5

### Goal

Render one arbitrary holon through the selected Node Visualizer before filling
its component slots with Property or Value visualization.

### Scope

Implement the initial Generic Holon Node Visualizer with:

- Title Bar;
- Node Action Bar host shell;
- an empty Property Viewer Pane slot;
- bottom Collection Tab Bar shell; and
- right-side Single-Value Tab Rail shell.

Use the Rust Selector to select the Node Visualizer and its implementation, and
the TypeScript Visualizer Runtime to resolve that supplied implementation.

### Geometric Requirements

The full initial Node geometry includes:

- main body;
- visible right-side rail;
- visible bottom tab bar; and
- a reserved Property Viewer Pane region.

Neither navigation surface yet opens child content. The Property Viewer Pane is
a visible, intentionally unpopulated Node-owned slot until PR 6 mounts its
selected Properties Visualizer.

### Acceptance Criteria

- The generic Node composition path asks Rust for a Node Visualizer selection.
- The selected Visualizer Holon and selected implementation reference resolve
  through the TypeScript runtime.
- Rust can select the Generic Holon Node Visualizer when it is an applicable
  candidate that satisfies the request; no fallback selection is implied.
- The Node, its Property Viewer Pane slot, and both navigation surfaces are
  visible in the Canvas.
- No domain-specific Node screen or Property/Value presentation is required.

---

## PR 5.b.1 — HolonSpace Home-Dancer Mount

**Planned Dev Points:** 5

### Goal

Land the launched application in the active HolonSpace's selected home Dancer
experience without making Launcher or Canvas depend on Space Navigator.

### Scope

- define and resolve the active HolonSpace's home-Dancer candidate set;
- request home-Dancer selection through the Rust DAHN Visualizer Selection
  Service using active-space, Theme/MDS, runtime, and person context;
- materialize the selected Dancer's root experience realization through the
  existing runtime boundary;
- give that realization the active HolonSpace context and a Canvas allocation;
  and
- present an explicit Canvas host error/retry state when home-Dancer selection
  or realization fails.

The initial candidate set MAY contain only `SpaceNavigator.Dancer`, but that is
a Selection Service result. Neither Launcher nor Canvas may name it as a
fallback or direct dependency.

### Non-Goals

Do not add alternate-home preference persistence, command-line launch override,
multi-window behavior, Space Navigator navigation, transaction controls, or
generic Dancer discovery beyond the declared home candidate set.

### Acceptance Criteria

- A successful launch mounts the selected Dancer's root experience realization
  in the Canvas allocation for the active HolonSpace.
- No compatible candidate and realization failure remain distinct explicit
  states; neither silently selects another Dancer.
- The active HolonSpace is Dancer experience context, not a request to select a
  Node Visualizer directly for `HolonSpace.HolonType`.
- Selection can resolve Space Navigator initially without a static Launcher or
  Canvas reference to it.

---

## PR 5.c — DAHN Launch Experience

**Planned Dev Points:** 3

### Goal

Provide a brief, offline-capable entry into DAHN that transitions from cosmos
to I-Space without turning the launch into a MAP visualizer, media subsystem,
or cinematic production.

### Dependencies

- the DAHN application shell can start initialization;
- initialization readiness is observable; and
- an initial home-Dancer state can render (PR 5.b.1).

### Scope

Implement a small application-shell launch controller with conceptual states:

    Initializing → Nebula → StellarTransition → Earth → Place
                 → RevealNavigator → Complete

Its only responsibilities are scene sequencing, readiness coordination, skip,
and handoff to the Navigator; it contains no MAP semantic logic. Use a small,
local declarative scene list so asset, duration, initial/final scale, focal
point, blur, fade, and easing can be tuned without scattering timing and
transforms through rendering components. This is not a generalized animation
DSL.

Use locally bundled, optimized still-image derivatives and ordinary platform
rendering: full-screen image layers, CSS transforms, opacity, filters,
crossfades, and `object-fit: cover` (or equivalent). The sequence is NGC 346,
stellar light, NASA DSCOVR / EPIC whole Earth, verified Okavango Delta
observational imagery, then the initial Space Navigator. NGC 346's light may
bridge into Earth but must not be represented as literally the Sun.

Start DAHN initialization immediately. Early readiness does not truncate the
narrative; late readiness enters a subtle final holding state. Skip becomes
available after a short interval: before readiness it advances to the holding
state, and after readiness it reveals the Navigator promptly. Implement
reduced-motion, keyboard-accessible Skip and Image credits controls, safe
brightness treatment, and an asset-load fallback that never blocks startup.

For each bundled asset, record in versioned provenance metadata: canonical
source URL; asset identity/title; mission/instrument; complete supplied credit;
usage-policy URL; retrieval date; third-party restrictions; and local crop,
resize, compression, color-space, or format transformations. Preserve exact
credits in the Image credits overlay and state that the imagery derives from
scientific observation, not AI-generated artwork. Verify the exact Okavango
asset and all source-provided attribution before bundling.

### Non-Goals

Do not introduce MAP image/video ValueTypes, media Holons, IPFS or other
storage receptors, Visualizer Commons infrastructure, dynamic media loading,
Canvas/WebGL/Three.js/GSAP, video, GIS, map tiles, geolocation, personalized
locality, a generalized scene framework, or a definitive DAHN aesthetic.

### Acceptance Criteria

- The local sequence reads NGC 346 → stellar light → Earth → living place →
  I-Space / Space Navigator through restrained still-image transitions.
- Initialization and narrative timing remain independent; both early- and
  late-readiness behavior, plus Skip in both states, are covered by tests.
- The Navigator handoff feels like arrival and never reveals incomplete UI.
- Reduced motion, keyboard-accessible controls, safe luminosity, offline
  operation, optimized assets, and failed-asset fallback are verified.
- Asset-by-asset provenance and complete supplied credits are recorded and
  exposed by an unobtrusive Image credits affordance.
- The implementation adds no new MAP semantic media, visualizer, animation,
  or geospatial infrastructure.

---

## PR 6 — Properties Pane and Descriptor-Driven Value Presentation

**Planned Dev Points:** 3

### Goal

Fill the selected Generic Holon Node Visualizer's Property Viewer Pane with
descriptor-driven scalar-property presentation.

### Scope

Introduce the minimum `PropertyMapVisualizer`, Property Visualizer, and Value
Visualizer contracts required to display current scalar types.

The generic Properties Visualizer MUST provide the initial Property Viewer
Pane: a set-level scalar-property presentation with named value slots. It
selects or receives individual Property/Value Visualizers without embedding a
growing switch statement for concrete value types.

Define the Properties Visualizer's named value slots and the Value Visualizer
selection/resolution path they use. Mount the selected Properties Visualizer
into the Property Viewer Pane established by PR 5.b.

### Non-Goals

Do not implement editing, standalone Property/Value presentation outside the
Node, table-cell integration, or property-set personalization yet.

### Acceptance Criteria

- A scalar Property set resolves to a `PropertyMapVisualizer` rather than a
  Node directly laying out raw values.
- The generic Properties Visualizer owns the initial Property Viewer Pane and
  provides Property/Value composition slots.
- Each supported value type resolves to an applicable Value Visualizer.
- Unknown-but-supported fallback behavior is explicit.
- The same Property and Value contracts can later support edit mode.
- Scalar Properties and Values are visibly rendered only inside the selected
  Node's Property Viewer Pane.

---

## PR 9 — Descriptor-Driven Affordance Classification

**Planned Dev Points:** 3

### Goal

Populate the visible Node structure from effective descriptor semantics.

### Scope

Classify:

| Affordance | Shape | Initial Placement |
| --- | --- | --- |
| Property | scalar | Property Viewer |
| Property | array | Collection Tab |
| Relationship | max = 1 | Single-Value Rail |
| Relationship | max > 1 / unbounded | Collection Tab |
| Dance | no result | Node Action classification |
| Dance | single holon | singular-result classification |
| Dance | collection | collection-result classification |

When this PR first renders descriptor-classified Node actions, it introduces
only the generic Action Visualizer needed for that rendering: initial button or
overflow-menu treatment that emits semantic action intent. This is not a
separate Action Visualizer delivery track. Each PR introduces or extends an
Action Visualizer only where its newly delivered behavior requires one.

Dance invocation itself is deferred.

### Normative Requirement

Runtime result count MUST NOT alter descriptor-defined cardinality.

### Acceptance Criteria

- Structural affordances derive from descriptors.
- Empty singular relationships remain classified singular.
- Plural relationships with zero or one target remain classified plural.
- Dance result shape can be classified before invocation.
- The Node Visualizer does not contain type-specific affordance rules.
- A descriptor-classified Node action is rendered through the selected generic
  Action Visualizer and emits semantic action intent.
- Action host scope remains explicit: holon actions mount in the Node Action
  Bar; Canvas-scoped actions mount in Canvas chrome, while transaction-scoped
  actions mount in the active Dancer's action surface
  when the PR delivering their behavior introduces them.

---

# 5. Phase 2 — Vertical Collection Exploration

---

## PR 10 — Collection Tab Activation

**Planned Dev Points:** 3

### Goal

Make plural affordances inspectable.

### Scope

Support activation of:

- array-valued property tabs;
- multi-valued relationship tabs.

On activation:

- retrieve contents lazily where needed;
- request/select a Collection Visualizer;
- render it below the Node;
- reuse the same collection region when switching tabs.

Support:

- unresolved;
- loading;
- loaded empty;
- loaded;
- error.

### Geometry

- Collection Tab Bar width equals owning Node width.
- Expanded Collection Visualizer width equals owning Node width.
- No collection content consumes vertical space before activation.

### Acceptance Criteria

- Array values display through Collection Visualizer.
- Relationship targets display through Collection Visualizer.
- Empty plural relationships display an empty collection state.
- One-target plural relationships still display as collections.
- Switching tabs does not replace the parent Node.

### Milestone

This is the first useful read-only Space Navigator slice:

    inspect holon
        |
    choose plural affordance
        |
    inspect collection

---

## PR 11 — Collection Row Selection

**Planned Dev Points:** 2

### Goal

Separate collection selection from navigation.

### Scope

Implement:

- single-click row selection;
- selected-row state;
- semantic activation event for navigation, initially via double-click.

The Collection Visualizer emits intent but does not place child Nodes.

### Acceptance Criteria

- Row selection does not itself navigate.
- Row activation emits the selected semantic holon reference.
- Collection code remains independent of Canvas geometry.
- Selected-row state belongs to the collection occurrence.

---

## PR 12 — First Vertical Child

**Planned Dev Points:** 3

### Goal

Navigate from a collection into one selected holon.

### Scope

On collection-row activation:

- create a child visualizer occurrence;
- select/resolve its Node Visualizer;
- render it beneath the Collection Visualizer;
- preserve source Node and Collection;
- record traversal provenance.

### Acceptance Criteria

- Child Node uses normal Node Visualizer selection and runtime resolution.
- Parent and collection remain present.
- Child occurrence identity is distinct from holon identity.
- Provenance records the collection traversal.
- The same holon may later appear in multiple occurrences.

---

## PR 13 — Vertical Sibling Switching and Retained Vertical Alternatives

**Planned Dev Points:** 5 (revised from 2 to include retained-path insertion)

### Goal

Support exploration of collection members while preserving traversed paths according
to the authoritative [Path Inspector Interaction Grammar](path-inspector-grammar.md)
v0.2, especially §§2.3–2.6 and §§3.1–3.8.

Replace an untraversed leaf; displace and retain a traversed path. This supersedes
this PR's earlier replacement-only scope and prohibition on simultaneous sibling
branches.

### Scope

When a collection already has a canonical vertical child:

- activating another member may replace that child in the same traversal position
  only while it remains an untraversed leaf;
- once navigation has continued through that child, retain its occurrence and
  continuation when another member is activated;
- place the new vertical alternative in the anchor's current column, displace the
  prior traversed vertical continuation into a newly inserted column immediately
  to the right, and shift pre-existing columns to the right as necessary;
- preserve occurrence identity, semantic Holon identity, source occurrence,
  collection/affordance provenance, traversal direction, and descendant attachment
  throughout insertion;
- keep the source Node and Collection available for sibling exploration without
  reconstructing them merely because another member is activated;
- update collection selection and focus the newly activated child through the
  normal Node Visualizer selection and realization path.

Keep topology separate from its sparse grid projection. Columns preserve vertical
traversal paths and rows preserve horizontal traversal paths; do not compact gaps
by falsely joining unrelated paths. Sparse cells carry no occurrence identity or
provenance. Insertion changes coordinates, not navigation identity, and does not
by itself change the current column focus.

Changing a collection tab or the collection viewed within a Node is local child
state, not a topology-producing operation. It must not erase retained traversal
history or insert a branch merely because the visible collection changes. Member
activation creates or activates a vertical child with the correct source
collection and affordance provenance.

Retained occurrences remain usable for further traversal and restoration. Integrate
with the existing PR 16 whole-row allocation and compression behavior: cells sharing
a row receive the same height, cells sharing a column receive the same width, and
compression or viewport movement does not rewrite topology. Keep retained columns
recoverable in a bounded viewport without requiring the later horizontal
compression policy.

### Boundaries and Sequencing

Build on PRs 10–12 collection activation, row selection, and vertical occurrence
realization. For delivery on the current branch, preserve the PR 16 vertical
compression substrate already present; its pending manual verification remains a
separate delivery check.

This PR implements retained **vertical** alternatives. Singular traversal and
horizontal alternative insertion remain subsequent horizontal-navigation work.
Do not add branch-closing or re-rooting controls, persistent navigation sessions,
editing semantics, or a general graph-layout engine. The topology and projection
must preserve the grammar's two-axis invariants without requiring those features.

### Acceptance Criteria

- A person can inspect several members in sequence; replacing an untraversed leaf
  preserves the source Node, open Collection, and correct selected-row state.
- Given a vertical path A → B → C, activating another member D from A retains B
  and C in a new column immediately to the right, with D below A in A's column.
  B and C retain their occurrence identities, local state, and original provenance.
- Repeated alternatives insert additional columns and shift existing columns
  without collisions, lost descendants, or false lineage. A nested alternative
  uses its own anchor's current column, including when that anchor was displaced.
- A child that has been traversed onward cannot become replaceable merely because
  its visible collection tab or local presentation later changes.
- Tab changes alone neither create branches nor discard retained paths; subsequent
  member activation records the actual source collection and affordance.
- The same semantic Holon can appear in distinct occurrences with independent
  provenance; sparse cells are not selectable occurrences.
- Retained occurrences can be restored and traversed further. Focus, compression,
  and viewport movement preserve their attachment and state, and whole-row and
  whole-column allocations remain consistent after insertion.
- Failed or stale asynchronous realization does not remove or displace the existing
  continuation; successful realization publishes the new alternative coherently.
- Automated topology/projection and selected-visualizer interaction tests cover
  leaf replacement, retained insertion, repeated and nested alternatives, tab
  changes, provenance stability, and failure recovery. Manual verification covers
  sibling exploration and retained-path recovery with PR 16 compression in a
  constrained viewport.

---

# 6. Phase 3 — Horizontal Navigation and Provenance Geometry

---

## PR 14 — First Singular Relationship Child

**Planned Dev Points:** 5 (revised from 3 to include retained horizontal alternatives)

### Goal

Activate singular relationship navigation to the right, including switching among
singular affordances without losing traversed history, according to the authoritative
[Path Inspector Interaction Grammar](path-inspector-grammar.md) v0.2, especially
§§2.2–2.4 and §§3.3–3.8.

### Scope

For max-cardinality-one relationships:

- activate a right-rail entry and retrieve its target lazily;
- select/resolve the target Node Visualizer through the normal selection path;
- display a distinct child occurrence to the right and retain its source;
- record source occurrence, relationship affordance, and horizontal traversal provenance;
- allow another singular selection to replace the canonical right-hand child only
  while that child remains an untraversed leaf;
- once navigation has continued through that child, retain it and its continuation:
  place the new alternative in the anchor's current row, displace the prior traversed
  horizontal continuation into a newly inserted row immediately below, and shift
  pre-existing rows below as necessary;
- preserve occurrence and Holon identities, local state, provenance, and descendant
  attachment throughout insertion, including descendants reached vertically;
- keep retained occurrences recoverable and usable through existing navigation
  capabilities, with the newly activated child becoming the focus.

The retention rule applies when onward traversal is vertical as well as horizontal.
Do not reject an otherwise valid alternative merely because the existing child has
been traversed. Changing local collection presentation does not erase traversed
history or make an occurrence replaceable again.

### Geometry

The first child SHOULD receive the same canonical full Node dimensions as its source
where available. No child width is consumed before rail activation.

Keep topology separate from sparse grid projection. Columns preserve vertical paths;
rows preserve horizontal paths. Insertion may change coordinates but MUST NOT change
identity, provenance, or descendant attachment. Sparse cells remain valid and carry
no occurrence identity. Insertion alone does not change the current row focus; a
successful traversal focuses its new child in the anchor's row.

Integrate with the delivered retained vertical alternatives and whole-row compression
substrate. All cells in a row share its height and all cells in a column share its
width. Retained paths remain recoverable in the bounded viewport without requiring
the later horizontal compression policy.

### Boundaries and Sequencing

Build on PRs 9–13 classification, collection interaction, occurrence realization and
retained vertical alternatives, preserving the PR 16 compression substrate already
present. This PR owns retained horizontal alternative insertion; it is not deferred
to PR 15. PR 15 remains responsible for recursive horizontal traversal. Existing
vertical capabilities must continue to work for horizontally reached occurrences.

Do not add horizontal compression, re-rooting or branch-closing controls, persistent
sessions, relationship editing, or a general graph-layout engine.

### Acceptance Criteria

- Singular relationship navigation opens rightward through normal Node Visualizer
  selection and realization; runtime population does not alter singular classification.
- Switching singular affordances replaces an untraversed leaf while retaining the
  source occurrence and its local context.
- Given a right-hand child B of A that has been traversed onward, selecting another
  singular target D from A retains B and its descendants. D occupies the canonical
  right-hand position in A's row; B's retained horizontal continuation is displaced
  into a newly inserted row below, with pre-existing lower rows shifted as required.
- The same retention rule holds when B was traversed vertically. Its descendants
  retain their attachment, occurrence IDs, semantic identities, state and provenance.
- Repeated alternatives and alternatives from displaced anchors preserve both axes
  without collisions, lost descendants, or false lineage. Tab changes alone neither
  create alternatives nor make traversed children replaceable.
- Retained occurrences remain recoverable and usable; focus, compression, resizing
  and viewport movement preserve topology and consistent row/column allocations.
- Failed or stale asynchronous realization neither replaces a child nor displaces
  existing paths; successful realization publishes the new alternative coherently.
- Automated navigation/projection and selected-artifact tests cover leaf replacement,
  retained row insertion, repeated alternatives, displaced anchors, mixed vertical
  descendants, provenance stability, and failure recovery. Manual verification covers
  switching and retained-path recovery in a constrained viewport with compression.

### Milestone

At this point the fundamental two-dimensional grammar exists:

- plural goes down;
- singular goes right;
- untraversed leaves may be replaced; traversed paths are displaced and retained.

---

## PR 15 — Recursive Horizontal Navigation

**Planned Dev Points:** 3

### Goal

Permit continued traversal to the right.

### Scope

A right-side child may itself:

- expose its rail;
- open another child;
- expose its own collection tabs.

Extend occurrence/provenance state to represent a horizontal chain.

### Acceptance Criteria

- A → B → C works.
- Each occurrence retains distinct provenance.
- A horizontally reached node can still navigate vertically.
- Semantic identity and occurrence identity remain separate.

---

## PR 16 — Vertical Compression

**Planned Dev Points:** 3

### Goal

Introduce Y-axis compression.

### Scope

Allow a Node occurrence to relinquish vertical space while preserving:

- compact identity;
- relevant active Collection Tab;
- active collection context where appropriate;
- restoration.

Prefer simple deterministic/manual compression over sophisticated adaptive rules.

### Acceptance Criteria

- Node can enter and leave Y-compressed state.
- Collection context needed for sibling exploration remains usable.
- Navigation state survives compression.
- Expanded subordinate geometry respects the compressed parent allocation.

---

## PR 17 — Horizontal Compression

**Planned Dev Points:** 3

### Goal

Introduce X-axis compression.

### Scope

Allow prior horizontal ancestors to relinquish width.

Preserve:

- compact identity;
- relevant singular-navigation context;
- recoverable Node state;
- recoverable collection state.

Any subordinate collection owned by the compressed Node must relinquish the same horizontal real estate.

### Acceptance Criteria

- A prior Node can compress to a narrow vertical representation.
- Continued rightward traversal does not require deleting prior provenance.
- Re-expansion restores context.
- Subordinate content does not retain full old width.

---

## PR 18 — Orthogonal Two-Axis Compression

**Planned Dev Points:** 3

### Goal

Allow X and Y compression to compose.

### Scope

Support conceptual states:

| State | Width | Height |
| --- | --- | --- |
| Full | full | full |
| X-compressed | narrow | full-ish |
| Y-compressed | full-ish | short |
| XY-compressed | narrow | short |

### Acceptance Criteria

- X and Y state are independently representable.
- Applying both produces a compact provenance cell.
- Selected affordances and child links survive.
- Restoration recovers prior local state.
- Compression hides presentation, not state.

---

# 7. Phase 4 — Read-Only Collection Refinement

---

## PR 19 — Collection Sorting

**Planned Dev Points:** 2

### Goal

Add the first collection-view operation.

### Scope

Support:

- column-oriented sorting under Design Specification §§19.4–19.6;
- descriptor-backed Key defaults, including concrete keyed members of broadly typed collections such as Owns;
- table defaults for unordered collections: Key ascending for keyed element/member HolonTypes, otherwise supplied order;
- ascending/descending state;
- preservation within the Collection Visualizer occurrence.

### Acceptance Criteria

- Sort state is visible and persistent within the occurrence.
- Switching tabs and returning restores sort state.
- Compression does not destroy sort state.
- Typed comparisons, missing values, stable ties, header gestures, and sort indicators conform to §19.4.
- Manual-order occurrence metadata and the Sequence column are deferred from this PR. Ordered collections remain readable and may use explicit property-column sorting; indicate unavailable manual order rather than fabricate positions.
- Unordered keyed holon collections default to Key ascending, including Owns with a broad keyless declared target and concrete keyed member types; keyless/scalar fallbacks retain supplied order. The intended Sequence-first default in the design specification requires the deferred occurrence-metadata work.
- Descriptor policy determines ordered/keyed classification; incidental row order and display labels do not.
- A valid saved sort overrides the table default; a missing/ineligible saved column restores the applicable default.
- SDK descriptor reads reuse the existing command/reference boundary, including `RelationshipDescriptorHandle.isOrdered()` backed by Rust `RelationshipDescriptor::is_ordered()`. Authoritative per-occurrence sequence exposure is a follow-up prerequisite for manual-order support; display indices cannot substitute.

---

## PR 20 — Collection Filtering

**Planned Dev Points:** 3

### Goal

Add column-level filtering.

### Scope

Support:

- basic filters;
- clear filter;
- filter-state preservation;
- composition with sorting.

### Acceptance Criteria

- Filtering changes displayed membership without changing semantic collection cardinality.
- Filter state survives ordinary navigation/compression.
- Sorting and filtering compose predictably.

---

# 8. Phase 5 — Adaptive Ordering and Visualizer Choice

This phase proves the DAHN adaptive seam without yet requiring full collective salience or Visualizer Commons discovery.

---

## PR 21 — Presentation Ordering from Rust

**Planned Dev Points:** 3

### Goal

Allow Rust to provide initial adaptive presentation ordering.

### Scope

Extend DAHN presentation context with ordering for some or all of:

- properties;
- singular rail entries;
- collection tabs;
- actions.

Initial ordering may remain deterministic/default.

The important requirement is that TypeScript consumes ordering supplied through the Rust-side boundary.

### Acceptance Criteria

- Generic Node presentation does not assume descriptor declaration order is always presentation order.
- Rust can return explicit ordering.
- TypeScript respects that ordering.

---

## PR 22 — Local Reordering and Adaptive Gesture Events

**Planned Dev Points:** 3

### Goal

Allow the person to personalize visible ordering and report the gesture semantically.

### Scope

Initially support reordering of one or more of:

- properties;
- collection tabs;
- singular rail entries.

On reorder:

1. update TypeScript presentation immediately;
2. emit a semantic adaptive gesture through the MAP adapter.

Persistent scoring may initially be minimal.

### Acceptance Criteria

- UI reorders without waiting for an IPC round trip.
- A semantic adaptive event reaches Rust.
- Local visual state reflects the person's choice.
- Presentation code does not implement aggregate salience itself.

---

## PR 23 — Alternate Visualizer Selection

**Planned Dev Points:** 3

### Goal

Prove explicit visualizer choice as an adaptive interaction.

### Scope

When Rust reports alternate applicable visualizers:

- advertise alternatives;
- allow selection of another locally resolvable visualizer;
- preserve the occurrence and navigation context where possible;
- emit a visualizer-preference signal.

The candidate set may initially be only core/local visualizers.

### Acceptance Criteria

- Visualizer replacement does not require replacing the semantic subject.
- Selection routes through Rust and updates the occurrence's selected Visualizer
  Holon reference.
- Explicit selection emits an adaptive signal.
- A new explicit selection request may be made; no fallback is implied.

---

# 9. Phase 6 — Staged Editing Foundation

---

## PR 24 — Edit Existing Holon: Scalar Properties

**Planned Dev Points:** 5

### Goal

Introduce staged edit mode while preserving the existing Node occurrence.

### Scope

Add holon-scoped **Edit** action.

On Edit:

- invoke Rust staging for the current holon;
- keep the same visualizer occurrence;
- enter edit mode;
- render eligible scalar properties through editable Value Visualizers;
- update staged property values through MAP operations.

Do not yet implement Commit.

### Acceptance Criteria

- Edit is a state transition, not navigation.
- Staged semantic state remains Rust-owned.
- Eligible scalar properties can be changed.
- Read-only properties remain read-only.
- Navigation still works while editing.
- Compression does not discard staged state.

---

## PR 25 — Dancer Transaction Status and Action State

**Planned Dev Points:** 3

### Goal

Make the active transaction visible at Canvas scope.

### Scope

Activate the pinned Space Navigator Action Bar against actual Rust transaction
state. Introduce the corresponding Dancer-scoped Action Visualizer states needed to
present this newly available transaction information.

Expose enough state for presentation of:

- transaction active/inactive;
- staged changes present;
- Commit availability placeholder;
- Undo/Redo availability placeholders.

Commit and Undo/Redo behavior are implemented in subsequent PRs.

### Acceptance Criteria

- Transaction state is not inferred separately by each Node.
- Editing one holon causes Space Navigator transaction state to update.
- Space Navigator Action Bar is the owner of transaction-scoped controls.
- Node Action Bar does not expose Commit.
- Transaction presentation is rendered through Dancer-scoped Action
  Visualizers rather than Canvas-specific button implementations.

---

## PR 26 — Meaningful Undo Boundaries

**Planned Dev Points:** 3

### Goal

Connect editing gestures to Rust transaction snapshot markers.

### Scope

For scalar property editing:

- determine an initial meaningful gesture-completion boundary;
- instruct Rust to establish an Undo marker;
- keep preservation snapshots conceptually separate from user-visible Undo boundaries.

### Acceptance Criteria

- One completed scalar edit can become one Undo step.
- TypeScript determines the UX boundary.
- Rust stores/restores semantic snapshot state.
- TypeScript does not maintain an independent semantic command history.

---

## PR 27 — Space Navigator Undo

**Planned Dev Points:** 3

### Goal

Expose semantic Undo from the pinned Space Navigator Action Bar.

### Scope

Implement:

- enabled/disabled state;
- request to Rust;
- restoration of prior staged transaction snapshot;
- refresh of affected visualizers.

### Acceptance Criteria

- Undo affects staged MAP state, not merely UI control state.
- Affected Node occurrences refresh from restored semantic state.
- Navigation geometry remains intact.
- Undo is not repeated in Node Action Bars.

---

## PR 28 — Space Navigator Redo

**Planned Dev Points:** 2

### Goal

Complete transaction history traversal.

### Scope

Implement:

- Redo availability;
- Rust roll-forward;
- affected presentation refresh.

### Acceptance Criteria

- Undo followed by Redo restores the semantic staged state.
- Redo uses the Space Navigator Action Bar.
- TypeScript does not reconstruct Redo locally.

---

## PR 29 — Space Navigator Transaction Commit

**Planned Dev Points:** 5

### Goal

Complete the first staged update lifecycle.

### Scope

Implement transaction-wide Commit from the Space Navigator Action Bar.

Commit flow:

- validate transaction;
- execute MAP Commit;
- return success/failure;
- refresh affected occurrences.

On success:

- affected visualizers return to read mode;
- navigation provenance remains intact.

On failure:

- transaction remains staged;
- affected visualizers remain editable;
- validation/commit errors remain visible.

### Acceptance Criteria

- Commit is not tied to one Node Visualizer.
- One edited holon can be successfully committed.
- Failed Commit does not discard staged state.
- Successful Commit refreshes committed values.
- Continuous preservation remains distinct from explicit Commit.

### Milestone

This completes the first full read/write flow:

    inspect
      |
    edit staged state
      |
    Undo / Redo
      |
    Space Navigator Commit
      |
    inspect committed state

---

# 10. Phase 7 — Multi-Holon Transaction Capability

---

## PR 30 — Edit Multiple Existing Holons in One Transaction

**Planned Dev Points:** 3

### Goal

Prove that the Space Navigator transaction is broader than one visualizer.

### Scope

Allow:

- edit A;
- navigate elsewhere;
- edit B;
- retain both staged changes in the same active transaction.

Ensure both occurrences are reflected in transaction presentation state.

### Acceptance Criteria

- A and B can both be staged concurrently.
- There is still one Space Navigator transaction Commit.
- Undo/Redo operate on the shared transaction history.
- Navigation away from A does not discard A's staged changes.
- TypeScript does not create independent transaction contexts per Node.

---

## PR 31 — Commit Multiple Updated Holons

**Planned Dev Points:** 3

### Goal

Prove multi-holon Commit end-to-end.

### Scope

Commit a transaction containing staged changes to multiple existing holons.

### Acceptance Criteria

- Full transaction validates together.
- Successful Commit refreshes all affected visible occurrences.
- Failure leaves the shared staged transaction intact.
- Transaction status clears only after successful completion according to MAP semantics.

---

## PR 32 — Multiple Occurrences of One Staged Holon

**Planned Dev Points:** 5

### Goal

Prevent semantic divergence when one staged holon is visible more than once.

### Scope

Handle:

- same semantic holon displayed through multiple traversal paths;
- one occurrence enters edit mode;
- another occurrence remains visible.

Define an initial presentation synchronization policy.

### Architectural Invariant

There is one authoritative staged semantic state in Rust.

### Acceptance Criteria

- TypeScript does not create independent staged semantic copies.
- Visible occurrences cannot silently diverge semantically.
- Refresh after edit/Undo/Redo/Commit keeps occurrences coherent.
- Occurrence-specific presentation state remains independent.

---

# 11. Phase 8 — Create, Clone, and Delete

---

## PR 33 — Clone Holon

**Planned Dev Points:** 3

### Goal

Initialize new staged state from an existing holon.

### Scope

Add **Clone** as a holon-scoped action.

Clone:

- creates a distinct staged holon;
- initializes it from the source according to MAP semantics;
- opens it in normal editable Node presentation;
- joins the active transaction.

### Acceptance Criteria

- Clone has a distinct semantic identity.
- No clone-specific editor is introduced.
- Clone source does not automatically become navigation provenance.
- Space Navigator transaction Commit publishes the clone.

---

## PR 34 — Create Instance from Concrete Type

**Planned Dev Points:** 3

### Goal

Provide generic type-driven creation.

### Scope

When viewing an applicable concrete Holon Type descriptor:

- expose **Create Instance**;
- stage a new holon in the active Space;
- apply defaults;
- present it through ordinary editable Node Visualizer behavior;
- join the active transaction.

### Acceptance Criteria

- Creation is descriptor-driven.
- No type-specific creation form is required.
- New holon can coexist with other staged changes.
- Space Navigator Commit publishes it.

---

## PR 35 — Stage Delete

**Planned Dev Points:** 3

### Goal

Add semantic deletion as a transaction participant.

### Scope

Add **Delete** at holon scope where permitted.

Support:

- explicit confirmation;
- staged deletion state;
- Space Navigator transaction inclusion;
- appropriate staged visual indication.

### Acceptance Criteria

- Delete does not immediately bypass the active transaction.
- Historical erasure is not implied.
- Deletion can coexist with other staged changes.
- Commit publishes deletion according to MAP semantics.
- Undo can restore staged state before Commit where supported by existing transaction semantics.

---

# 12. Phase 9 — Editable Collections and Relationships

---

## PR 36 — Editable Value Arrays

**Planned Dev Points:** 5

### Goal

Extend staged editing into array-valued properties.

### Scope

For mutable arrays:

- add value;
- remove value;
- edit value;
- reorder where allowed.

Reuse the existing Collection Visualizer.

Use Value Visualizers for individual element editing.

Establish suitable Undo boundaries.

### Acceptance Criteria

- No separate array-editing form exists.
- Mutation updates Rust-owned staged state.
- Undo/Redo covers array changes.
- Compression preserves staged presentation state.
- Space Navigator Commit publishes changes.

---

## PR 37 — Generic Relationship Target Selection

**Planned Dev Points:** 3

### Goal

Introduce the minimal reusable mechanism needed to choose a relationship target.

### Scope

Provide a simple generic selector suitable for:

- setting singular relationship targets;
- adding plural relationship targets.

Keep the first implementation intentionally narrow.

### Non-Goals

Do not build a generalized rich search/navigation subsystem unless required.

### Acceptance Criteria

- A valid target can be selected generically.
- Selection returns semantic holon reference.
- Selector is reusable by singular and plural relationship editing.
- Target-selection UI does not own relationship mutation semantics.

---

## PR 38 — Editable Multi-Valued Relationships

**Planned Dev Points:** 3

### Goal

Allow relationship membership mutation through Collection Visualizers.

### Scope

For mutable plural relationships:

- add target;
- remove target;
- reuse the generic target selector;
- preserve normal collection navigation;
- respect descriptor constraints.

### Acceptance Criteria

- Relationship membership edits source holon staged state.
- Target properties are not implicitly edited.
- Undo/Redo covers membership changes.
- Space Navigator Commit publishes changes.

---

## PR 39 — Editable Single-Valued Relationships

**Planned Dev Points:** 3

### Goal

Add set/replace/clear semantics to singular relationship affordances.

### Scope

For mutable singular relationships:

- set target;
- replace target;
- clear target;
- continue ordinary rightward navigation.

### Acceptance Criteria

- Relationship remains structurally singular.
- Empty state remains represented.
- Target editing is distinct from target-holon editing.
- Undo/Redo works.
- Space Navigator Commit publishes the change.

---

# 13. Phase 10 — Dances

---

## PR 40 — Effective Dance Actions

**Planned Dev Points:** 5

### Goal

Populate Node actions from effective available dances.

### Scope

Support:

- directly declared dances;
- inherited dances;
- effective permission/role filtering;
- generic Action Visualizer presentation;
- invocation plumbing.

Result rendering may initially be limited.

### Acceptance Criteria

- Raw type hierarchy is not blindly displayed.
- Effective available dances drive actions.
- Node does not need domain-specific action code.
- Dance invocation goes through existing semantic MAP operations.

---

## PR 40.a — Space Navigator Load Holons Action and Legacy-App Retirement

**Planned Dev Points:** 5

### Goal

Make `LoadHolons` available from the Space Navigator's pinned Action
Bar, then retire the separate Load Holons application after the replacement is
functionally complete.

### Scope

Add a Canvas-scoped `Load Holons` Action Visualizer and its request flow.
The flow MUST:

- identify the active `HolonSpace` as the affording holon;
- construct the canonical `HolonLoadSet` request from the selected host-ingress
  source;
- invoke the canonical `LoadHolons` Dance rather than a legacy raw-file
  Command ingress;
- present loading, success, and failure outcomes in the Space Navigator Action Bar or
  its scoped transient surface; and
- refresh the Space Navigator through normal MAP-backed inspection after a
  successful load.

The file/source picker is host ingress only. It does not define a second
semantic loading protocol or receive authority to mutate the Space directly.

After this flow is accepted, remove the existing Load Holons app's entry point,
routing, and duplicated presentation. Preserve any reusable host-ingress code
only when it is used by the Canvas action.

### Non-Goals

Do not create a Node-scoped Load action, duplicate `LoadHolons` as a new
Space Navigator Dance, or introduce an app-to-app compatibility bridge.

### Acceptance Criteria

- `Load Holons` is discoverable at Canvas scope and is not repeated on Nodes.
- The action invokes `LoadHolons` with the active `HolonSpace` as its affording
  holon and a request conforming to `HolonLoadSet`.
- Loading and failure states are visible without leaving the Canvas.
- A successful response makes the loaded semantic state available to normal
  Space Navigator inspection.
- The former Load Holons app is retired only after the Canvas action provides
  the equivalent user-facing load capability.

---

## PR 41 — Single-Holon Dance Results

**Planned Dev Points:** 3

### Goal

Route singular dance results into the existing rightward navigation grammar.

### Scope

For a dance whose response descriptor declares one holon:

- invoke;
- receive target;
- create/select Node occurrence to the right;
- record dance-result provenance.

### Acceptance Criteria

- Result shape is known from descriptor before execution.
- Normal Node selection/runtime resolution is reused.
- No special dance-result panel is introduced.

---

## PR 42 — Collection Dance Results

**Planned Dev Points:** 3

### Goal

Route plural dance results through Collection Visualizers.

### Scope

Support:

- holon collections;
- homogeneous value collections.

Expose using the existing Collection Tab / Collection Visualizer grammar.

### Acceptance Criteria

- No separate dance-result table implementation exists.
- Sorting/filtering apply where appropriate.
- Collection visualizer selection is reused.
- Provenance identifies dance result source.

---

## PR 43 — Scalar and No-Result Dances

**Planned Dev Points:** 5

### Goal

Complete the initial dance-result matrix.

### Scope

First resolve the open design decision for scalar results, then implement:

- scalar result presentation;
- no-result execution feedback.

### Acceptance Criteria

- Behavior is consistent with the finalized design specification.
- Neither result form requires a parallel visual architecture.

---

# 14. Phase 11 — Action Personalization

---

## PR 44 — Reorder Node Actions

**Planned Dev Points:** 2

### Goal

Extend adaptive ordering into Node action presentation.

### Scope

Allow permitted actions to be reordered.

On gesture:

- update presentation immediately;
- report adaptive event to Rust.

### Acceptance Criteria

- Immediate action order changes locally.
- Adaptive meaning is persisted through Rust boundary.
- Action behavior remains unchanged by presentation order.

---

## PR 45 — Space Navigator Action Personalization

**Planned Dev Points:** 2

### Goal

Apply the same adaptive principles to the pinned Space Navigator Action Bar.

### Scope

Where permitted, support changes to:

- ordering;
- prominence;
- overflow position.

### Acceptance Criteria

- Canvas retains ownership of its standard action set.
- User customization changes presentation rather than transaction semantics.
- Adaptive signals cross the normal Rust boundary.

---

# 15. Phase 12 — Visualizer Commons and Adaptive Selection Expansion

These PRs may occur later than the core Space Navigator release if the current milestone is focused on proving generic local visualizers first.

---

## PR 46 — Accessible Visualizer Commons Discovery

**Planned Dev Points:** 5

### Goal

Replace the fallback-only candidate source with federated MAP-native discovery.

### Scope

Discover Visualizer Commons reachable through applicable Space relationships.

Return eligible Visualizer Holons as candidate inputs to the Rust Selector.

### Acceptance Criteria

- Candidate population is not a centralized MAP-team registry.
- Accessible Commons are resolved through MAP semantics.
- TypeScript does not retrieve the full ecosystem simply to make selection decisions.

---

## PR 47 — Semantic Applicability over Discovered Visualizers

**Planned Dev Points:** 3

### Goal

Filter discovered candidates by visualizer category and semantic applicability.

### Scope

Use Visualizer Holon types, relationships, and semantic applicability to identify
applicable candidates.

### Acceptance Criteria

- Applicability is descriptor/semantic driven.
- TypeScript implementation classes are not the source of applicability.
- No fallback selection is available.

---

## PR 48 — Personal Visualizer Preference

**Planned Dev Points:** 3

### Goal

Use prior explicit choices in Rust-side visualizer selection.

### Scope

Persist and apply a user's visualizer preference signals.

### Acceptance Criteria

- Explicit visualizer replacement can influence later selection.
- Personal state remains Rust/MAP-owned.
- TypeScript does not reproduce preference scoring.

---

## PR 49 — Initial Collective Salience

**Planned Dev Points:** 5

### Goal

Introduce the first aggregate adaptive signal into selection or ordering.

### Scope

Choose one narrow aggregate signal rather than implementing the full future salience model.

Examples:

- aggregate visualizer preference;
- aggregate property ordering.

### Acceptance Criteria

- Aggregate state influences a selection/order result.
- Personal and collective inputs remain distinguishable.
- The scoring model is testable and documented.

---

## PR 50 — Explore/Exploit Selection Controls

**Planned Dev Points:** 3

### Goal

Prove that selection policy can vary between familiarity/stability and novelty/discovery.

### Scope

Introduce initial selector policy inputs for a constrained subset such as:

- personal versus collective weight;
- maturity preference;
- novelty/randomness.

### Acceptance Criteria

- Selector behavior changes predictably with policy.
- Policy remains Rust-side.
- Individual visualizers do not implement explore/exploit logic.

---

# 16. Phase 13 — Navigation and Transaction Hardening

---

## PR 51 — Staged-State Indicators Through Compression

**Planned Dev Points:** 3

### Goal

Make staged state unmistakable in compressed provenance.

### Scope

For X-, Y-, and XY-compressed occurrences:

- indicate staged state;
- indicate staged deletion where applicable;
- restore full edit context on expansion.

### Acceptance Criteria

- Compression never conceals the existence of staged work.
- Indicator is driven from authoritative transaction/staged context.
- Expansion restores editable presentation.

---

## PR 52 — Branch Closing and Pruning

**Planned Dev Points:** 3

### Goal

Allow explicit removal of unneeded traversal context.

### Scope

Define and implement:

- close child;
- prune descendants;
- interaction with staged occurrences;
- interaction with collection state.

### Acceptance Criteria

- Closing presentation does not silently abandon staged semantic state.
- Remaining provenance stays coherent.
- Canvas can intentionally reclaim space.

---

## PR 53 — Transaction Abandon/Revert

**Planned Dev Points:** 5

### Goal

Resolve and implement the design's transaction-abandon semantics.

### Scope

After the Design Specification resolves the open question, implement the chosen transaction-wide behavior.

### Acceptance Criteria

- User-facing semantics are explicit.
- Staged work is never silently lost.
- Canvas and visible occurrences refresh coherently.
- Behavior is testable across multiple staged holons.

---

## PR 54 — Deleted Holon Presentation

**Planned Dev Points:** 3

### Goal

Finalize staged and committed deleted-state presentation.

### Scope

Implement the design decision for:

- staged deletion;
- post-Commit deleted holon appearance;
- existing provenance paths containing deleted holons.

### Acceptance Criteria

- Deleted state remains semantically clear.
- Provenance can remain coherent.
- History is not confused with physical erasure.

---

# 17. Recommended Milestones

## Milestone A — First Dynamic Read-Only Node

PRs 1–9 plus PRs 5.a-pre, 5.a, 5.b, and 5.b.1, after Schema Task S1.

Delivers:

- DAHN adapter;
- first-cut DAHN Visualizer schema and separately loadable Space Navigator
  House Troupe Visualizer Holons;
- Visualizer Runtime;
- Rust Selector boundary;
- theme foundation;
- MAP Application Launcher foundation (PR 5.a-pre);
- Collection Visualizer;
- generic Canvas shell (PR 5.a);
- Generic Node shell (PR 5.b);
- HolonSpace home-Dancer mount (PR 5.b.1);
- Properties, Property, and Value Visualizers;
- descriptor-driven affordance classification and generic Action Visualizers.

Result:

    semantic holon
         |
    Rust selects Node Visualizer Holon
         |
    TypeScript resolves compatible implementation
         |
    visible Canvas-hosted Dancer experience renders the generic node and its component
    visualizers

This proves the fundamental DAHN selection/composition seam before navigation becomes complex.

---

## Milestone B — First Useful Vertical Exploration

PRs 10–13.

Result:

    inspect holon
        |
    select plural affordance
        |
    inspect collection
        |
    select member
        |
    inspect child holon

This is the first meaningful user-facing Space Navigator loop.

---

## Milestone C — Two-Dimensional Space Navigator

PRs 14–18.

Result:

- singular traversal goes right;
- plural traversal goes down;
- occurrences preserve provenance;
- context compresses along both axes.

This delivers the first concrete applications of the Interaction Grammar; it
does not define alternate lineage or compression semantics.

---

## Milestone D — Read-Only Usability and Initial Adaptation

PRs 19–23.

Result:

- sorting;
- filtering;
- Rust-provided ordering;
- personal reordering gestures;
- alternate visualizer choice.

This proves that DAHN is not merely dynamic but begins to expose the adaptive architecture.

---

## Milestone E — First Complete Update Flow

PRs 24–29.

Result:

    inspect
      |
    Edit
      |
    staged scalar changes
      |
    Undo / Redo
      |
    Space Navigator Commit
      |
    inspect committed state

This is the first complete staged editing transaction.

---

## Milestone F — Multi-Holon Transaction

PRs 30–32.

Result:

    edit A
      |
    navigate
      |
    edit B
      |
    shared transaction
      |
    shared Undo / Redo
      |
    one Commit

This proves the Space Navigator transaction model rather than a conventional one-form/one-save workflow.

---

## Milestone G — Generic Lifecycle Operations

PRs 33–39.

Result:

- Clone;
- Create;
- Delete;
- editable arrays;
- editable singular relationships;
- editable plural relationships.

At this point the Space Navigator supports generic manipulation of MAP holons without introducing domain-specific forms.

---

## Milestone H — Full Initial Dance Integration

PRs 40, 40.a, and 41–43.

Result:

- effective dances;
- Canvas-scoped Load Holons;
- singular dance results;
- collection dance results;
- scalar/no-result behavior.

Dances now participate in the same visual grammar as properties and relationships.

---

## Milestone I — Adaptive Visualizer Ecosystem

PRs 44–50.

Result:

- adaptive action ordering;
- Visualizer Commons discovery;
- semantic applicability;
- personal visualizer preference;
- initial collective salience;
- explore/exploit selector behavior.

This begins exercising DAHN as an open federated adaptive ecosystem rather than only a locally bundled generic browser.

---

# 18. Capabilities Intentionally Deferred

The initial Space Navigator implementation does not require full solutions for:

- remote arbitrary visualizer-code execution;
- production sandboxing;
- package signing;
- generalized dependency isolation;
- rich third-party package acquisition;
- all collective salience rubrics;
- sophisticated selector explanations;
- every explore/exploit control;
- every theme;
- arbitrary free-form Canvas layout;
- persistent collaborative Canvas sessions;
- complete mobile layout;
- full keyboard navigation;
- unlimited simultaneous sibling branching.

These capabilities should remain architecturally possible without becoming prerequisites for the first useful Space Navigator.

---

# 19. Cross-PR Implementation Principles

## 19.1 Preserve Architectural Seams Early

Simple implementations are acceptable.

Bypassing the intended boundary because the first implementation is simple is not.

For example:

- fallback-only selection still goes through Rust Selector;
- locally bundled visualizers still resolve through Visualizer Holon or
  implementation references;
- one default theme still goes through theme tokens.

---

## 19.2 One Semantic Source of Truth

Do not duplicate authoritative MAP state into TypeScript.

This includes:

- staged holons;
- transaction state;
- Undo history;
- adaptive preference state.

---

## 19.3 One Experience Occurrence Model

Do not use holon identity as Canvas occurrence identity.

Navigation state belongs to visualizer occurrences.

---

## 19.4 One Node Grammar

Do not introduce separate Node implementations merely because a node was reached:

- horizontally;
- vertically;
- through a dance;
- through creation;
- through cloning.

Visualizer selection may choose a different semantic visualizer, but placement does not define a new category.

---

## 19.5 One Collection Grammar

Do not create separate collection frameworks for:

- arrays;
- relationships;
- dance results.

They converge on Collection Visualizers.

---

## 19.6 Read and Edit Share the Visual Tree

Do not introduce a separate form framework for editing.

Editing changes interaction mode and staged semantic state.

---

## 19.7 Commit Belongs to the Transaction

Do not add Commit buttons to individual Node Visualizers.

One Space Navigator transaction may contain changes to many holons.

---

## 19.8 Undo Is Semantic

Do not implement Undo by replaying TypeScript UI state.

TypeScript defines the boundary.

Rust owns the recoverable transaction snapshot.

---

## 19.9 Personalization Is Immediate; Learning Is Durable

TypeScript should make drag/reorder/select interactions feel immediate.

Rust should persist and interpret the adaptive signal.

---

## 19.10 Parent Owns Placement

Child visualizers emit semantic events.

The parent Canvas or visualizer determines placement.

---

## 19.11 Compression Preserves State

Compression may hide:

- properties;
- actions;
- collections;
- rails.

It MUST NOT silently destroy:

- provenance;
- selections;
- staged state;
- transaction participation.

---

## 19.12 Prefer Working Slices

New infrastructure should be introduced close to the PR that first exercises it through visible behavior.

Avoid constructing speculative generalized systems several phases before any use.

---

# 20. Overall Capability Progression

The intended progression is:

    DAHN MAP adapter
        |
    DAHN Visualizer schema and separately loadable House Troupe Holons
        |
    Visualizer implementation runtime
        |
    Rust Selector boundary
        |
    theme tokens
        |
    MAP Application Launcher foundation
        |
    generic Collection Visualizer (already delivered as PR 5)
        |
    generic Canvas shell
        |
    generic Node Visualizer
        |
    HolonSpace home-Dancer mount
        |
    generic Properties, Property, and Value Visualizers
        |
    descriptor-driven affordances and generic Action Visualizers
        |
    inspect plural collections
        |
    navigate down
        |
    navigate right
        |
    compress provenance
        |
    sort / filter
        |
    adaptive ordering
        |
    explicit visualizer choice
        |
    edit staged scalar values
        |
    Space Navigator transaction state
        |
    Undo / Redo
        |
    Space Navigator Commit
        |
    edit multiple holons
        |
    Clone / Create / Delete
        |
    edit arrays and relationships
        |
    invoke dances
        |
    load holons from Canvas scope
        |
    personalize actions
        |
    discover Visualizer Commons
        |
    adaptive federated selection
        |
    harden navigation and transactions

Each increment extends the same architecture and visual grammar rather than replacing it.

---

# 21. Handoff to GitHub Issues

Each PR section in this plan is intended to become a separate GitHub enhancement issue.

When generating those issues, each issue SHOULD:

- link to the relevant Architecture Specification section;
- link to the relevant Design Specification section;
- state the narrow behavioral goal;
- state explicit non-goals;
- identify upstream PR dependencies;
- include acceptance criteria;
- avoid re-specifying architectural decisions already owned by the source specifications.

The issue should answer:

> What increment are we implementing now?

The Architecture and Design Specifications should continue to answer:

> Why is the system structured this way, and what behavior is required?


## Phase 4 — Slot-directed Visualizer selection correction

Align implementation with DAHN §13.2.1. Carry the actual slot through SDK, wire
binding and Rust selection. Validate parent-slot ownership when supplied. Read
accepted types from the slot instead of resolving a redundant requested-role key;
remove the post-selection scan of all parent slots. Stop applicability search at
the nearest local TKD, reporting missing matches and ambiguity explicitly.

Rename the property-map type, default instance, owned slots and references;
mark AcceptsVisualizerType definitional and regenerate schema bundles. Audit
fallback applicability at newly enforced TKD boundaries. Tests cover leaf
precedence, accepted-type inheritance, wrong-kind candidates, ambiguity, TKD
exhaustion, ownership, and no canonical role lookup. Keep Canvas launch and the
specialized collection-subject contract intact. Re-profile the same traversal.
