# Visualizer evaluation performance baseline — 2026-11-22

**Status:** baseline captured before the session-retained evaluation implementation.
**Revision:** [1166e4bc](https://github.com/evomimic/map-holons/commit/1166e4bc4490bf824354c72367d86de413b3ed1d),
including the initial-collection rendering and Rust-authoritative child-realization
fixes. The user reported manual verification green at this revision.
This page records implementation evidence; [DAHN evaluation semantics](../hx/dahn-design-spec.md#1454-runtime-index-and-preparation-validity)
and the [Space Session contract](../core-runtime/space-session-design-spec.md)
remain authoritative. No finding 3 runtime changes were made for this capture.

## Evidence and matching

The supplied browser profile starts at 2026-11-22T17:31:55.031Z (10:31:55.031
America/Denver) and reports outcome mounted. Its terminal start timestamp,
1795368664401, matches the 10:31:04 npm-start capture at the same revision.
The inferred mounted endpoint is 17:32:02.334Z. All browser profile values are
preserved in [the normalized JSON](evidence/2026-11-22-visualizer-evaluation-baseline/browser-startup-profile.json).
The [measurement manifest](evidence/2026-11-22-visualizer-evaluation-baseline/measurements.json)
records source paths, captured byte ranges, SHA-256 hashes, conditions, derived intervals
and limitations. The running app log is hashed only through the captured startup
prefix, so later appended activity does not change that evidence range.

One complete packaged startup is correlated here. Three separate disposable-
conductor composition samples supply repeated measurements. Earlier startup
attempts and the separate 4.2 s packaged launch observation are not pooled into
this matched run. Full raw traces remain local temporary artifacts; durable
[compact evidence](evidence/2026-11-22-visualizer-evaluation-baseline/README.md)
is retained here without credentials or unrelated application payloads.

## Full npm start to mounted Canvas

| Sequential boundary | Duration |
| --- | ---: |
| Recorded shell timestamp → first application log | 29.387 s |
| First application log → browser startup profile | 21.243 s |
| Browser startup profile → mounted Canvas | 7.303 s |
| **Recorded shell timestamp → mounted Canvas** | **57.933 s** |

The first interval includes npm preflight checks, hApp and frontend/native builds,
bundling, and executable launch overhead. It is not a standalone build timer.
The shell timestamp was recorded immediately before npm start; it also includes
the small shell/pipeline setup interval. Browser completion is calculated from
the profile's wall-clock run timestamp plus its monotonic elapsed duration, with
millisecond rounding and an assumption of no material wall-clock adjustment.

The first application log is at 17:31:33.788061Z. Navigator handoff is at
17:31:54.938110Z: 21.150 s later and approximately 93 ms before the browser profile.
App-log → mounted is 28.546 s. These are narrower views of the same interval,
not additional durations to add to 57.933 s.

The endpoint is successful Canvas mounting/initialization reported by the app.
Independent pixel paint and physical input-readiness were not measured, and time
spent using the app after mount is excluded.

### Build and native markers

| Reported component | Duration | Boundary |
| --- | ---: | --- |
| hApp Cargo release build | 0.230 s | Cached/incremental invocation, not a clean-build benchmark |
| Angular bundle generation | 2.010 s | Reported frontend bundle interval |
| Native Cargo dev build | 21.730 s | Debug application profile, optimized with debug information |
| Holochain runtime launch | 8.7 s | Rounded native launch marker |
| Provider setup | 8.751 s | Contains native runtime launch; do not add both |
| Retained Space discovery | 213 ms | Existing-store discovery |
| Supported CoreSchema identity lookup | 33 ms | Identity lookup, not schema loading |
| CoreSchema Open phase | 247 ms | Contains the preceding discovery/lookup work |

The log shows retained Space/Open behavior and reuse of the existing runtime,
Agent and Space at handoff. The native markers do not isolate home-Dancer
selection or explain every millisecond before browser initialization. See
[selected source markers](evidence/2026-11-22-visualizer-evaluation-baseline/npm-start-selected-markers.txt).

## Browser startup breakdown

| Phase | Duration | Share of browser wall time |
| --- | ---: | ---: |
| Session ready | 1 ms | <0.1% |
| Open transaction | 1 ms | <0.1% |
| Lookup launch resources | 90 ms | 1.2% |
| Materialize Canvas | 2,633 ms | 36.1% |
| Project Theme | 194 ms | 2.7% |
| Construct Canvas | 4,384 ms | 60.0% |
| **Total** | **7,303 ms** | **100%** |

Materialization and construction together account for 7.017 s (96.1%).
Construct Canvas is a broad owner interval, not exclusively selection time.

The browser profile records 306 command measurements. The most expensive rows are:

| Command | Count | Accumulated duration | Maximum call |
| --- | ---: | ---: | ---: |
| Transaction.DanceV2 | 7 | 4,214 ms | 2,151 ms |
| Holon.Read.GetRelatedHolons | 28 | 1,645 ms | 166 ms |
| Transaction.ResolveComposition | 1 | 703 ms | 703 ms |
| Holon.Write.WithDescriptor | 7 | 469 ms | 463 ms |
| Holon.Read.GetEffectiveDescriptor | 3 | 353 ms | 353 ms |
| Transaction.GetSavedHolonByBaseKey | 10 | 199 ms | 41 ms |
| Transaction.LoadTheme | 1 | 193 ms | 193 ms |
| Holon.Read.GetPropertyValue | 176 | 100 ms | 5 ms |
| Transaction.FetchArtifact | 7 | 8 ms | 3 ms |

Command durations sum to 7,995 ms, exceeding the browser wall interval. They are
not exclusive elapsed components; do not sum them with phase durations or subtract
them to infer unmeasured time. Neither DanceV2 nor GetRelatedHolons can be assigned
entirely to Visualizer selection from this aggregate alone. WithDescriptor is a
measured API operation; its presence does not establish a durable personal write.

## Repeated composition baseline

All three focused owner-directed composition acceptance runs passed. They use
the production coordinator, ordinary client ingress, and disposable stores;
they do not reset the user's retained application store. The recorded toolchain
is rustc 1.95.0 (59807616e 2026-04-14).

| Workload | Run 1 | Run 2 | Run 3 | Median |
| --- | ---: | ---: | ---: | ---: |
| Initial Inspector | 829.990 ms | 782.061 ms | 752.476 ms | 782.061 ms |
| Eighteen Date fields plus inherited Key | 614.297 ms | 630.300 ms | 633.654 ms | 630.300 ms |
| Cold host, existing test Space | 969.488 ms | 989.634 ms | 896.067 ms | 969.488 ms |
| Same-context warm request | 1,014.440 ms | 952.675 ms | 891.468 ms | 952.675 ms |

Initial Inspector and both boundary samples report six shared selections, six
within-round binding reuses, one personal-population request and zero discovery-
population requests. The eighteen-field composition reports two selections,
seventeen binding reuses, two metadata reuses, one personal-population request,
and zero discovery-population requests. These counters describe semantic
operations, not physical database/DHT reads.

Each cold sample records eight host/guest envelopes; the warm sample records
three. Each has one canonical composition invocation. Scalar composition data is
19,271 bytes. Canonical response carriers range from 36,910–36,975 bytes cold to
73,329–73,449 bytes warm. This records carrier growth over the measured pair,
not a proof of unlimited growth. Preserve payload-size accounting in comparison.

Warm-host here means a repeated request in the same host transaction against the
same conductor. Cold-host means a fresh host Runtime against that already-running
conductor/test Space; it is not a process restart or a cold operating-system cache.
These samples exclude executable materialization and browser paint.

## Reproduce the capture

Run from map-holons in the supported Nix development environment. Keep the
matching Node runtime and build profile consistent. Build once before the
composition samples; compilation is not part of their reported resolution timers.

```sh
npm run build:happ

MAP_SWEET_STARTUP_TIMEOUT_SECS=60 WASM_LOG=warn RUST_LOG=warn \
  bash scripts/test-run.sh cargo test \
    --manifest-path tests/sweetests/Cargo.toml \
    --test dance_tests owner_directed_composition_acceptance \
    -- --exact --nocapture --test-threads=1
```

Repeat the focused test three times, retaining each log. It uses disposable test
state. For the packaged startup, first record the revision and a wall-clock start
timestamp, then capture the complete npm start output:

```sh
git rev-parse HEAD
python3 -c 'import time; print(time.time_ns() // 1_000_000)'
MAP_PROFILE=1 RUST_LOG=host:info WASM_LOG=warn npm start
```

In Navigator's Web Inspector, recover the last automatic browser profile:

```js
JSON.parse(localStorage.getItem('map.startupProfiles') || '[]').at(-1)
```

Require outcome mounted and correlate its run with the native log. Compute
npm-start-to-mounted milliseconds as Date.parse(profile.run) + profile.totalMs
minus the recorded shell start timestamp. Capture the profile before more than
five startups overwrite its retained history. Keep the raw profile and log, and
exclude app-use time after mount. Do not time app exit as the startup endpoint.

## Interpretation and comparison protocol

The strongest observed target for registry reuse is the warm repeated request:
it still executes six selections and one personal-population request, with only
a small median elapsed reduction from the cold host. No new candidate discovery
is performed in either sample. The proposed design should demonstrate acquisition
of established results without repeating those selection/personal-evaluation
operations. A retained decision reconstructed after Session reset must be measured
separately from a first evaluation.

The complete npm-start sample includes substantial build and conductor work
outside Visualizer evaluation. A session-local registry adds no durable recovery
guarantee across process restart. Do not predict an equivalent reduction in the
57.933 s end-to-end startup figure from improvements to warm reuse alone.

For the implementation comparison:

1. Record revision and build/logging configuration. Use the same machine, retained
   application environment, Theme, subject, owner/Slot scope and request sequence.
2. Preserve the measured test workloads and all per-run values. Update semantic
   assertions to distinguish initial evaluation, retained acquisition, reset-time
   reconstruction and explicit agent reconsideration, without silently dropping work.
3. Measure at least three equivalent app startups before claiming a startup trend;
   distinguish first rebuild from incremental builds and retained Open from constitution.
4. Compare selection/evaluation counts, personal-population work, metadata
   reconstruction, transport calls/bytes, artifact loading and elapsed time separately.
5. Preserve mounted outcome, configuration, binding/child counts, and inactive-Slot
   behavior. No automatic notifications, staleness detection or reconsideration.
6. Keep profiling conditions matched. The native log contains 18,225
   failed_to_send_publish / NoPeersForLocation warning lines before the browser
   profile starts, and none during its 7.303 s interval. Their performance cost
   is unmeasured; a quieter logging experiment must be a separately labeled capture.

Machine load/thermal state, manual capture Node version/architecture, full screen
paint, and logging overhead were not independently recorded. The single matched
startup is a baseline observation, not a controlled speedup claim.

## Optional quieter startup capture

The original baseline uses RUST_LOG=host:info and includes the publication
warnings counted above. Keep that baseline unchanged. For a separate low-noise
capture, suppress warning-level messages from the publication workflow while
retaining errors:

```sh
MAP_PROFILE=1 RUST_LOG='host:info,holochain::core::workflow::publish_dht_ops_workflow=error' WASM_LOG=warn npm start
```

This filter changes diagnostic output only; it does not disable publication,
retry behavior, transport, or networking. It suppresses all warning-level messages
from that specific workflow, not only NoPeersForLocation messages. Apply it at
process launch; an already-running subscriber does not adopt environment changes.
Record the flag in the new capture. Repeat both control and implementation with
matching logging before attributing a performance change to registry reuse;
quiet/noisy comparisons are a separate experiment.
