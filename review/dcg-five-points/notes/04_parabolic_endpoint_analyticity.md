# Reviewer Point 4 — Real-analytic extension at the parabolic endpoint

## Status

**Closed analytically.**

Let

\[
K=(1+\sqrt2)^2=3+2\sqrt2>1,
\qquad 0\le q,x\le1,
\]

and define

\[
D^2=K^2+q^2,
\]

\[
R^2=K^2+q^2-2Kqx^2,
\]

\[
T^2=2K(K^2+q^2)+K^2(1-q)^2x^2.
\]

The stable integrand is

\[
H(q,x)=(P_1+P_2)\arctan Z+Q_0,
\]

where all coefficients are rational combinations of \(q,x,D,R,T\) and the denominators

\[
R+K-q,
\qquad R+K,
\qquad T,
\qquad K+q+D.
\]

The following explicit bounds hold on the complete closed square:

\[
D^2\ge K^2>0,
\]

\[
R^2\ge K^2+q^2-2Kq=(K-q)^2\ge(K-1)^2>0,
\]

\[
T^2\ge2K^3>0.
\]

Consequently,

\[
R\ge K-q,
\]

and therefore

\[
R+K-q\ge2(K-q)\ge2(K-1)>0.
\]

Also

\[
R+K\ge2K-1>0,
\]

\[
K+q+D\ge2K>0,
\]

and the numerator and denominator of

\[
Z=\frac{K((1+q)D+(1-q)R)}{T(K+q+D)}
\]

are strictly positive.  Thus \(Z>0\) everywhere.

Every radicand stays uniformly separated from zero, every displayed denominator stays uniformly separated from zero, and the principal real square root and principal real arctangent are analytic on neighborhoods of the relevant compact ranges.  The stable formula contains no negative power of \(q\).  It follows that \(H\) is real analytic on an open neighborhood of \([0,1]^2\).

In particular, all derivatives used by the concavity certificate extend continuously to the slabs meeting \(q=0\).  Differentiation under

\[
\Psi(q)=\int_0^1H(q,x)\,dx
\]

is justified by uniform boundedness of the derivatives on the compact square.  Hence \(\Psi\), and therefore the endpoint extension of \(\Phi\), is real analytic at \(q=0\).

The chord proof needs only continuity at the endpoints and concavity in the interior, but the stronger real-analytic statement is available at no additional computational cost.
