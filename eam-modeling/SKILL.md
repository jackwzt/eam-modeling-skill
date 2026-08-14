---
name: eam-modeling
description: Inspect, design, fit, diagnose, compare, and report evidence-accumulation analyses for choice and response-time data using R/EMC2 or BayesFlow simulation-based inference. Use for WDM, DDM, LBA, RDM, LNR, hierarchical and between-subject EAMs, dynamic trial-by-trial EAMs, reinforcement-learning EAMs, amortized EAM inference, stop-signal models, continuous judgments, joint cognitive/EEG models, SEM-linked or causal analyses, EMC2/BayesFlow convergence and calibration troubleshooting, and CSV/XLSX/RDS/RData datasets containing choices, RTs, rewards, conditions, or participant identifiers.
---

# EAM Modeling

Build reproducible cognitive-model analyses while keeping theory, data coding, estimation, and predictive adequacy separate and auditable.

## Route the request

Classify the task before acting:

- **Explain or review:** inspect the supplied code, model object, output, or course example; do not refit unless asked.
- **Audit data:** run the data audit and return a mapping plus blocking issues.
- **Build an analysis:** create an analysis directory, configuration, executable R script, and report skeleton.
- **Fit models:** run environment and data gates, then prior checks, pilot sampling, full sampling, diagnostics, and posterior prediction.
- **Amortized/SBI EAM:** validate the simulator, route structured observations through a BayesFlow adapter, train offline with validation, check recovery/calibration, then run real-data inference and simulator-based PPCs.
- **Causal EAM/SEM:** separate the cognitive measurement model from the causal estimand, confirm identification assumptions, propagate latent uncertainty, and calibrate causal language.
- **Diagnose a fit:** load the saved object, inspect convergence/efficiency and predictive fit, identify the cause, and change code only when asked.
- **Compare or report:** compare only models fit to the same observations and preprocessing; report absolute fit as well as relative preference.

## Load only the needed references

- Read [data-schema.md](references/data-schema.md) for every new dataset.
- Read [model-routing.md](references/model-routing.md) before choosing a likelihood or architecture.
- Read [emc2-workflow.md](references/emc2-workflow.md) for standard, hierarchical, between-subject, fitting, or diagnostic work.
- Read [rl-dynamic-workflow.md](references/rl-dynamic-workflow.md) for trial-varying covariates, custom kernels, learning, Q-values, or feedback.
- Read [advanced-models.md](references/advanced-models.md) for stop-signal, continuous-judgment, joint-model, fMRI, or SEM work.
- Read [reporting.md](references/reporting.md) before delivering an analysis or scientific interpretation.
- Read [course-map.md](references/course-map.md) only when locating a worked example or tracing the course source.
- Read [baygent-bayesian-gates.md](references/baygent-bayesian-gates.md) before any new fit, sensitivity analysis, or model comparison.
- Read [baygent-amortized-eam.md](references/baygent-amortized-eam.md) for BayesFlow, SBI, neural posterior estimation, simulator banks, adapters, recovery, calibration, or amortized inference.
- Read [baygent-causal-claims.md](references/baygent-causal-claims.md) when the user asks for causal, mediation, intervention, counterfactual, or structural claims.

## Execute the workflow

### 1. Preserve and orient

- Treat raw data and supplied fitted objects as immutable.
- Resolve the input file, current working directory, output directory, R executable, EMC2 version, and operating system.
- On Windows, locate `Rscript.exe` under `C:\Program Files\R` if it is not on `PATH`.
- Run `scripts/check_eam_environment.R` before building or fitting.

### 2. Audit the data

Run:

```powershell
& <Rscript.exe> <skill-dir>\scripts\inspect_eam_data.R `
  --input <data-file> `
  --output-dir <analysis-dir>\audit
```

Pass `--object <name>` when an `.RData` file contains multiple data frames. Pass `--rt-unit seconds` or `--rt-unit milliseconds` when units are known.

Inspect all generated files. Resolve at least:

- participant identifier;
- observed response and its factor ordering;
- response time and unit;
- stimulus/correct-response coding;
- trial ordering within participant;
- experimental factors and reference levels;
- reward, action/symbol, and feedback fields for RL-EAMs;
- missingness, impossible values, truncation/censoring, and trial exclusions.

Infer obvious mappings, but state them. Stop before fitting if response coding, RT units, trial order, or the scientific contrast is ambiguous.

### 3. Choose a theory-driven model set

- State the psychological processes each parameter is intended to represent.
- Match likelihood architecture to the task, not merely to software availability.
- Define a small candidate set that answers the question and exposes important alternatives.
- Keep preprocessing and observations identical across compared models.
- Do not select a final model solely from an information criterion.

### 4. Scaffold the analysis

Run:

```powershell
& <Rscript.exe> <skill-dir>\scripts\new_eam_analysis.R `
  --input <data-file> `
  --output-dir <analysis-dir> `
  --model-family hierarchical-lba
```

Edit the generated `analysis-config.R`; then create a task-specific R analysis script. Verify `sampled_pars()`, `mapped_pars()`, and `plot_design()` before sampling.

### 5. Validate priors and identifiability

- Specify priors on EMC2's sampling scale and inspect them after mapping to natural units.
- Enforce scale identification explicitly.
- Run prior-predictive simulation and reject impossible RT, accuracy, learning, or parameter trajectories.
- Use simulation/recovery when the design or custom parameter mapping is new.
- For BayesFlow EAMs, keep structured trial data out of flat condition vectors; use explicit adapters whenever constraints, masking, dtype conversion, or structural routing is needed.

### 6. Fit in stages

- Start with a short pilot fit to expose likelihood, coding, and sampler failures.
- Run the full fit only after the pilot is structurally sound.
- On Windows use `cores_for_chains`; do not use `cores_per_chain`.
- Save fitted objects without assignment: `save(fit, file = path)`. Do not write `fit <- save(...)`.
- Load with `load(path)` when the saved object name is known. Use `get(load(path))` only when deliberately capturing an unknown single object.
- Preserve seeds, package versions, formulas, constants, exclusions, and source-data hashes in the output.

### 7. Apply diagnostic gates

Do not interpret parameters until all relevant gates pass:

- chains are stationary and mixed;
- R-hat is acceptable for every inferential target;
- effective sample sizes are adequate;
- posterior correlations and boundary behavior are understood;
- participant-level pathologies are checked in hierarchical fits;
- posterior predictions reproduce the main choice and RT patterns.
- amortized estimators pass held-out recovery, calibration ECDF/coverage, contraction, and training-history checks before real-data inference.

Treat sampler convergence and model adequacy as separate questions. A converged bad model remains a bad model.

### 8. Criticize, compare, and report

- Plot defective densities or CDFs and targeted statistics by scientifically important conditions.
- Report persistent misfit, especially tails, errors, sparse cells, and speed–accuracy effects.
- Compare DIC/BPIC/marginal-deviance evidence only alongside predictive checks, identifiability, and theoretical interpretability.
- Distinguish coefficient scale from mapped natural scale.
- Label exploratory choices and avoid causal or clinical generalization beyond the design.

## Required output structure

For a new analysis, prefer:

```text
analysis-name/
├── audit/
├── config/
├── scripts/
├── fits/
├── diagnostics/
├── posterior-predictive/
├── tables/
├── figures/
├── logs/
└── report/
```

Return the following in the handoff:

- data mapping and exclusions;
- model formulas, contrasts, constants, and priors;
- convergence and efficiency status;
- posterior-predictive successes and failures;
- model-comparison result with limitations;
- paths to scripts, saved fits, and report;
- exact unresolved blockers or recommended next model.

## Hard guardrails

- Never alter raw data in place.
- Never silently convert milliseconds to seconds, reorder response levels, or collapse conditions.
- Never delete RT outliers solely because they are inconvenient; justify truncation/censoring from task and measurement facts.
- Never call a fit converged from one trace plot or a single summary statistic.
- Never claim psychological evidence from a parameter whose mapping was not verified.
- Never treat participant point estimates as error-free group data when a joint hierarchy is feasible.
- Never overwrite a supplied fit; create a new named version.
- Never launch a long fit when a precomputed course sample already answers an explanation-only request.
- Never use BayesFlow training loss alone as evidence that posterior inference is valid.
- Never flatten exchangeable or ordered EAM trials into a fixed condition vector merely to fit a neural network.
- Never make a causal claim from an EAM coefficient or model comparison without an identified causal design and explicit assumptions.
