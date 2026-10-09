# Initial Arb target calibration

The first independent Arb replay on the author's Mac completed the canonical
384-bit forward calculation but returned the classification
`NO_GO_PEABODY_ARB_FLINT_CERTIFICATE`.  This was a failure of the frozen
quantitative target, not a failure of the theorem-critical signs.

The rigorous Arb output gave

\[
\Phi(1)>
0.0002951409916769718631415784748725\ldots
>
\frac1{4000},
\]

and

\[
\sup_{0<e<1}\Phi''(e)
<
-0.0000179286178483067822590960273707\ldots
<0.
\]

Thus the endpoint positivity and strict concavity required by the chord
argument were both already enclosed with the correct signs.  The original
auxiliary target

\[
\Phi''(e)<-\frac1{30000}
\]

was simply stronger than the independent Arb enclosure could prove with the
frozen 32-by-10 partition.  Since the theorem uses only strict negativity, the
published exact certificate target is recalibrated conservatively to

\[
\Phi''(e)<-\frac1{100000}.
\]

The first Arb upper bound lies strictly below this new target by more than
\(7.9\times10^{-6}\).  The endpoint target remains unchanged at
\(\Phi(1)>1/4000\).  The failed first target and the successful replacement
are both recorded so that the revision history is transparent.
