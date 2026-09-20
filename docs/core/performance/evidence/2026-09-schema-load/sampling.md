# Core Schema post-coordinator-return sampling

The unoptimized benchmark was sampled for 10 seconds beginning approximately 0, 15, and 30 seconds after the coordinator's `load_holons_returning` marker. The test passed. This instrumented run's marker-to-conductor-completion interval was 49.99 seconds, versus 41.3–43.5 seconds in the preceding five unsampled runs. Sampling may perturb execution; these are CPU sample distributions, not a wall-time budget.

| Window | System validation / signature verification | Wasmer instance setup | WASM memory growth |
|---|---:|---:|---:|
| 0–10 s | 67.1% | 12.3% | 5.2% |
| 15–25 s | 0% classified | 48.5% | 21.9% |
| 30–40 s | 0% classified | 49.1% | 21.5% |

Percentages are approximate shares of non-waiting stack samples across process threads. Explicit kernel wait leaves are excluded. Classification uses stack ancestry and assigns each exclusive sample to one category. The remainder includes other native work, WASM execution/boundary work, and SQLite; these figures should not be interpreted as exact sequential phase durations. The final flush is not separately timed and the last approximately 10 seconds of this instrumented run are not covered by these windows.

Concrete stacks include cryptographic field operations under signature/system validation; RealRibosome::build_instance_with_store → Wasmer instance construction; and wasmer_vm_memory32_grow → WasmMmap::grow → memory copy. The Wasmer source confirms that growth exceeding reserved capacity allocates a new mapping and copies the prior buffer. The integrity WASM declares a minimum of 17 pages (1,114,112 bytes).

Prior optimized benchmark runs had approximately 18.8–18.9 seconds after the coordinator marker. The unoptimized series had median 41.66 seconds. This supports a controlled build-optimization experiment but is not a new same-session A/B comparison or a promised app speedup.

## Retention and interpretation

This is the preserved summary from the sampling session. Raw stack dumps remain
local and are not included in the repository; the approximate category totals
cannot be independently reclassified from this summary. Recommendations and the
subsequent negative memory experiment are recorded in the investigation page.
