# Remaining MatchSavedContent cost after bulk relationship retrieval

Follow-up: the first recommendation is now implemented; see [prepared relationship metadata reuse](prepared-relationship-reuse-profile.md) for behavior, validation and timings. The analysis below records the earlier state.

## Result

Two successful focused `commit_validation_correction_acceptance` runs on 2026-11-06
reproduced the [post-bulk result](bulk-relationship-profile.md). Both used temporary
nested native timing probes and the existing opt-in guest descriptor profiler. The
second additionally measured each bulk policy binding and split descriptor finalization.
No execution or comparison behavior was changed.

| Outer phase, summed across two roots | Capture 1 | Capture 2 |
| --- | ---: | ---: |
| Actual root properties | 0.282476s | 0.306869s |
| Root descriptor reference lookup | 0.279902s | 0.174016s |
| Effective descriptor acquisition | 7.199752s | 6.417611s |
| Actual root relationships | 5.076092s | 5.298756s |
| Five direct member comparisons | 0.000073s | 0.000187s |
| **Whole MatchSavedContent** | **12.838595s** | **12.197809s** |

Prepared relationship enumeration and policy-field reads totalled tens of microseconds.
The table excludes bootstrap and preceding fixture steps. Bootstrap load/commit was
88.408s / 85.184s, and complete test-process durations were 121.89s / 118.51s.
These are profiling samples, not a multi-sample benchmark; opt-in clocks and logs add
unquantified overhead. Their magnitude is close to the prior 12.474788s capture.

## Relationship retrieval: physical membership is already below a millisecond per source

The two source-wide physical link queries returned **four links total**, two per root.
In capture 2, scanning took 1.406ms combined, with another 0.073ms for SmartLink reference
binding and grouping. This is consistent with the 1.464ms combined scan/group total in
capture 1. There is no evidence that physical target retrieval or member comparison is
the remaining multi-second cost.

| Inside actual root relationship retrieval | Capture 1 | Capture 2 |
| --- | ---: | ---: |
| Available descriptor enumeration | 0.405439s | 0.420957s |
| Available relationship name resolution | 0.914518s | 1.209684s |
| Cache membership operation, including provider | 3.755215s | 3.667166s |

Declared descriptor enumeration, declared names, cache coverage, preparation, validation,
sealing, and installation were each at microsecond scale. The first row includes two
`get_holons_by_ids` calls. The second includes six `get_holon_by_id` calls, primarily
while resolving relationship names. The current prepared navigation accessor hydrates
members; following inverse names can require further saved-node reads.

Inside the two bulk guest calls, capture 2 measured **107 policy-binding operations**,
summing to **3.271723s** and **369 link queries**. Most individual bindings were roughly
12–44ms; the initial `OwnedBy` bindings cost 153.5ms and 176.9ms while warming candidate
schema state. The full guest bulk dispatch summed to 3.282147s. The difference from the
3.666328s host backend total belongs outside the timed guest dispatch.

Each binding calls `bind_relationship_policy`: resolve source vocabulary/candidates,
select the exact descriptor, and acquire its derived membership policy. It is required
for names whose cache entry has no retained policy association. The current host bulk
call asks the guest to do this even when a completed effective descriptor's prepared
relationship metadata already contains corresponding names and policy values.

Book/Person complete outbound vocabularies include many inherited/inverse names, most
empty for these instances. The comparator uses three Book definitional collections and
two Person definitional collections. Complete `all_related_holons` has a broader return
contract, so the 107 bindings are not five member comparisons. This observation does not
authorize dropping defined empty collections or narrowing the general read API.

The per-name timer encloses the whole binding function. It does not divide candidate
selection from derived-policy acquisition. Therefore the 3.27s is a measured binding
cost, not a claim that all of it is spent inside one scalar-policy accessor.

## Descriptor acquisition: genuine cold preparation plus extra host reads

The host registry lookup itself took about **one microsecond total** in each capture.
Both target types were cold and required construction after the successful Commit's
Session reset. The code already uses registry-first `acquire`; bypassing Session
retirement is not an optimization proposed by this evidence.

| Inside effective descriptor acquisition | Capture 1 | Capture 2 |
| --- | ---: | ---: |
| Build canonical invocations | 0.730525s | 0.722924s |
| Execute/bind canonical transport | 3.773956s | 3.671872s |
| Narrow response and require response body | 0.780491s | 0.656117s |
| Publish to host registry | 1.914711s | 1.366561s |

These acquisition rows are disjoint at this level. Their children must not be added
again. In capture 1, the first registry publication cost 1.914658s and included nine
auxiliary guest calls; the second cost 53 microseconds. Response narrowing cost
0.780456s on the first type and 35 microseconds on the second. This exposes a substantial
first-use cost for core descriptor/registry/response schema resolution on the host.
The timers cover the complete publication operation, including creating its root; they
do not attribute that whole duration to insertion into the registry map.

The guest descriptor construction counters report **597 link queries** across the two
types. The second capture split its previously large `finalize` interval:

| Guest construction phase | Combined time | Link queries |
| --- | ---: | ---: |
| Initial lineage and authoritative collection reads | 0.016960s | 18 |
| Navigation/cardinality preparation | 0.151715s | 222 |
| Allocate/populate result graph | 0.056619s | 4 |
| **PreparedSchema::compute** | **2.799237s** | **353** |
| Write prepared property / kind products / common products / seal | 0.004925s | 0 |

`PreparedSchema::compute` prepares relationship names, directions and scalar policies
for the union of declared contract members and navigation members. This broad policy
preparation dominates the measured guest construction. The separately timed bulk
binding then resolves policies again in another guest request. The shared policy
contract is appropriate; reuse across these boundaries is the opportunity to examine.

Canonical guest request validation also consumed time (about 0.32s combined in capture 1).
Complete canonical envelope/dispatch was about 3.50s there, compared with 3.77s in the host
backend timer. Serialization and scheduling are not separately isolated by these probes.

## Invocation count and host boundary cost

The complete comparison made **34 top-level guest invocations** in both captures:

| Invocation | Count |
| --- | ---: |
| Fetch one saved node | 14 |
| Named relationship query | 9 |
| Saved lookup by key | 5 |
| Bulk saved-node hydration | 2 |
| Bulk source relationships | 2 |
| Canonical effective-descriptor construction | 2 |

Thirty are within the policy/relationship scopes; two actual-property node reads and
the two canonical calls complete the count. Many simple operations take roughly
0.1–0.2s in the native backend while their guest adapter work takes only 1–2ms.
Host request capture and response pool binding are at microsecond scale, and pools are
small (canonical requests/responses contain only a handful of transient holons).
The gap includes conductor dispatch, WASM setup, transport encoding/decoding and scheduling;
these probes do not isolate those contributions. Reducing serial invocation count is
necessary alongside reducing guest preparation to reach a sub-second total.

## Implications for the sub-second target

Measured priorities, not implemented changes:

1. Reuse already prepared exact relationship bindings and scalar policy/name metadata
   for complete source reads. Preserve source/type identity, declared/navigation filters,
   inverse semantics, known empties and Fresh/TTL behavior. Avoid both re-resolving names
   through saved definitions and repeating guest policy construction. Prepared scalar
   names alone are not sufficient to manufacture descriptor IDs from identity strings;
   runtime binding must retain exact saved references/IDs and reject ambiguity.
2. Optimize cold effective-descriptor policy preparation and first-use host response /
   registry schema resolution. These are independently multi-second even if membership
   fetching becomes cheap. Keep the existing Session reset and validation contracts.
3. For this assertion, evaluate fetching the complete **actual definitional set** already
   identified by its policy step in a supported batch. The existing comparator checks
   only that set. Any implementation must still detect extra members, missing expected
   members, empty Predecessor collections, ordering and duplicates; selecting only names
   present in the fixture expectation would weaken the contract. This is an assertion
   execution optimization to design, not a change to `all_related_holons` semantics.

The physical link reads and five direct comparisons are compatible with the target.
A sub-second complete check has **not** been demonstrated. The current cold preparation
and 34-call execution shape must change to achieve it.

## Evidence, reproduction, and cleanup

- [Capture 1 raw markers](remaining-saved-content-profile-1.txt)
- [Capture 2 raw markers](remaining-saved-content-profile-2.txt)
- [Machine-readable aggregates and individual bindings](remaining-saved-content-profile.json)
- [Temporary instrumentation patch](remaining-saved-content-profile.patch)
- Capture 1 full log: `/private/tmp/map-holons-remaining-profile/run-vcRbIao0/test.log`
- Capture 2 full log: `/private/tmp/map-holons-remaining-profile-deep/run-VcFhCh8J/test.log`

Both focused integration runs passed. All instrumented source files were restored
byte-for-byte to their pre-measurement contents. The ordinary production DNA build,
format checks, whitespace checks, and dry-run application of the saved probe patch
passed after restoration. No permanent runtime/harness change was made in this pass.
The previously successful 41-fixture dance run was not repeated for measurement-only probes.

To reproduce capture 2, apply the probe patch to the corresponding post-bulk source,
build the opt-in profiling DNA inside Nix, pack it, and run the focused test:

```sh
cd happ
CARGO_TARGET_DIR=target cargo build -p holons_integrity -p holons --release \
  --target wasm32-unknown-unknown --features holons/descriptor-performance-profiling
hc app pack workdir --recursive
cd ..
RUST_LOG=warn,saved_content_profile=info,saved_content_detail=info,dance_tests::execution_steps::dance_test_runner=info,holons_test::harness::helpers::test_context=info \
WASM_LOG=warn bash scripts/test-run.sh cargo test \
  --manifest-path tests/sweetests/Cargo.toml --test dance_tests \
  commit_validation_correction_acceptance -- --ignored --exact --nocapture
```

Restore all patched files afterward and rebuild ordinary DNA with `npm run build:happ`.
