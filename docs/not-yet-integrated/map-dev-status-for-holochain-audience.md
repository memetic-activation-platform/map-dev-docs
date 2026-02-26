# Current State of the MAP (Memetic Activation Platform)

### Living infrastructure for self-organizing collective agency.

## Executive Summary

The Memetic Activation Platform (MAP) is a holon-native, agent-centric coordination runtime built on Holochain. 

It is not yet a user-facing platform.

Its core substrate is implemented and functioning. Higher-level coordination layers are architecturally defined but not yet implemented. The first surfaced capability will be a sovereign notification and signal normalization layer.

MAP is best understood not as a single application, but as:

> A living infrastructure for self-organizing collective agency — co-evolving participation, coordination, and regeneration across nested scales of life, from personal to local to planetary, without centralized control, capture, or domination.

Governance, economic flows, and ecological coordination are layered expressions of this architecture.

---

# Ontological Foundation — Structural Unification

At its core, the MAP is built on a single ontological pattern:

> Everything is a holon or a holon relationship.

A holon is:

- Self-describing (typed by a TypeDescriptor, which is itself a holon)
- Active (capable of participating in invocation flows)
- Evolvable (extensible through schema-as-data)
- Contextual (connected through typed relationships)

There is no structural distinction between:

- Schema and data
- System types and application types
- Governance structures and domain objects

All are holons.

---

## Holochain Minimalism

In Holochain terms, the MAP runtime is built from:

- One DNA
- One Zome
- One EntryType
- One LinkType

All domain variation — notifications, service agreements, capital flows, governance structures, resource types — emerges from this singular pattern.

The system extends itself through holon-defined schema rather than new entry types per application.

---

## Unified Schema & Data Import

Because TypeDescriptors are holons, schema is modeled as data.

The Holon Data Loader imports:

- TypeDescriptors (schema)
- Instances (data)
- Relationships between them

Any ontology expressible in the MAP’s Type Description Language can be imported — including both schema and instances — subject to the limits of that grammar.

This creates a structurally open runtime capable of evolving without modifying core code.

---

# Implemented: Core Coordination Substrate

The following layers are implemented and functioning:

- Holon CRUD
- Relationship modeling and traversal
- TypeDescriptor system (MetaType → Type → Instance)
- Two-pass Holon Data Loader (staging + resolution)
- `$ref` resolution model
- Structured JSON import format
- Invocation abstraction (Dance scaffolding)
- Action-based persistence via Holochain

Approximately 18,000 lines of Rust implement these layers.

This provides a domain-agnostic foundation for sovereign coordination.

---

# Architecturally Defined: Higher Coordination Layers

The following systems are designed but not yet implemented:

## Agreement-Mediated Coordination

- Validation framework
- Promise Weave protocol
- Multi-role inquiry templates
- LifeCode encoding
- Trust channel and membrane enforcement
- Signed agreement handling

These enable modeling of service agreements and multidimensional value flows.

---

## Multidimensional Value Flow Engine (Planned)

The intended next layers support:

- Vital capital stock modeling
- Service-based flow tracking
- Threshold monitoring (overshoot / undershoot)
- Adaptive response (dance more, dance less, renegotiate, inquire)
- Fractal scaling across agent hierarchies

This layer transforms governance into economic metabolism.

---

# Immediate Surface: Sovereign Signal & Notification Layer

The first visible capability will be a:

> Person-controlled notification and signal normalization engine.

This layer:

- Normalizes inbound signals from external channels (email, Discord, Signal, etc.)
- Unifies internal MAP-native notifications
- Applies schema-driven classification
- Enforces user-defined routing and policy
- Stores signals in a sovereign data context

It is not positioned as a notification aggregator, but as:

> The first surfaced expression of a person-centric coordination runtime.

This layer demonstrates:

- Holon-based extensibility
- Policy abstraction
- Unified internal/external signal grammar
- Agent sovereignty in practice

---

# Phased Architecture

The MAP unfolds in layered phases:

**Phase 1 — Sovereign Signal Control**  
Surface person-centric notification normalization and policy engine.

**Phase 2 — Agreement-Mediated Flows**  
Implement Promise Weave and service-based multidimensional value flows.

**Phase 3 — Threshold-Aware Adaptation**  
Enable capital stock monitoring and adaptive coordination responses.

**Phase 4 — Fractal Scaling**  
Apply identical coordination logic across families, organizations, watersheds, and bioregions.

Each phase builds on the same holon-native substrate.

---

# Strategic Positioning

The MAP today represents:

- A working holon-native runtime
- A self-describing schema architecture
- A unified schema-and-data import mechanism
- A minimal Holochain execution model
- A foundation for sovereign, multidimensional coordination

It is not yet a finished platform.  
It is a converged coordination operating system ready for its first surfaced capability.

---

# Closing

The MAP is:

- Substrate-real
- Ontologically unified
- Structurally open
- Governance-capable
- Economically extensible
- Experience-incomplete

The next milestone is to make the runtime visible through sovereign signal normalization, followed by agreement-mediated value flows and threshold-aware adaptation.