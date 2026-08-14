# Advanced course models

## Stop-signal models

- Identify go, stop, response, signal-delay, and inhibition-outcome fields.
- State the race/independence assumptions and whether trigger failures are modeled.
- Preserve censored/no-response information rather than treating it as ordinary missingness.
- Check inhibition functions, go RT distributions, failed-stop RTs, and participant-level sparse cells.

## Continuous judgments

- Route to the CDM/PSDM examples when responses are continuous rather than discrete choices.
- Verify response support, boundary treatment, and likelihood assumptions.
- Compare predictive distributions over the continuous response and RT jointly when available.
- Use the course R Markdown examples as implementation references; do not mechanically reuse their priors or trimming.

## Joint cognitive models

- Fit cognitive and auxiliary outcomes jointly when the goal depends on their latent association.
- Prefer joint propagation of uncertainty to regressions on noisy posterior means.
- Compare joint, blocked, single, and two-step variants only after aligning their estimands.
- Inspect posterior correlations, cross-domain predictions, and sensitivity to covariance structure.

## SEM-linked analyses

- Define latent variables, indicators, structural paths, and cognitive parameters before estimation.
- Check measurement invariance and group coding when comparing populations.
- Distinguish a factor model of cognitive parameters from a joint likelihood that propagates trial-level uncertainty.
- Avoid clinical generalization from demonstration datasets.

