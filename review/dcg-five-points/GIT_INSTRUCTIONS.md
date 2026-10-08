# Git integration instructions

This checkpoint belongs on a review branch created from the immutable public release tag `v1.0.0` in:

```text
~/github/meissner-minimality-confocal-peabody
```

## Branch

```text
review/dcg-five-points
```

## Initial checkpoint commit

```text
Open five-point DCG revision checkpoint
```

## Official-header MPFR replay commit

```text
Recompute the Peabody certificate with MPFR
```

## Policy

- Do not modify or retag `v1.0.0`.
- Do not merge the review branch into `main` until the five-point revision is complete.
- Update `REVIEW_PROGRESS_LEDGER.md` in every substantive commit.
- Do not treat the assistant runtime-only MPFR preflight as the final journal proof authority; the author's official-header replay is mandatory.
- Do not reopen the Peabody numerical search or begin a semi-regular extension.

## After the official-header replay passes

Run the promotion helper, then commit the generated replay outputs and Point 2 ledger update with:

```text
Recompute the Peabody certificate with MPFR
```
