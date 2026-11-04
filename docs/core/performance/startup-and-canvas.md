# Application startup and Canvas performance

**Status:** observed regression and recovery; attribution remains partial.
**Evidence:** September 19, 2026. This investigation began with the complete
`MAP_PROFILE=1 npm run start:info 2>&1 | tee /tmp/map-package-activation-profile.log`
launch path, then narrowed to separate bottlenecks. See the
[measurement conventions](index.md), [schema-load investigation](schema-load.md),
and [cache lessons](caching.md).

## Separate startup phases before assigning causes

The launch includes build/dev tooling, host initialization, hApp installation
(including compilation), Core Schema load, base-package activation, Canvas/home
selection, and browser-side Canvas mount. Base-package activation itself includes
another LoadHolons call. Native setup completion is not browser mount completion.

The retained September 19, 23:41 UTC native run shows:

| Boundary | Duration | Interpretation |
|---|---:|---|
| Provider setup | 4.907 s | Includes nested hApp install/update (1.062 s); do not add the two |
| Core Schema bootstrap | 129.108 s | Broader than its 126.174 s conductor call |
| Bootstrap completion to Canvas-selection start | 15.196 s | Activation interval inferred from markers; not an exclusive subphase profile |
| Native Canvas selection | 5.080 s | Separate from browser Canvas materialization and mount |
| Native setup total | 154.293 s | Does not include the later browser mount |
| Browser Canvas mount | 15.190 s | Run starting at 23:44:03.733Z |

The entire shell-command elapsed time, including rebuilds and development-server
startup, was not retained as one reproducible metric. Do not label native setup
or browser mount alone as “npm start time.” The install cost and any compilation
cost also depend on what state is warm.

## Canvas regression and recovery

The supplied browser profiles contain this history. Times are seconds; timestamps
are UTC on September 19. All runs report `mounted`.

| Run | Canvas total | Theme projection | Property discovery/rendering |
|---|---:|---:|---:|
| 17:22:25 | 76.648 | 29.578 | 24.095 |
| 17:41:51 | 80.183 | 30.252 | 26.372 |
| 19:17:23 | 12.443 | 6.470 | 2.922 |
| 19:32:51 | 12.766 | 6.487 | 2.918 |
| 20:24:45 | 91.543 | 44.640 | 9.183 |
| 20:57:54 | 118.661 | 31.631 | 40.173 |
| 22:41:16 | 14.017 | 6.041 | 3.824 |
| 23:44:03 | 15.190 | 6.595 | 3.824 |

The sequence includes both improvement and relapse. Canvas recovered from the
118.661-second run to 14.017 and 15.190 seconds, while the later native Core Schema
phase increased to approximately 129 seconds. A faster Canvas did not mean faster
startup overall. These snapshots span multiple changes; they do not isolate the
benefit of any single cache or UI patch.

### What changed in the expensive paths

| Browser measurement | Slow run 20:57:54 | Recovered run 23:44:03 |
|---|---:|---:|
| Total mount | 118.661 s | 15.190 s |
| Materialize Canvas | 12.735 s | 1.681 s |
| Project theme | 31.631 s | 6.595 s |
| Materialize rooted navigation | 11.144 s | 1.864 s |
| Materialize root node | 10.813 s | 0.483 s |
| Select/materialize Properties | 12.035 s | 0.609 s |
| Discover/render property fields | 40.173 s | 3.824 s |
| GetRelatedHolons command total (107 calls) | 31.605 s | 6.322 s |
| DanceV2 command total (6 calls) | 61.822 s | 4.862 s |
| SelectVisualizer command total (9 calls) | 23.310 s | 3.109 s |

Command rows overlap phase rows. Both runs also made 100 GetVersionedKey calls
and 124 GetPropertyValue calls. Stable command counts with sharply different
latencies locate the improvement below command issuance; they do not by
themselves prove a cache hit-rate improvement. Artifact fetch itself took only
3–5 ms across six commands in these two runs, despite expensive materialization
phases: semantic selection and dance execution must be distinguished from
fetching the JavaScript bytes. Canvas construction itself took about 1 ms.

Theme projection still consumed 6.595 seconds, about 43% of the recovered mount.
It traverses descriptor-backed token/assignment relationships; the phase name
must not be mistaken for browser styling or paint time. Theme traversal and
property presentation remain useful candidates for focused measurement.

## Insights and warnings

- **Do not explain an order-of-magnitude regression as profiling overhead
  without a controlled comparison.** Earlier profiled runs were fast too. The
  thread's suggested “7x overhead” was not established. Native sampling and
  ordinary startup instrumentation are different sources of overhead.
- **Counts are not identities.** Fifty fetches do not prove fifty repeats of one
  source. Inspect source identity, relationship name, cache lifetime, and expiry
  before predicting how many TTL hits should occur.
- **A local cache hit may leave an IPC command in the browser profile.** Measure
  storage/guest fetches and command latency as well as command counts.
- **Coordinator execution finishing does not release the host caller.** The
  service call remains pending while the conductor awaits local inline validation,
  integrity callbacks, and source-chain flush before returning the result.
  Subsequent distributed validation is a separate completion boundary.
- **Stored profile history is not a single run.** Correlate UTC timestamps and
  workload boundaries across browser and native logs before comparing results.
- **Avoid premature parallelization.** The current property presentation path
  serializes operations over one transaction-bound execution surface. Any
  concurrency proposal needs an explicit lifecycle/reentrancy analysis, not just
  a replacement of awaits with parallel promises.
- **Keep feedback visible during long phases.** Phase instrumentation and isolated
  visualizer error regions help distinguish slow work from failed composition;
  a spinner or a long aggregate timer cannot diagnose either.

## Next measurements

Keep a full startup phase ledger and separate baselines for schema loading,
activation packages, selection, theme projection, and property presentation.
For Canvas, correlate each expensive command with cache decisions and actual
transport/storage work. Measure repeated reads of the same identities separately
from first reads across many different token or descriptor sources. Investigate
batching or fewer boundary crossings only within the existing bound-reference
and Rust-owned selection architecture.

The [retained profiles and markers](evidence/2026-09-startup/README.md) preserve the
underlying measurements and their provenance limits.

## September 21: repeated descriptor-root key resolution

The application run at **2026-09-21T16:02:32.252Z** mounted the Canvas in
20,981 ms. It used map-holons commit `458975d1` plus phase-only instrumentation
separating affordance classification, Action selection, composition, and mount.
The launch command was `MAP_PROFILE=1 npm run start:info`. The user supplied the
browser profile and startup screenshot; native dance request keys and completed
`call_zome` timers were correlated with the browser phase boundaries. The compact
[lookup evidence](evidence/2026-09-startup/descriptor-root-lookups-2026-09-21.json)
preserves the extracted measurements. Raw logs remain local; this is one
observational run, not a controlled optimization experiment.

| Canvas phase | Duration |
|---|---:|
| Theme projection | 7,885 ms |
| Affordance classification | 5,698 ms |
| Property discovery/rendering | 3,166 ms |
| Select/materialize Actions | 546 ms |

Classification made **55 host-to-guest key-resolution calls for eight distinct
keys**, totaling approximately **2,323 ms**. Each of four property `is_array()`
checks resolved all seven canonical value-type roots (28 calls, 1,160 ms).
Each of 27 relationship `effective_cardinality()` calls separately resolved
`CardinalityConstraint.ConstraintType` (27 calls, 1,163 ms).

The relationship call path is:

1. `classifyNodeAffordances` calls the SDK descriptor's `effectiveCardinality()`.
2. `GetEffectiveCardinality` crosses IPC into the host command handler.
3. The host executes `RelationshipDescriptor::effective_cardinality()`.
4. `resolve_core_descriptor` first checks staged definitions; on absence it calls
   `LookupFacade::get_saved_holon_by_key`.
5. The host service initiates the `get_saved_holon_by_key` dance through the
   conductor's `call_zome`; the guest resolves the visible lineage head and returns
   a reference.
6. Host cardinality evaluation continues through effective constraints.

The property path uses `ValueDescriptor::is_array()` → `resolved_value_kind()` →
`ResolvedValueTypeRoots::resolve()`, which resolves seven roots per invocation.
These callers and the resolver are in `shared_crates/holons_core/src/descriptors/`;
the host service is in `host/crates/holochain_receptor/src/client_shared_objects/`.

**Confirmed:** repeated key resolution crossed the guest boundary even though
only eight keys were involved. This is not evidence of 55 descriptor-content
cache misses. Saved-holon content caching and key-to-current-head resolution are
different operations. The measured key-call cost is roughly 41% of classification
and 11% of Canvas startup; it is not a demonstrated achievable saving.

**Opportunity, deferred:** investigate reuse of resolved roots within a bounded
classification pass, or a host key-to-head cache with explicit freshness and
invalidation semantics. Preserve staged-definition precedence, current-head
semantics, bound-reference ownership, and schema-mutation behavior. Do not assume
that a cached saved version is necessarily the current head. No cache or
EffectiveDescriptor change was made during this investigation.

The same run showed Core Schema load at 76,105 ms and base-package activation at
21,923 ms; the workload now contained 717 loader holons versus the earlier 696.
The earlier September 21 observation of 115,993 ms activation and an unfinished
Canvas timer at 62,495 ms remains an **unexplained outlier**, not proof of a
persistent regression or a particular cause. Accept this measured baseline for
the classification delivery and defer optimization to the separate performance
workstream. Repeat controlled runs before making causal or speedup claims.

## November 1, 2026: initial ValueType and PropertyType DerivedDescriptors

The first ValueType/PropertyType DD implementation retained EffectiveHolonDescriptor.
Saved wrappers used private, nonserialized lazy handles and registry reuse by exact
saved descriptor identity. One guest construction lineage supplied constraints,
validation bindings and operator affordances, retaining provenance and duplicates.
Mutable definitions were recomputed; scalar metadata and value-kind classification
still used their then-existing paths. Later accessor unification and Session/Commit
transport changes must not be assumed present in this initial observation.

The user re-supplied the original findings on November 2. The completed browser
runs and recomputed native counts are preserved in the
[initial DD evidence](evidence/2026-11-01-derived-descriptors/README.md).

| Measurement | Previous: Nov 1 14:37 UTC | Initial DD: Nov 1 19:33 UTC |
|---|---:|---:|
| Startup to mounted | 90.450 s | **82.934 s** |
| Construct Canvas | 76.725 s | 69.717 s |
| SDK commands | 418 | 425 |
| Guest calls for startup requests | 383 | 384 |
| Relationship queries for startup requests | 248 | 248 |
| Extends queries for startup requests | 20 | 20 |
| Visualizer selection + usage selection | 41.643 s | 42.786 s |
| Property array classification | 3.756 s | 3.739 s |

**Finding:** Canvas mounted 7.516 s faster (8.3%), but measured startup work did
not decrease. Relationship and Extends query counts were unchanged, SDK command
count rose, and the original analysis reported summed command durations rising
by about two seconds. Overlap, scheduling or work outside those command timers
could explain the wall-time improvement; this observation does not isolate them.
There were no direct hit/miss or reconstruction counters to attribute savings to
DD memoization. It also did not show the large slowdown seen in the later runs.

Counts here cover request-associated guest calls wholly inside each completed
profile interval; they exclude background calls. This reproduces the original
383/384 counts. A later 385-call report for the same 19:33 run included a boundary
call through interval tolerance. Use the same strict boundary and request scope
when comparing it with November 2's 391 and 388 entries.

## November 2, 2026: registry transport observations

The browser history contains three relevant completed runs on November 2. The
first precedes the uncommitted registry-owner transport implementation; the next
two follow it. Before the last, the user stopped the conductor, left the Nix shell
and quit RustRover. Process restart and implementation changes were not alternated
under a controlled protocol. [Retained profiles and provenance](evidence/2026-11-02-registry-startup/README.md)
record the distinction from the subsequent INFO-level validation capture.

| UTC Canvas profile start | Total | Materialize Canvas | Construct Canvas | SDK commands |
|---|---:|---:|---:|---:|
| 15:54:50.794 | 83.497 s | 13.671 s | 68.595 s | 425 |
| 19:39:10.258 | 225.374 s | 65.551 s | 153.177 s | 425 |
| 19:53:48.147 | 123.602 s | 23.184 s | 98.120 s | 429 |

Restart improved the latter total by 45.2% relative to the first slow run, but it
remained 48.0% above the morning observation. The extra four SDK commands were
three property reads and one relationship read. These counts do not explain the
large timing differences on their own and do not establish their cause.

The 19:39 run had 391 native guest-call entries within the Canvas window; the
19:53 run had 388. A retained November 1 19:33:55 profile had 384 request-associated entries for an
82.934-second Canvas. These are correlated observations with small workload
variation, not a controlled savings estimate. Host command and native guest-call
durations can overlap and must not be added into a wall-time budget.

Both slow WARN-only logs recorded a SQLite lock error during bootstrap. That is
a lead, not a causal diagnosis. Home-Dancer selection returned to about 27.2 s
after restart, while Core Schema and package loading remained elevated. A later
INFO-level run separated coordinator MAP validation from conductor completion:
Core Schema MAP validation took 3.448 s, whereas 146.371 s elapsed after the
coordinator return marker. See the [schema-load follow-up](schema-load.md#november-2-2026-larger-bootstrap-and-recurring-post-return-delay)
for counts, historical measurements, native/integrity validation distinctions and
next measurements. No Canvas browser profile was supplied for that INFO run.

## November 3, 2026: frozen validation and consumer adoption

Completed browser profiles from ordinary `npm start` runs compare registry
transport alone, frozen validation reuse, and consumer adoption. These are single
successive observations, not controlled estimates of the changes' causal effect.

| UTC profile start | Implementation | Total | Materialize Canvas | Construct Canvas | SDK commands |
|---|---|---:|---:|---:|---:|
| 13:04:56.721 | Registry transport | 88.899 s | 13.189 s | 74.395 s | 429 |
| 13:35:15.051 | Frozen validation reuse | 96.870 s | 14.669 s | 80.712 s | 425 |
| 14:09:25.296 | Consumer adoption | 76.957 s | 10.961 s | 64.330 s | 429 |

The final observation is 19.913 s (20.6%) below the preceding run and 11.942 s
below the first. SDK work did not decrease: selection remains 12 calls, DanceV2
8, and property-array classification 4. Relationship commands increased from
53 to 54 and property-value reads from 224 to 227. Accumulated selection duration
fell from 38.246 to 31.457 s; DanceV2 from 23.342 to 17.061 s. These overlapping
command durations are not additive wall-time portions. No reconstruction or
registry-hit counts in this browser profile establish the source of the reduction.

The same final run's screenshot reports Core Schema 77.400 s, base packages
6.810 s and home-Dancer selection 23.369 s. Its unfinished Canvas timer reads
70.490 s; the completed browser profile above is authoritative for Canvas time.
The application remains well above the target of less than five seconds.
Raw completed profiles are retained in
[evidence/2026-11-03-consumer-adoption/canvas-profiles.json](evidence/2026-11-03-consumer-adoption/canvas-profiles.json).


## November 4: verified step 4 runtime

[Evidence](evidence/2026-11-04-step4/README.md). This run follows a confirmed stale
hApp failure and a clean guest rebuild; the source and packaged guest artifact
were checked before startup. Canvas completed in **95.454 seconds**, with
429 SDK commands: materialization 14.124 s, construction 79.924 s. Home Dancer
selection was 17.536 s in the UI. Do not use the screenshot's unfinished Canvas
timer (14.747 s) as its completed measurement.

Accumulated command durations: SelectVisualizer 12 / 46.569 s;
SelectVisualizerUsage 2 / 11.466 s; DanceV2 8 / 14.569 s; GetRelatedHolons
54 / 6.564 s; GetPropertyIsArray 4 / 3.261 s. Canonical guest calls include
seven Usage default-initialization calls totalling 17.295 s; those are nested
within command timings, not additional wall time. Four EHD commands cause one
guest construction; four property-array commands cause one derived construction.

The repaired host policy boundary has zero nested guest calls and sub-millisecond
accumulated policy-span time. Within the Canvas profile window there are 299
completed guest calls, including 169 relationship queries totalling 53.159 s.
Two bulk hydration calls total 0.429 s. Selection redesign remains deferred until
after PR 846. These measurements demonstrate use of the optimizations but do not
establish maximum consumer adoption or a causal overall speedup.


The same run's first DescribedBy completed in 86.263 s; close/repeat completed
in 8.604 s. Selection fell from 71.480 s to 0.015 s, but repeat EHD access cost
3.815 s and property-array classification 2.439 s. The repeat issued one EHD
and two derived construction calls. A successful background Commit saved one
holon between navigations, which retires the derived Session under current policy.
This distinguishes selection reuse from derived-state lifetime: the repeat is not
an unchanged-session memoization test. See the evidence directory's first/repeat
navigation JSON and lifecycle notes. No policy or implementation change was made.


### November 4: first post-unit-5 measurement

The completed profile beginning **12:58:50.421 UTC** records **196.011 s** to
mounted, compared with **88.671 s** in the preceding guest-profiled run beginning
12:05:01.868 UTC. The attached screenshot still showed an unfinished Canvas timer.
Core Schema load remains approximately unchanged against the earlier verified
November 4 screenshot (82.237 s versus 82.147 s); this observation does not quantify
its internal validation phases. Base activation is 22.008 s and home selection
79.393 s in the new screenshot.

| Measurement | Previous guest-profiled run | Post-unit-5 |
| --- | ---: | ---: |
| Total to mounted | 88.671 s | 196.011 s |
| Materialize Canvas | 12.927 s | 54.811 s |
| Construct Canvas | 74.064 s | 135.403 s |
| SDK commands | 429 | 429 |
| Completed guest calls in startup interval | 299 | 309 |
| Relationship guest calls | 169 | 179 |
| GetEffectiveDescriptor commands, summed | 2.433 s | 2.129 s |

Accumulated SDK command times increase mainly in DanceV2 (13.921 -> 84.445 s),
GetRelatedHolons (6.420 -> 32.971 s), and SelectVisualizerUsage
(11.667 -> 32.818 s). SelectVisualizer remains similar (41.593 -> 42.996 s).
These overlapping durations must not be summed as startup wall-time partitions.

The ten extra relationship calls are AffordsDance +7 (7 -> 14),
HasApplicableVisualizer +2 (9 -> 11), and HasImplementation +1 (3 -> 4).
AffordsDance reads report MaxAgeMillis(30000). The extended execution now spans
that TTL, making expiration a concrete amplification hypothesis; source identities
and per-entry expiry events are needed to establish which extra reads are expiry.

The longest individual relationship calls are ForMetaDesignSystem 19.642 s and
AffordsDance 17.530 s / 8.351 s. They occur during the early startup portion.
All eight EHD constructions retain exactly the prior per-construction link-query
counts: 354, 363, 318, 354, 354, 345, 345, 345. Their first construction rises from
1.725 s to 9.160 s despite the same 354 queries; the remaining seven take
1.473–1.726 s. Thus neither increased SDK command count nor a general increase in
EHD construction queries explains the doubling. The origin of the long individual
fetch/guest execution times remains unresolved; the run establishes regression,
not a causal attribution to unit 5 or to machine contention.

Evidence: [post-unit-5 profiles and correlated call records](evidence/2026-11-04-step5/README.md).


### November 4: post-clean follow-up on unit 5

The completed startup beginning **13:13:28.988 UTC** mounted in **94.944 s**,
versus 196.011 s before the conductor deep clean: 101.067 s faster (51.6%).
The fresh log explicitly reports `conductor dir does not exist yet — cold start`.
The screenshot Canvas timer was unfinished; the completed UI profile supplies
94.944 s. Materialize Canvas returns to 13.449 s and Construct Canvas to 80.275 s.
Screenshot stage times: Core Schema 79.629 s, base activation 7.309 s, home
selection 17.990 s (previously 82.237 / 22.008 / 79.393 s).

Startup work returns to **429 SDK commands, 299 guest calls, 169 relationship
queries**. Relationship-name counts exactly match the pre-unit-5 guest-profiled
run, including AffordsDance 7, HasApplicableVisualizer 9, HasImplementation 3.
The ten extra calls seen in the slow run disappear. No completed startup guest
call exceeds 2.629 s, versus 19.642 s for the longest pre-clean call. All eight
EHD constructor query counts remain unchanged; core construction takes
1.758–2.175 s, with no repeat of the 9.160 s first-construction outlier.

This restores the prior approximately 89–95-second startup range. It supports a
state/environment-sensitive regression and removes the basis for attributing the
doubling to additional unit-5 algorithmic work. It does not isolate the retained
WASM cache, database state, process state, or scheduling as the cause, and does
not demonstrate a unit-5 startup speedup. A controlled normal restart after this
healthy baseline would test recurrence without further source changes.

Evidence: `evidence/2026-11-04-step5/startup-profile-fresh.json` and
`fresh-calls.json`. Full local log snapshot:
`/private/tmp/map-step5-fresh-2026-11-04/snapshot.log`.
