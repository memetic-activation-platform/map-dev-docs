# Matched Step A smoke evidence

All four workloads completed at clean map-holons revision `ced364a40b0d6e74cbedcfdf45d29158957f0b30`: one run of six samples each. The retained raw logs reparse exactly to the saved measurements, and each workload test reports success. No new captures were taken for this analysis.

The capacity checkpoint is `a3a280d1b59745038b63e9eb84f47b27b2193ff9`. Both sides use guest cache 10,000, Holochain/HDK 0.7.1 and HDI 0.8.1, the same host/hApp/root Cargo and flake lockfile hashes, and a 60-second startup allowance. Source and guest artifact change as expected; the observed registry conditions match at every paired sample. Both source trees were clean. Compiler/tool versions, platform, machine and CPU-count metadata also match.
Cache-state and Session-product-reuse labels remain unavailable, not evidence of identical warmth;
CPU load/thermal conditions are unmeasured. The paired runtime registry observations, rather than
workload names, establish the registry comparison.

Before artifact SHA-256: `17fa2d5def6bb671b99aaa3f7c11ff5bc212616b6472610fc4f81729974d2662`.
After artifact SHA-256: `2ff1f58481bacc2692024c33735e4c376fbbc497c952e7ec3993c8db1faa8a07`.

## Assessment

The package-boundary controls pass: prepared definitions/products, identity-role visits, every non-readiness edge request/member count, fresh builds, restorations and index counts match. Readiness spans and edge observations are absent in all 24 after samples. The new guard span is present. However, these captures do **not** show an end-to-end performance improvement. Preparation is slower in all four workloads; backend calls and node reads are unchanged. Logical requests decrease, while structural-diagnosis events increase materially. The expectation of lower derivation work needs qualification, not a blanket success claim.

## Latency and requests

Medians below use sample indices 2–5 (four observations per workload). Sample 0 and index 1 are reported separately below. This is one smoke run, not a significance test or a fixed latency guarantee. Changes are `(after − before) / before`.

| Workload | Commit ms before → after | Change ms (%) | Preparation ms before → after | Change ms (%) | Assessment logical requests before → after | Change (%) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| usage | 2078.4 → 2217.7 | +139.3 (+6.7%) | 1596.0 → 1673.3 | +77.3 (+4.8%) | 7408 → 6476 | -932 (-12.6%) |
| no-op | 1898.5 → 1963.2 | +64.7 (+3.4%) | 1566.3 → 1640.5 | +74.1 (+4.7%) | 7438 → 6541 | -897 (-12.1%) |
| mixed | 2192.9 → 2300.8 | +108.0 (+4.9%) | 1579.1 → 1714.6 | +135.5 (+8.6%) | 8018 → 6726 | -1292 (-16.1%) |
| shared-type | 3128.9 → 3211.3 | +82.4 (+2.6%) | 1754.0 → 1931.1 | +177.1 (+10.1%) | 7513 → 6553 | -960 (-12.8%) |

Preparation means the complete `commit-construction` interval. Assessment request/call totals sum exclusive phase counts; they exclude host snapshot construction and persistence. Phase-local distinct membership counts are retained separately in the JSON and are never summed into a Commit-wide distinct count.

## Invariant work and reads

Values below are unchanged before/after for sample 2; the comparison checks **all six** paired samples, including first-construction differences. The JSON retains per-sample registry conditions and edge counts.

| Workload | Prepared definitions | Package requests / members | Removed readiness requests | Fresh builds / restorations | Index builds | Assessment backend calls / node reads | NameIndexes backend calls / node reads |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| usage | 127 | 1248 / 547 | 1116 | 125 / 2 | 407 | 765 / 191 | 75 / 63 |
| no-op | 124 | 1213 / 524 | 1089 | 124 / 0 | 398 | 769 / 193 | 81 / 67 |
| mixed | 125 | 1222 / 527 | 1098 | 125 / 0 | 402 | 770 / 192 | 81 / 67 |
| shared-type | 134 | 1311 / 554 | 1179 | 132 / 2 | 428 | 772 / 191 | 75 / 63 |

NameIndexes backend calls and node counts are unchanged at matching capacity. These 10,000-entry
observations do not replace the historical 99-entry high/low-residency evidence or establish
prepared-input retention at small capacity; that control remains Step C work.

Usage/shared-type receive zero registry entries at sample 0 and four at samples 1–5; their exact governor is absent/present at the corresponding boundaries on both sides. They perform zero restorations initially and two subsequently. No-op receives zero entries throughout. Mixed receives one entry throughout but keeps the affected-Schema bypass and performs zero restorations. Registry lookup/scan work remains unchanged (499 examined entries for repeated usage/shared-type). No registry infrastructure improvement is claimed.

## Derivation attribution

Counts are whole-assessment events, not interchangeable units of lineage work. In particular, replacing `resolve` with a diagnosed-lineage builder reduces resolution counters while creating diagnosis events. Zero resolution requests does not establish that lineage discovery disappeared.

| Workload | Schema resolutions before → after | Structural diagnoses before → after | Role walks before → after | Contract / constraint contribution resolutions before → after |
| --- | ---: | ---: | ---: | ---: |
| usage | 125 → 0 | 15 → 179 | 26 → 13 | 0 → 0 / 0 → 0 |
| no-op | 124 → 0 | 13 → 181 | 26 → 13 | 0 → 0 / 0 → 0 |
| mixed | 125 → 0 | 51 → 183 | 51 → 12 | 1 → 0 / 1 → 0 |
| shared-type | 132 → 0 | 29 → 186 | 26 → 13 | 0 → 0 / 0 → 0 |

Repeated usage shows the tradeoff clearly:

- FreshEffectiveSchema median rises from 411.8 ms to 486.9 ms (+75.2 ms). PreparedProducts records 124 structural diagnoses instead of zero; this work is inside the fresh-computation span. Build successes remain 125. The baseline used `resolve`/`ancestors`; the new path diagnoses the full lineage, reads aligned record keys and checks the root’s direct Extends before `from_valid_lineage`.
- ContractChecks rises from 85.2 ms to 115.1 ms (+29.9 ms). PackageValidation structural diagnoses rise from 13 to 53, while its role walks fall from 13 to zero. Source inspection shows that navigation/vocabulary members now use a full shared diagnosis, where some previous classification paths stopped at a matching ancestor. Aggregate evidence does not identify all 53 exact sources or prove their individual costs.
- The baseline ReadinessDiscovery and DependencyGrouping medians were 29.2 ms and 4.2 ms. Those spans are absent afterward; they are not measured zero. Candidate InterpretationGuards is 7 µs. Defect-fact generation remains inside ContractChecks, so that tiny span is not the total cost of interpretation guards.
- PackageValidation median changes only from 119.3 ms to 115.3 ms (−4.1 ms): the added contract work offsets most of the removed scheduling work. Do not sum these per-operation medians to claim an exact elapsed-time decomposition.
- PreparedProducts logical membership requests increase by 93 in repeated usage; PackageValidation membership requests decrease by 1,025. Content requests and observed backend/node reads remain unchanged. Across the other workloads the same higher fresh-computation cost is visible; mixed gets more benefit from eliminating declaration/role re-derivation.

This is source-supported attribution, not proof that all latency regression is caused by these changes. The capture contains runtime variability, and changed persistence/transport/host timing also affects complete Commit latency. Before more captures, inspect whether full diagnosis is justified for every construction/navigation consumer. Also audit whether the fuller navigation/vocabulary walk introduces new incidental defect/failure exposure beyond the fact that consumer needs. Preserve exact identity, structural-defect attribution and required-read behavior; do not undo guards or narrow the package closure merely to improve this checkpoint.

## First construction and sample index 1

Each cell is before → after in milliseconds. Sample index 1 is retained separately even where its host snapshot is zero. Mixed has its legacy snapshot spike in setup/sample 0 rather than index 1.

| Workload | Sample 0 Commit | Sample 0 preparation | Sample 0 host snapshot | Sample 1 Commit | Sample 1 preparation | Sample 1 host snapshot |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| usage | 2107.7 → 2101.6 | 1558.9 → 1754.3 | 0.0 → 0.0 | 4707.1 → 4321.9 | 1597.4 → 1699.4 | 2448.2 → 1995.6 |
| no-op | 1736.0 → 1925.9 | 1523.2 → 1588.6 | 0.0 → 0.0 | 1925.1 → 2118.5 | 1573.1 → 1720.3 | 0.0 → 0.0 |
| mixed | 3666.4 → 3589.1 | 1597.0 → 1801.3 | 1323.3 → 1057.4 | 2231.3 → 2497.9 | 1601.8 → 1895.9 | 0.3 → 0.3 |
| shared-type | 2915.8 → 3502.3 | 1707.1 → 2111.7 | 0.0 → 0.0 | 4434.8 → 5404.7 | 1684.6 → 2086.4 | 1625.1 → 1900.4 |

Usage sample 1’s lower total time must not be credited to guard changes: host snapshot construction itself falls by about 453 ms. Shared-type sample 1’s snapshot grows by about 275 ms. The legacy snapshot infrastructure remains in place. Transport-envelope encoding stays unavailable in this Sweettest path, as documented by the original capture protocol.

## Reproduction and remaining gates

Run `python3 compare-captures.py` in this directory (or use its full path). It verifies metadata/foundation equality, re-parses all locally retained raw logs, verifies test success, asserts per-sample package/registry invariants, and writes [comparison.json](comparison.json). Original capture files are not rewritten. Raw logs remain git-ignored; the JSON records their SHA-256 hashes. If logs are absent on another checkout, re-parsing is explicitly unavailable.

The committed implementation and the bounded smoke checkpoint are now recorded. This is not the final #822 evidence or a declaration of performance improvement. Sweettest regression results including `runtime_behavior_matrix` have not been supplied here. No additional capture is requested or run: the one-run/six-sample Step A budget is complete.
