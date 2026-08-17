# Credits and provenance

`eam-modeling` is an independent skill maintained by [jackwzt](https://github.com/jackwzt). It was informed by the 12th Model-Based Cognition and Neuroscience Summer School (MBNCS26, University of Amsterdam, 2026), but it is not an official course product and is not endorsed by the presenters, organizers, their institutions, the software projects named below, or any AI-agent platform vendor.

## MBNCS26 presenters

The following credits reflect the schedule published in the audited [MBNCS26 repository](https://github.com/niekstevenson/MBNCS26), commit `8e36fee0eaccfae831904cdcae7a94822c34014a`:

| Day | Presenter | Scheduled contribution |
| --- | --- | --- |
| 1 | Udo Böhm | Basic Bayes |
| 1 | Andrew Heathcote | Evidence-accumulation models; diffusion and race-model fitting |
| 2 | Niek Stevenson | Hierarchical cognitive models |
| 2 | Dora Matzke and Sarah Kemp | Stop-signal models |
| 2 | Dora Matzke | Within- versus between-subject correlations in cognitive models |
| 3 | Andrew Heathcote | Expressing psychological theories with EAMs |
| 3 | Amir Hosein Hadian | Circular diffusion models |
| 3 | Niek Stevenson | Joint modelling across tasks |
| 3 | Steven Miletić | Joint modelling with fMRI |
| 4 | Niek Stevenson | Individual differences with SEM; cognitive architectures |
| 4 | Steven Miletić | Time-varying and reinforcement-learning EAMs |
| 5 | Stefan T. Radev | Simulation-based inference, amortized Bayesian workflows, superstatistics, and agentic skills |
| 5 | Michael D. Nunez | Joint behavioural/M/EEG modelling with BayesFlow |

Niek Stevenson is also credited as maintainer of the audited MBNCS26 repository. Session credit does not imply authorship of every course file, and repository authorship does not imply presentation of every session.

The audited MBNCS26 repository did not contain a top-level license. This repository therefore links to and paraphrases the course concepts but does not redistribute its notebooks, slides, recordings, datasets, checkpoints, logos, or other course assets.

## Software and tutorial projects

| Project | Contribution to this skill | Credit and license boundary |
| --- | --- | --- |
| [EMC2](https://github.com/ampl-psych/EMC2) | Likelihood-based EAM design, hierarchical estimation, diagnostics, prediction, comparison, SEM, joint, and dynamic APIs | GPL-3.0-or-later; credit the EMC2 authors and cite the package paper when it is used |
| [BayesFlow](https://github.com/bayesflow-org/bayesflow) | NPE, NLE, NRE, neural model comparison, adapters, structured summaries, amortized training, and calibration | Project license and authorship remain with BayesFlow; cite the version-appropriate BayesFlow paper |
| [Superstats](https://github.com/LuSchumacher/superstats) | Time-varying parameter trajectories, transition models, and amortized neural superstatistics | MIT; copyright Lukas Schumacher; package metadata credits Lukas Schumacher and Stefan T. Radev |
| [dynamic_tutorial](https://github.com/StevenM1/dynamic_tutorial) | Day 4 dynamic EAM teaching patterns | MIT; copyright StevenM1 |
| [rl_eam_tutorial](https://github.com/StevenM1/rl_eam_tutorial) | Day 4 reinforcement-learning EAM teaching patterns | MIT; copyright StevenM1 |
| [baygent-skills](https://github.com/Learning-Bayesian-Statistics/baygent-skills) | Selected Bayesian quality gates, amortized-workflow checks, and causal-claim guardrails | MIT; the preserved notice is in `eam-modeling/references/baygent-license.md` |
| [amortized-dmc](https://github.com/simschaefer/amortized-dmc) | DMC simulator provenance referenced by the Day 5 material | Credit Simon Schaefer for direct use or close adaptation |
| [single_trial_nddm_compare](https://github.com/mdnunez/single_trial_nddm_compare/tree/workshop_demo) | Separately reviewed joint neural/decision-model workshop material | GPL-3.0; no source from this project is copied into the MIT skill |

Exact revisions and the audit date are recorded in [`eam-modeling/references/provenance-and-credits.md`](eam-modeling/references/provenance-and-credits.md).

## How to acknowledge the course

For a substantial deliverable adapted from a specific session, name the relevant presenter beside the method and include an acknowledgement such as:

> This independent workflow was informed by the 2026 MBNCS summer-school materials and credits the relevant presenters and source authors listed in its provenance record. It is not an official or endorsed MBNCS26 deliverable.

Course acknowledgement is not a substitute for scholarly citation. Cite the actual model, inference method, and software used; see [CITATIONS.md](CITATIONS.md) and [CITATIONS.bib](CITATIONS.bib).
