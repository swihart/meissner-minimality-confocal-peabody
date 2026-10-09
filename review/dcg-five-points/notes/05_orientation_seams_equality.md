# Reviewer Point 5 — Orientation classes, seams, and equality cases

## Status

**Closed analytically.**

## 1. The eight orientation choices form two tetrahedral orbits

Label the tetrahedron vertices \(A,B,C,D\).  The three opposite-edge pairs are

\[
\{AB,CD\},
\qquad
\{AC,BD\},
\qquad
\{AD,BC\}.
\]

An orientation vector \(\boldsymbol\sigma\in\{0,1\}^3\) selects one edge from each pair.  The eight possible selected triples are exactly:

### Vertex stars

\[
\{AB,AC,AD\},
\quad
\{AB,BD,BC\},
\quad
\{CD,AC,BC\},
\quad
\{CD,BD,AD\}.
\]

These are the triples of edges incident to \(A,B,C,D\), respectively.

### Face boundaries

\[
\{AB,AC,BC\},
\quad
\{AB,BD,AD\},
\quad
\{CD,AC,AD\},
\quad
\{CD,BD,BC\}.
\]

These are the edge sets bounding the faces \(ABC,ABD,ACD,BCD\), respectively.

The tetrahedral symmetry group acts transitively on vertices and transitively on faces.  Thus the eight orientations collapse to exactly two congruence classes:

1. round the three edges incident to a vertex;
2. round the three edges bounding a face.

In the manuscript, each orientation bit selects the elliptic edge, which
retains a circular singular arc at zero. The complementary edges are
rounded. Complementation exchanges the star and face types, so the list
of congruence classes is unchanged. At the all-zero parameter triple these
are precisely the two classical noncongruent Meissner bodies; see Kawohl
and Weber, *Meissner's Mysterious Bodies*.

## 2. Why seams may be ignored in area bookkeeping

For generic positive parameters `e_i>0`, the regular Peabody boundary
consists of finitely many smooth patch interiors whose closures meet
along finitely many piecewise-smooth seam curves and at four vertices.
The source construction gives a common tangent plane along nonvertex seams.

A finite union of these curves has physical area zero. Away from vertices,
the explicit seam maps and common normals are smooth. Exhaust each
nonvertex seam by countably many compact subarcs; each normal image has
spherical area zero, and so does their countable union.

This conclusion must not be applied to the singular circular arcs at zero
parameters. The union of unit normal regions along a collapsed wedge can
have positive spherical area. Mixed degenerations retain this contribution
by the continuity argument in note 01, Section 10.

The vertices are different: their normal cones can have positive spherical area and are included explicitly in the normal-sphere partition.  The equality

\[
N_K(A)=-\Omega_A
\]

between the unit vertex-normal region and the antipodal radial image of
the closed opposite spherical cap accounts for these contributions exactly.

## 3. Equality statement

The scalar theorem gives

\[
\Phi(0)=0,
\qquad
\Phi(e)>0\quad(0<e<1).
\]

The additive volume identity is

\[
V(K(\mathbf e,\boldsymbol\sigma))-V_M
=\Phi(e_1)+\Phi(e_2)+\Phi(e_3).
\]

Every term is nonnegative, so equality holds if and only if

\[
e_1=e_2=e_3=0.
\]

The preceding orbit classification then identifies the equality cases, over all eight orientation choices, with exactly the two classical Meissner congruence classes.
