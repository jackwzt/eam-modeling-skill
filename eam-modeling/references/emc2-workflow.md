# EMC2 workflow

## Design construction

1. Load and recode data explicitly.
2. Define `matchfun` for race models.
3. Define contrasts for scientifically meaningful coefficients.
4. Build `design()` with formulas, constants, functions, and truncation/censoring.
5. Inspect `sampled_pars()`, `mapped_pars()`, and `plot_design()`.
6. Check that every observed cell maps to valid natural-scale parameters.

Typical hierarchical LBA pattern:

```r
des <- design(
  data = dat,
  model = LBA,
  matchfun = function(d) d$S == d$lR,
  formula = list(v ~ lM * condition, B ~ lR + condition,
                 A ~ 1, t0 ~ 1, sv ~ lM),
  constants = c(sv = log(1))
)
```

Treat this as a pattern, not a default answer. Confirm parameter names and scales against the installed EMC2 version.

## Hierarchical and group design

- Understand the subject design as the set of coefficients each participant has.
- Use `group_design()` to explain population means of existing subject coefficients.
- Remember that omitted group predictors do not remove hierarchical intercepts or variances.
- Interpret population means/regressions/covariance, not participant point estimates as error-free observations.

## Priors

- Specify means and uncertainty on the sampling scale.
- Map priors back to natural, condition-specific parameters before fitting.
- Check positive parameters on log scale and bounded parameters on their configured transform.
- Set one appropriate scale parameter constant where required.
- Inspect population variance and correlation priors separately in hierarchical models.
- Use prior-predictive simulation to detect impossible RTs, accuracy, or participant heterogeneity.

## Windows fitting

Use parallel chains:

```r
fit_obj <- fit(
  emc,
  cores_for_chains = 3,
  fileName = "fits/pilot.RData"
)
```

Do not use `cores_per_chain` on Windows. With three default chains, `cores_for_chains = 3` generally means three chains in parallel and one CPU core per chain.

## Saving and loading

```r
dir.create("fits", recursive = TRUE, showWarnings = FALSE)
save(fit_obj, file = "fits/model-v1.RData")

rm(fit_obj)
load("fits/model-v1.RData")
```

Never assign the result of `save()` back to the fit object. `save()` returns `NULL`.

## Diagnostic gate

Inspect at minimum:

- `check()` selections for population mean, variance, correlation, and participant effects;
- split-chain R-hat for every inferential target;
- effective sample sizes and autocorrelation;
- trace plots for worst and scientifically central parameters;
- prior-to-posterior contraction and boundary behavior;
- posterior correlation/sloppiness;
- mapped credible intervals;
- posterior-predictive defective CDF/density and targeted statistics.

If chains fail, identify whether the cause is coding, impossible likelihood cells, weak identification, prior geometry, scaling, multimodality, or insufficient sampling before extending iterations.

## Comparison

- Compare only commensurate fits.
- Treat DIC, BPIC, and marginal deviance as relative evidence, not proof of adequacy.
- Report effective complexity and prior sensitivity.
- Prefer conclusions stable across predictive checks and defensible model alternatives.

