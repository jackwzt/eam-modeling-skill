#!/usr/bin/env python3
"""Install the eam-modeling package for Agent Skills-compatible clients."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "eam-modeling"
SKILL_NAME = "eam-modeling"

PROFILE_PATHS = {
    "shared": Path(".agents") / "skills",
    "codex": Path(".agents") / "skills",
    "copilot": Path(".agents") / "skills",
    "gemini": Path(".agents") / "skills",
    "claude": Path(".claude") / "skills",
}


def destinations(agent: str, scope_root: Path) -> list[tuple[str, Path]]:
    profiles = ("shared", "claude") if agent == "all" else (agent,)
    result: list[tuple[str, Path]] = []
    seen: set[Path] = set()
    for profile in profiles:
        target = (scope_root / PROFILE_PATHS[profile] / SKILL_NAME).resolve()
        if target not in seen:
            result.append((profile, target))
            seen.add(target)
    return result


def install_one(source: Path, target: Path, replace: bool) -> Path | None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(f".{target.name}.installing-{os.getpid()}")
    if temporary.exists():
        raise RuntimeError(f"temporary installation path already exists: {temporary}")

    backup: Path | None = None
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", ".DS_Store")
    try:
        shutil.copytree(source, temporary, ignore=ignore)
        if not (temporary / "SKILL.md").is_file():
            raise RuntimeError("copied package does not contain SKILL.md")

        if target.exists():
            if not replace:
                raise FileExistsError(
                    f"target already exists: {target} (use --replace to keep a backup and update)"
                )
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            backup = target.parent.parent / "skill-backups" / f"{target.name}-{stamp}"
            if backup.exists():
                raise FileExistsError(f"backup path already exists: {backup}")
            backup.parent.mkdir(parents=True, exist_ok=True)
            target.rename(backup)

        temporary.rename(target)
        return backup
    except Exception:
        if temporary.exists():
            shutil.rmtree(temporary)
        if backup is not None and backup.exists() and not target.exists():
            backup.rename(target)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--agent",
        choices=("shared", "codex", "claude", "copilot", "gemini", "all"),
        default="shared",
        help=(
            "Installation profile. 'shared' serves Codex, GitHub Copilot, and "
            "Gemini CLI; 'all' installs shared plus Claude Code."
        ),
    )
    parser.add_argument("--scope", choices=("user", "project"), default="user")
    parser.add_argument(
        "--project-root",
        type=Path,
        help="Project root for --scope project (default: current directory).",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace an existing installation after moving it to a timestamped backup.",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not (SOURCE / "SKILL.md").is_file():
        print(f"Source package is incomplete: {SOURCE}", file=sys.stderr)
        return 1
    if args.scope == "user" and args.project_root is not None:
        parser.error("--project-root is only valid with --scope project")

    scope_root = (
        Path.home().resolve()
        if args.scope == "user"
        else (args.project_root or Path.cwd()).resolve()
    )
    targets = destinations(args.agent, scope_root)

    existing = [target for _, target in targets if target.exists()]
    if existing and not args.replace and not args.dry_run:
        print("Installation stopped because target paths already exist:", file=sys.stderr)
        for target in existing:
            print(f"- {target}", file=sys.stderr)
        print("Use --replace to preserve backups and install the new version.", file=sys.stderr)
        return 2

    for profile, target in targets:
        if args.dry_run:
            action = (
                "would replace"
                if target.exists() and args.replace
                else "would stop because target exists"
                if target.exists()
                else "would install"
            )
            print(f"{profile}: {action} {target}")
            continue
        try:
            backup = install_one(SOURCE, target, args.replace)
        except Exception as exc:
            print(f"Installation failed for {profile}: {exc}", file=sys.stderr)
            return 1
        print(f"{profile}: installed {target}")
        if backup is not None:
            print(f"{profile}: previous installation retained at {backup}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
