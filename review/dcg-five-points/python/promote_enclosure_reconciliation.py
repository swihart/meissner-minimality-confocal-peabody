#!/usr/bin/env python3
"""Promote the bounded enclosure-reconciliation audit into the live review ledger."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

MARKER = "## Follow-up enclosure-provenance reconciliation"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint-dir", type=Path, required=True)
    args = parser.parse_args()
    root = args.checkpoint_dir
    result_path = root / "results/enclosure-reconciliation/enclosure_reconciliation.json"
    if not result_path.is_file():
        raise SystemExit(f"missing reconciliation result: {result_path}")
    result = json.loads(result_path.read_text(encoding="utf-8"))
    if result.get("pass") is not True:
        raise SystemExit(f"reconciliation audit did not pass: {result.get('classification')}")

    progress_path = root / "data/reviewer_point_progress.json"
    progress = json.loads(progress_path.read_text(encoding="utf-8"))
    point = progress["points"]["2"]
    if point.get("closed") is not True or point.get("percent") != 100:
        raise SystemExit(f"Reviewer Point 2 is not already closed: {point}")
    point["status"] = "CLOSED_BY_ARB_FLINT_REPLAY_PROVENANCE_RECONCILED"
    progress["interval_enclosure_provenance_reconciled"] = True
    progress["enclosure_reconciliation_classification"] = result["classification"]
    progress_path.write_text(json.dumps(progress, indent=2) + "\n", encoding="utf-8")

    ledger_path = root / "REVIEW_PROGRESS_LEDGER.md"
    ledger = ledger_path.read_text(encoding="utf-8")
    lines = ledger.splitlines()
    replaced = False
    for idx, line in enumerate(lines):
        if line.startswith("| 2 |"):
            lines[idx] = (
                "| 2 | Interval-arithmetic trust boundary | "
                "**CLOSED - ARB/FLINT REPLAY AND ENCLOSURE PROVENANCE RECONCILED - 100%** | "
                "Independent Arb proof authority; direct-MPFR and legacy mpmath endpoint-interval comparisons; bounded Arb refinement audit; conservative Arb constants used in the manuscript | "
                "Final editorial review only |"
            )
            replaced = True
            break
    if not replaced:
        raise SystemExit("could not locate Reviewer Point 2 ledger row")
    ledger = "\n".join(lines).rstrip() + "\n"
    if MARKER not in ledger:
        ledger += (
            "\n" + MARKER + "\n\n"
            "- The direct-MPFR and legacy `mpmath.iv` endpoint-interval implementations agree closely at the frozen `32x10` partition.\n"
            "- Arb midpoint-radius enclosures are wider on the coarse partition; the theorem uses only the conservative Arb result.\n"
            "- A bounded `32x10`, `64x20`, `128x20` refinement study records the enclosure-width behavior without changing the formula or theorem.\n"
            "- The manuscript now uses the Arb endpoint decimal consistently and no longer states the ambiguous `overlap` sentence.\n"
        )
    ledger_path.write_text(ledger, encoding="utf-8")

    promotion = {
        "classification": "PEABODY_DCG_ENCLOSURE_RECONCILIATION_PROMOTION_PASS",
        "pass": True,
        "result_classification": result["classification"],
        "point_2_status": point["status"],
    }
    out = root / "data/enclosure_reconciliation_promotion.json"
    out.write_text(json.dumps(promotion, indent=2) + "\n", encoding="utf-8")
    print(promotion["classification"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
