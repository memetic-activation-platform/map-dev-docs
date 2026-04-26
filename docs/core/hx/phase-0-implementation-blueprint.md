# DAHN Phase 0 Implementation Blueprint

## Purpose

This document translates the Phase 0 spec into a concrete implementation blueprint:

- proposed module layout
- core interfaces
- implementation responsibilities
- first PR slices

It assumes:

- Issue 408 has delivered the public TS SDK
- DAHN Phase 0 remains post-408 and descriptor-driven
- Phase 0 proves universal holon rendering through the generic `HolonNodeVisualizer`

This blueprint is intentionally implementation-oriented. It is subordinate to:

- [phase-0-post-408-spec.md](../../../archive/phase-0-post-408-spec-v1.0.md)

---

## 1. Recommended Initial Placement

For speed, Phase 0 should begin inside the existing host UI app:

- `host/ui/src/dahn/`

This keeps bring-up friction low while still preserving a package-like boundary that can later be extracted to:

- `host/dahn-runtime/`

### Boundary Rule

Everything under `host/ui/src/dahn/` should be written as if it were already a standalone package.

That means:

- no Angular-specific types in core runtime modules
- no direct imports from app components into core DAHN modules
- one framework bridge layer only

---

## 2. Proposed Module Layout

```text
host/ui/src/dahn/
  index.ts
  runtime/
    dahn-runtime.ts
    default-dahn-runtime.ts
    runtime-errors.ts
  contracts/
    targets.ts
    holon-view.ts
    actions.ts
    visualizers.ts
    canvas.ts
    selector.ts
    themes.ts
  adapters/
    sdk/
      sdk-holon-access-adapter.ts
      descriptor-mappers.ts
      action-hierarchy-builder.ts
  registry/
    visualizer-registry.ts
    builtins.ts
  selector/
    phase0-selector.ts
  canvas/
    minimal-canvas-element.ts
    minimal-canvas-controller.ts
  visualizers/
    holon-node/
      holon-node-visualizer.ts
      holon-node-template.ts
      holon-node-styles.css
      property-rendering.ts
      relationship-rendering.ts
      dance-rendering.ts
    action-menu/
      action-menu-visualizer.ts
      action-menu-template.ts
      action-menu-styles.css
    debug/
      holon-json-debug.ts
  themes/
    default-theme.ts
    theme-registry.ts
  integration/
    create-dahn-runtime.ts
    dahn-route.component.ts
```

You do not need every file on day one, but this is the target shape.

---

## 3. Core Contracts

## 3.1 `contracts/targets.ts`

```ts
export interface DahnTarget {
  reference: HolonReference;
}
```

Responsibility:

- identify the holon being opened

## 3.2 `contracts/holon-view.ts`

```ts
export interface ValueTypeDescriptorHandle {
  reference(): HolonReference;
  name(): Promise<string>;
  kind(): Promise<string | null>;
  format(): Promise<string | null>;
  enumValues(): Promise<string[]>;
}

export interface PropertyDescriptorHandle {
  reference(): HolonReference;
  name(): Promise<string>;
  label(): Promise<string | null>;
  valueTypeDescriptor(): Promise<ValueTypeDescriptorHandle>;
}

export interface RelationshipDescriptorHandle {
  reference(): HolonReference;
  name(): Promise<string>;
  label(): Promise<string | null>;
  relationshipKind(): Promise<'declared' | 'inverse'>;
}

export interface DanceDescriptorHandle {
  reference(): HolonReference;
  name(): Promise<string>;
  label(): Promise<string | null>;
  description(): Promise<string | null>;
}

export interface HolonTypeDescriptorHandle {
  reference(): HolonReference;
  typeName(): Promise<string>;
  displayName(): Promise<string | null>;
  propertyDescriptors(): Promise<PropertyDescriptorHandle[]>;
  relationshipDescriptors(): Promise<RelationshipDescriptorHandle[]>;
  danceDescriptors(): Promise<DanceDescriptorHandle[]>;
}

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

export interface HolonViewContext {
  holon: HolonViewAccess;
  actions: ActionNode[];
}
```

Responsibility:

- define the normalized DAHN-side read surface
- keep TS-side state thin and functional
- keep descriptor access reference-backed and accessor-based

Phase 0 descriptor assumption:

- Rust provides flattened/effective descriptor traversal across `Extends`
- TS consumes descriptor handles over that flattened descriptor surface
- TS does not reconstruct inheritance locally

## 3.3 `contracts/actions.ts`

```ts
export interface ActionNode {
  id: string;
  kind: 'action' | 'group';
  label: string;
  dance?: DanceDescriptorHandle;
  children?: ActionNode[];
}
```

Responsibility:

- represent dances as a renderable action hierarchy

Phase 0 rule:

- allow nesting in the contract
- use shallow grouping in the implementation

## 3.4 `contracts/visualizers.ts`

```ts
export interface VisualizerDefinition {
  id: string;
  displayName: string;
  version: string;
  componentTag: string;
  supportedTargets: VisualizerTargetRule[];
  load: () => Promise<void>;
}

export interface VisualizerContext {
  target: DahnTarget;
  holon: HolonViewAccess;
  actions: ActionNode[];
  theme: DahnTheme;
  canvas: CanvasApi;
}

export interface VisualizerElement extends HTMLElement {
  setContext(context: VisualizerContext): void;
}
```

Responsibility:

- define the runtime mount contract for Web Component visualizers

## 3.5 `contracts/canvas.ts`

```ts
export interface VisualizerMountPlan {
  visualizerId: string;
  target: DahnTarget;
  slot: 'primary';
}

export interface CanvasApi {
  mountVisualizers(plan: VisualizerMountPlan[]): Promise<void>;
  clear(): void;
  setTheme(theme: DahnTheme): void;
}
```

Responsibility:

- define the minimal canvas API

## 3.6 `contracts/selector.ts`

```ts
export interface CanvasDescriptor {
  id: string;
  slots: Array<'primary'>;
}

export interface SelectorInput {
  target: DahnTarget;
  holon: HolonViewAccess;
  actions: ActionNode[];
  availableVisualizers: VisualizerDefinition[];
  canvas: CanvasDescriptor;
}

export interface SelectorOutput {
  visualizers: VisualizerMountPlan[];
}

export interface SelectorFunction {
  select(input: SelectorInput): SelectorOutput;
}
```

Responsibility:

- preserve the selector seam while keeping Phase 0 trivial

## 3.7 `contracts/themes.ts`

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

Responsibility:

- define theme token payloads

---

## 4. Runtime Modules

## 4.1 `runtime/dahn-runtime.ts`

```ts
export interface DahnRuntime {
  open(target: DahnTarget): Promise<void>;
}
```

## 4.2 `runtime/default-dahn-runtime.ts`

Primary responsibilities:

- accept a target
- ask the access adapter for a `HolonViewContext`
- ask the selector for a mount plan
- ensure required visualizers are loaded
- mount them into the canvas

Suggested constructor dependencies:

```ts
interface DefaultDahnRuntimeDeps {
  adapter: DahnHolonAccessAdapter;
  selector: SelectorFunction;
  registry: VisualizerRegistry;
  canvas: CanvasApi;
  theme: DahnTheme;
}
```

Suggested flow:

```ts
async open(target: DahnTarget): Promise<void> {
  const context = await this.adapter.open(target);
  const plan = this.selector.select({
    target,
    holon: context.holon,
    actions: context.actions,
    availableVisualizers: this.registry.list(),
    canvas: { id: 'dahn-2d-minimal', slots: ['primary'] },
  });

  this.canvas.clear();
  this.canvas.setTheme(this.theme);

  for (const item of plan.visualizers) {
    await this.registry.ensureLoaded(item.visualizerId);
  }

  await this.canvas.mountVisualizers(plan);
}
```

---

## 5. Access Adapter Modules

## 5.1 `adapters/sdk/sdk-holon-access-adapter.ts`

Primary responsibility:

- bridge public MAP SDK calls into DAHN contracts

This module should be the only place in Phase 0 DAHN that directly imports the public SDK.

Suggested interface:

```ts
export interface DahnHolonAccessAdapter {
  open(target: DahnTarget): Promise<HolonViewContext>;
}
```

Suggested implementation approach:

1. create or receive a public `MapClient`
2. begin a transaction
3. obtain or bind a transaction-bound public `HolonReference` for the target
4. create a `HolonViewAccess` wrapper around bound reference methods
5. derive `ActionNode[]` from `availableDances()`
6. return `HolonViewContext`

### Public SDK Alignment Assumption

This blueprint assumes the public SDK matches the Rust-side semantics:

- `HolonReference` objects used for holon-scoped commands are already transaction-bound
- a separate manufactured public `ReadableHolon` wrapper is not required
- holon-scoped reads and writes are exposed on the bound reference objects themselves

That means DAHN should consume bound references directly and wrap them only in the narrower `HolonViewAccess` interface needed by the DAHN runtime.

The only remaining SDK concern is how the TS client obtains or selects the correct active transaction when creating or using transaction-bound references.

## 5.2 `adapters/sdk/descriptor-mappers.ts`

Primary responsibility:

- map public SDK/domain-facing descriptor results into:
  - `HolonTypeDescriptorHandle`
  - `PropertyDescriptorHandle`
  - `ValueTypeDescriptorHandle`
  - `RelationshipDescriptorHandle`
  - `DanceDescriptorHandle`

Rules:

- keep mapping logic out of visualizers
- keep mapping logic out of the runtime orchestrator
- preserve relationship kind (`declared` vs `inverse`) in `RelationshipDescriptorHandle`
- assume inheritance flattening is already handled on the Rust side

## 5.3 `adapters/sdk/action-hierarchy-builder.ts`

Primary responsibility:

- build a minimal `ActionNode[]` tree from dance descriptors

Phase 0 behavior:

- create one top-level action group if useful, for example `Actions`
- flatten all dances beneath it, or return a flat list if simpler
- no adaptive grouping yet

---

## 6. Registry and Loader Modules

## 6.1 `registry/visualizer-registry.ts`

Suggested class:

```ts
export class DefaultVisualizerRegistry implements VisualizerRegistry { ... }
```

Responsibilities:

- register built-ins
- list visualizers
- ensure each visualizer is loaded once

Required behaviors:

- duplicate visualizer ids rejected
- duplicate custom element definition avoided
- dynamic `load()` awaited safely

## 6.2 `registry/builtins.ts`

Primary responsibility:

- register:
  - `HolonNodeVisualizer`
  - `ActionMenuVisualizer`
  - optional `holon-json-debug`

This file should be the single place where the local Phase 0 built-in registry is assembled.

---

## 7. Selector Module

## 7.1 `selector/phase0-selector.ts`

Suggested implementation:

```ts
export class Phase0Selector implements SelectorFunction {
  select(input: SelectorInput): SelectorOutput {
    return {
      visualizers: [
        {
          visualizerId: 'holon-node',
          target: input.target,
          slot: 'primary',
        },
      ],
    };
  }
}
```

Phase 0 rule:

- node visualizer choice is trivial
- action visualizer choice is also trivial and happens inside the generic node visualizer composition

Do not over-engineer this file.

---

## 8. Canvas Modules

## 8.1 `canvas/minimal-canvas-element.ts`

Implement a Web Component or plain DOM-backed host for the minimal canvas.

Responsibilities:

- create the root render area
- expose one `primary` slot
- apply theme CSS variables
- host mounted visualizer elements

## 8.2 `canvas/minimal-canvas-controller.ts`

Responsibilities:

- implement `CanvasApi`
- translate `VisualizerMountPlan` into actual custom element instances
- call `setContext()` on each mounted visualizer

Important:

- keep DOM orchestration here, not in the runtime class

---

## 9. Visualizer Modules

## 9.1 `visualizers/holon-node/holon-node-visualizer.ts`

This is the key Phase 0 artifact.

Responsibilities:

- render any holon generically
- read identity information
- render descriptor-defined properties
- render descriptor-defined relationships
- render dances through the default action visualizer

Phase 0 rendering scope:

- expanded/read-mode equivalent only
- simple sections are enough:
  - header
  - properties
  - relationships
  - actions

### Suggested internal flow

On `setContext(context)`:

1. fetch `summarize()`
2. fetch `holonTypeDescriptor()`
3. render title/type
4. iterate descriptor-defined properties
5. for each property:
   - fetch `propertyValue(name)`
   - choose/configure generic property presentation from `ValueTypeDescriptor`
6. iterate descriptor-defined relationships
7. for each relationship:
   - fetch `relatedHolons(name)`
   - render a simple list/count
8. mount `ActionMenuVisualizer` with `ActionNode[]`

## 9.2 `visualizers/holon-node/property-rendering.ts`

Primary responsibility:

- provide generic property rendering helpers

Phase 0 should support only a small initial set, for example:

- short text
- long text / markdown-ish text
- numbers
- booleans
- dates
- simple enums
- fallback unknown-value renderer

The key rule is:

- choose/configure presentation from `ValueTypeDescriptor`

This is where the GitBook property-visualizer insight should land in code.

## 9.3 `visualizers/holon-node/relationship-rendering.ts`

Primary responsibility:

- provide simple generic relationship rendering

Phase 0 output is enough if it shows:

- relationship label/name
- count
- simple list of related holon summaries or references

Important semantic note:

- relationship descriptor handles must preserve whether the relationship is `declared` or `inverse`
- this distinction does not need rich UI treatment in Phase 0
- but it will matter later because only declared relationship types are directly mutable

No graph behavior required.

## 9.4 `visualizers/holon-node/dance-rendering.ts`

Primary responsibility:

- adapt `ActionNode[]` for the node visualizer’s action section

## 9.5 `visualizers/action-menu/action-menu-visualizer.ts`

Responsibilities:

- render `ActionNode[]`
- show simple action groups and action items
- allow future event emission for invocation

Phase 0 note:

- discovery/presentation only is enough
- actual dance invocation wiring may be stubbed if not yet ready

If invocation is wired, it should go through the public SDK only.

## 9.6 `visualizers/debug/holon-json-debug.ts`

Optional dev-only visualizer.

Use only if it accelerates bring-up.

---

## 10. Theme Modules

## 10.1 `themes/default-theme.ts`

Provide one minimal default theme token set.

Start with:

- `surface.background`
- `surface.card`
- `text.primary`
- `text.secondary`
- `accent.primary`
- `border.default`
- `space.sm`
- `space.md`
- `space.lg`
- `radius.sm`
- `radius.md`
- `font.body`
- `font.heading`

## 10.2 `themes/theme-registry.ts`

Provide a tiny registry or helper to retrieve the default theme.

Do not overbuild multi-theme switching yet.

---

## 11. Integration Modules

## 11.1 `integration/create-dahn-runtime.ts`

Primary responsibility:

- assemble all Phase 0 dependencies in one place

Suggested output:

```ts
export function createDahnRuntime(root: HTMLElement): DahnRuntime
```

It should wire together:

- default theme
- visualizer registry
- minimal canvas controller
- SDK-backed adapter
- Phase 0 selector

## 11.2 `integration/dahn-route.component.ts`

Angular-only bridge module.

Responsibilities:

- allocate DOM root
- instantiate runtime
- open a known target

This should be thin.

---

## 12. First PR Slices

The goal is small PRs that each establish a meaningful seam.

## PR 1: DAHN Contracts and Skeleton

Deliver:

- `host/ui/src/dahn/` directory scaffold
- contract files
- runtime interface
- empty/default error types
- no real rendering yet

Acceptance:

- TS compiles
- DAHN modules export cleanly

## PR 2: Visualizer Registry and Minimal Canvas

Deliver:

- `VisualizerRegistry`
- minimal canvas element/controller
- default theme application
- test coverage for loader/registry idempotence

Acceptance:

- a dummy visualizer can be registered and mounted

## PR 3: Public SDK Access Adapter Seam

Deliver:

- `SdkBackedHolonAccessAdapter`
- descriptor mappers
- `HolonViewAccess`
- `HolonViewContext`

Acceptance:

- a DAHN target can be opened into a functional read context
- no internal SDK imports leak into DAHN

## PR 4: Trivial Phase 0 Selector

Deliver:

- `Phase0Selector`
- selector tests

Acceptance:

- any target resolves to `holon-node`

## PR 5: Action Hierarchy and Action Menu Visualizer

Deliver:

- `ActionNode` builder
- `ActionMenuVisualizer`
- basic rendering tests

Acceptance:

- dances are visible as actions

## PR 6: Generic HolonNodeVisualizer

Deliver:

- `HolonNodeVisualizer`
- property rendering helpers
- relationship rendering helpers
- dance section integration

Acceptance:

- any holon can be rendered generically from descriptors

## PR 7: Host UI Mount and Bring-Up Route

Deliver:

- DAHN route/component
- `createDahnRuntime()`
- initial target open flow

Acceptance:

- DAHN mounts in the host UI and renders a known holon

## PR 8: Hardening and Boundary Tests

Deliver:

- boundary tests
- public-SDK-only checks
- runtime smoke-path tests
- documentation cleanup

Acceptance:

- Phase 0 seams are locked in before feature growth

---

## 13. Testing Blueprint

## Unit Tests

- contracts stay transport-free
- registry prevents duplicate registration
- registry `ensureLoaded()` is idempotent
- selector returns `holon-node`
- action hierarchy builder maps dances into `ActionNode[]`
- adapter returns `HolonViewContext`
- property rendering chooses generic presentation from `ValueTypeDescriptor`

## Component/DOM Tests

- minimal canvas mounts visualizer elements
- `HolonNodeVisualizer` renders descriptor-defined sections
- `ActionMenuVisualizer` renders action groups/items

## Boundary Tests

- no DAHN module imports MAP SDK `internal/*`
- no DAHN public exports leak wire/request envelope types

---

## 14. Key Open Questions to Resolve Before Coding

These are small but important.

1. How does the TS client obtain or select the correct transaction-bound `HolonReference` for a target holon?
2. What public SDK shape exposes the holon’s `HolonTypeDescriptor`?
3. What public SDK shape exposes dances/descriptors?
4. Is actual dance invocation in Phase 0 required, or is discovery/presentation sufficient?
5. What known target holon should be used for bring-up:
   - a `HolonTypeDescriptor`
   - a well-known bootstrap holon
   - a fixture/imported test holon

If unresolved, these should be answered before PR 3.

---

## 15. Minimal Recommended Bring-Up Demo

Use a known `HolonTypeDescriptor` as the first target.

Why:

- it proves universal rendering against the self-describing type system
- it exercises properties, relationships, and dances in the richest early object family
- it aligns with the broader TypeDescriptors-first roadmap

Suggested initial demo:

1. mount DAHN route
2. open one known `HolonTypeDescriptor`
3. show:
   - title/summary
   - descriptor-defined properties
   - descriptor-defined relationships
   - descriptor-defined dances in `ActionMenuVisualizer`

That is enough to prove Phase 0 is real.
