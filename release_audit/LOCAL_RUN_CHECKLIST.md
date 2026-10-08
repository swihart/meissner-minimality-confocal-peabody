# Local release-audit run checklist

This checklist assumes the frozen theorem package is already committed and tagged as
`v1.0.0-certified` in:

```text
~/github/confocal-peabody-family-minimality
```

All release-audit work belongs under `release_audit/` on:

```text
audit/confocal-peabody-formula-additivity-release
```

## 1. Confirm the frozen baseline

```bash
cd "$HOME/github/confocal-peabody-family-minimality"
git status --short
git rev-parse --verify 'v1.0.0-certified^{commit}'
git show --stat --oneline v1.0.0-certified
```

The working tree must be clean before bootstrapping the branch.

## 2. Bootstrap the audit branch

Use the downloadable bootstrap script or the copy inside `release_audit/scripts/`.
The bootstrap:

- verifies the audit scaffold manifest and checksum ledger;
- creates the audit branch from `v1.0.0-certified`;
- copies the scaffold only under `release_audit/`;
- verifies the frozen theorem payload;
- creates the first audit commit.

## 3. Inspect dependencies

```bash
cd "$HOME/github/confocal-peabody-family-minimality"
release_audit/scripts/check_release_audit_dependencies.sh
```

## 4. Run and commit the independent Python audits

```bash
release_audit/scripts/run_python_release_audit.sh "$PWD"

git add \
  release_audit/results/python \
  release_audit/notes/01_one_pair_volume_rederivation.md \
  release_audit/notes/02_width_normalization_line_audit.md \
  release_audit/notes/03_three_pair_additivity_audit.md

git diff --cached --stat
git commit -m "Independently audit the Peabody formulas and certificates"
```

## 5. Run and commit the Mathematica fresh-kernel audit

Run each proof-critical file in a separate `wolframscript` process:

```bash
WOLFRAMSCRIPT_BIN="/Applications/Mathematica.app/Contents/MacOS/wolframscript" \
release_audit/scripts/run_mathematica_release_audit.sh "$PWD"

git add release_audit/results/mathematica
git diff --cached --stat
git commit -m "Replay proof-critical Peabody Mathematica checks"
```

The script recursively scans output expressions. The only permitted unresolved expression is the
already-frozen optional fixed-`rho` `Integrate`, which remains outside proof authority.

## 6. Run and commit the R semantic audit

Install the external libraries and R packages once:

```bash
brew install gmp mpfr
Rscript -e 'install.packages(c("jsonlite","Rmpfr","gmp"), repos="https://cloud.r-project.org")'
```

Then run:

```bash
release_audit/scripts/run_R_release_audit.sh "$PWD"

git add release_audit/results/R release_audit/R
git diff --cached --stat
git commit -m "Add independent R semantic audit"
```

The R audit is not proof authority. It independently checks formulas, normalization, orientation
independence, exact partition coverage, terminal-box metadata, and high-precision sample containment.

## 7. Review and commit the human-readable proof

Read and edit only the release-audit proof document:

```text
release_audit/notes/04_human_readable_proof_draft.md
```

Do not edit the frozen theorem payload. After review:

```bash
git add release_audit/notes/04_human_readable_proof_draft.md
git diff --cached --stat
git commit -m "Rewrite the Peabody family minimality proof"
```

## 8. Finalize the release audit

```bash
release_audit/scripts/finalize_release_audit.sh "$PWD"
release_audit/scripts/build_release_audit_manifest.sh "$PWD"

git add \
  release_audit/RELEASE_AUDIT_REPORT.md \
  release_audit/RELEASE_AUDIT_MANIFEST.json \
  release_audit/results

git diff --cached --stat
git commit -m "Complete the confocal Peabody release audit"
```

The final classification must be:

```text
PEABODY_RELEASE_AUDIT_PASS
```

## 9. Push and tag

```bash
git push -u origin audit/confocal-peabody-formula-additivity-release

git tag -a v1.0.0-release-audited \
  -m "Independent formula, additivity, certificate, Mathematica, and R audit"

git push origin v1.0.0-release-audited
```

The original `v1.0.0-certified` tag remains the immutable theorem freeze. The later tag records the
independent review layer.
