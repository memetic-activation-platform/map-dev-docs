# Reproducing the matched diagnostics

Run from a clone of `memetic-activation-platform/map-holons`. The test and adapter snapshots are identical for both versions; the two support patches preserve each version's required dependency and conductor API adaptations. The patches also enable profiling, expose the runtime helper and align test networking/storage-authority settings. No production caching or retrieval policy changes are included.

## Prepare two worktrees

Set `EVIDENCE` to the absolute path of this evidence directory before changing directories. Use fresh worktree paths, or adapt these commands to existing disposable checkouts.

```sh
export EVIDENCE=/absolute/path/to/2026-10-holochain-matched-comparison
export HC06=/absolute/path/to/map-hc06
export HC07=/absolute/path/to/map-hc07

git worktree add --detach "$HC06" 87cb8349cf2989a2f00f394f65976fd64216644b
git worktree add --detach "$HC07" 9bf273a7

git -C "$HC06" apply "$EVIDENCE/diagnostic-support-hc06.patch"
git -C "$HC07" apply "$EVIDENCE/diagnostic-support-hc07.patch"

for checkout in "$HC06" "$HC07"; do
  cp "$EVIDENCE/authenticated-diagnostic.rs" "$checkout/tests/sweetests/tests/holon_fetch_profile_tests.rs"
  cp "$EVIDENCE/link-diagnostic.rs" "$checkout/tests/sweetests/tests/link_strategy_performance_tests.rs"
  cp "$EVIDENCE/dance-adapter.rs" "$checkout/happ/crates/holons_guest/src/dances_guest/dance_adapter.rs"
  cat "$EVIDENCE/link-probes.rs" >> "$checkout/happ/zomes/coordinator/holons_test_probes/src/lib.rs"
done
```

## Build and audit

Use the **0.7 checkout's Nix development shell for both builds** to match Rust 1.95.0 and native libraries. Use each checkout's existing version-specific lockfiles; do not run `cargo update`. Captured artifact/source/lockfile hashes are recorded in the JSON metadata. Native dev `opt-level="z"` and guest release `opt-level="z"`/LTO/one codegen unit are already configured at these commits. The full application host workspace is not used by these diagnostics.

For each checkout, run these commands inside `nix develop "$HC07"`; use separate target directories and wait for all builds to finish before measuring:

```sh
export CHECKOUT="$HC06"  # repeat with HC07

CARGO_TARGET_DIR="$CHECKOUT/target" cargo test --manifest-path "$CHECKOUT/tests/sweetests/Cargo.toml" --test holon_fetch_profile_tests --test link_strategy_performance_tests --no-run --offline

CARGO_TARGET_DIR="$CHECKOUT/happ/target" cargo build --manifest-path "$CHECKOUT/happ/Cargo.toml" -p holons_integrity -p holons --release --target wasm32-unknown-unknown --features holons/holon-fetch-profiling --offline

CARGO_TARGET_DIR="$CHECKOUT/happ/target" cargo build --manifest-path "$CHECKOUT/happ/Cargo.toml" -p holons_test_probes --release --target wasm32-unknown-unknown --offline
```

If the dependency cache is not populated, fetch the dependencies before running the offline builds. Pack each checkout with its matching Holochain CLI (`nix develop "$CHECKOUT" --command hc app pack "$CHECKOUT/happ/workdir" --recursive`). Run the repository's hApp artifact audit against the resulting production DNA/hApp and loose test probe, using `--deny-production-test-only`. Both captured versions passed; the probe must not be added to production manifests. The probe-enabled helper appends it only to the disposable conductor, restarts that conductor, and claims full storage authority again.

## Run sequentially

Run each version separately, using the same 0.7 Nix shell. Run from that checkout's `tests/sweetests` directory because the fixture uses relative artifact paths. Set `OUTPUT` to an existing absolute evidence-output directory. Each test bootstraps a fresh disposable database, executes its measurements, and explicitly shuts down its conductor. The native `timeout 360` wrapper used for the captures limits each test run to six minutes; an equivalent process timeout can be used where GNU timeout is unavailable.

```sh
cd "$CHECKOUT/tests/sweetests"

RUST_LOG=warn WASM_LOG=info cargo test --manifest-path Cargo.toml --test holon_fetch_profile_tests --offline -- --ignored --nocapture > "$OUTPUT/authenticated-read.log" 2>&1

RUST_LOG=warn WASM_LOG=warn MAP_LINK_STRATEGY_OUTPUT="$OUTPUT/link-samples.json" cargo test --manifest-path Cargo.toml --test link_strategy_performance_tests --offline -- --ignored --nocapture > "$OUTPUT/link-read.log" 2>&1
```

The captured native executables were run directly after compilation so no build overlapped either measurement. With Cargo commands, ensure artifacts remain fresh and no compilation occurs during measurement. The authenticated log contains paired `[read-call-profile]`, `[read-call-client]` and `[read-call-total]` records keyed by operation and sample. Keep all five authenticated calls per operation; derive the outside-adapter duration per request before calculating its median. The link probe writes all samples and canonical results to JSON. Exclude sample 0 from repeated link/control statistics, retaining it separately.

These sources/patches reproduce the diagnostic setup, not a standalone minimal Holochain reproducer. They require the MAP repository and full Core Schema bootstrap. Absolute paths in captured metadata identify the original machine; adapt paths locally. Compiler/platform changes can alter timings and binary hashes.
