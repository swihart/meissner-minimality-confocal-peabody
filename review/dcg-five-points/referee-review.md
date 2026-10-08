What must be proved or supplied before acceptance
These are the gaps a referee would hold the paper on. None look fatal, but the first three are mandatory.

Convexity and constant width across the entire parameter range. Proposition 2.2's geometry rests on the ten patches forming a convex body of constant width, and on the Gauss images plus the four vertex cones tiling S2S^2
S2 exactly (measure-zero seams aside). The paper asserts this and leans on [1]. The author must show, or cite into [1] with precise statement, that this holds for every e∈[0,1)e\in[0,1)
e∈[0,1) and every σ\sigma
σ, not merely at special values — and that no two Gauss images overlap and together they cover. Equation (2.3) and the whole area bookkeeping collapse if the tiling fails anywhere in the range being integrated.
The trust boundary of the interval arithmetic — this is the acceptance pivot, especially at Math Comp. The proof authority is mpmath's iv context. The author must justify that every operation used — sqrt, arctan, and the arithmetic combining them — returns a guaranteed outward-rounded enclosure under mpmath 1.3.0, including at the directed-rounding level for the transcendental calls. The strongest fix is an independent rigorous recomputation in a more heavily vetted library (Arb/FLINT or INTLAB), or a formalized check (Lean/Coq) of at least the endpoint and the weakest concavity slab. The margins are correct but thin: certified Φ(1)>0.0003077\Phi(1)>0.0003077
Φ(1)>0.0003077 against the claimed 3/1043/10^4
3/104, and Φ′′<−0.00004168\Phi''<-0.00004168
Φ′′<−0.00004168 against −1/25000=−0.00004-1/25000=-0.00004
−1/25000=−0.00004. A referee will want headroom that doesn't depend on an unaudited transcendental enclosure.
The "direct calculation gives" steps in Section 3 and Appendix A. The derivations of (3.4)–(3.11), the reduction to the fixed interval (3.13), and especially the stable chart H(q,x)=(P1+P2)arctan⁡Z+Q0H(q,x)=(P_1+P_2)\arctan Z+Q_0
H(q,x)=(P1​+P2​)arctanZ+Q0​ in (A.1) are stated without worked steps. For a result whose correctness is entirely downstream of these formulas, the full derivation must appear — in the paper or in a supplement detailed enough for a referee to reproduce independently, not just replay. Relatedly, the branch control of arctan⁡Z\arctan Z
arctanZ needs an explicit argument that ZZ
Z stays in the range where the principal branch is the correct analytic continuation of the geometric angle across the whole (q,x)∈[0,1]2(q,x)\in[0,1]^2
(q,x)∈[0,1]2 domain; the paper states denominators are nonzero and radicals are positive-branch, but does not pin the arctan branch globally.
**Smoothness of the extension to the parabolic endpoint q=0q=0
q=0 (e→1e\to1
e→1).** Section 4 claims Φ\Phi
Φ extends smoothly to [0,1][0,1]
[0,1] via the stable chart, and the chord bound requires concavity on the closed interval. The author mentions "rationalization of the removable differences near q=0q=0
q=0"; that removal should be shown to be genuine (no residual singularity in HH
H or the derivatives entering the jet) rather than asserted, since the concavity certificate is evaluated on slabs abutting q=0q=0
q=0.
Minor, but worth tightening. The equality statement says the all-zero triple yields "the two classical Meissner bodies," yet there are eight σ\sigma
σ-choices at e=0e=0
e=0. A sentence showing those eight orientation configurations collapse to exactly the two Meissner congruence classes (round-a-vertex vs. round-a-face) would close the loop. And the normal-sphere partition in §2.2 is invoked "ignoring seams of spherical measure zero" — fine for area, but state it as a lemma with the measure-zero claim justified.

Bottom line

This is a solid, well-engineered result with a genuinely elegant
reduction and model reproducibility practices, and the arithmetic I
spot-checked is airtight. It is not a solution to Blaschke–Lebesgue
and does not claim to be. For acceptance it needs (i) the
convex/constant-width tiling made rigorous over the full parameter
range, (ii) an independent or more heavily vetted confirmation of the
interval certificate given the thin margins, and (iii) the Section 3 /
Appendix A derivations supplied in full with global branch
control. Items (i)–(iii) are the difference between "promising" and
"publishable." I'd recommend major revision, with a strong lean toward
eventual acceptance at DCG or Math Comp once the trust boundary is
nailed down.
