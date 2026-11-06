# Dance regression after prepared relationship metadata reuse

The same three ordinary dance suites passed on 2026-11-06: **41 fixtures completed**,
three top-level tests passed and twelve focused selectors ignored. The command runs
only the prior measured dance scope, without the rest of `npm test`. Existing fixture
assertions were unchanged and temporary MatchSavedContent timing probes were absent.

## Comparable fixture totals

Fixture durations exclude builds, conductor/bootstrap, setup and teardown. All three
captures use the same timestamp collector and serial dance runner. Original timings
are from [dance-timings.txt](dance-timings.txt); the previous rerun includes source-wide
bulk retrieval and bounded rejection assertions. This rerun adds prepared relationship
metadata reuse, including the descriptor-source ancestry safeguard.

| Suite | Fixtures | Original | Bulk retrieval | Prepared reuse | Change from bulk |
| --- | ---: | ---: | ---: | ---: | ---: |
| pristine_bootstrap_and_loader | 2 | 522.736s | 536.289s | 551.515s | +2.8% |
| query_storage_boundaries | 2 | 30.719s | 32.318s | 32.463s | +0.4% |
| runtime_behavior_matrix | 37 | 2044.844s | 515.076s | 504.492s | -2.1% |
| **All fixtures** | **41** | **2598.299s** | **1083.683s** | **1088.470s** | **+0.4%** |

Dance test-binary duration: **1470.11s**. Whole narrower command including build,
audit and compilation: **1509.508s** (previous narrower command: 1517.120s).
The original 7874.427s npm command included other tests, so it is not comparable.

Across the same **30 MatchSavedContent steps**, total time fell from **80.682s**
to **56.483s** (-30.0%). Combined fixture time was effectively
unchanged (+0.4%). The broad ValidationBindings/inverse scan rose from 456.633s to
468.983s, and graph/version anchoring rose from 78.618s to 85.523s. A single rerun
does not distinguish ordinary variance from a repeatable regression in those steps.

Bootstrap guest load/commit samples: 91.358s, 88.959s, 92.027s.

## Fixture comparison

| Suite / Fixture | Bulk retrieval | Prepared reuse | Change |
| --- | ---: | ---: | ---: |
| pristine_bootstrap_and_loader / bootstrap_operational_schema | 534.546s | 549.626s | +2.8% |
| runtime_behavior_matrix / Simple StageNewVersion Testcase | 103.418s | 109.493s | +5.9% |
| runtime_behavior_matrix / load_book_person_inverse_schema | 52.664s | 51.289s | -2.6% |
| runtime_behavior_matrix / Book v1 and Title v2 exact references | 42.334s | 42.527s | +0.5% |
| runtime_behavior_matrix / Commit non-root lineage and independent clone | 35.776s | 33.376s | -6.7% |
| runtime_behavior_matrix / Schema successor membership history | 31.103s | 32.061s | +3.1% |
| query_storage_boundaries / query_qry1_scaffold | 23.637s | 23.647s | +0.0% |
| runtime_behavior_matrix / Cross-schema dependency coverage gap | 17.734s | 18.572s | +4.7% |
| runtime_behavior_matrix / Commit distinguishable same-key results | 17.988s | 18.498s | +2.8% |
| runtime_behavior_matrix / Graph-only siblings RemovalConflict | 16.352s | 16.247s | -0.6% |
| runtime_behavior_matrix / Historical key uniqueness | 12.125s | 13.235s | +9.2% |
| runtime_behavior_matrix / Commit branches across transactions | 13.715s | 12.541s | -8.6% |
| runtime_behavior_matrix / Commit sequential lineage | 13.921s | 12.151s | -12.7% |
| runtime_behavior_matrix / Graph-only siblings GraphThenVersion | 11.823s | 10.883s | -7.9% |
| runtime_behavior_matrix / Graph-only siblings VersionThenGraph | 11.412s | 10.562s | -7.4% |
| runtime_behavior_matrix / Commit version-producing siblings | 11.481s | 9.821s | -14.5% |
| runtime_behavior_matrix / Graph-only siblings Identical | 9.411s | 9.528s | +1.2% |
| runtime_behavior_matrix / Commit no-op and graph-only siblings | 9.546s | 9.386s | -1.7% |
| runtime_behavior_matrix / Graph-only siblings Disjoint | 9.652s | 9.356s | -3.1% |
| query_storage_boundaries / query_boundary_data | 8.681s | 8.816s | +1.6% |
| runtime_behavior_matrix / Commit mixed dispositions | 8.541s | 8.689s | +1.7% |
| runtime_behavior_matrix / Commit unchanged update | 7.917s | 7.846s | -0.9% |
| runtime_behavior_matrix / frozen_member_head_redirect_cross_tx | 8.164s | 7.210s | -11.7% |
| runtime_behavior_matrix / smartlink_commit_cache | 10.111s | 7.091s | -29.9% |
| runtime_behavior_matrix / Commit validation correction | 8.335s | 6.905s | -17.2% |
| runtime_behavior_matrix / Commit strict described membership | 6.471s | 6.643s | +2.6% |
| runtime_behavior_matrix / Staged Schema dependency cycle | 6.595s | 6.523s | -1.1% |
| runtime_behavior_matrix / stage_new_from_clone | 8.123s | 6.460s | -20.5% |
| runtime_behavior_matrix / Transaction Lifecycle Test | 5.691s | 4.878s | -14.3% |
| runtime_behavior_matrix / Attachment defaults persist | 4.659s | 4.734s | +1.6% |
| runtime_behavior_matrix / frozen_member_head_redirect | 6.201s | 4.692s | -24.3% |
| runtime_behavior_matrix / Simple AbandonStagedChanges Testcase | 4.979s | 4.362s | -12.4% |
| runtime_behavior_matrix / Simple Create/Get Holon Testcase | 3.506s | 3.490s | -0.5% |
| runtime_behavior_matrix / load_inverse_oriented_book_person_instances | 3.313s | 3.440s | +3.9% |
| runtime_behavior_matrix / DeleteHolon Testcase | 1.934s | 1.925s | -0.4% |
| pristine_bootstrap_and_loader / Loader Incremental Fixture | 1.743s | 1.889s | +8.4% |
| runtime_behavior_matrix / Simple Add / Remove Related Holon Testcase | 0.078s | 0.076s | -2.6% |
| runtime_behavior_matrix / Simple Add / Remove Holon Properties Testcase | 0.000s | 0.000s | +35.5% |
| runtime_behavior_matrix / cross_transaction_staged_target_diagnostic | 0.000s | 0.000s | -16.6% |
| runtime_behavior_matrix / Ergonomic Add / Remove Holon Properties Testcase | 0.000s | 0.000s | -14.3% |
| runtime_behavior_matrix / Ergonomic Add / Remove Related Holons Testcase | 0.000s | 0.000s | +0.0% |

## Remaining longest steps

Steps are inferred from successive existing START/END markers, including boundary and
logging overhead. Repeated step labels are separate occurrences.

| Suite / Fixture / Step | Seconds |
| --- | ---: |
| pristine_bootstrap_and_loader / bootstrap_operational_schema / Verify ValidationBindings descriptor contract and inverse traversal | 468.983 |
| runtime_behavior_matrix / Simple StageNewVersion Testcase / Verify graph-only and version-producing relationship anchoring | 85.523 |
| pristine_bootstrap_and_loader / bootstrap_operational_schema / Verify core schema descriptors | 36.652 |
| runtime_behavior_matrix / load_book_person_inverse_schema / Verify forward and inverse Book/Person instance SmartLink traversal | 34.445 |
| pristine_bootstrap_and_loader / bootstrap_operational_schema / Verify core schema command affordances | 17.585 |
| runtime_behavior_matrix / Book v1 and Title v2 exact references / Commit [expected_status: Rejected, expected_error: None, candidates: [], retry_participants: []] | 15.587 |
| pristine_bootstrap_and_loader / bootstrap_operational_schema / Verify core schema value semantics | 15.381 |
| runtime_behavior_matrix / Book v1 and Title v2 exact references / Commit [expected_status: Rejected, expected_error: None, candidates: [], retry_participants: []] | 13.017 |
| runtime_behavior_matrix / Cross-schema dependency coverage gap / Commit [expected_status: Rejected, expected_error: None, candidates: [], retry_participants: []] | 12.381 |
| query_storage_boundaries / query_qry1_scaffold / Direct seam with one explicit input member: Pending -> Failed, NotImplemented | 10.106 |
| runtime_behavior_matrix / Graph-only siblings RemovalConflict / Commit [expected_status: Rejected, expected_error: None, candidates: [], retry_participants: []] | 9.453 |
| pristine_bootstrap_and_loader / bootstrap_operational_schema / Verify core schema descriptor subtypes | 8.767 |
| runtime_behavior_matrix / load_book_person_inverse_schema / Verify Book/Person descriptors over loaded schema | 8.575 |
| runtime_behavior_matrix / Historical key uniqueness / Commit [expected_status: Rejected, expected_error: None, candidates: [], retry_participants: []] | 7.474 |
| runtime_behavior_matrix / Commit strict described membership / Commit [expected_status: Rejected, expected_error: None, candidates: [], retry_participants: []] | 6.474 |

## Interpretation and limits

This is one complete regression rerun, not a controlled multi-sample benchmark.
Shared schema/cache state, fixture order and ordinary runtime variance affect
per-fixture results. It supplies regression evidence for the existing lineage,
exact-version, clone, inverse, graph-update, rejection/retry, bootstrap and query
assertions. It does not add new correctness contracts or prove behavior beyond the
assertions exercised. The earlier bounded-rejection change is already present in
both narrower reruns; its effect is not new to this comparison.

The [isolated phase capture](prepared-relationship-reuse-profile.md) measures the
specific two-root retrieval change more directly: 5.104522s to 0.148242s, with cold
descriptor acquisition essentially unchanged. Broad suite timings need not reproduce
that magnitude because many steps perform named reads, descriptor-source policy
binding, or other work outside the optimized complete-read path.

## Evidence and reproduction

Historical raw logs are no longer available locally where indicated in the JSON;
those comparisons use their retained DevDocs timing summaries (millisecond precision).
Historical step lists from those summaries include only their slowest 30 steps.
The current run retains its full log and step list.

- [Raw timing summary](dance-timings-prepared-relationships.txt)
- [Machine-readable timing data](dance-timings-prepared-relationships.json)
- [Previous bulk comparison](dance-timings-bulk-relationships-comparison.md)
- Full log: `.notes/test-profiles/20261106T183748Z-d24a6e5c/console.log` in map-holons.
- Temporary-storage wrapper log: `/private/tmp/map-holons-dance-prepared-regression/run-w3CqExgB/test.log`.

```sh
nix develop --command env MAP_TEST_RUN_ROOT=/private/tmp/map-holons-dance-prepared-regression \
  python3 .notes/profile-dance-tests.py -- bash scripts/test-run.sh npm run sweet:dance
```

The entrypoint rebuilds production DNA and probe WASM, audits production artifacts,
and selects only `dance_tests --test-threads=1 --nocapture`. The collector selects
the same targeted INFO logging and arm64 Node runtime as the previous capture.
