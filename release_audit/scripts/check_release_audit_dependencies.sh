#!/usr/bin/env bash
set -u

printf '%s\n' '== Python =='
python3 --version
python3 - <<'PY'
import mpmath, sympy
print('mpmath', mpmath.__version__)
print('sympy', sympy.__version__)
PY

printf '%s\n' '== Mathematica =='
if command -v wolframscript >/dev/null 2>&1; then
  wolframscript -code '$Version'
else
  printf '%s\n' 'wolframscript not found; set WOLFRAMSCRIPT_BIN when running the Mathematica stage.'
fi

printf '%s\n' '== R =='
if command -v Rscript >/dev/null 2>&1; then
  Rscript --version
  Rscript -e 'for (p in c("jsonlite","Rmpfr","gmp")) cat(p, requireNamespace(p, quietly=TRUE), "\n")'
else
  printf '%s\n' 'Rscript not found.'
fi
