# Reporting standard

## Required sections

1. Scientific question and estimands
2. Data provenance and inclusion/exclusion ledger
3. Response, RT, stimulus, participant, condition, and trial mapping
4. Model architecture, formulas, contrasts, constants, and transforms
5. Prior rationale and prior-predictive results
6. Sampling configuration and software versions
7. Convergence and efficiency diagnostics
8. Posterior-predictive assessment
9. Mapped parameter estimates and uncertainty
10. Hypothesis tests or model comparison
11. Sensitivity analyses and limitations
12. Reproducibility paths and saved-object names

## Claim discipline

- Say “the fitted model estimates” rather than treating latent parameters as directly observed.
- Separate coefficient-scale results from mapped natural-scale quantities.
- Report uncertainty and model misfit near every substantive conclusion.
- Distinguish evidence for an effect, evidence for a null, and inconclusive evidence.
- Do not describe the preferred candidate as true or adequate solely because it wins comparison.
- Treat group/clinical findings as dataset- and model-conditional.

## Handoff table

Include a compact table with:

| Item | Status | Evidence/path |
|---|---|---|
| Data audit | pass/warn/block | audit report |
| Prior predictive | pass/warn/block | figure/table |
| Convergence | pass/warn/block | R-hat/ESS/trace output |
| Posterior predictive | pass/warn/block | condition-level plots |
| Model comparison | completed/not applicable | table |
| Main limitation | text | diagnostic or design fact |

