#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-$PWD}"
CHECKPOINT="$REPO/review/dcg-five-points"
CERTIFIER="$CHECKPOINT/arb/peabody_arb_concavity.py"
AUDITOR="$CHECKPOINT/python/audit_arb_certificate.py"
RESULTS="$CHECKPOINT/results/arb"
TRANSCRIPTS="$RESULTS/transcripts"
PIN="python-flint==0.9.0"

fail() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

[ -d "$REPO/.git" ] || fail "not a Git repository: $REPO"
[ -f "$CHECKPOINT/REVIEW_PROGRESS_LEDGER.md" ] || fail "DCG checkpoint ledger is missing"
[ -f "$CERTIFIER" ] || fail "Arb certifier is missing"
[ -f "$AUDITOR" ] || fail "Arb auditor is missing"

choose_python() {
  local candidate
  for candidate in "${PEABODY_ARB_PYTHON:-}" python3.14 python3.13 python3.12 python3.11 python3.10 python3; do
    [ -n "$candidate" ] || continue
    command -v "$candidate" >/dev/null 2>&1 || continue
    if "$candidate" - <<'PY' >/dev/null 2>&1
import sys
raise SystemExit(0 if (3, 10) <= sys.version_info[:2] <= (3, 14) else 1)
PY
    then
      command -v "$candidate"
      return 0
    fi
  done
  return 1
}

BASE_PYTHON="$(choose_python)" || fail "Python 3.10 through 3.14 is required"
PY_TAG="$($BASE_PYTHON -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
VENV="${PEABODY_ARB_VENV:-$HOME/.cache/peabody-arb/python-flint-0.9.0-py$PY_TAG}"

mkdir -p "$(dirname "$VENV")"
if [ ! -x "$VENV/bin/python" ]; then
  "$BASE_PYTHON" -m venv "$VENV"
fi
PY="$VENV/bin/python"

rm -rf "$RESULTS"
mkdir -p "$TRANSCRIPTS"

"$PY" -m ensurepip --upgrade > "$TRANSCRIPTS/ensurepip.txt" 2>&1 || true
if ! "$PY" -m pip install --help 2>/dev/null | grep -q -- '--report'; then
  "$PY" -m pip install --upgrade pip 2>&1 | tee "$TRANSCRIPTS/pip_upgrade.txt"
fi

if [ -n "${PEABODY_ARB_WHEEL:-}" ]; then
  [ -f "$PEABODY_ARB_WHEEL" ] || fail "PEABODY_ARB_WHEEL does not exist: $PEABODY_ARB_WHEEL"
  shasum -a 256 "$PEABODY_ARB_WHEEL" > "$RESULTS/local_wheel_sha256.txt"
  "$PY" -m pip install --force-reinstall --no-deps --report "$RESULTS/pip_install_report.json" "$PEABODY_ARB_WHEEL" 2>&1 | tee "$TRANSCRIPTS/pip_install.txt"
else
  "$PY" -m pip install --only-binary=:all: --no-deps --report "$RESULTS/pip_install_report.json" "$PIN" 2>&1 | tee "$TRANSCRIPTS/pip_install.txt"
fi

"$PY" - <<'PY' | tee "$RESULTS/python_flint_environment.txt"
import importlib.metadata
import json
import platform
import sys
import flint
from flint import arb, ctx

ctx.prec = 192
payload = {
    "python": sys.version,
    "platform": platform.platform(),
    "python_flint_distribution": importlib.metadata.version("python-flint"),
    "flint_module_version": getattr(flint, "__version__", "unknown"),
    "flint_module_file": str(flint.__file__),
    "arb_smoke_sqrt2": str(arb(2).sqrt()),
    "arb_smoke_atan_half": str(arb("1/2").atan()),
}
print(json.dumps(payload, indent=2))
if payload["python_flint_distribution"] != "0.9.0":
    raise SystemExit("python-flint 0.9.0 was not installed")
PY

run_pass() {
  local label="$1"
  shift
  mkdir -p "$RESULTS/$label"
  "$PY" "$CERTIFIER" --output-dir "$RESULTS/$label" "$@" 2>&1 | tee "$TRANSCRIPTS/$label.txt"
}

run_fail() {
  local label="$1"
  shift
  mkdir -p "$RESULTS/$label"
  set +e
  "$PY" "$CERTIFIER" --output-dir "$RESULTS/$label" "$@" 2>&1 | tee "$TRANSCRIPTS/$label.txt"
  local status=${PIPESTATUS[0]}
  set -e
  if [ "$status" -eq 0 ]; then
    fail "adversarial control unexpectedly passed: $label"
  fi
  printf '%s\n' "$status" > "$RESULTS/$label/EXPECTED_FAILURE_EXIT_CODE.txt"
}

run_pass forward_384 --bits 384
run_pass forward_512 --bits 512
run_pass reverse_384 --bits 384 --reverse
run_fail control_1x1 --bits 384 --q-slabs 1 --x-panels 1 --no-boxes
run_fail control_sign_mutation --bits 384 --q-slabs 4 --correction-sign -1 --no-boxes

"$PY" "$AUDITOR" --checkpoint-dir "$CHECKPOINT" 2>&1 | tee "$TRANSCRIPTS/arb_certificate_audit.txt"

RESULTS_DIR="$RESULTS" VENV_PATH="$VENV" BASE_PYTHON_PATH="$BASE_PYTHON" "$PY" - <<'PY'
import hashlib
import json
import os
from pathlib import Path

root = Path(os.environ["RESULTS_DIR"])
audit = json.loads((root / "arb_certificate_audit.json").read_text())
environment = (root / "python_flint_environment.txt").read_text()
payload = {
    "classification": "PEABODY_DCG_ARB_NO_BREW_REPLAY_PASS" if audit.get("pass") else "PEABODY_DCG_ARB_NO_BREW_REPLAY_FAIL",
    "pass": bool(audit.get("pass")),
    "audit_sha256": hashlib.sha256((root / "arb_certificate_audit.json").read_bytes()).hexdigest(),
    "python_flint_environment_sha256": hashlib.sha256(environment.encode()).hexdigest(),
    "venv": os.environ["VENV_PATH"],
    "base_python": os.environ["BASE_PYTHON_PATH"],
    "python_flint_pin": "0.9.0",
    "homebrew_used": False,
    "system_package_manager_used": False,
}
(root / "local_replay_summary.json").write_text(json.dumps(payload, indent=2) + "\n")
print(payload["classification"])
if not payload["pass"]:
    raise SystemExit(2)
PY

printf '%s\n' 'PEABODY_ARB_NO_BREW_REPLAY_PASS'
