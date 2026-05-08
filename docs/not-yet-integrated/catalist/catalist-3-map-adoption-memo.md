# Catalist 3.0 — MAP Adoption Decision Memo

---

## Purpose

Clarify the **real architectural decision** emerging around Catalist 3.0 and MAP, including:

- architectural gravity
- deployment/runtime commitments
- product implications
- migration realities
- organizational learning effects
- and the strategic tradeoff between:
    - delivery velocity
    - architectural coherence
    - and long-term coordination ownership

---

# The Actual Architectural Divergence

The current discussion is framed as:

> “Should Catalist use Supabase or MAP as a backend?”

That framing is too narrow.

The deeper divergence is:

> **Where does coordination live?**

---

## Supabase Path

The natural Supabase architecture is:

```text
Client / React / JS
  ↔ Supabase APIs
  ↔ Postgres / Storage / Realtime
```

This tends to place:
- synchronization
- collaboration semantics
- permission mediation
- state propagation
- conflict handling
- realtime coordination

inside:
- the frontend
- JavaScript runtime
- application-layer services

---

## MAP Path

MAP assumes a fundamentally different architecture:

```text
Human Interface
  ↔ Rust IntegrationHub / MAP Core
  ↔ Spaces / TrustChannels / storage receptors
```

In MAP:
- synchronization
- provenance
- agreement enforcement
- state lifecycle
- coordination semantics

are primarily:
- runtime responsibilities
- platform responsibilities
- Space-mediated responsibilities

—not frontend responsibilities.

---

# Core Insight

> **Choosing MAP is not choosing a backend. It is choosing a different architectural center of gravity.**

MAP is:
- a coordination platform / ecosystem

Catalist today is:
- an application

On MAP, Catalist would increasingly become:
- Dancers
- Visualizers
- interaction patterns
- domain semantics

inside a larger coordination substrate.

---

# The Hidden Cost of the Supabase Path

The Supabase proposal correctly identifies substantial infrastructure advantages:

- storage
- auth
- realtime subscriptions
- CRUD APIs
- operational maturity

However, many of the difficult design problems revealed by the proposal are *not* natively solved by Supabase:

- sync semantics
- conflict handling
- collaboration behavior
- provenance
- cross-space mediation
- permission coordination
- federation
- adaptive UX coordination
- local-first consistency
- portability boundaries

Those concerns still need to be implemented at the application layer.

---

# The Illusion of Velocity

This creates a subtle risk:

> **Infrastructure acceleration can be mistaken for coordination simplification**

Supabase may dramatically accelerate:
- backend setup
- realtime transport
- auth
- persistence

while still requiring the Catalist team to design and implement much of the actual coordination architecture themselves.

That means:
- early velocity may be real
- but long-term coordination complexity may still accumulate rapidly

---

# Architectural Gravity

The deeper concern is deployment/runtime architecture.

The Supabase ecosystem strongly encourages:
- client-side coordination logic
- JS-centric sync behavior
- application-owned state propagation
- frontend-managed collaboration semantics

Even if the conceptual goals remain MAP-aligned, the implementation gravity of the Supabase ecosystem may pull the team toward solutions that become largely throwaway under MAP because the logic exists in the wrong architectural layer.

---

# The Migration Risk Is Runtime Relocation

The migration challenge is not merely:
- storage migration
- sync migration
- auth migration

It is also:
- relocating runtime responsibilities
- moving coordination semantics out of the frontend
- replacing application-centric assumptions
- and potentially discarding large amounts of JS coordination code

---

# The Mental Model Risk

The deeper risk is not just technical debt.

It is:

> **learning to think about the system in the wrong architectural frame**

Over time, the team’s:
- coordination patterns
- debugging habits
- collaboration assumptions
- runtime mental models

may increasingly crystallize around:
- client/server
- JS coordination
- application-owned synchronization

rather than:
- Space-based coordination
- agreement-mediated access
- runtime-managed state lifecycle
- agent-centric authority

This compounds migration difficulty beyond code migration alone.

---

# The Hidden Cost of the MAP Path

The MAP path also carries substantial risk.

MAP is not merely:
- a storage system
- a sync engine
- a graph database

It is a fundamentally different runtime architecture and UX paradigm.

Adopting MAP means committing to:

- Agent-centric runtime
- Holon + relationship model
- Space-based architecture
- Flow-based security
- Agreement-driven coordination
- Visualizer-driven UX composition (DAHN)

---

# What MAP Core Already Provides

MAP Core already provides substantial runtime infrastructure:

- state management
- cache/staging/commit lifecycle
- undo/redo with persistence
- recovery of staged changes
- transaction semantics
- provenance
- TypeScript SDK abstraction layer

This removes much of:
- Redux/state plumbing
- optimistic UI complexity
- manual undo systems
- sync reconciliation logic

Importantly:

> many of these are exactly the areas where the Supabase proposal begins accumulating custom application-layer complexity.

---

# The Real UX Tradeoff

> **MAP shifts UX from handcrafted interfaces → dynamically composed, descriptor-driven interfaces**

---

## What gets easier

- state management
- undo/redo
- offline handling
- interaction consistency
- provenance
- synchronization semantics

---

## What gets harder

- visualizer selection
- abstraction via DAHN
- adaptive interface generation
- reduced direct UI control
- runtime composition
- open-ended extensibility

---

# The Dependency Reframing

The real choice may not be:

> “Which path is lower risk?”

It may be:

> **Which type of dependency do we want?**

---

## Supabase Path Dependency

Dependency on:
- mature infrastructure vendor
- but application-owned coordination architecture

This gives:
- faster operational startup
- immediate realtime capability
- familiar development patterns

But also:
- increasing ownership burden for coordination semantics
- growing JS/runtime complexity
- stronger application-centric gravity

---

## MAP Path Dependency

Dependency on:
- evolving platform/runtime team
- shared architectural direction
- less mature ecosystem

This gives:
- higher near-term uncertainty
- but potentially lower long-term coordination burden
- and stronger architectural coherence

Importantly:

Catalist would not be building:
- synchronization semantics
- runtime state lifecycle
- provenance infrastructure
- coordination architecture

alone.

Those responsibilities would increasingly belong to MAP Core and the MAP development team.

---

# A Critical Question

The key practical question may now be:

> **Are the currently missing MAP capabilities actually on the critical path for Catalist 3.0?**

Because if the answer is:

> “mostly no”

then the tradeoff changes substantially.

The MAP path may no longer be:

- visionary but impractical

but instead:

- architecturally coherent but operationally immature

—which is a very different category of risk.

---

# Product Framing

It is NOT:

- Catalist-on-Supabase vs Catalist-on-MAP

It IS:

- Catalist (application, likely Supabase-shaped)
- MAP (coordination platform/ecosystem)

where Catalist concepts may appear as:
- Dancers
- Visualizers
- interaction patterns
- domain semantics

---

# Implication

> **Catalist and MAP are fundamentally different products that can coexist**

- Catalist = curated, opinionated application experience
- MAP = open-ended, person-centric coordination substrate

The Catalist team may have:
- product ownership of Catalist
- ecosystem participation within MAP
- authorship of Dancers and Visualizers

without requiring full convergence.

---

# The Real Strategic Risk

The structural risk is not:

> “choosing the wrong backend”

It is:

> **accidentally committing the team to an architectural center of gravity without recognizing it**

Specifically:
- application-centric coordination
  vs.
- runtime-centric coordination

---

# The Migration Reality

> **Convergence and client migration are separate problems**

---

## Convergence (technical)

Questions include:
- Can MAP support Catalist features?
- Can the UX be expressed effectively?
- Can MAP meet operational expectations?
- Can runtime responsibilities move successfully out of the frontend?

---

## Migration (trust)

Clients are invested in:
- current security assumptions
- governance expectations
- operational predictability
- centralized accountability

MAP introduces:
- different trust assumptions
- different authority boundaries
- different operational models

Migration therefore requires:
- trust-building
- governance clarity
- operational confidence

—not merely feature parity.

---

# The Central Question for the Dual POC Strategy

The key question is not:

> “Can we defer MAP?”

It is:

> **Which coordination problems can safely be deferred without undermining the POC goals or creating major architectural gravity?**

---

## Potentially Safe to Defer

These may be postponable without undermining near-term product validation:

- provenance
- federation
- content-addressed storage
- advanced capability systems
- CRDT semantics
- portability abstractions

---

## Likely Dangerous to Defer

These may become deeply embedded into the application architecture very early:

- synchronization semantics
- cross-space mediation
- permission coordination
- local-first consistency
- collaboration ownership model
- deployment/runtime assumptions

These concerns shape:
- where coordination logic lives
- who owns state transitions
- how authority is modeled
- how the team conceptualizes the system

If solved primarily inside:
- React
- JS runtime
- Supabase client semantics

then migration later becomes:
- runtime relocation
- architectural retraining
- and potentially large-scale discard of coordination code

—not merely backend replacement.

---

# What the Dual POC Strategy Is Actually Testing

The dual POC strategy is not simply delaying a backend decision.

It is generating evidence about:

- runtime viability
- UX viability
- operational maturity
- coordination semantics
- architectural gravity
- organizational learning direction

---

# Option 1 — Commit to MAP Now

## Description

- Catalist 3.0 built directly on MAP
- MAP becomes primary runtime architecture

---

## Advantages

- Architectural alignment from the beginning
- Avoids JS coordination-layer buildup
- Avoids runtime relocation later
- Team learns MAP-native patterns immediately
- Prevents application-centric gravity from forming
- Leverages existing MAP runtime infrastructure
- Combines efforts of Catalist + MAP teams

---

## Risks

- MAP maturity risk
- tooling gaps
- deployment complexity
- operational uncertainty
- immediate paradigm shift
- UX/runtime model may not yet be sufficiently mature

---

## What You Are Really Choosing

> Early commitment to runtime-centric coordination architecture

---

# Option 2 — Dual POC Path

## Description

Run two parallel tracks:

### POC-1 (Catalist team)
Supabase-based implementation optimized for:
- client delivery
- realtime collaboration
- operational learning
- near-term product evolution

### POC-2 (MAP team)
MAP-native exploration validating:
- runtime model
- UX model
- developer experience
- coordination semantics

---

## Advantages

- Preserves near-term delivery velocity
- Generates real evidence instead of speculation
- Allows MAP maturity to be tested incrementally
- Avoids premature commitment

---

## Risks

- Architectural gravity toward application-centric coordination
- Accumulation of JS/runtime-specific coordination code
- Increasing migration cost over time
- Diverging mental models
- Potential product divergence
- Supabase implementation gradually becoming the de facto architecture

---

# Critical Truth

> **Dual POC will eventually reach a decision point where an architectural and product direction becomes concrete**

That decision may emerge gradually through:
- implementation choices
- deployment assumptions
- team habits
- client expectations
- runtime investments
- demonstrated MAP viability

The first architecture that becomes:
- operationally real
- experientially successful
- and organizationally trusted

may become the default conceptual model of the system.

---

# This Is Not Necessarily Failure

A dual-track outcome may still be strategically strong:

- Catalist as a product/application
- MAP as a coordination platform/ecosystem

with:
- shared concepts
- shared visualizers
- shared interaction patterns
- shared economic participation

without requiring full convergence.

---

# Required Discipline for the Dual POC Path

## 1. Avoid deep Supabase coupling

Frontend should NOT:
- depend directly on Supabase schema semantics
- embed coordination semantics into React hooks
- tightly couple synchronization logic to Supabase APIs

---

## 2. Avoid building “MAP-lite”

Do NOT attempt to simulate:
- TrustChannels
- Agreements
- membranes
- runtime coordination

inside:
- React
- JS services
- Supabase policies

---

## 3. Keep runtime responsibilities isolated

Anything resembling:
- synchronization semantics
- permission mediation
- provenance handling
- cross-space coordination
- collaboration semantics

should remain behind explicit boundaries so that runtime relocation remains possible later.

---

## 4. Start POC-2 early

Do not wait for “completion.”

MAP viability must be tested incrementally and continuously.

---

# Decision Framing

This is not:

> “Which backend should we use?”

Nor simply:

> “Which product direction should we choose?”

It is:

> **Which architectural center of gravity do we want the team learning toward?**

---

# Decision Test

## 1. MAP Confidence

“If MAP were sufficiently mature operationally today, would we commit?”

- Yes → Option 1 becomes viable
- No → Dual POC likely safer

---

## 2. Coordination Ownership

Where should synchronization, provenance, permissions, and coordination ultimately live?

- Application/frontend/runtime → Supabase gravity
- Platform/runtime layer → MAP gravity

---

## 3. Dependency Preference

Which dependency is more acceptable?

- mature infrastructure vendor + application-owned coordination
- evolving platform/runtime ecosystem + shared coordination infrastructure

---

## 4. Risk Preference

Which failure is worse?

- slower near-term delivery
- or long-term architectural/runtime relocation

---

# Final Recommendation

> Default to the Dual POC path unless MAP runtime maturity is already sufficiently high for full commitment.

But do so with explicit awareness that:

- the Supabase path also creates deep architectural commitments
- the apparent velocity advantage may be partially illusory
- migration costs are likely to involve runtime relocation and mental-model transition
- and the first successful operational architecture may become the organization’s default conceptual model of the system.

---

# Bottom Line

This is not a backend decision.

It is a decision about:
- where coordination lives
- where synchronization lives
- where authority lives
- where the team learns to think the system lives

MAP and Supabase are not simply alternative storage layers.

They are different architectural centers of gravity.