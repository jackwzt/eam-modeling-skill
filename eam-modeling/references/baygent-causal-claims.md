# Causal claims with cognitive models

Adapted for EAM/SEM work from `Learning-Bayesian-Statistics/baygent-skills` at commit `aa940481ebb9fbd087b2fc41dba3af386b5bdb31` (MIT; see `baygent-license.md`). Apply only when the request asks whether a manipulation, cognitive parameter, intervention, or neural variable causes another quantity.

Before causal estimation or language:

1. State the estimand (for whom, which contrast/intervention, and over what period).
2. Draw or describe the causal graph, including unobserved common causes and explicit non-edges.
3. Separate the EAM measurement model from the causal structural model.
4. Confirm the identification assumptions with the user; a fitted latent-parameter association is not identification.
5. Propagate cognitive-parameter uncertainty jointly when possible; do not treat posterior means as error-free mediators or outcomes.
6. Run design-specific refutation or sensitivity checks (placebo/falsification, alternative adjustment, measurement-model sensitivity, prior sensitivity).
7. Calibrate language: causal only when identification and refutation are defensible; otherwise use “associated with,” “consistent with,” or descriptive language.

Pre-treatment timing alone does not make a covariate safe: the graph must show that adjustment blocks a backdoor path without opening a collider. Mediation is a distinct estimand with stronger assumptions, including no unmeasured mediator–outcome confounding and no unhandled treatment-induced confounding.

Model comparison establishes relative predictive adequacy among candidates, not a causal effect.
