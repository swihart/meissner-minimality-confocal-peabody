# DCG five-point revision plan

## Gate A — official-header MPFR proof certificate

1. Install official MPFR/GMP development files.
2. Run `scripts/run_mpfr_replays.sh` from the public repository.
3. Require forward 384-bit, forward 512-bit, and reverse-order certificates to pass.
4. Require the 16-slab and correction-sign controls to fail.
5. Preserve compiler version, MPFR version, exact outputs, transcript, and checksums.
6. Make this official-header MPFR run the manuscript's proof authority.  Retain `mpmath.iv`, Mathematica, and R as redundant audits.

## Gate B — full-parameter geometry

- Convert `notes/01_full_parameter_geometry_and_gauss_partition.md` into formal manuscript lemmas.
- Cite Arelio–Montejano–Oliveros Theorem 3.3, Lemma 3.8, Theorem 4.5, Lemma 5.1, and Section 5.3 precisely.
- Have a convex geometer review the chart-to-device conventions, mixed degenerate cases, and normal-sphere partition.

## Gate C — exact formula supplement

- Align `notes/03_formula_derivation_and_branch_control.md` with manuscript equation numbering.
- Include the center-distance, normal-chart, wedge-Jacobian, `xi`-integration, fixed-interval, stable-chart, and branch-control steps.
- Keep `verify_formula_derivation_identities.py` as an exact audit, not as a substitute for the written derivation.

## Gate D — endpoint and equality cleanup

- Insert the real-analytic `q=0` lemma.
- Insert the eight-orientation/two-orbit lemma.
- State the seam-measure-zero lemma before the normal-area calculation.

## Gate E — manuscript and final release audit

- Replace the original `mpmath.iv` trust-boundary paragraph with the official-header MPFR certificate.
- Publish the weaker, higher-headroom bounds `Phi(1)>1/4000` and `Phi''<-1/30000`.
- Ask Arelio, Montejano, and Oliveros to review the geometric lemmas.
- Address the formula supplement and branch control in the paper or a referee-readable supplement.
- Create `v1.1.0` only after all five ledger rows are closed and the revised package passes a clean replay.
