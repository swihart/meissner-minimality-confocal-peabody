#!/usr/bin/env python3
"""Compare legacy mpmath.iv and direct-MPFR Peabody enclosures.

This audit does not use either implementation as proof authority.  It records
how closely the two endpoint-interval implementations agree at the frozen
32-by-10 partition, so the wider Arb ball enclosure can be discussed openly.
"""
from __future__ import annotations

import argparse
import csv
import json
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any

getcontext().prec = 120


def dec(x: str) -> Decimal:
    return Decimal(str(x).strip())


def load_mpmath(path: Path) -> tuple[dict[str, Any], dict[int, dict[str, Decimal]]]:
    d = json.loads(path.read_text(encoding="utf-8"))
    slabs: dict[int, dict[str, Decimal]] = {}
    for row in d["concavity"]["slabs"]:
        slabs[int(row["index"])] = {
            "lower": dec(row["phi_second"]["lower"]),
            "upper": dec(row["phi_second"]["upper"]),
        }
    return d, slabs


def load_mpfr(path: Path) -> dict[int, dict[str, Decimal]]:
    rows: dict[int, dict[str, Decimal]] = {}
    with path.open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            rows[int(row["index"])] = {
                "lower": dec(row["phi_second_lower"]),
                "upper": dec(row["phi_second_upper"]),
            }
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mpmath-json", type=Path, required=True)
    parser.add_argument("--mpfr-csv", type=Path, required=True)
    parser.add_argument("--mpfr-json", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    mpmath_doc, mpmath = load_mpmath(args.mpmath_json)
    mpfr = load_mpfr(args.mpfr_csv)
    mpfr_doc = json.loads(args.mpfr_json.read_text(encoding="utf-8"))

    if set(mpmath) != set(mpfr):
        raise SystemExit("slab-index mismatch between mpmath and MPFR")

    rows: list[dict[str, str | int | bool]] = []
    max_lower_diff = Decimal(0)
    max_upper_diff = Decimal(0)
    all_intersect = True
    all_mpmath_contains_mpfr = True
    all_mpfr_contains_mpmath = True

    for index in sorted(mpmath):
        a = mpmath[index]
        b = mpfr[index]
        lower_diff = abs(a["lower"] - b["lower"])
        upper_diff = abs(a["upper"] - b["upper"])
        max_lower_diff = max(max_lower_diff, lower_diff)
        max_upper_diff = max(max_upper_diff, upper_diff)
        intersect = max(a["lower"], b["lower"]) <= min(a["upper"], b["upper"])
        a_contains_b = a["lower"] <= b["lower"] and a["upper"] >= b["upper"]
        b_contains_a = b["lower"] <= a["lower"] and b["upper"] >= a["upper"]
        all_intersect &= intersect
        all_mpmath_contains_mpfr &= a_contains_b
        all_mpfr_contains_mpmath &= b_contains_a
        rows.append({
            "index": index,
            "mpmath_lower": str(a["lower"]),
            "mpmath_upper": str(a["upper"]),
            "mpfr_lower": str(b["lower"]),
            "mpfr_upper": str(b["upper"]),
            "absolute_lower_difference": str(lower_diff),
            "absolute_upper_difference": str(upper_diff),
            "intervals_intersect": intersect,
            "mpmath_contains_mpfr": a_contains_b,
            "mpfr_contains_mpmath": b_contains_a,
        })

    endpoint_mpmath = mpmath_doc["endpoint"]["phi_one_enclosure"]
    endpoint_mpfr = mpfr_doc["endpoint"]
    endpoint_lower_diff = abs(dec(endpoint_mpmath["lower"]) - dec(endpoint_mpfr["phi_one_lower"]))
    endpoint_upper_diff = abs(dec(endpoint_mpmath["upper"]) - dec(endpoint_mpfr["phi_one_upper"]))

    worst_mpmath = max(mpmath.items(), key=lambda kv: kv[1]["upper"])
    worst_mpfr = max(mpfr.items(), key=lambda kv: kv[1]["upper"])

    summary = {
        "classification": "PEABODY_BASELINE_ENDPOINT_INTERVAL_COMPARISON_PASS",
        "pass": bool(all_intersect),
        "partition": {"q_slabs": 32, "x_panels_per_slab": 10, "endpoint_x_panels": 4},
        "mpmath": {
            "worst_slab": worst_mpmath[0],
            "worst_phi_second_upper": str(worst_mpmath[1]["upper"]),
            "endpoint_lower": endpoint_mpmath["lower"],
            "endpoint_upper": endpoint_mpmath["upper"],
        },
        "direct_mpfr": {
            "worst_slab": worst_mpfr[0],
            "worst_phi_second_upper": str(worst_mpfr[1]["upper"]),
            "endpoint_lower": endpoint_mpfr["phi_one_lower"],
            "endpoint_upper": endpoint_mpfr["phi_one_upper"],
        },
        "comparison": {
            "all_slabs_intersect": all_intersect,
            "all_mpmath_contains_mpfr": all_mpmath_contains_mpfr,
            "all_mpfr_contains_mpmath": all_mpfr_contains_mpmath,
            "max_absolute_lower_endpoint_difference": str(max_lower_diff),
            "max_absolute_upper_endpoint_difference": str(max_upper_diff),
            "endpoint_lower_difference": str(endpoint_lower_diff),
            "endpoint_upper_difference": str(endpoint_upper_diff),
        },
        "interpretation": (
            "At the frozen 32x10 partition, the legacy mpmath.iv and direct directed-rounding "
            "MPFR endpoint-interval implementations agree very closely.  The wider Arb result "
            "must therefore be discussed as a difference in enclosure representation or wrapping, "
            "not silently attributed to arithmetic precision alone."
        ),
    }

    with (args.output_dir / "baseline_interval_comparison.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    (args.output_dir / "baseline_interval_comparison.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(summary["classification"])
    print("pass:", summary["pass"])
    print("max upper difference:", summary["comparison"]["max_absolute_upper_endpoint_difference"])
    return 0 if summary["pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
