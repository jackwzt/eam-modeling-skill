#!/usr/bin/env python3
"""Report SBI package/API prerequisites without importing heavy frameworks."""

from __future__ import annotations

import argparse
import importlib.util
from importlib import metadata
import os
import platform
import sys


PACKAGES = {
    "bayesflow": {"modules": ("bayesflow",), "distributions": ("bayesflow",)},
    "jax": {"modules": ("jax",), "distributions": ("jax",)},
    "keras": {"modules": ("keras",), "distributions": ("keras",)},
    "numpy": {"modules": ("numpy",), "distributions": ("numpy",)},
    "scipy": {"modules": ("scipy",), "distributions": ("scipy",)},
    "pandas": {"modules": ("pandas",), "distributions": ("pandas",)},
    "pymc": {"modules": ("pymc",), "distributions": ("pymc",)},
    "hssm": {"modules": ("hssm",), "distributions": ("hssm",)},
    "ssm-simulators": {
        "modules": ("ssms", "cssm"),
        "distributions": ("ssm-simulators", "ssms"),
        "module_mode": "any",
    },
    "superstats": {"modules": ("superstats",), "distributions": ("superstats",)},
    "torch": {"modules": ("torch",), "distributions": ("torch",)},
    "tensorflow": {"modules": ("tensorflow",), "distributions": ("tensorflow",)},
}

PROFILES = {
    "none": (),
    "base": ("numpy", "scipy", "pandas"),
    "day5": ("bayesflow", "jax", "keras", "numpy", "scipy", "pandas", "pymc", "hssm"),
    "nle-pymc": ("bayesflow", "keras", "numpy", "pymc"),
    "superstats": ("superstats", "bayesflow", "keras", "numpy"),
}


def installed_version(distributions: tuple[str, ...]) -> str:
    for distribution in distributions:
        try:
            return metadata.version(distribution)
        except metadata.PackageNotFoundError:
            continue
    return "unknown"


def package_status(spec: dict) -> tuple[bool, tuple[str, ...]]:
    modules = spec["modules"]
    found = tuple(importlib.util.find_spec(module) is not None for module in modules)
    mode = spec.get("module_mode", "all")
    available = any(found) if mode == "any" else all(found)
    missing = tuple(module for module, present in zip(modules, found) if not present)
    return available, missing


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=tuple(PROFILES), default="none")
    parser.add_argument(
        "--require",
        nargs="*",
        choices=tuple(PACKAGES),
        default=(),
        help="Add packages that must be import-discoverable; exit 2 when unavailable.",
    )
    args = parser.parse_args()

    profile_requirements = list(PROFILES[args.profile])
    if args.profile == "superstats":
        profile_requirements.append("torch" if sys.platform == "win32" else "jax")
    required = tuple(dict.fromkeys([*profile_requirements, *args.require]))

    print(f"Python: {sys.version.split()[0]}")
    print(f"Executable: {sys.executable}")
    print(f"Platform: {platform.platform()}")
    print(f"Profile: {args.profile}")
    print(f"KERAS_BACKEND: {os.environ.get('KERAS_BACKEND', 'not set')}")

    missing_required: list[str] = []
    for name, spec in PACKAGES.items():
        available, missing_modules = package_status(spec)
        if available:
            print(f"{name}: {installed_version(spec['distributions'])}")
        else:
            missing_text = ", ".join(repr(value) for value in missing_modules)
            print(f"{name}: unavailable (module candidates missing: {missing_text})")
            if name in required:
                missing_required.append(name)

    compatibility_issues: list[str] = []
    if args.profile in {"day5", "superstats"} and not ((3, 12) <= sys.version_info[:2] < (3, 14)):
        compatibility_issues.append(f"{args.profile} profile requires Python >=3.12,<3.14")

    print("Audited Day 5 lock: Python 3.12-3.13, BayesFlow 2.0.12, JAX 0.11.0, Keras 3.15.1, NumPy 2.4.6, PyMC 6.2.0.")
    print("Audited Superstats main: version 0.0.2; BayesFlow 2.0.12; NumPy >=2.4,<2.5; PyTorch on Windows, JAX elsewhere.")
    if args.profile == "superstats" and os.environ.get("KERAS_BACKEND") is None:
        print("WARNING: KERAS_BACKEND is not set; record the backend reported by BayesFlow at import time.")

    if missing_required:
        print(f"Missing required packages: {', '.join(missing_required)}", file=sys.stderr)
    for issue in compatibility_issues:
        print(f"Compatibility issue: {issue}", file=sys.stderr)

    return 2 if missing_required or compatibility_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
