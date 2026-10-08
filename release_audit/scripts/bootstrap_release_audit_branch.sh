#!/usr/bin/env bash
set -euo pipefail

if [[ "$#" -ne 2 ]]; then
  printf '%s\n' 'usage: bootstrap_release_audit_branch.sh AUDIT_SCAFFOLD_ZIP REPO_PATH'
  false
fi

AUDIT_ZIP="$1"
REPO="$2"
BRANCH="audit/confocal-peabody-formula-additivity-release"
TAG="v1.0.0-certified"

if [[ ! -f "$AUDIT_ZIP" ]]; then
  printf '%s\n' "Audit scaffold ZIP not found: $AUDIT_ZIP"
  false
fi
if [[ ! -d "$REPO/.git" ]]; then
  printf '%s\n' "Git repository not found: $REPO"
  false
fi

REPO="$(cd "$REPO" && pwd)"
git -C "$REPO" rev-parse --verify "$TAG^{commit}" >/dev/null
if [[ -n "$(git -C "$REPO" status --short)" ]]; then
  printf '%s\n' 'The repository is not clean. Preserve or commit current work before creating the audit branch.'
  git -C "$REPO" status --short
  false
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
unzip -q "$AUDIT_ZIP" -d "$TMP"
ROOT_COUNT="$(find "$TMP" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"
if [[ "$ROOT_COUNT" -ne 1 ]]; then
  printf '%s\n' 'The audit ZIP must contain exactly one top-level directory.'
  printf '%s\n' "Found $ROOT_COUNT directories."
  false
fi
ROOT="$(find "$TMP" -mindepth 1 -maxdepth 1 -type d | head -n 1)"

python3 - "$ROOT" <<'PY'
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
manifest_path = root / "RELEASE_AUDIT_MANIFEST.json"
ledger_path = root / "SHA256SUMS.txt"
if not manifest_path.is_file() or not ledger_path.is_file():
    raise SystemExit("audit scaffold control files are missing")
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
for row in manifest.get("files", []):
    path = root / row["path"]
    if not path.is_file():
        raise SystemExit(f"manifest file missing: {row['path']}")
    data = path.read_bytes()
    if len(data) != int(row["bytes"]):
        raise SystemExit(f"manifest size mismatch: {row['path']}")
    digest = hashlib.sha256(data).hexdigest()
    if digest != row["sha256"]:
        raise SystemExit(f"manifest hash mismatch: {row['path']}")
for raw in ledger_path.read_text(encoding="utf-8").splitlines():
    if not raw.strip():
        continue
    digest, rel = raw.split(maxsplit=1)
    rel = rel.lstrip("* ")
    path = root / rel
    if not path.is_file():
        raise SystemExit(f"checksum-ledger file missing: {rel}")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != digest:
        raise SystemExit(f"checksum-ledger mismatch: {rel}")
print("PEABODY_RELEASE_AUDIT_SCAFFOLD_ARCHIVE_PASS")
PY

if git -C "$REPO" show-ref --verify --quiet "refs/heads/$BRANCH"; then
  git -C "$REPO" switch "$BRANCH"
else
  git -C "$REPO" switch -c "$BRANCH" "$TAG"
fi

if [[ -e "$REPO/release_audit" ]]; then
  printf '%s\n' "$REPO/release_audit already exists; refusing to overwrite it."
  false
fi

mkdir -p "$REPO/release_audit"
cp -R "$ROOT"/. "$REPO/release_audit"/

"$REPO/release_audit/scripts/verify_frozen_baseline.sh" "$REPO"

git -C "$REPO" add release_audit
git -C "$REPO" diff --cached --stat
git -C "$REPO" commit -m "Add Peabody formula and release audit scaffold"
git -C "$REPO" status --short

printf '%s\n' "Created branch $BRANCH from $TAG."
printf '%s\n' 'Next: run release_audit/scripts/check_release_audit_dependencies.sh'
