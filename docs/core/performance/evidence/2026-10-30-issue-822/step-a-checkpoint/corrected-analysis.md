# Corrected Step A checkpoint

The checkpoint of record is clean map-holons `f374e25c16a2aec9d5df26c75902a063f4cca675`,
captured on 2026-11-03 with cache capacity 10,000 and the guest `get_rc_holon` trace unchanged.
Step A removes readiness work without reducing package demand or backend/node reads.
The diagnosis-scope correction removes the excess diagnoses, but this smoke capture does **not**
establish a net preparation latency gain across workloads. Untouched spans drift, especially in no-op,
mixed and shared-type. Treat latency as directional and partly environmental; no timing adjustment
or extrapolation has been applied.

## Verification and method

Each comparison re-parses all eight retained raw logs (four workloads on each side), checks each
workload test passed, verifies six ordered samples, clean revisions/artifact labels, runtime/build
foundation, generated schema hashes, environment, and per-sample package/registry invariants.
All checks pass. Source revisions and artifact hashes differ as intended; substrate changes from
`broad-readiness` to `broad-preparation` only in the cache-checkpoint comparison. Cache/Session
warmth labels remain `unavailable`, not inferred from workload names. Raw logs are git-ignored.

Results below use medians of samples 2–5; samples 0 and 1 appear separately. Durations are milliseconds,
and cells show before → after (absolute delta; percentage delta). Counts are requests or observations,
not durations. Missing spans are absent, not measured zero. Marginal span medians do not add exactly
to a median total; nested read-cost spans must not be added to assessment spans.

The generalized script reproduces the historical `comparison.json` **byte-for-byte**. The two new
reports include read-cost spans through `--include-read-costs`; the historical output stays unchanged.
Python compilation passes. Negative controls reject mismatched foundation metadata, changed package
edges, and disagreement between retained raw logs and parsed measurements.

```bash
# From this directory; no captures or input files are rewritten.
python3 compare-captures.py ../cache-10000-checkpoint matched comparison.json
python3 compare-captures.py ../cache-10000-checkpoint corrected corrected-comparison.json --include-read-costs
python3 compare-captures.py matched corrected diagnosis-correction-comparison.json --include-read-costs
```

## Stable work and read boundary

Prepared definitions/products, package edge requests/members, fresh builds, restorations, index
builds, received registry conditions, backend calls, link-query counts and node reads match **every
paired sample** in both comparisons, including samples 0 and 1. No readiness edges, ReadinessDiscovery
or DependencyGrouping spans remain. Candidate InterpretationGuards is present. This is broad preparation,
not declared demand. The following table is for samples 2–5; complete per-sample conditions and
edge totals are retained in both comparison JSON files.

| Workload | Definitions/products | Edge requests/members | Fresh/restored | Index builds | Backend calls/node reads |
| --- | ---: | ---: | ---: | ---: | ---: |
| usage | 127/127 | 1248/547 | 125/2 | 407 | 765/191 |
| no-op | 124/124 | 1213/524 | 124/0 | 398 | 769/193 |
| mixed | 125/125 | 1222/527 | 125/0 | 402 | 770/192 |
| shared-type | 134/134 | 1311/554 | 132/2 | 428 | 772/191 |

Logical cache/reference requests are **not** invariant: diagnosis and resolver paths issue different
logical requests even when backend reads are identical. Thus the correction meets the package/backend
read boundary, not a literal requirement that every logical read count stay unchanged. Only diagnosis,
resolution and role-walk derivation counts change between matched and corrected; builders, restorations
and index counts do not. Timing also changes in untouched spans, as documented below.

## Cache checkpoint → corrected Step A

This isolates Step A on the current foundation and is the checkpoint of record. Machine-readable report: [corrected-comparison.json](corrected-comparison.json).

| Workload / samples | Commit ms | Complete preparation ms |
| --- | --- | --- |
| usage / 2–5 median | 2078.371 → 2061.148 (-17.223; -0.8%) | 1595.979 → 1554.147 (-41.833; -2.6%) |
| usage / 0 | 2107.742 → 1878.464 (-229.278; -10.9%) | 1558.930 → 1553.678 (-5.252; -0.3%) |
| usage / 1 | 4707.099 → 3727.399 (-979.700; -20.8%) | 1597.401 → 1547.605 (-49.796; -3.1%) |
| no-op / 2–5 median | 1898.478 → 2115.609 (+217.131; +11.4%) | 1566.324 → 1754.845 (+188.521; +12.0%) |
| no-op / 0 | 1735.976 → 2073.439 (+337.463; +19.4%) | 1523.172 → 1754.119 (+230.947; +15.2%) |
| no-op / 1 | 1925.078 → 2109.830 (+184.752; +9.6%) | 1573.063 → 1716.428 (+143.365; +9.1%) |
| mixed / 2–5 median | 2192.883 → 2276.393 (+83.510; +3.8%) | 1579.062 → 1713.357 (+134.294; +8.5%) |
| mixed / 0 | 3666.386 → 3604.017 (-62.369; -1.7%) | 1596.995 → 1667.561 (+70.566; +4.4%) |
| mixed / 1 | 2231.266 → 2170.901 (-60.365; -2.7%) | 1601.834 → 1604.591 (+2.757; +0.2%) |
| shared-type / 2–5 median | 3128.851 → 3271.416 (+142.565; +4.6%) | 1754.024 → 1966.665 (+212.641; +12.1%) |
| shared-type / 0 | 2915.777 → 2889.181 (-26.596; -0.9%) | 1707.092 → 1702.642 (-4.450; -0.3%) |
| shared-type / 1 | 4434.754 → 4953.752 (+518.998; +11.7%) | 1684.578 → 1795.727 (+111.149; +6.6%) |

Sample 1 is retained separately because the legacy host snapshot spike is systematic. Host snapshot
construction/shipping remains outside guest preparation; its observations are in the report.

| Workload / samples | Host snapshot construction (ms) |
| --- | --- |
| usage / 0 | 0.000 → 0.000 (+0.000; n/a) |
| usage / 1 | 2448.250 → 1796.738 (-651.512; -26.6%) |
| usage / 2–5 median | 0.738 → 0.697 (-0.042; -5.6%) |
| no-op / 0 | 0.000 → 0.000 (+0.000; n/a) |
| no-op / 1 | 0.000 → 0.000 (+0.000; n/a) |
| no-op / 2–5 median | 0.000 → 0.000 (+0.000; n/a) |
| mixed / 0 | 1323.254 → 1284.375 (-38.879; -2.9%) |
| mixed / 1 | 0.286 → 0.250 (-0.036; -12.6%) |
| mixed / 2–5 median | 0.266 → 0.254 (-0.011; -4.3%) |
| shared-type / 0 | 0.000 → 0.000 (+0.000; n/a) |
| shared-type / 1 | 1625.129 → 1906.312 (+281.183; +17.3%) |
| shared-type / 2–5 median | 0.706 → 0.700 (-0.006; -0.9%) |

### Operation spans

These span observations are not a promise that only touched code changes wall time.

| Workload | Operation | Samples 2–5 median ms | Sample 0 ms | Sample 1 ms |
| --- | --- | --- | --- | --- |
| usage | FreshEffectiveSchema | 411.768 → 398.878 (-12.890; -3.1%) | 425.802 → 402.716 (-23.086; -5.4%) | 406.145 → 395.983 (-10.162; -2.5%) |
| usage | ContractChecks | 85.205 → 83.480 (-1.725; -2.0%) | 87.471 → 88.531 (+1.060; +1.2%) | 96.409 → 83.685 (-12.724; -13.2%) |
| usage | PackageValidation | 119.339 → 83.627 (-35.712; -29.9%) | 121.852 → 88.686 (-33.166; -27.2%) | 130.448 → 83.832 (-46.616; -35.7%) |
| usage | NameIndexes | 540.552 → 534.920 (-5.631; -1.0%) | 554.499 → 553.612 (-0.887; -0.2%) | 534.879 → 529.759 (-5.120; -1.0%) |
| usage | StructuralDiagnosis | 13.656 → 11.775 (-1.881; -13.8%) | 7.446 → 10.040 (+2.594; +34.8%) | 7.665 → 11.897 (+4.232; +55.2%) |
| usage | InterpretationGuards | absent → 0.007 | absent → 0.007 | absent → 0.007 |
| no-op | FreshEffectiveSchema | 417.883 → 478.370 (+60.486; +14.5%) | 415.439 → 504.480 (+89.041; +21.4%) | 434.422 → 469.438 (+35.016; +8.1%) |
| no-op | ContractChecks | 86.367 → 95.772 (+9.405; +10.9%) | 88.309 → 96.769 (+8.460; +9.6%) | 86.521 → 97.638 (+11.117; +12.8%) |
| no-op | PackageValidation | 119.227 → 95.962 (-23.265; -19.5%) | 121.352 → 96.925 (-24.427; -20.1%) | 119.477 → 97.791 (-21.686; -18.2%) |
| no-op | NameIndexes | 560.523 → 600.958 (+40.435; +7.2%) | 568.966 → 610.186 (+41.220; +7.2%) | 568.962 → 589.715 (+20.753; +3.6%) |
| no-op | StructuralDiagnosis | 11.628 → 13.847 (+2.219; +19.1%) | 8.555 → 13.918 (+5.363; +62.7%) | 10.236 → 14.301 (+4.065; +39.7%) |
| no-op | InterpretationGuards | absent → 0.007 | absent → 0.006 | absent → 0.006 |
| mixed | FreshEffectiveSchema | 412.776 → 457.877 (+45.102; +10.9%) | 403.371 → 424.282 (+20.911; +5.2%) | 413.837 → 415.316 (+1.479; +0.4%) |
| mixed | ContractChecks | 176.908 → 167.857 (-9.050; -5.1%) | 178.151 → 170.971 (-7.180; -4.0%) | 178.443 → 185.883 (+7.440; +4.2%) |
| mixed | PackageValidation | 225.186 → 181.957 (-43.230; -19.2%) | 225.440 → 185.273 (-40.167; -17.8%) | 226.650 → 199.657 (-26.993; -11.9%) |
| mixed | NameIndexes | 578.328 → 612.595 (+34.267; +5.9%) | 584.166 → 592.452 (+8.286; +1.4%) | 578.583 → 574.506 (-4.077; -0.7%) |
| mixed | StructuralDiagnosis | 16.316 → 17.355 (+1.040; +6.4%) | 17.000 → 14.575 (-2.425; -14.3%) | 17.962 → 18.686 (+0.724; +4.0%) |
| mixed | InterpretationGuards | absent → 0.014 | absent → 0.014 | absent → 0.014 |
| shared-type | FreshEffectiveSchema | 402.469 → 471.943 (+69.474; +17.3%) | 406.364 → 429.447 (+23.083; +5.7%) | 397.739 → 428.350 (+30.611; +7.7%) |
| shared-type | ContractChecks | 84.005 → 95.037 (+11.032; +13.1%) | 83.645 → 86.335 (+2.690; +3.2%) | 83.964 → 86.585 (+2.621; +3.1%) |
| shared-type | PackageValidation | 119.888 → 95.852 (-24.036; -20.0%) | 119.500 → 87.103 (-32.397; -27.1%) | 119.833 → 87.353 (-32.480; -27.1%) |
| shared-type | NameIndexes | 532.968 → 579.048 (+46.079; +8.6%) | 546.169 → 559.811 (+13.642; +2.5%) | 533.545 → 560.329 (+26.784; +5.0%) |
| shared-type | StructuralDiagnosis | 15.174 → 16.437 (+1.263; +8.3%) | 13.948 → 8.191 (-5.757; -41.3%) | 14.979 → 10.582 (-4.397; -29.4%) |
| shared-type | InterpretationGuards | absent → 0.070 | absent → 0.056 | absent → 0.056 |

### Diagnosis, resolution and logical requests

| Workload | Work | Samples 2–5 counts |
| --- | --- | --- |
| usage | All diagnoses | 15 → 14 (-1; -6.7%) |
| usage | Product-preparation diagnoses | 0 → 0 (+0; n/a) |
| usage | Schema resolutions | 125 → 124 (-1; -0.8%) |
| usage | Role walks | 26 → 26 (+0; +0.0%) |
| usage | Logical requests | 7408 → 6297 (-1111; -15.0%) |
| no-op | All diagnoses | 13 → 11 (-2; -15.4%) |
| no-op | Product-preparation diagnoses | 0 → 0 (+0; n/a) |
| no-op | Schema resolutions | 124 → 122 (-2; -1.6%) |
| no-op | Role walks | 26 → 26 (+0; +0.0%) |
| no-op | Logical requests | 7438 → 6336 (-1102; -14.8%) |
| mixed | All diagnoses | 51 → 29 (-22; -43.1%) |
| mixed | Product-preparation diagnoses | 0 → 0 (+0; n/a) |
| mixed | Schema resolutions | 125 → 121 (-4; -3.2%) |
| mixed | Role walks | 51 → 51 (+0; +0.0%) |
| mixed | Logical requests | 8018 → 6806 (-1212; -15.1%) |
| shared-type | All diagnoses | 29 → 21 (-8; -27.6%) |
| shared-type | Product-preparation diagnoses | 0 → 0 (+0; n/a) |
| shared-type | Schema resolutions | 132 → 124 (-8; -6.1%) |
| shared-type | Role walks | 26 → 26 (+0; +0.0%) |
| shared-type | Logical requests | 7513 → 6374 (-1139; -15.2%) |

### Drift controls

Controls are the twelve spans this change does not touch: PackageDiscovery, every MembershipPrefetch
role, NodeBackend and every Link* read-cost span. Each row summarizes their samples 2–5 median
changes; per-span values are in [corrected-comparison.json](corrected-comparison.json). Movements above roughly 5% indicate latency differences are
partly environmental; they do not establish a new code cost or a causal explanation by themselves.

| Workload | Control median change | Control range |
| --- | ---: | ---: |
| usage | -3.7% | -5.9% to +0.9% |
| no-op | +16.7% | +1.6% to +20.3% |
| mixed | +7.1% | +2.2% to +17.8% |
| shared-type | +11.4% | +1.5% to +25.2% |

## Uncorrected matched Step A → corrected Step A

This isolates the diagnosis-scope correction relative to `ced364a4`; both sides already omit readiness. Machine-readable report: [diagnosis-correction-comparison.json](diagnosis-correction-comparison.json).

| Workload / samples | Commit ms | Complete preparation ms |
| --- | --- | --- |
| usage / 2–5 median | 2217.706 → 2061.148 (-156.559; -7.1%) | 1673.311 → 1554.147 (-119.165; -7.1%) |
| usage / 0 | 2101.591 → 1878.464 (-223.127; -10.6%) | 1754.340 → 1553.678 (-200.662; -11.4%) |
| usage / 1 | 4321.943 → 3727.399 (-594.544; -13.8%) | 1699.381 → 1547.605 (-151.776; -8.9%) |
| no-op / 2–5 median | 1963.189 → 2115.609 (+152.420; +7.8%) | 1640.471 → 1754.845 (+114.374; +7.0%) |
| no-op / 0 | 1925.940 → 2073.439 (+147.499; +7.7%) | 1588.560 → 1754.119 (+165.559; +10.4%) |
| no-op / 1 | 2118.459 → 2109.830 (-8.629; -0.4%) | 1720.259 → 1716.428 (-3.831; -0.2%) |
| mixed / 2–5 median | 2300.843 → 2276.393 (-24.451; -1.1%) | 1714.560 → 1713.357 (-1.203; -0.1%) |
| mixed / 0 | 3589.111 → 3604.017 (+14.906; +0.4%) | 1801.294 → 1667.561 (-133.733; -7.4%) |
| mixed / 1 | 2497.926 → 2170.901 (-327.025; -13.1%) | 1895.883 → 1604.591 (-291.292; -15.4%) |
| shared-type / 2–5 median | 3211.297 → 3271.416 (+60.119; +1.9%) | 1931.142 → 1966.665 (+35.523; +1.8%) |
| shared-type / 0 | 3502.289 → 2889.181 (-613.108; -17.5%) | 2111.693 → 1702.642 (-409.051; -19.4%) |
| shared-type / 1 | 5404.669 → 4953.752 (-450.917; -8.3%) | 2086.427 → 1795.727 (-290.700; -13.9%) |

Sample 1 is retained separately because the legacy host snapshot spike is systematic. Host snapshot
construction/shipping remains outside guest preparation; its observations are in the report.

| Workload / samples | Host snapshot construction ms |
| --- | --- |
| usage / 0 | 0.000 → 0.000 (+0.000; n/a) |
| usage / 1 | 1995.559 → 1796.738 (-198.821; -10.0%) |
| usage / 2–5 median | 0.694 → 0.697 (+0.003; +0.4%) |
| no-op / 0 | 0.000 → 0.000 (+0.000; n/a) |
| no-op / 1 | 0.000 → 0.000 (+0.000; n/a) |
| no-op / 2–5 median | 0.000 → 0.000 (+0.000; n/a) |
| mixed / 0 | 1057.421 → 1284.375 (+226.954; +21.5%) |
| mixed / 1 | 0.284 → 0.250 (-0.034; -12.0%) |
| mixed / 2–5 median | 0.257 → 0.254 (-0.003; -1.0%) |
| shared-type / 0 | 0.000 → 0.000 (+0.000; n/a) |
| shared-type / 1 | 1900.356 → 1906.312 (+5.956; +0.3%) |
| shared-type / 2–5 median | 0.735 → 0.700 (-0.035; -4.8%) |

### Operation spans

These span observations are not a promise that only touched code changes wall time.

| Workload | Operation | Samples 2–5 median ms | Sample 0 ms | Sample 1 ms |
| --- | --- | --- | --- | --- |
| usage | FreshEffectiveSchema | 486.920 → 398.878 (-88.042; -18.1%) | 501.084 → 402.716 (-98.368; -19.6%) | 482.165 → 395.983 (-86.182; -17.9%) |
| usage | ContractChecks | 115.108 → 83.480 (-31.628; -27.5%) | 109.735 → 88.531 (-21.204; -19.3%) | 112.825 → 83.685 (-29.140; -25.8%) |
| usage | PackageValidation | 115.264 → 83.627 (-31.637; -27.4%) | 109.889 → 88.686 (-21.203; -19.3%) | 112.979 → 83.832 (-29.147; -25.8%) |
| usage | NameIndexes | 550.902 → 534.920 (-15.982; -2.9%) | 590.599 → 553.612 (-36.987; -6.3%) | 554.789 → 529.759 (-25.030; -4.5%) |
| usage | StructuralDiagnosis | 12.550 → 11.775 (-0.775; -6.2%) | 11.896 → 10.040 (-1.856; -15.6%) | 10.359 → 11.897 (+1.538; +14.8%) |
| usage | InterpretationGuards | 0.007 → 0.007 (+0.000; +0.0%) | 0.007 → 0.007 (+0.000; +0.0%) | 0.007 → 0.007 (+0.000; +0.0%) |
| no-op | FreshEffectiveSchema | 481.349 → 478.370 (-2.979; -0.6%) | 471.562 → 504.480 (+32.918; +7.0%) | 495.875 → 469.438 (-26.437; -5.3%) |
| no-op | ContractChecks | 119.319 → 95.772 (-23.547; -19.7%) | 118.214 → 96.769 (-21.445; -18.1%) | 124.263 → 97.638 (-26.625; -21.4%) |
| no-op | PackageValidation | 119.478 → 95.962 (-23.516; -19.7%) | 118.368 → 96.925 (-21.443; -18.1%) | 124.426 → 97.791 (-26.635; -21.4%) |
| no-op | NameIndexes | 570.107 → 600.958 (+30.851; +5.4%) | 568.085 → 610.186 (+42.101; +7.4%) | 581.699 → 589.715 (+8.016; +1.4%) |
| no-op | StructuralDiagnosis | 12.216 → 13.847 (+1.631; +13.3%) | 14.386 → 13.918 (-0.468; -3.3%) | 15.156 → 14.301 (-0.855; -5.6%) |
| no-op | InterpretationGuards | 0.007 → 0.007 (+0.000; +0.0%) | 0.007 → 0.006 (-0.001; -14.3%) | 0.007 → 0.006 (-0.001; -14.3%) |
| mixed | FreshEffectiveSchema | 498.647 → 457.877 (-40.769; -8.2%) | 520.327 → 424.282 (-96.045; -18.5%) | 534.614 → 415.316 (-119.298; -22.3%) |
| mixed | ContractChecks | 175.768 → 167.857 (-7.910; -4.5%) | 180.585 → 170.971 (-9.614; -5.3%) | 187.107 → 185.883 (-1.224; -0.7%) |
| mixed | PackageValidation | 189.569 → 181.957 (-7.612; -4.0%) | 194.294 → 185.273 (-9.021; -4.6%) | 201.043 → 199.657 (-1.386; -0.7%) |
| mixed | NameIndexes | 600.593 → 612.595 (+12.001; +2.0%) | 608.469 → 592.452 (-16.017; -2.6%) | 611.087 → 574.506 (-36.581; -6.0%) |
| mixed | StructuralDiagnosis | 16.111 → 17.355 (+1.244; +7.7%) | 22.462 → 14.575 (-7.887; -35.1%) | 17.284 → 18.686 (+1.402; +8.1%) |
| mixed | InterpretationGuards | 0.013 → 0.014 (+0.001; +7.7%) | 0.013 → 0.014 (+0.001; +7.7%) | 0.013 → 0.014 (+0.001; +7.7%) |
| shared-type | FreshEffectiveSchema | 508.195 → 471.943 (-36.252; -7.1%) | 587.727 → 429.447 (-158.280; -26.9%) | 550.897 → 428.350 (-122.547; -22.2%) |
| shared-type | ContractChecks | 116.326 → 95.037 (-21.288; -18.3%) | 143.199 → 86.335 (-56.864; -39.7%) | 130.649 → 86.585 (-44.064; -33.7%) |
| shared-type | PackageValidation | 117.102 → 95.852 (-21.250; -18.1%) | 144.196 → 87.103 (-57.093; -39.6%) | 131.424 → 87.353 (-44.071; -33.5%) |
| shared-type | NameIndexes | 558.731 → 579.048 (+20.316; +3.6%) | 627.835 → 559.811 (-68.024; -10.8%) | 585.346 → 560.329 (-25.017; -4.3%) |
| shared-type | StructuralDiagnosis | 11.871 → 16.437 (+4.566; +38.5%) | 14.310 → 8.191 (-6.119; -42.8%) | 10.047 → 10.582 (+0.535; +5.3%) |
| shared-type | InterpretationGuards | 0.057 → 0.070 (+0.013; +21.9%) | 0.079 → 0.056 (-0.023; -29.1%) | 0.065 → 0.056 (-0.009; -13.8%) |

### Diagnosis, resolution and logical requests

| Workload | Work | Samples 2–5 counts |
| --- | --- | --- |
| usage | All diagnoses | 179 → 14 (-165; -92.2%) |
| usage | Product-preparation diagnoses | 124 → 0 (-124; -100.0%) |
| usage | Schema resolutions | 0 → 124 (+124; n/a) |
| usage | Role walks | 13 → 26 (+13; +100.0%) |
| usage | Logical requests | 6476 → 6297 (-179; -2.8%) |
| no-op | All diagnoses | 181 → 11 (-170; -93.9%) |
| no-op | Product-preparation diagnoses | 122 → 0 (-122; -100.0%) |
| no-op | Schema resolutions | 0 → 122 (+122; n/a) |
| no-op | Role walks | 13 → 26 (+13; +100.0%) |
| no-op | Logical requests | 6541 → 6336 (-205; -3.1%) |
| mixed | All diagnoses | 183 → 29 (-154; -84.2%) |
| mixed | Product-preparation diagnoses | 121 → 0 (-121; -100.0%) |
| mixed | Schema resolutions | 0 → 121 (+121; n/a) |
| mixed | Role walks | 12 → 51 (+39; +325.0%) |
| mixed | Logical requests | 6726 → 6806 (+80; +1.2%) |
| shared-type | All diagnoses | 186 → 21 (-165; -88.7%) |
| shared-type | Product-preparation diagnoses | 124 → 0 (-124; -100.0%) |
| shared-type | Schema resolutions | 0 → 124 (+124; n/a) |
| shared-type | Role walks | 13 → 26 (+13; +100.0%) |
| shared-type | Logical requests | 6553 → 6374 (-179; -2.7%) |

### Drift controls

Controls are the twelve spans this change does not touch: PackageDiscovery, every MembershipPrefetch
role, NodeBackend and every Link* read-cost span. Each row summarizes their samples 2–5 median
changes; per-span values are in [diagnosis-correction-comparison.json](diagnosis-correction-comparison.json). Movements above roughly 5% indicate latency differences are
partly environmental; they do not establish a new code cost or a causal explanation by themselves.

| Workload | Control median change | Control range |
| --- | ---: | ---: |
| usage | -3.7% | -9.5% to +0.4% |
| no-op | +13.6% | +8.8% to +21.0% |
| mixed | +1.2% | -4.9% to +10.5% |
| shared-type | +6.0% | -3.3% to +9.1% |

## Received registry and removed readiness work

Actual conditions vary by sample; the reports retain every condition. Repeated samples 2–5:

| Workload | Registry condition | Readiness edge requests before → after | ReadinessDiscovery / DependencyGrouping removed (ms) |
| --- | --- | ---: | ---: |
| usage | population=4 | 1116 → absent | 29.210 / 4.234 |
| no-op | population=0 | 1089 → absent | 28.379 / 3.975 |
| mixed | population=1 | 1098 → absent | 28.697 / 4.989 |
| shared-type | population=4 | 1179 → absent | 30.367 / 4.359 |

## Interpretation

The one latency signal that holds despite drift is PackageValidation. Against the cache checkpoint
it falls in all four workloads: by 35.712, 23.265, 43.230 and 24.036 ms (19.2–29.9%), including
those whose untouched controls rose 7–17%. This is the removed readiness discovery and grouping.
Step A's exit criteria are met by work counts: package demand, products, restoration decisions and
backend/node reads are unchanged, readiness work is absent, and derivation counts are at or below the
checkpoint (shared diagnosis saves the most in mixed: 51 → 29 diagnoses).

As a consistency check, not an adjustment, compare preparation excluding PackageValidation
with the control median. Each figure is the after/before ratio:

| Workload | Preparation excluding PackageValidation | Control median | Unexplained residual |
| --- | ---: | ---: | ---: |
| usage | ×0.996 | ×0.963 | +3.4% (≈ +50 ms) |
| no-op | ×1.146 | ×1.167 | −1.8% (≈ −26 ms) |
| mixed | ×1.131 | ×1.071 | +5.6% (≈ +76 ms) |
| shared-type | ×1.145 | ×1.114 | +2.8% (≈ +46 ms) |

No-op tracks its drift. The other three sit 3–6% above it. That is within the spread of the controls
themselves, so this smoke capture cannot tell a small remaining cost apart from noise. The
foundation checkpoint before Step C and the final five-run captures will resolve it.

Against the cache checkpoint, usage improves by 17.223 ms in Commit (0.8%) and 41.833 ms in
preparation (2.6%). Its ContractChecks is close to the checkpoint (85.205 → 83.480 ms), with
unchanged role-walk count and zero product-preparation diagnoses. This is compatible with a small
benefit from removed readiness, but one run cannot establish a stable latency effect.

No-op regresses by 217.131 ms in Commit (11.4%) and 188.521 ms in preparation (12.0%). Untouched
PackageDiscovery grows 14.9%, NodeBackend 19.7%, and Link* spans roughly 10.6–20.3%. Mixed preparation
grows 134.294 ms (8.5%), alongside PackageDiscovery +7.1%, NodeBackend +17.8% and LinkPrefix +12.3%.
Shared-type preparation grows 212.641 ms (12.1%), alongside PackageDiscovery +10.1%, NodeBackend
+25.2% and LinkPrefix +17.8%. These broad increases with identical backend work support environmental
drift as a material contributor. They do not prove all regression is environmental; no stable net
gain should be claimed for these workloads from this smoke capture.

Compared with uncorrected Step A, product-preparation diagnoses fall from 121–124 to zero on repeated
samples. Total diagnoses fall by 84–94%, because incidental full diagnosis of package definitions and
vocabulary members is removed. Required candidate/governor and member checks still diagnose. Schema
resolutions return to 121–124, as definitions lacking an already-required diagnosis use the original
resolver; this counter records entry into resolution, not an extra product build. Role walks return
to the original vocabulary classifiers (26, 26, 51, 26), exactly matching the cache checkpoint.

ContractChecks improves 27.5%, 19.7%, 4.5% and 18.3% relative to uncorrected Step A. FreshEffectiveSchema
also decreases, most clearly in usage (18.1%). The no-op total nevertheless increases 7.0% in preparation
while its PackageDiscovery and NodeBackend rise 14.2% and 19.7%; the timing comparison is confounded.
Mixed preparation is effectively flat and shared-type grows 1.8%, despite reduced diagnosis work.
Even usage has >5% drift in some link and node controls versus matched. Work counts demonstrate the
scope correction; wall times do not isolate its exact benefit.

The `StructuralDiagnosis.PreparedDefinition` span measures construction-time required diagnoses,
not just the `PreparedProducts.structural_diagnoses` counter. Its nonzero duration is consistent with
zero diagnoses during the product-preparation phase. InterpretationGuards is tiny (microseconds);
it replaces neither complete package acquisition nor the remaining contract work.

The trace-off diagnostic is preserved separately in
[guest-trace-experiment](../diagnostics/guest-trace-experiment/README.md). It is outside the measurement
chain and does not alter either comparison. The trace removal still awaits the architect’s agreement.
