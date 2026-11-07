# Final capture

**Captured** 2026-11-06 UTC at map-holons `b2303fc8` (Step C `360231aa` plus the parser and
manifest-runner fixes; guest code unchanged since `360231aa`), clean source, `822-v3`, substrate
`declared-demand`, guest cache 10,000. Every Commit workload records `b2303fc8` as both guest
artifact and semantic revision.

The bounded manifest was run with **one run of six samples per workload and one bootstrap run**,
omitting `registry-eight-miss` and `registry-eight-hit`. That is a deliberate reduction from the
planned five runs: the smoke checkpoints already established the Step C effect, and every repeated
workload changed by more than 60%, so additional runs would not change a conclusion. Latency is
directional; work counts are primary.

```sh
export MAP_SWEET_STARTUP_TIMEOUT_SECS=60
python3 scripts/measure-commit-manifest.py \
  --output ../map-dev-docs/docs/core/performance/evidence/2026-10-30-issue-822/final/captured \
  --runs 1 --samples 6 --bootstrap-runs 1 \
  --exclude registry-eight-miss --exclude registry-eight-hit
```

`compare-final.py` regenerates `comparison.json`. Results: [analysis](analysis.md).
