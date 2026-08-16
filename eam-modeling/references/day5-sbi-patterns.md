# MBNCS26 Day 5 SBI patterns

Use these as teaching patterns only. Read `provenance-and-credits.md` before adapting course-specific content.

## Amortized DMC workflow

`Day5-SBI/amortized-workflow.ipynb` contrasts raw trial input with hand-crafted CAF/CDF/delta summaries, trains ensembles, applies an amortizer to observations, and regenerates posterior predictions.

- Keep DMC parameters `A`, `tau`, `mu_c`, `mu_r`, `b`, and `sd_r` in a documented order.
- Make the congruency-dependent sign of `A` explicit.
- State milliseconds-versus-seconds conversions and set `tmax` beyond the analyzed RT range.
- Count non-boundary crossings, document retry/rejection behavior, and keep contamination consistent across training and PPC simulation.
- Credit Simon Schaefer and `simschaefer/amortized-dmc` when using the DMC implementation carried in the course repository.

## Neural model comparison

`Day5-SBI/compare-models.ipynb` compares three-choice LBA/LCA variants. Match observation formatting, trial counts, simulation budgets, parameter-support rationale, and preprocessing across candidates. Evaluate held-out model-recovery confusion matrices under the declared model prior before interpreting observed-data probabilities.

## NLE, NRE, and PyMC

`Day5-SBI/likelihood-estimation.ipynb` and `ratio-estimation.ipynb` demonstrate learned likelihoods/ratios, DDM examples, exchangeable aggregation, and PyMC composition. Match parameter order and support transforms exactly. Compare learned and analytic likelihoods or posteriors on a tractable benchmark before applying the wrapper to an intractable model.

## Superstatistics

Use `superstats-workflow.md` for the maintained `LuSchumacher/superstats` implementation. Distinguish static individual differences, deterministic trends, trial-wise state recursions, and stochastic time-varying parameter processes; they imply different latent objects and validation targets.

## Joint behavior and M/EEG

The Michael D. Nunez materials introduce joint behavioral-neural and single-trial integrative BayesFlow patterns.

- Define behavioral and neural observation blocks, shared and modality-specific latent parameters, scaling, missingness, and conditional-independence assumptions.
- Validate each observation block separately before the joint model.
- Compare joint, behavior-only, and neural-only recovery to show whether the neural block adds information.
- For derived code from `mdnunez/single_trial_nddm_compare`, preserve its GPL-3.0 source/license boundary and do not copy its code into this MIT skill.

## Compatibility

The audited Day 5 `uv.lock` uses Python 3.12-3.13, BayesFlow 2.0.12, JAX 0.11.0, Keras 3.15.1, NumPy 2.4.6, PyMC 6.2.0, and `ssm-simulators` 0.13.2. Treat the lockfile as the reproducibility target for the course notebooks, not as a universal environment for future projects.
