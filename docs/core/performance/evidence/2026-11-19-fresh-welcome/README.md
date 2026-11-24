# November 19: fresh Welcome Core Schema loading

User completed a fresh packaged `local-constitution` Welcome run with new Space
and identity, following a rebuild and backup of the prior conductor/keystore store.
Unlike the earlier [retained-store capture](../2026-11-19-holochain-backport/README.md),
this log records actual Core Schema import and successful persistence.
Related implementation: [MAP PR 879](https://github.com/evomimic/map-holons/pull/879).
No merge is implied by this measurement.

## Results and historical comparison

| Measurement | November 4 comparator | Fresh Welcome | Change |
| --- | ---: | ---: | ---: |
| Core Schema: latest step-5 UI timer versus current command timer | 79.629 s | 81.852 s | +2.223 s (+2.8%) |
| Core Schema: matching command route timer, detailed step-4 run | 81.532 s | 81.852 s | +0.321 s (+0.4%) |
| Loader: old internal timer versus current stage-marker interval | 44.730 s | approximately 42.576 s | approximately 4.8% faster |
| Space Navigator import: matching command route timer | 8.443 s | 3.270 s | 61.3% faster |

The latest top-level baseline is the November 4
[post-clean step-5 capture](../../startup-and-canvas.md#november-4-post-clean-follow-up-on-unit-5).
The [step-4 capture](../2026-11-04-step4/README.md) retains detailed backend
markers; its UI Core Schema time was 82.147 s. These are separate baseline runs.
The old loader internal timer and current stage-marker interval have slightly
different boundaries; that row is an approximation, not a matched phase test.

The broader native bootstrap took **84.721 s**, including **2.867 s** of local
Space discovery. Input preparation was 2 ms. `load_and_commit_ms=81852` and
`command=load_holons route_ms=81852.171` describe the current load command;
`initiate_dance_round_trip_ms=81013` is the narrower client dance round trip.
Do not compare the broader bootstrap timer directly with the old UI load timer.

## Workload and correctness

Both detailed captures load 22 bundles. The new run commits **1,180 holons**,
versus **1,163** previously: **17 more (+1.5%)**. Loader-created links increase
**6,540 -> 6,639**, or **99 more (+1.5%)**. These loader link counts are distinct
from the old 13,080 SmartLink persistence insertions; current equivalent
persistence-insertion counts were not recorded.

The Core Schema commit reports `Complete`, attempted=1,180, saved=1,180,
rejected=0, failed=0. The snapshot has no ERROR-level events. Agent Spaces
subsequently loads 10 holons/46 links in 2.098 s; Space Navigator loads
21 holons/96 links in 3.270 s. The Agent Spaces import has no matched historical
comparator here. Package definitions and full result contents were not equated.

## Remaining return delay

Core Schema loader completion is logged at **13:24:01.903477 UTC**. The host
reports the completed client dance round trip at **13:24:37.019198 UTC**:
a remaining **35.115721 s** interval, approximately **35.116 s**.

This is a timestamp difference after the loader marker, not an isolated
Conductor timer. It can include remaining MAP guest response work, session
export, cleanup/serialization, Holochain finalization/storage, scheduling, and
host response handling. The current ordinary guest build emits neither the
fine-grained adapter timer nor commit-performance breakdown. `MAP_PROFILE=1`
and `WASM_LOG=info` do not enable those compile-time guest profiling features.
We cannot partition this interval or assign its cause from this capture.

The detailed November 4 run recorded 29.275 s from its **later guest adapter
return marker** to host call completion. Because that start boundary differs
from the present **loader completion marker**, subtracting the two intervals
would not establish a regression in return processing. What this run does show
is that the long bulk-load return interval remains despite much faster small
read invocations in the separate matched backport diagnostic.

## Interpretation and limits

Large Core Schema loading remains around 80 seconds: essentially unchanged on
the matching historical command timer, despite modestly more imported work.
The 2.8% difference from the latest UI baseline is small, uses different timer
boundaries, and comes from single samples; it does not establish a persistent
regression. Space Navigator import is substantially faster in this capture.

This is a historical application comparison spanning November 4 to November 19,
with intervening MAP changes, changed schema contents, different launch paths,
and different instrumentation. The latest step-5 baseline used `WASM_LOG=warn`;
the detailed step-4 run and current capture use `WASM_LOG=info`. Current host
logging is `RUST_LOG=host:info`; step 4 used `host:warn`. Actual running native
and guest artifact hashes were not captured. This does not isolate the
backport's effect on Core Schema provisioning or replace the matched diagnostic.
No completed browser startup/navigation profile was supplied for this run.

## Retained evidence

- [Selected backend markers](selected-backend-markers.txt): settings, native launch,
  loader phases, successful commits, and host completion timers.
- [Comparison data](comparison.json): exact values, timestamps, and baseline identities.
- [Provenance](provenance.json): frozen snapshot byte count/SHA256 and retention limits.

The source is `/private/tmp/map-welcome-fresh-profile-2026-11-19.log`; the frozen
analysis copy is `/private/tmp/map-welcome-fresh-profile-analysis-snapshot.log`.
Both raw files are local-only, not durable public artifacts. Compact supporting
markers are committed here; unrelated application data and publication warning
streams are excluded. A live source can continue growing after the snapshot.
