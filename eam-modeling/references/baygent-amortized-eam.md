# Amortized BayesFlow workflow for EAM simulators

Adapted from `Learning-Bayesian-Statistics/baygent-skills` at commit `aa940481ebb9fbd087b2fc41dba3af386b5bdb31` (MIT; see `baygent-license.md`). Use this route when the user requests BayesFlow/SBI or an EAM likelihood is unavailable or too costly. For ordinary EMC2 fits, use `emc2-workflow.md`.

## Route EAM observations correctly

| EAM input | BayesFlow route | Default encoder |
|---|---|---|
| Trial-level RT, response, condition; exchangeable given parameters | `summary_variables` | `SetTransformer` |
| Ordered trial dynamics, learning, sequential dependence | `summary_variables` | `TimeSeriesTransformer` or `TimeSeriesNetwork` |
| Fixed handcrafted summaries (CAF/CDF/delta/quantiles) | `inference_conditions` | none |
| Fixed metadata such as trial count or design constants | `inference_conditions` | none |

Do not flatten trial sets or ordered sequences into one condition vector. A workflow may use structured `summary_variables` and fixed `inference_conditions` together.

## Adapter rules

- Prefer an explicit `bf.Adapter()` whenever shapes, dtypes, constraints, broadcasting, or concatenation need work.
- Do not combine explicit `adapter=` with `inference_variables=`, `summary_variables=`, or `inference_conditions=` shorthand.
- Apply structural transforms first, then parameter constraints, feature transforms, dtype conversion, and final concatenation/routing.
- Constrain positive EAM parameters and bounded probabilities before concatenating them into inference variables.
- Keep RT unit conversion, choice coding, masks, and condition order identical for simulations and observations.

## Pilot workflow

1. Validate the simulator, priors, units, non-boundary-crossing behavior, contaminant mechanism, and parameter ordering.
2. Start offline. Use roughly 20,000 pilot simulations for a fast simulator or 3,000–5,000 for a slow one, plus a held-out validation set (about 300) when compute permits.
3. Start with a base-size `FlowMatching` inference network and a modality-appropriate summary network. Increase capacity only after held-out recovery/calibration shows a need.
4. Generate batched simulations through `workflow.simulate(N)`; do not write a Python loop around the simulator.
5. Pass `validation_data=` to training. Save `history.history` as JSON.
6. Run `scripts/inspect_bayesflow_training.py` before inference.
7. On fresh held-out simulations, run `compute_default_diagnostics` and `plot_default_diagnostics`; save recovery, calibration ECDF, coverage, and contraction outputs.
8. Run `scripts/check_bayesflow_diagnostics.py` on saved metrics.
9. Infer real-data posteriors only after training and in-silico diagnostics pass.
10. For PPCs, pass posterior draws through the original EAM simulator and compare task-specific RT/choice summaries. Never reimplement the simulator for PPCs.

Use online training only as a refinement after a healthy offline pass. Use disk training when the simulation bank does not fit memory.

## Interpretation priorities

- Trust calibration before apparent posterior narrowness.
- Good recovery with poor calibration indicates an unreliable uncertainty approximation.
- Poor recovery with good calibration often indicates weak identification or insufficient summaries.
- High contraction plus poor calibration indicates overconfidence.
- Real data outside prior-predictive support requires a revised simulation design and retraining, not extrapolation.
