# DAHN Foundation Implementation Roadmap v1.4

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

The [bounded composition refactor](../space-navigator/space-navigator-impl-plan.md#22-bounded-visualizer-composition-refactor)
is the proposed delivery home for small Visualizer Operator contracts, coherent
allocation, shared generic/loader geometry, and explicit policy extents. Its
VC-1–VC-3 sequence supersedes older rendered-content sizing proposals; it does not
change historical completion records or estimates. Broader F1 work remains deferred.


Identifiers refer to the integrated plan, not the archived blueprint's numbering.
Dependencies are specified on those slices. Reusable capability can be delivered
inside a cross-component PR without becoming Dancer-owned behavior.

| Capability and owner | Delivery home | Recorded status / scope boundary |
| --- | --- | --- |
| Public SDK access and effective descriptors — SDK / DAHN adapter | PR 1; invocation integration in 40–43 | Through-Phase-3 baseline for PR 1; later invocation work planned. No parallel semantic model or TypeScript inheritance reconstruction. |
| Visualizer schema, semantic/implementation identity, materialization — DAHN/Rust | S1, PR 2 | Through-Phase-3 baseline; reconcile current schema in issue grounding. No Property intermediary retirement in this slice; bounded Operator schema work is now proposed under VC-1, with broader F1 deferred. |
| Owner-slot and subject selection — DAHN/Rust | PR 3 and “Phase 4 — Slot-directed Visualizer selection correction” | PR 3 recorded baseline; correction planned. Kind-only lookup and unconditional implementation fallback are superseded. |
| Theme/token infrastructure — DAHN | PR 4 and 5.a | Recorded baseline; additional theme switching is retained backlog below. |
| Application startup and generic Canvas — Launcher / Canvas | 5.a-pre, 5.a | Recorded baseline; home-Dancer coupling belongs to 5.b.1. |
| Visualizer Operators and shared inspector composition — DAHN / concrete Visualizers | VC-1–VC-3 in the integrated plan | Documentation proposal; no implementation or new enhancement authorized before design acceptance. |
| Context host, surface/view and bounded attention — Host / Canvas / composition owners | 18.a–18.c | Planned; independent restore state and explicit request outcomes. |
| Branch close and source-preserving exploration tabs — Path Inspector / Dancer | 18.d–18.e | Planned; Space Navigator owns exploration tabs sharing its read transaction within one host context; navigation productions remain Path Inspector-owned. |
| Adaptive reporting and validated choice — DAHN/Rust with concrete gesture owners | 21–23, 44–45, 48 | Planned; immediate UI response does not move durable learning into TypeScript. |
| Semantic staging, validation, undo/redo, commit — MAP; coordination — Dancer | 24–39, 51–54 | Planned; concrete editors delegate mutation to MAP. |
| Commons discovery, applicability and collective/exploratory policy — DAHN | 46–50 | Planned later expansion; authorization and explicit selection policy precede executable use. |

## Established bindings and sparse personal state: design reconciliation

The [DAHN v2.13 target](dahn-design-spec.md#145-recursive-selection) supersedes
on-demand-only preparation, automatic Usage creation on a lookup miss, and
per-slot ancestry-based personal discovery. This documentation change records
intended behavior; it does not establish delivery or authorize runtime changes.
The integrated plan remains the delivery sequence; the following work requires
implementation grounding rather than inferred completion or new estimates:

- Resolve/validate developer-prescribed semantic child defaults separately from
  slot contracts, including subject-dependent defaults and personal precedence.
- Prepare shared bindings when Visualizers, slots, declarations, or compatibility
  dependencies change, so a first visit needs neither prior personal use nor
  speculative loading of inactive navigation destinations.
- Reach personal choices through authorized agent/context access; bulk-load and
  index relevant records, including reusable known absence. Evaluate ancestry
  from metadata instead of repeating backend Usage-discovery walks per slot.
- Support composition-owned subordinate settings and cross-cutting preferences,
  with explicit local overrides; keep exact relationships, scope keys, schema
  migration, and adaptive policy unresolved pending grounded design.
- Create/persist personal Usage only for meaningful personal state. Keep optional
  transient initialization, derived bindings, and learning evidence separate.
- Reconsider parent alternatives before dependent children; retain explicit open
  view application, admission, and state-preservation contracts.

### Recorded runtime findings, not target-state limits

The previous design recorded host-side selection and live transient Usage
preparation as each component was requested, with a consolidated
`ResolveVisualizerUsage` guest lookup. Its round-local memo shared found and
successful no-Usage answers, deduplicated identical in-flight calls, used selected
Visualizer/actual subject Type/Slot keys, and was bounded to 256 combinations.
It was discarded before background submission; errors were not cached. These
are recorded implementation findings, not the required future index keys or
proof that sparse Usage creation and bulk agent/context access are implemented.

The experimental full-presentation guest Dance was withdrawn after profiling:
guest saved-holon/relationship caches were execution-local and were not exported
with staged/transient session state. Returned references and live Usages did not
populate host saved caches, so host consumption could repeat metadata retrieval.
The host still performed affordance, value, Slot/Operator, and materialization
reads; shared selection metadata and saved caches reduced some repeated work.
The broader bulk runtime index remained subsequent work in that record. These
findings are preserved without a fresh runtime audit.

### Recorded guest Usage resolution and specialization

The recorded implementation exposes `ResolveVisualizerUsage`, a read-only,
Space-authoritative Dance afforded by `Visualizer.HolonType`; the selected Visualizer instance is the affording holon.
Its request supplies the actual subject descriptor (including PropertyType and
ValueType subjects) and the actual Slot. The execution context supplies the
authorized Agent Space; no independent agent parameter or cross-space search is
introduced.

The guest resolves the default ancestry policy in one call through ordinary
Reference Layer operations. Its response identifies an optional committed Usage
and its bound descriptor, the direct-applicability descriptor for default
creation when personal state requires it, and the ordered actual-first bounded
search path. Missing
applicability, malformed lineage, and unresolved ambiguity are errors. A miss is
a successful read result and does not create or stage a Usage.

The client Holon service delegates this capability to the guest. Current internal
transport follows the existing guest-only service Dance pattern; canonical
Dance invocation uses the same capability through its declared request/response
contracts. The host overlays only its own retained live Usages in nearest-type
order and never consults another context's uncommitted transaction. A nearer
committed configuration takes precedence over a farther live default. Creation,
configuration edits, and persistence retain their independent transaction
contract.

`SpecializeVisualizerUsage` explicitly copies a selected configuration into a
live Usage bound to the actual subject descriptor. Existing configuration at
that descriptor is reused rather than overwritten. Specialization does not copy
successful-use Slot associations or preferences, and the source configuration
remains unchanged. Ordinary `SaveVisualizerUsage` edits the selected Usage at
its existing scope, including a supertype scope.

This consolidated guest lookup is an existing transitional capability, not the
required personal-choice access path for every slot. The intended bulk
agent/context index replaces repeated per-slot ancestry discovery; retaining
this operation does not establish that the index or sparse creation is delivered.

### Reconciliation baseline and bounded persistence increment

The documentation reconciliation on 2026-10-30 incorporates DevDocs main
`28b3c3d` while retaining the DAHN binding and personal-state target above.
The current `EffectiveHolonDescriptor` contract, session ownership, prepared local
cache policies, and validation-owned duplicate handling remain authoritative.
They supersede the earlier transaction-scoped `EffectiveDescriptor` draft;
its historical implementation and verification notes do not establish completion
of the revised descriptor target.

[Issue #833](https://github.com/evomimic/map-holons/issues/833) defines the bounded
asynchronous Usage-persistence increment extending the historical PR 23.d
substrate. [PR #846](https://github.com/evomimic/map-holons/pull/846), inspected at
`62625dd6`, provides live transient Usage, startup/gesture batch ownership,
independent background saves, durable identity/version tracking, failure status,
and explicit retry. It also carries retained bindings, round-local metadata,
guest Usage resolution, inherited configuration, and type-owned composition
Slots. Their inclusion is explicitly accepted as supporting work in this branch;
retain that tested substrate rather than extracting it during the persistence
correction. Retained bindings and round-local metadata do not establish
pre-session binding preparation, and the current choice path does not establish
the PR 23.e session target. This scope acceptance does not mark the issue or PR
complete or add further selection-system work to #833.

The inspected implementation still initializes and queues default-only Usages,
coalesces repeated captures within one open round rather than across separately
submitted rounds, and resolves committed Usage through guest ancestry lookup.
The agreed reconciliation makes sparse creation a completion requirement for
#833: default-only rendering must create no durable VisualizerUsage records.
This explicitly extends the original persistence slice at the creation/admission
boundary; it does not require bulk agent/context access, developer-prescribed
defaults, or cross-composition personal indexing, which remain follow-up work.
The inspected implementation has not yet met that requirement.

The agreed immediate priority is usable application responsiveness during routine
verification, including the required npm start checks for PRs. #833 must avoid
durable Usage creation for default selections and commit required Usage creations
and updates asynchronously under the existing batching, isolation, ordering,
retry, and failure-status contracts. It does not redesign agent-initiated
Visualizer exploration or introduce an experience-design commit/cancel workflow.

The longer-term direction prepares shared Visualizer/Slot bindings before an
agent session so initial rendering minimizes or eliminates fresh selection work.
That preparation remains follow-up delivery; asynchronous persistence alone does
not establish it. PR 23.e / DevDocs #68 owns reconciliation of the agent-initiated
experience-design session. Whether its explicit commit waits for durable saving
or accepts a background handoff is unresolved and is not decided by #833.

Before closing the persistence increment, publish its reconciled scope, verify
zero durable Usage creation for default-only startup and navigation, verify
pending-revision coalescing across gesture submissions,
and record actual startup and explicit-switch responsiveness during background
commits. Include publication/usable-content time, queue wait, batch size,
transaction and attempt counts, backend duration, and foreground contention.
Passing mocked commit gates, CI, and nominal startup are useful verification but
do not replace that live evidence. No new measurements are claimed here.

The agreed merge criterion is bounded to this increment: default-only startup and
navigation create zero durable Usages, and required background saves introduce no
foreground dependency on queue drain, worker availability, or commit completion.
Live verification must show that foreground interaction remains available while
those saves run. Initial rendering may remain slow because selection and metadata
retrieval still dominate; report those timings and assign the remaining bottlenecks
to follow-up work. Residual latency from that deferred work is not by itself a
blocker for #833, and this increment must not claim to solve it. No absolute
startup-time target or percentage speedup is established by this decision.

### Experience Upgrade Session reconciliation

The revised target replaces automatic remembering after each successful explicit
replacement with agent-initiated acceptance of a coarser Experience Upgrade
Session. Current PR #846 publishes replacements, disposes their prior realization,
and reports successful explicit use for preference persistence immediately.
Those operations do not provide the proposed temporary working configuration,
session acceptance, or back-out lifecycle.

Visualizer choice and safe occurrence replacement belong to PR 23.e and
[DevDocs Issue #68](https://github.com/memetic-activation-platform/map-dev-docs/issues/68).
That issue currently specifies replacement of one captured Node occurrence and
permits remembered preference after successful publication; it does not yet
specify the coarser Experience Upgrade Session acceptance/back-out lifecycle.
Its existing exclusions also leave recursive choice and broader replacement
contracts outside that bounded delivery.

Agent-initiated Visualizer-selection design is deferred from #833 to PR 23.e /
Issue #68. Reconcile the new session target there before claiming its composition
boundary, acceptance/cancellation behavior, or persistence handoff settled.
Its commit may be synchronous or asynchronous; the choice remains open. Do not
make this session redesign a merge gate for #833 or infer that #833's background
saving contract settles the future explicit-commit experience.
#833 retains the agreed default-only sparse-creation gate and its background
persistence responsibilities. The session target does not establish bulk indexing
or prescribed-default implementation. No runtime or GitHub issue changes are
made by this documentation session.

### Documentation acceptance and later runtime validation

The default-only creation checks and required asynchronous saving apply to #833.
The Experience Upgrade Session scenarios belong to the PR 23.e design target;
shared preselection and bulk indexing scenarios describe later foundation work.
This table does not make all target scenarios prerequisites for #833.

| Scenario | Required behavior |
| --- | --- |
| First-time agent without personal Usages | Render prepared shared defaults without creating durable personal records for constituents. |
| First-time agent opens an Inspector with 18 properties, accepts all defaults, then closes it | Create no durable VisualizerUsage records for the Inspector or its constituents solely because they rendered successfully. Binding reuse and successful-use evidence remain separate. |
| Agent tries several alternatives during an Experience Upgrade Session | Keep the working changes temporary, including successfully presented alternatives; individual gestures do not update committed preferences. |
| Agent explicitly commits the Experience Upgrade Session | Retain the accepted resulting personal experience changes, without implicitly pinning them or committing subject edits. |
| Agent backs out without committing the Experience Upgrade Session | Preserve the previously committed personal configuration and remembered preferences. |
| Agent inspects or previews an alternative, or its replacement fails/cancels | Preserve the previous remembered preference. |
| Inspector with 18 scalar properties | Reuse one binding for each compatible resolution context; 18 occurrences do not imply 18 independent candidate searches or Usage ancestry traversals. Different contracts, ValueTypes, or relevant policy can require different bindings. |
| Preferred date interactor | Record once at agent/context scope and reuse across compatible compositions, including supported localization/calendar settings. |
| Local date override | Apply only in its declared scope, retaining the cross-cutting preference elsewhere. |
| Parent replacement | Resolve the chosen parent's actual child slots; do not explore obsolete descendants. |
| Newly contributed Visualizer | Expose during explicit exploration without silently replacing a valid active experience. |
| Stale/incompatible binding | Resolve locally or report an explicit error; never substitute an incompatible implementation. |
| Shared binding | Keep navigation, focus, staged edits, and expansion independent for each occurrence. |

Later runtime validation must count candidate discovery/ranking separately from
binding resolution, eligibility validation, configuration resolution,
materialization, and occurrence mounting. The reported roughly one-second
selection cost motivates reducing both cost and count; it is not a new benchmark
produced by this documentation task. With valid shared defaults, initial child
rendering performs no candidate search for those contexts. A genuinely unresolved
compatible context is resolved once and reused; merely batching 18 independent
searches into one SDK call does not meet this design. Measure the whole gesture,
including host-triggered reads and duplicate retrieval across host/guest scopes,
and distinguish guest-only timing, persistence latency, and selection work.

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
