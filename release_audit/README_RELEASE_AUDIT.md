# Confocal Peabody Formula, Additivity, and Release Audit

## Purpose

This directory is a **separate release-audit layer** for the frozen certified package at tag
`v1.0.0-certified`. It must not modify any of the 50 manifest-listed theorem-package files,
`PACKAGE_MANIFEST.json`, or `SHA256SUMS.txt`.

The audit concerns only the theorem:

> Meissner minimizes volume among width-one regular-tetrahedron confocal Peabodies.

It does not claim global Meissner extremality or improve the universal lower bound.

## Branch

```text
audit/confocal-peabody-formula-additivity-release
```

Create the branch from the immutable tag `v1.0.0-certified`, not from a later working branch.

## Finite audit tasks

1. Independently rederive the one-pair volume formula from the confocal geometry.
2. Audit every factor in the width-two to width-one normalization.
3. Audit the normal-sphere decomposition and the three opposite-edge contributions.
4. Replay the proof-critical Mathematica programs in separate fresh kernels.
5. Recursively reject unresolved symbolic expressions, except the frozen optional fixed-rho `Integrate`.
6. Recheck all central and tail certificate slabs with a second Python implementation that does not import the principal certifiers.
7. Run the matching R semantic audit.
8. Replace the short theorem note by a human-readable proof.
9. Assemble a final release-audit report and tag only after all gates pass.

## Quick start

From the repository root:

```bash
release_audit/scripts/run_python_release_audit.sh "$PWD"
```

On the Mac with Mathematica:

```bash
release_audit/scripts/run_mathematica_release_audit.sh "$PWD"
```

After installing R dependencies:

```bash
release_audit/scripts/run_R_release_audit.sh "$PWD"
```

When all three stages pass:

```bash
release_audit/scripts/finalize_release_audit.sh "$PWD"
```

## Python authority and independence

`python/independent_certificate_checker.py` does not import the principal central or tail
certifier. It uses a separate six-component derivative jet and reconstructs all slab bounds from
the archived exact rational endpoints.

`python/independent_one_pair_rederivation.py` independently implements:

- the two-dimensional confocal wedge/Gauss integral;
- the reduced one-dimensional integral;
- the fixed beam-coordinate integral;
- the stable q-chart integral;
- exact symbolic width normalization.

These are release audits. The frozen interval certificates remain proof authority.

## Mathematica protocol

The shell driver extracts a fresh copy of the frozen v4 checkpoint and launches each proof-critical
file in a new `wolframscript` process. It then runs both:

- a Wolfram Language recursive held-expression guard;
- an independent Python text/JSON guard.

The optional fixed-rho integral is expected to remain unevaluated and is explicitly excluded from
proof authority.

## R protocol

The R audit uses `Rmpfr`, `gmp`, and `jsonlite`. It checks formula samples, exact partition seams,
orientation independence, pair permutations, terminal-box metadata, and high-precision sample
containment. It is not proof authority.

Install on macOS with:

```bash
brew install gmp mpfr
Rscript -e 'install.packages(c("jsonlite","Rmpfr","gmp"), repos="https://cloud.r-project.org")'
```

## Mandatory final classification

A completed audit may use:

```text
PEABODY_RELEASE_AUDIT_PASS
```

only if every mandatory gate in `data/audit_task_matrix.csv` passes and the frozen baseline
verification still succeeds.

## Assistant-side preflight

Preliminary Python and static-validation outputs are archived under `preflight/assistant/`. They are
not final release-audit evidence. Fresh local outputs must be generated under `results/` on the audit
branch. Mathematica and R were not available in the assistant environment and must be run locally.

For the complete staged workflow and commit commands, read `LOCAL_RUN_CHECKLIST.md`.
