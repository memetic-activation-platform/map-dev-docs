# Issue 816 evidence — October 2026

This directory supports [Issue 816 findings](../../issue-816-findings.md).
It preserves measured results from October 12–14, 2026. Results are observations
from specific workloads, not runtime specifications or portable latency guarantees.

## Inventory

| File | Contents |
| --- | --- |
| [commit-measurements.json](commit-measurements.json) | Individual Commit samples, retained phase/cost/count metrics, condition summaries, and capture metadata for 12 variants |
| [construction-comparison.json](construction-comparison.json) | Fresh standard, bounded ValidatorPackage, and combined comparison; exact outcome signatures |
| [query-plans.json](query-plans.json) | Authored/DHT SQL, execution plans, row counts, index creation times, and before/after SQL timing samples |
| [retrieval-results.json](retrieval-results.json) | Synthetic retrieval metadata, workload summaries, variability, and source checksums |
| [retrieval-comparison.csv](retrieval-comparison.csv) | All 90 workload cells comparing Single Prefix Retrieval, Batched Prefix Retrieval, and Single Scan |
| [retrieval-run-01.json](retrieval-run-01.json), [run 02](retrieval-run-02.json), [run 03](retrieval-run-03.json) | Individual synthetic guest/conductor timing samples and correctness counts |
| [inverse-cache-audit.json](inverse-cache-audit.json) | Per-workload/stage totals, cache outcomes, missed source identities, and repeated-miss checks for one and ten subjects plus bootstrap |
| [warm-reuse-model.json](warm-reuse-model.json) | Warm probe samples and the explicitly hypothetical cached-Commit calculation |
| [validation-outcomes.json](validation-outcomes.json) | Six live outcome controls for standard and four experimental captures |
| [selected-markers.txt](selected-markers.txt) | Original timing/count markers selected from seven capture logs |
| [earlier-prefetch-experiment.json](earlier-prefetch-experiment.json) | Historical prefetch-removal screening summary; original sample files were unavailable |
| [provenance.json](provenance.json) | SHA-256 checksums of archived evidence files and retention limits |

Archived strategy labels `separate_prefixes`, `batched_prefixes`, and `consolidated`
mean Single Prefix Retrieval, Batched Prefix Retrieval, and Single Scan respectively.

Durations ending `_us` are microseconds; `_ms` are milliseconds. Other numeric
metrics include counts and profile labels. A batched backend call may contain
several logical link queries. Parent and child timers overlap. Component medians
need not sum to the median total. Backend/node counts apply to their named phase
or diagnostic span, not every read throughout the whole command.

## Conditions

- macOS 26.5.2, arm64; Rust/Cargo 1.94.0 in Nix; Holochain 0.6.3.
- Optimized release coordinator WASM; profiling enabled. Per-capture metadata
  records actual environment settings, source/schema/artifact hashes, revisions,
  and dirty worktree status. The implementation base was map-holons
  `f2dae85fbafcd6fb0082bf92b3dbd8e6dedd2312`, with uncommitted changes.
- Single-instance workload: one new VisualizerUsage, Key, and four outbound
  relationships. Ten-subject workload commits ten such subjects together.
- Bootstrap is excluded from timed instance commands. Commit intervals also
  exclude staging and endpoint lookup. Persisted forward/inverse checks occur
  afterward and may warm host/conductor caches for the next sample.
- Most Commit captures use one conductor with three commands: one first-use,
  two repeated. Exclusive-accounting/strategy trials use two commands; the
  ten-subject capture uses two commands. Repeated samples share a conductor,
  but each has a new transaction and guest invocation; inverse buckets grow.
- Synthetic retrieval uses three processes, 90 workload cells, three forced
  strategies, and six timed rounds per cell/strategy after warm-up. It excludes
  holon hydration, ordinary membership caching, and adaptive count-probe cost.
- The warm probe evaluates the same subject three extra times in one invocation.
  It does not implement cross-Commit retention. Actual command durations include
  those extra passes. The 811 ms result is a model with omitted applicability,
  rebinding, and cold-subject costs.

## Provenance and retention limits

Numeric samples and summaries were recovered from temporary capture directories.
Absolute workstation paths in metadata and excerpts were normalized; numeric
measurements are unchanged. `capture` names and source filenames identify originals,
not downloadable artifacts. The Commit archive selects useful metrics rather than
copying every profiling field; all original files are identified by checksums.
Synthetic individual sample files are retained in full.

Full raw logs, dirty source patches, and packaged binaries are **not archived here**.
Their checksums survive in provenance/metadata, but their temporary locations are
not durable evidence links or a complete reproducible source snapshot. Selected
markers and numeric records remain readable without those originals.

The prefetch-removal result is explicitly a historical narrative summary: its
original control/trial directories were absent when this evidence was published.
Do not treat it as recovered individual samples. The initial 20.6-second construction
observation also lacks an archived original capture; later controls locate the
same dominant phase but report different elapsed times.

The first inverse-cache capture prints abbreviated source identities. Its in-memory
probe grouped full IDs; the ten-subject follow-up emits full canonical identity
bytes, and its archived missed-source records are unambiguous. Node-cache observations
cover `get_rc_holon`; direct already-cached node access elsewhere is not counted
as a node hit. Staged graph access bypasses the saved membership cache.

Some runs passed their live test but initially failed summary parsing because of
an operation-marker or `count`/`invocations` mismatch. The intact logs were reparsed
with the corrected parser; timings were not regenerated or substituted. The bulk
audit's earlier directory-collision launch stopped before testing and is excluded.

Reproduction entry points remain in map-holons: `scripts/measure-commit-performance.py`
(with `--assessment`, `--subjects`, and `--index-mode`),
`scripts/measure-relationship-retrieval.py`, and
`tests/sweetests/tests/commit_performance_tests.rs`. Assessment labels verify
separately built artifacts; they do not enable Cargo features. Consult that repository's
operational notes for build and pack commands. New runs need fresh metadata and artifacts.
