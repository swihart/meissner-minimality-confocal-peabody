#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-$(pwd)}"
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$REPO/release_audit/python/finalize_release_audit.py" \
  --repo-root "$REPO" \
  --output-json "$REPO/release_audit/results/release_audit_summary.json" \
  --output-report "$REPO/release_audit/RELEASE_AUDIT_REPORT.md" \
  | tee "$REPO/release_audit/results/release_audit_summary.txt"
