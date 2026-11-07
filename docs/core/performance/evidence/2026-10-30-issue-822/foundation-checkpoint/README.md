# Consolidated foundation checkpoint

Integration inputs: working branch `7a3e64a547ca8a86663da348b866f84fcd515b4e`
and main `f191b72ac550d09dd49e98a2495a675d1430523e`. The merge preserves the
characterization and Step A revisions. Reviewed guidance: DevDocs
`194234974c05ce43ca1c44d3b7f5392321a4218b`, Commit preparation demand and prerequisites.

**Captured** 2026-11-06 UTC at map-holons `63bf97de` (merge `0e3761a7` plus a capture
log-filter fix), DevDocs `1942349`, clean source, guest DNA sha256 `d2363737a873…`. Local checks
and targeted Sweettests passed first: `runtime_behavior_matrix`, `effective_descriptor_tests`,
`commit_performance_tests`, `core_successor_tests` (without the rekey case), and
`key_uniqueness_tests`. The full Sweettest run is deferred to the pre-PR gate. Results:
[analysis](analysis.md).

```sh
bash ../map-dev-docs/docs/core/performance/evidence/2026-10-30-issue-822/foundation-checkpoint/capture-subset.sh \
  ../map-dev-docs/docs/core/performance/evidence/2026-10-30-issue-822/foundation-checkpoint/captured
```

## Reconciliation and attribution

One shared structural-diagnosis store and one frozen validation scope remain. Saved registry
hits restore before source diagnosis. Misses use a shared diagnosis for category routing,
then ValueType/PropertyType accessors or unmaterialized effective-schema computation. Defective
lineages remain diagnosed product errors. Readiness propagation and saved-subject declaration
traversal remain deleted. DS-STRUCT-006 and independent candidate diagnostics are preserved.

The profiling fixture still has 19 prepared definitions/products and 188 package edge requests.
Its category-routing preparation now diagnoses the 17 identities not already diagnosed (previously
zero); full resolver requests fall from 17 to zero. Five products use derived accessors and 14
use fresh schema computation. The abstract universal-contract fixture now asserts zero assessment
structural diagnoses (previously nine). These changes are foundation adoption, not narrowed demand.
Tests changed: `profiling_observes_preparation_without_changing_the_validation_report`,
`abstract_descriptor_universal_contract_needs_no_backend_reads_after_construction`, and
`saved_restoration_attempt_does_not_diagnose_lineage` (owned-registry setup). The lookup counter
control is now `indexed_lookup_counts_only_saved_targets_without_source_diagnosis`.

New captures use `822-v3`, still `broad-preparation`. This records host registry capture,
guest owner restoration and index rebuild, actual received HolonType/derived populations,
indexed lookups/hits, derived acquisitions by category, fresh derived builds, projections from
derived products, and frozen-product reuse. Historical snapshot/scan observations stay unavailable
on this substrate, rather than becoming zero. Envelope encoding has no separate timing because
Sweettest delegates encoding to the conductor.

The wire restoration seam asserts no saved-source cache requests, using a service that panics
on storage access, and verifies the owner/index boundary sequence. The capture records zero
ingress reads and no sample-1 snapshot spike, but only with an empty Session registry.
Host before/after-command governor membership is labeled separately from actual received counts.

`registry-thirtytwo-affected-schema` replaces `registry-thirtytwo-bypass` in the manifest.
Per-reference reuse may change restorations, builds, backend reads and registry populations.
Historical data is untouched. Trace removal, host cache capacity, transport/indexing, derived
reuse, bypass removal and extra category diagnoses belong to Step A → foundation. Compare
foundation → final separately for demand narrowing. Complete ValueType payload work includes
`AffordsOperator` reads even when validation does not consume that field.

Step C still owns consumer demand, local requiredness/governing defaults, ValueType selection,
prepared native kind, navigation/name-index retention, remaining binding-role fallback removal,
and zero assessment-time acquisition/derivation. No Step C narrowing is included here.
