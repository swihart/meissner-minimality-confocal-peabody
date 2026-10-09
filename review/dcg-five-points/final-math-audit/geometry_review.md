# Final internal geometry audit — 2026-10-09

Disposition: this is the independent review of the pre-correction `b9fb7c5` manuscript. Its bounded recommendations are incorporated in the current source and resolved in `FINAL_MATHEMATICAL_AUDIT.md`. Original line references refer to that input checkpoint. This is an internal AI-assisted review, not an external human report.

Target: the 896-line `main_dcg_closeout_review.tex` supplied in the closeout tree, corresponding to the user's committed checkpoint `b9fb7c5`. Line numbers below refer to that pre-audit file. This is a fresh adversarial mathematical reading, not a reuse of the previous PASS label.

## Scope and source reading

Read the complete geometry portion of the current manuscript, the paired-surface calculation needed to check normals and degenerations, and notes 01, 05, and 06 completely. Read the attached Arelio–Montejano–Oliveros source, particularly §§3.1–3.5, all of §4, and §5.3; these are PDF pp. 5–15. Checked the attached Kawohl–Weber text on noncongruence and rounded-edge identification (PDF pp. 2, 6–7). No numerical search, certificate enlargement, or family extension was performed.

## Verdict

**No geometric counterexample or unrepaired mathematical obstruction was found for the stated K(e,sigma) theorem.** Source-family admissibility, independent opposite-edge choices, mixed circle-line degeneration, and the two equality classes survive this audit.

There are two worthwhile analytic strengthening corrections before freezing the reviewed manuscript: (1) provide the short converse proving that the chart exhausts the elliptic–hyperbolic regular-tetrahedron construction; (2) replace the terse cap-cone strict-containment citation by the direct normal argument below. Both can be fully proved without changing any certificate or numerical target. Supporting notes retain several old formulations already corrected in the manuscript and should be synchronized.

## Findings and exact resolutions

### G1 — Local pea-pod membership: ESTABLISHED

Manuscript lines 107–208 correctly satisfy source Definitions 3.1, 3.2, and 3.5. The source elliptic device is a Steiner chain internally tangent to the principal circle and externally tangent to the secondary circle; the hyperbolic device is internally tangent to both circles.

The text's principal-circle formulas are correct. For completeness the omitted secondary-circle identities are:

- Elliptic secondary center `-ae k`, radius `a(1+e u0)`, and distance `a(1+e sin t)`. Its center distance minus its radius is `ae(sin t-u0)=R_E`, while the principal radius minus center distance is the same `R_E`.
- Hyperbolic secondary center `-a k`, radius `a(v0+e)`, and distance `a(cosh xi+e)`. Its radius minus center distance is `a(v0-cosh xi)=R_H`, identical to the principal-circle expression.

Both radii are strictly positive in the open center-curve arcs and vanish at beam endpoints. The ordering inequalities `u0>e` and `e v0<1` are exact and identify the principal circles correctly. Their centers are exactly the opposite bulb centers. All six beam-endpoint distances equal two by the displayed center-distance identity. No hidden cross-pair condition is introduced by these calculations.

Severity: no error; optional explicit secondary-circle line improves the source-definition bridge.

### G2 — Chart exhaustion: ESTABLISHED BY THE FOLLOWING ADDITION

Current manuscript lines 149–210 prove that every displayed chart is admissible; the introductory phrase “all regular-tetrahedron confocal Peabodies” is stronger unless chart exhaustion is made explicit. The quantified theorem about the defined `K(e,sigma)` is already unaffected, but the converse can be proved exactly.

Take any elliptic–hyperbolic convex-confocal device pair of the source with both beams of length two. After rigid motion and possibly reversing the common axis, let the elliptic principal center be `+ae k` and bulb be `+a k`. The opposite bulb/principal-center conditions then put the hyperbolic pea string on its positive branch, with bulb `+ae k` and principal center `+a k`. Orthogonal center planes and the common axis give precisely the X,Y parameterizations. The half-beam lengths one force `b cos theta=b sinh eta=1`, so `B=b²>1`, `u0=sqrt(B-1)/sqrt(B)`, `v0=sqrt(B+1)/sqrt(B)`, and `a=sqrt(B)/s`, where `s=sqrt(1-e²)`.

The elliptic frame convention forces `u0>e`, since its beam midpoint is beyond its nearer focus `+ae k`. The regular cross-distances two imply

`sqrt(B+1)-e sqrt(B-1)=2s`.

With `t=sqrt(B-1)>=0`, squaring gives

`s² t²-4 e s t+2-4s²=0`, hence `t=(2e ± sqrt(2))/s`.

The minus root is negative if `e<1/sqrt(2)`. If `e>=1/sqrt(2)`, it would give

`u0²-e² = (2+3e²-4sqrt(2)e)/B = ((sqrt(2)-e)(sqrt(2)-3e))/B < 0`,

contradicting the source elliptic-frame ordering. The plus root alone survives and yields exactly

`B=(3+3e²+4sqrt(2)e)/(1-e²)`.

The value `e=0` is the source §5.3 circle-line degeneration. This argument addresses only the existing regular-tetrahedron elliptic–hyperbolic family and its Meissner endpoint; it makes no extension of scope.

Severity: modest scope-justification omission in broad prose; exact minimal repair available above.

### G3 — Independent choices and eight orientations: ESTABLISHED

The source §4 (PDF p.10) explicitly chooses a confocal device pair for each other pair of opposite edges, without equating parameters. Source Theorem 4.5 (PDF p.13) proves the resulting assembled surface is a constant-width body. Thus manuscript line 210 uses the theorem with its actual hypotheses.

Swapping the devices is realized by an isometry exchanging the two opposite beams of the same regular tetrahedron. It preserves convex-confocality. The source independence permits this on each pair. Although the resulting global bodies need not be congruent, each individual pair contribution is unchanged by device exchange.

### G4 — Cap-cone converse: ESTABLISHED, RECOMMENDED DIRECT REPLACEMENT

Manuscript line 269 cites the “strict-containment argument” of source Lemma 4.3. The source's literal prose says entire wedge surfaces are inside the interiors of vertex balls even though some of their boundaries are on those spheres. Interpreting that as strict containment of wedge interiors is consistent with the construction, but the mathematical inference can be proved more transparently from already established facts, without relying on this imprecision.

Fix a tetrahedral vertex A. Since K has diameter two and contains A, `K⊂B(A,2)`. At any smooth `x∈∂K∩S(A,2)`, the radial vector `n=(x-A)/2` supports K. The opposite-support identity gives `R_K(-n)=A`.

If x is in a wedge interior, source Lemma 3.8 pairs it with a point of the opposite wedge interior on its length-two binormal. Both center parameters are interior and both pea radii positive. This point is the unique opposite support point and cannot be a tetrahedral vertex. Contradiction.

If x belongs to another cap `C_B`, or to a nonvertex seam bordering `C_B`, its unique normal is `(x-B)/2`. Equality with `(x-A)/2` forces `A=B`. Every nonvertex seam in source §4 borders one cap and one wedge, so this covers all seams. Finally, the only possible vertices on `S(A,2)` are the other three tetrahedral vertices, already contained in `C_A`.

Consequently `∂K∩S(A,2)=C_A` exactly. The forward cap-cone inclusion extends from cap interior to closure by closedness of the unit normal region. This proves `N_K(A)=-Omega_A` with `Omega_A={(x-A)/2:x∈C_A}` and no appeal to a strict-containment statement.

Severity: a compressed source-dependent argument, not a false theorem. The replacement is a complete finite analytic repair.

### G5 — Normal partition and additivity: ESTABLISHED FOR GENERIC PARAMETERS

Strict convexity of constant-width bodies gives unique support points. Coverage and disjointness follow from the source finite patch decomposition. Nonvertex seam normals are smooth on each compact subarc; countable exhaustion proves their spherical measure zero without the false assertion that a seam minus its vertices is compact. The corrected manuscript line 247 already uses the right argument.

The opposite wedges have antipodal normals by their source binormal pairing. Cap-cone duality gives the factor two on the caps. Radius-two caps have physical area four times spherical normal-image area. These yield `4pi=2 sum|Omega|+2 sum|Gamma|`, hence the displayed additive area formula. This chain does not assume the scalar result or numerical certificate.

### G6 — Mixed zero parameters: ESTABLISHED, WORDING PRECISELY INTERPRETED

At `e=0`, `a=b=sqrt(3)`, `R_E=0`, and the elliptic wedge collapses to the source's circular edge. The hyperbolic center curve becomes the straight beam and its wedge becomes the classical rounded surface. The source §5.3 explicitly identifies this surgery.

The surviving unit-normal region is the **union** of normal directions along the circular edge, not a positive-area spherical cone at each single edge point. In the explicit limiting chart,

`n(t,xi)=(sin(t)/cosh(xi), cos(t)/cosh(xi), -tanh(xi))`

in the `(k,p,q)` frame, and its spherical Jacobian is `1/cosh²(xi)>0`. Thus the two-parameter union has positive spherical area although the physical edge has zero surface area. At a fixed t the normal set is only an arc. Recommend phrasing “the union of its unit-normal cones” rather than a single cone of the whole edge.

For any fixed mixed tuple, reparameterize each center rectangle by an affine map from a fixed square. Near its zero coordinates all coefficients are continuous and `d=a(cosh(xi)-e sin(t))` remains uniformly positive; thus the explicit paired wedge maps converge uniformly. The assembled spherical-cap boundaries converge along their analytic seams, with the same prescribed cap side. The source circle-line limit consequently gives Hausdorff convergence of the convex bodies. Continuity of intrinsic volumes and of the scalar integral proves the generic additive identity at mixed zero tuples. No direct seam-nullity assertion is needed or valid for the newly singular circular edges.

Severity: no obstruction; improve union-of-normals wording and explicitly restrict supporting-note seam statements to positive parameters.

### G7 — Equality orientation classes: ESTABLISHED

There are exactly eight selections of one edge from each of the three opposite pairs: four vertex stars and four triangular face boundaries. Tetrahedral symmetries give transitivity within each class. Kawohl–Weber explicitly identifies the two rounded-edge patterns and their noncongruence (attached PDF pp.2,6–7), so this is more than a statement about abstract graph orbits.

The manuscript introduction says sigma selects the **elliptic** device, which at `e=0` retains a circular edge. The rounded edges are the complementary **hyperbolic** selections. Complementation swaps stars and faces; it does not create or merge congruence classes. Supporting note05 should make this convention explicit to avoid reversing the names of individual orientation patterns.

Severity: convention clarification only; equality theorem unchanged.

## Supporting-note synchronization required

1. note01 line263: replace “Each nonvertex seam is a compact piecewise-smooth curve” by the manuscript's countable compact-subarc exhaustion.
2. note01 line275: define Omega radially and N as unit normals, matching manuscript; explicitly extend the forward inclusion by closure.
3. note01 lines287–303: use the direct cap-cone proof above if inserted into the manuscript.
4. note01 line354: say the union of unit normal cones along the singular edge has positive spherical area; avoid suggesting each edge point has such area.
5. note05 lines56–68: explicitly restrict the seam/Gauss-nullity argument to `e_i>0`; refer mixed zero cases to continuity.
6. note05 lines49–54: distinguish the retained elliptic-edge selection from the complementary rounded-edge selection.
7. note06 Finding1.3 and note01 final recommendation: supersede the older reliance on source Lemma4.3 strict-containment wording with the explicit normal proof, preserving the historical finding if desired.

## Acceptance scope

After these bounded explanatory/synchronization corrections, this geometry component is internally ready for focused external author review. It is not evidence of completed external review. The audit does not promote submission readiness, alter the restricted-family theorem, or establish global Meissner minimality.
