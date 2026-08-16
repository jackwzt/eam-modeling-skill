#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
value_after <- function(flag, default = NULL) {
  hit <- which(args == flag)
  if (!length(hit) || hit[length(hit)] == length(args)) return(default)
  args[hit[length(hit)] + 1L]
}

input <- value_after("--input", NULL)
output_dir <- value_after("--output-dir", NULL)
object_name <- value_after("--object", NULL)
rt_unit_arg <- tolower(value_after("--rt-unit", "auto"))

if (is.null(input) || is.null(output_dir)) {
  stop("Usage: inspect_eam_data.R --input <file> --output-dir <dir> [--object <name>] [--rt-unit auto|seconds|milliseconds]", call. = FALSE)
}
if (!file.exists(input)) stop("Input file does not exist: ", input, call. = FALSE)
if (!rt_unit_arg %in% c("auto", "seconds", "milliseconds")) {
  stop("--rt-unit must be auto, seconds, or milliseconds", call. = FALSE)
}

read_input <- function(path, object_name = NULL) {
  ext <- tolower(tools::file_ext(path))
  if (ext == "csv") return(list(data = utils::read.csv(path, check.names = FALSE), object = basename(path)))
  if (ext %in% c("tsv", "txt")) return(list(data = utils::read.delim(path, check.names = FALSE), object = basename(path)))
  if (ext == "rds") return(list(data = readRDS(path), object = basename(path)))
  if (ext %in% c("xlsx", "xls")) {
    if (!requireNamespace("readxl", quietly = TRUE)) stop("Package 'readxl' is required for Excel files.", call. = FALSE)
    return(list(data = as.data.frame(readxl::read_excel(path)), object = basename(path)))
  }
  if (ext %in% c("rdata", "rda")) {
    env <- new.env(parent = emptyenv())
    loaded <- load(path, envir = env)
    if (!is.null(object_name)) {
      if (!object_name %in% loaded) stop("Object not found in RData: ", object_name, call. = FALSE)
      return(list(data = env[[object_name]], object = object_name, available = loaded))
    }
    candidates <- loaded[vapply(loaded, function(nm) is.data.frame(env[[nm]]) || is.matrix(env[[nm]]), logical(1))]
    if (!length(candidates)) stop("No data.frame or matrix found in RData. Available: ", paste(loaded, collapse = ", "), call. = FALSE)
    sizes <- vapply(candidates, function(nm) NROW(env[[nm]]), numeric(1))
    chosen <- candidates[which.max(sizes)]
    return(list(data = env[[chosen]], object = chosen, available = loaded))
  }
  stop("Unsupported extension: ", ext, call. = FALSE)
}

loaded <- read_input(input, object_name)
dat <- as.data.frame(loaded$data, check.names = FALSE)
if (!nrow(dat) || !ncol(dat)) stop("Loaded object has zero rows or columns.", call. = FALSE)
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

normalize_name <- function(x) gsub("[^a-z0-9]+", "", tolower(x))
normalized <- normalize_name(names(dat))

roles <- list(
  subjects = c("subjects", "subject", "subjectid", "participant", "participantid", "subj", "subjid", "id"),
  response = c("r", "response", "resp", "choice", "keypress", "key"),
  rt = c("rt", "responsetime", "reactiontime", "latency"),
  stimulus = c("s", "stimulus", "stim", "target", "correctresponse", "correct"),
  trial = c("trial", "trialnumber", "trialindex", "t"),
  reward = c("reward", "outcome", "feedback", "payoff"),
  action_or_symbol = c("action", "symbol", "option", "choiceid", "stimulusid"),
  group = c("group", "diagnosis", "cohort")
)

infer_one <- function(candidates) {
  exact <- which(normalized %in% candidates)
  if (length(exact)) return(names(dat)[exact[1]])
  partial_candidates <- candidates[nchar(candidates) >= 3L]
  partial <- which(vapply(normalized, function(nm) any(startsWith(nm, partial_candidates)), logical(1)))
  if (length(partial)) names(dat)[partial[1]] else NA_character_
}

mapping <- data.frame(
  role = names(roles),
  suggested_column = vapply(roles, infer_one, character(1)),
  stringsAsFactors = FALSE
)
utils::write.csv(mapping, file.path(output_dir, "suggested-mapping.csv"), row.names = FALSE, na = "")

profile <- data.frame(
  column = names(dat),
  class = vapply(dat, function(x) paste(class(x), collapse = "/"), character(1)),
  missing_n = vapply(dat, function(x) sum(is.na(x)), integer(1)),
  missing_pct = round(vapply(dat, function(x) mean(is.na(x)) * 100, numeric(1)), 3),
  unique_n = vapply(dat, function(x) length(unique(x[!is.na(x)])), integer(1)),
  example = vapply(dat, function(x) paste(utils::head(unique(as.character(x[!is.na(x)])), 3), collapse = " | "), character(1)),
  stringsAsFactors = FALSE
)
utils::write.csv(profile, file.path(output_dir, "column-profile.csv"), row.names = FALSE, na = "")

mapped <- setNames(mapping$suggested_column, mapping$role)
subject_col <- unname(mapped[["subjects"]])
response_col <- unname(mapped[["response"]])
rt_col <- unname(mapped[["rt"]])

if (!is.na(subject_col)) {
  counts <- as.data.frame(table(dat[[subject_col]], useNA = "ifany"), stringsAsFactors = FALSE)
  names(counts) <- c("subject", "trials")
  utils::write.csv(counts, file.path(output_dir, "subject-trial-counts.csv"), row.names = FALSE)
}

excluded <- unique(na.omit(unname(mapped)))
condition_rows <- list()
for (nm in setdiff(names(dat), excluded)) {
  x <- dat[[nm]]
  n_unique <- length(unique(x[!is.na(x)]))
  if ((is.factor(x) || is.character(x) || is.logical(x)) && n_unique >= 2L && n_unique <= 20L) {
    tab <- as.data.frame(table(x, useNA = "ifany"), stringsAsFactors = FALSE)
    names(tab) <- c("level", "n")
    tab$column <- nm
    condition_rows[[length(condition_rows) + 1L]] <- tab[, c("column", "level", "n")]
  }
}
if (length(condition_rows)) {
  utils::write.csv(do.call(rbind, condition_rows), file.path(output_dir, "condition-levels.csv"), row.names = FALSE)
}

rt_lines <- "- RT column: not confidently identified."
if (!is.na(rt_col)) {
  rt_raw <- suppressWarnings(as.numeric(dat[[rt_col]]))
  finite <- rt_raw[is.finite(rt_raw)]
  if (length(finite)) {
    inferred_unit <- if (rt_unit_arg == "auto") {
      if (stats::median(finite, na.rm = TRUE) > 20) "milliseconds (provisional)" else "seconds (provisional)"
    } else rt_unit_arg
    divisor <- if (startsWith(inferred_unit, "millisecond")) 1000 else 1
    rt_sec <- finite / divisor
    qs <- stats::quantile(rt_sec, probs = c(0, .01, .1, .5, .9, .99, 1), na.rm = TRUE, names = TRUE)
    rt_lines <- c(
      paste0("- RT column: `", rt_col, "`"),
      paste0("- RT unit: ", inferred_unit),
      paste0("- RT finite values: ", length(finite)),
      paste0("- RT <= 0: ", sum(rt_sec <= 0)),
      paste0("- RT < 0.10 s: ", sum(rt_sec < .10)),
      paste0("- RT < 0.20 s: ", sum(rt_sec < .20)),
      paste0("- RT > 2 s: ", sum(rt_sec > 2)),
      paste0("- RT > 5 s: ", sum(rt_sec > 5)),
      paste0("- RT quantiles (s): `", paste(names(qs), round(qs, 4), sep = "=", collapse = ", "), "`")
    )
  }
}

response_lines <- "- Response column: not confidently identified."
if (!is.na(response_col)) {
  tab <- sort(table(dat[[response_col]], useNA = "ifany"), decreasing = TRUE)
  response_lines <- c(
    paste0("- Response column: `", response_col, "`"),
    paste0("- Response counts: `", paste(names(tab), as.integer(tab), sep = "=", collapse = ", "), "`")
  )
}

available_note <- if (!is.null(loaded$available)) paste(loaded$available, collapse = ", ") else loaded$object
lines <- c(
  "# EAM data audit",
  "",
  paste0("- Input: `", normalizePath(input, winslash = "/", mustWork = FALSE), "`"),
  paste0("- Loaded object: `", loaded$object, "`"),
  paste0("- Available/identified objects: `", available_note, "`"),
  paste0("- Rows: ", nrow(dat)),
  paste0("- Columns: ", ncol(dat)),
  paste0("- Rows identical across all supplied columns: ", sum(duplicated(dat)), " (not proof of duplicated trials without a unique trial key)"),
  paste0("- Cells missing: ", sum(is.na(dat)), " / ", nrow(dat) * ncol(dat)),
  "",
  "## Suggested mapping",
  "",
  paste0("- `", mapping$role, "`: `", ifelse(is.na(mapping$suggested_column), "UNRESOLVED", mapping$suggested_column), "`"),
  "",
  "## Response",
  "",
  response_lines,
  "",
  "## Response time",
  "",
  rt_lines,
  "",
  "## Required review",
  "",
  "- Confirm every suggested mapping; name similarity is not semantic proof.",
  "- Confirm RT units from task documentation.",
  "- Confirm response factor ordering and boundary/accumulator mapping.",
  "- Inspect participant-by-condition counts and task-specific exclusions.",
  "- For RL/dynamic models, verify trial order and reset boundaries before computing covariates."
)
writeLines(lines, file.path(output_dir, "data-audit.md"), useBytes = TRUE)
cat(normalizePath(file.path(output_dir, "data-audit.md"), winslash = "/", mustWork = FALSE), "\n")
