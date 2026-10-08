# Git workflow for the release-audit branch

## Branch creation

The branch must begin at the immutable certified tag:

```bash
cd "$HOME/github/confocal-peabody-family-minimality"
git status --short
git rev-parse --verify 'v1.0.0-certified^{commit}'
git switch -c audit/confocal-peabody-formula-additivity-release v1.0.0-certified
```

Do not modify or move `v1.0.0-certified`.

## Recommended commits

1. `Add Peabody formula and release audit scaffold`
2. `Independently rederive the Peabody pair formula`
3. `Audit Peabody width normalization and pair additivity`
4. `Replay proof-critical Peabody Mathematica checks`
5. `Add independent Peabody certificate checker`
6. `Add independent R semantic audit`
7. `Rewrite the Peabody family minimality proof`
8. `Complete the confocal Peabody release audit`

## Push the audit branch

```bash
git push -u origin audit/confocal-peabody-formula-additivity-release
```

## Final tag, only after every gate passes

```bash
git tag -a v1.0.0-release-audited \
  -m "Independent formula, additivity, certificate, Mathematica, and R audit"
git push origin v1.0.0-release-audited
```

A pull request may then merge the audit material to `main`. The original certified tag remains the
unaltered theorem freeze; the release-audited tag records the independent review layer.
