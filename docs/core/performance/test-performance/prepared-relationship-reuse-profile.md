# Prepared relationship metadata reuse

The first recommendation from [remaining MatchSavedContent profiling](remaining-saved-content-profile.md)
is implemented. Saved reads reuse already prepared relationship names and exact policy
associations. Cold descriptor construction and auxiliary host-call optimization remain separate work.

## Focused result

The final implementation passed `commit_validation_correction_acceptance` on 2026-11-06.
The following sums both saved roots, using the same temporary outer probes as the
[post-bulk baseline](bulk-relationship-profile.md):

| Phase | Post-bulk baseline | Prepared reuse |
| --- | ---: | ---: |
| Actual root relationships | 5.104522s | 0.148242s |
| Effective descriptor acquisition | 6.854097s | 6.868866s |
| Whole MatchSavedContent | 12.474788s | 7.687909s |

Relationship retrieval meets the sub-second target in this focused capture. The whole
comparison remains above target; effective descriptor acquisition dominates it. These
are individual profiling samples, not a statistical benchmark. Timing variation in cold
acquisition is not evidence of an implemented cold-preparation optimization.

## Implementation and correctness

- EffectiveHolonDescriptor projects prepared names and policies against exact saved
  descriptor references. Display identities are matched, never parsed into IDs.
- Complete content reads include every declared contract member plus filtered singular
  and plural navigation, preserving inverse identity and maximum-zero filtering.
  Metadata-only reads do not warm saved descriptor nodes.
- The relationship cache consumes prepared bindings only when it has no retained policy.
  Named and requested-set reads use a resident, unexpired DescribedBy association to
  locate existing preparation without new schema discovery. Missing preparation retains
  ordinary provider binding.
- Descriptor sources whose declared instance contract includes Extends retain guest
  binding of unresolved policies, because their own ancestry may add SourceOf candidates beyond the describing
  type's preparation. Complete reads can still reuse their prepared names.
- Reuse, Fresh, bounded age, RequireFresh, known-empty memberships, generation checks,
  Session retirement and atomic installation after successful bulk retrieval retain their
  established meaning. A prepared policy alone does not establish fetched coverage.
- No transport payload or MatchSavedContent assertion contract changed.

Validation: 700 core unit tests, 17 boundary unit tests, host workspace check, hApp WASM
workspace check, production guest/DNA build, formatting, and the focused integration test
passed. A subsequent [ordinary three-suite dance rerun](dance-timings-prepared-relationships-comparison.md)
also passed all 41 fixtures. Full npm test was not rerun. The prior bulk change's broad
regression run is recorded separately.

## Evidence and reproduction

- [Final capture](prepared-relationship-reuse-profile-3.txt)
- [Exploratory capture](prepared-relationship-reuse-profile-1.txt), before the final
  descriptor-source fallback safeguard and projection cleanup; not the final-code sample.
- [Safeguard experiment](prepared-relationship-reuse-profile-2.txt): the guard incorrectly
  tested all navigation for Extends. Book/Person also have navigable Extends, so policy
  binding returned to the guest and retrieval rose to 3.790128s. The final guard tests
  only the declared instance contract, with a unit regression for this distinction.
- [Machine-readable phase totals](prepared-relationship-reuse-profile.json)
- Existing [outer timing patch](match-saved-content-profile.patch), applied temporarily
  for all three captures and removed afterward. Production guest artifacts contain no new probes.

Rebuild ordinary DNA with `nix develop --command npm run build:happ`. Apply the outer
patch temporarily, then run:

```sh
nix develop --command env \
  RUST_LOG=warn,saved_content_profile=info,dance_tests::execution_steps::dance_test_runner=info,holons_test::harness::helpers::test_context=info \
  WASM_LOG=warn MAP_TEST_RUN_ROOT=/private/tmp/map-prepared-reuse-profile \
  bash scripts/test-run.sh cargo test --manifest-path tests/sweetests/Cargo.toml \
  --test dance_tests commit_validation_correction_acceptance -- --ignored --exact --nocapture
```

Restore the original harness files after capture; the probes are not production code.
