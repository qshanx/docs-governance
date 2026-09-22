# docs-governance

> A knowledge, decision, and verification governance system for long-running AI-assisted projects.
>
> **It turns a strong agent's one-off work into shared project capability that future agents can inherit, verify, and evolve.**

It works with Claude Code, Codex, and ChatGPT. The goal is not to create more documents, but to keep project rules, architecture, decisions, test rationale, and delivery evidence trustworthy across sessions, agents, and long-term change.

[简体中文](README.zh-CN.md) · [Chinese usage guide](使用说明.md) · [Contributing](CONTRIBUTING.md)

## Try it in three minutes

Install it in Claude Code:

```text
/plugin marketplace add Seekers2001/docs-governance
/plugin install docs-governance@docs-governance
```

Then open an existing project and run a read-only audit:

```text
/governance-audit
```

Or in Codex / ChatGPT:

```text
$docs-governance audit the current project in read-only mode and recommend the smallest useful next step
```

The first output is a report, not an automatic rewrite. Confirm the findings before using `/governance` or a focused skill to change project documents.

## What it provides

### A thin documentation spine

| Document | Single responsibility |
| --- | --- |
| `CLAUDE.md` | durable rules and entry points |
| `CLAUDE_MAP.md` | non-obvious navigation, misleading paths, and do-not-touch areas |
| `PROJECT_STATUS.md` | current health, risks, and priorities |
| `PROJECT_LOG.md` | append-only project history |

The point is not to create four documents in every repository. Use them progressively: a small project can stay small, while a long-running project gains a stable handoff surface for humans and agents.

For a multi-Module project, an optional standalone `ARCHITECTURE.md` carries the current architecture contract: one owner per responsibility and mutable state, explicit Interfaces, allowed and forbidden dependencies, a code-dependency diagram, and a separate runtime-flow diagram. `CLAUDE_MAP.md` only links to it. The two diagrams stay distinct because data may return upstream while source-code dependencies remain one-way.

### Focused workflows

- **Living documentation**: initialize, audit, and synchronize the documentation spine.
- **Context and decisions**: keep stable domain language in `CONTEXT.md`; record high-cost-to-reverse decisions as ADRs.
- **Change impact**: inspect code, data, contracts, tests, docs, deployment, and rollback before and after a risky change.
- **Contract-first collaboration**: use one machine-readable contract indexed by `CONTRACT.md` as the shared source of truth for frontend/backend or multi-service work.
- **Test collaboration**: register requirements, risks, and fixed bugs as TEST-IDs with durable evidence.
- **Module regression**: maintain downstream consumers and executable regression commands for modules that can break each other.

产品文档管理：`product-evolution` 按项目初始化、市场分析、需求调研、需求分析、原型、PRD、需求评审、研发、测试上线、运营反馈组织 docs 下的产品空间，并审查来源、基线与交付证据。参见本插件的 [产品管理入口](docs/product/README.md)。

The implementation lives in these skills: `skills/docs-governance`, `skills/living-docs-governance`, `skills/context-and-decisions`, `skills/change-impact`, `skills/contract-first`, `skills/test-collaboration`, `skills/module-regression`, and `skills/loop-design-check`.

## Why it exists

AI makes code cheap to regenerate, but project intent and verification evidence become easier to lose. A README can become stale, an architecture decision can lose its rationale, and a new agent can repeatedly rediscover the same structure.

Task-level engineering skills help an agent perform one piece of work well. docs-governance preserves the confirmed context, decisions, test rationale, and handoff evidence so that good work survives the session and becomes a project capability.

docs-governance treats project documentation as a small system with one owner per fact, graded reading instead of loading everything every session, and read-only checks before edits.

For tooling, `bash scripts/audit-cheap.sh full --format json` returns the same audit results with scope, Git context, statuses, and evidence. See the [audit result interface](references/audit-result-format.md) for exit codes and verification limits.

## Evidence and safety boundaries

- Audits are read-only by default.
- The plugin does not require a database for ordinary projects. Markdown stays the source of truth; the optional SQLite index is rebuildable and gitignored.
- Task assignment and schedules stay in the repository's existing tracker (for example GitHub Issues or Linear), rather than being copied into governance documents.
- The repository is dogfooded on real projects and its own structure check runs via `bash scripts/verify.sh`.

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
bash scripts/verify.sh
```

Run this before submitting a change. The check validates manifests, hooks, Python syntax, unit tests, the OpenAPI template, and the full documentation audit. PR CI compares log history against the target branch base; local committed-change reviews can set `DOCS_GOVERNANCE_BASE_REF`. The plugin scripts use the Python standard library; third-party validators are development-only dependencies.

See [`TESTS.md`](TESTS.md) for the actual test inventory, why each suite exists, the TEST-IDs it protects, and the remaining gaps.

## License

[MIT](LICENSE) · [Seekers2001](https://github.com/Seekers2001)

文件归位与变更审计可由项目显式启用 `.docs-governance.json`；Stop 按变更检查，提交检查暂存区，推送／PR CI 复用同一规则。配置及安装见 [护栏说明](references/document-policy.md)。
