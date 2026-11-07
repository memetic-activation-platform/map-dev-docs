# Bounded Commit rejection verification

## Scope and coverage

The `Commit validation correction` fixture opts into fixture-scoped rejection verification.
It stages a Book and Person, with two `DescribedBy` relationships and one `AuthoredBy`
relationship. Removing Title causes rejection; restoring Title allows the same transaction
to commit successfully. The fixture remains in the default runtime behavior matrix.

The rejection adder captures both staged fixture subjects. Before dispatch the executor
requires exact correspondence with the live runtime candidates. Before and after rejection,
saved lookup must report both unique keys absent, and fresh reads of `Instances` on the two
saved descriptors must have unchanged target identity occurrences, including multiplicity.
Ordinary Commit status, empty saved-result, open-transaction, staged-subject, and exact
Title-finding checks remain. The corrected retry and `MatchSavedContent` step are unchanged.

Existing Commit authoring entrypoints retain the original persistence snapshot checks. Only
this fixture opts in. The bounded contract proves client-visible non-persistence and unchanged
named collections; it does not establish absence of inaccessible substrate records. See the
[test-step guide](../../testing/test-step-authoring-guide.md#26-fixture-scoped-rejection-checks).

## Measurement method

Measured locally on 2026-11-06, using the Issue 852 working branches. Production DNA was
rebuilt through `npm run build:happ` in Nix. Native/WASM build time is excluded below.
Each isolated execution uses a fresh disposable conductor and bootstrap, runs serially, and
uses the same focused selector and log filters. Fixture and step times are inferred from
successive START markers and the fixture END marker; they include boundary/logging overhead.

For the control, only the fixture's rejected Commit adder call was temporarily switched back
to `add_commit_step(..., Rejected, ...)`. The surrounding fixture setup, including descriptor
lookups, remained identical. Source was restored automatically after the control. The initial
bounded sample preceded the added unsupported-retry guard; it exercises the same supported
new-root path. The final sample uses the final implementation.

| Execution phase | Existing checks control | Bounded sample 1 | Bounded final sample |
|---|---:|---:|---:|
| Bootstrap load/commit | 87.488 s | 88.183 s | 88.886 s |
| Rejected Commit step | 100.110 s | 4.480 s | 4.298 s |
| Corrected successful Commit | 2.801 s | 3.435 s | 2.690 s |
| MatchSavedContent | 51.886 s | 53.418 s | 50.141 s |
| Whole fixture, excluding bootstrap | 164.610 s | 69.967 s | 67.109 s |
| Whole isolated test, excluding compilation | 256.67 s | 162.73 s | 160.57 s |

All three runs passed. Relative to the control, the bounded samples reduce the rejected
Commit step by approximately 96% and the fixture execution by approximately 57–59%. The broad rejection scan accounts for the measured difference; the
unchanged saved-content check remains a substantial separate cost. No full-suite or CI
speedup is established by these focused runs. This isolated control has a different suite
context from the earlier [dance timings](dance-timings.txt); their absolute fixture durations
are not a matched comparison.

Retained local logs:

- Control: `/private/tmp/map-holons-rejection-baseline/run-yKbO78bh/test.log`
- Bounded sample 1: `/private/tmp/map-holons-bounded-rejection/run-1otLKvCA/test.log`
- Bounded final sample: `/private/tmp/map-holons-bounded-rejection-final/run-hzOXZS3T/test.log`

## Focused rerun

After building fresh production DNA in Nix:

```sh
RUST_LOG=warn,dance_tests::execution_steps::dance_test_runner=info,holons_test::harness::helpers::test_context=info \
WASM_LOG=warn bash scripts/test-run.sh cargo test \
  --manifest-path tests/sweetests/Cargo.toml --test dance_tests \
  commit_validation_correction_acceptance -- --ignored --exact --nocapture
```

The focused entrypoint is ignored to avoid duplicate default execution. The same fixture
continues to run in `runtime_behavior_matrix`. Harness units and all fixture authoring gates
run through `npm run test:unit:sweetests`.

## Validation

The Sweettest library and fixture-authoring gates pass (56 library tests and 4 authoring tests),
including rejection of updates, missing/duplicate keys, staged collection guards, and retained
relationship retries. Negative assertion tests detect leaked saved subjects, operational lookup
failures, extra/missing runtime candidates, and added/duplicated inverse occurrences.
The Dance, disposition, and incomplete integration targets compile with the shared executor;
Sweettest formatting checks pass. The original-mode control and both bounded focused
integration runs pass. The full local suite and CI were not rerun for this increment.
