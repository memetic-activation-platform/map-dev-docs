# Step C checkpoint analysis

**Compared captures.**
- Before: core lookup reuse (`../foundation-checkpoint/captured-fed00431/`, map-holons `fed00431`, `broad-preparation`).
- After: Step C (`captured/`, map-holons `9fb59701`, `declared-demand`).

Same conditions: smoke subset, one run of six samples, guest cache 10,000, empty Session registry.
Values are medians of samples 2–5 unless noted; latency is directional.

## Result

Consumer-declared demand removes most of Commit preparation. Guest preparation falls 52–71% and
Commit 33–64% in every workload. The reduction comes from acquiring fewer descriptors, not from
moving work: package edge requests, logical reads and backend link queries fall by similar
proportions.

| | usage | no-op | mixed | shared-type |
|---|---:|---:|---:|---:|
| Commit command (ms) | 1859 → 663 (−64%) | 1630 → 657 (−60%) | 1826 → 995 (−46%) | 2548 → 1701 (−33%) |
| Guest preparation (ms) | 1391 → 423 (−70%) | 1434 → 412 (−71%) | 1420 → 675 (−52%) | 1648 → 677 (−59%) |
| Acquired products | 128 → 3 | 129 → 8 | 130 → 23 | 135 → 3 |
| Package edge requests | 1,257 → 47 | 1,258 → 45 | 1,267 → 105 | 1,320 → 47 |
| Logical requests | 9,818 → 1,376 | 9,946 → 1,638 | 10,761 → 3,200 | 9,944 → 1,495 |
| Assessment link queries | 923 → 223 | 947 → 245 | 945 → 353 | 930 → 230 |
| Assessment node reads | 205 → 107 | 211 → 113 | 210 → 151 | 205 → 107 |

For historical reference, the cache-99 baseline `usage` Commit was 2.84 s with 127 prepared
definitions, and the corrected Step A checkpoint was 2.06 s.

- **Acquired products.** `usage` now acquires the VisualizerUsage contract, its one effective
  property and that property's ValueType. Its seven relationship members still receive diagnosis
  and endpoint checks but are no longer built as full products. Before Step C, every endpoint type,
  constraint, rule and Schema reached by the broad walk was acquired (88 fresh and 40 derived builds).
- **Samples 0 and 1** match later samples (`usage` 836 and 817 ms), so there is no first- or
  second-Commit spike.
- **Validation outcomes are unchanged.** Each workload asserts its own outcome, and the targeted
  Sweettests passed before capture.

## Where preparation goes now (`usage`, ms)

| Operation | `fed00431` | Step C | Link queries |
|---|---:|---:|---:|
| MembershipPrefetch (all roles) | 470 | 93 | 343 → 54 |
| Navigation (lineage `SourceOf`, member `SourceType`) | — | 98 | — → 67 |
| NameIndexes | 213 | 3 | 86 → 0 |
| Fresh effective schemas | 314 | 1 | 261 → 0 |
| Derived PropertyType + ValueType | 209 | 43 | 167 → 6 |
| ContentRetention | 100 | 30 | — |
| StructuralDiagnosis | 21 | 19 | — |
| ContractChecks | 54 | 4 | — |

- **Navigation inputs are now attributed separately.** Before Step C, the same lineage `SourceOf`
  and member `SourceType` reads ran inside NameIndexes. They now run in their own span ahead of
  index construction, and NameIndexes issues no backend reads. Navigation is the largest remaining
  schema-side operation (98–117 ms, 67–76 link queries, single-name prepares per member).
- **Payload-collection prefetch** covers the collections that used to miss for every build.
  Batched prefix reads dominate (75–112 ms). The count-probe (12–17 ms) and single-scan (5–12 ms)
  strategies still run for a minority of requests, as they did before Step C (55–62 and 36–38 ms).
- **The first derived build carries a fixed cost.** In `usage` and `shared-type` a single
  PropertyType build takes 42–53 ms, against about 5 ms per build when 26 builds shared the
  warm-up (`no-op`: 6 builds in 49 ms; `mixed`: 15 in 58 ms). It includes the transaction's first
  `DerivedDescriptor.HolonType` key lookup and first reads of the PropertyType lineage.
- **Checks moved into construction.** ContractChecks, BindingDispatch, SchemaChecks and
  DeclarationChecks now run before `PackageValidation`, which reports 0. Their combined cost fell
  (ContractChecks 54 → 4 ms), so this relocation adds nothing to preparation.

## Cost outside preparation

- **Cold-start costs moved later in `usage`.** DS-KEY-006 key evidence
  (`saved_lineage_roots_by_key`) rose from 7 to 40 ms, and the owns-key lookup from 8 to 24 ms.
  These are the same single queries; the broad walk used to warm them. In `shared-type`, where 8
  subjects already paid the cold cost, key evidence is unchanged (248 → 256 ms).
- **`shared-type` is now dominated by subject work,** not schema preparation. Key evidence
  (256 ms, one lineage-root scan per subject) and persistence pass 2 (451 ms) together exceed its
  remaining schema preparation. Both are outside #822.
- About 150 ms of `usage` Commit time outside the guest adapter also disappeared (command minus
  adapter total, 272 → 123 ms). Current spans do not attribute it.

## Implications

1. **#822's narrowing goal is met on the smoke subset.** The final capture (Phase 10) should confirm
   it on the registry and bootstrap workloads, where saved restoration is exercised.
2. **Remaining schema-side levers** are navigation preparation (single-name `SourceType` prepares
   could batch) and the per-Commit derived-build warm-up. Neither is required for #822.
3. **Cross-Commit reuse of derived products** matters less now: one or two derived builds remain
   per Commit in these workloads.
4. **Subject-side costs** (DS-KEY-006 lineage-root scans, persistence pass 2) are the largest
   remaining Commit costs for multi-subject workloads, and belong to separate issues.
