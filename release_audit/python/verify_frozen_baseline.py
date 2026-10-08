#!/usr/bin/env python3
"""Verify that the certified Peabody theorem package remains byte-for-byte frozen.

This verifier intentionally ignores the ``release_audit`` directory so that the
release-audit branch can add new material without altering the certified payload.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

EXPECTED_CLASSIFICATION = "GO_PEABODY_FAMILY_MINIMALITY_CERTIFIED"
EXPECTED_FILE_COUNT = 50
EXPECTED_TOTAL_BYTES = 4_193_688
EXPECTED_TAG = "v1.0.0-certified"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_value(repo: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def verify(repo: Path) -> dict[str, Any]:
    manifest_path = repo / "PACKAGE_MANIFEST.json"
    ledger_path = repo / "SHA256SUMS.txt"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"missing {manifest_path}")
    if not ledger_path.is_file():
        raise FileNotFoundError(f"missing {ledger_path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    records: list[dict[str, Any]] = []
    total_bytes = 0
    for entry in manifest.get("files", []):
        relative = Path(entry["path"])
        path = repo / relative
        exists = path.is_file()
        actual_bytes = path.stat().st_size if exists else None
        actual_hash = sha256(path) if exists else None
        size_ok = exists and actual_bytes == int(entry["bytes"])
        hash_ok = exists and actual_hash == entry["sha256"]
        total_bytes += actual_bytes or 0
        records.append(
            {
                "path": relative.as_posix(),
                "exists": exists,
                "expected_bytes": int(entry["bytes"]),
                "actual_bytes": actual_bytes,
                "size_ok": size_ok,
                "expected_sha256": entry["sha256"],
                "actual_sha256": actual_hash,
                "hash_ok": hash_ok,
            }
        )

    manifest_gate = (
        manifest.get("classification") == EXPECTED_CLASSIFICATION
        and manifest.get("file_count") == EXPECTED_FILE_COUNT
        and manifest.get("total_bytes") == EXPECTED_TOTAL_BYTES
        and len(records) == EXPECTED_FILE_COUNT
        and total_bytes == EXPECTED_TOTAL_BYTES
        and all(row["size_ok"] and row["hash_ok"] for row in records)
    )

    # Verify the portable checksum ledger independently. Lines have the usual
    # ``sha256  relative/path`` shape. Empty lines are ignored.
    ledger_rows: list[dict[str, Any]] = []
    for raw in ledger_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        pieces = line.split(maxsplit=1)
        if len(pieces) != 2:
            ledger_rows.append({"line": raw, "parse_ok": False})
            continue
        expected_hash, relative_text = pieces
        relative_text = relative_text.lstrip("* ")
        path = repo / relative_text
        actual_hash = sha256(path) if path.is_file() else None
        ledger_rows.append(
            {
                "path": relative_text,
                "parse_ok": True,
                "exists": path.is_file(),
                "expected_sha256": expected_hash,
                "actual_sha256": actual_hash,
                "hash_ok": actual_hash == expected_hash,
            }
        )
    ledger_gate = bool(ledger_rows) and all(
        row.get("parse_ok") and row.get("exists") and row.get("hash_ok")
        for row in ledger_rows
    )

    git_root = git_value(repo, "rev-parse", "--show-toplevel")
    tag_commit = git_value(repo, "rev-parse", f"{EXPECTED_TAG}^{{commit}}")
    head_commit = git_value(repo, "rev-parse", "HEAD")
    branch = git_value(repo, "branch", "--show-current")
    status = git_value(repo, "status", "--short")
    tag_exists = tag_commit is not None

    passed = manifest_gate and ledger_gate and tag_exists
    return {
        "classification": (
            "PEABODY_FROZEN_BASELINE_VERIFICATION_PASS"
            if passed
            else "PEABODY_FROZEN_BASELINE_VERIFICATION_FAIL"
        ),
        "pass": passed,
        "repo_root": str(repo.resolve()),
        "expected_tag": EXPECTED_TAG,
        "tag_exists": tag_exists,
        "tag_commit": tag_commit,
        "head_commit": head_commit,
        "current_branch": branch,
        "working_tree_status": status,
        "git_root": git_root,
        "manifest_gate": manifest_gate,
        "ledger_gate": ledger_gate,
        "manifest_summary": {
            "classification": manifest.get("classification"),
            "file_count": manifest.get("file_count"),
            "total_bytes": manifest.get("total_bytes"),
            "verified_file_count": len(records),
            "verified_total_bytes": total_bytes,
        },
        "manifest_records": records,
        "checksum_ledger_records": ledger_rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = verify(args.repo_root.resolve())
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    raise SystemExit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
