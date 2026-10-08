#!/usr/bin/env python3
"""Rigorous concavity compression for the confocal Peabody scalar Phi.

The frozen fixed-interval formula is

    Psi(q) = integral_0^1 H(q,x) dx,
    Phi(e) = (Psi(q(e)) - Psi(1))/8,
    q(e) = (1-e)/(1+e).

This certifier proves two statements:

  1. The continuous parabolic endpoint satisfies Phi(1) > 3/10000.
  2. Phi''(e) < -1/25000 for every 0 < e < 1.

The second statement follows from

    Phi''(e) = (1+q)^3/32 * integral_0^1 C(q,x) dx,
    C(q,x) = (1+q) H_qq(q,x) + 2 H_q(q,x).

A third-order parameter jet and a second-order x jet evaluate H and all
required derivatives with outward-rounded mpmath.iv arithmetic.  The x
integrals use the midpoint rule with an interval second-derivative remainder.
Each q slab uses a centered mean-value enclosure for integral C.

The proof uses 4 endpoint panels and 32*10 concavity panels, for 324 terminal
rectangles in total.  No search over Peabody bodies is performed.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import sys
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable

import mpmath as mp
from mpmath.libmp import to_str

CERTIFICATE_VERSION = "PEABODY_ANALYTIC_COMPRESSION_CONCAVITY_V1"
FORMULA_VERSION = "PEABODY_CENTRAL_STABLE_Q_V1"
DEFAULT_DPS = 80
ENDPOINT_X_PANELS = 4
CONCAVITY_Q_SLABS = 32
CONCAVITY_X_PANELS = 10
ENDPOINT_TARGET = Fraction(3, 10_000)
CONCAVITY_TARGET = Fraction(1, 25_000)  # Phi'' < -1/25000
MAX_BOXES = 1_000
MAX_DATA_BYTES = 5_000_000


def fracstr(f: Fraction) -> str:
    return f"{f.numerator}/{f.denominator}"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass(frozen=True)
class Constants:
    iv: Any
    one: Any
    sqrt2: Any
    kappa: Any
    K: Any
    psi0: Any


def setup(dps: int) -> Constants:
    if dps < 50:
        raise ValueError("precision must be at least 50 decimal digits")
    mp.iv.dps = dps
    iv = mp.iv
    one = iv.mpf(1)
    sqrt2 = iv.sqrt(2)
    kappa = one + sqrt2
    K = kappa * kappa
    alpha = iv.atan2(2 * sqrt2, one)  # acos(1/3)
    psi0 = -(2 * iv.pi / iv.sqrt(3)) * alpha
    return Constants(iv=iv, one=one, sqrt2=sqrt2, kappa=kappa, K=K, psi0=psi0)


def ivpoint(f: Fraction, c: Constants) -> Any:
    return c.iv.mpf(f.numerator) / f.denominator


def ivhull(a: Fraction, b: Fraction, c: Constants) -> Any:
    if a > b:
        a, b = b, a
    den = math.lcm(a.denominator, b.denominator)
    return c.iv.mpf([
        a.numerator * (den // a.denominator),
        b.numerator * (den // b.denominator),
    ]) / den


def endpoint(value: Any, which: str, digits: int) -> str:
    item = value._mpi_[0 if which == "lower" else 1]
    return to_str(item, digits, strip_zeros=False)


def enclosure(value: Any, digits: int) -> dict[str, str]:
    return {
        "lower": endpoint(value, "lower", digits),
        "upper": endpoint(value, "upper", digits),
    }


# Univariate parameter jet storing ordinary derivatives through order three.
@dataclass
class D3:
    v: Any
    d1: Any
    d2: Any
    d3: Any

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
        other = as_d3(other)
        return other - self

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
        v = self.v
        return D3(
            1 / v,
            -self.d1 / v**2,
            2 * self.d1**2 / v**3 - self.d2 / v**2,
            -6 * self.d1**3 / v**4
            + 6 * self.d1 * self.d2 / v**3
            - self.d3 / v**2,
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
        n = power
        while n:
            if n & 1:
                result = result * base
            base = base * base
            n //= 2
        return result


# Second-order x jet whose coefficients are D3 parameter jets.
@dataclass
class X2:
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
        other = as_x2(other)
        return other - self

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
        v = self.v
        return X2(1 / v, -self.x / v**2,
                  2 * self.x**2 / v**3 - self.xx / v**2)

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
        n = power
        while n:
            if n & 1:
                result = result * base
            base = base * base
            n //= 2
        return result


_IV: Any = None


def as_d3(value: Any) -> D3:
    if isinstance(value, D3):
        return value
    if hasattr(value, "_mpi_"):
        zero = _IV.mpf(0)
        return D3(value, zero, zero, zero)
    zero = _IV.mpf(0)
    return D3(_IV.mpf(value), zero, zero, zero)


def as_x2(value: Any) -> X2:
    if isinstance(value, X2):
        return value
    if isinstance(value, D3):
        return X2(value, as_d3(0), as_d3(0))
    return X2(as_d3(value), as_d3(0), as_d3(0))


def sqrt_d3(value: Any) -> D3:
    value = as_d3(value)
    s = _IV.sqrt(value.v)
    return D3(
        s,
        value.d1 / (2 * s),
        value.d2 / (2 * s) - value.d1**2 / (4 * s**3),
        value.d3 / (2 * s)
        - 3 * value.d1 * value.d2 / (4 * s**3)
        + 3 * value.d1**3 / (8 * s**5),
    )


def atan_d3(value: Any) -> D3:
    value = as_d3(value)
    den = 1 + value.v**2
    return D3(
        _IV.atan2(value.v, _IV.mpf(1)),
        value.d1 / den,
        value.d2 / den - 2 * value.v * value.d1**2 / den**2,
        value.d3 / den
        - 6 * value.v * value.d1 * value.d2 / den**2
        + (6 * value.v**2 - 2) * value.d1**3 / den**3,
    )


def sqrt_x2(value: Any) -> X2:
    value = as_x2(value)
    s = sqrt_d3(value.v)
    return X2(s, value.x / (2 * s),
              value.xx / (2 * s) - value.x**2 / (4 * s**3))


def atan_x2(value: Any) -> X2:
    value = as_x2(value)
    den = 1 + value.v**2
    return X2(atan_d3(value.v), value.x / den,
              value.xx / den - 2 * value.v * value.x**2 / den**2)


def h_jet(q_value: Any, x_value: Any, c: Constants,
          correction_sign: int = 1) -> X2:
    """Return H and q/x derivatives on intervals.

    ``correction_sign`` is exposed only for an adversarial sign-mutation test.
    The certified run always uses +1.
    """
    global _IV
    _IV = c.iv
    zero = c.iv.mpf(0)
    Q = X2(D3(q_value, c.iv.mpf(1), zero, zero), as_d3(0), as_d3(0))
    X = X2(D3(x_value, zero, zero, zero), as_d3(1), as_d3(0))
    one = as_x2(1)
    K = as_x2(c.K)
    sqrt2 = as_x2(c.sqrt2)
    kappa = as_x2(c.kappa)

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
    q_value: Any,
    x_panels: int,
    c: Constants,
    value_fn: Callable[[X2, Any], Any],
    second_x_fn: Callable[[X2, Any], Any],
    correction_sign: int = 1,
    record: bool = False,
) -> tuple[Any, list[dict[str, Any]]]:
    width = c.iv.mpf(1) / x_panels
    total = c.iv.mpf(0)
    rows: list[dict[str, Any]] = []
    for index in range(x_panels):
        midpoint = c.iv.mpf(2 * index + 1) / (2 * x_panels)
        x_box = c.iv.mpf([index, index + 1]) / x_panels
        at_mid = h_jet(q_value, midpoint, c, correction_sign=correction_sign)
        on_box = h_jet(q_value, x_box, c, correction_sign=correction_sign)
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


def endpoint_phi(c: Constants, x_panels: int, record: bool = False,
                 correction_sign: int = 1) -> tuple[Any, list[dict[str, Any]]]:
    q_zero = c.iv.mpf(0)
    psi_one, rows = midpoint_integral(
        q_zero, x_panels, c,
        value_fn=lambda jet, _q: jet.v.v,
        second_x_fn=lambda jet, _q: jet.xx.v,
        correction_sign=correction_sign,
        record=record,
    )
    return (psi_one - c.psi0) / 8, rows


def c_integral_at_point(q: Fraction, c: Constants, x_panels: int,
                        correction_sign: int = 1,
                        record: bool = False) -> tuple[Any, list[dict[str, Any]]]:
    q_value = ivpoint(q, c)
    return midpoint_integral(
        q_value, x_panels, c,
        value_fn=lambda jet, qv: (1 + qv) * jet.v.d2 + 2 * jet.v.d1,
        second_x_fn=lambda jet, qv: (1 + qv) * jet.xx.d2 + 2 * jet.xx.d1,
        correction_sign=correction_sign,
        record=record,
    )


def cq_integral_on_slab(q_lo: Fraction, q_hi: Fraction, c: Constants,
                        x_panels: int, correction_sign: int = 1,
                        record: bool = False) -> tuple[Any, list[dict[str, Any]]]:
    q_box = ivhull(q_lo, q_hi, c)
    return midpoint_integral(
        q_box, x_panels, c,
        value_fn=lambda jet, qv: (1 + qv) * jet.v.d3 + 3 * jet.v.d2,
        second_x_fn=lambda jet, qv: (1 + qv) * jet.xx.d3 + 3 * jet.xx.d2,
        correction_sign=correction_sign,
        record=record,
    )


def concavity_slab(q_lo: Fraction, q_hi: Fraction, c: Constants,
                   x_panels: int, correction_sign: int = 1,
                   record: bool = False) -> tuple[Any, Any, dict[str, Any], list[dict[str, Any]]]:
    q_mid = (q_lo + q_hi) / 2
    c_mid, point_rows = c_integral_at_point(
        q_mid, c, x_panels, correction_sign=correction_sign, record=record)
    c_q, derivative_rows = cq_integral_on_slab(
        q_lo, q_hi, c, x_panels, correction_sign=correction_sign, record=record)
    q_delta = ivhull(q_lo - q_mid, q_hi - q_mid, c)
    c_enclosure = c_mid + q_delta * c_q
    q_box = ivhull(q_lo, q_hi, c)
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


def domain_diagnostics(c: Constants) -> dict[str, Any]:
    q = c.iv.mpf([0, 1])
    x = c.iv.mpf([0, 1])
    K = c.K
    D2 = K * K + q * q
    R2 = K * K + q * q - 2 * K * q * x * x
    T2 = 2 * K * (K * K + q * q) + K * K * (1 - q)**2 * x * x
    D = c.iv.sqrt(D2)
    R = c.iv.sqrt(R2)
    T = c.iv.sqrt(T2)
    diagnostics = {
        "D2": D2,
        "R2": R2,
        "T2": T2,
        "delta_denominator": R + K - q,
        "angle_denominator": T * (K + q + D),
        "angle_numerator": K * ((1 + q) * D + (1 - q) * R),
    }
    diagnostics["Z"] = diagnostics["angle_numerator"] / diagnostics["angle_denominator"]
    return diagnostics


def write_csv(path: Path, rows: list[dict[str, Any]], digits: int) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized: list[dict[str, Any]] = []
    for row in rows:
        out: dict[str, Any] = {}
        for key, value in row.items():
            if hasattr(value, "_mpi_"):
                out[key + "_lower"] = endpoint(value, "lower", digits)
                out[key + "_upper"] = endpoint(value, "upper", digits)
            else:
                out[key] = value
        normalized.append(out)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(normalized[0].keys()))
        writer.writeheader()
        writer.writerows(normalized)


def run(output_dir: Path, dps: int, reverse: bool = False,
        correction_sign: int = 1, write_boxes: bool = True,
        q_slabs: int = CONCAVITY_Q_SLABS,
        x_panels: int = CONCAVITY_X_PANELS) -> dict[str, Any]:
    start = time.time()
    output_dir.mkdir(parents=True, exist_ok=True)
    c = setup(dps)
    digits = dps + 20

    diagnostics = domain_diagnostics(c)
    diagnostics_json = {
        key: {**enclosure(value, digits), "strictly_positive": bool(value.a > 0)}
        for key, value in diagnostics.items()
    }

    endpoint_value, endpoint_rows = endpoint_phi(
        c, ENDPOINT_X_PANELS, record=write_boxes, correction_sign=correction_sign)
    endpoint_target = ivpoint(ENDPOINT_TARGET, c)
    endpoint_pass = bool(endpoint_value.a > endpoint_target.b)

    indices = list(range(q_slabs))
    if reverse:
        indices.reverse()
    slab_records: list[dict[str, Any]] = []
    box_records: list[dict[str, Any]] = []
    worst_upper = None
    all_concave = True
    negative_target = -ivpoint(CONCAVITY_TARGET, c)

    for index in indices:
        q_lo = Fraction(index, q_slabs)
        q_hi = Fraction(index + 1, q_slabs)
        c_value, phi_second, info, rows = concavity_slab(
            q_lo, q_hi, c, x_panels,
            correction_sign=correction_sign, record=write_boxes)
        slab_pass = bool(phi_second.b < negative_target.a)
        all_concave = all_concave and slab_pass
        if worst_upper is None or bool(phi_second.b > worst_upper):
            worst_upper = phi_second.b
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
            for row in rows:
                box_records.append({"q_slab_index": index, **row})

    slab_records.sort(key=lambda item: item["index"])
    terminal_boxes = ENDPOINT_X_PANELS + q_slabs * x_panels
    if terminal_boxes > MAX_BOXES:
        raise RuntimeError("terminal-box hard stop exceeded")

    if write_boxes:
        write_csv(output_dir / "endpoint_terminal_boxes.csv", endpoint_rows, digits)
        write_csv(output_dir / "concavity_terminal_boxes.csv", box_records, digits)
        with (output_dir / "concavity_slab_summary.csv").open(
            "w", newline="", encoding="utf-8") as stream:
            fields = [
                "index", "q_lo", "q_hi", "q_mid",
                "c_lower", "c_upper", "phi_second_lower", "phi_second_upper",
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
            "GO_PEABODY_ANALYTIC_COMPRESSION_CONCAVITY_CERTIFIED"
            if passed else "NO_GO_PEABODY_ANALYTIC_COMPRESSION"
        ),
        "proof_status": "CERTIFIED" if passed else "NOT_CERTIFIED",
        "proof_authority": "mpmath.iv outward-rounded interval arithmetic",
        "python_version": sys.version,
        "platform": platform.platform(),
        "mpmath_version": mp.__version__,
        "interval_precision_decimal_digits": dps,
        "endpoint": {
            "definition": "Phi(1)=lim_{e->1-} Phi(e), equivalently q=0",
            "x_panels": ENDPOINT_X_PANELS,
            "terminal_boxes": ENDPOINT_X_PANELS,
            "phi_one_enclosure": enclosure(endpoint_value, digits),
            "simple_rational_target": fracstr(ENDPOINT_TARGET),
            "exceeds_target": endpoint_pass,
        },
        "concavity": {
            "identity": "Phi''(e)=((1+q)^3/32)*integral((1+q)H_qq+2H_q)dx",
            "q_range": "0 <= q <= 1",
            "q_slabs": q_slabs,
            "x_panels_per_slab": x_panels,
            "terminal_boxes": q_slabs * x_panels,
            "simple_uniform_conclusion": f"Phi''(e) < -{fracstr(CONCAVITY_TARGET)} for 0<e<1",
            "worst_phi_second_upper": endpoint(worst_upper, "upper", digits),
            "all_slabs_below_target": all_concave,
            "subdivision_order": "reverse" if reverse else "forward",
            "slabs": slab_records,
        },
        "deduced_scalar_bound": "Phi(e) > (3/10000)e for every 0<e<1 by concavity and endpoint chords",
        "global_domain_diagnostics": diagnostics_json,
        "terminal_boxes": terminal_boxes,
        "maximum_terminal_boxes": MAX_BOXES,
        "elapsed_seconds": time.time() - start,
        "correction_sign": correction_sign,
    }

    certificate_path = output_dir / "peabody_concavity_certificate.json"
    certificate_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    data_bytes = sum(path.stat().st_size for path in output_dir.iterdir() if path.is_file())
    summary["certificate_data_bytes"] = data_bytes
    summary["certificate_size_pass"] = data_bytes <= MAX_DATA_BYTES
    summary["hard_stop_pass"] = terminal_boxes <= MAX_BOXES and summary["certificate_size_pass"]
    certificate_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    hash_path = output_dir / "certificate_file_hashes.json"
    hash_path.write_text(json.dumps({
        path.name: sha256(path)
        for path in sorted(output_dir.iterdir())
        if path.is_file() and path.name != hash_path.name
    }, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=2))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--precision-dps", type=int, default=DEFAULT_DPS)
    parser.add_argument("--reverse", action="store_true")
    parser.add_argument("--correction-sign", type=int, choices=[-1, 1], default=1)
    parser.add_argument("--no-boxes", action="store_true")
    parser.add_argument("--q-slabs", type=int, default=CONCAVITY_Q_SLABS)
    parser.add_argument("--x-panels", type=int, default=CONCAVITY_X_PANELS)
    args = parser.parse_args()
    result = run(
        args.output_dir,
        args.precision_dps,
        reverse=args.reverse,
        correction_sign=args.correction_sign,
        write_boxes=not args.no_boxes,
        q_slabs=args.q_slabs,
        x_panels=args.x_panels,
    )
    raise SystemExit(0 if result["proof_status"] == "CERTIFIED" else 1)


if __name__ == "__main__":
    main()
