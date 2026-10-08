#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-$(pwd)}"
RESULTS="$REPO/release_audit/results/mathematica"
WORK="$RESULTS/fresh_kernel_workspace"
OUTPUTS="$RESULTS/outputs"
V4_ARCHIVE="$REPO/frozen_inputs/confocal_peabody_v4_validated_checkpoint_2026-09-30.zip"
WOLFRAMSCRIPT_BIN="${WOLFRAMSCRIPT_BIN:-$(command -v wolframscript || true)}"

if [[ -z "$WOLFRAMSCRIPT_BIN" ]]; then
  printf '%s\n' 'wolframscript was not found.'
  printf '%s\n' 'Set WOLFRAMSCRIPT_BIN to the full Mathematica wolframscript executable.'
  false
fi

rm -rf "$WORK"
mkdir -p "$WORK"
TMP="$(mktemp -d)"
unzip -q "$V4_ARCHIVE" -d "$TMP"
V4_ROOT="$(find "$TMP" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
cp "$V4_ROOT"/wolfram/*.wl "$WORK"/

run_one() {
  local script="$1"
  local transcript="$2"
  "$WOLFRAMSCRIPT_BIN" -file "$WORK/$script" | tee "$RESULTS/$transcript"
}

run_one 00_run_peabody_component_diagnostic_v4.wl 00_component_diagnostic_fresh_kernel.txt
run_one 01_run_peabody_compressed_audit_v4.wl 01_compressed_audit_fresh_kernel.txt
run_one 02_run_peabody_primitive_probe_v4_1.wl 02_primitive_probe_fresh_kernel.txt
run_one 03_prepare_peabody_interval_inputs_v4.wl 03_interval_inputs_fresh_kernel.txt

rm -rf "$OUTPUTS"
mkdir -p "$OUTPUTS"
for d in \
  mathematica_output_component_diagnostic_v4 \
  mathematica_output_compressed_audit_v4 \
  mathematica_output_primitive_probe_v4 \
  mathematica_output_interval_inputs_v4; do
  cp -R "$WORK/$d" "$OUTPUTS/$d"
done

export PEABODY_WOLFRAM_OUTPUT_ROOT="$OUTPUTS"
export PEABODY_WOLFRAM_GUARD_JSON="$RESULTS/wolfram_recursive_guard_summary_mathematica.json"
"$WOLFRAMSCRIPT_BIN" -file "$REPO/release_audit/wolfram/check_proof_critical_outputs.wl" \
  | tee "$RESULTS/wolfram_recursive_guard_mathematica.txt"

PYTHONDONTWRITEBYTECODE=1 python3 \
  "$REPO/release_audit/python/scan_wolfram_outputs.py" \
  --output-root "$OUTPUTS" \
  --output "$RESULTS/wolfram_recursive_guard_summary.json" \
  | tee "$RESULTS/wolfram_recursive_guard_python.txt"

mkdir -p "$V4_ROOT/mathematica_outputs" "$V4_ROOT/data"
for d in \
  mathematica_output_component_diagnostic_v4 \
  mathematica_output_compressed_audit_v4 \
  mathematica_output_primitive_probe_v4 \
  mathematica_output_interval_inputs_v4; do
  rm -rf "$V4_ROOT/mathematica_outputs/$d"
  cp -R "$OUTPUTS/$d" "$V4_ROOT/mathematica_outputs/$d"
done
PYTHONDONTWRITEBYTECODE=1 python3 "$V4_ROOT/python/validate_mathematica_outputs_v4.py" \
  | tee "$RESULTS/validate_mathematica_outputs_v4_fresh.txt"
cp "$V4_ROOT/data/validated_output_summary.json" "$RESULTS/validated_output_summary_fresh.json"

rm -rf "$TMP" "$WORK"
printf '%s\n' 'PEABODY_RELEASE_AUDIT_MATHEMATICA_STAGE_PASS'
