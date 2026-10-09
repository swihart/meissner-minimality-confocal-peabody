#!/usr/bin/env python3
"""Independent Arb/FLINT certificate for the confocal Peabody scalar.

This file deliberately does not import any principal Peabody certifier.  It
reconstructs the stable q-chart and the required automatic-differentiation
jets directly with python-flint's :class:`flint.arb` real balls.

The frozen identities are

    Psi(q) = integral_0^1 H(q,x) dx,
    Phi(e) = (Psi(q(e)) - Psi(1))/8,
    q(e) = (1-e)/(1+e),

and

    Phi''(e) = (1+q)^3/32 * integral_0^1 C(q,x) dx,
    C(q,x) = (1+q) H_qq(q,x) + 2 H_q(q,x).

The certificate proves the deliberately conservative publication bounds

    Phi(1) > 1/4000,
    Phi''(e) < -1/100000  for 0 < e < 1.

All interval operations, including sqrt and atan, are evaluated by Arb ball
arithmetic.  Exact rational slab and panel endpoints are converted without
passing through Python binary floats.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import platform
import sys
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable

import flint
from flint import arb, ctx, fmpq

CERTIFICATE_VERSION = "PEABODY_ARB_FLINT_CONCAVITY_V2"
FORMULA_VERSION = "PEABODY_CENTRAL_STABLE_Q_V1"
PYTHON_FLINT_PIN = "0.9.0"
DEFAULT_BITS = 384
ENDPOINT_X_PANELS = 4
CONCAVITY_Q_SLABS = 32
CONCAVITY_X_PANELS = 10
ENDPOINT_TARGET = Fraction(1, 4000)
CONCAVITY_TARGET = Fraction(1, 100000)
MAX_BOXES = 1000


def fracstr(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rational(value: Fraction | int) -> arb:
    """Return an Arb ball enclosing an exact rational input."""
    if isinstance(value, int):
        return arb(value)
    return arb(fmpq(value.numerator, value.denominator))


def rational_interval(lo: Fraction, hi: Fraction) -> arb:
    """Return a ball containing the exact interval [lo, hi]."""
    if lo > hi:
        lo, hi = hi, lo
    midpoint = (lo + hi) / 2
    radius = (hi - lo) / 2
    # Rational strings are documented inputs for both midpoint and radius.
    # Arb rounds the radius upward if necessary, preserving inclusion.
    return arb(fracstr(midpoint), fracstr(radius))


def point_text(value: arb, digits: int = 90) -> str:
    """Render a finite or nonfinite Arb point without raising.

    Canonical proof runs have finite exact directed endpoints. Deliberately
    under-resolved or sign-mutated controls can instead produce unbounded or
    indeterminate balls. Those controls still need a semantic NO-GO JSON
    certificate, so diagnostic serialization must not call ``man_exp`` on a
    nonfinite value.
    """
    try:
        return value.str(digits, radius=False)
    except Exception:  # pragma: no cover - diagnostic fallback only
        return str(value)


def lower_text(value: arb, digits: int = 90) -> str:
    try:
        return point_text(value.lower(), digits)
    except Exception:  # pragma: no cover - diagnostic fallback only
        return str(value)


def upper_text(value: arb, digits: int = 90) -> str:
    try:
        return point_text(value.upper(), digits)
    except Exception:  # pragma: no cover - diagnostic fallback only
        return str(value)


def exact_binary_point(value: arb) -> dict[str, int | str] | None:
    """Serialize an exact finite Arb point, or return ``None``.

    Python-FLINT's ``man_exp`` is defined only for exact finite values. The
    authoritative runs must have such endpoints; negative controls are allowed
    to produce nonfinite diagnostic bounds and are serialized with null binary
    endpoints instead of crashing before their expected NO-GO certificate is
    written.
    """
    if not bool(value.is_finite()) or not bool(value.is_exact()):
        return None
    mantissa, exponent = value.man_exp()
    return {"mantissa": str(mantissa), "exponent": int(exponent)}


def enclosure(value: arb, digits: int = 90) -> dict[str, Any]:
    try:
        lower = value.lower()
    except Exception:  # pragma: no cover - diagnostic fallback only
        lower = value
    try:
        upper = value.upper()
    except Exception:  # pragma: no cover - diagnostic fallback only
        upper = value
    return {
        "lower": point_text(lower, digits),
        "upper": point_text(upper, digits),
        "finite": bool(value.is_finite()),
        "lower_binary": exact_binary_point(lower),
        "upper_binary": exact_binary_point(upper),
    }


def definitely_gt(left: arb, right: arb | int) -> bool:
    right_ball = right if isinstance(right, arb) else arb(right)
    return bool(left.lower() > right_ball.upper())


def definitely_lt(left: arb, right: arb | int) -> bool:
    right_ball = right if isinstance(right, arb) else arb(right)
    return bool(left.upper() < right_ball.lower())


@dataclass(frozen=True)
class Constants:
    one: arb
    sqrt2: arb
    kappa: arb
    K: arb
    psi0: arb


def setup(bits: int) -> Constants:
    if bits < 160:
        raise ValueError("precision must be at least 160 bits")
    ctx.prec = bits
    one = arb(1)
    sqrt2 = arb(2).sqrt()
    kappa = one + sqrt2
    K = kappa * kappa
    alpha = rational(Fraction(1, 3)).acos()
    psi0 = -(2 * arb.pi() / arb(3).sqrt()) * alpha
    return Constants(one=one, sqrt2=sqrt2, kappa=kappa, K=K, psi0=psi0)


@dataclass
class D3:
    """Ordinary q-derivatives through order three."""

    v: arb
    d1: arb
    d2: arb
    d3: arb

    def __add__(self, other: Any) -> "D3":
        other = as_d3(other)
        return D3(self.v + other.v, self.d1 + other.d1,
                  self.d2 + other.d2, self.d3 + other.d3)

    __radd__ = __add__

    def __sub__(self, other: Any) -> "D3":
        other = as_d3(other)
        return D3(self.v - other.v, self.d1 - other.d1,
                  self.d2 - other.d2, self.d3 - other.d3)

    def __rsub__(self, other: Any) -> "D3":
        return as_d3(other) - self

    def __mul__(self, other: Any) -> "D3":
        other = as_d3(other)
        return D3(
            self.v * other.v,
            self.d1 * other.v + self.v * other.d1,
            self.d2 * other.v + 2 * self.d1 * other.d1 + self.v * other.d2,
            self.d3 * other.v + 3 * self.d2 * other.d1
            + 3 * self.d1 * other.d2 + self.v * other.d3,
        )

    __rmul__ = __mul__

    def __neg__(self) -> "D3":
        return D3(-self.v, -self.d1, -self.d2, -self.d3)

    def inv(self) -> "D3":
        value = self.v
        return D3(
            1 / value,
            -self.d1 / value**2,
            2 * self.d1**2 / value**3 - self.d2 / value**2,
            -6 * self.d1**3 / value**4
            + 6 * self.d1 * self.d2 / value**3
            - self.d3 / value**2,
        )

    def __truediv__(self, other: Any) -> "D3":
        return self * as_d3(other).inv()

    def __rtruediv__(self, other: Any) -> "D3":
        return as_d3(other) * self.inv()

    def __pow__(self, power: int) -> "D3":
        if power == 0:
            return as_d3(1)
        if power < 0:
            return (self ** (-power)).inv()
        result = as_d3(1)
        base = self
        exponent = power
        while exponent:
            if exponent & 1:
                result = result * base
            base = base * base
            exponent //= 2
        return result


@dataclass
class X2:
    """Second x-derivatives whose coefficients are q-jets."""

    v: D3
    x: D3
    xx: D3

    def __add__(self, other: Any) -> "X2":
        other = as_x2(other)
        return X2(self.v + other.v, self.x + other.x, self.xx + other.xx)

    __radd__ = __add__

    def __sub__(self, other: Any) -> "X2":
        other = as_x2(other)
        return X2(self.v - other.v, self.x - other.x, self.xx - other.xx)

    def __rsub__(self, other: Any) -> "X2":
        return as_x2(other) - self

    def __mul__(self, other: Any) -> "X2":
        other = as_x2(other)
        return X2(
            self.v * other.v,
            self.x * other.v + self.v * other.x,
            self.xx * other.v + 2 * self.x * other.x + self.v * other.xx,
        )

    __rmul__ = __mul__

    def __neg__(self) -> "X2":
        return X2(-self.v, -self.x, -self.xx)

    def inv(self) -> "X2":
        value = self.v
        return X2(1 / value, -self.x / value**2,
                  2 * self.x**2 / value**3 - self.xx / value**2)

    def __truediv__(self, other: Any) -> "X2":
        return self * as_x2(other).inv()

    def __rtruediv__(self, other: Any) -> "X2":
        return as_x2(other) * self.inv()

    def __pow__(self, power: int) -> "X2":
        if power == 0:
            return as_x2(1)
        if power < 0:
            return (self ** (-power)).inv()
        result = as_x2(1)
        base = self
        exponent = power
        while exponent:
            if exponent & 1:
                result = result * base
            base = base * base
            exponent //= 2
        return result


def as_d3(value: Any) -> D3:
    if isinstance(value, D3):
        return value
    ball = value if isinstance(value, arb) else arb(value)
    zero = arb(0)
    return D3(ball, zero, zero, zero)


def as_x2(value: Any) -> X2:
    if isinstance(value, X2):
        return value
    if isinstance(value, D3):
        return X2(value, as_d3(0), as_d3(0))
    return X2(as_d3(value), as_d3(0), as_d3(0))


def sqrt_d3(value: Any) -> D3:
    value = as_d3(value)
    root = value.v.sqrt()
    return D3(
        root,
        value.d1 / (2 * root),
        value.d2 / (2 * root) - value.d1**2 / (4 * root**3),
        value.d3 / (2 * root)
        - 3 * value.d1 * value.d2 / (4 * root**3)
        + 3 * value.d1**3 / (8 * root**5),
    )


def atan_d3(value: Any) -> D3:
    value = as_d3(value)
    den = 1 + value.v**2
    return D3(
        value.v.atan(),
        value.d1 / den,
        value.d2 / den - 2 * value.v * value.d1**2 / den**2,
        value.d3 / den
        - 6 * value.v * value.d1 * value.d2 / den**2
        + (6 * value.v**2 - 2) * value.d1**3 / den**3,
    )


def sqrt_x2(value: Any) -> X2:
    value = as_x2(value)
    root = sqrt_d3(value.v)
    return X2(root, value.x / (2 * root),
              value.xx / (2 * root) - value.x**2 / (4 * root**3))


def atan_x2(value: Any) -> X2:
    value = as_x2(value)
    den = 1 + value.v**2
    return X2(atan_d3(value.v), value.x / den,
              value.xx / den - 2 * value.v * value.x**2 / den**2)


def h_jet(q_value: arb, x_value: arb, constants: Constants,
          correction_sign: int = 1) -> X2:
    """Evaluate H and the needed q/x derivatives on Arb balls."""
    zero = arb(0)
    Q = X2(D3(q_value, arb(1), zero, zero), as_d3(0), as_d3(0))
    X = X2(D3(x_value, zero, zero, zero), as_d3(1), as_d3(0))
    one = as_x2(1)
    K = as_x2(constants.K)
    sqrt2 = as_x2(constants.sqrt2)
    kappa = as_x2(constants.kappa)

    D = sqrt_x2(K * K + Q * Q)
    R = sqrt_x2(K * K + Q * Q - 2 * K * Q * X * X)
    T = sqrt_x2(2 * K * (K * K + Q * Q)
                + K * K * (one - Q) * (one - Q) * X * X)
    delta = 2 * K * (one - X * X) / (R + K - Q)
    M = K * (Q - 2 * K * X * X) / (R + K) \
        + (one - K) * R - K * K - Q * R - Q - Q * Q

    primary = -16 * sqrt2 * kappa * (K * K + Q * Q) / (R * T)
    correction = -4 * K * (one - Q * Q) * (K * K + Q * Q) \
        * delta * M / (R * T * T * T)
    algebraic = -4 * K * (one - Q * Q) * (K * K + Q * Q) \
        * delta / (R * T * T)
    Z = K * ((one + Q) * D + (one - Q) * R) / (T * (K + Q + D))
    return (primary + correction_sign * correction) * atan_x2(Z) + algebraic


def midpoint_integral(
    q_value: arb,
    x_panels: int,
    constants: Constants,
    value_fn: Callable[[X2, arb], arb],
    second_x_fn: Callable[[X2, arb], arb],
    correction_sign: int = 1,
    record: bool = False,
) -> tuple[arb, list[dict[str, Any]]]:
    width = rational(Fraction(1, x_panels))
    total = arb(0)
    rows: list[dict[str, Any]] = []
    for index in range(x_panels):
        midpoint = rational(Fraction(2 * index + 1, 2 * x_panels))
        x_box = rational_interval(Fraction(index, x_panels),
                                  Fraction(index + 1, x_panels))
        at_mid = h_jet(q_value, midpoint, constants,
                       correction_sign=correction_sign)
        on_box = h_jet(q_value, x_box, constants,
                       correction_sign=correction_sign)
        main = width * value_fn(at_mid, q_value)
        remainder = width**3 / 24 * second_x_fn(on_box, q_value)
        contribution = main + remainder
        total += contribution
        if record:
            rows.append({
                "x_panel_index": index,
                "x_lo": f"{index}/{x_panels}",
                "x_hi": f"{index + 1}/{x_panels}",
                "midpoint_term": main,
                "remainder_term": remainder,
                "contribution": contribution,
            })
    return total, rows


def endpoint_phi(constants: Constants, x_panels: int,
                 correction_sign: int = 1,
                 record: bool = False) -> tuple[arb, list[dict[str, Any]]]:
    psi_one, rows = midpoint_integral(
        arb(0), x_panels, constants,
        value_fn=lambda jet, _q: jet.v.v,
        second_x_fn=lambda jet, _q: jet.xx.v,
        correction_sign=correction_sign,
        record=record,
    )
    return (psi_one - constants.psi0) / 8, rows


def c_integral_at_point(q: Fraction, constants: Constants, x_panels: int,
                        correction_sign: int = 1,
                        record: bool = False) -> tuple[arb, list[dict[str, Any]]]:
    q_value = rational(q)
    return midpoint_integral(
        q_value, x_panels, constants,
        value_fn=lambda jet, qv: (1 + qv) * jet.v.d2 + 2 * jet.v.d1,
        second_x_fn=lambda jet, qv: (1 + qv) * jet.xx.d2 + 2 * jet.xx.d1,
        correction_sign=correction_sign,
        record=record,
    )


def cq_integral_on_slab(q_lo: Fraction, q_hi: Fraction,
                        constants: Constants, x_panels: int,
                        correction_sign: int = 1,
                        record: bool = False) -> tuple[arb, list[dict[str, Any]]]:
    q_box = rational_interval(q_lo, q_hi)
    return midpoint_integral(
        q_box, x_panels, constants,
        value_fn=lambda jet, qv: (1 + qv) * jet.v.d3 + 3 * jet.v.d2,
        second_x_fn=lambda jet, qv: (1 + qv) * jet.xx.d3 + 3 * jet.xx.d2,
        correction_sign=correction_sign,
        record=record,
    )


def concavity_slab(q_lo: Fraction, q_hi: Fraction,
                   constants: Constants, x_panels: int,
                   correction_sign: int = 1,
                   record: bool = False) -> tuple[arb, arb, dict[str, Any], list[dict[str, Any]]]:
    q_mid = (q_lo + q_hi) / 2
    c_mid, point_rows = c_integral_at_point(
        q_mid, constants, x_panels,
        correction_sign=correction_sign, record=record)
    c_q, derivative_rows = cq_integral_on_slab(
        q_lo, q_hi, constants, x_panels,
        correction_sign=correction_sign, record=record)
    q_delta = rational_interval(q_lo - q_mid, q_hi - q_mid)
    c_enclosure = c_mid + q_delta * c_q
    q_box = rational_interval(q_lo, q_hi)
    phi_second = ((1 + q_box)**3 / 32) * c_enclosure
    info = {
        "q_lo": fracstr(q_lo),
        "q_hi": fracstr(q_hi),
        "q_mid": fracstr(q_mid),
        "c_mid": c_mid,
        "c_q": c_q,
        "c_enclosure": c_enclosure,
        "phi_second": phi_second,
    }
    rows: list[dict[str, Any]] = []
    if record:
        for point, derivative in zip(point_rows, derivative_rows):
            rows.append({
                "q_lo": fracstr(q_lo),
                "q_hi": fracstr(q_hi),
                "q_mid": fracstr(q_mid),
                "x_panel_index": point["x_panel_index"],
                "x_lo": point["x_lo"],
                "x_hi": point["x_hi"],
                "c_point_midpoint_term": point["midpoint_term"],
                "c_point_remainder_term": point["remainder_term"],
                "c_point_contribution": point["contribution"],
                "cq_midpoint_term": derivative["midpoint_term"],
                "cq_remainder_term": derivative["remainder_term"],
                "cq_contribution": derivative["contribution"],
            })
    return c_enclosure, phi_second, info, rows


def domain_diagnostics(constants: Constants) -> dict[str, arb]:
    q = rational_interval(Fraction(0), Fraction(1))
    x = rational_interval(Fraction(0), Fraction(1))
    K = constants.K
    D2 = K * K + q * q
    R2 = K * K + q * q - 2 * K * q * x * x
    T2 = 2 * K * (K * K + q * q) + K * K * (1 - q)**2 * x * x
    D = D2.sqrt()
    R = R2.sqrt()
    T = T2.sqrt()
    diagnostics = {
        "D2": D2,
        "R2": R2,
        "T2": T2,
        "delta_denominator": R + K - q,
        "angle_numerator": K * ((1 + q) * D + (1 - q) * R),
        "angle_denominator": T * (K + q + D),
    }
    diagnostics["Z"] = diagnostics["angle_numerator"] / diagnostics["angle_denominator"]
    return diagnostics


def normalize_row(row: dict[str, Any], digits: int) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in row.items():
        if isinstance(value, arb):
            interval = enclosure(value, digits)
            lower_binary = interval["lower_binary"]
            upper_binary = interval["upper_binary"]
            if lower_binary is None or upper_binary is None:
                raise RuntimeError(
                    f"authoritative terminal-box field {key!r} has a nonfinite "
                    "or nonexact directed endpoint"
                )
            output[key + "_lower"] = interval["lower"]
            output[key + "_upper"] = interval["upper"]
            output[key + "_lower_mantissa"] = lower_binary["mantissa"]
            output[key + "_lower_exponent"] = lower_binary["exponent"]
            output[key + "_upper_mantissa"] = upper_binary["mantissa"]
            output[key + "_upper_exponent"] = upper_binary["exponent"]
        else:
            output[key] = value
    return output


def write_csv(path: Path, rows: list[dict[str, Any]], digits: int) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = [normalize_row(row, digits) for row in rows]
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(normalized[0].keys()))
        writer.writeheader()
        writer.writerows(normalized)


def module_version_info() -> dict[str, Any]:
    attrs: dict[str, str] = {}
    for name in dir(flint):
        if "version" in name.lower():
            try:
                attrs[name] = str(getattr(flint, name))
            except Exception as exc:  # pragma: no cover - diagnostic only
                attrs[name] = f"<unreadable: {exc}>"
    return {
        "python_flint_distribution": importlib.metadata.version("python-flint"),
        "flint_module_version": str(getattr(flint, "__version__", "unknown")),
        "flint_module_file": str(Path(flint.__file__).resolve()),
        "version_like_module_attributes": attrs,
    }


def run(output_dir: Path, bits: int, reverse: bool = False,
        correction_sign: int = 1, q_slabs: int = CONCAVITY_Q_SLABS,
        x_panels: int = CONCAVITY_X_PANELS,
        write_boxes: bool = True) -> dict[str, Any]:
    start = time.time()
    output_dir.mkdir(parents=True, exist_ok=True)
    constants = setup(bits)
    digits = max(80, int(bits * 0.30103) + 15)

    diagnostics = domain_diagnostics(constants)
    diagnostics_json = {
        key: {**enclosure(value, digits),
              "strictly_positive": definitely_gt(value, 0)}
        for key, value in diagnostics.items()
    }

    endpoint_value, endpoint_rows = endpoint_phi(
        constants, ENDPOINT_X_PANELS,
        correction_sign=correction_sign, record=write_boxes)
    endpoint_target = rational(ENDPOINT_TARGET)
    endpoint_pass = definitely_gt(endpoint_value, endpoint_target)

    indices = list(range(q_slabs))
    if reverse:
        indices.reverse()
    negative_target = -rational(CONCAVITY_TARGET)
    slab_records: list[dict[str, Any]] = []
    terminal_rows: list[dict[str, Any]] = []
    worst_upper: arb | None = None
    all_concave = True

    for index in indices:
        q_lo = Fraction(index, q_slabs)
        q_hi = Fraction(index + 1, q_slabs)
        c_value, phi_second, info, rows = concavity_slab(
            q_lo, q_hi, constants, x_panels,
            correction_sign=correction_sign, record=write_boxes)
        slab_pass = definitely_lt(phi_second, negative_target)
        all_concave = all_concave and slab_pass
        upper = phi_second.upper()
        if worst_upper is None or bool(upper > worst_upper):
            worst_upper = upper
        slab_records.append({
            "index": index,
            "q_lo": info["q_lo"],
            "q_hi": info["q_hi"],
            "q_mid": info["q_mid"],
            "c_mid": enclosure(info["c_mid"], digits),
            "c_q": enclosure(info["c_q"], digits),
            "c_enclosure": enclosure(c_value, digits),
            "phi_second": enclosure(phi_second, digits),
            "below_negative_target": slab_pass,
        })
        if write_boxes:
            terminal_rows.extend({"q_slab_index": index, **row} for row in rows)

    slab_records.sort(key=lambda item: item["index"])
    terminal_rectangles = ENDPOINT_X_PANELS + q_slabs * x_panels
    if terminal_rectangles > MAX_BOXES:
        raise RuntimeError("terminal-rectangle hard stop exceeded")

    if write_boxes:
        write_csv(output_dir / "endpoint_terminal_boxes.csv", endpoint_rows, digits)
        write_csv(output_dir / "concavity_terminal_boxes.csv", terminal_rows, digits)
        with (output_dir / "concavity_slab_summary.csv").open(
                "w", newline="", encoding="utf-8") as stream:
            fields = [
                "index", "q_lo", "q_hi", "q_mid",
                "c_lower", "c_upper",
                "phi_second_lower", "phi_second_upper",
                "below_negative_target",
            ]
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            for record in slab_records:
                writer.writerow({
                    "index": record["index"],
                    "q_lo": record["q_lo"],
                    "q_hi": record["q_hi"],
                    "q_mid": record["q_mid"],
                    "c_lower": record["c_enclosure"]["lower"],
                    "c_upper": record["c_enclosure"]["upper"],
                    "phi_second_lower": record["phi_second"]["lower"],
                    "phi_second_upper": record["phi_second"]["upper"],
                    "below_negative_target": record["below_negative_target"],
                })

    passed = (
        endpoint_pass
        and all_concave
        and all(item["strictly_positive"] for item in diagnostics_json.values())
    )
    summary: dict[str, Any] = {
        "certificate_version": CERTIFICATE_VERSION,
        "formula_version": FORMULA_VERSION,
        "classification": (
            "GO_PEABODY_ARB_FLINT_CERTIFICATE"
            if passed else "NO_GO_PEABODY_ARB_FLINT_CERTIFICATE"
        ),
        "pass": passed,
        "proof_status": "CERTIFIED" if passed else "NOT_CERTIFIED",
        "proof_authority": "python-flint Arb rigorous real-ball arithmetic",
        "environment": {
            "python_version": sys.version,
            "platform": platform.platform(),
            "precision_bits": bits,
            **module_version_info(),
        },
        "domain_diagnostics": diagnostics_json,
        "endpoint": {
            "definition": "Phi(1)=lim_{e->1-} Phi(e), equivalently q=0",
            "x_panels": ENDPOINT_X_PANELS,
            "phi_one_enclosure": enclosure(endpoint_value, digits),
            "target": fracstr(ENDPOINT_TARGET),
            "pass": endpoint_pass,
        },
        "concavity": {
            "identity": "Phi''(e)=((1+q)^3/32)*integral((1+q)H_qq+2H_q)dx",
            "q_range": "0 <= q <= 1",
            "q_slabs": q_slabs,
            "x_panels_per_slab": x_panels,
            "target": f"-{fracstr(CONCAVITY_TARGET)}",
            "worst_phi_second_upper": upper_text(worst_upper, digits) if worst_upper else None,
            "worst_phi_second_upper_binary": (
                exact_binary_point(worst_upper) if worst_upper is not None else None
            ),
            "pass": all_concave,
        },
        "terminal_rectangles": terminal_rectangles,
        "subdivision_order": "reverse" if reverse else "forward",
        "correction_sign": correction_sign,
        "deduced_bound": "Phi(e) > e/4000 for 0<e<1" if passed else None,
        "elapsed_seconds": time.time() - start,
    }
    certificate_path = output_dir / "peabody_arb_concavity_certificate.json"
    certificate_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    generated = [certificate_path]
    for name in (
        "endpoint_terminal_boxes.csv",
        "concavity_terminal_boxes.csv",
        "concavity_slab_summary.csv",
    ):
        path = output_dir / name
        if path.exists():
            generated.append(path)
    hashes = {path.name: sha256(path) for path in generated}
    (output_dir / "OUTPUT_SHA256.json").write_text(
        json.dumps(hashes, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--bits", type=int, default=DEFAULT_BITS)
    parser.add_argument("--reverse", action="store_true")
    parser.add_argument("--correction-sign", type=int, choices=(-1, 1), default=1)
    parser.add_argument("--q-slabs", type=int, default=CONCAVITY_Q_SLABS)
    parser.add_argument("--x-panels", type=int, default=CONCAVITY_X_PANELS)
    parser.add_argument("--no-boxes", action="store_true")
    args = parser.parse_args()

    installed = importlib.metadata.version("python-flint")
    if installed != PYTHON_FLINT_PIN:
        raise RuntimeError(
            f"python-flint {PYTHON_FLINT_PIN} is required; found {installed}")

    summary = run(
        args.output_dir,
        bits=args.bits,
        reverse=args.reverse,
        correction_sign=args.correction_sign,
        q_slabs=args.q_slabs,
        x_panels=args.x_panels,
        write_boxes=not args.no_boxes,
    )
    print(summary["classification"])
    print("pass:", summary["pass"])
    print("endpoint lower:", summary["endpoint"]["phi_one_enclosure"]["lower"])
    print("worst Phi'' upper:", summary["concavity"]["worst_phi_second_upper"])
    return 0 if summary["pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
