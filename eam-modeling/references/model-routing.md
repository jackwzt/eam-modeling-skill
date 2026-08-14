# Model routing

## Choose the architecture

| Data/question | Start with | Important alternative or warning |
|---|---|---|
| Two-boundary choice and RT | WDM or reduced DDM | Add DDM trial variability only when justified and identifiable |
| One accumulator per response | LBA | Compare with RDM/LNR when architecture or computation matters |
| Need rate quality and overall urgency | LBA/RDM/LNR with match contrasts | Verify matching/mismatching rate identification when errors are rare |
| Multiple participants and population claims | Hierarchical EAM | Avoid two-step inference on noisy participant estimates |
| Participant predictors or groups | Subject design plus `group_design()` | Center/code predictors and distinguish beta from mapped cell values |
| Parameter changes across trials | Dynamic EAM | Preserve trial order and verify covariate/kernel recursion |
| Instrumental learning with rewards | RL-EAM | Define actions, feedback ownership, resets, and Q-value initialization |
| Stop trials and inhibition | Stop-signal race architecture | Go/stop dependence and trigger failures require explicit assumptions |
| Continuous judgments | CDM/PSDM course workflow | Do not force discrete-choice EAM conventions onto continuous responses |
| Cognitive parameters linked to other outcomes | Joint cognitive model or SEM | Propagate measurement uncertainty; avoid error-free two-step scores |

## Parameter-to-process discipline

For every free coefficient, record:

1. sampled name and scale;
2. formula term and reference level;
3. mapped trial/cell parameter;
4. proposed psychological interpretation;
5. manipulation or predictor expected to affect it;
6. identification constraints and plausible range;
7. observable patterns it should reproduce.

Do not interpret a coefficient merely because its name resembles a process. Formula coding can turn an apparent intercept into a bias, urgency, baseline-cell value, or contrast.

## Candidate-set discipline

- Build the smallest set that represents substantive alternatives.
- Prefer nested simplifications for focused parameter tests when appropriate.
- Include architecture alternatives when the psychological conclusion depends on architecture.
- Keep the same data rows, RT treatment, prior rationale, and response coding across comparisons.
- Use simulation and parameter recovery before trusting a novel custom mapping.

