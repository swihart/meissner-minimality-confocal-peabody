#!/usr/bin/env python3
"""Independent exact audit for DCG Reviewer Points 1 and 3.

This script does not import any Peabody certifier.  It checks the algebraic
identities used in the full-parameter device construction and in the passage
from the fixed one-pair integral to the stable q-chart.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def zero(expr: sp.Expr) -> str:
    return str(sp.factor(sp.cancel(sp.together(expr))))


def reduce_radical(expr: sp.Expr, var: sp.Symbol, relation: sp.Expr) -> str:
    num = sp.together(expr).as_numer_denom()[0]
    rem = sp.Poly(sp.expand(num), var).rem(sp.Poly(sp.expand(relation), var)).as_expr()
    return str(sp.factor(rem))


def main(output: Path) -> None:
    rt2 = sp.sqrt(2)
    rt3 = sp.sqrt(3)
    e = sp.symbols("e", real=True)
    q, x = sp.symbols("q x", positive=True)
    A, H = sp.symbols("A H", real=True)
    R, D, T = sp.symbols("R D T", positive=True)
    K = 3 + 2 * rt2

    B = (3 + 3 * e**2 + 4 * rt2 * e) / (1 - e**2)

    checks: dict[str, str] = {}

    # Regular-beam and principal-circle data.
    checks["B_plus_one"] = zero(B + 1 - 2 * (e + rt2) ** 2 / (1 - e**2))
    checks["B_minus_one"] = zero(B - 1 - 2 * (rt2 * e + 1) ** 2 / (1 - e**2))
    checks["u0_squared_minus_e_squared"] = zero(
        (B - 1) / B - e**2 - (2 + 3 * e**2 + 4 * rt2 * e) / B
    )
    checks["one_minus_e2v0_squared"] = zero(
        1 - e**2 * (B + 1) / B - (3 + 2 * e**2 + 4 * rt2 * e) / B
    )
    checks["center_distance_square"] = zero(
        (A - e * H) ** 2
        + (1 - e**2) * ((1 - A**2) + (H**2 - 1))
        - (H - e * A) ** 2
    )
    checks["ellipse_principal_focus_distance"] = zero(
        (A - e) ** 2 + (1 - e**2) * (1 - A**2) - (1 - e * A) ** 2
    )
    checks["hyperbola_principal_focus_distance"] = zero(
        (e * H - 1) ** 2 + (1 - e**2) * (H**2 - 1) - (H - e) ** 2
    )

    # Exact endpoint formula at e=0.
    checks["tan_pi_over_12"] = zero(sp.tan(sp.pi / 12) - (2 - rt3))
    checks["meissner_half_angle"] = zero(
        1 - 2 * (sp.Rational(1, 3)) - sp.Rational(1, 3)
    )

    # Stable q-chart.
    e_q = (1 - q) / (1 + q)
    D2 = K**2 + q**2
    R2 = D2 - 2 * K * q * x**2
    T2 = 2 * K * D2 + K**2 * (1 - q) ** 2 * x**2
    Rrel = R**2 - R2
    Drel = D**2 - D2
    Trel = T**2 - T2

    Bq = sp.factor(B.subs(e, e_q))
    checks["b2_q_chart"] = zero(Bq - D2 / (2 * K * q))
    Aq2 = sp.factor(Bq / (1 - e_q**2))
    checks["a2_q_chart"] = zero(Aq2 - D2 * (1 + q) ** 2 / (8 * K * q**2))
    checks["A_squared_q_chart"] = zero(
        1 - x**2 / Bq - R2 / D2
    )
    checks["u0_squared_q_chart"] = zero(
        (Bq - 1) / Bq - (K - q) ** 2 / D2
    )
    checks["v0_squared_q_chart"] = zero(
        (Bq + 1) / Bq - (K + q) ** 2 / D2
    )

    Cq = (1 - q) * R / ((1 + q) * D)
    # Reduce the stable identity successively by the defining radical relations.
    expr = sp.together(
        1 - Cq**2 - 2 * q * T**2 / (K * (1 + q) ** 2 * D**2)
    ).as_numer_denom()[0]
    expr = sp.Poly(sp.expand(expr), T).rem(sp.Poly(sp.expand(Trel), T)).as_expr()
    expr = sp.Poly(sp.expand(expr), D).rem(sp.Poly(sp.expand(Drel), D)).as_expr()
    expr = sp.Poly(sp.expand(expr), R).rem(sp.Poly(sp.expand(Rrel), R)).as_expr()
    checks["one_minus_C_squared_full_remainder"] = str(sp.factor(expr))

    Aplus = (1 + q) * D + (1 - q) * R
    Aminus = (1 + q) * D - (1 - q) * R
    expr = sp.expand(Aplus * Aminus - 2 * q * T**2 / K)
    expr = sp.Poly(expr, T).rem(sp.Poly(sp.expand(Trel), T)).as_expr()
    expr = sp.Poly(sp.expand(expr), D).rem(sp.Poly(sp.expand(Drel), D)).as_expr()
    expr = sp.Poly(sp.expand(expr), R).rem(sp.Poly(sp.expand(Rrel), R)).as_expr()
    checks["angle_product_identity"] = str(sp.factor(expr))

    delta = 2 * K * (1 - x**2) / (R + K - q)
    checks["delta_rationalization"] = reduce_radical(
        (R - K + q) / q - delta, R, Rrel
    )

    M = (
        K * (q - 2 * K * x**2) / (R + K)
        + (1 - K) * R
        - K**2
        - q * R
        - q
        - q**2
    )
    M_unstable = ((1 - q) * (K + q) * R - (1 + q) * D2) / q
    checks["M_rationalization"] = reduce_radical(M_unstable - M, R, Rrel)

    # Stable arctangent argument, checked after positive cross multiplication.
    Z = K * Aplus / (T * (K + q + D))
    y2 = 2 * K * q / (K + q + D) ** 2
    ratio = Aplus / Aminus
    expr = sp.together(Z**2 - y2 * ratio).as_numer_denom()[0]
    expr = sp.Poly(sp.expand(expr), T).rem(sp.Poly(sp.expand(Trel), T)).as_expr()
    expr = sp.Poly(sp.expand(expr), D).rem(sp.Poly(sp.expand(Drel), D)).as_expr()
    expr = sp.Poly(sp.expand(expr), R).rem(sp.Poly(sp.expand(Rrel), R)).as_expr()
    checks["stable_angle_argument_squared"] = str(sp.factor(expr))

    # Derive the stable coefficients from the fixed-interval factors.
    sqrtK = 1 + rt2
    sqrtq = sp.sqrt(q)
    bq = D / (rt2 * sqrtK * sqrtq)
    A_q = R / D
    inv_a = 2 * rt2 * sqrtK * q / ((1 + q) * D)
    I_coeff = 4 * (1 + q) * D * sqrtK / (rt2 * sqrtq * T)
    prefactor = -4 * bq / A_q
    P1_direct = sp.factor(prefactor * inv_a * I_coeff)
    P1_target = -16 * rt2 * (1 + rt2) * D2 / (R * T)
    expr = sp.together(P1_direct - P1_target).as_numer_denom()[0]
    expr = sp.Poly(sp.expand(expr), D).rem(sp.Poly(sp.expand(Drel), D)).as_expr()
    checks["P1_derivation"] = str(sp.factor(expr))

    ratio_factor = K * (1 - q**2) * D * delta / (2 * T**2)
    bracket_atan = 4 * sqrtK * sqrtq * M / (rt2 * D * T)
    bracket_alg = 4 * sqrtK * sqrtq / (rt2 * D)
    P2_direct = sp.factor(prefactor * ratio_factor * bracket_atan)
    Q0_direct = sp.factor(prefactor * ratio_factor * bracket_alg)
    P2_target = -4 * K * (1 - q**2) * D2 * delta * M / (R * T**3)
    Q0_target = -4 * K * (1 - q**2) * D2 * delta / (R * T**2)
    expr = sp.together(P2_direct - P2_target).as_numer_denom()[0]
    expr = sp.Poly(sp.expand(expr), D).rem(sp.Poly(sp.expand(Drel), D)).as_expr()
    checks["P2_derivation"] = str(sp.factor(expr))
    expr = sp.together(Q0_direct - Q0_target).as_numer_denom()[0]
    expr = sp.Poly(sp.expand(expr), D).rem(sp.Poly(sp.expand(Drel), D)).as_expr()
    checks["Q0_derivation"] = str(sp.factor(expr))

    passed = all(value == "0" for value in checks.values())
    result = {
        "classification": (
            "PEABODY_DCG_POINTS_1_3_EXACT_IDENTITY_AUDIT_PASS"
            if passed
            else "PEABODY_DCG_POINTS_1_3_EXACT_IDENTITY_AUDIT_FAIL"
        ),
        "pass": passed,
        "checks": checks,
        "non_symbolic_proof_obligations": [
            "positivity and ordering used to choose principal circles",
            "source Theorem 4.5 applies independently on the three edge pairs",
            "strict-convexity normal partition and seam-nullity argument",
            "closed-cap identification in cap-cone duality",
            "continuity through the e=0 singular-arc degeneration",
            "positive-quantity branch selection for 0<q<=1 and analytic continuation at q=0",
        ],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    main(args.output)
