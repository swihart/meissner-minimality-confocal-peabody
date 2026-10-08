# Independent rederivation of the one-pair Peabody volume contribution

## Audit status

This note rederives the one-pair formula from the confocal geometry without importing the
principal Python implementation. The accompanying program
`python/independent_one_pair_rederivation.py` implements the derivation independently.

A notation defect in the frozen additivity note is resolved here: after defining
`u=sin(theta)`, two formulas display `nu`. Those occurrences must be read as `u`; the frozen
code uses `u`, and the independent derivation below confirms that choice.

## 1. Regular-tetrahedron confocal chart

Work first at width two. Choose an orthonormal frame `(k,p,q)` and let

\[
e=\frac ca\in[0,1),\qquad b=a\sqrt{1-e^2}.
\]

Parameterize the ellipse and hyperbola center curves by

\[
X(t)=a\sin t\,k+b\cos t\,p,
\]

\[
Y(\xi)=ae\cosh\xi\,k+b\sinh\xi\,q.
\]

The longitudinal beams have length two. Thus their endpoint parameters satisfy

\[
b\cos\theta=1,\qquad b\sinh\eta=1.
\]

Put

\[
u=\sin\theta=\sqrt{1-\frac1{b^2}},\qquad
v=\cosh\eta=\sqrt{1+\frac1{b^2}}.
\]

At a cross-beam endpoint the regular-tetrahedron distance is two. Orthogonality of the beam
directions reduces this to

\[
a(u-ev)=\sqrt2.
\]

Squaring and using `a^2=b^2/(1-e^2)` gives the admissible root

\[
\boxed{
 b^2=\frac{3+3e^2+4\sqrt2\,e}{1-e^2}.
}
\]

The other algebraic root has the wrong confocal orientation. The same identity implies

\[
a(v-eu)=2.
\]

This last equality is the width-two constant in the distance-plus-radii identity below.

## 2. Center distance and pea radii

A direct expansion gives

\[
\|X(t)-Y(\xi)\|^2
=a^2(\cosh\xi-e\sin t)^2.
\]

On the chosen parameter rectangle the positive square root is

\[
d=a(\cosh\xi-e\sin t).
\]

The radii of the two moving spheres are

\[
R_E=ae(\sin t-u),
\]

\[
R_H=a(v-\cosh\xi).
\]

Therefore

\[
\begin{aligned}
d+R_E+R_H
&=a(\cosh\xi-e\sin t)
  +ae(\sin t-u)+a(v-\cosh\xi)\\
&=a(v-eu)=2.
\end{aligned}
\]

This reproduces the confocal Peabody identity in the canonical chart.

## 3. Normal map and conformality

Define the unit vector from the hyperbolic center toward the elliptic center by

\[
n=\frac{X-Y}{d}.
\]

Substitution yields

\[
n(t,\xi)=
\frac{
(\sin t-e\cosh\xi)k
+\sqrt{1-e^2}\cos t\,p
-\sqrt{1-e^2}\sinh\xi\,q
}{\cosh\xi-e\sin t}.
\]

Differentiating and simplifying gives

\[
n_t\cdot n_\xi=0,
\qquad
\|n_t\|=\|n_\xi\|=\frac bd.
\]

Hence the Gauss-image area element is

\[
\boxed{d\omega=\frac{b^2}{d^2}\,dt\,d\xi.}
\]

The independent numerical audit checks the unit-normal, orthogonality, and Jacobian identities
through the equality of four integral representations.

## 4. The two opposite wedge-pod surfaces

The paired boundary points are

\[
U_E=X+R_E n,
\qquad
U_H=Y-R_H n.
\]

Since `X-Y=dn`, differentiation gives

\[
X_t=d_t n+d n_t,
\qquad
Y_\xi=-d_\xi n-d n_\xi.
\]

Differentiating `d+R_E+R_H=2` in the appropriate variable cancels the normal components, leaving

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

Because `n_t` and `n_xi` are orthogonal, the physical areas are

\[
|W_E|=\iint R_E(2-R_H)\,d\omega,
\]

\[
|W_H|=\iint R_H(2-R_E)\,d\omega.
\]

The common Gauss-image area is

\[
|\Gamma|=\iint d\omega.
\]

## 5. Local pair functional

The normal-sphere bookkeeping subtracts four copies of the Gauss-image area from the two
physical wedge areas. Thus

\[
\Psi(e)=|W_E|+|W_H|-4|\Gamma|.
\]

The integrand simplifies exactly:

\[
\begin{aligned}
R_E(2-R_H)+R_H(2-R_E)-4
&=2(R_E+R_H)-2R_ER_H-4\\
&=-2(d+R_ER_H),
\end{aligned}
\]

where `R_E+R_H=2-d` was used. Therefore

\[
\boxed{
\Psi(e)
=-2b^2
\int_\theta^{\pi-\theta}
\int_{-\eta}^{\eta}
\frac{d+R_ER_H}{d^2}\,d\xi\,dt.
}
\]

This is the first independently rederived one-pair formula.

## 6. Reduction of the xi integral

For fixed `t`, set

\[
A=\sin t,\qquad C=eA,\qquad y=\tanh(\eta/2).
\]

The basic integral is

\[
I(C)=\int_{-\eta}^{\eta}\frac{d\xi}{\cosh\xi-C}
=\frac{4}{\sqrt{1-C^2}}
\arctan\!\left(y\sqrt{\frac{1+C}{1-C}}\right).
\]

Differentiation under this elementary integral gives

\[
\int_{-\eta}^{\eta}
\frac{v-\cosh\xi}{(\cosh\xi-C)^2}\,d\xi
=(v-C)I'(C)-I(C).
\]

Using `sinh(eta)=1/b`, the derivative combination reduces to

\[
(v-C)I'(C)-I(C)
=\frac{(vC-1)I(C)+2/b}{1-C^2}.
\]

Symmetry about `t=pi/2` then gives

\[
\boxed{
\Psi(e)=-4b^2\int_\theta^{\pi/2}
\left[
\frac{I(e\sin t)}a
+
\frac{e(\sin t-u)}{1-e^2\sin^2t}
\left((ve\sin t-1)I(e\sin t)+\frac2b\right)
\right]dt.
}
\]

## 7. Fixed beam-coordinate formula

Set

\[
x=b\cos t.
\]

Then `x` runs from one to zero as `t` runs from `theta` to `pi/2`, and

\[
\sin t=\sqrt{1-\frac{x^2}{b^2}}.
\]

Reversing the limits removes the moving endpoint and gives

\[
\Psi(e)=\int_0^1 H(e,x)\,dx,
\]

where the exact function `H` is implemented independently in the release-audit Python and R
programs. This formula is algebraically equivalent to the stable `q=(1-e)/(1+e)` chart used by
the interval certificates.

## 8. Meissner endpoint

At `e=0`,

\[
a=b=\sqrt3,
\qquad
I(0)=\frac\pi3,
\qquad
\pi-2\theta=\arccos\frac13.
\]

Thus

\[
\boxed{
\Psi(0)=-\frac{2\pi}{\sqrt3}\arccos\frac13.
}
\]

The exact width-one Meissner volume follows after the normalization audited separately:

\[
V_M=\frac{2\pi}{3}+\frac{3\Psi(0)}8
=\pi\left(\frac23-\frac{\sqrt3}{4}\arccos\frac13\right).
\]

## 9. Independent computational gates

The release-audit implementation compares, at high precision:

- the two-dimensional wedge/Gauss formula;
- its collapsed two-dimensional form;
- the reduced one-dimensional formula;
- the fixed beam-coordinate formula;
- the stable q-chart formula.

The required classification is

```text
PEABODY_INDEPENDENT_ONE_PAIR_REDERIVATION_PASS
```

Numerical quadrature is audit evidence. The theorem still relies on the frozen exact derivation and
outward-rounded interval certificates.
