# ValidationBindings and inverse-traversal cost

## Result

Subsequent decision: [retire the bespoke inventory verification](validation-bindings-verification-retirement.md), with an assertion audit and explicit declarative-enforcement gaps. The measurements below describe the pre-removal test.

The unchanged pristine suite passed with temporary probes on 2026-11-06. Its
ValidationBindings step took **472.621s**, reproducing the prior 468.983s result.
**452.695s (95.8%)** belonged to a whole-schema occurrence scan. It made 1,158
serial descriptor-associated guest requests to discover empty collections.

A separate controlled traversal checked all **1,168 sources**, all **24 authored
occurrences**, and the absence of additional bindings in **1.052s**. This is diagnostic
evidence, not a committed harness optimization or an end-to-end post-change benchmark.

Both the original pristine suite and the ignored diagnostic passed. All temporary
source changes were restored byte-for-byte; ordinary production DNA was rebuilt.
No assertion or production behavior changed permanently.

## Full step breakdown

| Phase | Work | Seconds |
| --- | --- | ---: |
| Enumeration | Observer context and loaded saved holons | 2.230 |
| Descriptor pair | Forward/inverse shape, endpoints and round-trip name | 3.365 |
| Expected inverse bindings | 24 rule sources, exact owner keys | 10.124 |
| Expected forward bindings | Nine owners, exact rule keys | 3.456 |
| Explicit empty collections | TypeDescriptor forward; CrossSchemaDependenciesDeclared inverse | 0.751 |
| **Whole-schema occurrence scan** | **1,168 sources, expected aggregate 24 occurrences** | **452.695** |
| **Whole step** | Includes logging and small intervening work | **472.621** |

The current code checks 24 bindings on nine owners. The older comment describing
seven C1 occurrences and the approximate 1,060-source note do not describe the full
current inventory. The authoritative executed counts are 1,168 loaded holons, nine
non-empty forward collections, and 24 occurrences. These are holon counts, not a
claim that all loaded holons are ordinary HolonTypes.

## Where the scan time goes

Ten memberships were already reusable: nine populated owners and one explicit empty
root. The remaining **1,158 fetches all returned empty ValidationBindings collections**.
The host cache observations and transport counts agree on those misses.

| Scan measurement | Value |
| --- | ---: |
| Logical reads | 1,168 |
| Resident hits | 10 |
| Host query_relationships calls | 1,158 |
| Sum of timed host transport calls | 452.646s |
| Guest link queries during those dispatches | 100,647 |
| Returned links across those queries, including auxiliary schema reads | 159,467 |
| Direct requested membership reads, including construction of empty collections | 0.769s |
| Requested membership targets returned by the new fetches | 0 |

The direct requested membership query accounts for one of each request's link queries.
The other **99,489 queries** arise around descriptor/name/policy binding. The adapter's
include_relationship_descriptor path calls bind_relationship_policy before retrieving
membership. That function gathers candidates from the describing contract and, for
descriptor sources, the source's own ancestry/SourceOf surface; it then obtains the
exact relationship's derived membership policy. Each ordinary guest call starts with
request-local state, so its schema work is repeated across independent requests.

This preserves the production binding contract. The earlier prepared-policy optimization
intentionally retains guest binding for sources whose declared instance contract includes
Extends, because their own ancestry can add candidates. The cost here is exposed by
making a separate ordinary cached read for every source, primarily to check absence.

This capture does **not** precisely partition the full scan's 452.695s between guest
execution and everything outside the guest. The first adapter clock helper was feature-gated
off, so its zero-valued guest timing fields are invalid and excluded from analysis.
Native timers, guest link counters, and the direct-membership timers use independent
working clocks/counters and remain valid. The controlled sample below fixes the guest
clock before measuring that boundary.

## Inverse traversal is smaller but has the same amplification

The 24 expected ValidationBindingFor reads took **10.124s** and made **2,175 link queries**.
Their 24 direct membership reads took **0.013s** and returned 24 owner occurrences.
The remaining 2,151 link queries are ancillary to the exact descriptor/policy binding.

A corrected-clock sample of three inverse reads (two populated, one empty) made 270
link queries and spent 0.618s inside guest dispatch. The physical inverse membership
is not intrinsically a multi-second operation; repeated resolution and boundaries
surround it. A complete batched inverse rewrite was not implemented or benchmarked.

## Controlled single-source versus multi-source traversal

The diagnostic uses the existing query_relationships compatibility path through
Runtime::execute_command and TransactionAction::Dance. It changes two aspects together:
consolidating sources into one request and requesting actual memberships without
policy associations for cache retention. It therefore tests the combined opportunity;
it does not independently attribute gains to those two changes.

The 20 selected sources include all nine populated binding owners plus empty examples
from meta-types, properties, schema types and validation rules.

| Read shape | Sources | Host elapsed | Guest adapter total | Link queries |
| --- | ---: | ---: | ---: | ---: |
| Individual, descriptor-associated | 20 | 8.413s | 4.331s | 1,725 |
| One membership-only traversal, same sources | 20 | 0.275s | 0.028s | 20 |
| One membership-only traversal, complete loaded set | 1,168 | 1.052s | 0.953s | 1,168 |

All three shapes found the same 24 authored occurrences. For the matched 20-source
comparison, about 4.082s lies outside the timed guest adapter; that includes the
remaining command/conductor/WASM/transport/scheduling work, which is not separated
further. Guest envelope validation, hydration and projection were tiny relative to
4.329s of individual guest dispatch.

The whole-set traversal spent 0.950s in guest dispatch and returned 24 links. It did
not collapse all physical sources into one get_links call: it performed 1,168 local
link queries inside **one guest invocation**. Avoiding repeated policy resolution and
host/guest boundaries is the measured gain.

The diagnostic assertions require:

- Every requested source exactly once, with no omitted or unexpected sources.
- An explicit result collection for each source, including empty collections.
- Exact target saved identities and multiplicity for the 20 sampled sources.
- Empty collections for every other source in the complete traversal.
- Exactly 24 total authored occurrences.

The original full suite separately retained the descriptor-pair, all 24 inverse,
all nine forward, explicit-empty, and whole-schema count assertions.

## Recommended implementation boundary

Keep the existing verification contract and batch its persisted named membership reads.
Start with the whole-schema scan: retain all 1,168 sources and unexpected-binding detection,
while avoiding acquisition of a retention policy for each one-off assertion read. Keep
returned data available to the exact forward/empty checks where appropriate.

The measured scan replacement suggests roughly 451s of avoidable work; it is not a
measured whole-step speedup. About 20s of other work remains in this profile. The inverse
checks are the next batching opportunity, followed by descriptor-pair and enumeration
costs if a lower overall target is required.

The compatibility executor is explicitly marked deprecated, and its existing generic
QueryRelationships test step has a TODO for result matching. The experiment establishes
feasibility; permanent implementation should choose the supported batch-read surface
and add complete result assertions rather than treating that TODO executor as proven
verification. Do not globally remove descriptor associations, change cache freshness,
or narrow the scan to only known positive owners as an incidental optimization.

## Evidence and reproduction

- [Full native phase capture](validation-bindings-profile-full.txt)
- [Controlled sample capture](validation-bindings-profile-sample.txt)
- [Machine-readable counters and timings](validation-bindings-profile.json)
- [Historical full-run probes](validation-bindings-profile-full.patch): guest adapter
  clock fields were disabled; use native timings and counters only.
- [Corrected probes and temporary ignored control](validation-bindings-profile-sample.patch)

The patches are alternatives against map-holons checkpoint 9863d4fb, not cumulative.
The corrected patch can profile either selector. Save current sources before applying
probes, restore them after capture, and rebuild ordinary production DNA.

```sh
nix develop --command npm run build:happ
nix develop --command env \
  RUST_LOG=warn,validation_profile=info,dance_tests::execution_steps::dance_test_runner=info,holons_test::harness::helpers::test_context=info \
  WASM_LOG=warn MAP_TEST_RUN_ROOT=/private/tmp/map-validation-bindings-profile \
  bash scripts/test-run.sh cargo test --manifest-path tests/sweetests/Cargo.toml \
  --test dance_tests pristine_bootstrap_and_loader -- --exact --nocapture
```

With the corrected control patch, select validation_bindings_query_profile_sample using
--ignored --exact --nocapture for the sample instead. The full run preserves preceding
pristine checks and their warming. The sample uses a separate fresh bootstrap and a
specified 20-source control; its timing is not an end-to-end replacement for the full
pristine fixture. Both are individual profiling samples with unquantified probe overhead.

Retained full logs:

- /private/tmp/map-validation-bindings-profile/run-MtLyX35Q/test.log (658.17s test process)
- /private/tmp/map-validation-bindings-sample/run-Wmld7FC6/test.log (107.88s test process)
