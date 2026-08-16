# Provenance, credits, and redistribution boundaries

## MBNCS26 scope

This independent skill was informed by the 12th Model-Based Cognition and Neuroscience Summer School (University of Amsterdam, 2026). It is not an official MBNCS26 product and does not imply endorsement by presenters, organizers, repository maintainers, their institutions, software projects, or OpenAI.

Audited course repository: `https://github.com/niekstevenson/MBNCS26`, commit `8e36fee0eaccfae831904cdcae7a94822c34014a`, audited 2026-08-16. The audited repository has no top-level license. Treat course notebooks, scripts, slides, recordings, datasets, checkpoints, and logos as all-rights-reserved unless their rights holders state otherwise. Link to the source and paraphrase concepts; do not redistribute course assets through this skill.

## Presenter credits from the published schedule

| Day | Presenter | Scheduled contribution |
|---|---|---|
| 1 | Udo Böhm | Basic Bayes |
| 1 | Andrew Heathcote | EAM introduction; fitting diffusion and race models |
| 2 | Niek Stevenson | Hierarchical models |
| 2 | Dora Matzke and Sarah Kemp | Stop-signal models |
| 2 | Dora Matzke | Within- versus between-subject correlations in cognitive models |
| 3 | Andrew Heathcote | Expressing psychological theories |
| 3 | Amir Hosein Hadian | Circular diffusion models |
| 3 | Niek Stevenson | Joint modelling across tasks |
| 3 | Steven Miletić | Joint modelling with fMRI |
| 4 | Niek Stevenson | Individual differences with SEM; cognitive architectures |
| 4 | Steven Miletić | Time-varying EAMs; reinforcement-learning EAMs |
| 5 | Stefan T. Radev | SBI introduction; amortized Bayesian workflows; superstatistics and agentic skills |
| 5 | Michael D. Nunez | Joint modelling with M/EEG and BayesFlow |

Credit Niek Stevenson separately as maintainer of the MBNCS26 repository. Session credit does not imply authorship of every file, and repository authorship does not by itself imply presentation of a session.

## External software and tutorial sources

| Source | Audited revision | License/credit boundary |
|---|---|---|
| `ampl-psych/EMC2` | main `beab948d...`; dev `b1e05438...` | GPL-3.0-or-later; package authors/contributors are listed in `DESCRIPTION` |
| `StevenM1/dynamic_tutorial` | `86c6412b2baad021e26f2516091d3ffedadfc88f` | MIT, copyright StevenM1 |
| `StevenM1/rl_eam_tutorial` | `5285ea62b77036669e7c0b184c70705d7e6da546` | MIT, copyright StevenM1 |
| `LuSchumacher/superstats` | `00b40acd97e6eb2b0f5c0e1c933afd69cd9dcd40` | MIT, copyright Lukas Schumacher; package metadata names Lukas Schumacher and Stefan Radev |
| `Learning-Bayesian-Statistics/baygent-skills` | `aa940481ebb9fbd087b2fc41dba3af386b5bdb31` | MIT; preserved notice in `baygent-license.md` |
| `simschaefer/amortized-dmc` | link recorded in the course DMC source | Credit Simon Schaefer when using that implementation or a close adaptation |
| `mdnunez/single_trial_nddm_compare` workshop branch | use the exact checked-out commit in a deliverable | GPL-3.0; keep code outside this MIT skill unless license obligations are deliberately handled |

## Recommended scholarly citations

Match citations to the route actually used; do not cite every item by default.

| Route | Recommended source |
|---|---|
| EMC2 | Stevenson, Donzallaz, Innes, Forstmann, Matzke, and Heathcote (2026), *Bayesian hierarchical cognitive modeling with the EMC2 package*, `https://doi.org/10.3758/s13428-025-02869-y` |
| BayesFlow 2 | Kühmichel et al. (2026), *BayesFlow 2: Multi-Backend Amortized Bayesian Inference in Python*, `https://arxiv.org/abs/2602.07098` |
| BayesFlow software/workflow | Radev et al. (2023), *BayesFlow: Amortized Bayesian workflows with neural networks*, `https://doi.org/10.21105/joss.05702` |
| Neural superstatistics | Schumacher, Bürkner, Voss, Köthe, and Radev (2023), `https://doi.org/10.1038/s41598-023-40278-3` |
| Non-stationary-model validation | Schumacher, Schnuerch, Voss, and Radev (2025), `https://doi.org/10.1007/s42113-024-00218-4` |
| Linear ballistic accumulation | Brown and Heathcote (2008), `https://doi.org/10.1016/j.cogpsych.2007.12.002` |
| Diffusion decision model | Ratcliff, Smith, Brown, and McKoon (2016), `https://doi.org/10.1016/j.tics.2016.01.007` |
| Simulation-based calibration | Talts, Betancourt, Simpson, Vehtari, and Gelman (2018), `https://arxiv.org/abs/1804.06788` |

Check each upstream project's current citation guidance when using a later major release.

## Required acknowledgement

For a substantial deliverable that adapts MBNCS26 material, include:

> This independent workflow was informed by the 2026 MBNCS summer-school materials and credits the relevant presenters and source authors listed in its provenance record. It is not an official or endorsed MBNCS26 deliverable.

Add session-specific and software-specific credit next to the adapted method. Cite primary papers and official software documentation for scientific claims; course acknowledgement is not a substitute for scholarly citation.

## Review checklist

- Confirm names, diacritics, session ownership, and source URLs with organizers before public release.
- Record the exact course, software, tutorial, data, and simulator revisions used by the deliverable.
- Preserve MIT/GPL notices when code is copied or adapted under those licenses.
- Obtain permission before adding course branding or redistributing course assets.
- Keep unrelated courses and summer-school materials outside this skill.
