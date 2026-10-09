# Bounded final mathematical audit — Gauss sphere, degenerations, additivity

Disposition: this is the independent review of the pre-correction `b9fb7c5` manuscript. Its bounded recommendations are incorporated in the current source and resolved in `FINAL_MATHEMATICAL_AUDIT.md`. Original line references refer to that input checkpoint. This is an internal AI-assisted review, not an external human report.

Audit target: the b9fb7c5 closeout content represented by `closeout_work/repository/review/dcg-five-points/manuscript/main_dcg_closeout_review.tex` and supporting notes 01, 05, 06. This review re-read the analytic geometry and original source sections rather than accepting earlier PASS classifications. No numerical search or new interval certification was performed.

## Verdict

**GEOMETRIC_REDUCTION_SURVIVES_WITH_FINITE_PROOF_PRESENTATION_REPAIRS.** No counterexample or unfilled mathematical obstruction was found in the area/additivity argument. Before the final internal PASS is issued, replace the cap–cone converse with the direct support-point classification below, synchronize the seam argument in the supporting notes, and describe the collapsed arc's *union* of unit normal regions accurately. The mixed-parameter continuity argument is valid and can be strengthened with the compactness justification below.

## 1. Cap–cone converse: replace the fragile strict-containment citation

Location: manuscript lines 266–269; note01 §8, lines 275–303; note06 Finding 1.3.

The result is correct. The present proof cites the source Lemma 4.3 for strict containment of wedge interiors and then asserts `partial K intersect S(A,2)=C_A`. The source proof uses “interior” informally even for closed wedges that include the tetrahedral vertices, so this is an unnecessarily fragile place to rest the exact closed-set identification. A shorter direct argument uses source facts already needed elsewhere in the manuscript.

Precisely verified source facts (`project_sources/10-2021_peabodies.pdf`; extracted in `audit_temp/peabodies_source_final.txt`):

- §3.5 pp. 9–10, extracted lines 375–391: the paired maps `phi_1,phi_2` take the interior parameter rectangle to the two wedge interiors; boundary degeneracies occur at the endpoint parameters. The maps are smooth embeddings there.
- §3.5 pp. 9–10, extracted lines 392–405: each wedge boundary consists of two curves on spheres centered at the opposite beam endpoints. Each curve connects the endpoints of the wedge's own beam.
- Lemma 3.8, p. 10, extracted lines 411–417: the two paired wedge points are endpoints of a length-two binormal.
- §4 p. 10, extracted lines 433–441: `C_A` has boundary the three curves `Atilde_BC`, `Atilde_CD`, `Atilde_DB`. In particular, `B,C,D in C_A`.
- §4 p. 10, extracted lines 442–445: every nonvertex seam borders a spherical cap and has the common radial normal of that cap.
- Theorem 4.5 p. 13 identifies the assembled surface with a convex constant-width body and gives uniqueness of the tangent plane away from the four vertices.

### Ready replacement TeX for the converse

```tex
Conversely, let $m\in N_K(A)$ and put
$x=R_K(-m)=A-2m$. If $x$ lies in the interior of a wedge,
its paired point is in the opposite wedge interior, by the
parameterization in \cite[Section~3.5]{ArelioMontejanoOliveros2023}.
The length-two binormal pairing and \Cref{lem:opposite} identify
that paired point with $R_K(m)=A$, a contradiction.
If $x$ lies in a spherical-cap interior or on a nonvertex seam,
let $C_B$ be that cap, or the cap bordering that seam.
The source assembly gives its unique outer normal as $(x-B)/2$.
The opposite-support identity therefore gives $R_K(m)=B$, so $B=A$
and $x\in C_A$. Finally, if $x$ is a tetrahedral vertex, then
$x\ne A$ and $x\in\{B,C,D\}\subset C_A$, since these are the
three boundary vertices of $C_A$. This exhausts the boundary
partition and proves $-m\in\Omega_A$.
```

The same argument proves the asserted exact boundary-sphere identity if it is desired, but the identity need not be a separate hypothesis. For any `x in partial K intersect S(A,2)`, the diameter bound makes `(x-A)/2` a supporting normal at x and its opposite support point is A.

### Matching note prose

Define `Omega_A={(x-A)/2:x in C_A}` and `N_K(A)={n in S^2:R_K(n)=A}` explicitly. These definitions remain meaningful at cap vertices, where a single Gauss map is not defined. The forward inclusion follows first in the cap interior and then by closure. For the converse, classify `x=R_K(-m)` by the boundary partition: an interior wedge point has its opposite support point in the opposite wedge interior; a cap-interior or nonvertex seam point has its opposite support point at the center of the cap; and each of the three other tetrahedral vertices belongs to `C_A`. Thus only points of `C_A` can be opposite A.

## 2. Supporting seam notes are stale

The manuscript lines 245–247 correctly use a countable compact exhaustion. Note01 line 263 still asserts that “Each nonvertex seam is a compact piecewise-smooth curve”; deleting its endpoint vertices makes it noncompact. Note05 §2 also asserts a finite-union Gauss-image conclusion without establishing behavior at vertex endpoints. These do not alter the measure-zero result, but the supporting notes should match the corrected manuscript.

Replace with:

> Away from the vertices the explicit seam parameterizations and their common unit normals are smooth. Exhaust each nonvertex seam by countably many compact subarcs. On each subarc the physical curve and its normal image have two-dimensional measure zero. Countable subadditivity proves the same for the whole nonvertex seam; the finitely many vertices themselves have zero physical area. Their unit normal regions are accounted for separately and may have positive spherical area.

Also change note01 §5's reference “endpoint e=0 is treated in Section 9” to Section 10.

## 3. Degenerate-arc normal wording

Locations: manuscript line 297; note01 §10, line 354; note06 Finding 1.4.

The limiting statement should refer to the **union of unit normal regions along the arc**. At a fixed interior arc point (fixed t), varying xi gives a one-dimensional arc of unit normals. The positive spherical area comes from taking their union over the entire collapsed physical arc (varying t). It is inaccurate or at least seriously ambiguous to describe this as a single positive-area normal cone of the arc.

Suggested wording:

> At `e_i=0`, one wedge collapses to a circular singular arc. Its physical area is zero, while the union of its unit normal regions has positive spherical area and is the limit of `Gamma_i`. The generic additive identity must therefore be extended by continuity, retaining this limiting normal term.

This is consistent with the explicit maps: `R_E=0` gives `U_E=X(t)` independently of xi, whereas `n(t,xi)` retains dependence on both parameters.

Also prefer `Gamma_i=Gauss(W_i^{+,circ})` (or its closure) for generic parameters. `Gauss(W_i^+)` without an interior convention is formally undefined at the endpoint vertices. Closure changes no spherical area.

## 4. Mixed-zero continuity: a complete compactness bridge

Location: manuscript line 297; note01 §10.

The existing conclusion is valid. The text claims uniform convergence of explicit patch maps, but only wedge/seam maps are displayed. It is possible to make the cap part precise without constructing separate cap parameterizations:

1. Fix an orientation and a target tuple in `[0,1)^3`. Work in a compact parameter neighborhood whose coordinates are bounded above by some `rho<1`. Reparameterize the t and xi intervals onto `[0,1]`. After rigidly identifying the same tetrahedron, all center curves, radii, n, wedge maps and seam maps depend continuously on parameters, including e=0. In particular `d=a(cosh xi-e sin t)` stays uniformly positive near the fixed tuple. They converge uniformly.
2. For each generic tuple, cap–cone duality makes `Omega_A` a closed spherically convex set. It lies in a fixed open hemisphere. Indeed, with `v_B=(B-A)/2`, containment in the Reuleaux tetrahedron gives `n dot v_B >= 1/2` for all `n in Omega_A` and `B != A`. Thus a common hemisphere has a positive uniform margin.
3. In that hemisphere, `Omega_A` is the spherical convex hull of its three radial boundary arcs. Under gnomonic projection spherical hulls become ordinary convex hulls, and convex hull is continuous for compact sets in Hausdorff distance. The uniformly convergent seam maps therefore give Hausdorff convergence of each cap.
4. The union of the six wedges and four caps converges in Hausdorff distance. Taking its convex hull produces the unique limiting convex body. This agrees with the source circle-line construction (source §5.3) on every zero pair and preserves the other pairs.
5. Surface area and volume are continuous for convex-body Hausdorff convergence. The integral for Psi is continuous at e=0 by fixed-domain reparameterization and the same positive denominator bound. Therefore the generic additive formula passes to every mixed-zero tuple.

A concise paragraph covering steps 1–3 is sufficient. This is a fixed-parameter limit; no uniform control as e tends to 1 is required here.

## 5. Arithmetic and logical bookkeeping checked

- Constant width implies strict convexity, hence unique support points; the opposite-support relation follows from width=diameter and equality in Cauchy–Schwarz.
- Distinct open smooth patches cannot share support normals. Source seam smoothness plus compact exhaustion removes the seam Gauss images in spherical area.
- Closed-cap radial images differ from their interior images only by smooth boundary arcs and finitely many endpoint images, a spherical-null set.
- Generic wedge interiors pair antipodally. Their source parameterizations and positive pea radii ensure the paired point is interior and the Gauss map is injective through uniqueness of support points.
- The partition `4pi=2 sum |Omega_v|+2 sum |Gamma_i|` gives `sum|C_v|=8pi-4sum|Gamma_i|` exactly because the cap spheres have radius two.
- Adding wedge areas gives `S_2=8pi+sum Psi(e_i)`. Blaschke's identity at width two yields `V_2=16pi/3+sum Psi(e_i)`; scaling by 1/2 multiplies volume by 1/8. Thus `Phi(e)=(Psi(e)-Psi(0))/8` gives the stated additive volume identity.
- Device exchange swaps the two wedge physical areas and antipodally swaps their normal regions, so Psi is orientation independent.
- The eight edge choices split into four vertex stars and four face cycles. The tetrahedral action gives two orbits, and the cited classical noncongruence result is needed to identify them as two full Euclidean congruence classes; the manuscript now supplies that citation.
- No modification of the scalar gates, certificate targets, or theorem quantifiers is warranted by this audit.

## Remaining status

This is an internal adversarial proof review. It is not external source-author review and does not record new correspondence or submission readiness. The recommended fixes remove ambiguity and synchronize the supporting record; they do not extend the family or reopen any numerical campaign.
