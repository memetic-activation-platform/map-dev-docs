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
817 exact node reads**. The mode-stratified comparison below shows a much smaller command gap. These observations
do not identify registry size as the cause of the entire latency difference. Command standard deviations in those two groups are approximately **469 ms**
and **723 ms**; the thirtytwo-hit maximum is **5.285 seconds**. Do not infer a small total-latency
benefit from the difference of medians alone.

Saved restoration and the conservative affected-Schema bypass are both represented. Descriptor
and mixed cases restore no saved products despite receiving snapshots. Host snapshot construction
remains measurable even when the guest bypasses it. Production envelope shipping time is unavailable
in this mock-conductor capture path; unavailable is not zero.

## Sample-level variance sources

[Sample-level calculations](diagnostics/baseline-variance.json) reveal two systematic patterns
hidden by pooled repeated-sample medians. They should be reported separately in Phase 9.

### Two NameIndexes read modes

Across the 350 repeated samples, exact node reads in NameIndexes occupy two disjoint ranges:
**119–166** and **795–1,046**. All 14 workloads show both ranges; **215/350** samples are in the
high group. The calculation uses 400 reads to divide the empty gap; this is a descriptive split,
not a performance acceptance threshold. Both modes occur within individual runs.

| Workload | High-mode repeated samples | High-mode command median | Low-mode command median |
| --- | ---: | ---: | ---: |
| `usage` | 21/25 | 2.878 s | 2.050 s |
| `slot` | 12/25 | 2.776 s | 2.191 s |
| `no-op` | 15/25 | 2.552 s | 1.931 s |
| `registry-eight-hit` | 12/25 | 3.179 s | 2.315 s |
| `registry-thirtytwo-hit` | 17/25 | 3.464 s | 2.575 s |

The high group is associated with roughly 0.6–0.9 seconds more command time in these cases.
Mode mix can reverse pooled rankings: usage is faster than slot in the low group despite its
higher pooled median. Comparing eight-hit and thirtytwo-hit within the same read group reduces
the observed command gap from about 775 ms to approximately **260 ms (low)** or **285 ms (high)**.
These are descriptive comparisons, not controlled estimates of a causal registry-size effect.

Capacity/eviction pressure is a plausible explanation. The ordinary saved-content cache requests
99 entries, while retained content lives in a separate residency table. Retained entries are not
subject to ordinary eviction, but the original insertion can also remain in the evictable cache.
Unretained name-index members and other reads still compete there. The relationship-membership
cache is separate. Consequently, 99 is not a cap on all guest-held holons or all guest caches.
Quick_cache can round its requested capacity into per-shard capacities.

The hApp resolves quick_cache 0.6.18 without ahash, using std RandomState. Hashing and shard
allocation can influence eviction, and read order can also matter. A larger-cache experiment can
test capacity pressure; it does not by itself prove that hash seeding specifically causes the modes.
Retaining the required index content is the intended demand-scoped remedy; increasing a global
cache budget is an independent tuning decision with memory costs.

### Capacity intervention: 99 versus 1024

The [capacity comparison](diagnostics/cache-capacity-comparison.json) records one run/six samples
per variant at the same clean source revision `284c456a5dabbc9a88d91a1ca856a8b772d30864`.
Runtime versions match. Guest instrumentation verifies the requested capacities, and the two
artifact hashes are retained in the report and per-variant metadata. Only the guest diagnostic
capacity is increased; the host's default stays unchanged. These are diagnostic captures,
not additions to the original production-default baseline.

| Guest capacity | NameIndexes exact node reads, samples 0–5 | High-read samples |
| --- | --- | ---: |
| 99 | 848, 121, 812, 824, 121, 824 | 4/6 |
| 1024 | 63, 63, 63, 63, 63, 63 | 0/6 |

Both variants still prepare 127 definitions and build 407 indexes per assessment; fresh/restored
product counts match for corresponding samples. Thus the improvement is reuse of member content,
not preparation narrowing or less semantic work. Exactly 63 reads at larger capacity is consistent
with one initial fetch per member in the earlier 63-definition inventory, although these timed
captures do not themselves log every read identity. Together with the earlier repeated-fetch
inventory, this is strong intervention evidence for capacity/eviction pressure behind the read modes.
It does not isolate RandomState seeding from shard geometry, eviction policy, or traversal order.

For sample indices 2–5, excluding both the first Commit and the second-Commit transition:

| Median interval | Capacity 99 | Capacity 1024 | Observed change |
| --- | ---: | ---: | ---: |
| Complete command | 2.862 s | 2.108 s | −0.754 s (−26.4%) |
| Preparation | 2.184 s | 1.540 s | −0.643 s (−29.5%) |
| NameIndexes | 1.143 s | 0.534 s | −0.609 s (−53.3%) |

These percentages describe four later samples in each of two single-run captures, not a general
performance guarantee or a completed #822 result. Even after repeat-fetch pressure disappears,
407 index builds and roughly 0.53 seconds in NameIndexes remain, reinforcing the separate need
to narrow consumer demand. At both capacities NameIndexes also issues 75–77 backend link queries
per assessment, relationship reads that occur after package-discovery prefetch; the capacity
delta implies roughly 0.8 ms per avoided node read, so the 63 remaining node reads explain only
about 50 ms of the residual, leaving most of it to those unprefetched link reads and index
computation.

The host transition spike persists: sample 1 snapshot construction takes **1.491 s** at capacity
99 and **2.533 s** at capacity 1024. Its complete command takes 3.545 s and 4.462 s respectively.
This experiment does not show that larger guest capacity fixes the snapshot path, nor does one
observation per variant establish that it worsens it. Attribute that host cost separately and
investigate nested snapshot work before assigning a cause.

Required member retention should be verified under small-cache pressure so that a larger global
budget cannot conceal missing preparation. A production cache-size change needs its own memory
and representative-workload assessment; the diagnostic build does not change production defaults.
No full baseline recapture is required on the strength of this experiment.

### Approved 10,000-entry cache checkpoint

On November 2, we also captured `usage`, `no-op`, `mixed`, and `shared-type` at the approved
10,000-entry guest capacity: one run of six samples each, at clean revision `a3a280d1`.
[Checkpoint records](cache-10000-checkpoint/usage/measurements.json) verify capacity 10,000.
All 24 samples avoid the high-read mode: NameIndexes reads 63 nodes for usage/shared-type and
67 for no-op/mixed. Repeated-sample definition, fresh/restored product, and index-build counts
match the historical baseline.

For usage sample indices 2–5, median command time is **2.078 s** and NameIndexes **0.541 s**, close
to **2.108 s** and **0.534 s** in the 1024-entry diagnostic. These small captures show no material
additional latency benefit from 10,000 over 1024 for this workload; they are not a capacity-sizing
study. The host snapshot spike remains (usage sample index 1: **2.448 s**). This checkpoint is the
same-capacity reference for Step A, separate from the historical 99-entry baseline.

### Second-Commit host snapshot spike

Sample index 1 is the second measured Commit, and the first after these workloads acquire a
non-empty saved-schema registry. Its host snapshot preparation is much slower than later samples:

| Workload | Second-Commit host snapshot median | Later host snapshots (approx.) |
| --- | ---: | ---: |
| `usage` | 1799 ms | 0.7 ms |
| `slot` | 1891 ms | 0.7 ms |
| `shared-type` | 1776 ms | 0.7 ms |
| `registry-zero` | 1789 ms | 0.7 ms |

This cost is inside the timed host Commit command, outside guest assessment. It is systematic
startup-of-reuse cost, not unexplained random noise. Seeded cases perform relevant setup outside
the timed interval and do not provide the same transition case. Snapshot cloning can perform
reentrant preparation, making that path a plausible source of the cost, but the current aggregate
span does not prove which nested operations account for it. Existing registry entries were already
available for shipping; this spike alone does not establish when every entry was acquired.

Keep sample index 1 visible in comparisons, separately from indices 2–5, and distinguish host
snapshot construction from guest lookup. Investigating/eliminating this cold snapshot-construction
cost is a concrete follow-up candidate; changing host snapshot selection/shipping remains outside #822.

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

Report NameIndexes read-mode frequencies and within-mode results, plus sample index 1 separately
from later repeated samples. Summarize independent runs as well as pooled sample medians/spread. The 25 repeated samples share
only five Session histories; they are not 25 independent fresh-session experiments. First/repeated
labels are execution order, not proof of cold/warm caches. Claims about small latency differences
need stronger evidence than deterministic work-count reductions. No fixed latency promise follows
from this baseline.

## Suggested PR baseline paragraph

The instrumented baseline covers 420 Commit samples across 14 workload cases and five bootstrap
runs. An ordinary one-instance Commit prepares 127 exact definitions and builds 407 name indexes.
Repeated usage has a pooled command median of 2.837 s, but this mixes low-read and high-read
NameIndexes modes with command medians of 2.050 s and 2.878 s. Separate inventories identify
repeated loads of the same 63 relationship/command definitions, motivating demand-scoped retention.
A systematic second-Commit host snapshot cost of about 1.8 s is another distinct source of latency.
Readiness discovery itself costs roughly 30 ms; its larger significance is the broad preparation
closure it sustains. Final comparisons must report work counts, read-mode frequencies, and the
second-Commit transition alongside end-to-end latency, while preserving validation semantics.
