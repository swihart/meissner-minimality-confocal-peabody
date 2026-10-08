# Reviewer Point 3 — Full one-pair derivation and global arctangent branch control

## Status

**Detailed derivation draft complete; exact algebraic cross-check passes.  Manuscript integration and independent human proofreading remain.**

This supplement expands the steps previously summarized as “direct calculation.”  It starts from the confocal center curves, derives the surface Jacobians, performs the \(\xi\)-integration, fixes the moving interval, and derives the stable \(q\)-chart.  A separate exact SymPy script verifies the rationalization identities.

## 1. Center distance

Let

\[
X(t)=a\sin t\,\mathbf k+b\cos t\,\mathbf p,
\]

\[
Y(\xi)=ae\cosh\xi\,\mathbf k+b\sinh\xi\,\mathbf q,
\]

where \(b^2=a^2(1-e^2)\).  Then

\[
\frac{|X-Y|^2}{a^2}
=(\sin t-e\cosh\xi)^2
 +(1-e^2)(\cos^2t+\sinh^2\xi).
\]

Expanding and using \(\cosh^2\xi=1+\sinh^2\xi\) gives

\[
\frac{|X-Y|^2}{a^2}
=\cosh^2\xi-2e\sin t\cosh\xi+e^2\sin^2t
=(\cosh\xi-e\sin t)^2.
\]

On the chosen parameter rectangle, \(\cosh\xi-e\sin t>0\), so

\[
d:=|X-Y|=a(\cosh\xi-e\sin t).
\]

The pea radii are

\[
R_E=ae(\sin t-u_0),
\qquad
R_H=a(v_0-\cosh\xi).
\]

The regular beam constraint is \(a(v_0-eu_0)=2\), hence

\[
d+R_E+R_H=2.
\]

## 2. Normal chart and conformality

Put

\[
D=\cosh\xi-e\sin t,
\qquad
s=\sqrt{1-e^2}.
\]

The unit vector from the hyperbolic center to the elliptic center is

\[
n=\frac{U}{D},
\]

where

\[
U=(\sin t-e\cosh\xi)\mathbf k
+s\cos t\,\mathbf p
-s\sinh\xi\,\mathbf q.
\]

Since \(|U|=D\), for either parameter \(r\),

\[
|n_r|^2=\frac{|U_r|^2-D_r^2}{D^2}.
\]

For \(t\),

\[
U_t=\cos t\,\mathbf k-s\sin t\,\mathbf p,
\qquad
D_t=-e\cos t,
\]

so

\[
|U_t|^2-D_t^2
=\cos^2t+s^2\sin^2t-e^2\cos^2t
=1-e^2=s^2.
\]

For \(\xi\),

\[
U_\xi=-e\sinh\xi\,\mathbf k-s\cosh\xi\,\mathbf q,
\qquad
D_\xi=\sinh\xi,
\]

and again

\[
|U_\xi|^2-D_\xi^2=s^2.
\]

Moreover,

\[
U_t\cdot U_\xi=-e\cos t\sinh\xi=D_tD_\xi,
\]

which gives

\[
n_t\cdot n_\xi=0.
\]

Therefore

\[
|n_t|=|n_\xi|=\frac{s}{D}=\frac b d,
\]

and the Gauss-image area element is

\[
d\omega=|n_t\times n_\xi|\,dt\,d\xi
=\frac{b^2}{d^2}\,dt\,d\xi.
\]

## 3. Wedge Jacobians

The paired boundary points are

\[
U_E=X+R_En,
\qquad
U_H=Y-R_Hn.
\]

Using \(X=Y+dn\) and \(d+R_E+R_H=2\),

\[
U_E=Y+(2-R_H)n,
\qquad
U_H=X-(2-R_E)n.
\]

Because \(Y,R_H\) are independent of \(t\), while \(X,R_E\) are independent of \(\xi\),

\[
(U_E)_t=(2-R_H)n_t,
\qquad
(U_E)_\xi=R_En_\xi,
\]

\[
(U_H)_t=-R_Hn_t,
\qquad
(U_H)_\xi=-(2-R_E)n_\xi.
\]

Since \(n_t\perp n_\xi\),

\[
dA_E=R_E(2-R_H)\frac{b^2}{d^2}\,dt\,d\xi,
\]

\[
dA_H=R_H(2-R_E)\frac{b^2}{d^2}\,dt\,d\xi.
\]

Subtracting four times the Gauss-image area gives

\[
R_E(2-R_H)+R_H(2-R_E)-4
=-2(d+R_ER_H),
\]

because \(R_E+R_H=2-d\).  Hence

\[
\Psi(e)
=-2b^2\int_\theta^{\pi-\theta}
\int_{-\eta}^{\eta}
\frac{d+R_ER_H}{d^2}\,d\xi\,dt.
\]

## 4. The elementary \(\xi\)-integration

For fixed \(t\), put

\[
A=\sin t,
\qquad
C=eA,
\qquad
y=\tanh\frac\eta2.
\]

The substitution \(z=\tanh(\xi/2)\) gives

\[
\cosh\xi=\frac{1+z^2}{1-z^2},
\qquad
d\xi=\frac{2\,dz}{1-z^2}.
\]

Therefore

\[
I(C):=\int_{-\eta}^{\eta}\frac{d\xi}{\cosh\xi-C}
=\int_{-y}^y\frac{2\,dz}{(1-C)+(1+C)z^2},
\]

and thus

\[
I(C)=\frac4{\sqrt{1-C^2}}
\arctan\left(y\sqrt{\frac{1+C}{1-C}}\right).
\]

Also,

\[
\int_{-\eta}^{\eta}
\frac{v_0-\cosh\xi}{(\cosh\xi-C)^2}\,d\xi
=(v_0-C)I'(C)-I(C).
\]

Differentiating the explicit formula for \(I\) gives

\[
I'(C)=\frac{CI(C)}{1-C^2}
+\frac{4z}{(1-C^2)^{3/2}(1+z^2)},
\]

where now \(z=y\sqrt{(1+C)/(1-C)}\).  Since

\[
1+z^2=\frac{(1-y^2)(v_0-C)}{1-C}
\]

and

\[
\frac{2y}{1-y^2}=\sinh\eta=\frac1b,
\]

one obtains

\[
(v_0-C)I'(C)-I(C)
=\frac{(v_0C-1)I(C)+2/b}{1-C^2}.
\]

Using the symmetry \(\sin(\pi-t)=\sin t\) gives the stated one-dimensional formula.

## 5. Fixed integration interval

Set

\[
x=b\cos t.
\]

Because \(b\cos\theta=1\), the interval \(\theta\le t\le\pi/2\) maps to \(1\ge x\ge0\).  Put

\[
A(e,x)=\sin t=\sqrt{1-\frac{x^2}{b^2}},
\qquad
C=eA.
\]

Since

\[
dt=-\frac{dx}{bA},
\]

we obtain

\[
\Psi(e)=\int_0^1H(e,x)\,dx,
\]

with

\[
H(e,x)
=-\frac{4b}{A}
\left[
\frac{I(C)}a
+\frac{e(A-u_0)}{1-C^2}
\left((v_0C-1)I(C)+\frac2b\right)
\right].
\]

This is the fixed-interval formula from which the stable chart is derived.

## 6. Stable \(q\)-chart

Let

\[
q=\frac{1-e}{1+e},
\qquad
K=(1+\sqrt2)^2,
\qquad
\rho^2=\frac Kq.
\]

Then

\[
1-e^2=\frac{4q}{(1+q)^2},
\]

\[
b^2=\frac{K^2+q^2}{2Kq},
\]

\[
a^2=\frac{(K^2+q^2)(1+q)^2}{8Kq^2}.
\]

Introduce

\[
D=\sqrt{K^2+q^2},
\]

\[
R=\sqrt{K^2+q^2-2Kqx^2},
\]

\[
T=\sqrt{2K(K^2+q^2)+K^2(1-q)^2x^2}.
\]

The shifted-rapidity radicals scale as

\[
\sqrt{\rho^4+1}=\frac Dq,
\qquad
\sqrt{\rho^4+1-2\rho^2x^2}=\frac Rq,
\qquad
\sqrt{2K(\rho^4+1)+(\rho^2-K)^2x^2}=\frac Tq.
\]

The apparent difference

\[
\frac{R-K+q}{q}
\]

is rationalized by

\[
R^2-(K-q)^2=2Kq(1-x^2),
\]

which gives

\[
\delta=\frac{2K(1-x^2)}{R+K-q}.
\]

The second removable quotient is

\[
\frac{(1-q)(K+q)R-(1+q)(K^2+q^2)}q.
\]

Using

\[
R-K=\frac{q(q-2Kx^2)}{R+K}
\]

reduces it to

\[
M=\frac{K(q-2Kx^2)}{R+K}
 +(1-K)R-K^2-qR-q-q^2.
\]

Substitution now gives

\[
P_1=-\frac{16\sqrt2(1+\sqrt2)(K^2+q^2)}{RT},
\]

\[
P_2=-\frac{4K(1-q^2)(K^2+q^2)\delta M}{RT^3},
\]

\[
Q_0=-\frac{4K(1-q^2)(K^2+q^2)\delta}{RT^2}.
\]

## 7. Global arctangent branch control

In the original formula,

\[
0\le C=e\sin t<1,
\]

and

\[
y=\tanh(\eta/2)>0.
\]

Therefore

\[
y\sqrt{\frac{1+C}{1-C}}>0,
\]

and the geometric angle is represented by the principal value in \((0,\pi/2)\).

In the \(q\)-chart, define

\[
A_+=(1+q)D+(1-q)R,
\qquad
A_-=(1+q)D-(1-q)R.
\]

The identity

\[
A_+A_-=\frac{2q}{K}T^2
\]

follows directly from the definitions of \(D,R,T\).  Rationalizing

\[
K+q-D=\frac{2Kq}{K+q+D}
\]

and using the preceding product identity gives

\[
y\sqrt{\frac{1+C}{1-C}}
=\frac{KA_+}{T(K+q+D)}=:Z.
\]

All factors in the last expression are strictly positive on the closed square \(0\le q,x\le1\).  The equality is obtained between positive quantities, not merely after squaring.  Hence no sign choice or multiple of \(\pi\) is introduced, and

\[
\arctan Z
\]

is the same principal analytic branch as the original geometric angle throughout the domain.

## 8. Exact machine check

The accompanying script `verify_formula_derivation_identities.py` reduces the following differences exactly to zero:

- the two beam-normalization identities;
- the rationalization of \(\delta\);
- the rationalization of \(M\);
- the angle-product identity;
- the cross-multiplied equality of the original and stable arctangent arguments;
- the scaling identities for \(P_2\) and \(Q_0\).

The script is an audit of the written derivation, not a substitute for it.
