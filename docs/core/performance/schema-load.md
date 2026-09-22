# Core Schema load performance

**Status:** open investigation. **Measurements:** September 19–20, 2026.
This record captures implementation observations, not new validation or caching
contracts. Schema-load performance is separate from the functional closeout of
[map-holons #706](https://github.com/evomimic/map-holons/issues/706).

This is one part of the broader [application startup investigation](startup-and-canvas.md).
See [caching lessons](caching.md) for host/guest policy discoveries and future options.

## Scope and architectural references

The measured workload provisions the first Core Schema: 21 bundles, 696 loader
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
