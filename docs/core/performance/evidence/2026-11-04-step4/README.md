# November 4: step 4 with verified guest artifact

Branch 833, commit `36d72365`. Guest WASM SHA256:
`de3be839c2e38e6fdae4052954c55bf0296eb4b64e4b4b99252d17a786834f41`.
The rebuilt .dna and .happ contain that exact WASM; AbstractPropertyParent,
DS-STRUCT-006 and SavedRelationship markers were verified before startup.

Command: `MAP_PROFILE=1 RUST_LOG=host:warn WASM_LOG=info npm run start:host`.
User performed the application run. Core Schema 82.147 s, base packages 8.315 s,
home Dancer 17.536 s from the UI. Completed Canvas profile at
2026-11-04T11:40:34.510Z: 95.454 s, 429 SDK commands.

Full Rust log snapshot retained locally at
`/private/tmp/map-step4-verified-artifact-2026-11-04/snapshot.log`.
Selected backend markers and the decoded newest browser profile are retained here.
No causal whole-application speedup is claimed from a single run.

Host policy spans contain zero guest calls; their accumulated duration across
this captured run is below one millisecond. During the Canvas profile window,
169 relationship-query guest calls total 53.159 s, including queries inside
selection and materialization. These overlap SDK command measurements.
One effective-descriptor construction and one property-array derived construction
serve four commands each. Two bulk hydration calls total 0.429 s. The logs do not
provide complete per-descriptor registry hit/miss or Extends-walk counts, so this
is evidence of reuse, not proof that all consumers exploit prepared products.


## First and repeated DescribedBy

First navigation at 11:49:21.217 UTC completed in 86.263 s with 383 SDK commands;
repeat at 11:52:06.856 UTC completed in 8.604 s with 372 commands.
Selection: 23 calls / 71.480 s first, 23 / 0.015 s repeat. EHD access:
4 / 3.153 s first, 4 / 3.815 s repeat. Property-array classification:
9 / 4.524 s first, 9 / 2.439 s repeat. Related-holon commands:
59 / 3.233 s first, 58 / 1.479 s repeat. Command timings are nested/overlapping.

Repeat's foreground interval has 24 completed guest calls: 9 key lookups,
12 relationship queries and 3 canonical calls. The canonical calls comprise
one EHD construction and two property-array derived constructions. No guest
calls appear within host policy spans. Module cache: 23 hits, about 0.006 s.

A successful background Commit completed at 11:51:01.282 UTC between navigations
(attempted=1, saved=1). Client successful-persistence handling retires the derived
Session by design. The repeat's EHD/DD reconstruction is therefore consistent
with the agreed blanket retirement policy; a missing registry index is not
established by this observation. The repeat is warm for selection but follows
a derived-session retirement, so it is not a pure unchanged-session DD hit test.
The log has no explicit retirement marker, so lifecycle attribution also relies
on the verified client Commit code path.
