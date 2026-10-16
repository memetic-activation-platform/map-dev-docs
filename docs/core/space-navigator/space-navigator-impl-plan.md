# DAHN Space Navigator Implementation Plan v1.6

## Status

The [four-mode inspector geometry review](inspector-geometry-review.md) proposes
a simplification of §22. Its per-axis retention, local view switching,
remembered restoration, loader default and Properties-header decisions are accepted
individually. Coordinated owning-spec edits are in the unmerged review draft;
implementation and enhancement issues still wait for consolidated acceptance.


The [bounded composition refactor](#22-bounded-visualizer-composition-refactor)
is a documentation proposal for review, not delivered work. It supersedes the
rendered-extent negotiation portions of older slices without changing their
historical delivery records or estimates. Runtime work and issue creation wait
for this design to be accepted and merged.


Phase 3 is delivered (project-owner confirmation, 2026-09-28). Phase 3A is the next planned increment for the newly clarified DAHN composition/view contracts. This document does not treat the newly added slices as delivered.

Integrated delivery plan using the [DAHN foundation roadmap](../hx/dahn-implementation-plan.md)
and the concern-specific authorities linked on each slice. Delivery status is
the existing recorded baseline, not a fresh code or GitHub issue audit.

This plan supersedes the earlier Space Navigator implementation plan.

## Change Log

| Version | Changes from prior version |
| --- | --- |
| v1.6 | Adds bounded Operator/allocation and shared inspector increments, with explicit supersession of rendered-content sizing and review decisions. |
| v1.5 | Resolves PR23f discovery-evidence, Inspector-owned slot, state-survival, nested lifecycle and technical-placement decisions; keeps performance and broader real-estate work deferred. |
| v1.4 | Replaces historical PR 23 with PRs 23.a–23.f for the Visualizer icon, multi-level inspector, authoritative discovery, usage selection, safe explicit choice, and recursive ancestry explorer; records new planned estimates and design gates. |
| v1.3 | Maps every slice to owning components, specification authority and dependencies; preserves identifiers, historical estimates and recorded status; reconciles retired Property selection and defers F1 schema work. |
| v1.2 | Reconciles delivery through Phase 3; moves new foundation work into Phase 3A (PRs 18.a–18.e), starting with surface/view separation against the delivered navigator. |
| v1.1 | Separates reusable DAHN foundation from Space Navigator delivery; sequences Window Manager contexts, surface/view state, participation negotiation, close branch, and non-destructive re-root through the existing slices. Preserves Path Inspector ownership of rooted navigation. |
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

Architectural decisions belong in [DAHN Architecture](../hx/dahn-arch.md).
The v0.4 baseline listed above is historical; current contracts use its canonical
successor and the DAHN design specification.

Reusable composition belongs to [DAHN design](../hx/dahn-design-spec.md).
Dancer contracts belong to [Space Navigator](space-navigator-interaction-grammar.md).
Rooted-navigation productions belong to [Path Inspector](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md).

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
- Window Manager ownership of top-level contexts and display allocation;
- parent-owned layout allocation within each grant;
- distinct topology, layout/surface, and view-transform state;
- slot Operator participation and explicit policy-extent seams;
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
- the initial Path Inspector layout may use explicit profile dimensions validated against retained-capability requirements;
- the initial Window Manager may use one active context with context switching, before richer placement policies.

The seam matters before the sophisticated implementation behind it does.

---

## 1.1 Foundation and First Application

This delivery has two products: reusable DAHN contracts/infrastructure and the first Space Navigator Dancer with its selected Visualizer set. Path Inspector remains a reusable concrete RootedNavigation Visualizer, not behavior built into the generic Canvas or Dancer.

| Reusable DAHN foundation | First Space Navigator / Visualizer application | Delivery |
| --- | --- | --- |
| Window Manager/context lifecycle and bounded Canvas grants | Home Dancer hosting and bounded experience allocation | PR 18.b, PR 5.a, PR 5.b.1 |
| Parent allocation and slot Operator participation | Node/Holon Inspector internal composition and minimum useful extent | PR 18.a, integrating delivered PRs 5.b/12 |
| Surface/viewport and independent view-transform state | Path Inspector navigation surface, grid and lineage | PR 18.a, preserving delivered PRs 12–18 |
| Bounded focus/maximize request propagation | Local region maximize and occurrence attention | PR 18.c |
| State-survival contracts and semantic ownership | Branch closing, re-root, staged-state recovery | PR 18.d, PR 18.e, PRs 25/32/52 |
| Extensible slot applicability/context contracts | First concrete Node/Collection participation obligations | PR 18.a on existing selection/slot seams; PR 47 extends discovery |

Extract/generalize contracts that are clear; keep speculative schema dimensions as extension seams. Do not require a generalized Window Manager ecosystem, every Canvas form, or a final slot schema before shipping the first useful experience. New slices below require issue-grounded sizing; existing Dev Points are historical planning estimates and must be revisited where scope changes.

## 1.2 Migration and Dependency Order

Phase 3 is already delivered. Preserve PRs 1–18 as the baseline and implement the newly clarified contracts in **Phase 3A**, before resuming Phase 4 collection refinement. References to earlier slices identify integration points, not outstanding prerequisites or retroactive acceptance criteria.

1. **PR 18.a — Surface View Transform and Recovery:** separate topology, layout/allocation, and view state in the existing navigation implementation; use explicit useful policy extents and surface growth, pan/zoom, Zoom to Fit, and actual-size recovery. Audit clipping-only `overflowed` state separately from real layout overflow.
2. **PR 18.b — Minimal Window Manager Context Host:** extract top-level context/display authority around the existing Canvas, initially preserving the current single-context experience. Keep launcher startup separate.
3. **PR 18.c — Bounded Focus and Maximize Requests:** exercise local, Canvas, and Window Manager authority through distinct request paths.
4. **PR 18.d — Close Navigation Branch:** implement occurrence-based pruning and focus recovery with semantic-state survival checks.
5. **PR 18.e — Re-root into a New Experiential Context:** retain at least two exploration tabs under one Space Navigator, sharing its read transaction and routing each semantic anchor through its RootedNavigation slot.

PRs 25 and 32 later integrate staged-state ownership with these operations. PR 52 hardens branch removal under transactions rather than introducing it. Transaction policy across exploration tabs must be settled before editing integration; it does not block the read-only Phase 3A work.

Use the grammars as behavioral authority; the plan records implementation deltas and tests, not a second rule set.

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
- collection row interaction plus Path Inspector traversal plus compression;
- staging plus Undo plus Commit;
- relationship editing plus a sophisticated target-search UX;
- adaptive gesture recording plus collective salience aggregation.

## 2.1 Planned Dev Point Estimates

Existing PR estimates use the MAP Dev Points rubric; newly inserted slices await issue-grounded estimates:
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

**Capability owners and design authority:** [SDK](../hx/dahn-arch.md), [DAHN](../hx/dahn-design-spec.md).

**Integration prerequisites:** Public SDK descriptor/access seams. Existing detailed dependencies below still apply.

**Recorded status:** Recorded delivered baseline through Phase 3.

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

**Capability owners and design authority:** [Schema](../hx/dahn-design-spec.md#11-visualizerslot), [DAHN](../hx/dahn-design-spec.md).

**Integration prerequisites:** Current DAHN type/slot design; F1 extensions deferred. Existing detailed dependencies below still apply.

**Recorded status:** Recorded delivered baseline through Phase 3.

**Planned Dev Points:** 5

### Goal

Define the minimal MAP-native DAHN schema in `map-holons` before the Space
Navigator introduces runtime visualizer resolution or Rust-side selection.

### Scope

Author the schema source of truth and its bootstrap resources for:

- the abstract `Visualizer` type-family anchor;
- concrete `CanvasVisualizer`, `NodeVisualizer`, `CollectionVisualizer`,
  `PropertyMapVisualizer`, `ValueVisualizer`,
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

**Capability owners and design authority:** [DAHN](../hx/dahn-design-spec.md).

**Integration prerequisites:** S1 and public SDK access. Existing detailed dependencies below still apply.

**Recorded status:** Recorded delivered baseline through Phase 3.

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

**Capability owners and design authority:** [DAHN](../hx/dahn-design-spec.md).

**Integration prerequisites:** S1, PRs 1–2; current slot-directed selection. Existing detailed dependencies below still apply.

**Recorded status:** Recorded delivered baseline through Phase 3.

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

    select visualizer for owner-declared slot + typed subject/context

After Space Navigator activation, the initial implementation MAY
deterministically select the sole compatible package-provided Visualizer Holon
under ordinary applicability. Missing or multiple eligible candidates follow
the explicit error policy; this is not an unconditional fallback.

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
- The bundled-candidate implementation proves the correct architectural direction.

---

## PR 4 — Theme Token Foundation

**Capability owners and design authority:** [Theme](../hx/dahn-design-spec.md#45-design-tokens-meta-design-systems-and-theme-ownership), [DAHN](../hx/dahn-design-spec.md).

**Integration prerequisites:** Runtime contracts. Existing detailed dependencies below still apply.

**Recorded status:** Recorded delivered baseline through Phase 3.

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
ordering, and responsive treatment); it may directly compose String labels and typed Value Visualizers. There is no
intervening Property VisualizerKind or Property selector.

---

## PR 5 — Static Table Collection Visualizer

**Capability owners and design authority:** [Table](../hx/visualizers/collection/table/design-spec.md), [Collection](../hx/visualizers/collection/kind-spec.md).

**Integration prerequisites:** Runtime and collection projection. Existing detailed dependencies below still apply.

**Recorded status:** Recorded delivered baseline through Phase 3.

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

**Capability owners and design authority:** [SDK](../hx/dahn-arch.md), [Host](../hx/dahn-design-spec.md#30-parent-owned-allocation).

**Integration prerequisites:** Application-session and home-Dancer contracts. Existing detailed dependencies below still apply.

**Recorded status:** Recorded delivered baseline through Phase 3.

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

**Capability owners and design authority:** [Canvas](../hx/dahn-design-spec.md#29-canvas-dancer-and-rooted-navigation-responsibilities), [Theme](../hx/dahn-design-spec.md#45-design-tokens-meta-design-systems-and-theme-ownership).

**Integration prerequisites:** 5.a-pre, theme and runtime seams. Existing detailed dependencies below still apply.

**Recorded status:** Recorded delivered baseline through Phase 3.

**Planned Dev Points:** 3

### Goal

Introduce the generic DAHN Canvas Visualizer and mount it from the MAP-bound
ApplicationSession produced by PR 5.a-pre, with its current application host. PR 18.b subsequently introduces the Window Manager grant around this delivered Canvas.

### Scope

Create:

- an initial Canvas Holon loaded with bootstrap schema resources and a runtime
  `CanvasVisualizer` holonic wrapper for the selected Canvas;
- generic Canvas chrome and a distinct hosted-Dancer allocation region, both bounded by the containing application allocation;
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

**Capability owners and design authority:** [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md).

**Integration prerequisites:** Canvas and semantic Visualizer resolution. Existing detailed dependencies below still apply.

**Recorded status:** Recorded delivered baseline through Phase 3.

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

**Capability owners and design authority:** [Dancer](space-navigator-design-spec.md), [Canvas](../hx/dahn-design-spec.md#29-canvas-dancer-and-rooted-navigation-responsibilities).

**Integration prerequisites:** 5.a-pre, 5.a, 5.b and home-Dancer selection. Existing detailed dependencies below still apply.

**Recorded status:** Recorded delivered baseline through Phase 3.

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

**Capability owners and design authority:** [Launch](../hx/dahn-launch-experience-design-spec.md).

**Integration prerequisites:** 5.a-pre, 5.a, 5.b.1; readiness/handoff. Existing detailed dependencies below still apply.

**Recorded status:** Recorded delivered baseline through Phase 3.

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

**Capability owners and design authority:** [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md), [PropertyMap / Value](../hx/visualizers/property-map/kind-spec.md).

**Integration prerequisites:** 5.b and recursive DAHN selection. Existing detailed dependencies below still apply.

**Recorded status:** Recorded delivered baseline through Phase 3.

**Planned Dev Points:** 3

### Goal

Fill the selected Generic Holon Node Visualizer's Property Viewer Pane with
descriptor-driven scalar-property presentation.

### Scope

Use `PropertyMapVisualizer` with directly selected String labels and typed Value
Visualizers to display current scalar types.

The generic Properties Visualizer MUST provide the initial Property Viewer
Pane: a set-level scalar-property presentation with named value slots. It
selects or receives String label and typed Value Visualizers without embedding a
growing switch statement for concrete value types.

Define the Properties Visualizer's named value slots and the Value Visualizer
selection/resolution path they use. Mount the selected Properties Visualizer
into the Property Viewer Pane established by PR 5.b.

### Non-Goals

Do not implement editing, standalone label/value presentation outside the
Node, table-cell integration, or property-set personalization yet.

### Acceptance Criteria

- A scalar Property set resolves to a `PropertyMapVisualizer` rather than a
  Node directly laying out raw values.
- The generic Properties Visualizer owns the initial Property Viewer Pane and
  provides distinct label/value composition slots.
- Each supported value type resolves to an applicable Value Visualizer.
- Generic candidates use ordinary applicability; missing or ambiguous selection is explicit.
- The same PropertyMap and Value contracts can later support edit mode.
- Scalar Properties and Values are visibly rendered only inside the selected
  Node's Property Viewer Pane.

---

## PR 9 — Descriptor-Driven Affordance Classification

**Capability owners and design authority:** [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md), [SDK](../hx/dahn-arch.md).

**Integration prerequisites:** Effective descriptors and 5.b. Existing detailed dependencies below still apply.

**Recorded status:** Recorded delivered baseline through Phase 3.

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
- Discover relationship population asynchronously with bounded concurrency after
  initial Node display; reveal populated rail/tab affordances and known collection
  counts progressively (Design §§16.4, 30).
- Preserve access to empty relationships for editing/schema inspection; distinguish
  unknown, failed, and verified empty results and ignore obsolete discovery work.
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

**Capability owners and design authority:** [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md), [Collection](../hx/visualizers/collection/kind-spec.md).

**Integration prerequisites:** 5, 9 and collection access. Existing detailed dependencies below still apply.

**Recorded status:** Recorded delivered baseline through Phase 3.

**Planned Dev Points:** 3

### Goal

Make plural affordances inspectable.

### Scope

Support activation of:

- array-valued property tabs;
- multi-valued relationship tabs.

On activation:

- establish relationship target existence before structural changes;
- open the destination below the Node and show pending feedback in that region;
- retrieve contents lazily and request/select/materialize a Collection Visualizer;
- replace pending feedback in-place;
- retain the region when switching tabs, identifying the requested collection
  during the pending state and preventing stale completion from replacing it.

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
- Verified empty relationships are absent from normal browse affordances; a
  zero-target activation produces local feedback without allocating a region.
- Explicit edit/inspection flows can display empty collections.
- Pending and final collection content occupy the same region; switching does
  not collapse/reopen it or discard retained navigation paths.
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

**Capability owners and design authority:** [Table](../hx/visualizers/collection/table/design-spec.md).

**Integration prerequisites:** 10 and member-reference binding. Existing detailed dependencies below still apply.

**Recorded status:** Recorded delivered baseline through Phase 3.

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

**Capability owners and design authority:** [Path Inspector](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md), [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md).

**Integration prerequisites:** 10–11 and Node child selection. Existing detailed dependencies below still apply.

**Recorded status:** Recorded delivered baseline through Phase 3.

**Planned Dev Points:** 3

### Goal

Navigate from a collection into one selected holon.

### Scope

On collection-row activation:

- establish the selected member destination beneath the Collection Visualizer;
- show pending feedback in the allocated child region;
- select/resolve its Node Visualizer and replace pending feedback in-place;
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

**Capability owners and design authority:** [Path Inspector](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md), [Table](../hx/visualizers/collection/table/design-spec.md).

**Integration prerequisites:** 12 and retained-path grammar. Existing detailed dependencies below still apply.

**Recorded status:** Recorded delivered baseline through Phase 3.

**Planned Dev Points:** 5 (revised from 2 to include retained-path insertion)

### Goal

Support exploration of collection members while preserving traversed paths according
to the authoritative [Path Inspector Interaction Grammar](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md)
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
- Destination allocation and pending feedback precede content realization. Existing
  continuations remain recoverable throughout structural transitions; failures stay
  local to the pending destination and stale completions cannot mutate newer state.
- Automated topology/projection and selected-visualizer interaction tests cover
  leaf replacement, retained insertion, repeated and nested alternatives, tab
  changes, provenance stability, and failure recovery. Manual verification covers
  sibling exploration and retained-path recovery with PR 16 compression in a
  constrained viewport.

---

# 6. Phase 3 — Horizontal Navigation and Provenance Geometry

---

## PR 14 — First Singular Relationship Child

**Capability owners and design authority:** [Path Inspector](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md), [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md).

**Integration prerequisites:** 9, 12–13 and singular target access. Existing detailed dependencies below still apply.

**Recorded status:** Recorded delivered baseline through Phase 3.

**Planned Dev Points:** 5 (revised from 3 to include retained horizontal alternatives)

### Goal

Activate singular relationship navigation to the right, including switching among
singular affordances without losing traversed history, according to the authoritative
[Path Inspector Interaction Grammar](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md) v0.2, especially
§§2.2–2.4 and §§3.3–3.8.

### Scope

For max-cardinality-one relationships:

- activate a populated right-rail entry and establish valid target existence;
- partially compress the expanded source and allocate the right-hand destination
  before displaying target content, with pan/reflow preserving spatial continuity;
- show pending feedback in that destination, retrieve its target lazily, and
  select/resolve its Node Visualizer through the normal selection path;
- replace pending feedback in-place with the distinct child and retain its source;
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
width. Retained paths remain recoverable in the bounded viewport. Destination-first
source compression is required here; PR 17 extends the broader compression policy.

### Boundaries and Sequencing

Build on PRs 9–13 classification, collection interaction, occurrence realization and
retained vertical alternatives, preserving the PR 16 compression substrate already
present. This PR owns retained horizontal alternative insertion; it is not deferred
to PR 15. PR 15 remains responsible for recursive horizontal traversal. Existing
vertical capabilities must continue to work for horizontally reached occurrences.

Include the source compression needed for destination-first feedback; broader
horizontal compression policy remains in PR 17. Do not add re-rooting or
branch-closing controls, persistent sessions, relationship editing, or a general
graph-layout engine.

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
- Zero-target activation leaves layout and focus unchanged with local feedback.
- Destination allocation, source compression, and pending feedback precede target
  content. Retained paths survive structural transitions; failures appear locally
  and stale completions cannot overwrite newer navigation state.
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

**Capability owners and design authority:** [Path Inspector](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md).

**Integration prerequisites:** 14. Existing detailed dependencies below still apply.

**Recorded status:** Recorded delivered baseline through Phase 3.

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

**Capability owners and design authority:** [Path Inspector](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md), [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md).

**Integration prerequisites:** 12–15 and axis participation. Existing detailed dependencies below still apply.

**Recorded status:** Recorded delivered baseline through Phase 3.

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

**Capability owners and design authority:** [Path Inspector](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md), [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md).

**Integration prerequisites:** 14–16. Existing detailed dependencies below still apply.

**Recorded status:** Recorded delivered baseline through Phase 3.

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

**Capability owners and design authority:** [Path Inspector](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md), [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md).

**Integration prerequisites:** 16–17 and independent axis state. Existing detailed dependencies below still apply.

**Recorded status:** Recorded delivered baseline through Phase 3.

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

# 6A. Phase 3A — DAHN Composition and View Foundations

Phase 3 is delivered, as confirmed by the project owner on 2026-09-28. The original PRs 14–18 are the completed navigation/compression baseline. The following slices are new work; they do not reopen earlier phases or imply these new requirements have already shipped.

Implement in the listed order. Start by grounding the surface/view delta against the delivered code, preserving its traversal and retained-branch behavior. Each slice must demonstrate a visible improvement or an independently verifiable authority boundary before the next is added. Collection refinement in Phase 4 follows this foundation increment.

## PR 18.a — Surface View Transform and Recovery

**Capability owners and design authority:** [Canvas](../hx/dahn-design-spec.md#29-canvas-dancer-and-rooted-navigation-responsibilities), [Path Inspector](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md), [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md).

**Integration prerequisites:** Delivered PR 18; surface/view and extent contracts. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

### Goal

Prove reusable view-transform infrastructure through Path Inspector's first navigation surface.

### Scope and Dependencies

Depends on the delivered PRs 12–18. Use the explicit policy profile at the Node slot boundary and protect useful inspection through surface growth; the older child-report sizing approach is superseded by §22. Preserve occurrence identity, provenance, retained alternatives, and whole-row/column compression while separating layout from view state. Implement pan/scroll, zoom, Zoom to Fit, and focus/actual-size against surface geometry. Keep pinned host chrome outside the transform. Derive off-viewport visibility independently from compression and layout overflow. Test nested hosting so Canvas requests reach the surface owner without reaching into its layout.

### Agreed Initial Presentation Policies

For [map-holons #759](https://github.com/evomimic/map-holons/issues/759), apply these initial policies:

- **Fit extent:** include all currently laid-out navigation geometry, including connectors and status regions. Exclude retained alternatives without current layout.
- **Actual size:** use scale `1.0` and center the active/open occurrence, preserving its allocation and compression state.
- **Extent policy:** explicit configured profile limits determine track budgets; no rendered child report or fallback DOM measurement may drive ancestor allocation. Pending and materialized children share the same geometry. §22 owns the migration to this contract.
- **Viewport resize:** a real viewport resize may explicitly recalculate layout while honoring minimum useful extents. Pan or zoom alone never triggers that recalculation.
- **Controls:** provide discoverable pan/zoom, Zoom to Fit, and Actual Size controls, bounded positive zoom scale, and predictable zoom anchoring. Exact gestures, bounds, padding, and dimensions remain implementation presentation choices.
- **Empty or unmeasured content:** retain a valid transform and disable or safely defer fit/centering until the required geometry exists. Empty topology must remain usable, including after root closure.

These policies settle the initial implementation posture without requiring a generalized slot schema or Window Manager. They do not change the independent topology/layout/view contract.

### Acceptance Criteria

- At 50% zoom and after panning, occurrence budgets, layout coordinates, topology, and compression remain unchanged.
- Zoom to Fit changes only view position/scale and covers the relevant extent; actual-size recovers useful scale and centers the active occurrence.
- Surface content exceeding a small viewport remains reachable; clipping does not create overflow state or trigger further compression.
- Connectors stay registered with occurrences, while pinned chrome retains its own allocation.

---

## PR 18.b — Minimal Window Manager Context Host

**Capability owners and design authority:** [Host](../hx/dahn-design-spec.md#30-parent-owned-allocation), [Canvas](../hx/dahn-design-spec.md#29-canvas-dancer-and-rooted-navigation-responsibilities).

**Integration prerequisites:** 5.a-pre/5.a; sequenced after 18.a, no navigation-geometry dependency. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

### Goal

Introduce reusable top-level context lifecycle and bounded display grants between application startup and Canvas mounting.

### Scope and Dependencies

Build on the delivered launcher and Canvas (PRs 5.a-pre/5.a); the listed execution order follows PR 18.a, although the host extraction does not depend on navigation geometry. Implement a Dancer-neutral context identity, create/destroy/switch requests, allocation notifications, and maximize/restore/minimize capability reporting. Start with a single-context host; preserve a creation seam for future top-level context extensions. PR 18.e adds Dancer-owned exploration tabs within the existing context. No desktop-window API is mandatory.

### Acceptance Criteria

- A test host creates and tears down a Canvas allocation without importing Space Navigator.
- Canvas receives finite bounds and cannot mutate global display allocation directly.
- Unsupported operations/refused requests are explicit and preserve the existing context.
- Teardown does not call semantic transaction abandonment; semantic ownership is supplied separately.

---

## PR 18.c — Bounded Focus and Maximize Requests

**Capability owners and design authority:** [Host](../hx/dahn-design-spec.md#30-parent-owned-allocation), [Canvas](../hx/dahn-design-spec.md#29-canvas-dancer-and-rooted-navigation-responsibilities), [Path Inspector](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md), [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md), [Table](../hx/visualizers/collection/table/design-spec.md).

**Integration prerequisites:** 18, 18.a, 18.b; independent restoration. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

### Goal

Exercise the three composition authorities through the first complete navigation surface.

### Scope and Dependencies

Depends on PR 18, PR 18.a, and PR 18.b. Wire Visualizer-local `maximize-region`/restore, Canvas occurrence attention, and Window/context maximize as distinct request paths. Preserve local restore information and route expansion requests through each parent. Leave presentation controls to the design realization.

### Acceptance Criteria

- A child local maximize stays inside its occurrence grant; restore recovers local composition.
- Canvas attention preserves navigation branches and does not invoke Window Manager maximize implicitly.
- Context maximize changes only the host grant; refusal preserves usable current presentation.
- View-only focus/actual-size does not invoke compression or layout recomputation.

---

## PR 18.d — Close Navigation Branch

**Capability owners and design authority:** [Path Inspector](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md).

**Integration prerequisites:** 18.a; retained topology and branch pruning. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

### Goal

Implement the Path Inspector close production for the read-only explorer.

### Scope and Dependencies

Depends on PR 18. Remove branches by occurrence parentage and reconcile focus, connectors, and layout. Use a semantic-state boundary test double before transaction UI exists; do not implement semantic abandonment.

### Acceptance Criteria

- Closing C in A–B–C–D retains A–B and a sibling B–E–F branch.
- Collection-descendant closure removes only that lineage; collection closure removes all exploration descended through it.
- Other occurrences of the same Holon survive, and focus falls back according to the grammar.
- Closing the root clears topology without destroying the host context.
- External staged/Nursery state is unchanged by closure.

---

## PR 18.e — Re-root into a New Experiential Context

**Capability owners and design authority:** [Host](../hx/dahn-design-spec.md#30-parent-owned-allocation), [Canvas](../hx/dahn-design-spec.md#29-canvas-dancer-and-rooted-navigation-responsibilities), [Dancer](space-navigator-design-spec.md), [Path Inspector](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md).

**Integration prerequisites:** 18.b, 18.d; source-preserving exploration-tab creation. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

### Goal

Connect Space Navigator's re-root intent to additional exploration tabs owned by the same Space Navigator experience.

### Scope and Dependencies

Depends on PR 18, PR 18.b, PR 18.d, and PR 5.b.1. Retain and switch between at least two exploration tabs within one Space Navigator experience. The initial Path Inspector is rooted at the HolonSpace; re-root creates another tab rooted at the requested Holon. Pass the explicit anchor and inherited experience context through each RootedNavigation slot; preserve the source occurrence and topology. Keep active HolonSpace separate from explicit navigation-root input. No additional Canvas or Window Manager context is required.

Read-only tabs share the Space Navigator-owned read transaction and semantic cache, with request coordination through its execution surface. Tab disposal releases only presentation resources. Verify read/write segregation and valid bound-reference reuse; do not infer existing runtime enforcement from this design decision. Before staged editing integration, resolve transaction policy across tabs in the authoritative transaction design.

Implement the [activation and realization outcomes](space-navigator-interaction-grammar.md#activation-and-realization-outcomes): immediate pending feedback, source retained until a usable root is ready, no completion-driven focus theft after a user tab switch, and destination cleanup with dismissible Space Navigator error/Retry on failure. Test cancellation and late completion; an unavailable-Dancer placeholder is not successful readiness.

Deferred: detaching an existing exploration tab into its own Window Manager-hosted window while preserving Space Navigator ownership and exploration state. PR 18.e establishes in-experience tabs only; detachment, reattachment, and detached-window closure policy are follow-up work.

### Acceptance Criteria

- Re-root C in A–B–C–D leaves the source intact and creates a distinct exploration tab/root occurrence at semantic C.
- Switching between the HolonSpace-rooted tab and C-rooted tab preserves independent topology, selections, focus, and view state.
- Both tabs share the read transaction; closing one neither disposes it nor affects the other tab. No additional Window Manager context is created.
- Failure/refusal leaves source topology and semantic state intact.
- `replace-current-root`, if retained, has a separately named intent and tests; it is not the re-root handler.

---

# 7. Phase 4 — Read-Only Collection Refinement

---

## PR 19 — Collection Sorting

**Capability owners and design authority:** [Table](../hx/visualizers/collection/table/design-spec.md).

**Integration prerequisites:** Collection projection and retained occurrence state. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

**Planned Dev Points:** 2

### Goal

Add the first collection-view operation.

### Scope

Support:

- column-oriented sorting under [Table sorting and ordering](../hx/visualizers/collection/table/design-spec.md#column-operations);
- descriptor-backed Key defaults, including concrete keyed members of broadly typed collections such as Owns;
- table defaults for unordered collections: Key ascending for keyed element/member HolonTypes, otherwise supplied order;
- ascending/descending state;
- preservation within the Collection Visualizer occurrence.

### Acceptance Criteria

- Sort state is visible and persistent within the occurrence.
- Switching tabs and returning restores sort state.
- Compression does not destroy sort state.
- Typed comparisons, missing values, stable ties, header gestures, and sort indicators conform to the linked Table sorting contract.
- Manual-order occurrence metadata and the Sequence column are deferred from this PR. Ordered collections remain readable and may use explicit property-column sorting; indicate unavailable manual order rather than fabricate positions.
- Unordered keyed holon collections default to Key ascending, including Owns with a broad keyless declared target and concrete keyed member types; keyless/scalar fallbacks retain supplied order. The intended Sequence-first default in the design specification requires the deferred occurrence-metadata work.
- Descriptor policy determines ordered/keyed classification; incidental row order and display labels do not.
- A valid saved sort overrides the table default; a missing/ineligible saved column restores the applicable default.
- SDK descriptor reads reuse the existing command/reference boundary, including `RelationshipDescriptorHandle.isOrdered()` backed by Rust `RelationshipDescriptor::is_ordered()`. Authoritative per-occurrence sequence exposure is a follow-up prerequisite for manual-order support; display indices cannot substitute.

---

## PR 20 — Collection Filtering

**Capability owners and design authority:** [Table](../hx/visualizers/collection/table/design-spec.md), [SDK](../hx/dahn-arch.md).

**Integration prerequisites:** 19 and authoritative query/filter semantics. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

# 8. Phase 5 — Adaptive Ordering, Visualizer Inspection, and Choice

This phase exposes the DAHN selection and personalization flow without requiring
full collective learning or Visualizer Commons discovery. PRs 21–22 retain their
ordering scope. The former PR 23 is superseded by PRs 23.a–23.f below; its original
3-point estimate is historical, not the estimate for the expanded experience.

The first useful delivery is a read-only Visualizer icon and inspector. It does
not depend on PRs 21–22, alternate candidates, preference ranking, or completion
of a broader composition refactor. Later slices use the same action to expose
choice, with the ancestry explorer as a subsequent extension.

| Unit | Lifecycle | Planned Dev Points | Deliverable |
| --- | --- | --- | --- |
| 23.a | Planned | 3 | Target-bound V and read-only Node Visualizer inspector |
| 23.b | Planned | 3 | Multi-level inspection and homogeneous Table access |
| 23.c | Planned | 5 | Rust candidate discovery and explicit-choice validation |
| 23.d | Planned | 5 | VisualizerUsage selection and new-usage initialization |
| 23.e | Planned | 5 | Inspector choice and failure-safe occurrence replacement |
| 23.f | Planned | 5 | Replaceable ancestry explorer and recursive choice |

The replacement PR 23 track totals **26 planned Dev Points**: 6 for read-only
multi-level inspection, 15 more for the first working selector/replacement flow,
and 5 for the subsequent explorer extension. With unchanged PRs 21–22, Phase 5
rolls up to **32 planned Dev Points**. These are plan-level estimates, not defined
issue estimates or delivered actuals. Each rationale and re-estimation trigger
is recorded with its chunk.

Adaptive delivery follows the [shared design principles](../hx/dahn-design-spec.md#48-adaptive-human-experience)
and [reporting contract](../hx/dahn-design-spec.md#148-adaptive-interaction-reporting).
The deterministic bootstrap remains valid. PRs 21–22 establish ordering and
semantic gesture seams; 23.c discovers and validates candidates, 23.d selects
and initializes usage, and 23.e realizes occurrence choice and reports its
outcome. Candidate inspection or authorization is not successful adoption.
An occurrence-scoped choice does not implicitly pin, persist a general
preference, update session memory, or consent to collective contribution.
Resolve context matching, reporting correlation, and persistence/sharing scope
before the affected slices rely on them. Automatic collective aggregation and agent-facing adaptive controls, including
the historical slider dimensions, remain intended future capabilities.
Collective capture/aggregation requires Agent Space participation and sharing
contracts. Learning, trending, exploration algorithms, and adaptive-control UI
require separately bounded delivery; these principles do not expand the listed
PR scopes.

Delivery dependencies: 23.a → 23.b; 23.c and 23.d can be prepared independently
of read-only inspection; 23.e requires 23.a–23.d; 23.f follows 23.e. Before
implementation, resolve each listed design gate in its authoritative spec and
ground the affected chunk against the then-current code and issue scope.

---

## PR 21 — Presentation Ordering from Rust

**Capability owners and design authority:** [DAHN](../hx/dahn-design-spec.md), [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md), [PropertyMap / Value](../hx/visualizers/property-map/kind-spec.md).

**Integration prerequisites:** Rust presentation preferences. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md), [PropertyMap / Value](../hx/visualizers/property-map/kind-spec.md), [DAHN](../hx/dahn-design-spec.md).

**Integration prerequisites:** 21 and adaptive reporting. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

## PR 23.a — Visualizer Icon and Read-Only Inspector

**Capability owners and design authority:** [DAHN §14.7](../hx/dahn-design-spec.md#147-multi-level-visualizer-information-and-choice), [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md).

**Integration prerequisites:** A realized Node occurrence with its selected
Visualizer reference, actual slot, owner, subject, and context available.

**Recorded status:** Merged in [PR 800](https://github.com/evomimic/map-holons/pull/800), together with PR 23.b.

**Planned Dev Points:** 3

**Estimate rationale:** A bounded user-visible workflow spanning occurrence
context, presentation controls, holon reads, and accessible inspector hosting.
Re-estimate if occurrence identity or theme-controlled icon presentation needs
substantial new runtime infrastructure. The accepted auxiliary-region and custom
Visualizer scope expands the original information-box estimate; review the
3-point estimate against the grounded implementation.

### Scope

- Supply a target-bound semantic action from the composition owner/runtime.
- Expose the circled V in the Holon Inspector's controls, with theme-controlled
  presentation, an accessible name, and the selected Visualizer's display name
  in a tooltip above the control on hover and keyboard focus.
- Establish the Space Navigator-owned collapsible auxiliary region described in
  design spec §4.5, with stable open desktop width and responsive narrow-display
  hosting.
- Select a custom Visualizer for the inspected shared Visualizer definition; show
  its name, available description, presented subject, applicability, composition,
  implementations, and additional properties. Do not substitute the generic
  Holon Inspector or only a properties pane.
- Keep Visualizer definition information distinct from any selected usage.
- Capture the target when opened; support dismissal and focus return; closing
  the target dismisses inspection and restores focus to a surviving control. No choice, score, or usage creation is needed.

### Acceptance Criteria

- Two occurrences of the same subject open information for their own selected
  Visualizers; focus changes do not retarget an open inspector.
- Information remains useful with one candidate or no alternative-discovery API.
- Keyboard operation and focus return work; opening the inspector does not mutate
  the subject, usage, selection, or staged editing state. Custom presentation
  realization may create transient materialization protocol holons; it must not
  stage or commit semantic changes.

---

## PR 23.b — Multi-Level Visualizer Inspection

**Capability owners and design authority:** [DAHN §14.7.3](../hx/dahn-design-spec.md#1473-access-at-composition-levels), [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md), [Table](../hx/visualizers/collection/table/design-spec.md).

**Integration prerequisites:** 23.a and explicit selected-child composition metadata.

**Recorded status:** Merged in [PR 800](https://github.com/evomimic/map-holons/pull/800), together with PR 23.a.

**Planned Dev Points:** 3 (original estimate; re-estimate with the column selection foundation included)

**Estimate rationale:** Reuses the inspector across several composition boundaries
and adds contextual access tests. The scope now includes Table-owned Value slots,
descriptor-backed selection once per property column, selected cell realization,
and column-heading inspection. Re-estimate or split if ActionBar, Properties,
Collection Tabs, or Vertical Rail require new independently selected Visualizers;
creating those missing composition boundaries is not hidden in this estimate.

### Scope

- Expose inspection at the actual selected presentations for the ActionBar,
  Properties Pane, Collection Tabs bar, Vertical Rail, and active Collection View.
- Make nested ActionGroup/Action and property-name/value presentations reachable
  through containing inspection or contextual controls, without per-value icons.
- Select one Value Visualizer per descriptor-backed property column through
  Table's owned Value slot and reuse that definition across all cell instances.
- Provide column-heading V access to the actual selected Value Visualizer.
  Table owns row visualization; add no Row Visualizer, row V, or per-cell V.
- Keep descriptor bindings separate from projected values; identify columns
  without authoritative bindings as Table-owned rather than inferring selection.
- Identify implementation-owned regions honestly where a region is not an
  independently selected child; record missing boundaries for separate grounding.

### Acceptance Criteria

- Parent and child inspection targets remain distinct at every supported level.
- Homogeneous Table columns expose their actual Value Visualizer through one
  heading control; all cells in the column use that selection and rows remain
  Table-owned. Column inspection identifies its scope without authorizing choice.
- Compact controls remain keyboard accessible; closed children cannot be
  confused with subsequently mounted children.

---

## PR 23.c — Authoritative Candidate Discovery and Choice Validation

**Capability owners and design authority:** [DAHN §§14.2.1–14.8](../hx/dahn-design-spec.md#1421-slot-directed-descriptor-selection), Rust selector, existing host materializer, and public SDK.

**Integration prerequisites:** Existing slot-directed selection, bound-reference
command/SDK pipeline, Theme/MDS schema, and local implementation materialization.
No dependency on Agent Space adaptive services, preference scoring, 23.a/23.b UI,
23.d usage persistence, or deferred composition-contract adoption.

**Recorded status:** Merged in [PR 805](https://github.com/evomimic/map-holons/pull/805). The implementation record includes targeted Rust selector/command/wire/materializer tests, SDK tests and typecheck, web tests and typecheck, hApp WASM check, canonical-loader acceptance, and fixture-authoring checks; the local full Sweettest suite was not completed at that checkpoint.

**Planned Dev Points:** 5 (provisional). Re-estimate during implementation planning
if propagating mandatory selection context or sharing the host capability seam
is larger than this bounded local-runtime slice. Do not absorb separate schema,
subject-model, or composition migrations into the estimate.

### Delivery boundary

Deliver Rust/SDK discovery and explicit selection for the existing generic
**descriptor-based selection path**, with a working Node case and regression
coverage for its existing PropertyMap, Value, ActionBar, Action, Property, and
RootedNavigation request interpretations. Preserve the currently implemented
subject binding rules while centralizing their resolution. The transitional
Property layer and current Action binding are repository reality, not new target
architecture: their retirement/realignment is a separate migration.

Canvas launch and Collection selection retain dedicated contracts. Do not
invent descriptor subjects for collections or implement new Structure topology
subjects. Those paths do not silently inherit this unit's guarantees.

### Request and authoritative context

The shared request identifies:

- the actual bound subject and current supported subject discriminator;
- the actual slot and its explicitly typed composition owner;
- the selected semantic Theme reference;
- the requested candidate for explicit choice, when applicable;
- the currently displayed Visualizer for discovery, when provided separately.

Owner checks support existing Visualizer `HasSlot` and Dancer
`HasExperienceVisualizerSlot` declarations; never fake a parent Visualizer for a
Dancer-owned slot. Owner information is required on the supported generic path,
including automatic requests. Update its current call sites, command binders,
and SDK adapters together rather than leaving an unchecked omission path.

Rust derives the effective MDS from the selected Theme's `ForMetaDesignSystem`
relationship and checks `ConsumesDesignToken` against `DefinesDesignToken`.
Theme values/projection validation remains its existing contract. A caller
must not supply an arbitrary independent MDS or a boolean claiming compatibility.
The experience supplies its active Theme; revalidation uses the context of the
new request and does not certify that caller-reported presentation is mounted.

The runtime is the host's existing local TypeScript/ESModule capability and
local materializer catalog, not a caller-selected runtime or a new platform
registry. Bound reference/transaction and existing host authorization boundaries
remain authoritative. No new Human Agent identity model, Trust Channel service,
preference key, locale, device profile, workflow vocabulary, or adaptive-policy
schema is required here. Exact Rust/SDK names are implementation choices; keep
subject, owner, Theme, and runtime facts distinct from future policy inputs.

### Concrete contracts emerging through implementation

The implemented Rust/wire/SDK names, current subject interpretations, assessment
codes, error boundary, read-only lifecycle, exact Theme reference, and meaning of
`alternatives_available` are specified in [DAHN §14.2.2](../hx/dahn-design-spec.md#1422-current-descriptor-candidate-command-contract).
Keep that contract authoritative as implementation precision develops. Discovery
order is deterministic ancestry encounter order, not preference rank. Selection
availability is not materialization verification or an artifact reservation.

### Shared viability evaluation

Use one per-level discovery/assessment path for automatic selection, enumeration,
and explicit revalidation. Share subject resolution and candidate assessment;
keep ancestry traversal strategy and winner policy separate.

Required checks now:

1. Actual owner/slot association and nonempty accepted-type contract.
2. Applicability declared on the permitted subject lineage and candidate type
   equality/subtyping against `AcceptsVisualizerType`.
3. Candidate DesignToken requirements covered by the Theme's effective MDS.
4. Exactly one supported local implementation declaration, required metadata,
   TypeScript runtime, ESModule format, and a configured available local artifact.

Reuse a read-only capability check backed by the current host materializer's
catalog; no duplicated TS catalog, artifact execution, one-use handle issuance,
or transient materialization merely to enumerate candidates. Arrange dependency
injection/boundaries without introducing a reverse crate dependency. Digest
verification, module execution, actual callable validation, and owner admission
remain materialization/realization checks and may still fail after selection.
A discovery-time availability finding is not a reservation or behavioral proof.

Report candidates as viable under these checks, incompatible, or implementation
unavailable, with machine-readable reasons and applicable evidence. Invalid
request context, malformed required declarations, lookup failures, cycles, and
multiple-parent ancestry are explicit structural/evaluation errors; do not turn
failed evaluation into a successful empty discovery or invent a score of zero.
Optional learned evidence is not part of this initial viability result.

### Discovery and explicit choice

- Enumerate local applicability declarations throughout permitted subject
  ancestry. Check HolonType inclusively for holon lineages and never its parent;
  other descriptor families stop at lineage exhaustion. TypeKind definers do not
  stop interactive discovery. Deduplicate by established semantic identity and
  preserve every declaring-descriptor provenance, including repeated declarations.
- Return the caller-captured current selection separately, with its current
  assessment or no-longer-applicable status. It is not automatically an eligible
  alternative and is not proof of current mounted state.
- Explicit choice re-resolves applicability and all supported viability checks
  using the actual request context. It may select a viable general candidate
  despite a nearer automatic winner or unresolved nearer ambiguity. It cannot
  select an unrelated identity, waive a required check, or cross the boundary.
- Do not require a cached candidate list or token as authorization. A changed
  slot, Theme, applicability, or implementation state can invalidate a choice;
  fail explicitly without substituting another Visualizer.

### Automatic policy and extension seams

Automatic selection remains lazy: evaluate the nearest level; return its sole
viable candidate, report ambiguity if multiple remain, and read a parent only
when none is viable. Do not perform an ancestry-wide discovery first. No
preference service or score is needed for a sole candidate.

Keep the policy decision separate from viability so a later scoring algorithm,
holonic policy/ruleset, or agent-controlled exploration can consume assessed
candidates without duplicating hard checks. This unit implements only the
existing deterministic policy, not a score-combiner, rule registry, plugin
framework, slider UI, or placeholders pretending absent evidence is a score.
Preference diagnostics remain optional; provenance and viability reasons are
required. TypeScript displays Rust outcomes and does not rank/select candidates.

[Deferred DevDocs PR 63](https://github.com/memetic-activation-platform/map-dev-docs/pull/63)
shows how required/offered participation contracts can later extend the hard
assessment stage. No Operator schema, binding protocol, conformance framework,
or Path/Inspector/loader refactor is adopted here. Do not claim accepted types
prove complete participation or executable behavior. Future required contracts
must have an evaluator; unsupported known requirements cannot be claimed fulfilled.

### SDK and semantic effects

Expose discovery and explicit-choice operations through existing read-only
transaction command/domain/wire/SDK seams. Bind ingress references, preserve
runtime/wire separation, and return public handles with provenance and diagnostics.
Update automatic generic selection context and its consumers alongside them.

Discovery and validation do not stage/commit, create or reset VisualizerUsage,
change session memory, pin a preference, record successful adoption, or replace
an occurrence. Captured presentation target IDs and asynchronous replacement
admission remain 23.e responsibilities. Two new shipped alternative UI artifacts
are not required; graph fixtures prove choice among eligible candidates.

### Acceptance Criteria

- A Node fixture has specialized and general locally supported candidates;
  discovery reports both with provenance, automatic selection picks the nearest,
  and an explicit viable general choice succeeds.
- A viable explicit choice also resolves nearer-level ambiguity; automatic
  ambiguity remains explicit and never falls back merely to evade it.
- Regression tests retain current subject interpretation across supported
  generic request kinds. Canvas/Collection remain explicitly dedicated paths.
- Visualizer- and Dancer-owned slots validate their actual owners; omitted/foreign
  owners, empty contracts, incompatible types, and missing context fail clearly.
- Theme token mismatch rejects a candidate. Rust derives the MDS from Theme,
  and a new Theme at choice time causes current eligibility to be reevaluated.
- Unsupported runtime/format, missing implementation/catalog/artifact availability,
  and malformed metadata have distinguishable outcomes; no execution or artifact
  capability is issued by discovery.
- Duplicate identities retain all declaration provenance; current selection
  stays separately identifiable when no longer applicable or viable.
- Tests cover accepted subtypes, invalid subject/candidate ancestry, boundary
  inclusion, no reads above HolonType, and no unnecessary ancestor reads after
  automatic success or ambiguity. Structural failures remain explicit.
- Changing applicability, owner/slot requirements, Theme, or implementation state
  between discovery and choice is detected without a fallback or semantic mutation.
- Host selector, command binding/dispatch/result projection, and public SDK tests
  cover the full request and outcome. Run relevant Rust/SDK checks and consumer
  typechecks; no choice UI or unrelated Holochain fixture is required.
- Materialization/admission limitations and all unrun checks are recorded. Broader
  adaptive, subject-model, security, and composition migrations stay deferred.

---

## PR 23.d — VisualizerUsage Selection and Initialization

**Capability owners and design authority:** [DAHN §11.1](../hx/dahn-design-spec.md#111-visualizerusage), [DAHN selection policy](../hx/dahn-design-spec.md#146-agent-choice-and-selection-policy), Rust personalization services.

**Integration prerequisites:** Selected Visualizer identity and the existing local
space context; the agent is implicitly the space's agent.
**Design decisions:** DAHN §11.1 defines the initial usage contract. Implement
the schema representation of retained slot associations and descriptor-specific
preferred usage under existing local-space transaction/access policies; this does
not require new multi-space authorization infrastructure. Initial usage matching, prior-association reuse,
zero/one/multiple-match handling, and automatic persistence through an independent
transaction are specified in DAHN §11.1. Low, nonzero randomness applies only
to Visualizer choice; usage selection preserves configuration continuity. No
slider UI is required for this default. Visualizer exploration is owned by the
Visualizer selection policy, not usage-configuration arbitration.

**Current implementation boundary:** Only one space is supported. For this slice,
the applicable Agent Space/Focal Space is the existing local space. No space
picker, foreign-space usage access, cross-space writes, or new Agent Space
infrastructure is required. Multi-space ownership, routing, and sharing behavior
remain deferred; this boundary does not claim those capabilities are implemented.

**Recorded status:** Implemented and reviewed in [PR 806](https://github.com/evomimic/map-holons/pull/806); pending merge in the PR 23.d–23.f stack as of 2026-10-11.

**Planned Dev Points:** 5

**Estimate rationale:** A bounded Rust-owned usage lifecycle with schema/SDK
integration and configuration preservation tests. Assumes a resolved matching
policy and existing preference inputs or documented deterministic defaults;
re-estimate if schema migration or a new collective-learning service is required.

### Scope

- Select applicable prior usage after Visualizer selection through the
  deterministic initial policy in DAHN §11.1. Keep Visualizer preference and
  exploration policy distinct from usage configuration reuse. New scoring,
  randomized Visualizer exploration algorithms, and preference-input services
  are not prerequisites for this usage-lifecycle slice.
- Reuse an applicable prior slot association. Without one, reuse the sole
  matching usage, create and initialize on zero matches, and report an explicit
  error on multiple matches. Do not randomly choose a configuration.
- Preserve selected existing usage configuration unchanged.
- Persist new usage through an independent transaction before returning it as
  usable. Serialize initialization by Visualizer and subject descriptor within
  the local space, recheck after serialization, and commit creation/configuration
  atomically. Retry reuses a committed result; failures expose no partial usage
  and leave the current presentation and subject transaction untouched.
- When no applicable prior usage exists, create and initialize usage with property
  salience, relationship salience, action groups, and action salience using the
  defined initial preference/default policy. Without applicable preference
  evidence, initialize four empty override sets; absent entries mean neutral
  salience/default presentation. No per-member score records or future editing
  score model are required for this initialization.
- Reconcile historical FillsVisualizerSlot / FulfilledByVisualizerUsage
  relationships with the slot-choice association defined in DAHN §11.1. Preserve
  the distinction between Visualizer selection, applicable usage reuse, and
  personalized configuration. Support many-to-many retained associations and
  a separate remembered preferred usage per slot and subject descriptor;
  regenerate affected schema and bootstrap resources.
- Preserve the distinction between persisted usage preparation and successful
  use. Slot associations and remembered preference are updated only on successful
  presentation reported to Rust; only explicit choice updates preference.
  PR 23.e owns presentation and outcome reporting. Failed or exploratory choice
  must not overwrite remembered preference.
- Keep occurrence binding, agent usage, and shared Visualizer identity distinct.
  Advanced scoring, preference editing, and collective learning are outside this slice.
- Defer explicit creation of a separate personalized configuration (copying a
  usage and rebinding one slot) to follow-up work. The corresponding target
  interaction in DAHN §11.1 does not expand PR 23.d. This slice does not require
  a copy-configuration action, multiple configuration presets, or a new
  default-versus-copy usage classification.

### Acceptance Criteria

- The space's agent is implicit; no caller-supplied agent parameter or separate
  UsageContext ontology is introduced.
- Different instances with the same subject descriptor and selected Visualizer
  reuse applicable usage; different subject descriptors have separate usages.
- An applicable prior slot association is reused. Without one, zero matches
  initialize, one match reuses, and multiple matches return an explicit error.
- Existing configuration is neither reset nor rescored; four empty override sets
  provide neutral/default initialization when preference evidence is absent.
- New usage survives restart after independent commit. Concurrent missing-usage
  requests converge on one committed result, retries reuse it, and failures expose
  no partial usage or unintended subject-transaction changes.
- Retained associations support multiple slots and Visualizers. Preferred usage
  is distinct and descriptor-specific; no usage is said to fulfill the slot.
- Successful-use reporting is separate from preparation. Only a successfully
  presented explicit choice updates preference; failed or exploratory choices
  do not. Presentation realization/reporting remains PR 23.e responsibility.
- Shared Visualizer definitions remain unchanged. Subject-instance and occurrence
  identity do not partition usage, and slot identity guides association reuse
  without becoming a mandatory configuration partition.
- Separate-configuration creation, editing UI, slider UI, collective learning,
  and multi-space infrastructure remain outside this slice.

---

## PR 23.e — Visualizer Choice and Safe Occurrence Replacement

**Capability owners and design authority:** [DAHN §14.7](../hx/dahn-design-spec.md#147-multi-level-visualizer-information-and-choice), [DAHN architecture](../hx/dahn-arch.md), Holon Inspector and its composition owner.

**Integration prerequisites:** 23.a–23.d, materialization and lifecycle guards;
reusable semantic event reporting, without requiring PR 22's reordering UI.

**Recorded status:** Implemented and reviewed in [PR 810](https://github.com/evomimic/map-holons/pull/810); pending merge in the PR 23.d–23.f stack as of 2026-10-11.

**Planned Dev Points:** 5

**Estimate rationale:** An end-to-end choice workflow across Rust authorization,
usage selection, asynchronous realization, and owner-controlled replacement.
Assumes two small local Node alternatives fulfilling the same existing slot
contract. Re-estimate for unrelated implementation-private state transfer or
additional subject-family replacement contracts.

### Resolved design decisions

- Readiness requires successful explicit initialization, Node participation
  validation, and acceptance of the current allocation. Keep the prior Node
  usable until the owner rechecks liveness, generation, and dismissal guards and
  publishes the replacement; then dispose the prior realization. Clean up failed
  or superseded preparations. Browser paint is not the admission signal.
- Occurrence identity, topology, focus, allocation/compression, and external edits
  remain owner-held. Preserve selected collection/rail targets and collection
  sort/filter/selection through shared contracts; private presentation state may
  reset. Refuse replacement while an interaction cannot safely dismiss.
- Successful-use capture is best-effort after publication. Failures cannot undo
  replacement or block the primary task. Use bounded safe background retries;
  offer a mild, dismissible, non-modal warning only with a meaningful corrective
  action. Otherwise use diagnostics. Usage preparation remains a prerequisite.
- Reports carry occurrence identity and an ordered choice token. Rust deduplicates
  retries and protects the remembered preference against older choices across all
  occurrences sharing the local-space slot and exact subject descriptor. Retrying
  keeps original identity/order. Reconcile the current SDK/Rust reporting seam;
  no general event framework or deferred Operator refactor is required.

### Scope

- Extend the information inspector with eligible alternatives and separate inspect
  and choose actions; display preference explanations only when supplied.
- Prove the full flow with two locally materializable Node alternatives:
  Visualizer selection → usage selection → initialize only new usage → present.
- Prepare the replacement before publishing it, reject stale results, preserve
  occurrence/subject/context identity and parent allocation authority, and respect
  active-interaction dismissal guards.
- Retain externally owned staged state and contracted navigation/selection state;
  do not promise arbitrary private-state transfer.
- Emit an occurrence-scoped explicit-choice event, not an implicit global
  preference or instruction to overwrite shared usage configuration.

### Acceptance Criteria

- Initialization readiness and allocation acceptance precede publication; failed
  or superseded preparations release resources and preserve the prior Node.
- Reporting failure does not roll back a presented Node, block interaction, or
  discard configuration. Retry is bounded; any actionable warning is dismissible
  and does not steal focus. Older retries cannot overwrite newer preferences,
  including choices from another occurrence of the same slot/descriptor.

- One occurrence changes while another occurrence of the same subject remains
  unchanged; selected Visualizer and usage agree with the mounted realization.
- Failed selection, usage initialization, materialization, or admission leaves the
  prior presentation usable and reports the failure without a hard-coded fallback.
- Cancellation, target closure, and competing requests cannot publish a stale
  result. Existing usage configuration and external transactions survive.
- Unsupported row/column-wide or Canvas/Collection replacement remains unavailable
  until its explicit owner/subject contract exists; read-only inspection still works.

---

## PR 23.f — Ancestry Explorer and Recursive Visualizer Choice

**Capability owners and design authority:** [DAHN §14.7.4](../hx/dahn-design-spec.md#1474-composition-recursive-access-and-replacement-boundaries), [Structure kind](../hx/visualizers/structure/kind-spec.md).

**Integration prerequisites:** 23.e.
**Design decisions:** Resolved with the project owner on 2026-10-10; authoritative
contracts are in DAHN §14.7.4 and Space Navigator §4.5. No open product-design gate
remains. Concrete schema names, compatible projection mechanics, and an initial
finite nesting limit are implementation choices under those contracts.

**Recorded status:** Functionally complete and reviewed for merge into PR 23.e in
[PR 818](https://github.com/evomimic/map-holons/pull/818), implementing
[Issue 817](https://github.com/evomimic/map-holons/issues/817). Pending merge as of
2026-10-11. CI checks passed; the project owner reported successful hApp and host
builds, nominal `npm test` and `npm start`, and manual verification of inspection,
alternative choice, discovery explanation, and tree/level-list switching.

**Landing sequence:** Collapse the reviewed stack top-down: PR 23.f into PR 23.e,
then PR 23.e into PR 23.d, then PR 23.d into main. This avoids repeated descendant
rebases, redundant long CI cycles, and cascading conflicts. Broader Commit
performance work and real-estate management brittleness remain deferred; their
known limitations do not expand this delivery slice.

**Planned Dev Points:** 5

**Estimate rationale:** A bounded Structure presentation with two small local
realizations and nested interaction/lifecycle verification. Re-estimate if a generic
query explorer, new DAHN-wide kind, or new hosting framework is proposed.

### Scope

- Place “How these choices were identified” under initially closed Technical
  Details; realize its evidence/explorer on first opening. Keep purpose, preview,
  and Choose in the ordinary choice experience.
- Project the existing Rust discovery evidence into a transient holonic Structure
  subject; preserve visited levels, declarations, eligibility and endpoint/reason.
  Enrich that same operation for missing evidence, without a new discovery path.
  Rust excludes declarations whose Visualizer type is not accepted by the actual
  slot; retain matching-type Theme/implementation failures with their assessment.
  Resolve each projection record-type anchor once per snapshot, not per record.
  Opening/reopening/refreshing the explanation must not initialize persisted
  usage or commit. Read existing completed configuration, or use defaults; retain
  ordinary initialization/reporting for explicit explorer choice.
  Explain selection rationale only from actual selection evidence; no historical
  analysis or inferred narrative.
- The Visualizer Inspector owns the explorer's actual Structure slot. Provide a
  tree and level-list realization fulfilling the same subject/participation
  contract; add bounded Structure support to existing SDK/command/runtime seams.
  Declare the Discovery Explorer Structure subtype as the slot's accepted type;
  broad Structure ancestry does not make RootedNavigation a participant.
  Recursive transient-subject projection borrows its source semantic context
  without disposing it; the top-level owner releases the complete chain.
  Display replacement failures beside the attempted choice.
- Preserve captured evidence and owner-held semantic selection/preview state
  across explorer switching. Refresh separately; private expansion/scroll may reset.
- Reuse v inspection and choice recursively with separately captured targets.
  One top-level Inspector owns all child resources and nested sessions; mount one
  information session at a time and retain only contracted state for suspended
  sessions. A different main-area v, close, target invalidation, or host disposal
  cancels/disposes the whole chain through one idempotent ownership path.

### Acceptance Criteria

- Both independently selected local realizations present the same authoritative
  discovery chain and deterministic plain-language explanations without TypeScript
  reconstructing inheritance, compatibility or stopping/selection policy.
- Switching the explorer preserves the original subject's selected Visualizer,
  discovery evidence, semantic candidate/declaration selection and preview context.
- Nested inspection occurs only through explicit interaction, is depth-bounded,
  and restores a live invoker/replacement counterpart or containing control.
- Back, nested target invalidation, top-level replacement/closure and host disposal
  exercise cancellation, resource cleanup and stale-result rejection. Unmounted
  suspended sessions release presentation resources; late preparations are disposed.
- Required readiness/allocation admission precedes publication; failed replacement
  leaves the prior explorer usable and reporting remains best-effort after success.
- Performance optimization and broader real-estate/layout/Window Manager repair
  remain deferred. Existing allocation admission and state/resource safety apply;
  no generalized hosting or Operator refactor is required.

---

# 9. Phase 6 — Staged Editing Foundation

---

## PR 24 — Edit Existing Holon: Scalar Properties

**Capability owners and design authority:** [MAP transactions](../hx/dahn-arch.md), [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md), [PropertyMap / Value](../hx/visualizers/property-map/kind-spec.md).

**Integration prerequisites:** Read-only composition and staged scalar mutation. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [Dancer](space-navigator-design-spec.md), [MAP transactions](../hx/dahn-arch.md).

**Integration prerequisites:** 24 and transaction status. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

Integrate closure and context lifecycle with authoritative Rust staged/Nursery state. Resolve the editing-transaction policy across exploration tabs identified in PR 18.e before enabling re-root from an editing tab; retain Space Navigator experience ownership rather than attaching transaction ownership to Inspector occurrences.

### Acceptance Criteria

- Transaction state is not inferred separately by each Node.
- Editing one holon causes Space Navigator transaction state to update.
- Space Navigator Action Bar is the owner of transaction-scoped controls.
- Node Action Bar does not expose Commit.
- Transaction presentation is rendered through Dancer-scoped Action
  Visualizers rather than Canvas-specific button implementations.

---

## PR 26 — Meaningful Undo Boundaries

**Capability owners and design authority:** [MAP transactions](../hx/dahn-arch.md), [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md).

**Integration prerequisites:** 24–25. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [Dancer](space-navigator-design-spec.md), [MAP transactions](../hx/dahn-arch.md).

**Integration prerequisites:** 26. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [Dancer](space-navigator-design-spec.md), [MAP transactions](../hx/dahn-arch.md).

**Integration prerequisites:** 27. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [Dancer](space-navigator-design-spec.md), [MAP transactions](../hx/dahn-arch.md).

**Integration prerequisites:** 24–28 and commit contract. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [MAP transactions](../hx/dahn-arch.md), [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md).

**Integration prerequisites:** 24–29. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [Dancer](space-navigator-design-spec.md), [MAP transactions](../hx/dahn-arch.md).

**Integration prerequisites:** 30. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [MAP transactions](../hx/dahn-arch.md), [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md), [Path Inspector](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md).

**Integration prerequisites:** 30–31 and occurrence identity. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

Extend tests to close one occurrence, pan another off-viewport, and re-root into a second exploration tab under the explicit editing-transaction policy. Verify the authoritative staged state and Undo history remain available through their owner, including when no Inspector for the edited Holon remains open.

### Acceptance Criteria

- TypeScript does not create independent staged semantic copies.
- Visible occurrences cannot silently diverge semantically.
- Refresh after edit/Undo/Redo/Commit keeps occurrences coherent.
- Occurrence-specific presentation state remains independent.

---

# 11. Phase 8 — Create, Clone, and Delete

---

## PR 33 — Clone Holon

**Capability owners and design authority:** [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md), [MAP transactions](../hx/dahn-arch.md).

**Integration prerequisites:** Staged lifecycle and commit. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md), [MAP transactions](../hx/dahn-arch.md).

**Integration prerequisites:** 33 and concrete-type creation. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md), [MAP transactions](../hx/dahn-arch.md).

**Integration prerequisites:** Staged deletion and commit. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [Collection](../hx/visualizers/collection/kind-spec.md), [Table](../hx/visualizers/collection/table/design-spec.md), [PropertyMap / Value](../hx/visualizers/property-map/kind-spec.md), [MAP transactions](../hx/dahn-arch.md).

**Integration prerequisites:** 24 and typed array mutation. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md), [SDK](../hx/dahn-arch.md).

**Integration prerequisites:** Generic target discovery and binding. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [Collection](../hx/visualizers/collection/kind-spec.md), [Table](../hx/visualizers/collection/table/design-spec.md), [MAP transactions](../hx/dahn-arch.md).

**Integration prerequisites:** 37 and relationship mutation. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md), [MAP transactions](../hx/dahn-arch.md).

**Integration prerequisites:** 37 and singular relationship mutation. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md), [DAHN](../hx/dahn-design-spec.md), [SDK](../hx/dahn-arch.md).

**Integration prerequisites:** Effective Dance discovery and invocation. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Recorded status:** Superseded planning entry; delivery is tracked through the
[Load Holons implementation plan](../dancers/data-loader/data-loader-impl-plan.md).
The heading is retained for existing links.

**Historical Planned Dev Points:** 5. Do not add this estimate to the replacement
plan's PR estimates for the same work.

Load Holons retains semantic ownership with its affording `HolonSpace` and is
initiated from HolonInspector's action bar. The previously disabled actions were
an incremental delivery choice. Load Holons establishes the reusable initiation
contract for enabled holon-level actions; it is not moved to the Space Navigator
or Canvas action bar.

The replacement plan decomposes request preparation, canonical Dance invocation,
action interaction, Visualizer-owned result composition, diagnostics, committed
result inspection, and legacy entry-point retirement. It reuses the working
loader and preserves host source ingress without creating a second semantic
loading protocol. Retirement follows verified replacement coverage.

---

## PR 41 — Single-Holon Dance Results

**Capability owners and design authority:** [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md), [Path Inspector](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md).

**Integration prerequisites:** 40 and singular result binding. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md), [Collection](../hx/visualizers/collection/kind-spec.md), [Table](../hx/visualizers/collection/table/design-spec.md), [Path Inspector](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md).

**Integration prerequisites:** 40 and collection result binding. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md), [PropertyMap / Value](../hx/visualizers/property-map/kind-spec.md).

**Integration prerequisites:** 40 and response-shape contracts. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md), [DAHN](../hx/dahn-design-spec.md).

**Integration prerequisites:** 40 and adaptive reporting. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [Dancer](space-navigator-design-spec.md), [DAHN](../hx/dahn-design-spec.md).

**Integration prerequisites:** Dancer actions and adaptive reporting. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [DAHN](../hx/dahn-design-spec.md).

**Integration prerequisites:** Discovery, authorized loading, and execution policy. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

**Planned Dev Points:** 5

### Goal

Replace the bundled candidate source with federated MAP-native discovery.

### Scope

Discover Visualizer Commons reachable through applicable Space relationships.

Return eligible Visualizer Holons as candidate inputs to the Rust Selector.

### Acceptance Criteria

- Candidate population is not a centralized MAP-team registry.
- Accessible Commons are resolved through MAP semantics.
- TypeScript does not retrieve the full ecosystem simply to make selection decisions.

---

## PR 47 — Semantic Applicability over Discovered Visualizers

**Capability owners and design authority:** [DAHN](../hx/dahn-design-spec.md).

**Integration prerequisites:** 46 and slot-compatible applicability. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [DAHN](../hx/dahn-design-spec.md).

**Integration prerequisites:** 47 and validated preference selection. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [DAHN](../hx/dahn-design-spec.md).

**Integration prerequisites:** 48 and governed aggregate evidence. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [DAHN](../hx/dahn-design-spec.md).

**Integration prerequisites:** 47–49 and an explicit ranking/exploration policy. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md), [Path Inspector](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md), [MAP transactions](../hx/dahn-arch.md).

**Integration prerequisites:** Staged editing and axis compression. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

## PR 52 — Transaction-Aware Branch Closing Hardening

**Capability owners and design authority:** [Path Inspector](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md), [MAP transactions](../hx/dahn-arch.md).

**Integration prerequisites:** 18.d and transaction lifecycle. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

**Planned Dev Points:** 3

### Goal

Harden the branch closing delivered in PR 18.d against real transaction and collection state.

### Scope

Depends on PR 18.d and PRs 25/32. Exercise the existing close production with staged edits/deletion, shared semantic subjects, collection-mediated retained branches, and focus recovery. Do not define a new pruning grammar or treat removal of the last visible Inspector as transaction abandonment.

### Acceptance Criteria

- Closing presentation does not silently abandon staged semantic state.
- Remaining provenance stays coherent.
- Path Inspector reclaims branch layout space within its parent grant.

---

## PR 53 — Transaction Abandon/Revert

**Capability owners and design authority:** [Dancer](space-navigator-design-spec.md), [MAP transactions](../hx/dahn-arch.md).

**Integration prerequisites:** Staged transaction lifecycle. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

**Capability owners and design authority:** [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md), [Path Inspector](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md), [MAP transactions](../hx/dahn-arch.md).

**Integration prerequisites:** 35 and occurrence refresh. Existing detailed dependencies below still apply.

**Recorded status:** Planned in this document; delivery not re-audited.

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

PRs 14–18. Delivered; the composition/view extensions below are new work.

Result:

- singular traversal goes right;
- plural traversal goes down;
- occurrences preserve provenance;
- context compresses along both axes.

## Milestone C.1 — Composable Navigation Contexts

PRs 18.a–18.e (Phase 3A), building on delivered Milestone C.

Result:

- the surface can exceed the viewport, with independent pan/zoom and Zoom to Fit;
- local/Canvas/context focus requests respect authority;
- branches close independently and re-root opens a retained exploration tab under the same Space Navigator.

This proves reusable DAHN seams through the Space Navigator Dancer and selected Path Inspector/Holon Inspector/Collection set; it
does not define alternate lineage or compression semantics.

---

## Milestone D — Read-Only Usability and Initial Adaptation

PRs 19–22 and 23.a–23.e; PR 23.f extends the milestone with ancestry exploration
and recursive choice.

Result:

- sorting;
- filtering;
- Rust-provided ordering;
- personal reordering gestures;
- multi-level read-only Visualizer inspection;
- explicit Visualizer choice, usage selection, and safe occurrence replacement.

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
- arbitrary free-form Canvas layout and multiple sophisticated Window Manager placement policies;
- a complete generalized slot participation schema (the initial negotiation seam is required);
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

- bundled-candidate selection still goes through Rust Selector;
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

The immediate parent Canvas or visualizer determines placement within its grant; the Window Manager owns top-level display allocation. Child requests for more space propagate through parents. Path Inspector owns its navigation geometry, not the generic Canvas.

---

## 19.11 Independent Topology, Layout, and View Preserve State

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

Pan/zoom and off-viewport visibility must not mutate allocation or topology. Closing removes occurrence topology only; staged state belongs to its semantic owner. Re-root creates another exploration tab in the same Space Navigator by default and must not use the destructive root-replacement path. Test these dimensions independently rather than enumerating combined UI states.

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
    Window Manager context host and bounded Canvas shell
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
    navigate down with independent navigation surface / view transform
        |
    navigate right
        |
    compress provenance; pan / zoom / fit without reallocating
        |
    bounded focus, close branch, and re-root into another exploration tab
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

**Owners:** DAHN/Rust selector, SDK request binding, and owner-declared slots.
**Status:** planned correction; historical earlier delivery is not evidence of conformance.
**Dependencies:** PRs 1–3/S1 and the current slot/subject contracts; re-ground scope
and estimate before implementation.

Align implementation with [DAHN §14.2.1](../hx/dahn-design-spec.md#1421-slot-directed-descriptor-selection). Carry the actual slot through SDK, wire
binding and Rust selection. Validate parent-slot ownership when supplied. Read
accepted types from the slot instead of resolving a redundant requested-role key;
remove the post-selection scan of all parent slots. Stop applicability search at
the nearest local TKD, reporting missing matches and ambiguity explicitly.

Rename the property-map type, default instance, owned slots and references;
mark AcceptsVisualizerType definitional and regenerate schema bundles. Audit
default-candidate applicability at newly enforced TKD boundaries. Tests cover leaf
precedence, accepted-type inheritance, wrong-kind candidates, ambiguity, TKD
exhaustion, ownership, and no canonical role lookup. Keep Canvas launch and the
specialized collection-subject contract intact. Re-profile the same traversal.


## Deferred design and scope reconciliation handoff

The [F1 design record](../hx/dahn-docs-refactor-impl-plan.md#deferred-design-participation-contracts-and-occurrence-invocation)
is narrowed by the [bounded composition refactor](#22-bounded-visualizer-composition-refactor):
small required/offered Visualizer Operator contracts now have a proposed design.
A general contract execution framework, persisted occurrence model, and broader
affordance discovery remain deferred. Existing runtime participation is migrated
through the integrated increments below, not a parallel implementation sequence.
PR 18.c refers to [Issue 770](https://github.com/evomimic/map-holons/issues/770) and
[DAHN independent restoration](../hx/dahn-design-spec.md#independent-restoration-and-request-outcomes),
[Holon Inspector local actions](../hx/visualizers/node/holon-inspector/design-spec.md#local-region-maximize-and-restore),
and [Table participation](../hx/visualizers/collection/table/design-spec.md#participation-in-maximize-and-restore).
Its planned status here is preserved; this reconciliation does not verify delivery.

S1, PRs 3, 6, 18.a–18.e, 23.a–23.f, and 47 require issue-grounded scope review against
current slot ownership, direct label/value composition, candidate policy and
participation contracts. Except for the explicitly re-estimated PR 23.a–23.f track in Phase 5, existing
Dev Points remain historical planning values. No new delivery claim is made. Retired Property intermediary,
kind-only lookup, hard-coded fallback, and parent ownership of descendants must
not be reintroduced from historical acceptance wording.

Owner links identify each component's portion of a cross-component slice: DAHN
owns selection/runtime, parents own allocation, concrete Visualizers own their
presentation, and MAP owns mutation/transactions. Dependencies above are integration
prerequisites, not new evidence that their implementations conform. The Phase 3A
sequence and milestones remain the delivery order.


# 22. Bounded Visualizer Composition Refactor

## Proposal status and authority

This is the single delivery home for the refactor motivated by generic/loader
composition divergence. It is not a new enhancement issue or an implementation
start. Review, revise, and merge the documentation first; then ground the first
increment against the current implementation and estimate it. Existing PR numbers,
Dev Points, and recorded historical delivery remain unchanged.

Authorities:

- [DAHN Operator mechanism](../hx/dahn-design-spec.md#visualizer-operators-and-operations)
  and [coherent assignments/requests](../hx/dahn-design-spec.md#coherent-assignments-and-parent-requests).
- [Path policy](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md#441-node-inspector-slot-compression-contract).
- [Shared inspector composition](../hx/visualizers/node/holon-inspector/design-spec.md#shared-inspector-composition)
  and [local expansion](../hx/visualizers/node/holon-inspector/design-spec.md#local-region-maximize-and-restore).
- [Loader bindings](../dancers/data-loader/data-loader-design-spec.md#95-result-presentation-and-navigator-refresh).

Inputs are the read-only implementation assessment and the Node-slot counter-
proposal developed in the design discussion (`NodeSlotContracts.md` in the
request). No file by that name was found in the inspected checkouts; the supplied
proposal text is the design input, not a new normative document.

## Intentional changes and simplifications

| Previous contract or counter-proposal | Proposed treatment |
| --- | --- |
| Child/collection rendered extents size Path tracks | Explicit policy profiles and useful limits; local content measurement stays inside the Node grant. |
| Node receives axis states and matching retention flags | Only dimensions and canonical required capabilities; axes stay in Path policy. |
| Separate generic and loader layout | Shared composition and participation with specialized semantic bindings. |
| Suspended expansion intent, automatic resume, cancellation | Holon Inspector clears incompatible expansion; preserve content/navigation and restore within current grant. Other Visualizers may define different local policies. |
| Universal pixel compatibility thresholds | Provisional Path configuration, validated across supported themes and independent implementations. |
| Required new layout engine before integration | Extract only the deterministic geometry needed to remove competing sizing inputs; migrate the reviewed topology rules while preserving occurrence/reference seams. |
| General contract framework or persisted occurrence | Small Operator identity/binding contract; broader framework and occurrence persistence remain deferred. |

## Recovery and implementation assessment — 2026-10-15

**Recovered design:** [DevDocs PR #63](https://github.com/memetic-activation-platform/map-dev-docs/pull/63)
on `codex/visualizer-composition-contract`, still draft/unmerged when checked.
Its four published revisions are `bb23b60` (Operator/allocation design), `7659cd0`
(generic mechanism versus concrete policy), `bfb86f4` (bounded context/fallback),
and `2de3f40` (loader ownership/routing). No submitted GitHub review or approval
was present. These are proposals, not evidence of accepted or implemented contracts.
This continuation merges published main (`2aa072e`) without discarding its later
contracts or loader design. It remains draft for review, revision and re-review.

**Since that proposal:** DevDocs PR #66 and map-holons PR #796 merged on October 7,
settling loader request/evidence navigation and lifecycle fixes. DevDocs PR #69
merged October 11, publishing PR23 contracts; map-holons PRs #806 and #810 merged
usage/replacement on October 11. Main explicitly references #63 as deferred design
evidence, not adopted Operator schema. Its enduring parent-authority principle
coexists with rendered extent sizing. The original DAHN v2.5 title in #63 is now
reconciled to v2.11 after main v2.10; the Path v0.8 proposal is retained.

**Inspected implementation:** map-holons `409879c4` on
`codex/816-measurement-foundation`. No implementation edits were made during this
assessment. Findings below describe the checked files, not a claim to have run a
native application from every historical PR.

| Path / boundary | Confirmed code behavior | Required remaining delta |
| --- | --- | --- |
| Host → Canvas → experience/Path | `dom-canvas.ts`, `exploration-tabs.ts` and `composed-spatial-extents.ts` add chrome to upward spatial reports; `initial-window-allocation.ts` can enlarge the initial native window once | Policy-derived preference only, immediate owners and one framing contribution each; ongoing native growth stays optional VC-3 |
| Collection → generic Node → Path | Table `getCollectionViewportHeight(5)` and content-extent events feed `inspectorHeightParts()`/`getNodeInspectorExtents()`; Path `childExtents()`/`allocateRows()` turn these into shared tracks | Remove rendered-content feedback from Path; keep local measurement and responsive content behavior inside the grant |
| Properties → loader Node → Path | Loader reads preferred/scroll height and Collection rows in `getNodeInspectorExtents()`; content events reapply allocation and bubble spatial changes | Share internal allocation and stop the upward sizing path; preserve actual loader reads and reference contexts |
| Pending → selected destination | `PathNavigator.reserveDestination()` copies source Node extents to a placeholder, then target reports replace them | Reserve from Path policy/profile for the selected destination role; materialization fills the same grant |
| Track caches | Path retains prior `bandMetrics` maxima for matching states; viewport changes and extent events clear caches | Deterministic dimensions from explicit policy inputs; no measurement/history-dependent stabilization |
| Participation | `realize-node.ts` and replacement inspect private method names; no `ApplyNodePresentation` or required/offered Operator declarations found in executable source | Semantic contract identity plus Rust viability and materialized binding admission, preserving PR23 replacement |
| Composition | Generic and loader share title source code but duplicate body geometry; `getVisualizerComposition()` includes parent-owned regions | Bounded Title Bar selected-slot pilot, actual child inspection and reusable private geometry; tabs/rail migration follows |

No infinite measurement loop was established. Extent-event feedback and retained
maxima are confirmed competing inputs; oscillation, timing dependence, and every
possible native overlap remain risks to test rather than proven causes.

### Connections First evidence and disposition

Connections First was introduced in commit `06fcc57b` (October 9), part of merged
[PR #810](https://github.com/evomimic/map-holons/pull/810), as an alternate Node for
choice/replacement. `schema-src/dahn/schema.tdl` gives it nearer HolonSpace
applicability than generic Holon Inspector's HolonType applicability, so ordinary
automatic specificity can select it. It is not merely an opt-in test renderer.
Its source changes the generic body's rows to
`max-content max-content minmax(0, 1fr)` while inheriting collection reservation,
height allocation and region expansion logic from the two-row composition.

A temporary loopback browser fixture loaded the checked **shipped artifacts**,
without rebuilding or editing them. It supplied a HolonSpace-like title, two
Action buttons, two singular relationships, four Collection tabs, wrapping
properties, and an open scrollable Collection with an explicit 240 px local
five-row report. Theme-like 16 px/24 px text, 8 px gaps, and 160 px rail were
fixture values, not the complete application Theme. Three grants (800×396,
360×280 and 800×700) exercised seven distinct axis combinations plus full/full
restoration for each of generic, loader and Connections First: 72 assignments.
This fixture did not cover all nine combinations, real semantic loading or a
complete native Space Navigator traversal.

At 360×280 full/full, Connections First's body grant was 0 px, but its computed
rows were 70 px + 42 px + 0 px. Its action rectangle crossed the Collection
region by 62 px. The Collection region was 306 px high and extended below the
Node. A fresh mount reproduced the intersection before any compression cycle;
therefore stale compression state is not necessary for this failure. Reducing
only the fixture's Collection report from 240 to 80 px eliminated action/Collection
intersection across the same 72 assignments. This supports reservation pressure
plus uncontained intrinsic rows as the local failure mechanism; it is not a fix
or proof that all child bounds are valid. Generic also exceeded its short grant
with the fixed Collection reservation. Loader did not exhibit that specific
intersection, but retains the architectural upward path noted above.

The body has `min-height:0`, yet its content-sized tracks have visible overflow.
A child's overflow can therefore paint over its sibling even while the outer Node
clips to its own boundary. Other risks needing coverage include auto flex/grid
minimums, wrapped controls, absolute maximize controls and fixed popover placement.
A positioned popup is legitimate only under an explicit bounded overlay contract.

**Disposition:** retire Connections First from the normal bundled candidates in
VC-1 instead of fixing it. Retain its failure pattern as evidence and replace its
role in selection tests with independently authored conformance fixtures. Removal
alone does not repair generic/loader allocation or prove the new policy. Withdraw
its declarations, artifacts and generated references coherently; assess saved
VisualizerUsage/preferences in existing spaces through normal Rust eligibility
and explicit unavailable-choice outcomes, never a hard-coded UI fallback.

### Issue #807 foundation and delivery boundary

[Issue #807](https://github.com/evomimic/map-holons/issues/807) is open architectural
design, not an accepted implementation-ready mandate. Its component=slot proposal
addresses agent substitution and honest inspection; shared code alone supplies
neither. This design adopts the bounded shared Title Bar pilot as the structural
foundation of VC-1. DAHN owns the component criterion, constraint openness and
actual selected-child correspondence; the Holon Inspector owns the concrete
Title Bar contract. Private allocation helpers remain private implementation.

The pilot is integrated with working downward allocation and visible containment
in generic and loader inspectors. It must not land as an abstract registry while
the demonstrated sizing paths remain active. Do not require universal component
migration, new Row semantics, or final resolution of every #807 question before
that working integration. Tabs/rail delegation needs later reviewed component contracts and migration;
the component=slot target principle is accepted in the design review below.
#807 is not declared completed by this pilot.

**Recommended first increment:** VC-1 with a selected Title Bar, explicit Operator
admission, shared generic/loader internal composition, deterministic Path policy
tracks, stable pending rectangles, and Connections First retirement. Carry the
minimum deterministic bounded fallback/overflow needed to honor constrained grants in
this increment; VC-2 may refine the moving selected-context viewport but cannot
be used to postpone removal of competing track inputs. Reuse logical placement
and reference/lifecycle work already delivered. If grounding exceeds one coherent
unit, split by working generic integration and working loader adoption, with an
explicit temporary loader adapter that consumes the same downward contract and
never feeds child extents back to Path. Do not create a schema-only first slice.

**Observed validation:** Six existing focused artifact/runtime test files passed
142 tests using the verified bundled arm64 Node runtime. Those jsdom tests did
not establish browser containment; the real-browser probe above failed despite
their passing baseline. No implementation, enhancement issue or runtime fix is
claimed by this documentation continuation.

### Required verification for the first implementation issue

Use the current artifact/runtime/selector infrastructure and one small reusable
conformance fixture. Its browser assertions must measure immediate child bounds,
sibling paint/hit overlap and keyboard recovery, not merely CSS strings. Include:

- Generic and loader presentations; the historical Connections First overlap
  pattern remains a regression input after its production candidate is removed.
- All nine axis combinations, mixed independent Nodes sharing row/column tracks,
  larger inactive intersections and intentional final-track capability richness.
- Right → down → right → down, reverse turns, older focus restoration and retained
  alternatives, using the existing worked policy cases and bounded protection.
- Narrow/short and below-minimum grants, wrapping and multiple supported text scales;
  pan/scroll recovery, visible overflow cues and no automatic zoom or infinite shrink.
- Pending-to-materialized transitions with equal policy rectangles; different target
  content and completion order cannot resize tracks through rendered reports.
- Expansion followed by compression/resize: incompatible local emphasis clears,
  restore uses current grants, title/subject/occurrence/selected-child/edit state survives.
- Title Bar alternatives selected through Rust, occurrence-local replacement and
  inspection, incompatible offers/missing bindings, stale targets and explicit failure.
- Loader retained request/parser/no-response/typed-evidence flows, committed-review
  failure with independent materialization, actual reference-owner routing and draining
  dependent work before disposing presentation/loader contexts.

Numeric profile checks establish finite positive ordered extents and channel
budgets. Browser conformance establishes behavior for the supported fixture/Theme
set; neither proves universal usability of arbitrary Visualizers. Preserve this
separation in the issue and its review evidence.

## Feasibility and migration seams

The following paragraph retains the 2026-10-06 participation-interface baseline;
loader-specific delivery is reconciled in the dated assessment below.

The 2026-10-06 source inspection found a coherent dimensions-plus-axis call in
`host/ui/src/dahn/contracts/node-inspector-slot.ts`; evolve it to dimensions plus
capabilities rather than retaining duplicate representations. Existing
`presentation.ts`, `context-host.ts`, and VisualizerElement request callbacks
provide explicit outcomes and immediate-owner binding mechanisms. They do not
provide a complete ongoing preferred-extent request chain.

`PathNavigator` already owns occurrence/reference identity and traversal state;
`traversal-layout.ts` owns logical placement. Preserve occurrence/reference identity,
but migrate placement to the reviewed whole-band/source-adjacent rules below.
`path-inspector.js` still combines pixel allocation with child measurements and
band caches. Generic and loader inspectors duplicate geometry. PR #796 has since
landed retained LoadRequest/diagnostic/evidence navigation, ordinary response
collections, selected PropertyMap support and independent presentation routing.
Preserve those bindings; do not schedule them again as missing work. Remaining
injected Action-owned result projections and Node-owned ordinary relationship
collections are different paths: ground any migration against the actual owning
slot and selector parent, not the old blanket Action-owned diagnosis.

`schema-src/dahn/schema.tdl` supplies HasSlot/accepted type/applicability and
implementation identities. `host/crates/dahn_selection/src/selection.rs` owns
candidate filtering. `materialized-visualizer-runtime.ts` owns materialized
composition. Add required/offered contracts to those seams; a bound Operator is
not another SDK command or transaction protocol. Shared implementation packaging
must work with verified, materialized artifacts, not unresolvable relative
imports from loaded source blobs.

The authoritative direct PropertyMap/Value composition and the current code's
Property intermediary are an existing separate mismatch. Do not expand this
refactor into retiring that intermediary. Ground selected chips against the
then-current supported PropertyMap boundary and preserve selector authority.

This is a feasible integrated change, but schema declarations, Rust filtering,
materialization, and both inspectors must move together. The first slice below
is the minimum working integration, not merely an Operator registry. If grounding
shows it exceeds a coherent reviewable unit, split by generic integration first
and loader adoption second, each with visible working behavior; do not ship a
schema-only abstraction slice. No final Dev Points are assigned at this design step.

## VC-1 — Coherent Node assignment and shared generic/loader geometry

**Working behavior:** Both generic and loader roots receive one capability
assignment, preserve state through every Path context, and share rail, collection,
expansion, and restore behavior. Properties chips can be selected through a real
PropertyMap boundary. Pending destinations no longer borrow measured source sizes.
Their Title Bars are real selected children under the bounded Issue #807 pilot,
and their regions remain contained under constrained grants. Connections First
is retired rather than repaired.

**Affected components:** DAHN schema source and regenerated imports (implementation
phase only), Rust selection compatibility, materialized operation bindings, Node
participation interfaces, Path allocation, generic/loader inspector composition,
loader result binding adapter, Title Bar slot realization/replacement/inspection,
Connections First registration/artifact retirement, and existing UI/selector fixtures.

**Dependencies:** Accepted design; current integrated loader/reference work available
on the implementation base; existing verified artifact materialization and Rust
slot selection. No new core reference capability, transaction behavior, ongoing
window negotiation, or persisted occurrence is a prerequisite.

**Scope and compatibility:** Introduce the small required/offered Operator graph
using supported TDL and regenerate normally. Use a fixed Operator identity for the
Path-owned input/result contract. Generic invocation remains contract-relative
and does not require every Operator to be synchronous. Migrate required slots
and bundled candidates together;
missing offers fail selection and missing callables fail materialization explicitly.
An implementation-local adapter can bridge old methods during transition, but must
not advertise unsupported behavior or become a second allocation authority.
The Title Bar pilot is the component=slot foundation for this increment, not a
prerequisite to finish every component migration in Issue #807. Reuse current
slot-directed selection, usage matching and occurrence replacement. Shared layout
helpers allocate only immediate child slots; selected Title Bars receive their
own band and identity-bound presentation operation. No new global composition
engine or universal Operator protocol is required.
Remove rendered child reports from Path sizing. Use one validated initial profile
and implement the reviewed deterministic logical placement rules. Extract a pure pixel helper in this slice
only to the extent necessary to make its dimensions deterministic.

**Acceptance criteria:**

- Title Bar slot selection uses Rust and actual owner/subject/Theme inputs. Two
  independently authored alternatives (inline identity/actions versus compact
  identity with an accessible action menu) fulfill the same contract. Replacement
  changes only the title, with actual child inspection, revoked stale targets and
  containing Node/transaction/other-child state preserved.
- Generic and loader selection pass explicit required/offered checks; incompatible
  candidates and lying materialized implementations fail at the correct boundary.
- All nine policy combinations derive canonical capability assignments. Both-context
  retains both navigation capabilities; compact retains identity and restore.
- Shared-track dimensions satisfy the final aggregated requirements; a destination
  or retained source is not erased by another cell's minimal request.
- Rail width caps/right alignment, collection surplus, and local scrolling agree
  between both inspector bindings. Include a non-table Collection fixture.
- Incompatible Holon Inspector expansion clears once; content, selection, edit state, and bound
  references survive. Restore and attention use current grants, not saved pixels.
- Assignments do not invoke Dances, fetch geometry data, change selection, or
  reconstruct occurrences. Pending and materialized rectangles agree.
- Loader diagnostic/review/outcome bindings and transaction ownership survive,
  including the merged retained-request and typed-evidence behavior from PR #796.
- Real browser bounds checks show no sibling paint/input overlap; short grants,
  intrinsic wrapping/minima, positioned controls and recovery paths are covered.
  A hidden or clipped but unreachable required control is a failure.
- Connections First no longer participates in normal bundled selection/discovery.
  Remove its authored declarations/source and regenerate bundles normally. Preserve
  explicit-choice/replacement coverage through independent test candidates; handle
  stale saved usage/preference explicitly without substituting a renderer in UI
  code. Ground persisted-resource withdrawal for existing spaces before removal.

**Verification:** Start with a reusable allocation-conformance fixture that mounts
an independently selected Node/Title Bar and a non-table Collection under explicit
grants, using real browser rectangles, paint/hit containment and keyboard recovery.
It exercises the same public Operator binding path as production; it must not
read private region names to establish compatibility. Component-specific assertions
may inspect their own test handles. Keep one expected-failure historical probe for
the retired Connections First pattern as evidence without shipping that Visualizer.
Extend existing artifact and runtime tests plus Rust selector
fixtures; use narrow web checks and meaningful browser containment/keyboard
checks. Run appropriate schema compilation and host/hApp checks if generated
contracts reach those consumers. Reuse a small independent Node fixture with
explicit Operator bindings and a non-table collection; it should not need private
methods or a comprehensive new test framework. Inspect real generic and loader
renderings, not only CSS/class assertions.

**Exclusions:** New reference/IPC lifecycles, loader execution changes, legacy ingress
retirement, duplicate-head repair, Linux picker work, Property intermediary
retirement, general Operator execution framework, automatic window growth,
Commons discovery, and changes to unrelated Visualizer families.

## VC-2 — Bounded moving viewport and profile fallback

**Working behavior:** Repeated horizontal/vertical exploration keeps a bounded
preferred context window; mixed/branching paths aggregate shared tracks correctly;
smaller viewports retain useful geometry and recoverable history.

**Affected components:** Path navigation policy, deterministic pixel helper if not
already extracted, connector presentation, profile configuration, viewport/view
integration, and browser navigation fixtures.

**Dependencies:** VC-1; existing focus/provenance and pan/scroll/zoom. Preserve
reviewed logical placement and mounted Node instances. No native-window API is required.

**Acceptance criteria:** Mature chains use minimal + partial + full preferences;
short paths count only present tracks; mixed turns follow the same explicit rules.
Fallback first moves oldest context offscreen, then reduces budgets within useful
limits, then scrolls. No silent state compression, automatic zoom, or history
removal. Connector labels retain accessible provenance. Wide/tall shared tracks
exercise different surplus rules. Pure geometry outputs repeat for identical
explicit inputs. Use the reviewed stable per-state sizing policy; actual intervening historical
tracks must not determine the reduction factor; no
history-dependent stabilization or adaptive weighting is introduced.

**Verification:** Pure policy/geometry fixtures for chains, turns, shared tracks,
retained alternatives and close/restore; browser tests across narrow grants,
multiple themes/text scales, and active attention resize. Assert identity/state
survival and operation counts as well as rectangle containment.

**Compatibility/exclusions:** Profile values remain configurable and provisional;
validate useful bounds rather than treating example pixels as semantic eligibility.
Do not add a global layout service or change zoom into compression. No ongoing
preferred-window request chain or broad protected-context framework.

## VC-3 — Optional preferred-extent propagation through composition

**Working behavior:** A composed experience can request a policy-derived preferred
viewport from its immediate owner, with explicit unsupported/refused outcomes and
actual grants delivered separately. Human-invoked expansion remains usable when
native resizing is unavailable.

**Affected components:** Parent request capability, hosted composition/Canvas,
Window Manager adapters, and initial-window allocation integration.

**Dependencies:** VC-1 and settled VC-2 profile behavior; existing ContextHost
allocation/results. This is not a prerequisite for the first working increment.

**Acceptance criteria:** No owner is bypassed; each adds its framing once. Accepting
a preference is not a grant. Refusal preserves current presentation. Host resize
flows down through current allocations, and restore preserves topology/state.
Ordinary traversal does not repeatedly grow a native window.

**Verification:** Nested-host fixtures with accepted, refused, unsupported, and
constrained grants; application smoke check where supported. Exclude automatic
native-window growth and a general multi-window ecosystem.

## Review decisions and recommendations

These are reviewable recommendations embodied in the proposed specifications,
not concealed implementation choices. Amend the authoritative spec if changed.

| Decision | Recommended answer and consequence |
| --- | --- |
| Path Node-slot capability vocabulary | `inspect`, singular navigation, plural navigation, active collection; identity/restore unconditional. No Node axis input. |
| Minimal dominance | Yes, only after max-per-track aggregation; compactness never removes required source/target capability. |
| Mixed-direction context | Retain the latest source on each active-lineage axis; protect the immediate source and destination without permanent expansive claims for alternatives. |
| Partial/partial | Retain both capabilities recoverably. Validate the smallest configured rectangle with an independent fixture. |
| Holon Inspector expansion after incompatible assignment | Clear it for this implementation. Other Visualizers may explicitly support suspension/resumption. |
| Node attention | Temporary bounded normal-inspection projection; restore current grid, clear attention if resized below useful limits. |
| Schema naming and stewardship | DAHN-defined describing/invocation mechanism with independently contributed contracts. Slot owners choose requirements; contributors promise offers. Confirm executable keys during grounding without centralized contract approval or repurposed Core query semantics. |
| Numeric profiles | Do not ratify the counter-proposal's pixels as universal promises. Choose and validate one desktop profile in VC-1; exercise reduction in VC-2. |
| Layout helper extraction | Necessary deterministic allocation first; broader reusable helper only when it removes competing sizing inputs or duplication. |
| Viewport negotiation | Optional VC-3; initial allocation and manual recovery suffice for earlier increments. |

The existing issue sequence contains historical estimates/status and earlier
contracts. VC-1–VC-3 supersede only the allocation/composition deltas identified
here; re-ground dependencies before creating the first enhancement after design
acceptance. Do not infer delivery or close existing work from this documentation.


## Documentation validation record

For this proposal, all five portal builds in `.github/workflows/pages.yml`
completed successfully using temporary output directories. Comparison against
published main introduced no new warnings or link/anchor diagnostics. All 19
added relative links/fragments resolve, and `git diff --check` passes.

Strict Core build is not clean: its pre-existing missing
`data-loader-source-verification.md` link remains a warning. The source file is
uncommitted in the separate working checkout and is deliberately not imported.
The Roadmap portal retains two existing cross-portal-link warnings; existing
anchor diagnostics are also unchanged. These are baseline limitations, not
validation of runtime behavior. No executable schema, runtime, or application
configuration was changed or tested by this documentation proposal.


## Generality review revision

The design separates reusable mechanisms from concrete contracts. DAHN owns
Operator declaration, identity-based binding/admission, contract-relative input
validation, generic allocation authority, and failure reporting. Operator
contracts may be independently contributed and stewarded; incompatible revisions
use distinct identities. Synchronous and asynchronous contracts are both possible,
without adding asynchronous infrastructure to this refactor.

Path's Node-slot contract alone defines its dimensions/capabilities input,
canonical sets, synchronous completion, and receiver identity convention. Path
policy owns track sizing, useful limits, matrix, viewport, and fallback. Holon
Inspector alone owns rail/collection layout and clearing incompatible expansion.
Family specifications retain semantic promises without promoting these concrete
policies. VC-1 integrates these owners; it does not universalize their signatures.

Conformance fixtures should demonstrate the distinction: generic admission checks
an Operator's declared contract and bindings, while Node-specific fixtures check
Path capability combinations and synchronous allocation. Holon-specific fixtures
check expansion clearing; another explicitly conforming Visualizer is not rejected
merely for supporting suspension/resumption. Geometry tests must not prohibit
later authorized content loading through ordinary interaction/data binding.

No new unresolved placement decision is introduced: the concrete Node contract
stays with Path until broader family applicability is demonstrated. Final schema
keys and profile values remain implementation-grounding decisions already listed
above. Distributed stewardship is a mechanism requirement, not an additional
central approval workflow.


Generality revision validation: all five portal builds pass with no new warnings
or link/anchor diagnostics relative to the preceding proposal. All four newly
introduced relative links/fragments resolve and `git diff --check` passes.
Strict Core remains blocked only by the previously recorded missing-document
warning. No runtime or executable-schema validation is claimed.


## Historical Path allocation clarification revision (superseded sizing details)

The dated design review below supersedes this revision's terminal-placement and
actual-intervening-span sizing details. Retain it as proposal history only.

VC-1 follows the required Path Node Operator contract, including synchronous
validation/acceptance and explicit rejection preserving the last valid assignment.
Its structural profile checks validate positive finite ordered dimensions and
channel budgets, not arbitrary Visualizer usability. Behavioral checks cover the
shared inspector, explicit minimum/preferred allocations, every required capability
combination, and relevant Theme/text-size configurations without live negotiation.

VC-2 uses the [worked protection cases](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md#worked-protection-and-aggregation-examples)
as policy fixtures: continuing chains, both alternating-turn directions, older
focus restoration, and retained alternatives. Assert per-step protected/compact
roles, final track states, derived capabilities, and selected versus off-viewport
context. Shared-track overprovisioning is intentional; do not introduce a hidden
per-occurrence presentation clamp. Richer assignment alone must not fetch content.

The preferred request covers policy-selected context and actual intervening
geometry, not all history. Test common-factor reduction independently per axis,
fixed framing, P=M, grants below minima, compact context whose removal does not
shrink one axis, and shared tracks containing inactive cells. Moving history out
of the preferred view must leave its logical cells and connectors retained.

Collection-region creation, switching, and placement stay in the selected Node.
Path reserves a destination only for the selected Holon member's navigation intent.
Test with a substitute Node that places collections differently from Holon Inspector.

Review recommendation: retain the bounded latest-source-per-axis rule and one
older compact context, with intentional final-track overprovisioning. A long mixed
path may span a large actual footprint despite at most two protected sources;
accept pan/scroll recovery rather than a new compaction or protection framework.
Profile values and supported theme/text-size fixtures remain implementation-grounding
decisions. No other contract-placement change or implementation work is introduced.


Path clarification validation: all five portal builds pass with no new diagnostics;
all five added relative links/fragments resolve; `git diff --check` passes. An
independent temporary calculation checked all 17 worked rows (protected and compact
roles, track states, capabilities, and selected context) against the stated rule,
plus interpolation endpoints, below-minimum overflow, and P=M. This checks the
document's examples, not runtime implementation. The existing strict-Core missing-
document warning remains unchanged.


## Historical loader ownership and context reconciliation (2026-10-07)

The findings below predate merged PR #796. The 2026-10-15 assessment supersedes
claims that request roots, independent materialization, and ordinary result slots
are still absent. Retain the ownership/lifecycle requirements as constraints.

VC-1 includes the single [resolved composition and phase/context contract](../dancers/data-loader/data-loader-design-spec.md#81-composition-and-slot-ownership).
The Action owns preparation/submission, workflow lifetime, and disposal coordination;
the selected response/report Node owns presentation slots and bindings; shared
inspector code supplies geometry; Path owns occurrences and tracks. The experience
owns the load tab and its Rooted Navigation role. Do not conflate these owners.

Verify remaining Action-owned projected-result paths separately from the Node-owned
ordinary relationship path delivered in PR #796. Migrate only an actual remaining
ownership mismatch, with saved slot declarations and selector parent inputs together. Reuse the
existing presentation context for realization when committed review is absent or
fails; do not make parser/no-response feedback depend on `openCommittedReview()`.
Route actual subjects by bound ownership and materialize saved executable resources
in an open eligible context. An unsupported target owner fails locally rather than
being rebound to the saved review. Preserve the [dependency-ordered teardown](../dancers/data-loader/data-loader-design-spec.md#43-cancellation-and-dismissal).

Reference reusable definitions in DAHN for Action selection and destruction guards,
Commands for runtime admission/disposal, and Collection kind for projected-input
witnesses. The witness's empty envelope is not displayed membership; verify explicit
unsupported-input failure and stable row/actual-handle separation without Table
fallback. Do not introduce a universal action framework or new transaction merely
to reconcile documentation.

The loader plan's latest historical estimate is 70 (earlier 68 plus DL-10's two-point
revision). Its tables are historical decomposition, not remaining work. Reuse the
integrated loader capabilities evidenced by PR 791; follow-on local edits are not
claimed merged. All shared-composition/context-routing deltas are counted here,
not again as fresh DL-08/DL-12/DL-13 scope. Issue grounding after design acceptance
must size only the remaining integrated delta.

Loader reconciliation validation: all five portal builds pass, with no new warnings
or link/anchor diagnostics against the preceding revision. All 15 added relative
links/fragments resolve; `git diff --check` passes. The stale Commands-to-loader
anchor is corrected. Strict Core still reports the existing missing source-
verification document; Roadmap retains its two existing cross-portal warnings.
These are documentation checks, not runtime conformance evidence.

Review must ratify the Node-owned slot migration and independent reuse of the
existing presentation context. Exact persisted slot keys, implementation sizing,
and runtime phase/routing tests remain subsequent grounding work after acceptance;
there is no unresolved competing slot owner or requirement for a new context.


## Continuation validation — 2026-10-15

All five CI portal builds (Core, DAHN, Mapp Dev, Glossary and Roadmap) pass from
this branch. Comparison against published main `2aa072e` adds no link/anchor or
warning diagnostics. Core retains eight existing informational fragment diagnostics,
Glossary six, and Roadmap two existing cross-portal warnings. The older missing
loader-source-verification warning is resolved by the main merge; the historical
validation paragraphs above describe their own earlier baselines.

The 17 worked protection/aggregation rows were independently recalculated against
the stated ancestry rule, including final-track capabilities. Common-factor
reduction endpoints, an interior allocation and below-minimum overflow were checked.
These validate design examples, not application conformance. `git diff --check`
passes. Six focused existing web suites pass 142 tests with arm64 Node; the browser
probe still reproduces current-code overlap as recorded above. Runtime fixes and
the complete planned browser conformance matrix remain future implementation work.

Review recommendations added in this continuation are the bounded Issue #807 Title
Bar slot contract and independent alternative, keeping geometry helpers private,
retiring Connections First, preserving merged loader/PR23 behavior, and requiring
contained working allocation in VC-1. Measure added selection/materialization
cost at Node creation and child replacement; allocation/resize must cause zero
semantic selection/materialization calls. No broad component migration, new issue,
implementation change or merge is authorized by completing this documentation step.


## Design review decisions — 2026-10-15

This is a chronological review record. Later decisions supersede earlier open
questions and recommendations. The owning specifications contain the reconciled
contracts. Accepted directions here do not imply approval/merge of the whole PR.


### Component=slot target architecture — accepted direction

The project owner accepted component=slot as the target architecture for every
identifiable experiential component, with private layout/binding machinery outside
the criterion. Title Bar is the first implementation, not the sole architectural
exception to private regions. This records one settled review decision; the
remaining contracts, delivery scope and the draft PR as a whole still require review.

Temporary migration exceptions are explicit: the current implementation-owned
Title Bar remains until VC-1; Collection Tabs and singular-navigation Rail remain
until their subsequent component migrations. Existing Table-owned row exclusions
must be reviewed against the criterion before their disposition is settled; no
RowVisualizer kind is introduced by accepting the principle. Implementation issues
must identify exceptions they retain and their intended migration/review boundary.
Do not claim independently selected child identity for an unmigrated region.


### Experiential component criterion — accepted direction

Meaningful independent substitution determines the boundary: replace a presented
role while preserving the containing experience. Visual separateness and source/DOM
structure are not the criterion. Title Bar, Collection Tabs and Navigation Rail
qualify; ordinary layout wrappers/calculations and binding adapters do not. Table
headers, rows and other ambiguous roles still need review against this criterion;
these examples do not silently approve a RowVisualizer kind or a permanent exemption.


### Title Bar semantic subject — accepted; augmentation open

The project owner confirmed that the Holon is the Title Bar's semantic subject,
while allowing consideration of Visualizer-related aspects in its presentation.
Whether these are explicit context/bound references or a richer subject projection,
and their effect on selection, remain open. Do not infer an accepted composite
subject, new occurrence Holon, or usage-matching dimension from this decision.


### Subject-preserving presentation actions — accepted direction

Augmentation must not change the Title Bar's semantic subject. The standard
Explore-from-here, Close, Expand/Restore and Show Visualizer actions are afforded
by the presentation contract independently of that Holon's subject affordances.
The project owner proposed a Title Bar-owned action-icons slot. Selection and
invocation for presentation actions must not assume a Dance afforded by the
subject. Slot granularity, action targets, availability and constrained-presentation
behavior are subsequent review decisions; the standard set must not be inferred
from the Holon's type or private callbacks.


### Central declaration of required Title Bar actions — accepted requirement

The standard action set must be specified once and take effect across participating
Node Visualizers without HX developers remembering to copy/include it. Use the
shared Title Bar role contract and required Title Bar Actions child role; shared
composition resolves the canonical membership and binds occurrence-specific
operations. Per-Node callback/action lists must not become competing authorities.
VC-1 must cover propagation of a changed shared declaration, explicit failure for
missing required membership/bindings, and behavioral accessibility conformance.
Exact executable keys and version/adoption handling require grounding; ordinary
installed-contract lifecycle applies, not an implicit live update across spaces.
Specialized Nodes may declare additive actions under the accepted extension rule below.


### Additive Title Bar action extensions — accepted direction

Specialized Nodes may add explicitly declared presentation actions alongside the
shared mandatory standard set. Extensions cannot remove, replace or redefine
standard identities or meanings. Shared composition resolves membership and checks
bindings rather than relying on each renderer to concatenate its own copy.
Verification must include a specialized addition, propagation of a shared-set
change and explicit rejection of attempted standard-action replacement/removal.


### Inspection access versus visible v controls — clarified direction

The project owner identified permanent v controls on every selected Visualizer
as a potential source of visual clutter. Universal inspectability does not require
universal direct icon display: some children may be accessible only through their
parent's VisualizerInspector. Preserve actual child identity and a reachable
keyboard-accessible entry point through the composition. The accepted ownership rule is recorded below.
This distinction does not remove inspection from the standard action contract.


### Direct v display ownership — accepted direction

Each selected child owns responsive display of its own direct v control. Its
immediate composition owner guarantees recursive inspection of the actual child
selection; the enclosing experience preserves a discoverable keyboard-accessible
entry point. No universal pixel threshold or parent manipulation of private child
controls is required. Inspection action membership remains centrally declared.
Coverage must include suppressed child controls, nested access to their actual
selections, and a usable entry point under constrained grants.


### Inspector-to-display correspondence — requirement raised; highlight design open

The project owner identified the need to connect information about Visualizers in
VisualizerInspector with the real estate occupied by their displayed occurrences.
Region highlighting on interaction with an inspector entry is the proposed means.
The same selected Visualizer/subject may have several occurrences, so correspondence
must use the actual occurrence/slot binding rather than definition identity alone.
Existing inspection targets already carry occurrence identity, live element and
liveness checks; this is substrate, not evidence that highlighting is implemented.
The highlight's geometry, interaction/lifetime and behavior for clipped/off-viewport
or replaced targets remain review questions. This does not yet settle which
selection the standard Title Bar Show Visualizer action targets.


### Shared choice scope and affected-region highlighting — review correction

The project owner intends a slot's Visualizer change within a context to affect
all instances sharing that selection, and therefore wants inspection to reveal
all affected display regions. A definition-wide or single-occurrence-only highlight
would not necessarily represent that scope. The exact shared-selection key remains
to be resolved, including reused slot definitions with different subject bindings.

This differs from the inspected implementation: PathNavigator replacement prepares
and publishes one captured occurrence, and DAHN §14.7 currently defines choice as
occurrence-local while distinguishing remembered preference/shared usage. Existing
Table column selection already applies a selected Value Visualizer across its
cells. Do not claim general live context-wide replacement is implemented. Resolving
the intended shared choice scope must precede highlight semantics and sizing of
any resulting replacement work; it may change the previously preserved PR23 contract.


### Issue #746 session choice scope — recovered design dependency

[Issue #746](https://github.com/evomimic/map-holons/issues/746), still open when
checked, already proposes Rust-owned session presentation choices keyed by the
actual leaf subject descriptor, normalized slot compatibility contract and explicit
presentation context (Theme/MDS plus optional discriminator). Concrete slot/parent,
DOM occurrence, transaction and available geometry do not partition it by default.
Thus equivalent String-column bindings can share a session choice across columns;
a column-specific partition is not the default proposed by #746.

Its explicit-choice rule updates subsequent matching requests, while already-mounted
occurrences retain their current implementation/state unless the agent explicitly
requests application to open views. This is distinct from the project owner's
proposed live all-instance effect and must be reconciled rather than asserted
already provided by #746. Durable preferences remain another scope/lifetime.

Use #746's semantic scope as the basis for affected-region preview rather than a
new UI-local grouping key. Reconcile its older acceptance-set-only normalization
with the required/offered Operator compatibility now proposed here: accepted-type
equality alone cannot establish equivalence when required participation contracts
differ. Transient pixel grants remain outside session choice identity. Exact
normalization and explicit open-view application semantics require design review;
the issue's historical TypeKind boundary references are not current selector authority.


### Explicit application to matching open views — accepted direction

The project owner accepted the recommended distinction: session choice updates
subsequent matching presentations; replacing existing matching open views requires
an explicit Apply action with affected-region preview. Keep locating one occurrence,
updating the session choice, explicit application to mounted occurrences and durable
preference persistence distinct. Shared scope follows the reconciled #746 contract,
not a new UI-local column/DOM grouping. The atomic publication policy is accepted below; its
delivery separation is accepted below; this decision does not
claim #746 or multi-view replacement is implemented or automatically add it to VC-1.


### Atomic application to matching open views — accepted direction

The project owner agreed that any targeted replacement failure leaves every
targeted mounted view unchanged. Prepare/validate all before publishing any;
unsafe dismissal, failed initialization or inability to preserve required state
blocks the batch with explicit feedback. Dispose unpublished preparations without
damaging live views. The independently selected session choice remains in effect.
This is presentation publication, not MAP Commit or a new distributed semantic
transaction. Verify a failing member among otherwise-ready replacements, active
workflow guards, retained edits/selection and cleanup of unpublished resources.
Delivery separation is accepted below; target-set capture/revalidation remains follow-up design.


### First-slice delivery boundary — accepted direction

The project owner agreed to keep #746 session choice memory, shared-choice affected-
region preview and atomic application to matching open views out of VC-1. Their
intended behavior remains in the design; implementation follows as separately
grounded work. VC-1 delivers downward allocation, shared inspector geometry,
selected Title Bar/Title Bar Actions composition and Connections First retirement.
Preserve actual occurrence/slot bindings and existing explicit occurrence-local
replacement; do not add a temporary UI-owned shared selection mechanism.

Ordinary occurrence-location highlighting remains a distinct potential capability;
this scope decision does not imply that complete shared-scope previews or batch
replacement must be delivered to correct layout. Ground the first issue only after
the remaining allocation/action contracts and review of this documentation settle.


### Standard action membership and availability — accepted direction

The project owner confirmed that standard actions remain members of the shared
set when unavailable. Their owning authority supplies availability and a reason;
the selected Actions presentation makes that state discoverable without requiring
a permanent icon. Protected-root and active-workflow closure cases must not be
confused with missing required bindings. Verify both legitimate unavailability
and explicit admission failure for an omitted binding, preserving recursive
inspection access when a direct v is suppressed.


### Path topology reconsideration — prerequisite to compression-policy acceptance

The project owner proposed a simpler band-insertion model: first rightward
navigation extends the source row with a new column; first downward navigation
extends the source column with a new row. In the discussed A→B, A↓X, B↓C case,
B↓C inserts a row before X and pushes X's row downward, rather than placing C
alongside X. A subsequent selection from the same source replaces the destination
cell's contents. The effect when that destination already has descendants remains
a review question; do not assume authorization to discard a retained branch.

This differs from current branch-local group insertion/terminal append in grammar
§2.4 and `traversal-layout.ts`: current placement moves retained branches on their
lateral axis as needed and does not always insert a whole grid band. Current
`PathNavigator.commitDestination()` replaces an untraversed leaf, but preserves a
previously traversed destination as an alternative. Both distinctions need explicit
resolution before finalizing topology and deriving compression from it.

The previous four-cell shared-track example is not an agreed target topology.
The 17 existing worked rows validate the previously proposed policy only; rework
placement, examples, retained-history behavior and related scope assumptions if
the band-insertion decision supersedes that policy. No topology code is changed
or new insertion rule silently treated as accepted by recording this discussion.


### Destination replacement versus branch retention — accepted direction

The project owner explicitly retained the existing distinction: a new selection
replaces an untraversed destination; a destination traversed onward is retained
with its descendants as an alternative. Existing dismissal/state-safety guards
continue to apply. The proposed band-insertion model must preserve this rule.
This settles retention, not the replacement/retained branch's coordinates or
whether repeated same-provenance selections use source-adjacent versus terminal
placement. Those placement rules remain under review.


### Source-adjacent placement of new destinations — accepted direction

The project owner agreed that every newly selected new destination takes the
source-adjacent position, including another selection through the same relationship.
Explored prior continuations move outward intact; untraversed prior destinations
are replaced under the retained safety rule. This supersedes same-group terminal
append and first-member spatial-anchor policy in the existing grammar/code.

Grammar §2.4 records this decision. Reconcile its other spatial definitions,
examples and invariant summaries after whole-band insertion and retained-target
reactivation are settled. Existing worked examples/tests validate the old policy,
not this decision. The earlier plan to reuse logical placement without change
must be revisited; topology-code deltas cannot be treated as mere pixel allocation.


### Source-driven retained branch reactivation and swap — accepted direction

The project owner agreed that selecting an already-retained destination through
its source reuses and promotes that branch to the source-adjacent position. If the
outgoing destination is untraversed, replace it under existing safety guards. If
explored, move its branch to the alternative position vacated by the incoming
branch. Do not move the outgoing branch above/left of its source. Unequal branch
footprints may require outward reflow; preserve internal structure, identities,
provenance and meaningful state rather than swapping raw pixel rectangles.

Explicit reactivation may move the incoming branch inward, so the old blanket
monotonic-placement invariant must distinguish it from new-destination creation.
The current code's restore-without-reordering behavior is not evidence of this new
source-driven rule. Direct occurrence restoration is a separate review decision.
Topology scope/estimates and worked examples must be re-grounded accordingly.


### Direct Restore preserves placement — accepted direction

The project owner agreed that directly restoring a displayed occurrence changes
focus/allocation/view while retaining its logical row/column position and topology.
It does not promote that branch or change its source's selected continuation.
Source-driven selection of the retained destination still promotes/swaps under
§2.4. Verify both gestures against the same retained branch, preserving state and
occurrence identity while observing their intentionally different placement effects.


### Whole-band first-time destination insertion — accepted direction

The project owner agreed: establishing a rightward destination first inserts a
whole column immediately right of the source across all rows; establishing a
downward destination first inserts a whole row below the source stage across all
columns. Shift existing bands outward even when the target intersection would be
empty. Replacement reuses an established cell; repeated selection and retained-
branch reactivation follow the accepted source-adjacent/retention/exchange rules.

Grammar v0.13 and Path design v0.9 reconcile the primary placement definitions,
repeat-traversal examples and invariant summaries. The shared-alternative policy
example now puts X below C after the inserted row, rather than beside C. Complete
policy/example validation follows the remaining compression decisions. The old
17-row validation record remains historical evidence for its earlier proposal.


### Bounded directional context protection — accepted direction

The project owner agreed: focus receives full inspection; retain at most the latest
source of rightward traversal and latest source of downward traversal as usable
partial context, derived from the focused ancestry. For A→B↓C→D, protect C and B,
with A compact/recoverable. If D↓E follows, D replaces B as the protected vertical
source. Older turns do not accumulate protection. This bounds protected source
count, not necessarily pixel span after retained-branch placement. Required
partial-context capabilities and reduced-allocation behavior remain under review.


### Partial context as retained navigation capabilities — accepted direction

The project owner agreed that both-axis partial context retains singular and plural
navigation and access to an already-active Collection, without requiring full Restore.
They endorsed capability retention as the framing rather than purely spatial states.
Path derives and delivers required capabilities plus dimensions; the child owns the
responsive arrangement. Verification asserts navigability/state preservation through
keyboard-accessible scrolling/disclosure, not identical rail/tab/widget geometry.
Optional inspection detail may yield; required navigation cannot silently disappear.


### Minimal context and unconditional Restore access — accepted direction

The project owner agreed that minimal context may require Restore before navigation
is possible again, and required Restore to remain available so no collapsed cell
can become frozen. Verify recognizable identity and operable keyboard restoration
for all minimal-axis combinations, suppressed direct v controls and constrained
allocations. Retained off-viewport occurrences must remain recoverable via the
surface and composition inspection. Restore access is a mandatory shared contract
obligation, not a per-HX-developer convention. Small-viewport restoration outcome
semantics are the next review point.


### Retained surface versus finite viewport — accepted direction

The project owner required that accumulated collapsed Nodes never progressively
starve new inspectors of real estate. Advance the viewport as exploration grows;
left-most columns/top-most rows may disappear while their topology/state remain.
Keep a hint of their presence. Recovery uses Pan to reveal a collapsed Node, then
Restore to regain navigation. Merely panning does not restore or rearrange it.

Allocation must remain independent of total retained history. Reconcile the draft
common-factor reduction's actual intervening-span accounting: a long protected
mixed-path span must not progressively squeeze active inspection to fit history.
It may extend off-viewport. The edge-hint representation and precise bounded
current-context budget remain review decisions; do not infer accepted profile
values or a complete reduction algorithm from this direction.


### Inbound arrowheads as offscreen provenance cues — proposed refinement

The project owner suggested reusing inbound connector arrowheads for the hint of
history outside the viewport. Current Path rendering already draws provenance-bound
horizontal/vertical connectors and target arrowheads on the scrollable surface;
this does not yet guarantee their visibility at a viewport boundary. Prefer actual
connector/arrowhead continuation over a new per-hidden-Node breadcrumb system.
Keeping a small incoming-channel portion visible is a viewport concern, not a
reason to enlarge historical track allocations or alter recorded endpoints.
Passive cues versus additional navigation actions remain the next review decision.


### Offscreen provenance cue without counts — accepted direction

The project owner agreed to inbound arrowheads as a cue that something continues
offscreen, without indicating how many Nodes/branches are hidden. Do not add
breadcrumbs or reserve per-hidden-Node space. Preserve actual provenance attachment;
viewport/channel visibility supplies the cue rather than additional history budgets.
This settles cue meaning/membership, not approval of additional clickable behavior.


### Protected capability versus visibility; truthful channel cues — accepted direction

The project owner agreed that protected context retains navigation capabilities
while being allowed offscreen. Pan alone exposes a still-partial protected Node;
minimal context may additionally require Restore. Do not squeeze focus to keep
all protected sources visible.

They corrected the arrow-only cue: in A→B↓C↓D↓E, retained column A can be left of
E without any inbound left arrow into E. Actual empty channel space is the proper
spatial cue in that direction. Keep arrowheads tied to actual provenance and use
real adjacent channel geometry where there is no such connection. Do not fabricate
arrows, counts, per-hidden-Node crumbs or padding before the true surface origin.
The precise channel glimpse/framing and accessibility verification remain to ground.


### Empty-band reclamation on explicit Close — accepted direction

The project owner agreed: after explicit branch removal, reclaim wholly empty
rows/columns and shift subsequent bands together. Keep partially occupied bands
and legitimate sparse cells; no independent packing of unrelated Nodes into holes.
Preserve surviving identities, provenance, topology attachments and state, with
existing workflow dismissal guards. Verify whole-band removal versus partially
occupied-band retention, including retained alternatives and sparse mixed paths.


### Complete contractual promise before selection — accepted requirement

The project owner confirmed and sharpened the rule: Visualizers promise compliance
with all contractual obligations before being considered for selection. Rust-owned
selection checks the complete required contract, ensuring parent contract-bound
directives can be issued without conditional child negotiation. A previously
selected child reporting inability to comply does not trigger reconsideration of
selection. Treat a valid-directive failure as a contract violation. Distinguish
parent-invalid inputs, missing materialized bindings and false behavioral promises;
none permits silent fallback or upward rendered-extent sizing. Conformance fixtures
verify supported input/capability ranges; declaration checks alone cannot prove
arbitrary executable behavior. Failure presentation/recovery is the next review point.


### Contract violation recovery — accepted direction

The project owner agreed to explicit local failure and deliberate recovery. Retain
the last usable presentation where safe, preserve owner-provided restoration/
inspection/closure recovery as applicable, and identify the affected slot and
failure. Explicit retry or agent choice may recover; no automatic replacement,
upward size negotiation or false successful admission is allowed. Distinguish
valid-directive violations from invalid parent inputs. Verify a buggy selected
child cannot strand a collapsed occurrence or destroy externally owned state.


### Topology and downward allocation in one delivery sequence — accepted direction

The project owner agreed that the first delivery sequence implements the reviewed
whole-band/source-adjacent topology together with downward allocation. Do not test
new compression against superseded terminal-append placement or claim logical
placement is reused unchanged. Preserve reference/occurrence/lifecycle seams while
migrating `traversal-layout.ts` and the relevant navigation transitions. Ground
reviewable working increments and estimates after this design review; no abstraction-
only first slice. Shared selection memory and atomic multi-view application remain
separately deferred under the earlier #746 delivery decision.


### Title Bar Actions reuse ActionBar/Action composition — accepted direction

The project owner agreed: Title Bar owns Title Bar Actions slot → selected ActionBar
→ declared individual Action slots → selected Action Visualizers. Shared membership
comes from the common Title Bar contract, with explicit additive extensions. Bind
presentation action activation to authorized Visualizer Operators and occurrence
targets rather than fabricating Dances or deriving the set from the Holon subject.
Preserve Rust selection and the Title Bar's unchanged semantic subject. Extend
the Dance-oriented executable Action input only as needed for this bounded use;
no general workflow/form/executable-contract engine is a prerequisite. The standard
inspection action's target remains an explicit review question.


### Explicit v binding and standard Node inspection target — accepted direction

The project owner agreed that the standard Title Bar Show Visualizer action
inspects its containing Node occurrence, and generalized the rule: every v must
be unambiguously bound to one specific inspectable Visualizer. Physical placement,
rendering Action implementation or a nearest-DOM-parent search cannot determine
that target. Bind the actual occurrence/slot/selection explicitly. Component
Title Bar/ActionBar/Action selections remain separately inspectable; any optional
direct controls have their own explicit targets. Verify repeated subjects and
shared definitions do not retarget controls, including after child replacement.


### Bounded reduction on actual viewport resize — accepted; minimum ownership open

The project owner agreed that an actual smaller viewport may reduce full inspection
toward a useful minimum, then retain useful geometry with pan/scroll overflow.
Required capabilities survive throughout; history growth alone does not reduce
that grant. They explicitly raised how/where useful minima are defined. Resolve
that owner and declarative contract before specifying or estimating the reduction
implementation. Do not use a selected child's later inability report to establish
its minimum or trigger reselection.


### Useful minimum ownership and declaration — accepted direction

The project owner confirmed ownership as the crucial decision: Path Inspector's
Node-slot participation profile is the clear authoritative place to express useful
minima, preferred extents and supported ranges for required capability combinations.
Exact values are determined by testing, not ratified as universal pixel constants
in this review. Keep policy data declared once; Theme/MDS supplies typography/
spacing inputs, and eligible Nodes promise the required profile before selection.

The Operator input domain must include these profile constraints. A positive 1×1
rectangle is not automatically a valid directive. A viewport below useful minima
causes surface overflow/pan, not a below-contract child grant. Distinguish invalid
parent directives from selected-child violations. Ground exact executable profile
keys and initial tested values after review; do not reintroduce rendered minima.


### Recursive immediate-owner participation policy — accepted direction

The project owner agreed to the same rule at every composition boundary: immediate
slot owners declare required capabilities/supported allocation ranges; candidates
promise full compliance before selection; owners allocate within those contracts.
Apply it through Path→Node→Title Bar→Actions→Action, without ancestor sizing of
grandchildren. Parent conformance includes successfully composing its children
within its own promised range. DAHN owns the mechanism/authority rule, while each
slot owner supplies its concrete policy and tested values. Avoid a global minimum
or new generalized contract framework as a prerequisite.


### Stable dimensions per state — accepted structural invariant

The project owner confirmed this as essential structure: for an unchanged usable
Path viewport, Theme and participation profile, dimensions associated with full,
partial and minimal states remain stable through navigation. Insertion, branch
swaps, focus changes and history growth may change band count/positions/states,
but not the dimensions assigned to a given state. Actual grant/Theme/profile
changes may recompute them within declared ranges. No child-content feedback,
prior-band maximum cache or retained-span factor determines state dimensions.

The old actual-intervening-span interpolation is superseded. Concrete bounded
reduction remains a numerical policy decision. Candidate: resolve one factor per
axis from the profile's fixed minimal+partial+full reference composition and two
connector budgets, independent of actual retained band count/positions, then apply
resolved per-state/channel dimensions consistently across the whole surface.
Alternative: reduce context budgets first to retain preferred focus size longer.
This candidate is not yet recorded as an accepted algorithm. Useful minima and
stable inputs are already accepted regardless of which simple rule is chosen.

### Structural review checkpoint validation

After reconciling the accepted review directions, all five documentation portals
build with no new warnings or link/anchor diagnostics against published main
`2aa072e`. The 17 capability/protection rows were independently recalculated with
the whole-band alternative case updated to X(0,2); they agree with the stated
capability policy. This checks example assignments, not the new runtime placement
algorithm, branch exchanges or browser containment. Historical interpolation
checks do not validate a new reduction rule; that numerical policy remains open.
`git diff --check` passes. No runtime, schema or enhancement issue is changed.


### Fixed-reference common-factor reduction — accepted direction

The project owner accepted a common factor per axis for the initial viewport-
resize policy. Calculate it from the profile's fixed minimal+partial+full reference
and two connector channels, not actual retained tracks or protected-source span.
Use the same resolved per-state/channel dimensions throughout the surface. At
minima use overflow/pan; do not adaptively weight or apply context-first reduction.
Grammar §4.4.1 owns the formula and bounds; initial tested profile numbers remain
grounding work. This settles the numerical-policy question left open at the prior
review checkpoint; individual-direction acceptance still does not merge the PR.

### Sizing-policy review completion check

After accepting the fixed-reference reduction rule, Core builds with no new
warning/link/anchor diagnostics against the recorded main baseline. The other
four portals passed at the preceding structural checkpoint; this final change
is confined to Core-owned Path specifications and the integrated plan. Recalculated
17 capability/protection example rows and checked common-factor endpoints,
interior allocation and below-minimum overflow. `git diff --check` passes.
These are specification/example checks, not execution of the future implementation.
The consolidated draft still needs final review and merge before enhancement
grounding. Profile values, executable schema keys and working-issue estimates are
subsequent grounding/validation work, not unresolved allocation ownership.


### Layer dependency audit — 2026-10-15

The project owner required downward architectural dependencies: upper experiences
may require reusable lower-layer capabilities without lower layers knowing their
consumers' presentation or usage. Audit of PR #63 found generic command-lease/
disposal clarification mixed with DOM and Visualizer materialization consequences.
Commands now states caller-independent admission/lifecycle/disposal guarantees;
DAHN owns presentation teardown/materialization consequences, and the loader
experience owns its phase/context adaptation. Removed the Commands-to-loader
workflow prescription/cross-reference from the retained-evidence rule.

The Data Loader document is explicitly an upper-layer experience specification,
not a contract that makes canonical loader execution depend on DAHN geometry.
Commands' named semantic operations are not themselves upward dependencies; live
DOM, inspector arrangement and workflow-specific rebinding must not become lower-
layer requirements. Rust eligibility reads semantic participation declarations,
not browser geometry or executable child presentation code. No runtime dependency
or implementation is changed by this documentation correction.

Code inspection confirms leases cover execution/recovery persistence, active
leases cause Dispose to fail, and disposed contexts reject further admission.
The checked host loader client and guest loader Cargo manifests do not depend on
DAHN presentation modules. This is a scoped documentation/dependency audit, not
a proof of the entire repository's transitive dependency graph.


## 23. Four-mode inspector geometry revision

The [geometry review](inspector-geometry-review.md) records the repository-grounded
assessment, individually accepted decisions, symbolic path examples and bounded
implementation/verification sequence. The accompanying Path grammar, Path design,
Holon Inspector, DAHN and Data Loader revisions replace the prior nine-state
track-derived presentation mapping and simultaneous property/collection composition.

The review preserves latest-source-per-axis retention, explicit selection-time
participation, topology, title composition, reference ownership and Connections
First retirement. Per-occurrence intents are independent of shared track sizes.
Properties/Collection switching is always local; subsequent allocation updates
preserve the user's choice. New traversal may establish context again. Loader
inspection starts in Properties; Restore returns to the remembered full-content
view. A shallow full-width Properties header supplies local return from Collection.

Delivery order is local switching, pure vertical traversal/restore, pure horizontal
traversal/restore, compact aspect ratios, mixed paths/alternatives, then loader and
independent-substitute regressions. Contract encoding and numeric policy minima
require deliberate implementation grounding and usable allocation fixtures. No
runtime work or enhancement issue is authorized by individual design decisions;
consolidated documentation review remains the gate. Performance work is deferred.


### Alternating contract structure and migration accounting

Concrete Visualizer specs expose both incoming slot obligations fulfilled and
outgoing immediate child contracts declared. DAHN owns this documentation rule;
Path Inspector and Holon Inspector now apply it explicitly in the same geometry
review. A kind label or a bare region inventory is not the complete contract.

The existing Path Node slot identity is `PathInspector.RootNodeSlot`, repeated
across root and reached occurrences. Holon Inspector's top-level child-role
inventory describes target composition. Its Title Bar and ActionBar type contracts
are established; rail and collection-tab-index descriptors/bindings remain staged
composition work. The authored `HolonInspector.SingleValueSlot` declaration and
actual Path-owned destination selection require reconciliation during that migration;
do not treat a legacy slot declaration as evidence that the singular rail already
has its own selected presentation. No schema identifiers are renamed in this draft.

Apply the experiential-component criterion to Path's view controls and lineage
presentations before claiming they are permanently private. Track calculations,
coordinate transforms, wrappers and binding adapters remain private machinery.
Any experiential role left embedded during delivery must be named as a temporary
migration exception with its follow-up boundary; inspection must not fabricate a
selected child by copying the containing Visualizer's identity. This review adds
no runtime migration or enhancement issue for those roles.
