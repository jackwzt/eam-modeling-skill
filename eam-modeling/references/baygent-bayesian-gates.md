# Bayesian quality gates for EAMs

Adapted for EMC2/EAM work from `Learning-Bayesian-Statistics/baygent-skills` at commit `aa940481ebb9fbd087b2fc41dba3af386b5bdb31` (MIT; see `baygent-license.md`). EMC2 conventions override PyMC-specific advice.

## Required sequence

1. State the generative story and estimands.
2. Justify priors on the actual EMC2 sampling scale and inspect mapped natural-scale implications.
3. Run prior-predictive simulation; revise priors when simulated RT, accuracy, learning, or parameter paths are implausible.
4. Fit a pilot before the full run.
5. Check convergence and effective information before interpretation.
6. Criticize absolute fit using posterior predictions and task-specific summaries.
7. Test sensitivity to consequential priors, RT treatment, coding, and candidate-set assumptions.
8. Compare models only on identical observations and preprocessing.
9. Save fits immediately and produce a fixed-structure report with an audit trail.

For amortized inference, replace MCMC-only diagnostics with the applicable approximation gates: training stability, fresh held-out recovery, SBC/calibration/coverage, contraction, estimator/seed disagreement, and simulator-based PPCs. If NLE/NRE is sampled with PyMC, apply both approximation and MCMC gates.

## Diagnostic escalation

- Treat R-hat, ESS, chain mixing, autocorrelation, boundary behavior, and posterior correlation as a gate, not decoration.
- When convergence fails, change one rung at a time: inspect coding/likelihood failures; extend warmup or sampling; adjust EMC2 proposal/fit settings; simplify or reparameterize the hierarchy; isolate the problematic component; reconsider the architecture only with the user because that changes scientific meaning.
- If convergence is acceptable but posterior predictions fail, revise the model rather than sampling longer.
- If a parameter has high posterior correlation, weak recovery, or a prior-like posterior, report it as weakly identified. Do not rescue its interpretation with a narrow interval from another parameterization.

## Model criticism

Check at least:

- response probability/accuracy by condition and participant;
- correct and error RT distributions, quantiles, defective CDFs, and tails;
- speed–accuracy relationships and sparse error cells;
- trial-order, sequential, reward, or inhibition summaries when they are part of the theory;
- participant-level failures hidden by group averages;
- posterior predictive calibration and recovery for new/custom mappings.

Use model comparison as predictive evidence among candidates, not proof that a model is true. If comparison is close relative to uncertainty, prefer the simpler interpretable model or retain model uncertainty. A winning but predictively inadequate model is not ready for substantive interpretation.

## Sensitivity

Repeat or importance-reweight when feasible across scientifically consequential choices: group-level scale priors, correlation priors, contaminant/outlier treatment, RT cutoffs/censoring, response-factor order, reference levels, and hierarchical covariance structure. Document sensitivity rather than loosening priors only to silence a warning.
