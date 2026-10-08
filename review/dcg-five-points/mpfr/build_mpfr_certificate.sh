#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
SRC="$ROOT/peabody_mpfr_concavity.c"
OUT="$ROOT/peabody_mpfr_concavity"
CC_BIN="${CC:-cc}"
HEADER_SOURCE=""

if command -v pkg-config >/dev/null 2>&1 && pkg-config --exists mpfr; then
  CFLAGS="$(pkg-config --cflags mpfr)"
  LIBS="$(pkg-config --libs mpfr)"
  HEADER_SOURCE="pkg-config"
elif command -v brew >/dev/null 2>&1 && [ -f "$(brew --prefix mpfr 2>/dev/null)/include/mpfr.h" ]; then
  MPFR_PREFIX="$(brew --prefix mpfr)"
  GMP_PREFIX="$(brew --prefix gmp)"
  CFLAGS="-I$MPFR_PREFIX/include -I$GMP_PREFIX/include"
  LIBS="-L$MPFR_PREFIX/lib -L$GMP_PREFIX/lib -lmpfr -lgmp"
  HEADER_SOURCE="homebrew"
elif [ -f /usr/include/mpfr.h ]; then
  CFLAGS=""
  LIBS="-lmpfr -lgmp"
  HEADER_SOURCE="/usr/include/mpfr.h"
else
  echo "STOP: official MPFR development header not found." >&2
  echo "On macOS run: brew install mpfr gmp pkg-config" >&2
  echo "On Debian/Ubuntu run: sudo apt-get install libmpfr-dev libgmp-dev pkg-config" >&2
  exit 2
fi

# Intentional word splitting for compiler and linker flags.
# shellcheck disable=SC2086
"$CC_BIN" -O2 -std=c11 -Wall -Wextra -pedantic $CFLAGS "$SRC" $LIBS -o "$OUT"

SMOKE="$ROOT/_build_smoke"
rm -rf "$SMOKE"
"$OUT" --output-dir "$SMOKE" --precision-bits 192 --q-slabs 32 >/dev/null
rm -rf "$SMOKE"

printf 'PEABODY_MPFR_BUILD_OFFICIAL_HEADER_PASS\n'
printf 'MPFR_HEADER_SOURCE=%s\n' "$HEADER_SOURCE"
printf 'COMPILER=%s\n' "$($CC_BIN --version 2>/dev/null | head -1)"
