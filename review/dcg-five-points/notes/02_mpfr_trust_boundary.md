# Reviewer Point 2 — Independent directed-rounding certificate

## Status

**Independent certificate completed in direct MPFR 4.2.2 arithmetic.  A local rebuild using the official `mpfr.h` remains recommended before journal submission.**

The original theorem package used `mpmath 1.3.0`'s experimental interval context as proof authority.  This review checkpoint replaces that trust boundary with a second implementation that calls MPFR directly and evaluates every lower endpoint with `MPFR_RNDD` and every upper endpoint with `MPFR_RNDU`.

The implementation is independent of the principal Python certifier:

- it is written in C;
- it does not import the `mpmath` implementation;
- it reconstructs the stable formula and automatic-differentiation jets directly;
- it calls `mpfr_sqrt` and `mpfr_atan` with directed rounding;
- it uses exact rational panel and slab endpoints;
- it archives every endpoint and concavity enclosure.

## Certified statements

To increase publication headroom, the independent certificate proves the weaker conclusions

\[
\boxed{\Phi(1)>\frac1{4000}}
\]

and

\[
\boxed{\Phi''(e)<-\frac1{30000}\qquad(0<e<1).}
\]

The raw MPFR enclosures are

\[
\Phi(1)>
0.0003076528682490342053580258083025767\ldots,
\]

and

\[
\sup_{0<e<1}\Phi''(e)
< -0.0000416491903361455479929355233265745\ldots.
\]

These have comfortable margins over

\[
\frac1{4000}=0.00025
\]

and

\[
-\frac1{30000}=-0.0000333333\ldots.
\]

By concavity and \(\Phi(0)=0\),

\[
\Phi(e)\ge e\Phi(1)>\frac e{4000}.
\]

## Replays and controls

| Replay or control | Result |
|---|---|
| 384-bit forward run | PASS |
| 512-bit forward run | PASS |
| 384-bit reverse slab order | PASS |
| 16-slab under-resolved control | correctly rejected |
| correction-sector sign mutation | correctly rejected |
| all 32 MPFR slab enclosures overlap the archived `mpmath.iv` enclosures | PASS |
| all global radicand and denominator diagnostics | strictly positive |

The 384- and 512-bit runs produced identical reported endpoint and weakest-concavity leading digits.  The reverse-order run produced the same certificate.

## Directed-rounding implementation

The interval operations are elementary endpoint formulas.  For example,

\[
[a,b]+[c,d]=[\operatorname{RNDD}(a+c),\operatorname{RNDU}(b+d)],
\]

and multiplication takes the minimum of the four downward-rounded endpoint products and the maximum of the four upward-rounded endpoint products.  Since square root and arctangent are monotone on the certified positive domains,

\[
\sqrt{[a,b]}
=[\operatorname{RNDD}(\sqrt a),\operatorname{RNDU}(\sqrt b)],
\]

\[
\arctan[a,b]
=[\operatorname{RNDD}(\arctan a),\operatorname{RNDU}(\arctan b)].
\]

The code calls the MPFR transcendental functions directly rather than relying on an interval wrapper.

## Header and platform note

Publication builds should compile against the official MPFR development header.  The archived build script detects `pkg-config`, Homebrew, or a normal system installation and defines `PEABODY_USE_SYSTEM_MPFR_HEADER`.  The assistant container had the runtime library but not the development header, so its replay used a small archived ABI declaration fallback.  The numerical operations were still performed by `libmpfr.so.6`, version 4.2.2.

Before submission, run the same source on the author's machine after

```text
brew install mpfr gmp pkg-config
```

and archive the official-header transcript.  The expected final marker is

```text
GO_PEABODY_MPFR_DIRECTED_CERTIFICATE
```

## Publication recommendation

The manuscript should make the MPFR certificate the proof authority and retain `mpmath.iv`, Mathematica, and R as redundant semantic audits.  This directly answers the reviewer's trust-boundary concern without requiring a full formalization in Lean or Coq.
