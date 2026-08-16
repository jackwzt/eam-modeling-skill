# Security policy

## Supported version

Security fixes are applied to the current `main` branch. Tagged releases, when available, state their support status in the release notes.

## Report a vulnerability

Do not disclose a suspected vulnerability, credential, private dataset, identifiable participant information, or unsafe model artifact in a public issue.

Use GitHub's private [security advisory form](https://github.com/jackwzt/eam-modeling-skill/security/advisories/new) and include:

- the affected file and revision;
- the smallest safe reproduction;
- the expected impact;
- whether credentials, private data, arbitrary code execution, or unsafe file writes are involved;
- any proposed mitigation.

For ordinary modeling errors, documentation problems, or non-sensitive bugs, use the public bug-report template.

## Scope

This policy covers the skill instructions and bundled helper scripts. It does not provide security support for EMC2, BayesFlow, Superstats, R, Python, Codex, or other upstream dependencies; report upstream vulnerabilities to their maintainers as well.
