# Draft response to the follow-up review

We thank the reviewer for the careful second audit and for verifying the load-bearing geometric and algebraic identities independently.  We have adopted the substantive recommendations and made the interval-certificate provenance explicit.

## Why the restricted theorem is not automatic

We added a paragraph to the introduction explaining that the restricted result is proved independently, without assuming the still-open Bonnesen--Fenchel conjecture.  The fully tetrahedrally symmetric Robert endpoint is a natural competing shape, whereas the Meissner bodies break full tetrahedral symmetry.  A high-precision evaluation places the Robert endpoint only about 0.27% above the Meissner volume.  The exact disappearance of all mixed terms between the three opposite-edge deformations and the positivity of the one-pair scalar increment are therefore substantive parts of the theorem.

We did **not** adopt two qualitative statements from the review:

1. Robert's body is not a "second-smallest" member of the family, because nonzero parameters can approach zero and hence produce volumes arbitrarily close to the Meissner value.
2. Strict concavity and a positive initial derivative do not by themselves imply that `Phi` attains an interior maximum and decreases afterward.  The manuscript therefore makes no global monotonicity claim.

The revised wording retains the valid point: strict concavity alone would not prevent a negative parabolic endpoint, so the independent certification of `Phi(1)>0` is essential.

## Reconciliation of the reported interval bounds

The manuscript now uses Arb/FLINT as the sole proof authority and states only the conservative bounds

\[
\Phi(1)>\frac1{4000},
\qquad
\Phi''(e)<-\frac1{100000}<0.
\]

The decimal in the endpoint lemma has been changed to the Arb lower endpoint

\[
0.0002951409916769718\ldots,
\]

so it now agrees with the certificate described in the appendix.

At the same nominal 32-by-10 partition, the archived endpoint-interval implementations give

| implementation | lower bound for `Phi(1)` | weakest upper bound for `Phi''` |
|---|---:|---:|
| direct MPFR with explicit directed rounding | `0.000307652868249034...` | `-0.000041649190336146...` |
| legacy `mpmath.iv` | `0.000307652868249034...` | `-0.000041679824171374...` |
| Arb/FLINT balls | `0.000295140991676972...` | `-0.000017928617848307...` |

A slabwise audit shows that the direct-MPFR intervals contain the corresponding `mpmath.iv` intervals on all 32 slabs.  The endpoint enclosures agree to the displayed precision.  Accordingly, the revision does **not** claim that the older `mpmath.iv` calculation was shown false.  Instead, it states plainly that the Arb midpoint-radius evaluation is wider on the coarse partition and that only the conservative Arb result is used for publication.

The completed bounded refinement audit is archived with classification `PEABODY_ENCLOSURE_RECONCILIATION_PASS`. It ran Arb on 32-by-10, 64-by-20, and 128-by-20 partitions and evaluates the parabolic endpoint with 4, 8, and 16 panels.  The audit is designed to distinguish enclosure-width or wrapping effects from arithmetic precision without changing the formula, theorem, or proof target.

The former sentence that the enclosures merely "overlap" has been removed.

## Remaining source-level review

The cap--cone converse and the invocation of the source global assembly theorem remain deliberately tied to the cited Peabody construction.  External source-convention and formula proofreading remain recommended before submission. No completed external-review response or correspondence confirming delivery is archived in this checkpoint.  These are now citation-depth and expert-proofreading questions rather than omitted calculations.

## Scope

The theorem remains restricted to regular-tetrahedron confocal Peabodies.  We make no claim of global Meissner extremality, no universal lower-bound improvement, and no extension to arbitrary semi-regular tetrahedral bases.

## Closeout audit of the recorded revision

The closeout review of source checkpoint `ab320cf` independently checks the archived exact binary endpoints, all 96 authoritative concavity slabs, all 224 diagnostic refinement slabs, and the associated input hashes. It does not claim a fresh Arb replay or completed external human review. The revised table rounds lower bounds downward and upper bounds upward and states every partition explicitly. Historical initial-checkpoint manifests are preserved under their original scope; the current closeout has a separate manifest and validator.
