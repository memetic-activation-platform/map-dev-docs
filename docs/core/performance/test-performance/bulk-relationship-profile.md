# Source-wide relationship retrieval measurement

On 2026-11-06, the focused `commit_validation_correction_acceptance` dance passed
against rebuilt production DNA using the source-wide relationship read enhancement.
The same temporary phase probes used in the [baseline](match-saved-content-profile.md)
were applied for this capture and then restored byte-for-byte. The comparison contract
and fixture remained unchanged: two saved roots, five definitional collections including
empty Predecessor collections, and cheap saved-identity/key-only member comparisons.

| Phase, summed across two roots | Baseline | Bulk retrieval | Reduction |
| --- | ---: | ---: | ---: |
| Actual relationships, including vocabulary discovery | 45.940181 s | 5.104522 s | 88.89% |
| Effective descriptor acquisition | 7.648874 s | 6.854097 s | 10.39% |
| Whole MatchSavedContent | 54.321828 s | 12.474788 s | 77.04% |

| Root | Descriptor acquisition | Actual relationships | Root total |
| --- | ---: | ---: | ---: |
| Book (`4faff5bf` saved snapshot) | 4.413940 s | 3.171050 s | 7.794962 s |
| Person (`abae6331` saved snapshot) | 2.440157 s | 1.933472 s | 4.679797 s |

The five direct member comparisons summed to 61 microseconds. Effective descriptor
acquisition is now the largest measured phase. This change does not alter how that
acquisition works. Its modest observed difference from baseline is not isolated as an
effect of bulk retrieval. Bootstrap load/commit was 92.372 s; the test process finished
in 126.91 s excluding compilation. Bootstrap, setup, and other fixture steps are
excluded from the MatchSavedContent table. The fixture itself ran about 29.80 s.

## Implemented behavior

`HolonCacheManager` retains complete described vocabulary discovery, including declared
relationships omitted by presentation navigation and available inverse relationships.
`RelationshipCache` shares the existing preparation logic: it returns valid resident
collections and obtains missing memberships through one source-wide provider query.
A defined name absent from the physical results becomes an explicit empty collection.
Coverage checks use reusable membership under ordinary policy, generation, and TTL
rules; policy-only Fresh entries do not count as resident membership.

The existing fetch-all dance now also supports a requested relationship set, with
exact descriptor bindings for unresolved policies. It uses the guest's existing
`expand_all_from_source` SmartLink query, rather than the old loop over named cache
reads. This is one membership query for the source; descriptor binding and vocabulary
discovery can still perform their own reads. Retained policy bindings need no rebinding.

Valid retained collections keep their identities, Fresh results return directly for
this call, and malformed or failed responses install no partial new collections.
Bulk target construction shares the named path's SmartLink reference helper and now
accepts keyless targets as named reads already do. Existing cache diagnostic observations
remain available for each logical relationship read.

The enduring contract is in the
[saved-Holon cache specification](../../core-runtime/saved-holon-cache-design-spec.md#complete-source-relationship-reads).

## Validation and limits

- 695 core unit tests passed, including bulk-vs-named sharing, Fresh membership,
  known-empty coverage, TTL expiry without policy reacquisition, atomic failure,
  sealed collections, declared content outside navigation, and direct bulk dance retrieval.
- 17 boundary unit tests passed, including empty-set and policy-binding wire preservation.
- Host workspace check and hApp WASM workspace check passed.
- Production DNA build and the focused correction integration dance passed.
- Temporary phase probes were removed. No comparator or fixture contract was weakened.
- This is one successful sample against one measured baseline. The full dance suite and
  runtime_behavior_matrix were not rerun; no suite-wide timing claim follows.

## Evidence and reproduction

- [Raw timing markers](bulk-relationship-profile.txt)
- Full log: `/private/tmp/map-holons-bulk-relationship-profile/run-DryuQHdm/test.log`
- Reusable probe patch: [baseline probes](match-saved-content-profile.patch)

Rebuild production DNA, apply the temporary probe patch, and run in Nix:

```sh
RUST_LOG=warn,saved_content_profile=info,dance_tests::execution_steps::dance_test_runner=info,holons_test::harness::helpers::test_context=info \
WASM_LOG=warn bash scripts/test-run.sh cargo test \
  --manifest-path tests/sweetests/Cargo.toml --test dance_tests \
  commit_validation_correction_acceptance -- --ignored --exact --nocapture
```

Restore the two harness files after capture. The production implementation adds no
permanent timing probes. The final source also preserves ordinary opt-in cache-read
observations, verified separately after this capture; these are inactive in this run.

## Subsequent complete dance-suite rerun

All three ordinary dance suites subsequently passed, covering all 41 baseline fixtures.
The runtime matrix's fixture time fell from 2044.844s to 515.076s (74.8% reduction);
combined fixture time fell 58.3%. Pristine and query fixture times remained close to
baseline. See the [complete comparison](dance-timings-bulk-relationships-comparison.md)
for all fixture timings, correctness scope, attribution limits, and remaining hotspots.

## Remaining-cost profile

Two subsequent focused captures decomposed the remaining 5s relationship read and
12s saved-content comparison. See the [remaining-cost profile](remaining-saved-content-profile.md).
Physical link retrieval is already about 1.5ms across both sources; repeated policy
preparation and auxiliary host calls dominate the remaining time.
