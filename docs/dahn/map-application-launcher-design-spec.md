# MAP Application Launcher Design Specification

## Status

Draft normative design specification.

## Purpose

The **MAP Application Launcher** establishes one usable local MAP application
session and presents the person's home Dancer experience for its active
`HolonSpace`.

It is a Rust/Tauri composition module. It is not a Visualizer, Dancer, Canvas,
or Holons Loader. It owns startup sequencing and hides Tauri setup ordering,
MAP-host readiness, Core Schema bootstrap, and initial Canvas realization
behind one application-facing operation:

```text
LaunchApplication(configuration) -> ApplicationSession
```

The Launcher MUST remain Dancer-neutral. It asks the DAHN Visualizer Selection
Service to select the active `HolonSpace`'s home Dancer experience. Space
Navigator MAY be the sole initial eligible result, but the Launcher MUST NOT
name, select, or depend on Space Navigator directly.

---

# 1. Responsibilities

The Launcher owns:

- Tauri application startup and shutdown coordination;
- initialization of the MAP host and command runtime;
- opening or creating one local active `HolonSpace`;
- intrinsic, idempotent bootstrap of Core Schema when the active space requires
  it;
- activation of the base packages needed to resolve the generic Canvas;
- Canvas selection, materialization, and mounting through the established MAP
  command/SDK and DAHN runtime seams;
- home-Dancer selection for the active `HolonSpace`;
- passing the active `HolonSpace` context and a Canvas allocation to the
  selected Dancer experience realization; and
- explicit startup and realization failure state.

The Launcher does not own persistent MAP semantic state, Dancer behavior,
Canvas composition policy, Visualizer selection policy, or TypeScript
rendering. Rust owns startup orchestration; TypeScript is a thin readiness
client that realizes selected implementations returned through the SDK/command
runtime seam.

---

# 2. Application Session

`LaunchApplication` returns an **ApplicationSession**. It is the runtime
session established for one launched application window, not a persistent MAP
holon and not a long-lived transaction.

An ApplicationSession includes the active `HolonSpace` reference, MAP host and
command-runtime readiness, selected Theme/MDS context, selected and
materialized Canvas realization, hosted-Dancer realization state, and lifecycle
or recoverable-failure state.

The session MAY retain read-capable context for its active `HolonSpace`. It
MUST NOT retain a long-lived write transaction. Each later mutation or Dance
invocation establishes and completes its own transaction according to MAP
transaction rules.

---

# 3. Startup Sequence

The initial local startup sequence is:

```text
Tauri initialization
  -> MAP Application Launcher
    -> initialize MAP host and command runtime
    -> open or create one local active HolonSpace
    -> bootstrap Core Schema if required
    -> activate required base packages
    -> resolve Theme and Canvas
    -> materialize and mount Canvas
    -> select HolonSpace home Dancer
    -> allocate and mount its root experience realization
```

The Launcher begins with the person's active `HolonSpace`; it does not present
a space chooser in this initial design.

Canvas receives the active space, selected Theme, and its own realization
through normal selection and materialization. Canvas receives the selected home
Dancer experience and allocates real estate to that experience's root
visualizer realization(s). Canvas does not interpret the Dancer's internal
composition or layout grammar.

---

# 4. Core Bootstrap and Ordinary Loading

Core Schema bootstrap is a required base case: MAP cannot depend on a dynamic
Dancer or ordinary `LoadHolons` Dance before the descriptors and execution
machinery that make those facilities usable exist.

The Launcher MAY use one statically available intrinsic bootstrap adapter to
load Core Schema into the active `HolonSpace`. Bootstrap MUST be idempotent. It
MUST establish completion from durable Core Schema/version state and required
descriptor availability, and expose a recoverable failure when a prior
bootstrap is incomplete or inconsistent.

No other ordinary runtime import is intrinsic to the Launcher. After Core is
usable, ordinary loading enters only through the canonical `LoadHolons` Dance
and the MAP command/SDK runtime path.

The Launcher MUST NOT use or revive this obsolete ingress path:

```text
HolonsClient -> MultiplexService.dance() -> invoke("map_request")
  -> deprecated Holochain receptor
```

---

# 5. Home Dancer Selection

A `HolonSpace` offers the Dancers that may realize its home experience. The
DAHN Visualizer Selection Service evaluates those candidates in the active
space, Theme/MDS, runtime, and person context, then returns one selected Dancer
and the materializable realization of its experience roles.

The selected Dancer is represented holonically. The Launcher does not imply a
Visualizer kind from the Dancer's concrete holon type. For example,
`SpaceNavigator.HolonType` extends `Dancer`; it can compose a generic Rooted
Navigation Visualizer rooted at the active `HolonSpace`, along with other
experience-role visualizers, when it is an eligible home candidate.

The Launcher supplies the active `HolonSpace` as the Dancer experience context.
It does not request a Visualizer directly for `HolonSpace.HolonType`, and it
does not substitute a generic or Space Navigator fallback when no compatible
home Dancer is selected. Determinism with one eligible Dancer is a Selection
Service result, not a Launcher fallback.

## 5.1 Default and Alternate Homes

The `HolonSpace` supplies the default home-Dancer candidate set. A later
person-specific, `HolonSpace`-scoped alternate-home preference MAY override
that default before selection. The exact preference representation is deferred;
it MUST remain distinct from Canvas state and preserve a valid HolonSpace
default when no person preference applies.

## 5.2 Explicit Launch Override

An explicit command-line launch argument MAY identify a Dancer as a
launch-policy override. It constrains home-Dancer selection for that
ApplicationSession; it does not add a static Launcher dependency on that
Dancer. If the named Dancer is unavailable, ineligible, or cannot be realized,
the Launcher presents an explicit error and retry path rather than silently
choosing another Dancer.

---

# 6. Startup States and Recovery

An ApplicationSession exposes these observable states:

```text
initializing-host
opening-space
bootstrapping-core
activating-base-packages
realizing-canvas
selecting-home-dancer
realizing-home-dancer
ready
failed
```

`failed` identifies the failed stage and preserves diagnostics appropriate to
that stage. Retrying restarts from the earliest stage whose prerequisite cannot
be trusted; it MUST NOT treat an uncertain bootstrap as complete or reuse an
unrealized Visualizer as if it were mounted.

When Canvas is ready but home-Dancer selection or realization fails, Canvas
MUST present a Dancer-host failure state with retry. A neutral empty Canvas is
permitted only when the active `HolonSpace` deliberately offers no home Dancer;
it is not the fallback for selection or realization failure.

---

# 7. Lifecycle Boundaries

Closing an ApplicationSession coordinates shutdown of its window-bound runtime
resources and Canvas/Dancer realizations. It does not discard committed MAP
state, change Dancer adoption or activation semantics, or automatically commit
an unfinished transaction.

The initial Launcher does not define multi-window placement, tiling,
persistence of Canvas layout, cross-Dancer interaction policy, or a space
chooser. Canvas may develop those desktop-manager capabilities independently.

---

# 8. Invariants

1. Every initial application session has one active local `HolonSpace`.
2. Core Schema is the only intrinsically loaded package.
3. Ordinary runtime loading uses canonical `LoadHolons` Dance execution after
   Core becomes usable.
4. The deprecated receptor ingress path is not a Launcher path.
5. Canvas and home-Dancer Visualizers are selected and materialized through the
   normal Rust Selection Service, SDK/command runtime, and TypeScript
   realization seams.
6. The Launcher does not hard-code Space Navigator or any other Dancer.
7. Canvas hosts the selected Dancer; the selected Dancer owns its internal
   visualizer composition and transaction actions.
8. Launcher state, Canvas state, Dancer experience state, and MAP transaction
   state remain distinct.
