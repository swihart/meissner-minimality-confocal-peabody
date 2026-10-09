#!/usr/bin/env python3
"""Static validation for the no-Homebrew Arb reviewer-response overlay."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
from pathlib import Path

VERSION = "PEABODY_ARB_GATE_SCAFFOLD_VALIDATOR_V2"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint-dir", type=Path, required=True)
    args = parser.parse_args()
    root = args.checkpoint_dir.resolve()

    expected = [
        root / "arb" / "peabody_arb_concavity.py",
        root / "arb" / "requirements-arb.txt",
        root / "python" / "audit_arb_certificate.py",
        root / "python" / "promote_arb_replay.py",
        root / "python" / "validate_arb_gate_scaffold.py",
        root / "scripts" / "run_arb_no_brew_replay.sh",
        root / "notes" / "02_arb_flint_trust_boundary.md",
        root / "notes" / "02a_arb_initial_target_calibration.md",
        root / "ARB_NO_BREW_REPLAY.md",
        root / "REVIEW_PROGRESS_LEDGER.md",
        root / "data" / "reviewer_point_progress.json",
    ]
    checks: dict[str, bool] = {}
    checks["all_expected_files_present"] = all(path.is_file() for path in expected)

    py_files = [path for path in expected if path.suffix == ".py"]
    syntax_ok = True
    for path in py_files:
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError:
            syntax_ok = False
    checks["python_ast_parse"] = syntax_ok

    runner = root / "scripts" / "run_arb_no_brew_replay.sh"
    checks["shell_syntax"] = subprocess.run(
        ["bash", "-n", str(runner)], check=False,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).returncode == 0

    certifier = (root / "arb" / "peabody_arb_concavity.py").read_text(encoding="utf-8")
    checks["python_flint_pin_present"] = 'PYTHON_FLINT_PIN = "0.9.0"' in certifier
    checks["publication_targets_present"] = (
        "ENDPOINT_TARGET = Fraction(1, 4000)" in certifier
        and "CONCAVITY_TARGET = Fraction(1, 100000)" in certifier
    )
    checks["independent_no_principal_import"] = not any(
        token in certifier
        for token in (
            "peabody_concavity_certificate import",
            "peabody_central_interval_certificate import",
            "mpmath.iv",
        )
    )
    runner_text = runner.read_text(encoding="utf-8")
    checks["no_homebrew_in_runner"] = "brew install" not in runner_text.lower() and "command -v brew" not in runner_text.lower()
    checks["binary_wheel_policy"] = "--only-binary=:all:" in runner_text
    checks["isolated_venv"] = ".cache/peabody-arb" in runner_text
    checks["three_replays_and_two_controls"] = all(
        marker in runner_text
        for marker in (
            "forward_384", "forward_512", "reverse_384",
            "control_1x1", "control_sign_mutation",
        )
    )

    progress = json.loads((root / "data" / "reviewer_point_progress.json").read_text())
    checks["progress_ledger_ready"] = (
        progress.get("branch") == "review/dcg-major-revision"
        and progress["points"]["2"]["status"] == "ARB_FLINT_NO_BREW_REPLAY_READY"
        and progress["points"]["2"]["closed"] is False
    )

    passed = all(checks.values())
    report = {
        "validator_version": VERSION,
        "classification": (
            "PEABODY_ARB_GATE_SCAFFOLD_PASS"
            if passed else "PEABODY_ARB_GATE_SCAFFOLD_FAIL"
        ),
        "pass": passed,
        "checks": checks,
        "actual_arb_runtime_executed_in_builder_environment": False,
        "reason": "python-flint was unavailable in the builder environment; local wheel replay remains mandatory",
        "file_hashes": {str(path.relative_to(root)): sha256(path) for path in expected if path.is_file()},
    }
    out = root / "data" / "arb_gate_static_validation.json"
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(report["classification"])
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
