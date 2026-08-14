# Contributing

Contributions that improve the accuracy, reproducibility, portability, or usability of `eam-modeling` are welcome.

## Before you start

- Open a feature request before proposing a new modeling framework or a major workflow change.
- Do not commit private datasets, fitted samples, credentials, tokens, or identifiable participant information.
- Prefer small changes with a concrete EAM use case and a reproducible example.

## Keep the package focused

The installable package is `eam-modeling/`:

- Put core routing and mandatory workflow instructions in `eam-modeling/SKILL.md`.
- Put detailed, route-specific guidance in `eam-modeling/references/` and link it directly from `SKILL.md`.
- Put deterministic, reusable helpers in `eam-modeling/scripts/`.
- Keep user-facing repository documents such as README and CHANGELOG at the repository root, not inside the skill package.
- Avoid duplicating the same guidance in `SKILL.md` and a reference file.

Keep `SKILL.md` concise and under 500 lines. Its YAML frontmatter must retain a valid lowercase hyphenated `name` and a description that states both what the skill does and when it should trigger.

## Make a change

1. Fork or clone the repository and create a focused branch.
2. Edit only the files required by the proposed behavior.
3. Update `CHANGELOG.md` under **Unreleased** for user-visible changes.
4. Add or revise references when new dependencies, assumptions, or diagnostic gates are introduced.
5. Keep `eam-modeling/agents/openai.yaml` aligned with the skill's purpose and default prompt.

## Validate

Run an Agent Skills validator from the repository root:

```bash
skills-ref validate ./eam-modeling
```

When working inside Codex on Windows, the bundled validator can also be used:

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" ".\eam-modeling"
```

For script changes:

- Run the changed script on a small synthetic or public fixture.
- Exercise both the normal path and at least one expected failure path.
- Confirm that failures give actionable messages and do not modify raw input files.
- Do not launch a costly MCMC fit or amortizer training run merely for a documentation change.

For workflow changes, test a realistic prompt and verify that the skill chooses the intended route, reads only the relevant references, and applies the required diagnostic gates.

## Pull request checklist

- [ ] The change has one clear purpose.
- [ ] No private data, fitted samples, secrets, or generated caches are included.
- [ ] `SKILL.md` remains concise and all referenced paths resolve.
- [ ] Helper scripts were exercised when changed.
- [ ] The skill validator passes.
- [ ] `CHANGELOG.md` describes user-visible behavior.
- [ ] New scientific claims include appropriate assumptions and limitations.

By contributing, you agree that your contribution will be licensed under the repository's MIT License.
