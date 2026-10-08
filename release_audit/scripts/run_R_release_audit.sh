#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-$(pwd)}"
RESULTS="$REPO/release_audit/results/R"
JSON_OUT="$RESULTS/peabody_release_semantic_audit.json"
TEXT_OUT="$RESULTS/peabody_release_semantic_audit.txt"
mkdir -p "$RESULTS"

if ! command -v Rscript >/dev/null 2>&1; then
  printf '%s\n' 'Rscript was not found. Install R, then run:'
  printf '%s\n' '  brew install gmp mpfr'
  printf '%s\n' '  Rscript -e '\''install.packages(c("jsonlite","Rmpfr","gmp"), repos="https://cloud.r-project.org")'\'''
  false
fi

# Prevent a failed rerun from leaving an older passing JSON in place.
rm -f "$JSON_OUT" "$TEXT_OUT"

Rscript "$REPO/release_audit/R/peabody_release_semantic_audit.R" \
  "$REPO" \
  "$JSON_OUT" \
  2>&1 | tee "$TEXT_OUT"

python3 - "$JSON_OUT" <<'PY'
from __future__ import annotations
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
if not path.is_file():
    raise SystemExit(f"R audit JSON was not created: {path}")
data = json.loads(path.read_text(encoding="utf-8"))
if data.get("classification") != "PEABODY_R_SEMANTIC_AUDIT_PASS" or not data.get("pass"):
    raise SystemExit("R semantic audit did not return its PASS classification")
print("PEABODY_RELEASE_AUDIT_R_JSON_GATE_PASS")
PY

printf '%s\n' 'PEABODY_RELEASE_AUDIT_R_STAGE_PASS'
