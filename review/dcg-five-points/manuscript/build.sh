#!/usr/bin/env bash
set -euo pipefail
HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$HERE"
pdflatex -interaction=nonstopmode -halt-on-error main_dcg_revision_checkpoint.tex >/dev/null
pdflatex -interaction=nonstopmode -halt-on-error main_dcg_revision_checkpoint.tex >/dev/null
rm -f main_dcg_revision_checkpoint.aux main_dcg_revision_checkpoint.log main_dcg_revision_checkpoint.out
printf 'PEABODY_DCG_REVISION_MANUSCRIPT_BUILD_PASS\n'
