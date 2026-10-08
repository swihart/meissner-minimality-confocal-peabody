#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-dir", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.package_dir.resolve()
    manifest_path = root / "CHECKPOINT_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    checks: dict[str, bool] = {}
    expected = {entry["path"]: entry for entry in manifest["files"]}
    actual_payload = {
        str(path.relative_to(root))
        for path in root.rglob("*")
        if path.is_file() and path.name not in {"CHECKPOINT_MANIFEST.json", "SHA256SUMS.txt"}
    }
    checks["payload_file_set_exact"] = actual_payload == set(expected)

    file_checks = []
    for rel, entry in sorted(expected.items()):
        path = root / rel
        ok = path.is_file() and path.stat().st_size == entry["bytes"] and sha256(path) == entry["sha256"]
        file_checks.append(ok)
    checks["all_payload_sizes_and_hashes"] = all(file_checks)

    preflight = json.loads((root / "preflight/assistant_mpfr_runtime_only/mpfr_certificate_audit.json").read_text())
    formula = json.loads((root / "data/formula_derivation_identity_audit.json").read_text())
    progress = json.loads((root / "data/reviewer_point_progress.json").read_text())
    checks["assistant_mpfr_preflight_pass"] = preflight.get("pass") is True
    checks["exact_formula_identity_audit_pass"] = formula.get("pass") is True
    checks["points_1_and_3_manuscript_integrated"] = progress["points"]["1"]["percent"] >= 90 and progress["points"]["3"]["percent"] >= 90
    checks["points_4_and_5_closed"] = progress["points"]["4"]["closed"] is True and progress["points"]["5"]["closed"] is True
    checks["no_shape_search_reopened"] = progress.get("shape_search_reopened") is False
    checks["no_semi_regular_extension"] = progress.get("semi_regular_extension_started") is False

    c_source = (root / "mpfr/peabody_mpfr_concavity.c").read_text(encoding="utf-8")
    build = (root / "mpfr/build_mpfr_certificate.sh").read_text(encoding="utf-8")
    checks["official_mpfr_header_required"] = "#include <mpfr.h>" in c_source and "mpfr_compat.h" not in c_source
    checks["build_has_no_abi_fallback"] = "ABI fallback" not in build and "official MPFR development header not found" in build
    checks["local_replay_not_preclaimed"] = progress["points"]["2"]["closed"] is False
    checks["revision_manuscript_present"] = (root / "manuscript/main_dcg_revision_checkpoint.tex").is_file() and (root / "manuscript/main_dcg_revision_checkpoint.pdf").is_file()

    passed = all(checks.values())
    result = {
        "classification": "PEABODY_DCG_FIVE_POINT_CHECKPOINT_PACKAGE_PASS" if passed else "PEABODY_DCG_FIVE_POINT_CHECKPOINT_PACKAGE_FAIL",
        "pass": passed,
        "checks": checks,
        "payload_file_count": len(expected),
        "payload_bytes": sum(entry["bytes"] for entry in expected.values()),
    }
    print(json.dumps(result, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
