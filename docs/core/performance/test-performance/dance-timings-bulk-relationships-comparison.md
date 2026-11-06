# Dance suite regression and timing comparison

The three ordinary dance suites passed on 2026-11-06: **41 fixtures completed**, with
three top-level tests passed and twelve focused diagnostic selectors ignored, as intended.
This reruns the dance scope captured in [the original timing baseline](dance-timings.txt),
without running the rest of `npm test`. No test code or assertions were changed for this run.

## Comparable fixture timings

Fixture durations exclude bootstrap, suite setup/teardown, builds, and compilation.
Both reports use the same existing timestamp collector and serial dance runner.

| Suite | Fixtures | Baseline | Current | Change |
| --- | ---: | ---: | ---: | ---: |
| pristine_bootstrap_and_loader | 2 | 522.736s | 536.289s | +2.6% |
| query_storage_boundaries | 2 | 30.719s | 32.318s | +5.2% |
| runtime_behavior_matrix | 37 | 2044.844s | 515.076s | -74.8% |
| **All fixtures** | **41** | **2598.299s** | **1083.683s** | **-58.3%** |

The baseline’s 131-minute whole command included builds and other tests. The new
command runs only dances, so those whole-command times are not comparable.

The dance test binary completed in **1476.70s (24m 36.7s)**. The complete narrower
command, including builds, artifact audit, and compilation, took **1517.12s (25m 17.1s)**.
Bootstrap load/commit samples were 87.923s, 91.314s, and 95.688s. Additional query
contract assertions run outside the fixture timing markers and also passed.

## Fixture detail

| Suite / fixture | Baseline | Current | Change |
| --- | ---: | ---: | ---: |
| pristine_bootstrap_and_loader / bootstrap_operational_schema | 521.091s | 534.546s | +2.6% |
| runtime_behavior_matrix / Simple StageNewVersion Testcase | 230.790s | 103.418s | -55.2% |
| runtime_behavior_matrix / load_book_person_inverse_schema | 66.501s | 52.664s | -20.8% |
| runtime_behavior_matrix / Book v1 and Title v2 exact references | 183.422s | 42.334s | -76.9% |
| runtime_behavior_matrix / Commit non-root lineage and independent clone | 244.248s | 35.776s | -85.4% |
| runtime_behavior_matrix / Schema successor membership history | 135.627s | 31.103s | -77.1% |
| query_storage_boundaries / query_qry1_scaffold | 22.610s | 23.637s | +4.5% |
| runtime_behavior_matrix / Commit distinguishable same-key results | 103.971s | 17.988s | -82.7% |
| runtime_behavior_matrix / Cross-schema dependency coverage gap | 123.738s | 17.734s | -85.7% |
| runtime_behavior_matrix / Graph-only siblings RemovalConflict | 93.311s | 16.352s | -82.5% |
| runtime_behavior_matrix / Commit sequential lineage | 76.393s | 13.921s | -81.8% |
| runtime_behavior_matrix / Commit branches across transactions | 69.933s | 13.715s | -80.4% |
| runtime_behavior_matrix / Historical key uniqueness | 30.421s | 12.125s | -60.1% |
| runtime_behavior_matrix / Graph-only siblings GraphThenVersion | 59.161s | 11.823s | -80.0% |
| runtime_behavior_matrix / Commit version-producing siblings | 58.768s | 11.481s | -80.5% |
| runtime_behavior_matrix / Graph-only siblings VersionThenGraph | 68.345s | 11.412s | -83.3% |
| runtime_behavior_matrix / smartlink_commit_cache | 40.214s | 10.111s | -74.9% |
| runtime_behavior_matrix / Graph-only siblings Disjoint | 46.411s | 9.652s | -79.2% |
| runtime_behavior_matrix / Commit no-op and graph-only siblings | 40.142s | 9.546s | -76.2% |
| runtime_behavior_matrix / Graph-only siblings Identical | 46.034s | 9.411s | -79.6% |
| query_storage_boundaries / query_boundary_data | 8.109s | 8.681s | +7.1% |
| runtime_behavior_matrix / Commit mixed dispositions | 55.312s | 8.541s | -84.6% |
| runtime_behavior_matrix / Commit validation correction | 62.364s | 8.335s | -86.6% |
| runtime_behavior_matrix / frozen_member_head_redirect_cross_tx | 27.456s | 8.164s | -70.3% |
| runtime_behavior_matrix / stage_new_from_clone | 38.068s | 8.123s | -78.7% |
| runtime_behavior_matrix / Commit unchanged update | 32.474s | 7.917s | -75.6% |
| runtime_behavior_matrix / Staged Schema dependency cycle | 17.370s | 6.595s | -62.0% |
| runtime_behavior_matrix / Commit strict described membership | 22.295s | 6.471s | -71.0% |
| runtime_behavior_matrix / frozen_member_head_redirect | 21.902s | 6.201s | -71.7% |
| runtime_behavior_matrix / Transaction Lifecycle Test | 13.214s | 5.691s | -56.9% |
| runtime_behavior_matrix / Simple AbandonStagedChanges Testcase | 15.715s | 4.979s | -68.3% |
| runtime_behavior_matrix / Attachment defaults persist | 12.280s | 4.659s | -62.1% |
| runtime_behavior_matrix / Simple Create/Get Holon Testcase | 3.505s | 3.506s | +0.0% |
| runtime_behavior_matrix / load_inverse_oriented_book_person_instances | 3.426s | 3.313s | -3.3% |
| runtime_behavior_matrix / DeleteHolon Testcase | 1.746s | 1.934s | +10.8% |
| pristine_bootstrap_and_loader / Loader Incremental Fixture | 1.645s | 1.743s | +6.0% |
| runtime_behavior_matrix / Simple Add / Remove Related Holon Testcase | 0.289s | 0.078s | -72.9% |
| runtime_behavior_matrix / Simple Add / Remove Holon Properties Testcase | 0.000s | 0.000s | baseline rounded to zero |
| runtime_behavior_matrix / cross_transaction_staged_target_diagnostic | 0.000s | 0.000s | baseline rounded to zero |
| runtime_behavior_matrix / Ergonomic Add / Remove Holon Properties Testcase | 0.000s | 0.000s | baseline rounded to zero |
| runtime_behavior_matrix / Ergonomic Add / Remove Related Holons Testcase | 0.000s | 0.000s | baseline rounded to zero |

## Interpretation and limits

This is one complete rerun, not a controlled multi-sample benchmark. It verifies the
existing suite assertions across bootstrap/schema loading, query storage boundaries,
lineage, clones, inverse traversal, graph-only updates, and Commit rejection/retry.
Existing unit checks additionally cover bulk cache coverage, known-empty collections,
policy retention, TTL/Fresh behavior, and atomic failure.

The implementation also includes the earlier bounded rejection check in the
`Commit validation correction` fixture. Its timing improvement cannot be attributed
solely to bulk relationship retrieval. Shared suite state and ordinary run variance
also affect per-fixture comparisons. Named relationship reads and broad verification
loops are not automatically consolidated by this enhancement.

The isolated [phase measurement](bulk-relationship-profile.md) provides the more
direct attribution: actual relationship retrieval fell from 45.94s to 5.10s with
the same two-root comparison contract. No claim is made about tests outside this run.

## Remaining measured hotspots

The complete-schema ValidationBindings/inverse scan remained the largest step:
**456.633s versus 447.840s** previously. It still performs named relationship reads
across loaded holons. Graph-only/version-producing anchoring verification was next
at **78.618s versus 111.058s**. The Book/Person forward/inverse traversal check was
**34.334s versus 34.173s**. These measurements identify remaining work; this rerun
does not modify those verification contracts.

## Reproduction and evidence

- [Current raw timing summary](dance-timings-bulk-relationships.txt)
- [Original baseline](dance-timings.txt)
- Full captured output: `/Users/stevemelville/dev/map-holons/.notes/test-profiles/20261106T142529Z-bb6afff7/console.log`
- Temporary-storage wrapper log: `/private/tmp/map-holons-dance-bulk-regression/run-fwEICCtB/test.log`

The root entrypoint rebuilt production DNA and probe WASM, passed the production
artifact audit, and ran only `dance_tests` with `--test-threads=1 --nocapture`.
The collector sets the same targeted INFO logging used for the baseline.

```sh
nix develop --command env MAP_TEST_RUN_ROOT=/private/tmp/map-holons-dance-bulk-regression \
  python3 .notes/profile-dance-tests.py -- bash scripts/test-run.sh npm run sweet:dance
```
