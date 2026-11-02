# Issue #822 instrumented baseline

The [baseline performance summary](baseline-summary.md) describes measured costs, limitations,
Phase 4/Phase 9 guidance, and a suggested PR paragraph.

Separate [cache-capacity diagnostic results](diagnostics/cache-capacity-comparison.json) test
99 versus 1024 entries; these counterfactual captures are not part of the baseline below.

Successful captures are consolidated under [`baseline/`](baseline/), with one directory per
workload. The set contains 14 Commit workloads, each with five runs and six samples
(420 Commit samples total), plus five bootstrap runs. Aborted, incomplete, and unprofiled
attempts have been removed from this evidence directory.

[`baseline/manifest.json`](baseline/manifest.json) lists the full workload plan and retains the
three original capture manifests in `capture_groups`. This is an assembled baseline, not a
single capture revision. The individual `metadata.json`, `measurements.json`, raw logs, and
working-tree patches were moved without changing their contents. All 120 selected capture
files were checked byte-for-byte during consolidation.

| Capture revision (map-holons) | Workload directories under `baseline/` | Startup allowance |
| --- | --- | --- |
| `0915d2311ed80deaec61b0ab17b25d72e97151b2` | `usage`, `slot`, `shared-type`, `descriptor`, `new-version`, `mixed`, `no-op` | Upstream 10-second default |
| `bfd2a86479cb993824d08c4e1c188b526bbeb94f` | `graph-only`, `graph-only-overlap`, `registry-zero`, `registry-eight-miss`, `registry-thirtytwo-hit` | Upstream 10-second default |
| `f6c25b8a29d5d9ebf90c0abc3281fac712a8874a` | `registry-eight-hit`, `registry-thirtytwo-bypass`, `bootstrap` | Explicit 60-second allowance |

The semantic baseline is `3d053ba8becbac13496d7531abea8ce9a5303c53`. Phase 1 instrumentation
was committed at `95b9966337d6fe70f4b7685544b72089f7be9b35`. Each selected capture used the
same profiled DNA artifact:

```text
SHA-256: 9ef52c2b3195be915ba250551f15cd828b31089f857a12ed60dfcc65488f4c82
```

The Commit captures record instrumentation `822-v2`, substrate `broad-readiness`, Holochain
`0.7.1`, HDK `0.7.1`, and HDI `0.8.1`. The original per-workload metadata remains authoritative
for all recorded conditions, including unavailable cache/Session labels; consolidation does
not fill missing observations or establish a performance conclusion.

The startup allowance changed only conductor initialization, outside the timed Commit command.
Bootstrap's end-to-end total includes initialization and must be compared with its own recorded
startup conditions. Bootstrap retains loader observations separately from ordinary Commit samples.

Raw `run-*.log` files remain alongside each capture locally and are still excluded by the existing
Git ignore policy. Their presence on disk does not mean they are included in a documentation commit.
Parsed measurements, metadata, patches, and manifests provide the tracked capture records.
