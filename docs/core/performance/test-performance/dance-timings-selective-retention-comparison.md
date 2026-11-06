# Dance performance rerun after selective retention

This historical capture includes branch 852 checkpoint `9863d4fb` and the then-uncommitted #853 selective-retention changes. It predates removal of the bespoke ValidationBindings inventory step. Differences are cumulative since the prior capture; they do not isolate #853 or measure the subsequent test removal.

Identical completed fixture inventory: **True** (41 current, 41 previous).

| Suite | Fixtures | Previous seconds | Current seconds | Change |
| --- | ---: | ---: | ---: | ---: |
| pristine_bootstrap_and_loader | 2 | 551.515 | 573.209 | +3.9% |
| query_storage_boundaries | 2 | 32.463 | 29.008 | -10.6% |
| runtime_behavior_matrix | 37 | 504.492 | 422.002 | -16.4% |
| **All fixtures** | **41** | **1088.470** | **1024.219** | **-5.9%** |

Fixture times exclude builds, conductor/bootstrap, setup, and teardown.

Previous dance test binary: **1470.11s**; previous profiled command: **1509.508s**.
Current result: `test result: ok. 3 passed; 0 failed; 12 ignored; 0 measured; 0 filtered out; finished in 1409.90s`.
Current profiled command: **1453.961s**.

## Largest fixture changes

| Fixture | Previous seconds | Current seconds | Change seconds |
| --- | ---: | ---: | ---: |
| pristine_bootstrap_and_loader / bootstrap_operational_schema | 549.626 | 571.388 | +21.762 |
| runtime_behavior_matrix / Simple StageNewVersion Testcase | 109.493 | 89.021 | -20.472 |
| runtime_behavior_matrix / Commit distinguishable same-key results | 18.498 | 11.266 | -7.232 |
| runtime_behavior_matrix / Commit non-root lineage and independent clone | 33.376 | 26.700 | -6.677 |
| runtime_behavior_matrix / Commit unchanged update | 7.846 | 12.143 | +4.297 |
| runtime_behavior_matrix / Commit mixed dispositions | 8.689 | 5.025 | -3.664 |
| runtime_behavior_matrix / Commit branches across transactions | 12.541 | 8.890 | -3.651 |
| runtime_behavior_matrix / frozen_member_head_redirect_cross_tx | 7.210 | 3.840 | -3.370 |
| runtime_behavior_matrix / Graph-only siblings GraphThenVersion | 10.883 | 7.608 | -3.275 |
| runtime_behavior_matrix / Graph-only siblings VersionThenGraph | 10.562 | 7.433 | -3.130 |
| runtime_behavior_matrix / load_book_person_inverse_schema | 51.289 | 48.292 | -2.997 |
| runtime_behavior_matrix / Book v1 and Title v2 exact references | 42.527 | 39.531 | -2.996 |

## MatchSavedContent steps

Previous: 30 steps, 56.483s.
Current: 30 steps, 22.285s.

## Slowest current steps

- 488.553s — pristine_bootstrap_and_loader / bootstrap_operational_schema / Verify ValidationBindings descriptor contract and inverse traversal
- 76.313s — runtime_behavior_matrix / Simple StageNewVersion Testcase / Verify graph-only and version-producing relationship anchoring
- 38.101s — pristine_bootstrap_and_loader / bootstrap_operational_schema / Verify core schema descriptors
- 32.666s — runtime_behavior_matrix / load_book_person_inverse_schema / Verify forward and inverse Book/Person instance SmartLink traversal
- 17.659s — pristine_bootstrap_and_loader / bootstrap_operational_schema / Verify core schema command affordances
- 15.647s — pristine_bootstrap_and_loader / bootstrap_operational_schema / Verify core schema value semantics
- 13.685s — runtime_behavior_matrix / Book v1 and Title v2 exact references / Commit [expected_status: Rejected, expected_error: None, candidates: [], retry_participants: []]
- 12.645s — runtime_behavior_matrix / Book v1 and Title v2 exact references / Commit [expected_status: Rejected, expected_error: None, candidates: [], retry_participants: []]
- 12.243s — runtime_behavior_matrix / Cross-schema dependency coverage gap / Commit [expected_status: Rejected, expected_error: None, candidates: [], retry_participants: []]
- 8.970s — runtime_behavior_matrix / Graph-only siblings RemovalConflict / Commit [expected_status: Rejected, expected_error: None, candidates: [], retry_participants: []]

Bootstrap guest load/commit samples: 90.733s, 93.422s, 92.271s.

No test assertion was changed for this rerun. Sources remained unchanged throughout the capture.

- [Full timing summary](dance-timings-selective-retention.txt)
- [Machine-readable timings](dance-timings-selective-retention.json)
- [Command and source checksums](dance-timings-selective-retention-context.json)
- Local full log: `map-holons/.notes/test-profiles/20261106T223651Z-7e19fe20/console.log`.
- [Subsequent inventory-step retirement](validation-bindings-verification-retirement.md)
