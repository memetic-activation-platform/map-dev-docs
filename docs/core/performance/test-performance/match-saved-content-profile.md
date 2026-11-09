# MatchSavedContent phase measurement

## Result

On 2026-11-06, the focused `Commit validation correction` scenario passed with temporary
monotonic phase timings. `MatchSavedContent` checked exactly two saved roots: Book and Person.
The execution registry contained 15 records, of which only two were complete saved snapshots.
It did not enumerate or compare the whole schema as saved roots.

| Phase, summed across both roots | Seconds | Share of step |
|---|---:|---:|
| Actual root relationship fetch (`all_related_holons`) | 45.940181 | 84.57% |
| Effective descriptor acquisition | 7.648874 | 14.08% |
| Root descriptor reference lookup | 0.381264 | 0.70% |
| Actual root properties | 0.351003 | 0.65% |
| Prepared relationship enumeration | 0.000023 | <0.01% |
| Relationship policy fields | 0.000043 | <0.01% |
| Expected root properties | 0.000006 | <0.01% |
| Expected root relationships | 0.000006 | <0.01% |
| Member comparison loops | 0.000092 | <0.01% |
| **Whole MatchSavedContent step** | **54.321828** | **100%** |

The nested policy-resolution total was 8.030280 s; it includes descriptor reference lookup,
acquisition, prepared enumeration, and policy fields and must not be added again to the table.
Member-loop timing includes per-relationship logging overhead; the five direct member
comparison calls themselves summed to 0.000076 s. Registry cloning took 0.000003 s.

| Root | Acquisition | Actual relationship fetch | Root total |
|---|---:|---:|---:|
| Book (`4faff5bf` saved snapshot) | 4.565343 s | 25.438438 s | 30.172617 s |
| Person (`abae6331` saved snapshot) | 3.083531 s | 20.501743 s | 24.149179 s |

Book's prepared contract exposed five declared relationships, three definitional:
`AuthoredBy`, `DescribedBy`, and `Predecessor`. Person exposed three declared relationships,
two definitional: `DescribedBy` and `Predecessor`. The expected Predecessor collections are
empty and are still checked. Both member loops terminate cheaply, consistent with saved
identity anchoring and key-only schema stubs.

## Interpretation and limits

The dominant measured cost is obtaining all actual root relationships, rather than recursive
member comparison or reading fields from the prepared descriptor. Effective acquisition is a
secondary cost. These probes do not distinguish registry hits from misses or attribute the
acquisition duration between transport, construction, and restoration.

The saved-reference path reaches `HolonCacheManager::get_all_related_holons` in
`shared_crates/holons_core/src/core_shared_objects/holon_cache_manager.rs`. That implementation
collects declared relationship names, adds available navigable relationship names, and retrieves
each named collection. Therefore the measured fetch phase includes vocabulary discovery and
collection retrieval; it is not a measurement of storage I/O alone. The comparator subsequently
uses only definitional collections from that returned map.

A focused next experiment is to read each collection named by the complete definitional policy
set, rather than fetch every relationship. Such an experiment must retain empty-collection,
extra-member, order, duplicate, and identity checks; reading only names present in the expected
snapshot would weaken the current contract. No such behavior change was made in this capture.

This is one successful instrumented sample. The step's 54.32 s is close to the earlier
50.14–53.42 s [unmodified comparison observations](bounded-rejection.md), but instrumentation
cost and ordinary run variance were not separately measured. No full-suite or CI claim follows.
An earlier launch failed during conductor peer-store initialization before fixture execution
and contributes no measurements here; its log is retained at
`/private/tmp/map-holons-match-saved-profile/run-TV459OuW/test.log`.

## Reproduction and evidence

- [Raw phase markers](match-saved-content-profile.txt)
- [Temporary probe patch](match-saved-content-profile.patch)
- Successful full log: `/private/tmp/map-holons-match-saved-profile/run-aQJixsFx/test.log`

The probes were applied to the two test-harness files only. Their original bytes were restored
after the successful capture; neither the comparison contract nor production code was changed.
The patch is retained for reproducibility and is not installed in the source tree.

After applying the probe patch to the measured source and using existing fresh production DNA,
run in Nix:

```sh
RUST_LOG=warn,saved_content_profile=info,dance_tests::execution_steps::dance_test_runner=info,holons_test::harness::helpers::test_context=info \
WASM_LOG=warn bash scripts/test-run.sh cargo test \
  --manifest-path tests/sweetests/Cargo.toml --test dance_tests \
  commit_validation_correction_acceptance -- --ignored --exact --nocapture
```

The test passed in 164.84 s excluding compilation; bootstrap load/commit was 90.061 s.
Compilation, bootstrap, setup and preceding fixture steps are excluded from the phase table.
The temporary changes passed compilation and the focused integration test. After restoration,
Sweettest formatting, whitespace checks, and a dry-run application of the retained probe patch
passed. The full suite was not rerun for this measurement-only task.

## Follow-up implementation

The source-wide relationship retrieval enhancement was subsequently implemented and
measured with these same probes. See the [bulk retrieval measurement](bulk-relationship-profile.md):
actual relationship retrieval fell to 5.10 s and the complete comparison step to 12.47 s
in that sample. The baseline above remains a record of the pre-enhancement implementation.
