# DAHN Foundation Implementation Roadmap v1.3

## Purpose and delivery authority

This roadmap identifies reusable DAHN capabilities and their delivery homes.
The [Space Navigator integrated plan](../space-navigator/space-navigator-impl-plan.md)
is the single PR sequence for the initial experience, including shared foundation
work. Each slice there identifies its owners, design authority, dependencies,
and recorded status. This roadmap does not create a parallel milestone schedule.

The recorded baseline is delivery through Phase 3, confirmed by the project owner
on 2026-09-28; Phase 3A (18.a–18.e) and subsequent work remain planned in that
record. Documentation reconciliation is not a fresh implementation-status audit.
Existing Dev Points are historical estimates, not actuals or revised commitments.
The former speculative week ranges are archived, not carried into this roadmap.

## Design authorities

- [DAHN architecture](dahn-arch.md): public SDK seam, Rust/TypeScript responsibility,
  semantic versus experience state, transactions, and adaptation.
- [DAHN design](dahn-design-spec.md): owner-local slots, Rust selection and
  materialization, runtime/security, themes, allocation, and restoration.
- [Visualizer families](visualizers/index.md): kind promises and concrete behavior.
- [Space Navigator](../space-navigator/space-navigator-design-spec.md): direct
  Dancer roles, local HolonSpace binding, and transaction coordination.
- [Launch experience](dahn-launch-experience-design-spec.md): application-shell
  narrative, readiness, accessibility, and observational imagery provenance.

## Foundation capability map

Identifiers refer to the integrated plan, not the archived blueprint's numbering.
Dependencies are specified on those slices. Reusable capability can be delivered
inside a cross-component PR without becoming Dancer-owned behavior.

| Capability and owner | Delivery home | Recorded status / scope boundary |
| --- | --- | --- |
| Public SDK access and effective descriptors — SDK / DAHN adapter | PR 1; invocation integration in 40–43 | Through-Phase-3 baseline for PR 1; later invocation work planned. No parallel semantic model or TypeScript inheritance reconstruction. |
| Visualizer schema, semantic/implementation identity, materialization — DAHN/Rust | S1, PR 2 | Through-Phase-3 baseline; reconcile current schema in issue grounding. No Property intermediary or F1 schema expansion. |
| Owner-slot and subject selection — DAHN/Rust | PR 3 and “Phase 4 — Slot-directed Visualizer selection correction” | PR 3 recorded baseline; correction planned. Kind-only lookup and unconditional implementation fallback are superseded. |
| Theme/token infrastructure — DAHN | PR 4 and 5.a | Recorded baseline; additional theme switching is retained backlog below. |
| Application startup and generic Canvas — Launcher / Canvas | 5.a-pre, 5.a | Recorded baseline; home-Dancer coupling belongs to 5.b.1. |
| Context host, surface/view and bounded attention — Host / Canvas / composition owners | 18.a–18.c | Planned; independent restore state and explicit request outcomes. |
| Branch close and source-preserving new context — Path Inspector / Dancer / Host | 18.d–18.e | Planned; context hosting is reusable, navigation productions remain Path Inspector-owned. |
| Adaptive reporting and validated choice — DAHN/Rust with concrete gesture owners | 21–23, 44–45, 48 | Planned; immediate UI response does not move durable learning into TypeScript. |
| Semantic staging, validation, undo/redo, commit — MAP; coordination — Dancer | 24–39, 51–54 | Planned; concrete editors delegate mutation to MAP. |
| Commons discovery, applicability and collective/exploratory policy — DAHN | 46–50 | Planned later expansion; authorization and explicit selection policy precede executable use. |

## Concrete experience delivery map

| Concrete owner | Integrated delivery home |
| --- | --- |
| Holon Inspector | 5.b, 6, 9–10; child participation in 12–18.c; editing/action presentation in 24, 26, 30, 32–45, 51, 54 |
| PropertyMap and typed Value children | 6, 21–22, 24, 36, 43; label and value selection are direct |
| Table Collection | 5, 11, 13, 19–20, 36, 38, 42; common mutation semantics remain in Collection kind |
| Path Inspector | 12–18, 18.a, 18.c–18.e, 32, 41–42, 51–52, 54 |
| Space Navigator Dancer | 5.b.1, 18.e, 25, 27–31, 40.a, 45, 53 |
| Application-shell launch experience | 5.c |

## Older roadmap and blueprint disposition

The [v1.2 roadmap](archive/dahn-mvp-implementation-plan-v1.2.md) and
[v1.1 Phase 0 blueprint](archive/phase-0-implementation-blueprint-v1.1.md)
are historical archives. Their original content and estimates remain available;
they are not current contracts or competing PR sequences.

| Historical source | Current treatment / delivery home |
| --- | --- |
| Roadmap Phase 0: runtime, SDK, loader | PRs 1–4/S1; preserve public-SDK-only access, effective descriptors, lazy loading and framework independence. Development hot reload is backlog FDN-1 below. |
| Roadmap Phase 1: Canvas/theme/property/relationship/action presentation | 5.a, 5.b, 6, 9–18, 40; no permanent one-region Canvas or fixed renderer per kind. Token roles remain; exact example names are illustrative. |
| Roadmap §1.4: hardcoded static affinity | Superseded by DAHN slot-directed compatible-candidate policy; no TypeScript final selector. |
| Roadmap §1.5 and blueprint §15: TypeDescriptor demo | Retained as an integrated demonstration fixture across Node, property, relationship, and action delivery. Declared/inverse relationship provenance remains visible; schema editing uses ordinary permitted MAP operations. |
| Roadmap Phase 2: generic/schema editing and creation | 24–39, 53–54; validate in MAP, surface feedback in selected editors. Trusted-space/no-permission assumptions do not override current authorization. The old blanket inverse-editing assertion yields to current MAP mutation contracts. |
| Roadmap Phase 3: salience, affinity, theme switching | 21–23, 44–45, 48; multiple-theme catalogue and switching retained as FDN-2. No fixed theme-count commitment. |
| Roadmap Phase 4: Commons, community signals, contributor tooling | 46–49; authoring kit/docs retained as FDN-3. Discovery does not authorize execution. |
| Roadmap Phase 5: Canvas variants and adaptive controls | 18.a–18.e and 50 for established contracts; additional host/Canvas/Visualizer forms retained as FDN-4. Navigation grammar is not universally Canvas-owned. |
| Roadmap Phase 6: Alpha / “Walk the MAP” | Retained as an eventual integration demonstration, not a dated release or evidence of completion. Includes descriptor navigation/editing, themes, choice, actions, Commons and adaptation. |
| Roadmap Phase 7: localization, accessibility, devices | FDN-5; existing per-feature accessibility obligations still apply now. |
| Blueprint §§1–2, 4, 11: host placement/module wiring | PRs 1–4, 5.a-pre/5.a/5.b.1; thin host integration and package-like boundaries retained. Suggested filenames are historical examples, not required code structure. |
| Blueprint §§3, 5: bound handles, context, affordance projections | PR 1/current SDK and DAHN contracts. `BoundHolonCollection`, preconstructed `AffordanceNode[]`, old target/context interfaces and wire assumptions are superseded, not copied forward as interfaces. |
| Blueprint §§6–7: registry, builtin and selector | PRs 2–3; loader idempotence remains useful validation. Unconditional `holon-node` selection and client final resolution are retired. |
| Blueprint §§8–10: Canvas, Node, action/value helpers, theme | 4–6, 9, 40; child selection replaces growing renderer switches. Optional debug viewer stays optional bring-up tooling. |
| Blueprint §12: eight early PR slices | Superseded identifiers; use integrated PRs 1–6/S1, 5.a-pre/5.a/5.b/5.b.1, 9 and 40. Do not equate the two numbering systems. |
| Blueprint §13: tests | Preserve SDK boundary checks, transport-free contracts, loader idempotence and mounting checks in relevant slices. Replace obsolete selector/affordance-tree expectations with current slot/subject semantics. |
| Blueprint §14: open SDK/fixture questions | Revisit current SDK exposure during issue grounding; known TypeDescriptor fixture remains useful. These are not assumed missing runtime APIs. |

## Retained foundation backlog

These entries are the delivery home for unique future work not already assigned
an integrated PR. They are unscheduled and unestimated; do not pull them into the
initial delivery or assign old speculative week ranges to them.

| ID | Capability / owner | Prerequisites and disposition |
| --- | --- | --- |
| FDN-1 | Development hot reload and optional diagnostic viewer — DAHN tooling | Authorized artifact loading and runtime lifecycle; later developer tooling, not production loading authority. |
| FDN-2 | Theme switching, multiple theme catalogue and persisted preference — DAHN | Complete token/meta-design contracts and validated theme selection; includes light/dark variants without prescribing a fixed count. |
| FDN-3 | Visualizer contributor starter kit and authoring guide — DAHN Commons | Stable runtime/slot contracts and authorized materialization; connect to PR 46, retain as separate tooling work. |
| FDN-4 | Additional Canvas/host experiences and richer layout — Canvas/Host and concrete Visualizers | Established allocation/context contracts; classify card/reading/navigation experiences by their actual owner rather than automatically making each a Canvas kind. Collaborative persistence, sophisticated placement and multimodal/spatial variants remain deferred. |
| FDN-5 | Localization, accessibility completion and device variants — shared themes/host plus each concrete Visualizer | Translation, locale formatting, RTL, keyboard/screen-reader coverage, contrast, reduced motion, touch/context menus and compact layouts. Existing immediate accessibility requirements are not deferred by this backlog. |

Full production sandboxing, signing, dependency isolation and rich external
package acquisition remain deferred under the integrated plan's “Capabilities
Intentionally Deferred”; they must be resolved before any delivery requiring
those security guarantees. No archive example relaxes current execution policy.

## Deferred design handoff

[F1](dahn-docs-refactor-impl-plan.md#deferred-design-participation-contracts-and-occurrence-invocation)
retains holonic participation contracts, Visualizer/slot-afforded actions,
Commands/Dances/Operators reconciliation, and occurrence representation.
Maximize/Restore behavior and independent pane/Node state are established;
new schema and dispatch vocabulary are not. Exact undeclared child accepted types
also remain open. Revisit these before grounding work that depends on their
representation, not as a prerequisite for finishing the documentation refactor.

## Change log

v1.3 replaces competing historical phases with capability ownership, one integrated
PR sequence, explicit source disposition, and a retained unscheduled backlog.


## Architecture delivery and validation guidance

Retained from architecture §§67–70. Apply these checks in the integrated slices
that own each capability, not as a separate PR sequence. Module trees are
illustrative; current design and code grounding determine exact placement.

### 67. Space Navigator as an Architectural Proof

The Space Navigator should prove the DAHN architecture through a constrained initial implementation.

The first implementation does not need the complete future ecosystem.

It should, however, preserve the intended boundaries around:

- Rust-side visualizer selection;
- Visualizer Holon and implementation-reference runtime resolution;
- ordinary generic candidates;
- descriptor-driven composition;
- hierarchical layout;
- theme tokens;
- TypeScript occurrence state;
- Rust-owned staged state;
- transaction snapshots;
- Dancer-experience-scoped transaction controls;
- adaptive gesture reporting.

The implementation MAY initially use only locally bundled core visualizers while keeping the interfaces compatible with future Visualizer Commons discovery.

### 68. Initial Architectural Modules

A possible TypeScript decomposition might include:

    dahn/
      canvas/
      visualizer-runtime/
      visualizers/
        node/
        collection/
        property-map/
        value/
        action/
      layout/
      theme/
      state/
      map-adapter/

A possible Rust conceptual decomposition might include:

    dahn/
      discovery/
      selector/
      adaptation/
      presentation-context/

Existing MAP transaction, cache, command, and holon infrastructure SHOULD be reused rather than duplicated into a DAHN-specific runtime.

The exact repository structure is not normative.

The responsibility boundaries are.

### 69. Architectural Testing Boundaries

The architecture SHOULD support testing at multiple levels.

#### 69.1 Rust / MAP Tests

Test:

- descriptor resolution;
- visualizer discovery;
- visualizer applicability;
- Selector behavior;
- adaptive signal processing;
- transaction staging;
- transaction snapshots;
- Undo;
- Redo;
- validation;
- Commit;
- relationship expansion;
- dance/query execution.

#### 69.2 DAHN Adapter Tests

Test:

- SDK translation;
- async behavior;
- error normalization;
- visualizer selection requests;
- adaptation-event reporting;
- transaction control.

#### 69.3 Visualizer Runtime Tests

Test:

- Visualizer Holon / implementation-reference resolution;
- failure to resolve selected implementation;
- no semantic or generic-fallback selection after a resolution failure;
- version compatibility where implemented.

#### 69.4 Visualizer Tests

Given:

- semantic input;
- descriptor context;
- layout budget;
- theme;
- interaction mode;

verify:

- rendering;
- child composition;
- semantic events emitted.

#### 69.5 Composition and Dancer Tests

Verify:

- visualizer occurrence management;
- layout allocation;
- navigation state at its owning Visualizer;
- transaction-action state;
- composition of child visualizers.

#### 69.6 Adaptive Interaction Tests

Verify:

- immediate TypeScript reordering;
- semantic adaptive event emission;
- persistent preference influence;
- alternate visualizer selection signals.

### 70. Architecture That Should Not Be Over-Generalized Initially

The initial Space Navigator implementation SHOULD NOT require full implementation of:

- remote visualizer package loading;
- arbitrary third-party code execution;
- production-grade sandboxing;
- sophisticated adaptive scoring;
- every salience rubric;
- every maturity model;
- decentralized package dependency resolution;
- advanced recommendation explanation;
- theme marketplaces;
- generalized layout constraint solving;
- complete cross-device adaptation;
- every visualizer category;
- every possible dance result shape.

The architecture should leave room for these capabilities without requiring them before the Space Navigator can be useful.
