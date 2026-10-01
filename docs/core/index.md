# MAP Core Developers

This documentation set is for **MAP Core Developers** — those who steward, evolve, and maintain the foundational infrastructure of the Memetic Activation Platform.

MAP Core Developers work at the deepest layers of the system, shaping:
- The **agent-centric architecture** of MAP
- The **holonic type system** and schema foundations
- Core protocols such as **Dances**, **TrustChannels**, and **Agreements**
- Validation, evolution, and interoperability rules that all other MAP capabilities depend on

These documents focus on **design intent, architectural constraints, and evolution strategy**, not just implementation details. They aim to make the system *legible* — so that changes can be made responsibly, extensions can remain compatible, and long-term coherence is preserved.

Much of the content here is **actively evolving**. MAP Core Developers are expected to reason about tradeoffs, not simply follow recipes. Where patterns are still emerging, this documentation will say so explicitly.

If you are looking to:
- Extend MAP with new capabilities → see **Holon Extension Developers**
- Build human-facing interfaces and experiences → see **Human Experience Developers**

This space exists to support the careful stewardship of MAP’s core — the substrate on which all higher-level ecosystems grow.

## Documentation Architecture

The [MAP Core Document Role Manifest](document-role-manifest.md) defines the
target documentation sections, their ownership boundaries, and the scoped
authority of design specs, architecture documents, language specifications,
guides, plans, checklists, and archived material.

## Performance Investigations

The [Performance section](performance/index.md) records measured behavior,
experiments, rejected approaches, and open questions. Start with the
[application startup investigation](performance/startup-and-canvas.md),
[host/guest caching lessons](performance/caching.md), and
[Core Schema load investigation](performance/schema-load.md).

## DAHN and Visualizer Specifications

| Concern | Start here |
| --- | --- |
| Shared foundation | [DAHN architecture](hx/dahn-arch.md) and [composition/runtime design](hx/dahn-design-spec.md) |
| Kind contracts and concrete realizations | [Visualizer families](hx/visualizers/index.md), organized by VisualizerKind |
| Dancer experience and subject binding | [Space Navigator](space-navigator/index.md) |
| Application-shell launch | [Launch experience](hx/dahn-launch-experience-design-spec.md) |
| Delivery planning | [Foundation roadmap](hx/dahn-implementation-plan.md) and [integrated sequence](space-navigator/space-navigator-impl-plan.md) |
| Refactor evidence and deferred design | [Refactor plan](hx/dahn-docs-refactor-impl-plan.md) and [migration ledger](hx/dahn-docs-refactor-ledger.md) |

A slot owner defines its contract and subject binding; the selected Visualizer
owns its internal experience. Kind contracts and concrete designs have separate
authority. The example Space Navigator → Path Inspector → Holon Inspector →
Table composition is substitutable, not a mandatory DAHN hierarchy.
