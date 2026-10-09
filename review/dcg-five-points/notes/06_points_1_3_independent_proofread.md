# Independent proofread of DCG Reviewer Points 1 and 3

## Classification

```text
POINT_1_INTERNAL_PROOF_AUDIT_PASS
POINT_3_INTERNAL_PROOF_AUDIT_PASS
EXTERNAL_AUTHOR_REVIEW_RECOMMENDED
```

This was an adversarial rereading of the source construction, the explicit chart, the normal-sphere argument, and the full one-pair reduction. It found two substantive omissions and one branch-endpoint overstatement in the earlier draft. All three are repaired in the v2 notes and revised manuscript.

## Point 1 findings

### Finding 1.1 — Convex-confocal admissibility had not actually been checked

The earlier proof showed that the center curves were confocal and that the distance-plus-radii identity held. The source definition requires more: the principal-circle center of each device must be the bulb center of the other.

The revised proof identifies the centers and frame radii explicitly:

- elliptic principal center `ae k`, elliptic bulb center `a k`;
- hyperbolic principal center `a k`, hyperbolic bulb center `ae k`.

It also proves the ordering inequalities `u_0>e` and `ev_0<1`, which determine the principal circles under the source conventions. This closes the chart-to-source bridge for every `0<e<1`.

### Finding 1.2 — The regular tetrahedron should be proved, not inferred from coordinates

The revised proof observes that the two beam lengths are two and that all four cross distances equal two because both pea radii vanish at the beam endpoints. Thus all six pairwise distances among the four beam endpoints equal two.

### Finding 1.3 — The converse cap-cone inclusion needed a boundary-sphere identification

The opposite-support identity alone gives a boundary point on `S(A,2)`. The revised proof adds the source construction and strict-containment statement: wedge interiors lie strictly inside the vertex balls, and the other spherical-cap interiors meet `S(A,2)` only on seams. Hence `partial K intersect S(A,2)` is exactly the closed cap `C_A`.

### Finding 1.4 — The direct degenerate bookkeeping was incorrect

At `e=0`, the elliptic wedge surface collapses to a circular arc. Its physical area is zero, but its normal cone has positive spherical area. Therefore the earlier suggestion to retain it as a zero-area patch and repeat the generic normal bookkeeping was not correct.

The revised proof extends the generic identity by continuous degeneration/Hausdorff convergence. It explicitly retains the limiting normal region in `Psi(0)`.

## Point 3 findings

### Finding 3.1 — The fixed-to-stable substitution needed a complete table

The earlier draft jumped from `H(e,x)` to the final stable coefficients. The revised derivation now displays:

- `b`, `a`, `A`, `u_0`, `v_0`, `C`, and `y` in `q`-coordinates;
- the exact formula for `1-C^2`;
- the two removable-difference rationalizations;
- the separate derivations of `P_1`, `P_2`, and `Q_0`.

### Finding 3.2 — `Psi(0)` was stated rather than derived

The revised derivation proves

- `y=2-sqrt(3)=tan(pi/12)`;
- `I(0)=pi/3`;
- `pi/2-theta=(1/2)acos(1/3)`;

and obtains `Psi(0)` directly.

### Finding 3.3 — Branch equality at `q=0` was overstated

For `q>0`, the original and stable arctangent arguments are equal as positive quantities. At `q=0`, the original elliptic-hyperbolic product is a limiting indeterminate expression and should not be equated term-by-term.

The revised statement proves equality on `0<q<=1` and then uses the positive real-analytic stable expression to continue the same principal branch to `q=0`.

## Exact audit

The independent script `python/audit_points_1_3_identities.py` imports no Peabody certifier. It verifies exact zero remainders for:

- beam normalization;
- principal-focus distance formulas;
- center distance;
- the endpoint trigonometric identities;
- the complete stable substitution table;
- both removable-difference rationalizations;
- the angle-product identity;
- the stable arctangent argument after positive cross multiplication;
- the three stable coefficients `P_1`, `P_2`, and `Q_0`.

Its classification is:

```text
PEABODY_DCG_POINTS_1_3_EXACT_IDENTITY_AUDIT_PASS
```

## Remaining recommendation

No unresolved mathematical gap remains in Reviewer Points 1 or 3 after these corrections. Before DCG submission, send the geometry section and formula appendix to Arelio, Montejano, and Oliveros for an external source-convention check. That is now a proofreading safeguard, not an unfilled proof obligation.
