# Central interval certificate for the confocal Peabody scalar

**Date:** 2026-09-30  
**Scope:** width-one regular-tetrahedron confocal Peabodies only  
**Central classification:** `GO_PEABODY_CENTRAL_PHI_POSITIVITY_CERTIFIED`

## 1. Certified statement

Let

\[
\Phi(e)=\frac{\Psi(e)-\Psi(0)}8,
\qquad
\Psi(e)=\int_0^1 H(e,x)\,dx,
\]

where `H` is the frozen fixed-interval Peabody pair integrand. The certificate proves

\[
\boxed{\Phi(e)>0\qquad\left(0<e\le \frac{199}{200}\right).}
\]

The proof is split at the exact rational endpoint

\[
e_0=\frac1{100}.
\]

Near the Meissner endpoint it certifies a positive divided quotient. On the compact bulk it certifies `Phi` directly.

## 2. Authoritative formula and chart

The frozen chart is

\[
q=\frac{1-e}{1+e},\qquad e=\frac{1-q}{1+q}.
\]

The stable `q`-integrand is the exact algebraic rewrite already used in the certified tail. Put

\[
\kappa=1+\sqrt2,\qquad K=\kappa^2,
\]

\[
D=\sqrt{K^2+q^2},
\]

\[
R=\sqrt{K^2+q^2-2Kqx^2},
\]

\[
T=\sqrt{2K(K^2+q^2)+K^2(1-q)^2x^2},
\]

and

\[
\delta=\frac{2K(1-x^2)}{R+K-q},
\]

\[
M=\frac{K(q-2Kx^2)}{R+K}+(1-K)R-K^2-qR-q-q^2.
\]

Then

\[
P_1=-\frac{16\sqrt2\,\kappa(K^2+q^2)}{RT},
\]

\[
P_2=-\frac{4K(1-q^2)(K^2+q^2)\delta M}{RT^3},
\]

\[
Q_0=-\frac{4K(1-q^2)(K^2+q^2)\delta}{RT^2},
\]

\[
Z=\frac{K((1+q)D+(1-q)R)}{T(K+q+D)},
\]

and

\[
H(q,x)=(P_1+P_2)\arctan Z+Q_0.
\]

The original and stable formulas were compared at 110 decimal digits for the eleven mandated parameters and thirty additional dyadic parameters. There were 287 pointwise integrand comparisons and 41 independent quadrature comparisons. The largest observed integrand discrepancy was below `7e-109`; the largest integrated discrepancy was below `7e-111`.

All radicands and denominators are interval-certified positive on

\[
\frac1{399}\le q\le 1,\qquad 0\le x\le1.
\]

Thus the chart is branch-safe and smooth throughout the central rectangle.

## 3. Rigorous midpoint integration rule

For an `x`-panel `[a,b]` of width `h` and midpoint `m`, the certifier uses

\[
\int_a^b f(x)\,dx
\in
h f(m)+\frac{h^3}{24}\,f''([a,b]).
\]

The midpoint Peano kernel is nonnegative and has integral `h^3/24`, so an outward interval enclosure of the second derivative gives a rigorous signed remainder enclosure. A nested automatic-differentiation jet computes, with interval arithmetic, all four quantities needed by the proof:

\[
H,
\qquad H_q,
\qquad H_{xx},
\qquad H_{qxx}.
\]

For a parameter slab `Q=[q_-,q_+]` with midpoint `q_m`, the bulk proof uses the mean-value enclosure

\[
\Psi(q)
\in
\Psi(q_m)+(Q-q_m)\,\Psi_q(Q).
\]

The integrated quantity is the target; no pointwise sign condition on `H` is assumed.

## 4. Near-Meissner endpoint lemma

Define

\[
J(e)=\frac{\Phi(e)}e\quad(e>0),
\qquad
J(0)=\Phi'(0).
\]

The exact endpoint derivative is

\[
\boxed{
\Phi'(0)=\frac12\left[
\frac{5\pi}{3\sqrt3}-3
+\arccos\!\frac13
\left(
\frac{3\sqrt2}{2}-\frac{5\sqrt6\,\pi}{18}
\right)
\right].
}
\]

The local interval proof covers

\[
0\le e\le\frac1{100},
\qquad
\frac{99}{101}\le q\le1.
\]

It uses sixteen exact rational `q` slabs and ten rational `x` panels per slab, for 160 terminal boxes. On every slab it certifies the integrated derivative

\[
\Phi'(e)>\frac1{2000}.
\]

The weakest raw lower endpoint is

\[
0.0005415852980838714162751786042230447\ldots.
\]

By the fundamental theorem of calculus,

\[
\boxed{
J(e)=\frac1e\int_0^e\Phi'(t)\,dt\ge\frac1{2000}
\qquad\left(0<e\le\frac1{100}\right).
}
\]

The continuous extension at zero is the exact value above. In particular,

\[
\Phi\!\left(\frac1{100}\right)\ge\frac1{200000}.
\]

## 5. Compact bulk certificate

The bulk range is

\[
\frac1{100}\le e\le\frac{199}{200}.
\]

Starting from eight equal rational `e` segments, the certifier bisects only inconclusive segments. The final partition has:

- 43 exact rational parameter slabs;
- 10 rational `x` panels per slab;
- 430 terminal boxes;
- maximum bisection depth 8.

Every accepted slab proves the stronger simple conclusion

\[
\Phi(e)>\frac1{10^7}.
\]

The weakest raw lower endpoint is

\[
\boxed{
0.0000003289951660397968513639698874811370840941\ldots
}
\]

on the first bulk slab

\[
\left[\frac1{100},\frac{4293}{409600}\right].
\]

All exact partition endpoints are stored in `certificates/peabody_central_certificate.json` and `data/central_bulk_slab_summary.csv`.

## 6. Seam checks

The local and bulk certificates meet exactly at

\[
e=\frac1{100}.
\]

The central and previously certified tail certificates meet exactly at

\[
e=\frac{199}{200}
\quad\Longleftrightarrow\quad
q=\frac1{399}.
\]

There is no open seam, floating conversion, or uncovered parameter value.

## 7. Resource accounting

| Component | Parameter slabs | `x` panels | Terminal boxes |
|---|---:|---:|---:|
| Local endpoint | 16 | 10 | 160 |
| Compact bulk | 43 | 10 | 430 |
| **New central total** | — | — | **590** |
| Frozen tail | 5 | 400 | 2,000 |
| **Combined scalar certificate** | — | — | **2,590** |

The new central certificate uses 80-decimal `mpmath.iv` arithmetic. Its archived proof data occupy about 1.2 MB. The frozen limits were 10,000 new central boxes, 25 MB, and depth 24; the actual values are 590 boxes, about 1.2 MB, and depth 8.

## 8. Replays and adversarial checks

The following passed:

1. complete tail dependency replay;
2. original-versus-stable central comparison at 110 digits;
3. exact `Phi(0)=0` normalization;
4. exact recovery of `Phi'(0)`;
5. direct high-precision agreement of `Phi(e)/e` with the local bound;
6. independent 80- and 100-digit interval replays;
7. reverse adaptive-subdivision order with the same exact partition;
8. high-precision quadrature containment inside sampled terminal slabs;
9. deliberate sign reversal of the correction sector, which was detected;
10. shifted `Psi(0)` baseline, which correctly destroyed the certificate;
11. an under-resolved two-panel partition, which was rejected;
12. exact local-bulk seam;
13. exact central-tail seam;
14. automatic-differentiation checks against independent high-precision derivatives;
15. deterministic semantic clean replay.

## 9. Trust boundary

Proof authority is:

- Python integer and exact-rational control flow;
- `mpmath 1.3.0` interval arithmetic at the archived precision;
- the elementary interval operations `+`, `-`, `*`, `/`, `sqrt`, and `atan2`;
- the stated midpoint Peano-kernel identity;
- exact rational partition endpoints.

Floating-point quadratures are audit evidence only, not proof authority.

## 10. Claim ledger

| Category | Result |
|---|---|
| **Established from sources** | Peabody construction and constant width; inclusion of the Meissner and Robert limiting constructions. |
| **Frozen project derivation** | Exact three-pair additivity, orientation independence, and the one-pair definition of `Phi`. |
| **Certified before this campaign** | `Phi(e)>1/20000` for `199/200<=e<1`. |
| **Certified here** | `Phi(e)/e>=1/2000` for `0<=e<=1/100`; `Phi(e)>1/10^7` for `1/100<=e<=199/200`. |
| **Not claimed** | Global positivity of `Phi'`, global Meissner extremality, a universal lower-bound improvement, or arbitrary-Peabody minimality. |
