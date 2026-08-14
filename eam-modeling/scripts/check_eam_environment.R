#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
value_after <- function(flag, default = NULL) {
  hit <- which(args == flag)
  if (!length(hit) || hit[length(hit)] == length(args)) return(default)
  args[hit[length(hit)] + 1L]
}

output <- value_after("--output", NULL)
packages <- c(
  "EMC2", "coda", "data.table", "ggplot2", "readxl",
  "rmarkdown", "knitr", "Rcpp", "bookdown"
)
emc2_functions <- c(
  "design()" = "design",
  "group_design()" = "group_design",
  "prior()" = "prior",
  "make_emc()" = "make_emc",
  "fit()" = "fit",
  "check()" = "check",
  "predict() for emc" = "predict.emc",
  "mapped_pars()" = "mapped_pars",
  "sampled_pars()" = "sampled_pars",
  "make_base()" = "make_base",
  "make_kernel()" = "make_kernel"
)

lines <- c(
  "# EAM environment check",
  "",
  paste0("- Timestamp: `", format(Sys.time(), tz = "UTC"), " UTC`"),
  paste0("- R: `", R.version.string, "`"),
  paste0("- Platform: `", R.version$platform, "`"),
  paste0("- OS: `", Sys.info()[["sysname"]], " ", Sys.info()[["release"]], "`"),
  paste0("- Working directory: `", normalizePath(getwd(), winslash = "/", mustWork = FALSE), "`"),
  "",
  "## Packages",
  "",
  "| Package | Installed | Version |",
  "|---|---:|---|"
)

for (pkg in packages) {
  installed <- requireNamespace(pkg, quietly = TRUE)
  version <- if (installed) as.character(utils::packageVersion(pkg)) else "—"
  lines <- c(lines, sprintf("| %s | %s | %s |", pkg, if (installed) "yes" else "no", version))
}

if (requireNamespace("EMC2", quietly = TRUE)) {
  ns <- asNamespace("EMC2")
  lines <- c(
    lines,
    "",
    "## EMC2 API surface",
    "",
    "| Function | Available in namespace |",
    "|---|---:|"
  )
  for (label in names(emc2_functions)) {
    fn <- unname(emc2_functions[[label]])
    lines <- c(lines, sprintf("| `%s` | %s |", label, if (exists(fn, envir = ns, inherits = FALSE)) "yes" else "no"))
  }
  if (!exists("make_base", envir = ns, inherits = FALSE) || !exists("make_kernel", envir = ns, inherits = FALSE)) {
    lines <- c(
      lines,
      "",
      "WARNING: dynamic/RL tutorial APIs are incomplete in this EMC2 installation. Pin or upgrade to the tutorial-compatible version before reproducing those models."
    )
  }
}

lines <- c(
  lines,
  "",
  "## Parallel guidance",
  "",
  if (.Platform$OS.type == "windows") {
    "Windows detected: use `cores_for_chains`; do not use `cores_per_chain`."
  } else {
    "Non-Windows platform detected: verify both chain-level and within-chain options against the installed EMC2 version."
  },
  "",
  if (requireNamespace("EMC2", quietly = TRUE)) {
    "EMC2 is available. Confirm function arguments with the installed help before launching a long fit."
  } else {
    "BLOCKER: EMC2 is not installed in this R library. Do not attempt fitting until the intended package version is installed."
  }
)

if (is.null(output)) {
  cat(paste(lines, collapse = "\n"), "\n")
} else {
  dir.create(dirname(output), recursive = TRUE, showWarnings = FALSE)
  writeLines(lines, output, useBytes = TRUE)
  cat(normalizePath(output, winslash = "/", mustWork = FALSE), "\n")
}
