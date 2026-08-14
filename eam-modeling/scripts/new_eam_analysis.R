#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
value_after <- function(flag, default = NULL) {
  hit <- which(args == flag)
  if (!length(hit) || hit[length(hit)] == length(args)) return(default)
  args[hit[length(hit)] + 1L]
}

input <- value_after("--input", NULL)
output_dir <- value_after("--output-dir", NULL)
model_family <- value_after("--model-family", "hierarchical-lba")

if (is.null(input) || is.null(output_dir)) {
  stop("Usage: new_eam_analysis.R --input <file> --output-dir <dir> [--model-family <name>]", call. = FALSE)
}

dirs <- c(
  "audit", "config", "scripts", "fits", "diagnostics",
  "posterior-predictive", "tables", "figures", "logs", "report"
)
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
for (d in dirs) dir.create(file.path(output_dir, d), recursive = TRUE, showWarnings = FALSE)

config_path <- file.path(output_dir, "config", "analysis-config.R")
if (file.exists(config_path)) {
  stop("Refusing to overwrite existing config: ", config_path, call. = FALSE)
}

q <- function(x) encodeString(normalizePath(x, winslash = "/", mustWork = FALSE), quote = '"')
config <- c(
  "# Review every value before fitting. NA means unresolved.",
  paste0("input_file <- ", q(input)),
  paste0("model_family <- ", encodeString(model_family, quote = '"')),
  "",
  "columns <- list(",
  "  subjects = NA_character_,",
  "  response = NA_character_,",
  "  rt = NA_character_,",
  "  stimulus = NA_character_,",
  "  trial = NA_character_,",
  "  condition = character(),",
  "  group = NA_character_,",
  "  reward = NA_character_,",
  "  action_or_symbol = NA_character_",
  ")",
  "",
  "rt_unit <- NA_character_  # 'seconds' or 'milliseconds'",
  "rt_bounds_seconds <- c(lower = NA_real_, upper = NA_real_)",
  "response_levels <- character()",
  "reference_levels <- list()",
  "",
  "subject_formula <- list()",
  "group_formula <- list()",
  "constants <- numeric()",
  "prior_notes <- character()",
  "",
  "n_chains <- 3L",
  "cores_for_chains <- 3L  # Windows: parallel chains, one core per chain",
  "seed <- 20260813L",
  "pilot_iterations <- 100L",
  "fit_file <- file.path('fits', paste0(model_family, '-v1.RData'))"
)
writeLines(config, config_path, useBytes = TRUE)

cat("Created analysis scaffold at:\n")
cat(normalizePath(output_dir, winslash = "/", mustWork = FALSE), "\n")
cat("Review config before fitting:\n")
cat(normalizePath(config_path, winslash = "/", mustWork = FALSE), "\n")

