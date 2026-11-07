#!/usr/bin/env bash
# Run from map-holons inside nix develop, after committing the foundation.
set -euo pipefail
checkpoint_output=${1:?Provide a new checkpoint output directory}
if [[ -e "$checkpoint_output" ]]; then
  echo "Output directory already exists: $checkpoint_output" >&2
  exit 1
fi
if [[ -n $(git status --porcelain) ]]; then
  echo "Commit the foundation implementation before capturing." >&2
  exit 1
fi
foundation_revision=$(git rev-parse HEAD)
export MAP_SWEET_STARTUP_TIMEOUT_SECS=60
npm run build:commit-perf -w map-happ
capture_foundation() {
  local workload=$1
  shift
  python3 scripts/measure-commit-performance.py --runs 1 --samples 6 \
    --instrumentation 822-v3 --preparation-substrate broad-preparation --expected-guest-cache-capacity 10000 \
    --guest-artifact-revision "$foundation_revision" --semantic-revision "$foundation_revision" \
    --output "$checkpoint_output/$workload" "$@"
}
capture_foundation usage --mode create
capture_foundation no-op --mode no-op
capture_foundation mixed --mode mixed
capture_foundation shared-type --mode create --subjects 8
