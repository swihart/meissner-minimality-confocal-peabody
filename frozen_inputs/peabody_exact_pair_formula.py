#!/usr/bin/env python3
"""Exact one-pair surface/volume formula for regular-tetrahedron Peabodies.

This module implements the theorem-architecture reduction

    V_1(e1,e2,e3) = V_M + Phi(e1) + Phi(e2) + Phi(e3),

where V_1 denotes width-one volume, V_M is the exact Meissner volume, and
Phi(e) = (Psi(e)-Psi(0))/8.  The scalar Psi can be evaluated either by the
original two-dimensional confocal integral or by an analytically reduced
one-dimensional integral.

The derivation is documented in ``peabody_exact_additivity_note.md``.
Only NumPy and the Python standard library are required.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
from numpy.polynomial.legendre import leggauss

SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)
SQRT6 = math.sqrt(6.0)
ALPHA = math.acos(1.0 / 3.0)
MEISSNER_WIDTH1 = math.pi * (2.0 / 3.0 - SQRT3 * ALPHA / 4.0)


@dataclass(frozen=True)
class ConfocalParameters:
    """Parameters for the elliptic-hyperbolic Peabody chart."""

    e: float
    a: float
    b: float
    c: float
    theta: float
    eta: float
    u: float
    v: float
    y: float


@dataclass(frozen=True)
class PairIntegral:
    """Two-dimensional decomposition of one opposite-edge pair."""

    e: float
    wedge_elliptic_area: float
    wedge_hyperbolic_area: float
    gauss_image_area: float
    psi: float
    psi_collapsed: float


@dataclass(frozen=True)
class LocalIdentityAudit:
    """Maximum residuals in the local differential identities."""

    samples: int
    unit_normal_max_abs: float
    orthogonality_max_abs: float
    conformal_scale_max_rel: float
    elliptic_area_max_rel: float
    hyperbolic_area_max_rel: float


def confocal_parameters(e: float) -> ConfocalParameters:
    """Return the exact-chart parameters for 0 <= e < 1.

    The formulas are algebraic consequences of the regular tetrahedral beam
    constraints.  ``e`` is the eccentricity c/a.
    """

    if not math.isfinite(e) or not (0.0 <= e < 1.0):
        raise ValueError(f"e must satisfy 0 <= e < 1; received {e!r}")

    one_minus_e2 = 1.0 - e * e
    numerator = 3.0 + 3.0 * e * e + 4.0 * SQRT2 * e
    b2 = numerator / one_minus_e2
    b = math.sqrt(b2)
    a = b / math.sqrt(one_minus_e2)
    c = e * a
    theta = math.acos(1.0 / b)
    eta = math.asinh(1.0 / b)
    u = math.sin(theta)
    v = math.cosh(eta)
    y = math.tanh(eta / 2.0)
    return ConfocalParameters(e=e, a=a, b=b, c=c, theta=theta, eta=eta, u=u, v=v, y=y)


def psi_meissner_exact() -> float:
    """Return Psi(0) in exact closed form, evaluated in binary64."""

    return -(2.0 * math.pi / SQRT3) * ALPHA


def endpoint_phi_derivative_exact() -> float:
    """Return the exact right derivative Phi'(0), evaluated in binary64.

    The exact expression is

      1/2 * [5*pi/(3*sqrt(3)) - 3
             + acos(1/3)*(3*sqrt(2)/2 - 5*sqrt(6)*pi/18)].
    """

    bracket = (
        5.0 * math.pi / (3.0 * SQRT3)
        - 3.0
        + ALPHA * (3.0 * SQRT2 / 2.0 - 5.0 * SQRT6 * math.pi / 18.0)
    )
    return 0.5 * bracket


def _kernel_i(c_value: np.ndarray, y: float) -> np.ndarray:
    """Evaluate I(C)=int_{-eta}^{eta} dxi/(cosh(xi)-C)."""

    c_value = np.asarray(c_value, dtype=float)
    q = np.sqrt(np.maximum(0.0, 1.0 - c_value * c_value))
    z = y * np.sqrt((1.0 + c_value) / (1.0 - c_value))
    return 4.0 * np.arctan(z) / q


def psi_1d(e: float, order: int = 480) -> float:
    """Evaluate Psi(e) using the exact one-dimensional reduction.

    Gauss-Legendre quadrature is applied only to a smooth one-dimensional
    integral.  Increasing ``order`` gives a reproducible convergence audit.
    """

    if order < 16:
        raise ValueError("order must be at least 16")
    p = confocal_parameters(e)
    nodes, weights = leggauss(order)
    half_length = 0.5 * (math.pi / 2.0 - p.theta)
    midpoint = 0.5 * (math.pi / 2.0 + p.theta)
    t = half_length * nodes + midpoint
    wt = half_length * weights

    a_sin = np.sin(t)
    c_value = e * a_sin
    i_value = _kernel_i(c_value, p.y)
    denominator = 1.0 - c_value * c_value

    # This is the simplified form of
    # I/a + e(A-u)[(v-C)I'(C)-I(C)].
    integrand = i_value / p.a + e * (a_sin - p.u) * (
        (p.v * c_value - 1.0) * i_value + 2.0 / p.b
    ) / denominator

    return float(-4.0 * p.b * p.b * np.dot(wt, integrand))


def pair_integral_2d(e: float, order: int = 260) -> PairIntegral:
    """Evaluate the original two-dimensional local pair integral.

    Coordinates are s=b cos(t) and r=b sinh(xi).  The two wedge areas and
    the common Gauss-image area are returned separately.  The identity

      Psi = A_E + A_H - 4 Omega
          = -2 int (d + R_E R_H) dOmega

    supplies an internal independent check.
    """

    if order < 16:
        raise ValueError("order must be at least 16")
    p = confocal_parameters(e)
    nodes, weights = leggauss(order)

    t_half = 0.5 * (math.pi - 2.0 * p.theta)
    t = t_half * nodes + math.pi / 2.0
    wt = t_half * weights
    xi = p.eta * nodes
    wx = p.eta * weights

    a_sin = np.sin(t)[:, None]
    b_cosh = np.cosh(xi)[None, :]
    d = p.a * (b_cosh - e * a_sin)
    r_e = p.a * e * (a_sin - p.u)
    r_h = p.a * (p.v - b_cosh)
    gauss_jacobian = p.b * p.b / (d * d)
    quadrature = wt[:, None] * wx[None, :]

    area_e = float(np.sum(quadrature * r_e * (2.0 - r_h) * gauss_jacobian))
    area_h = float(np.sum(quadrature * r_h * (2.0 - r_e) * gauss_jacobian))
    omega = float(np.sum(quadrature * gauss_jacobian))
    psi = area_e + area_h - 4.0 * omega
    psi_collapsed = float(
        np.sum(quadrature * (-2.0) * (d + r_e * r_h) * gauss_jacobian)
    )
    return PairIntegral(
        e=e,
        wedge_elliptic_area=area_e,
        wedge_hyperbolic_area=area_h,
        gauss_image_area=omega,
        psi=psi,
        psi_collapsed=psi_collapsed,
    )


def phi(e: float, order: int = 480) -> float:
    """Return the width-one volume increment contributed by one edge pair."""

    return (psi_1d(e, order=order) - psi_meissner_exact()) / 8.0


def volume_width1(e_values: Sequence[float], order: int = 480) -> float:
    """Return the exact-formula width-one volume for three pair parameters."""

    if len(e_values) != 3:
        raise ValueError("exactly three Peabody pair parameters are required")
    return MEISSNER_WIDTH1 + sum(phi(float(e), order=order) for e in e_values)


def _canonical_local_fields(e: float, t: float, xi: float) -> tuple[np.ndarray, ...]:
    """Return X,Y,n,U_E,U_H and scalar fields in a translation-free frame."""

    p = confocal_parameters(e)
    x = np.array([p.a * math.sin(t), p.b * math.cos(t), 0.0], dtype=float)
    y = np.array([p.a * e * math.cosh(xi), 0.0, p.b * math.sinh(xi)], dtype=float)
    diff = x - y
    d = float(np.linalg.norm(diff))
    n = diff / d
    r_e = p.a * e * (math.sin(t) - p.u)
    r_h = p.a * (p.v - math.cosh(xi))
    u_e = x + r_e * n
    u_h = y - r_h * n
    return x, y, n, u_e, u_h, np.array([d, r_e, r_h], dtype=float)


def audit_local_differential_identities(
    samples: int = 160,
    seed: int = 20260929,
    step: float = 2.0e-6,
) -> LocalIdentityAudit:
    """Numerically stress-test the differential identities behind the formula."""

    if samples < 1:
        raise ValueError("samples must be positive")
    rng = np.random.default_rng(seed)
    unit_err = 0.0
    orth_err = 0.0
    scale_err = 0.0
    area_e_err = 0.0
    area_h_err = 0.0

    for _ in range(samples):
        e = float(rng.uniform(1.0e-3, 0.985))
        p = confocal_parameters(e)
        # Stay away from the degenerate boundary when taking finite differences.
        t = float(rng.uniform(p.theta + 0.08 * (math.pi / 2.0 - p.theta),
                              math.pi - p.theta - 0.08 * (math.pi / 2.0 - p.theta)))
        xi = float(rng.uniform(-0.84 * p.eta, 0.84 * p.eta))

        _, _, n0, ue0, uh0, scalars = _canonical_local_fields(e, t, xi)
        d, r_e, r_h = map(float, scalars)
        _, _, ntp, uetp, uhtp, _ = _canonical_local_fields(e, t + step, xi)
        _, _, ntm, uetm, uhtm, _ = _canonical_local_fields(e, t - step, xi)
        _, _, nxp, uexp, uhxp, _ = _canonical_local_fields(e, t, xi + step)
        _, _, nxm, uexm, uhxm, _ = _canonical_local_fields(e, t, xi - step)

        n_t = (ntp - ntm) / (2.0 * step)
        n_x = (nxp - nxm) / (2.0 * step)
        ue_t = (uetp - uetm) / (2.0 * step)
        ue_x = (uexp - uexm) / (2.0 * step)
        uh_t = (uhtp - uhtm) / (2.0 * step)
        uh_x = (uhxp - uhxm) / (2.0 * step)

        expected_scale = p.b / d
        norm_t = float(np.linalg.norm(n_t))
        norm_x = float(np.linalg.norm(n_x))
        unit_err = max(unit_err, abs(float(np.dot(n0, n0)) - 1.0))
        orth_err = max(orth_err, abs(float(np.dot(n_t, n_x))))
        scale_err = max(
            scale_err,
            abs(norm_t - expected_scale) / expected_scale,
            abs(norm_x - expected_scale) / expected_scale,
        )

        expected_e = r_e * (2.0 - r_h) * expected_scale * expected_scale
        expected_h = r_h * (2.0 - r_e) * expected_scale * expected_scale
        observed_e = float(np.linalg.norm(np.cross(ue_t, ue_x)))
        observed_h = float(np.linalg.norm(np.cross(uh_t, uh_x)))
        area_e_err = max(area_e_err, abs(observed_e - expected_e) / max(1.0e-14, expected_e))
        area_h_err = max(area_h_err, abs(observed_h - expected_h) / max(1.0e-14, expected_h))

    return LocalIdentityAudit(
        samples=samples,
        unit_normal_max_abs=unit_err,
        orthogonality_max_abs=orth_err,
        conformal_scale_max_rel=scale_err,
        elliptic_area_max_rel=area_e_err,
        hyperbolic_area_max_rel=area_h_err,
    )


def derivative_scan(e_values: Iterable[float], order: int = 520) -> list[dict[str, float]]:
    """Return a reproducible finite-difference scan of Phi'(e)."""

    rows: list[dict[str, float]] = []
    for raw_e in e_values:
        e = float(raw_e)
        if e == 0.0:
            derivative = endpoint_phi_derivative_exact()
            method = "exact_endpoint"
            step = 0.0
        else:
            step = min(2.0e-5, max(2.0e-8, (1.0 - e) / 40.0), e / 4.0)
            # Five-point centered stencil.
            fm2 = phi(e - 2.0 * step, order=order)
            fm1 = phi(e - step, order=order)
            fp1 = phi(e + step, order=order)
            fp2 = phi(e + 2.0 * step, order=order)
            derivative = (fm2 - 8.0 * fm1 + 8.0 * fp1 - fp2) / (12.0 * step)
            method = "five_point"
        rows.append(
            {
                "e": e,
                "phi": phi(e, order=order),
                "phi_derivative": derivative,
                "step": step,
                "method": method,
            }
        )
    return rows


def build_validation_rows(
    e_values: Sequence[float],
    order_1d: int = 520,
    order_2d: int = 280,
) -> list[dict[str, float]]:
    """Compare the one- and two-dimensional exact formulas."""

    rows: list[dict[str, float]] = []
    psi0 = psi_meissner_exact()
    for raw_e in e_values:
        e = float(raw_e)
        one = psi_1d(e, order=order_1d)
        two = pair_integral_2d(e, order=order_2d)
        pair_phi = (one - psi0) / 8.0
        rows.append(
            {
                "e": e,
                "psi_1d": one,
                "psi_2d": two.psi,
                "psi_collapsed_2d": two.psi_collapsed,
                "abs_1d_minus_2d": abs(one - two.psi),
                "abs_2d_internal": abs(two.psi - two.psi_collapsed),
                "phi_width1": pair_phi,
                "one_pair_volume_width1": MEISSNER_WIDTH1 + pair_phi,
                "symmetric_volume_width1": MEISSNER_WIDTH1 + 3.0 * pair_phi,
                "gauss_image_area": two.gauss_image_area,
                "wedge_elliptic_area": two.wedge_elliptic_area,
                "wedge_hyperbolic_area": two.wedge_hyperbolic_area,
            }
        )
    return rows


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError("cannot write an empty CSV")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def run_validation(output_dir: Path) -> dict[str, object]:
    """Run the complete reproducible audit and write machine-readable outputs."""

    output_dir.mkdir(parents=True, exist_ok=True)
    e_values = (0.0, 1.0e-4, 1.0e-2, 0.1, 0.5, 0.9, 0.98, 0.999)
    validation = build_validation_rows(e_values)
    derivative = derivative_scan((0.0, 0.001, 0.01, 0.1, 0.2, 0.4, 0.6, 0.8, 0.9, 0.98, 0.995))
    local_audit = audit_local_differential_identities()

    max_1d_2d = max(float(row["abs_1d_minus_2d"]) for row in validation)
    max_internal = max(float(row["abs_2d_internal"]) for row in validation)
    meissner_reconstruction = 2.0 * math.pi / 3.0 + 3.0 * psi_1d(0.0) / 8.0
    meissner_error = abs(meissner_reconstruction - MEISSNER_WIDTH1)
    min_derivative = min(float(row["phi_derivative"]) for row in derivative)

    # Numerical validation gates.  They certify the implementation, not the theorem.
    assert max_1d_2d < 2.0e-10, max_1d_2d
    assert max_internal < 2.0e-11, max_internal
    assert meissner_error < 2.0e-13, meissner_error
    assert min_derivative > 0.0, min_derivative
    assert local_audit.conformal_scale_max_rel < 2.0e-8
    assert local_audit.elliptic_area_max_rel < 3.0e-8
    assert local_audit.hyperbolic_area_max_rel < 3.0e-8

    _write_csv(output_dir / "exact_formula_validation.csv", validation)
    _write_csv(output_dir / "exact_formula_derivative_scan.csv", derivative)

    summary: dict[str, object] = {
        "classification": "GO_PEABODY_EXACT_ADDITIVITY_REDUCTION",
        "normalization": "regular tetrahedron side 2, Peabody width 2; reported volumes width 1",
        "meissner_width1": MEISSNER_WIDTH1,
        "psi0_exact_numeric": psi_meissner_exact(),
        "phi_prime_zero_exact_numeric": endpoint_phi_derivative_exact(),
        "max_abs_psi_1d_minus_2d": max_1d_2d,
        "max_abs_psi_2d_internal_identity": max_internal,
        "meissner_reconstruction_error": meissner_error,
        "minimum_sampled_phi_derivative": min_derivative,
        "local_differential_identity_audit": asdict(local_audit),
        "claims": {
            "exact_additivity": "proposed theorem with complete derivation in accompanying note",
            "orientation_independence": "proposed theorem by tetrahedral congruence",
            "global_scalar_monotonicity": "not proved; positive numerical derivative scan only",
            "below_meissner_candidate": False,
            "universal_lower_bound_change": False,
        },
    }
    with (output_dir / "exact_additivity_flight_recorder.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="directory for CSV and JSON audit outputs",
    )
    args = parser.parse_args()
    summary = run_validation(args.output_dir)
    print(json.dumps(summary, indent=2, sort_keys=True))
    print(summary["classification"])


if __name__ == "__main__":
    main()
