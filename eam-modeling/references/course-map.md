# MBNCS26 five-day source map

Use these materials to locate worked examples. Never treat a course default as a validated prior, exclusion rule, model, or software configuration for new data. Read `provenance-and-credits.md` before adapting course-specific content.

## Day 1: Bayesian and basic EAM foundations

- `Day1-BasicEAMs/1-EAMs.R`: core evidence-accumulation concepts and model setup.
- `2-Dual.R`: diffusion-model design, fitting, checking, and prediction.
- `3-Race.R`: LBA, RDM, and LNR race-model patterns.
- `4-BasicExercisesAnswers.R`: worked exercises.
- Use this day for WDM/DDM/LBA/RDM/LNR model construction, single-level fits, recovery, prediction, and introductory comparison.

## Day 2: hierarchy, group relations, and stopping

- `Day2-Hierarchical/1-HierarchicalFitting.R`: hierarchical design, mapped and non-mapped priors, fitting, and checks.
- `2-HierarchicalInference.R`: group-level inference and prediction.
- `3-BetweenSubject.Rmd`: participant predictors and within/between-subject interpretation.
- `stop signal lesson/`: stop-signal race-model code, slides, and precomputed examples.
- Use this day for population means, variances, correlations, group design, between-subject regression, and stop-signal assumptions.

## Day 3: theory expression and joint models

- `Day3-Expressing/ExpressingPsychologicalTheories.R`: explicit theory-to-parameter mappings.
- `continuous_judgments/`: CDM/PSDM single and hierarchical workflows.
- `joint_modelling/`: joint, blocked, single, and two-step cognitive-model comparisons.
- Use this day for custom theory mappings, circular/continuous judgments, joint models across tasks, and joint fMRI-related modeling concepts.

## Day 4: SEM, dynamics, RL, and architectures

- `Day-4/SEM/`: SEM-linked cognitive-model examples.
- `Day-4/dynamic_tutorial/`: deterministic trends, trial covariates, memory kernels, custom kernels, and dynamic EAM recovery.
- `Day-4/rl_eam_tutorial/`: delta-rule kernels, factual/counterfactual feedback, RL-DDM/RDM/ARD variants, and reset logic.
- `Day-4/Cognitive Architectures/`: cognitive-architecture and model-checking slides.
- Require the EMC2 dynamic API before running kernel/trend examples; see `emc2-compatibility.md`.

## Day 5: simulation-based inference

- `Day5-SBI/amortized-workflow.ipynb`: DMC amortized inference, learned versus hand-crafted summaries, ensembles, real-data inference, and PPCs.
- `compare-models.ipynb`: neural LBA/LCA model comparison.
- `likelihood-estimation.ipynb`: NLE and PyMC integration.
- `ratio-estimation.ipynb`: NRE, exchangeable aggregation, and PyMC wrappers.
- `dmc/` and `bmc/`: simulator/model-comparison helpers with separate upstream attribution.
- `Joint_Modeling_EEG/`: joint behavior/M/EEG concepts and single-trial BayesFlow demonstration.
- `single_trial_nddm_compare/`: separately licensed external workshop material; do not treat it as part of the unlicensed MBNCS repository.
- Use `superstats-workflow.md` for the maintained external Superstats implementation supplied for the superstatistics session.

## Upstream repositories

- MBNCS26: `https://github.com/niekstevenson/MBNCS26`
- EMC2: `https://github.com/ampl-psych/EMC2`
- Dynamic EAM tutorial: `https://github.com/StevenM1/dynamic_tutorial`
- RL-EAM tutorial: `https://github.com/StevenM1/rl_eam_tutorial`
- Superstats: `https://github.com/LuSchumacher/superstats`

Before copying an example, inspect the installed API, package lock, source license, target dataset, and intended estimand. Course scripts can target development APIs, contain platform-specific parallel settings, or encode experiment-specific assumptions.
