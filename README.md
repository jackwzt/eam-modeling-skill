# EAM and SBI Modeling Skill

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-4b32c3)](https://agentskills.io/specification)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Validate skill](https://github.com/jackwzt/eam-modeling-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/jackwzt/eam-modeling-skill/actions/workflows/validate.yml)
[![Cite this repository](https://img.shields.io/badge/citation-CFF-blue.svg)](CITATION.cff)

`eam-modeling` is a unified Codex skill for the five-day MBNCS26 curriculum: evidence-accumulation modeling with R/EMC2 plus simulation-based inference with BayesFlow and Superstats. It designs, fits, diagnoses, compares, validates, and reports both likelihood-based and amortized cognitive-model analyses.

The skill turns choice and response-time data into a reproducible analysis workflow with explicit data mapping, prior validation, convergence and calibration checks, posterior predictive assessment, and cautious scientific interpretation.

## What it supports

| Area | Coverage |
| --- | --- |
| Model families | WDM, DDM, LBA, RDM, LNR, stop-signal, continuous-judgment, and related EAMs |
| Study designs | Individual, hierarchical, between-subject, dynamic trial-by-trial, and reinforcement-learning EAMs |
| Estimation | R/EMC2 sampling; BayesFlow NPE/NLE/NRE and model comparison; PyMC composition |
| Dynamic SBI | Superstats time-varying trajectories and transition models |
| Extended analyses | Joint cognitive/EEG models, SEM-linked models, and guarded causal interpretation |
| Validation | Data audits, prior prediction, parameter recovery, convergence, calibration, contraction, and posterior predictive checks |
| Input formats | CSV, XLSX, RDS, and RData files with choices, RTs, conditions, rewards, trials, or participant identifiers |
| Course coverage | MBNCS26 Days 1-5, with presenter/source credits and redistribution boundaries |

## Install

### From Codex

Ask Codex:

> Use `$skill-installer` to install the `eam-modeling` skill from `https://github.com/jackwzt/eam-modeling-skill/tree/main/eam-modeling`.

Codex detects installed skill changes automatically. Restart Codex only if the skill does not appear.

### Manual installation

Clone the repository and copy only the `eam-modeling/` directory into your Codex skills directory.

PowerShell:

```powershell
git clone https://github.com/jackwzt/eam-modeling-skill.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\.agents\skills" | Out-Null
Copy-Item -Recurse -Force ".\eam-modeling-skill\eam-modeling" "$env:USERPROFILE\.agents\skills\"
```

macOS or Linux:

```bash
git clone https://github.com/jackwzt/eam-modeling-skill.git
mkdir -p "$HOME/.agents/skills"
cp -R ./eam-modeling-skill/eam-modeling "$HOME/.agents/skills/"
```

## Quick start

Invoke the skill explicitly with `$eam-modeling`, or ask a matching question in natural language. For example:

```text
Use $eam-modeling to audit this RData file and map its participant, response,
RT, condition, and trial-order columns before fitting anything.
```

```text
Use $eam-modeling to build a hierarchical LBA analysis in EMC2, validate the
priors, run a short pilot fit, and define the posterior predictive checks.
```

```text
Use $eam-modeling to design a BayesFlow amortized workflow for this DDM
simulator, including recovery, calibration, and real-data PPCs.
```

```text
Use $eam-modeling to build a Superstats workflow for time-varying drift and
threshold, using offline training, trajectory recovery, calibration, and PPCs.
```

```text
Use $eam-modeling to explain this MBNCS26 Day 5 NLE notebook and adapt it to
PyMC without copying course assets into the output.
```

The skill deliberately stops before expensive fitting when response coding, RT units, trial order, model contrasts, or simulator structure are ambiguous.

## Workflow

1. Audit the data and preserve the raw inputs.
2. Route the task to EMC2, BayesFlow, or a specialized EAM workflow.
3. Define a small, theory-driven model set.
4. Validate priors, mappings, constraints, and identifiability.
5. Pilot before launching a full fit or amortizer training run.
6. Apply convergence, recovery, calibration, and predictive diagnostic gates.
7. Report both successful predictions and persistent model misfit.

## Requirements

The skill itself is plain Markdown plus helper scripts. Runtime dependencies depend on the selected route:

- **EMC2 route:** R and the packages required by the target EMC2 analysis.
- **BayesFlow route:** Python 3.12-3.13 and the BayesFlow backend stack required by the target simulator and estimator.
- **Superstats route:** the current Superstats environment; audited 0.0.2 metadata selects PyTorch on Windows and JAX on Linux/macOS.
- **Data helpers:** additional R or Python packages may be needed for formats such as XLSX.

The included environment-check scripts report missing dependencies before analysis begins.

## Repository layout

```text
.
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
├── CITATION.cff
├── CITATIONS.md
├── CITATIONS.bib
├── CREDITS.md
├── SECURITY.md
├── tools/validate_skill.py
├── .github/
│   ├── workflows/validate.yml
│   ├── ISSUE_TEMPLATE/
│   ├── CODEOWNERS
│   └── dependabot.yml
└── eam-modeling/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── references/
    └── scripts/
```

`eam-modeling/` is the installable Agent Skill package. Repository documentation and GitHub community files remain outside that directory so they do not consume the skill's runtime context.

## Validation

The skill follows the [Agent Skills specification](https://agentskills.io/specification). Validate the package with a compatible validator:

```bash
skills-ref validate ./eam-modeling
```

The repository also includes a dependency-free structural validator used by GitHub Actions:

```bash
python tools/validate_skill.py
```

Contributors using Codex's bundled skill tools can additionally run `quick_validate.py` against the `eam-modeling/` directory. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full checklist.

## Citation and attribution

Selected Bayesian workflow, amortized-inference, and causal-claim guardrails were adapted from [Learning-Bayesian-Statistics/baygent-skills](https://github.com/Learning-Bayesian-Statistics/baygent-skills). The preserved upstream MIT notice is in [`eam-modeling/references/baygent-license.md`](eam-modeling/references/baygent-license.md).

Use [`CITATION.cff`](CITATION.cff) to cite this repository. Use [`CITATIONS.md`](CITATIONS.md) and [`CITATIONS.bib`](CITATIONS.bib) to cite the actual models and software used in an analysis, including [EMC2](https://github.com/ampl-psych/EMC2), [BayesFlow](https://github.com/bayesflow-org/bayesflow), and [Superstats](https://github.com/LuSchumacher/superstats).

See [`CREDITS.md`](CREDITS.md) for the five-day presenter schedule, repository maintainers, upstream tutorial authors, audited revisions, and licensing boundaries. The skill does not redistribute MBNCS26 assets or copy GPL-licensed project code into this MIT repository.

## License

This repository is released under the [MIT License](LICENSE).
