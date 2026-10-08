# Git instructions: Peabody analytical compression

The safest branch starts from the immutable release-audited tag:

```text
v1.0.0-release-audited
```

Recommended branch:

```text
work/confocal-peabody-analytic-compression
```

Recommended commit:

```text
Compress the Peabody positivity proof through concavity
```

## Create the branch and import the package

Assume:

```text
Repository: ~/github/confocal-peabody-family-minimality
Package ZIP: ~/Downloads/confocal_peabody_analytic_compression_2026-10-01.zip
```

Run:

```bash
REPO="$HOME/github/confocal-peabody-family-minimality"
```

```bash
ZIP="$HOME/Downloads/confocal_peabody_analytic_compression_2026-10-01.zip"
```

```bash
STAGE="$(mktemp -d)"
```

```bash
cd "$REPO"
```

```bash
git fetch origin --prune --tags
```

```bash
git status --short
```

Continue only with a clean worktree.

```bash
git switch -c work/confocal-peabody-analytic-compression v1.0.0-release-audited
```

```bash
unzip -q "$ZIP" -d "$STAGE"
```

```bash
SRC="$STAGE/confocal_peabody_analytic_compression_2026-10-01"
```

```bash
rm -rf research/confocal_peabody_analytic_compression
```

```bash
mkdir -p research/confocal_peabody_analytic_compression
```

```bash
cp -R "$SRC"/. research/confocal_peabody_analytic_compression/
```

## Validate before staging

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/confocal_peabody_analytic_compression/python/validate_analytic_compression_package.py --package-dir research/confocal_peabody_analytic_compression
```

Expected:

```text
PEABODY_ANALYTIC_COMPRESSION_PACKAGE_PASS
```

## Commit

```bash
git add research/confocal_peabody_analytic_compression
```

```bash
git diff --cached --stat
```

```bash
git status --short
```

```bash
git commit -m "Compress the Peabody positivity proof through concavity"
```

```bash
git push -u origin work/confocal-peabody-analytic-compression
```

## Manuscript integration later

After review, copy the revised TeX and PDF from

```text
research/confocal_peabody_analytic_compression/manuscript/
```

onto the manuscript branch in a separate commit. Do not rewrite the frozen theorem tag or the release-audited tag.
