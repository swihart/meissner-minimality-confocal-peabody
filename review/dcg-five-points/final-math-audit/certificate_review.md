# Bounded final mathematical audit: certificate-to-theorem chain

Disposition: this is the independent review of the pre-correction `b9fb7c5` manuscript. Its bounded recommendations are incorporated in the current source and resolved in `FINAL_MATHEMATICAL_AUDIT.md`. Original line references refer to that input checkpoint. This is an internal AI-assisted review, not an external human report.

Date: 2026-10-09. Input: the corrected closeout tree subsequently committed by
the author as `b9fb7c5` on `review/dcg-major-revision`.

## Verdict

**PASS for the certificate-to-theorem chain, with one recommended notation
clarification.** No certificate-critical formula mismatch, missing parameter
region, incorrect automatic-differentiation rule, reversed rational gate, or
invalid inference from the two scalar gates was found. This is an internal
adversarial audit; it does not mark external proofreading or submission complete.

The numerical search and subdivision architecture stayed frozen. No new Arb,
MPFR, mpmath, or R certificate was evaluated. The existing 365-check archive audit
was inspected as a downstream arithmetic audit, not assumed to prove equivalence
of the mathematical integrand and the certifier.

## Inputs and scope

The audit read the current manuscript from the additive scalar definition
through its two appendices, the full production Arb certifier, the archive
verifier, the original Arb output auditor, the replay driver, and the stable
formula/endpoint proof notes. Principal paths relative to the repository are:

- `review/dcg-five-points/manuscript/main_dcg_closeout_review.tex`
- `review/dcg-five-points/arb/peabody_arb_concavity.py`
- `review/dcg-five-points/python/verify_archived_reconciliation.py`
- `review/dcg-five-points/python/audit_arb_certificate.py`
- `review/dcg-five-points/python/format_reconciliation_table.py`
- `review/dcg-five-points/notes/02_arb_flint_trust_boundary.md`
- `review/dcg-five-points/notes/04_parabolic_endpoint_analyticity.md`
- `review/dcg-five-points/scripts/run_arb_no_brew_replay.sh`

The geometric validity of the source family and the derivation of the original
surface integrand are separate review tasks. This review starts from the
manuscript's explicit stable integrand, checks its implementation, and checks the
entire computational implication back to the scalar theorem. It also checks
the parameter substitution and width-normalization factor.

## 1. Exact normalization and parameter endpoints

At native width two, the area/volume reduction gives

`Phi(e) = (Psi(e) - Psi(0))/8`.

The factor `1/8` is the three-dimensional scale change from width two to width
one, not an extra quadrature or orientation multiplicity. In the stable chart

`q = (1-e)/(1+e)`, `e = (1-q)/(1+q)`,

the Meissner endpoint `e=0` is `q=1`, and the parabolic extension `e=1` is
`q=0`. The certifier docstring correctly uses `Psi(1)` for the reparameterized
Meissner baseline, while `setup` stores its value under the historical variable
name `psi0`:

`-(2*pi/sqrt(3))*acos(1/3)`.

`endpoint_phi` evaluates `H` at `q=0`, subtracts this baseline, and divides by
eight. The function's variable `psi_one` names the physical `e=1` endpoint,
not the stable `q=1` endpoint. No endpoint reversal or normalization mismatch
was found.

Differentiating the rational substitution gives

`q_e = -(1+q)^2/2`, `q_ee = (1+q)^3/2`.

Thus the `1/8` normalization gives exactly

`Phi_ee = (1+q)^3/32 * integral((1+q)*H_qq + 2*H_q, x=0..1)`.

The production `concavity_slab` has precisely this positive prefactor.

## 2. Stable expression and analyticity

The assignments in `h_jet` reproduce the manuscript's `D`, `R`, `T`, `delta`,
`M`, `P1`, `P2`, `Q0`, and `Z` exactly. With default `correction_sign=1`, the
return value is `(P1+P2)*atan(Z)+Q0`. Constants are computed inside Arb; no
decimal approximation or Python binary float enters the analytic expression.

The manual domain argument is sufficient and is stronger than finite positive
diagnostics alone. On the full closed square, `K=(1+sqrt(2))^2>1` and

- `D^2 >= K^2`;
- `R^2 >= (K-q)^2 >= (K-1)^2`;
- `T^2 >= 2*K^3`;
- `R+K-q >= 2*(K-1)`;
- `R+K > 0` and `K+q+D > 0`.

Consequently the square roots and denominators stay away from their singular
sets on an open neighborhood of the compact square. The positive principal
arctangent argument has a continuous analytic extension at `q=0`. Hence the
needed mixed derivatives, including `H_qqqxx`, are continuous and bounded on
the square, and differentiation under the fixed `x` integral is justified.
The slabs touching `q=0` and `q=1` require no omitted limiting computation.

## 3. Automatic-differentiation rules

`D3` stores ordinary derivatives, not Taylor coefficients. Its product rule
uses binomial coefficients `1,3,3,1` at order three; the reciprocal rule is

`(1/f)''' = -6*f'^3/f^4 + 6*f'*f''/f^3 - f'''/f^2`.

The square-root and arctangent third derivatives match direct differentiation:

`(sqrt(f))''' = f'''/(2*sqrt(f)) - 3*f'*f''/(4*f^(3/2)) + 3*f'^3/(8*f^(5/2))`,

`(atan(f))''' = f'''/(1+f^2) - 6*f*f'*f''/(1+f^2)^2 + (6*f^2-2)*f'^3/(1+f^2)^3`.

The `X2` operations apply the ordinary second-derivative chain rules with `D3`
coefficients. These coefficients form the required derivative algebra, so the
nested composition yields every mixed derivative through q order three and x
order two. The positive-radicand/domain argument above supplies the hypotheses
for the smooth scalar chain rules. Interval dependency may enlarge enclosures
but cannot invalidate them under Arb's operation contracts.

A new bounded **Python-only exact finite corroboration** executed the actual
production definitions, extracted by AST without importing `flint`. It compared
three exact rational mixed-jet assignments against an independently implemented
bivariate Taylor algebra using coefficient convolution, reciprocal geometric
series, binomial square-root coefficients, and the recurrence obtained from
`d atan(a+z)/dz = 1/(1+(a+z)^2)`.

The result was **285 exact coefficient identities PASS**, plus **one deliberately
wrong arctangent third-derivative sign rejected**, for **286 checks PASS**.
The arctangent constant term was intentionally excluded; the test concerns
derivatives and does not numerically evaluate a transcendental function.
Finite tests corroborate the manually derived rules and do not substitute for
their universal chain-rule argument or for rigorous interval semantics.

Supplementary audit artifacts:

- `../python/verify_final_derivative_jets.py`
- `derivative_jet_audit.json`
- `../R/verify_final_derivative_jets.R`

The JSON records the SHA-256 of the exact production source inspected. Both
scripts accept `--repo-root` and `--output`. The matching R script uses `gmp`
exact rational arithmetic and `jsonlite`, with the same three fixtures and
285-identity-plus-one-control count. Its derivative rules are independently
transcribed rather than extracted from the Python AST. **R runtime status:
UNEXECUTED**, since `Rscript` is unavailable. No Python/R runtime agreement is
claimed. The previously prepared paired R archive auditor remains a separate,
unchanged artifact.

## 4. Quadrature and full parameter coverage

For each fixed parameter, the centered Taylor remainder can be written with a
nonnegative kernel. Its integral has total mass `h^3/24`, proving

`integral_a^b f = h*f(m) + (h^3/24)*r`, with `r in range(f'', [a,b])`.

This validates the signed interval remainder used by `midpoint_integral`; an
absolute error bound is not required. A midpoint represented by a rational
enclosure also remains valid, since it contains the exact midpoint.

Writing `C=(1+q)*H_qq+2*H_q` gives

`C_q=(1+q)*H_qqq+3*H_qq`.

The code uses this coefficient `3` in both the midpoint and second-x-derivative
callbacks. There is no missing derivative of the factor `1+q`.

For `F(q)=integral C(q,x) dx`, the code implements the mean-value enclosure

`F(Q) subset F(q_mid) + (Q-q_mid)*F'(Q)`.

Uniform derivative enclosure on each slab justifies this expression. Interval
multiplication by `(1+Q)^3/32` then contains every `Phi_ee` value for that slab.
No monotonicity of `Phi_ee` or independence of the two factors is assumed.

The canonical loops cover exactly `Q_j=[j/32,(j+1)/32]`, j=0,...,31, and ten
panels `[k/10,(k+1)/10]`. Adjacent slabs share endpoints. The four endpoint
panels cover the full `x` interval. The exact Fraction archive verifier checks
these domains in all three authoritative runs. The reported 324 rectangles
count 320 parameter/integration rectangles plus four endpoint panels; each
rectangle has several AD evaluations and is not being described as one scalar
evaluation.

## 5. Rational gates and proof conclusion

`rational` constructs exact-rational inputs through `fmpq`; interval endpoints
are rational strings from exact `Fraction` values. The acceptance functions
compare the computed lower endpoint to the upper endpoint of `1/4000`, and
the computed upper endpoint to the lower endpoint of `-1/100000`. Both strict
comparisons are conservative in the correct direction.

In particular, the concavity comparison uses `-rational(1/100000)` rather than
a binary64 literal `-0.00001`. If any ball is nonfinite or too wide to decide
the sign, the strict predicate cannot establish the gate.

With continuity on `[0,1]`, `Phi(0)=0`, the certified positive `Phi(1)`, and
strict concavity on the interior, the graph lies above its endpoint chord.
Even the weak chord inequality used in the manuscript suffices because
`Phi(1)>1/4000`: for every `0<e<1`, `Phi(e)>e/4000>0`.
Exact additivity then implies equality precisely when every parameter is zero.
No finite sampling is being used to extrapolate a positivity statement.

## 6. Serialization, archive semantics, and controls

Python-FLINT's documented `lower()` and `upper()` return exact finite binary
points directed outward at the working precision. `man_exp()` records each
such point as an exact integer mantissa and power of two. Authoritative
terminal fields reject nonfinite or nonexact endpoints during serialization.
The theorem-critical downstream checks use these exact binary records.

The human-readable `.str(..., radius=False)` outputs are not generally directed
decimal endpoints. The current archive verifier correctly treats decimal
comparisons as diagnostic displays and uses exact binary fractions for
publication gates and the 96 reconstructed concavity upper bounds. The table
formatter rounds lower displays down and upper displays up relative to the
archived decimal displays. It expressly does not create new authoritative
certificates from those displays.

The archive verifier reconstructs the concavity integrals and slab products
from the stored terminal contribution intervals. It trusts those stored terms
as outputs of the original Arb derivative computations. Its endpoint gate uses
the stored final exact binary endpoint; it does not independently reevaluate
the transcendental baseline. These limits are correctly stated in its own
trust-boundary field. Hashes identify the trusted inputs, but are not proofs
of their analytic meaning.

The frozen under-resolved partition and correction-sector sign mutation must
produce semantic NO-GO JSON, not merely crash. The replay script explicitly
checks this, and the archive verifier checks both expected exit code and
semantic rejection. These controls are useful fault tests; they are not a
complete correctness proof. Forward/reverse and precision agreement likewise
supports reproducibility without independently proving every analytic identity.

Trusted components remain the Python interpreter and exact-integer/rational
operations; the Python-FLINT binding and its pinned binary distribution;
FLINT/Arb arithmetic and elementary-function contracts; the inspected derivative
and quadrature implementation; and the authentic archived terminal outputs.
No fresh Arb reevaluation occurred during this final audit.

## 7. Recommended manuscript clarification

In the Arb appendix, the display currently uses `integral C(Q_j,x) dx` on the
left of the mean-value inclusion. Read as an Aumann/interval-valued integral,
this could allow q to vary with x and is not the set the code proves to be
enclosed. The intended fixed-parameter range is correct.

Recommended replacement: define `F(q)=integral_0^1 C(q,x) dx` and state

`F(Q_j) subset F(q_j)+(Q_j-q_j)*F'(Q_j)`,

where `F(Q_j)={F(q):q in Q_j}` and `F'(Q_j)` is enclosed by integrating the
uniform-in-q derivative bounds. Say explicitly that q is held fixed during
each x integration. This repairs a notation ambiguity; it does not alter the
code, numerical outputs, rational bounds, or theorem.

No further certificate-code repair is required by this audit.

## Documentation checked

Official Python-FLINT 0.9.0 documentation was consulted for the numerical trust
contract; this was not a search for new mathematical results:

- <https://python-flint.readthedocs.io/en/stable/arb.html>
  (rational-string construction, radius rounding, exact directed endpoints,
  `man_exp`, and nondirected human-readable decimal output).
- <https://python-flint.readthedocs.io/en/latest/general.html>
  (rigorous ball-operation bounds and conservative comparison predicates).

The coordinating review also consulted these official documentation pages.

## Repository effect

This sub-audit made no changes to the repository, certificate data, manifest,
or manuscript. Its report and supplementary exact test are scratch artifacts
for the coordinating final audit. The coordinator may include them in the
bounded audit package and apply the one wording correction above.
