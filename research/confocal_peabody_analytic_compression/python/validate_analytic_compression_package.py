#!/usr/bin/env python3
"""Validate the assembled Peabody analytical-compression package."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-dir", type=Path, required=True)
    args = parser.parse_args()
    root = args.package_dir.resolve()

    canonical = json.loads((root / "data/certificate_80dps/peabody_concavity_certificate.json").read_text())
    high = json.loads((root / "data/certificate_100dps/peabody_concavity_certificate.json").read_text())
    reverse = json.loads((root / "data/certificate_reverse_80dps/peabody_concavity_certificate.json").read_text())
    under = json.loads((root / "data/control_underresolved_16/peabody_concavity_certificate.json").read_text())
    mutation = json.loads((root / "data/control_correction_sign/peabody_concavity_certificate.json").read_text())
    audit = json.loads((root / "data/analytic_compression_adversarial_audit.json").read_text())

    tex = (root / "manuscript/main_analytic_compression.tex").read_text(encoding="utf-8")
    pdf = root / "manuscript/main_analytic_compression.pdf"
    note = root / "notes/peabody_analytic_compression_note.md"

    checks = {
        "canonical_certificate_pass": canonical.get("proof_status") == "CERTIFIED",
        "canonical_classification_pass": canonical.get("classification") == "GO_PEABODY_ANALYTIC_COMPRESSION_CONCAVITY_CERTIFIED",
        "endpoint_bound_pass": canonical["endpoint"].get("exceeds_target") is True,
        "concavity_bound_pass": canonical["concavity"].get("all_slabs_below_target") is True,
        "terminal_box_count_pass": canonical.get("terminal_boxes") == 324,
        "hard_stop_pass": canonical.get("hard_stop_pass") is True,
        "high_precision_replay_pass": high.get("proof_status") == "CERTIFIED",
        "reverse_order_replay_pass": reverse.get("proof_status") == "CERTIFIED",
        "underresolved_control_rejected": under.get("proof_status") == "NOT_CERTIFIED",
        "sign_mutation_rejected": mutation.get("proof_status") == "NOT_CERTIFIED",
        "independent_audit_pass": audit.get("pass") is True,
        "frozen_dependency_replay_pass": "PEABODY_FAMILY_PACKAGE_VALIDATION_PASS" in (root / "transcripts/frozen_package_validation.txt").read_text(),
        "three_lemma_manuscript_pass": all(token in tex for token in [
            "\\begin{lemma}[Parabolic endpoint]",
            "\\begin{lemma}[Strict concavity]",
            "\\begin{lemma}[Chord bound]",
        ]),
        "old_proposition_removed": "\\begin{proposition}[Scalar certificate]" not in tex,
        "revised_pdf_present": pdf.is_file() and pdf.stat().st_size > 100_000,
        "proof_note_present": note.is_file() and note.stat().st_size > 5_000,
        "python_sources_present": all((root / path).is_file() for path in [
            "python/peabody_concavity_certificate.py",
            "python/audit_peabody_concavity_certificate.py",
        ]),
        "cross_language_audits_present": all((root / path).is_file() for path in [
            "R/peabody_analytic_compression_semantic_audit.R",
            "wolfram/peabody_concavity_semantic_audit.wl",
        ]),
    }

    # Optional outer manifest/checksum gate, available after package assembly.
    checksum_path = root / "SHA256SUMS.txt"
    if checksum_path.exists():
        failures = []
        for line in checksum_path.read_text().splitlines():
            if not line.strip():
                continue
            digest, rel = re.split(r"\s+", line.strip(), maxsplit=1)
            path = root / rel
            if not path.is_file() or sha256(path) != digest:
                failures.append(rel)
        checks["sha256_ledger_pass"] = not failures
    else:
        checks["sha256_ledger_pass"] = True
        failures = []

    passed = all(checks.values())
    result = {
        "validation_version": "PEABODY_ANALYTIC_COMPRESSION_PACKAGE_VALIDATOR_V1",
        "classification": "PEABODY_ANALYTIC_COMPRESSION_PACKAGE_PASS" if passed else "PEABODY_ANALYTIC_COMPRESSION_PACKAGE_FAIL",
        "pass": passed,
        "checks": checks,
        "sha256_failures": failures,
        "canonical_certificate_sha256": sha256(root / "data/certificate_80dps/peabody_concavity_certificate.json"),
        "revised_pdf_sha256": sha256(pdf),
    }
    output = root / "data/package_validation.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
