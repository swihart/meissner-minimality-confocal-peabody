#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-$(pwd)}"
RESULTS="$REPO/release_audit/results/python"
mkdir -p "$RESULTS"

"$REPO/release_audit/scripts/verify_frozen_baseline.sh" "$REPO"

PYTHONDONTWRITEBYTECODE=1 python3 \
  "$REPO/release_audit/python/independent_one_pair_rederivation.py" \
  --repo-root "$REPO" \
  --output-dir "$RESULTS" \
  --precision-dps 70 \
  --order-1d 96 \
  --order-2d 48 \
  | tee "$RESULTS/independent_one_pair_rederivation.txt"

PYTHONDONTWRITEBYTECODE=1 python3 \
  "$REPO/release_audit/python/independent_certificate_checker.py" \
  --repo-root "$REPO" \
  --output "$RESULTS/independent_certificate_check.json" \
  --precision-dps 80 \
  | tee "$RESULTS/independent_certificate_check.txt"

printf '%s\n' 'PEABODY_RELEASE_AUDIT_PYTHON_STAGE_PASS'
