---
title: Dancers Design Specification
description: Normative architecture for Dancer representation, dependency declaration, adoption, activation, implementation resolution, capability mediation, and House Troupe realization in MAP.
status: draft
---

# Dancers Design Specification

## 1. Purpose

This specification defines the normative MAP architecture for **Dancers**.

The conceptual meaning of Dance, Dancer, Repertory, Troupe, House Troupe, adoption, and activation is defined in `dancers-concept.md`.

This specification defines how those concepts are realized architecturally.

It establishes requirements for:

- Dancer representation;
- Dancer-to-Dance relationships;
- semantic dependency declaration;
- adoption into an AgentSpace;
- activation and deactivation;
- implementation resolution;
- separation of Dancer identity from executable implementation;
- capability mediation;
- MAP sovereignty over effects;
- external interaction through Trust Channels;
- House Troupe organization;
- repository boundaries;
- the initial Space Navigator realization;
- compatibility with future dynamically loaded Dancer implementations.

The initial implementation MUST support Space Navigator as the first concrete Dancer without requiring completion of the future Dynamic Dancer Runtime.

---

## 2. Scope

This specification covers the semantic and runtime seams required for Dancers to exist as independently represented MAP software Agents.

It does not define:

- the complete Dance invocation protocol, which is defined by the Dance architecture;
- the complete Agent ingestion or entitlement architecture;
- Commons discovery and marketplace behavior;
- the final executable artifact format;
- the final dynamic execution runtime;
- executable signing and provenance protocols;
- a comprehensive Dancer lifecycle state machine.

Those concerns may evolve independently provided they preserve the contracts established here.

---

## 3. Design Principles

### 3.1 Dancer is a Core abstraction

`Dancer` MUST be defined as a MAP Core semantic concept.

MAP Core MUST define enough semantics to:

- identify a Holon as a Dancer;
- identify the Dances offered by that Dancer;
- represent applicable Dancer dependencies;
- support adoption and activation semantics;
- resolve implementations of offered Dances;
- mediate the Dancer's access to MAP capabilities.

Concrete Dancers MUST NOT become part of MAP Core solely because they are distributed with MAP.

### 3.2 Concrete Dancers remain outside Core

A concrete Dancer MAY introduce:

- schemas;
- modules;
- types;
- relationships;
- Visualizers;
- Dances;
- other semantic resources.

Those resources SHOULD remain associated with the concrete Dancer rather than being added to Core unless they are independently determined to be foundational MAP concepts.

### 3.3 Semantic identity is independent of implementation

A Dancer's identity MUST NOT depend on:

- a Rust crate;
- a TypeScript module;
- a WebAssembly artifact;
- a process;
- a Holochain zome;
- a filesystem location;
- a deployment package.

Implementation artifacts realize Dancer behavior but do not define Dancer identity.

### 3.4 Dancers extend behavior; receptors abstract infrastructure

A Dancer MUST operate against MAP semantic capabilities rather than directly against infrastructure providers.

A Dancer implementation SHOULD NOT depend directly upon:

- Holochain;
- SQLite;
- Yjs;
- conductor APIs;
- storage-provider-specific APIs;
- other receptor implementations.

Infrastructure-specific behavior belongs behind receptor boundaries.

### 3.5 MAP remains sovereign over effects

Dancer execution MUST NOT bypass MAP's authoritative semantics for:

- authorization;
- validation;
- staging;
- transactions;
- provenance;
- Undo/Redo;
- commit;
- persistence.

A Dancer may compute behavior and request effects.

MAP remains sovereign over those effects.

---

## 4. Dancer Semantic Model

### 4.1 Dancer Type

MAP Core SHALL define a `Dancer` Holon Type.

The exact descriptor properties remain subject to schema design, but the semantic model MUST support at least:

- stable Dancer identity;
- descriptive metadata;
- stewardship;
- offered Dances;
- semantic dependencies;
- implementation-resolution information.

The Dancer Type MUST NOT encode assumptions about a particular executable runtime.

### 4.2 Offered Dances

A Dancer MUST be able to declare the Dances in its Repertory.

Conceptually:

    Dancer
        |
        +-- OffersDance --> Dance
        +-- OffersDance --> Dance
        +-- OffersDance --> Dance

The exact relationship name MAY differ according to established MAP descriptor naming conventions.

The relationship MUST be semantically many-valued.

A Dance MAY be offered by more than one Dancer where such reuse is semantically valid.

### 4.3 Repertory

Repertory is derived from the Dances offered by a Dancer or by the members of a Troupe.

The initial implementation does not require `Repertory` to exist as a separately persisted collection Holon unless another design requirement justifies doing so.

A Dancer's Repertory MAY therefore initially be derived from its Dance relationships.

---

## 5. Dancer Dependencies

### 5.1 Explicit dependency declaration

A Dancer SHOULD explicitly declare semantic resources required for its operation.

Dependencies MAY include:

- Schemas;
- Modules;
- Holon Types;
- other Dances;
- Visualizer definitions;
- other Dancers;
- other semantically identifiable resources.

Dependencies MUST NOT be inferred solely from implementation code where they can be represented semantically.

### 5.2 Dependency stewardship

A Dancer MUST NOT be assumed to steward every dependency it requires.

For example:

    SpaceNavigator.Dancer
        |
        +-- Requires --> DAHN Schema
        +-- Requires --> Space Navigator Schema

A schema MAY be independently stewarded and shared among multiple Dancers.

### 5.3 Dependency availability

Activation MUST ensure that required semantic dependencies are available or resolvable.

The mechanism used to satisfy a dependency MAY vary.

For the initial implementation, a required schema MAY be loaded from a locally distributed resource.

Future implementations MAY instead resolve the same schema from a steward Space or another authorized source.

The Dancer contract MUST remain independent of that acquisition mechanism.

---

## 6. Adoption

### 6.1 Meaning

Adoption establishes a Dancer as belonging within an AgentSpace, typically an Agent's I-Space.

The detailed relationship between Dancer adoption and the broader Agent ingestion architecture remains subject to separate design.

### 6.2 Adoption is not activation

A Dancer MAY be adopted while inactive.

Adoption MUST NOT imply that:

- executable code remains resident;
- every dependency has been eagerly loaded;
- every offered Dance is immediately executable;
- runtime resources are permanently allocated.

### 6.3 House Troupe Dancers

The mechanism by which House Troupe Dancers become available to a Traveler MAY differ from adoption of Dancers discovered elsewhere.

That difference MUST NOT create a distinct semantic Dancer subtype.

Once available within an I-Space, a House Troupe Dancer and any other Dancer MUST participate in the same generic Dancer lifecycle semantics.

---

## 7. Activation

### 7.1 Activate Dance

MAP Core SHALL provide a generic semantic operation for activating a Dancer.

Conceptually:

    Activate(Dancer)

The exact Dance name and request/response descriptor SHALL follow existing Dance naming and descriptor conventions.

### 7.2 Activation contract

Activation means:

> Make the Dancer's declared capabilities available within the current MAP environment.

Activation MUST NOT be defined as synonymous with any particular implementation action such as:

- loading a module;
- starting a process;
- instantiating WebAssembly;
- registering a Rust implementation;
- loading a schema.

Those actions may be required to satisfy activation but are not themselves its semantic meaning.

### 7.3 Activation responsibilities

Activation MUST ensure, either eagerly or lazily, that:

1. the Dancer is available to the current AgentSpace;
2. required semantic dependencies can be resolved;
3. required descriptors are available;
4. implementations for invoked Dances can be resolved;
5. applicable runtime authority can be established;
6. the Dancer's Repertory can be exposed as available affordances.

### 7.4 Idempotence

Activating an already-active Dancer SHOULD be idempotent.

It MUST NOT:

- duplicate schemas;
- duplicate Dancer identity;
- create duplicate semantic relationships;
- unnecessarily reload already-satisfied dependencies.

### 7.5 Partial activation failure

If activation cannot satisfy a required dependency or implementation requirement, activation MUST fail explicitly.

Failure MUST NOT leave the Dancer represented as fully active when required capabilities are unavailable.

The initial implementation MAY use coarse-grained activation failure semantics.

More detailed degraded or partially-active states are deferred.

---

## 8. Deactivation

A generic `Deactivate` operation MAY be introduced with the initial Dancer lifecycle if needed by the Space Navigator track.

Deactivation means:

> Stop exposing the Dancer's currently active capabilities while preserving its semantic identity and adoption.

Deactivation MUST NOT imply:

- deletion of the Dancer;
- removal from an I-Space;
- removal from the House Troupe;
- deletion of schemas;
- deletion of data previously created through its Dances.

Whether implementation artifacts or cached resources are unloaded following deactivation is a runtime policy, not part of the semantic definition.

The initial Space Navigator implementation MAY defer Deactivate if no MVP behavior requires it.

---

## 9. Implementation Resolution

### 9.1 Resolution seam

MAP MUST provide an implementation-resolution seam between a Dance's semantic identity and the executable behavior that realizes it.

Conceptually:

    Dance invocation
          |
          v
    implementation resolution
          |
          v
    executable implementation

Callers MUST NOT need to know whether the implementation is:

- statically linked;
- locally bundled;
- dynamically loaded;
- remotely acquired and cached;
- hosted by a future runtime mechanism.

### 9.2 Bundled implementations

The initial implementation MAY resolve some Dances to implementations already bundled in the Host.

Bundling MUST be treated as an acquisition and deployment optimization.

It MUST NOT:

- alter Dancer semantics;
- create a bundled Dancer subtype;
- bypass generic activation;
- become encoded into Dance request contracts;
- make concrete Dancers part of MAP Core.

### 9.3 Future dynamic resolution

The resolution boundary MUST permit future substitution of dynamically acquired implementations without changing:

- Dancer identity;
- Dance identity;
- Dance request descriptors;
- Dance response descriptors;
- adoption semantics;
- activation semantics.

---

## 10. Dancer Capability Boundary

### 10.1 Explicit authority

A Dancer implementation MUST receive only the MAP authority required to perform its behavior.

Execution locality MUST NOT grant ambient authority.

### 10.2 MAP capabilities

A Dancer MAY require MAP capabilities such as:

- inspecting Holons;
- projecting values;
- traversing relationships;
- querying;
- creating or staging Holons;
- modifying staged properties;
- modifying staged relationships;
- invoking other Dances;
- requesting authorized Trust Channel use.

The exact generic Dancer capability interface remains outside the initial Space Navigator scope.

### 10.3 Direct infrastructure access

The general Dancer architecture MUST NOT require Dancers to access receptors directly.

A Dancer SHOULD NOT directly:

- write to Holochain;
- access a primary storage provider;
- manipulate SQLite staging storage;
- participate directly in Yjs;
- bypass MAP transaction semantics.

Such capabilities must remain mediated by MAP abstractions.

---

## 11. State-Changing Dances

When a Dancer performs behavior that affects MAP state, its implementation MUST operate through MAP-owned state-transition mechanisms.

Conceptually:

    Dancer
        |
        | requests semantic effect
        v
    MAP
        |
        +-- authorization
        +-- staging
        +-- validation
        +-- transaction semantics
        +-- provenance
        +-- commit
        |
        v
    receptors

A Dancer MUST NOT create an alternate authoritative persistence path for MAP state.

This requirement applies regardless of whether the implementation is currently bundled or dynamically loaded.

---

## 12. External Interaction

### 12.1 External endpoints

External services and autonomous external applications are not Dancer implementation substrates merely because a Dancer interacts with them.

Interaction beyond the AgentSpace membrane remains governed by MAP Trust Channel architecture.

### 12.2 Trust Channel mediation

A Dancer requiring communication with an external endpoint MUST use the applicable authorized Trust Channel mechanism.

The implementation SHOULD request MAP-mediated access to the channel rather than receiving unrestricted network authority.

Depending on the endpoint, the Trust Channel may be bound by:

- an Agreement between MAP Agents; or
- a Declared External Commitment governing interaction with an endpoint that does not participate as a MAP Agent.

### 12.3 Orthogonal authority dimensions

Local computational authority and membrane-crossing authority MUST remain independent.

Authorization to inspect or transform MAP data does not inherently authorize that data to leave the AgentSpace.

---

## 13. Troupes

### 13.1 Troupe Type

MAP SHOULD represent Troupe as a semantic collection of Dancers where explicit Troupe identity is useful.

A Troupe MUST NOT create a distinct Dancer subtype.

### 13.2 Membership

Troupe membership MUST be independently stewardable from the Dancer itself.

A Dancer's behavior MUST NOT change merely because it is a member of a particular Troupe unless separate semantic relationships explicitly provide additional context.

### 13.3 Repertory derivation

A Troupe's Repertory SHOULD be derivable from the Repertories of its member Dancers.

The initial design does not require duplicating those Dance relationships onto the Troupe.

---

## 14. House Troupe

### 14.1 Definition

The House Troupe is the MAP-stewarded Troupe included with the standard MAP experience.

### 14.2 Membership governance

House Troupe membership MUST be controlled by the stewardship context responsible for the House Troupe.

Travelers MUST NOT be given an ordinary affordance to mutate House Troupe membership.

Travelers MAY independently:

- activate House Troupe Dancers available to them;
- deactivate them where permitted;
- adopt additional non-House Dancers into their own I-Spaces.

### 14.3 No subtype semantics

House Troupe membership MUST NOT:

- create a `HouseDancer` subtype;
- change the Dancer lifecycle;
- grant additional runtime authority merely by membership;
- require a distinct implementation mechanism.

### 14.4 Distribution independence

A House Troupe Dancer MAY initially ship with its semantic resources and implementation within the MAP distribution.

Its semantic identity MUST remain independent of that distribution mechanism.

---

## 15. Repository Architecture

### 15.1 MAP Core Dancer implementation

Generic Dancer semantic implementation belongs in the existing Core/shared architecture.

Where Rust logic must compile into both Host and hApp execution contexts, it SHALL follow the existing `shared_crates/` constraints.

Generic Core Dancer code MUST NOT depend on Space Navigator or any other concrete Dancer.

### 15.2 House Troupe package resources

The repository SHALL provide a peer-level directory for House Troupe semantic packages:

    house-troupe/
        space-navigator/
        ...

`house-troupe/` is not an execution workspace.

It represents a MAP extension-package organization boundary.

### 15.3 Executable code location

Executable code for a House Troupe Dancer MUST continue to reside in the workspace corresponding to where that code actually executes.

For example, the initial Space Navigator implementation executes in the Host/HX environment and therefore remains under the Host workspace.

Conceptually:

    house-troupe/
        space-navigator/
            semantic package resources

    host/
        ...
        space-navigator/
            current executable implementation

### 15.4 No new execution context

Introducing `house-troupe/` MUST NOT create a new Cargo workspace or runtime execution class.

The repository SHALL continue to mirror actual execution contexts according to the existing repository architecture.

---

## 16. Documentation Architecture

Generic Dancer documentation SHALL live under the Core documentation hierarchy:

    docs/
        core/
            dancers/
                dancers-concept.md
                dancers-design-spec.md
                index.md

Concrete House Troupe Dancer documentation SHALL live outside Core:

    docs/
        house-troupe/
            space-navigator/
                ...

This reflects the semantic boundary:

    Core
        defines what a Dancer is

    House Troupe
        contains concrete MAP-stewarded Dancers

---

## 17. Space Navigator Initial Realization

### 17.1 Classification

Space Navigator SHALL be represented as:

- a concrete Dancer;
- outside MAP Core;
- a member of the House Troupe.

### 17.2 Space Navigator schema

Space Navigator-specific schema resources SHOULD NOT be added to the Core Schema solely because Space Navigator is part of the standard MAP experience.

Those resources SHOULD remain separately loadable.

### 17.3 Activation

Activating Space Navigator SHOULD:

1. resolve `SpaceNavigator.Dancer`;
2. determine whether its required semantic dependencies are available;
3. load or otherwise resolve missing Space Navigator semantic resources;
4. make the applicable Space Navigator descriptors available;
5. resolve its currently bundled implementation;
6. expose its Repertory as available affordances.

### 17.4 Bundled executable implementation

The initial Space Navigator executable implementation MAY remain bundled within the Host workspace.

Activation MUST nevertheless pass through the generic Dancer lifecycle and implementation-resolution seam.

Space Navigator code MUST NOT be treated as intrinsic MAP Core behavior merely because its implementation is currently bundled.

### 17.5 Testing

Space Navigator tests SHOULD explicitly establish the Dancer environment they require.

Tests unrelated to Space Navigator SHOULD NOT require loading Space Navigator-specific schemas merely because Space Navigator belongs to the House Troupe.

Conceptually:

    generic MAP test
        Core Schema

    Space Navigator test
        Core Schema
            +
        Activate SpaceNavigator.Dancer
            ↓
        resolve Space Navigator resources

This separation SHOULD help prevent optional Dancer schemas from increasing baseline bootstrap costs for unrelated tests.

---

## 18. Core Schema Boundary

The Core Schema SHOULD contain only the generic semantic machinery necessary to represent and work with Dancers.

The initial Dancer work MAY require Core additions for:

- `Dancer`;
- `Troupe`;
- Dancer-to-Dance relationships;
- Dancer dependency relationships;
- generic lifecycle Dances such as Activate;
- any minimal descriptor types required for implementation resolution.

The Core Schema SHOULD NOT contain:

- `SpaceNavigator.Dancer`;
- Space Navigator-specific Visualizer Types;
- Space Navigator-specific schemas or modules;
- other concrete House Troupe Dancer definitions.

The exact TDL changes SHALL be specified separately in the applicable schema design and implementation work.

---

## 19. Dynamic Dancer Runtime Compatibility

The eventual Dynamic Dancer Runtime is expected to support executable implementations that can be introduced without recompiling or restarting MAP.

The current POC is exploring WebAssembly Components hosted by a MAP-controlled sidecar runtime.

This specification does not make that implementation technology normative.

Any future Dynamic Dancer Runtime MUST preserve the following requirements:

1. Dancer identity remains independent of executable artifacts.
2. A Dancer may expose many Dances.
3. Dance request and response contracts remain semantic MAP contracts.
4. implementation resolution remains hidden from callers.
5. Dancer code operates through explicit MAP capabilities.
6. Dancer implementations remain independent of receptors.
7. MAP remains authoritative over state-changing effects.
8. external communication remains Trust Channel mediated.
9. executable locality does not grant ambient authority.
10. implementations may be loaded or unloaded without changing Dancer identity.
11. dynamically introducing a new Dancer implementation does not require recompiling MAP Core.

---

## 20. Initial MVP Scope

The initial implementation required for the Space Navigator track SHALL be deliberately narrow.

### Required

- Core `Dancer` semantic concept;
- minimum relationship from Dancer to its offered Dances;
- ability to represent semantic dependencies needed by Space Navigator;
- House Troupe representation or equivalent stewarded membership relationship;
- `SpaceNavigator.Dancer` outside Core;
- generic `Activate` semantics;
- on-demand availability of Space Navigator schema resources;
- implementation-resolution seam;
- resolution to the currently bundled Space Navigator Host implementation;
- tests proving that Space Navigator-specific resources need not be loaded for unrelated MAP operation.

### Deferred

The Space Navigator track does not require:

- WebAssembly execution;
- Wasmtime;
- the MAP Dancer Runtime sidecar;
- WIT or another final Dancer ABI;
- executable artifact acquisition from Commons;
- executable signature validation;
- general capability grants for arbitrary third-party code;
- runtime eviction or executable caching;
- production sidecar packaging;
- arbitrary dynamic Dancer installation;
- a comprehensive lifecycle state machine;
- final Dancer dependency-resolution architecture.

The MVP MUST preserve seams for those capabilities without implementing them prematurely.

---

## 21. Validation and Error Semantics

### 21.1 Invalid Dancer

Activation MUST fail if the target does not conform to the required Dancer semantics.

### 21.2 Missing semantic dependency

If a required semantic dependency cannot be resolved, activation MUST fail with a distinguishable error.

### 21.3 Missing implementation

If required semantic resources are available but no applicable implementation can be resolved for a required Dance, invocation MUST fail explicitly.

The system MUST NOT silently treat the absence of an implementation as absence of the Dance's semantic definition.

### 21.4 Duplicate activation

Repeated activation MUST NOT produce duplicate semantic resources or duplicate Dancer instances.

### 21.5 Infrastructure failure

Failures from underlying loaders, repositories, receptors, or other infrastructure SHOULD preserve their meaningful existing error semantics rather than being collapsed into a generic Dancer failure.

---

## 22. Architectural Testing

The initial Dancer architecture SHOULD include tests proving the semantic boundaries established by this specification.

At minimum, tests SHOULD verify:

- `Dancer` exists as a Core concept;
- `SpaceNavigator.Dancer` is not part of Core Schema;
- Space Navigator declares its offered Dances;
- Space Navigator dependencies can be resolved on activation;
- activating Space Navigator loads or resolves required semantic resources when absent;
- activating Space Navigator is idempotent;
- Space Navigator's bundled implementation is resolved through an explicit seam;
- unrelated tests do not require Space Navigator schema loading;
- Dancer identity is independent of implementation identity;
- House Troupe membership does not change Dancer type semantics.

Future Dynamic Dancer Runtime tests will additionally verify executable isolation and capability enforcement.

---

## 23. Architectural Invariants

The implementation SHALL preserve the following invariants.

### Core defines Dancer; concrete Dancers remain extensions

> MAP Core defines the Dancer abstraction but does not absorb concrete Dancers merely because they ship with MAP.

### A Dance is behavior; a Dancer is the agentic boundary

> Individual Dances remain semantic affordances while a Dancer groups a coherent Repertory into an adoptable and activatable software Agent.

### Troupe membership is orthogonal to Dancer type

> Membership in a Troupe, including the House Troupe, does not produce a distinct kind of Dancer.

### Adoption and activation remain distinct

> Adoption establishes presence in an AgentSpace; activation makes the Dancer's capabilities available.

### Activation is semantic

> Activate means make a Dancer's capabilities available, not perform a specific executable-loading operation.

### Semantic identity is independent of implementation

> Neither Dancer nor Dance identity depends upon how executable behavior is currently resolved.

### Dancers extend behavior; receptors abstract infrastructure

> Dancer implementations operate against MAP capabilities rather than receptor technologies.

### MAP remains sovereign over effects

> A Dancer may request state-changing behavior but may not bypass MAP's authoritative state-transition machinery.

### Membrane crossing is explicit

> External communication remains governed by Trust Channels rather than implicit network authority.

### Repository structure follows execution context

> House Troupe package organization does not introduce a new runtime workspace; executable code remains in the workspace where it actually executes.

---

## 24. Open Design Areas

The following remain intentionally unresolved:

- exact `Dancer` TypeDescriptor properties;
- exact relationship names and cardinalities;
- whether Repertory requires an explicit Holon Type;
- exact Troupe representation;
- House Troupe stewardship representation;
- exact dependency descriptor model;
- dependency version constraints;
- transitive dependency handling;
- final adoption versus ingestion semantics;
- entitlement rules for non-House Dancers;
- exact activation response contract;
- degraded or partial activation states;
- Deactivate semantics beyond the conceptual definition;
- implementation selection where multiple compatible implementations exist;
- artifact identity and versioning;
- executable provenance and signatures;
- Dynamic Dancer Runtime technology;
- Dancer capability ABI;
- Dancer-to-Dancer invocation authority;
- resource limits and runtime lifecycle;
- Commons acquisition and discovery.

These areas MUST be resolved through subsequent design work rather than implicitly encoded in the Space Navigator implementation.

---

## 25. Related Documents

- `dancers-concept.md` — conceptual foundation for Dancers, Repertories, Troupes, House Troupe, adoption, and activation.
- Dance design specifications — Dance descriptors and invocation semantics.
- Space Navigator concept, architecture, interaction grammar, design specification, and implementation plan — initial concrete Dancer.
- `dynamic-dance-poc.md` — proof plan for dynamically loaded executable Dancer implementations.
- Trust Channel specifications — governed interaction across AgentSpace membranes.
- receptor specifications — infrastructure abstraction.
- transaction specifications — staging, validation, Undo/Redo, and commit.
- repository `ARCHITECTURE.md` — execution-context and workspace boundaries.