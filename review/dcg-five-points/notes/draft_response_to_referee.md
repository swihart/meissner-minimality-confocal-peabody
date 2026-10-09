# Draft response to the five-point review

We thank the reviewer for a careful and constructive report. The revision has been organized around the five requested points. The theorem statement and its scope are unchanged.

## 1. Convexity, constant width, and the normal-sphere tiling

We expanded Section 2 substantially.

- The explicit eccentricity chart is now matched to the source definition of a **convex confocal** pea-pod pair, including the principal-circle centers, the two bulb centers, and the ordering inequalities selecting the principal circles.
- We prove that the four beam endpoints have all six mutual distances equal to two and hence form the prescribed regular tetrahedron.
- We cite the source construction precisely for independent choices on all three opposite-edge pairs and both orientations.
- We state and prove a normal-sphere partition lemma, a seam-nullity lemma, and the cap-cone duality needed for the area bookkeeping.
- We corrected the degenerate case: the collapsed Meissner arc has zero physical area but a nonzero normal cone. The additive identity is extended to mixed zero-parameter tuples by continuous degeneration, not by deleting that normal contribution.

## 2. Trust boundary of the interval arithmetic

The original `mpmath.iv` calculation is no longer the sole proof authority. We added an independently written Arb/FLINT implementation through `python-flint`, reconstructed from the stable formula without importing the original certifier. It was replayed at 384 and 512 bits and in reverse slab order. Deliberately under-resolved and sign-mutated controls produce semantic no-go certificates. The paper now uses the conservative bounds

\[
 \Phi(1)>\frac1{4000},
 \qquad
 \Phi''(e)<-\frac1{100000}.
\]

The Arb outputs overlap the independent MPFR preflight and the earlier interval calculation.

## 3. Formula derivation and branch control

We replaced the `direct calculation` steps by a complete derivation.

- The center distance, normal chart, conformal Gauss area element, and wedge Jacobians are worked out.
- The `xi`-integration is shown explicitly.
- The exact value `Psi(0)` is derived.
- The change to the fixed interval is displayed.
- A complete substitution table derives the stable `q`-chart and the coefficients `P_1,P_2,Q_0`.
- The principal arctangent branch is proved globally for `q>0`; the parabolic endpoint is handled by analytic continuation of the positive stable expression.

A separate exact symbolic audit reduces every algebraic identity used in this derivation to zero.

## 4. Smoothness at the parabolic endpoint

The revised appendix proves uniform lower bounds for every radicand and denominator on the closed square `0<=q,x<=1`. The stable formula contains no negative power of `q`, so it is real analytic in a neighborhood of the closed square. This justifies differentiation under the fixed integral on slabs meeting `q=0`.

## 5. Equality orientations and seams

We now state explicitly that the eight zero-parameter choices are the four vertex stars and the four face boundaries, giving exactly two tetrahedral congruence classes. The seam set is a finite union of piecewise-smooth curves; the common normal map sends it to a one-dimensional subset of the unit sphere, hence a set of spherical area zero.

## Scope

The result remains restricted to regular-tetrahedron confocal Peabodies. We make no claim of global Meissner extremality, no universal lower-bound improvement, and no global construction theorem for arbitrary semi-regular tetrahedral bases.
