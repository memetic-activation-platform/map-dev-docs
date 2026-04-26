# DAHN Phase 0 Specification (Post-Issue 408)

## Purpose

This document specifies **Phase 0 of DAHN implementation** under the explicit assumption that **Issue 408 has been delivered**:

- the public TypeScript MAP SDK exists
- DAHN consumes the public SDK only
- DAHN does not depend on MAP command-wire, IPC-envelope, or Tauri transport internals

Phase 0 is therefore **not** “finish the SDK.” Phase 0 is the first DAHN-facing runtime substrate built **on top of** the delivered SDK.

Its purpose is to establish the minimum runtime contracts needed for later DAHN work:

- a framework-independent visualizer contract
- a minimal canvas abstraction
- a token-based theme system
- a DAHN-facing functional holon access adapter
- a minimal action hierarchy contract for dances
- a dynamic visualizer loader
- a trivial Phase 0 selector function

The central proof of Phase 0 is the generic `HolonNodeVisualizer`:

- a universal node visualizer capable of visualizing any holon
- by reading the holon's `HolonTypeDescriptor`
- and using the property, relationship, and dance descriptors defined there
- with property presentation driven by the associated `ValueTypeDescriptor` semantics

If Phase 0 is completed successfully, the repo will be ready to begin the first end-to-end DAHN rendering loop in Phase 1.

---

## 1. Assumed Starting Point

Phase 0 assumes the following are true before work begins:

1. `dispatch_map_command` exists and is the only TS-side MAP IPC entrypoint.
2. The internal TS command layer exists and remains private.
3. Issue 408 has delivered the public SDK surface:
   - `MapClient`
   - `MapTransaction`
   - public reference/value/domain-facing types required by the SDK spec
   - transaction-bound `HolonReference` objects that expose holon-scoped read behavior
   - writable behavior on bound references where applicable
4. DAHN code is prohibited from importing internal MAP SDK modules such as:
   - internal command builders
   - wire types
   - request/response envelopes
   - request metadata types
5. The current host UI remains the initial shell in which DAHN will first mount.

This document treats those points as prerequisites, not deliverables.

---

## 2. Phase 0 Outcome

At the end of Phase 0, the system must be able to:

1. Open a DAHN route or mount point inside the host UI.
2. Resolve a holon target through a DAHN access adapter backed only by the public SDK.
3. Select the generic `HolonNodeVisualizer` deterministically for any holon target.
4. Dynamically load the required Web Components.
5. Mount the generic node visualizer into a minimal canvas.
6. Render descriptor-defined properties, relationships, and dances.
7. Apply a DAHN theme via semantic design tokens.

Phase 0 does **not** require polished rendering, editing, personalization, or advanced navigation. It establishes the runtime substrate those later phases depend on.

---

## 3. Phase 0 Scope

### In Scope

- SEA runtime foundations needed by DAHN
- read-only holon access for DAHN through the public SDK
- dynamic loading of DAHN visualizers
- a minimal canvas container
- semantic theme tokens
- a trivial selector implementation
- DAHN package/module boundaries
- tests for runtime contracts and loader behavior

### Out of Scope

- holon editing UI
- personalization
- community signals
- graph/spatial canvases
- advanced layout systems
- animation systems
- permission systems
- multi-space DAHN coordination
- direct use of MAP SDK internals

---

## 4. Architecture for Phase 0

Phase 0 introduces a new DAHN runtime layer above the public SDK:

```text
host UI shell
  -> DAHN application adapter
  -> DAHN runtime
      -> canvas
      -> selector
      -> theme registry
      -> visualizer registry / loader
      -> holon access adapter
  -> public MAP SDK
  -> internal MAP SDK command layer (private)
  -> dispatch_map_command
```

### Key Rule

DAHN depends on the **public SDK contract**, not the MAP transport contract.

That separation must be visible in package structure, imports, and tests.

---

## 5. Proposed Package Boundaries

The exact folder names may be adjusted, but the separation below should be preserved.

### 5.1 DAHN Runtime Package

Introduce a DAHN runtime module/package responsible for:

- runtime orchestration
- canvas abstractions
- theme registry
- visualizer definitions
- dynamic loading
- selector contract
- data adapter interfaces

Suggested location:

- `host/dahn-runtime/` as a standalone TS package, or
- `host/ui/src/dahn/` if the team prefers to start inside the host UI app

Preferred direction:

- start with `host/ui/src/dahn/` if speed is the priority
- keep the code internally package-shaped so it can later be extracted cleanly

### 5.2 Host UI Integration Layer

The host UI should contain only:

- the route or mount point for DAHN
- the adapter that instantiates the DAHN runtime
- any framework-specific bridging code

The host UI must not become the home of DAHN’s core runtime contracts.

### 5.3 Public MAP SDK Dependency

DAHN runtime imports must come only from the public SDK entrypoint.

Allowed:

- public `MapClient`
- public `MapTransaction`
- public reference/value/domain types
- public transaction-bound `HolonReference` types

Forbidden:

- `src/internal/*`
- `*Wire` types
- request/response envelopes
- request metadata types

---

## 6. Core Runtime Contracts

Phase 0 should define the following stable contracts.

## 6.1 Holon Target Contract

DAHN needs a single runtime-level way to identify “what is being rendered.”

```ts
export interface DahnTarget {
  reference: HolonReference;
}
```

Rules:

- DAHN runtime treats references as opaque handles.
- DAHN runtime does not resolve or inspect internal reference structure.
- All further data access occurs through the data adapter.

## 6.2 Holon Access Contract

DAHN visualizers should not talk directly to the MAP SDK.

This phase should **not** assume that DAHN materializes a full TypeScript-side holon object or snapshot as its primary model.

The MAP architecture already has:

- Rust-side in-memory holon management
- efficient reference passing across the TS/Rust boundary
- a public SDK built around fine-grained holon access
- holon references that are internally bound to transactions

Accordingly, the default Phase 0 approach is:

- keep authoritative model-layer state in Rust
- keep DAHN TS code reference-centered
- expose holon data through a functional access interface
- allow only small, derived, ephemeral TS-side render state where useful
- support descriptor-driven generic holon rendering rather than type-specific TS models

Suggested contract:

```ts
export interface HolonViewAccess {
  reference(): HolonReference;
  holonId(): Promise<HolonId>;
  key(): Promise<string | null>;
  versionedKey(): Promise<string>;
  summarize(): Promise<string>;
  essentialContent(): Promise<EssentialHolonContent>;
  holonTypeDescriptor(): Promise<HolonTypeDescriptorHandle>;
  propertyValue(name: PropertyName): Promise<BaseValue | null>;
  relatedHolons(name: RelationshipName): Promise<HolonCollection>;
  availableDances(): Promise<DanceDescriptorHandle[]>;
}
```

This is a DAHN runtime interface, not a MAP SDK replacement.

Rules:

- `HolonViewAccess` is backed by the public SDK.
- the underlying public `HolonReference` is already transaction-bound and is itself the active holon-scoped facade
- It does not expose transaction identity.
- It does not expose wire-layer types.
- It does not claim to own holon state on the TS side.
- It may internally memoize read results for the lifetime of a render cycle, but such caching is an optimization, not an architectural source of truth.

`HolonTypeDescriptorHandle` and the related descriptor handles are DAHN-facing, reference-backed accessor objects. They are conceptually part of DAHN's descriptor-driven runtime, not transport types, and they should not be treated as replicated TS-side state.

### Descriptor Handles and Rust-Side Flattening

Descriptor handles should expose descriptor-specific accessors while internally retaining the bound holon reference to the underlying descriptor holon.

Phase 0 assumes:

- descriptor inheritance flattening is provided by the Rust layer
- TS does not reconstruct inheritance through `Extends`
- DAHN consumes the effective flattened descriptor surface returned by Rust-side logic

This means the generic `HolonNodeVisualizer` can render against the descriptor surface it is given without implementing inheritance-merging logic in TypeScript.

### Property Descriptors vs Value Type Descriptors

Since the earlier GitBook work, MAP now distinguishes more clearly between property identity and value semantics.

For DAHN purposes:

- the `PropertyDescriptor` identifies the property slot on the holon
- the `ValueTypeDescriptor` specifies the semantic/value constraints that govern how that property's value should be presented, validated, and eventually edited

Therefore, property visualization should be modeled as **value-type-driven** rather than as a direct consequence of property name alone.

Phase 0 implication:

- the generic `HolonNodeVisualizer` reads the holon's descriptor-defined properties
- for each property, it should use the associated `ValueTypeDescriptor` semantics to choose or configure the generic property presentation

This preserves the GitBook's descriptor-driven property visualizer intent while aligning it with the newer MAP ontology.

### Relationship Descriptor Kinds

Relationship type descriptors come in two flavors:

- `DeclaredRelationshipType`
- `InverseRelationshipType`

That distinction must be preserved in the DAHN descriptor handle model even when Rust returns a flattened effective relationship set.

Phase 0 implication:

- the generic `HolonNodeVisualizer` may render both declared and inverse relationships
- the relationship descriptor handle should expose which kind it represents

Post-Phase-0 implication:

- mutation operations such as `add_related_holons` and `remove_related_holons` are only valid for declared relationship types
- inverse relationship types are viewable and navigable, but not directly mutable

## 6.3 Action Hierarchy Contract

Because holons are active, DAHN must expose not only what a holon is and how it is related, but also what it can do.

DAHN should therefore model dances through a minimal action hierarchy contract that supports:

- individual actions
- action groups
- nested action groups

Suggested minimal contract:

```ts
export interface ActionNode {
  id: string;
  kind: 'action' | 'group';
  label: string;
  dance?: DanceDescriptorHandle;
  children?: ActionNode[];
}
```

Phase 0 rules:

- actions correspond to dances offered by the holon or by DAHN visualizers
- groups represent natural action groupings for presentation
- nesting is allowed in the contract, even if Phase 0 uses only shallow groupings
- ordering and grouping are structural in Phase 0, not yet adaptive

Phase 0 does **not** require:

- personalized regrouping
- affinity-driven group reassignment
- salience-driven ordering
- deep action hierarchy editing

The action hierarchy contract exists in Phase 0 so that action visualizers have a stable semantic object to render, and later phases can attach salience and affinity behavior without replacing the model.

## 6.4 Data Adapter Contract

The DAHN runtime should depend on an adapter interface, not directly on `MapClient`.

```ts
export interface DahnHolonAccessAdapter {
  open(target: DahnTarget): Promise<HolonViewContext>;
}
```

Phase 0 implementation:

- `SdkBackedHolonAccessAdapter`

Suggested composite context:

```ts
export interface HolonViewContext {
  holon: HolonViewAccess;
  actions: ActionNode[];
}
```

Responsibilities:

- begin a transaction
- select or obtain a transaction-bound public `HolonReference` for the target
- manufacture a `HolonViewAccess` wrapper over bound reference calls
- construct a minimal action hierarchy from available dances
- commit or close according to the public SDK contract

Important:

- The adapter may use a short-lived transaction internally.
- Visualizers must not manage MAP transaction lifecycle directly.
- DAHN runtime code should prefer functional reads over TS-side holon materialization.

## 6.4 Visualizer Definition Contract

Visualizers are framework-independent Web Components plus metadata.

```ts
export interface VisualizerDefinition {
  id: string;
  displayName: string;
  version: string;
  componentTag: string;
  supportedTargets: VisualizerTargetRule[];
  load: () => Promise<void>;
}
```

Rules:

- `componentTag` must be a custom element tag.
- `load()` must be idempotent.
- A visualizer registers its element exactly once.
- Phase 0 visualizers are read-only.
- `VisualizerDefinition` should be treated as the local/runtime form of a visualizer descriptor, not as the final storage model for the visualizer ecosystem.

### Future Visualizer Descriptor Direction

Phase 0 uses a local `VisualizerRegistry` populated in code.

However, the architecture must preserve a path toward:

- visualizer descriptors stored as holons in a MAP HolonSpace
- visualizer availability and compatibility determined from MAP-side descriptor data
- dynamic loading of contributed visualizer code beyond the local build
- eventual commons/markets participation for contributed visualizers

Accordingly, Phase 0 must not assume that visualizers are permanently:

- compile-time-only artifacts
- locally bundled only
- described solely by hardcoded TS metadata

The local registry is a Phase 0 bootstrap mechanism, not the final architecture.

## 6.5 Visualizer Element Contract

Each visualizer Web Component must implement a small common surface.

```ts
export interface VisualizerElement extends HTMLElement {
  setContext(context: VisualizerContext): void;
}
```

```ts
export interface VisualizerContext {
  target: DahnTarget;
  holon: HolonViewAccess;
  actions: ActionNode[];
  theme: DahnTheme;
  canvas: CanvasApi;
}
```

Rules:

- `setContext()` is the only required runtime injection point in Phase 0.
- Visualizers render from supplied context and do not fetch independently.
- Visualizers may emit DOM events upward, but Phase 0 does not require a full event bus.

## 6.6 Canvas Contract

The canvas is the experience container that mounts visualizers and applies layout semantics.

```ts
export interface CanvasApi {
  mountVisualizers(plan: VisualizerMountPlan[]): Promise<void>;
  clear(): void;
  setTheme(theme: DahnTheme): void;
}
```

```ts
export interface VisualizerMountPlan {
  visualizerId: string;
  target: DahnTarget;
  slot: 'primary';
}
```

Phase 0 canvas rules:

- exactly one visible region: `primary`
- vertical flow layout only
- scroll supported
- responsive width behavior
- no docking
- no split panes
- no transitions required

## 6.7 Theme Contract

The theme system should express semantic tokens rather than component-specific styling.

```ts
export interface DahnTheme {
  id: string;
  label: string;
  colorTokens: Record<string, string>;
  typographyTokens: Record<string, string>;
  spacingTokens: Record<string, string>;
  radiusTokens: Record<string, string>;
}
```

Initial semantic token families:

- `surface.*`
- `text.*`
- `accent.*`
- `border.*`
- `space.*`
- `font.*`
- `size.*`
- `radius.*`

Application rule:

- tokens are applied as CSS custom properties on the canvas root
- visualizers consume only semantic token names
- visualizers must not hardcode app-specific colors as a primary styling mechanism

## 6.8 Selector Function Contract

Phase 0 requires the interface, but only a static implementation.

```ts
export interface SelectorInput {
  target: DahnTarget;
  holon: HolonViewAccess;
  actions: ActionNode[];
  availableVisualizers: VisualizerDefinition[];
  canvas: CanvasDescriptor;
}
```

```ts
export interface SelectorOutput {
  visualizers: VisualizerMountPlan[];
}
```

```ts
export interface SelectorFunction {
  select(input: SelectorInput): SelectorOutput;
}
```

Phase 0 selector behavior:

- deterministic
- static
- no personalization
- no collective signals
- no randomness
- always resolves the node visualizer to `HolonNodeVisualizer`
- may resolve one default action presentation visualizer when dances are shown

### Selector Placement

The selector should **not** move fully into Rust in Phase 0.

The selector has two different concerns:

1. semantic recommendation
2. final runtime resolution

Semantic recommendation may eventually belong in Rust because it can depend on:

- holon semantics
- affinity/salience models
- collective patterns
- durable MAP-side intelligence

Final runtime resolution must remain TS-side because it depends on:

- currently available visualizers
- dynamic module loading state
- host/runtime capabilities
- device and canvas context

Accordingly, Phase 0 should define the selector boundary so it can later split into:

- Rust-side semantic recommendation
- TS-side final visualizer resolution

But for Phase 0 itself:

- implement the selector entirely in TS
- keep it static and deterministic
- keep node visualizer selection trivial
- keep action visualizer selection trivial
- design the interface so semantic recommendation can later be delegated to Rust without breaking DAHN visualizer/runtime contracts

### Phase 0 Node Visualizer Selection

Phase 0 includes only one required node visualizer:

- `HolonNodeVisualizer`

Therefore the node visualizer selector implementation is intentionally trivial:

- for any holon target, select `HolonNodeVisualizer`

This is a deliberate MVP simplification, not a statement about the long-term selector design.

### Phase 0 Action Visualizer Selection

Action visualizers are a first-class DAHN visualizer family because they present the dances offered by active holons and by DAHN visualizers themselves.

Phase 0 requires only a minimal action presentation mechanism.

Suggested default:

- `ActionMenuVisualizer`

Phase 0 action visualizer behavior:

- when dances are available, present them through one default action visualizer
- no adaptive selection among alternate action visualizers yet
- no adaptive regrouping yet

---

## 7. Phase 0 Workstreams

## 7.1 Workstream A: SEA Runtime Foundations

Deliver:

1. Core DAHN runtime types and interfaces
2. Runtime orchestrator
3. Minimal canvas implementation
4. Theme registry
5. Visualizer registry
6. Trivial selector stub
7. Generic descriptor-driven `HolonNodeVisualizer`
8. Minimal action hierarchy and default action visualizer

### Runtime Orchestrator

Phase 0 should define a single coordinator responsible for:

- taking a target holon reference
- opening a holon view context through the adapter
- asking the selector for a render plan
- loading required visualizers
- mounting them into the canvas

Suggested shape:

```ts
export interface DahnRuntime {
  open(target: DahnTarget): Promise<void>;
}
```

Suggested implementation:

- `DefaultDahnRuntime`

### Acceptance Criteria

- `open(target)` performs one coherent render cycle
- failure to load one visualizer fails predictably and surfaces a DAHN runtime error
- no visualizer reaches into MAP SDK internals
- no DAHN contract requires a fully materialized TS-side holon model
- the generic `HolonNodeVisualizer` can render any holon from its descriptors
- dances are available to the runtime via a minimal action hierarchy

## 7.2 Workstream B: Uniform API Integration

Deliver a DAHN adapter layer over the public SDK.

### Adapter Responsibilities

- create a `MapClient`
- open a transaction
- obtain or bind a transaction-bound `HolonReference` for the target
- derive a minimal action hierarchy from the holon's dances
- expose functional read methods needed by DAHN:
  - `holonId()`
  - `key()`
  - `versionedKey()`
  - `summarize()`
  - `essentialContent()`
  - `holonTypeDescriptor()`
  - `propertyValue(name)`
  - `relatedHolons(name)`
  - `availableDances()`

### Important Design Choice

The adapter should **not** normalize DAHN’s read needs into a primary TS-side holon snapshot object.

Instead, it should expose a functional access facade over the public SDK.

This preserves:

- Rust as the model-layer state holder
- opaque holon references as the primary cross-boundary handle
- the TS side as an experience-composition layer rather than a second model layer
- DAHN's ability to render any holon generically from type descriptors

If the adapter memoizes reads during a render cycle, that is acceptable, but the memoized values remain adapter-local derived state.

### Acceptance Criteria

- DAHN runtime can obtain a `HolonViewContext` for any valid holon reference
- all SDK access remains through public exports
- transport-layer types never appear in DAHN module exports
- the adapter does not require materializing a full TS-side holon object
- the adapter exposes enough descriptor information for universal generic holon rendering
- the adapter exposes a minimal action hierarchy for dances

## 7.3 Workstream C: Dynamic Loader

Deliver a visualizer loader that supports runtime registration and development-time refresh.

### Loader Requirements

- load visualizer modules via dynamic `import()`
- register custom elements safely
- avoid duplicate element definitions
- allow multiple visualizers to be declared available before loading

### Registry Behavior

The registry should support:

- list available visualizers
- get visualizer by id
- ensure visualizer loaded

Suggested interface:

```ts
export interface VisualizerRegistry {
  register(definition: VisualizerDefinition): void;
  get(id: string): VisualizerDefinition | undefined;
  list(): VisualizerDefinition[];
  ensureLoaded(id: string): Promise<VisualizerDefinition>;
}
```

Phase 0 registry guidance:

- the initial registry may be populated statically in code
- the registry API should remain agnostic about where visualizer definitions originate
- a future implementation may hydrate this registry from MAP-stored visualizer descriptor holons

### Development Hot Reload

Phase 0 only needs a pragmatic development strategy:

- in dev mode, dynamic imports may use cache-busting query params or equivalent loader behavior
- a full plugin marketplace protocol is not required yet

### Acceptance Criteria

- DAHN can dynamically load a visualizer module at runtime
- repeated loading does not crash or redefine the custom element
- loader behavior is testable independently from the host UI framework

---

## 8. Minimum Built-In Visualizers for Phase 0

Phase 0 should keep built-in visualizers to the minimum needed to prove universal holon rendering.

Required built-ins:

1. `HolonNodeVisualizer`
   - the universal generic node visualizer
   - capable of rendering any holon
   - uses the holon's `HolonTypeDescriptor` to discover:
     - properties
     - relationships
     - dances
   - initially focuses on the equivalent of expanded/read-mode
   - may present properties, relationships, and dances using very simple layouts in Phase 0

2. `ActionMenuVisualizer`
   - the default Phase 0 action visualizer
   - presents dances from the minimal action hierarchy
   - may render as a simple button list or menu
   - does not yet require alternate action-group visualizers

Optional development aid:

2. `holon-json-debug`
   - development/debug visualizer only
   - useful during bring-up, but not required as part of the core Phase 0 concept

### Generic HolonNodeVisualizer Responsibilities

The generic `HolonNodeVisualizer` is the default visualizer capable of visualizing any holon.

It should:

- display basic holon identity
- display descriptor-defined properties
- display descriptor-defined relationships
- display descriptor-defined dances
- use generic property, relationship, and action presentation mechanisms
- embed or host the default action visualizer for dances
- select/configure generic property presentation using `ValueTypeDescriptor` semantics

It does **not** need in Phase 0 to implement:

- collapsed states
- selected states
- edit mode
- type-specific layouts
- advanced graph transitions
- personalization controls

### Generic HolonNodeVisualizer and Type-Specific Visualizers

The architecture must remain open to future type-specific node visualizers.

But Phase 0 requires only:

- one generic `HolonNodeVisualizer`
- one default `ActionMenuVisualizer`

Therefore:

- the selector does not yet need type-hierarchy fallback logic in implementation
- the selector does not yet need alternate action visualizer selection logic in implementation
- future fallback semantics remain an architectural extension point

---

## 9. Host UI Integration

Phase 0 should add a DAHN mount point in the existing host UI.

Minimum integration:

1. add a DAHN route or component mount
2. instantiate `DefaultDahnRuntime`
3. pass in:
   - canvas implementation
   - theme registry
   - visualizer registry
   - selector implementation
   - SDK-backed holon access adapter
4. open a known target holon for development/testing

Rules:

- Angular may host DAHN
- Angular must not become the visualizer abstraction
- DAHN visualizers remain Web Components, not Angular components

---

## 10. Testing Requirements

Phase 0 tests should focus on contracts and separation boundaries.

## 10.1 Runtime Tests

- `DefaultDahnRuntime.open()` opens a `HolonViewContext`, invokes selector, loads visualizers, and mounts them in order
- runtime failures are surfaced clearly when holon access or visualizer loading fails
- the selector resolves `HolonNodeVisualizer` for any valid holon target in Phase 0
- the generic `HolonNodeVisualizer` renders properties, relationships, and dances from descriptors
- dances are passed to visualizers through the `ActionNode[]` hierarchy

## 10.2 Data Adapter Tests

- adapter uses only public SDK imports
- adapter returns a `HolonViewContext`
- adapter handles missing optional values correctly
- adapter can memoize reads without changing public semantics

## 10.3 Selector Tests

- selector returns `HolonNodeVisualizer` deterministically for node rendering
- selector returns the default action visualizer deterministically for dances
- selector ignores personalization/community inputs in Phase 0
- selector contract preserves a future split between semantic recommendation and final runtime resolution

## 10.4 Registry/Loader Tests

- registry prevents duplicate visualizer registration bugs
- `ensureLoaded()` is idempotent
- custom element redefinition is avoided

## 10.5 Boundary Tests

- DAHN packages do not import MAP SDK internal modules
- DAHN public runtime exports do not expose transport or wire concerns

---

## 11. Definition of Done for Phase 0

- [ ] DAHN runtime contracts are implemented in code
- [ ] A minimal canvas mounts dynamically loaded Web Component visualizers
- [ ] A semantic theme can be applied through CSS tokens
- [ ] A trivial selector function chooses `HolonNodeVisualizer` deterministically
- [ ] A DAHN holon access adapter exposes functional reads through the public SDK only
- [ ] A minimal action hierarchy exists for descriptor-defined dances
- [ ] The host UI can mount DAHN and open a target holon
- [ ] The generic `HolonNodeVisualizer` can render any holon from its descriptors
- [ ] The default `ActionMenuVisualizer` can present dances from the action hierarchy
- [ ] Tests cover runtime orchestration, loader idempotence, selector behavior, and SDK-boundary enforcement

---

## 12. Recommended Sequencing

Implement Phase 0 in this order:

1. Define runtime interfaces and folder boundaries.
2. Implement the visualizer registry and loader.
3. Implement the minimal canvas.
4. Implement the theme registry and one default theme.
5. Implement the SDK-backed holon access adapter.
6. Implement the trivial selector.
7. Implement the minimal action hierarchy and `ActionMenuVisualizer`.
8. Implement the generic descriptor-driven `HolonNodeVisualizer`.
9. Implement the runtime orchestrator.
10. Mount DAHN in the host UI.
11. Add tests that lock in the public/internal boundary.

This sequencing gives a visible end-to-end result early while preserving architecture.

---

## 13. Explicit Non-Goals to Preserve

To avoid Phase 0 sprawl, do not add any of the following yet:

- property editing
- relationship editing
- personal salience/affinity persistence
- community aggregation
- multi-pane canvas layout
- plugin marketplace semantics
- direct visualizer execution of MAP commands
- TS-side promotion of DAHN into a second authoritative holon model layer
- full Rust-side selector migration in Phase 0

---

## 14. Result

Phase 0, post-Issue 408, is the phase where DAHN becomes a real runtime substrate instead of a concept:

- the MAP SDK becomes the stable data boundary
- DAHN gains its own runtime contracts
- visualizers become dynamically loadable expression modules
- the canvas becomes the first experiential container
- themes become semantic and portable
- Rust remains the authoritative model-state holder
- the selector boundary stays evolvable toward later Rust-side semantic recommendation
- universal holon rendering is proven through the generic `HolonNodeVisualizer`

That is the correct base for Phase 1’s first universal holon rendering milestone.
