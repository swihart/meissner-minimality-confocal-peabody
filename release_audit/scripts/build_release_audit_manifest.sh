#!/usr/bin/env bash
set -euo pipefail
REPO="${1:-$(pwd)}"
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$REPO/release_audit/python/build_release_audit_manifest.py" \
  --audit-root "$REPO/release_audit" \
  --output "$REPO/release_audit/RELEASE_AUDIT_MANIFEST.json" \
  > "$REPO/release_audit/results/release_audit_manifest_transcript.txt"
shasum -a 256 "$REPO/release_audit/RELEASE_AUDIT_MANIFEST.json"
