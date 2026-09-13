---
title: Dancers
description: Conceptual model for Dancers, Troupes, Repertories, adoption, activation, and the House Troupe in MAP.
status: draft
---

# Dancers

## Purpose

A **Dancer** is a software Agent that provides a coherent set of related **Dances**.

Dancers are an important unit of extensibility in MAP. They allow new behavioral capabilities to be introduced without expanding MAP Core with every capability that may eventually exist in the ecosystem.

A Dancer is represented holonically. Its identity, capabilities, relationships, dependencies, provenance, and lifecycle can therefore be described and reasoned about using the same semantic substrate as other MAP concepts.

This document establishes the conceptual model for Dancers. It intentionally separates the meaning of a Dancer from the particular technologies by which its executable implementation may be acquired, loaded, or executed.

---

## Dance and Dancer

A **Dance** is a named, invocable semantic behavior or operation.

A **Dancer** is the software Agent that offers a coherent set of related Dances.

Conceptually:

    Dancer
      ├── Dance A
      ├── Dance B
      └── Dance C

This distinction is important.

A Dance is an individual affordance.

A Dancer is the agentic boundary that gathers related affordances into a coherent capability.

A Dancer may therefore offer many fine-grained Dances while remaining one discoverable, adoptable, activatable, and stewardable software Agent.

---

## Dancers as Software Agents

A Dancer is not merely a code library, executable artifact, service endpoint, or deployment package.

It is a **software Agent represented within MAP**.

Its holonic representation may describe such things as:

- its identity;
- its purpose;
- the Dances it offers;
- semantic resources on which those Dances depend;
- provenance and stewardship;
- implementation references;
- compatibility information;
- other affordances associated with the Dancer itself.

Because the Dancer exists semantically independently of its executable implementation, MAP can know about, inspect, discover, reference, or reason about a Dancer even when no implementation code for it is currently loaded.

Conceptually:

    Dancer
        semantic identity
        purpose
        repertory
        dependencies
        provenance
        implementation references
              │
              ▼
    implementation resolution
              │
              ▼
    executable behavior

The executable implementation realizes the Dancer's behavior.

It does not define the Dancer's identity.

---

## Repertory

A **Repertory** is the collection of Dances that a Dancer or Troupe can perform.

A Dancer's repertory is the coherent set of affordances it offers.

For example:

    Foo Dancer
      ├── Import Foo
      ├── Validate Foo
      ├── Synchronize Foo
      └── Export Foo

Those Dances collectively form the Foo Dancer's repertory.

A Troupe's repertory is the combined set of Dances offered by its member Dancers.

Repertory therefore describes **available behavior**, not the collection of Dancers themselves.

---

## Troupes

A **Troupe** is a stewarded collection of Dancers.

Troupe membership groups Dancers for some meaningful purpose without creating a different kind of Dancer or changing the semantics of the member Dancers.

Conceptually:

    Troupe
      ├── Dancer A
      ├── Dancer B
      └── Dancer C

A Troupe can therefore have a combined Repertory derived from the Dances offered by its members.

The meaning of a particular Troupe depends on how and why that collection is stewarded.

---

## House Troupe

The **House Troupe** is the MAP-stewarded collection of Dancers included as part of the standard MAP experience.

For example, Space Navigator may be a member of the House Troupe.

House Troupe membership is a stewardship and distribution choice.

It does **not** define a distinct kind of Dancer.

A House Troupe Dancer:

- has the same Dancer semantics as any other Dancer;
- follows the same lifecycle as any other Dancer;
- may ultimately use the same implementation-resolution mechanisms as any other Dancer;
- does not become part of MAP Core merely because MAP includes it in the standard experience.

The House Troupe is therefore analogous to the set of applications that come pre-provided with a general-purpose computing environment.

They are ordinary applications whose inclusion has been stewarded as part of the default experience.

---

## MAP Core and the House Troupe

**Dancer** is a MAP Core concept.

Individual members of the House Troupe generally are not.

MAP Core provides the semantic foundation that makes Dancers possible.

The House Troupe provides concrete capabilities built upon that foundation.

Conceptually:

    MAP Core
      └── defines Dancer

    House Troupe
      ├── Space Navigator Dancer
      ├── ...
      └── other MAP-stewarded Dancers

This distinction allows the standard MAP experience to grow without requiring every new capability to become part of MAP Core.

It also prevents the Core Schema from accumulating descriptors that are needed only by optional or higher-level capabilities.

---

## Dancer Semantic Dependencies

A Dancer may depend on semantic resources that are not themselves part of MAP Core.

These may include:

- schemas;
- modules;
- types;
- relationships;
- Dances;
- Visualizers;
- other semantic resources.

Those dependencies should remain distinguishable from the Dancer's executable implementation.

For example, activating Space Navigator may require making its DAHN and Space Navigator schema resources available before its behaviors can be used.

A Dancer need not steward every semantic resource it uses.

Multiple Dancers may depend upon shared schemas or other independently stewarded resources.

This allows Dancer packages to remain cohesive while avoiding unnecessary duplication.

---

## Adoption

A Dancer may exist in the broader MAP ecosystem without being available inside a particular Traveler's I-Space.

**Adoption** brings a Dancer into an I-Space as an available software Agent.

Conceptually:

    Commons / broader ecosystem
              │
              │ adopt
              ▼
          Traveler's I-Space
              │
              └── Foo Dancer

The detailed offer, entitlement, Agreement, Trust Channel, and ingestion processes by which adoption occurs may vary and are defined elsewhere.

The important conceptual distinction is that adoption concerns **which Dancers belong within an Agent's own environment**.

---

## House Troupe Membership and Adoption

House Troupe membership and I-Space adoption are different relationships.

House Troupe membership is a MAP stewardship decision.

I-Space adoption is an Agent decision.

MAP Travelers may adopt additional Dancers into their own I-Spaces.

They do not thereby add those Dancers to the House Troupe.

Likewise, Travelers do not modify House Troupe membership.

Conceptually:

    House Troupe
        MAP-stewarded membership

    Traveler's I-Space
        Traveler-stewarded adoption

    Commons
        broader discoverable ecosystem

This allows all Dancers to retain identical semantics while participating in different stewardship contexts.

---

## Activation

Adoption does not necessarily mean that a Dancer is currently active.

**Activation** makes a Dancer's declared capabilities available within the current MAP environment.

Conceptually:

    adopted Dancer
          │
          │ Activate
          ▼
    available repertory

Activation may require such things as:

- resolving semantic dependencies;
- making required descriptors available;
- resolving implementations of offered Dances;
- preparing whatever runtime resources are required;
- establishing applicable permissions or capabilities.

These are mechanisms used to accomplish activation.

They are not the meaning of activation itself.

The conceptual meaning remains:

> **Activate a Dancer means make its capabilities available for use.**

---

## Adoption and Activation Are Independent

A Dancer may be adopted but inactive.

Deactivation does not imply that the Dancer has ceased to belong to the I-Space.

Likewise, implementation code need not remain loaded merely because the Dancer remains adopted or active.

These are distinct concerns:

    adoption
        Does this Dancer belong in this Agent's environment?

    activation
        Are this Dancer's capabilities currently available?

    implementation residency
        Is executable code currently loaded?

Keeping these concepts independent allows MAP to support lazy loading, unloading, caching, alternate runtime technologies, and other implementation strategies without changing the semantic lifecycle of the Dancer.

---

## Semantic Identity and Implementation

A Dancer's semantic identity must remain independent of the technology that implements it.

A Dancer may initially have an implementation bundled with MAP.

Another Dancer may eventually have an implementation acquired dynamically.

A future Dancer could potentially have compatible implementations available for different execution environments.

None of these differences imply different Dancer semantics.

Conceptually:

    Dancer
      │
      └── offers Dance
              │
              ▼
       implementation resolution
              │
       ┌──────┴────────┐
       ▼               ▼
    bundled         dynamically
    implementation  resolved implementation

The implementation mechanism is replaceable.

The Dancer and Dance contracts remain stable.

---

## Dancers and Receptors

Dancers and receptors represent different kinds of MAP extensibility.

> **Dancers extend behavior; receptors abstract infrastructure.**

A Dancer should operate in terms of MAP semantics.

It should not require knowledge of the infrastructure technology currently providing those semantics.

Conceptually:

    Dancer
        │
        ▼
    MAP semantic capabilities
        │
        ▼
    MAP runtime
        │
        ▼
    receptors
        │
        ▼
    infrastructure

This allows the same Dancer model to remain valid regardless of whether a particular MAP capability is ultimately backed by Holochain, SQLite, Yjs, or some future substrate.

---

## Dancers and MAP State

Dancers may perform computation and participate in operations that affect MAP state.

They do not thereby become independent authorities over that state.

MAP remains responsible for its own applicable semantics, including:

- authorization;
- validation;
- staging;
- transactions;
- provenance;
- Undo and Redo;
- commit;
- persistence.

A useful conceptual invariant is:

> **Dancers may compute behavior and request effects; MAP remains sovereign over effects.**

This keeps the behavioral extensibility of Dancers compatible with the integrity and sovereignty guarantees of the surrounding AgentSpace.

---

## Dancers and the Agent Membrane

A Dancer's presence inside an Agent's environment does not imply unrestricted authority to communicate outside that environment.

Interaction across the AgentSpace membrane remains governed by MAP Trust Channel semantics.

A Dancer that needs an external service therefore operates through whatever Trust Channel relationships and commitments authorize that interaction.

Conceptually:

    Dancer
        │
        ▼
    MAP-mediated interaction
        │
        ▼
    Trust Channel
        │
        ▼
    external Agent or endpoint

This keeps two forms of authority distinct:

- authority to perform computation within MAP;
- authority to exchange information across the membrane.

---

## Space Navigator as the First Dancer

Space Navigator is the first concrete Dancer being introduced through the DAHN / Space Navigator implementation track.

It provides a useful first realization of the Dancer model because it combines:

- its own semantic schema;
- a coherent family of visual and interactive affordances;
- a set of related Dances;
- implementation code;
- activation requirements;
- semantic dependencies.

Space Navigator is:

- a Dancer;
- a member of the House Troupe;
- outside MAP Core.

Its initial executable implementation may remain bundled with the MAP Host while the broader dynamic Dancer implementation architecture is developed.

That bundling is an implementation and distribution detail.

It is not part of the semantic definition of Space Navigator as a Dancer.

---

## Toward Dynamic Dancer Extensibility

The long-term Dancer architecture is intended to support Dancers whose implementations can be introduced into a running MAP environment without recompiling or restarting MAP.

That requires future mechanisms for areas such as:

- implementation discovery;
- executable acquisition;
- provenance and integrity verification;
- compatibility;
- sandboxed execution;
- explicit capability grants;
- resource management;
- loading and unloading.

Those mechanisms are being explored separately.

The Dancer concept intentionally precedes them.

This allows MAP to establish the semantic unit of extensibility now without prematurely coupling that unit to a particular executable packaging or runtime technology.

---

## Conceptual Invariants

The Dancer model preserves the following conceptual invariants.

### A Dance is a behavior

> A Dance is a named, invocable semantic affordance.

### A Dancer is a software Agent

> A Dancer is a software Agent offering a coherent repertory of Dances.

### A Repertory is behavior, not performers

> A Repertory is the collection of Dances a Dancer or Troupe can perform.

### A Troupe groups Dancers

> Troupe membership groups Dancers without creating a new kind of Dancer.

### The House Troupe is stewarded, not typed

> House Troupe membership identifies Dancers included in the MAP-stewarded standard experience; it does not alter their Dancer semantics.

### Dancer is Core; individual Dancers are not

> MAP Core defines the Dancer abstraction. Concrete Dancers build on that abstraction without becoming part of Core.

### Adoption and activation are independent

> Adoption establishes a Dancer within an Agent's environment; activation makes its capabilities available for use.

### Identity is independent of implementation

> A Dancer remains the same semantic Agent regardless of how or whether its executable implementation is currently loaded.

### Dancers extend behavior; receptors abstract infrastructure

> Dancers interact with MAP semantics rather than depending directly on infrastructure technologies.

### MAP remains sovereign over effects

> Dancers may compute behavior and request effects; MAP remains sovereign over MAP state.

### Membrane crossing remains explicit

> A Dancer's local presence does not imply unrestricted external communication; membrane-crossing interaction remains governed by Trust Channels.

---

## Related Concepts

- **Dance** — an individual named MAP affordance.
- **Repertory** — the collection of Dances a Dancer or Troupe can perform.
- **Troupe** — a stewarded collection of Dancers.
- **House Troupe** — the MAP-stewarded Troupe included in the standard MAP experience.
- **I-Space** — the AgentSpace into which a Traveler may adopt Dancers.
- **Trust Channel** — the governed membrane-crossing relationship through which external interactions occur.
- **Receptor** — an abstraction over infrastructure used by MAP.
- **DAHN** — MAP's dynamic adaptive human-experience layer.
- **Space Navigator** — the initial concrete Dancer and a member of the House Troupe.