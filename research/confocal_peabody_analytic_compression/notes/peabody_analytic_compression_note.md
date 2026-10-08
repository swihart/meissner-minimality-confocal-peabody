# Analytical compression of the confocal Peabody positivity proof

**Date:** 2026-10-01  
**Scope:** width-one regular-tetrahedron confocal Peabodies only  
**Principal classification:** `GO_PEABODY_ANALYTIC_COMPRESSION_CONCAVITY_CERTIFIED`

## 1. Executive result

The previous restricted-family proof established

\[
\Phi(e)>0\qquad(0<e<1)
\]

by three separate interval blocks: a local endpoint certificate, a compact bulk certificate, and a tail certificate, using 2,590 terminal boxes in total.

The present compression replaces that three-block proposition by three ordinary lemmas:

1. **Parabolic endpoint lemma.** The stable fixed-interval formula extends continuously to \(e=1\), and
   \[
   \Phi(1)>\frac{3}{10000}.
   \]
2. **Strict concavity lemma.** On the whole open interval,
   \[
   \Phi''(e)<-\frac1{25000}\qquad(0<e<1).
   \]
3. **Chord lemma.** Concavity and the endpoint values imply
   \[
   \Phi(e)>\frac{3e}{10000}>0\qquad(0<e<1).
   \]

The finite verification now uses 324 terminal rectangles rather than 2,590: four panels for the parabolic endpoint and 32 rational parameter slabs with ten integration panels each for strict concavity.

This is still a computer-assisted proof, but it is substantially more analytical. The computation certifies one global structural property—strict concavity—rather than positivity separately on three parameter regions.

## 2. Stable chart and endpoint extension

Let

\[
q=\frac{1-e}{1+e},\qquad e=\frac{1-q}{1+q},
\]

so that \(e\in[0,1]\) corresponds to \(q\in[1,0]\). Write

\[
\Psi(q)=\int_0^1 H(q,x)\,dx,
\qquad
\Phi(e)=\frac{\Psi(q(e))-\Psi(1)}8.
\]

With

\[
\kappa=1+\sqrt2,\qquad K=\kappa^2=3+2\sqrt2,
\]

define

\[
D=\sqrt{K^2+q^2},
\]

\[
R=\sqrt{K^2+q^2-2Kqx^2},
\]

\[
T=\sqrt{2K(K^2+q^2)+K^2(1-q)^2x^2},
\]

\[
\delta=\frac{2K(1-x^2)}{R+K-q},
\]

\[
M=\frac{K(q-2Kx^2)}{R+K}+(1-K)R-K^2-qR-q-q^2,
\]

and

\[
Z=\frac{K((1+q)D+(1-q)R)}{T(K+q+D)}.
\]

The validated fixed-interval integrand is

\[
H(q,x)=(P_1+P_2)\arctan Z+Q_0,
\]

where

\[
P_1=-\frac{16\sqrt2\,\kappa(K^2+q^2)}{RT},
\]

\[
P_2=-\frac{4K(1-q^2)(K^2+q^2)\delta M}{RT^3},
\]

\[
Q_0=-\frac{4K(1-q^2)(K^2+q^2)\delta}{RT^2}.
\]

All radicands and denominators remain strictly positive on the closed square

\[
0\le q\le1,\qquad 0\le x\le1.
\]

Therefore \(H\), \(\Psi\), and the endpoint extension of \(\Phi\) are smooth on their closed parameter intervals.

At \(q=0\), put

\[
A=2K+x^2.
\]

Then the integrand simplifies to

\[
\begin{aligned}
H(0,x)=\bigg[
&-\frac{16\sqrt2\,\kappa}{\sqrt A}
+\frac{4(1-x^2)(A-1)}{A^{3/2}}
\bigg]\arctan\frac1{\sqrt A}
-\frac{4(1-x^2)}A.
\end{aligned}
\]

The endpoint value is

\[
\Phi(1)=\frac18\left(\int_0^1H(0,x)\,dx-\Psi(1)\right),
\]

where

\[
\Psi(1)=-\frac{2\pi}{\sqrt3}\arccos\frac13.
\]

A four-panel outward-rounded midpoint enclosure gives

\[
0.0003076528682490342052053580\ldots
<\Phi(1)<
0.0004451561703065328614450094\ldots .
\]

Hence

\[
\boxed{\Phi(1)>\frac3{10000}.}
\]

A separate 100-digit quadrature audit gives

\[
\Phi(1)=0.0003777843496914536189216521\ldots,
\]

but this decimal is audit evidence only.

## 3. Concavity identity

Differentiate through the fixed integral. Since

\[
q'(e)=-\frac{(1+q)^2}{2},
\qquad
q''(e)=\frac{(1+q)^3}{2},
\]

one obtains

\[
\boxed{
\Phi''(e)=\frac{(1+q)^3}{32}
\int_0^1\left((1+q)H_{qq}(q,x)+2H_q(q,x)\right)\,dx.
}
\]

Set

\[
C(q,x)=(1+q)H_{qq}(q,x)+2H_q(q,x).
\]

The certificate uses a third-order automatic-differentiation jet in \(q\) and a second-order jet in \(x\). On each exact rational slab

\[
Q_j=\left[\frac j{32},\frac{j+1}{32}\right],
\qquad j=0,\ldots,31,
\]

it first encloses

\[
\int_0^1C(q_j,x)\,dx
\]

at the slab midpoint \(q_j=(2j+1)/64\), then applies the centered mean-value form

\[
\int_0^1C(Q_j,x)\,dx
\subseteq
\int_0^1C(q_j,x)\,dx
+(Q_j-q_j)
\int_0^1C_q(Q_j,x)\,dx.
\]

Each \(x\)-integral uses ten rational panels and the rigorous midpoint enclosure

\[
\int_a^bf(x)\,dx
\in
h f(m)+\frac{h^3}{24}f''([a,b]).
\]

All 32 slabs prove

\[
\Phi''(e)<-\frac1{25000}.
\]

The weakest raw upper endpoint is

\[
-0.0000416798241713739432518832547351\ldots,
\]

which occurs on the first \(q\)-slab and remains strictly below

\[
-\frac1{25000}=-0.00004.
\]

Thus the extended scalar function is strictly concave on \([0,1]\).

## 4. Positivity by the chord inequality

For a concave function on \([0,1]\),

\[
\Phi(e)\ge(1-e)\Phi(0)+e\Phi(1).
\]

Here \(\Phi(0)=0\) exactly and \(\Phi(1)>3/10000\). Therefore, for every \(0<e<1\),

\[
\boxed{
\Phi(e)>\frac{3e}{10000}>0.
}
\]

This gives the restricted-family theorem immediately from the frozen exact additive identity

\[
\operatorname{Vol}K(\mathbf e,\boldsymbol\sigma)
=V_M+\Phi(e_1)+\Phi(e_2)+\Phi(e_3).
\]

Equality is possible only when \(e_1=e_2=e_3=0\).

## 5. Certificate size and validation

| Item | Result |
|---|---:|
| Endpoint panels | 4 |
| Concavity parameter slabs | 32 |
| Integration panels per concavity slab | 10 |
| Concavity terminal boxes | 320 |
| Total terminal boxes | **324** |
| Canonical precision | 80 decimal digits |
| Canonical runtime | about 31 seconds |
| Canonical proof data | 476,780 bytes |
| Previous direct positivity boxes | 2,590 |
| Box-count reduction | **87.5%** |

The following checks passed:

- 80-digit canonical replay;
- independent 100-digit replay;
- reverse slab-order replay;
- exact rational coverage of \([0,1]\) by the 32 slabs;
- independent high-precision evaluation of \(\Phi(1)\);
- independent numerical differentiation at seven representative slabs;
- numerical verification of the chain-rule identity for \(\Phi''\);
- agreement of the general \(q=0\) formula with the separately simplified endpoint formula;
- rejection of a 16-slab under-resolved control;
- rejection of a deliberate sign mutation in the correction sector;
- terminal-box metadata and hash checks.

The proof authority remains outward-rounded `mpmath.iv` interval arithmetic. High-precision quadrature and numerical differentiation are audit evidence only.

## 6. What this changes in the paper

The former scalar-certificate proposition can be replaced by the following sequence.

### Lemma 1 — parabolic endpoint

The function \(\Phi\) extends smoothly to \([0,1]\), satisfies \(\Phi(0)=0\), and obeys

\[
\Phi(1)>\frac3{10000}.
\]

### Lemma 2 — strict concavity

For every \(0<e<1\),

\[
\Phi''(e)<-\frac1{25000}.
\]

### Lemma 3 — scalar positivity

For every \(0<e<1\),

\[
\Phi(e)>\frac{3e}{10000}>0.
\]

The first two lemmas contain the finite verification. The third is an ordinary one-line consequence of concavity. The paper no longer needs separate local, bulk, and tail arguments or seam bookkeeping.

## 7. Claim ledger

| Category | Result |
|---|---|
| **Established from sources** | Regular-tetrahedron Peabody construction and constant width. |
| **Frozen project derivation** | Exact three-pair additivity, orientation independence, and fixed-interval formula. |
| **Certified previously** | Direct local/bulk/tail positivity by 2,590 interval boxes. |
| **Certified here** | Endpoint bound \(\Phi(1)>3/10000\); global strict concavity \(\Phi''<-1/25000\); chord bound \(\Phi(e)>3e/10000\). |
| **Method improvement** | The direct three-region scalar certificate is replaced by one endpoint lemma and one global concavity lemma. |
| **Not established** | Global Meissner extremality, a universal lower-bound improvement, or a theorem for non-regular Peabody assemblies. |

## 8. Classification

```text
GO_PEABODY_ANALYTIC_COMPRESSION_CONCAVITY_CERTIFIED
```

This result is a proof compression, not a new family search.
