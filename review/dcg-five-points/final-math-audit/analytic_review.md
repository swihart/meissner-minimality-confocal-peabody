# Bounded final analytic audit — Confocal Peabody

Disposition: this is the independent review of the pre-correction `b9fb7c5` manuscript. Its bounded recommendations are incorporated in the current source and resolved in `FINAL_MATHEMATICAL_AUDIT.md`. Original line references refer to that input checkpoint. This is an internal AI-assisted review, not an external human report.

Date: 2026-10-09. Reviewed source: the closeout manuscript corresponding to user commit `b9fb7c5`, before any final-audit corrections. References below are original source line numbers in `review/dcg-five-points/manuscript/main_dcg_closeout_review.tex`.

## Result

**ANALYTIC_CHAIN_PASS_WITH_TWO_LOCAL_EXPOSITORY_REPAIRS.** No incorrect scalar identity, branch change, endpoint singularity, chain-rule factor, quadrature implication, or positivity/equality deduction was found. This is a bounded internal analytic review, conditional on the geometric source-family and normal-partition arguments reviewed by the separate geometry auditors. It is not completed external human proofreading and does not report a fresh Arb replay.

The two local repairs are: (1) explicitly demonstrate that the normal chart is one-to-one before integrating its area element without multiplicity; (2) use finite outward-rounded decimals, rather than ellipses or nearest-rounded displays, whenever a displayed decimal is asserted as a rigorous bound. Neither repair changes the scalar function, certificate, partition, or theorem constants.

## Scope and evidence

Read the complete current manuscript; notes `03_formula_derivation_and_branch_control.md` and `04_parabolic_endpoint_analyticity.md`; the independent release-audit one-pair derivation; the symbolic identity checker; and the proof-relevant definition, derivative-jet, midpoint, endpoint, and slab routines in `arb/peabody_arb_concavity.py`.

No numerical search, refinement, new parameter sampling, or new interval certification was performed. Attempting to replay the existing SymPy identity checker failed before calculations because `sympy` is not installed in this runtime. No algebraic check failed. The verification below was performed directly by exact analytic manipulation; archived symbolic checks are not relabeled as new executions.

## Findings and exact checks

### 1. Width and area normalization — PASS

Lines 283–320 give

\[
S_2=8\pi+\sum_i\Psi(e_i),\qquad
V_2=S_2-8\pi/3=16\pi/3+\sum_i\Psi(e_i).
\]

Scaling width two to width one gives a factor `1/8` in volume. Consequently

\[
\Phi(e)=[\Psi(e)-\Psi(0)]/8.
\]

Together with the independently evaluated Meissner value

\[
\Psi(0)=-\frac{2\pi}{\sqrt3}\arccos(1/3),
\]

this recovers

\[
\frac{2\pi}{3}+\frac{3\Psi(0)}8
=\pi\left(\frac23-\frac{\sqrt3}{4}\arccos(1/3)\right).
\]

There is no missing factor of two, four, or eight in this chain.

### 2. Center-distance, normal metric, and wedge Jacobians — PASS

Lines 344–435 correctly obtain `d=a(cosh(xi)-e sin(t))`. The unsquared factor is at least `1-e>0`, so taking this square root is valid throughout `0<=e<1`.

Writing `s=sqrt(1-e^2)`, the differentiation of `n=U/D0` gives the diagonal metric `|n_t|=|n_xi|=s/D0=b/d` and orthogonality. The alternative representations of the paired boundary points yield exactly

\[
(U_E)_t=(2-R_H)n_t,\quad (U_E)_\xi=R_E n_\xi,
\]

\[
(U_H)_t=-R_Hn_t,\quad (U_H)_\xi=-(2-R_E)n_\xi.
\]

The radii are nonnegative and satisfy `R_E+R_H=2-d<2`, so the area coefficients have the signs used. Subtracting four normal-image area units gives `-2(d+R_E R_H)`, with no sign loss.

**Local repair: parameter injectivity.** The source should explicitly connect this local Jacobian to image area. Strict convexity alone does not say an arbitrary parametrization is one-to-one. Here there is a short direct inverse. Put `n_k=n dot k`, `n_p=n dot p`, and `n_q=n dot q`; then

\[
\tanh\xi=-\frac{s n_q}{1+e n_k},\qquad
\cos t=\frac{s\cosh\xi\,n_p}{1+e n_k}.
\]

The denominator is positive because `1+e n_k>=1-e>0`. The first expression uniquely determines `xi`, and the second uniquely determines `t` on `[theta,pi-theta] subset (0,pi)`. Thus `n` is injective on the full parameter rectangle, including at `e=0`. This supplies an exact no-multiplicity proof without a new assumption. Insert after lines 398–402 and amend the corresponding sentence in note 03.

### 3. Elementary xi integration and fixed-domain reduction — PASS

Lines 439–509 use the correct half-angle substitution. With `C=e sin(t) in [0,1)`, the denominator becomes `(1-C)+(1+C)z^2`; integrating over `[-y,y]` gives

\[
I(C)=\frac4{\sqrt{1-C^2}}\arctan\left(y\sqrt{\frac{1+C}{1-C}}\right).
\]

Differentiation here treats `eta`, and hence `y`, as fixed while varying `C`. The identity

\[
\int\frac{v_0-\cosh\xi}{(\cosh\xi-C)^2}\,d\xi
=(v_0-C)I'(C)-I(C)
=\frac{(v_0 C-1)I(C)+2/b}{1-C^2}
\]

is correct. Symmetry supplies the factor two in the reduced formula. The substitution `x=b cos(t)` reverses the interval and gives `dt=-dx/(bA)`, so the displayed factor `-4b/A` is correct.

At `e=0`, `y=2-sqrt(3)=tan(pi/12)` and `L=arcsin(1/sqrt(3))=acos(1/3)/2`; all inverse-function branches used to obtain `Psi(0)` are correct.

### 4. Stable parameter and principal branch — PASS

The actual parameter is

\[
q=(1-e)/(1+e),
\]

not `e^2`. The Meissner endpoint is `q=1`; the parabolic endpoint is `q=0`. Lines 656–758 correctly substitute this parameter into the original formula.

In particular, `A-u0=q delta/D`, `v0 C-1=q M/((1+q)D^2)`, and `Aplus Aminus=(2q/K)T^2` produce the displayed coefficients `P1`, `P2`, and `Q0`. For `q>0`, the equation between the original angle argument and `Z` is an equality of positive quantities, not a conclusion merely from squaring. Therefore the same principal arctangent is used throughout the connected chart.

At `q=0` the original product is indeterminate term by term, but the stable `Z` is finite and strictly positive. The manuscript correctly continues the stable expression rather than substituting separately into the singular factors.

### 5. Analyticity on a neighborhood of the closed square — PASS

Lines 769–783 establish the uniform bounds

\[
D^2\ge K^2,\quad R^2\ge(K-1)^2>0,\quad T^2\ge2K^3>0,
\]

and positive lower bounds for every remaining denominator. Since the square is compact, these strict separations persist on an open neighborhood. The principal real square roots and real arctangent are analytic there. This justifies all derivatives used in the certificate, including at both endpoints and uniformly in `x`, and differentiation under the fixed integral. No radius of analytic continuation needs numerical certification.

At `q=0`, `R=D=K`, `T=K sqrt(A)`, `delta=1-x^2`, and `M=-K(A-1)`, where `A=2K+x^2`. Substitution reproduces lines 545–553 exactly.

### 6. Independently rederived endpoint derivative — PASS

The displayed `Phi'(0)` at lines 521–529 is not required by the proof, but its exact value was checked directly. Let `w=sqrt(3-x^2)` and `L=acos(1/3)/2`. First-order expansion of the original fixed integrand at `e=0` gives

\[
H_e(0,x)=\frac{4\pi}{\sqrt3}-12
+\frac{12\sqrt2-4\pi\sqrt6/3}{w}
+\frac{8\pi\sqrt6\,x^2}{9w^3}.
\]

Here `I_e=A0-sqrt(6)/3`, including the derivative of the moving `xi` endpoints; omitting that endpoint contribution would give an incorrect answer. The exact integrals

\[
\int_0^1\frac{dx}{w}=L,\qquad
\int_0^1\frac{x^2\,dx}{w^3}=1/\sqrt2-L
\]

yield the manuscript's expression after division by eight. Its positive sign also follows directly from differentiability, concavity, and the subsequently proved positive endpoint: `Phi'(0)>=Phi(1)>1/4000`. Thus no additional unsupported decimal positivity claim is needed.

### 7. Certificate-to-theorem analytic interface — PASS

Lines 574–584 use the exact derivatives

\[
q'=-(1+q)^2/2,\qquad q''=(1+q)^3/2.
\]

Consequently

\[
\Phi''(e)=\frac{(1+q)^3}{32}\int_0^1[(1+q)H_{qq}+2H_q]dx.
\]

The coefficient `1/32` includes the volume normalization `1/8`. The third derivative combination is correctly `C_q=(1+q)H_qqq+3H_qq`, as implemented at Arb source lines 468–469.

The centered midpoint enclosure is valid for every `C^2` integrand, with signed remainder in `h^3 f''([a,b])/24`. The mean-value enclosure should be read as an enclosure of the integrated scalar function `F(q)=integral C(q,x)dx`; the mean-value theorem applied to `F` gives `F(Q) subset F(qmid)+(Q-qmid)F'(Q)`. There is no requirement that a pointwise mean-value parameter be independent of `x`.

Arb source lines 330–396 implement the ordinary first, second, and third derivative chain rules consistently, and lines 399–489 use the needed `x`-second derivatives of those `q` derivatives. The analytic interface therefore supports the existing finite certificate. This review does not independently reevaluate Arb square roots or arctangents.

### 8. Chord, strict positivity, and equality quantifiers — PASS

Lines 593–618 need only continuity on `[0,1]`, concavity inside, `Phi(0)=0`, and `Phi(1)>1/4000`. These imply for every `0<e<1`

\[
\Phi(e)\ge e\Phi(1)>e/4000>0.
\]

The first inequality can be non-strict without weakening the conclusion. All three summands are nonnegative, and each positive parameter makes its summand strictly positive, so equality forces and is forced by the all-zero tuple. Mixed zero/nonzero tuples are included. Dilation gives the stated result for every positive width. No physical assertion about the excluded `e=1` body is needed to use the analytic endpoint in this chord proof.

### 9. Decimal display repair

Lines 555–559, 586–589, and 816–826 use ellipses in inequalities. The finite prefixes are outward-safe when interpreted as finite rationals, but an ellipsis is ambiguous about the omitted tail and can make a strict assertion at the exact enclosure endpoint. Use, for example, the exact finite displays

\[
\Phi(1)>0.000295140991676971>1/4000,
\]

\[
\sup\Phi''<-0.000017928617848306<-1/100000.
\]

Both displays are deliberately less sharp than the archived exact binary bounds. The nearest-rounded summaries at lines 830–844 should either be labeled approximate representations of enclosure endpoints, or be omitted in favor of the already directed-rounded generated comparison table. In particular `-0.000017928617848307` is inward as an upper bound if its finite digits are read literally.

## Conclusion

The one-pair formula, stable chart, endpoints, scalar certificate interface, and final positivity/equality deduction survive the bounded adversarial analytic review. The stated two local expository repairs make the argument's parameter multiplicity and decimal semantics explicit. No new mathematical search or stronger theorem constant is justified or required by this audit.
