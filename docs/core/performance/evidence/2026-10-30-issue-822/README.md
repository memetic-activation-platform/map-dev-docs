# Issue #822 baseline preparation

Phase 1 revision: `95b9966337d6fe70f4b7685544b72089f7be9b35`.
Semantic baseline: `3d053ba8becbac13496d7531abea8ce9a5303c53`.

**No valid baseline samples have been captured.** Phase 2 workload changes are uncommitted
and have not passed the conductor smoke gate. The workload revision must be recorded after
smoke validation and commit; the Phase 1 revision is not the complete workload revision.

Nix starts with `XDG_CACHE_HOME=/tmp/map-822-nix-cache`. The profiled guest build succeeded
(`profiled-build.log`). The no-op smoke run failed before bootstrap while constructing the
conductor: `Failed to bind iroh endpoint` / `Failed to create netmon monitor` /
`Operation not permitted (os error 1)` (`blocked-no-op-smoke.log`). This sandbox cannot
supply conductor measurements; no performance conclusion follows from this attempt.

Pending gates:

- Smoke every manifest row and bootstrap outside this sandbox; fix any workload/control failures.
- Confirm graph-only overlap reaches binding, identities, and keys; the parser requires evidence.
- Verify controlled requested versus received populations and governor restoration; setup publication
  alone does not establish the population eventually shipped after staging.
- Confirm fresh-ingress cache observations and Session reuse separately.
- Commit the instrumentation/workload support, record its revision and actual guest artifact revision.
- Capture the complete manifest with matched settings and retain raw logs/metadata/parsed samples here.

Commands from map-holons (normal defaults are five runs and six samples):

```sh
XDG_CACHE_HOME=/tmp/map-822-nix-cache nix develop --command python3 scripts/measure-commit-manifest.py --smoke --output /tmp/map-822-smoke
# After successful smoke tests, commit support and rebuild from that revision:
XDG_CACHE_HOME=/tmp/map-822-nix-cache nix develop --command python3 scripts/measure-commit-manifest.py --output ../map-dev-docs/docs/core/performance/evidence/2026-10-30-issue-822/baseline
```

The manifest is `scripts/commit-performance-manifest.json`. It covers ordinary shapes, shared type,
updated and mixed definitions, no-op, graph deltas and overlap, registry miss/hit/bypass conditions,
and bootstrap without a Cartesian product. Unprofiled bootstrap remains the default; the manifest
explicitly selects profiling. Bootstrap uses its loader-specific raw observations rather than treating
multiple loader Commits as one ordinary Commit sample.
