# Issue 811 capture: scalar constraints active

**Captured** 2026-11-12 at map-holons `66267b44` (clean source), with `PropertyValueConformance`
bound and `Length16k` attached to `MapStringValueType`. Same bounded manifest and flags as the
[#822 final capture](../2026-10-30-issue-822/final/README.md), which is the comparison point:
one run of six samples per workload and one bootstrap run.

```sh
export MAP_SWEET_STARTUP_TIMEOUT_SECS=60
python3 scripts/measure-commit-manifest.py \
  --output ../map-dev-docs/docs/core/performance/evidence/2026-11-12-issue-811/captured \
  --runs 1 --samples 6 --bootstrap-runs 1 \
  --exclude registry-eight-miss --exclude registry-eight-hit
```

`compare-811.py` regenerates `comparison.json` and prints the tables summarized here.
Latency is directional at one run per side; work counts are primary.

## Results

- **Work counts.** Every workload now prepares one more reached constraint and its type
  (`Constraint.DescribedBy`, `ConstraintType.Extends`, `ApplicableToDescriptorTypes`,
  `InstanceProperties`). That adds 9 link queries per repeated Commit (15 on a first Commit) and
  changes logical requests by −4% to +4%.
- **Descriptor workload.** Guest validation rose from 553 to 705 ms (repeated median), and every
  sample after is slower than every sample before. The increase is in schema-side construction
  (`PackageDiscovery`, governing navigation, property-type preparation, membership reads), not in
  subject evaluation.
- **Other workloads.** Validation moved between −25% and +7%, with overlapping sample ranges.
  No systematic change.
- **Bootstrap.** 122.2 s before, 107.0 s after, one run each. No regression.
- **Subject-side evaluation.** No subject-phase timing rose on any workload; grapheme counting
  and per-value evaluator selection are below what this capture resolves.

The guest profile line does not emit `prepared_constraint_parameters`, so that count is covered
by unit tests only.
