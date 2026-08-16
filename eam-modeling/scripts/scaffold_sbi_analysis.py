#!/usr/bin/env python3
"""Create an idempotent uv-ready SBI analysis skeleton."""

from __future__ import annotations

import argparse
from pathlib import Path


ROUTES = ("npe", "nle", "nre", "comparison", "superstats")


def pyproject(route: str) -> str:
    dependencies = [
        '"numpy>=2.4,<2.5"',
        '"pandas"',
        '"scipy"',
        '"matplotlib"',
        '"ipykernel"',
    ]
    if route == "superstats":
        dependencies.append('"superstats==0.0.2"')
    else:
        dependencies.extend(
            ['"bayesflow==2.0.12"', '"keras==3.15.1"', '"jax==0.11.0"']
        )
        if route in {"nle", "nre"}:
            dependencies.append('"pymc==6.2.0"')
    body = ",\n    ".join(dependencies)
    return f'''[project]
name = "sbi-analysis"
version = "0.1.0"
requires-python = ">=3.12,<3.14"
dependencies = [
    {body}
]
'''


def files(route: str) -> dict[str, str]:
    return {
        "README.md": (
            "# SBI analysis\n\n"
            f"Route: `{route}`. Record the question, simulator, prior, representation, estimator, validation gates, and provenance.\n\n"
            "Create the environment with `uv sync`, then run scripts with `uv run python`. "
            "Ordinary BayesFlow routes use the audited JAX backend. "
            "On Windows, prefer a short project path to avoid virtual-environment path-length failures.\n"
        ),
        "pyproject.toml": pyproject(route),
        "config.yaml": (
            "seed: 123\n"
            f"route: {route}\n"
            "num_train_simulations: 10000\n"
            "num_validation_simulations: 1000\n"
            "num_test_simulations: 1000\n"
            "num_posterior_samples: 1000\n"
        ),
        "data_schema.md": (
            "# Data schema\n\n"
            "Document one observation/sequence, identifiers, time order, units, conditions, choices, missingness, masks, padding, and exclusions.\n"
        ),
        "provenance.md": (
            "# Provenance and credits\n\n"
            "- Data source and hash:\n"
            "- Simulator source, version, and hash:\n"
            "- Software versions and lockfile:\n"
            "- Course/external material adapted:\n"
            "- Presenter/author credit:\n"
            "- License and commit:\n"
            "- Modifications:\n"
        ),
        "simulator.py": (
            '"""Define the prior and vectorized simulator; document parameter order, support, units, and failure handling."""\n\n'
        ),
        "train.py": (
            '"""Create disjoint simulation splits, train the selected estimator, and save history/checkpoints."""\n\n'
        ),
        "validate.py": (
            '"""Run prior prediction, recovery, SBC/calibration, contraction, PPCs, and benchmark comparisons."""\n\n'
        ),
        "infer.py": (
            '"""Apply frozen preprocessing and the validated estimator to real observations."""\n\n'
        ),
        "report.md": (
            "# SBI validation report\n\n"
            "## Scientific question and estimand\n\n"
            "## Data and simulator\n\n"
            "## Prior predictive checks\n\n"
            "## Representation and training\n\n"
            "## Recovery, calibration, and contraction\n\n"
            "## Posterior predictive checks\n\n"
            "## Sensitivity and model comparison\n\n"
            "## Provenance and credits\n\n"
            "## Limitations\n"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--route", choices=ROUTES, default="npe")
    args = parser.parse_args()

    args.path.mkdir(parents=True, exist_ok=True)
    created = 0
    expected = files(args.route)
    for name, content in expected.items():
        target = args.path / name
        if target.exists():
            print(f"skip existing: {target}")
            continue
        target.write_text(content, encoding="utf-8")
        print(f"created: {target}")
        created += 1
    print(f"summary: created {created}, total expected {len(expected)}, route {args.route}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
