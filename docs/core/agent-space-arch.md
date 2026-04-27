# MAP Architectural Consolidation — AgentSpace, TrustChannels, Routing, and Protocol Extensibility

>One DNA. One Zome. One EntryType. One LinkType.
The entire MAP runtime emerges from this singular, self-similar pattern — replicated fractally at every scale of agency.

A series of related insights have resulted in the MAP architecture converging into a unified and elegant runtime model. Many of the early “fuzzy edges” have been clarified, revealing a single coherent structure that expresses the holonic principle at every level of the system.

At its core, MAP now recognizes **one coordinator zome — AgentSpace**.  The same AgentSpace codebase governs every context of interaction: personal I-Spaces, collective We-Spaces, and any higher-order federations built from them.  Each AgentSpace is simultaneously a *whole* (coordinating its own members and internal Dances) and a *part* (participating as an agent within larger collectives).  This mirrors the biological and social logic that inspired the platform: every living entity is both autonomous and relational.

The sections that follow unpack how this consolidation simplifies the entire MAP runtime — beginning with the shift to a single DNA, and continuing through the unification of I-Space and We-Space roles, the definition of TrustChannels and RoutingHolons, and the design of MAP’s extensible communication protocols.

---

## 1. One DNA: Decoupling Social Context from Application Code

Perhaps the most fundamental architectural distinction between **Holochain** and **MAP** lies in how each defines an *application*.  
A Holochain application, or **hApp**, always couples two things:

1. a **DNA** — the code container that defines what data structures and zomes exist, and
2. a **DHT** — the membership container that holds the agents participating in that shared membrane.

Each hApp therefore bundles *who participates* together with *what code runs*.  
That coupling makes every hApp an **app-specific shard** of the social graph.  
If four housemates want to use ten Holochain apps together, they must join ten DHTs with identical membership, updating each one whenever someone joins or leaves.  
This intertwining of social and functional boundaries leaves a trace of app-centricity in an otherwise agent-centric framework.

MAP dissolves that coupling entirely. In MAP, a **mApp** (*memetic application*) is *not* a new DNA and does *not* create its own DHT. Instead, it is a *declarative extension* of the shared runtime — a bundle of **schemas, Dances, and visualizers** that introduces new affordances within existing Spaces.

The consolidated MAP runtime now operates from **a single DNA — AgentSpace** — whose sole purpose is to maintain the *social context* of each collective: its members, roles, LifeCode, and Agreements. Every social organism in MAP, from an individual to a federation of cooperatives, runs this same AgentSpace DNA.

All other functionality — Promises, Trust Channels, Vital Capital Flows, Governance Scaffolds, and more — is governed by **digitally signed Agreements** that define how Dances are invoked *within* and *between* AgentSpaces. Each AgentSpace executes its own Dances locally, while TrustChannels mediate secure exchanges of DanceRequests and DanceResponses across membranes.

Executable logic becomes available through **Dynamic Dance Dispatch**. This mechanism allows any type within the ontology to declare the Dances it *affords* and bind them to runtime implementations, so new behaviors can be dynamically loaded, verified, and executed — all without embedding code in the DNA itself. For more details, see the [Dances Design Spec](dances/dances-design-spec.md).

This yields a *purely agent-centric architecture*:

- **The DHT corresponds to who is in relationship.**
- **mApps define how those agents can interact.**  
  Membership changes once — at the membrane — and immediately applies across all applications.

**Benefits of the one-DNA model:**

- 🔹 Dramatically reduced deployment and onboarding complexity
- 🔹 Unified governance and membership management
- 🔹 Lower network and storage overhead
- 🔹 Simplified developer workflow (no DHT proliferation)
- 🔹 Clear separation between *social topology* and *functional affordances*
- 🔹 Extensibility through *mApps* and **Dynamic Dance Dispatch** — introducing new schemas and executable behaviors without modifying the base DNA

---

## 2. One Zome: Unification of I-Space and We-Space

While Section 1 clarified that MAP runs on a single DNA pattern, this section shows how that DNA is expressed through a single zome: **AgentSpace**.  AgentSpace unifies the code underlying I-Space and We-Space into one self-similar runtime component capable of playing both roles.

Every AgentSpace is simultaneously:

- A **whole**, containing and coordinating its internal agents (inward-facing behavior).
- A **part**, participating as a member within larger collectives (outward-facing behavior).

This dual role embodies the holonic principle: *every holon is both a whole and a part*.  
There are no separate codebases for I-Space vs. We-Space; configuration — via LifeCode, Agreements, and memberships — determines the current orientation and responsibilities.

**Key outcomes of this unification:**

- 🧩 One coordinator zome for all social contexts (AgentSpace).
- 🛡️ Each DHT now represents a distinct social organism — from an individual to a federation.
- 📜 Differentiation occurs through LifeCodes and Agreements, not through divergent codebases.
- ♻️ The same logic applies recursively at every scale of agency.

---

## 2. Responsibilities of an AgentSpace

An AgentSpace holon:

1. **Manages Membership** – defines its join membrane, validates new sub-agents, and governs internal roles.
2. **Maintains Agreements** – stores and enforces both internal (LifeCode) and external (Trust-based) Agreements.
3. **Coordinates Dances** – orchestrates local Dances among internal agents and bridges to external Spaces.
4. **Hosts TrustChannels** – instantiates inbound and outbound TrustChannel instances at its membrane boundaries.
5. **Handles Routing** – collaborates with RoutingHolons to resolve addresses, select transports, and ensure reliable delivery.
6. **Enforces LifeCode** – applies local norms and validation rules to all actions within its membrane.
7. **Provides Sovereign Persistence** – persists its own Holons and governs external references through secure fetches.
8. **Acts as Participant** – when part of a larger collective, joins We-Spaces via the same TrustChannel interface it uses internally.

---

## 3. TrustChannel Architecture

- **Single codebase** for TrustChannels; every instance represents a membrane boundary.
- **Instances** are created wherever two AgentSpaces interact.
    - *Outbound instance* on the sending side wraps, signs, and transmits capsules.
    - *Inbound instance* on the receiving side verifies and unwraps capsules.
- A single Dance involves two cooperating instances — one outbound, one inbound — each governed by its side’s LifeCode or Agreement.
- The TrustChannel code itself is a lightweight **capsule assembler/disassembler**; it does not hard-code envelope logic.

### 3.1 Envelope and Capsule Model

- A **Capsule** is an ordered stack of **Envelopes** wrapped around a **payload**.
- Each **EnvelopeType** is a HolonType descriptor defining:
    - its attributes (what’s written “on the outside”),
    - its order in the stack,
    - and the Dances that perform `wrap()` and `unwrap()`.
- Capsule composition for any interaction is determined dynamically by:
    - the **Agreement** (for cross-Space interactions), or
    - the **LifeCode** (for intra-Space interactions).

### 3.2 Envelope Responsibilities

Typical envelope layers:

1. **SessionEnvelope** – context/state exchange (optional, LifeCode-governed).
2. **SecurityEnvelope** – Agreement reference, Persona signature, nonces, proofs.
3. **TransportEnvelope** – framing and routing hints for the selected transport.
4. **Payload** – the opaque DanceRequest or DanceResponse.

Each layer is self-describing via its HolonType and can evolve independently.

---

## 4. RoutingHolon

- A reusable holon providing transport Dances for discovery, path selection, retries, and delivery.
- Operates identically whether:
    - routing inside an AgentSpace (originator → bridge sub-agent), or
    - routing between AgentSpaces (bridge → recipient Persona).
- Maintains registries of active agents, bridge health, and performance metrics.
- Provides retry, back-off, and K-parallel sending for resilience.
- Exposes a consistent API to TrustChannels:
    - `resolve_candidates(address) → [AgentRoute]`
    - `select(candidates, policy) → AgentRoute`
    - `send(route, Capsule) → Result`

---

## 5. Pluggable Transport Protocols

- Transport is **pluggable**; Holochain networking is one possible carrier, not the only one.
- Alternate transports (HTTP, JLINC, mesh, peer-to-peer bus, etc.) can be bound via different RoutingHolon implementations.
- Agreements specify which transport protocols are valid for a given TrustChannel.
- Each protocol corresponds to a **set of envelopes** defining its framing and security layers.
- Cross-Space communication with non-Holochain services is supported as long as both sides honor the same **protocol definition** (the envelope schema).

---

## 6. Protocol vs. API

- **API**: language-specific surface used by local code (e.g., RoutingHolon Dances).  
  It encapsulates how capsules are constructed or interpreted within a particular runtime.
- **Protocol**: language-independent definition of the envelope stack and payload semantics.  
  Any implementation in any environment can participate if it can construct and parse the same capsule structure.
- The combination of:
    - the *API layer* (RoutingHolon + TrustChannel code) and
    - the *protocol definition* (Agreement-defined envelope schema)
      enables MAP to interoperate across different runtimes and evolve its protocols without changing core code.

---

## 7. Extensibility Through Agreements

- Agreements are the **living source of protocol definition**:
    - They specify which EnvelopeTypes apply and in what order.
    - They dictate validation rules, privacy levels, and transport preferences.
    - They can introduce new capsule types without touching core zome logic.
- LifeCodes serve the same role internally within a Space.
- This design allows MAP’s communication layer to evolve purely through new HolonType definitions and Agreements, keeping the base AgentSpace and TrustChannel code stable.

---

## 8. Summary: The Unified Pattern

| Layer | Responsibility | Extensible By |
|--------|----------------|---------------|
| **AgentSpace** | Governs members, manages Agreements, instantiates TrustChannels | LifeCode |
| **TrustChannel** | Wraps/unwraps capsules, enforces Agreement/LifeCode rules | EnvelopeType holons |
| **RoutingHolon** | Finds paths, chooses transport, ensures delivery | Transport adapter holons |
| **Transport Protocol** | Defines envelope stack and serialization | Agreement |
| **Capsule / Envelope** | Self-describing data structure governing how value flows | HolonType descriptors |

Together they form a **fractal, self-describing communication fabric** where:
- Every AgentSpace is both a whole and a part.
- Every membrane crossing is mediated by a TrustChannel.
- Every Capsule structure is governed by the living Agreements of the participating Spaces.
- New social or technical protocols can be introduced by publishing new EnvelopeType holons—no hard-coded changes required.

**This is the extensible core of the Memetic Activation Platform’s holonic communication model.**