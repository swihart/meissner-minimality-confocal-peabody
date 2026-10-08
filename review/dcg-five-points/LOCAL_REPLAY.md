# Local official-header MPFR replay

The assistant preflight used the MPFR 4.2.2 runtime library in a container lacking the development header.  The publication replay must compile the same source against the official `mpfr.h`.  The supplied build script refuses to use fallback ABI declarations.

## macOS prerequisites

```bash
brew install mpfr gmp pkg-config
```

## Run from the public repository root

```bash
review/dcg-five-points/scripts/run_mpfr_replays.sh "$PWD"
```

Required final marker:

```text
PEABODY_DCG_MPFR_REPLAY_PASS
```

Required build marker:

```text
PEABODY_MPFR_BUILD_OFFICIAL_HEADER_PASS
```

Required certificate classification:

```text
GO_PEABODY_MPFR_DIRECTED_CERTIFICATE
```

The 16-slab under-resolved control and the four-slab correction-sign mutation must both return nonzero exit codes and be recorded as rejected by `mpfr_certificate_audit.json`.

## Commit after the replay passes

Generated files appear under:

```text
review/dcg-five-points/results/mpfr/
```

Commit those outputs separately from the initial checkpoint so the official-header evidence has a clear history.

## Promote Reviewer Point 2 after a passing replay

Run:

```bash
python3 review/dcg-five-points/python/promote_official_mpfr_replay.py \
  --checkpoint-dir review/dcg-five-points
```

Required final marker:

```text
PEABODY_DCG_POINT_2_OFFICIAL_HEADER_PROMOTION_PASS
```

This updates the machine-readable progress record and the Point 2 row of `REVIEW_PROGRESS_LEDGER.md`, and creates `data/official_header_mpfr_promotion.json`.
