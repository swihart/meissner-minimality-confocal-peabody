# Meissner minimality in the confocal Peabody family

This repository is the public research release for the theorem that the classical Meissner degenerations minimize volume within the width-one regular-tetrahedron confocal Peabody family.

The exact family reduction is

\[
\operatorname{Vol}K(\mathbf e,\boldsymbol\sigma)
=
V_M+\Phi(e_1)+\Phi(e_2)+\Phi(e_3),
\]

independent of the eight orientation patterns. The current compressed proof certifies

\[
\Phi(1)>\frac{3}{10000},
\qquad
\Phi''(e)<-\frac{1}{25000}\quad(0<e<1),
\]

so strict concavity and \(\Phi(0)=0\) give

\[
\Phi(e)>\frac{3e}{10000}>0\quad(0<e<1).
\]

## Scope

This is a restricted-family theorem. It does not prove global Meissner extremality among all three-dimensional bodies of constant width, and it does not establish a global six-patch construction for arbitrary semi-regular tetrahedral bases.

## Contents

- the immutable release-audited theorem package;
- independent formula, certificate, Mathematica, and R release-audit materials;
- the analytical-compression package with 324 terminal rectangles;
- the current manuscript and archived earlier drafts;
- exact manifests, checksums, scripts, transcripts, and trust-boundary documentation.

## Proof authority

The proof authority is exact rational partition control together with outward-rounded interval arithmetic. High-precision quadrature, Mathematica, and R are independent audit evidence rather than proof authority.

## Status

This is public research release v1.0.0. A later revision will address external review points in preparation for possible submission to *Discrete & Computational Geometry*.
