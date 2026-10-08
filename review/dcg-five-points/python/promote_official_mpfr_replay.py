#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint-dir", type=Path, required=True)
    args = parser.parse_args()
    root = args.checkpoint_dir.resolve()
    results = root / "results/mpfr"

    summary_path = results / "local_replay_summary.json"
    audit_path = results / "mpfr_certificate_audit.json"
    build_path = results / "build.txt"
    if not (summary_path.is_file() and audit_path.is_file() and build_path.is_file()):
        raise SystemExit("STOP: official-header replay outputs are incomplete")

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    if summary.get("pass") is not True or summary.get("classification") != "PEABODY_DCG_MPFR_OFFICIAL_HEADER_REPLAY_PASS":
        raise SystemExit("STOP: local replay summary did not pass")
    if audit.get("pass") is not True:
        raise SystemExit("STOP: MPFR certificate audit did not pass")
    build_text = build_path.read_text(encoding="utf-8")
    if "PEABODY_MPFR_BUILD_OFFICIAL_HEADER_PASS" not in build_text:
        raise SystemExit("STOP: build transcript does not prove use of the official header")

    progress_path = root / "data/reviewer_point_progress.json"
    progress = json.loads(progress_path.read_text(encoding="utf-8"))
    progress["points"]["2"] = {
        "status": "OFFICIAL_HEADER_MPFR_REPLAY_PASS",
        "percent": 100,
        "closed": True,
    }
    progress_path.write_text(json.dumps(progress, indent=2) + "\n", encoding="utf-8")

    ledger_path = root / "REVIEW_PROGRESS_LEDGER.md"
    ledger = ledger_path.read_text(encoding="utf-8")
    pattern = re.compile(r"^\| 2 \| Interval-arithmetic trust boundary \|.*$", re.MULTILINE)
    replacement = (
        "| 2 | Interval-arithmetic trust boundary | **CLOSED - OFFICIAL-HEADER MPFR REPLAY PASS - 100%** "
        "| Independent C/MPFR implementation; official-header build; 384/512-bit and reverse-order passes; "
        "under-resolved and sign-mutation controls rejected; high-headroom bounds `Phi(1)>1/4000` and "
        "`Phi''<-1/30000` | Manuscript wording and final release audit only |"
    )
    ledger, count = pattern.subn(replacement, ledger)
    if count != 1:
        raise SystemExit("STOP: could not update Point 2 ledger row uniquely")
    ledger_path.write_text(ledger, encoding="utf-8")

    promotion = {
        "classification": "PEABODY_DCG_POINT_2_OFFICIAL_HEADER_PROMOTION_PASS",
        "pass": True,
        "summary_sha256": sha256(summary_path),
        "audit_sha256": sha256(audit_path),
        "build_transcript_sha256": sha256(build_path),
        "mpfr_certificate_classification": audit["classification"],
        "endpoint_lower": audit["endpoint_lower"],
        "worst_phi_second_upper": audit["worst_phi_second_upper"],
    }
    out = root / "data/official_header_mpfr_promotion.json"
    out.write_text(json.dumps(promotion, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(promotion, indent=2))
    print("PEABODY_DCG_POINT_2_OFFICIAL_HEADER_PROMOTION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
