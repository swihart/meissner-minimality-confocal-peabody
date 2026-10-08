# New chat handoff: Confocal Peabody Formula, Additivity, and Release Audit

Use PRO-level proof review, exact normalization, interval-certificate audit, and adversarial validation.

## Frozen baseline

Work in the private repository:

```text
~/github/confocal-peabody-family-minimality
```

Begin from the immutable annotated tag:

```text
v1.0.0-certified
```

The frozen theorem package contains 50 manifest-listed payload files, plus
`PACKAGE_MANIFEST.json` and `SHA256SUMS.txt`. Do not edit any frozen package file during the audit.
Add all new material only under:

```text
release_audit/
```

## Audit branch

```text
audit/confocal-peabody-formula-additivity-release
```

## Exact scope

Audit the certified claim:

> Meissner minimizes volume among width-one regular-tetrahedron confocal Peabodies, with equality
> exactly at the all-zero Meissner degeneration.

Do not promote the result to global Meissner extremality, arbitrary Meissner polyhedra, arbitrary
Peabodies, or a universal lower-bound improvement.

## Mandatory tasks

1. Independently rederive the one-pair volume formula.
2. Review the factor-of-eight width normalization line by line.
3. Review the normal-sphere decomposition of the three opposite-edge pairs.
4. Run the proof-critical Mathematica files from fresh kernels with recursive unresolved-expression guards.
5. Run the independent Python certificate checker that does not import the principal certifiers.
6. Run the R semantic audit.
7. Turn the theorem note into a human-readable proof.
8. Assemble `PEABODY_RELEASE_AUDIT_PASS` only if every mandatory gate succeeds.

## Immediate commands

```bash
release_audit/scripts/run_python_release_audit.sh "$PWD"
```

Then run Mathematica and R using the dedicated scripts documented in `README_RELEASE_AUDIT.md`.

## Claim discipline

The optional fixed-rho Mathematica `Integrate` remains unevaluated. Preserve that classification.
Numerical quadrature and R checks are audit evidence, not proof authority. The proof authority remains
the frozen exact derivation plus the outward-rounded central and tail interval certificates.
