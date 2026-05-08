# Velocity Comparison — What Exists vs What Still Must Be Built

The current discussion assumes:

- Supabase = fast path
- MAP = future path

The reality is more nuanced.

Both approaches already provide substantial infrastructure.

Both approaches also leave important responsibilities unresolved.

The key differences are:

- how soon critical functionality becomes operationally usable
- where unresolved complexity accumulates
- and how much “throwaway work” accumulates along the way

---

# Supabase Path

## Functionality Available Immediately

Supabase provides rapid access to:

- auth/session management
- storage
- CRUD APIs
- SQL/query infrastructure
- realtime collaboration infrastructure
- operational maturity
- hosted deployment
- browser SDK ecosystem

This creates real near-term delivery velocity, especially for:

- conventional SaaS patterns
- realtime CRUD collaboration
- centralized operational models

---

## What Still Must Be Built

However, many of the difficult coordination concerns revealed by the proposal are *not* solved natively by Supabase:

- synchronization semantics
- collaboration behavior
- conflict handling
- provenance
- cross-space mediation
- permission coordination
- local-first consistency
- federation
- adaptive UX coordination
- portability boundaries

The need to provide solutions to the above introduces significant uncertainty into development velocity along this path. Strategies to reduce this uncertainty include:

- aggressively leveraging AI assist
- retaining significant portions of the existing Catalist 2.5 collaboration model

Solutions along this path not using any MAP components or design elements and are being developed:

- in a distinctly non-MAP architecture (centralized database, app-centric architecture, 2-tier vs. de-centralized, person-centric, 3-tier)
- _inside_ the Catalist application instead of as shared infrastructure
- in Javascript/React runtime instead of Rust

If Catalist later pivots toward MAP, significant portions of this logic may become:

- architecturally stranded
- difficult to migrate
- or entirely throwaway

In effect, this path delivers near-term velocity while significantly delaying or precluding delivery of an integrated Catalist/MAP solution.

---

# MAP Path

## Functionality Already Available

MAP already provides substantial coordination/runtime infrastructure:

- graph-native data model
- Holon lifecycle management
- cache/staging/commit semantics
- undo/redo with persistence
- recovery of staged changes
- provenance-oriented architecture
- semantic transaction model
- storage abstraction
- synchronization assumptions
- Space-based architecture
- agreement-oriented security model
- TypeScript SDK abstraction layer

Importantly:

Many of these are exactly the areas where the Supabase proposal begins accumulating custom application-layer complexity.

## What Still Requires Significant Foundational Development

At the same time, MAP is still under active foundational development.

Significant work remains around:

### Runtime / Platform Maturity
- operational hardening
- deployment tooling
- runtime observability
- diagnostics
- production lifecycle tooling
- operational reliability

### DAHN / UX Composition
- descriptor-driven rendering maturity
- visualizer integration patterns
- adaptive UX composition
- runtime interaction ergonomics
- shell/runtime UX hardening

### Query / Dance Runtime
- distributed query semantics
- runtime planning/distribution
- descriptor-semantic validation alignment
- dynamic dance binding/runtime evolution
- stable cross-runtime contracts

### Multi-Space Coordination
- cross-space query semantics
- reference resolution
- trust-channel enforcement
- agreement propagation
- conflict-resolution flows
- role-based coordination/security models

### Developer Experience
- onboarding simplicity
- tooling ergonomics
- documentation maturity
- debugging workflows
- deployment confidence
- developer operational familiarity

---

# The Core Tradeoff

## Supabase Path

Advantages:

- immediate operational velocity
- mature infrastructure
- rapid product execution
- lower onboarding friction
- familiar architecture

Costs:

- increasing accumulation of application-owned coordination logic
- growing JS/runtime complexity
- architectural gravity toward client/server semantics
- potential large-scale runtime relocation later
- duplicated coordination infrastructure
- increasing technical and intellectual debt

---

## MAP Path

Advantages:

- stronger architectural coherence
- shared runtime coordination infrastructure
- reduced duplication of coordination semantics
- alignment between runtime and product semantics
- earlier MAP-native learning
- opportunity for Catalist requirements to shape MAP evolution directly

Costs:

- significant foundational work still required
- operational immaturity
- tooling gaps
- onboarding complexity
- novel architecture risk
- slower velocity in some categories
- execution uncertainty around unresolved runtime/platform capabilities

---

# The Actual Strategic Question

The real comparison is therefore not _which path is faster?_ it is _where do we want unresolved complexity to accumulate?_

The Supabase path concentrates unresolved complexity inside:

- the application layer
- frontend coordination semantics
- and JS runtime infrastructure.

The MAP path concentrates unresolved complexity inside:

- runtime/platform maturation
- shared infrastructure evolution
- and operationalization of a new architectural model.

Those are fundamentally different categories of risk, investment, and long-term consequence.
