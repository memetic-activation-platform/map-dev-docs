# DAHN Compositional Authority Documentation Refactor Plan

> **Status:** In progress — DOC1 complete; DOC2–DOC6 pending. Detailed extraction has not started.
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

## Findings from the current documents

- [DAHN Design Specification](dahn-design-spec.md) Section 4 provides the new
  conceptual anchor. Later sections still prescribe Holon Inspector slots,
  projection, navigation axes, and concrete compression. INV-6 assumes slots
  are Visualizer-local; INV-13–15 mix semantic cardinality with spatial grammar.
- [Space Navigator Design Specification](../space-navigator/space-navigator-design-spec.md)
  v0.7 contains Dancer orchestration, launch experience, Node internals, table
  sorting, editing, and navigation geometry in one normative document.
- [Space Navigator Architecture](../space-navigator/space-navigator-arch.md)
  v0.4 explicitly claims reusable DAHN architectural authority despite its
  application-specific location. Its introduction still attributes navigation
  geometry to the Space Navigator interaction grammar.
- [Space Navigator Interaction Grammar](../space-navigator/space-navigator-interaction-grammar.md)
  v0.3 and [Path Inspector Grammar](../space-navigator/path-inspector-grammar.md)
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
exist after DOC1; architecture, launch, and grammar moves remain pending. Keep current DAHN and Space Navigator design
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

Populate the Holon Inspector and Table Collection spec shells from the mapped material.
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
- [ ] DOC2 — DAHN and contract authority
- [ ] DOC3 — Path Inspector, Space Navigator, and launch separation
- [ ] DOC4 — Holon Inspector and Collection realization
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
