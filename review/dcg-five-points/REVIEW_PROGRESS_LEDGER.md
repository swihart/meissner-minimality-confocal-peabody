# Five-point reviewer progress ledger

Update this ledger in every substantive revision commit.

| # | Reviewer point | Current status | Evidence in this checkpoint | Remaining gate |
|---:|---|---|---|---|
| 1 | Convexity, constant width, and exact Gauss tiling for every `e` and `sigma` | **CLOSED INTERNALLY — 100%** | Explicit principal-circle and bulb-center verification; regular-tetrahedron endpoint proof; source-theorem crosswalk; strict-convexity normal partition; seam nullity; cap-cone duality; corrected singular-arc degeneration | External source-author or convex-geometer convention check recommended before submission |
| 2 | Interval-arithmetic trust boundary | **CLOSED — INDEPENDENT ARB/FLINT REPLAY PASS — 100%** | Independent `python-flint` 0.9.0 implementation; rigorous Arb balls for arithmetic, `sqrt`, and `atan`; 384/512-bit and reverse-order passes; under-resolved and sign-mutation controls rejected; overlap with the archived direct-MPFR preflight; high-headroom bounds `Phi(1)>1/4000` and `Phi''<-1/100000` | Final editorial integration into the DCG manuscript and release-response letter only |
| 3 | Full derivation of the one-pair formula and branch control | **CLOSED INTERNALLY — 100%** | Complete center-distance, normal-chart, wedge-Jacobian, `xi`-integration, `Psi(0)`, fixed-interval, stable-chart, coefficient, and principal-branch derivations; independent exact identity audit passes | External line-by-line mathematical proofread recommended before submission |
| 4 | Smooth extension at `q=0` | **CLOSED ANALYTICALLY — 100%** | `notes/04_parabolic_endpoint_analyticity.md` proves radicands and denominators are uniformly separated from zero and that the stable integrand is real analytic near the closed square | Inserted in the checkpoint manuscript; final editorial review only |
| 5 | Eight orientations, equality classes, and seam measure zero | **CLOSED ANALYTICALLY — 100%** | `notes/05_orientation_seams_equality.md` enumerates four vertex stars and four face boundaries, proves two tetrahedral orbits, seam nullity, and equality classification | Inserted in the checkpoint manuscript; final editorial review only |

## Overall revision state

- **Counterexample or theorem failure found:** no.
- **Regular Peabody theorem changed:** no.
- **New shape search begun:** no.
- **Mandatory technical risks remaining:** final manuscript integration, external geometric/formula review, and five-point release audit.
- **Current recommendation:** continue the finite major revision; do not reopen numerical search or semi-regular extensions.
