# Assistant-side preflight results

These files record preliminary runtime tests performed before delivery of the release-audit scaffold.
They are **not** the branch's final audit outputs and are deliberately separated from `results/`.

Completed in the assistant environment:

- independent one-pair formula rederivation: PASS;
- independent Python certificate checker: PASS;
- Python static compilation: PASS;
- shell syntax checks: PASS;
- Wolfram Language delimiter/string/comment static checks: PASS;
- simulated Git bootstrap and frozen-baseline verification: PASS.

Not executable in the assistant environment:

- Wolfram Engine / Mathematica fresh-kernel replay;
- R semantic audit (`Rscript` was unavailable).

Run the supplied scripts locally. Only outputs generated under `results/` on the audit branch count toward
`PEABODY_RELEASE_AUDIT_PASS`.
