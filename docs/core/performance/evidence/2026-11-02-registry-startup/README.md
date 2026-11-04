# November 2 registry/startup observations

This evidence supplements [Core Schema load](../../schema-load.md#november-2-2026-larger-bootstrap-and-recurring-post-return-delay)
and [startup and Canvas](../../startup-and-canvas.md#november-2-2026-registry-transport-observations).
It records observations, not a controlled before/after result for registry transport.

| File | Contents |
|---|---|
| [selected-markers.txt](selected-markers.txt) | ANSI-free native/guest timestamps, validation phases, Commit/loader/adapter summaries and logging settings |
| [measurements.json](measurements.json) | Core bootstrap interval decomposition, all three Commit summaries and base-package timings |
| [canvas-profiles.json](canvas-profiles.json) | Five completed browser profiles, including prior baseline and both WARN-only November 2 runs |
| [metadata.json](metadata.json) | Revision, dirty-source limitation, launch commands, artifact/log hashes and environment differences |

The INFO capture begins its Core Schema guest interval at 20:03:39 UTC. Its
browser profile was not supplied; the final browser record here is the earlier
19:53:48 UTC WARN-only run. Do not combine their durations as one startup ledger.

The INFO run committed 1,162 Core Schema candidates and 13,068 SmartLink attempts;
base-package activation committed 21 candidates. The later seven-candidate Commit
is background usage persistence, a separate workload. Marker intervals are wall
time; phase and operation counters nest and must not be added twice.

Full raw logs and the idle-app CPU sample remain temporary local files. Selected
markers preserve the reported timing arithmetic without those files, but do not
permit reclassification of CPU samples or a fully reproducible source rebuild.
No same-workload, same-artifact, same-logging checkpoint comparison is claimed.

## Rolled-back checkpoint comparison

[baseline-selected-markers.txt](baseline-selected-markers.txt) and
[baseline-measurements.json](baseline-measurements.json) preserve the subsequent
`3764a9ee` launch with Part 1 removed, using the same profiling feature and logging
flags. The app remained slow. This is one sequential observational comparison,
not a repeated matched A/B. The baseline's Canvas screenshot timer was still
running; it must not be recorded as completed Canvas startup time. Detailed
interpretation and missing Part 1 instrumentation are in the schema-load record.

## Known-fast source audit

[fast-state-audit.json](fast-state-audit.json) records the recovered 14:44 UTC Nix
snapshot, comparison with the later checkpoint, matching configuration/input hashes
and source-edit chronology. It strongly supports equivalent runtime source for the
fast working tree and checkpoint, but does not recover the exact fast executable
or WASM binaries. It also records the extra profiling feature/INFO logging used in
the diagnostic rollback versus normal-build/WARN startup. These configuration
differences must remain explicit in future comparisons.
