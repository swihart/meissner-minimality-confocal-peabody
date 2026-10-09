# Reviewer Point 1 — Full-parameter geometry and normal-sphere partition

## Status

**Closed internally after a second, adversarial derivation. External review by a convex geometer remains recommended before journal submission.**

This note replaces the earlier geometry draft. It makes explicit the principal-circle and bulb-center data required by the source definition of a *convex confocal* pea-pod pair, proves that the four beam endpoints form the prescribed regular tetrahedron, sharpens the cap-cone argument, and corrects the treatment of the Meissner degeneration.

## 1. Source statements used

For convex confocal pea-pod devices, Arelio--Montejano--Oliveros prove:

1. the center-distance plus the two pea radii is constant (their Theorem 3.3);
2. paired wedge-pod surfaces are joined by binormals of that constant length (their Lemma 3.8);
3. for a regular tetrahedron, independent choices on all three opposite-edge pairs assemble into six wedge-pod surfaces and four spherical caps, whose convex hull is a body of constant width two (their Section 4 and Theorem 4.5);
4. the circle-line degeneration gives the classical Meissner surgery (their Section 5.3).

Our task is to verify that the explicit eccentricity chart used in the volume calculation satisfies those hypotheses for every `e in [0,1)` and for either orientation of each opposite-edge pair.

## 2. Explicit local chart

Fix `0 < e < 1`. Put

\[
 b^2=\frac{3+3e^2+4\sqrt2\,e}{1-e^2},
 \qquad
 a=\frac b{\sqrt{1-e^2}},
\]

and

\[
 \theta=\arccos\frac1b,
 \qquad
 \eta=\operatorname{arsinh}\frac1b,
 \qquad
 u_0=\sin\theta,
 \qquad
 v_0=\cosh\eta.
\]

In an orthonormal frame `(k,p,q)`, define

\[
 X(t)=a\sin t\,\mathbf k+b\cos t\,\mathbf p,
 \qquad \theta\le t\le\pi-\theta,
\]

\[
 Y(\xi)=ae\cosh\xi\,\mathbf k+b\sinh\xi\,\mathbf q,
 \qquad -\eta\le\xi\le\eta.
\]

The curves lie in orthogonal planes, share the axis `R k`, and are confocal because

\[
 a^2-b^2=a^2e^2.
\]

The beam endpoints are

\[
 X_\pm=a u_0\,\mathbf k\pm\mathbf p,
 \qquad
 Y_\pm=ae v_0\,\mathbf k\pm\mathbf q,
\]

because `b cos theta = b sinh eta = 1`. Hence each beam has length two.

The pea radii are

\[
 R_E(t)=ae(\sin t-u_0),
 \qquad
 R_H(\xi)=a(v_0-\cosh\xi).
\]

They are nonnegative on the stated subarcs and vanish exactly at the beam endpoints.

## 3. Principal circles and bulb centers

The missing point in the earlier draft was the explicit verification of Definition 3.5 in the source.

### 3.1 Elliptic device

The ellipse has foci

\[
 c_E^+=ae\,\mathbf k,
 \qquad
 c_E^-=-ae\,\mathbf k.
\]

For every `t`,

\[
 |X(t)-c_E^+|=a(1-e\sin t),
 \qquad
 |X(t)-c_E^-|=a(1+e\sin t).
\]

At the beam endpoints, the corresponding frame radii are

\[
 r_E^+=a(1-eu_0),
 \qquad
 r_E^-=a(1+eu_0).
\]

The beam midpoint is `m_E=a u_0 k`. Moreover,

\[
 u_0^2-e^2
 =\frac{2+3e^2+4\sqrt2\,e}{b^2}>0,
\]

so `u_0>e`. Therefore `m_E` lies beyond `c_E^+` and is not between the two circle centers; `c_E^+` is the closer center and hence the principal-circle center. The pea radius generated from that principal circle is

\[
 r_E^+-|X-c_E^+|
 =ae(\sin t-u_0)=R_E(t).
\]

The center of the elliptic bulb is

\[
 X(\pi/2)=a\,\mathbf k.
\]

### 3.2 Hyperbolic device

The hyperbola has foci

\[
 c_H^+=a\,\mathbf k,
 \qquad
 c_H^-=-a\,\mathbf k.
\]

For every `xi`,

\[
 |Y(\xi)-c_H^+|=a(\cosh\xi-e),
 \qquad
 |Y(\xi)-c_H^-|=a(\cosh\xi+e).
\]

At the beam endpoints, the frame radii are

\[
 r_H^+=a(v_0-e),
 \qquad
 r_H^-=a(v_0+e).
\]

The beam midpoint is `m_H=ae v_0 k`. Also,

\[
 1-e^2v_0^2
 =\frac{3+2e^2+4\sqrt2\,e}{b^2}>0,
\]

so `ev_0<1`; thus `m_H` lies between `-a k` and `a k`. The smaller frame circle is the one centered at `c_H^+`, so it is the principal circle. Its pea radius is

\[
 r_H^+-|Y-c_H^+|
 =a(v_0-\cosh\xi)=R_H(\xi).
\]

The center of the hyperbolic bulb is

\[
 Y(0)=ae\,\mathbf k.
\]

### 3.3 Convex-confocal condition

The two principal-circle centers are exactly the opposite bulb centers:

\[
 c_E^+=Y(0),
 \qquad
 c_H^+=X(\pi/2).
\]

Hence the pair is *convex confocal* in the precise sense of the source definition, not merely a pair of confocal center curves with a constant distance identity.

## 4. Regular-tetrahedron normalization

Let `B=b^2`. Directly,

\[
 B+1=\frac{2(e+\sqrt2)^2}{1-e^2},
 \qquad
 B-1=\frac{2(\sqrt2 e+1)^2}{1-e^2}.
\]

Since all factors are positive,

\[
 \sqrt{B+1}-e\sqrt{B-1}=2\sqrt{1-e^2},
\]

or equivalently

\[
 a(v_0-eu_0)=2.
\]

The exact center-distance computation gives

\[
 |X(t)-Y(\xi)|=a(\cosh\xi-e\sin t).
\]

Therefore

\[
 |X-Y|+R_E+R_H=2.
\]

At all four pairs of beam endpoints, both radii vanish, so every cross distance `|X_\pm-Y_\pm|` and `|X_\pm-Y_\mp|` equals two. Together with the two beam lengths, all six distances among `X_+,X_-,Y_+,Y_-` equal two. Thus the beams are opposite edges of a regular tetrahedron of side two.

This proves full local admissibility for every `0<e<1`.

## 5. Three independent opposite-edge pairs and orientations

Section 4 of the source chooses a convex confocal device pair on each of the three opposite-edge pairs of the same regular tetrahedron and then constructs the six wedge-pod surfaces and four spherical caps. No cross-pair parameter equality is assumed.

For our family, the three parameters `e_1,e_2,e_3` may therefore be chosen independently. An orientation bit `sigma_i` exchanges the elliptic and hyperbolic devices within the `i`th opposite-edge pair. This leaves the unordered convex-confocal pair unchanged and preserves the source hypotheses. Consequently, the source constant-width theorem applies for every

\[
 (e_1,e_2,e_3)\in(0,1)^3,
 \qquad
 \boldsymbol\sigma\in\{0,1\}^3.
\]

The endpoint `e=0` is treated in Section 9 below.

## 6. Generic patch decomposition

For a generic tuple `e_i>0`, the boundary is the union of:

- four open spherical-cap interiors `C_A^\circ,C_B^\circ,C_C^\circ,C_D^\circ`;
- six open wedge-pod interiors `W_i^{+,\circ},W_i^{-,\circ}`, `i=1,2,3`;
- finitely many nonvertex seam curves;
- the four tetrahedral vertices.

The source proves that the assembled surface is smooth away from the four vertices. In particular, adjacent patches have a common tangent plane along every nonvertex seam.

## 7. Normal-sphere partition

Let `R_K(n)` be the unique support point with outer unit normal `n`. Constant-width bodies are strictly convex, so `R_K(n)` is single-valued.

### Lemma 7.1 — Almost-everywhere partition

For a generic regular-tetrahedron confocal Peabody, the Gauss images of the ten open smooth patch interiors, together with the four vertex normal cones, cover `S^2` up to the Gauss images of the seam curves. Their interiors are pairwise disjoint. Each seam Gauss image has spherical area zero.

### Proof

If two distinct smooth patch interiors shared an outer normal, the corresponding supporting plane would touch the strictly convex body at two distinct points, impossible. Every support point belongs to a patch interior, a seam, or a vertex, so the listed normal sets cover the sphere after the seam normals are added.

Each nonvertex seam is a compact piecewise-smooth curve. Because the assembled surface has a common tangent plane along it, the unit normal restricted to the seam is piecewise smooth. Its image is therefore a finite union of one-dimensional curves in `S^2`, which has two-dimensional spherical measure zero. ∎

## 8. Vertex-cone / opposite-cap duality

For a body of constant width two,

\[
 R_K(-n)=R_K(n)-2n.
\]

Indeed, if `x=R_K(n)` and `y=R_K(-n)`, then `(x-y)·n=2` while `|x-y|<=2`; equality in Cauchy--Schwarz gives `x-y=2n`.

Let `C_A` denote the closed spherical cap lying on `S(A,2)` and let `Omega_A` be its Gauss image. If `x\in C_A^\circ`, then its outer normal is

\[
 n=\frac{x-A}{2},
\]

so the opposite-support identity gives `R_K(-n)=A`. Hence

\[
 -\Omega_A\subseteq N_K(A).
\]

Conversely, let `m\in N_K(A)`. Then

\[
 x:=R_K(-m)=A-2m
\]

lies on `\partial K\cap S(A,2)`. By the patch construction and the strict-containment statement used in the proof of the source Lemma 4.3, every wedge-pod interior is strictly inside `B(A,2)`. The interiors of the other spherical caps lie on their own supporting spheres and meet `S(A,2)` only along shared seam curves. Therefore

\[
 \partial K\cap S(A,2)=C_A
\]

as closed sets, and `x\in C_A`. Thus `-m\in\Omega_A`, proving

\[
 N_K(A)=-\Omega_A.
\]

The same argument applies to all four vertices.

## 9. Opposite wedges and additive area

The source binormal pairing and the opposite-support identity show that the two wedge surfaces in an opposite-edge pair have antipodal Gauss images. If

\[
 \Gamma_i=\operatorname{Gauss}(W_i^+),
\]

then

\[
 \operatorname{Gauss}(W_i^-)=-\Gamma_i.
\]

The almost-everywhere normal partition therefore gives

\[
 4\pi
 =2\sum_{v\in\{A,B,C,D\}}|\Omega_v|
 +2\sum_{i=1}^3|\Gamma_i|.
\]

A radius-two spherical patch has physical area four times its Gauss-image area. Hence

\[
 \sum_v|C_v|
 =8\pi-4\sum_{i=1}^3|\Gamma_i|.
\]

Adding the six wedge areas gives

\[
 S_2
 =8\pi+\sum_{i=1}^3\Psi(e_i),
\]

where

\[
 \Psi(e_i)
 =|W_i^+|+|W_i^-|-4|\Gamma_i|.
\]

Swapping the two devices exchanges `W_i^+` and `W_i^-`; the antipodal Gauss images have equal area. Thus `\Psi` is orientation independent.

## 10. Degenerate parameters and the correction to the earlier draft

At `e=0`, the elliptic wedge-pod surface collapses to a circular arc. It is **not** correct to regard its Gauss contribution as zero: the singular arc carries a two-dimensional normal cone, which is the limit of `\Gamma_i`.

The additive identity is extended to mixed tuples with zero parameters by continuity, not by deleting that normal contribution. The explicit patch maps converge uniformly as `e\downarrow0`, the source identifies the limiting circle-line construction with the Meissner surgery, and the resulting convex bodies converge in Hausdorff distance. Volume and surface area are continuous under Hausdorff convergence of convex bodies. The scalar integral defining `\Psi(e)` is also continuous at `e=0`. Therefore the generic additive identity passes to every tuple

\[
 (e_1,e_2,e_3)\in[0,1)^3.
\]

This correction is important: the physical area of the collapsed surface is zero, while its limiting normal region is not.

## 11. Equality orientations

At the all-zero tuple, one edge is chosen from each of

\[
 \{AB,CD\},\qquad \{AC,BD\},\qquad \{AD,BC\}.
\]

The eight choices are exactly:

- four three-edge stars incident to one vertex;
- four three-edge cycles bounding one face.

The tetrahedral symmetry group is transitive on vertices and on faces, so these form exactly two congruence classes. They are the two classical Meissner types.

## 12. Audit conclusion

The full-parameter geometry and normal-sphere bookkeeping are now supplied in a form sufficient for the additive reduction. The earlier two omissions—principal-circle/bulb-center verification and the nonzero normal cone of the collapsed Meissner arc—have been repaired.

An external geometric proofread remains prudent, especially for the concise citation to the source Lemma 4.3 in the cap-cone converse, but no unresolved mathematical gap remains in this point.
