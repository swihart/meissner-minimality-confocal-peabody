# Arb adversarial-control serialization repair

The first recalibrated Arb replay completed all three authoritative runs:
384-bit forward, 512-bit forward, and 384-bit reverse order.  It then stopped
inside the deliberately under-resolved and sign-mutated controls while trying
to serialize diagnostic interval endpoints.

The controls are intentionally allowed to produce unbounded or indeterminate
Arb balls.  Python-FLINT's `arb.man_exp()` is defined only for exact finite
values, so calling it on such a diagnostic endpoint raises `ValueError`.  This
was a flight-recorder bug, not a failure of the authoritative inequalities.

The repaired serializer now:

1. archives exact binary mantissa/exponent pairs only for exact finite directed
   endpoints;
2. writes `null` binary endpoints for nonfinite control diagnostics;
3. keeps the strict exact-finite requirement for every authoritative terminal
   box; and
4. requires each negative control to emit a JSON certificate with
   `pass=false`, `proof_status=NOT_CERTIFIED`, and classification
   `NO_GO_PEABODY_ARB_FLINT_CERTIFICATE`.

Thus an expected negative control can no longer count as successful merely by
crashing before the semantic certificate is written.
