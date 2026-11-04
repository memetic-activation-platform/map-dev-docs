# Issue 831 evidence — October 2026

Before/after measurements for [map-holons #831](https://github.com/evomimic/map-holons/issues/831),
which replaced independent Core-anchor discovery (`ReadinessContext`) and the interim
required-anchor successor restriction with role recognition on definitions reached
through bound references.

> **Caveat.** All results come from runs on one local developer machine, using a
> local Sweettest conductor. They are observations of specific workloads, not
> runtime specifications or production latency guarantees.

## Conditions

| | Before | After |
| --- | --- | --- |
| map-holons revision | `5afe0ff7` (`245fc402` plus measurement harness) | `fc8ff7f9` |
| Captured | 2026-10-27 | 2026-10-28 |
| Anchor-evidence policy | per new-version Commit | retired |

Both sets used macOS 26.6.2 arm64 (10 cores), Rust 1.95.0 in Nix, Holochain/HDK 0.7.1,
HDI 0.8.1, and the DescriptorPackage substrate. Working trees were clean. Each Commit
workload ran 5 fresh-runtime runs × 6 samples (1 first, 5 repeated; one subject per
Commit). Only the Commit command is timed. Repeated samples use new transactions but
grow shared inverse buckets, so they are repeated executions, not identical snapshots.
Bootstrap ran 5 times in fresh runtimes with the ordinary (unprofiled) guest.

These measurements were taken after the Holochain 0.7 upgrade. They are not comparable
with the pre-0.7 timings in [Issue 816 findings](../../issue-816-findings.md).

| Workload | Timed Commit |
| --- | --- |
| VisualizerUsage | One new instance with four outbound members |
| VisualizerSlot | One new instance with a string property and three outbound members |
| New-version | One property-only successor of a saved, non-root PropertySlot |
| Descriptor | One new concrete HolonType descriptor in the saved Core Schema |

## Commit results

Medians of the 25 repeated samples, with ranges where variability matters.

| Workload | Command (ms) | Construction (ms) | Construction link queries | Construction node reads |
| --- | --- | --- | --- | --- |
| VisualizerUsage | 3248 → **2038** (−37%) | 2596 → **1365** (−47%) | 464 → **345** | 183 → **126** |
| VisualizerSlot | 3373 → **2049** (−39%) | 2732 → **1348** (−51%) | 458 → **339** | 180 → **123** |
| New-version | 4521 → **2060** (−54%) | 3899 → **1439** (−63%) | 509 → **339** | 181 → **124** |
| Descriptor | 3329 → **2093** (−37%) | 2611 → **1274** (−51%) | 422 → **304** | 171 → **114** |

First-sample medians follow the same pattern:

| Workload | Command (ms) | Construction (ms) |
| --- | --- | --- |
| VisualizerUsage | 3174 → 2043 | 2534 → 1360 |
| VisualizerSlot | 3213 → 1930 | 2702 → 1321 |
| New-version | 3864 → 1970 | 3396 → 1441 |
| Descriptor | 2896 → 2131 | 2280 → 1320 |

Repeated-sample command ranges narrowed in every workload:

| Workload | Before (ms) | After (ms) |
| --- | --- | --- |
| VisualizerUsage | 2270–3986 | 1901–2208 |
| VisualizerSlot | 2231–3966 | 1804–2301 |
| New-version | 3147–5079 | 1758–2304 |
| Descriptor | 3073–3559 | 1801–2257 |

Link-query and node-read counts were identical in every sample of each workload and
capture; only timings varied.

## Where the change comes from

Removed per Commit (identical in every before sample):

| Removed cost | Link queries | Backend calls | Node reads | Repeated median (ms) |
| --- | --- | --- | --- | --- |
| Readiness resolution (all workloads) | 123 | 123 | 60 | 1352–1490 |
| Anchor-successor restriction, including its lineage evidence (new-version only) | 51 | 51 | 1 | 1167 |

Added per Commit by role recognition on reached definitions, which reads the keys of
records that anchor discovery previously loaded in advance:

| Phase | Link queries | Node reads |
| --- | --- | --- |
| Subject preparation | +2 to +3 | +2 to +3 |
| Package discovery | +2 | +0 to +1 |

Net construction change: −118 to −119 link queries (−170 for new-version) and −57 node
reads.

## Semantic controls

Five controls ran after the timed samples in both instance-creation workloads: valid,
extra property, wrong key kind, undeclared relationship, and missing key, plus a
corrected retry. Status, violation counts, saved counts, finding kinds and rule keys
were identical before and after.

## Bootstrap

One Commit of 1,061 Core holons per fresh runtime; medians of 5 runs.

| Metric | Before (ms) | After (ms) |
| --- | --- | --- |
| Commit validation | 4462 | **3707** (−17%) |
| Commit pass 2 (persistence and links) | 36244 | 37263 |
| Loader total | 45017 | 45308 |
| Bootstrap total | 88823 | 89759 |

Every bootstrap work counter was identical before and after. Validation, the only stage
#831 changed, fell by 755 ms. The ~1 s rise in pass 2 spread evenly across persistence
steps that #831 does not touch, while each session's own runs were tight. It is treated
as session-to-session variation between capture days, not an effect of this change.

## Captured data

`831-before/` and `831-after/` hold the captures summarized above, one directory per
workload plus `bootstrap/`.

| File | Contents |
| --- | --- |
| `metadata.json` | Revision, working-tree status, environment, runtime versions, substrate, run dimensions, and artifact hashes |
| `measurements.json` | Per-sample metrics and first/repeated summaries; the source of the Commit tables |
| `run-*-cases.json` | Semantic control outcomes for each run (instance-creation workloads only) |
| `working-tree.patch` | Uncommitted changes at capture time; empty because both trees were clean |
| `bootstrap/revision.txt` | Revision and working-tree status for the bootstrap runs |

Command and construction times are `commit-baseline.command_us` and
`commit-construction.elapsed_us`; the removed costs are the `ReadinessResolution`
assessment phase and the `anchor-evidence` preparation operation. Raw run logs are not
retained here, so the bootstrap table has no committed source data beyond
`revision.txt`.

## Limitations

- One local developer machine and conductor; no network, hosted-runner, or
  multi-agent conditions.
- Five runs per workload; first-sample statistics rest on five values.
- Before and after were captured on consecutive days, so ambient machine state may
  differ. Counts are exact; timings carry that variation.
- Minimal workloads. Larger or multi-subject Commits were not measured.
