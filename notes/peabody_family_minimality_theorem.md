# Meissner minimality in the regular-tetrahedron confocal Peabody family

**Date:** 2026-09-30  
**Principal classification:** `GO_PEABODY_FAMILY_MINIMALITY_CERTIFIED`

## Theorem

Let

\[
\mathbf e=(e_1,e_2,e_3)\in[0,1)^3
\]

be an admissible parameter triple for a width-one regular-tetrahedron confocal Peabody, and let

\[
\boldsymbol\sigma\in\{0,1\}^3
\]

be any of the eight choices assigning the two confocal devices to the members of the three opposite-edge pairs. Then

\[
\boxed{
V\!\left(K(\mathbf e,\boldsymbol\sigma)\right)
\ge
V_M,
}
\]

where

\[
V_M
=
\pi\left(
\frac23-\frac{\sqrt3}{4}\arccos\frac13
\right).
\]

Equality holds if and only if

\[
e_1=e_2=e_3=0.
\]

Within this family, the equality cases are the classical Meissner degenerations.

## Proof assembly

### 1. Source-established geometry

Arelio, Montejano, and Oliveros construct the Peabody boundary from six wedge-pod surfaces and four spherical caps. Their confocal identity pairs opposite patches by width-length binormals, and their assembly theorem proves that the resulting surface bounds a body of constant width. In the circle-line degeneration, the wedge-pod construction becomes precisely the classical Meissner edge surgery.

### 2. Frozen exact family reduction

The project-derived normal-sphere decomposition gives

\[
V\!\left(K(\mathbf e,\boldsymbol\sigma)\right)
=
V_M+\Phi(e_1)+\Phi(e_2)+\Phi(e_3),
\]

independent of `boldsymbol sigma`. The factor-of-eight width normalization is the exact identity

\[
\frac18\left(\frac{16\pi}{3}+\Psi(e_1)+\Psi(e_2)+\Psi(e_3)\right)
-
\left(\frac{2\pi}{3}+\frac{3\Psi(0)}8\right)
=
\sum_{i=1}^3\frac{\Psi(e_i)-\Psi(0)}8.
\]

The semantic audit checks all eight orientation patterns, all pair permutations, exact symbolic mixed differences, one-pair/two-pair/three-pair consistency, Meissner recovery, and the archived mesh-based separability evidence.

### 3. Scalar positivity

The new central certificate proves

\[
\Phi(e)>0
\qquad
\left(0<e\le\frac{199}{200}\right).
\]

More specifically,

\[
\frac{\Phi(e)}e\ge\frac1{2000}
\qquad
\left(0<e\le\frac1{100}\right),
\]

and

\[
\Phi(e)>\frac1{10^7}
\qquad
\left(\frac1{100}\le e\le\frac{199}{200}\right).
\]

The frozen tail theorem gives

\[
\Phi(e)>\frac1{20000}
\qquad
\left(\frac{199}{200}\le e<1\right).
\]

Together with `Phi(0)=0`, these statements imply

\[
\Phi(e)\ge0\quad(0\le e<1),
\]

with equality exactly at `e=0`.

### 4. Volume and equality

Each term in

\[
V-V_M=\Phi(e_1)+\Phi(e_2)+\Phi(e_3)
\]

is nonnegative, so `V>=V_M`. If equality holds, each nonnegative summand must vanish, hence all three parameters are zero. Conversely, the all-zero triple is the classical Meissner degeneration and has volume `V_M`.

This proves the theorem.

## Exact scope and exclusions

This theorem concerns only **regular-tetrahedron confocal Peabodies**. It does not establish:

- Meissner minimality among all three-dimensional bodies of constant width;
- minimality among arbitrary Meissner polyhedra;
- minimality among Peabodies built from arbitrary self-dual ball polyhedra;
- a new universal volume lower bound;
- global monotonicity of `Phi` or `Phi'`.

## Certificate summary

| Proof block | Range | Result | Boxes |
|---|---|---:|---:|
| Local endpoint | `0<=e<=1/100` | `Phi(e)/e>=1/2000` | 160 |
| Central bulk | `1/100<=e<=199/200` | `Phi(e)>1/10^7` | 430 |
| Frozen tail | `199/200<=e<1` | `Phi(e)>1/20000` | 2,000 |
| **Combined** | `0<e<1` | `Phi(e)>0` | **2,590** |

The weakest raw central bulk lower endpoint is

\[
3.2899516603979685\times10^{-7},
\]

and the weakest frozen tail lower endpoint is

\[
6.0546375326427965\times10^{-5}.
\]
