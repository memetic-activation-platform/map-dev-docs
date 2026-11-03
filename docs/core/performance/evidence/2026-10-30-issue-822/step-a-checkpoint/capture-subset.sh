#!/usr/bin/env bash
# Run from map-holons inside nix develop, after committing Step A.
set -euo pipefail
checkpoint_output=${1:?Provide a new checkpoint output directory}
if [[ -e "$checkpoint_output" ]]; then
  echo "Output directory already exists: $checkpoint_output" >&2
  exit 1
fi
if [[ -n $(git status --porcelain) ]]; then
  echo "Commit the Step A implementation before capturing." >&2
  exit 1
fi
step_a_revision=$(git rev-parse HEAD)
export MAP_SWEET_STARTUP_TIMEOUT_SECS=60
npm run build:commit-perf -w map-happ
capture_step_a() {
  local workload=$1
  shift
  python3 scripts/measure-commit-performance.py --runs 1 --samples 6 \
    --preparation-substrate broad-preparation --expected-guest-cache-capacity 10000 \
    --guest-artifact-revision "$step_a_revision" --semantic-revision "$step_a_revision" \
    --output "$checkpoint_output/$workload" "$@"
}
capture_step_a usage --mode create
capture_step_a no-op --mode no-op
capture_step_a mixed --mode mixed
capture_step_a shared-type --mode create --subjects 8
