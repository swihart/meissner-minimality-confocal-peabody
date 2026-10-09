# Interval-enclosure reconciliation

## Purpose

This note reconciles the three reported enclosure scales without changing the Peabody formula or theorem.  It is a bounded proof-provenance audit, not a new numerical search.

The published proof authority is the independent Arb/FLINT ball calculation.  Two earlier endpoint-interval implementations are retained as redundant audits:

- legacy `mpmath.iv`;
- a direct libMPFR implementation with explicit upward and downward rounding.

## Frozen 32-by-10 comparison

At the same 32 rational parameter slabs, ten rational integration panels per slab, and four endpoint panels, the archived global bounds are:

| implementation | lower bound for `Phi(1)` | weakest upper bound for `Phi''` |
|---|---:|---:|
| `mpmath.iv` | `0.0003076528682490342052...` | `-0.0000416798241713739433...` |
| direct MPFR | `0.0003076528682490342052...` | `-0.0000416491903361455480...` |
| Arb/FLINT | `0.0002951409916769718631...` | `-0.0000179286178483067823...` |

The complete slabwise comparison gives:

- all 32 `mpmath.iv` and direct-MPFR slab intervals intersect;
- every direct-MPFR slab interval contains the corresponding `mpmath.iv` slab interval;
- the two endpoint intervals agree to roughly 80 decimal digits;
- the largest difference between slab upper endpoints is approximately `2.70e-6`;
- the weakest slab is `q in [0,1/32]` in both endpoint-interval implementations.

Thus the earlier endpoint-interval calculations agree closely with each other.  The wider Arb result cannot be explained by arithmetic precision alone.  It is consistent with a difference in interval representation and accumulated wrapping in a long automatic-differentiation expression.  The paper does not assert that explanation as a theorem; it records the refinement data directly.

## Bounded Arb refinement audit

The replay script performs exactly the following runs at 384 bits:

- concavity: `32x10`, `64x20`, and `128x20` rational partitions;
- endpoint: 4, 8, and 16 rational panels.

For refined Arb partitions, subslabs are aggregated back to the original 32 slabs before comparison with direct MPFR.  The audit records interval widths, intersection and containment relations, the weakest slab, and runtimes.

Hard limits:

- no formula change;
- no shape search;
- no parameter optimization;
- at most 4,000 diagnostic terminal rectangles;
- the result does not replace the canonical Arb certificate.

## Publication convention

The manuscript now uses only:

\[
\Phi(1)>\frac1{4000},
\qquad
\Phi''(e)<-\frac1{100000}.
\]

The direct-MPFR and `mpmath.iv` figures appear only in a reproducibility comparison.  The tighter `0.0003076528...` endpoint bound is no longer attributed to the Arb appendix or used in the proof.
