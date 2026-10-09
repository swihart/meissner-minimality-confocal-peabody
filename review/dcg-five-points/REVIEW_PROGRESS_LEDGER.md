# Five-point reviewer progress ledger

Update this ledger in every substantive revision commit.

| # | Reviewer point | Current status | Evidence in this checkpoint | Remaining gate |
|---:|---|---|---|---|
| 1 | Convexity, constant width, and exact Gauss tiling for every `e` and `sigma` | **CLOSED INTERNALLY — 100%** | Explicit principal-circle and bulb-center verification; regular-tetrahedron endpoint proof; source-theorem crosswalk; strict-convexity normal partition; seam nullity; cap-cone duality; corrected singular-arc degeneration | External source-author or convex-geometer convention check recommended before submission |
| 2 | Interval-arithmetic trust boundary | **CLOSED - ARB/FLINT REPLAY AND ENCLOSURE PROVENANCE RECONCILED - 100%** | Independent Arb proof authority; direct-MPFR and legacy mpmath endpoint-interval comparisons; bounded Arb refinement audit; conservative Arb constants used in the manuscript | Final editorial review only |
| 3 | Full derivation of the one-pair formula and branch control | **CLOSED INTERNALLY — 100%** | Complete center-distance, normal-chart, wedge-Jacobian, `xi`-integration, `Psi(0)`, fixed-interval, stable-chart, coefficient, and principal-branch derivations; independent exact identity audit passes | External line-by-line mathematical proofread recommended before submission |
| 4 | Smooth extension at `q=0` | **CLOSED ANALYTICALLY — 100%** | `notes/04_parabolic_endpoint_analyticity.md` proves radicands and denominators are uniformly separated from zero and that the stable integrand is real analytic near the closed square | Inserted in the checkpoint manuscript; final editorial review only |
| 5 | Eight orientations, equality classes, and seam measure zero | **CLOSED ANALYTICALLY — 100%** | `notes/05_orientation_seams_equality.md` enumerates four vertex stars and four face boundaries, proves two tetrahedral orbits, seam nullity, and equality classification | Inserted in the checkpoint manuscript; final editorial review only |

## Overall revision state

- **Counterexample or theorem failure found:** no.
- **Regular Peabody theorem changed:** no.
- **New shape search begun:** no.
- **Mandatory technical risks remaining:** final manuscript integration, external geometric/formula review, and five-point release audit.
- **Current recommendation:** continue the finite major revision; do not reopen numerical search or semi-regular extensions.

## Follow-up enclosure-provenance reconciliation

- The direct-MPFR and legacy `mpmath.iv` endpoint-interval implementations agree closely at the frozen `32x10` partition.
- Arb midpoint-radius enclosures are wider on the coarse partition; the theorem uses only the conservative Arb result.
- A bounded `32x10`, `64x20`, `128x20` refinement study records the enclosure-width behavior without changing the formula or theorem.
- The manuscript now uses the Arb endpoint decimal consistently and no longer states the ambiguous `overlap` sentence.

## Bounded closeout audit, 2026-10-09

The actual `ab320cf` archive verifies the recorded reconciliation PASS. The separate current closeout audit passes 365 archive-semantic checks, including exact downstream reconstruction of all 96 authoritative concavity slabs. Published rational targets and the underlying Arb source/results are unchanged. Corrected source, directed table formatting, current build instructions, and a separate current manifest are supplied. External geometry/formula proofreading remains undocumented; final submission sign-off remains pending. See `closeout/CLOSEOUT_REPORT.md`.

## Final internal mathematical audit based on `b9fb7c5`, 2026-10-09

**PEABODY_FINAL_INTERNAL_MATHEMATICAL_AUDIT_PASS.** Four independent internal
review tracks and coordinating re-review found no unresolved theorem-level
obstruction after finite corrections. The manuscript now includes the source
chart converse, a direct cap-cone proof, the normal-chart inverse, explicit
mixed-limit continuity, precise singular-arc and orientation conventions, and
fixed-parameter mean-value notation. Supporting notes are synchronized.

The theorem, the protected 50-file package, all archived scalar certificates,
the canonical partition, and both rational targets are unchanged. The 365
archive checks still pass; the new exact-rational Python corroboration passes
285 derivative coefficient identities and rejects one intentional sign mutation.
The matching R script is supplied but unexecuted; no cross-language runtime
agreement or fresh Arb replay is claimed. The 15-page PDF is internally ready
for an external review request after this checkpoint is integrated and pushed.
External review and final submission remain pending. See
`final-math-audit/FINAL_MATHEMATICAL_AUDIT.md`.
