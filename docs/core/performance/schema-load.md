# Core Schema load performance

**Status:** open investigation. **Measurements:** September 19–20 and November 2, 2026.
This record captures implementation observations, not new validation or caching
contracts. Schema-load performance is separate from the functional closeout of
[map-holons #706](https://github.com/evomimic/map-holons/issues/706).

This is one part of the broader [application startup investigation](startup-and-canvas.md).
See [caching lessons](caching.md) for host/guest policy discoveries and future options.

## Scope and architectural references

The original September workload provisions the first Core Schema: 21 bundles, 696 loader
holons, 3,425 queued relationships, and 7,412 SmartLink creation attempts.
Core Schema loading, base-package activation (which includes another schema
load), and Canvas startup are separate phases. Improvements to one do not
establish improvements to the others.

Authoritative behavior remains in:

- [Core Schema bootstrap](../core-schema-bootstrap/core-schema-bootstrap-design-spec.md)
- [Holon Loader](../holon-data-loader-design-spec.md)
- [Validation architecture](../validation/validation-arch.md) and
  [commit validation](../validation/commit-validation-design-spec.md)
- [Transactions](../transactions/transactions-design-spec.md)

## Execution boundaries and responsibility

| Context | Observed work | Cache/validation distinction |
|---|---|---|
| Host | Bootstrap orchestration, transport, response processing | Host cache contents do not transfer into guest validation |
| Coordinator guest | Bind LoaderRefRep, load/stage graph, descriptor-driven commit validation, persist actions | Request-local cache starts cold; reuse can benefit work within the request |
| Native conductor | System validation and source-chain flush after coordinator execution | Includes checking the local authoring agent's action signatures |
| Integrity guest | MAP PVL application validation, invoked through Wasmer | No descriptor retrieval; distinct from coordinator descriptor validation |

The `load_holons_returning` marker precedes conductor completion. Holochain
0.6.3's call-zome workflow performs inline system/application validation and
flush work before returning the result. Action signatures establish the signer
and action integrity; they are not signatures of schema publishers or approvals
from other peers. For these create-entry/create-link actions, the signer is the
local authoring agent.

The host service call remains pending through local inline validation and
source-chain flush: the conductor does not return its successful zome-call result
to the host before those finish. MAP's synchronous host adapter waits for that
result. The coordinator marker means “coordinator execution finished,” not
“host received the result” or “durable commit complete.” System validation runs
natively in the conductor; PVL runs in integrity WASM. Subsequent DHT integration,
publication, and remote-peer validation are separate from this local completion
boundary and may continue after the response.

## Wall-time measurements

All values below are seconds. “Before entry” starts at the conductor-call timer;
“Coordinator” spans guest entry to its return marker; “After marker” ends at the
caller receiving the conductor result. The latter includes remaining conductor
work and return-path overhead, not just PVL execution.

| Measurement | Before entry | Coordinator | After marker | Entire call |
|---|---:|---:|---:|---:|
| Earlier app run | 9.43 | 33.24 | 36.13 | 78.80 |
| Slow app run | 9.84 | 36.66 | 79.69 | 126.17 |
| Five-run unoptimized harness medians | 9.70 | 32.40 | 41.66 | 83.65 |
| Memory experiment original: three-run medians | 9.45 | 29.29 | 39.27 | 77.68 |
| Memory experiment 4 MiB: three-run medians | 9.39 | 36.22 | 57.65 | 103.29 |

The earlier app's broader bootstrap timer was 81.70 seconds; it is not the
78.80-second conductor call. Harness total timers also include setup and are
not equivalent to the app's bootstrap timer. Component medians are independent.

The harness uses in-process SweetConductor. Its transport, dependency feature
set, and conductor configuration differ from the app. Matching native
optimization alone does not make the environments identical.

**Confirmed:** the largest measured interval is after coordinator return.
The slow app's 79.69-second interval was not reproduced in the initial five
controlled runs (41.26–43.52 seconds). Its cause remains unresolved.

Inside the coordinator, the slow app log reports about 3.13 seconds of commit
validation and 29.47 seconds for the whole guest commit. These are nested
measurements; they must not be added to coordinator time. The evidence does not
support attributing the post-return delay to descriptor retrieval.

## Post-return CPU sampling

One unoptimized harness run was sampled for ten seconds starting approximately
0, 15, and 30 seconds after the coordinator marker.

| Window | Native system validation/signatures | Wasmer instance setup | WASM memory growth/copying |
|---|---:|---:|---:|
| 0–10 s | 67.1% | 12.3% | 5.2% |
| 15–25 s | 0% classified | 48.5% | 21.9% |
| 30–40 s | 0% classified | 49.1% | 21.5% |

These are approximate shares of active CPU samples across process threads,
classified exclusively by stack ancestry, with explicit kernel waits excluded.
The remainder includes other native work, WASM execution/boundary work, and
SQLite. This is **not a wall-time budget** or proof that PVL rule execution
accounts for only the remaining percentage.

The sampled run took 49.99 seconds after the marker, compared with 41–44 seconds
in the preceding unsampled series. Sampling may perturb execution. The final
approximately ten seconds were not sampled and flush was not separately timed.

Observed stacks include cryptographic field operations under system validation,
`RealRibosome::build_instance_with_store` leading to Wasmer instance construction,
and `wasmer_vm_memory32_grow` leading to allocation and memory copying. These
identify concrete costs around validation without isolating their full elapsed
contribution. See the [sampling record](evidence/2026-09-schema-load/sampling.md).

## Experiments and decisions

### Initial integrity memory: 4 MiB worsened performance

**Hypothesis:** more initial memory could avoid repeated memory growth/copying.
The original integrity WASM declares 17 pages (1,114,112 bytes); this includes
stack, static data, and heap, not 1 MiB of free heap.

Three alternating pairs compared the original with 64 pages (4 MiB). The native
executable and coordinator WASM were unchanged. Exactly one byte in the original
integrity WASM changed: its memory-section minimum. All executable code was
identical. An initial linker rebuild was discarded from the comparison because
it changed other WASM sections.

| Pair | Original after marker | 4 MiB after marker | Original entire call | 4 MiB entire call |
|---|---:|---:|---:|---:|
| 1 | 39.27 s | 56.66 s | 77.68 s | 102.61 s |
| 2 | 38.47 s | 57.65 s | 76.85 s | 103.29 s |
| 3 | 47.03 s | 63.72 s | 92.56 s | 107.84 s |

Execution order within each pair was 4 MiB then original. All six tests passed
with 696 validation candidates and 7,412 SmartLink attempts. Median post-return
time increased **47%**, and median entire-call time increased **33%**.

**Decision:** reject 4 MiB initial memory for this workload/configuration.
Original DNA and WASM were restored and checked byte-for-byte. No permanent
build setting changed. Allocation/initialization cost is a possible explanation,
but this timing experiment does not isolate the mechanism or rule out other
memory strategies.

### Native optimization: promising, requires controlled confirmation

Two earlier optimized harness runs had post-marker intervals of approximately
18.8–18.9 seconds, versus the five-run unoptimized median of 41.66 seconds.
The tests inherited `opt-level="z"` from the root profile; the host app's dev
build used the default unoptimized profile. The unoptimized harness series
explicitly set native dev/test optimization to zero and verified built artifacts.

**Conclusion:** native optimization is the strongest next experiment, not a
proven app speedup. The earlier optimized observations were not an alternating,
otherwise-identical A/B. Their complete per-run metadata is not retained in this
section, so treat them as provisional comparison evidence.

### Cache changes: separate correctness from performance attribution

The investigated implementation uses guest request-local membership reuse
without descriptor policy lookup; host retention remains descriptor-driven.
Host TTL decisions were observed after correcting descriptor discovery, and
functional cache tests passed during the investigation. These establish paths
and behavior, not a quantified startup speedup. There is no controlled evidence
here assigning the app's post-return variability to cache policy changes.

The source-oriented inverse-descriptor discovery and cache lifetime contracts
remain owned by the transaction and descriptor specifications. Do not infer
that a host-cache optimization benefits a fresh guest cache, or that caches can
be removed from guest workloads that reuse data within one request.

## Recommendations and open questions

1. Run an alternating native-optimization A/B with the same DNA, workload,
   logging, validation, and conductor settings. Record dependency optimization
   separately from application debugging settings.
2. Time system validation, integrity instance setup/execution, and flush
   separately to explain the full post-marker interval.
3. Investigate repeated Wasmer instance construction and memory lifecycle costs.
   Any reuse strategy must preserve isolation and reset behavior; this is not
   MAP descriptor-cache reuse.
4. Reproduce app variability with repeated runs and recorded machine load,
   artifact hashes, build profiles, and conductor settings.
5. Maintain separate baselines for activation-package loading and Canvas startup
   before drawing conclusions about their bottlenecks.

Open questions include the unmeasured persistence tail, why the slow app run
nearly doubled post-return time, the mechanism behind the 4 MiB regression, and
how much native optimization transfers to the app. No recommendation here
requires disabling validation.

## Evidence and reproducibility

The [evidence inventory](evidence/2026-09-schema-load/README.md) preserves all
individual controlled-run metrics, artifact hashes, selected app marker excerpts,
and sampling methodology. It also identifies missing provenance and raw traces
that remain local. No timing claim depends on a reader retaining `/tmp` files.

## November 2, 2026: larger bootstrap and recurring post-return delay

A profiled application launch on branch
`833-prepare-space-navigators-initial-visualizer-composition-and-eliminate-repeated-selection-reads`
used checkpoint `3764a9ee` plus uncommitted registry-owner transport/acquisition
changes. Native dev code was optimized (`opt-level="z"`); guest code was built in
release with `holons/commit-performance-profiling`. Launch used `MAP_PROFILE=1`,
`RUST_LOG=host:warn`, and `WASM_LOG=info`. This is one observation, not an A/B
attribution to those changes. The [evidence inventory](evidence/2026-11-02-registry-startup/README.md)
retains markers, metrics, browser history and provenance limits.

The workload had grown to **22 bundles, 1,162 candidates, 5,938 queued
relationships and 13,068 SmartLink attempts**. September had 696 candidates and
7,412 attempts under Holochain 0.6.3; November used 0.7.1. Counts, implementation,
optimization and instrumentation differ, so these are historical comparisons,
not normalized regression or speedup measurements.

| Core Schema measurement | September earlier app | September slow app | November 2 INFO capture |
|---|---:|---:|---:|
| Candidates | 696 | 696 | 1,162 |
| MAP coordinator Commit validation | 3.001 s | 3.128 s | **3.448 s** |
| Commit Pass 1 | 1.055 s | 1.157 s | 0.617 s |
| Commit Pass 2 | 22.235 s | 25.177 s | **53.334 s** |
| Coordinator entry to return marker | 33.24 s | 36.66 s | **64.724 s** |
| After return marker to host receipt | 36.13 s | 79.69 s | **146.371 s** |
| Entire conductor call | 78.80 s | 126.17 s | **214.628 s** |

November's pre-entry interval was 3.533 s. Its adapter's independent internal timer
was 64.723 s (hydration 2.222 s, dispatch 62.253 s, session export 0.246 s).
The loader measured 62.252 s, including a 57.564-second guest Commit. These nested
timers are not additional intervals. Commit Pass 2 included **25.510 s across
1,162 ownership-key lookups**, and 14.802 s in SmartLink persistence; the latter
includes expansion and action creation. These are concrete costs to investigate,
not demonstrated removable overhead.

Within the 3.448-second MAP validation total, PackageValidation took 2.136 s,
PreparedProducts 0.691 s, PackageDiscovery 0.228 s, SubjectPreparation 0.208 s,
SchemaWorksetPreparation 0.045 s and InstanceValidation 0.135 s. Core preparation
reported zero backend/link queries and exact-node reads in these phase counters;
this staged bootstrap observation does not establish the cost of saved-descriptor
validation in other workloads.

**Interpretation:** MAP coordinator descriptor validation is a small part of this
capture (about 1.6% of the conductor call). This does **not** mean validation as a
whole is cheap: native Holochain system validation and integrity-WASM application
validation belong to the later completion boundary. September already located
system/signature checks and integrity instance/memory costs in that interval.
November confirms the long interval has recurred, but does not re-measure its
internal composition or establish that the same components caused its increase.

The coordinator emitted `load_holons_returning` at **20:04:44.071710 UTC**;
the host call completed at **20:07:10.442324 UTC**. Investigation should reuse the
existing post-return work rather than treat this as a newly discovered descriptor
validation problem. Trace native system validation, integrity instance setup and
execution, source-chain/database flush, and return-path overhead separately.
Background database activity may contend with those operations; it must not be
confused with required inline completion work.

The base-package call in the same INFO capture took **8.516 s**: MAP validation
3.555 s for 21 candidates, Pass 1 0.012 s and Pass 2 1.629 s. The later
seven-candidate background Commit took 3.813 s at the host boundary, with MAP
validation 2.361 s. Keep these separate from Core Schema bootstrap.

The two preceding WARN-only app runs reported SQLite `database is locked` errors
while deleting live ephemeral scheduled functions during bootstrap. That error
was not present in this INFO capture. It remains a contention clue, not a proven
cause of the post-return interval. An earlier idle-app stack sample showed SQLite
page reads and SQLCipher activity; it was taken after rendering, outside the
bootstrap interval, and cannot attribute the bootstrap delay.

No matched checkpoint run has yet established whether registry transport changed
validation or overall startup performance. Use identical workload, build features,
logging and conductor configuration for that comparison. INFO profiling itself
can perturb execution; the WARN-only Canvas history is a separate observation.

### November 2 rollback comparison: slowdown persists without Part 1

The uncommitted registry-owner transport/acquisition step was backed up and its
17 files restored to checkpoint `3764a9ee`; the separate test-only navigation
probe was left untouched. The app was rebuilt with the same release guest
profiling feature and launched with the same INFO/WARN/MAP_PROFILE flags after
stopping the preceding development launch. This is a sequential single-pair
comparison, not a repeated alternating experiment; machine load was uncontrolled
and terminal output handling differed (tee versus redirected output).

| Measurement | Part 1 INFO run | Checkpoint with Part 1 removed |
|---|---:|---:|
| Core candidates / SmartLink attempts | 1,162 / 13,068 | 1,162 / 13,068 |
| Core MAP validation | 3.448 s | **3.549 s** |
| Core Commit Pass 1 | 0.617 s | 0.674 s |
| Core Commit Pass 2 | 53.334 s | **64.198 s** |
| Core coordinator marker interval | 64.724 s | 75.975 s |
| Core post-return interval | 146.371 s | **174.554 s** |
| Core conductor call | 214.628 s | **254.610 s** |
| Base-package MAP validation, 21 candidates | 3.555 s | **19.058 s** |
| Base-package Commit Pass 2 | 1.629 s | **10.116 s** |
| Base-package conductor call | 8.516 s | **45.187 s** |
| Later seven-candidate Commit conductor call | 3.813 s | 3.350 s |

Base-package validation performed identical counted work in both runs:
SubjectPreparation had 23 backend calls, PackageDiscovery 310, PreparedProducts
527, PackageValidation 81 and InstanceValidation zero. Each phase's link-query,
returned-link and exact-node-read counts also matched. PreparedProducts increased
from 1.589 s to 9.143 s; PackageValidation from 0.894 s to 4.839 s. This supports
slower execution of the same counted work, not additional counted read operations;
it does not isolate CPU scheduling, storage latency, native/WASM boundary costs,
or all uncounted work.

The checkpoint again reported `database is locked` while deleting live ephemeral
scheduled functions, at 20:29:44.952203 UTC during the post-return interval. Core
coordinator return was 20:26:56.756142 UTC; host receipt was 20:29:51.310615 UTC.
The error's presence does not establish causality. A later process check found
the app at about 0.2% CPU; macOS reported no recorded thermal/performance warning.
Those observations do not establish conditions during the timed slow phases.

**Conclusion:** backing out Part 1 did not recover the earlier app timings, and
Core MAP validation was essentially unchanged. The slowdown is reproducible with
that step absent. This does not quantify Part 1's benefit or overhead, nor rule
out a separate contribution from it. Base-package validation really was slow in
the checkpoint run, so a small Core validation total must not be generalized to
all validation workloads. Preserve the rolled-back state while diagnosing the
shared runtime slowdown; do not infer an improvement from this single pair.

The Part 1 logs also lack direct capture/restoration/index-build timings and
registry-entry/hit/reconstruction counters. The 29 ms hydration timer encloses
restoration and indexing when a registry is present, but cannot establish their
individual costs or confirm live registry reuse. Correctness tests prove reuse
for controlled fixtures; equivalent app reuse across these runs is unmeasured.
The 2.89 ms envelope encoding timer starts after capture and must not be reported
as capture cost. Instrument those boundaries and old graph copying separately
before claiming measured effects for Part 1.

[Baseline markers](evidence/2026-11-02-registry-startup/baseline-selected-markers.txt)
and [baseline measurements/provenance](evidence/2026-11-02-registry-startup/baseline-measurements.json)
preserve this comparison. The UI screenshot showed Core Schema 258.642 s,
base packages 45.002 s, home-Dancer selection 94.479 s, and an unfinished Canvas
start timer of 152.653 s. These UI timers differ from conductor-call boundaries;
no completed baseline Canvas profile has been supplied.

### Fast-state source and build audit

A subsequent audit recovered an immutable Nix source snapshot registered at
**14:44:59 UTC on November 2**, before the 15:54:50.794 UTC fast run. Comparison
against checkpoint `3764a9ee` covered 1,349 tracked files: **1,346 matched byte for
byte**; two files differed only in doc comments. The snapshot omitted the then
untracked `space_session.rs`. Reconstructing that file from the retained creation,
test-addition and comment-edit scripts gives the same code as the checkpoint,
allowing for comments, formatting and optional trailing commas.

The immutable snapshot has identical native/guest Cargo manifests and lockfiles,
launch scripts, UI and generated schema inputs, including both copies of the
bootstrap manifest. Host `opt-level="z"`, guest release size optimization,
Holochain 0.7.1 and saved-node capacity were not changed by the later checkpoint.
The recorded session shows no runtime source edits between the fast run and the
19:00:24 UTC commit; that interval contained audits, documentation, checks and
committing the existing work. Part 1 edits began at 19:05 UTC.

**Correction to the earlier uncertainty:** the checkpoint's later creation time
is not evidence that it contained different runtime behavior from the fast working
tree. The snapshot and edit chronology strongly support source equivalence.
They do not prove the exact binaries loaded by the fast app: its native/DNA/hApp
hashes and full native log were not retained, and the Nix snapshot itself is not
an app artifact. The audit is not a complete OS-level record of all possible
external writes.

One actual build/configuration difference remains explicit. The fast working tree
was built through normal `build:happ`/`npm start` with WARN-level WASM logging. The
later Part 1 diagnostic capture **and its rollback comparison** deliberately used
`holons/commit-performance-profiling` and `WASM_LOG=info`. The feature adds timing
and per-operation diagnostics and changes coordinator WASM; INFO produces much
more output. Those two INFO runs compare the implementation under instrumentation,
but neither reproduces the original fast-run configuration. This does not explain
the first slow WARN-only runs, whose logs show the normal build path.

The next clean recovery check should use the already-restored checkpoint with the
normal hApp build and WARN logging, preserving the same UI/native profiling
settings used for the 83.497-second reference. Record artifact hashes **before**
launch and a complete Canvas profile. Keep that experiment distinct from the
extra-instrumented validation comparison. No additional app launch or source
change was performed during this audit.

[Fast-state audit evidence](evidence/2026-11-02-registry-startup/fast-state-audit.json)
retains snapshot registration/NAR identity, matching-file hashes, comparison
counts, chronology and limitations. The local immutable snapshot and temporary
creation scripts are provenance sources, not durable downloadable artifacts.


## November 4: verified step 4 runtime

[Evidence](evidence/2026-11-04-step4/README.md). Core Schema UI time was 82.147 s:
1,163 committed holons, 5,943 relationship collections and 13,080 SmartLink insertions.
MAP validation was 2.828 s, Commit Pass 2 was 36.736 s, keyed Owns lookups were
17.470 s (1,163 checks; no additional keyed index insertions), and SmartLink
persistence was 10.209 s. Descriptor resolution was 1.466 s; endpoint resolution
was 0.618 s. Nested timings must not be added together.

The guest adapter total was 47.215 s. Its return marker preceded host call
completion by 29.275 s; the current log does not attribute that interval to
specific Holochain finalization/integrity/storage operations. No database-lock or
slow-statement warnings were recorded. Guest-local MAP validation is not a measure
of all Holochain integrity validation.

The additional Space Navigator package took 8.315 s in the UI. Its loader total
was 7.347 s for 21 candidates, including MAP validation 3.995 s and Commit Pass 2
1.354 s. Small-load validation/preparation overhead therefore deserves separate
measurement from the large-load keyed-index/persistence cost. No implementation
change is inferred from these measurements alone.
