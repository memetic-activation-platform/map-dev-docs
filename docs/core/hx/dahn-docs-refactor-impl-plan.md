# DAHN Compositional Authority Documentation Refactor Plan

> **Status:** In progress — DOC1–DOC4 complete; DOC5–DOC6 pending. Shared and concrete design authority is reconciled; delivery planning is next.
> **Tracks:** [map-dev-docs #56](https://github.com/memetic-activation-platform/map-dev-docs/issues/56).
> **Baseline:** Working tree on 2026-09-30, including the inserted DAHN Design Concept
> and the current Path Inspector grammar edits.

## Purpose and scope

Refactor the documentation so that authority follows composition boundaries:
DAHN owns reusable composition/runtime mechanisms, Dancers own experience roles
and subject coupling, and selected Visualizers own their internal experiential
behavior. Preserve existing behavior while relocating its normative authority.

This plan implements the documentation changes requested by issue #56. It does
not implement runtime or schema changes, create implementation issues, re-estimate
Dev Points, or change reported delivery status. Follow
[CONTRIBUTING](https://github.com/memetic-activation-platform/map-dev-docs/blob/main/CONTRIBUTING.md) and the
[document role manifest](../document-role-manifest.md): design decisions belong
in specs; migration decisions, sequencing, and acceptance checks belong here.

## Findings from the DOC1 baseline documents

- [DAHN Design Specification](dahn-design-spec.md) Section 4 provides the new
  conceptual anchor. Later sections still prescribe Holon Inspector slots,
  projection, navigation axes, and concrete compression. INV-6 assumes slots
  are Visualizer-local; INV-13–15 mix semantic cardinality with spatial grammar.
- [Space Navigator Design Specification](../space-navigator/space-navigator-design-spec.md)
  v0.7 contains Dancer orchestration, launch experience, Node internals, table
  sorting, editing, and navigation geometry in one normative document.
- [DAHN Architecture](dahn-arch.md)
  v0.4 explicitly claims reusable DAHN architectural authority despite its
  application-specific location. Its introduction still attributes navigation
  geometry to the Space Navigator interaction grammar.
- [Space Navigator Interaction Grammar](../space-navigator/space-navigator-interaction-grammar.md)
  v0.3 and [Path Inspector Grammar](visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md)
  v0.4 already separate substantial Dancer and Visualizer authority. Preserve
  that work. Path Inspector's “PropertyMap sub-slot content extent” material
  still reaches into Holon Inspector's child composition and needs extraction.
- [Space Navigator Implementation Plan](../space-navigator/space-navigator-impl-plan.md)
  v1.2 records delivery through Phase 3 and introduces Phase 3A, PRs 18.a–18.e.
  Its existing foundation/application distinction is a useful starting point.
- [DAHN Implementation Plan](dahn-implementation-plan.md) v1.2 and the
  [Phase 0 Blueprint](phase-0-implementation-blueprint.md) describe older
  delivery models. The blueprint still uses `BoundHolonCollection` and
  `AffordanceNode[]`, concepts explicitly superseded by the current DAHN spec.
- `mkdocs-core.yml` still labels the current DAHN spec “Phase 0”; the document
  role manifest has no explicit DAHN/Dancer/Visualizer ownership entries.

## Proposed authoritative homes

Paths below are relative to `docs/core/`. The kind and concrete Visualizer frames
exist after DOC1; the architecture move is complete after DOC2. Launch and grammar
moves are complete after DOC3. Keep current DAHN and Space Navigator design
spec paths stable; move reusable architecture and concrete Visualizer material
out of the Space Navigator directory.

| Destination | Authority and treatment |
| --- | --- |
| `hx/dahn-design-spec.md` | Master composition/runtime design, anchored by Section 4; delegates concrete behavior and focused contract definitions. |
| `hx/dahn-arch.md` | Move and narrow `space-navigator/space-navigator-arch.md`; own subsystem responsibilities and boundaries. Detailed mechanisms delegate to the DAHN design spec rather than being defined twice. |
| `hx/visualizers/` kind hierarchy | VisualizerKind provides the organizational parent: Structure → RootedNavigation, Node, and Collection each have `kind-spec.md`. Slot contracts remain with their composition owners; kind-level shared promises do not replace local requirements. |
| `space-navigator/space-navigator-design-spec.md` | Dancer purpose, local HolonSpace binding, directly owned roles, coordination, actions, and transaction interaction. Delegate MAP transaction semantics to their existing owners. |
| `space-navigator/space-navigator-interaction-grammar.md` | Dancer-level interaction productions only; reference shared DAHN mechanisms and selected Visualizer grammars. |
| `hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md` | Move the existing grammar, retaining its authoritative topology, lineage, spatial projection, focus, compression, overflow, and branch productions. |
| `hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md` | RootedNavigation fulfillment, compatible root subjects, direct child slots, state ownership, and realization details extracted from the larger specs. Link the grammar instead of repeating it. |
| `hx/visualizers/node/holon-inspector/design-spec.md` | Concrete Node realization, six current internal slots, affordance projection, child composition, responsive behavior, and local editing presentation. |
| `hx/visualizers/collection/table/design-spec.md` | Concrete table rows/columns, sorting/filtering, metadata, selection, restoration, editing presentation, and child roles supported by existing material. |
| `hx/dahn-launch-experience-design-spec.md` | Extract the already substantial DAHN launch narrative, accessibility, imagery provenance, and readiness/handoff behavior from Space Navigator §1.8. Preserve the existing application-shell/Launcher boundary. |
| `hx/dahn-implementation-plan.md` | Reconciled foundation roadmap, referencing the integrated delivery sequence rather than maintaining a conflicting PR schedule. |
| `space-navigator/space-navigator-impl-plan.md` | Integrated demonstration/delivery sequence; every capability attributed to its architectural owner and governing spec. |

Property is not a VisualizerKind in the accepted target model. PropertyMap
composes label and value roles directly. Do not create concrete Value or Action
implementation specs merely
for symmetry. Use kind specs for established common promises and owner specs for slot contracts and the concrete
owner's spec for existing internal behavior; extract further documents only
when the inventory demonstrates an independently meaningful implementation.

For moved documents, leave a short non-normative relocation page at the old
path. Preserve old externally useful heading anchors where practical, linking
to their replacements. Internal links must use canonical destinations. Archive
historical content only after unique still-valid behavior has been accounted for.

## Additional accepted framing decisions

Create kind directories on demand only; do not preallocate a taxonomy or mirror
every ValueType. PropertyMap, Value, and String kind frames extend DOC1 because
the accepted composition gives each a concrete documentation role. PropertyMap owns set-level
layout, visibility, personalization, and label/value composition. Its label role
may select a String Visualizer for PropertyName; its value role selects an
applicable ValueType-specific Visualizer. Neither role requires an intervening
Property VisualizerKind. PropertyDescriptor metadata remains available at the
selection/binding boundary.

DOC2 must remove Property from the target kind registry and reconcile the old
PropertySlot / PropertyVisualizer / ValueViewerSlot chain, selector signatures,
examples, and invariants. Preserve useful metadata and semantic validation
requirements while retiring only the unnecessary presentation layer. DOC4 must
apply the same model to concrete PropertyMap and Table cell composition wherever
the source inventory establishes it. Do not assume Table composition is identical
to PropertyMap composition.

## Initial source-to-owner map

Section numbers refer to the baseline above. During execution, track heading
names and individual statements as well as numbers so renumbering cannot hide
missing content. These groups seed the audit; they are not a completed inventory.

| Source material | Disposition |
| --- | --- |
| DAHN §§1–14, §§33–43, §45–52 | Audit and primarily retain composition/runtime material; split out concrete examples and implementation-specific rules. Reconcile architecture duplication. |
| DAHN §§15–18, §§20–26, §32, §53 | Split reusable contract promises from Holon Inspector slots/projection and concrete Collection/Property/Action behavior. The Book rendering example belongs with Holon Inspector or is a clearly linked illustration. |
| DAHN §19 and §28; INV-13–15 | Retain cardinality as semantic input; move horizontal/vertical realization and collection-mediated lineage to Path Inspector. |
| DAHN §27 | Retain Collection/Structure classification and peer Graph, Geospatial, RootedNavigation specializations; kind-level detail delegates to the family specs; slot contracts remain owner-local. |
| DAHN §§29–31 | Separate reusable allocation/state-survival rules from Path Inspector geometry and child realization. |
| DAHN §§54–57 | Move delivery guidance into plans; reconcile supersession and conclusions so they no longer grant Space Navigator authority over all topology. |
| Space Navigator §§1–6 | Split Dancer semantics and direct actions from launch (§1.8), shared selection, active-frontier, and geometry material. |
| Space Navigator §§7–17 and §25 | Holon Inspector internal composition and projection; distinguish semantic inputs from concrete placement. |
| Space Navigator §§18–24 | Collection contract versus Table Collection realization and editing; preserve semantic editing ownership through references to existing runtime/transaction specs. |
| Space Navigator §§26–30, §§34–36, §49 | Split Path Inspector topology/allocation, child responsive/loading presentation, and shared state contracts. |
| Space Navigator §§31–48 | Statement-level split: Dancer transaction controls, local Visualizer edit presentation, and upstream MAP staging/transaction semantics. Do not move this range wholesale. |
| Space Navigator §§50–54 and trailing selection alignment | Rehome scenarios, open questions, and invariants by owner; integrated examples may remain with links and explicit illustrative status. |
| Both grammars, architecture, concept, and index | Retain their distinct roles; remove cross-boundary normative claims and update the authority map. |

## Migration ledger and review rules

Maintain `hx/dahn-docs-refactor-ledger.md`, created during DOC1, as an implementation-plan
companion. For every normative statement or tightly coupled group, record:

| Field | Required evidence |
| --- | --- |
| Source | Original path, heading/anchor, and identifiable statement text; record baseline commit plus working-tree changes. |
| Owner and boundary | Architectural owner, nearest slot boundary, and result of the conforming-substitute test. |
| Disposition | Retain, move, rewrite, or retire. |
| Destination | Canonical path and heading; for retirement, record the obsolete assumption and reason. |
| Verification | Pending or checked, with conflicts and their resolution recorded. |

A source section can require several rows. Removing a paragraph is complete
only when its normative statements have a checked destination or an explicit
retirement rationale. Preserve source wording when moving; rewrite only to
correct authority, reconcile a conflict, or remove duplication.

For each documented slot, inventory its owner, required role/contract, bound
subject, selection inputs, participation obligations, and selected child's
freedoms. Document only established requirements. Mark genuinely unspecified
promises as open design questions; do not invent an API to make the table full.

## Deferred design: participation contracts and occurrence invocation

**Disposition (2026-10-01):** Stabilize the documentation first. Preserve this
question for a separate design pass; it is not a prerequisite for DOC3–DOC6.
This record captures discussion, not an approved runtime or schema extension.

### Problem to retain

Node kind membership alone does not guarantee compatibility with Path
Inspector's independent horizontal/vertical compression states, extent reporting,
and state-survival requirements. Alternative RootedNavigation Visualizers may
require different Node participation while satisfying the same Dancer slot.
Those participation obligations need to be discoverable by implementers and,
eventually, available holonically to selection.

### Directions discussed, not yet specified

- Multiple reusable participation contracts, with contract types defining
  semantics/configuration shape and ordinary contract instances supplying
  configurations, following the Rule/Constraint precedent. Exact type names,
  relationships, composition, versioning, and compatibility rules remain open.
- Required operations could connect conformance declarations with runtime
  dispatch. `InstanceOperations` was considered, then explicitly set aside
  pending examination of existing affordances: HolonTypes afford Dances and
  Commands; ValueTypes afford Operators. Do not introduce a new operation
  vocabulary by assumption. Dances appear too heavy for these interactions;
  Command applicability and receiver semantics need investigation.
- Visualizer supplies reusable capability and implemented behavior. The user's
  intended VisualizerUsage is agent-relative, approximately one per agent per
  Visualizer, rather than one per active presentation. Exact identity/cardinality
  rules are not yet formalized.
- A VisualizerOccurrence may provide per-realization identity and state so the
  same agent/Visualizer can present multiple subjects independently. Occurrence
  is already a runtime concept; making it a Holon, choosing its lifecycle or
  persistence, and partitioning semantic versus renderer-local state are open.
- Names such as Two-Axis Path Inspector and Outline Navigator illustrate
  different concrete grammars, not approved renames or new VisualizerKinds.

### Retained requirement: Visualizer- and slot-afforded actions

Visualizers and their slots can offer presentation actions beyond the actions
afforded by their bound semantic subjects. The need is accepted; the holonic
representation and invocation mechanism remain deferred under this record.

The concrete example from DOC4 review is Maximize/Restore:

- Properties Pane and CollectionViewer can each maximize to occupy the full
  Node Visualizer area, then restore their prior dimensions within the current
  grant. These are actions on the owner's local slot composition.
- Node Maximize requests more Path Inspector real estate; the parent owns that
  allocation and its restoration.
- Pane and Node restore states remain independent. Restoring a pane must not
  also restore the Node's outer allocation.
- These actions should have action slots and concrete Action Visualizers. The
  described realization uses opposing diagonal arrows whose Maximize/Restore
  presentation responds to the relevant state.

The future design must account for the declaring Visualizer or slot owner,
the runtime presentation target, state-dependent availability/presentation,
and Action Visualizer selection. An owner Holon's HolonType selection anchor
explains subject actions but does not yet account for these presentation actions.
Do not generalize that subject-action assumption into a complete model of all
actions. Resolve this gap alongside existing Commands/Dances/Operators and
occurrence identity; no new schema type, relationship, dispatch protocol, or
persisted slot-occurrence model is chosen here.

### Boundary for the remaining refactor

Continue moving established behavior to its proper owner. Keep Path Inspector's
current participation obligations explicit at its child slot boundary; distinguish
those obligations from Holon Inspector's private realization. Preserve existing
runtime state and invocation descriptions with scoped authority. Where a source
assumes an unresolved representation, flag it in the ledger rather than silently
promoting that assumption or inventing a replacement.

Do not add contract-type TDL, operation relationships, dispatch mechanisms,
occurrence persistence, or uniqueness constraints during this refactor. Slot
contracts can be documented as participation requirements without claiming that
their complete holonic representation has been settled. The earlier accepted
kind organization and direct PropertyMap label/value composition remain in scope.

### Revisit after stabilization

After DOC6, review this record before planning schema/runtime follow-ons. Inspect
the actual Rule/Constraint and Dance/Command/Operator models in `map-holons`, then
settle receiver identity/state ownership, contract composition/conformance, and
invocation together. Identify both upstream type-system implications and downstream
TDL, selection, runtime, and conformance-test work. Do not lose this dependency
when reconciling delivery plans in DOC5.

## Delivery sequence

Each chunk includes its migration-ledger updates, source deletions/delegations,
and affected link repairs. Avoid leaving two active normative copies between
chunks. These are documentation review units, not new runtime PR identifiers.

### DOC1 — Frame the spec family and provisional authority map

Create the destination shells first so existing content has an explicit home:

- a VisualizerKind-organized family index and Structure, RootedNavigation, Node,
  and Collection kind-spec frames;
- Path Inspector Design Specification, linked to the existing authoritative
  Path Inspector grammar until its move in DOC3;
- Holon Inspector Design Specification; and
- Table Collection Visualizer Design Specification.

Each concrete Visualizer shell should establish:

1. purpose and architectural authority;
2. contract fulfilled and compatible subject shape;
3. direct child roles/contracts and subject bindings, where already established;
4. internally owned behavior and state;
5. boundaries with parent, children, DAHN runtime, and MAP semantics; and
6. links to current source material awaiting extraction.

Use the same outline where useful, but do not invent child slots or requirements
for symmetry. Kind specs describe semantic classification and established common promises;
owner-defined slot contracts describe local substitutability requirements;
concrete specs describe particular realizations. Keep the existing Path Inspector
grammar authoritative for its detailed behavior rather than scaffolding a second
copy of it.

Mark each shell as an incomplete extraction destination. Its status must name
which existing documents still own behavior pending migration; creating the shell
does not silently supersede their contents. Keep paragraph-level migration tasks
in the ledger, not in the design specs. Link the family from the relevant indexes
and navigation so it can be reviewed before extraction.

Record the current uncommitted Design Concept and grammar changes as part of the
baseline. Seed the ledger with the source-to-owner map above and add the proposed
ownership model to the document role manifest, distinguishing target authority
from completed migration. Inventory source headings and invariants now; expand
rows to individual statements as each extraction proceeds. A complete statement
inventory is required at completion, not as a prerequisite to the first move.

Record these known tensions and resolve each before its dependent extraction:

- Slots may be Dancer-owned or Visualizer-owned; revise DAHN INV-6 accordingly.
- Visualizer fulfills a contract; VisualizerUsage records agent-specific use.
  Reconcile the old chain in DAHN Near-Term Design Priorities.
- “Selector Function” denotes a typed function of the Rust-owned Visualizer
  Selection Service, preserving existing centralized authority and explicit
  no-candidate errors. Agent overrides must remain conforming selections through
  that authority, not independent TypeScript resolution.
- Holon/Visualizer identity and content-addressed executable identity are distinct;
  resolve ambiguous “Visualizer identity” wording against the architecture.
- Path Inspector's child participation/extent requirements may constrain Node
  substitutes, but cannot require Holon Inspector's private sub-slot layout.
- Current Table Collection default ordering, progressive population, destination-first
  transitions, and stable collection switching must survive extraction.

**Exit:** The four kind-spec frames and three concrete Visualizer spec shells are
reviewable, with explicit authority boundaries and links to current sources.
All source headings and invariants have provisional destinations in the ledger.
Any unresolved design decision identifies the affected chunk and does not block
independent, unambiguous migrations.

### DOC2 — Establish DAHN and contract authority

Move reusable architecture to `hx/dahn-arch.md`, narrow its role, and reconcile
shared concepts in the DAHN spec using Section 4 as the anchor. Populate the
kind specifications and owner-local slot contracts framed in DOC1 by extracting existing minimum promises, not lifting all
current implementation behavior into universal requirements. Preserve
Structure specializations, subject identity/type/topology versus bound data,
agent preferences/usage/configuration/overrides, and runtime trust boundaries.

Transfer reusable composition rules from the Space Navigator grammar where
needed. Replace their former normative copies with references. Review all
DAHN invariants: retain runtime rules, revise ownership assumptions, and identify
concrete invariants for relocation in DOC3–DOC4.

**Exit:** A reader can distinguish a slot contract from a concrete Visualizer's
grammar. Shared allocation, selection, and state authority each have one home.
Remaining concrete extractions are explicitly accounted for in the ledger.

### DOC3 — Extract Path Inspector and narrow Space Navigator

Move the existing Path Inspector grammar and populate its complementary design
spec shell. Extract occurrence topology, lineage, navigation geometry, focus,
compression/overflow, direct child requests, close, and re-root behavior.
Keep generic root compatibility explicit; local HolonSpace binding belongs
only to Space Navigator. Preserve the current grammar's surface/view distinction
and non-destructive context requests.

Reduce the Space Navigator spec and grammar to Dancer authority: direct roles,
local HolonSpace subject binding, orchestration/actions, and transaction-level
interaction genuinely owned there. Split staged-state contracts from their
presentation. Extract the launch experience into its own application-shell spec.

**Exit:** Space Navigator requires RootedNavigation without selecting Path
Inspector by fiat or owning its descendants. Path Inspector has a single spatial
grammar and can operate over a compatible Holon other than a HolonSpace. Review this with
a hypothetical conforming alternative that uses different navigation geometry.

### DOC4 — Extract Holon Inspector and Collection realization

Complete the Holon Inspector and Table Collection specifications from the mapped
material. DOC3 already relocated their Space Navigator sections and the private
PropertyMap extent contract to establish the Dancer boundary.
Move internal slots, projection rules, placement, responsive realization, loading,
and editing presentation to their concrete owners. Transfer the PropertyMap
content-extent subsection from Path Inspector into Holon Inspector; retain only
the actual child participation contract in the Path Inspector authority set.

Separate Collection promises from tabular behavior. Preserve table sorting,
filtering, metadata, occurrence-local restoration, array/relationship/Dance
editability distinctions, and semantic editing ownership. Move relevant scenarios
and open questions without prematurely resolving them.

**Exit:** DAHN, Space Navigator, and Path Inspector no longer prescribe private
Holon Inspector or Table internals. Every concrete child slot identifies its
subject binding and selector boundary; all removed behavior is ledger-checked.

### DOC5 — Reconcile implementation planning

Recast the DAHN plan as the reusable foundation roadmap. Retain the Space
Navigator plan as the integrated delivery sequence. For every existing slice,
record owning component(s), capability-to-owner attribution, authoritative spec
links, dependencies, and existing status. Cross-component slices remain valid.

Preserve PR identifiers, issue references, delivered-through-Phase-3 status,
and the planned status of 18.a–18.e. Preserve existing estimates as historical
planning values; flag materially changed scopes for later issue-grounded
re-estimation. Do not infer code delivery from documentation conformance.

Audit the Phase 0 blueprint and older DAHN milestones. Preserve still-valid
unique work in the appropriate plan; explicitly supersede/archive obsolete
material and remove its active navigation entry. Keep deferred personalization
and Commons work visible without pulling it into the initial delivery scope.

**Exit:** Every planned capability has an architectural owner and one delivery
home; the older plan/blueprint cannot direct a reader to superseded contracts.

### DOC6 — Finish navigation, diagrams, and acceptance review

Update `mkdocs-core.yml`, `docs/core/index.md`, the Space Navigator concept/index,
and the document role manifest. Present DAHN foundation, contracts, Dancer, and
concrete Visualizers as distinct navigation groups. Add canonical links for the
new specs and this plan; remove the obsolete DAHN “Phase 0” label.

Audit inbound references across active documentation and all MkDocs portal
configs. Keep historical archives historical; fix their links only where moves
would break access. Review the DAHN composition diagram and other affected
diagrams for contract fulfillment, agent-relative usage, peer Structure kinds,
subject binding, and illustrative versus mandatory composition.

**Exit:** All issue #56 acceptance criteria map to checked evidence; no normative
statement has an unaccounted deletion, no ownership conflict remains unresolved,
and changed links/anchors and navigation entries resolve.

## Ordering and validation

Execute `DOC1 → DOC2 → DOC3 → DOC4 → DOC5 → DOC6`. DOC3 and DOC4 have deliberate
handoffs: preserve intermediate references and move material with its callers.
Do not renumber runtime PRs to match these documentation chunks.

Validation is primarily semantic review, supported by mechanical checks:

1. Reconcile every ledger row and every issue acceptance criterion. Audit all
   remaining normative claims using the conforming-substitute test.
2. Check every slot's contract, subject binding, owner, and selection boundary.
   Trace Space Navigator → RootedNavigation → Path Inspector → Node → Holon
   Inspector → Collection as an illustrative composition, then check that
   substitutions do not inherit private implementation requirements.
3. Search active docs for old paths, `VisualizerUsage`, `HolonNodeVisualizer`,
   `RootedNavigation`, horizontal/vertical invariants, selector fallbacks, and
   Space Navigator ownership claims. Inspect context; a term's presence alone
   is not a failure. Preserve historical changelog wording as history.
4. Check relative links, relocated fragment anchors, image references, heading
   numbering, and MkDocs navigation. Run `git diff --check` for each chunk.
5. Run `mkdocs build --strict -f mkdocs-core.yml --site-dir /tmp/map-docs-56-core`
   and inspect the generated navigation and representative new pages. Record
   pre-existing warnings separately from regressions; do not claim a clean
   strict build if unrelated baseline warnings prevent one.
6. Run the other portal builds listed in `.github/workflows/pages.yml` when their
   links/configuration are affected. Use temporary output directories and do not
   commit generated site output. No deployment is part of this plan.

Completion means DOC1–DOC6 are checked, all preserved behavior has exactly one
normative home, deliberate retirements have reasons, implementation ownership
is traceable without changing delivery history, and issue #56 can be reviewed
entirely from the resulting documentation and migration ledger.

## Progress

- [x] DOC1 — Spec-family shells and provisional authority map
- [x] DOC2 — DAHN and contract authority
- [x] DOC3 — Path Inspector, Space Navigator, and launch separation
- [x] DOC4 — Holon Inspector and Collection realization
- [ ] DOC5 — Implementation-plan reconciliation
- [ ] DOC6 — Navigation, diagrams, and acceptance verification

## DOC1 completion evidence — 2026-09-30

- Created the [family index](visualizers/index.md), four VisualizerKind frames,
  and three concrete Visualizer design frames in the accepted kind hierarchy.
- Created the [migration ledger](dahn-docs-refactor-ledger.md), recording baseline
  commit/content hashes, all 1,024 source headings across ten documents,
  provisional destinations, slot framing, and eight reconciliation conflicts.
  Heading coverage is not statement-level migration completion.
- Updated the document role manifest, Core and Space Navigator indexes, and
  Core MkDocs navigation. No detailed normative content was extracted in DOC1.
- Verified new document relative links and generated family navigation/pages.
  `git diff --check` and the strict Core MkDocs build passed. Build output was
  directed to `/tmp/map-docs-56-doc1`.

## Architecture delivery guidance retained for DOC5

The following material moved from architecture §§67–70. It is planning source
material for DOC5 reconciliation, not a new runtime schedule or a claim of
delivery. Historical names and scope assumptions require review against the
current kind and selection contracts.

### 67. Space Navigator as an Architectural Proof

The Space Navigator should prove the DAHN architecture through a constrained initial implementation.

The first implementation does not need the complete future ecosystem.

It should, however, preserve the intended boundaries around:

- Rust-side visualizer selection;
- Visualizer Holon and implementation-reference runtime resolution;
- generic fallback visualizers;
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
        property/
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

#### 69.5 Dancer Top-Level Visualizer Tests

Verify:

- visualizer occurrence management;
- layout allocation;
- navigation state;
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

## DOC2 completion evidence — 2026-09-30

- Moved architecture to [DAHN Architecture](dahn-arch.md), preserving legacy
  section navigation at the old path. Shared mechanisms delegate to the DAHN
  design; architecture delivery/test guidance moved to the planning source notes.
- Reconciled owner-local slots, actual subject binding, agent-relative usage,
  Rust-authorized agent choice, implementation materialization, and semantic
  versus artifact identity. Retired the intervening Property selector.
- Moved shared composition rules from Space Navigator grammar §§1.5–1.9 to
  DAHN §§29–31, retaining link-based delegation at the source headings.
- Established all seven existing kind specifications as normative for their
  shared semantic boundaries, without adding directories. Collection covers
  homogeneous Holon and value collections; concrete table behavior remains local.
- Reviewed every DAHN invariant and recorded the disposition in the ledger.
  Spatial-axis rules retain reference identities but are scoped to Path Inspector.
- Concrete behavior extraction, diagram reconciliation, and delivery-plan
  reconciliation remain DOC3–DOC6 work; no runtime delivery status changed.
- Validation passed: strict Core MkDocs build, 3,732 rendered local links and
  fragment targets across changed pages, continuous DAHN Sections 1–57,
  preservation of all 23 invariant identifiers, removal of the Property selector,
  and `git diff --check`. Build output is `/tmp/map-docs-56-doc2`; no generated
  site files are included in the changes.


## DOC3 completion evidence — 2026-10-01

- Path Inspector design and interaction grammar now reside together under
  `visualizers/structure/rooted-navigation/path-inspector/`. The old grammar
  page preserves heading anchors and delegates to the canonical document.
- Space Navigator retains direct roles, local HolonSpace binding, new-context
  coordination, and transaction-level interactions. Its former concrete sections
  are reference stubs, preserving links while transferring authority.
- DAHN launch narrative, readiness/handoff, accessibility, and image provenance
  now reside in `dahn-launch-experience-design-spec.md`.
- To complete the Dancer boundary, Space Navigator's Holon Inspector and Table
  presentation was relocated in this slice. Path Inspector's private child
  responsive/PropertyMap extent paragraphs moved to Holon Inspector. DOC4 still
  owns detailed reconciliation with DAHN and separation of Collection-kind
  promises from table realization; these relocations do not mark DOC4 complete.
- Substitution review: a conforming RootedNavigation implementation using a
  sidebar inspector and vertical navigation can fill the Dancer role without
  supplying Path Inspector's two-axis Node protocol. That protocol belongs to
  Path Inspector's own Node slot. Path Inspector accepts a compatible Holon root
  independently of Space Navigator's initial local HolonSpace binding.
- Existing topology productions, close/re-root semantics, surface/view separation,
  and discrete extent protocol are preserved. Superseded open questions and
  authority transfers are recorded in the migration ledger. F1 remains deferred.
- Validation: strict Core MkDocs build, rendered local-link/anchor verification,
  and whitespace checks. No runtime code or delivery status changed.


## DOC4 completion evidence — 2026-10-01

- Starts from checkpoint `6af62f0` (DOC2–DOC3). DAHN §§16–18, 24–26, 32,
  and 53 now delegate to Holon Inspector, preserving source heading anchors.
- Holon Inspector owns its six direct slots, effective descriptor projection,
  per-action selection, lazy collection activation, child allocation, responsive
  retention/suppression, content-extent negotiation, and Book rendering example.
- Child inventories identify semantic subjects, context, and DAHN selection
  boundaries. Exact accepted types for title/action-bar/rail/tab-index slots and
  exact Table value-cell slot declarations remain open; no schema is invented.
- Collection kind owns common provenance and mutation semantics. Table owns
  rows/columns, typed sorting, Sequence metadata, default ordering, filtering,
  occurrence-local restoration, selection, and editing controls. Its external
  placement belongs to the parent; Holon Inspector owns below-tab placement.
- Detailed table sorting and restoration text is unchanged. Private partial-width,
  partial-height and PropertyMap measurement rules remain intact. Former Property
  intermediary wording is corrected to PropertyMap plus Value under D3.
- F1 remains deferred. No additional kind directory or runtime vocabulary added.
- Validation: strict Core documentation build, local-link/anchor checks, source
  preservation comparison, and whitespace check. DOC4 changes remain uncommitted.


### DOC4 review addendum: bounded Maximize/Restore

Reconciled Issue 770's intended behavior into DAHN §30, Holon Inspector local
region Maximize/Restore, and Table participation. Concrete controls remain open;
no separate Table-local maximize feature or implementation completion is claimed.
Independent restore state and current-grant restoration are explicit. DOC5 should
reference these design homes when reconciling PR 18.c.
