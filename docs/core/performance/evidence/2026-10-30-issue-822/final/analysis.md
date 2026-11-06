# Final capture analysis

**Compared captures.**
- Historical baseline: `../baseline/` (semantic baseline `3d053ba8`, cache 99, `822-v2`, five runs).
- Final: `captured/` (map-holons `b2303fc8`, cache 10,000, `822-v3`, `declared-demand`, one run).

The baseline precedes the cache change, Step A and the #846 foundation, so this is the historical
end-to-end comparison. The matched foundation → Step C comparison exists for the smoke subset in
[`../step-c-checkpoint/analysis.md`](../step-c-checkpoint/analysis.md). "Repeated" is the median
of samples 1–5, as in [`../baseline-summary.md`](../baseline-summary.md).

## Commit workloads

| Workload | First Commit (s) | Repeated Commit (s) | Repeated preparation (s) | Prepared definitions | Package edge requests | Logical requests |
|---|---:|---:|---:|---:|---:|---:|
| `usage` | 2.73 → 0.71 | 2.84 → 0.76 (−73%) | 2.18 → 0.39 (−82%) | 127 → 3 | 2,364 → 47 | 8,180 → 1,376 |
| `slot` | 2.60 → 0.67 | 2.57 → 0.66 (−75%) | 1.66 → 0.41 (−75%) | 124 → 8 | 2,302 → 45 | 7,345 → 1,629 |
| `shared-type` | 3.59 → 1.23 | 3.51 → 1.32 (−62%) | 2.02 → 0.61 (−70%) | 134 → 3 | 2,490 → 47 | 7,607 → 1,495 |
| `descriptor` | 3.71 → 0.81 | 2.61 → 0.87 (−67%) | 2.07 → 0.55 (−73%) | 115 → 17 | 2,157 → 86 | 8,212 → 2,472 |
| `new-version` | 5.26 → 0.84 | 2.66 → 0.79 (−70%) | 2.21 → 0.43 (−80%) | 124 → 8 | 2,302 → 45 | 8,049 → 1,634 |
| `mixed` | 3.71 → 0.96 | 2.87 → 0.91 (−68%) | 2.22 → 0.64 (−71%) | 125 → 23 | 2,320 → 105 | 8,840 → 3,200 |
| `no-op` | 2.37 → 0.70 | 2.42 → 0.72 (−70%) | 2.15 → 0.41 (−81%) | 124 → 8 | 2,302 → 45 | 8,215 → 1,638 |
| `graph-only` | 2.62 → 0.68 | 2.76 → 0.52 (−81%) | 2.25 → 0.40 (−82%) | 127 → 3 | 2,364 → 47 | 8,231 → 1,381 |
| `graph-only-overlap` | 2.78 → 0.47 | 2.74 → 0.71 (−74%) | 2.23 → 0.42 (−81%) | 127 → 3 | 2,364 → 47 | 8,251 → 1,420 |
| `registry-zero` | 2.65 → 0.89 | 2.73 → 0.91 (−67%) | 2.13 → 0.46 (−78%) | 127 → 3 | 2,364 → 47 | 8,173 → 1,376 |
| `registry-thirtytwo-hit` | 3.12 → 0.68 | 3.30 → 0.77 (−77%) | 2.37 → 0.47 (−80%) | 127 → 3 | 2,364 → 47 | 8,192 → 1,376 |
| `registry-thirtytwo-affected-schema` | 2.95 → 1.23 | 2.56 → 0.93 (−64%) | 1.50 → 0.61 (−60%) | 115 → 17 | 2,157 → 86 | 7,460 → 2,472 |

Baseline edge requests include the removed readiness walk. The affected-Schema workload is the
renamed `registry-thirtytwo-bypass`.

- **Every Commit workload is 62–81% faster** on repeated samples and 58–84% faster on the first.
  The work reduction is larger still: prepared definitions fall 82–98%, edge requests 95–98%, logical
  requests 64–83%.
- **Workloads shared with the Step C smoke checkpoint repeat it:** the same definition counts, with
  preparation within 10%.
- **Graph-only overlap** passed its branch-evidence checks (overlap buckets, binding interpretation,
  target identities and keys).
- **Sample 1 shows no spike** in any workload.

## Registry workloads

- **The transported registry is restored and used on the first Commit.** In
  `registry-thirtytwo-hit` sample 0, 32 HolonType entries arrive; guest ingress restoration takes
  27 ms and index rebuild 7.6 ms, and the governor is restored from the registry (1 restoration).
  In the affected-Schema workload, 32 entries arrive (34 ms, 6.7 ms) and no demanded saved
  definition is among them, so nothing is restored; the assessment-wide bypass is gone.
- **The host Session registry is empty after the first Commit.** The workload's governor check
  reports `present=true` before sample 0 and `present=false` after it, and samples 1–5 receive an
  empty registry. This is the #846 Session/registry lifecycle, not #822 code, but it means repeated
  registry samples measure an empty registry. The baseline carried 32–35 entries into every sample.

## Bootstrap

| | Baseline `3d053ba8` (5 runs) | Foundation `fed00431` (1 run) | Final `b2303fc8` (1 run) |
|---|---:|---:|---:|
| Total | 93.8 s | 131.2 s | 122.2 s |
| Guest Commit validation | 4.44 s | 5.61 s | 4.40 s |
| Persistence pass 2 | 38.8 s | 49.1 s | 46.9 s |
| Session export after the load | 0.08 s | 13.0 s | 10.1 s |
| Conductor call outside the guest adapter | 36.9 s | 47.4 s | 45.5 s |

`bootstrap-fed00431/` holds the foundation run (clean source, same generated schema of 1,169 holons).

- **The regression belongs to the foundation segment, not #822.** Bootstrap was already 131.2 s
  at `fed00431` (+40% over the baseline). Step C then made it 7% faster (−9.0 s), with guest
  validation down 22% (5.61 → 4.40 s) on an identical schema.
- **The foundation increase** is mostly Session export (`restore_session_state_from_context`,
  77 ms → 13.0 s; it changed with the #846 registry transport, `887f0f3d`), persistence pass 2
  (+10.3 s) and conductor time outside the guest adapter (+10.5 s, consistent with a larger exported
  response but not attributed by current spans). The generated schema also grew from 1,101 to 1,169
  holons.
- Construction rose from 2.63 to 3.56 s because contract and declaration checks moved into it;
  total validation fell.
- Both bootstrap figures after the baseline are single runs. The baseline's five runs spanned
  0.7 s, so the 9 s Step C improvement is well outside that spread.

## Definition of Done mapping

- **Reduced preparation and discovery work:** above and in the Step C checkpoint.
- **Total Commit latency evaluated:** every workload, first and repeated.
- **Cache and registry infrastructure separated:** cache checkpoint, foundation checkpoint, and
  registry ingress timings above.
- **Significant regressions explained:** bootstrap, above (measured at the foundation). The Step A +3–7% regression was resolved
  by its diagnosis-scope correction; the foundation +0.4–0.6 s regression by `fed00431`.
