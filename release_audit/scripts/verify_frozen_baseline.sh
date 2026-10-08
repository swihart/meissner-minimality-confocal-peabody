#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-$(pwd)}"
OUT="$REPO/release_audit/results/python/frozen_baseline_verification.json"
mkdir -p "$(dirname "$OUT")"
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$REPO/release_audit/python/verify_frozen_baseline.py" \
  --repo-root "$REPO" \
  --output "$OUT" \
  | tee "$REPO/release_audit/results/python/frozen_baseline_verification.txt"
