# Reviewer Point 2: independent Arb/FLINT trust-boundary response

## Referee concern

The public version used `mpmath.iv` as proof authority. The referee correctly
observed that a journal reader should not have to infer directed-rounding
semantics for every arithmetic, square-root, and arctangent call from an
experimental interval context.

## Revision

The revised checkpoint contains an independently written certificate using
`python-flint==0.9.0` and Arb real balls. The implementation does not import the
principal certifier. It reconstructs the stable `q`-chart function and the
required mixed derivatives directly.

For an exact rational interval `[a,b]`, the program constructs the Arb ball
with exact rational midpoint `(a+b)/2` and radius `(b-a)/2`. Every subsequent
operation is a real-ball operation. In particular, the square-root and
arctangent evaluations return balls enclosing the exact images of their input
balls.

The certificate proves the publication bounds

\[
\Phi(1)>\frac1{4000}
\]

and

\[
\Phi''(e)<-\frac1{100000}\qquad(0<e<1).
\]

The endpoint bound and the strict-concavity bound leave substantial headroom relative to the independent Arb enclosures. The concavity constant is intentionally much weaker than the raw negative upper bound because only strict negativity is used in the theorem. The endpoint bound and concavity also imply the simple chord estimate

\[
\Phi(e)>\frac e{4000}\qquad(0<e<1).
\]

## Finite architecture

The canonical run uses 4 endpoint panels and 32 by 10 concavity rectangles,
for 324 terminal rectangles. It is replayed at 384 and 512 bits and in reverse
slab order. Two controls must be rejected:

1. a deliberately under-resolved one-slab, one-panel partition;
2. a correction-sector sign mutation.

The output auditor checks overlap of all 32 Arb slab enclosures with the
archived direct-MPFR preflight certificate. Agreement is therefore checked
between three independent implementations:

- the original `mpmath.iv` certificate;
- the direct-MPFR C preflight;
- the new Arb/FLINT certifier.

## Installation isolation

The author replay uses a Python virtual environment under the user's cache
directory. It installs a pinned prebuilt wheel and records the pip install
report, module path, Python version, platform, precision, and hashes. Homebrew,
administrator privileges, and system-wide libraries are not used.

## Promotion rule

Reviewer Point 2 remains open until the local replay produces all of:

```text
PEABODY_ARB_NO_BREW_REPLAY_PASS
PEABODY_ARB_FLINT_CERTIFICATE_AUDIT_PASS
PEABODY_DCG_POINT_2_ARB_FLINT_PROMOTION_PASS
```

Only then may the progress ledger mark the point closed.
