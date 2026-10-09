#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

REPO="${1:-$PWD}"
CHECKPOINT="$REPO/review/dcg-five-points"
RESULTS="$CHECKPOINT/results/enclosure-reconciliation"
TRANSCRIPTS="$RESULTS/transcripts"
CERTIFIER="$CHECKPOINT/arb/peabody_arb_concavity.py"
BASELINE="$CHECKPOINT/python/compare_baseline_interval_enclosures.py"
REFINEMENT="$CHECKPOINT/python/run_arb_refinement_audit.py"
PROMOTE="$CHECKPOINT/python/promote_enclosure_reconciliation.py"
MANUSCRIPT="$CHECKPOINT/manuscript/main_dcg_revision_enclosure_reconciled.tex"

fail() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

[ -d "$REPO/.git" ] || fail "not a Git repository: $REPO"
[ -f "$CERTIFIER" ] || fail "missing Arb certifier: $CERTIFIER"
[ -f "$BASELINE" ] || fail "missing baseline comparison script"
[ -f "$REFINEMENT" ] || fail "missing Arb refinement script"
[ -f "$PROMOTE" ] || fail "missing promotion script"
[ -f "$MANUSCRIPT" ] || fail "missing reconciled manuscript source"

find_first() {
  local candidate
  for candidate in "$@"; do
    [ -n "$candidate" ] || continue
    if [ -f "$candidate" ]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done
  return 1
}

MPFR_CSV="$(find_first \
  "$CHECKPOINT/preflight/assistant_mpfr_runtime_only/forward_384/concavity_slab_summary.csv" \
  "$CHECKPOINT/results/mpfr/forward_384/concavity_slab_summary.csv" \
  || true)"
MPFR_JSON="$(find_first \
  "$CHECKPOINT/preflight/assistant_mpfr_runtime_only/forward_384/peabody_mpfr_concavity_certificate.json" \
  "$CHECKPOINT/results/mpfr/forward_384/peabody_mpfr_concavity_certificate.json" \
  || true)"
MPMATH_JSON="$(find_first \
  "$REPO/research/confocal_peabody_analytic_compression/data/certificate_80dps/peabody_concavity_certificate.json" \
  "$CHECKPOINT/frozen_inputs/confocal_peabody_analytic_compression_2026-10-01/data/certificate_80dps/peabody_concavity_certificate.json" \
  || true)"

[ -n "$MPFR_CSV" ] || fail "could not locate direct-MPFR slab summary"
[ -n "$MPFR_JSON" ] || fail "could not locate direct-MPFR certificate JSON"
[ -n "$MPMATH_JSON" ] || fail "could not locate legacy mpmath certificate JSON"

choose_arb_python() {
  local summary venv candidate
  summary="$CHECKPOINT/results/arb/local_replay_summary.json"
  if [ -n "${PEABODY_ARB_PYTHON:-}" ] && [ -x "$PEABODY_ARB_PYTHON" ]; then
    printf '%s\n' "$PEABODY_ARB_PYTHON"
    return 0
  fi
  if [ -f "$summary" ]; then
    venv="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("venv", ""))' "$summary")"
    if [ -n "$venv" ] && [ -x "$venv/bin/python" ]; then
      printf '%s\n' "$venv/bin/python"
      return 0
    fi
  fi
  for candidate in "$HOME"/.cache/peabody-arb/python-flint-0.9.0-py*/bin/python; do
    [ -x "$candidate" ] || continue
    printf '%s\n' "$candidate"
    return 0
  done
  return 1
}

ARB_PYTHON="$(choose_arb_python)" || fail "could not locate the existing python-flint virtual environment"
"$ARB_PYTHON" - <<'PY'
import importlib.metadata
import flint
version = importlib.metadata.version("python-flint")
if version != "0.9.0":
    raise SystemExit(f"python-flint 0.9.0 required; found {version}")
print("PEABODY_ENCLOSURE_RECONCILIATION_FLINT_ENV_PASS")
print("python-flint:", version)
print("module:", flint.__file__)
PY

rm -rf "$RESULTS"
mkdir -p "$TRANSCRIPTS"

python3 "$BASELINE" \
  --mpmath-json "$MPMATH_JSON" \
  --mpfr-csv "$MPFR_CSV" \
  --mpfr-json "$MPFR_JSON" \
  --output-dir "$RESULTS" \
  2>&1 | tee "$TRANSCRIPTS/baseline_interval_comparison.txt"

"$ARB_PYTHON" "$REFINEMENT" \
  --certifier "$CERTIFIER" \
  --mpfr-csv "$MPFR_CSV" \
  --mpfr-json "$MPFR_JSON" \
  --mpmath-json "$MPMATH_JSON" \
  --output-dir "$RESULTS" \
  2>&1 | tee "$TRANSCRIPTS/arb_refinement_audit.txt"

python3 "$PROMOTE" --checkpoint-dir "$CHECKPOINT" \
  2>&1 | tee "$TRANSCRIPTS/enclosure_reconciliation_promotion.txt"

cp "$RESULTS/generated_enclosure_reconciliation.tex" \
  "$CHECKPOINT/manuscript/generated_enclosure_reconciliation.tex"

BUILD_DIR="$(mktemp -d)"
trap 'rm -rf "$BUILD_DIR"' EXIT
(
  cd "$CHECKPOINT/manuscript"
  latexmk -pdf -interaction=nonstopmode -halt-on-error \
    -outdir="$BUILD_DIR" \
    main_dcg_revision_enclosure_reconciled.tex \
    2>&1 | tee "$TRANSCRIPTS/manuscript_build.txt"
)
cp "$BUILD_DIR/main_dcg_revision_enclosure_reconciled.pdf" \
  "$CHECKPOINT/manuscript/main_dcg_revision_enclosure_reconciled.pdf"

# LaTeX may emit warning lines with trailing spaces.  Normalize archived text
# transcripts so Git's whitespace gate remains useful and quiet.
python3 - "$TRANSCRIPTS" <<'PY'
from pathlib import Path
import sys
root = Path(sys.argv[1])
for path in root.rglob("*.txt"):
    lines = [line.rstrip() for line in path.read_text(encoding="utf-8", errors="replace").splitlines()]
    while lines and not lines[-1]:
        lines.pop()
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("PEABODY_ENCLOSURE_RECONCILIATION_TRANSCRIPT_NORMALIZATION_PASS")
PY

python3 - "$RESULTS" <<'PY'
from pathlib import Path
import sys
root = Path(sys.argv[1])
bad = [str(p) for p in root.rglob("*.csv") if b"\r" in p.read_bytes()]
if bad:
    raise SystemExit(f"CSV files contain carriage returns: {bad}")
print("PEABODY_ENCLOSURE_RECONCILIATION_CSV_LF_ONLY_PASS")
PY

rm -rf "$CHECKPOINT/arb/__pycache__" "$CHECKPOINT/python/__pycache__"

GIT_PAGER=cat git -C "$REPO" diff --check

printf '%s\n' 'PEABODY_ENCLOSURE_RECONCILIATION_RUN_PASS'
printf 'Results: %s\n' "$RESULTS"
printf 'Manuscript: %s\n' "$CHECKPOINT/manuscript/main_dcg_revision_enclosure_reconciled.pdf"
