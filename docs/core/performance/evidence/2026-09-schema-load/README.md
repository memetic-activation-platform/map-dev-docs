# September 2026 Core Schema evidence

## Inventory

| File | Contents |
|---|---|
| [baseline.json](baseline.json) | Five sequential fresh-process unoptimized runs, native executable and DNA hashes, compiler version |
| [memory-4mib.json](memory-4mib.json) | Six alternating experimental/control runs, matching native executable hash, DNA hash per variant |
| [app-earlier.txt](app-earlier.txt) | Selected first Core Schema call markers and nested metrics from the earlier app run |
| [app-slow.txt](app-slow.txt) | Equivalent excerpts from the slow app run |
| [sampling.md](sampling.md) | CPU sampling windows, category shares, stack observations, and limitations |

JSON durations ending in `_ms` are milliseconds. `total_ms` includes harness
setup; `conductor_ms` is the conductor call. `guest_ms` spans coordinator markers;
`after_guest_ms` ends at caller receipt; `before_guest_ms` is derived by subtraction.
Log filenames identify original source files, not downloadable attachments.
Absolute workstation paths were removed from JSON; numeric results are unchanged.

## Conditions and provenance

- Runs: September 19–20, 2026; timestamps in excerpts and baseline JSON are UTC.
- Platform: developer macOS workstation. Hardware and background load were not
  recorded systematically; do not assume equivalence on another machine.
- Dependencies inspected: Holochain 0.6.3, holochain_wasmer_host 0.0.102.
- Controlled series: native opt-level 0, debug information level 2, debug
  assertions enabled; `RUST_LOG=info`, `WASM_LOG=info`; no sampler attached.
- Test: `bootstrap_performance_tests::measures_generated_core_schema_bootstrap`,
  run as a fresh process from `tests/sweetests` for each measurement.
- Build: `CARGO_PROFILE_DEV_OPT_LEVEL=0 CARGO_PROFILE_TEST_OPT_LEVEL=0 cargo test
  --locked --manifest-path tests/sweetests/Cargo.toml --test
  bootstrap_performance_tests --no-run --message-format=json` in the Nix environment.
- Execute the resulting test binary with `--exact
  measures_generated_core_schema_bootstrap --nocapture` from `tests/sweetests`.
- DNA input: `happ/workdir/map_holons.dna`. Both series check artifact hashes;
  the memory series changes only the integrity WASM minimum from 17 to 64 pages
  and repacks the DNA. Native executable SHA-256 is identical across series.
- App launch: `MAP_PROFILE=1 npm run start:info 2>&1 | tee
  /tmp/map-package-activation-profile.log`.
- The worktree contained uncommitted implementation changes. No clean source
  revision or complete patch snapshot was captured for these runs. Artifact
  hashes identify measured binaries but do not make them rebuildable by themselves.

These are historical measurements, not a portable benchmark fixture. Reproduction
requires the MAP Holochain/Nix environment and current test setup; record a clean
revision or patch plus input hashes in future experiments.

## Retention limits

Compact results and selected log excerpts are retained here. Full logs, scripts,
CPU stack dumps, and binaries were local under `/tmp/map-bootstrap-matched-profile/`,
`/tmp/map-post-return-windows/`, and `/tmp/map-memory-4mib/`; those paths are provenance,
not durable links. Raw traces are not archived here. The earlier optimized
18.8–18.9-second observations lack an archived complete run record and should be
confirmed in a controlled experiment.
