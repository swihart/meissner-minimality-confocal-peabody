#!/usr/bin/env python3
"""Independent numerical and exact audit of the Peabody one-pair formula.

This program deliberately does not import any theorem-package Python module.
It implements four representations from the geometric definitions:

1. the two-dimensional confocal wedge/Gauss integral;
2. the reduced one-dimensional moving-endpoint integral;
3. the fixed beam-coordinate integral;
4. the stable q-chart used by the interval certificates.

It also checks the exact width-two to width-one normalization symbolically.
The quadratures are audit evidence, not proof authority.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import mpmath as mp
import sympy as sp

DEFAULT_DPS = 70
DEFAULT_GL_ORDER_1D = 96
DEFAULT_GL_ORDER_2D = 48
E_VALUES = ("0", "0.01", "0.1", "0.5", "0.9", "0.995")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass(frozen=True)
class Parameters:
    e: mp.mpf
    a: mp.mpf
    b: mp.mpf
    b2: mp.mpf
    theta: mp.mpf
    eta: mp.mpf
    u: mp.mpf
    v: mp.mpf
    y: mp.mpf


def setup_constants() -> dict[str, mp.mpf]:
    sqrt2 = mp.sqrt(2)
    sqrt3 = mp.sqrt(3)
    kappa = 1 + sqrt2
    K = kappa * kappa
    alpha = mp.acos(mp.mpf(1) / 3)
    psi0 = -(2 * mp.pi / sqrt3) * alpha
    meissner = mp.pi * (mp.mpf(2) / 3 - sqrt3 * alpha / 4)
    return {
        "sqrt2": sqrt2,
        "sqrt3": sqrt3,
        "kappa": kappa,
        "K": K,
        "alpha": alpha,
        "psi0": psi0,
        "meissner": meissner,
    }


def parameters(e: mp.mpf, c: dict[str, mp.mpf]) -> Parameters:
    if not (0 <= e < 1):
        raise ValueError(f"e must be in [0,1); got {e}")
    one_minus_e2 = 1 - e * e
    b2 = (3 + 3 * e * e + 4 * c["sqrt2"] * e) / one_minus_e2
    b = mp.sqrt(b2)
    a = b / mp.sqrt(one_minus_e2)
    theta = mp.acos(1 / b)
    eta = mp.asinh(1 / b)
    u = mp.sqrt(1 - 1 / b2)
    v = mp.sqrt(1 + 1 / b2)
    y = 1 / (mp.sqrt(b2 + 1) + b)
    return Parameters(e, a, b, b2, theta, eta, u, v, y)


def gauss_legendre(order: int) -> tuple[list[mp.mpf], list[mp.mpf]]:
    nodes, weights = mp.gauss_quadrature(order, "legendre")
    return [nodes[i] for i in range(order)], [weights[i] for i in range(order)]


def kernel_i(C: mp.mpf, y: mp.mpf) -> mp.mpf:
    return 4 * mp.atan(y * mp.sqrt((1 + C) / (1 - C))) / mp.sqrt(1 - C * C)


def psi_reduced_1d(e: mp.mpf, c: dict[str, mp.mpf], order: int) -> mp.mpf:
    p = parameters(e, c)
    nodes, weights = gauss_legendre(order)
    lower, upper = p.theta, mp.pi / 2
    total = mp.mpf(0)
    for z, w in zip(nodes, weights):
        t = (upper - lower) * z / 2 + (upper + lower) / 2
        sin_t = mp.sin(t)
        C = e * sin_t
        I = kernel_i(C, p.y)
        core = I / p.a + e * (sin_t - p.u) * (
            (p.v * C - 1) * I + 2 / p.b
        ) / (1 - C * C)
        total += w * core
    return -4 * p.b2 * (upper - lower) * total / 2


def h_fixed_original(e: mp.mpf, x: mp.mpf, c: dict[str, mp.mpf]) -> mp.mpf:
    p = parameters(e, c)
    amp = mp.sqrt(1 - x * x / p.b2)
    C = e * amp
    I = kernel_i(C, p.y)
    core = I / p.a + e * (amp - p.u) * (
        (p.v * C - 1) * I + 2 / p.b
    ) / (1 - C * C)
    return -4 * p.b * core / amp


def stable_h(e: mp.mpf, x: mp.mpf, c: dict[str, mp.mpf]) -> mp.mpf:
    q = (1 - e) / (1 + e)
    K = c["K"]
    kappa = c["kappa"]
    sqrt2 = c["sqrt2"]
    D = mp.sqrt(K * K + q * q)
    R = mp.sqrt(K * K + q * q - 2 * K * q * x * x)
    T = mp.sqrt(2 * K * (K * K + q * q) + K * K * (1 - q) ** 2 * x * x)
    delta = 2 * K * (1 - x * x) / (R + K - q)
    M = K * (q - 2 * K * x * x) / (R + K) + (1 - K) * R - K * K - q * R - q - q * q
    primary = -16 * sqrt2 * kappa * (K * K + q * q) / (R * T)
    correction = -4 * K * (1 - q * q) * (K * K + q * q) * delta * M / (R * T**3)
    algebraic = -4 * K * (1 - q * q) * (K * K + q * q) * delta / (R * T * T)
    Z = K * ((1 + q) * D + (1 - q) * R) / (T * (K + q + D))
    return (primary + correction) * mp.atan(Z) + algebraic


def integrate_fixed(function, e: mp.mpf, c: dict[str, mp.mpf], order: int) -> mp.mpf:
    nodes, weights = gauss_legendre(order)
    total = mp.mpf(0)
    for z, w in zip(nodes, weights):
        x = (z + 1) / 2
        total += w * function(e, x, c)
    return total / 2


def psi_2d(e: mp.mpf, c: dict[str, mp.mpf], order: int) -> tuple[mp.mpf, mp.mpf, mp.mpf, mp.mpf, mp.mpf]:
    p = parameters(e, c)
    nodes, weights = gauss_legendre(order)
    area_e = mp.mpf(0)
    area_h = mp.mpf(0)
    omega = mp.mpf(0)
    collapsed = mp.mpf(0)
    for zt, wt in zip(nodes, weights):
        t = (mp.pi - 2 * p.theta) * zt / 2 + mp.pi / 2
        t_weight = (mp.pi - 2 * p.theta) * wt / 2
        sin_t = mp.sin(t)
        for zx, wx in zip(nodes, weights):
            xi = p.eta * zx
            xi_weight = p.eta * wx
            cosh_xi = mp.cosh(xi)
            distance = p.a * (cosh_xi - e * sin_t)
            radius_e = p.a * e * (sin_t - p.u)
            radius_h = p.a * (p.v - cosh_xi)
            gauss_jacobian = p.b2 / (distance * distance)
            weight = t_weight * xi_weight
            area_e += weight * radius_e * (2 - radius_h) * gauss_jacobian
            area_h += weight * radius_h * (2 - radius_e) * gauss_jacobian
            omega += weight * gauss_jacobian
            collapsed += weight * (-2) * (distance + radius_e * radius_h) * gauss_jacobian
    psi = area_e + area_h - 4 * omega
    return psi, collapsed, area_e, area_h, omega


def exact_symbolic_checks() -> dict[str, Any]:
    pi = sp.pi
    alpha = sp.acos(sp.Rational(1, 3))
    psi0, psi1, psi2, psi3 = sp.symbols("psi0 psi1 psi2 psi3")
    surface_width2 = 8 * pi + psi1 + psi2 + psi3
    volume_width2 = sp.simplify(surface_width2 - sp.Rational(8, 3) * pi)
    volume_width1 = sp.simplify(volume_width2 / 8)
    meissner_from_psi0 = sp.simplify(sp.Rational(2, 3) * pi + 3 * psi0 / 8)
    phi_sum = sp.simplify(sum((p - psi0) / 8 for p in (psi1, psi2, psi3)))
    normalization_residual = sp.simplify(volume_width1 - meissner_from_psi0 - phi_sum)
    psi0_exact = -2 * pi * alpha / sp.sqrt(3)
    meissner_exact = pi * (sp.Rational(2, 3) - sp.sqrt(3) * alpha / 4)
    meissner_residual = sp.simplify(meissner_from_psi0.subs(psi0, psi0_exact) - meissner_exact)

    d, re, rh = sp.symbols("d re rh")
    pair_area_raw = re * (2 - rh) + rh * (2 - re) - 4
    pair_area_collapsed = sp.simplify((pair_area_raw + 2 * (d + re * rh)).subs(rh, 2 - d - re))

    return {
        "width2_surface_formula": str(surface_width2),
        "width2_volume_formula": str(volume_width2),
        "width1_volume_formula": str(volume_width1),
        "normalization_residual": str(normalization_residual),
        "normalization_identity_zero": normalization_residual == 0,
        "meissner_recovery_residual": str(meissner_residual),
        "meissner_recovery_identity_zero": meissner_residual == 0,
        "pair_area_collapse_residual": str(pair_area_collapsed),
        "pair_area_collapse_identity_zero": pair_area_collapsed == 0,
    }


def confocal_identity_audit(c: dict[str, mp.mpf]) -> dict[str, str]:
    maximum = mp.mpf(0)
    for e_text in ("0.01", "0.2", "0.6", "0.95"):
        e = mp.mpf(e_text)
        p = parameters(e, c)
        for t_fraction in (mp.mpf("0.2"), mp.mpf("0.5"), mp.mpf("0.8")):
            t = p.theta + t_fraction * (mp.pi - 2 * p.theta)
            for xi_fraction in (mp.mpf("-0.7"), mp.mpf("0"), mp.mpf("0.7")):
                xi = xi_fraction * p.eta
                distance = p.a * (mp.cosh(xi) - e * mp.sin(t))
                radius_e = p.a * e * (mp.sin(t) - p.u)
                radius_h = p.a * (p.v - mp.cosh(xi))
                maximum = max(maximum, abs(distance + radius_e + radius_h - 2))
    return {
        "maximum_confocal_identity_residual": mp.nstr(maximum, 50),
        "pass": maximum < mp.mpf("1e-55"),
    }


def run(repo: Path, output_dir: Path, dps: int, order_1d: int, order_2d: int) -> dict[str, Any]:
    start = time.time()
    mp.mp.dps = dps
    c = setup_constants()
    output_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str]] = []
    maximum_discrepancy = mp.mpf(0)
    for e_text in E_VALUES:
        e = mp.mpf(e_text)
        psi_moving = psi_reduced_1d(e, c, order_1d)
        psi_fixed = integrate_fixed(h_fixed_original, e, c, order_1d)
        psi_stable = integrate_fixed(stable_h, e, c, order_1d)
        psi_two_d, psi_collapsed, area_e, area_h, omega = psi_2d(e, c, order_2d)
        discrepancy = max(
            abs(psi_moving - psi_fixed),
            abs(psi_moving - psi_stable),
            abs(psi_moving - psi_two_d),
            abs(psi_moving - psi_collapsed),
        )
        maximum_discrepancy = max(maximum_discrepancy, discrepancy)
        rows.append(
            {
                "e": e_text,
                "psi_reduced_1d": mp.nstr(psi_moving, dps),
                "psi_fixed_x": mp.nstr(psi_fixed, dps),
                "psi_stable_q": mp.nstr(psi_stable, dps),
                "psi_two_dimensional": mp.nstr(psi_two_d, dps),
                "psi_collapsed_two_dimensional": mp.nstr(psi_collapsed, dps),
                "wedge_elliptic_area": mp.nstr(area_e, dps),
                "wedge_hyperbolic_area": mp.nstr(area_h, dps),
                "gauss_image_area": mp.nstr(omega, dps),
                "maximum_representation_discrepancy": mp.nstr(discrepancy, 50),
            }
        )

    csv_path = output_dir / "independent_one_pair_rederivation.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    symbolic = exact_symbolic_checks()
    confocal = confocal_identity_audit(c)
    psi0_error = abs(mp.mpf(rows[0]["psi_reduced_1d"]) - c["psi0"])
    pass_gate = (
        maximum_discrepancy < mp.mpf("1e-50")
        and psi0_error < mp.mpf("1e-50")
        and symbolic["normalization_identity_zero"]
        and symbolic["meissner_recovery_identity_zero"]
        and symbolic["pair_area_collapse_identity_zero"]
        and confocal["pass"]
    )

    sources = {
        "exact_additivity_note": repo / "frozen_inputs/peabody_exact_additivity_note.md",
        "exact_pair_formula": repo / "frozen_inputs/peabody_exact_pair_formula.py",
        "phi_mathematica": repo / "frozen_inputs/peabody_phi_monotonicity.wl",
    }
    result = {
        "classification": (
            "PEABODY_INDEPENDENT_ONE_PAIR_REDERIVATION_PASS"
            if pass_gate
            else "PEABODY_INDEPENDENT_ONE_PAIR_REDERIVATION_FAIL"
        ),
        "pass": pass_gate,
        "scope": "width-one regular-tetrahedron confocal Peabodies only",
        "python_version": sys.version,
        "platform": platform.platform(),
        "mpmath_version": mp.__version__,
        "sympy_version": sp.__version__,
        "precision_decimal_digits": dps,
        "gauss_legendre_order_1d": order_1d,
        "gauss_legendre_order_2d": order_2d,
        "maximum_representation_discrepancy": mp.nstr(maximum_discrepancy, 50),
        "psi0_recovery_error": mp.nstr(psi0_error, 50),
        "exact_symbolic_checks": symbolic,
        "confocal_identity_audit": confocal,
        "rows_csv": csv_path.name,
        "source_hashes": {
            key: sha256(path) for key, path in sources.items() if path.is_file()
        },
        "elapsed_seconds": time.time() - start,
        "proof_role": "independent formula audit; numerical quadrature is not proof authority",
    }
    json_path = output_dir / "independent_one_pair_rederivation.json"
    json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--precision-dps", type=int, default=DEFAULT_DPS)
    parser.add_argument("--order-1d", type=int, default=DEFAULT_GL_ORDER_1D)
    parser.add_argument("--order-2d", type=int, default=DEFAULT_GL_ORDER_2D)
    args = parser.parse_args()
    result = run(
        args.repo_root.resolve(),
        args.output_dir.resolve(),
        args.precision_dps,
        args.order_1d,
        args.order_2d,
    )
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
