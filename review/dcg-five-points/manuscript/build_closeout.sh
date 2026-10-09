#!/usr/bin/env bash
set -euo pipefail
HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$HERE"
test -s main_dcg_closeout_review.tex
test -s generated_enclosure_reconciliation_closeout.tex
JOB=main_dcg_closeout_review
INPUT=main_dcg_closeout_review.tex
mkdir -p build-closeout
if [ "${1:-}" = "--portable-fonts" ]; then
  INPUT='\def\PeabodyPortableFonts{1}\input{main_dcg_closeout_review.tex}'
fi
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build-closeout -jobname="$JOB" "$INPUT"
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build-closeout -jobname="$JOB" "$INPUT"
printf 'PEABODY_DCG_CLOSEOUT_MANUSCRIPT_BUILD_PASS\n'
