# Step C checkpoint (consumer-declared preparation)

**Captured** 2026-11-06 UTC at map-holons `9fb59701`: Step C `360231aa` plus a parser fix
that accepts consumer-role `MembershipPrefetch` spans. The guest code is the same as `360231aa`.
Clean source (empty `working-tree.patch`), `822-v3` instrumentation, substrate `declared-demand`,
guest cache 10,000, smoke subset (`usage`, `no-op`, `mixed`, `shared-type`), one run of six samples.

Before capturing, local checks and these targeted Sweettests passed:
- `runtime_behavior_matrix`, `effective_descriptor_tests`, `commit_performance_tests`;
- `core_successor_tests` without the rekey case, `key_uniqueness_tests`;
- `attachment_defaults_tests`, `load_theme_tests`, `visualizer_usage_resolution_tests`.

The comparison point is `../foundation-checkpoint/captured-fed00431/`. `compare-step-c.py`
regenerates `comparison.json`. Implementation notes: [Step C implementation](../step-c-implementation.md).
Results: [analysis](analysis.md).

```sh
bash ../map-dev-docs/docs/core/performance/evidence/2026-10-30-issue-822/step-c-checkpoint/capture-subset.sh \
  ../map-dev-docs/docs/core/performance/evidence/2026-10-30-issue-822/step-c-checkpoint/captured
```
