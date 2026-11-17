# Issue 812 capture: enum, default, and holon conformance active

**Captured** 2026-11-16 at map-holons `4931f068` (clean source), with `EnumTokenMembership`,
`EnumMemberNamesUnique`, `DefaultsRequireRequiredProperties`, `DefaultValueConformance`,
`ConcreteDescribingType`, `UniquePropertyMemberBinding`, and `AbstractMemberMinimumEnforcement`
bound. Same bounded manifest and flags as the [#811 capture](../2026-11-12-issue-811/README.md),
which is the comparison point: one run of six samples per workload and one bootstrap run.

```sh
export MAP_SWEET_STARTUP_TIMEOUT_SECS=60
python3 scripts/measure-commit-manifest.py \
  --output ../map-dev-docs/docs/core/performance/evidence/2026-11-15-issue-812/captured \
  --runs 1 --samples 6 --bootstrap-runs 1 \
  --exclude registry-eight-miss --exclude registry-eight-hit
```

`compare-812.py` regenerates `comparison.json` and prints the tables summarized here.
Latency is directional at one run per side; work counts are primary.

## Results

- **Backend work.** Each Commit now reaches two more effective rule bindings
  (`ConcreteDescribingType` and `UniquePropertyMemberBinding` on `HolonType`), three on the
  descriptor workloads, which also reach `AbstractMemberMinimumEnforcement`. Each binding's rule
  costs one `DescribedBy` link query and one node read during package discovery. That is the
  whole backend increase: +2 to +3 link queries and +2 to +3 exact node reads per Commit.
- **Logical requests.** +9 per Commit on single-subject workloads and +30 on `shared-type`
  (eight subjects), +0.3% to +2%. Beyond the binding reads, each subject adds one
  `SubjectPreparation` content request, and prepared-product membership requests rise by 4
  (`usage`), 10 (`descriptor`), and 18 (`shared-type`). None of these reach the backend: only
  the binding reads above do.
- **Latency.** Repeated-sample validation moved between −14% (`descriptor`, 705 to 606 ms) and
  +8% (`registry-zero`, 344 to 372 ms), with no direction shared across workloads. No
  systematic change.
- **Bootstrap.** 107.0 s before, 106.4 s after, one run each. No regression. Bootstrap is the only
  measured path that exercises enum membership, enum-definition, and default-declaration
  preparation, since no Commit workload carries enum values or property descriptors.

The guest profile line does not emit `prepared_enum_definitions` or
`prepared_constraint_parameters`, so those counts are covered by unit tests only.

## Rule dispatch

The opt-in audit build (`npm run sweet:scalar-audit`) asserts that the strict Core bootstrap
dispatches every active value, enum, default, and conformance rule with zero violations.
`UniquePropertyMemberBinding` is attributed only when a populated property name is ambiguous, so
a clean bootstrap does not dispatch it; `EnumTokenNonRetroactivity` remains unimplemented.
