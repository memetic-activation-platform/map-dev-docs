# Issue #822 baseline performance summary

This summary describes the existing broad-preparation implementation. It is a reference for
Phase 4 iteration and Phase 9 comparison, not evidence of an implemented #822 improvement.
Capture provenance and the common profiled DNA hash are in [README.md](README.md) and
[baseline/manifest.json](baseline/manifest.json). Original per-workload records remain authoritative.

## Capture scope and headline timings

The baseline contains 14 Commit workload cases, five independent runs per case and six samples
per run: five first samples and 25 repeated samples per case, 420 Commit samples total.
Five separate bootstrap captures complete the manifest. Instrumentation is `822-v2`, with
Holochain 0.7.1, HDK 0.7.1 and HDI 0.8.1 recorded for the Commit captures. Captures were
assembled across three workload revisions using the same profiled guest artifact.

Times below are medians in seconds. “Commit” means the complete host Commit command interval,
not just guest validation. Preparation is the guest construction boundary. Phase/component
medians need not sum to the median total.

| Workload | First Commit | Repeated Commit | Repeated preparation | Prepared definitions |
| --- | ---: | ---: | ---: | ---: |
| `usage` | 2.734 | 2.837 | 2.177 | 127 |
| `slot` | 2.598 | 2.573 | 1.657 | 124 |
| `shared-type` | 3.588 | 3.510 | 2.017 | 134 |
| `descriptor` | 3.714 | 2.609 | 2.071 | 115 |
| `new-version` | 5.256 | 2.659 | 2.205 | 124 |
| `mixed` | 3.705 | 2.865 | 2.215 | 125 |
| `no-op` | 2.367 | 2.423 | 2.152 | 124 |
| `graph-only` | 2.620 | 2.757 | 2.250 | 127 |
| `graph-only-overlap` | 2.775 | 2.738 | 2.232 | 127 |

`shared-type` stages eight instances sharing a governor; `mixed` stages a descriptor and an
instance. Graph-only cases preserve the saved source identity and verify persisted edges outside
timing; overlap additionally verifies compatible puts from two candidates and branch evidence.
No-op performs no persistence but still spends a median 2.152 seconds in preparation.

Bootstrap's median end-to-end time is **93.786 seconds**, range **93.633–94.299 seconds**, across
five runs. This includes conductor startup and loader processing; it is not a Commit-only latency.
The bootstrap captures used the explicit 60-second startup allowance. Earlier Commit groups used
the upstream ten-second allowance; this wait lies outside their timed Commit interval.

## Where the work is

For repeated `usage` samples, the baseline prepares **127 exact definitions**, with **125 fresh
schema builder attempts**, **two saved-product restorations**, and **407 name-index builds**.
Preparation's median is **2.177 seconds**, compared with **2.837 seconds** for the complete command.

The observed work includes:

- Package traversal: **1,248 edge requests / 547 traversed members**.
- Separate readiness traversal: **1,116 edge requests / 464 traversed members**.
- Preparation phases: **6,827 logical cache requests** in aggregate. This count includes content
  and membership requests; it is not a count of unique memberships or backend calls.
- NameIndexes: **1.141 seconds** and **806 exact node reads** (separate medians).
- FreshEffectiveSchema: **0.407 seconds**.
- Readiness discovery: **29.8 ms**; dependency grouping: **3.4 ms**.

Removing the scheduler's own execution time cannot explain a seconds-scale improvement.
Its larger importance is the preparation demand and validity dependence sustained by its broad
closure. Measure eliminated work across the whole assessment rather than relocating it.

Assessment also repeats derivation after construction: repeated `usage` samples record 13
structural diagnoses and 13 role walks across PackageValidation/InstanceValidation; `mixed`
records 47 diagnoses, 39 role walks, and one constraint-contribution resolution. These are useful
work-count controls for migrating consumers to prepared products. Fresh schema resolution,
building and saved restoration already record zero in those assessment phases for these cases;
preserve that guarantee rather than claiming it as a new improvement.

## Registry observations and limits

Population flags seed a Session once per run; subsequent staging, host reads, verification and
snapshot preparation can enrich it. They do not maintain fixed populations across samples.
For example, `registry-zero` ships zero entries initially and four in repeated samples.
`registry-eight-miss` ships nine initially and twelve thereafter. A global registry-hit count does
not establish whether the particular instance governor was present. Treat these as workload labels,
not asserted lookup conditions.

Repeated-sample medians give the following component evidence:

| Seeded workload | Actual shipped entries | Entries examined | SnapshotLookup | Host snapshot construction |
| --- | ---: | ---: | ---: | ---: |
| `usage` | 4 | 499 | 11.2 ms | 0.69 ms |
| `registry-eight-miss` | 12 | 1,507 | 27.4 ms | 1.77 ms |
| `registry-eight-hit` | 11 | 1,374 | 25.3 ms | 1.70 ms |
| `registry-thirtytwo-hit` | 35 | 4,374 | 76.1 ms | 4.93 ms |

The latter cases make **126 eligible snapshot lookups per assessment**. Scan time is roughly
17–18 microseconds per examined entry in these observations. This is neither a universal per-entry
constant nor a measurement of index construction, which includes its own metadata access,
allocation, hashing and failure handling. Narrowing the requested products should change lookup
count substantially, so defer the index decision until that count is known.

The eight-hit versus thirtytwo-hit repeated-command medians differ by about **775 ms**; measured
lookup differs by only **51 ms**. NameIndexes medians differ by about **620 ms**, with **127 versus
817 exact node reads**. These observations do not identify registry size as the cause of the entire
latency difference. Command standard deviations in those two groups are approximately **469 ms**
and **723 ms**; the thirtytwo-hit maximum is **5.285 seconds**. Do not infer a small total-latency
benefit from the difference of medians alone.

Saved restoration and the conservative affected-Schema bypass are both represented. Descriptor
and mixed cases restore no saved products despite receiving snapshots. Host snapshot construction
remains measurable even when the guest bypasses it. Production envelope shipping time is unavailable
in this mock-conductor capture path; unavailable is not zero.

## Separate NameIndexes diagnostic

The later opt-in inventory captures are diagnostics, **not additional timing samples**. The normalized
[source-level inventory](diagnostics/name-index-inventory.json) records the diagnostic revision,
artifact hash, input-log hashes, exact source IDs and semantic keys. Keys were joined to smart-reference
ID/key pairs in each corresponding raw log, rather than comparing generated IDs across runs.

| Diagnostic | Sample | NameIndexes node-cache misses | Distinct missing definitions |
| --- | --- | ---: | ---: |
| usage | First | 848 | 63 |
| usage | Repeated | 819 | 63 |
| thirtytwo-hit | First | 155 | 63 |
| thirtytwo-hit | Repeated | 121 | 63 |

All four samples involve the same semantic-key set: **50 relationship definitions and 13 command
definitions**. Some are loaded 26 times in the usage capture. The difference is therefore largely
repeated loading of the same required content, not a larger missing-member set in one capture.
This strongly motivates retaining the content required by each requested index. It does not yet
explain every eviction or why a particular capture gets better cache residency.

Exact governor observations in the diagnostic show usage absent before/in the first snapshot,
then present in the second snapshot of four entries. The thirtytwo-hit governor is present in both
samples, with populations 32 then 35. These controls should accompany the cheap registry follow-up.

## Phase 4 and Phase 9 measurement guidance

For Phase 4, use small work-count captures and focused tests while narrowing demand. Prioritize
ordinary usage, no-op, mixed/Schema bypass, and shared-governor cases. Verify requested products,
traversed memberships, content retention and derivation counts independently of cache warmth.
Do not simply retain every baseline-discovered definition: retention follows the actual consumers
of the narrowed products. Every mandatory check must still complete or have its prescribed explaining
finding; lower counts alone do not demonstrate correct validation.

After narrowing, use the same observation tooling on the baseline and narrowed implementations for
the saved registry follow-up: normally one run/two samples at small and large populations. Record
before-command and actually shipped governor membership, observed population, lookups, entries
examined, restoration and component time. These are natural-growth captures unless fixed-population
controls are explicitly added. Additional timing runs are justified only if the index decision remains
ambiguous. Include index construction in the comparison if an index is implemented.

For Phase 9, retain this full baseline and repeat the bounded workload manifest with equivalent
instrumentation, artifacts, runtime settings, workload sizes and documented cache/Session conditions.
Report absolute and percentage changes in complete command and preparation time alongside logical
requests, traversal, content/backend reads, semantic computations and restoration. Keep host snapshot
construction, guest lookup and guest computation distinct. Explain instrumentation changes, bypass
costs, bootstrap behavior and significant regressions.

Summarize independent runs as well as pooled sample medians/spread. The 25 repeated samples share
only five Session histories; they are not 25 independent fresh-session experiments. First/repeated
labels are execution order, not proof of cold/warm caches. Claims about small latency differences
need stronger evidence than deterministic work-count reductions. No fixed latency promise follows
from this baseline.

## Suggested PR baseline paragraph

The instrumented baseline covers 420 Commit samples across 14 workload cases and five bootstrap
runs. An ordinary one-instance Commit prepares 127 exact definitions and builds 407 name indexes;
its repeated-command median is 2.837 s, including 2.177 s of preparation. NameIndexes accounts for
1.141 s, versus roughly 30 ms for readiness discovery itself. Separate read inventories identify
repeated loads of the same 63 relationship/command definitions, motivating demand-scoped retention.
Registry scans scale with examined entries, but the broad baseline performs 126 eligible lookups per
assessment, so indexing must be judged against the narrowed demand and include construction cost.
Registry population grows between samples and command timings vary substantially; final improvement
claims must combine matched end-to-end measurements with work-count and semantic regression evidence.
