#!/usr/bin/env python3
"""Independent semantic and adversarial audit of the Peabody concavity certificate.

This script does not import the principal certifier.  It reimplements the stable
q-chart with ordinary high-precision mpmath arithmetic, checks the endpoint
formula, numerically differentiates the integral, verifies certificate coverage,
compares the 80/100-digit and reverse-order replays, and confirms that the two
archived adversarial controls fail.

The high-precision calculations here are audit evidence, not proof authority.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath as mp

AUDIT_VERSION = "PEABODY_ANALYTIC_COMPRESSION_AUDIT_V1"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_fraction(text: str) -> Fraction:
    if "/" in text:
        n, d = text.split("/", 1)
        return Fraction(int(n), int(d))
    return Fraction(int(text), 1)


def stable_h(q: mp.mpf, x: mp.mpf) -> mp.mpf:
    sqrt2 = mp.sqrt(2)
    kappa = 1 + sqrt2
    K = kappa * kappa
    D = mp.sqrt(K * K + q * q)
    R = mp.sqrt(K * K + q * q - 2 * K * q * x * x)
    T = mp.sqrt(2 * K * (K * K + q * q) + K * K * (1 - q)**2 * x * x)
    delta = 2 * K * (1 - x * x) / (R + K - q)
    M = K * (q - 2 * K * x * x) / (R + K) + (1 - K) * R \
        - K * K - q * R - q - q * q
    primary = -16 * sqrt2 * kappa * (K * K + q * q) / (R * T)
    correction = -4 * K * (1 - q * q) * (K * K + q * q) \
        * delta * M / (R * T**3)
    algebraic = -4 * K * (1 - q * q) * (K * K + q * q) \
        * delta / (R * T**2)
    Z = K * ((1 + q) * D + (1 - q) * R) / (T * (K + q + D))
    return (primary + correction) * mp.atan(Z) + algebraic


def endpoint_h_explicit(x: mp.mpf) -> mp.mpf:
    sqrt2 = mp.sqrt(2)
    kappa = 1 + sqrt2
    K = kappa * kappa
    A = 2 * K + x * x
    coefficient = -16 * sqrt2 * kappa / mp.sqrt(A) \
        + 4 * (1 - x * x) * (A - 1) / A**mp.mpf("1.5")
    return coefficient * mp.atan(1 / mp.sqrt(A)) - 4 * (1 - x * x) / A


def psi0_exact() -> mp.mpf:
    return -(2 * mp.pi / mp.sqrt(3)) * mp.acos(mp.mpf(1) / 3)


def psi_q(q: mp.mpf) -> mp.mpf:
    return mp.quad(lambda x: stable_h(q, x), [0, 1])


def phi_e(e: mp.mpf) -> mp.mpf:
    q = (1 - e) / (1 + e)
    return (psi_q(q) - psi0_exact()) / 8


def interval_contains(record: dict[str, str], value: mp.mpf) -> bool:
    return mp.mpf(record["lower"]) <= value <= mp.mpf(record["upper"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    mp.mp.dps = 100
    package = args.package_dir
    canonical_path = package / "data/certificate_80dps/peabody_concavity_certificate.json"
    high_path = package / "data/certificate_100dps/peabody_concavity_certificate.json"
    reverse_path = package / "data/certificate_reverse_80dps/peabody_concavity_certificate.json"
    under_path = package / "data/control_underresolved_16/peabody_concavity_certificate.json"
    mutation_path = package / "data/control_correction_sign/peabody_concavity_certificate.json"

    canonical = json.loads(canonical_path.read_text())
    high = json.loads(high_path.read_text())
    reverse = json.loads(reverse_path.read_text())
    under = json.loads(under_path.read_text())
    mutation = json.loads(mutation_path.read_text())

    checks: dict[str, Any] = {}
    checks["canonical_pass"] = canonical["proof_status"] == "CERTIFIED"
    checks["box_count"] = canonical["terminal_boxes"] == 324
    checks["endpoint_target"] = canonical["endpoint"]["exceeds_target"] is True
    checks["concavity_target"] = canonical["concavity"]["all_slabs_below_target"] is True
    checks["hard_stop"] = canonical["hard_stop_pass"] is True

    slabs = canonical["concavity"]["slabs"]
    exact_coverage = len(slabs) == 32
    for index, slab in enumerate(slabs):
        exact_coverage = exact_coverage and parse_fraction(slab["q_lo"]) == Fraction(index, 32)
        exact_coverage = exact_coverage and parse_fraction(slab["q_hi"]) == Fraction(index + 1, 32)
        exact_coverage = exact_coverage and slab["below_negative_target"] is True
    checks["exact_partition_coverage"] = exact_coverage

    # Endpoint formula: compare general q=0 form with a separately simplified form.
    endpoint_samples = [mp.mpf(k) / 20 for k in range(21)]
    endpoint_formula_error = max(abs(stable_h(mp.mpf(0), x) - endpoint_h_explicit(x))
                                 for x in endpoint_samples)
    checks["endpoint_formula_match"] = endpoint_formula_error < mp.mpf("1e-90")

    phi_one = (psi_q(mp.mpf(0)) - psi0_exact()) / 8
    checks["endpoint_high_precision_inside_certificate"] = interval_contains(
        canonical["endpoint"]["phi_one_enclosure"], phi_one)
    checks["endpoint_high_precision_above_target"] = phi_one > mp.mpf(3) / 10000

    # Independent numerical differentiation at representatives of selected slabs.
    selected_indices = [0, 1, 3, 7, 15, 23, 31]
    derivative_rows: list[dict[str, str | int | bool]] = []
    derivative_checks = True
    chain_rule_checks = True
    scalar_bound_checks = True
    for index in selected_indices:
        q = mp.mpf(2 * index + 1) / 64
        e = (1 - q) / (1 + q)
        phi_second = mp.diff(phi_e, e, 2, addprec=35)
        slab = slabs[index]
        contained = interval_contains(slab["phi_second"], phi_second)
        derivative_checks = derivative_checks and contained and phi_second < -mp.mpf(1) / 25000

        psi_first = mp.diff(psi_q, q, 1, addprec=35)
        psi_second = mp.diff(psi_q, q, 2, addprec=35)
        chain_value = (1 + q)**3 / 32 * ((1 + q) * psi_second + 2 * psi_first)
        chain_error = abs(chain_value - phi_second)
        chain_ok = chain_error < mp.mpf("1e-70")
        chain_rule_checks = chain_rule_checks and chain_ok

        value = phi_e(e)
        scalar_ok = value > 3 * e / 10000
        scalar_bound_checks = scalar_bound_checks and scalar_ok
        derivative_rows.append({
            "slab_index": index,
            "q": mp.nstr(q, 40),
            "e": mp.nstr(e, 40),
            "phi": mp.nstr(value, 50),
            "phi_second": mp.nstr(phi_second, 50),
            "chain_error": mp.nstr(chain_error, 8),
            "inside_certificate": contained,
            "scalar_bound_pass": scalar_ok,
        })
    checks["sampled_second_derivatives_inside_certificate"] = derivative_checks
    checks["chain_rule_identity_numeric"] = chain_rule_checks
    checks["sampled_global_chord_bound"] = scalar_bound_checks

    # Precision and order stability.
    checks["precision_replay_same_classification"] = (
        high["classification"] == canonical["classification"]
        and high["proof_status"] == canonical["proof_status"]
    )
    checks["reverse_replay_same_classification"] = (
        reverse["classification"] == canonical["classification"]
        and reverse["proof_status"] == canonical["proof_status"]
    )
    checks["stable_leading_endpoint_digits"] = (
        high["endpoint"]["phi_one_enclosure"]["lower"][:55]
        == canonical["endpoint"]["phi_one_enclosure"]["lower"][:55]
    )
    checks["stable_leading_concavity_digits"] = (
        high["concavity"]["worst_phi_second_upper"][:55]
        == canonical["concavity"]["worst_phi_second_upper"][:55]
    )

    # Adversarial controls must fail.
    checks["underresolved_partition_rejected"] = under["proof_status"] == "NOT_CERTIFIED"
    checks["correction_sign_mutation_rejected"] = mutation["proof_status"] == "NOT_CERTIFIED"

    # CSV row counts and rational panel metadata.
    concavity_csv = package / "data/certificate_80dps/concavity_terminal_boxes.csv"
    endpoint_csv = package / "data/certificate_80dps/endpoint_terminal_boxes.csv"
    with concavity_csv.open(newline="", encoding="utf-8") as stream:
        concavity_rows = list(csv.DictReader(stream))
    with endpoint_csv.open(newline="", encoding="utf-8") as stream:
        endpoint_rows = list(csv.DictReader(stream))
    checks["terminal_box_metadata"] = len(concavity_rows) == 320 and len(endpoint_rows) == 4

    passed = all(bool(value) for value in checks.values())
    result = {
        "audit_version": AUDIT_VERSION,
        "classification": "PEABODY_ANALYTIC_COMPRESSION_AUDIT_PASS" if passed
                          else "PEABODY_ANALYTIC_COMPRESSION_AUDIT_FAIL",
        "pass": passed,
        "python_version": sys.version,
        "platform": platform.platform(),
        "mpmath_version": mp.__version__,
        "checks": checks,
        "endpoint_formula_max_error": mp.nstr(endpoint_formula_error, 25),
        "phi_one_high_precision": mp.nstr(phi_one, 80),
        "sampled_derivatives": derivative_rows,
        "source_hashes": {
            str(path.relative_to(package)): sha256(path)
            for path in [canonical_path, high_path, reverse_path, under_path,
                         mutation_path, concavity_csv, endpoint_csv]
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
