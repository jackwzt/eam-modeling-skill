# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project intends to follow semantic versioning once tagged releases begin.

## Unreleased

### Added

- Expanded repository documentation, installation instructions, contribution guidance, citation metadata, and GitHub Issue/PR templates.
- Unified MBNCS26 Days 1-5 routing across EMC2 likelihood-based EAMs and BayesFlow/Superstats SBI.
- NPE, NLE, NRE, PyMC composition, neural model-comparison, Day 5, Superstats, EMC2 compatibility, and course-provenance references.
- SBI environment checking and uv-ready analysis scaffolding.
- Public `CREDITS.md`, `CITATIONS.md`, and `CITATIONS.bib` files that separate course acknowledgement, software credit, and scholarly citation.
- Repository security policy, CODEOWNERS, Dependabot configuration, and continuous validation for skill structure plus Python/R syntax.

### Fixed

- BayesFlow diagnostics now import the correctly named training-history helper.
- Training-history heuristics now handle negative losses and non-finite values more safely.

## 0.1.0 - 2026-08-14

### Added

- Initial public release of the `eam-modeling` Agent Skill.
- R/EMC2 workflows for standard, hierarchical, between-subject, dynamic, and reinforcement-learning EAMs.
- BayesFlow/SBI guidance for amortized EAM inference, simulator validation, recovery, calibration, and posterior predictive checks.
- Data-audit, environment-check, analysis-scaffolding, and diagnostic helper scripts.
- Advanced guidance for stop-signal, continuous-judgment, joint cognitive/neural, SEM-linked, and causally interpreted analyses.
- MIT licensing and preserved attribution for adapted Baygent material.
