#!/usr/bin/env python3
"""Independent checker for the Peabody central and tail certificates.

The checker does not import the principal certifiers.  It reimplements the
stable q-chart and the required q/x derivatives using a single six-component
jet ``(f, f_q, f_x, f_xx, f_qx, f_qxx)``.  This is structurally different from
the nested dual/jet implementation in the proof-authority central certifier.

It independently rechecks:
  * all 16 local endpoint slabs;
  * all 43 accepted central-bulk slabs;
  * all 5 tail slabs (2,000 tail boxes);
  * exact partition coverage and seam endpoints;
  * terminal-box metadata and target inequalities.

The proof authority remains the frozen principal certificate.  This program is
an independent release checker using the same mpmath interval library.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import sys
import tempfile
import time
import zipfile
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath as mp
from mpmath.libmp import to_str

DEFAULT_DPS = 80
LOCAL_TARGET = Fraction(1, 2000)
BULK_TARGET = Fraction(1, 10_000_000)
TAIL_TARGET = Fraction(1, 20_000)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def frac(value: str | Fraction) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value)


def q_from_e(e: Fraction) -> Fraction:
    return (1 - e) / (1 + e)


def e_from_q(q: Fraction) -> Fraction:
    return (1 - q) / (1 + q)


def point(value: Fraction, iv: Any) -> Any:
    return iv.mpf(value.numerator) / value.denominator


def hull(lower: Fraction, upper: Fraction, iv: Any) -> Any:
    if lower > upper:
        lower, upper = upper, lower
    return iv.mpf([lower.numerator / lower.denominator, upper.numerator / upper.denominator])


def endpoint(value: Any, which: str, digits: int) -> str:
    return to_str(value._mpi_[0 if which == "lower" else 1], digits, strip_zeros=False)


@dataclass
class Jet:
    """Value and derivatives f_q, f_x, f_xx, f_qx, f_qxx."""

    v: Any
    q: Any
    x: Any
    xx: Any
    qx: Any
    qxx: Any

    def __add__(self, other: Any) -> "Jet":
        b = as_jet(other)
        return Jet(
            self.v + b.v,
            self.q + b.q,
            self.x + b.x,
            self.xx + b.xx,
            self.qx + b.qx,
            self.qxx + b.qxx,
        )

    __radd__ = __add__

    def __neg__(self) -> "Jet":
        return Jet(-self.v, -self.q, -self.x, -self.xx, -self.qx, -self.qxx)

    def __sub__(self, other: Any) -> "Jet":
        return self + (-as_jet(other))

    def __rsub__(self, other: Any) -> "Jet":
        return as_jet(other) + (-self)

    def __mul__(self, other: Any) -> "Jet":
        b = as_jet(other)
        a = self
        return Jet(
            a.v * b.v,
            a.q * b.v + a.v * b.q,
            a.x * b.v + a.v * b.x,
            a.xx * b.v + 2 * a.x * b.x + a.v * b.xx,
            a.qx * b.v + a.q * b.x + a.x * b.q + a.v * b.qx,
            a.qxx * b.v
            + a.xx * b.q
            + 2 * (a.qx * b.x + a.x * b.qx)
            + a.q * b.xx
            + a.v * b.qxx,
        )

    __rmul__ = __mul__

    def reciprocal(self) -> "Jet":
        a = self
        v = a.v
        return Jet(
            1 / v,
            -a.q / v**2,
            -a.x / v**2,
            2 * a.x**2 / v**3 - a.xx / v**2,
            2 * a.q * a.x / v**3 - a.qx / v**2,
            -a.qxx / v**2
            + 4 * a.x * a.qx / v**3
            + 2 * a.xx * a.q / v**3
            - 6 * a.q * a.x**2 / v**4,
        )

    def __truediv__(self, other: Any) -> "Jet":
        return self * as_jet(other).reciprocal()

    def __rtruediv__(self, other: Any) -> "Jet":
        return as_jet(other) * self.reciprocal()

    def __pow__(self, exponent: int) -> "Jet":
        if exponent == 0:
            return as_jet(1)
        if exponent < 0:
            return (self ** (-exponent)).reciprocal()
        result = as_jet(1)
        base = self
        n = exponent
        while n:
            if n & 1:
                result = result * base
            base = base * base
            n //= 2
        return result


_IV: Any = None


def as_jet(value: Any) -> Jet:
    if isinstance(value, Jet):
        return value
    interval = value if hasattr(value, "_mpi_") else _IV.mpf(value)
    z = _IV.mpf(0)
    return Jet(interval, z, z, z, z, z)


def sqrt_jet(value: Any) -> Jet:
    a = as_jet(value)
    s = _IV.sqrt(a.v)
    g1 = 1 / (2 * s)
    g2 = -1 / (4 * s**3)
    g3 = 3 / (8 * s**5)
    return Jet(
        s,
        g1 * a.q,
        g1 * a.x,
        g1 * a.xx + g2 * a.x**2,
        g1 * a.qx + g2 * a.q * a.x,
        g1 * a.qxx
        + g2 * (a.q * a.xx + 2 * a.x * a.qx)
        + g3 * a.q * a.x**2,
    )


def atan_jet(value: Any) -> Jet:
    a = as_jet(value)
    den = 1 + a.v * a.v
    g1 = 1 / den
    g2 = -2 * a.v / den**2
    g3 = (6 * a.v * a.v - 2) / den**3
    return Jet(
        _IV.atan2(a.v, _IV.mpf(1)),
        g1 * a.q,
        g1 * a.x,
        g1 * a.xx + g2 * a.x**2,
        g1 * a.qx + g2 * a.q * a.x,
        g1 * a.qxx
        + g2 * (a.q * a.xx + 2 * a.x * a.qx)
        + g3 * a.q * a.x**2,
    )


@dataclass(frozen=True)
class Constants:
    iv: Any
    sqrt2: Any
    kappa: Any
    K: Any
    psi0: Any


def setup(dps: int) -> Constants:
    if dps < 50:
        raise ValueError("precision must be at least 50 decimal digits")
    mp.iv.dps = dps
    iv = mp.iv
    sqrt2 = iv.sqrt(2)
    kappa = 1 + sqrt2
    K = kappa * kappa
    alpha = iv.atan2(2 * sqrt2, iv.mpf(1))
    psi0 = -(2 * iv.pi / iv.sqrt(3)) * alpha
    return Constants(iv, sqrt2, kappa, K, psi0)


def stable_jet(Q_value: Any, X_value: Any, c: Constants, q_derivative: bool, x_derivative: bool) -> Jet:
    global _IV
    _IV = c.iv
    z = c.iv.mpf(0)
    Q = Jet(Q_value, c.iv.mpf(1) if q_derivative else z, z, z, z, z)
    X = Jet(X_value, z, c.iv.mpf(1) if x_derivative else z, z, z, z)
    one = as_jet(1)
    K = as_jet(c.K)
    sqrt2 = as_jet(c.sqrt2)
    kappa = as_jet(c.kappa)

    D = sqrt_jet(K * K + Q * Q)
    R = sqrt_jet(K * K + Q * Q - 2 * K * Q * X * X)
    T = sqrt_jet(2 * K * (K * K + Q * Q) + K * K * (one - Q) * (one - Q) * X * X)
    delta = 2 * K * (one - X * X) / (R + K - Q)
    M = K * (Q - 2 * K * X * X) / (R + K) + (one - K) * R - K * K - Q * R - Q - Q * Q
    primary = -16 * sqrt2 * kappa * (K * K + Q * Q) / (R * T)
    correction = -4 * K * (one - Q * Q) * (K * K + Q * Q) * delta * M / (R * T * T * T)
    algebraic = -4 * K * (one - Q * Q) * (K * K + Q * Q) * delta / (R * T * T)
    Z = K * ((one + Q) * D + (one - Q) * R) / (T * (K + Q + D))
    return (primary + correction) * atan_jet(Z) + algebraic


def integrate_point(q: Fraction, c: Constants, x_panels: int) -> Any:
    h = c.iv.mpf(1) / x_panels
    q_value = point(q, c.iv)
    total = c.iv.mpf(0)
    for panel in range(x_panels):
        midpoint = c.iv.mpf(2 * panel + 1) / (2 * x_panels)
        box = c.iv.mpf([panel, panel + 1]) / x_panels
        at_mid = stable_jet(q_value, midpoint, c, False, True)
        on_box = stable_jet(q_value, box, c, False, True)
        total += h * at_mid.v + h**3 * on_box.xx / 24
    return total


def integrate_q_derivative(q_lo: Fraction, q_hi: Fraction, c: Constants, x_panels: int) -> Any:
    h = c.iv.mpf(1) / x_panels
    q_value = hull(q_lo, q_hi, c.iv)
    total = c.iv.mpf(0)
    for panel in range(x_panels):
        midpoint = c.iv.mpf(2 * panel + 1) / (2 * x_panels)
        box = c.iv.mpf([panel, panel + 1]) / x_panels
        at_mid = stable_jet(q_value, midpoint, c, True, True)
        on_box = stable_jet(q_value, box, c, True, True)
        total += h * at_mid.q + h**3 * on_box.qxx / 24
    return total


def direct_tail_slab(index: int, q_den: int, c: Constants, x_panels: int) -> Any:
    Q = c.iv.mpf([index, index + 1]) / q_den
    width = c.iv.mpf(1) / x_panels
    psi = c.iv.mpf(0)
    for panel in range(x_panels):
        X = c.iv.mpf([panel, panel + 1]) / x_panels
        psi += stable_jet(Q, X, c, False, False).v * width
    return (psi - c.psi0) / 8


def exact_cover(intervals: list[tuple[Fraction, Fraction]], start: Fraction, end: Fraction) -> bool:
    ordered = sorted(intervals)
    if not ordered or ordered[0][0] != start or ordered[-1][1] != end:
        return False
    return all(ordered[i][1] == ordered[i + 1][0] for i in range(len(ordered) - 1))


def csv_metadata(path: Path, slab_field: str, panels_per_slab: int) -> dict[str, Any]:
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    per_slab: dict[str, set[int]] = {}
    for row in rows:
        key = row[slab_field]
        per_slab.setdefault(key, set()).add(int(row["x_panel_index"]))
    panels_ok = all(indices == set(range(panels_per_slab)) for indices in per_slab.values())
    return {
        "row_count": len(rows),
        "slab_count": len(per_slab),
        "panels_per_slab_expected": panels_per_slab,
        "panels_per_slab_ok": panels_ok,
    }


def locate_tail_package(repo: Path) -> tuple[tempfile.TemporaryDirectory[str], Path]:
    archive = repo / "frozen_inputs/confocal_peabody_tail_first_gate_2026-09-30.zip"
    holder: tempfile.TemporaryDirectory[str] = tempfile.TemporaryDirectory(prefix="peabody_tail_release_audit_")
    with zipfile.ZipFile(archive) as zf:
        zf.extractall(holder.name)
    children = [path for path in Path(holder.name).iterdir() if path.is_dir()]
    if len(children) != 1:
        holder.cleanup()
        raise RuntimeError("tail archive must contain one package root")
    return holder, children[0]


def run(repo: Path, output: Path, dps: int) -> dict[str, Any]:
    start = time.time()
    c = setup(dps)
    central_path = repo / "certificates/peabody_central_certificate.json"
    central = json.loads(central_path.read_text(encoding="utf-8"))
    holder, tail_root = locate_tail_package(repo)
    try:
        tail_path = tail_root / "data/certificate_80dps/tail_certificate.json"
        tail = json.loads(tail_path.read_text(encoding="utf-8"))

        local_results: list[dict[str, Any]] = []
        for slab in central["local_endpoint"]["slabs"]:
            q_lo, q_hi = frac(slab["q_lo"]), frac(slab["q_hi"])
            dpsi = integrate_q_derivative(q_lo, q_hi, c, int(central["local_endpoint"]["x_panels"]))
            Q = hull(q_lo, q_hi, c.iv)
            dq_de = -(1 + Q) * (1 + Q) / 2
            phi_prime = dpsi * dq_de / 8
            local_results.append(
                {
                    "index": int(slab["index"]),
                    "lower": endpoint(phi_prime, "lower", dps + 20),
                    "upper": endpoint(phi_prime, "upper", dps + 20),
                    "target_pass": bool(phi_prime.a > point(LOCAL_TARGET, c.iv).b),
                }
            )

        bulk_results: list[dict[str, Any]] = []
        for slab in central["bulk"]["slabs"]:
            q_lo, q_hi, q_mid = frac(slab["q_lo"]), frac(slab["q_hi"]), frac(slab["q_mid"])
            psi_mid = integrate_point(q_mid, c, int(central["bulk"]["x_panels"]))
            dpsi = integrate_q_derivative(q_lo, q_hi, c, int(central["bulk"]["x_panels"]))
            delta_q = hull(q_lo - q_mid, q_hi - q_mid, c.iv)
            phi = (psi_mid + delta_q * dpsi - c.psi0) / 8
            bulk_results.append(
                {
                    "index": int(slab["index"]),
                    "lower": endpoint(phi, "lower", dps + 20),
                    "upper": endpoint(phi, "upper", dps + 20),
                    "target_pass": bool(phi.a > point(BULK_TARGET, c.iv).b),
                }
            )

        tail_results: list[dict[str, Any]] = []
        for slab in tail["slabs"]:
            phi = direct_tail_slab(
                int(slab["q_slab_index"]),
                int(slab["q_den"]),
                c,
                int(tail["x_panels_per_slab"]),
            )
            tail_results.append(
                {
                    "index": int(slab["q_slab_index"]),
                    "lower": endpoint(phi, "lower", dps + 20),
                    "upper": endpoint(phi, "upper", dps + 20),
                    "target_pass": bool(phi.a > point(TAIL_TARGET, c.iv).b),
                }
            )

        local_cover = exact_cover(
            [(frac(s["e_lo"]), frac(s["e_hi"])) for s in central["local_endpoint"]["slabs"]],
            Fraction(0),
            Fraction(1, 100),
        )
        bulk_cover = exact_cover(
            [(frac(s["e_lo"]), frac(s["e_hi"])) for s in central["bulk"]["slabs"]],
            Fraction(1, 100),
            Fraction(199, 200),
        )
        tail_cover = exact_cover(
            [
                (Fraction(int(s["q_lo_num"]), int(s["q_den"])), Fraction(int(s["q_hi_num"]), int(s["q_den"])))
                for s in tail["slabs"]
            ],
            Fraction(0),
            Fraction(1, 399),
        )

        metadata = {
            "central_local": csv_metadata(repo / "data/central_local_terminal_boxes.csv", "local_q_slab_index", 10),
            "central_bulk": csv_metadata(repo / "data/central_bulk_terminal_boxes.csv", "bulk_slab_index", 10),
            "tail": csv_metadata(tail_root / "data/certificate_80dps/tail_terminal_boxes.csv", "q_slab_index", 400),
        }
        metadata_gate = (
            metadata["central_local"]["row_count"] == 160
            and metadata["central_bulk"]["row_count"] == 430
            and metadata["tail"]["row_count"] == 2000
            and all(item["panels_per_slab_ok"] for item in metadata.values())
        )

        local_gate = len(local_results) == 16 and all(item["target_pass"] for item in local_results)
        bulk_gate = len(bulk_results) == 43 and all(item["target_pass"] for item in bulk_results)
        tail_gate = len(tail_results) == 5 and all(item["target_pass"] for item in tail_results)
        coverage_gate = local_cover and bulk_cover and tail_cover and q_from_e(Fraction(199, 200)) == Fraction(1, 399)
        archived_gate = (
            central.get("classification") == "GO_PEABODY_CENTRAL_PHI_POSITIVITY_CERTIFIED"
            and tail.get("classification") == "GO_PEABODY_TAIL_PHI_POSITIVITY_CERTIFIED"
        )
        passed = local_gate and bulk_gate and tail_gate and coverage_gate and metadata_gate and archived_gate

        result = {
            "classification": (
                "PEABODY_INDEPENDENT_CERTIFICATE_CHECK_PASS"
                if passed
                else "PEABODY_INDEPENDENT_CERTIFICATE_CHECK_FAIL"
            ),
            "pass": passed,
            "scope": "width-one regular-tetrahedron confocal Peabodies only",
            "python_version": sys.version,
            "platform": platform.platform(),
            "mpmath_version": mp.__version__,
            "interval_precision_decimal_digits": dps,
            "implementation_independence": "does not import the principal certifiers; uses a separate six-component q/x jet",
            "local_gate": local_gate,
            "bulk_gate": bulk_gate,
            "tail_gate": tail_gate,
            "coverage_gate": coverage_gate,
            "terminal_metadata_gate": metadata_gate,
            "archived_classification_gate": archived_gate,
            "weakest_local_lower": min((item["lower"] for item in local_results), key=mp.mpf),
            "weakest_bulk_lower": min((item["lower"] for item in bulk_results), key=mp.mpf),
            "weakest_tail_lower": min((item["lower"] for item in tail_results), key=mp.mpf),
            "local_results": local_results,
            "bulk_results": bulk_results,
            "tail_results": tail_results,
            "coverage": {
                "local_0_to_1_over_100": local_cover,
                "bulk_1_over_100_to_199_over_200": bulk_cover,
                "tail_q_0_to_1_over_399": tail_cover,
                "central_tail_seam_exact": q_from_e(Fraction(199, 200)) == Fraction(1, 399),
            },
            "terminal_box_metadata": metadata,
            "source_hashes": {
                "central_certificate": sha256(central_path),
                "tail_archive": sha256(repo / "frozen_inputs/confocal_peabody_tail_first_gate_2026-09-30.zip"),
                "tail_certificate": sha256(tail_path),
            },
            "elapsed_seconds": time.time() - start,
            "trust_boundary": "Python exact Fraction control flow plus mpmath.iv outward-rounded interval arithmetic",
        }
    finally:
        holder.cleanup()

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--precision-dps", type=int, default=DEFAULT_DPS)
    args = parser.parse_args()
    result = run(args.repo_root.resolve(), args.output.resolve(), args.precision_dps)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
