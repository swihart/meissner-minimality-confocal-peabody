#!/usr/bin/env python3
"""Assemble the final release-audit gate from independent outputs."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-report", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    audit = repo / "release_audit"

    paths = {
        "baseline": audit / "results/python/frozen_baseline_verification.json",
        "formula": audit / "results/python/independent_one_pair_rederivation.json",
        "certificate": audit / "results/python/independent_certificate_check.json",
        "wolfram": audit / "results/mathematica/wolfram_recursive_guard_summary.json",
        "r": audit / "results/R/peabody_release_semantic_audit.json",
    }
    loaded: dict[str, Any] = {}
    gates: dict[str, bool] = {}
    for key, path in paths.items():
        if path.is_file():
            loaded[key] = read_json(path)
            gates[key] = bool(loaded[key].get("pass"))
        else:
            loaded[key] = {"missing": True, "path": str(path)}
            gates[key] = False

    proof_path = audit / "notes/04_human_readable_proof_draft.md"
    proof_text = proof_path.read_text(encoding="utf-8") if proof_path.is_file() else ""
    proof_gate = proof_path.is_file() and "[TODO]" not in proof_text and "TODO:" not in proof_text
    gates["human_readable_proof"] = proof_gate

    passed = all(gates.values())
    classification = "PEABODY_RELEASE_AUDIT_PASS" if passed else "PEABODY_RELEASE_AUDIT_INCOMPLETE"
    result = {
        "classification": classification,
        "pass": passed,
        "gates": gates,
        "inputs": loaded,
        "human_readable_proof": {
            "path": str(proof_path),
            "exists": proof_path.is_file(),
            "sha256": sha256(proof_path) if proof_path.is_file() else None,
            "no_todo_markers": proof_gate,
        },
        "release_scope": "Meissner minimality among width-one regular-tetrahedron confocal Peabodies only",
        "exclusions": [
            "global Meissner extremality",
            "a universal lower-bound improvement",
            "arbitrary Meissner polyhedra",
            "Peabodies based on arbitrary self-dual ball polyhedra",
        ],
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Confocal Peabody Formula, Additivity, and Release Audit",
        "",
        f"**Classification:** `{classification}`",
        "",
        "## Mandatory gates",
        "",
        "| Gate | Result |",
        "|---|---:|",
    ]
    for key, value in gates.items():
        lines.append(f"| `{key}` | {'PASS' if value else 'PENDING/FAIL'} |")
    lines.extend(
        [
            "",
            "## Exact scope",
            "",
            "This release audit concerns only width-one regular-tetrahedron confocal Peabodies.",
            "It does not solve the global three-dimensional Blaschke-Lebesgue problem.",
            "",
            "## Output hashes",
            "",
        ]
    )
    for key, path in paths.items():
        lines.append(f"- `{key}`: `{sha256(path) if path.is_file() else 'MISSING'}`")
    lines.append(f"- `human_readable_proof`: `{sha256(proof_path) if proof_path.is_file() else 'MISSING'}`")
    lines.append("")
    args.output_report.parent.mkdir(parents=True, exist_ok=True)
    args.output_report.write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps(result, indent=2))
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
