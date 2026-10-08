#!/usr/bin/env Rscript

# Independent semantic audit for the Peabody analytical-compression package.
# This script is not proof authority.  It checks the stable q formula, endpoint
# simplification, certificate metadata, and sampled concavity/chord behavior
# using Rmpfr high-precision arithmetic and a separate composite midpoint rule.

suppressPackageStartupMessages({
  library(jsonlite)
  library(gmp)
  library(Rmpfr)
})

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2L) {
  stop("usage: peabody_analytic_compression_semantic_audit.R PACKAGE_DIR OUTPUT_JSON")
}
package_dir <- normalizePath(args[[1]], mustWork = TRUE)
output_json <- args[[2]]
prec <- 256L
mp <- function(x) mpfr(as.character(x), precBits = prec)

sqrt2 <- sqrt(mp(2))
kappa <- mp(1) + sqrt2
K <- kappa^2
pi_mp <- Const("pi", prec)
alpha <- acos(mp(1) / mp(3))
psi0 <- -(mp(2) * pi_mp / sqrt(mp(3))) * alpha

stable_h <- function(q, x) {
  q <- mpfr(q, precBits = prec)
  x <- mpfr(x, precBits = prec)
  D <- sqrt(K^2 + q^2)
  RR <- sqrt(K^2 + q^2 - mp(2) * K * q * x^2)
  TT <- sqrt(mp(2) * K * (K^2 + q^2) + K^2 * (mp(1) - q)^2 * x^2)
  delta <- mp(2) * K * (mp(1) - x^2) / (RR + K - q)
  MM <- K * (q - mp(2) * K * x^2) / (RR + K) + (mp(1) - K) * RR - K^2 - q * RR - q - q^2
  primary <- -mp(16) * sqrt2 * kappa * (K^2 + q^2) / (RR * TT)
  correction <- -mp(4) * K * (mp(1) - q^2) * (K^2 + q^2) * delta * MM / (RR * TT^3)
  algebraic <- -mp(4) * K * (mp(1) - q^2) * (K^2 + q^2) * delta / (RR * TT^2)
  Z <- K * ((mp(1) + q) * D + (mp(1) - q) * RR) / (TT * (K + q + D))
  (primary + correction) * atan(Z) + algebraic
}

endpoint_h <- function(x) {
  x <- mpfr(x, precBits = prec)
  A <- mp(2) * K + x^2
  coeff <- -mp(16) * sqrt2 * kappa / sqrt(A) + mp(4) * (mp(1) - x^2) * (A - mp(1)) / A^(mp(3) / mp(2))
  coeff * atan(mp(1) / sqrt(A)) - mp(4) * (mp(1) - x^2) / A
}

midpoint_integral <- function(fn, n) {
  total <- mp(0)
  for (i in 0:(n - 1L)) {
    x <- (mp(2 * i + 1L)) / mp(2L * n)
    total <- total + fn(x)
  }
  total / mp(n)
}

psi_q <- function(q, n = 2048L) midpoint_integral(function(x) stable_h(q, x), n)
phi_e <- function(e, n = 2048L) {
  e <- mpfr(e, precBits = prec)
  q <- (mp(1) - e) / (mp(1) + e)
  (psi_q(q, n) - psi0) / mp(8)
}

# Endpoint formula agreement.
endpoint_errors <- mp(0)
for (i in 0:20) {
  x <- mp(i) / mp(20)
  err <- abs(stable_h(mp(0), x) - endpoint_h(x))
  if (err > endpoint_errors) endpoint_errors <- err
}

phi_one <- (midpoint_integral(endpoint_h, 4096L) - psi0) / mp(8)
endpoint_pass <- phi_one > mp(3) / mp(10000)

# Sampled finite-difference concavity and chord checks.
sample_e <- c("0.1", "0.25", "0.5", "0.75", "0.9")
concavity_rows <- list()
concavity_pass <- TRUE
chord_pass <- TRUE
h <- mp("0.0005")
for (text in sample_e) {
  e <- mp(text)
  fm <- phi_e(e - h, 1024L)
  f0 <- phi_e(e, 1024L)
  fp <- phi_e(e + h, 1024L)
  second <- (fp - mp(2) * f0 + fm) / h^2
  c_ok <- second < -mp(1) / mp(25000)
  b_ok <- f0 > mp(3) * e / mp(10000)
  concavity_pass <- concavity_pass && c_ok
  chord_pass <- chord_pass && b_ok
  concavity_rows[[length(concavity_rows) + 1L]] <- list(
    e = as.character(e),
    phi = formatMpfr(f0, digits = 40),
    finite_difference_second = formatMpfr(second, digits = 30),
    concavity_sample_pass = c_ok,
    chord_sample_pass = b_ok
  )
}

cert_path <- file.path(package_dir, "data", "certificate_80dps", "peabody_concavity_certificate.json")
cert <- fromJSON(cert_path, simplifyVector = FALSE)
metadata_pass <- identical(cert$proof_status, "CERTIFIED") &&
  identical(as.integer(cert$terminal_boxes), 324L) &&
  identical(as.integer(cert$concavity$q_slabs), 32L) &&
  identical(as.integer(cert$concavity$x_panels_per_slab), 10L) &&
  isTRUE(cert$endpoint$exceeds_target) &&
  isTRUE(cert$concavity$all_slabs_below_target)

pass <- endpoint_errors < mp("1e-60") && endpoint_pass && concavity_pass && chord_pass && metadata_pass
result <- list(
  audit_version = "PEABODY_ANALYTIC_COMPRESSION_R_SEMANTIC_V1",
  classification = if (pass) "PEABODY_ANALYTIC_COMPRESSION_R_SEMANTIC_PASS" else "PEABODY_ANALYTIC_COMPRESSION_R_SEMANTIC_FAIL",
  pass = pass,
  proof_authority = FALSE,
  precision_bits = prec,
  endpoint_formula_max_error = formatMpfr(endpoint_errors, digits = 30),
  phi_one_midpoint_4096 = formatMpfr(phi_one, digits = 50),
  endpoint_target_pass = endpoint_pass,
  sampled_concavity_pass = concavity_pass,
  sampled_chord_pass = chord_pass,
  certificate_metadata_pass = metadata_pass,
  sampled_rows = concavity_rows
)
dir.create(dirname(output_json), recursive = TRUE, showWarnings = FALSE)
write_json(result, output_json, pretty = TRUE, auto_unbox = TRUE)
cat(toJSON(result, pretty = TRUE, auto_unbox = TRUE), "\n")
if (!pass) quit(status = 1L)
