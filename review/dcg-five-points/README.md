# Confocal Peabody DCG major revision

**Current repository:** `swihart/meissner-minimality-confocal-peabody`
**Current branch:** `review/dcg-major-revision`
**Audited input checkpoint:** `ab320cf`
**Protected public baseline:** `v1.0.0` (`1485d7e`)

This directory contains the bounded revision of the restricted-family theorem: the classical Meissner degenerations minimize volume among width-one regular-tetrahedron confocal Peabodies. The revision does not establish global Meissner extremality or a universal lower-bound improvement. The regular Peabody search and semi-regular extensions remain closed.

## Current manuscript

The source checkpoint contains the following reconciled source/PDF pair, retained unchanged:

- `manuscript/main_dcg_revision_enclosure_reconciled.tex`
- `manuscript/main_dcg_revision_enclosure_reconciled.pdf`
- `manuscript/generated_enclosure_reconciliation.tex` (required local input)

The `main_dcg_revision_checkpoint` and `main_dcg_revision_points_1_3_closed` files are earlier drafts. `manuscript/current/` at the repository root is the public-release manuscript, not this revision.

The corrected closeout source is `manuscript/main_dcg_closeout_review.tex`, with required input `manuscript/generated_enclosure_reconciliation_closeout.tex`. Its build and preview-font details are in `manuscript/README.md`. The current gate is `python3 review/dcg-five-points/python/validate_current_closeout.py --repo-root .` from the repository root. See `closeout/CLOSEOUT_REPORT.md` for its exact scope and remaining submission gates.

## Exact reviewer status

| Point | Status in the recorded checkpoint | Remaining work |
|---|---|---|
| 1: Full-parameter geometry and Gauss partition | Closed internally; corrected construction and cap-cone arguments supplied | External source-convention or convex-geometer proofreading remains recommended |
| 2: Rigorous-arithmetic provenance | Closed by the archived Arb/FLINT replay and completed enclosure reconciliation | Final editorial consistency audit |
| 3: Formula derivation and branch control | Closed internally; complete derivations and exact identity audits supplied | External line-by-line proofreading remains recommended |
| 4: Parabolic endpoint regularity | Closed analytically | Final editorial review |
| 5: Orientation classes, equality, and seam nullity | Closed analytically | Final editorial review |

See `REVIEW_PROGRESS_LEDGER.md` and `data/reviewer_point_progress.json`. The package contains internal proofreading notes and a draft referee response. It does not contain an identifiable external reviewer response or confirmation from the source authors. A statement in a draft response about correspondence is not evidence that the external review was completed.

This remains a review package; final submission approval has not been recorded.

## Proof authority and completed reconciliation

The revised manuscript uses the independently implemented Arb/FLINT certifier and the conservative scalar bounds

$$
\Phi(1)>\frac1{4000},\qquad
\Phi''(e)<-\frac1{100000}\quad(0<e<1).
$$

The archived authoritative replay comprises 384-bit and 512-bit forward runs, a 384-bit reverse run, exact-rational partition coverage, and rejected under-resolution and sign-mutation controls. Its data are under `results/arb/`. `ARB_NO_BREW_REPLAY.md` documents the supported replay and trust boundary.

The bounded reconciliation is complete in `results/enclosure-reconciliation/enclosure_reconciliation.json`, with classification `PEABODY_ENCLOSURE_RECONCILIATION_PASS`. It records the 32-by-10, 64-by-20, and 128-by-20 Arb comparison and 4-, 8-, and 16-panel endpoint calculations. At the frozen 32-by-10 partition, all 32 direct-MPFR intervals contain their legacy `mpmath.iv` counterparts. Arb's coarse enclosures are wider, and the bounded refinements tighten them. This did not show the older calculation false and does not change the published conservative targets.

Direct-MPFR runtime-only preflight data, legacy `mpmath.iv`, Mathematica, and R are supporting audits. An official-header MPFR run is not an outstanding prerequisite for the Arb-based manuscript. `LOCAL_REPLAY.md`, the original MPFR trust note, and the MPFR preflight README describe the superseded initial promotion route.

## Historical manifest scope

`CHECKPOINT_MANIFEST.json`, `SHA256SUMS.txt`, and `python/validate_checkpoint_package.py` describe the initial 51-file checkpoint, before the Arb promotion, proof corrections, and reconciliation. They are preserved as history, not a checksum claim for this expanded directory. In particular, the old validator requires Point 2 to remain open, so its failure on the current closed review state is expected and must not be presented as a theorem failure.

The immutable root theorem package and analytical-compression manifests retain their original scopes. The historical `release_audit/` layer likewise predates this DCG revision. Current closeout checks must use a separately scoped current manifest and audit report rather than rewriting those historical records.
