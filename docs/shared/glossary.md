---
title: Glossary
description: Key terms and concepts for understanding the Memetic Activation Platform (MAP).
---

# 🧾 Glossary

This glossary defines key concepts and terms used throughout the MAP architecture and narrative framework. Terms are listed alphabetically. Multiple definitions are included where distinctions emerged between narrative threads.

---

## Agent

An **Agent** is any entity capable of sensing and responding to its environment. It may be biological (e.g., a person, whale, or tree), technical (e.g., a computing process), or social (e.g., a family, cooperative, or commons).

- Every Agent has a unique identity and a corresponding [I-Space](#i-space) — a private AgentSpace that houses its [LifeCode](#lifecode), [Data Grove](#data-grove), and core affordances. 
- Agents can make [offers](#offer) and accept _offers_ made by others to form [Agreements](#agreement).

Agents are expressed as [Holons](#holon) that belong to one or more [AgentSpaces](#agentspace). Every Agent belongs to the [Exosphere](#exosphere) and typically one or more additional _AgentSpaces_.

---

## AgentSpace

An **AgentSpace** is a membrane-bound social space where [Agents](#agent) interact, co-create, and participate in regenerative value flows. It is simultaneously:

- A [HolonSpace](#holonspace) — stewarding both Agents and [Holons](#holon)
- A **container** for knowledge, relationships, and shared governance
- A venue for [Offers](#offer), [Agreements](#agreement), [Promises](#promise), and visualization

Every AgentSpace has its own [LifeCode](#lifecode), and every interaction between Agents happens **within** an AgentSpace.

⚠️ *Not every AgentSpace is itself an Agent (i.e., not all are [Social Organisms](#social-organism)), but some  AgentSpaces, once sufficiently coherent and governed, may themselves become Agents — emergent wholes acting at a higher level of the holarchy.*

---

## Agreement

An **Agreement** is created from an [Offer](#offer) when agents have accepted all of the mandatory roles of the Offer. An Agreement may instantiate its own [Agreement-Based AgentSpace](#agreement-based-agentspace) which becomes the interaction venue for activities governed by that agreement.

---

## Agreement-Based AgentSpace

An **Agreement-Based AgentSpace** is a bounded interaction context that emerges when an [Offer](#offer) is accepted and an [Agreement](#agreement) is formed.

It includes:
- All participating [Agents](#agent)
- A [LifeCode](#lifecode) derived from the shared promises and intent of the Agreement
- A scoped [Data Grove](#data-grove) of relevant Holons and references
- The governance and coordination logic encoded in the Agreement, including optional roles for verification, mediation, or escalation

While agreements may **expire**, be **revoked**, or become **inactive**, the AgentSpace itself — like all entities in the MAP — is **immutable and persistent**. Its history, structure, and prior interactions remain verifiable and accessible, preserving both accountability and lineage.

> An Agreement-Based AgentSpace is the **sovereign membrane** where promises take form, interactions unfold, and trust-based coordination becomes possible — with a cryptographically assured memory.


---
## Choreographer

The **Choreographer** is the MAP’s native coordination engine. It manages the invocation and sequencing of modular dances across agents, spaces, and roles using **declarative [Dance Flows](glossary.md#dance-flow)**. 

Each dance performs a single task and emits a completion signal. The Choreographer listens for these signals and, based on the active flow specification and local context, invokes the next appropriate step. By keeping sequencing logic outside of individual dances, MAP enables complex behaviors to be composed from simple, intelligible parts.


---
## Commoning

Commoning is the ongoing social process through which people collaboratively create, steward, and sustain shared resources (i.e., [Vital Capitals](#vital-capital)) and relationships. At its core, commoning is a relational, participatory, and adaptive practice that reclaims shared power in managing the conditions of life. It is not just a structure, but a way of being and doing together.

Commoning emerges outside of — and often in resistance to — market and state logics, cultivating trust, reciprocity, and long-term ecological and social flourishing. The lived practice of mutual care, collective governance, and cultural co-creation is what enables a [commons](#commons) to thrive.

“Commoning is a verb. It’s about the social practices and cultural traditions that people devise to manage shared resources in fair, inclusive, and sustainable ways.” 
— David Bollier, “Think Like a Commoner” (2014)

“There is no commons without commoning.”
— Peter Linebaugh, “The Magna Carta Manifesto” (2008)

---

## Commons

A **Commons** is a *social system* for the long-term stewardship of [Vital Capital](#vital-capital) that preserves shared values and community identity. A self-organized system by which communities manage *vital capital* (both depletable and replenishable) with minimal or no reliance on the Market or State. In the MAP, a *commons* is represented by an [Agent Space](#agentspace) whose  [LifeCode](#lifecode) conveys its community values, [join membrane](#join-membrane), and governance model.

---

## DAHN (Dynamic Adaptive Holon Navigator) {#dahn}

A personalized, dynamic interface layer for exploring the MAP holon graph. DAHN empowers each agent to shape their own experience — not just by choosing settings, but by composing the very way information is seen, explored, and interacted with.

Rather than each app imposing its own interface, DAHN provides a **coherent visual and interaction layer across all Mapps**. This coherence is achieved through dynamic selection of visualizers — modular components contributed by HX designers to the federated [Visualizer Commons](#visualizer-commons).

DAHN embodies the MAP design philosophy: **putting agents at the center of their digital experience**, enabling expressive, adaptable, and trustable interfaces that evolve with collective and individual needs.

---

## Dance

A **Dance** is a named, invocable action that a [Holon](#holon) can perform or participate in — such as querying data, initiating a service, accepting an offer, or responding to a relationship.

In MAP, **dances** represent **affordances** — the ways a Holon can be interacted with — but the term _affordance_ felt overly technical and lacked poetic resonance.

So we coined the term **Dance**.

Why _Dance_?

- Because dances are relational — they involve interaction, timing, rhythm, consent.
- Because they convey **graceful interdependence**, not mechanical execution.
- Because in MAP, even technical operations are wrapped in patterns of trust, meaning, and flow.

Dances are defined through the [MAP Uniform API](#uniform-api), where each `DanceRequest` expresses:
- **Who is dancing** (the Holon)
- **What dance is being performed**
- **With what input parameters**
- **Under what conditions**

And the `DanceResponse` returns:
- The result of the dance
- A set of next possible dances based on the current state of the system

> A **Dance** is not just a function call — it's a structured act of agency within a living graph of relationship and meaning.

---

### Dance Flow

A **Dance Flow** is a named, context-aware sequence of individual dances that collectively coordinate a process across agents, promises, or Agent Spaces.

Each *dance* within the flow performs a discrete task or role and emits a signal upon completion. The **MAP Choreographer** responds to these signals by invoking the next appropriate dance in the flow, guided by shared agreements and contextual conditions.

**Key Characteristics**:
- **Composable**: Built from modular, reusable dances.
- **Declarative**: Specifies *what should unfold*, not *how each dance works* internally.
- **Membrane-aware**: Executes within or across Agent Spaces while respecting boundaries and permissions.
- **Promise-aligned**: Flows often reflect and reinforce explicit promises among participants.

**Purpose**:  
Dance Flows enable complex behaviors to emerge through the orchestration of simple, intelligible steps — making collaborative processes legible, adaptable, and agency-respecting.

**Related Concepts**:  
→ *Dance*, *Choreographer*, *Promise Weave*, *Agent Space*

---

## Dance Interface Protocol

The **Dance Interface Protocol** is the universal invocation protocol in the MAP. It replaces traditional REST or RPC calls with a more expressive, memetic, and composable request model.

Every [Holon](#holon) exposes available [Dances](#dance) depending on its current state and context.

---

## DanceRequest

A **DanceRequest** is a Holon-encoded invocation of a [Dance](#dance). It tells a Holon what is being requested — and under what terms.

Each `DanceRequest` contains:
- The **ID of the Holon** being danced with
- The **name of the Dance** being invoked
- A **RequestBody** — including input parameters, context, and initiating agent identity
- (Optionally) an associated [Agreement](#agreement) that governs the terms of the interaction

Like all things in the MAP, the DanceRequest is itself a [Holon](#holon) — with its own type descriptor, provenance, access policy, and potential for visual representation.

DanceRequests can be created by:
- Human users interacting through [DAHN](#dahn-dynamic-adaptive-holon-navigator) 
- Other Holons (e.g., service Holons triggering dances)
- External systems interfacing through the MAP Uniform API

> A `DanceRequest` is a **memetically and permissionally aware act of intent** — a moment of coordinated agency within a shared graph.

---

## DanceResponse

A **DanceResponse** is the result of performing a [Dance](#dance). It includes not only the outcome of the request but also the forward affordances — what the Holon now makes possible.

Each `DanceResponse` includes:
- A **ResponseBody** — containing results, messages, or new Holons
- A list of **next available Dances** — HATEOAS-style descriptors of follow-up actions
- Provenance metadata and optional diagnostics
- Links to updated state, derived Agreements, or resulting relationships

Like the `DanceRequest`, the `DanceResponse` is a fully self-describing Holon and can be visualized, shared, or referenced by other components of the MAP.

> A `DanceResponse` is not just a return value — it’s the **moment-by-moment emergence of possibility** in a living graph of consent and flow.

---

## Data Grove

A **Data Grove** is the sovereign, Holochain-based data storage area. Each [AgentSpace](#agentspace) has its own private Data Grove.  All of the [mapps](#mapps) that are imported into an Agent Space store their information in the Data Grove of that Space.

---

## Echo

An **Echo** is a signed affirmation of a [Promise](#promise) made by another [Agent](#agent), issued by an agent who chooses to align with that promise.

Echoes serve as memetic endorsements—reinforcing, repeating, and extending the trustworthiness of a promise in a given [AgentSpace](#agentspace) or across spaces.

An Echo is:

- A **verbatim reference** to an existing Promise, not a reinterpretation
- A **social trust gesture**—binding the echoing agent’s reputation to the original claim
- A **signal of observability**—often grounded in direct experience, shared context, or role-based verification
- A building block of **memetic trust networks**, used to evaluate promises, inform [Agreements](#agreement), and govern access or delegation

Echoes may carry optional metadata such as **echo weight**, reasoning, or contextual scope (e.g., “within this space only”).

> ✳️ Echoes are foundational to MAP’s distributed trust model—allowing agents to construct verifiable, socially-scaffolded identity and reputation without centralized authorities.

---

## Echo Weight

An **Echo Weight** is an optional indicator attached to an [Echo](#echo), expressing the echoing [Agent](#agent)’s degree of confidence, verification, or proximity to the original [Promise](#promise).

Echo Weights enable more nuanced interpretation of social signals by:

- Differentiating firsthand from secondhand endorsements
- Informing access decisions, [Agreement](#agreement) thresholds, and trust scores
- Supporting evaluative logic in [AgentSpaces](#agentspace) and across social holarchies

Weights may be numeric (e.g., 0.9), categorical (e.g., “strong,” “light”), or policy-defined by a [GroupAgent](#group-agent).

> ✳️ While optional, Echo Weights help MAP spaces distinguish between weak support and strong verification—without requiring rigid central scoring systems.


---

---

## Exosphere

The **Exosphere** is the outermost, most inclusive [AgentSpace](#agentspace) in the MAP. It includes all [Agents](#agent) by default and serves as the **lowest-threshold interaction venue** across the entire platform.

The Exosphere is:

- **Non-governed** (aside from platform-level rules)
- **High-reach, low-trust**
- The place where initial [Offers](#offer) may be surfaced to broad audiences

It is not a commons or [Social Organism](#social-organism) — it is a **shared membrane of visibility**.

---

## Governance Scaffold
<!-- summary:start -->
A **Governance Scaffold** is a modular structure of roles, rules, and processes that guides how coordination and decision-making unfold within an [AgentSpace](#agentspace).
<!-- summary:end -->

Rather than imposing a fixed governance model, a governance scaffold provides **lightweight, composable affordances** that can evolve alongside the needs and context of the space. These scaffolds are often **memetically sourced** from the [Global Meme Pool](#meme-pool), where patterns like sociocracy, holacracy, liquid democracy, or bespoke cultural traditions can be adapted and instantiated.

Governance scaffolds define:
- **Who has voice and agency**
- **How decisions are made and validated**
- **What roles exist and how they are assigned or rotated**
- **How conflicts are mediated or escalated**

They can be:
- **Hard-coded** into [Agreements](#agreement)
- **Expressed** as [Memeplexes](#meme) in the Meme Pool
- **Referenced dynamically** during [Dance Flows](#dance-flow)

> 🧩 Governance scaffolds are to governance what protocols are to software: flexible, interoperable building blocks that support resilient, adaptive coordination.

**See also:** [AgentSpace](#agentspace), [LifeCode](#lifecode), [Agreement](#agreement), [Meme Pool](#meme-pool)

---

## Holon

A **Holon** is the foundational unit of structure, meaning, and interaction in the MAP.

Every object in the MAP — whether it’s a piece of content, an [Agent](#agent), a relationship, a service, or a visual element — is encoded as a self-describing, active Holon or HolonRelationship.

---

### ✧ Self-Describing

A Holon contains within itself everything needed to interpret and interact with it. When you encounter a Holon “in the wild,” you can ask:

- **What properties do you have?**  
  What are your current values for those properties?

- **What types of relationships do you participate in?**  
  To what other Holons are you related via those relationships?

- **Through what visualizations can I view and interact with you?**  
  Holons reference one or more [Visualizers](#visualizer) from the commons, allowing fully customizable rendering and interaction — from list views to immersive spatial experiences.

- **What types of data access are permitted?**  
  Holons carry their own access policies, provenance signatures, and licensing terms — enabling granular, trustable permissioning.

---

### ✧ Active

Holons aren’t just data — being active means holons can do stuff... they offer _**affordances**_.

Every Holon can declare the [Dances](#dance) it is capable of performing — actions that can be invoked via the MAP Uniform API. These may include:

- Responding to queries
- Invoking relationships
- Triggering services
- Participating in negotiations, offers, or agreements

In this way, Holons are not passive records, but sovereign, interactive knowledge actors that make up the living substrate of the MAP.

---

> A Holon is not just a piece of data —  
> it is a meaningful, permissioned, expressive agent of action in a graph of relationships.  
> It sees, responds, and evolves.

---

## HolonSpace

A **HolonSpace** is the foundational data container in the MAP, equivalent to an [AgentSpace](#agentspace). While the term highlights its function as a steward of [Holons](#holon), in MAP narratives, the two terms are generally treated as synonymous.

---

## I-Space

An **I-Space** is an [AgentSpace](#agentspace) viewed from the **interior** perspective — focusing on internal structure, properties, intentions, and affordances of an [Agent](#agent).

Every Agent has an I-Space. For persons, this is often referred to as a **Personal I-Space**, but not all I-Spaces are personal.

See also: [We-Space](#we-space)

---

## Join Membrane

The set of rules defined by an [AgentSpace's](#agentspace) [Life Code](#lifecode) that govern adding new members of the Agent Space.

---

## LifeCode
<!-- summary:start -->
A **LifeCode** (also known as a [Memetic Signature](#memetic-signature)) is the values-and-identity encoding of an [Agent](#agent), [AgentSpace](#agentspace), [Offer](#offer) or [Agreement](#agreement). It defines:

- Aspirational purpose
- Memetic values and ethics
- Governance expectations
- Membership criteria
- Expressed [Promises](#promise)
<!-- summary:end -->

The LifeCode is the symbolic "membrane" of an AgentSpace and plays a foundational role in trust-based interaction.

---

## Meme
<!-- summary:start -->
A **Meme** is a pattern, story, value, or shared practice that carries meaning and can be passed from one person or group to another.
<!-- summary:end -->

In the MAP, a meme could be a community ritual, a traditional teaching, a way of solving problems, a decision-making method, a symbol, or even a sacred story. Some memes are old and passed down through generations. Others are new, shared in conversation, taught in workshops, or built into tools and agreements.

What matters is not just where a meme comes from — but that it helps people **live together with intention**, **take action**, or **share understanding**.

Memes travel in many ways. Some are copied, some are taught, some are woven into daily life. In MAP, we honor all of these. Whether a meme is passed in a ceremony, a drawing, a document, or a song — it becomes part of our **living culture** when people put it into use.

Memes are gathered into [Meme Pools](#meme-pool), where they can be shared, adapted, and stewarded with care — so that wisdom from one place can grow in another, without losing its roots.

**See also:** [Meme Pool](#meme-pool), [Vital Capital](#vital-capital), [LifeCode](#lifecode)

## Meme (technical)
<!-- summary:start -->
A **Meme** is a structured unit of cultural meaning that can be defined, expressed, enacted, and evolved by [Agents](#agent).

In the MAP, a meme may take many forms — including values, principles, protocols, schemas, profiles, practices, rituals, governance models, economic models, or other cultural structures that guide interaction and meaning-making. Every meme is modular, stewardable, and context-aware.

> In the MAP, memes are not just viral ideas — they are the living infrastructure of cultural evolution.
<!-- summary:end -->

MAP extends Richard Dawkins’ original definition — which emphasized replication through imitation — to include **agentic enactment**, **contextual re-use**, and **memetic evolution**. Memes may spread via imitation (per Dawkins), but also through instruction, documentation, or embedded use in systems and agreements. What defines a meme is not just *how* it spreads, but that it **encodes actionable meaning** and can be **activated across diverse contexts**.

Memes are **replicable** and **selectable**: they persist through evolutionary dynamics, where their relevance and effectiveness are tested in lived experience. In this way, MAP supports not just cultural transmission, but the **iterative refinement and ecological adaptation** of its memetic commons.

> **Epistemic rigor** — such as practices rooted in the scientific method — can strengthen the **fidelity and resilience** of a meme by making it easier to reproduce, test, and refine across contexts.  
> However, epistemic rigor is **neither the sole pathway to replicability nor a universal standard**: many memes in MAP draw from spiritual traditions, embodied practices, or lived experience that offer their own forms of coherence, relevance, and transmission.

Memes can be classified by:

- **Type** (e.g. atomic meme, schema, protocol, visualizer)
- **Category** (e.g. governance, economics, learning, identity)
- **Functional structure** (e.g. memeplex, memefamily)

Every Meme in MAP is a form of [Vital Capital](#vital-capital), and is stewarded within one or more [Meme Pools](#meme-pool).

**See also:** [Meme Pool](#meme-pool), [Vital Capital](#vital-capital), [LifeCode](#lifecode)

---

## Meme Pool

A Meme Pool is a collection of memes together with the agents and governance processes that steward them. In other words, a Meme Pool is a [Commons](#commons).

---

## Memetic Signature

Synonym for [LifeCode](#lifecode). Refers to the expressive encoding of an Agent’s identity, values, and memetic alignment.

---

## Observability

**Observability** describes the degree to which a [Promise](#promise) can be independently verified by other [Agents](#agent) within a given [AgentSpace](#agentspace).

Every Promise has an implicit or explicit observability profile, which may be:

- **Direct** — fulfillment is visible to others (e.g., a submitted file, a public action)
- **Indirect** — fulfillment is verifiable through roles, logs, or trusted intermediaries
- **Unobservable** — fulfillment is private or unverifiable (e.g., internal state, intentions)

Spaces may define [Observability Profiles](#observability-profiles) that specify the kinds of promises they accept, echo, or require in [Agreements](#agreement).

> ✳️ Observability governs the **memetic legibility** of a promise—what others can trust, echo, or build upon.

---

## Offer
<!-- summary:start -->
An **Offer** is a proposed bundle of [Promises](#promise), expressing both:

- What the offering [Agent](#agent) is willing to do or provide
- What reciprocal Promises it expects in return

Offers are shared into specific [AgentSpaces](#agentspace) (e.g., the [Exosphere](#exosphere) or a [Social Organism](#social-organism)) and may result in [Agreements](#agreement).
<!-- summary:end -->

---

## Offer Type
<!-- summary:start -->
An **Offer Type** is a reusable template or pattern that defines the structure, roles, conditions, and expectations for a class of [Offers](#offer) in the MAP.
<!-- summary:end -->

Offer Types allow communities and [Agents](#agent) to create Offers with shared semantics and validated structure. Each Offer Type is a [Meme](#meme) — discoverable, remixable, and stewarded in the [Global Meme Pool](#meme-pool).

Key properties of an Offer Type may include:
- A named **purpose** or intent (e.g., “Timebank Exchange”, “Microgrant Application”, “Commons Stewardship Invitation”)
- The required and optional **roles** (e.g., Initiator, Contributor, Verifier)
- **Preconditions** and **fulfillment criteria**
- Common **reciprocity patterns** (e.g., “offer of service in exchange for learning”)

By standardizing structure while remaining adaptable, Offer Types reduce friction and ambiguity in peer coordination, and enable the creation of [Agreements](#agreement) that are intelligible across diverse contexts.

> 📦 An Offer Type is a **memetic design pattern** for regenerative coordination — shaping how value is proposed, negotiated, and enacted.

**See also:** [Offer](#offer), [Agreement](#agreement), [Meme](#meme), [Meme Pool](#meme-pool)

## Promise

A **Promise** is a voluntary, sovereign commitment made by one [Agent](#agent). It is the atomic unit of value coordination within MAP.

Promises may be formal (e.g., I promise to transfer 10 units of water in exchange for 5 units of labor) or informal (e.g., I promise to show up with care and attention).

All [Agreements](#agreement) are built from bundles of Promises.

---

## Service

Services support the flow and transformation of vital capitals to/from other agents for mutual benefit. Services are the focus of [Offers](#offer), [Agreements](#agreement), and [Service Invocations](#service-invocation).

---

## Service Invocation

A request to an offering agent to perform a requested service within the context of an active agreement.

---

## Social Organism

A **Social Organism** is an [AgentSpace](#agentspace) that has developed enough internal coherence, governance capacity, and memetic identity to act as an [Agent](#agent) in its own right—a [Holon](#holon) one level up.

Unlike the default [Exosphere](#exosphere), which includes all agents by default and lacks any collective governance, a Social Organism is formed intentionally. It may emerge from one or more [Agreement-Based AgentSpaces](#agreement-based-agentspace) and evolve into an agentic identity through extensions to its LifeCode.

A key property of Social Organisms—described by Ken Wilber as **Social Holons**[^1]—is that **membership is non-exclusive**. That is, an individual agent can participate in multiple Social Organisms at once. This contrasts with **Biological Holons** (e.g., cells or mitochondria), whose parts typically belong to a single organism. Social Holons reflect the fluid, overlapping, and context-dependent nature of social identity and affiliation.

Social Organisms are not merely large groups—they are **living holons**: capable of acting, adapting, evolving, and participating in higher-order Social Organisms themselves. A canonical example is a **corporation**—a persistent, governance-equipped AgentSpace that can form agreements and delegate authority to sub-agents.

Other examples might include co-ops, intentional communities, DAOs, or bioregional networks.


**See also:** [AgentSpace](#agentspace), [Exosphere](#exosphere), [LifeCode](#lifecode), [Agreement](#agreement), [Agent](#agent), [Holon](#holon)

[^1]: Wilber, Ken. *Sex, Ecology, Spirituality: The Spirit of Evolution.* Shambhala Publications, 1995.

---

## Stewardship

In the MAP, **stewardship** replaces "ownership" to describe the relationship between an [AgentSpace](#agentspace) and the [Holons](#holon) it is responsible for. Each Holon is stewarded by exactly one AgentSpace, though it may be referenced in many.

Stewardship emphasizes care, consent, and accountability.

---

## Uniform API

The **Uniform API** is the singular interface through which all interactions with the MAP take place. It is based on the metaphor of the [Dance](#dance), framing every invocation — from data queries to service calls — as a shared, consensual interaction.

At its core is the `dance()` function, which accepts a `DanceRequest` and returns a `DanceResponse`.

- The **DanceRequest** specifies:
  - The Holon (or relationship) initiating the Dance
  - Parameters for the action (e.g., queries, inputs, filters)
  - Optionally, an [OpenCypher](https://opencypher.org/) query — enabling expressive graph traversal and transformation

- The **DanceResponse** returns:
  - Results from the invocation (e.g., data, confirmation, computation)
  - Updated state where appropriate
  - Additional `DanceRequest` options (HATEOAS-style), revealing the next set of affordances available in the current state

Because the MAP is **knowledge-graph native**, all interactions — including service calls, interface rendering, and value flows — are expressible as Dances across a dynamic graph of [Holons](#holon).

> The Uniform API means **every Holon interaction is symmetric, discoverable, and composable** — turning the MAP into a danceable language of consent, action, and agency.

---

## Vital Capital

A core MAP holon type representing the diverse forms of value that can flow between Agents — including knowledge, care, trust, materials, attention, and more. Vital Capital is *what flows* as a result of service invocations and fulfilled Promises. While not inherently scarce or commodified, each Vital Capital holon is definable, describable, and context-aware. When under the stewardship of a particular Agent, it may be treated as an **Asset**. The concept draws from multiple sources, including **Context-Based Sustainability (McElroy)**, the **Metacurrency Project** (which defines wealth as *"the capacity to meet the needs of a living system"*), and the **8 Forms of Capital** in permaculture theory.

The MAP concept of **Vital Capital** refers to the many forms of value — not just financial — that flow through MAP [Agreements](#agreement). These include:

draws heavily on the work around Context-Based Sustainability (see citation below) 

| **Capital Type**         | **Description**                                                                 |
|--------------------------|---------------------------------------------------------------------------------|
| **Natural Capital**      | Ecosystem services, land, water, air, biodiversity                              |
| **Human Capital**        | Skills, labor, knowledge, health, attention                                     |
| **Social Capital**       | Trust, reputation, relationships, group cohesion                                |
| **Cultural Capital**     | Stories, rituals, symbols, traditions, identity                                 |
| **Built Capital**        | Tools, infrastructure, digital systems, physical assets                         |
| **Financial Capital**    | Currency, tokens, credit, investments                                           |
| **Experiential Capital** | Aesthetic, emotional, and lived experiences                                     |
| **Memetic Capital**      | Values, beliefs, narratives, memetic signatures                                 |
| **Temporal Capital**     | Time, availability, scheduling of attention or actions                          |
| **Spiritual Capital**    | Purpose, presence, connection to meaning (optional but supported dimension)     |

- Social capital
- Ecological contributions
- Attention, care, and creativity
- Knowledge and memetic resources

Vital capital flows are explicitly tracked via [Promises](#promise) and [Agreements](#agreement).
>For more information: see 
> **McElroy, M. W. (2008).** *Social Footprints: Measuring the Social Sustainability Performance of Organizations.*  
> Middlebury: Center for Sustainable Innovation.  
> [https://www.sustainableinnovation.org](https://www.sustainableinnovation.org)  
> [ResearchGate PDF](https://www.researchgate.net/publication/239781019_Social_Footprints_Measuring_the_Social_Sustainability_Performance_of_Organizations)

---

## Visualizer

A **Visualizer** is a Holon that describes how another Holon should be rendered and interacted with — in 2D, 3D, text, graph, gallery, immersive environment, or any other format.

Visualizers are contributed to the [Visualizer Commons](#visualizer-commons) and selected at runtime by [DAHN](#dahn-dynamic-adaptive-holon-navigator) based on:
- The type of Holon
- The preferences of the Agent viewing it
- The popularity and contextual fit of available visualizers

Every Holon can reference one or more Visualizers, allowing radically different renderings for different contexts — from dashboards to immersive journeys.

> A Visualizer is not just a UI component — it is a **semantic lens**, a votable style, and a participatory aesthetic contribution to the shared experience of the MAP.
> 
---

## Visualizer Commons

A federated network of stewarded sets of [Visualizers](#visualizer). [DAHN](#dahn-dynamic-adaptive-holon-navigator) dynamically selects and configures visualizers from the _Visualizer Commons_ to present and enable interaction with the MAP' self-describing, active [Holons](#holon)

---

## We-Space

A **We-Space** is an [AgentSpace](#agentspace) viewed from the **exterior** perspective — how it participates within larger structures, how it exposes interfaces and affordances, and how it relates to other spaces.

A [Social Organism](#social-organism) is always a We-Space, but not all We-Spaces are yet Social Organisms.

---