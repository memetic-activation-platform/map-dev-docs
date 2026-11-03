# Step A — scoped interpretation guards and shared diagnosis

**Matched capture completed:** clean map-holons `ced364a4`, four workloads × six samples.
[The analysis](analysis.md) verifies unchanged package demand and removed readiness, but records
slower preparation and no backend/node-read reduction. This is not a performance-win sign-off.
The full comparisons and source/raw-log hashes are in [comparison.json](comparison.json).

## Historical implementation attempt

Implementation base: map-holons `372747e8b2e73d533a1837af19bb10cd9c4867c3` (characterization).
The historical sandbox attempt used a working-tree build labeled
`372747e8-step-a-working-tree` because the sandbox denied creating `.git/index.lock`.
That label is not a committed revision. Its failed capture retains the original source label,
artifact metadata and working-tree patch. The review-corrected implementation was subsequently
committed as `ced364a40b0d6e74cbedcfdf45d29158957f0b30`; use that revision for the matched
checkpoint's source. Redundant source copies have been removed from this evidence directory.

The reviewed decision remains DevDocs PR #80 (`e23c4dd`, approved `1d9865d`). This checkpoint
uses the current foundation, guest cache 10,000, existing Session snapshot transport and the
unchanged affected-Schema snapshot bypass. No registry index, frozen scope, DerivedDescriptor
adoption, package-demand narrowing or property interpretation migration is included.

## Changes and attribution

- Removed `commitment_order`, reverse acceptance propagation, post-hoc peer blocking,
  package acceptance states/finish and the unused general dependency-group module.
- Graph-only overlap checks all declared relationship identities for the requested name before
  selecting a binding; conflicting identities or unnamed declarations fail closed. An added test
  covers this previously untested guard, reversing participants and forbidding saved population
  reads. Repeated contributions of the same identity do not become name ambiguity.
- One assessment-scoped structural memo shares exact-definition diagnoses across candidate kind
  preparation, fresh package computation, supporting contracts and constraint declarations. Snapshot
  restoration itself performs no eager structural diagnosis; later consumers reuse any diagnosis
  required for their checks. Fresh products
  use the kernel's existing `from_valid_lineage`; the saved-restoration decision is unchanged.
  Direction classification can consume a diagnosed lineage through the same kernel classifier.
  BindingRoleMemo's fallback and subject value interpretation remain Step C consumers.
- Universal contracts use prepared contributions of the exact reached meta-type. Constraint
  declarations project effective and parent obligations from prepared products, retaining occurrence
  identity and provenance rather than calling `ConstraintContributions::resolve` again.
- Contract vocabulary ambiguity/unnamed members block only the affected candidate's traversal.
  A property's unusable category or ValueType blocks only its affected checks; usable requiredness
  and sibling checks continue. Repetition and unrelated vocabulary findings still reject without
  becoming general prerequisites. Saved supporting defects retain one aggregate per exact governor.
- Staged descriptor defects without an available compatible bound handler receive a candidate-local
  explaining finding. This replaces the scheduler's rejection fallback; it does not add acceptance
  dependence on another candidate. Universal prerequisites retain their established diagnostic codes.
- Supporting contracts and bounded Schema checks run before staged definition assessment, followed
  by remaining candidates in input order. Stable contribution traversal and candidate-specific
  routing remain intact.
- `authored_targets` and its saved-subject derivation branch were removed. Commit's production
  subject set is staged; the gate explicitly requires a staged subject and sorts every populated
  authored relationship name, including undeclared names, preserving occurrence attribution without
  an IsDefinitional filter. The saved branch was unreachable: **no latency claim for deleting it**.

The discovery queue, role-specific edge lists, source decision and cache capacity are unchanged.
`broad-preparation` requires package discovery counters and forbids readiness discovery/grouping
spans and readiness edges. It cannot be labeled `declared-demand`. `InterpretationGuards` observes
candidate guard lookup/decisions; supporting defect-fact generation remains within ContractChecks.
Member-local guard branches are within ordinary subject evaluation. These costs are not relocated
into a claim of reduced preparation demand.

## Behavior controls

Kept characterization tests were updated in place:

| Scenario | Step A behavior |
| --- | --- |
| Owning Schema cycle | DS-SCHEMA-001 remains on owner; Component receives no UnresolvedLocalDependency and runs its checks |
| Saved predecessor beside invalid successor | Exact saved consumer stays valid; explicit successor consumer runs against its usable contract without a generic readiness blocker |
| Referenced staged descriptor ownership failure | Descriptor has its own SchemaOwnership finding; consumer reports its own required-property failure, with no propagated blocker |
| Malformed governing lineage | Every consuming candidate gets an explaining finding; no incomplete candidate is Validated |
| Unusable Title ValueType, absent Title, invalid Key | Requiredness and Key kind checks run; absent values get no value blocker. With optional Title and a corrected Key, the candidate validates while the saved-governor aggregate still rejects the Commit independently. Populating Title activates the scoped value blocker |
| Mutual describing peers | Both products proven usable; only B's missing required Title rejects; A validates in both candidate orders |
| DS-KEY-006 on a referenced new definition | Claimant rejects; dependent runs independently, without general result propagation |
| Malformed candidate lineage | Cycle and multiple parents retain DS-STRUCT-003 / DS-STRUCT-002 attribution |
| Required backend failure | Existing operational failure and prior-outcome preservation controls remain passing |

Existing alias/outcome tests additionally prove one shared diagnosis for saved/no-op/graph-only
aliases without merging their outcomes. The abstract descriptor boundary test independently observes
zero assessment-time structural, contract-contribution and constraint-contribution resolutions for
its fixture, alongside zero backend reads. This is not a claim that Step C's broader zero-derivation
guarantee is complete.

No incidental membership fault controls were removed: broad acquisition remains. The three sampled
read-removal controls and complete before/after inventory comparison remain Step C work.

## Verification

- holons_validation: 140 passed, 2 temporary evidence tests ignored (three dependency-group-only
  tests retired with the scheduler helper).
- holons_core: 621 unit tests passed; one doc test passed, five documentation examples ignored.
- Measurement parser: 30 tests passed, including matching Step A labeling, retained broad package
  counters, historical readiness completeness and rejection of readiness records in the new substrate.
- `npm run fmt:check` and `npm run check`: passed (native, hApp/WASM and web typecheck).
- Profiled hApp/WASM build and packing: passed.
- Sweettest regression gate including `runtime_behavior_matrix`: user-run, still required.

## Capture protocol

Only the bounded subset: usage, no-op, mixed, shared-type; one run of six samples each. Retain
`MAP_SWEET_STARTUP_TIMEOUT_SECS=60`, matching the capacity checkpoint. Each workload asserts its
own outcome. Compare against `../cache-10000-checkpoint/`, not the historical 99-entry latency.
Report sample index 1 separately and keep actual received registry conditions.

The standard performance script runs inside Nix. In this sandbox the Nix fetcher cache is set to
`XDG_CACHE_HOME=/private/tmp/map-822-nix-cache`; this only changes the development-shell cache
location. Capture arguments are `--runs 1 --samples 6 --preparation-substrate broad-preparation`,
with both source labels set to `372747e8-step-a-working-tree`. Usage uses `--mode create`,
shared-type adds `--subjects 8`, and the others select `--mode no-op` / `--mode mixed`.

## Observed capture status

The user completed [matched/](matched/) at clean revision
`ced364a40b0d6e74cbedcfdf45d29158957f0b30`, using artifact SHA-256
`2ff1f58481bacc2692024c33735e4c376fbbc497c952e7ec3993c8db1faa8a07`.
All 24 samples pass parser checks; every workload test succeeded. The source and artifact
revision labels agree. Every sample matches the capacity checkpoint's package edge counts,
prepared products and actual registry conditions. Readiness observations are absent.

The earlier sandbox attempt in `usage/` remains historical environment evidence: iroh could not
create its network monitor before sampling. Its source label and artifact are not the matched
capture. The committed revision above is the source authority for the matched captures. [capture-status.json](capture-status.json) retains that failed attempt
separately from current results.

Commit and bounded-capture exit conditions are now recorded. The analysis exposes higher full
structural-diagnosis work and slower preparation; do not infer improved latency from removed
readiness or zero schema-resolution counters. Full Sweettest regression results including
`runtime_behavior_matrix` have not been supplied here. No Step C preparation changes were started.

Run [capture-subset.sh](capture-subset.sh) from map-holons inside `nix develop` after committing the
implementation, providing a new output directory (for example this directory's `matched/`). It
builds once, retains the startup allowance, and captures exactly one run of six samples for the
four required workloads; it stops on the first failed workload. Keep the failed `usage/` attempt
as environment evidence rather than overwriting it.

## Review corrections before the user-run capture

- Value usability guards run only for present values. Tests cover optional/required absence,
  an independently invalid sibling, and the same contract with a present value. A saved supporting
  aggregate remains independent of whether a particular consuming candidate has a value to assess.
- Snapshot restoration skips eager diagnosis. A focused restoration-error control observes one
  registry hit/restoration attempt and zero structural diagnoses or fresh builds.
- Constraint contribution projection requires a valid lineage; invalid invocation is InvalidState.
  Authored cycle/multiple-parent products retain typed CyclicExtends/MultipleExtends errors instead
  of being represented as missing preparation. Tests assert both boundaries.
- Fresh diagnosis fallbacks are compiled only in tests. Production without a supplied shared store
  returns an explicit missing-preparation error.
- Effective-schema assessment returns interpretation facts into the single exact-definition map.
  Rule products carry diagnostics, not another copy of those facts; member keys use DefinitionIdentity.
- Declared relationship names are skipped before member enumeration; undeclared occurrences retain
  sorting and attribution. Graph-only name conversion is done once per requested name.
- Scenario names now describe independent assessment, and the Schema-cycle test positively observes
  the component's own required-property check.

The historical source snapshot was refreshed for these corrections. The user subsequently rebuilt
and captured the committed implementation in `matched/`; the sandbox-failed attempt remains separate.

## Diagnosis scope correction

Step A shares only structural diagnoses already required by its consumers. Other reached package
definitions keep the original effective-schema resolver. Vocabulary category and direction
classification reuse valid evidence when present and otherwise retain the original classifiers,
including their short-circuit behavior; classification does not depend on memo population.
The implementation plan’s goal of kind and role classification without repeated lineage discovery
is completed in Step C, not Step A.

Regression controls: `vocabulary_classification_is_independent_of_defective_memo_entries` compares
classification, findings and backend reads with and without defective memo entries above category
anchors; `structural_memo_lookup_preserves_absence_and_required_read_failure` verifies lookup does
not compute or hide a stored read failure. The existing
`profiling_observes_preparation_without_changing_the_validation_report` checks preparation work
counts. Kept characterization assertions are unchanged. Unit tests now construct their shared store
explicitly. `abstract_descriptor_universal_contract_needs_no_backend_reads_after_construction`
retains its zero-backend-read and zero-contribution-resolution assertions, and now asserts exactly
nine assessment-time structural diagnoses: structural member checks no longer inherit diagnoses created
incidentally for every package definition. Those required member checks may diagnose during Step A
assessment; eliminating assessment-time diagnosis remains Step C work.

The trace-on checkpoint and trace-off diagnostic results remain historical captures of their
original source revisions. This correction takes no performance captures and includes no trace
change.

Saved-only unit fixture work counts (`profiling_observes_preparation_without_changing_the_validation_report`),
measured with clock-free probes on `ced364a4` and the cleanup working tree:

| Work | Before | After |
| --- | ---: | ---: |
| Prepared definitions / constructed products | 19 / 19 | 19 / 19 |
| Package edge requests | 188 | 188 |
| Schema builder attempts / successes | 19 / 19 | 19 / 19 |
| Name-index builds | 59 | 59 |
| Structural diagnoses during product preparation | 17 | 0 |
| Structural diagnoses across assessment | 19 | 6 |
| Effective-schema resolver calls | 0 | 17 |

The fixture asserts the stable package/product/edge counts and zero diagnoses initiated by product
preparation. Resolver count follows the exact identities already diagnosed, so it is observed rather
than fixed as a target. These are unit work observations, not new performance captures.
