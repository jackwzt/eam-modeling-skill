# EMC2 compatibility and API routing

Use feature probes before writing code. The release number alone does not identify whether the dynamic/trend API is present.

## Audited upstream states

| Channel | Audited commit | Package field | Relevant API |
|---|---|---:|---|
| `ampl-psych/EMC2` `main` | `beab948d283cfff25139de7f1a2dae11839cfddd` | 3.5.0 | Core design, prior, fitting, checking, prediction, comparison, SBC, joint/group/SEM facilities |
| `ampl-psych/EMC2` `dev` | `b1e05438b1534eff3ac36e9f86806c9db6bb5be5` | 3.4.1 | Core API plus exported `make_kernel()`, `make_base()`, `make_trend()`, and `trend_help()` used by the Day 4 dynamic/RL tutorials |

Audit date: 2026-08-16. Recheck the repository and installed namespace when reproducing later.

## Route by capability

- Use the stable/core route for Days 1-3, ordinary hierarchical/group work, standard posterior prediction, comparison, and SBC.
- Require the dynamic API for Day 4 time-varying kernels, delta rules, and RL-EAM tutorials.
- Treat a package reporting version 3.4.1 as ambiguous: released 3.4.1 can lack the dynamic functions while the audited development branch with the same package field contains them.
- Do not source individual `R/` files into an installed release. Install a coherent branch/commit into a project-local library and record its commit.

Probe with:

```r
ns <- asNamespace("EMC2")
required <- c("design", "prior", "make_emc", "fit", "check")
dynamic <- c("make_kernel", "make_base", "make_trend")
vapply(c(required, dynamic), exists, logical(1), envir = ns, inherits = FALSE)
```

Run `scripts/check_eam_environment.R --require-api standard` or `--require-api dynamic` for a reproducible report and non-zero exit status on missing requirements.

## Installation isolation

Prefer `renv` or a dedicated `.libPaths()` entry. For the ordinary release, use the package source recommended by EMC2. For the dynamic tutorial, install the audited `dev` branch or a deliberately selected later commit after reviewing its API and tests. Do not replace a working global installation merely to reproduce one tutorial.

## Stable workflow checks

Before sampling, verify:

- `design()`, `group_design()`, `prior()`, `make_emc()`, `sampled_pars()`, `mapped_pars()`, and `plot_design()` exist and accept the intended arguments;
- observed response-factor order matches the boundary/accumulator convention;
- the `prior`/`prior_list` call matches installed help rather than relying on partial argument matching;
- `fit()` exposes both `cores_per_chain` and `cores_for_chains` when expected;
- prediction and comparison functions operate on the exact installed fit class.

On Windows, EMC2 rejects `cores_per_chain > 1`; use `cores_for_chains` for parallel chains and keep one core within each chain.

## Source and license

EMC2 is maintained at `https://github.com/ampl-psych/EMC2` and licensed GPL-3.0-or-later. Its package metadata credits Niek Stevenson, Michelle Donzallaz, Andrew Heathcote, and Steven Miletić as authors, with additional contributors listed in `DESCRIPTION`. This skill contains independently written procedural guidance and does not redistribute EMC2 source code.

For research use, cite Stevenson, Donzallaz, Innes, Forstmann, Matzke, and Heathcote (2026), `https://doi.org/10.3758/s13428-025-02869-y`, and report the installed EMC2 version or source commit.
