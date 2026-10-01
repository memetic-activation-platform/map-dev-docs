# DAHN Documentation Refactor Migration Ledger

## Baseline and status

DOC1 recorded provisional destinations. DOC2 reconciled shared authority; DOC3 transfers are recorded below.
The initial heading inventory remains historical; the transfer tables supersede
its pending status only for the explicitly named source groups. Before deleting source text, split mixed rows,
record identifiable statements and final destination headings, then mark checked
or explicitly retired with a reason. Unmoved concrete sources retain detailed authority within their scoped owners.

Baseline commit: `fb34f2acfd60b3c00b48eee6b31c29696bb04cfc`.
Working-tree baseline includes the added Design Concept and composition diagram,
and the existing Path Inspector grammar modifications. SHA-256 hashes below
identify source contents at DOC1 inventory time, before index updates.

## Decisions and unresolved conflicts

| ID | Decision or conflict | Owner / next step |
| --- | --- | --- |
| D1 | Accepted: directories follow VisualizerKind, not VisualizerSlot. Slots remain local to their composition owner. | Applied in DOC1 frames. |
| D2 | Accepted: RootedNavigation, Graph, and Geospatial are peer Structure specializations. | Structure and RootedNavigation frames. |
| C1 | DAHN §§11–11.2 and INV-6 restrict slot ownership or represent VisualizerUsage as fulfillment, contrary to Design Concept. | Resolved in DOC2: DAHN §11 defines Dancer/Visualizer ownership and agent-relative usage; exact Dancer schema remains open. |
| C2 | Central Rust selection must coexist with conforming agent overrides. | Resolved in DOC2: DAHN §14.6 validates explicit choices through Rust under ordinary conformance and error policy. |
| C3 | Visualizer Holon identity versus executable content identity is ambiguous in some sections. | Resolved in DOC2: architecture §9.2 and DAHN §§37–40 / INV-18 distinguish semantic, implementation, artifact, occurrence, and usage identities. |
| C4 | Path Inspector includes PropertyMap sub-slot extent behavior. | Moved in DOC3: outer participation remains in grammar §4.4.1; private responsive realization and PropertyMap content extent now reside in Holon Inspector. DOC4 reviews remaining DAHN overlap. |
| C5 | Collection kind table says multiple Holons; other sections explicitly support value collections. | Resolved in DOC2: Collection kind admits homogeneous Holon and value collections, preserving the explicit array/table source contracts. |
| C6 | Space Navigator calls Table an initial selector fallback while newer policy requires compatible selection or an explicit error. | Shared policy resolved in DOC2: Space Navigator §18.2 now treats Table as an ordinary candidate; concrete extraction remains DOC4. |
| C7 | Current table sorting, progressive population, destination-first transitions and collection switching must survive. | Moved in DOC3: table sorting to Table Collection; progressive child population/switching to Holon Inspector; destination-first transitions to Path Inspector. DOC4 reconciles remaining overlap. |
| C8 | Six Holon Inspector roles have unevenly specified exact contracts; Table child slot identities remain incomplete. | DOC4: extract existing commitments, record unresolved details, do not invent APIs. |

## Deferred design dependency — 2026-10-01

**F1 — Holonic participation contracts and occurrence invocation:** deferred by
the user until documentation stabilization. The
[design parking record](dahn-docs-refactor-impl-plan.md#deferred-design-participation-contracts-and-occurrence-invocation)
preserves reusable configured contracts, existing invocation-vocabulary questions,
agent-relative Usage versus occurrence state, and possible schema/runtime impact.
These proposals do not authorize new normative schema or dispatch rules.

F1 does not block DOC3–DOC6. Preserve and relocate existing participation behavior,
flag unresolved representation assumptions, and carry F1 into the DOC5 handoff.
Revisit after DOC6 before grounding schema/runtime implementation work.

## Additional accepted decisions after initial DOC1 framing

| ID | Decision | Reconciliation |
| --- | --- | --- |
| D3 | Property is not a VisualizerKind or independently selected presentation layer. | DOC2: retire the intervening Property selection layer in DAHN §§10, 20–23, selector signatures, examples, and affected invariants; preserve property semantic metadata. |
| D4 | PropertyMap owns set-level layout, visibility, personalization, and label/value pairing. | Framed in `visualizers/property-map/kind-spec.md`; DOC4 reconciles embedded concrete behavior. |
| D5 | PropertyName can be presented by a selected String Visualizer alongside a separately selected ValueType-specific value Visualizer. | Label and value have distinct subjects, roles, and permitted interactions; exact slot names remain implementation-owned. |
| D6 | String specializes Value; ValueType and VisualizerKind remain distinct concepts. | Framed in `visualizers/value/` and `value/string/`; additional specializations require established semantic boundaries. |

The initial source inventory below is retained as a baseline. Its references to
Property presentation require reassessment under D3, not preservation of the
retired layer. DOC2 transfers and deliberate retirements are recorded below; the baseline
inventory remains the audit trail for later concrete extraction.

## Slot framing inventory

| Owner | Role | Subject binding | Required boundary / review |
| --- | --- | --- | --- |
| Space Navigator | RootedNavigation | Local HolonSpace | RootedNavigation requirements; DAHN selection; no required Path Inspector internals. |
| Path Inspector | Node participation | Holon represented by occurrence | Owner-specific extent participation; selected Node owns private composition. |
| Path Inspector | Collection provenance, not a direct slot | Source collection and selected member | DOC3: Holon Inspector owns CollectionViewerSlot; Path Inspector coordinates traversal intents without claiming that child. |
| Holon Inspector | NodeTitleBarSlot | Holon identity/title context | Exact accepted types remain source-review work. |
| Holon Inspector | ActionBarSlot | Applicable executable affordances | Separate bar composition and individual Action selection. |
| Holon Inspector | VerticalRailSlot | Singular navigational affordances | Internal rail presentation; semantic navigation crosses parent boundary. |
| Holon Inspector | PropertyMapSlot | Bound Holon's property facet | PropertyMap child fulfillment. |
| Holon Inspector | CollectionTabsSlot | Collection-shaped affordances | Affordance index; distinguish it from active collection data. |
| Holon Inspector | CollectionViewerSlot | Selected active collection | Collection child fulfillment. |
| Table Collection | Value cell roles where established | Projected row property/value | Exact slot names/contracts remain unresolved. |

Every actual slot is a subject-binding, substitutability, and DAHN selection
boundary. This table seeds the inventory; DOC2–DOC4 must expand it to cover all
slots found in the source, including PropertyMap label and value roles. Old nested Property renderer roles
are candidates for deliberate retirement under D3, not new kind specifications.

## DOC3 transfer and retirement evidence

DOC3 follows the user-approved DOC2 working tree. The initial inventory below is
retained unchanged for provenance; this table records the completed transfers.
Detailed Holon Inspector / Collection reconciliation remains DOC4.

| Source statements / group | Disposition and canonical home | Verification |
| --- | --- | --- |
| Path Inspector grammar §§1–15 | Moved to `visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md`; topology productions, independent axis states, ordered positive extents, stable full extents, discrete compression, surface growth, viewport rules, branch-close compaction, and source-preserving re-root retained. Old path preserves heading links. | Checked against pre-DOC3 grammar diff |
| Grammar §4.4.1 private partial-height / partial-width behavior and PropertyMap content measurement | Moved verbatim to Holon Inspector “Responsive realization under Path Inspector” and “PropertyMap sub-slot content extent”; grammar retains outer participation obligations and delegates private behavior. | Checked |
| Grammar opening hierarchy and §§11–13 composition references | Shared authority now links DAHN; Space Navigator composition is an example. Path Inspector design is adjacent authority for concrete interactions. | Checked |
| Grammar §14 question whether compression is discrete/continuous/hybrid | Retired as an unresolved current choice: §4.4.1 already requires discrete states. Future alternatives remain open. | Explicit retirement |
| Space Navigator §1.8 and subsections | Launch purpose, five-scene sequence, shell boundary, independent readiness timeline, Skip/holding state, reduced motion/accessibility, observational imagery and complete provenance moved to DAHN Launch Experience specification. Launcher retains home-Dancer selection. | Checked |
| Space Navigator §§1–4 and §54 | Narrowed to direct experience roles, subject binding, context preservation, allocation, selection, and host coordination. Removed universal axis/presentation claims; concrete rules moved below. §3 retains old anchor. | Checked |
| Space Navigator §§6, 26, 28, 29, 35 | Path Inspector “Active Traversal Frontier”, “Applying the Interaction Grammar”, “Compression and Editing”, “Loading States”, and “Editing While Navigating”. Focus/allocation boundaries and generic root documented alongside direct Node role. | Checked |
| DAHN §§19, 28 | Spatial realization delegates Path Inspector “Structural cardinality and traversal” / “Applying the Interaction Grammar”. Descriptor cardinality remains semantic input. | Checked |
| Space Navigator §§7–17, 25, 27, 30–31, 36–39, 48–49 | Moved to Holon Inspector concrete presentation: six regions, property/array presentation, singular rail and collection tabs, cardinality/Dance-result mapping, focus realization, retrieval, editing, Create/Clone/Delete, personalization. Selection delegates DAHN; outer focus delegates Path Inspector. | Relocation checked; remaining DAHN reconciliation DOC4 |
| Space Navigator §§18–23 | Moved to Table Collection: collection subjects and ordinary candidate selection, geometry, rows/columns/header, column sorting and restoration, Sequence column, default row ordering, arrays/relationships/Dance-result editability. | Relocation checked; kind/concrete reconciliation DOC4 |
| Space Navigator §50.3–7, .19 | Navigation and compression scenarios moved to Path Inspector. | Checked |
| Space Navigator §50.1–2, .8–16 | Inspection, collection activation, editing and Create/Clone/Delete scenarios moved to Holon Inspector. §50.17–18 transaction scenarios remain with Dancer. | Checked |
| Space Navigator §51.1–4, .8–9 | Moved to Path Inspector. Old sibling retention, overflow and branch-close alternatives are superseded by established grammar §§2.4, 2.9, 3.3–3.6, 4.6–4.7 and 7.4. Presentation controls/thresholds remain open. | Checked; explicit retirement of conflicting alternatives |
| Space Navigator §51.5–7, .11–13 | Moved unresolved child presentation questions to Holon Inspector. §51.10 transaction scope remains with Dancer. | Checked |
| Space Navigator §53.4–7, .9–10 | Delegate to existing Path Inspector grammar invariants, avoiding duplicate rules. | Checked |
| Space Navigator §53.8, .11, .17 | Presentation invariants moved to Holon Inspector. Remaining transaction/semantic invariants retain their shared-authority context in Space Navigator. | Checked |
| Index, concept, manifest, navigation and incoming links | Point to canonical family documents; concept scopes two-axis exploration to initial Path Inspector. Property intermediary removed from concept under D3. | Build and rendered-link verification |

No runtime vocabulary, contract-type schema, occurrence persistence rules, or
new kind directories were introduced. F1 remains deferred. Source section numbers
in the baseline inventory are historical identifiers, not current destination
heading numbers.

## DOC2 transfer and retirement evidence

DOC2 starts from checkpoint `443dc3b`; the earlier hashes remain the DOC1 source
inventory baseline.

Destinations below identify canonical sections, not another copy of their rules.
“Checked” means the named shared statements were retained, moved, or deliberately
retired; it does not mark unrelated concrete material complete.

| Source statements / group | Disposition and exact home | Verification |
| --- | --- | --- |
| Architecture purpose and §1 claim DAHN-wide authority under a Space Navigator document | Move/rewrite to `hx/dahn-arch.md` Purpose and §1; retire universal parent-spec hierarchy in favor of concern-local authority. | Checked |
| Architecture §§2–14: deployment, Rust/TS responsibilities, state, IPC, Holon/type/implementation identity, Commons/discovery, schema applicability/capabilities/version domains | Retained at matching sections in `hx/dahn-arch.md`; §9 separates usage from occurrence; §9.1 replaces Property with PropertyMap; §10 generic candidates obey ordinary selection policy. | Checked |
| Architecture §§15–16: centralized semantic selection, preferences, context, trend/maturity/explore-exploit inputs | Consolidated in DAHN §§12–14, especially §14.6. Old architecture headings delegate. Future randomness/ranking is not introduced into current ambiguity policy. | Checked |
| Architecture §§17–21: explore/exploit, personal/collective adaptation, immediate gestures, adaptive presentation context | Retained in `hx/dahn-arch.md` at matching headings; these own adaptive responsibility, not a second selector algorithm. | Checked |
| Architecture §22: selected semantic reference, selected type, alternatives, capability context, optional diagnostics; no substitution of implementation identity | DAHN §14.2 result contract. | Checked |
| Architecture §22.1 and §§23–25: Materialize Dance, typed code/module payload, local backend, cache/loader/runtime responsibilities, trust and compatibility concerns | DAHN §§33–34, §§37–42 and §40.1; cache lookup may use semantic identity but must resolve an authorized implementation/version and verified artifact. Dependency isolation/acquisition retained in §34. | Checked |
| Architecture §§26–31: recursive children, parent placement, layout budget fields, declared extents/capabilities, selection versus allocation, responsive nesting | DAHN §§11, 14.5, 15, 29–31; obsolete Property-mediated illustration retired under D3. Layout field/capability lists retained in §30.1; batching and reuse of authorized selection remain available in §14.5. | Checked |
| Architecture §§32–33: token dependencies, external themes, semantic token consumption, theme metrics versus semantic roles | DAHN §45 and §45.5; illustrative token names omitted without dropping any required token role (they were examples). | Checked |
| Architecture §§34–44: action scopes, occurrence identity, events, progressive retrieval, effective descriptors | Retained at matching sections in `hx/dahn-arch.md`; concrete application extraction remains DOC3–DOC4. | Checked for relocation |
| Architecture §§45–46: Property extension layer, typed value behavior, Collection sources, concrete table and graph/map examples | Property intermediary deliberately retired under D3; PropertyMap/Value kinds preserve inspection/edit/validation-feedback/compact capabilities; Collection kind preserves array/relationship/Dance sources; topology classification delegates Structure. Architecture links these homes. | Checked |
| Architecture §§47–66: semantic editing, transaction boundaries, SDK adapter, asynchrony, errors and refresh | Retained at matching sections in `hx/dahn-arch.md`; error recovery explicitly uses ordinary Rust selection. Existing MAP semantics are not redefined. | Checked for relocation |
| Architecture §§67–70: delivery proof, suggested module trees, test lists, initial deferrals | Moved intact to plan “Architecture delivery guidance retained for DOC5”; historical Property names are recorded as source assumptions for reconciliation, not current spec. | Checked |
| Architecture §§71–72: invariants and summary | Retained as architectural responsibility summaries; shared mechanisms delegate DAHN design; generic candidate failure is explicit; spatial grammar belongs to selected Visualizer. | Checked |
| Space Navigator grammar §§1.5–1.6: Window Manager, Canvas grant, nested surfaces, layout/view distinction, pan/zoom, minimum extent, Zoom to Fit and actual-size semantics | DAHN §§29.1–29.2. Path Inspector minimum-extent link is illustrative. Source headings delegate. | Checked |
| Space Navigator grammar §§1.7–1.8: local/Canvas/window maximize authorities, bounded allocation, propagation, participation dimensions | DAHN §30 and §30.1; no new finalized slot schema introduced. Source headings delegate. | Checked |
| Space Navigator grammar §1.9: independent state dimensions, state survival, context destruction versus semantic disposal | DAHN §31.1. Closing a branch is generalized to closing under the owner's grammar; it never abandons external semantic state. | Checked |
| DAHN §6: Rust semantic/selection/verification state; TS ephemeral presentation state | Canonical architecture §§5–7, with DAHN §6 delegating. Tabs/hover/DOM/local state explicitly retained in architecture §7.2. | Checked |
| DAHN §§10–14: kind registry, slots, usage indirection, subjects, selector signatures and descriptor walk | Rewritten in place; kind membership is insufficient for slot conformance; actual subject binding preserved; retired Property selector and denial of Dancer slots. HasSlot, accepted types, applicability, TKD boundary and explicit errors preserved. | Checked |
| DAHN §§20–23: PropertyMap, PropertySlot/PropertyVisualizer, ValueViewerSlot chain | Property intermediary retired under D3; direct label/value composition lives in PropertyMap and Value kind specs, with in-place DAHN delegation. DefaultPropertyMap identity remains; no mandatory new slot names. | Checked |
| DAHN §27 and §27.1: homogeneous collections, semantic topology, root-anchor independence, alternative realizations | Collection, Structure, and RootedNavigation kind specs; DAHN retains summary and links. RootedNavigation remains a peer of Graph/Geospatial. | Checked |
| DAHN §29: Space Navigator roles/OwnedBy context/future AgentSpace illustration | Dancer-specific coupling and future AgentSpace example preserved in architecture §10.1 pending DOC3; DAHN §29 now owns host authority. | Checked |
| DAHN §53: Book example repeatedly selecting PropertyMap per scalar | Rewritten as one illustrative set-level PropertyMap with separate label/value children; Book properties, relationships, Dances and projection outcomes retained. | Checked |
| Space Navigator §11.2, §18.2 and trailing slot alignment | Replace stale Property chain and hard-coded Table fallback with canonical DAHN/kind references. Table behavior and sorting remain untouched for DOC4. | Checked |

## DAHN invariant review

| Invariant | Disposition / authority | Verification |
| --- | --- | --- |
| INV-1 | Retain SDK boundary; DAHN §5, architecture §8. | Checked |
| INV-2 | Retain Rust semantic authority; architecture §§5–7. | Checked |
| INV-3 | Retain semantic descriptor inputs; DAHN §§7–8. | Checked |
| INV-4 | Retain selected Visualizer grammar authority; DAHN §§4, 11, 15. | Checked |
| INV-5 | Retain kind semantic classification; kind specs and DAHN §10. | Checked |
| INV-6 | Rewrite Visualizer-local to owner-local (Dancer or Visualizer); DAHN §11. | Checked |
| INV-7 | Retain slot/selector separation; DAHN §14. | Checked |
| INV-8 | Retain recursive centralized selection; DAHN §14.5. | Checked |
| INV-9 | Retain Rust final authority; DAHN §14.3 and §14.6 include agent choice. | Checked |
| INV-10 | Retain subject/context-rich selection; DAHN §§12–14. | Checked |
| INV-11 | Clarify PropertyMap/Value separation and direct composition; Property intermediary retired. | Checked |
| INV-12 | Retain Action selection boundary; concrete button/bar choices stay local. | Checked |
| INV-13 | Rewrite as semantic cardinality versus runtime population; remove universal spatial implication. | Checked |
| INV-14 | Remove DAHN-wide force; preserve identifier linking Path Inspector §10; concrete consolidation DOC3. | Checked |
| INV-15 | Remove DAHN-wide force; preserve identifier linking Path Inspector §10; concrete consolidation DOC3. | Checked |
| INV-16 | Retain allocation normally preserving selected identity; DAHN §31. | Checked |
| INV-17 | Retain parent allocation authority; DAHN §30. | Checked |
| INV-18 | Distinguish semantic Holon identity from content-addressed artifact identity; DAHN §§37–40. | Checked |
| INV-19 | Retain verification before execution; materialization bootstrap is no exception. | Checked |
| INV-20 | Retain stewardship/transport distinction; DAHN §39. | Checked |
| INV-21 | Retain provenance versus runtime safety; DAHN §34. | Checked |
| INV-22 | Retain origin-independent executable delivery; DAHN §§37–41. | Checked |
| INV-23 | Retain bootstrap as ordinary selection policy; DAHN §14.4 and §44. | Checked |

## Source heading inventory

Disposition codes: **R** retain/reconcile; **M** move; **S** split by statement.
Owner abbreviations: DAHN = shared foundation; SN = Space Navigator; PI = Path
Inspector; HI = Holon Inspector; TC = Table Collection. Component destinations
are the paths in the [implementation plan](dahn-docs-refactor-impl-plan.md) and
[family index](visualizers/index.md). All headings are inventoried, including
historical change logs; historical text is not automatically normative.

### hx/dahn-design-spec.md

Baseline SHA-256: `237fa588d264e0a6d1e90bdec0c9888ee182c552cdbe770444acd225a71130f6`.

| Source heading | Provisional owner / destination | Disposition | Verification |
| --- | --- | --- | --- |
| DAHN Design Specification v2.3 | DAHN / architecture and design | R | Pending |
| Status | DAHN / architecture and design | R | Pending |
| Change Log | DAHN / architecture and design | R | Pending |
| v2.3 | DAHN / architecture and design | R | Pending |
| v2.2 | DAHN / architecture and design | R | Pending |
| v2.1 | DAHN / architecture and design | R | Pending |
| v2.0 | DAHN / architecture and design | R | Pending |
| v1.4 | DAHN / architecture and design | R | Pending |
| v1.3 | DAHN / architecture and design | R | Pending |
| 1. Purpose | DAHN / architecture and design | R | Pending |
| 2. Relationship to Adjacent Specifications | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 3. Core Architectural Principles | DAHN / architecture and design | R | Pending |
| 3.1 MAP semantics remain authoritative | DAHN / architecture and design | R | Pending |
| 3.2 Holons describe affordances, not UI | DAHN / architecture and design | R | Pending |
| 3.3 Visualizers define presentation grammar | DAHN / architecture and design | R | Pending |
| 3.4 Visualizer selection is centralized | DAHN / architecture and design | R | Pending |
| 3.5 Visualizer composition and selection are separate | DAHN / architecture and design | R | Pending |
| 3.6 Navigation topology and Visualizer composition are separate | DAHN / architecture and design | R | Pending |
| 4. Design Concept | DAHN / architecture and design | R | Pending |
| 4.1 Experience Composition and Data Coupling | DAHN / architecture and design | R | Pending |
| 4.2 VisualizerSlots as Composition Boundaries | DAHN / architecture and design | R | Pending |
| 4.3 Contracts and Visualizer Fulfillment | DAHN / architecture and design | R | Pending |
| 4.4 Subjects and MAP Data | DAHN / architecture and design | R | Pending |
| 4.5 Selector Functions | DAHN / architecture and design | R | Pending |
| 4.6 Agent Agency and Personalization | DAHN / architecture and design | R | Pending |
| 4.7 Recursive Composition and Distributed Design Authority | DAHN / architecture and design | R | Pending |
| 5. Public MAP SDK Boundary | DAHN / architecture and design | R | Pending |
| 6. State Ownership | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 6.1 Rust-owned state | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 6.2 TypeScript-owned state | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 7. Active Holon Model | DAHN / architecture and design | R | Pending |
| 8. Descriptor Requirements for DAHN | DAHN / architecture and design | R | Pending |
| 8.1 Property Descriptor | DAHN / architecture and design | R | Pending |
| 8.2 Relationship Descriptor | DAHN / architecture and design | R | Pending |
| 8.3 Dance Descriptor | DAHN / architecture and design | R | Pending |
| 9. Visualizer Model | DAHN / architecture and design | R | Pending |
| 9.1 AbstractVisualizer | DAHN / architecture and design | R | Pending |
| 10. VisualizerKind | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 11. VisualizerSlot | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 11.1 VisualizerUsage | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 11.2 Dancer Roles and Visualizer Slots | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 12. Visualization Requests | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 13. Visualization Subject | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 14. DAHN Visualizer Selection Service | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 14.1 Responsibility | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 14.2 Selector signatures | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 14.2.1 Slot-directed descriptor selection | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 14.3 Rust ownership | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 14.4 Initial deterministic bootstrap policy | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 14.5 Recursive selection | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 15. Visualizer Composition | HI / concrete design; DAHN or kind spec for shared promises | S | Pending |
| 16. HolonInspectorVisualizer | HI / concrete design; DAHN or kind spec for shared promises | S | Pending |
| 17. HolonInspectorVisualizer Slots | HI / concrete design; DAHN or kind spec for shared promises | S | Pending |
| 18. HolonInspectorVisualizer Descriptor Projection | HI / concrete design; DAHN or kind spec for shared promises | S | Pending |
| 18.1 Scalar Properties | HI / concrete design; DAHN or kind spec for shared promises | S | Pending |
| 18.2 ValueArray Properties | HI / concrete design; DAHN or kind spec for shared promises | S | Pending |
| 18.3 Singular Relationships | HI / concrete design; DAHN or kind spec for shared promises | S | Pending |
| 18.4 Plural Relationships | HI / concrete design; DAHN or kind spec for shared promises | S | Pending |
| 18.5 Singular Navigational Dances | HI / concrete design; DAHN or kind spec for shared promises | S | Pending |
| 18.6 Plural Navigational Dances | HI / concrete design; DAHN or kind spec for shared promises | S | Pending |
| 18.7 Other Dances | HI / concrete design; DAHN or kind spec for shared promises | S | Pending |
| 19. Structural Cardinality Invariant | PI / grammar; DAHN for shared allocation/cardinality | S | Pending |
| 20. PropertyMapSlot | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 21. PropertyMapVisualizer | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 22. PropertySlot and ValueViewerSlot | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 23. ValueVisualizer | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 24. Action Bar and ActionVisualizer | HI / concrete design; DAHN or kind spec for shared promises | S | Pending |
| 25. Collection Tabs | HI / concrete design; DAHN or kind spec for shared promises | S | Pending |
| 26. Collection Viewer | HI / concrete design; DAHN or kind spec for shared promises | S | Pending |
| 27. Collection and Structure Visualizers | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 27.1 Rooted Navigation Visualizer | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 28. Node Navigation Semantics | PI / grammar; DAHN for shared allocation/cardinality | S | Pending |
| Singular navigation | PI / grammar; DAHN for shared allocation/cardinality | S | Pending |
| Plural navigation | PI / grammar; DAHN for shared allocation/cardinality | S | Pending |
| 29. Canvas, Dancer, and Rooted-Navigation Responsibilities | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 30. Parent-Owned Allocation | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 31. Compression and Visualizer Identity | PI / grammar; DAHN for shared allocation/cardinality | S | Pending |
| 32. HolonInspectorVisualizer Extent Realization | HI / concrete design; DAHN or kind spec for shared promises | S | Pending |
| 33. Visualizer Runtime Contract | DAHN / architecture and design | R | Pending |
| 34. Visualizer Runtime Security Boundary | DAHN / architecture and design | R | Pending |
| 35. Visualizer Definition and Stewardship | DAHN / architecture and design | R | Pending |
| 36. Visualizer Commons | DAHN / architecture and design | R | Pending |
| 37. Visualizer Implementation Artifacts | DAHN / architecture and design | R | Pending |
| 38. Content-Addressed Identity | DAHN / architecture and design | R | Pending |
| 39. Distribution Does Not Imply Authority | DAHN / architecture and design | R | Pending |
| 40. Visualizer Artifact Loading | DAHN / architecture and design | R | Pending |
| 41. DAHN-Controlled Module Materialization | DAHN / architecture and design | R | Pending |
| 42. Visualizer Protocol Compatibility | DAHN / architecture and design | R | Pending |
| 43. Relationship to Dynamic Dance Implementations | DAHN / architecture and design | R | Pending |
| 44. Initial Bootstrap Visualizers | DAHN / architecture and design | R | Pending |
| 45. Design Tokens, Meta Design Systems, and Theme Ownership | DAHN / architecture and design | R | Pending |
| 45.1 Design Tokens | DAHN / architecture and design | R | Pending |
| 45.2 Meta Design System Contract | DAHN / architecture and design | R | Pending |
| 45.3 Themes and Complete Assignment | DAHN / architecture and design | R | Pending |
| 45.4 Theme Selection and Runtime Projection | DAHN / architecture and design | R | Pending |
| 46. DAHN Runtime Orchestration | DAHN / architecture and design | R | Pending |
| 47. Holon Access | DAHN / architecture and design | R | Pending |
| 48. Lazy Semantic Expansion | DAHN / architecture and design | R | Pending |
| 49. Commands and Dances | DAHN / architecture and design | R | Pending |
| 50. Editing and Staged State | DAHN / architecture and design | R | Pending |
| 51. Interaction Reporting and Future Selection-Service Learning | DAHN / architecture and design | R | Pending |
| 52. Architectural Invariants | DAHN / architecture and design | R | Pending |
| INV-1 — Public SDK boundary | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| INV-2 — Rust model authority | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| INV-3 — Active Holons describe semantics, not UI | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| INV-4 — Visualizers own presentation grammar | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| INV-5 — VisualizerKind is DAHN-wide | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| INV-6 — Slots are Visualizer-local | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| INV-7 — Slots do not choose implementations | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| INV-8 — Selection is recursive and centralized | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| INV-9 — Selector authority resides in Rust | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| INV-10 — Selection is richer than category lookup | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| INV-11 — Properties and Value visualization are distinct | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| INV-12 — Actions are independently visualizable | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| INV-13 — Structural cardinality determines navigation shape | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| INV-14 — Singular navigation is horizontal | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| INV-15 — Plural Holon navigation is collection-mediated vertical | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| INV-16 — Allocation does not ordinarily cause reselection | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| INV-17 — Parents own external allocation | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| INV-18 — Visualizer identity is independent of artifact location | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| INV-19 — Verification precedes execution | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| INV-20 — Distribution does not imply authority | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| INV-21 — Provenance does not imply safety | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| INV-22 — Visualizer loading is origin-agnostic | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| INV-23 — Bootstrap selection is policy, not ontology | DAHN design / kind contracts / architecture as mapped above | R/S | Checked — DOC2 |
| 53. Initial Holon Inspector Rendering Example | HI / concrete design; DAHN or kind spec for shared promises | S | Pending |
| 54. Implementation Posture | DAHN / design or implementation plan by statement | S | Pending |
| 55. Near-Term Design Priorities | DAHN / design or implementation plan by statement | S | Pending |
| 56. Superseded v1.4 Concepts | DAHN / design or implementation plan by statement | S | Pending |
| TS-owned final Visualizer resolution | DAHN / design or implementation plan by statement | S | Pending |
| SelectorOutput as a Canvas mount plan | DAHN / design or implementation plan by statement | S | Pending |
| One default Node Visualizer plus one default Action Menu as the selector model | DAHN / design or implementation plan by statement | S | Pending |
| Property visualization directly driven by ValueType | DAHN / design or implementation plan by statement | S | Pending |
| Generic preconstructed `AffordanceNode[]` as the Active Holon presentation model | DAHN / design or implementation plan by statement | S | Pending |
| Minimal one-region scrolling Canvas as the DAHN Canvas model | DAHN / design or implementation plan by statement | S | Pending |
| 57. Result | DAHN / design or implementation plan by statement | S | Pending |

### space-navigator/space-navigator-design-spec.md

Baseline SHA-256: `5133c953ba553a90658bea79f33644d8fbc0dbbdc8d7d6a2b3135b1eb7749980`.

| Source heading | Provisional owner / destination | Disposition | Verification |
| --- | --- | --- | --- |
| DAHN Space Navigator Design Specification v0.7 | SN / Dancer design | S | Pending |
| Status | SN / Dancer design | S | Pending |
| Change Log | SN / Dancer design | S | Pending |
| Purpose | SN / Dancer design | S | Pending |
| 1. Design Goals | SN / Dancer design | S | Pending |
| 1.1 Descriptor-Driven | SN / Dancer design | S | Pending |
| 1.2 Generic | SN / Dancer design | S | Pending |
| 1.3 Shape-Oriented | SN / Dancer design | S | Pending |
| 1.4 Context-Preserving | SN / Dancer design | S | Pending |
| 1.5 Spatially Scalable | SN / Dancer design | S | Pending |
| 1.6 Unified Read and Edit Experience | SN / Dancer design | S | Pending |
| 1.7 Incrementally Implementable | SN / Dancer design | S | Pending |
| 1.8 DAHN Launch Experience | DAHN launch experience / focused spec | S | Pending |
| 1.8.1 Narrative and scenes | DAHN launch experience / focused spec | S | Pending |
| 1.8.2 Application-shell boundary | DAHN launch experience / focused spec | S | Pending |
| 1.8.3 Readiness, handoff, and control | DAHN launch experience / focused spec | S | Pending |
| 1.8.4 Observational imagery and provenance | DAHN launch experience / focused spec | S | Pending |
| 2. Core Design Principles | SN / Dancer design | S | Pending |
| 2.1 Definitions Determine Structure | SN / Dancer design | S | Pending |
| 2.2 Navigation Determines Visibility | SN / Dancer design | S | Pending |
| 2.3 Descriptors Determine Editability | SN / Dancer design | S | Pending |
| 2.4 Staged State Determines What Is Being Changed | SN / Dancer design | S | Pending |
| 2.5 Compression Hides Presentation, Not State | SN / Dancer design | S | Pending |
| 3. Core Visual Roles | SN / Dancer design | S | Pending |
| 4. Space Navigator Experience Composition | SN / Dancer design | S | Pending |
| 4.1 Responsibility | SN / Dancer design | S | Pending |
| 4.2 Experience Structure | SN / Dancer design | S | Pending |
| 5. Space Navigator Action Bar | SN / Dancer design | S | Pending |
| 5.1 Purpose | SN / Dancer design | S | Pending |
| 5.2 Transaction Actions | SN / Dancer design | S | Pending |
| 5.3 Space Navigator Actions | SN / Dancer design | S | Pending |
| 5.4 Personalization | SN / Dancer design | S | Pending |
| 5.5 Action Scope Rule | SN / Dancer design | S | Pending |
| 6. Active Traversal Frontier | PI / grammar and design; HI or TC for child presentation | S | Pending |
| 7. Node Visualizer | HI / concrete design; PI for navigation consequences | S | Pending |
| 7.1 Responsibility | HI / concrete design; PI for navigation consequences | S | Pending |
| 7.2 Selection | HI / concrete design; PI for navigation consequences | S | Pending |
| 7.3 Inputs | HI / concrete design; PI for navigation consequences | S | Pending |
| 8. Full Node Geometry | HI / concrete design; PI for navigation consequences | S | Pending |
| 9. Node Title Bar | HI / concrete design; PI for navigation consequences | S | Pending |
| 10. Node Action Bar | HI / concrete design; PI for navigation consequences | S | Pending |
| 10.1 Purpose | HI / concrete design; PI for navigation consequences | S | Pending |
| 10.2 Effective Dances | HI / concrete design; PI for navigation consequences | S | Pending |
| 10.3 Alternate Visualizers | HI / concrete design; PI for navigation consequences | S | Pending |
| 10.4 Compression | HI / concrete design; PI for navigation consequences | S | Pending |
| 11. Property Viewer Pane | HI / concrete design; PI for navigation consequences | S | Pending |
| 11.1 Purpose | HI / concrete design; PI for navigation consequences | S | Pending |
| 11.2 Property Visualizers | HI / concrete design; PI for navigation consequences | S | Pending |
| 11.3 Scalar Values | HI / concrete design; PI for navigation consequences | S | Pending |
| 11.4 Read Mode | HI / concrete design; PI for navigation consequences | S | Pending |
| 11.5 Edit Mode | HI / concrete design; PI for navigation consequences | S | Pending |
| 11.6 Property Ordering | HI / concrete design; PI for navigation consequences | S | Pending |
| 12. Array-Valued Properties | HI / concrete design; PI for navigation consequences | S | Pending |
| 13. Vertical Single-Value Tab Rail | HI / concrete design; PI for navigation consequences | S | Pending |
| 13.1 Purpose | HI / concrete design; PI for navigation consequences | S | Pending |
| 13.2 Eligible Affordances | HI / concrete design; PI for navigation consequences | S | Pending |
| 13.3 Structural Presence | HI / concrete design; PI for navigation consequences | S | Pending |
| 13.4 Activation | HI / concrete design; PI for navigation consequences | S | Pending |
| 13.5 Personalization | HI / concrete design; PI for navigation consequences | S | Pending |
| 14. Editing Single-Valued Relationships | HI / concrete design; PI for navigation consequences | S | Pending |
| 15. Horizontal Collection Tab Bar | HI / concrete design; PI for navigation consequences | S | Pending |
| 15.1 Purpose | HI / concrete design; PI for navigation consequences | S | Pending |
| 15.2 Eligible Affordances | HI / concrete design; PI for navigation consequences | S | Pending |
| 15.3 Geometry | HI / concrete design; PI for navigation consequences | S | Pending |
| 15.4 Initial State | HI / concrete design; PI for navigation consequences | S | Pending |
| 15.5 Activation | HI / concrete design; PI for navigation consequences | S | Pending |
| 15.6 Personalization | HI / concrete design; PI for navigation consequences | S | Pending |
| 16. Relationship Presentation | HI / concrete design; PI for navigation consequences | S | Pending |
| 16.1 Cardinality Rule | HI / concrete design; PI for navigation consequences | S | Pending |
| 16.2 Singular Relationship | HI / concrete design; PI for navigation consequences | S | Pending |
| 16.3 Plural Relationship | HI / concrete design; PI for navigation consequences | S | Pending |
| 16.4 Progressive Relationship Affordances | HI / concrete design; PI for navigation consequences | S | Pending |
| 17. Dance Result Presentation | HI / concrete design; PI for navigation consequences | S | Pending |
| 17.1 Descriptor-Based Classification | HI / concrete design; PI for navigation consequences | S | Pending |
| 17.2 Single-Holon Result | HI / concrete design; PI for navigation consequences | S | Pending |
| 17.3 Holon Collection Result | HI / concrete design; PI for navigation consequences | S | Pending |
| 17.4 Value Collection Result | HI / concrete design; PI for navigation consequences | S | Pending |
| 17.5 Scalar Result | HI / concrete design; PI for navigation consequences | S | Pending |
| 17.6 No-Result Dance | HI / concrete design; PI for navigation consequences | S | Pending |
| 18. Collection Visualizer | Collection / kind spec; TC / concrete design; MAP for semantic editing | S | Pending |
| 18.1 Responsibility | Collection / kind spec; TC / concrete design; MAP for semantic editing | S | Pending |
| 18.2 Selection | Collection / kind spec; TC / concrete design; MAP for semantic editing | S | Pending |
| 18.3 Geometry | Collection / kind spec; TC / concrete design; MAP for semantic editing | S | Pending |
| 19. Table Collection Visualizer | Collection / kind spec; TC / concrete design; MAP for semantic editing | S | Pending |
| 19.1 Rows | Collection / kind spec; TC / concrete design; MAP for semantic editing | S | Pending |
| 19.2 Columns | Collection / kind spec; TC / concrete design; MAP for semantic editing | S | Pending |
| 19.3 Collection Header | Collection / kind spec; TC / concrete design; MAP for semantic editing | S | Pending |
| 19.4 Column Operations | Collection / kind spec; TC / concrete design; MAP for semantic editing | S | Pending |
| 19.4.1 Column-Oriented Sorting Semantics | Collection / kind spec; TC / concrete design; MAP for semantic editing | S | Pending |
| 19.4.2 Sort State Lifetime | Collection / kind spec; TC / concrete design; MAP for semantic editing | S | Pending |
| 19.5 Sequence Column | Collection / kind spec; TC / concrete design; MAP for semantic editing | S | Pending |
| 19.6 Table-Level Default Row Ordering | Collection / kind spec; TC / concrete design; MAP for semantic editing | S | Pending |
| 20. Editable Collection Visualizers | Collection / kind spec; TC / concrete design; MAP for semantic editing | S | Pending |
| 21. Editable Value Arrays | Collection / kind spec; TC / concrete design; MAP for semantic editing | S | Pending |
| 22. Editable Multi-Valued Relationships | Collection / kind spec; TC / concrete design; MAP for semantic editing | S | Pending |
| 23. Dance Result Collection Editability | Collection / kind spec; TC / concrete design; MAP for semantic editing | S | Pending |
| 24. Semantic Editing Ownership | Collection / kind spec; TC / concrete design; MAP for semantic editing | S | Pending |
| 25. Descriptor-to-Presentation Mapping | HI / concrete design; PI for navigation consequences | S | Pending |
| 26. Applying the Interaction Grammar | PI / grammar and design; HI or TC for child presentation | S | Pending |
| 26.1 Horizontal Navigation | PI / grammar and design; HI or TC for child presentation | S | Pending |
| 26.2 Vertical Navigation | PI / grammar and design; HI or TC for child presentation | S | Pending |
| 26.3 Recursive Exploration and Provenance | PI / grammar and design; HI or TC for child presentation | S | Pending |
| 27. Focus and Concrete Extent Realization | PI / grammar and design; HI or TC for child presentation | S | Pending |
| 28. Compression and Editing | PI / grammar and design; HI or TC for child presentation | S | Pending |
| 29. Loading States | PI / grammar and design; HI or TC for child presentation | S | Pending |
| 30. Progressive Retrieval | PI / grammar and design; HI or TC for child presentation | S | Pending |
| 31. Entering Edit Mode | SN / transaction interactions; HI or TC / local editing; MAP / state semantics | S | Pending |
| 32. Continuous Preservation of Staged Work | SN / transaction interactions; HI or TC / local editing; MAP / state semantics | S | Pending |
| 33. Multiple Holons in Edit Mode | SN / transaction interactions; HI or TC / local editing; MAP / state semantics | S | Pending |
| 34. Staged State and Visualizer Occurrences | PI / grammar and design; HI or TC for child presentation | S | Pending |
| 35. Editing While Navigating | PI / grammar and design; HI or TC for child presentation | S | Pending |
| 36. Compressing Editable Visualizers | PI / grammar and design; HI or TC for child presentation | S | Pending |
| 37. Create | SN / transaction interactions; HI or TC / local editing; MAP / state semantics | S | Pending |
| 38. Clone | SN / transaction interactions; HI or TC / local editing; MAP / state semantics | S | Pending |
| 39. Delete | SN / transaction interactions; HI or TC / local editing; MAP / state semantics | S | Pending |
| 40. Commit | SN / transaction interactions; HI or TC / local editing; MAP / state semantics | S | Pending |
| 41. Commit Flow | SN / transaction interactions; HI or TC / local editing; MAP / state semantics | S | Pending |
| 42. Commit Failure | SN / transaction interactions; HI or TC / local editing; MAP / state semantics | S | Pending |
| 43. Undo and Redo | SN / transaction interactions; HI or TC / local editing; MAP / state semantics | S | Pending |
| 44. Undo Boundaries | SN / transaction interactions; HI or TC / local editing; MAP / state semantics | S | Pending |
| 45. Undo Flow | SN / transaction interactions; HI or TC / local editing; MAP / state semantics | S | Pending |
| 46. Redo Flow | SN / transaction interactions; HI or TC / local editing; MAP / state semantics | S | Pending |
| 47. Abandon or Revert Transaction | SN / transaction interactions; HI or TC / local editing; MAP / state semantics | S | Pending |
| 48. Adaptive and Personalizable Interactions | SN / transaction interactions; HI or TC / local editing; MAP / state semantics | S | Pending |
| 49. Personalization and Constrained Geometry | PI / grammar and design; HI or TC for child presentation | S | Pending |
| 50. Interaction Scenarios | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 50.1 Inspect a Holon | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 50.2 Open a Multi-Valued Relationship | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 50.3 Navigate Through a Collection | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 50.4 Follow a Singular Relationship | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 50.5 Continue Horizontally | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 50.6 Continue Vertically | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 50.7 Mixed Traversal | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 50.8 Enter Edit Mode | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 50.9 Edit Scalar Property | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 50.10 Edit Array | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 50.11 Edit Multi-Valued Relationship | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 50.12 Edit Singular Relationship | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 50.13 Edit Related Holon Separately | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 50.14 Create | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 50.15 Clone | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 50.16 Delete | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 50.17 Undo Across Multiple Holons | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 50.18 Commit Multiple Holons | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 50.19 Compress While Editing | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 51. Open Design Questions | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 51.1 Sibling History | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 51.2 Compression Thresholds | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 51.3 Horizontal Overflow | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 51.4 Vertical Overflow | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 51.5 Scalar Dance Results | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 51.6 Dance Result Tabs | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 51.7 Empty Singular Relationships | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 51.8 Branch Closing | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 51.9 Focus Presentation | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 51.10 Transaction Abandon Semantics | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 51.11 Multiple Occurrences of a Staged Holon | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 51.12 Relationship Target Selection | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 51.13 Deleted Holon Presentation | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 52. Non-Goals of the Initial Design | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 53. Normative Design Invariants | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 53.1 Descriptor Semantics Over Runtime Accident | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 53.2 Visualizer Categories Are Roles | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 53.3 Generic Fallbacks Preserve Basic Use | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 53.4 Singular Traversal Goes Right | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 53.5 Plural Traversal Goes Down | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 53.6 Navigation Preserves Provenance | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 53.7 Holon Identity Is Not Occurrence Identity | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 53.8 Child Content Claims Space Only When Activated | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 53.9 Parent Geometry Constrains Subordinate Geometry | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 53.10 Compression Preserves State | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 53.11 Read and Edit Share One Visual Grammar | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 53.12 Staging Is Holon-Specific; Commit Is Transaction-Wide | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 53.13 Multiple Holons May Participate in One Transaction | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 53.14 Undo and Redo Are Space Navigator/Transaction Operations | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 53.15 Editing Membership Is Not Editing the Target | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 53.16 Immediate Personalization and Durable Adaptation Are Distinct | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 53.17 Lazy Population, Early Structure | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| 54. Summary | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |
| Slot-directed selection alignment | SN / PI / HI / TC / DAHN by scenario or invariant | S | Pending |

### space-navigator/path-inspector-grammar.md

Baseline SHA-256: `2374ab4ae24463c96968f59e8c4f453e07b90e2d8bae1a34b84da287e49a8cc2`.

| Source heading | Provisional owner / destination | Disposition | Verification |
| --- | --- | --- | --- |
| DAHN Path Inspector Interaction Grammar | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| Change Log | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| v0.4 | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| v0.3 | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| v0.2 | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| v0.1 | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| Status | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| Purpose and Authority | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 1. Vocabulary | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 1.1 Rooted Navigation Topology | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 1.2 Root | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 1.3 Occurrence | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 1.4 Focus | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 1.5 Viewport | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 1.6 Navigation Topology Versus Spatial Projection | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 1.7 Horizontal Traversal | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 1.8 Vertical Traversal | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 1.9 Column | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 1.10 Row | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 1.11 Sparse Cell | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 1.12 Spatial Budget | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 1.13 Semantic Presentation Obligations | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 2. Topology Production Rules | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 2.1 Inspect | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 2.2 Horizontal Traversal | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 2.3 Vertical Traversal | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 2.4 Branch | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 2.5 Scan | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 2.6 Restore | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 2.7 Re-root | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 2.8 Destination-First Transitions | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 2.9 Close Branch | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 3. Two-Dimensional Grid Projection | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 3.1 Projection as a Derived Grid | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 3.2 Traversal-Path Integrity | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 3.3 Replaceable Leaves | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 3.4 Vertical Alternative Insertion | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 3.5 Horizontal Alternative Insertion | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 3.6 Grid-Band Insertion Preserves Identity | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 3.7 Sparse Cells Are Not Occurrences | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 3.8 Stable Attachment | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 3.9 Lineage Connectors | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 4. Focus-Dependent Geometry | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 4.1 Navigation Focus Determines Allocation Priority | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 4.2 Column Width Is a Path Inspector Decision | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 4.3 Row Height Is a Path Inspector Decision | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 4.4 Cell Budget Is Derived | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 4.4.1 Node Inspector Slot Compression Contract | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| PropertyMap sub-slot content extent | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 4.5 Geometry Emerges From Topology and Focus | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 4.6 Minimum Useful Extent and Surface Growth | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 4.7 View Operations and Pinned Chrome | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 5. Parent and Child Spatial Responsibility | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 5.1 Parent Owns Inter-Child Geometry | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 5.2 Child Owns Intra-Child Adaptation | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 5.3 Recursive Spatial Allocation | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 5.4 Budget Changes Do Not Trigger Reselection by Default | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 5.5 Semantic Capability May Constrain Selection | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 6. Responsive Child Realization | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 6.1 Responsive Realization Belongs to the Child | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 6.2 Compression Is Not Scaling | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 6.3 Semantic Obligations Survive Compression | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 6.4 Responsive Thresholds Belong to the Visualizer | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 7. Compression and Overflow | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 7.1 Compression Is Allocation Change | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 7.2 Independent Axis Compression | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 7.3 Partial and Full Compression | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 7.4 Layout Overflow Versus Off-Viewport | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 7.5 Branch-Local Overflow | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 8. State Preservation | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 9. Derived Rather Than Enumerated Interaction | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 9.1 Small Grammar, Large State Space | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 9.2 Mockups as Conformance Examples | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 9.3 Unmocked Paths Must Remain Coherent | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 10. Grammar Invariants | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 11. Relationship to Space Navigator | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 12. Relationship to Visualizer Selection | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 13. Relationship to Adjacent Specifications | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 14. Intentionally Deferred Decisions | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |
| 15. Summary | PI / moved grammar; DAHN for shared rules; HI for private child details | S | Pending |

### space-navigator/space-navigator-interaction-grammar.md

Baseline SHA-256: `34965c266c42f90034974c02ae5476b94a619e6e6782411a7fff6999f00997e8`.

| Source heading | Provisional owner / destination | Disposition | Verification |
| --- | --- | --- | --- |
| DAHN Space Navigator Interaction Grammar | SN / Dancer grammar; DAHN / shared composition | S | Pending |
| Status | SN / Dancer grammar; DAHN / shared composition | S | Pending |
| Change Log | SN / Dancer grammar; DAHN / shared composition | S | Pending |
| v0.3 | SN / Dancer grammar; DAHN / shared composition | S | Pending |
| v0.2 | SN / Dancer grammar; DAHN / shared composition | S | Pending |
| v0.1 | SN / Dancer grammar; DAHN / shared composition | S | Pending |
| Purpose and Authority | SN / Dancer grammar; DAHN / shared composition | S | Pending |
| 1. Space Navigator Composition | SN / Dancer grammar; DAHN / shared composition | S | Pending |
| 1.1 Active HolonSpace Context | SN / Dancer grammar; DAHN / shared composition | S | Pending |
| 1.2 RootedNavigation Role | SN / Dancer grammar; DAHN / shared composition | S | Pending |
| 1.3 Visualizer Selection | SN / Dancer grammar; DAHN / shared composition | S | Pending |
| 1.4 Spatial Allocation | SN / Dancer grammar; DAHN / shared composition | S | Pending |
| 1.5 DAHN Composition Authorities | DAHN §§29–31 / shared composition contracts | M | Checked — DOC2 |
| 1.6 Surface, Layout, and View | DAHN §§29–31 / shared composition contracts | M | Checked — DOC2 |
| 1.7 Parent-Owned Allocation and Maximization | DAHN §§29–31 / shared composition contracts | M | Checked — DOC2 |
| 1.8 Slots as Participation Contracts | DAHN §§29–31 / shared composition contracts | M | Checked — DOC2 |
| 1.9 Independent State and Experiential Authority | DAHN §§29–31 / shared composition contracts | M | Checked — DOC2 |
| 2. Interaction Boundary | SN / Dancer grammar; DAHN / shared composition | S | Pending |
| 2.1 Delegated Rooted Navigation | SN / Dancer grammar; DAHN / shared composition | S | Pending |
| 2.2 Dancer-Level Interactions | SN / Dancer grammar; DAHN / shared composition | S | Pending |
| 2.3 New Exploration Context Requests | SN / Dancer grammar; DAHN / shared composition | S | Pending |
| 3. Ownership Invariants | SN / Dancer grammar; DAHN / shared composition | S | Pending |
| 4. Relationship to Path Inspector | SN / Dancer grammar; DAHN / shared composition | S | Pending |
| 5. Relationship to Adjacent Specifications | SN / Dancer grammar; DAHN / shared composition | S | Pending |
| 6. Deferred Presentation Decisions | SN / Dancer grammar; DAHN / shared composition | S | Pending |
| 7. Summary | SN / Dancer grammar; DAHN / shared composition | S | Pending |

### space-navigator/space-navigator-arch.md

Baseline SHA-256: `d853d440a767393c1d785b33dd595a4cb3ec25003b353d31cf36da0e9f29a832`.

| Source heading | Provisional owner / destination | Disposition | Verification |
| --- | --- | --- | --- |
| DAHN Space Navigator Architecture Specification v0.4 | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| Status | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| Purpose | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 1. Relationship to the Space Navigator Document Set | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 2. DAHN | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 2.1 Dynamic | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 2.2 Adaptive | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 3. Existing MAP Deployment Architecture | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 4. Primary Responsibility Boundary | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 5. Rust Responsibilities | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 6. TypeScript Responsibilities | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 7. MAP State Versus Experience State | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 7.1 MAP State | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 7.2 Experience State | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 8. IPC Boundary | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 9. Visualizers Are Holons | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 9.1 Visualizer Holon Types | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 9.2 Semantic Identity and Executable Realization | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 10. Generic Versus Specialized Visualizers | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 10.1 Static Core Visualizers | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 11. Visualizer Commons | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 12. Accessible Visualizer Population | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 13. Visualizer Discovery | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 14. Minimal DAHN Visualizer Schema | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 14.1 Applicability | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 14.2 Capabilities | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 14.3 Version and Evolution Domains | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 15. DAHN Selector Function | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 16. Selector Inputs | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 17. Explore Versus Exploit | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 17.1 Exploit-Oriented Selection | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 17.2 Explore-Oriented Selection | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 18. Adaptive Salience | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 19. Personal and Collective Adaptation | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 19.1 Personal Adaptation | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 19.2 Collective Adaptation | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 20. Gesture Handling Boundary | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 21. Adaptive Presentation Context | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 22. Visualizer Selection Result | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 22.1 Visualizer Materialization | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 23. Visualizer Acquisition and Execution | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 24. Visualizer Runtime | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 25. Trust and Compatibility | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 26. Recursive Visual Composition | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 27. Parent-Owned Placement | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 28. Layout Budgets | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 29. Visualizer Layout Capabilities | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 30. Selection Versus Layout | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 31. Responsive Composition | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 32. Theme Architecture | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 33. Theme Versus Semantic Layout | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 34. Action Architecture | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 35. Action Sources | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 35.1 Holon-Semantic Actions | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 35.2 Collection Actions | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 35.3 Visualizer Actions | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 35.4 Canvas Actions and Dancer Transaction Actions | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 36. Action Visualizers | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 37. Dancer and Canvas Interaction Surfaces | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 38. Action Personalization | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 39. Visualizer Occurrence | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 40. Holon Identity Versus Occurrence Identity | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 41. DAHN Interaction Events | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 42. DAHN Events Versus MAP Commands | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 43. Progressive Semantic Retrieval | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 44. Effective Descriptor Boundary | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 45. Property and Value Visualizers | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 46. Collection Visualizers | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 47. Read and Edit Architecture | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 48. Staged State Ownership | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 49. Semantic Editing Ownership | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 50. Multi-Holon Transaction Scope | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 51. Commit Ownership | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 52. Commit Flow | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 53. Create, Edit, and Clone | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| Edit | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| Clone | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| Create | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 54. Delete | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 55. Transaction Snapshots | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 56. UX Undo Boundaries | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 57. Undo | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 58. Redo | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 59. Transaction Status | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 60. Continuous Snapshotting Versus Undo Semantics | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 61. Adaptive Gestures and Transaction Gestures Are Distinct | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 62. DAHN MAP Adapter | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 63. Asynchrony | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 64. Error Boundaries | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 65. Presentation Refresh After Semantic Change | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 66. Multiple Occurrences of the Same Holon | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 67. Space Navigator as an Architectural Proof | Refactor implementation plan / architecture delivery guidance retained for DOC5 | M/S | Checked — DOC2 transfer evidence |
| 68. Initial Architectural Modules | Refactor implementation plan / architecture delivery guidance retained for DOC5 | M/S | Checked — DOC2 transfer evidence |
| 69. Architectural Testing Boundaries | Refactor implementation plan / architecture delivery guidance retained for DOC5 | M/S | Checked — DOC2 transfer evidence |
| 69.1 Rust / MAP Tests | Refactor implementation plan / architecture delivery guidance retained for DOC5 | M/S | Checked — DOC2 transfer evidence |
| 69.2 DAHN Adapter Tests | Refactor implementation plan / architecture delivery guidance retained for DOC5 | M/S | Checked — DOC2 transfer evidence |
| 69.3 Visualizer Runtime Tests | Refactor implementation plan / architecture delivery guidance retained for DOC5 | M/S | Checked — DOC2 transfer evidence |
| 69.4 Visualizer Tests | Refactor implementation plan / architecture delivery guidance retained for DOC5 | M/S | Checked — DOC2 transfer evidence |
| 69.5 Dancer Top-Level Visualizer Tests | Refactor implementation plan / architecture delivery guidance retained for DOC5 | M/S | Checked — DOC2 transfer evidence |
| 69.6 Adaptive Interaction Tests | Refactor implementation plan / architecture delivery guidance retained for DOC5 | M/S | Checked — DOC2 transfer evidence |
| 70. Architecture That Should Not Be Over-Generalized Initially | Refactor implementation plan / architecture delivery guidance retained for DOC5 | M/S | Checked — DOC2 transfer evidence |
| 71. Core Architectural Invariants | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 71.1 Rust Owns Semantic Truth | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 71.2 TypeScript Owns Experience Realization | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 71.3 Rust Owns the DAHN Selector | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 71.4 Visualizer Discovery Is Federated | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 71.5 Visualizers Are Holons | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 71.6 Visualizer Selection and Execution Are Separate | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 71.7 Generic Fallbacks Preserve Usability | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 71.8 Parent Owns Child Placement | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 71.9 Layout Is Hierarchical | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 71.10 Themes Are External | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 71.11 Read and Edit Share the Same Visual Structure | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 71.12 Staged State Remains in Rust | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 71.13 Transactions May Span Multiple Holons | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 71.14 Undo and Redo Are Transaction-Scoped | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 71.15 Subject, Visualizer, and Occurrence Are Distinct | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 71.16 Adaptive Preferences Refer to Visualizer Holons | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 71.17 User Gestures May Become Adaptive Signals | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 71.18 Action Scope Determines Ownership | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 71.19 Architecture Defines Contracts, Not Space Navigator UX | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 72. Architectural Summary | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 72.1 MAP Semantic and Adaptive Layer — Rust | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 72.2 DAHN Experience Layer — TypeScript | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 72.3 Visualizer Ecosystem — Federated MAP Agent Spaces | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |
| 72.4 Canvas-Hosted Dancer Experiences | hx/dahn-arch.md / same heading or DOC2 canonical delegation | M/S | Checked — DOC2 transfer evidence |

### space-navigator/space-navigator-concept.md

Baseline SHA-256: `3341709e8fa3686af0ec16e8100bbac902ec1629df358729b9b66e839d2d5513`.

| Source heading | Provisional owner / destination | Disposition | Verification |
| --- | --- | --- | --- |
| DAHN Space Navigator — Concept | SN / explanatory orientation and source links | R | Pending |
| What It Is | SN / explanatory orientation and source links | R | Pending |
| Why This Model Exists | SN / explanatory orientation and source links | R | Pending |
| Entering DAHN | SN / explanatory orientation and source links | R | Pending |
| Descriptor-Driven Experience | SN / explanatory orientation and source links | R | Pending |
| Two Complementary Ways to Explore | SN / explanatory orientation and source links | R | Pending |
| Reusable Visual Roles | SN / explanatory orientation and source links | R | Pending |
| Context, Provenance, and Scale | SN / explanatory orientation and source links | R | Pending |
| Read and Edit Are One Experience | SN / explanatory orientation and source links | R | Pending |
| Relationship to the Rest of the Specification | SN / explanatory orientation and source links | R | Pending |

### space-navigator/index.md

Baseline SHA-256: `07d16aebc177eb6947cb8625a5f55b9d305ef6e2673acde0c4f3902e9bf9c30f`.

| Source heading | Provisional owner / destination | Disposition | Verification |
| --- | --- | --- | --- |
| DAHN Space Navigator | SN / explanatory orientation and source links | R | Pending |
| Purpose | SN / explanatory orientation and source links | R | Pending |
| Specification Hierarchy | SN / explanatory orientation and source links | R | Pending |
| Document Responsibilities | SN / explanatory orientation and source links | R | Pending |
| Concept | SN / explanatory orientation and source links | R | Pending |
| Architecture | SN / explanatory orientation and source links | R | Pending |
| Interaction Grammar | SN / explanatory orientation and source links | R | Pending |
| Design Specification | SN / explanatory orientation and source links | R | Pending |
| Implementation Plan | SN / explanatory orientation and source links | R | Pending |
| Authority and Precedence | SN / explanatory orientation and source links | R | Pending |
| Stable Center | SN / explanatory orientation and source links | R | Pending |
| Reading Order | SN / explanatory orientation and source links | R | Pending |

### hx/dahn-implementation-plan.md

Baseline SHA-256: `41db3ab2afc695d18aa2086aeb0acd3c7298ad3e143cebe97a14679b5a3910a2`.

| Source heading | Provisional owner / destination | Disposition | Verification |
| --- | --- | --- | --- |
| **DAHN MVP Implementation Plan (Descriptors-Synthesized v1.2)** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| *A pragmatic path to bringing the MAP’s human experience to life.* | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Change Log | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| v1.2 | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| --------------------------------- | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **PHASE 0 — Foundational Runtime (Weeks 1–2)** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| *Lay the SEA substrate DAHN will run on.* | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **0.1. SEA Runtime Foundations** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **0.2. Uniform API Integration** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **0.3. Dynamic Loader** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| --------------------------------- | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **PHASE 1 — Minimal Canvas, Minimal Theme, Initial Visualizers + TypeDescriptors (Weeks 3–6)** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| *Deliver the first full end-to-end experience loop using the MAP’s Type System itself.* | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **1.1. MVP Canvas: “DAHN-2D Minimal Canvas”** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **1.2. MVP Theme** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **1.3. Three Core Visualizers** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **1.3.1. Property Sheet Visualizer** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **1.3.2. Relationship List Visualizer** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **1.3.3. Action Menu Visualizer** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **1.3.4. Descriptor-Aware Presentation Rules** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **1.4. Selector Function (Static v0)** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **1.5. Milestone Zero — Universal Holon Rendering (FIRST DEMO)** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| --------------------------------- | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **PHASE 2 — Holon Editing (Universal, Minimal, Safe) (Weeks 7–10)** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| *From observation to participation.* | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **2.1. Generic Holon Editing Infrastructure** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **2.2. Relationship Editing (Minimal v0)** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **2.3. TypeDescriptor Editing (First-Class Demonstration)** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **2.4. Create New Holons (TypeDescriptors First)** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| --------------------------------- | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **PHASE 3 — Personalization (Salience + Affinity) + Theme Switching (Weeks 11–16)** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| *Now the system adapts to the person.* | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **3.1. Salience Gestures** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **3.2. Affinity Gestures** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **3.3. Selector Function v1** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **3.4. Theme Switching** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| --------------------------------- | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **PHASE 4 — Visualizer Commons + Community Signals (Weeks 16–22)** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| *DAHN opens to the ecosystem.* | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **4.1. Visualizer Commons v0** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **4.2. Selector Function v2 (Community-aware stub)** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| --------------------------------- | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **PHASE 5 — Canvas Evolution + Adaptive Controls (Weeks 22–30)** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| *DAHN becomes multi-modal, more expressive, and more adaptive.* | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **5.1. Enhanced 2D Canvas** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **5.2. Additional Canvases** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **5.3. Adaptive Controls (Explore ↔ Exploit)** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **5.4. Selector Function v3 (Adaptive)** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| --------------------------------- | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **PHASE 6 — DAHN Alpha Release** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| *The experience layer of the MAP is fully alive.* | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| --------------------------------- | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **PHASE 7 — Localization + Accessibility + Device Variants (Weeks 30–40)** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| *Make DAHN globally inclusive and widely usable.* | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **7.1. Localization Foundations** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **7.2. Accessibility Foundations** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **7.3. Mobile / Tablet Optimization** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| --------------------------------- | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **Guiding Principles Throughout** | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| **In Summary** | DAHN or integrated delivery plan / preserve historical status | S | Pending |

### space-navigator/space-navigator-impl-plan.md

Baseline SHA-256: `9ea1a37ac58dbe8f60b0702bbc48a198b3f5c84f68812e91f8e2ae3c79172880`.

| Source heading | Provisional owner / destination | Disposition | Verification |
| --- | --- | --- | --- |
| DAHN Space Navigator Implementation Plan v1.2 | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Status | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Change Log | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Purpose | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 1. Delivery Strategy | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 1.1 Foundation and First Application | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 1.2 Migration and Dependency Order | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 2. PR Sizing Rule | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 2.1 Planned Dev Point Estimates | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 3. Phase 0 — DAHN Runtime Seams | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 1 — DAHN TypeScript MAP Adapter | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Non-Goals | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Schema Task S1 — First-Cut DAHN Visualizer Schema Definition | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Non-Goals | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Dependency | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 2 — Visualizer Implementation Runtime Resolution | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Non-Goals | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 3 — Rust DAHN Selector Boundary | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Non-Goals | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 4 — Theme Token Foundation | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Non-Goals | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 4. Phase 1 — Canvas-First Read-Only Experience | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 5 — Static Table Collection Visualizer | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Non-Goals | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 5.a-pre — MAP Application Launcher Foundation | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Non-Goals | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 5.a — DAHN Canvas Visualizer | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Non-Goals | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 5.b — Basic Generic Holon Node Shell | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Geometric Requirements | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 5.b.1 — HolonSpace Home-Dancer Mount | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Non-Goals | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 5.c — DAHN Launch Experience | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Dependencies | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Non-Goals | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 6 — Properties Pane and Descriptor-Driven Value Presentation | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Non-Goals | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 9 — Descriptor-Driven Affordance Classification | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Normative Requirement | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 5. Phase 2 — Vertical Collection Exploration | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 10 — Collection Tab Activation | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Geometry | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Milestone | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 11 — Collection Row Selection | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 12 — First Vertical Child | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 13 — Vertical Sibling Switching and Retained Vertical Alternatives | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Boundaries and Sequencing | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 6. Phase 3 — Horizontal Navigation and Provenance Geometry | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 14 — First Singular Relationship Child | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Geometry | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Boundaries and Sequencing | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Milestone | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 15 — Recursive Horizontal Navigation | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 16 — Vertical Compression | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 17 — Horizontal Compression | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 18 — Orthogonal Two-Axis Compression | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 6A. Phase 3A — DAHN Composition and View Foundations | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 18.a — Surface View Transform and Recovery | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope and Dependencies | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Agreed Initial Presentation Policies | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 18.b — Minimal Window Manager Context Host | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope and Dependencies | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 18.c — Bounded Focus and Maximize Requests | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope and Dependencies | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 18.d — Close Navigation Branch | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope and Dependencies | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 18.e — Re-root into a New Experiential Context | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope and Dependencies | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 7. Phase 4 — Read-Only Collection Refinement | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 19 — Collection Sorting | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 20 — Collection Filtering | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 8. Phase 5 — Adaptive Ordering and Visualizer Choice | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 21 — Presentation Ordering from Rust | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 22 — Local Reordering and Adaptive Gesture Events | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 23 — Alternate Visualizer Selection | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 9. Phase 6 — Staged Editing Foundation | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 24 — Edit Existing Holon: Scalar Properties | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 25 — Dancer Transaction Status and Action State | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 26 — Meaningful Undo Boundaries | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 27 — Space Navigator Undo | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 28 — Space Navigator Redo | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 29 — Space Navigator Transaction Commit | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Milestone | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 10. Phase 7 — Multi-Holon Transaction Capability | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 30 — Edit Multiple Existing Holons in One Transaction | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 31 — Commit Multiple Updated Holons | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 32 — Multiple Occurrences of One Staged Holon | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Architectural Invariant | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 11. Phase 8 — Create, Clone, and Delete | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 33 — Clone Holon | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 34 — Create Instance from Concrete Type | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 35 — Stage Delete | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 12. Phase 9 — Editable Collections and Relationships | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 36 — Editable Value Arrays | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 37 — Generic Relationship Target Selection | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Non-Goals | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 38 — Editable Multi-Valued Relationships | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 39 — Editable Single-Valued Relationships | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 13. Phase 10 — Dances | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 40 — Effective Dance Actions | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 40.a — Space Navigator Load Holons Action and Legacy-App Retirement | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Non-Goals | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 41 — Single-Holon Dance Results | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 42 — Collection Dance Results | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 43 — Scalar and No-Result Dances | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 14. Phase 11 — Action Personalization | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 44 — Reorder Node Actions | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 45 — Space Navigator Action Personalization | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 15. Phase 12 — Visualizer Commons and Adaptive Selection Expansion | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 46 — Accessible Visualizer Commons Discovery | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 47 — Semantic Applicability over Discovered Visualizers | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 48 — Personal Visualizer Preference | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 49 — Initial Collective Salience | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 50 — Explore/Exploit Selection Controls | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 16. Phase 13 — Navigation and Transaction Hardening | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 51 — Staged-State Indicators Through Compression | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 52 — Transaction-Aware Branch Closing Hardening | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 53 — Transaction Abandon/Revert | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 54 — Deleted Holon Presentation | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Goal | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Scope | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Acceptance Criteria | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 17. Recommended Milestones | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Milestone A — First Dynamic Read-Only Node | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Milestone B — First Useful Vertical Exploration | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Milestone C — Two-Dimensional Space Navigator | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Milestone C.1 — Composable Navigation Contexts | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Milestone D — Read-Only Usability and Initial Adaptation | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Milestone E — First Complete Update Flow | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Milestone F — Multi-Holon Transaction | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Milestone G — Generic Lifecycle Operations | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Milestone H — Full Initial Dance Integration | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Milestone I — Adaptive Visualizer Ecosystem | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 18. Capabilities Intentionally Deferred | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 19. Cross-PR Implementation Principles | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 19.1 Preserve Architectural Seams Early | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 19.2 One Semantic Source of Truth | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 19.3 One Experience Occurrence Model | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 19.4 One Node Grammar | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 19.5 One Collection Grammar | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 19.6 Read and Edit Share the Visual Tree | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 19.7 Commit Belongs to the Transaction | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 19.8 Undo Is Semantic | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 19.9 Personalization Is Immediate; Learning Is Durable | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 19.10 Parent Owns Placement | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 19.11 Independent Topology, Layout, and View Preserve State | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 19.12 Prefer Working Slices | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 20. Overall Capability Progression | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 21. Handoff to GitHub Issues | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Phase 4 — Slot-directed Visualizer selection correction | DAHN or integrated delivery plan / preserve historical status | S | Pending |

### hx/phase-0-implementation-blueprint.md

Baseline SHA-256: `4d633cb4fae726fc0d5f0aca446279890cbb5cb72550d44c22497764118149fb`.

| Source heading | Provisional owner / destination | Disposition | Verification |
| --- | --- | --- | --- |
| DAHN Phase 0 Implementation Blueprint (v1.1) | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Change Log | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| v1.1 | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Purpose | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 1. Recommended Initial Placement | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Boundary Rule | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 2. Proposed Module Layout | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 3. Core Contracts | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 3.1 `contracts/targets.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 3.2 `contracts/holon-view.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 3.3 `contracts/affordances.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 3.4 `contracts/visualizers.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 3.5 `contracts/canvas.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 3.6 `contracts/selector.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 3.7 `contracts/themes.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 4. Runtime Modules | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 4.1 `runtime/dahn-runtime.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 4.2 `runtime/default-dahn-runtime.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 5. Access Adapter Modules | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 5.1 `adapters/sdk/sdk-holon-access-adapter.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Public SDK Alignment Assumption | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 5.2 `adapters/sdk/descriptor-mappers.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 5.3 `adapters/sdk/affordance-hierarchy-builder.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 6. Registry and Loader Modules | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 6.1 `registry/visualizer-registry.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 6.2 `registry/builtins.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 7. Selector Module | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 7.1 `selector/phase0-selector.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 8. Canvas Modules | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 8.1 `canvas/minimal-canvas-element.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 8.2 `canvas/minimal-canvas-controller.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 9. Visualizer Modules | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 9.1 `visualizers/holon-node/holon-node-visualizer.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Suggested internal flow | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 9.2 `visualizers/holon-node/property-rendering.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 9.3 `visualizers/holon-node/relationship-rendering.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 9.4 `visualizers/holon-node/affordance-rendering.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 9.5 `visualizers/action-menu/action-menu-visualizer.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 9.6 `visualizers/debug/holon-json-debug.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 10. Theme Modules | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 10.1 `themes/default-theme.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 10.2 `themes/theme-registry.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 11. Integration Modules | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 11.1 `integration/create-dahn-runtime.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 11.2 `integration/dahn-route.component.ts` | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 12. First PR Slices | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 1: DAHN Contracts and Skeleton | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 2: Visualizer Registry and Minimal Canvas | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 3: Public SDK Access Adapter Seam | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 4: Trivial Phase 0 Selector | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 5: Affordance Hierarchy and Action Menu Visualizer | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 6: Generic HolonNodeVisualizer | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 7: Host UI Mount and Bring-Up Route | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| PR 8: Hardening and Boundary Tests | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 13. Testing Blueprint | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Unit Tests | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Component/DOM Tests | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| Boundary Tests | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 14. Key Open Questions to Resolve Before Coding | DAHN or integrated delivery plan / preserve historical status | S | Pending |
| 15. Minimal Recommended Bring-Up Demo | DAHN or integrated delivery plan / preserve historical status | S | Pending |
