# Five-point reviewer progress ledger

Update this ledger in every substantive revision commit.

| # | Reviewer point | Current status | Evidence in this checkpoint | Remaining gate |
|---:|---|---|---|---|
| 1 | Convexity, constant width, and exact Gauss tiling for every `e` and `sigma` | **PROOF DRAFT + MANUSCRIPT INTEGRATION COMPLETE — 90%** | `notes/01_full_parameter_geometry_and_gauss_partition.md` gives the source crosswalk, full-parameter chart admissibility, patch decomposition, normal-sphere disjointness/coverage, seam nullity, vertex-cone duality, and opposite-wedge antipodality | Independent proofread by a convex geometer; apply any corrections to the integrated manuscript lemmas |
| 2 | Interval-arithmetic trust boundary | **CLOSED — INDEPENDENT ARB/FLINT REPLAY PASS — 100%** | Independent `python-flint` 0.9.0 implementation; rigorous Arb balls for arithmetic, `sqrt`, and `atan`; 384/512-bit and reverse-order passes; under-resolved and sign-mutation controls rejected; overlap with the archived direct-MPFR preflight; high-headroom bounds `Phi(1)>1/4000` and `Phi''<-1/100000` | Final editorial integration into the DCG manuscript and release-response letter only |
| 3 | Full derivation of the one-pair formula and branch control | **DERIVATION + MANUSCRIPT INTEGRATION COMPLETE — 90%** | `notes/03_formula_derivation_and_branch_control.md`; exact identity checker returns `PEABODY_FORMULA_DERIVATION_IDENTITIES_PASS` | Independent line-by-line human rederivation; apply any corrections and finalize equation numbering |
| 4 | Smooth extension at `q=0` | **CLOSED ANALYTICALLY — 100%** | `notes/04_parabolic_endpoint_analyticity.md` proves radicands and denominators are uniformly separated from zero and that the stable integrand is real analytic near the closed square | Inserted in the checkpoint manuscript; final editorial review only |
| 5 | Eight orientations, equality classes, and seam measure zero | **CLOSED ANALYTICALLY — 100%** | `notes/05_orientation_seams_equality.md` enumerates four vertex stars and four face boundaries, proves two tetrahedral orbits, seam nullity, and equality classification | Inserted in the checkpoint manuscript; final editorial review only |

## Overall revision state

- **Counterexample or theorem failure found:** no.
- **Regular Peabody theorem changed:** no.
- **New shape search begun:** no.
- **Mandatory technical risks remaining:** independent review and manuscript integration of Points 1 and 3.
- **Current recommendation:** continue the finite major revision; do not reopen numerical search or semi-regular extensions.
