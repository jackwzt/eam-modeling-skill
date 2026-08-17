"""Repository-level structural validation for the eam-modeling Agent Skill."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "eam-modeling"
SKILL_MD = SKILL / "SKILL.md"
ALLOWED_TOP_LEVEL = {"SKILL.md", "LICENSE", "agents", "assets", "references", "scripts"}
COURSE_ASSET_SUFFIXES = {
    ".csv",
    ".ipynb",
    ".mp3",
    ".mp4",
    ".pdf",
    ".ppt",
    ".pptx",
    ".rdata",
    ".rds",
    ".wav",
    ".xlsx",
    ".zip",
}
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) != 3:
        raise ValueError("SKILL.md frontmatter is not closed")
    result: dict[str, str] = {}
    for raw_line in parts[1].splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {raw_line!r}")
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def local_link_target(markdown_file: Path, target: str) -> Path | None:
    target = target.strip().split(" ", 1)[0].strip("<>")
    if not target or target.startswith(("#", "http://", "https://", "mailto:")):
        return None
    target = unquote(target.split("#", 1)[0])
    return (markdown_file.parent / target).resolve()


def tracked_files() -> set[Path]:
    """Return Git-tracked paths so ignored runtime caches do not fail local checks."""
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "-z"],
            check=True,
            capture_output=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return set()
    return {
        (ROOT / raw.decode("utf-8")).resolve()
        for raw in result.stdout.split(b"\0")
        if raw
    }


def main() -> int:
    errors: list[str] = []
    tracked = tracked_files()

    if not SKILL_MD.is_file():
        errors.append("missing eam-modeling/SKILL.md")
    else:
        text = SKILL_MD.read_text(encoding="utf-8")
        try:
            frontmatter = parse_frontmatter(text)
        except ValueError as exc:
            errors.append(str(exc))
            frontmatter = {}
        if set(frontmatter) != {"name", "description"}:
            errors.append("SKILL.md frontmatter must contain only name and description")
        if frontmatter.get("name") != SKILL.name:
            errors.append("skill name must match the eam-modeling directory")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", frontmatter.get("name", "")):
            errors.append("skill name must follow the Agent Skills naming convention")
        if len(frontmatter.get("name", "")) > 64:
            errors.append("skill name must be at most 64 characters")
        if not frontmatter.get("description"):
            errors.append("skill description must not be empty")
        if len(frontmatter.get("description", "")) > 1024:
            errors.append("skill description must be at most 1024 characters")
        if len(text.splitlines()) >= 500:
            errors.append("SKILL.md must remain under 500 lines")

        for raw_target in LINK_PATTERN.findall(text):
            target = local_link_target(SKILL_MD, raw_target)
            if target is not None and not target.exists():
                errors.append(f"SKILL.md has a broken local link: {raw_target}")

    top_level = {path.name for path in SKILL.iterdir()} if SKILL.is_dir() else set()
    unexpected = sorted(top_level - ALLOWED_TOP_LEVEL)
    if unexpected:
        errors.append(f"unexpected top-level skill entries: {', '.join(unexpected)}")

    for path in SKILL.rglob("*") if SKILL.is_dir() else []:
        lowered_parts = {part.lower() for part in path.parts}
        if (
            "__pycache__" in lowered_parts or path.suffix.lower() in {".pyc", ".pyo"}
        ) and path.resolve() in tracked:
            errors.append(f"generated Python cache is not allowed: {path.relative_to(ROOT)}")
        if path.is_file() and path.suffix.lower() in COURSE_ASSET_SUFFIXES:
            errors.append(f"course/data asset is not allowed in the skill: {path.relative_to(ROOT)}")
        if path.is_file() and path.suffix.lower() == ".py":
            try:
                compile(path.read_text(encoding="utf-8"), str(path), "exec")
            except SyntaxError as exc:
                errors.append(f"Python syntax error in {path.relative_to(ROOT)}: {exc}")

    openai_yaml = SKILL / "agents" / "openai.yaml"
    if openai_yaml.is_file():
        interface = openai_yaml.read_text(encoding="utf-8")
        short_match = re.search(r'^\s*short_description:\s*"([^"]+)"\s*$', interface, re.MULTILINE)
        prompt_match = re.search(r'^\s*default_prompt:\s*"([^"]+)"\s*$', interface, re.MULTILINE)
        if short_match is None or not 25 <= len(short_match.group(1)) <= 64:
            errors.append("openai.yaml short_description must be a quoted 25-64 character string")
        if prompt_match is None or "$eam-modeling" not in prompt_match.group(1):
            errors.append("openai.yaml default_prompt must be quoted and mention $eam-modeling")

    scaffold = SKILL / "scripts" / "scaffold_sbi_analysis.py"
    if scaffold.is_file():
        scaffold_text = scaffold.read_text(encoding="utf-8")
        for required_dependency in ('"bayesflow==2.0.12"', '"jax==0.11.0"'):
            if required_dependency not in scaffold_text:
                errors.append(
                    "SBI scaffold is missing its audited inference dependency: "
                    f"{required_dependency}"
                )

    installer = ROOT / "tools" / "install_skill.py"
    if not installer.is_file():
        errors.append("missing cross-agent installer: tools/install_skill.py")

    for path in (ROOT / "tools").glob("*.py"):
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except SyntaxError as exc:
            errors.append(f"Python syntax error in {path.relative_to(ROOT)}: {exc}")

    if tracked:
        markdown_files = sorted(
            path for path in tracked if path.suffix.lower() == ".md" and path.is_file()
        )
    else:
        excluded_runtime_dirs = {".git", ".venv", "venv", "__pycache__"}
        markdown_files = [
            path
            for path in ROOT.rglob("*.md")
            if excluded_runtime_dirs.isdisjoint(path.parts)
        ]

    for markdown_file in markdown_files:
        for raw_target in LINK_PATTERN.findall(markdown_file.read_text(encoding="utf-8")):
            target = local_link_target(markdown_file, raw_target)
            if target is not None and not target.exists():
                errors.append(
                    f"broken local link in {markdown_file.relative_to(ROOT)}: {raw_target}"
                )

    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in sorted(set(errors)):
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Skill validation passed.")
    print(f"- package: {SKILL.relative_to(ROOT)}")
    print(f"- SKILL.md lines: {len(SKILL_MD.read_text(encoding='utf-8').splitlines())}")
    print(f"- Python helpers: {len(list((SKILL / 'scripts').glob('*.py')))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
