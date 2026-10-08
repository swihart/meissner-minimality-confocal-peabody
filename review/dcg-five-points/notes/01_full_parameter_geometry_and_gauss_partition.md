# Reviewer Point 1 — Full-parameter Peabody geometry and normal-sphere partition

## Status

**Proof draft complete; independent geometric proofreading remains.**

This note supplies the missing bridge between the explicit eccentricity chart used in the manuscript and the source construction of Arelio–Montejano–Oliveros.  It also states and proves the normal-sphere partition needed for the additive area formula.

## 1. Source statements used

For a pair of convex confocal pea-pod devices, Arelio–Montejano–Oliveros prove:

- Theorem 3.3: the center distance plus the two pea radii is constant.
- Lemma 3.8: the two opposite wedge-pod surfaces are paired by binormals of that constant length, with tangent planes orthogonal to the binormal.
- Section 4 and Theorem 4.5: for a regular tetrahedron, three independent opposite-edge pairs assemble into six wedge-pod surfaces and four spherical caps; the resulting surface bounds a convex body of constant width two and is smooth away from the four tetrahedral vertices.
- Section 5.3: the circle-line degeneration is the classical Meissner surgery.

The source theorem is formulated for any choice of convex confocal devices on the three opposite-edge pairs.  It is therefore not restricted to the Robert or Meissner endpoints.

## 2. The explicit chart is admissible for every parameter

Fix one opposite-edge pair and let

\[
0\le e<1,
\qquad
b^2=\frac{3+3e^2+4\sqrt2\,e}{1-e^2},
\qquad
a=\frac b{\sqrt{1-e^2}}.
\]

Then \(b^2\ge 3\), so \(b>1\), and the endpoint parameters

\[
\theta=\arccos\frac1b,
\qquad
\eta=\operatorname{arsinh}\frac1b
\]

are real.  Put

\[
X(t)=a\sin t\,\mathbf k+b\cos t\,\mathbf p,
\qquad
Y(\xi)=ae\cosh\xi\,\mathbf k+b\sinh\xi\,\mathbf q,
\]

with

\[
\theta\le t\le\pi-\theta,
\qquad
-\eta\le\xi\le\eta.
\]

The two curves lie in orthogonal planes, have a common axis, and are confocal because

\[
a^2-b^2=a^2e^2.
\]

Their transverse endpoint coordinates are

\[
b\cos\theta=1,
\qquad
b\sinh\eta=1,
\]

so their longitudinal beams are the two prescribed length-two opposite edges in the local regular-tetrahedron frame.

Let

\[
u_0=\sin\theta,
\qquad
v_0=\cosh\eta,
\]

and define the pea radii

\[
R_E(t)=ae(\sin t-u_0),
\qquad
R_H(\xi)=a(v_0-\cosh\xi).
\]

On the stated parameter intervals,

\[
R_E\ge0,
\qquad
R_H\ge0,
\]

with equality precisely at the beam endpoints.  Thus the displayed subarcs are the center curves of the corresponding convex confocal devices.

The regular-tetrahedron normalization is exact.  If \(B=b^2\), then

\[
B+1=\frac{2(e+\sqrt2)^2}{1-e^2},
\qquad
B-1=\frac{2(\sqrt2e+1)^2}{1-e^2}.
\]

Since all quantities are positive,

\[
\sqrt{B+1}-e\sqrt{B-1}=2\sqrt{1-e^2}.
\]

Equivalently,

\[
a(v_0-eu_0)=2.
\]

A direct center-distance calculation gives

\[
\lVert X(t)-Y(\xi)\rVert
=a(\cosh\xi-e\sin t),
\]

and hence

\[
\lVert X-Y\rVert+R_E+R_H=2.
\]

Therefore every \(e\in(0,1)\) produces exactly a convex confocal device pair satisfying the hypotheses of the source construction.  At \(e=0\) the ellipse-hyperbola pair degenerates to the circle-line pair of Section 5.3 of the source, giving the classical Meissner surgery.

For a triple \((e_1,e_2,e_3)\in[0,1)^3\), apply this construction independently to the three pairs of opposite tetrahedral edges.  A bit \(\sigma_i\) only interchanges which member of the pair receives the elliptic or hyperbolic device.  The unordered pair of convex confocal devices is unchanged, so the source theorem applies to every \(\boldsymbol\sigma\in\{0,1\}^3\).

## 3. Patch decomposition

For \(0<e_i<1\), denote the four open spherical-cap interiors by

\[
C_A^\circ,C_B^\circ,C_C^\circ,C_D^\circ
\]

and the six open wedge-pod interiors by

\[
W_1^{+,\circ},W_1^{-,\circ},\ldots,W_3^{+,\circ},W_3^{-,\circ}.
\]

The source construction gives a finite patch decomposition of \(\partial K\): the complement of these ten open patches consists of finitely many seam curves and the four tetrahedral vertices.  Adjacent patches have the same tangent plane along a seam; the source describes the assembled surface as smooth away from the four vertices.

## 4. Normal-sphere partition lemma

### Lemma

For every admissible regular-tetrahedron confocal Peabody with \(0<e_i<1\), the following sets partition \(S^2\) up to spherical measure zero:

1. the Gauss images of the ten smooth patch interiors;
2. the four vertex normal cones.

The interiors of the listed sets are pairwise disjoint.  The Gauss images of the seams have spherical area zero.

### Proof

A body of constant width is strictly convex.  Hence every \(n\in S^2\) supports \(K\) at a unique point \(R_K(n)\).  If two distinct smooth patch interiors had a common outer normal, the corresponding support plane would touch \(K\) at two distinct points, contradicting strict convexity.  Thus their Gauss images are disjoint.

Every support point lies either in a smooth patch interior, on a seam, or at one of the four vertices, so these Gauss images together with the vertex normal cones cover \(S^2\).

Each seam is a compact piecewise-smooth one-dimensional curve.  Because the adjacent patches have a common tangent plane there, its normal image is also a finite union of one-dimensional curves in \(S^2\).  Such a set has two-dimensional spherical measure zero.  This proves the asserted almost-everywhere partition.  ∎

## 5. Vertex cone versus opposite spherical cap

Let \(C_A\subset S(A,2)\) be the spherical cap centered at vertex \(A\), and let \(\Omega_A\) be its Gauss image.  For \(x\in C_A^\circ\),

\[
n=\frac{x-A}{2}.
\]

The opposite-point identity for a width-two body is

\[
R_K(-n)=R_K(n)-2n.
\]

Since \(R_K(n)=x\), it gives \(R_K(-n)=A\).  Therefore

\[
-\Omega_A\subset N_K(A).
\]

Conversely, if \(m\in N_K(A)\), then the opposite support point is

\[
R_K(-m)=A-2m\in\partial K\cap S(A,2)=C_A.
\]

Hence \(-m\in\Omega_A\), and

\[
N_K(A)=-\Omega_A.
\]

The same holds at the other three vertices.

## 6. Opposite wedge Gauss images

Lemma 3.8 of the source pairs every smooth point of \(W_i^+\) with a point of \(W_i^-\) at distance two, with tangent planes perpendicular to the joining segment.  The outward normals are therefore antipodal:

\[
\operatorname{Gauss}(W_i^-)=-\operatorname{Gauss}(W_i^+).
\]

Writing \(\Gamma_i=\operatorname{Gauss}(W_i^+)\), the normal-sphere partition yields

\[
4\pi
=2\sum_{v\in\{A,B,C,D\}}|\Omega_v|
 +2\sum_{i=1}^3|\Gamma_i|.
\]

This is the exact tiling statement required for the surface-area bookkeeping.

## 7. Degenerate parameters

The preceding proof is written on the generic stratum \(0<e_i<1\).  The formulas, patch surfaces, and Gauss-image areas extend continuously when one or more \(e_i\to0\).  The source identifies this limit with the circle-line Meissner surgery.  The additive area identity therefore extends to all \(e_i\in[0,1)\) by continuity.  Equivalently, one may treat the collapsed wedge as a zero-area patch and repeat the same normal bookkeeping directly.

## 8. Remaining release task

Before marking Reviewer Point 1 fully closed in the manuscript, a convex geometer should check:

- that the chart-to-device identification above uses the same principal-circle convention as the source;
- that the source theorem indeed permits independent choices on all three opposite-edge pairs, as its Section 4 wording indicates;
- that the direct continuity argument at mixed degenerate triples is presented cleanly.

No numerical search or new geometric construction is required.
