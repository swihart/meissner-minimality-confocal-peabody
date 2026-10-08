#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-$PWD}"
HERE="$REPO/review/dcg-five-points"
MPFR_DIR="$HERE/mpfr"
RESULTS="$HERE/results/mpfr"
REFERENCE="$REPO/research/confocal_peabody_analytic_compression/data/certificate_80dps/peabody_concavity_certificate.json"

if [ ! -f "$REFERENCE" ]; then
  echo "STOP: archived mpmath reference not found: $REFERENCE" >&2
  exit 2
fi

rm -rf "$RESULTS"
mkdir -p "$RESULTS"

"$MPFR_DIR/build_mpfr_certificate.sh" | tee "$RESULTS/build.txt"
BIN="$MPFR_DIR/peabody_mpfr_concavity"

"$BIN" --output-dir "$RESULTS/forward_384" --precision-bits 384 | tee "$RESULTS/forward_384.txt"
"$BIN" --output-dir "$RESULTS/forward_512" --precision-bits 512 | tee "$RESULTS/forward_512.txt"
"$BIN" --output-dir "$RESULTS/reverse_384" --precision-bits 384 --reverse | tee "$RESULTS/reverse_384.txt"

set +e
"$BIN" --output-dir "$RESULTS/control_16_slabs" --precision-bits 384 --q-slabs 16 > "$RESULTS/control_16_slabs.txt" 2>&1
RC16=$?
"$BIN" --output-dir "$RESULTS/control_sign_mutation" --precision-bits 384 --correction-sign -1 --q-slabs 4 > "$RESULTS/control_sign_mutation.txt" 2>&1
RCM=$?
set -e

if [ "$RC16" -eq 0 ]; then
  echo "STOP: under-resolved 16-slab control unexpectedly passed" >&2
  exit 3
fi
if [ "$RCM" -eq 0 ]; then
  echo "STOP: correction-sign mutation unexpectedly passed" >&2
  exit 4
fi

python3 "$HERE/python/audit_mpfr_certificate.py" \
  --mpfr-forward "$RESULTS/forward_384/peabody_mpfr_concavity_certificate.json" \
  --mpfr-512 "$RESULTS/forward_512/peabody_mpfr_concavity_certificate.json" \
  --mpfr-reverse "$RESULTS/reverse_384/peabody_mpfr_concavity_certificate.json" \
  --underresolved "$RESULTS/control_16_slabs/peabody_mpfr_concavity_certificate.json" \
  --mutation "$RESULTS/control_sign_mutation/peabody_mpfr_concavity_certificate.json" \
  --mpmath "$REFERENCE" \
  --output "$RESULTS/mpfr_certificate_audit.json" \
  | tee "$RESULTS/mpfr_certificate_audit.txt"

python3 "$HERE/python/verify_formula_derivation_identities.py" \
  --output "$RESULTS/formula_derivation_identity_audit.json" \
  | tee "$RESULTS/formula_derivation_identity_audit.txt"

python3 - "$RESULTS" <<'PY'
import json, pathlib, subprocess, sys
r = pathlib.Path(sys.argv[1])
a = json.loads((r / "mpfr_certificate_audit.json").read_text())
f = json.loads((r / "formula_derivation_identity_audit.json").read_text())
assert a["pass"] is True
assert f["pass"] is True
meta = {
    "classification": "PEABODY_DCG_MPFR_OFFICIAL_HEADER_REPLAY_PASS",
    "pass": True,
    "mpfr_certificate_audit": a["classification"],
    "formula_identity_audit": f["classification"],
    "git_head": subprocess.run(["git", "rev-parse", "HEAD"], text=True, capture_output=True).stdout.strip(),
}
(r / "local_replay_summary.json").write_text(json.dumps(meta, indent=2) + "\n")
print(json.dumps(meta, indent=2))
PY

echo "PEABODY_DCG_MPFR_REPLAY_PASS"
