# Exact pairwise additivity for regular-tetrahedron Peabodies

**Date:** 2026-09-29  
**Campaign status:** `GO_PEABODY_EXACT_ADDITIVITY_REDUCTION`  
**Normalization:** regular tetrahedron side length `2`; Peabody width `2`; final volume coefficients divided by `8` to report width `1`.

## Executive result

The machine-precision additivity seen in the numerical moonshot is not merely a feature of the triangular mesh. For a regular-tetrahedron Peabody with three confocal parameters \(e_1,e_2,e_3\in[0,1)\) and arbitrary orientation bits, the exact surface area and volume split into three independent opposite-edge-pair contributions.

For width two,

\[
S(K)=8\pi+\Psi(e_1)+\Psi(e_2)+\Psi(e_3),
\]

and Blaschke's identity gives

\[
V_2(K)=\frac{16\pi}{3}+\Psi(e_1)+\Psi(e_2)+\Psi(e_3).
\]

Consequently, after rescaling to width one,

\[
\boxed{
V_1(K)=V_M+\Phi(e_1)+\Phi(e_2)+\Phi(e_3),
\qquad
\Phi(e)=\frac{\Psi(e)-\Psi(0)}8 .
}
\]

The scalar \(\Psi(e)\) is independent of which member of an opposite-edge pair carries the elliptic device. Thus the three orientation bits disappear exactly.

The remaining Peabody-family minimality question is one-dimensional:

\[
\Phi(e)\ge 0\quad(0\le e<1).
\]

A closed one-dimensional integral for \(\Psi\) is derived below. It yields the exact endpoint derivative

\[
\Phi'(0)
=\frac12\left[
\frac{5\pi}{3\sqrt3}-3
+\arccos\!\frac13
\left(
\frac{3\sqrt2}{2}-\frac{5\sqrt6\,\pi}{18}
\right)
\right]
=0.00149010420703821\ldots>0.
\]

This proves exact first-order one-sided stability of the Meissner endpoint inside the confocal family. Global monotonicity of \(\Phi\) is still not proved.

---

## 1. Source inputs and what is new

Arelio, Montejano, and Oliveros construct the Peabody boundary from six wedge-pod surfaces and four radius-two spherical caps. Their Theorem 3.3 gives the confocal distance-plus-radii identity; Lemma 3.8 pairs opposite wedge-pod points by length-two binormals; and Theorem 4.5 proves that the assembled surface bounds a body of constant width two and is smooth except at the four tetrahedral vertices.

The following ingredients are new in this note:

1. a normal-sphere partition that eliminates all four spherical caps at once;
2. the exact three-pair additive surface-area formula;
3. a conformal local chart for a generic elliptic-hyperbolic pair;
4. the reduction of its two-dimensional surface integral to one dimension;
5. the exact right derivative at the Meissner endpoint.

Bogosel's normal-sphere bookkeeping for Meissner polyhedra is an important precedent: there, spherical face areas are eliminated using a partition of the unit normal sphere, leaving a sum of local dual-edge terms. The argument below performs an analogous elimination for the curved Peabody seams.

---

## 2. Exact normal-sphere decomposition

Let \(K\) be a generic Peabody with \(0<e_i<1\). Denote the four radius-two spherical caps by

\[
C_A,C_B,C_C,C_D,
\]

and the two wedge-pod surfaces associated with the \(i\)-th opposite-edge pair by

\[
W_i^+,W_i^-\qquad(i=1,2,3).
\]

Let \(\Omega_A,\ldots,\Omega_D\subset S^2\) be the Gauss images of the four spherical caps, and let \(\Gamma_i\subset S^2\) be the Gauss image of \(W_i^+\).

### 2.1 Cap image versus vertex normal cone

A convex body of constant width two is strictly convex. Its reverse Gauss map satisfies

\[
R_K(-n)=R_K(n)-2n.
\]

Take a point \(x\in C_A\). Since \(C_A\subset S(A,2)\), its outward normal is

\[
n=\frac{x-A}{2}.
\]

The antipodal support point is therefore

\[
x-2n=A.
\]

Hence every normal in \(-\Omega_A\) is a supporting normal at the vertex \(A\).

Conversely, if \(m\) is a supporting normal at \(A\), then the opposite support point is

\[
R_K(-m)=A-2m.
\]

It lies on \(\partial K\cap S(A,2)\), which is exactly the spherical cap \(C_A\) including its boundary. Thus \(-m\in\Omega_A\). Therefore the full normal cone at the vertex is

\[
N_K(A)=-\Omega_A.
\]

The same statement holds at all four vertices.

### 2.2 Opposite wedge Gauss images

The Peabody binormal pairing sends every smooth point of \(W_i^+\) to a point of \(W_i^-\) at distance two, with parallel tangent planes orthogonal to the joining segment. Their outward normals are opposite. Therefore

\[
\operatorname{Gauss}(W_i^-)=-\Gamma_i,
\qquad
|\operatorname{Gauss}(W_i^-)|=|\Gamma_i|.
\]

### 2.3 Partition of the unit normal sphere

Apart from patch boundaries of spherical measure zero, the smooth-patch Gauss images and the four vertex normal cones partition \(S^2\). Hence

\[
4\pi
=2\sum_{v\in\{A,B,C,D\}}|\Omega_v|
 +2\sum_{i=1}^3|\Gamma_i|.
\]

Thus

\[
\sum_v|\Omega_v|=2\pi-\sum_{i=1}^3|\Gamma_i|.
\]

A radius-two sphere scales its Gauss image area by \(2^2=4\). Consequently,

\[
\sum_v |C_v|
=4\sum_v|\Omega_v|
=8\pi-4\sum_{i=1}^3|\Gamma_i|.
\]

Adding the six wedge-pod areas gives

\[
S(K)
=8\pi+
\sum_{i=1}^3
\left(
|W_i^+|+|W_i^-|-4|\Gamma_i|
\right).
\]

Define the local pair functional

\[
\Psi_i:=|W_i^+|+|W_i^-|-4|\Gamma_i|.
\]

The three regular-tetrahedron opposite-edge configurations are congruent. An order-two tetrahedral isometry exchanges the two edges in any one pair, so interchanging the elliptic and hyperbolic devices does not change \(\Psi_i\). Therefore there is one scalar function \(\Psi(e)\) such that

\[
S(K)=8\pi+\sum_{i=1}^3\Psi(e_i).
\]

This proves exact additivity and exact orientation independence for \(0<e_i<1\). The explicit formulas below are continuous at \(e=0\), so the identity extends to Meissner degenerations by taking limits.

---

## 3. Canonical confocal chart for one pair

Fix an orthonormal local frame \((\mathbf k,\mathbf p,\mathbf q)\). Let

\[
e=\frac ca\in[0,1),
\qquad
b=a\sqrt{1-e^2},
\]

with the regular-tetrahedron beam constraints encoded by

\[
b^2=\frac{3+3e^2+4\sqrt2\,e}{1-e^2}.
\]

Introduce endpoint parameters

\[
\theta=\arccos\frac1b,
\qquad
\eta=\operatorname{arsinh}\frac1b,
\qquad
u=\sin\theta,
\qquad
v=\cosh\eta.
\]

The ellipse and hyperbola are parameterized by

\[
s=b\cos t,
\qquad
r=b\sinh\xi,
\]

with

\[
t\in[\theta,\pi-\theta],
\qquad
\xi\in[-\eta,\eta].
\]

After an irrelevant common translation, their centers can be written

\[
X(t)=a\sin t\,\mathbf k+b\cos t\,\mathbf p,
\]

\[
Y(\xi)=ae\cosh\xi\,\mathbf k+b\sinh\xi\,\mathbf q.
\]

Set

\[
D=\cosh\xi-e\sin t.
\]

Then the center distance and pea radii are

\[
d=\|X-Y\|=aD,
\]

\[
R_E=ae(\sin t-\nu),
\qquad
R_H=a(v-\cosh\xi).
\]

The confocal identity is exactly

\[
d+R_E+R_H=2.
\]

The unit normal pointing from the hyperbolic center toward the elliptic center is

\[
n(t,\xi)=
\frac{
(\sin t-e\cosh\xi)\mathbf k
+\sqrt{1-e^2}\cos t\,\mathbf p
-\sqrt{1-e^2}\sinh\xi\,\mathbf q
}{D}.
\]

Direct differentiation gives the conformal Gauss-chart identities

\[
n_t\cdot n_\xi=0,
\qquad
\|n_t\|=\|n_\xi\|=\frac bd.
\]

Therefore the spherical area element on \(\Gamma(e)\) is

\[
d\omega=\frac{b^2}{d^2}\,dt\,d\xi.
\]

---

## 4. Wedge areas and the scalar pair functional

The two opposite boundary points are

\[
U_E=X+R_E n,
\qquad
U_H=Y-R_H n.
\]

Using \(X-Y=dn\) and \(d+R_E+R_H=2\), differentiation collapses to

\[
(U_E)_t=(2-R_H)n_t,
\qquad
(U_E)_\xi=R_E n_\xi,
\]

\[
(U_H)_t=-R_H n_t,
\qquad
(U_H)_\xi=-(2-R_E)n_\xi.
\]

Hence

\[
|W_E(e)|
=\int\!\!\int
R_E(2-R_H)\frac{b^2}{d^2}\,dt\,d\xi,
\]

\[
|W_H(e)|
=\int\!\!\int
R_H(2-R_E)\frac{b^2}{d^2}\,dt\,d\xi,
\]

and

\[
|\Gamma(e)|
=\int\!\!\int\frac{b^2}{d^2}\,dt\,d\xi.
\]

The three terms combine to

\[
\boxed{
\Psi(e)
=-2b^2
\int_{\theta}^{\pi-\theta}
\int_{-\eta}^{\eta}
\frac{d+R_E R_H}{d^2}\,d\xi\,dt .
}
\]

This two-dimensional expression already proves that the exact family volume is a sum of three local scalar contributions.

---

## 5. Exact reduction to one dimension

For fixed \(t\), put

\[
A=\sin t,
\qquad
C=eA,
\qquad
y=\tanh\frac\eta2.
\]

Define

\[
I(C)
:=\int_{-\eta}^{\eta}\frac{d\xi}{\cosh\xi-C}
=\frac{4}{\sqrt{1-C^2}}
\arctan\left(
 y\sqrt{\frac{1+C}{1-C}}
\right).
\]

Also,

\[
\int_{-\eta}^{\eta}
\frac{v-\cosh\xi}{(\cosh\xi-C)^2}\,d\xi
=(v-C)I'(C)-I(C).
\]

Using \(\sinh\eta=1/b\), the derivative combination simplifies to

\[
(v-C)I'(C)-I(C)
=\frac{(vC-1)I(C)+2/b}{1-C^2}.
\]

The symmetry \(\sin(\pi-t)=\sin t\) now yields the one-dimensional formula

\[
\boxed{
\Psi(e)
=-4b^2
\int_{\theta}^{\pi/2}
\left[
\frac{I(e\sin t)}a
+
\frac{e(\sin t-\nu)}{1-e^2\sin^2t}
\left(
(ve\sin t-1)I(e\sin t)+\frac2b
\right)
\right]dt .
}
\]

The integrand is smooth for every fixed \(0\le e<1\). This is the promised exact scalar formula.

At \(e=0\),

\[
b=a=\sqrt3,
\qquad
\pi-2\theta=\arccos\frac13=:\alpha,
\qquad
I(0)=\frac\pi3,
\]

and therefore

\[
\boxed{
\Psi(0)=-\frac{2\pi}{\sqrt3}\arccos\frac13.
}
\]

Substitution into

\[
V_1=\frac{2\pi}{3}+\frac18\sum_i\Psi(e_i)
\]

recovers exactly

\[
V_M
=\pi\left(
\frac23-\frac{\sqrt3}{4}\arccos\frac13
\right).
\]

---

## 6. Exact endpoint derivative

Differentiate the one-dimensional expression at \(e=0\), including the moving lower limit \(\theta(e)\). The required endpoint values are

\[
b(0)=a(0)=\sqrt3,
\quad
\theta'(0)=\frac23,
\quad
I(0)=\frac\pi3,
\quad
\partial_C I(0)=1.
\]

After simplification,

\[
\Psi'(0)
=4\left[
\frac{5\pi}{3\sqrt3}-3
+\alpha\left(
\frac{3\sqrt2}{2}-\frac{5\sqrt6\,\pi}{18}
\right)
\right]
=0.011920833656305684\ldots .
\]

Thus

\[
\boxed{
\Phi'(0)=\frac{\Psi'(0)}8
=0.0014901042070382106\ldots>0.
}
\]

This agrees with the earlier mesh secant slope \(1.4907\times10^{-3}\) but no longer depends on mesh extrapolation.

---

## 7. Runtime validation

The Python audit independently evaluates \(\Psi\) in two ways:

1. the two-dimensional confocal integral, with the two wedge areas and Gauss-image area retained separately;
2. the reduced one-dimensional integral.

It also checks the collapsed identity

\[
|W_E|+|W_H|-4|\Gamma|
=-2\int_{\Gamma}(d+R_E R_H)\,d\omega
\]

and finite-difference versions of the conformal and surface-Jacobian identities.

On the recorded validation grid, including \(e=0.999\):

- maximum one-dimensional versus two-dimensional discrepancy: `4.21e-13`;
- maximum internal two-dimensional identity discrepancy: `3.89e-13`;
- Meissner reconstruction error: `3.89e-16`;
- exact \(\Phi'(0)\): `1.490104207038224e-3` in binary64;
- all sampled scalar derivatives were positive.

Python 3.13.5 executed all validation gates successfully. A matching base-R script is included, but `Rscript` was unavailable in the assistant environment and therefore the R implementation was not runtime-tested here.

Re-evaluating the ten best previous Sobol candidates with the exact additive formula leaves all ten above Meissner. The former best candidate has exact-formula width-one volume

\[
0.419909222236944\ldots,
\]

which is above \(V_M\) by \(4.9176271864\times10^{-5}\). Its difference from the prior refined mesh estimate is only \(-7.10\times10^{-9}\).

---

## 8. What remains

The additivity question is closed at theorem-architecture level: the exact continuum formula separates pairwise, and orientation bits disappear.

The remaining mathematical task is the scalar inequality

\[
\Phi(e)\ge0\quad(0\le e<1),
\]

or the stronger monotonicity statement

\[
\Phi'(e)>0\quad(0\le e<1).
\]

Numerically, \(\Phi\) is positive, increasing, and concave, with \(\Phi'(e)\downarrow0\) toward the parabolic endpoint. However, differentiating the local two-dimensional integrand does **not** produce a pointwise nonnegative function; positive and negative regions cancel. The same remains true after integrating out either one of the two confocal coordinates. Therefore the hoped-for proof is not an immediate pointwise-positivity argument.

The next viable routes are:

1. integrate by parts in the one-dimensional formula to expose a positive kernel;
2. reparameterize by the rapidity \(\lambda=\operatorname{artanh}e\), for which
   \(b^2=\cosh(2\lambda+2\operatorname{arsinh}1)\), and seek a convexity or comparison identity;
3. if the analytic sign does not collapse quickly, certify the one-dimensional derivative with a modest outward-rounded interval partition.

This is now a finite one-variable theorem problem, not a three-parameter geometry or meshing campaign.

---

## 9. Claim ledger

| Category | Claim |
|---|---|
| **ESTABLISHED FROM SOURCES** | The six wedge-pod/four-cap assembly is a width-two convex body; the opposite wedge-pod patches are paired by length-two binormals; the generic surface is smooth except at four vertices. |
| **PROPOSED THEOREM — COMPLETE DERIVATION** | Exact pairwise additivity and orientation independence: \(S=8\pi+\sum_i\Psi(e_i)\), hence \(V_1=V_M+\sum_i\Phi(e_i)\). |
| **ALGEBRAICALLY DERIVED** | The conformal normal chart, wedge Jacobians, two-dimensional pair integral, one-dimensional reduction, \(\Psi(0)\), and exact \(\Phi'(0)\). |
| **RUNTIME-TESTED PYTHON** | Independent 1D/2D quadrature agreement, local differential identities, Meissner recovery, and positive derivative samples. |
| **PREPARED BUT NOT RUNTIME-TESTED** | Matching base-R formula audit. |
| **NOT ESTABLISHED** | \(\Phi(e)\ge0\) on the full interval, Peabody-family minimality, a body below Meissner, or any improvement of the universal lower bound. |

---

## 10. Strategic classification

```text
GO_PEABODY_EXACT_ADDITIVITY_REDUCTION
```

The numerical structural signal has become an exact formula. The appropriate next checkpoint is one bounded attempt at the one-variable sign theorem. A large new search is not justified.

## References

- I. Arelio, L. Montejano, D. Oliveros, *Peabodies of Constant Width*, Beiträge zur Algebra und Geometrie 64 (2023), 367–385; arXiv:2107.05769.
- B. Bogosel, *Volume computation for Meissner polyhedra and applications*, arXiv:2310.17672.
- B. Kawohl, C. Weber, *Meissner's Mysterious Bodies*, The Mathematical Intelligencer 33 (2011), 94–101.
- H. Martini, L. Montejano, D. Oliveros, *Bodies of Constant Width*, Birkhäuser, 2019.
