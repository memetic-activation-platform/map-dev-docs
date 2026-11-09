# Test execution improvements: Issue 852 delivery summary

[map-holons PR 858](https://github.com/evomimic/map-holons/pull/858) merged on
2026-11-09 as `b35a474541573bf5e7fd590a653a2186baab5dc9`, following merged
PRs 855 and 854. Issue 852 is closed. This summary records the final test-side
countermeasures; earlier captures in this directory remain historical evidence
for their named code checkpoints, not measurements of the final merged state.

## Countermeasures and coverage

- Replace standalone persisted-graph verification in 14 graph/lineage/retry fixtures
  with opt-in shared Commit verification bounded to fixture-declared worksets.
  Preserve exact saved identities, inverse occurrences, multiplicity and lineage,
  fresh observer reads, and original expectations across Incomplete retries.
- Remove redundant StageNewVersion anchoring/graph checks and the standalone
  ancestry selector. Dedicated matrix scenarios retain graph and lineage coverage.
- Remove the pristine bootstrap/loader suite and incremental-loader fixture.
  The cross-bundle duplicate-loader-key branch loses its dedicated integration
  check; this is an explicit coverage retirement, not replacement coverage.
- Share the runtime matrix's bootstrap with attachment defaults, relationship-cache
  policies, domain reimport rejection, Space/Dancer import, visualizer composition,
  and visualizer-usage resolution. Usage resolution runs before other fixtures:
  missing usage is asserted before creation, fresh-transaction resolution, and
  canonical invocation. Its 12 original assertions remain.
- Remove two disposition-diagnostic integrations. Classifier/reporting units and
  retained real Commit-failure scenarios own the substantive checks; the removed
  real-executor diagnostic panic wiring is not claimed as retained coverage.
- Consolidate canonical-loader scenarios around one Navigator import, read-only
  discovery first. Consolidate effective-descriptor scenarios with independent
  Sessions, preserve Runtime-drop behavior, and mutate Core definitions last.
- Combine cache and theme checks while retaining distinct measured transports and
  fresh host caches. Combine two CI-enabled incomplete-commit scenarios with
  independent transactions and fixture registries and injected-link cleanup.
  Keep the already excluded third scenario separate.
- Select the matrix in required heavy-rest CI. Priority and remaining selections
  are disjoint. Probe conductors remain separate from ordinary runtime suites.

Independent bootstrap executions fall from **23 to 10 in default local testing**
across PR 858. Relative to its initial checkpoint, the final batch reduces local
loads **17 to 10**, and loads across active CI checks **14 to 7**.

## Observed full-run and CI durations

| Measurement | Initial PR 858 checkpoint | After additional consolidations | Approximate reduction |
| --- | ---: | ---: | ---: |
| Local npm test | 51m 13s | 40m | 22% |
| CI heavy (commit) | 70m | 46m | 34% |
| CI heavy (rest) | 65m | 54m | 17% |
| CI heavy (storage) | 18m | 17m | 6% |

The longest heavy job falls from 70m to 54m (about 23%); heavy-rest becomes the
long pole. The three heavy jobs sum to approximately 153 versus 117 runner-minutes
(about 24% less), excluding light, formatting and aggregation. This is not a
measurement of total workflow elapsed time.

These are successive observed runs, not controlled benchmarks. The local 40-minute
result is maintainer-reported; CI durations are rounded from the recorded checks.
Build/cache conditions and runner variation prevent attributing every minute to
consolidation. The matrix's addition to required CI also changes the workload.
The timing comparison predates integration of PR 857; no new duration is claimed
for the final combined-state run. See the [PR performance note](https://github.com/evomimic/map-holons/pull/858#issuecomment-6742629390).

## Final verification

The tested PR head is `c6728967b33d29763c069ef27bf0724002e41d56`, integrating
main containing PR 857. [CI run 665](https://github.com/evomimic/map-holons/actions/runs/42621039728)
passed all six active checks; the separate dance job remains intentionally skipped,
with the runtime matrix covered by required heavy-rest. The maintainer reported
successful hApp and host builds, nominal npm start, and passing full npm test
on the combined state before merge.

During implementation, 59 harness library tests, 8 fixture-authoring tests, the
four consolidated integration targets, and the complete runtime matrix passed.
The final usage-first matrix regression passed in 551.07s; that focused result is
correctness evidence, not a comparable full-suite benchmark.

## Historical profiling stages

| Capture | What it establishes |
| --- | --- |
| [Initial versus PR 855 checkpoint](dance-timings-final-pr-comparison.md) | Cumulative earlier 41-fixture evidence; predates PR 858 |
| [Post-854/855](dance-timings-post-854-855.txt) | Integrated baseline and fixture/step costs, with JSON and context alongside |
| [Drop anchoring](dance-timings-drop-anchoring.txt) | Removing the bespoke check moved cost to the retained verifier; no substantial speedup established |
| [Stage without graph](dance-timings-stage-without-graph.txt) | Focused ancestry run under different setup conditions; not a matrix comparison |
| [Bounded Commit](dance-timings-bounded-commit.txt) | Case-scoped verification capture, excluding bootstrap and work outside fixture boundaries |

The retired pristine, loader and ancestry names in historical artifacts are not
current default selectors. Saved patches and absolute local log paths describe
capture provenance; they are not instructions to apply those patches.

## Remaining limits

Legacy rejection snapshots, Book/Person presentation verification, and cache-test
ID selection still include broad reads. Three default-local tests remain excluded
from active CI: `query_runtime`,
`incomplete_commit_repeats_error_then_completes_relationship_retry`, and
`rekeyed_core_successor_commits_after_independent_rejection`. This work does not
claim those exclusions have been repaired. Guest-to-host descriptor registry return,
production read-path work, and declarative required-binding-retention enforcement
remain separate concerns.
