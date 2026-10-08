# Design of the independent certificate checker

The principal central certifier represents q derivatives inside an `x`-jet by nesting two custom
classes. The release checker deliberately uses a different representation:

\[
(f,f_q,f_x,f_{xx},f_{qx},f_{qxx}).
\]

Product, reciprocal, square-root, and arctangent rules are coded directly for this six-component jet.
No theorem-package Python module is imported.

For each local slab, the checker independently reconstructs

\[
\Phi'(e)=\frac18\frac{d\Psi}{dq}\frac{dq}{de}
\]

using the midpoint rule and the `qxx` remainder term.

For each bulk slab, it reconstructs

\[
\Psi(q)\in\Psi(q_m)+(q-q_m)\Psi_q(Q)
\]

and then `Phi=(Psi-Psi(0))/8`.

For each tail slab, it directly interval-evaluates the stable integrand on all 400 archived `x` panels.

The checker also verifies:

- the exact local, bulk, and tail partitions;
- the exact seams `e=1/100` and `e=199/200 <-> q=1/399`;
- terminal-box row counts and complete panel indices;
- the archived central and tail classifications.

A pass by this program is not logically independent of the `mpmath.iv` library, but it is independent
of the principal code path and catches transcription, derivative, control-flow, and metadata errors.
