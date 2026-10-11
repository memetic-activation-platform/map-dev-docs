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
