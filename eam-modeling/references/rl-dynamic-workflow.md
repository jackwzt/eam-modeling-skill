# RL and dynamic EAM workflow

## Required sequence

1. Sort trials within participant, session, and block.
2. Define reset points and initial latent state/Q-values.
3. Identify chosen action and the symbol/action receiving each feedback value.
4. Recode reward/outcome to the scale required by the learning rule.
5. Define dynamic covariates and custom kernel recursion.
6. Map latent learning signals to EAM parameters and accumulators.
7. Simulate trajectories before fitting.
8. Verify generated choices, RTs, Q-values, and parameter paths.
9. Fit a reduced pilot, then the intended hierarchical model.
10. Check both behavioral predictions and latent trajectory plausibility.

## RL-EAM design questions

- Does drift depend on Q-value difference, chosen value, action-specific values, prediction error, or another signal?
- Is feedback factual, counterfactual, partial, or delayed?
- Are learning rates shared across outcome signs or conditions?
- Are unchosen actions updated?
- How are missing responses, omitted feedback, and block transitions handled?
- Which accumulator coding connects symbols/actions to latent responses?
- Are learning and decision parameters jointly identifiable from the trial schedule?

## Dynamic EAM questions

- Is variability structured by an observed covariate, latent state, time trend, or autoregression?
- Does the covariate affect drift, threshold, non-decision time, bias, or several parameters?
- Is the covariate exogenous, or is it generated from previous responses/outcomes?
- Does the likelihood evaluate trial order correctly?
- Are kernel parameters constrained to stable/plausible regions?

## Validation

- Plot several participant-level latent trajectories.
- Reconstruct the recursion independently on a small hand-checkable sequence.
- Test reset behavior at participant/session/block boundaries.
- Compare simulated and observed learning curves, choices, RT distributions, and switch behavior.
- Run recovery across realistic trial counts and parameter correlations before substantive interpretation.

