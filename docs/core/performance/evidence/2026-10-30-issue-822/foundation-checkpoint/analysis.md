# Foundation checkpoint analysis

**Compared captures.**
- Before: the corrected Step A checkpoint (`../step-a-checkpoint/corrected/`, map-holons `f374e25c`, `822-v2`).
- After: the foundation checkpoint (`captured/`, map-holons `63bf97de`, `822-v3`), taken 2026-11-06 UTC.

Both captures use the smoke subset with one run of six samples per workload, guest cache 10,000 and guest trace removed. Values are medians of samples 2–5 unless noted, and latency is directional. `compare-foundation.py` regenerates `comparison.json`.

## Result

Commit is slower on the consolidated foundation, almost entirely because PropertyType and ValueType products are now acquired as `DerivedDescriptor`s on every Commit. This regression belongs to the Step A → foundation segment. It follows main's product routing; #822's only addition, category-routing diagnosis, costs about 10 ms.

| ms | usage | no-op | mixed | shared-type |
|---|---:|---:|---:|---:|
| Commit command | 2061 → 2621 | 2116 → 2524 | 2276 → 2737 | 3271 → 3393 |
| Guest preparation | 1554 → 2174 | 1755 → 2320 | 1713 → 2321 | 1967 → 2379 |
| Derived PropertyType + ValueType | — → 1059 | — → 1134 | — → 1160 | — → 1028 |
| `LinkPrefix` read cost | 204 → 1008 | 212 → 1100 | 233 → 1161 | 412 → 1189 |
| NameIndexes | 535 → 206 | 601 → 212 | 613 → 212 | 579 → 201 |
| Other guest construction cost | 643 → 363 | 681 → 367 | 686 → 370 | 697 → 361 |
| Fresh effective schemas | 399 → 309 | 478 → 311 | 458 → 299 | 472 → 310 |
| Category-routing diagnosis | — → 10 | — → 10 | — → 9 | — → 9 |

- **Derived acquisition** builds 40–45 descriptors per Commit (26–31 PropertyTypes and 14 ValueTypes) at about 25 ms each, compared with about 3.5 ms for a fresh HolonType schema. These builds issue 245–276 backend link queries, about 6 per descriptor. They are single prefix queries outside the Commit membership prefetch, because the builder reads `Constraints`, `ValidationBindings` and `AffordsOperator` on each lineage member. No product is reused across Commits: the frozen-product reuse count is 0 and the guest receives no derived entries.
- **Offsets.**
  - NameIndexes (−0.33 to −0.40 s) and other guest construction (−0.28 to −0.34 s) fell with identical or higher read counts, consistent with main's guest logging removal.
  - Fresh schema builds fell by 37–40, and PackageValidation fell by 32–112 ms.

## Work counts (usage)

| | Step A | Foundation |
|---|---:|---:|
| Prepared definitions / package edge requests | 127 / 1,248 | 128 / 1,257 |
| Structural diagnoses | 14 | 128 |
| Full schema resolutions | 124 | 0 |
| Fresh schema builds / derived builds | 125 / — | 88 / 40 |
| Logical requests | 6,297 | 9,818 |
| Assessment backend calls / exact node reads | 765 / 191 | 916 / 244 |

Main's schema changes move discovery slightly. Across workloads, prepared definitions rise by 1–5 and package edge requests by 9–45. Diagnoses now cover every non-restored definition for category routing, as recorded in the README. Full resolutions drop to zero.

## Registry transport and sample 1

- **The legacy sample-1 host snapshot is gone.** In Step A it cost 1.80 s (usage) and 1.91 s (shared-type). Sample 1 Commit now takes 2.49 s (was 3.73 s) for usage and 3.29 s (was 4.95 s) for shared-type.
- Registry capture takes 1–2 µs, and ingress restoration takes about 8 µs with zero logical reads.
- **The Session registry is empty in every workload.** Step A carried 4 entries (usage, shared-type) or 1 (mixed), so there are no saved restorations and no registry hits. These results therefore verify transport and the spike's removal only for an empty registry. The registry workloads in the final capture exercise populated transport and restoration.

## Read inventory (usage)

`../diagnostics/derived-read-inventory/` holds an inventory build of `usage` at map-holons `b0d5fe58`, which extends operation-scoped read attribution to derived and fresh builds. It has two samples, and their read inventories are identical, so nothing is reused across Commits.

| Operation | Builds | Logical misses per build | Backend link queries (timed capture) |
|---|---:|---|---:|
| Derived PropertyType | 26 | 4: `AffordsOperator`, `AffordsDance`, `AffordsCommand`, `InstanceKeyRule` | 161 |
| Derived ValueType | 14 | 4: the same four | 84 |
| Fresh effective schema | 87 | 3: `AffordsDance`, `AffordsCommand`, `InstanceKeyRule` | 261 |

- **Derived builds issue about two backend link queries and one node read per build that never pass through the logical cache.** Logical misses explain 107 of the 161 PropertyType queries and 56 of the 84 ValueType queries. `build_derived_descriptor` calls `resolve_core_descriptor("DerivedDescriptor.HolonType")` on every build. In the guest, that is an uncached saved-key lookup (lineage roots, heads, delete check, node read), so the same lookup repeats 40 times per Commit. Payload misses alone resemble fresh builds, which take about 3.5 ms each including their 3 misses. That suggests most of the roughly 25 ms per derived build is this lookup. This split is inferred, not timed.
- **Every prepared definition misses `AffordsDance`, `AffordsCommand` and `InstanceKeyRule`, and derived builds also miss `AffordsOperator`.** The Commit membership prefetch does not cover these relationships, so about 420 single-prefix queries per Commit read mostly empty collections. PropertyType and ValueType products read them because effective-schema projection reads every contribution collection.
- **Lineage ancestors are not the cost.** Only the first derived build misses ancestor content; later builds hit the cache.
- **NameIndexes misses are unchanged from the Phase 5 audit:** `SourceOf` 27, `SourceType` 59, content 72.

## Implications

1. **Attribution.** Report this regression as a foundation cost. Foundation → final then measures #822 narrowing on the same schema and substrate.
2. **Step C priority.** Derived acquisition is now about half of guest preparation. Demand narrowing should acquire PropertyType and ValueType products only for the properties that candidates use.
3. **Descriptor runtime (outside #822).**
   - Resolve the `DerivedDescriptor` type descriptor once per transaction instead of once per build. This is likely the largest single saving.
   - Products are rebuilt on every Commit.
4. **Prefetch and demand (#822 Step C).** Whatever demand Step C keeps for the four unprefetched collections should be prepared in batched form; demand it drops removes the queries outright. PropertyType and ValueType products do not need Dance, Command or key-rule vocabulary for validation.
