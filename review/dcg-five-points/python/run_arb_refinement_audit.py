#!/usr/bin/env python3
"""Bounded Arb refinement study for Peabody enclosure provenance.

This is not a new proof search.  It compares enclosure width under a frozen
stable formula and increasingly fine rational partitions.  It also compares
with the archived direct-MPFR and legacy mpmath.iv endpoint-interval outputs.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import sys
import time
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

getcontext().prec = 160

CONFIGS = [(32, 10), (64, 20), (128, 20)]
ENDPOINT_PANELS = [4, 8, 16]
BITS = 384


def d(x: Any) -> Decimal:
    return Decimal(str(x).strip())


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("peabody_arb_concavity_reconcile", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import Arb certifier: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_mpfr(path: Path) -> dict[int, dict[str, Decimal]]:
    out: dict[int, dict[str, Decimal]] = {}
    with path.open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            out[int(row["index"])] = {
                "lower": d(row["phi_second_lower"]),
                "upper": d(row["phi_second_upper"]),
            }
    return out


def load_mpmath(path: Path) -> tuple[dict[int, dict[str, Decimal]], dict[str, Decimal]]:
    doc = json.loads(path.read_text(encoding="utf-8"))
    slabs = {
        int(row["index"]): {
            "lower": d(row["phi_second"]["lower"]),
            "upper": d(row["phi_second"]["upper"]),
        }
        for row in doc["concavity"]["slabs"]
    }
    endpoint = {
        "lower": d(doc["endpoint"]["phi_one_enclosure"]["lower"]),
        "upper": d(doc["endpoint"]["phi_one_enclosure"]["upper"]),
    }
    return slabs, endpoint


def arb_bounds(value, digits: int = 140) -> tuple[Decimal, Decimal]:
    return d(value.lower().str(digits, radius=False)), d(value.upper().str(digits, radius=False))


def compute_arb_slabs(module, q_slabs: int, x_panels: int) -> list[dict[str, Any]]:
    constants = module.setup(BITS)
    rows: list[dict[str, Any]] = []
    for index in range(q_slabs):
        q_lo = Fraction(index, q_slabs)
        q_hi = Fraction(index + 1, q_slabs)
        _, phi_second, _, _ = module.concavity_slab(
            q_lo, q_hi, constants, x_panels, correction_sign=1, record=False
        )
        lo, hi = arb_bounds(phi_second)
        rows.append({
            "index": index,
            "q_lo": f"{q_lo.numerator}/{q_lo.denominator}",
            "q_hi": f"{q_hi.numerator}/{q_hi.denominator}",
            "lower": lo,
            "upper": hi,
        })
    return rows


def aggregate_to_32(rows: list[dict[str, Any]], q_slabs: int) -> dict[int, dict[str, Decimal]]:
    if q_slabs % 32:
        raise ValueError("q_slabs must be divisible by 32")
    per = q_slabs // 32
    out: dict[int, dict[str, Decimal]] = {}
    for base in range(32):
        chunk = rows[base * per:(base + 1) * per]
        out[base] = {
            "lower": min(row["lower"] for row in chunk),
            "upper": max(row["upper"] for row in chunk),
        }
    return out


def overlap(a: dict[str, Decimal], b: dict[str, Decimal]) -> bool:
    return max(a["lower"], b["lower"]) <= min(a["upper"], b["upper"])


def contains(a: dict[str, Decimal], b: dict[str, Decimal]) -> bool:
    return a["lower"] <= b["lower"] and a["upper"] >= b["upper"]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certifier", type=Path, required=True)
    parser.add_argument("--mpfr-csv", type=Path, required=True)
    parser.add_argument("--mpfr-json", type=Path, required=True)
    parser.add_argument("--mpmath-json", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    module = load_module(args.certifier)
    module.MAX_BOXES = 10000  # diagnostic hard cap; no new proof search
    constants = module.setup(BITS)

    endpoint_rows: list[dict[str, Any]] = []
    for panels in ENDPOINT_PANELS:
        start = time.time()
        value, _ = module.endpoint_phi(constants, panels, correction_sign=1, record=False)
        lo, hi = arb_bounds(value)
        endpoint_rows.append({
            "implementation": "Arb",
            "bits": BITS,
            "x_panels": panels,
            "lower": str(lo),
            "upper": str(hi),
            "width": str(hi - lo),
            "elapsed_seconds": f"{time.time() - start:.6f}",
            "proves_phi_one_positive": bool(lo > 0),
            "proves_phi_one_gt_1_over_4000": bool(lo > Decimal(1) / Decimal(4000)),
        })

    arb_runs: dict[tuple[int, int], list[dict[str, Any]]] = {}
    run_rows: list[dict[str, Any]] = []
    for q_slabs, x_panels in CONFIGS:
        start = time.time()
        rows = compute_arb_slabs(module, q_slabs, x_panels)
        elapsed = time.time() - start
        arb_runs[(q_slabs, x_panels)] = rows
        worst = max(rows, key=lambda row: row["upper"])
        run_rows.append({
            "implementation": "Arb",
            "bits": BITS,
            "q_slabs": q_slabs,
            "x_panels": x_panels,
            "terminal_rectangles": q_slabs * x_panels,
            "worst_slab_index": worst["index"],
            "worst_phi_second_lower": str(worst["lower"]),
            "worst_phi_second_upper": str(worst["upper"]),
            "proves_strict_concavity": bool(worst["upper"] < 0),
            "proves_target_minus_1_over_100000": bool(worst["upper"] < -(Decimal(1) / Decimal(100000))),
            "elapsed_seconds": f"{elapsed:.6f}",
        })
        write_csv(args.output_dir / f"arb_slabs_{q_slabs}x{x_panels}.csv", [
            {k: str(v) for k, v in row.items()} for row in rows
        ])

    mpfr = load_mpfr(args.mpfr_csv)
    mpfr_doc = json.loads(args.mpfr_json.read_text(encoding="utf-8"))
    mpmath, mpmath_endpoint = load_mpmath(args.mpmath_json)
    mpfr_endpoint = {
        "lower": d(mpfr_doc["endpoint"]["phi_one_lower"]),
        "upper": d(mpfr_doc["endpoint"]["phi_one_upper"]),
    }

    comparisons: list[dict[str, Any]] = []
    for index in range(32):
        row: dict[str, Any] = {
            "index": index,
            "q_lo": f"{index}/32",
            "q_hi": f"{index+1}/32",
            "mpfr_lower": str(mpfr[index]["lower"]),
            "mpfr_upper": str(mpfr[index]["upper"]),
            "mpmath_lower": str(mpmath[index]["lower"]),
            "mpmath_upper": str(mpmath[index]["upper"]),
            "mpmath_mpfr_intersect": overlap(mpmath[index], mpfr[index]),
            "mpfr_contains_mpmath": contains(mpfr[index], mpmath[index]),
        }
        for q_slabs, x_panels in CONFIGS:
            agg = aggregate_to_32(arb_runs[(q_slabs, x_panels)], q_slabs)[index]
            prefix = f"arb_{q_slabs}x{x_panels}"
            row[f"{prefix}_lower"] = str(agg["lower"])
            row[f"{prefix}_upper"] = str(agg["upper"])
            row[f"{prefix}_intersects_mpfr"] = overlap(agg, mpfr[index])
            row[f"{prefix}_contains_mpfr"] = contains(agg, mpfr[index])
            row[f"{prefix}_width"] = str(agg["upper"] - agg["lower"])
        comparisons.append(row)

    arb_worst = [d(row["worst_phi_second_upper"]) for row in run_rows]
    tightening = all(arb_worst[i + 1] <= arb_worst[i] for i in range(len(arb_worst) - 1))
    all_signs = all(bool(row["proves_strict_concavity"]) for row in run_rows)
    all_targets = all(bool(row["proves_target_minus_1_over_100000"]) for row in run_rows)
    all_endpoints = all(bool(row["proves_phi_one_gt_1_over_4000"]) for row in endpoint_rows)
    all_intersections = all(
        bool(row[f"arb_{q}x{x}_intersects_mpfr"])
        for row in comparisons for q, x in CONFIGS
    )

    summary = {
        "classification": "PEABODY_ENCLOSURE_RECONCILIATION_PASS" if (all_signs and all_endpoints and all_intersections) else "PEABODY_ENCLOSURE_RECONCILIATION_REVIEW",
        "pass": bool(all_signs and all_endpoints and all_intersections),
        "scope": "bounded enclosure-provenance audit; no new shape search and no formula change",
        "arb": {
            "bits": BITS,
            "runs": run_rows,
            "endpoint_runs": endpoint_rows,
            "worst_upper_tightens_monotonically": tightening,
            "all_runs_prove_strict_concavity": all_signs,
            "all_runs_prove_minus_1_over_100000": all_targets,
            "all_endpoint_runs_prove_1_over_4000": all_endpoints,
        },
        "archived_endpoint_interval_implementations": {
            "direct_mpfr": {
                "endpoint_lower": str(mpfr_endpoint["lower"]),
                "endpoint_upper": str(mpfr_endpoint["upper"]),
                "worst_phi_second_upper": str(max(v["upper"] for v in mpfr.values())),
            },
            "legacy_mpmath_iv": {
                "endpoint_lower": str(mpmath_endpoint["lower"]),
                "endpoint_upper": str(mpmath_endpoint["upper"]),
                "worst_phi_second_upper": str(max(v["upper"] for v in mpmath.values())),
            },
            "all_32x10_slab_intervals_intersect": all(overlap(mpfr[i], mpmath[i]) for i in range(32)),
            "direct_mpfr_contains_legacy_mpmath_on_all_slabs": all(contains(mpfr[i], mpmath[i]) for i in range(32)),
        },
        "arb_mpfr_comparison": {
            "all_aggregated_arb_intervals_intersect_mpfr": all_intersections,
            "interpretation": (
                "The endpoint-interval implementations agree closely with each other.  "
                "Arb ball enclosures are wider on the coarse partition.  Refinement behavior is "
                "reported directly rather than attributed to arithmetic precision or to a failure "
                "of the legacy mpmath calculation.  The paper uses only the conservative Arb bound."
            ),
        },
    }

    write_csv(args.output_dir / "arb_refinement_runs.csv", run_rows)
    write_csv(args.output_dir / "endpoint_refinement_runs.csv", endpoint_rows)
    write_csv(args.output_dir / "slabwise_enclosure_comparison.csv", comparisons)
    (args.output_dir / "enclosure_reconciliation.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    # Markdown report.
    md = [
        "# Interval-enclosure reconciliation", "",
        "This is a bounded provenance audit. It does not alter the Peabody formula or search a new family.", "",
        "## Global results", "",
        "| Implementation | Partition | Endpoint lower | Weakest upper bound for `Phi''` |", "|---|---:|---:|---:|",
        f"| legacy `mpmath.iv` | 32 x 10; endpoint 4 | {mpmath_endpoint['lower']} | {max(v['upper'] for v in mpmath.values())} |",
        f"| direct directed-rounding MPFR | 32 x 10; endpoint 4 | {mpfr_endpoint['lower']} | {max(v['upper'] for v in mpfr.values())} |",
    ]
    for row in run_rows:
        md.append(f"| Arb | {row['q_slabs']} x {row['x_panels']} | see endpoint table | {row['worst_phi_second_upper']} |")
    md.extend(["", "## Arb endpoint refinement", "", "| x panels | lower | upper |", "|---:|---:|---:|"])
    for row in endpoint_rows:
        md.append(f"| {row['x_panels']} | {row['lower']} | {row['upper']} |")
    md.extend([
        "", "## Interpretation", "",
        summary["arb_mpfr_comparison"]["interpretation"], "",
        f"Classification: `{summary['classification']}`.", "",
    ])
    (args.output_dir / "enclosure_reconciliation.md").write_text("\n".join(md), encoding="utf-8")

    # LaTeX table for the manuscript.
    row_end = r"\\"
    lines = [
        r"\begin{table}[t]", r"\centering", r"\small",
        r"\begin{tabular}{lcc}", r"\toprule",
        f"implementation & endpoint lower bound & weakest upper bound for $\\Phi''$ {row_end}",
        r"\midrule",
        f"legacy \\texttt{{mpmath.iv}} & ${mpmath_endpoint['lower']:.12E}$ & ${max(v['upper'] for v in mpmath.values()):.12E}$ {row_end}",
        f"direct MPFR & ${mpfr_endpoint['lower']:.12E}$ & ${max(v['upper'] for v in mpfr.values()):.12E}$ {row_end}",
    ]
    # use finest Arb run in generated manuscript table
    finest = run_rows[-1]
    finest_endpoint = endpoint_rows[-1]
    lines.append(
        f"Arb refinement & ${d(finest_endpoint['lower']):.12E}$ & "
        f"${d(finest['worst_phi_second_upper']):.12E}$ {row_end}"
    )
    lines.extend([
        r"\bottomrule", r"\end{tabular}",
        r"\caption{Enclosure comparison.  The endpoint-interval implementations are retained only as redundant audits; Arb is the proof authority.}",
        r"\label{tab:enclosure-reconciliation}", r"\end{table}", "",
    ])
    (args.output_dir / "generated_enclosure_reconciliation.tex").write_text("\n".join(lines), encoding="utf-8")

    print(summary["classification"])
    print("pass:", summary["pass"])
    for row in run_rows:
        print(f"Arb {row['q_slabs']}x{row['x_panels']} worst upper:", row["worst_phi_second_upper"])
    return 0 if summary["pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
