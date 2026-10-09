#!/usr/bin/env python3
"""Promote DCG Reviewer Points 1 and 3 after the internal proof audit passes."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def replace_table_row(text: str, point: int, new_row: str) -> str:
    lines = text.splitlines()
    prefix = f"| {point} |"
    matches = [i for i, line in enumerate(lines) if line.startswith(prefix)]
    if len(matches) != 1:
        raise RuntimeError(f"expected one ledger row for point {point}, found {len(matches)}")
    lines[matches[0]] = new_row
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint-dir", type=Path, required=True)
    parser.add_argument("--audit-json", type=Path, required=True)
    parser.add_argument("--proofread-note", type=Path, required=True)
    args = parser.parse_args()

    checkpoint = args.checkpoint_dir.resolve()
    ledger_path = checkpoint / "REVIEW_PROGRESS_LEDGER.md"
    progress_path = checkpoint / "data" / "reviewer_point_progress.json"
    audit_path = args.audit_json.resolve()
    proofread_path = args.proofread_note.resolve()

    for path in (ledger_path, progress_path, audit_path, proofread_path):
        if not path.is_file():
            raise FileNotFoundError(path)

    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    if audit.get("pass") is not True:
        raise RuntimeError("Point 1 / Point 3 exact identity audit has not passed")

    ledger = ledger_path.read_text(encoding="utf-8")
    ledger = replace_table_row(
        ledger,
        1,
        "| 1 | Convexity, constant width, and exact Gauss tiling for every `e` and `sigma` | **CLOSED INTERNALLY — 100%** | Explicit principal-circle and bulb-center verification; regular-tetrahedron endpoint proof; source-theorem crosswalk; strict-convexity normal partition; seam nullity; cap-cone duality; corrected singular-arc degeneration | External source-author or convex-geometer convention check recommended before submission |",
    )
    ledger = replace_table_row(
        ledger,
        3,
        "| 3 | Full derivation of the one-pair formula and branch control | **CLOSED INTERNALLY — 100%** | Complete center-distance, normal-chart, wedge-Jacobian, `xi`-integration, `Psi(0)`, fixed-interval, stable-chart, coefficient, and principal-branch derivations; independent exact identity audit passes | External line-by-line mathematical proofread recommended before submission |",
    )
    ledger = ledger.replace(
        "independent review and manuscript integration of Points 1 and 3.",
        "final manuscript integration, external geometric/formula review, and five-point release audit.",
    )
    ledger_path.write_text(ledger, encoding="utf-8")

    progress = json.loads(progress_path.read_text(encoding="utf-8"))
    progress.setdefault("points", {})
    progress["points"]["1"] = {
        "status": "CLOSED_INTERNALLY_EXTERNAL_GEOMETRIC_CHECK_RECOMMENDED",
        "percent": 100,
        "closed": True,
    }
    progress["points"]["3"] = {
        "status": "CLOSED_INTERNALLY_EXTERNAL_LINE_BY_LINE_CHECK_RECOMMENDED",
        "percent": 100,
        "closed": True,
    }
    progress["all_five_points_mathematically_addressed"] = all(
        bool(progress["points"].get(str(i), {}).get("closed")) for i in range(1, 6)
    )
    progress["external_review_recommended"] = True
    progress["final_dcg_release_audit_pending"] = True
    progress_path.write_text(json.dumps(progress, indent=2) + "\n", encoding="utf-8")

    promotion = {
        "classification": "PEABODY_DCG_POINTS_1_3_INTERNAL_CLOSEOUT_PASS",
        "pass": True,
        "points": [1, 3],
        "exact_identity_audit": sha256(audit_path),
        "proofread_note": sha256(proofread_path),
        "progress_all_five_closed": progress["all_five_points_mathematically_addressed"],
        "external_review_recommended": True,
    }
    out = checkpoint / "data" / "points_1_3_internal_closeout.json"
    out.write_text(json.dumps(promotion, indent=2) + "\n", encoding="utf-8")
    print(promotion["classification"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
