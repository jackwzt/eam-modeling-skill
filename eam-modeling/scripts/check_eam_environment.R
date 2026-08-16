#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)

value_after <- function(flag, default = NULL) {
  hit <- which(args == flag)
  if (!length(hit) || hit[length(hit)] == length(args)) return(default)
  args[hit[length(hit)] + 1L]
}

output <- value_after("--output", NULL)
required_api <- tolower(value_after("--require-api", "none"))
if (!required_api %in% c("none", "standard", "dynamic")) {
  stop("--require-api must be one of: none, standard, dynamic", call. = FALSE)
}

packages <- c(
  "EMC2", "coda", "data.table", "ggplot2", "readxl",
  "rmarkdown", "knitr", "Rcpp", "bookdown", "renv", "remotes"
)

standard_functions <- c(
  "design", "group_design", "prior", "make_emc", "fit", "check",
  "mapped_pars", "sampled_pars", "plot_design"
)
dynamic_functions <- c("make_kernel", "make_base", "make_trend", "trend_help")
diagnostic_functions <- c("predict.emc", "summary.emc", "plot.emc")

lines <- c(
  "# EAM environment check",
  "",
  paste0("- Timestamp: `", format(Sys.time(), tz = "UTC"), " UTC`"),
  paste0("- R: `", R.version.string, "`"),
  paste0("- Platform: `", R.version$platform, "`"),
  paste0("- OS: `", Sys.info()[["sysname"]], " ", Sys.info()[["release"]], "`"),
  paste0("- Working directory: `", normalizePath(getwd(), winslash = "/", mustWork = FALSE), "`"),
  paste0("- Required API profile: `", required_api, "`"),
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

emc2_installed <- requireNamespace("EMC2", quietly = TRUE)
standard_ok <- FALSE
dynamic_ok <- FALSE

if (emc2_installed) {
  ns <- asNamespace("EMC2")
  exports <- getNamespaceExports("EMC2")
  all_functions <- c(standard_functions, dynamic_functions, diagnostic_functions)
  available <- vapply(all_functions, exists, logical(1), envir = ns, inherits = FALSE)
  exported <- all_functions %in% exports
  standard_ok <- all(available[standard_functions])
  dynamic_ok <- all(available[dynamic_functions] & exported[match(dynamic_functions, all_functions)])

  lines <- c(
    lines,
    "",
    "## EMC2 API surface",
    "",
    paste0("- Installed EMC2 version: `", as.character(utils::packageVersion("EMC2")), "`"),
    paste0("- Standard API complete: **", if (standard_ok) "yes" else "no", "**"),
    paste0("- Dynamic/trend API complete and exported: **", if (dynamic_ok) "yes" else "no", "**"),
    "",
    "| Function | Namespace | Exported |",
    "|---|---:|---:|"
  )
  for (fn in all_functions) {
    lines <- c(
      lines,
      sprintf(
        "| `%s()` | %s | %s |",
        fn,
        if (available[[fn]]) "yes" else "no",
        if (exported[match(fn, all_functions)]) "yes" else "no"
      )
    )
  }

  fit_method <- tryCatch(
    utils::getS3method("fit", "emc", optional = TRUE, envir = ns),
    error = function(e) NULL
  )
  if (!is.null(fit_method)) {
    fit_args <- names(formals(fit_method))
    lines <- c(
      lines,
      "",
      "## Fitting API",
      "",
      paste0("- `fit.emc()` arguments: `", paste(fit_args, collapse = ", "), "`"),
      paste0("- `cores_for_chains` present: **", if ("cores_for_chains" %in% fit_args) "yes" else "no", "**"),
      paste0("- `cores_per_chain` present: **", if ("cores_per_chain" %in% fit_args) "yes" else "no", "**")
    )
  }

  if (!dynamic_ok) {
    lines <- c(
      lines,
      "",
      "WARNING: the installed EMC2 namespace lacks the complete exported dynamic/trend API. Standard EAM work may still be available, but Day 4 `make_kernel()`/`make_base()`/`make_trend()` models require a coherent compatible development installation."
    )
  }
} else {
  lines <- c(lines, "", "BLOCKER: EMC2 is not installed in the active R library paths.")
}

lines <- c(
  lines,
  "",
  "## Parallel guidance",
  "",
  if (.Platform$OS.type == "windows") {
    "Windows detected: use exact argument `cores_for_chains`; keep `cores_per_chain = 1`."
  } else {
    "Non-Windows platform detected: verify chain-level and within-chain settings against installed `fit.emc()` formals."
  },
  "",
  "## Audited upstream channels",
  "",
  "- Stable/core reference: `ampl-psych/EMC2` main at `beab948d283cfff25139de7f1a2dae11839cfddd` (package field 3.5.0).",
  "- Dynamic/trend reference: `ampl-psych/EMC2` dev at `b1e05438b1534eff3ac36e9f86806c9db6bb5be5` (feature-probe the namespace; do not rely on the package field alone).",
  "- Prefer a project-local R library when switching channels."
)

if (is.null(output)) {
  cat(paste(lines, collapse = "\n"), "\n")
} else {
  dir.create(dirname(output), recursive = TRUE, showWarnings = FALSE)
  writeLines(lines, output, useBytes = TRUE)
  cat(normalizePath(output, winslash = "/", mustWork = FALSE), "\n")
}

requirements_ok <- switch(
  required_api,
  none = TRUE,
  standard = emc2_installed && standard_ok,
  dynamic = emc2_installed && standard_ok && dynamic_ok
)
if (!requirements_ok) quit(save = "no", status = 2L)
