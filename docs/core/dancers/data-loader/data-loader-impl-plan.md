# Load Holons — DAHN Replacement Implementation Plan

## Status and purpose

Historical decomposition authored 2026-10-03, with current reconciliation below.
DL identifiers are local planning IDs, not GitHub PR numbers. Their estimates and
original Planned labels are historical planning evidence, not a new backlog or
claims that already implemented capabilities must be delivered again.

The repository history records the loader integration through
[map-holons PR 791](https://github.com/evomimic/map-holons/pull/791), including the
committed-result inspection and default-entry work in PRs 789/790. The current
working implementation also contains follow-on diagnostic/navigation changes;
source inspection is not merge or runtime-verification evidence for those edits.
No new Delivered Actual estimates or per-DL completion claims are inferred here.

Current shared-inspector and context-routing deltas belong exclusively to
[VC-1 in the integrated plan](../../space-navigator/space-navigator-impl-plan.md#vc-1-coherent-node-assignment-and-shared-genericloader-geometry).
Reuse delivered preparation, invocation, review, and lifecycle mechanisms. Do not
count VC-1 work again in DL-08/DL-12/DL-13 or sum the historical total as remaining
work. Linux mixed selection, formal legacy ingress retirement, and duplicate-head
handling retain their separate scope and delivery evidence.

Deliver the [replacement use case](data-loader-use-case-spec.md) incrementally,
reusing the working Holons Data Loader. `LoadHolons` remains a Dance afforded
by `HolonSpace`. HolonSpace retains semantic ownership; HolonInspector presents
the action in its action bar and delegates request interaction and result
presentation through its Visualizer composition. Space Navigator hosts the
exploration context. This plan does not introduce a Data Loader Dancer, its activation
lifecycle, or a second semantic loading protocol.

Every PR is estimated separately using the MAP Dev Points rubric: 1, 2, 3, 5,
or 8 points. All chunks are below the requested maximum of 13 points. Estimates
are **Planned Dev Points**, not delivered actuals or elapsed-time commitments.

The ownership revision increases DL-07 from 5 to 8 planned points for the reusable
action contract and reduces DL-08 from 8 to 5 by removing Dancer-owned slot work.
That revision left the historical total at 68. DL-10 subsequently increased
from 3 to 5 for structured parser/loading feedback, making the latest recorded
planning total **70** (37 + 30 + 3), matching both tables. Preserve the earlier
68 as history, not the current total or a remaining-work estimate.

## Authority and relationship to other plans

- [Replacement use case](data-loader-use-case-spec.md): intended user flow.
- [Holon Data Loader design](../../holon-data-loader-design-spec.md): parsing,
  assembly, reference resolution, staging, and commit semantics.
- [Dance design](../../dances/dances-design-spec.md): canonical invocation,
  affording HolonSpace, request and response contracts.
- [Commit validation design](../../validation/commit-validation-design-spec.md):
  semantic rejection, staged findings, unattached findings, and persistence outcomes.
- [DAHN design](../../hx/dahn-design-spec.md): slot ownership, selection,
  realization, public SDK boundary, and state survival.
- [Space Navigator design](../../space-navigator/space-navigator-design-spec.md)
  and [interaction grammar](../../space-navigator/space-navigator-interaction-grammar.md):
  enclosing experience ownership and normal inspection.
- [Holon Inspector design](../../hx/visualizers/node/holon-inspector/design-spec.md):
  holon-level action initiation, subject binding, and result composition.
- [Collection kind](../../hx/visualizers/collection/kind-spec.md) and
  [Table Collection design](../../hx/visualizers/collection/table/design-spec.md):
  collection subjects, projection, selection, ordering, and presentation.

This is the detailed decomposition of the replacement currently represented by
[Space Navigator PR 40.a](../../space-navigator/space-navigator-impl-plan.md#pr-40a--space-navigator-load-holons-action-and-legacy-app-retirement).
Its existing 5-point estimate must not be added to this plan's estimate for the
same work. That entry now points to this plan and retains its historical estimate.
Existing delivery history is preserved; new tracking must first subtract delivered
capability and use the integrated VC sequence for the current composition delta.

Load Holons is the first enabled holon-level action. Its implementation establishes
a reusable activation contract for actions discovered from the displayed holon:
bound subject and Dance identity, execution readiness, request preparation, explicit
submission, pending state, and outcome routing. Loader-specific source selection
plugs into that contract. Unsupported actions remain disabled with a reason.
At issue grounding, reuse delivered action capabilities and remove overlap; this
plan does not require forms or execution support for every discovered Dance.

The current enduring ownership/context contracts are resolved in the owning
specifications. DL-01 records the earlier design task, not an open ownership
choice. Subsequent issues sequence the accepted design and qualify historical work. This
plan owns sequencing, scope, validation, and exit criteria, not a competing
semantic authority.

## Historical source-inspection baseline

The initial analysis inspected `map-holons` at `050cb3fc`. Relevant uploader and
SDK entry points were rechecked at `c66467fa` while preparing this plan. These
are source-inspection baselines, not a claim that the running screenshots used
either exact revision or that the full workflow was rerun.

Implementation paths below are relative to the sibling `map-holons` repository:

| Area                   | Existing implementation and planning consequence                                                                                                                                                                                                                                   |
|------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Legacy interaction     | `host/ui/src/app/components/json-data-uploader/` already selects files/directories, retains content, validates JSON/schema, submits, and displays summaries. Extract useful behavior rather than preserving its separate application.                                              |
| Host preparation       | `host/crates/holons_loader_client/src/` constructs a transient `HolonLoadSet` and per-file bundles. Keep parsing and graph construction in host Rust.                                                                                                                              |
| Guest execution        | `happ/crates/holons_loader/src/controller.rs` stages, resolves cross-bundle references, completes values, commits, and returns counts/status/errors. Reuse this pipeline.                                                                                                          |
| Invocation             | `host/map-sdk/src/sdk/transaction.ts` exposes `loadHolons(ContentSet)`; the host path reaches the legacy standalone request in `shared_crates/holon_dance_builders/src/load_holons_dance.rs`. Canonical descriptor-afforded invocation is a migration, not just enabling a button. |
| Existing action        | `host/conductora/resources/dahn-visualizers/actions.js` renders discovered actions but disables all controls. Disabling was deliberate incremental scope. Retain the HolonSpace inspector action placement and enable it through the shared holon-action contract.                                                          |
| Transaction            | The standalone uploader begins a transaction per submission. Preserve load isolation; do not import into Navigator's shared read transaction or implicitly commit unrelated edits.                                                                                                 |
| Status                 | Guest returns `Complete`, `Incomplete`, `Rejected`, and `Skipped`. UI currently infers success from `ErrorCount`, omitting validation findings from that decision.                                                                                                                 |
| Provenance             | Source filename and byte offset already exist. UI submits the basename even when it has a richer display path.                                                                                                                                                                     |
| Descriptor typing      | Response construction does not attach its response descriptor. Error descriptor lookup uses a suffix different from canonical TDL and tolerates lookup failure. Descriptor-driven rendering needs this corrected.                                                                  |
| Result access          | Counts and `HasLoadError` are available. Public committed-member enumeration and complete finding access need work; the loader does not forward the commit's unattached finding collection.                                                                                        |
| Collection realization | Current collection activation is relationship-oriented, and SDK selection takes a parent Visualizer. Extend Visualizer-owned composition for action results; Dancer-owned result slots are not required.                                                                                                              |

The supplied **Current (Deprecated) Holons Loader Flow** archive is UX evidence:
repeated filenames, duplicate validity displays, controls below the viewport,
stale pending text after failure, and successful counts without result browsing.
Its suggestions do not supersede the use case: validate before review, retain
one valid/invalid indication, and defer source-fragment viewing. The reported
WASM `unreachable` failure has not been diagnosed; no root-cause fix is included
in these estimates.

## Delivery assumptions and boundaries

- Reuse the loader engine and existing `HolonLoadSet`, bundle, response, error,
  and validation representations. Do not redesign import syntax or commit.
- Use one dedicated load transaction per submission. Retain its staged state
  for results/findings; closing presentation does not implicitly clear or abandon
  the Nursery. DL-01 specifies ownership and explicit lifecycle operations.
- Source review is request-preparation presentation initiated by the HolonSpace
  action. HolonInspector delegates it through the action interaction contract.
  A separately selected Source Review Visualizer is not a prerequisite.
- The selected LoadHolons response/report Node owns the PropertyMap, Diagnostics,
  and Committed Holons slots under the [resolved composition](data-loader-design-spec.md#81-composition-and-slot-ownership).
  The Action owns workflow lifetime and coordinates context disposal; the shared
  shell owns reusable geometry, not semantic slots. HolonSpace remains the affording
  subject. The experience owns its Rooted Navigation role and load tab, not Node
  result Collection slots. VC-1 migrates existing Action-owned slots and caller
  parent references together; this is not new DL work counted separately.
- Prefer existing Table Collection and normal Holon/RootedNavigation inspection.
  No new VisualizerKind is presumed necessary. Selection and realization errors
  remain explicit; no hard-coded Table fallback is introduced.
- Preserve the use case's mixed files/directories picker goal. DL-05 verifies
  platform support. An interim separate-choice picker must be documented as an
  incomplete capability, not declared equivalent to the target.
- Source bytes validated in review are the bytes submitted. Guest semantic
  validation remains authoritative regardless of preflight success.
- Preserve diagnostic categories. Semantic findings are not reclassified as
  operational `HolonLoadError`s merely to display them in one collection.
- Additional sources, source-fragment display, staged repair, file-grouped errors,
  guest progress subscriptions, and cancellation after submission remain deferred.

## Historical PR decomposition and recorded estimates

These dependencies and Planned labels record the original decomposition. Apply
the current reconciliation and integrated VC dependencies before grounding any
remaining issue; the table is not a claim that all rows remain undelivered.

| PR | Deliverable | Historical phase | Recorded points | Depends on | Rationale | Re-estimate or split if |
| --- | --- | --- | ---: | --- | --- | --- |
| DL-01 | Resolve replacement contracts and plan ownership | Planned | 3 | — | Bounded design reconciliation across existing authorities | General Dancer composition or lifecycle redesign becomes necessary |
| DL-02 | Correct status presentation and response typing | Planned | 3 | DL-01 | Focused producer/consumer corrections with existing outcomes | Response construction requires a broader bootstrap redesign |
| DL-03 | Expose host request preparation through the SDK | Planned | 5 | DL-01 | Host command, binding, SDK, and parser reuse | Preparation cannot be separated from execution without engine changes |
| DL-04 | Invoke canonical LoadHolons through HolonSpace | Planned | 8 | DL-02, DL-03 | Dance dispatch, invocation authority, and transaction lifecycle cross boundaries | Missing generic Dance infrastructure exceeds this concrete adapter |
| DL-05 | Native source ingress and preserved paths | Planned | 5 | DL-01 | Platform integration and deterministic recursive discovery | Mixed selection requires a custom native picker implementation |
| DL-06 | Automatic validation and bounded source review | Planned | 5 | DL-03, DL-05 | Nontrivial review state machine and accessibility | A generic editable-collection framework becomes required |
| DL-07 | First enabled holon action and loading feedback | Planned | 8 | DL-04, DL-06 | Establishes reusable activation, preparation, submission, and result routing through HolonInspector | A universal request-form or action framework becomes necessary |
| DL-08 | Visualizer-owned action-result Collection composition | Planned | 5 | DL-01, DL-02 | Reuses Visualizer ownership while extending collection binding beyond relationship tabs | Existing slot contracts cannot support delegated action results |
| DL-09 | Preserve and expose commit validation diagnostics | Planned | 5 | DL-04 | Guest response, staged findings, and SDK projection | Findings require a new validator or unrelated validation capability |
| DL-10 | Structured parser diagnostics and distinct loading feedback | Planned | 5 | DL-03 | Existing parser issues need structured outward delivery | Parser issue capture must be substantially rewritten |
| DL-11 | Public committed-result reference access | Planned | 5 | DL-04 | Staged membership, saved identity, and read-context binding | Persistence does not retain sufficient committed identity evidence |
| DL-12 | DAHN diagnostic collection presentation | Planned | 5 | DL-07, DL-08, DL-09, DL-10 | Typed projections, ordering policy, and error-first presentation | Generic compound interactive sorting is required |
| DL-13 | Committed collection and normal inspection | Planned | 5 | DL-07, DL-08, DL-11 | Heterogeneous member projection and navigation integration | Result inspection requires a new navigation model |
| DL-14 | Replacement verification and default-entry migration | Planned | 3 | DL-01–DL-13 | Bounded integration evidence and targeted route removal | Any required predecessor capability remains incomplete |
| **Total** | | **Planned** | **70** | | **Largest PR: 8 points** | |

### DL-01 — Resolve replacement contracts and plan ownership

**Historical Planned Dev Points: 3.**

**Scope**

- Reconcile the use case with the existing Dance boundary and source-before-submit
  interaction. Preserve HolonSpace ownership and HolonInspector initiation.
- Specify the reusable holon-action activation contract, including separation of
  semantic availability from implemented execution readiness. Bind the displayed
  holon and selected Dance explicitly; never infer the target from the current
  navigation root. Keep loader-specific request preparation outside generic
  action-bar code.
- Record preparation versus invocation, dedicated transaction ownership, retained
  results, explicit disposal, active-space changes, and dismissal during loading.
- Define outcome mapping, including empty `Skipped` results, rejected validation,
  operational partial persistence, and failure without a usable response.
- Record the result subjects, diagnostic provenance, missing/keyless values, and
  committed-reference handoff. The current Node-owned slot and Action-owned
  workflow boundary is settled in §8.1 of the design, not left to this historical task.
- Keep the Space Navigator PR 40.a cross-reference aligned with this decomposition
  and prevent duplicate planned accounting.

**Exit and validation:** Owning specs contain the enduring decisions and link to
this plan for sequencing. The normal, partial, rejected, parser-failure, and
no-response flows can each be traced to a transaction and presentation owner.
Unresolved platform feasibility remains explicitly assigned to DL-05.

### DL-02 — Correct status presentation and response typing

**Historical Planned Dev Points: 3.**

**Scope**

- Drive success/failure presentation from authoritative `LoadCommitStatus`, with
  operational error and validation-violation counts kept separate.
- Stop presenting a terminal invocation failure as still submitting. Preserve
  structured SDK error details where available instead of showing only a category.
- Attach the canonical response and error descriptors for ordinary runtime use;
  preserve explicitly supported bootstrap behavior without fabricating types.
- Apply corrections to the existing presenter so they benefit the working loader
  before its entry point is retired. Do not clear source/schema state on rejection
  merely because operational error count is zero.

**Exit and validation:** Focused cases cover every status, rejection with zero
operational errors, `NoAction` count differences, unavailable response fields,
and invocation failure. Response/error descriptor lookup agrees with canonical
TDL. This does not claim to fix the archive's underlying WASM failure.

### DL-03 — Expose host request preparation through the SDK

**Historical Planned Dev Points: 5.**

**Scope**

- Extract/reuse host parsing and load-set construction independently of execution.
- Add the minimum public SDK operation and host command/binding support to prepare
  the request in its owning load transaction. Keep wire types internal.
- Preserve the selected source identity and exact reviewed contents in the bundle
  graph. Preparation does not stage imported domain holons or invoke Commit.
- Leave the existing uploader operational while the canonical consumer is built.

**Exit and validation:** A multi-file input produces one correct transient load
set, preserves source provenance, and supports cross-file references for later
resolution. Preparation failure performs no commit. Request references cannot
accidentally cross transaction ownership boundaries.

### DL-04 — Invoke canonical LoadHolons through HolonSpace

**Historical Planned Dev Points: 8.**

**Scope**

- Build and execute descriptor-based `LoadHolons` invocation with the prepared
  request and explicitly bound HolonSpace as affording holon, through the public SDK.
- Connect the canonical guest adapter to the existing loader controller; preserve
  the loader's staging, resolution, value completion, and commit behavior.
- Retain dedicated transaction isolation and existing status-driven terminal/open
  lifecycle semantics. Preserve Nursery evidence after return.
- Retain any infrastructure/bootstrap entry points still required by other
  callers; the replacement UI does not invoke the legacy standalone protocol.

**Exit and validation:** Host/guest integration verifies an afforded invocation,
refusal for an invalid affording subject, successful load, reference-resolution
failure, semantic rejection, and operational incomplete outcome. Existing loader
integration cases remain valid. Unrelated Navigator edits are not committed.

### DL-05 — Native source ingress and preserved paths

**Historical Planned Dev Points: 5.**

**Scope**

- Introduce a reusable host source-selection adapter and verify supported desktop
  platforms' mixed file/directory and multiple-directory selection capabilities.
- Recursively discover directory contents; define deterministic JSON filtering,
  duplicate/overlapping selection, symlink, unreadable-file, and empty-input behavior.
- Retain stable source identity, absolute display path when supplied by the native
  host, and content. Do not manufacture an absolute path from a browser basename.
- Carry paths through preparation rather than substituting `file.name`.

**Exit and validation:** Same-basename files from different directories remain
distinguishable in review and loader provenance. Discovery and cancellation are
verified on supported platforms, with a recorded capability matrix. If mixed
selection needs work beyond this estimate, split a follow-on PR before declaring
the picker goal complete; keep any interim limitation explicit.

### DL-06 — Automatic validation and bounded source review

**Historical Planned Dev Points: 5.**

**Scope**

- Automatically validate after source acquisition using the supported import
  schema; hide schema internals behind optional detail rather than a primary form.
- Implement one scrollable review list with paths, one validity indicator,
  per-file diagnostics, checkboxes, and always-visible actions.
- Select all files when all are valid; otherwise initially select only invalid
  entries. Submission requires at least one selected file and no invalid entries
  anywhere in the list. Removal changes only the request.
- Keep Cancel pre-submission, prevent stale validation results from applying to
  replaced sources, and submit the exact validated contents.

**Exit and validation:** Exercise all-valid, mixed-validity, deselected-invalid,
remove-invalid, no-selection, read/schema failure, and cancellation flows.
Keyboard operation and a long review list preserve access to actions. This
component is not yet a separately selectable Source Review Visualizer.

### DL-07 — First enabled holon action and loading feedback

**Historical Planned Dev Points: 8.**

**Scope**

- Enable Load Holons in the existing HolonInspector action bar through a reusable
  activation interface carrying the bound affording holon, Dance identity, and
  occurrence/invocation context. Retain disabled presentation for unsupported actions.
- Separate generic activation/readiness/pending/outcome handling from the
  LoadHolons-specific source choice and review handler. Activation prepares a
  request; only explicit Submit invokes this Dance.
- Keep HolonSpace as target throughout the flow. No pinned Space Navigator action
  or second independent loader experience is added.
- Present bounded loading and result-summary feedback with elapsed time. Only
  display phase changes actually observed by the client.
- Prevent duplicate submission and stale completion after disposal or context
  changes. Capture the target space; never silently retarget an in-flight load.
- Apply DL-01's dismissal/transaction ownership policy. Closing presentation does
  not masquerade as cancellation after submission.

**Exit and validation:** A user starts from the displayed HolonSpace's action bar
and sees a truthful terminal summary or failure. Pre-submit cancellation does not
invoke the Dance; double activation does not submit twice. A second test action
exercises the same activation interface without loader branches in generic
action-bar code. Unsupported actions remain disabled; invocation uses the captured
affording subject even after navigation changes. Existing navigation survives
the load. Detailed DAHN result browsing follows later.

### DL-08 — Visualizer-owned action-result Collection composition

**Historical Planned Dev Points: 5.**

**Scope**

- Historical delivery established selected result composition. The current target
  assigns its slots to the selected response/report Node. Ownership migration,
  including schema declarations and selector parent inputs, is VC-1 work and is
  not estimated again here.
- Support explicitly described action-result collections beyond relationship tabs,
  with the originating holon and Dance retained as provenance. Preserve the real
  parent Visualizer in selection and mounting; do not add a Dancer ownership
  schema or assign presentation slots to the HolonSpace data subject.
- Supply accepted types, element shape, subject references, Theme, allocation,
  and runtime context; reuse ordinary selection and artifact materialization.
- Keep diagnostic/result occurrence state independent, even in a shared region.

**Exit and validation:** Both slots realize a compatible selected Collection
Visualizer from typed fixture subjects. Invalid ownership, no candidate,
ambiguity, and materialization failure remain explicit. Existing relationship
collection selection still works. Update TDL and regenerate affected resources;
do not hand-edit generated schema imports.

### DL-09 — Preserve and expose commit validation diagnostics

**Historical Planned Dev Points: 5.**

**Scope**

- Preserve access from the load outcome to per-staged-holon validation findings
  and unattached commit findings, including their category, message, rule identity,
  code, severity, and structured subject where supplied.
- Extend the loader response/reference path for unattached findings using existing
  validation carriers and owning schema conventions; do not serialize a report
  into a string property.
- Expose the necessary public SDK reads. Enrich with loader source provenance
  where a reliable association exists; leave unknown locations explicitly absent.

**Exit and validation:** A rejected load with zero `HolonLoadError`s exposes its
actual findings. A finding without a staged carrier remains reachable. Counts
include both destinations without duplication. No new validation rules or repair
workflow are part of this PR.

### DL-10 — Structured parser diagnostics and distinct loading feedback

**Historical Planned Dev Points: 5.** Original parser-only estimate: 3; expanded to include
the distinct pending presentation and retry/lifecycle verification approved in #785.

**Scope**

- Preserve existing `ImportFileParsingIssue` records across the public boundary
  instead of exposing only a concatenated `LoaderParsingError` message.
- Carry source identity, issue category, message, and location when available.
  Support diagnostics produced before a load-set member or staged holon exists.
- Provide typed diagnostic subjects/projections compatible with the result
  contract, reusing existing types where their semantics fit.
- On submit, transition the neighboring load tab from source review to a distinct
  “Load in progress” view. Replace review controls with a prominent indeterminate
  loading indicator, “Loading holons…” text, submitted file count, and elapsed
  time. Do not imply measured progress or cancellation support that execution
  does not provide. On completion, replace the pending view with the authoritative
  outcome (complete, rejected, incomplete, skipped, or execution failure).

**Exit and validation:** Malformed JSON and structurally invalid input produce
actionable file diagnostics without invoking Commit. Multiple-file diagnostics
remain distinguishable. UI code does not parse human-readable error strings to
recover semantic fields. Submission visibly replaces the review form; pending
feedback remains accessible and transitions to the result on success or failure.

### DL-11 — Public committed-result reference access

**Historical Planned Dev Points: 5.**

**Scope**

- Expose this load's committed members through the public reference/SDK boundary,
  using retained staged state and authoritative committed IDs.
- Bind resulting saved identities into the applicable read context and obtain
  keys from committed state. Do not seed saved properties from staged maps.
- Preserve concrete member descriptors while providing a common collection shape
  suitable for heterogeneous imported holons, including keyless members.
- Support successful members after incomplete persistence. Distinguish committed
  node identity from complete relationship persistence and from `NoAction` entries.

**Exit and validation:** Multiple loads do not contaminate each other's result
membership. References retrieve committed properties, including when staged
properties differ. Missing key/retrieval failures remain display/access failures
without rewriting the load outcome. No persistent load-session schema is required
under the dedicated-transaction assumption.

### DL-12 — DAHN diagnostic collection presentation

**Historical Planned Dev Points: 5.**

**Scope**

- Bind operational loader errors, parser diagnostics, and semantic findings into
  a flat collection with a shared effective display shape and preserved categories.
- Present source holon key where known, message, source file, and location. Do not
  substitute a generated error-holon key for the offending subject's key.
- Reuse a compatible Table realization. Add a bounded default-order contract for
  source path, coordinate representation, then numeric coordinates, with missing values last and stable ties.
  This must coexist with Table's current Key/Sequence defaults and saved user sort.
- Give diagnostics primary attention on partial/failing outcomes. Keep summary,
  navigation, and actions reachable within the available allocation.

**Exit and validation:** Mixed diagnostic categories render without a staged
subject requirement. Ordering compares locations numerically, survives switching
between result roles, and does not mutate membership. Selection/realization
failure retains accessible failure feedback. Full interactive multi-column sorting
and source-fragment display are excluded.

### DL-13 — Committed collection and normal inspection

**Historical Planned Dev Points: 5.**

**Scope**

- Bind committed results into the selected Collection Visualizer on success and
  offer the same collection as a secondary view after partial persistence.
- Route selected members to existing MAP-backed Node/RootedNavigation inspection
  with correct read-context binding and preserved source/result context.
- Refresh affected normal Navigator reads through supported public APIs, without
  recreating the whole experience or using stale cached membership as fresh state.
- Preserve independent selection, sort, and scroll state for diagnostics/results.

**Exit and validation:** Loaded holons can be inspected for committed properties
and relationships; heterogeneous and keyless members remain usable. Returning
to results preserves view state. A failed member read is distinguishable from a
failed import. Existing Navigator explorations remain intact.

### DL-14 — Replacement verification and default-entry migration

**Historical Planned Dev Points: 3.**

**Scope**

- Verify the replacement against the coverage matrix and record remaining platform limitations.
- Route the app-internal `/load-holons` entry into the new Canvas/Space Navigator loader.
  Always bind to the active HolonSpace, never prompt or select a substitute.
  Report no active Space or an unavailable required action explicitly.
- Retain the old loader at `/load-holons-deprecated`. Formal legacy ingress
  retirement is separate work; do not remove the old wrapper, uploader, or
  infrastructure in this unit.
- Preserve the existing afforded action, selected Visualizers, and transaction
  ownership. Block route departure during active submission.
- Update documentation and verification status. Linux mixed selection (#780)
  does not block this milestone; duplicate-schema handling remains separate.

**Exit and validation:** The default loader entry uses the active HolonSpace's
canonical afforded action. The deprecated route remains usable. Replacement
verification records precise evidence and limitations. Any underlying WASM crash
requires a separately grounded fix and estimate.

## Milestones and coverage

Milestone points sum the latest historical PR estimates (70), not remaining
work, Delivered Actuals, or separately estimated milestones.

| Milestone | PRs | Points | Visible capability |
| --- | --- | ---: | --- |
| First enabled holon action | DL-01–DL-07 | 37 | HolonSpace action, reusable initiation contract, reviewed sources, truthful feedback |
| Complete DAHN outcome inspection | DL-08–DL-13 | 30 | Flat diagnostics, committed collection, normal inspection |
| Default-entry migration | DL-14 | 3 | Verified replacement; legacy route retained for separate retirement |
| **Total** | **DL-01–DL-14** | **70** | |

| Use-case capability | Primary PRs | Required evidence |
| --- | --- | --- |
| Entry and affording HolonSpace | DL-04, DL-07 | Existing HolonInspector action, reusable activation, explicitly bound target |
| Source choice and discovery | DL-05, DL-07 | Native selection, recursive discovery, distinguishable paths |
| Validation and review | DL-03, DL-06 | Automatic preflight, invalid-first selection, all-invalid-removed gate |
| Canonical submission | DL-03, DL-04 | Reviewed contents become one request; canonical afforded invocation |
| Loading and cancellation | DL-06, DL-07 | Visible elapsed time, truthful transitions, pre-submit cancellation only |
| Full success | DL-02, DL-11, DL-13 | Correct outcome and saved-reference collection/inspection |
| Partial persistence | DL-02, DL-09, DL-11–DL-13 | Errors first; known committed members remain inspectable |
| Semantic rejection | DL-02, DL-09, DL-12 | Zero-write rejection and findings even with zero loader errors |
| Parser/no-response failure | DL-02, DL-10, DL-12 | Diagnostics without a staged carrier; terminal failure clears pending state |
| Nursery retention | DL-01, DL-04, DL-11 | No implicit clear on commit or presentation close; committed reads remain distinct |
| Default-entry migration | DL-14 | End-to-end coverage; active-Space binding and deprecated route retained |

## Validation and re-estimation policy

Each implementation PR runs the narrow checks appropriate to its boundary:
host/SDK unit tests and type checks for preparation and projection, hApp/WASM
checks for shared or guest changes, loader/Dance integration tests for execution,
and UI interaction tests plus visual/manual inspection for bounded presentation
and native dialogs. Tests should prove behavior and boundary invariants rather
than duplicate implementation structure.

Ground each PR against the implementation and its prerequisites before creating
its GitHub issue. Reuse newly delivered work rather than counting it again.
Record estimate changes explicitly; preserve any historical Defined estimate
and Delivered Actual. If a discovery makes a PR exceed 13 points, split it into
independently reviewable PRs before implementation. Under the current rubric,
work larger than a coherent 8-point unit should normally be decomposed rather
than assigned a new 13-point category.


## Shared inspector composition follow-up

The [integrated bounded refactor](../../space-navigator/space-navigator-impl-plan.md#22-bounded-visualizer-composition-refactor)
is the sole delivery home for the loader's adoption of Visualizer Operators,
capability assignment, selected chips PropertyMap, and shared inspector geometry.
Keep diagnostic evidence, committed-review membership, outcome defaults, and
bound transaction ownership in specialized bindings. This supersedes earlier
no-rail result presentation, not loader execution or reference semantics. It is
a documentation proposal, with enhancement creation and implementation deferred
until design acceptance. Existing DL estimates and delivered work are unchanged.


## Current composition/context migration evidence

The inspected executable schema still gives `LoadHolons.ActionVisualizer` the
Diagnostics/Committed slots and gives `LoadHolons.NodeVisualizer` no `HasSlot`
composition declaration. `ActionResultCollections` selects with the Action as
parent while the specialized Node receives injected children. VC-1 must migrate
all three result/presentation slots to the Node with its materialized composition
roles and real selector parent inputs; a shared shell does not become a slot owner.

`LoadDiagnosticPresentation` already owns an open presentation transaction;
`openCommittedReview()` requires a returned canonical response and creates a
separate saved-state review. Current result-root initialization awaits review,
and `SpaceNavigatorExperience.presentResult` routes L-owned subjects to L and
assumes other targets belong to its second supplied context. These are migration
limitations, not target promises. Reuse/expose the existing P as the realization
capability independently of R; route actual L/P/R-owned references explicitly.
Unknown or unsupported ownership yields a local unavailable-inspection result,
not guessed rebinding. No new core reference/transaction protocol is required.

Acceptance for VC-1 must cover parser failure without R, no-response failure,
Complete retained L reads with open P materialization, partial Saved staged
subjects, review-init failure preserving summary/diagnostics, singular response
target ownership, unsupported ownership, and dependency-ordered disposal with
pending reads/materialization. Preserve source-review guards and duplicate-submit
prevention. These tests qualify migration behavior, not new loader execution work.
