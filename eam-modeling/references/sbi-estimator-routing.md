# SBI estimator and representation routing

Choose the estimator from the inferential object needed after training, not from whichever tutorial runs first.

| Goal | Default route | Required validation |
|---|---|---|
| Many repeated posterior queries | NPE / amortized posterior | recovery, SBC/coverage, contraction, PPC |
| Compose a learned likelihood with an explicit prior or PyMC model | NLE | learned-vs-analytic likelihood and posterior comparison on a tractable case |
| Learn evidence through density ratios | NRE | ratio calibration and posterior comparison on a tractable case |
| Choose among simulators | classifier/model-comparison workflow | held-out confusion matrix, balanced simulation design, declared model prior |
| Infer time-varying trajectories and transition parameters | Superstats or custom time-series NPE | trajectory recovery, per-step calibration, contraction, posterior resimulation |

## Observation representation

- Route exchangeable trial-level observations through a set encoder such as `SetTransformer` when conditional exchangeability is scientifically defensible.
- Route ordered dynamics, reinforcement learning, sequential dependence, and time-varying parameters through `TimeSeriesTransformer`, `TimeSeriesNetwork`, or the Superstats time-series workflow.
- Use fixed interpretable summaries such as CAF/CDF/delta functions, RT quantiles, accuracy, and condition counts when they are sufficient for the question and stable under variable trial counts.
- Preserve masks, retained-trial proportions, condition order, and actual trial counts. Never pad without a mask or flatten an ordered sequence into a fixed condition vector.
- Train on one observation and aggregate at inference only when the likelihood factorizes over observations and the wrapper implements that exact aggregation.

## Model-comparison semantics

- Declare the complete candidate set and the model prior before simulation.
- Hold trial counts, parameter-support rationale, observation formatting, preprocessing, and train/test separation constant across candidates.
- Evaluate model recovery before observed-data probabilities.
- Interpret classifier logits as log Bayes factors only under the assumptions implemented by the workflow; under a uniform model prior this relation is simpler, but it still requires calibration and a correctly specified candidate set.
- A preferred model can remain predictively inadequate. Report absolute PPC results alongside relative preference.

## PyMC composition

Match parameter names, ordering, support transforms, batching, and log-density conventions exactly. Validate NLE/NRE wrappers on an analytic likelihood or posterior before using NUTS on an intractable simulator. Separate failures of PyMC sampling from failures of the learned approximation.
