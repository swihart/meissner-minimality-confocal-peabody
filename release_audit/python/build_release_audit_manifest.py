#!/usr/bin/env python3
"""Create a deterministic manifest for the release_audit directory."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

CONTROL_FILES = {"RELEASE_AUDIT_MANIFEST.json", "SHA256SUMS.txt"}
IGNORED_PARTS = {"__pycache__", ".DS_Store"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.audit_root.resolve()
    output = args.output.resolve()
    files = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if relative in CONTROL_FILES or any(part in IGNORED_PARTS for part in path.parts):
            continue
        files.append({"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)})
    manifest = {
        "classification": "CONFOCAL_PEABODY_RELEASE_AUDIT_SCAFFOLD_MANIFEST",
        "scope": "Confocal Peabody Formula, Additivity, and Release Audit",
        "frozen_parent_tag": "v1.0.0-certified",
        "audit_branch": "audit/confocal-peabody-formula-additivity-release",
        "control_files_excluded": sorted(CONTROL_FILES),
        "file_count": len(files),
        "total_bytes": sum(item["bytes"] for item in files),
        "files": files,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
