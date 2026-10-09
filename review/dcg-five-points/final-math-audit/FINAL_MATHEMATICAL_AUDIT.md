# Confocal Peabody: final internal mathematical audit

Date: 2026-10-09. Input checkpoint: **`b9fb7c5`**, committed by the author on
`review/dcg-major-revision` as *Audit Peabody reconciliation and correct submission
provenance*. The supplied terminal record confirms that local commit, not a push.
Only its abbreviated identifier is available here; no full identifier is invented.

## Verdict

**PEABODY_FINAL_INTERNAL_MATHEMATICAL_AUDIT_PASS**

The restricted-family theorem survives the bounded final internal audit. Four
independent AI-assisted review tracks examined source geometry, Gauss-sphere
bookkeeping, analytic formulas, and the certificate-to-theorem implication. A
coordinating review resolved the findings and independent re-review accepted the
revised geometric and analytic arguments. No unresolved theorem-level obstruction
was found. The finite corrections below are incorporated in the manuscript and
supporting notes.

This is an internal mathematical assessment, not formal proof verification or
completed external human review. The manuscript is internally ready to accompany
a focused external review request after the corrected checkpoint is integrated
and pushed. **Submission readiness remains false.**

In plain language: the audit checked why the calculation proves the stated
geometric result, not just whether its files agree. Several compressed steps
now have explicit arguments, and the supporting notes match the manuscript.
Neither the theorem nor its numerical proof targets changed.

## Authoritative record and baseline

The master handoff `confocal_peabody_master_handoff_2026-10-09.md` was read in full
during the preceding campaign-record review and remains authoritative for scope
and history. Subsequent user terminal evidence and the actual repository archive
resolved its then-pending reconciliation and integration status. The current
audit starts from the exact closeout payload installed and committed as `b9fb7c5`.

The supplied archive at `ab320cff615408af8ca8f35f54715e75932c1dd5` plus the previously
validated 23-file closeout overlay reproduces that reviewed payload. Before this
audit, the current validator passed all 150 payload-file records, all 365 archive
semantic checks, and all 50 protected original certificate files. Its saved output
is `input_closeout_validation.json`. The original input tree was preserved.

The current enclosure reconciliation remains
**PEABODY_ENCLOSURE_RECONCILIATION_PASS**. The canonical Arb source, its archived
outputs, the 324-box partition, and the two proof targets are unchanged:

$$
\Phi(1)>\frac1{4000},\qquad
\Phi''(e)<-\frac1{100000}\quad(0<e<1).
$$

No numerical search, partition refinement, shape optimization, or extension of
the source family was performed.

## Progress against the preceding committed checkpoint

| Item | `b9fb7c5` | Final audited source | Delta |
|---|---|---|---|
| Restricted theorem and equality cases | Existing claim | Same claim; analytic chain reviewed | Unchanged claim, stronger review |
| Source-family chart | Forward admissibility explicit | Converse normalized-branch argument added | Improved |
| Cap-cone converse | Terse strict-containment citation | Exhaustive support-point proof | Improved |
| Normal-chart area multiplicity | Implicit source embedding | Explicit inverse map | Improved |
| Mixed degenerations | Continuity stated tersely | Cap convergence and union-normal meaning explicit | Improved |
| Supporting seam/orientation notes | Some older wording remained | Notes synchronized with generic and singular cases | Corrected |
| Parameter mean-value argument | Ambiguous interval-integral notation | Scalar range with one fixed parameter | Clarified |
| Decimal proof displays | Ellipses beside bounds | Finite rational outward bounds | Improved |
| Archive semantics | 365 PASS | 365 PASS | Unchanged |
| Supplementary production-jet audit | None at this checkpoint | 285 exact identities and one rejected mutation | New corroboration |
| Current PDF | 14-page closeout preview | 15-page final internal-review PDF | Updated |
| External review / submission | Pending / false | Pending / false | Unchanged |

## Resolved findings

### 1. The chart covers the stated source devices

For a normalized source elliptic-hyperbolic pair, let `B=b^2`,
`s=sqrt(1-e^2)`, and `z=sqrt(B-1)>=0`. The width and equal-beam conditions give

$$
\sqrt{B+1}-e\sqrt{B-1}=2s,
\qquad z=\frac{2e\pm\sqrt2}{s}.
$$

The minus root is either negative or violates the source principal-center
condition `u_0>e`. The plus root is exactly the manuscript's `b^2` formula.
This closes the converse behind the broad source-family description. It adds
no parameters or bodies to the theorem.

### 2. Cap-cone duality has a direct proof

For `m` in the unit normal region at a tetrahedral vertex `A`, the opposite
support point is `x=A-2m`. A wedge-interior point has its opposite support in
the opposite wedge interior, so cannot be paired with `A`. Every nonvertex
seam borders a spherical cap; on `C_B` or its nonvertex boundary the unique
normal is `(x-B)/2`, which forces `B=A`. The remaining possible support points
are the other three tetrahedral vertices, already in `C_A`. These cases prove
the reverse cap-cone inclusion without the earlier strict-containment shorthand.

### 3. The normal chart has no multiplicity

With `s=sqrt(1-e^2)`, the normal components recover the parameters by

$$
\tanh\xi=-\frac{s n_q}{1+e n_k},\quad
D_0=\frac{s^2\cosh\xi}{1+e n_k},\quad
\cos t=\frac{n_pD_0}{s}.
$$

The denominator is positive and the two inverse functions are single-valued
on the parameter rectangle. This explicitly justifies integrating the spherical
Jacobian as image area, rather than inferring parameter injectivity from strict
convexity alone.

### 4. Generic seams and singular arcs are distinguished

For positive parameters, smooth seam-normal maps on a countable exhaustion by
compact subarcs have spherical area zero. The supporting notes no longer claim
that an entire nonvertex seam is compact. At a zero parameter, the collapsed
wedge has zero physical area but its **union of unit normal regions along the
arc** has positive spherical area; a single nonvertex point is not being assigned
a positive-area normal region.

Uniform convergence of the explicit wedges and seams is supplemented by cap
convergence: cap-cone duality makes the radial cap regions spherically convex,
and the diameter constraint puts them in a common open hemisphere. Gnomonic
projection reduces continuity of their spherical convex hulls to ordinary convex
hull continuity. The resulting Hausdorff limit justifies the mixed-zero area and
volume identities. Selected elliptic edges are also distinguished from their
complementary rounded edges; complementation swaps the star and face labels.

### 5. The certifier encloses a fixed-parameter integral

The appendix now defines `F(q)=integral C(q,x) dx` and writes

$$
F(Q_j)\subseteq F(q_j)+(Q_j-q_j)F'(Q_j).
$$

The range is formed after integration with a single fixed `q`. It is not an
interval integral allowing that parameter to change with `x`. The production
code already implements the correct meaning, so no certifier edit was needed.

### 6. Stated decimal bounds are exact finite rationals

All proof inequalities now use the conservative finite decimals
`0.000295140991676971` and `-0.000017928617848306`. The current validator checks
their outward direction and the theorem thresholds against the exact binary
endpoints of all three authoritative runs. The old comparison decimals are
explicitly approximate diagnostics. The separately generated enclosure table
retains its directed formatting and explicit resolutions.

## Complete implication checked

The audit follows this finite chain: source admissibility and assembly;
strict-convexity normal partition; cap-cone duality; antipodal wedge pairing;
exact additive area; Blaschke's identity and the width scaling factor `1/8`;
one-pair integration; the stable Möbius chart; principal-branch control;
analyticity near the closed parameter square; the exact second-derivative
identity; complete rational slab coverage and valid quadrature remainders;
the two scalar gates; the chord inequality; and the equality/orientation cases.

All three parameter coordinates and all eight orientation choices are covered.
The conclusion remains restricted to the stated regular-tetrahedron family.

## Execution and trust boundaries

- **Python archive audit:** 365 checks PASS, including exact reconstruction of
  all 96 authoritative concavity slab targets. No fresh special-function replay.
- **New exact derivative-rule corroboration:** 285 exact coefficient comparisons
  PASS and one intentional arctangent third-derivative sign mutation rejected.
  Production `D3`/`X2` definitions are extracted from the actual source via AST
  and compared with a separately implemented bivariate Taylor algebra over
  exact fractions. Arctangent constant values and interval arithmetic semantics
  are excluded. Three finite fixtures corroborate the analytic rule derivations;
  they do not prove universal correctness by sampling.
- **R companion:** supplied for the same 286 finite checks, using `gmp` and
  `jsonlite`. It independently transcribes the rules rather than extracting the
  Python AST. **UNEXECUTED here**; no cross-language runtime agreement is claimed.
- **Existing symbolic replay:** unavailable because SymPy is absent. The
  analytic identities were reviewed directly; no failed mathematical identity
  is being reported, and archived symbolic checks are not relabeled as reruns.
- **PDF:** compiled twice with the documented portable fonts; all 15 pages were
  visually reviewed, with no final-pass undefined-reference, overfull, or
  underfull warnings. The historical 14-page PDF is retained separately.
- **External review:** not completed. The four component reports are internal
  AI-assisted reviews, not four human referee reports.

The trusted interval authority remains the archived pinned Arb/FLINT run and
its actual elementary-function enclosure contract. The new checks neither
replace that dependency nor promote the refined diagnostic values.

## Files and replay

The current manuscript source is `../manuscript/main_dcg_closeout_review.tex`.
The current review attachment is **`main_dcg_final_math_review.pdf`** in this
directory. Earlier PDFs remain historical. The component reports below document
the original findings against `b9fb7c5`; their recommended repairs are resolved
above, and their original line references need not match the revised source:

- `geometry_review.md`
- `gauss_review.md`
- `analytic_review.md`
- `certificate_review.md`

From the repository root, the single current gate is:

```bash
python3 review/dcg-five-points/python/validate_current_closeout.py --repo-root .
```

It checks the current manifest, protected files, archive semantics, regenerated
table, derivative-rule corroboration, finite bounds, and internal-only status.
Its PASS does not mechanically certify the analytic proofs in this report.

Optional separate R replay:

```bash
Rscript review/dcg-five-points/R/verify_final_derivative_jets.R \
  --repo-root . --output /tmp/peabody_final_derivative_jets_R.json
```

## Finite remaining path

1. Integrate this bounded overlay on `review/dcg-major-revision`, validate, commit,
   and push. Recommended commit: **Complete the bounded Peabody mathematical audit**.
2. Attach the current 15-page PDF to the focused source-author review request;
   pin supporting-note links to the resulting commit after verifying access.
3. Obtain identifiable geometry/source-convention and formula feedback, resolve
   actual findings, then perform the final submission audit and freeze.

No email, Git commit, push, submission, or release was performed here. Other
MinVol workstreams and their forecasts are outside this audit.

Recommended next mode: **MEDIUM** for integration and review-request preparation;
**PRO** for substantive mathematical feedback and final claim/submission review.
