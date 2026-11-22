# Session-retained Visualizer evaluation — implementation comparison

The separate Visualizer evaluation registry now retains Rust-resolved hierarchies, exact saved identities, effective settings, participation requirements, scalar metadata, and observed populations. Ordinary requests and compatible occurrences reconstruct those answers. Scoped reconsideration is explicit; publication and preference saves do not refresh established results. Notifications and staleness detection remain deferred.

This is implementation evidence for the [DAHN evaluation design](../hx/dahn-design-spec.md#1454-runtime-index-and-preparation-validity), not a separate behavioral specification. The [baseline](visualizer-evaluation-baseline-2026-11-22.md) is revision `1166e4bc`, with findings 1 and 2 already implemented. The measurements were captured from the finding 3 working tree before commit. That source is checkpointed as [a7667482](https://github.com/evomimic/map-holons/commit/a7667482fc561f753c16bf00781ac4c2906ef66b); the [manifest](evidence/2026-11-22-visualizer-evaluation-comparison/source-manifest.json) preserves exact source and artifact hashes.

## Composition measurements

Three passing disposable-conductor runs use the same timed Inspector and 18-field workloads and logging levels as the baseline. Existing preference checks now explicitly request reconsideration where they formerly expected automatic refresh. Additional successor-publication checks run **after** the measured workload, preserving the benchmark fixture graph at measurement time. `RUST_BACKTRACE=1` affects failure diagnostics; successful samples have no backtrace output. No application build is included in these spans.

| Operation | Baseline median ms | Implementation median ms | Change | Implementation range ms |
| --- | ---: | ---: | ---: | ---: |
| Initial Inspector evaluation | 782.061 | 798.647 | +2.12% | 785.656–830.252 |
| Initial 18-field PropertyMap | 630.300 | 662.540 | +5.11% | 641.837–666.211 |
| Fresh host Inspector composition | 969.488 | 853.632 | -11.95% | 843.699–941.738 |
| Repeated host Inspector composition | 952.675 | 0.085 | -99.99% | 0.076–0.086 |

The repeated request is a Rust Commands composition operation, not full UI rendering. It reuses all 12 bindings and 22 metadata entries, with zero selector calls, personal-population requests, or candidate-population requests. The baseline repeated six selections and one personal-population request. Baseline warm transport had one canonical guest call plus two lookup calls; retained Commands results now need no guest round trip. Ordinary realization still reads actual subject values and checks executable/callable readiness.

The initial evaluation still performs semantic work on demand. A fresh host must acquire the subject's descriptor to identify reuse scope, and cold transport now includes the separate evaluation carrier. Its extra payload is a cold-path cost; no startup improvement should be inferred from the warm result alone. Work counters are semantic operations, not physical database reads. The per-run [measurements](evidence/2026-11-22-visualizer-evaluation-comparison/measurements.json) record actual transport calls and bytes separately.

## Packaged startup

| Sequential startup boundary | Baseline | Implementation |
| --- | ---: | ---: |
| npm start → first application log (checks/build/bundle/launch) | 29.387 s | 28.667 s |
| First application log → Welcome ready | 9.999 s | 6.282 s |
| Welcome ready → Navigator handoff (includes user entry) | 11.151 s | 198.149 s |
| Handoff → browser profile | 0.093 s | 0.112 s |
| Browser startup → mounted Canvas | 7.303 s | 8.823 s |
| **Interactive npm start → mounted Canvas** | **57.933 s** | **242.032 s** |

Welcome requires the **Enter my space** gesture. The implementation capture waited 198.149 s between Welcome readiness and Navigator handoff, including the user's entry and handoff preparation. This is not a program-only startup timer or evidence of a registry runtime regression. Desktop automation was unavailable; the user confirmed Canvas open and the saved diagnostic was read from only the `map.startupProfiles` key in the application's local storage, using read-only SQLite.

Browser startup increased by 1520 ms in this one observation. Canvas materialization increased from 2633 to 3808 ms; Canvas construction increased from 4384 to 4678 ms. The initial `Transaction.ResolveComposition` command was 703 ms in the baseline and 710 ms here, with one call in each. These single samples do not isolate causality or establish a cold-start improvement. Reuse benefits follow an established evaluation; the first Canvas composition is still an uncovered scope.

See the [browser profile](evidence/2026-11-22-visualizer-evaluation-comparison/browser-startup-profile.json), [native/build markers](evidence/2026-11-22-visualizer-evaluation-comparison/npm-start-selected-markers.txt), and [coordinator maintenance receipt](evidence/2026-11-22-visualizer-evaluation-comparison/coordinator-upgrade-markers.txt). An earlier attempt rebuilt native dependencies (133 s Cargo time) and stopped at the existing coordinator compatibility guard. The supported coordinator-only upgrade verified the existing DNA, integrity, cell and author, then updated the packaged coordinator in 416 ms. This maintenance attempt is excluded. The measured ordinary launch subsequently passed the guard; its native Cargo interval was 21.31 s versus 21.73 s in the baseline.

## Regression evidence and limits

- Boundary tests cover compatible occurrence rebinding, distinct ValueType scopes, covered Slot demand reuse, exact metadata/configuration reconstruction after carrier eviction/reset, private owner isolation, and superseded-publication rejection.
- The production-conductor acceptance checks initial defaults without personal writes, retained absence after a preference save, explicit reconsideration, saved configuration adoption, compatible occurrences, and successor publication without implicit version adoption.
- The UI suite retains the regressions for inactive Slots and declared initial collections. Registry acquisition returns Rust bindings; no TypeScript winner cache was introduced.
- Descriptor and Visualizer participants have separate restricted owner transactions and share transport-owner validation. A reset retires the Visualizer carrier, preserves compact recipes, and opens a new owner lazily. Returned occurrence references are rebound to the current caller; retired owner-qualified temporary identities are not revived.
- Recipes with uncommitted semantic dependencies remain request-local. No process-restart cache or automatic residency policy is introduced.

A separate preference-replacement defect was found while extending version-adoption coverage: replacing a persisted preferred Visualizer can leave both targets in the required-singular `PreferredVisualizer` relationship. Graph-only Commit currently persists remaining members additively; removing a member from the staged collection does not remove its old stored link. Retained choices are unaffected until reconsideration, which correctly reports the ambiguity rather than falling back. The [separate finding](evidence/2026-11-22-visualizer-evaluation-comparison/preference-replacement.md), preserved reproducer and failed-adoption source manifest document this separately; resolving general relationship replacement is outside this registry change.

## Validation

- Runtime/wire unit tests: 105 + 3 passed.
- Boundary unit tests: 28 passed.
- SDK tests: 402 passed; SDK typecheck passed.
- UI tests: 546 passed, one skipped; UI typecheck passed.
- hApp/WASM build and packaging passed.
- Three production-conductor acceptance runs passed (the samples above).

Raw logs are temporary; compact evidence and checksums are retained beside this page. Three samples on one developer machine do not provide a confidence interval or a system-wide speedup claim.
