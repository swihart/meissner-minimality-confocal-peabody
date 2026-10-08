# Release-audit task matrix

| Order | Task | Required gate | Output |
|---:|---|---|---|
| 1 | Frozen baseline verification | All manifest sizes and SHA-256 hashes match; `v1.0.0-certified` exists | `results/python/frozen_baseline_verification.json` |
| 2 | Independent one-pair derivation | 2D, reduced 1D, fixed-x, and stable-q formulas agree; exact symbolic identities vanish | `results/python/independent_one_pair_rederivation.json` |
| 3 | Width normalization audit | Every coefficient in the factor-of-eight conversion is justified | `notes/02_width_normalization_line_audit.md` |
| 4 | Three-pair decomposition audit | Normal-sphere partition, seam measure-zero statement, and orientation independence pass | `notes/03_three_pair_additivity_audit.md` |
| 5 | Fresh-kernel Mathematica replay | Required summaries pass and recursive unresolved-expression guards pass | `results/mathematica/wolfram_recursive_guard_summary.json` |
| 6 | Independent certificate checker | All 16 local, 43 bulk, and 5 tail slabs re-certify their rational targets | `results/python/independent_certificate_check.json` |
| 7 | R semantic audit | Formulas, orientation, partitions, metadata, and sample containment pass | `results/R/peabody_release_semantic_audit.json` |
| 8 | Human-readable proof | No TODO markers; scope and trust boundary explicit | `notes/04_human_readable_proof_draft.md` |
| 9 | Final release gate | All above pass and baseline remains frozen | `RELEASE_AUDIT_REPORT.md` |

## Hard stops

- Do not alter the certified payload to make an audit pass.
- Do not silently replace the one-pair formula by the archived implementation.
- Do not treat the optional fixed-rho Mathematica integral as evaluated.
- Do not promote beyond regular-tetrahedron confocal Peabodies.
- Stop and open an issue if the independent formula or certificate checker fails.
