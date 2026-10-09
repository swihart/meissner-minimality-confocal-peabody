# Reviewer Point 3 — Complete one-pair derivation and global branch control

## Status

**Closed internally after a second derivation and exact symbolic audit. External line-by-line review remains recommended before journal submission.**

This note replaces the earlier derivation draft. It retains the center-distance, normal-chart, wedge-Jacobian, and one-dimensional reductions, and adds the missing substitution table from the fixed-interval formula to the stable `q`-chart, an explicit derivation of `Psi(0)`, and a corrected branch statement at the parabolic endpoint.

## 1. Center distance and width identity

Let

\[
 X(t)=a\sin t\,\mathbf k+b\cos t\,\mathbf p,
\]

\[
 Y(\xi)=ae\cosh\xi\,\mathbf k+b\sinh\xi\,\mathbf q,
\]

where `b^2=a^2(1-e^2)`. Then

\[
 \frac{|X-Y|^2}{a^2}
 = (\sin t-e\cosh\xi)^2
 +(1-e^2)(\cos^2t+\sinh^2\xi).
\]

Using `cosh^2 xi=1+sinh^2 xi`, this becomes

\[
 \frac{|X-Y|^2}{a^2}
 =(\cosh\xi-e\sin t)^2.
\]

On the parameter rectangle, `cosh xi-e sin t >= 1-e>0`, so

\[
 d:=|X-Y|=a(\cosh\xi-e\sin t).
\]

With

\[
 R_E=ae(\sin t-u_0),
 \qquad
 R_H=a(v_0-\cosh\xi),
\]

and `a(v_0-eu_0)=2`, one obtains

\[
 d+R_E+R_H=2.
\]

## 2. Normal chart and conformality

Set

\[
 D_0=\cosh\xi-e\sin t,
 \qquad
 s=\sqrt{1-e^2}.
\]

The unit vector from `Y` to `X` is

\[
 n=\frac{U}{D_0},
\]

where

\[
 U=(\sin t-e\cosh\xi)\mathbf k
   +s\cos t\,\mathbf p
   -s\sinh\xi\,\mathbf q.
\]

Since `|U|=D_0`, differentiation of `n=U/D_0` gives

\[
 |n_r|^2=\frac{|U_r|^2-D_{0,r}^2}{D_0^2}
\]

for `r=t,xi`. Directly,

\[
 |U_t|^2-D_{0,t}^2=s^2,
 \qquad
 |U_\xi|^2-D_{0,\xi}^2=s^2,
\]

and

\[
 U_t\cdot U_\xi=D_{0,t}D_{0,\xi}.
\]

Hence

\[
 n_t\cdot n_\xi=0,
 \qquad
 |n_t|=|n_\xi|=\frac{s}{D_0}=\frac bd.
\]

Thus the Gauss-image area element is

\[
 d\omega=|n_t\times n_\xi|\,dt\,d\xi
 =\frac{b^2}{d^2}\,dt\,d\xi.
\]

## 3. Wedge-pod Jacobians

The paired boundary points are

\[
 U_E=X+R_En,
 \qquad
 U_H=Y-R_Hn.
\]

Because `X=Y+dn` and `d+R_E+R_H=2`, also

\[
 U_E=Y+(2-R_H)n,
 \qquad
 U_H=X-(2-R_E)n.
\]

Choose whichever representation removes the differentiated center curve. Then

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

Since `n_t` and `n_xi` are orthogonal,

\[
 dA_E=R_E(2-R_H)\frac{b^2}{d^2}\,dt\,d\xi,
\]

\[
 dA_H=R_H(2-R_E)\frac{b^2}{d^2}\,dt\,d\xi.
\]

The normal chart is injective on a smooth wedge interior by strict convexity, so its area element integrates the Gauss-image area without multiplicity. Since `R_E+R_H=2-d`,

\[
 R_E(2-R_H)+R_H(2-R_E)-4
 =-2(d+R_ER_H).
\]

Therefore

\[
 \Psi(e)
 =-2b^2\int_\theta^{\pi-\theta}\int_{-\eta}^{\eta}
 \frac{d+R_ER_H}{d^2}\,d\xi\,dt.
\]

## 4. Elementary integration in `xi`

For fixed `t`, put

\[
 A=\sin t,
 \qquad C=eA,
 \qquad y=\tanh(\eta/2).
\]

The substitution `z=tanh(xi/2)` gives

\[
 \cosh\xi=\frac{1+z^2}{1-z^2},
 \qquad
 d\xi=\frac{2\,dz}{1-z^2}.
\]

Hence

\[
 I(C):=\int_{-\eta}^{\eta}\frac{d\xi}{\cosh\xi-C}
 =\frac4{\sqrt{1-C^2}}
 \arctan\left(y\sqrt{\frac{1+C}{1-C}}\right).
\]

Also,

\[
 \frac{v_0-\cosh\xi}{(\cosh\xi-C)^2}
 =\frac{v_0-C}{(\cosh\xi-C)^2}
  -\frac1{\cosh\xi-C},
\]

so its integral is `(v_0-C)I'(C)-I(C)`. Differentiation of the displayed formula for `I`, followed by

\[
 1+z^2=\frac{(1-y^2)(v_0-C)}{1-C},
 \qquad
 \frac{2y}{1-y^2}=\sinh\eta=\frac1b,
\]

gives

\[
 (v_0-C)I'(C)-I(C)
 =\frac{(v_0C-1)I(C)+2/b}{1-C^2}.
\]

Substitution and the symmetry `sin(pi-t)=sin t` yield

\[
\begin{aligned}
 \Psi(e)=-4b^2\int_\theta^{\pi/2}
 \bigg[&\frac{I(e\sin t)}a\\
 &+\frac{e(\sin t-u_0)}{1-e^2\sin^2t}
 \left((v_0e\sin t-1)I(e\sin t)+\frac2b\right)
 \bigg]dt.
\end{aligned}
\]

## 5. Exact value at the Meissner endpoint

At `e=0`,

\[
 a=b=\sqrt3,
 \qquad
 \eta=\operatorname{arsinh}(1/\sqrt3)=\log\sqrt3.
\]

Therefore

\[
 y=\tanh(\eta/2)=2-\sqrt3=\tan(\pi/12),
\]

and

\[
 I(0)=4\arctan y=\frac\pi3.
\]

If `L=pi/2-theta=arcsin(1/sqrt3)`, then

\[
 \cos(2L)=1-2\sin^2L=\frac13,
\]

and `0<2L<pi`, so

\[
 L=\frac12\arccos\frac13.
\]

The second term in the one-dimensional integrand vanishes at `e=0`, hence

\[
 \Psi(0)
 =-4b^2\frac{I(0)}aL
 =-\frac{2\pi}{\sqrt3}\arccos\frac13.
\]

## 6. Fixed integration interval

Set

\[
 x=b\cos t.
\]

Because `b cos theta=1`, the interval `[theta,pi/2]` maps to `[1,0]`. Put

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

where

\[
 H(e,x)=-\frac{4b}{A}
 \left[
 \frac{I(C)}a
 +\frac{e(A-u_0)}{1-C^2}
 \left((v_0C-1)I(C)+\frac2b\right)
 \right].
\]

## 7. Complete substitution table for the stable `q`-chart

Let

\[
 q=\frac{1-e}{1+e},
 \qquad
 K=(1+\sqrt2)^2,
 \qquad
 D=\sqrt{K^2+q^2},
\]

\[
 R=\sqrt{K^2+q^2-2Kqx^2},
\]

\[
 T=\sqrt{2K(K^2+q^2)+K^2(1-q)^2x^2}.
\]

Then

\[
 e=\frac{1-q}{1+q},
 \qquad
 b=\frac{D}{\sqrt{2Kq}},
 \qquad
 a=\frac{(1+q)D}{2\sqrt{2K}\,q}.
\]

The elementary quantities in the fixed-interval formula become

\[
 A=\frac RD,
 \qquad
 u_0=\frac{K-q}{D},
 \qquad
 v_0=\frac{K+q}{D},
\]

\[
 C=\frac{(1-q)R}{(1+q)D},
\]

\[
 y=\frac{\sqrt{2Kq}}{K+q+D}.
\]

The last identity follows from

\[
 y=\frac{\sinh\eta}{\cosh\eta+1}
 =\frac{1/b}{v_0+1}.
\]

Furthermore,

\[
 1-C^2
 =\frac{2qT^2}{K(1+q)^2D^2}.
\]

Define

\[
 A_+=(1+q)D+(1-q)R,
 \qquad
 A_-=(1+q)D-(1-q)R.
\]

Then

\[
 A_+A_-=\frac{2q}{K}T^2.
\]

For `q>0`, all quantities are positive and

\[
 y\sqrt{\frac{1+C}{1-C}}
 =\frac{KA_+}{T(K+q+D)}=:Z.
\]

Thus

\[
 I(C)=4\frac{(1+q)D}{T}\sqrt{\frac K{2q}}\,\arctan Z.
\]

Two removable differences are rationalized as

\[
 A-u_0=\frac{q\delta}{D},
 \qquad
 \delta=\frac{2K(1-x^2)}{R+K-q},
\]

and

\[
 v_0C-1=\frac{qM}{(1+q)D^2},
\]

where

\[
 M=\frac{K(q-2Kx^2)}{R+K}
 +(1-K)R-K^2-qR-q-q^2.
\]

These formulas are obtained from

\[
 R^2-(K-q)^2=2Kq(1-x^2)
\]

and

\[
 R-K=\frac{q(q-2Kx^2)}{R+K}.
\]

## 8. Derivation of `P_1`, `P_2`, and `Q_0`

The first term in `H` is

\[
 -\frac{4b}{A}\frac{I(C)}a
 =-\frac{16\sqrt2(1+\sqrt2)(K^2+q^2)}{RT}\arctan Z.
\]

For the second term, first note

\[
 \frac{e(A-u_0)}{1-C^2}
 =\frac{K(1-q^2)D\delta}{2T^2}.
\]

Also,

\[
 (v_0C-1)I(C)+\frac2b
 =\frac{4\sqrt{Kq/2}}D
 \left(\frac MT\arctan Z+1\right).
\]

Finally,

\[
 -\frac{4b}{A}=-\frac{4D^2}{R\sqrt{2Kq}}.
\]

Multiplying and collecting the arctangent and algebraic parts gives

\[
 H(q,x)=(P_1+P_2)\arctan Z+Q_0,
\]

with

\[
 P_1=-\frac{16\sqrt2(1+\sqrt2)(K^2+q^2)}{RT},
\]

\[
 P_2=-\frac{4K(1-q^2)(K^2+q^2)\delta M}{RT^3},
\]

\[
 Q_0=-\frac{4K(1-q^2)(K^2+q^2)\delta}{RT^2}.
\]

No symbolic integration is used in this reduction.

## 9. Global arctangent branch control

For the original elliptic-hyperbolic chart with `0<=e<1`,

\[
 0\le C=e\sin t<1,
 \qquad
 y>0.
\]

Thus

\[
 y\sqrt{\frac{1+C}{1-C}}>0,
\]

and the geometric angle is represented by the principal arctangent in `(0,pi/2)`.

For `0<q<=1`, the identities above are equalities between positive quantities, not merely identities after squaring. Hence

\[
 y\sqrt{\frac{1+C}{1-C}}=Z>0
\]

and the principal branch is preserved globally on `(0,1]x[0,1]`.

At `q=0`, the original elliptic-hyperbolic expression is a limiting expression and should not be equated term-by-term with the indeterminate product `y sqrt((1+C)/(1-C))`. Instead, the stable expression

\[
 Z=\frac{K((1+q)D+(1-q)R)}{T(K+q+D)}
\]

extends real analytically and remains strictly positive at `q=0`. Therefore `arctan Z` extends continuously and analytically on the same principal branch to the parabolic endpoint. No multiple of `pi` can appear.

## 10. Parabolic regularity

On the closed square `0<=q,x<=1`,

\[
 D^2\ge K^2,
\]

\[
 R^2\ge(K-q)^2\ge(K-1)^2>0,
\]

\[
 T^2\ge2K^3>0.
\]

Also,

\[
 R+K-q\ge2(K-1)>0,
 \qquad
 R+K>0,
 \qquad
 K+q+D>0.
\]

Thus every radical and denominator is uniformly separated from zero, and the stable formula contains no negative power of `q`. It is therefore real analytic on a neighborhood of the closed square. This justifies differentiation under the fixed integral, including on slabs meeting `q=0`.

## 11. Audit conclusion

The complete chain

\[
 \text{center curves}
 \longrightarrow \Psi(e)
 \longrightarrow H(e,x)
 \longrightarrow H(q,x)
\]

is now displayed without a `direct calculation` gap. The exact symbolic audit checks all polynomial/radical identities after clearing positive denominators. The corrected branch statement distinguishes the genuine elliptic-hyperbolic range `q>0` from the analytic continuation at `q=0`.
