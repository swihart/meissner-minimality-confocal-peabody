# Independent audit of the three opposite-edge decomposition

## 1. Patch inventory

A generic regular-tetrahedron confocal Peabody has:

- four radius-two spherical caps `C_A,C_B,C_C,C_D`;
- two wedge-pod surfaces for each of the three pairs of opposite tetrahedral edges.

Write the two wedge surfaces in pair `i` as `W_i^+` and `W_i^-`. Their Gauss images are antipodal;
write one of them as `Gamma_i`.

## 2. Vertex normal cones

For a point `x` on the cap centered at vertex `A`, the outward normal is

\[
n=\frac{x-A}{2}.
\]

Constant width two pairs `x` with the opposite support point

\[
x-2n=A.
\]

Therefore the antipodal Gauss image of the cap is exactly the normal cone at the vertex:

\[
N_K(A)=-\Omega_A.
\]

The same holds at all four vertices. This is why each cap Gauss image appears twice in the normal
sphere: once as the smooth cap image and once antipodally as a vertex normal cone.

## 3. Partition of the normal sphere

Ignoring patch boundaries, which have spherical measure zero, the unit normal sphere is partitioned by

- the four cap Gauss images `Omega_v`;
- their four antipodal vertex normal cones `-Omega_v`;
- the six wedge images `Gamma_i` and `-Gamma_i`.

Hence

\[
4\pi=2\sum_v|\Omega_v|+2\sum_{i=1}^3|\Gamma_i|.
\]

Thus

\[
\sum_v|\Omega_v|=2\pi-\sum_i|\Gamma_i|.
\]

A radius-two sphere multiplies Gauss-image area by four, so the total physical cap area is

\[
\sum_v|C_v|=4\sum_v|\Omega_v|
=8\pi-4\sum_i|\Gamma_i|.
\]

Adding the six wedge areas gives

\[
S_2=8\pi+\sum_{i=1}^3
\left(|W_i^+|+|W_i^-|-4|\Gamma_i|\right).
\]

This is exact additivity before any quadrature or mesh approximation.

## 4. One scalar per opposite-edge pair

Define

\[
\Psi_i=|W_i^+|+|W_i^-|-4|\Gamma_i|.
\]

All three opposite-edge configurations of the regular tetrahedron are congruent. More importantly,
within a fixed pair, exchanging the elliptic and hyperbolic devices merely exchanges `W_i^+` and
`W_i^-`; their sum is unchanged, and the two Gauss images are antipodal with equal area. Therefore

\[
\Psi_i=\Psi(e_i)
\]

and no orientation bit remains.

This pairwise symmetry is sufficient; no appeal to a global tetrahedral isometry is needed for the
orientation-independence conclusion.

## 5. Degenerate Meissner endpoint

The partition argument is written for generic `0<e_i<1`, where the patch Gauss maps are smooth. The
explicit one-pair formula extends continuously to `e_i=0`. The all-zero limit is exactly the circle-line
Meissner surgery. Thus the additive formula extends to every admissible parameter triple in `[0,1)^3`.

## 6. Mixed differences

Once

\[
V=V_M+\Phi(e_1)+\Phi(e_2)+\Phi(e_3)
\]

is established, every mixed finite difference vanishes symbolically, for example

\[
V(e,f,0)-V(e,0,0)-V(0,f,0)+V(0,0,0)=0.
\]

The archived mesh residuals near machine precision are corroborating evidence only; they are not the
reason the mixed difference vanishes.

## 7. Release gates

The decomposition passes release audit only if all of the following are explicitly retained:

1. cap Gauss images and vertex cones are both counted;
2. patch seams are measure zero;
3. the radius-two area factor is four;
4. all three opposite-edge pairs are included once;
5. device exchange leaves the local pair functional unchanged;
6. continuity to the Meissner endpoint is stated;
7. width normalization is applied only after the width-two volume is formed.
