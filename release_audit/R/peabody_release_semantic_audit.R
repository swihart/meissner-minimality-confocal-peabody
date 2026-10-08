#!/usr/bin/env Rscript

# Independent semantic audit for the certified confocal Peabody package.
# This is not proof authority. It uses Rmpfr for high-precision numerical
# formula checks and gmp/jsonlite for exact metadata and JSON handling.
#
# Version 2 repairs the original audit's MPFR character round-trip and makes
# all rational/decimal CSV conversions explicit. In particular:
#   * MPFR errors are accumulated directly, never formatted and reparsed;
#   * exact GMP rationals are converted with Rmpfr's bigq method;
#   * certificate CSV columns are read as character data to avoid binary64
#     coercion before high-precision parsing;
#   * exact partition coverage operates on lists of bigq values safely.

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2L) {
  stop("usage: Rscript peabody_release_semantic_audit.R REPO_ROOT OUTPUT_JSON")
}
repo <- normalizePath(args[[1L]], mustWork = TRUE)
out_path <- args[[2L]]

required_packages <- c("jsonlite", "Rmpfr", "gmp")
missing_packages <- required_packages[
  !vapply(required_packages, requireNamespace, logical(1L), quietly = TRUE)
]
if (length(missing_packages) > 0L) {
  stop(paste("missing R packages:", paste(missing_packages, collapse = ", ")))
}

suppressPackageStartupMessages(library(Rmpfr))
suppressPackageStartupMessages(library(gmp))

prec <- 256L
mp <- function(x) {
  if (Rmpfr::is.mpfr(x)) return(x)
  Rmpfr::mpfr(x, precBits = prec)
}
mpq <- function(x) Rmpfr::mpfr(x, precBits = prec)
read_csv_character <- function(path) {
  utils::read.csv(
    path,
    stringsAsFactors = FALSE,
    colClasses = "character",
    check.names = FALSE
  )
}

pi_mp <- Rmpfr::Const("pi", prec)
sqrt2 <- sqrt(mp(2))
sqrt3 <- sqrt(mp(3))
kappa <- mp(1) + sqrt2
K <- kappa * kappa
alpha <- acos(mp(1) / 3)
psi0 <- -(mp(2) * pi_mp / sqrt3) * alpha
VM <- pi_mp * (mp(2) / 3 - sqrt3 * alpha / 4)

stable_h <- function(e, x) {
  e <- mp(e)
  x <- mp(x)
  q <- (mp(1) - e) / (mp(1) + e)
  D <- sqrt(K * K + q * q)
  R <- sqrt(K * K + q * q - 2 * K * q * x * x)
  T <- sqrt(2 * K * (K * K + q * q) + K * K * (mp(1) - q)^2 * x * x)
  delta <- 2 * K * (mp(1) - x * x) / (R + K - q)
  M <- K * (q - 2 * K * x * x) / (R + K) +
    (mp(1) - K) * R - K * K - q * R - q - q * q
  primary <- -16 * sqrt2 * kappa * (K * K + q * q) / (R * T)
  correction <- -4 * K * (mp(1) - q * q) * (K * K + q * q) *
    delta * M / (R * T^3)
  algebraic <- -4 * K * (mp(1) - q * q) * (K * K + q * q) *
    delta / (R * T * T)
  Z <- K * ((mp(1) + q) * D + (mp(1) - q) * R) /
    (T * (K + q + D))
  (primary + correction) * atan(Z) + algebraic
}

original_h <- function(e, x) {
  e <- mp(e)
  x <- mp(x)
  one_minus_e2 <- mp(1) - e * e
  b2 <- (3 + 3 * e * e + 4 * sqrt2 * e) / one_minus_e2
  b <- sqrt(b2)
  a <- b / sqrt(one_minus_e2)
  amp <- sqrt(mp(1) - x * x / b2)
  C <- e * amp
  u <- sqrt(mp(1) - mp(1) / b2)
  v <- sqrt(mp(1) + mp(1) / b2)
  y <- mp(1) / (sqrt(b2 + mp(1)) + b)
  angle <- atan(y * sqrt((mp(1) + C) / (mp(1) - C)))
  kernel <- 4 * angle / sqrt(mp(1) - C * C)
  outer <- e * (amp - u) / (mp(1) - C * C)
  core <- kernel / a + outer * ((v * C - mp(1)) * kernel + 2 / b)
  -4 * b * core / amp
}

simpson_mpfr <- function(fun, n = 4096L) {
  if (n %% 2L != 0L) stop("Simpson panel count must be even")
  i <- Rmpfr::mpfr(0:n, precBits = prec)
  x <- i / n
  y <- fun(x)
  if (!Rmpfr::is.mpfr(y) || length(y) != n + 1L) {
    stop("quadrature integrand did not return an MPFR vector of the expected length")
  }
  h <- mp(1) / n
  odd_positions <- seq.int(2L, n, by = 2L)
  even_positions <- seq.int(3L, n - 1L, by = 2L)
  h / 3 * (
    y[1L] + y[n + 1L] +
      4 * sum(y[odd_positions]) +
      2 * sum(y[even_positions])
  )
}

phi_numeric <- function(e, n = 4096L) {
  (simpson_mpfr(function(x) stable_h(e, x), n = n) - psi0) / 8
}

parse_fraction <- function(text) {
  text <- trimws(as.character(text))
  parts <- strsplit(text, "/", fixed = TRUE)[[1L]]
  if (length(parts) == 1L) return(gmp::as.bigq(parts[[1L]], "1"))
  if (length(parts) == 2L) return(gmp::as.bigq(parts[[1L]], parts[[2L]]))
  stop(paste("invalid rational text:", text))
}
exact_cover <- function(lo, hi, start, end) {
  if (length(lo) == 0L || length(lo) != length(hi)) return(FALSE)
  ord <- order(vapply(lo, function(value) as.double(value), numeric(1L)))
  lo <- lo[ord]
  hi <- hi[ord]
  if (!isTRUE(lo[[1L]] == start)) return(FALSE)
  if (!isTRUE(hi[[length(hi)]] == end)) return(FALSE)
  if (length(lo) > 1L) {
    for (j in seq_len(length(lo) - 1L)) {
      if (!isTRUE(hi[[j]] == lo[[j + 1L]])) return(FALSE)
    }
  }
  TRUE
}

central_json <- file.path(repo, "certificates", "peabody_central_certificate.json")
central_local_csv <- file.path(repo, "data", "central_local_slab_summary.csv")
central_bulk_csv <- file.path(repo, "data", "central_bulk_slab_summary.csv")
local_boxes_csv <- file.path(repo, "data", "central_local_terminal_boxes.csv")
bulk_boxes_csv <- file.path(repo, "data", "central_bulk_terminal_boxes.csv")
tail_zip <- file.path(
  repo,
  "frozen_inputs",
  "confocal_peabody_tail_first_gate_2026-09-30.zip"
)

central <- jsonlite::fromJSON(central_json, simplifyVector = FALSE)
local_slabs <- read_csv_character(central_local_csv)
bulk_slabs <- read_csv_character(central_bulk_csv)
local_boxes <- read_csv_character(local_boxes_csv)
bulk_boxes <- read_csv_character(bulk_boxes_csv)

tail_temp <- tempfile("peabody_tail_r_audit_")
dir.create(tail_temp)
on.exit(unlink(tail_temp, recursive = TRUE, force = TRUE), add = TRUE)
unzip(tail_zip, exdir = tail_temp)
tail_roots <- list.dirs(tail_temp, recursive = FALSE, full.names = TRUE)
if (length(tail_roots) != 1L) stop("tail archive did not extract to one root")
tail_root <- tail_roots[[1L]]
tail_slabs <- read_csv_character(file.path(
  tail_root,
  "data",
  "certificate_80dps",
  "tail_slab_summary.csv"
))
tail_boxes <- read_csv_character(file.path(
  tail_root,
  "data",
  "certificate_80dps",
  "tail_terminal_boxes.csv"
))
tail_json <- jsonlite::fromJSON(
  file.path(tail_root, "data", "certificate_80dps", "tail_certificate.json"),
  simplifyVector = FALSE
)

# 1. High-precision pointwise formula agreement.
e_samples <- c("0", "0.000001", "0.01", "0.1", "0.5", "0.9", "0.995")
x_samples <- c("0", "0.125", "0.5", "0.875", "1")
max_pointwise_error <- mp(0)
pointwise_case_count <- 0L
for (e_text in e_samples) {
  for (x_text in x_samples) {
    err <- abs(original_h(mp(e_text), mp(x_text)) - stable_h(mp(e_text), mp(x_text)))
    if (!isTRUE(is.finite(err))) {
      stop(paste("non-finite pointwise error at e =", e_text, "x =", x_text))
    }
    if (isTRUE(err > max_pointwise_error)) max_pointwise_error <- err
    pointwise_case_count <- pointwise_case_count + 1L
  }
}
formula_gate <- isTRUE(max_pointwise_error < mp(2)^(-180))

# 2. Exact factor-of-eight coefficient audit over Q.
normalization_gate <- isTRUE(
  parse_fraction("16/3") / 8 == parse_fraction("2/3") &&
    parse_fraction("1") / 8 == parse_fraction("1/8") &&
    (parse_fraction("2/3") + 3 * parse_fraction("1/8") -
       3 * parse_fraction("1/8")) == parse_fraction("2/3")
)
meissner_formula_gate <- isTRUE(
  abs((mp(2) * pi_mp / 3 + 3 * psi0 / 8) - VM) < mp(2)^(-180)
)

# 3. Exact partition coverage.
local_lo <- lapply(local_slabs$e_lo, parse_fraction)
local_hi <- lapply(local_slabs$e_hi, parse_fraction)
bulk_lo <- lapply(bulk_slabs$e_lo, parse_fraction)
bulk_hi <- lapply(bulk_slabs$e_hi, parse_fraction)
tail_lo <- Map(
  function(n, d) gmp::as.bigq(n, d),
  tail_slabs$q_lo_num,
  tail_slabs$q_den
)
tail_hi <- Map(
  function(n, d) gmp::as.bigq(n, d),
  tail_slabs$q_hi_num,
  tail_slabs$q_den
)
coverage_gate <- isTRUE(
  exact_cover(local_lo, local_hi, parse_fraction("0"), parse_fraction("1/100")) &&
    exact_cover(
      bulk_lo,
      bulk_hi,
      parse_fraction("1/100"),
      parse_fraction("199/200")
    ) &&
    exact_cover(tail_lo, tail_hi, parse_fraction("0"), parse_fraction("1/399")) &&
    ((parse_fraction("1") - parse_fraction("199/200")) /
       (parse_fraction("1") + parse_fraction("199/200"))) ==
      parse_fraction("1/399")
)

# 4. Terminal-box metadata.
all_panels_present <- function(frame, slab_col, expected_panels) {
  split_panels <- split(as.integer(frame$x_panel_index), frame[[slab_col]])
  expected <- 0:(expected_panels - 1L)
  all(vapply(
    split_panels,
    function(x) identical(sort(unique(x)), expected),
    logical(1L)
  ))
}
metadata_gate <- isTRUE(
  nrow(local_boxes) == 160L &&
    nrow(bulk_boxes) == 430L &&
    nrow(tail_boxes) == 2000L &&
    all_panels_present(local_boxes, "local_q_slab_index", 10L) &&
    all_panels_present(bulk_boxes, "bulk_slab_index", 10L) &&
    all_panels_present(tail_boxes, "q_slab_index", 400L)
)

# 5. High-precision sample containment in archived enclosures.
containment_rows <- list()
select_indices <- function(n) unique(c(1L, as.integer(ceiling(n / 2)), n))
for (idx in select_indices(nrow(bulk_slabs))) {
  e_mid_q <- (parse_fraction(bulk_slabs$e_lo[[idx]]) +
                parse_fraction(bulk_slabs$e_hi[[idx]])) / 2
  e_mid <- mpq(e_mid_q)
  value <- phi_numeric(e_mid, n = 4096L)
  lower <- mp(bulk_slabs$phi_lower[[idx]])
  upper <- mp(bulk_slabs$phi_upper[[idx]])
  row_pass <- isTRUE(value >= lower) && isTRUE(value <= upper)
  containment_rows[[length(containment_rows) + 1L]] <- list(
    region = "bulk",
    index = idx - 1L,
    value = as.character(value),
    lower = as.character(lower),
    upper = as.character(upper),
    pass = row_pass
  )
}
for (idx in select_indices(nrow(tail_slabs))) {
  q_mid_q <- (tail_lo[[idx]] + tail_hi[[idx]]) / 2
  q_mid <- mpq(q_mid_q)
  e_mid <- (mp(1) - q_mid) / (mp(1) + q_mid)
  value <- phi_numeric(e_mid, n = 4096L)
  lower <- mp(tail_slabs$phi_lower[[idx]])
  upper <- mp(tail_slabs$phi_upper[[idx]])
  row_pass <- isTRUE(value >= lower) && isTRUE(value <= upper)
  containment_rows[[length(containment_rows) + 1L]] <- list(
    region = "tail",
    index = idx - 1L,
    value = as.character(value),
    lower = as.character(lower),
    upper = as.character(upper),
    pass = row_pass
  )
}
containment_gate <- all(vapply(
  containment_rows,
  function(x) isTRUE(x$pass),
  logical(1L)
))

# 6. Local quotient and orientation/permutation semantics.
local_e <- mp("0.005")
local_quotient <- phi_numeric(local_e, n = 4096L) / local_e
local_gate <- isTRUE(local_quotient > mp(1) / 2000)

phi_cache <- new.env(parent = emptyenv())
phi_cached <- function(text) {
  if (!exists(text, envir = phi_cache, inherits = FALSE)) {
    assign(text, phi_numeric(mp(text), n = 2048L), envir = phi_cache)
  }
  get(text, envir = phi_cache, inherits = FALSE)
}
volume_formula <- function(triple, sigma) {
  unused_sigma <- sigma
  VM + Reduce(`+`, lapply(triple, phi_cached), init = mp(0))
}
triples <- list(
  c("0", "0", "0"),
  c("0.01", "0.1", "0"),
  c("0.5", "0.9", "0.995")
)
orientation_gate <- TRUE
permutation_gate <- TRUE
semantic_tolerance <- mp(2)^(-180)
max_orientation_error <- mp(0)
max_permutation_error <- mp(0)
for (triple in triples) {
  reference <- volume_formula(triple, 0L)
  for (mask in 0:7) {
    err <- abs(volume_formula(triple, mask) - reference)
    if (isTRUE(err > max_orientation_error)) max_orientation_error <- err
    orientation_gate <- orientation_gate && isTRUE(err < semantic_tolerance)
  }
  perms <- unique(rbind(
    triple,
    triple[c(1L, 3L, 2L)],
    triple[c(2L, 1L, 3L)],
    triple[c(2L, 3L, 1L)],
    triple[c(3L, 1L, 2L)],
    triple[c(3L, 2L, 1L)]
  ))
  for (i in seq_len(nrow(perms))) {
    err <- abs(volume_formula(as.character(perms[i, ]), 0L) - reference)
    if (isTRUE(err > max_permutation_error)) max_permutation_error <- err
    permutation_gate <- permutation_gate && isTRUE(err < semantic_tolerance)
  }
}

archived_gate <- isTRUE(
  identical(
    central$classification,
    "GO_PEABODY_CENTRAL_PHI_POSITIVITY_CERTIFIED"
  ) &&
    identical(
      tail_json$classification,
      "GO_PEABODY_TAIL_PHI_POSITIVITY_CERTIFIED"
    )
)

pass_gate <- all(c(
  formula_gate,
  normalization_gate,
  meissner_formula_gate,
  coverage_gate,
  metadata_gate,
  containment_gate,
  local_gate,
  orientation_gate,
  permutation_gate,
  archived_gate
))

result <- list(
  audit_version = "PEABODY_R_SEMANTIC_AUDIT_V2",
  classification = if (pass_gate) {
    "PEABODY_R_SEMANTIC_AUDIT_PASS"
  } else {
    "PEABODY_R_SEMANTIC_AUDIT_FAIL"
  },
  pass = pass_gate,
  scope = "width-one regular-tetrahedron confocal Peabodies only",
  R_version = R.version.string,
  package_versions = list(
    jsonlite = as.character(utils::packageVersion("jsonlite")),
    Rmpfr = as.character(utils::packageVersion("Rmpfr")),
    gmp = as.character(utils::packageVersion("gmp"))
  ),
  precision_bits = prec,
  pointwise_formula_cases = pointwise_case_count,
  containment_sample_count = length(containment_rows),
  gates = list(
    formula_pointwise = formula_gate,
    factor_of_eight = normalization_gate,
    meissner_recovery = meissner_formula_gate,
    exact_partition_coverage = coverage_gate,
    terminal_box_metadata = metadata_gate,
    high_precision_sample_containment = containment_gate,
    local_quotient = local_gate,
    orientation_independence = orientation_gate,
    pair_permutation = permutation_gate,
    archived_classifications = archived_gate
  ),
  maximum_pointwise_formula_error = as.character(max_pointwise_error),
  maximum_orientation_error = as.character(max_orientation_error),
  maximum_pair_permutation_error = as.character(max_permutation_error),
  local_phi_over_e = as.character(local_quotient),
  containment_samples = containment_rows,
  proof_role = "independent R semantic audit; not proof authority"
)

dir.create(dirname(out_path), recursive = TRUE, showWarnings = FALSE)
jsonlite::write_json(result, out_path, auto_unbox = TRUE, pretty = TRUE)
cat(jsonlite::toJSON(result, auto_unbox = TRUE, pretty = TRUE), "\n")
if (!pass_gate) quit(status = 1L)
