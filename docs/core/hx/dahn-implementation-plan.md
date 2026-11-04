# DAHN Foundation Implementation Roadmap v1.6

## Purpose and delivery authority

This roadmap identifies reusable DAHN capabilities and their delivery homes.
The [Space Navigator integrated plan](../space-navigator/space-navigator-impl-plan.md)
is the single PR sequence for the initial experience, including shared foundation
work. Each slice there identifies its owners, design authority, dependencies,
and recorded status. This roadmap does not create a parallel milestone schedule.

The recorded baseline is delivery through Phase 3, confirmed by the project owner
on 2026-09-28; Phase 3A (18.a–18.e) and subsequent work remain planned in that
record. Documentation reconciliation is not a fresh implementation-status audit. The
bounded October 30 checkpoint record below adds implementation and live-profile
evidence without changing unrelated roadmap delivery status.
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
| Theme/token infrastructure — DAHN | PR 4 and 5.a | Recorded baseline; guest-side LoadTheme follow-up implemented in map-holons #843; existing explicit switching verified; broader Theme workflows remain backlog. |
| Application startup and generic Canvas — Launcher / Canvas | 5.a-pre, 5.a | Recorded baseline; home-Dancer coupling belongs to 5.b.1. |
| Visualizer Operators and shared inspector composition — DAHN / concrete Visualizers | VC-1–VC-3 in the integrated plan | Documentation proposal; no implementation or new enhancement authorized before design acceptance. |
| Context host, surface/view and bounded attention — Host / Canvas / composition owners | 18.a–18.c | Planned; independent restore state and explicit request outcomes. |
| Branch close and source-preserving exploration tabs — Path Inspector / Dancer | 18.d–18.e | Planned; Space Navigator owns exploration tabs sharing its read transaction within one host context; navigation productions remain Path Inspector-owned. |
| Adaptive reporting and validated choice — DAHN/Rust with concrete gesture owners | 21–23, 44–45, 48 | Planned; immediate UI response does not move durable learning into TypeScript. |
| Semantic staging, validation, undo/redo, commit — MAP; coordination — Dancer | 24–39, 51–54 | Planned; concrete editors delegate mutation to MAP. |
| Commons discovery, applicability and collective/exploratory policy — DAHN | 46–50 | Planned later expansion; authorization and explicit selection policy precede executable use. |

## Reusable saved-Holon cache capability

[Enhancement #847](https://github.com/evomimic/map-holons/issues/847) has a local
Rust runtime implementation: `ensure_cached(ids)` filters usable cache hits and
bulk-populates missing saved identities under the
[saved-Holon cache contract](../core-runtime/saved-holon-cache-design-spec.md).
Its delivery includes cache/service/Dance/wire support, capability-level tests,
and cold/warm instrumentation. Success is implicit with an errors-only return;
population is ordinarily evictable and returns no retention leases. Optional
population-and-retention support belongs to a separately scoped usage.
It does not require a DAHN consumer integration.

Effective descriptor construction, named member lookup, and Inspector projection
are potential usages whose insertion point, target scope, timing, and retention
policy must be considered separately. No unconditional all-target warming policy
is selected here. Usage evaluation must weigh guest-call savings against unused
retrieval, serialization, transfer, and cache occupancy. The 10,000-entry local
capacity experiment investigates eviction independently of this capability.

October 30 local verification used the working tree based on map-holons
`8569d47b477730babbc983e5711a01aaca9dbf15`, macOS arm64, the repository Nix
Rust 1.95.0 environment, and a real local Holochain conductor with freshly built
production DNA. Controlled host-cache scenarios used the same 100 saved IDs and
existing 10,000-entry local capacity experiment; each scenario also verified
subsequent-request reuse through its same space/cache owner.

| Usable hits | Missing IDs | Bulk guest invocations | Errors | Population elapsed |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 100 | 1 | 0 | 359.778 ms |
| 85 | 15 | 1 | 0 | 87.473 ms |
| 100 | 0 | 0 | 0 | 0.061 ms |

Inputs included duplicate IDs, with only distinct misses crossing the boundary.
These are single local observations after bootstrap, not application latency
claims; underlying storage reads were not measured. Existing references and later
requests reused populated state, an unrelated staged edit remained intact, and a
malformed ID did not prevent an independent valid ID from being populated.

The permanent regression fixture uses 64 saved IDs (0, 54, or 64 initial hits)
so its residency assertions fit the original 99-entry cache independently of the
capacity experiment. Reproduce its real transport checks and measurements with:

```sh
nix develop --command npm run build:happ
nix develop --command cargo test --manifest-path tests/sweetests/Cargo.toml --test cache_population_tests -- --nocapture
```


## Theme loading follow-up

[map-holons #843](https://github.com/evomimic/map-holons/issues/843) adds the
Theme-afforded, Space-authoritative LoadTheme Dance after the delivered Theme
foundation and Canvas projection slices. The guest resolves assignments and
returns one consolidated browser-independent result; the SDK returns exact
Theme/MDS/token identities and scalar bindings in one operation, and DAHN performs
local CSS projection. This is a bounded unnumbered addition, not a new roadmap PR.

The implementation passes local host/WASM, schema, SDK, UI, and real-conductor
checks on the active map-holons branch. A 63-token Theme took 742 ms on its first
load and 567 ms on repeat load in the integration harness; guest resolution took
148 ms and 144 ms respectively. First-load invocation setup took 299 ms. These
measurements begin after bootstrap and package loading, not at process startup.
Both one-token and 63-token Themes execute one canonical LoadTheme invocation;
the warm path also has one fixed descriptor lookup. SDK boundary tests cover
1, 63 and 126 bindings with one IPC operation and no follow-up reads.

The 63-token scalar payload was 8,212 bytes and the consolidated SDK result was
24,908 bytes. Local response decoding took 38 microseconds; fixture-based local
CSS projection took approximately 0.11 ms. Exact token versions survive transport,
and an unrelated staged edit remains open and unchanged. Transport envelopes grew
across repeated calls as existing transaction transients accumulated; that broader
transport behavior remains a performance reassessment item.

Live verification subsequently measured Theme projection at 392 ms, down from
80,194 ms, with one SDK LoadTheme command. An explicit switch between the existing
Themes visibly updated the experience promptly; its host loading route took
749 ms for 63 bindings. Later cold-start samples measured 368 ms and 796 ms.
These observations verify the current startup and explicit-switch paths; they
do not establish a general latency guarantee. See the performance record below.

THEME-001, THEME-002 and THEME-003 remain declared without active validation
bindings. LoadTheme removes the old read-time semantic validation loops without
implementing or activating their replacement. Authoritative Theme validation
remains a separate follow-up; this delivery does not establish Theme validity.

## October 30 implementation checkpoints

The active map-holons branch backing [PR #846](https://github.com/evomimic/map-holons/pull/846)
contains two pushed checkpoints:

| Checkpoint | Bounded implementation |
| --- | --- |
| [3ce622b9](https://github.com/evomimic/map-holons/commit/3ce622b9) | Slot-Usage-first selection, applicability-scoped default Usage reuse, cross-submission asynchronous save coalescing, and guest-side LoadTheme with consolidated SDK bindings. |
| [8569d47b](https://github.com/evomimic/map-holons/commit/8569d47b) | Guest-prepared singular/plural navigation, duplicate-preserving composition, zero-maximum omission, preserved structural provenance, and shared home-Dancer Visualizer selection. |

### Prepared navigation and shared home selection

EffectiveHolonDescriptor now stores `SingularNavigableRelationships` and
`PluralNavigableRelationships`. Construction resolves direct directional bounds
in the guest. Maximum one is singular, maximum greater than one or unbounded is
plural, and explicit maximum zero is omitted from both. The composed accessor
preserves duplicates. Complete declared contracts and structural navigation
provenance remain available independently of the presentation partitions.
Commands and SDK expose lifecycle-filtered partition requests; DAHN consumes them
without resolving cardinality separately for each relationship. See the
[runtime descriptor contract](../core-runtime/descriptors/descriptors-design-spec.md#143-navigablerelationships-and-instance-availability).

Home-Dancer orchestration retains discovery of the HolonSpace's afforded Dancers,
but its private `select_for_slot()` implementation has been removed. Both initial
Visualizer bindings call the shared selector with the active HolonSpace and Theme:
the RootedNavigation Slot belongs to the selected Dancer; the root Node Slot
belongs to the selected RootedNavigation Visualizer. Slot Usage reuse, owner/Slot
validation, Theme token compatibility, implementation availability, and ambiguity
policy now follow the same selection path used by ordinary composition.

Local validation includes Core/runtime and selector regressions, schema contract
checks and regenerated bootstrap assets, host/WASM checks, SDK/UI tests, formatting,
and real-conductor retained-descriptor/transport tests. Regression cases cover
zero/one/finite-many/unbounded cardinality, duplicate occurrences, malformed bounds,
structural provenance after partitioning, unavailable or Theme-incompatible home
candidates, and eligible Slot Usage reuse in the presence of broad ambiguity.
These checkpoints and local checks do not claim PR approval, merge, issue closure,
or completion of every live #833 gesture/coalescing verification gate.

### Observed startup performance

The following are individual live development-mode runs on the same Mac on
2026-10-30. They are observations, not benchmark guarantees. Canvas Start is the
frontend interval from session readiness through mounted Canvas composition;
it excludes earlier Core Schema loading, base-package activation, and home-Dancer
selection. Core Schema loading remained approximately 77–79 seconds in these runs.
The earlier pre-LoadTheme frontend baseline was 221.116 seconds, including
80.194 seconds of Theme projection and 925 SDK commands.

| Live profile start (UTC) | Implementation state | Canvas Start | Construct Canvas | Theme projection | SDK commands | Guest-call entries |
| --- | --- | --- | --- | --- | --- | --- |
| 17:13:26.058 | LoadTheme; before navigation partitions | 118.593 s | 104.065 s | 0.392 s | 474 | 593 |
| 18:07:46.819 | Navigation partitions; before shared home selector | 95.882 s | 81.796 s | 0.368 s | 417 | 470 |
| 18:28:19.370 | Navigation partitions and shared home selector | 96.704 s | 82.454 s | 0.796 s | 421 | 455 |

The partition change removed all 59 frontend GetEffectiveCardinality commands,
previously totaling 23.796 seconds. It replaced one prepared relationship
availability request with two partition requests: 0.313 seconds before versus
0.913 seconds after in that comparison. The latest run spent 0.775 seconds on
the two requests and still issued no individual cardinality commands.

Shared home selection established uniform behavior but did not improve the
observed launch latency. The home-Dancer phase increased from 21.358 to 26.813
seconds. Approximately corresponding guest-call entries increased from 97 to
118: relationship queries 62 to 75, canonical invocations 8 to 10, key lookups
20 to 24, and holon fetches 7 to 9. Added eligibility reads and supporting
preparation are visible; broad applicability discovery still occurred for both
initial bindings. Combined home selection plus Canvas Start increased from
117.240 to 123.517 seconds in this pair of runs. The counts are consistent with some preparation moving earlier: Canvas Start
guest-call entries fell by 15 while home-selection entries rose by 21.

The latest Canvas Start remains dominated by selection and materialization.
Its 12 SelectVisualizer and two SelectVisualizerUsage commands generated 211
guest calls, including 134 relationship queries. The eight complete Visualizer
materialization flows generated 88 SDK commands and 111 guest calls, including
73 relationship queries; all eight SDK DanceV2 requests were MaterializeVisualizer.
The first, Canvas materialization Dance took 10.607 seconds of the 19.126-second
DanceV2 total; complete materialization flows also include invocation construction,
response decoding, and artifact fetching.

These two directly attributable responsibilities account for 322 of 455 guest
entries. Twenty identified launch/Theme/Usage-bookkeeping commands account for
five more. The remaining 299 standalone SDK reads account for 128 guest entries;
they mix subject values, subject schema/affordance metadata, and presentation
metadata. The current trace does not reliably assign those reads to logical
responsibilities. They must not be reported as 299 subject-data reads. Logical
responsibility and target/property tagging remain profiling follow-up work.
Guest entries are counted by completion timestamp within the relevant phase;
they are query occurrences, not counts of distinct source definitions.
Accumulated SDK/guest durations may overlap, and guest durations are nested within
SDK durations; neither should be added to the other or treated as wall-clock time.

Pre-session binding preparation, bulk agent/context indexes, broader materialization
and metadata consolidation, and Experience Upgrade Session commit/cancel remain
follow-up work. THEME-001/002/003 remain inactive as described above. The remaining
startup cost does not justify relaxing eligibility or reviving a separate selector.

## Established bindings and sparse personal state: design reconciliation

The [DAHN v2.16 target](dahn-design-spec.md#145-recursive-selection) supersedes
on-demand-only preparation, automatic durable default Usage creation, and fresh
candidate discovery for every constituent. Associated personal Usages participate
under full local-choice/cross-cutting-preference/default precedence. Each selected
owner directs current child demand through shared Rust resolution. This is the
intended design, not a claim of delivery or authorization for runtime changes.
The October 30 checkpoint's applicability-scoped default Usage behavior remains
recorded implementation evidence; it does not establish sparse personal Usages.
The integrated plan remains the delivery sequence; the following work requires
implementation grounding rather than inferred completion or new estimates:

- Formalize descriptor-authored Slot activation and subject expansion; use enums
  for controlled vocabulary while retaining extensible owner-local roles. Owners
  declare demand and contracts; the Selection Service chooses concrete Visualizers.
- Prepare shared bindings when Visualizers, slots, declarations, or compatibility
  dependencies change, so a first visit needs neither prior personal use nor
  speculative loading of inactive navigation destinations.
- Reach personal choices through authorized agent/context access; bulk-load and
  index relevant records, including reusable known absence. Evaluate ancestry
  from metadata instead of repeating backend Usage-discovery walks per slot.
- Support composition-owned subordinate settings and cross-cutting preferences,
  with explicit local overrides; keep exact relationships, scope keys, schema
  migration, and adaptive policy unresolved pending grounded design.
- Render automatic/inherited defaults without durable personal Usage creation.
  Retain accepted personal choice/configuration, pins, presets, or an explicitly
  remembered default; keep transient initialization and automatic binding caches
  separate. Preserve background batching and coalescing for required personal saves.
- Apply explicit/local choices, cross-cutting preferences, compatible service-prepared
  defaults, then localized discovery. Validate associated personal Usages
  within their precedence tier; a miss does not by itself require discovery.
- Interpret selected owners' effective Slot descriptors in shared Rust. Execute
  application selection and internal child resolution in the guest without
  Visualizer-specific Rust callbacks or per-child Command/Dance redispatch. Remove
  TypeScript child-selection orchestration; retain semantic interaction requests
  and host/client realization responsibilities.
- Reuse Rust resolution contexts, semantic metadata, batches, and in-flight work.
  Consider guest-side storage-dependent resolution without freezing host-only
  orchestration. A consolidated boundary must return useful authorized binding/
  configuration metadata or explicitly account for remaining reads. Preserve
  host artifact verification, materialization, and runtime admission.
- Reconsider parent alternatives before dependent children; retain explicit open
  view application, admission, and state-preservation contracts.

### Activation scope for the selection foundation

For the Issue 848 increment, effective owner descriptors determine presentation
versus demand activation. Personal activation-policy overrides are deferred:
no new Usage configuration for initially opening a chosen collection, override
precedence, or persistence/invalidation of such activation preferences is required.
This deferral does not restrict existing personal Visualizer selection or
configuration, and does not redefine retained live-occurrence state as a durable
activation preference. A later increment may add explicit activation preferences.

Presentation activation resolves all logical constituents, including all 18
properties when only four rows fit onscreen. Compatible constituents reuse
bindings; viewport virtualization does not issue semantic selection requests.

### Subject-binding scope for the selection foundation

Use bounded semantic binding operations for the owner's subject, property-name
labels, typed property values, afforded actions, and activated collections.
Shared Rust interprets descriptor declarations for all contributed Visualizers.
Arbitrary navigation expressions and an embedded query language are deferred
from Issue 848. Finalize enum identities and per-operation context before TDL
changes; the vocabulary above establishes semantic coverage, not ratified keys.

Use VisualizerKind as the shared MAP-recognized grounding vocabulary on both
Visualizers and Slots, backed by the same schema enum and shared Rust vocabulary.
Rename the current CompositionKind Slot declaration accordingly; there is no
separate composition-kind taxonomy. Reconcile the current Rust enum with the
semantic kind contracts, including retirement of Property. Establish governing
kind through the Visualizer's describing type and its nearest locally annotated
Extends ancestor. Prepare/reuse that result with type/ancestry dependency evidence;
do not repeat guest relationship queries per Slot to rediscover the kind. Preserve
the agreed single required kind per Slot, validate kind
agreement and coherence with all AcceptsVisualizerType targets, and distinguish
schema diagnostics from an ordinary no-candidate outcome. Cover multiple accepted
types within one kind and rejection of a Value kind paired with a Node type.

Do not introduce an EffectiveVisualizer aggregate or wrapper in this increment.
Resolve descriptor-authored kind through the existing reference/descriptor
surfaces and retain reusable results in the selection metadata where appropriate.
A broader effective-Visualizer product may be considered later when concrete
consumer needs establish its contract; kind inheritance alone does not require it.

Separate semantic selection from executable realization. Remove host local
artifact-presence/loadability and validation/loaded-status gates from candidate
selection and prepared-binding reuse, including the existing
visualizer_artifact_available checks. Do not replace these gates with a host
readiness snapshot or per-candidate callback. Host verification, materialization,
loading, and admission follow selection. For Issue 848, record/report the
materialization or loading error and stop that realization attempt. Do not
implement automatic or agent-driven retry cycles, candidate-exclusion plumbing,
or alternative selection on this failure path. A code comment may identify the
future retry integration point. No TypeScript fallback selector is introduced.

Future retry guidance retains the agreed request-local exclusion scope: failed
Visualizers are excluded only for the current presentation attempt and retry
chain, including prepared reuse, without changing durable preferences, shared
defaults, or later independent attempts. Retry initiation and protected-choice
behavior remain follow-up decisions, not requirements of this increment. The
historical source-inspection and startup records above describe the previous
artifact-availability gating, not the successor selection contract.

Value selection in this increment depends on declared ValueType and applicable
non-value semantic context. Actual stored values and populated/unset state do
not enter winner resolution or reuse keys, and selection must not fetch values
merely to select their Visualizers. Cover an unset/populated optional date pair
with the same other context. Value-content-dependent selection is deferred.

### Design behavior checks for subsequent implementation grounding

These scenarios check the documentation target. They are not runtime test results
or new issue acceptance gates imposed by this documentation change.

| Scenario | Required target behavior and authority |
| --- | --- |
| First-time agent | Prepared defaults work with no prior rendering or durable constituent Usages (§§11.1, 14.5.1). |
| Inspector with 18 scalar properties | Compatible contexts reuse bindings and indexed personal metadata; no independent candidate search or Usage-discovery walk per property (§14.5.3–4; Holon Inspector). |
| Current Holon Inspector | Requests visible constituents; no Collection Viewer binding until collection activation (§14.5.1; Holon Inspector). |
| Inspector initially opening one collection | Its owner requests that collection during initial composition and leaves the others unresolved (§14.5.1). |
| Preferred date interactor | One agent/context preference carries calendar/localization behavior across compatible compositions; incompatible read/edit/range contracts still reject it (§11.1; Value kind). |
| Local configuration | Subordinate composition settings are reached through their Usage, apply only in declared scope, and preserve broader preferences (§11.1). |
| Parent replacement | Resolve the parent first; the replacement owns new child demand, so obsolete descendant alternatives need no exploration (§14.7.2). |
| New visualizers | Explicit exploration can expose them, including general compatible candidates, without changing the valid active experience (§§14.6–7). |
| Stale binding | Refresh affected entries and resolve locally or fail explicitly, without incompatible fallback or a repeated per-slot read cascade (§14.5.4). |
| Shared binding | Focus, navigation, edits, and expansion remain independent per live occurrence (§14.5.3). |
| Several owner-issued child requests | Share Rust resolution context and metadata; a request need not cross host/guest, and independent requests can batch (§14.5.4). |

### Open design work and performance accounting

Required behavior is settled above; representation remains open for semantic
activation scope and subject expansion, direct
agent/context access relationships, preference/configuration scopes and index
keys, validity evidence, and consolidated resolution result metadata. Ground
these in the existing schema, Dancer/Dance architecture, and SDK/reference
contracts before naming new relationships or transfer formats. The Experience
Upgrade Session acceptance-versus-durability interaction also remains open.

Track improvements separately:

- **Candidate-selection count:** prepared choices, direct validated defaults, and
  compatible binding reuse eliminate repeated discovery/ranking. A roughly
  one-second-per-selection observation motivates reducing count as well as cost;
  it is not a latency guarantee or a new measurement from this reconciliation.
- **Backend reads:** bulk personal access and reusable metadata/absence indexes
  replace per-property Usage ancestry walks and repeated descriptor/Slot reads.
  Subject data, stale metadata, and uncached executable artifacts can still need reads.
- **Boundary crossings:** shared Rust contexts and batching let owner requests
  resolve locally or near storage. Count useful metadata consumption and remaining
  reads, not just guest calls; references alone may leave the host read cascade.
- **Child activation:** selected owners request only current demand. Preparing a
  default does not open collections, load targets, or explore future navigation.

### Recorded runtime findings, not target-state limits

The previous design recorded host-side selection and live transient Usage
preparation as each component was requested, with a consolidated
`ResolveVisualizerUsage` guest lookup. Its round-local memo shared found and
successful no-Usage answers, deduplicated identical in-flight calls, used selected
Visualizer/actual subject Type/Slot keys, and was bounded to 256 combinations.
It was discarded before background submission; errors were not cached. These
are recorded implementation findings, not the required future index keys or
proof that applicability-scoped Usage reuse and bulk agent/context access are implemented.

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
this operation does not establish that the index or Slot-Usage-first resolution is delivered.

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

The following is the **historical #833 delivery contract** at the inspected
checkpoints. It distinguished default Usage from default selection and superseded
an earlier zero-default-Usage gate in DevDocs PR #78. Its automatic default Usage
creation is now superseded as target design by §11.1; retain this record to explain
what the branch implements. This reconciliation does not edit #833 or PR #846.
The recorded requirements were:

- Missing default Usage is initialized at the selected Visualizer's relevant
  direct applicability type, not automatically at the actual presented subtype.
  For HolonInspector, SpaceNavigator, Book, and Person presentations can share
  the HolonType-scoped default configuration.
- Ordinary rendering examines applicable, eligible Usages associated with its
  Slot before broad discovery. With one, reuse its Visualizer/configuration;
  with several, select within those Usages only; with none, run existing
  selection and reuse or initialize the applicability-scoped default.
- Existing eligibility and configuration ambiguity rules remain. Slot association
  alone grants no eligibility, and unknown lookup failure is not absence.
- Required default/customized Usage creation and updates persist asynchronously
  under the existing startup/gesture batching, coalescing, identity, isolation,
  retry, and failure-status contracts. No save wait belongs on the rendering path.

In that recorded contract, the Usage-first path was a completion requirement for
#833, distinct from pre-session preparation. The inspected PR #846 at `62625dd6` already initializes
from `resolution.default_type` and tests shared defaults across sibling types.
That behavior conformed to the recorded delivery contract; it does not fulfill
the revised sparse-personal-state target. At that inspected baseline, the
ordinary miss path still selected a Visualizer before resolving Usage; retained
exact-request bindings did not establish Slot Usage-first selection. The October
30 checkpoints above implement Slot-Usage-first selection and cross-round pending
revision coalescing. Live gesture/coalescing behavior remains a review gate
separate from the startup and Theme-switch observations recorded above.

The immediate priority is usable application responsiveness during routine
verification, including npm start checks. Bulk agent/context indexing,
service-prepared defaults, and preparing shared bindings before any agent
session remain follow-up work. Agent-initiated experience-design sessions belong
to PR 23.e / DevDocs #68, including their unresolved synchronous-versus-asynchronous
commit acceptance. Retain the accepted supporting code instead of extracting it.

Before closing #833, publish the corrected scope, verify sequential reuse of a
shared default at its applicable configuration scope rather than per presented subtype, test the 0/1/N
Slot Usage paths, and verify coalescing across separate gesture submissions.
Record actual startup/navigation and existing supported replacement timings while
required saves run: broad candidate-discovery counts, Usage lookup/reuse counts,
publication/usable-content time, queue wait, batch size, transaction/attempt counts,
backend duration, and foreground contention. Mocked gates and nominal startup do
not replace live evidence. The October 30 record above supplies targeted startup
and Theme-switch observations; it does not claim a new live gesture/coalescing matrix.

Residual metadata or selection costs outside these gates must be reported but do
not by themselves block #833. A usable associated Slot Usage must avoid broad
candidate discovery, and required saves must not impose a queue/worker/commit
wait. No absolute startup-time target or percentage speedup is established.

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
The recorded #833 contract retains applicability-scoped default Usage, Slot
Usage-first resolution, and asynchronous persistence for that bounded increment.
Automatic Usage creation differs from the revised target and needs subsequent
implementation reconciliation. The session target does not establish bulk indexing
or prescribed-default implementation. These documentation changes do not implement
runtime behavior; the linked GitHub issue records the corresponding delivery scope.

### Documentation acceptance and later runtime validation

The [design behavior checks](#design-behavior-checks-for-subsequent-implementation-grounding)
cover the current target, including a first visit without durable constituent
Usages. Historical #833 gates above describe applicability-scoped default creation,
Slot Usage-first selection, and asynchronous saving in that bounded increment;
they do not replace the revised target. Experience Upgrade Session work belongs
to PR 23.e design reconciliation; shared preselection and bulk indexes remain
foundation work. This does not make every target scenario a prerequisite for #833.

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
