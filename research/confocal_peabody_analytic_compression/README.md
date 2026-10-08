# Confocal Peabody analytical-compression checkpoint

## Principal result

```text
GO_PEABODY_ANALYTIC_COMPRESSION_CONCAVITY_CERTIFIED
```

This package replaces the earlier three-region local/bulk/tail positivity proposition for the one-pair scalar \(\Phi\) by three ordinary lemmas:

1. the parabolic endpoint extension satisfies \(\Phi(1)>3/10000\);
2. \(\Phi''(e)<-1/25000\) for every \(0<e<1\);
3. concavity gives \(\Phi(e)>3e/10000>0\).

The proof uses 324 outward-rounded terminal rectangles rather than the earlier 2,590-box direct positivity certificate. It is a proof compression, not a new Peabody search.

## Scope

The result concerns only width-one regular-tetrahedron confocal Peabodies. It does not prove global Meissner extremality, improve the universal lower bound, or establish a global six-patch theorem for semi-regular tetrahedral bases.

## Proof authority

The proof authority is:

- exact rational parameter partitions;
- the validated stable \(q=(1-e)/(1+e)\) fixed-interval formula;
- nested automatic differentiation through third order in \(q\) and second order in \(x\);
- outward-rounded `mpmath.iv` arithmetic at 80 decimal digits;
- the midpoint quadrature enclosure with an interval second-derivative remainder.

High-precision quadrature, sampled numerical differentiation, R, and Mathematica are audit evidence only.

## Key files

```text
notes/peabody_analytic_compression_note.md
python/peabody_concavity_certificate.py
python/audit_peabody_concavity_certificate.py
python/validate_analytic_compression_package.py
R/peabody_analytic_compression_semantic_audit.R
wolfram/peabody_concavity_semantic_audit.wl
data/certificate_80dps/peabody_concavity_certificate.json
data/certificate_80dps/concavity_terminal_boxes.csv
manuscript/main_analytic_compression.tex
manuscript/main_analytic_compression.pdf
```

## Canonical Python replay

From the package root:

```bash
python3 python/peabody_concavity_certificate.py \
  --output-dir /tmp/peabody-concavity-80 \
  --precision-dps 80
```

Expected classification:

```text
GO_PEABODY_ANALYTIC_COMPRESSION_CONCAVITY_CERTIFIED
```

Independent semantic/adversarial audit:

```bash
python3 python/audit_peabody_concavity_certificate.py \
  --package-dir . \
  --output /tmp/peabody-analytic-compression-audit.json
```

Expected classification:

```text
PEABODY_ANALYTIC_COMPRESSION_AUDIT_PASS
```

Package validation:

```bash
python3 python/validate_analytic_compression_package.py --package-dir .
```

Expected classification:

```text
PEABODY_ANALYTIC_COMPRESSION_PACKAGE_PASS
```

## Cross-language audits

The R and Mathematica files are semantic audits, not proof authority.

R:

```bash
Rscript R/peabody_analytic_compression_semantic_audit.R \
  . \
  /tmp/peabody_analytic_compression_R_audit.json
```

Mathematica, from a fresh kernel:

```wl
Get["/full/path/to/wolfram/peabody_concavity_semantic_audit.wl"]
```

These two files were statically checked but could not be runtime-tested in the assistant environment because R and Mathematica were unavailable.

## Manuscript build

```bash
cd manuscript
pdflatex -interaction=nonstopmode -halt-on-error main_analytic_compression.tex
pdflatex -interaction=nonstopmode -halt-on-error main_analytic_compression.tex
```

The revised paper is nine pages. Section 4 now consists of the parabolic-endpoint lemma, strict-concavity lemma, and chord lemma.

## Frozen dependency

Before this work began, the complete release-audited Peabody theorem package replayed successfully with proof-core hash

```text
8ab4bfbf764da3c76a76810904e8289292b4c538957af68b15567a935882ac35
```

The analytical-compression package does not modify that frozen theorem package or its tag.
