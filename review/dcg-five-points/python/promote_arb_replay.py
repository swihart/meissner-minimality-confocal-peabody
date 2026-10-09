#!/usr/bin/env python3
"""Promote Reviewer Point 2 after a successful independent Arb replay."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

PROMOTION_VERSION = "PEABODY_DCG_ARB_FLINT_PROMOTION_V1"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint-dir", type=Path, required=True)
    args = parser.parse_args()

    checkpoint = args.checkpoint_dir.resolve()
    results = checkpoint / "results" / "arb"
    replay_path = results / "local_replay_summary.json"
    audit_path = results / "arb_certificate_audit.json"
    cert_path = results / "forward_384" / "peabody_arb_concavity_certificate.json"
    ledger_path = checkpoint / "REVIEW_PROGRESS_LEDGER.md"
    progress_path = checkpoint / "data" / "reviewer_point_progress.json"

    for path in (replay_path, audit_path, cert_path, ledger_path, progress_path):
        if not path.is_file():
            raise FileNotFoundError(path)

    replay = json.loads(replay_path.read_text(encoding="utf-8"))
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    cert = json.loads(cert_path.read_text(encoding="utf-8"))
    if replay.get("pass") is not True:
        raise RuntimeError("local Arb replay has not passed")
    if audit.get("pass") is not True:
        raise RuntimeError("independent Arb audit has not passed")
    if cert.get("pass") is not True:
        raise RuntimeError("forward Arb certificate has not passed")

    old_fragments = [
        (
            "| 2 | Interval-arithmetic trust boundary | **DIRECT-MPFR PREFLIGHT PASS — 85%** | "
            "Independent C implementation; 384/512-bit and reverse-order passes; under-resolved and sign-mutation controls rejected; high-headroom bounds `Phi(1)>1/4000` and `Phi''<-1/30000` | "
            "Author's local replay compiled with official `mpfr.h`; archive compiler/MPFR transcript and generated results. Optional Arb replay is no longer mandatory if official MPFR replay passes |"
        ),
        (
            "| 2 | Interval-arithmetic trust boundary | **NO-HOMEBREW ARB/FLINT REPLAY READY — 90%** | "
            "Independent `python-flint` 0.9.0 certifier and independent output auditor are included; they reconstruct the stable chart without importing the principal certifier; 384/512-bit and reverse-order runs plus two rejection controls are scripted | "
            "Run the isolated virtual-environment replay on the author's Mac, archive the wheel/install report and generated balls, then promote this point to closed |"
        ),
    ]
    new_fragment = (
        "| 2 | Interval-arithmetic trust boundary | **CLOSED — INDEPENDENT ARB/FLINT REPLAY PASS — 100%** | "
        "Independent `python-flint` 0.9.0 implementation; rigorous Arb balls for arithmetic, `sqrt`, and `atan`; 384/512-bit and reverse-order passes; under-resolved and sign-mutation controls rejected; overlap with the archived direct-MPFR preflight; high-headroom bounds `Phi(1)>1/4000` and `Phi''<-1/30000` | "
        "Final editorial integration into the DCG manuscript and release-response letter only |"
    )
    ledger = ledger_path.read_text(encoding="utf-8")
    replaced = False
    for old_fragment in old_fragments:
        if old_fragment in ledger:
            ledger = ledger.replace(old_fragment, new_fragment)
            replaced = True
            break
    if not replaced and "INDEPENDENT ARB/FLINT REPLAY PASS" not in ledger:
        raise RuntimeError("could not locate Reviewer Point 2 ledger row")
    for remaining_text in (
        "official-header MPFR replay; independent review and manuscript integration of Points 1 and 3.",
        "independent Arb/FLINT replay; independent review and manuscript integration of Points 1 and 3.",
    ):
        ledger = ledger.replace(
            remaining_text,
            "independent review and manuscript integration of Points 1 and 3."
        )
    ledger_path.write_text(ledger, encoding="utf-8")

    progress = json.loads(progress_path.read_text(encoding="utf-8"))
    progress["branch"] = "review/dcg-major-revision"
    progress["points"]["2"] = {
        "status": "CLOSED_INDEPENDENT_ARB_FLINT_REPLAY_PASS",
        "percent": 100,
        "closed": True,
    }
    progress_path.write_text(json.dumps(progress, indent=2) + "\n", encoding="utf-8")

    promotion = {
        "promotion_version": PROMOTION_VERSION,
        "classification": "PEABODY_DCG_POINT_2_ARB_FLINT_PROMOTION_PASS",
        "pass": True,
        "reviewer_point": 2,
        "status": progress["points"]["2"],
        "python_flint_distribution": cert["environment"]["python_flint_distribution"],
        "endpoint_lower": cert["endpoint"]["phi_one_enclosure"]["lower"],
        "endpoint_target": cert["endpoint"]["target"],
        "worst_phi_second_upper": cert["concavity"]["worst_phi_second_upper"],
        "concavity_target": cert["concavity"]["target"],
        "hashes": {
            "local_replay_summary": sha256(replay_path),
            "arb_certificate_audit": sha256(audit_path),
            "forward_384_certificate": sha256(cert_path),
        },
        "homebrew_used": False,
        "system_package_manager_used": False,
    }
    out = checkpoint / "data" / "arb_flint_promotion.json"
    out.write_text(json.dumps(promotion, indent=2) + "\n", encoding="utf-8")
    print(promotion["classification"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
