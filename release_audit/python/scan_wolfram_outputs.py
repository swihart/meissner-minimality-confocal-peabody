#!/usr/bin/env python3
"""Recursively scan fresh Mathematica outputs for unresolved expressions.

The only unresolved expression allowed by the frozen campaign is the optional
fixed-rho ``Integrate`` in ``rt_sector_fixed_rho_primitive.wl``.  It must remain
explicitly classified as unevaluated and is not proof authority.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

FORBIDDEN_TOKENS = (
    "$Aborted",
    "$Failed",
    "Indeterminate",
    "ComplexInfinity",
    "DirectedInfinity",
    "Undefined",
    "Failure[",
    "Missing[",
)
UNRESOLVED_HEADS = (
    "Integrate[",
    "NIntegrate[",
    "Inactive[Integrate]",
    "FullSimplify[",
    "Reduce[",
    "Resolve[",
    "FindInstance[",
)
OPTIONAL_INTEGRATE_RELATIVE_SUFFIX = "mathematica_output_primitive_probe_v4/rt_sector_fixed_rho_primitive.wl"
PLACEHOLDER_PATTERN = re.compile(r"\b[A-Za-z$][A-Za-z0-9$]*Expr\b")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.output_root.resolve()

    required_summaries = {
        "component": root / "mathematica_output_component_diagnostic_v4/component_diagnostic_summary.json",
        "compressed": root / "mathematica_output_compressed_audit_v4/compressed_audit_summary.json",
        "primitive": root / "mathematica_output_primitive_probe_v4/primitive_probe_summary.json",
        "interval": root / "mathematica_output_interval_inputs_v4/interval_input_summary.json",
    }
    summaries: dict[str, Any] = {}
    summary_gate = True
    for key, path in required_summaries.items():
        if not path.is_file():
            summaries[key] = {"missing": True, "path": str(path)}
            summary_gate = False
            continue
        data = load_json(path)
        summaries[key] = data

    summary_gate = summary_gate and bool(summaries["component"].get("Pass"))
    summary_gate = summary_gate and bool(summaries["compressed"].get("Pass"))
    summary_gate = summary_gate and bool(summaries["primitive"].get("ExactLowComplexityObstructionPass"))
    summary_gate = summary_gate and bool(summaries["interval"].get("NumericalScoutPass"))
    summary_gate = summary_gate and summaries["interval"].get("ProofStatus") == "NOT_CERTIFIED"

    file_rows: list[dict[str, Any]] = []
    unexpected_gate = True
    optional_integrate_seen = False
    for path in sorted(root.rglob("*.wl")):
        relative = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        forbidden = [token for token in FORBIDDEN_TOKENS if token in text]
        unresolved = [token for token in UNRESOLVED_HEADS if token in text]
        placeholders = sorted(set(PLACEHOLDER_PATTERN.findall(text)))
        optional = relative.endswith(OPTIONAL_INTEGRATE_RELATIVE_SUFFIX)
        if optional and "Integrate[" in unresolved:
            optional_integrate_seen = True
            unresolved = [token for token in unresolved if token != "Integrate["]
        pass_file = not forbidden and not unresolved and not placeholders
        unexpected_gate = unexpected_gate and pass_file
        file_rows.append(
            {
                "path": relative,
                "bytes": path.stat().st_size,
                "optional_fixed_rho_integrate_file": optional,
                "forbidden_tokens": forbidden,
                "unexpected_unresolved_heads": unresolved,
                "unresolved_placeholder_symbols": placeholders,
                "pass": pass_file,
            }
        )

    optional_status = summaries.get("primitive", {}).get("FixedRhoIntegrateStatus")
    optional_gate = optional_integrate_seen and optional_status in {"COMPLETED", "UNEVALUATED_INTEGRATE"}
    # The old v4 summary calls the top-level Times[Integrate[...]] expression
    # "COMPLETED".  The recursive scan above is the authoritative release-audit
    # classification and requires the nested Integrate to be present only here.

    passed = summary_gate and unexpected_gate and optional_gate
    result = {
        "classification": (
            "PEABODY_WOLFRAM_RECURSIVE_GUARD_PASS"
            if passed
            else "PEABODY_WOLFRAM_RECURSIVE_GUARD_FAIL"
        ),
        "pass": passed,
        "output_root": str(root),
        "required_summary_gate": summary_gate,
        "unexpected_unresolved_expression_gate": unexpected_gate,
        "optional_fixed_rho_integrate_seen": optional_integrate_seen,
        "optional_fixed_rho_summary_status": optional_status,
        "optional_fixed_rho_gate": optional_gate,
        "summaries": summaries,
        "wolfram_files": file_rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
