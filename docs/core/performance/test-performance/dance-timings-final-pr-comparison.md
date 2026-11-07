# Initial baseline versus final PR checkpoint

This compares the initial branch capture on 2026-11-05 with a new run at map-holons commit `b6f2cd23e4e94cda33b0eda6a138895e346e40f4`. The final run includes every code change in PR #855, including selective Session retention and removal of the bespoke ValidationBindings inventory step. It is cumulative PR evidence, not attribution to any one change.

## Comparable fixture totals

The query and runtime suites passed in the initial invocation; pristine passed on an isolated retry: **41 fixtures completed across the successful suite executions**. The initial invocation reported 2 passed, 1 failed, and 12 ignored because pristine hit a Holochain peer-store timeout before schema loading or fixture assertions. An initial isolated retry hit the same setup timeout. A further isolated retry using the default temporary-storage location passed (1 passed, 0 failed). No code or harness change was made; this does not establish the cause of the setup failures. Fixture names match the initial capture exactly. The bootstrap fixture intentionally has one fewer verification step; its retired assertions and enforcement gaps are documented separately.

Times below exclude builds, conductor/bootstrap, setup before fixture START, and teardown. Both captures use the same timestamp collector and serial dance runner.

| Suite | Initial baseline | Final PR | Change |
| --- | ---: | ---: | ---: |
| pristine_bootstrap_and_loader | 522.736s | 78.905s | -84.9% |
| query_storage_boundaries | 30.719s | 34.173s | +11.2% |
| runtime_behavior_matrix | 2044.844s | 451.932s | -77.9% |
| **All 41 fixtures** | 2598.299s | 565.010s | -78.3% |

## Selected fixture comparisons

| Fixture | Initial baseline | Final PR | Change |
| --- | ---: | ---: | ---: |
| bootstrap_operational_schema | 521.091s | 77.009s | -85.2% |
| Commit validation correction | 62.364s | 5.349s | -91.4% |
| Commit non-root lineage and independent clone | 244.248s | 25.809s | -89.4% |
| Book v1 and Title v2 exact references | 183.422s | 44.792s | -75.6% |
| Simple StageNewVersion Testcase | 230.790s | 107.542s | -53.4% |
| Schema successor membership history | 135.627s | 33.395s | -75.4% |

## Scope and evidence

Initial final-head invocation: `test result: FAILED. 2 passed; 1 failed; 12 ignored; 0 measured; 0 filtered out; finished in 779.29s`.
Isolated pristine retry: `test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 14 filtered out; finished in 190.05s`.
Initial final-head profiled command including builds and artifact audit (pristine setup failed): **795.955 seconds**.
The initial 7,874.427-second npm command included other test targets and is not comparable to this narrower command. No full-npm wall-time percentage is claimed. One successful measured execution per suite is shown; ordinary timing variance applies.

The schema-wide inventory step was removed, not accelerated: its initial 447.840-second check no longer runs. Generic graph/Commit verification and behavioral validation fixtures remain. See [the retirement audit](validation-bindings-verification-retirement.md) for the exact coverage boundary and the unresolved declarative binding-retention gap.

- [Initial baseline](dance-timings.txt)
- [Final timing summary](dance-timings-final-pr.txt)
- [Final machine-readable data](dance-timings-final-pr.json)
- [Final command and source checksums](dance-timings-final-pr-context.json)
- Local initial full log: `/Users/stevemelville/dev/map-holons/.notes/test-profiles/20261106T235335Z-d4c79e20/console.log`.
- Local failed isolated retry log: `/Users/stevemelville/dev/map-holons/.notes/test-profiles/20261107T000733Z-f6d91d5e/console.log`.
- Local successful pristine retry log: `/Users/stevemelville/dev/map-holons/.notes/test-profiles/20261107T000857Z-915ae31b/console.log`.

```sh
nix develop --command env MAP_TEST_RUN_ROOT=/private/tmp/map-852-final-pr-comparison python3 .notes/profile-dance-tests.py -- bash scripts/test-run.sh npm run sweet:dance
```

Successful pristine retry command:

```sh
nix develop --command python3 .notes/profile-dance-tests.py -- bash scripts/test-run.sh cargo test --manifest-path tests/sweetests/Cargo.toml --test dance_tests pristine_bootstrap_and_loader -- --exact --nocapture
```
