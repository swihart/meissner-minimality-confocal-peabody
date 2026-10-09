#!/usr/bin/env python3
"""Independent audit of the no-Homebrew Arb/FLINT replay.

This checker deliberately does not import the Arb certifier.  It verifies the
archived JSON/CSV outputs, precision and order replays, adversarial controls,
and overlap with the previously archived direct-MPFR preflight certificate.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

AUDIT_VERSION = "PEABODY_ARB_FLINT_CERTIFICATE_AUDIT_V3"
PINNED_PYTHON_FLINT = "0.9.0"
getcontext().prec = 180


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dec(text: str) -> Decimal:
    return Decimal(str(text))



def binary_fraction(point: dict[str, Any]) -> Fraction:
    mantissa = int(point["mantissa"])
    exponent = int(point["exponent"])
    if exponent >= 0:
        return Fraction(mantissa * (1 << exponent), 1)
    return Fraction(mantissa, 1 << (-exponent))

def intervals_overlap(lo1: str, hi1: str, lo2: str, hi2: str) -> bool:
    return max(dec(lo1), dec(lo2)) <= min(dec(hi1), dec(hi2))


def load_slab_csv(path: Path) -> dict[int, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    return {int(row["index"]): row for row in rows}


def require_cert(path: Path) -> dict[str, Any]:
    data = load_json(path)
    required = {
        "certificate_version",
        "classification",
        "pass",
        "environment",
        "endpoint",
        "concavity",
        "terminal_rectangles",
        "subdivision_order",
        "correction_sign",
    }
    missing = sorted(required - data.keys())
    if missing:
        raise RuntimeError(f"{path}: missing keys {missing}")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint-dir", type=Path, required=True)
    args = parser.parse_args()

    checkpoint = args.checkpoint_dir.resolve()
    result_root = checkpoint / "results" / "arb"
    preflight_root = checkpoint / "preflight" / "assistant_mpfr_runtime_only"

    paths = {
        "forward_384": result_root / "forward_384" / "peabody_arb_concavity_certificate.json",
        "forward_512": result_root / "forward_512" / "peabody_arb_concavity_certificate.json",
        "reverse_384": result_root / "reverse_384" / "peabody_arb_concavity_certificate.json",
        "control_underresolved": result_root / "control_1x1" / "peabody_arb_concavity_certificate.json",
        "control_mutation": result_root / "control_sign_mutation" / "peabody_arb_concavity_certificate.json",
        "mpfr": preflight_root / "forward_384" / "peabody_mpfr_concavity_certificate.json",
    }
    for name, path in paths.items():
        if not path.is_file():
            raise FileNotFoundError(f"missing {name}: {path}")

    forward = require_cert(paths["forward_384"])
    precision = require_cert(paths["forward_512"])
    reverse = require_cert(paths["reverse_384"])
    control_underresolved = require_cert(paths["control_underresolved"])
    mutation = require_cert(paths["control_mutation"])
    mpfr = load_json(paths["mpfr"])

    checks: dict[str, bool] = {}
    checks["forward_pass"] = forward["pass"] is True
    checks["precision_pass"] = precision["pass"] is True
    checks["reverse_pass"] = reverse["pass"] is True
    checks["underresolved_rejected"] = control_underresolved["pass"] is False
    checks["mutation_rejected"] = mutation["pass"] is False
    checks["controls_emit_semantic_no_go"] = (
        control_underresolved.get("classification") == "NO_GO_PEABODY_ARB_FLINT_CERTIFICATE"
        and control_underresolved.get("proof_status") == "NOT_CERTIFIED"
        and mutation.get("classification") == "NO_GO_PEABODY_ARB_FLINT_CERTIFICATE"
        and mutation.get("proof_status") == "NOT_CERTIFIED"
    )
    checks["pinned_python_flint"] = (
        forward["environment"].get("python_flint_distribution") == PINNED_PYTHON_FLINT
        and precision["environment"].get("python_flint_distribution") == PINNED_PYTHON_FLINT
        and reverse["environment"].get("python_flint_distribution") == PINNED_PYTHON_FLINT
    )
    checks["precision_bits"] = (
        int(forward["environment"].get("precision_bits", 0)) == 384
        and int(precision["environment"].get("precision_bits", 0)) == 512
        and int(reverse["environment"].get("precision_bits", 0)) == 384
    )
    checks["subdivision_orders"] = (
        forward["subdivision_order"] == "forward"
        and precision["subdivision_order"] == "forward"
        and reverse["subdivision_order"] == "reverse"
    )
    checks["correct_formula_controls"] = (
        int(forward["correction_sign"]) == 1
        and int(precision["correction_sign"]) == 1
        and int(reverse["correction_sign"]) == 1
        and int(mutation["correction_sign"]) == -1
    )
    checks["box_counts"] = (
        int(forward["terminal_rectangles"]) == 324
        and int(precision["terminal_rectangles"]) == 324
        and int(reverse["terminal_rectangles"]) == 324
    )
    endpoint_binary = forward["endpoint"]["phi_one_enclosure"].get("lower_binary")
    concavity_binary = forward["concavity"].get("worst_phi_second_upper_binary")
    checks["exact_binary_endpoints_archived"] = endpoint_binary is not None and concavity_binary is not None
    checks["publication_bounds"] = (
        forward["endpoint"].get("target") == "1/4000"
        and forward["concavity"].get("target") == "-1/100000"
        and endpoint_binary is not None
        and concavity_binary is not None
        and binary_fraction(endpoint_binary) > Fraction(1, 4000)
        and binary_fraction(concavity_binary) < -Fraction(1, 100000)
    )
    checks["all_domain_diagnostics_positive"] = all(
        item.get("strictly_positive") is True
        for item in forward.get("domain_diagnostics", {}).values()
    )

    # Replays must enclose compatible values.
    checks["endpoint_forward_precision_overlap"] = intervals_overlap(
        forward["endpoint"]["phi_one_enclosure"]["lower"],
        forward["endpoint"]["phi_one_enclosure"]["upper"],
        precision["endpoint"]["phi_one_enclosure"]["lower"],
        precision["endpoint"]["phi_one_enclosure"]["upper"],
    )
    checks["endpoint_forward_reverse_overlap"] = intervals_overlap(
        forward["endpoint"]["phi_one_enclosure"]["lower"],
        forward["endpoint"]["phi_one_enclosure"]["upper"],
        reverse["endpoint"]["phi_one_enclosure"]["lower"],
        reverse["endpoint"]["phi_one_enclosure"]["upper"],
    )
    checks["endpoint_arb_mpfr_overlap"] = intervals_overlap(
        forward["endpoint"]["phi_one_enclosure"]["lower"],
        forward["endpoint"]["phi_one_enclosure"]["upper"],
        mpfr["endpoint"]["phi_one_lower"],
        mpfr["endpoint"]["phi_one_upper"],
    )

    arb_forward_slabs = load_slab_csv(result_root / "forward_384" / "concavity_slab_summary.csv")
    arb_precision_slabs = load_slab_csv(result_root / "forward_512" / "concavity_slab_summary.csv")
    arb_reverse_slabs = load_slab_csv(result_root / "reverse_384" / "concavity_slab_summary.csv")
    mpfr_slabs = load_slab_csv(preflight_root / "forward_384" / "concavity_slab_summary.csv")
    checks["all_32_slabs_present"] = (
        sorted(arb_forward_slabs) == list(range(32))
        and sorted(arb_precision_slabs) == list(range(32))
        and sorted(arb_reverse_slabs) == list(range(32))
        and sorted(mpfr_slabs) == list(range(32))
    )

    slab_overlap_checks: dict[str, bool] = {}
    if checks["all_32_slabs_present"]:
        for index in range(32):
            f = arb_forward_slabs[index]
            p = arb_precision_slabs[index]
            r = arb_reverse_slabs[index]
            m = mpfr_slabs[index]
            slab_overlap_checks[str(index)] = all((
                intervals_overlap(f["phi_second_lower"], f["phi_second_upper"],
                                  p["phi_second_lower"], p["phi_second_upper"]),
                intervals_overlap(f["phi_second_lower"], f["phi_second_upper"],
                                  r["phi_second_lower"], r["phi_second_upper"]),
                intervals_overlap(f["phi_second_lower"], f["phi_second_upper"],
                                  m["phi_second_lower"], m["phi_second_upper"]),
                f["below_negative_target"].lower() == "true",
            ))
    checks["all_slab_intervals_overlap"] = bool(slab_overlap_checks) and all(slab_overlap_checks.values())

    # Verify generated-output hashes from each authoritative run.
    hash_checks: dict[str, bool] = {}
    for label in ("forward_384", "forward_512", "reverse_384"):
        directory = result_root / label
        hash_path = directory / "OUTPUT_SHA256.json"
        if not hash_path.is_file():
            hash_checks[label] = False
            continue
        records = load_json(hash_path)
        hash_checks[label] = all(
            (directory / filename).is_file()
            and sha256(directory / filename) == expected
            for filename, expected in records.items()
        )
    checks["all_output_hashes_match"] = all(hash_checks.values())

    passed = all(checks.values())
    report = {
        "audit_version": AUDIT_VERSION,
        "classification": (
            "PEABODY_ARB_FLINT_CERTIFICATE_AUDIT_PASS"
            if passed else "PEABODY_ARB_FLINT_CERTIFICATE_AUDIT_FAIL"
        ),
        "pass": passed,
        "checks": checks,
        "slab_overlap_checks": slab_overlap_checks,
        "output_hash_checks": hash_checks,
        "forward_certificate_sha256": sha256(paths["forward_384"]),
        "mpfr_preflight_certificate_sha256": sha256(paths["mpfr"]),
        "endpoint_lower": forward["endpoint"]["phi_one_enclosure"]["lower"],
        "endpoint_target": forward["endpoint"]["target"],
        "worst_phi_second_upper": forward["concavity"]["worst_phi_second_upper"],
        "concavity_target": forward["concavity"]["target"],
        "proof_authority": "independent python-flint Arb ball-arithmetic replay",
    }
    out = result_root / "arb_certificate_audit.json"
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(report["classification"])
    print("pass:", report["pass"])
    print("endpoint lower:", report["endpoint_lower"])
    print("worst Phi'' upper:", report["worst_phi_second_upper"])
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
