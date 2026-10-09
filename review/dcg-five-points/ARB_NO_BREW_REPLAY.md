# No-Homebrew Arb/FLINT replay for Reviewer Point 2

This replay replaces the Homebrew-dependent official-header MPFR step. It uses
an isolated Python virtual environment and the prebuilt `python-flint==0.9.0`
wheel. No system package manager and no root installation are used.

## What is independent

The Arb certifier does not import the principal `mpmath.iv` certifier or the
archived direct-MPFR C implementation. It reconstructs the stable `q` chart,
automatic-differentiation jets, midpoint quadrature remainders, exact rational
partitions, endpoint inequality, and concavity inequality from the frozen
formula definitions.

The proof targets are deliberately conservative:

\[
\Phi(1)>\frac1{4000},
\qquad
\Phi''(e)<-\frac1{30000}\quad(0<e<1).
\]

The canonical certificate uses:

- 4 endpoint panels;
- 32 exact rational `q` slabs;
- 10 exact rational `x` panels per slab;
- 324 terminal rectangles;
- Arb real-ball arithmetic for all arithmetic, square roots, and arctangents.

## One command

From the repository root on branch `review/dcg-major-revision`:

```bash
review/dcg-five-points/scripts/run_arb_no_brew_replay.sh "$PWD"
```

The runner:

1. selects Python 3.10--3.14;
2. creates a virtual environment under `~/.cache/peabody-arb/`;
3. installs exactly `python-flint==0.9.0` from a binary wheel;
4. archives the pip install report and module provenance;
5. runs 384-bit, 512-bit, and reverse-order certificates;
6. requires an under-resolved partition and a correction-sign mutation to fail;
7. compares every Arb slab with the archived direct-MPFR preflight enclosure;
8. checks every generated-output hash;
9. emits `PEABODY_ARB_NO_BREW_REPLAY_PASS` only if every gate passes.

If corporate networking blocks pip, download a matching wheel in a browser and
run:

```bash
PEABODY_ARB_WHEEL="$HOME/Downloads/<wheel-file>.whl" review/dcg-five-points/scripts/run_arb_no_brew_replay.sh "$PWD"
```

## Promotion

After the replay passes:

```bash
python3 review/dcg-five-points/python/promote_arb_replay.py --checkpoint-dir review/dcg-five-points
```

The expected marker is:

```text
PEABODY_DCG_POINT_2_ARB_FLINT_PROMOTION_PASS
```

This changes only the reviewer-response ledger and creates the promotion
record. It does not modify the frozen public `v1.0.0` release.

## Proof authority and trust boundary

The proof authority for this reviewer response is the archived Arb output. The
trust boundary consists of:

- CPython;
- `python-flint==0.9.0` and its bundled FLINT/Arb implementation;
- the independent certifier source;
- exact rational partitions and ball conversions;
- the operating system and hardware executing the wheel.

The archived `mpmath.iv` and direct-MPFR computations remain redundant audits,
not the sole authority for the revised paper.
