# Dynamic Dancer Runtime POC

## Status

Proposed architecture proof.

This specification captures the current candidate architecture for dynamically loading and executing Dancer implementations in a running MAP environment without recompiling or restarting MAP.

The primary candidate is a MAP-controlled WebAssembly Component runtime hosted in a separate native sidecar process.

The POC should prove the architecture incrementally before MAP's full production deployment architecture is complete.

---

## 1. Motivation

MAP is intentionally open-ended.

Anyone may define and offer new:

- schemas and ontologies;
- visualizers;
- Dancers and their Dances.

Schema extensibility is already substantially addressed through descriptor-driven loading. Loading new descriptors can immediately provide MAP with generic capabilities including:

- holonic storage;
- queryability;
- descriptor-driven validation;
- descriptor-driven visualization;
- generic editing and navigation affordances;
- other behaviors already defined for supported MAP types.

Visualizer extensibility is expected to rely on established dynamic frontend module-loading techniques together with provenance, integrity, compatibility, and sandboxing controls.

Executable behavioral extensibility remains the larger architectural unknown.

MAP must be able to adopt new Dancers into a running environment without:

- recompiling MAP;
- restarting MAP;
- compiling arbitrary third-party implementations into HolonsHost;
- coupling Dancer implementations to Holochain;
- granting downloaded code uncontrolled access to MAP state, local resources, or external endpoints.

This POC addresses that behavioral extensibility problem.

---

## 2. Terminology

### Dance

A **Dance** is a semantic behavior or operation exposed within MAP.

A Dance has a declared request and response contract and may be made available as an affordance on applicable holons.

### Dancer

A **Dancer** is a software agent that provides a coherent set of related Dances.

The Dancer, not each individual Dance, is the natural executable packaging, loading, lifecycle, provenance, and resource-management unit.

Conceptually:

    Dancer
      ├── Dance A
      ├── Dance B
      └── Dance C

### Dancer Artifact

A **Dancer Artifact** is an executable representation of a Dancer suitable for a particular execution environment.

For the candidate architecture, the artifact is a WebAssembly Component.

### MAP Dancer Runtime

The **MAP Dancer Runtime** is a MAP-controlled execution environment responsible for:

- validating Dancer artifacts;
- loading them dynamically;
- instantiating them;
- exposing explicitly granted MAP capabilities;
- invoking Dances;
- returning results;
- enforcing resource and capability boundaries;
- unloading or evicting Dancers.

The candidate runtime is a separate native process embedding Wasmtime or an equivalent WebAssembly Component runtime.

---

## 3. Architectural Principles

### 3.1 Dancers extend behavior; receptors abstract infrastructure

Dancer extensibility and receptor extensibility are separate architectural concerns.

Receptors may abstract infrastructure such as:

- primary holonic persistence;
- Holochain;
- future peer-to-peer storage providers;
- SQLite persistence for staged state and Undo/Redo;
- Yjs or similar collaboration substrates;
- other infrastructure providers.

Dancers should not depend directly on any of those technologies.

A Dancer should interact with MAP semantics through MAP-defined capabilities.

Conceptually:

    Dancer
        ↓
    MAP capability interface
        ↓
    MAP Core
        ↓
    receptors
        ↓
    Holochain / SQLite / Yjs / future substrates

This preserves storage-substrate independence.

### 3.2 MAP remains sovereign over state

A dynamically loaded Dancer MUST NOT establish uncontrolled authoritative state.

A Dancer may perform computation and may request MAP-mediated effects, but authoritative MAP state remains governed by MAP.

For example, a Dancer may request:

- inspection;
- queries;
- creation or staging of holons;
- property mutations;
- relationship mutations;
- other explicitly granted semantic operations.

MAP remains responsible for applicable:

- transaction semantics;
- staging;
- validation;
- authorization;
- provenance;
- Undo/Redo;
- commit;
- receptor interaction;
- persistent storage.

A useful invariant is:

> Dancers may compute behavior and request effects; MAP remains sovereign over effects.

### 3.3 No ambient authority

Dancers MUST NOT gain authority merely because they execute locally.

By default, a Dancer should have no direct access to:

- Holochain;
- receptors;
- arbitrary filesystem paths;
- arbitrary network endpoints;
- environment variables;
- OS processes;
- arbitrary local databases;
- MAP internal memory;
- other Dancers.

Capabilities are explicitly supplied by the MAP Dancer Runtime.

### 3.4 External services remain behind Trust Channels

External services are not a Dancer execution substrate.

Interaction with systems outside the MAP agent membrane is governed by existing Trust Channel architecture.

Depending on the endpoint, communication may occur through:

- Agreement-bound Trust Channels, where participating parties are MAP agents with bilateral signed commitments;
- Declared-External-Commitment-bound Trust Channels, where the local agent declares the degree of trust and permitted information exchange with an endpoint that is not participating as a MAP agent.

A local Dancer that needs an external capability should therefore request use of an authorized Trust Channel rather than receive arbitrary network access.

Conceptually:

    Dancer
        ↓
    MAP capability request
        ↓
    Trust Channel authorization
        ↓
    approved external endpoint

This keeps local computational authority and membrane-crossing authority as distinct security dimensions.

---

## 4. Candidate Execution Architecture

The leading candidate is a separate MAP Dancer Runtime process hosting dynamically loaded WebAssembly Components.

Conceptually:

    MAP Desktop Application

    ┌────────────────────────────────────────────┐
    │ HolonsHost / Tauri process                 │
    │                                            │
    │ MAP Core                                   │
    │ transaction semantics                      │
    │ validation                                 │
    │ authorization                              │
    │ Trust Channels                             │
    │ receptors                                  │
    └───────────────────┬────────────────────────┘
                        │ narrow IPC
                        │
    ┌───────────────────▼────────────────────────┐
    │ MAP Dancer Runtime                         │
    │                                            │
    │ Wasmtime / Component Model                 │
    │ MAP capability bindings                    │
    │                                            │
    │ dynamically loaded Dancer A                │
    │ dynamically loaded Dancer B                │
    │ dynamically loaded Dancer C                │
    └────────────────────────────────────────────┘

The MAP Dancer Runtime itself should have no Tauri or Holochain dependency.

It should ideally depend only on:

- a native runtime implementation;
- WebAssembly Component support;
- MAP-defined typed interfaces;
- the IPC mechanism used to communicate with MAP Core.

This keeps dynamically loaded behavior independent of the active primary-storage technology.

---

## 5. Why a Separate Runtime Process

Embedding Wasmtime directly in HolonsHost remains technically possible, but a separate process is preferred.

The process boundary provides additional isolation beyond the WebAssembly sandbox.

Benefits include:

- Dancer faults do not directly corrupt or crash HolonsHost;
- Dancer runtime memory does not monotonically contaminate the main host process;
- the runtime can be restarted independently;
- runtime caches can be reclaimed independently;
- imported Dancer code does not increase HolonsHost dependency surface;
- Dancer execution remains separable from Tauri;
- Dancer execution remains separable from Holochain;
- different resource limits can be applied to the Dancer process.

The runtime may keep hot Dancers instantiated and evict cold ones.

A possible lifecycle is:

    available
        ↓
    verified
        ↓
    compiled
        ↓
    instantiated
        ↓
    executing
        ↓
    idle
        ↓
    evicted

Compiled artifacts may be cached separately from active instances.

The entire runtime process may also be recycled if necessary without restarting MAP's primary host or conductor.

---

## 6. Deployment Model

For the current desktop architecture, the MAP Dancer Runtime can be packaged as a native sidecar executable launched by the Tauri application.

Conceptually:

    MAP.app
      ├── HolonsHost / Tauri executable
      ├── frontend assets
      ├── Holochain dependencies
      └── map-dancer-runtime

The runtime executable is part of the MAP application distribution.

Individual Dancer artifacts are not.

Dancers may instead be obtained dynamically, for example through Commons:

    Commons
        ↓
    artifact acquisition
        ↓
    provenance / digest / signature verification
        ↓
    local artifact cache
        ↓
    MAP Dancer Runtime
        ↓
    instantiate and invoke

The production deployment proof will eventually need to address:

- sidecar packaging;
- application signing and notarization;
- runtime startup and shutdown;
- process supervision;
- secure IPC establishment;
- Dancer artifact storage;
- Dancer artifact updates;
- runtime updates;
- OS-specific packaging.

Those concerns are separate from the core behavioral-execution POC.

---

## 7. Typed Capability Boundary

The WebAssembly Component Model should be used to define a narrow, typed MAP capability surface.

The exact interface is intentionally not specified yet.

It should be discovered empirically through implementation of real Dancers rather than designed speculatively as a large generic plugin API.

Illustrative capability families might eventually include:

    map:holons/inspect
    map:holons/query
    map:holons/stage
    map:dances/invoke
    map:trust-channels/use

These names are illustrative only.

The architectural requirement is that a Dancer receives only the capabilities needed for the requested operation.

If a capability is not granted, the Dancer should have no alternate path to perform that operation.

---

## 8. Source Acquisition, Format Interpretation, and Holonic Loading

The existing Holons Loader architecture already contains an important abstraction boundary.

Incoming source data is transformed into a source- and format-independent **LoaderRefRep ContentSet** before being supplied to the Holons Loader Dance.

LoaderRefRep content is itself holonic.

This creates three distinct concerns:

    SOURCE ACQUISITION
    local file / Trust Channel / UI / other source
            ↓
    raw content

    FORMAT INTERPRETATION
    TDL / JSON / RDF / future formats
            ↓
    LoaderRefRep ContentSet

    HOLONIC LOAD
    LoaderRefRep ContentSet
            ↓
    Holons Loader Dance
            ↓
    MAP-mediated staged state

This separation should be preserved.

---

## 9. Filesystem Access

The Holons Loader itself does not require filesystem authority.

Its contract already accepts LoaderRefRep ContentSets rather than filenames.

Local file access should therefore remain outside the Loader Dancer.

A preferred flow is:

    DAHN / caller
        ↓
    trusted file selection
        ↓
    host reads explicitly authorized content
        ↓
    raw content / Content Holon
        ↓
    applicable parser Dancer
        ↓
    LoaderRefRep ContentSet
        ↓
    Holons Loader Dancer

The Dancer runtime should not initially expose arbitrary filesystem access.

This avoids granting downloaded code ambient access to the local machine.

It also preserves source independence: identical parsing and loading behavior can be used whether content originated from:

- a local file;
- a Trust Channel;
- an API;
- Commons;
- another MAP agent;
- DAHN;
- generated content;
- any other future source.

---

## 10. Parser Dancers

Format-specific parsing is a promising first practical use of dynamically loaded Dancers.

For example:

    TDL Parser Dancer

    input:
        TDL content

    output:
        LoaderRefRep ContentSet

The parser should not receive a filename and should not require filesystem access.

The host or another trusted source-acquisition mechanism provides the content itself.

This permits parser implementations for arbitrary formats without modifying MAP Core:

    TDL content
        ↓
    TDL Parser Dancer
        ↓
    LoaderRefRep

    JSON content
        ↓
    JSON Parser Dancer
        ↓
    LoaderRefRep

    RDF content
        ↓
    RDF Parser Dancer
        ↓
    LoaderRefRep

    future format
        ↓
    corresponding Parser Dancer
        ↓
    LoaderRefRep

The Holons Loader remains unaware of the original format.

---

## 11. Holons Loader as a Dynamic Dancer

The existing Holons Loader remains a strong long-term candidate for extraction into a dynamically loaded Dancer.

Its runtime contract is already well suited to sandboxing because it consumes LoaderRefRep ContentSets rather than directly acquiring files.

Its responsibilities should remain semantic rather than infrastructural.

Conceptually:

    LoaderRefRep ContentSet
        ↓
    Holons Loader Dancer
        ↓
    MAP capability requests
        ↓
    Nursery / staging
        ↓
    validation
        ↓
    commit
        ↓
    receptors / persistence

The Loader Dancer should not directly persist data.

---

## 12. Bootstrap Loading Caveat

The current Sweettest environment bootstraps Core Schema for every test environment.

That is a consequence of the current single-space/mock-conductor architecture, not necessarily the intended production lifecycle.

In production, the expected model is that:

- one space acts as steward of Core Schema;
- that steward space must bootstrap Core Schema when necessary;
- other spaces reference the stewarded Core Schema rather than loading independent copies.

The future mechanism by which a Space determines whether to:

- bootstrap Core Schema;
- reference an existing steward space;
- obtain or resolve that reference;

remains outside this POC.

The architectural requirement is that bootstrap loading MUST NOT become an unconditional production startup operation.

It should occur only when an appropriate Core Schema reference is unavailable and the current space has responsibility for establishing it.

---

## 13. Avoiding Bootstrap Circularity

The initial POC MUST avoid requiring the dynamically loaded Holons Loader before enough MAP infrastructure exists to discover and execute that Dancer.

For now, bootstrap loading may remain intrinsic.

A possible implementation structure is:

    holons-loader-core
        │
        ├── bootstrap adapter
        │      statically available where required
        │
        └── dynamic Dancer adapter
               compiled as a Wasm Component

This can preserve one semantic loader implementation while allowing two invocation environments.

Longer term, the intrinsic bootstrap path may potentially be reduced further, but that is not required for the dynamic-Dancer POC.

---

## 14. Sweettest Compatibility

Most of the candidate architecture can be proven before MAP has a production deployment.

The existing Sweettest environment can provide MAP state and conductor behavior while the Dancer runtime is exercised independently.

Conceptually:

    Sweettest process
      ├── SweetConductor
      ├── MAP test infrastructure
      └── MAP capability endpoint
                ↑
                │ IPC
                ↓
         map-dancer-runtime
                ↓
         dynamically loaded Dancer

This permits testing of the actual Dancer runtime binary while substituting SweetConductor for the eventual production conductor environment.

The Dancer remains unaware of that distinction.

---

## 15. Recommended POC Sequence

### POC 0 — Minimal External Component

Create a tiny Dancer implementation that is genuinely absent from HolonsHost and loaded only at runtime.

Purpose:

- prove WebAssembly Component compilation;
- prove runtime artifact loading;
- prove typed invocation;
- prove result return;
- prove that previously unknown executable behavior can enter a running environment.

This component should remain intentionally trivial.

### POC 1 — TDL Parser Dancer

Extract or implement TDL parsing as a dynamically loaded Dancer.

Contract:

    TDL content
        →
    LoaderRefRep ContentSet

Purpose:

- exercise meaningful existing MAP-related code;
- prove nontrivial typed data exchange;
- prove a useful dynamically loaded Dancer;
- prove a Dancer can operate without filesystem authority;
- avoid MAP mutation-capability complexity in the first substantial test;
- establish the source-format-intermediate-representation architecture.

The TDL Parser Dancer should behave as essentially pure computation.

### POC 2 — Separate MAP Dancer Runtime Process

Move Wasmtime execution from an in-process test harness into the `map-dancer-runtime` sidecar process.

Purpose:

- prove process isolation;
- prove IPC;
- prove runtime startup/shutdown;
- prove Dancer lifecycle;
- prove load / invoke / unload / reload;
- prove HolonsHost need not embed the runtime.

Initially this may continue to run under Sweettest rather than Tauri.

### POC 3 — Holons Loader Dancer

Extract the runtime Holons Loader as a dynamically loaded Dancer.

Contract:

    LoaderRefRep ContentSet
        →
    MAP-mediated load effects / result

Purpose:

- discover the minimum useful Dancer-to-MAP capability surface;
- prove capability-mediated staging and mutation;
- prove MAP retains state sovereignty;
- prove substantial existing behavior can move outside HolonsHost;
- prove the Dancer remains storage-substrate independent.

Bootstrap loading may continue using an intrinsic adapter.

### POC 4 — Capability-Denial Tests

Deliberately attempt operations that were not granted.

Examples:

- filesystem access;
- network access;
- unsupported MAP mutations;
- arbitrary receptor access.

Expected result:

- the operation is impossible or explicitly denied;
- no alternate ambient path exists.

This is a required architectural proof, not merely a security hardening task.

### POC 5 — Lifecycle and Resource Tests

Exercise:

- repeated load/unload;
- cold eviction;
- compiled artifact reuse;
- multiple Dancers;
- Dancer failure;
- Dancer runtime failure;
- runtime restart;
- resource limits.

Verify that failure or recycling of the Dancer runtime does not require restarting MAP Core or the Holochain conductor.

### POC 6 — Tauri Sidecar Integration

Launch the same `map-dancer-runtime` binary from the MAP Tauri application.

Purpose:

- prove desktop process launch;
- prove real host/runtime IPC;
- prove development deployment topology.

### POC 7 — Packaged Deployment

Package and install MAP with the Dancer runtime sidecar.

Purpose:

- prove production packaging;
- prove signing/notarization;
- prove executable discovery;
- prove artifact directories;
- prove production process supervision;
- prove update lifecycle.

This is the point at which the production deployment architecture itself is considered proven.

---

## 16. POC Success Criteria

The architecture is considered substantially validated when all of the following are demonstrated:

- [ ] MAP can execute a Dancer implementation that was not compiled into HolonsHost.
- [ ] The Dancer can be introduced after MAP has started.
- [ ] MAP does not require recompilation or restart to adopt the Dancer.
- [ ] The Dancer executes as a WebAssembly Component.
- [ ] The production candidate runtime executes outside the HolonsHost process.
- [ ] The runtime itself has no Tauri dependency.
- [ ] The runtime itself has no Holochain dependency.
- [ ] Dancer code sees MAP capabilities rather than receptor or storage technologies.
- [ ] A Dancer can be loaded, invoked, unloaded, and reloaded.
- [ ] A useful TDL Parser Dancer can transform TDL content into LoaderRefRep.
- [ ] The parser requires no filesystem capability.
- [ ] A dynamic Holons Loader Dancer can consume LoaderRefRep.
- [ ] Loader mutations occur only through MAP-mediated capabilities.
- [ ] MAP validation and transaction semantics remain authoritative.
- [ ] Ungranted filesystem access is unavailable.
- [ ] Ungranted network access is unavailable.
- [ ] Ungranted MAP operations are unavailable.
- [ ] Dancer runtime failure can be isolated from MAP Core.
- [ ] The same runtime architecture works against Sweettest and the eventual production MAP host.
- [ ] The Dancer runtime can be launched by the Tauri desktop application.
- [ ] The architecture remains independent of Holochain as the primary storage provider.

---

## 17. Explicit Non-Goals

This POC does not need to resolve:

- full Commons design;
- Dancer marketplace economics;
- complete Dancer provenance/governance policy;
- final signature scheme;
- final compatibility/version negotiation;
- dependency resolution among arbitrary Dancers;
- mobile deployment;
- multi-space Core Schema stewardship protocol;
- production bootstrap discovery;
- every possible Dancer capability;
- arbitrary filesystem capability;
- arbitrary network capability;
- alternate primary-storage receptors;
- Yjs collaboration architecture;
- SQLite staging architecture;
- external hApps as Dancer runtimes.

These may be addressed separately.

---

## 18. Alternatives Considered

### Dynamically installed Holochain coordinator zomes

Coordinator zomes can be changed independently of integrity zomes and remain a technically viable mechanism for privileged Holochain-native extensions.

They are not the preferred general Dancer mechanism because:

- they couple Dancers to Holochain;
- they expose comparatively broad Holochain capabilities;
- they weaken storage-substrate independence;
- they do not naturally provide the narrow MAP-controlled capability boundary desired for arbitrary Commons Dancers.

They may remain useful for privileged or Holochain-specific extensions.

### Separate Holochain hApp or cell

A separate hApp/cell is not considered a primary Dancer implementation substrate.

Once an implementation:

- owns its own cell;
- persists into its own DHT;
- establishes its own authoritative state;

it is better treated as an autonomous external system.

Interaction with such a system belongs behind MAP Trust Channel machinery.

Whether the Trust Channel is Agreement-bound or Declared-External-Commitment-bound depends on the identity and commitment relationship of the external party.

### Remote services

Remote services are not Dancer execution substrates.

They are external endpoints accessed through authorized Trust Channels.

### Native dynamically linked libraries in HolonsHost

Arbitrary dynamically linked native libraries should not be used as the general Dancer extension mechanism.

They create undesirable:

- trust;
- crash isolation;
- ABI compatibility;
- portability;
- unloading;
- dependency;
- supply-chain;
- host contamination

problems.

---

## 19. Architectural Invariants Emerging from the POC

The current candidate architecture should preserve the following invariants.

### Behavioral extensibility is independent of storage implementation

> Dancers extend MAP behavior; receptors abstract MAP infrastructure.

### State sovereignty remains with MAP

> Dynamically loaded code may request MAP effects but may not establish uncontrolled authoritative MAP state.

### External communication crosses the membrane explicitly

> Dancers do not receive ambient network access; external interactions use authorized Trust Channels.

### Source acquisition, format parsing, and semantic loading are independent

> A source does not determine a format, and a format does not determine the Holons Loader.

### LoaderRefRep is the import intermediate representation

> Format-specific importers produce LoaderRefRep ContentSets; the Holons Loader consumes LoaderRefRep rather than source-specific representations.

### Dancer packaging occurs at the software-agent level

> A Dancer is the executable/lifecycle unit and may expose many Dances.

### Dynamic executable code has no ambient authority

> Local execution alone conveys no permission to filesystem, network, MAP state, receptors, or external endpoints.

---

## 20. Desired End State

The intended architectural result is:

    arbitrary external source
            ↓
    MAP-controlled acquisition
            ↓
    raw content
            ↓
    dynamically selected Parser Dancer
            ↓
    LoaderRefRep ContentSet
            ↓
    dynamically loaded Holons Loader Dancer
            ↓
    MAP capability boundary
            ↓
    staging / validation / transactions / commit
            ↓
    receptor abstraction
            ↓
    active persistence substrate

More generally:

    Commons
        ↓
    discover Dancer
        ↓
    acquire + verify artifact
        ↓
    MAP Dancer Runtime
        ↓
    instantiate with explicit capabilities
        ↓
    invoke Dance
        ↓
    MAP-mediated effects and/or holonic result
        ↓
    unload or retain according to runtime policy

If the POC succeeds, MAP gains a general-purpose, dynamically extensible behavioral substrate that is:

- sandboxed;
- storage-technology agnostic;
- independent of Tauri;
- independent of Holochain;
- capable of on-demand loading;
- compatible with MAP's holonic request/response model;
- aligned with MAP's existing transaction, receptor, and Trust Channel architecture.

