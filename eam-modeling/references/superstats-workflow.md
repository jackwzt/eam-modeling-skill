# Superstats workflow for time-varying SBI

Use this route when the scientific target includes latent parameter trajectories and the parameters governing their evolution. Use ordinary EMC2 for static/hierarchical likelihood-based EAMs, and use the EMC2 dynamic route when the intended model is specifically expressed by its kernel/trend machinery.

## Audited upstream

- Repository: `https://github.com/LuSchumacher/superstats`
- Main commit: `00b40acd97e6eb2b0f5c0e1c933afd69cd9dcd40`
- Package version: 0.0.2
- License: MIT, copyright 2026 Lukas Schumacher
- Python: 3.12-3.13
- Key dependencies: BayesFlow 2.0.12 and NumPy 2.4.x; current metadata selects PyTorch on Windows and JAX on Linux/macOS.

Audit date: 2026-08-16. Verify current signatures before adapting code.

For research use, cite Schumacher et al. (2023), `https://doi.org/10.1038/s41598-023-40278-3`. For validation and comparison of non-stationary cognitive models, also cite Schumacher et al. (2025), `https://doi.org/10.1007/s42113-024-00218-4`. Check the upstream repository for newer citation guidance.

## Generative decomposition

Define the observation model and transition model separately:

- local parameters: time-varying trajectories;
- hyper parameters: time-invariant parameters governing transitions;
- shared parameters: time-invariant observation-model parameters;
- fixed parameters: constants excluded from posterior inference.

Use `JointPrior` to assign a transition, prior, or fixed value to every simulator argument. The simulator must return a non-empty dictionary of named observation arrays and must preserve the time axis.

Available transition families in the audited main branch include random walks, autoregression, Lévy flights, Ornstein-Uhlenbeck processes, jumps, mixtures, Gaussian processes, linear trends, and polynomial trends. Choose transition structure as a substantive prior, not an automatic flexibility upgrade.

## Current API pattern

1. Construct `superstats.JointPrior` with `superstats.Prior` and `superstats.transition.*` objects.
2. Wrap the named simulator in `superstats.GenerativeModel`; specify missingness and contamination deliberately.
3. Inspect trajectory priors and the observation prior push-forward.
4. Construct `superstats.Workflow`, using an explicit adapter only when the default time-series routing is insufficient.
5. Simulate fixed training and validation banks and call `fit_offline(data=..., validation_data=...)` first.
6. Inspect `plot_history()` and checkpoint/history persistence.
7. Optionally refine with `fit_online(num_steps=...)` after a healthy offline run.
8. On fresh simulations, call `sample()` and assess `verify_time_varying()` plus `verify_time_invariant()`.
9. Convert long observed data with `df_to_dict()` only after confirming dataset IDs, time order, mapping, padding, and missing sentinels.
10. Draw the real-data posterior and run `resimulate_posterior()` for PPCs.

## Validation gates

- Confirm the simulator signature matches every `JointPrior` key and default.
- Test vectorized shapes for multiple batch sizes and sequence lengths.
- Verify seed handling for the prior, observation simulator, missingness, and contamination.
- Check prior trajectories and push-forward observations before training.
- Evaluate full-trajectory recovery, time-point recovery, calibration error/coverage by time, posterior contraction, and transition-hyperparameter recovery.
- Inspect early, middle, and late time points; aggregate metrics can hide boundary failures.
- Compare posterior-resimulated RT/choice trajectories and task-specific sequential summaries with observations.
- Test sensitivity to transition family, bounds, missingness, contamination, sequence length, and smoothing used only for visualization.

Do not interpret smooth posterior trajectories as evidence for a smooth psychological process when smoothness was imposed by the transition prior.

## uv environment

Create a separate project environment rather than modifying the Day 5 course lock in place:

```powershell
uv init --python 3.12
uv add "superstats==0.0.2"
uv sync
uv run python <script.py>
```

On Windows, expect the package metadata to install PyTorch; on Linux/macOS, expect JAX. Record the active Keras/BayesFlow backend. Do not assume that merely having both JAX and PyTorch installed selects the intended backend.
