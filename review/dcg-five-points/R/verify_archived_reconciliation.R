#!/usr/bin/env Rscript
# Independent core companion to verify_archived_reconciliation.py.
# PREPARATION STATUS: not executed in the assembly environment (Rscript absent).
# Running this file locally produces its own result; no cross-language PASS is
# claimed until both programs have run. Requires jsonlite and gmp.
#
# Usage:
# Rscript verify_archived_reconciliation.R --root /path/to/confocal-repo \
#   --output /path/to/archived_reconciliation_R.json
#
# This is an ARCHIVE audit, not fresh Arb evaluation or an independent proof
# of analytic derivative enclosures. Exact rational downstream arithmetic trusts
# the archived Arb terminal terms. Decimal strings are historical diagnostics,
# never promoted to outward-rounded proof endpoints. This companion implements
# a documented subset of the Python audit, not its full check-count ledger.

main <- function() {
  args <- commandArgs(trailingOnly = TRUE)
  option <- function(flag) {
    hits <- which(args == flag)
    if (length(hits) != 1L || hits + 1L > length(args)) return(NULL)
    args[[hits + 1L]]
  }
  root <- option("--root")
  output <- option("--output")
  if (is.null(root) || is.null(output)) {
    cat("ARCHIVED_RECONCILIATION_R_CORE_AUDIT_FAIL\n")
    cat("Required: --root REPOSITORY_ROOT --output REPORT.json\n")
    return(2L)
  }
  missing <- c("jsonlite", "gmp")[!vapply(c("jsonlite", "gmp"),
    requireNamespace, logical(1), quietly = TRUE)]
  if (length(missing)) {
    cat("ARCHIVED_RECONCILIATION_R_CORE_AUDIT_FAIL\nMissing R packages:",
        paste(missing, collapse = ", "), "\n")
    cat('Install missing dependencies with install.packages(c("jsonlite", "gmp")).\n')
    dir.create(dirname(output), recursive = TRUE, showWarnings = FALSE)
    writeLines(paste0('{"classification":"ARCHIVED_RECONCILIATION_R_CORE_AUDIT_FAIL",',
      '"pass":false,"reason":"missing R dependencies: ',
      paste(missing, collapse = ", "), '"}'), output)
    return(2L)
  }

  checks <- list()
  errors <- list()
  seen_inputs <- character()
  counters <- list(authoritative_runs = 0L, reconstructed_slabs = 0L,
    authoritative_terminal_rectangles = 0L, endpoint_panels = 0L,
    refinement_rows = 0L)
  reconstructed <- list()
  ck <- function(label, value) {
    if (!is.null(checks[[label]])) stop("Duplicate check: ", label)
    checks[[label]] <<- isTRUE(value)
    invisible(isTRUE(value))
  }
  section <- function(label, fun) {
    tryCatch(fun(), error = function(e) {
      errors[[label]] <<- conditionMessage(e)
      ck(paste0(label, ": readable and well-formed inputs"), FALSE)
      invisible(NULL)
    })
  }
  need <- function(x, key) {
    value <- x[[key]]
    if (is.null(value) || length(value) == 0L) stop("Missing field: ", key)
    value
  }
  integer_control <- function(x) {
    text <- as.character(x)
    if (length(text) != 1L || !grepl("^[+-]?[0-9]+$", text))
      stop("Invalid integer control: ", paste(text, collapse = ","))
    value <- suppressWarnings(as.integer(text))
    if (is.na(value)) stop("Integer control out of range: ", text)
    value
  }
  # Mantissas and decimal digits enter GMP directly as strings. Only small
  # indices and exponents become native integers; proof endpoints never do.
  q <- function(text) {
    text <- trimws(as.character(text))
    if (length(text) != 1L) stop("Expected one rational string")
    if (grepl("^[+-]?[0-9]+/[0-9]+$", text)) {
      pieces <- strsplit(text, "/", fixed = TRUE)[[1L]]
      den <- gmp::as.bigz(pieces[[2L]])
      if (den == 0) stop("Zero rational denominator")
      return(gmp::as.bigq(gmp::as.bigz(pieces[[1L]]), den))
    }
    if (!grepl("^[+-]?[0-9]+(\\.[0-9]*)?([eE][+-]?[0-9]+)?$", text))
      stop("Invalid exact decimal/rational string: ", text)
    parts <- strsplit(tolower(text), "e", fixed = TRUE)[[1L]]
    exponent <- if (length(parts) == 2L) integer_control(parts[[2L]]) else 0L
    base <- parts[[1L]]
    dots <- strsplit(base, ".", fixed = TRUE)[[1L]]
    places <- if (length(dots) == 2L) nchar(dots[[2L]]) else 0L
    digits <- gsub(".", "", base, fixed = TRUE)
    value <- gmp::as.bigq(gmp::as.bigz(digits))
    power <- exponent - places
    if (power >= 0L) value * gmp::as.bigz(10)^power
    else value / gmp::as.bigz(10)^(-power)
  }
  Q0 <- q("0")
  Q1 <- q("1")
  rational <- function(n, d = 1L) q(paste0(n, "/", d))
  qmin <- function(xs) Reduce(function(a, b) if (a <= b) a else b, xs)
  qmax <- function(xs) Reduce(function(a, b) if (a >= b) a else b, xs)
  qsum <- function(xs) Reduce(`+`, xs, init = Q0)
  binary <- function(point) {
    mantissa <- gmp::as.bigq(gmp::as.bigz(as.character(need(point, "mantissa"))))
    exponent <- integer_control(need(point, "exponent"))
    if (exponent >= 0L) mantissa * gmp::as.bigz(2)^exponent
    else mantissa / gmp::as.bigz(2)^(-exponent)
  }
  bp <- function(row, prefix) lapply(c("lower", "upper"), function(side) {
    binary(list(mantissa = need(row, paste0(prefix, "_", side, "_mantissa")),
                exponent = need(row, paste0(prefix, "_", side, "_exponent"))))
  })
  plus <- function(a, b) list(a[[1L]] + b[[1L]], a[[2L]] + b[[2L]])
  times <- function(a, b) {
    products <- list(a[[1L]] * b[[1L]], a[[1L]] * b[[2L]],
                     a[[2L]] * b[[1L]], a[[2L]] * b[[2L]])
    list(qmin(products), qmax(products))
  }
  contains <- function(a, b) isTRUE(a[[1L]] <= b[[1L]]) &&
    isTRUE(b[[1L]] <= b[[2L]]) && isTRUE(b[[2L]] <= a[[2L]])
  as_bool <- function(x) {
    text <- tolower(as.character(x))
    if (length(text) != 1L || !text %in% c("true", "false"))
      stop("Invalid Boolean")
    identical(text, "true")
  }
  track <- function(path) {
    if (!file.exists(path)) stop("Missing input: ", path)
    seen_inputs <<- unique(c(seen_inputs, path))
    path
  }
  doc <- function(path) jsonlite::fromJSON(track(path), simplifyVector = FALSE)
  rows <- function(path) read.csv(track(path), colClasses = "character",
    check.names = FALSE, stringsAsFactors = FALSE, na.strings = NULL)
  row_at <- function(df, i) as.list(df[i, , drop = FALSE])

  checkpoint <- file.path(root, "review", "dcg-five-points")
  arb <- file.path(checkpoint, "results", "arb")
  recon <- file.path(checkpoint, "results", "enclosure-reconciliation")
  names_runs <- c("forward_384", "forward_512", "reverse_384")
  for (run_index in seq_along(names_runs)) {
    run <- names_runs[[run_index]]
    section(run, function() {
      directory <- file.path(arb, run)
      cert <- doc(file.path(directory, "peabody_arb_concavity_certificate.json"))
      terminal <- rows(file.path(directory, "concavity_terminal_boxes.csv"))
      endpoint <- rows(file.path(directory, "endpoint_terminal_boxes.csv"))
      slab_summary <- rows(file.path(directory, "concavity_slab_summary.csv"))
      ck(paste(run, "certificate metadata"),
        isTRUE(cert$pass) && identical(cert$proof_status, "CERTIFIED") &&
        identical(cert$classification, "GO_PEABODY_ARB_FLINT_CERTIFICATE") &&
        identical(cert$certificate_version, "PEABODY_ARB_FLINT_CONCAVITY_V2") &&
        integer_control(cert$environment$precision_bits) == c(384L, 512L, 384L)[[run_index]] &&
        identical(cert$environment$python_flint_distribution, "0.9.0") &&
        identical(cert$subdivision_order, c("forward", "forward", "reverse")[[run_index]]))
      ck(paste(run, "exact binary publication targets"),
        identical(cert$endpoint$target, "1/4000") &&
        identical(cert$concavity$target, "-1/100000") &&
        binary(cert$endpoint$phi_one_enclosure$lower_binary) > rational(1, 4000) &&
        binary(cert$concavity$worst_phi_second_upper_binary) < -rational(1, 100000))
      expected_domains <- c("D2", "R2", "T2", "delta_denominator",
                           "angle_numerator", "angle_denominator", "Z")
      ck(paste(run, "exact binary domain positivity"),
        setequal(names(cert$domain_diagnostics), expected_domains) &&
        length(cert$domain_diagnostics) == 7L &&
        all(vapply(cert$domain_diagnostics, function(d) isTRUE(d$finite) &&
          isTRUE(d$strictly_positive) && binary(d$lower_binary) > Q0 &&
          binary(d$lower_binary) <= binary(d$upper_binary), logical(1))))
      ck(paste(run, "counts and correction sign"),
        nrow(terminal) == 320L && nrow(endpoint) == 4L && nrow(slab_summary) == 32L &&
        integer_control(cert$terminal_rectangles) == 324L &&
        integer_control(cert$correction_sign) == 1L)
      endpoint_geometry <- endpoint_terms <- TRUE
      for (j in seq_len(nrow(endpoint))) {
        r <- row_at(endpoint, j)
        endpoint_geometry <- endpoint_geometry &&
          integer_control(r$x_panel_index) == j - 1L &&
          q(r$x_lo) == rational(j - 1L, 4) && q(r$x_hi) == rational(j, 4)
        endpoint_terms <- endpoint_terms && contains(bp(r, "contribution"),
          plus(bp(r, "midpoint_term"), bp(r, "remainder_term")))
      }
      ck(paste(run, "exact endpoint coverage"), endpoint_geometry)
      ck(paste(run, "exact endpoint contribution containment"), endpoint_terms)
      uppers <- list()
      geometry_all <- terms_all <- TRUE
      for (i in 0:31) {
        indices <- vapply(terminal$q_slab_index, integer_control, integer(1))
        chunk <- terminal[indices == i, , drop = FALSE]
        chunk <- chunk[order(vapply(chunk$x_panel_index, integer_control, integer(1))), , drop = FALSE]
        geometry <- nrow(chunk) == 10L
        cm_parts <- cq_parts <- list()
        for (j in seq_len(nrow(chunk))) {
          r <- row_at(chunk, j)
          geometry <- geometry && q(r$q_lo) == rational(i, 32) &&
            q(r$q_hi) == rational(i + 1L, 32) && q(r$q_mid) == rational(2L * i + 1L, 64) &&
            integer_control(r$x_panel_index) == j - 1L &&
            q(r$x_lo) == rational(j - 1L, 10) && q(r$x_hi) == rational(j, 10)
          for (prefix in c("c_point", "cq")) {
            terms_all <- terms_all && contains(bp(r, paste0(prefix, "_contribution")),
              plus(bp(r, paste0(prefix, "_midpoint_term")),
                   bp(r, paste0(prefix, "_remainder_term"))))
          }
          cm_parts[[j]] <- bp(r, "c_point_contribution")
          cq_parts[[j]] <- bp(r, "cq_contribution")
        }
        geometry_all <- geometry_all && geometry
        if (!geometry) stop("Incomplete terminal coverage for slab ", i)
        cm <- lapply(1:2, function(s) qsum(lapply(cm_parts, `[[`, s)))
        cq <- lapply(1:2, function(s) qsum(lapply(cq_parts, `[[`, s)))
        c_interval <- plus(cm, times(list(-rational(1, 64), rational(1, 64)), cq))
        factor <- list((Q1 + rational(i, 32))^3 / q("32"),
                       (Q1 + rational(i + 1L, 32))^3 / q("32"))
        phi <- times(factor, c_interval)
        ck(paste(run, "exact reconstructed target slab", i),
           phi[[1L]] <= phi[[2L]] && phi[[2L]] < -rational(1, 100000))
        uppers[[i + 1L]] <- phi[[2L]]
        counters$reconstructed_slabs <<- counters$reconstructed_slabs + 1L
      }
      ck(paste(run, "all exact terminal domains"), geometry_all)
      ck(paste(run, "all exact terminal contribution containments"), terms_all)
      displayed_uppers <- lapply(slab_summary$phi_second_upper, q)
      ck(paste(run, "display-only slab summaries"),
        identical(unname(vapply(slab_summary$index, integer_control, integer(1))), 0:31) &&
        q(cert$concavity$worst_phi_second_upper) == qmax(displayed_uppers) &&
        all(vapply(displayed_uppers, function(x) x < -rational(1, 100000), logical(1))) &&
        all(vapply(slab_summary$below_negative_target, as_bool, logical(1))))
      reconstructed[[run]] <<- list(worst_upper_exact_fraction = as.character(qmax(uppers)))
      counters$authoritative_runs <<- counters$authoritative_runs + 1L
      counters$authoritative_terminal_rectangles <<- counters$authoritative_terminal_rectangles + nrow(terminal)
      counters$endpoint_panels <<- counters$endpoint_panels + nrow(endpoint)
    })
  }

  section("refinement diagnostics", function() {
    summary <- doc(file.path(recon, "enclosure_reconciliation.json"))
    runs <- rows(file.path(recon, "arb_refinement_runs.csv"))
    endpoints <- rows(file.path(recon, "endpoint_refinement_runs.csv"))
    ck("diagnostic run counts", nrow(runs) == 3L && nrow(endpoints) == 3L &&
       length(summary$arb$runs) == 3L && length(summary$arb$endpoint_runs) == 3L)
    configurations <- list(c(32L, 10L), c(64L, 20L), c(128L, 20L))
    worst_uppers <- list()
    for (j in 1:3) {
      n <- configurations[[j]][[1L]]
      m <- configurations[[j]][[2L]]
      ss <- rows(file.path(recon, paste0("arb_slabs_", n, "x", m, ".csv")))
      ck(paste("diagnostic", n, "row count"), nrow(ss) == n)
      lo <- hi <- list()
      for (k in seq_len(nrow(ss))) {
        r <- row_at(ss, k)
        lo[[k]] <- q(r$lower)
        hi[[k]] <- q(r$upper)
        ck(paste("diagnostic", n, "row", k - 1L),
          integer_control(r$index) == k - 1L && q(r$q_lo) == rational(k - 1L, n) &&
          q(r$q_hi) == rational(k, n) && lo[[k]] <= hi[[k]] &&
          hi[[k]] < -rational(1, 100000))
        counters$refinement_rows <<- counters$refinement_rows + 1L
      }
      worst <- qmax(hi)
      worst_index <- which(vapply(hi, function(x) x == worst, logical(1)))[[1L]]
      run <- row_at(runs, j)
      ck(paste("diagnostic", n, "summary extrema"),
        integer_control(run$q_slabs) == n && integer_control(run$x_panels) == m &&
        integer_control(run$bits) == 384L && integer_control(run$terminal_rectangles) == n * m &&
        integer_control(run$worst_slab_index) == worst_index - 1L &&
        q(run$worst_phi_second_lower) == lo[[worst_index]] &&
        q(run$worst_phi_second_upper) == worst &&
        as_bool(run$proves_strict_concavity) && as_bool(run$proves_target_minus_1_over_100000))
      json_run <- summary$arb$runs[[j]]
      ck(paste("diagnostic", n, "JSON CSV core agreement"),
        integer_control(json_run$q_slabs) == n && integer_control(json_run$x_panels) == m &&
        q(json_run$worst_phi_second_lower) == q(run$worst_phi_second_lower) &&
        q(json_run$worst_phi_second_upper) == q(run$worst_phi_second_upper))
      worst_uppers[[j]] <- worst
    }
    ck("display-only worst uppers strictly tighten", worst_uppers[[2L]] < worst_uppers[[1L]] &&
       worst_uppers[[3L]] < worst_uppers[[2L]] &&
       isTRUE(summary$arb$worst_upper_tightens_monotonically))
    endpoint_intervals <- list()
    for (j in 1:3) {
      r <- row_at(endpoints, j)
      bounds <- list(q(r$lower), q(r$upper))
      ck(paste("display-only endpoint", j, "target width and configuration"),
        integer_control(r$x_panels) == c(4L, 8L, 16L)[[j]] && integer_control(r$bits) == 384L &&
        bounds[[2L]] > bounds[[1L]] && bounds[[1L]] > rational(1, 4000) &&
        q(r$width) == bounds[[2L]] - bounds[[1L]] &&
        as_bool(r$proves_phi_one_positive) && as_bool(r$proves_phi_one_gt_1_over_4000))
      json_endpoint <- summary$arb$endpoint_runs[[j]]
      ck(paste("display-only endpoint", j, "JSON CSV core agreement"),
        q(json_endpoint$lower) == bounds[[1L]] && q(json_endpoint$upper) == bounds[[2L]] &&
        integer_control(json_endpoint$x_panels) == integer_control(r$x_panels))
      endpoint_intervals[[j]] <- bounds
    }
    ck("display-only endpoint intervals nested", contains(endpoint_intervals[[1L]], endpoint_intervals[[2L]]) &&
       contains(endpoint_intervals[[2L]], endpoint_intervals[[3L]]))
  })
  ck("all planned core records examined", counters$authoritative_runs == 3L &&
    counters$reconstructed_slabs == 96L && counters$authoritative_terminal_rectangles == 960L &&
    counters$endpoint_panels == 12L && counters$refinement_rows == 224L)
  passed <- length(checks) > 0L && all(vapply(checks, isTRUE, logical(1))) && length(errors) == 0L
  classification <- if (passed) "ARCHIVED_RECONCILIATION_R_CORE_AUDIT_PASS" else
    "ARCHIVED_RECONCILIATION_R_CORE_AUDIT_FAIL"
  report <- list(classification = classification, pass = passed, checks_count = length(checks),
    scope = "Core archive audit only; no fresh Arb, MPFR, special-function, or geometric proof replay.",
    runtime_status = "Executed by this R invocation; compare with Python before claiming language agreement.",
    implementation = list(R = R.version.string, jsonlite = as.character(utils::packageVersion("jsonlite")),
                          gmp = as.character(utils::packageVersion("gmp"))),
    trust_boundary = paste("GMP exact rational reconstruction trusts archived Arb terminal terms as",
                           "enclosures. It checks downstream arithmetic, coverage and conservative targets."),
    decimal_comparisons = "Exact comparisons of display strings for diagnostic consistency only; not outward-rounded proof enclosures.",
    not_implemented_from_python = c("SHA-256 manifest verification", "32 MPFR/legacy aggregate comparisons",
      "baseline-difference report checks", "adversarial-control artifact checks"),
    counters = counters, publication_bounds = list(endpoint_lower = "1/4000", concavity_upper = "-1/100000"),
    input_files = seen_inputs, reconstructed_concavity = reconstructed, checks = checks,
    failures = names(checks)[!vapply(checks, isTRUE, logical(1))], input_errors = errors)
  dir.create(dirname(output), recursive = TRUE, showWarnings = FALSE)
  jsonlite::write_json(report, output, pretty = TRUE, auto_unbox = TRUE, null = "null")
  cat(classification, "\nChecks:", length(checks), " Failures:", length(report$failures), "\n")
  if (length(report$failures)) cat(paste(report$failures, collapse = "\n"), "\n")
  if (length(errors)) for (label in names(errors)) cat(label, ": ", errors[[label]], "\n", sep = "")
  if (passed) 0L else 2L
}

status <- tryCatch(main(), error = function(e) {
  cat("ARCHIVED_RECONCILIATION_R_CORE_AUDIT_FAIL\n", conditionMessage(e), "\n")
  2L
})
if (!interactive()) quit(save = "no", status = status)
