# Contributing to docs-governance

Thanks for helping improve a small, evidence-oriented governance plugin.

## Before opening a pull request

1. Read [README.md](README.md), then locate the owning `skills/<category>/<name>/SKILL.md` through [CLAUDE_MAP.md](CLAUDE_MAP.md).
2. Keep one canonical owner for each piece of methodology. Commands and agents are host adapters; they should point to a Skill instead of copying its procedure.
3. Keep the change narrow. Do not add a document, directory, or process for a hypothetical future need.
4. Run the verification suite:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements-dev.txt
   bash scripts/verify.sh
   ```

## Where a change belongs

| You are changing | Preferred location |
| --- | --- |
| Methodology or decision rules | `skills/<category>/<name>/SKILL.md` |
| Claude Code interaction adapter | `commands/` or `agents/` |
| A reusable starter file | `templates/` |
| Deterministic validation | `scripts/` plus tests in `tests/` |
| Plugin decision | `docs/adr/` |
| User-facing explanation | `README.md` or `使用说明.md` |

## Pull request expectations

Please explain:

- the concrete project problem or user workflow;
- why the existing skills do not already solve it;
- the smallest change proposed;
- how you verified it; and
- any documentation or compatibility effect.

For a workflow-level idea, open an Issue first. A small, reproducible bug fix can go directly to a pull request.

## Security

Do not include credentials, private project material, or real customer data in issues, examples, tests, or screenshots. If you believe you found a security issue, use GitHub's private security-reporting channel when it is available rather than publishing exploit details in a public issue.
