# Confocal Peabody five-point DCG revision checkpoint

**Date:** 2026-10-08  
**Target branch:** `review/dcg-five-points`  
**Immutable baseline:** public release tag `v1.0.0`

This checkpoint begins the finite major revision prompted by the five-point review of *Meissner Minimality in the Confocal Peabody Family*.  It does not reopen the regular-tetrahedron Peabody search, enlarge the theorem's scope, or start a semi-regular construction campaign.

## Principal progress

1. **Independent rigorous arithmetic.**  A second certifier was written in C against MPFR.  It reconstructs the stable formula independently of the principal Python certifier and calls `mpfr_sqrt` and `mpfr_atan` with explicit downward/upward rounding.  The assistant preflight proves the publication-headroom bounds
   \[
   \Phi(1)>1/4000,
   \qquad
   \Phi''(e)<-1/30000.
   \]
   The release script deliberately requires the official `mpfr.h`; the author's local official-header replay is the remaining promotion gate.
2. **Full-parameter geometry.**  A proof draft connects the explicit eccentricity chart to the source construction for every `e` and every orientation pattern, then proves the almost-everywhere normal-sphere partition used in the area bookkeeping.
3. **Formula derivation and branch control.**  A detailed supplement derives the one-pair formula, fixed-interval formula, stable `q` chart, and global principal-`arctan` branch.  An exact SymPy audit reduces the frozen algebraic identities to zero.
4. **Parabolic regularity.**  Uniform positive radicand and denominator bounds prove real analyticity at `q=0`.
5. **Equality and seams.**  The eight zero-parameter orientations are classified into the two classical Meissner congruence classes, and the seam Gauss images are shown to have spherical area zero.

## Current status

This is a **revision checkpoint**, not yet the final DCG submission package.

- Reviewer Points 4 and 5 are analytically closed.
- Point 2 has a successful direct-MPFR assistant preflight and awaits the author's official-header replay.
- Points 1 and 3 have complete proof drafts integrated into a 12-page revision manuscript and await independent human proofreading.

See `REVIEW_PROGRESS_LEDGER.md` for the standing status and `LOCAL_REPLAY.md` for the mandatory MPFR replay.

## Revision manuscript

`manuscript/main_dcg_revision_checkpoint.pdf` integrates all five reviewer responses at draft level.  It is not yet a submission version: Point 2 still requires the official-header replay, and Points 1 and 3 still require independent human proofreading.
