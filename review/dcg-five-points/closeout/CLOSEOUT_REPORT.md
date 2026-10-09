# Confocal Peabody: bounded DCG closeout review

Date: 2026-10-09. Recommended next-turn mode: **PRO** for external-proofreading
resolution and final mathematical/submission sign-off; **MEDIUM** for integration.

## Result and scope

The completed enclosure reconciliation is confirmed from the actual archived
results. Its exact recorded verdict is `PEABODY_ENCLOSURE_RECONCILIATION_PASS`.
This review independently verifies the archived arithmetic and provenance and
prepares bounded source/packaging corrections. The regular-family theorem and
its published constants are unchanged. No new shape search or extension was run.

Input repository: `swihart/meissner-minimality-confocal-peabody`, branch
`review/dcg-major-revision`. Input commit:
`ab320cff615408af8ca8f35f54715e75932c1dd5`, recorded in the Git archive comment.
The supplied ZIP has SHA-256
`8590cc2b29798fca0bb9ecc1b3462d43de0a8e9e0b93eb3fa7e65eb8a878aacc`.
The user's terminal record identifies reconciliation commit `4f332c2` and
editorial/provenance commit `ab320cf`; this ZIP is a tree snapshot, not Git history.

The claim ledger remains:

| Kind | Status |
|---|---|
| Source-established construction | Confocal devices and regular-tetrahedron constant-width assembly |
| Exact project derivation | Pairwise volume additivity, orientation independence, stable formula, normalization |
| Finite certificate | Canonical Arb scalar bounds retained; archive arithmetic verified here |
| Numerical/diagnostic evidence | Refined displayed endpoints and enclosure-width comparisons |
| Workflow update | Current documentation, display rounding, build target, and audit-manifest corrections |
| Pending | Identifiable external geometry/source-convention and formula proofreading; final submission sign-off |
| Not established by this work | Global Meissner extremality or a new universal lower bound |

## Progress against the immediately preceding checkpoint

| Item | `ab320cf` supplied state | Closeout result | Delta |
|---|---|---|---|
| Reconciliation evidence | Committed result present | Actual data independently checked | Improved evidence access |
| Canonical exact scalar targets | `Phi(1)>1/4000`, `Phi''<-1/100000` | Same targets, exact archived dyadic checks pass | Unchanged theorem |
| Independent archive verifier | Earlier overlap/hash auditor | 365 checks; 37 inputs hashed; 96 slabs reconstructed | Improved |
| Refined data | 224 slabs and 32 aggregate rows | All checked against reports | Improved verification |
| Printed enclosure table | Two upper endpoints rounded inward; partitions unstated | Outward formatting and four explicit resolutions | Corrected |
| Build instructions | Historical checkpoint selected | Corrected closeout source selected; required table | Corrected |
| Manifest scope | Initial 51-file manifest used beyond its scope | Separate current manifest/validator | Corrected |
| External-review wording | Unsupported statement that material was sent | Completion/correspondence not documented | Corrected wording; gate unchanged |
| External reviews / submission | Not documented / not frozen | Still not documented / not frozen | Unchanged |

In plain language: the recorded calculation did finish and its files are
consistent. The apparent changes in decimal bounds come from different
enclosures, with refinement producing tighter ones. The remaining work is
human proofreading and submission preparation, not another numerical campaign.

## Numerical provenance

The following are approximate diagnostic displays, not replacement proof gates.

| Arb computation | Lower endpoint for `Phi(1)` | Worst upper endpoint for `Phi''` |
|---|---:|---:|
| Canonical 32 x 10; endpoint 4 panels | 0.000295140991676972 | -0.000017928617848307 |
| Refinement 64 x 20 | — | -0.000157521889754448 |
| Refinement 128 x 20; endpoint 16 panels | 0.000376664510492940 | -0.000179370994780069 |

All 32 direct-MPFR slab intervals contain their legacy `mpmath.iv` counterparts.
All 96 aggregated Arb/MPFR comparisons intersect. The refined worst upper bounds
tighten monotonically, and the endpoint intervals are nested. These observations
do not show the historical `mpmath.iv` computation false. The canonical Arb
certificate remains the sole publication authority for the two rational bounds.

## What was executed

`python/verify_archived_reconciliation.py` uses standard-library exact Fractions
for the publication gates and reconstruction from archived binary endpoints.
It checks three authoritative runs, 960 terminal rectangles, 12 endpoint panels,
all 96 reconstructed concavity targets, 224 diagnostic refinement rows, 32
aggregate comparisons, baseline differences, two recorded negative controls,
and recorded output hashes. Its report is `archive_semantic_audit.json`. Two new mutation controls (a false exact endpoint and a corrupted slab boundary) were rejected by the semantic checks as well as the hash checks; see `adversarial_archive_controls.json`.

This is **not a fresh Arb or MPFR special-function replay**. It trusts the
archived terminal terms as enclosures of the analytic derivative expressions,
then independently checks their downstream arithmetic, coverage, and targets.
Installation of the pinned Arb wheel was attempted in an isolated environment,
but no matching distribution was available through this environment's package
access. No replacement arithmetic backend or relaxed version pin was used.

The R companion `R/verify_archived_reconciliation.R` uses `jsonlite` and `gmp` for
the same core exact-rational targets and coverage, plus refinement diagnostics.
It explicitly omits Python's hash, baseline-comparison, and control-artifact
checks. **R was not executed** because `Rscript` is unavailable. No cross-language
agreement is claimed. To run it locally from the repository root:

```bash
Rscript review/dcg-five-points/R/verify_archived_reconciliation.R \
  --root . --output /tmp/peabody_closeout_R.json
```

## Bounded source corrections

The new `main_dcg_closeout_review.tex` preserves the earlier reconciled source/PDF
pair as historical evidence. It fixes the conjecture-implication wording, makes
the unit-normal convention and seam-nullity argument explicit, cites the known
noncongruence of the two Meissner types, distinguishes the reparameterized
functions, requires the reconciliation table, and adds code/AI disclosures.
The referee response no longer asserts undocumented correspondence. These are
internal proofreading corrections, not completed external approval.

The table formatter rounds lower displays downward and upper displays upward,
prints mathematical powers of ten, and records canonical/refined partitions.
The refinement runner uses that formatter for future outputs; its integrand,
partitions, and archived numerical results are unchanged. A corrected table for
the new manuscript is separate from the archived table.

`build.sh` now selects the new source through `build_closeout.sh`. The default
retains New TX fonts. The supplied 14-page review PDF was rebuilt successfully, with no undefined references or overfull/underfull box warnings. It uses the documented Latin Modern
portable-font option because New TX is absent here. Default-font pagination
should be reviewed at final submission freeze. No journal submission or message
to a reviewer/source author was sent.

## Historical checksums and trust boundaries

| Historical scope | Verified result |
|---|---:|
| Immutable root manifest | 50/50 match |
| Root checksum ledger | 51/51 match |
| Analytical-compression manifest and checksum ledger | 38/38 each match |
| Five Arb output-hash sets | 14/14 match |
| Historical release-audit manifest | 101/102 match |
| Historical release-audit checksum ledger | 39/42 match |
| Initial DCG manifest | 47/51 match |
| Initial DCG checksum ledger | 48/52 match |

The initial DCG hashes predate four revised notes/status files, and its validator
requires Point 2 to remain open. Its failure on the expanded revision is a scope
mismatch. The release-audit manifest also hashed its own stdout transcript while
that file was empty, before writing it; some R/support hashes are stale. These
records are preserved, not silently rewritten. See `historical_manifest_audit.json`.

The historical release checker converts rational endpoints through binary64 in
one interval constructor; it must not be described as an exact-rational replay.
The current Arb source does not use that conversion. No current canonical Arb
output-hash mismatch was found.

The separate `CURRENT_REVIEW_MANIFEST.json` covers this corrected review tree.
Its validator checks exact current file coverage, hashes, the protected 50-file
theorem package, archive semantics, regenerated directed table, and status
consistency. It explicitly excludes itself, Python bytecode caches, and local
LaTeX build products (except the tracked build-directory ignore file), so it
does not repeat the self-transcript hash defect. Run before local edits:

```bash
python3 review/dcg-five-points/python/validate_current_closeout.py --repo-root .
```

## Finite path to submission

| Remaining block | Next action | Expected commits |
|---|---|---:|
| Integrate these bounded corrections | Apply the guarded overlay; run current validator | 1 |
| External geometry and formula proofreading | Obtain identifiable responses; resolve any corrections | Depends on actual feedback |
| Submission freeze | Review default-font PDF, declarations and final checklist; then create `submission/dcg-v1` | 1, after reviews |

No focused-hour estimate is assigned to external reviewers' availability. Mountain
I and other MinVol workstreams are outside this closeout; their status and
forecasts are unchanged. The published regular-family result is preserved.

Recommended commit: **`Audit Peabody reconciliation and correct submission provenance`**.
No commit or push was performed in the user's repository.
Recommended next-turn mode: **PRO** for final review; **MEDIUM** for applying the overlay.
