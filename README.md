# docs-governance

> A knowledge, decision, and verification governance system for long-running AI-assisted projects.
>
> **It turns a strong agent's one-off work into shared project capability that future agents can inherit, verify, and evolve.**

It works with Claude Code, Codex, and ChatGPT. The goal is not to create more documents, but to keep project rules, architecture, decisions, test rationale, and delivery evidence trustworthy across sessions, agents, and long-term change.

[简体中文](README.zh-CN.md) · [Chinese usage guide](使用说明.md) · [Contributing](CONTRIBUTING.md)

模块功能、公共接口或共享数据变更，可在项目入口接入 [模块变更流程](skills/documentation/docs-governance/SKILL.md#模块变更流程)：改前分析影响 → 实施后核对 diff → 本模块及下游回归 → 文档同步。它是 Agent 执行约定，不等于已安装自动 Hook。

## Try it in three minutes

Install it in Claude Code:

```text
/plugin marketplace add qshanx/docs-governance
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

The first output is a report, not an automatic rewrite. Use `/governance-setup` for new, discussed-but-not-built, or existing projects: it discovers existing sources, confirms the file scope, then organizes existing documents, adds the sources needed for the agreed scope, connects navigation and status, and configures Agent entrypoints through shared skills. Product documentation is added when needed. Existing PRD/Spec files stay authoritative; unknowns remain explicit. `/governance-init` is a compatibility alias, and `/governance` handles ongoing maintenance. Setup does not implicitly install hooks, initialize Git, commit, or push.

## What it provides

### A thin documentation spine

| Document | Single responsibility |
| --- | --- |
| `CLAUDE.md` | durable rules and entry points |
| `CLAUDE_MAP.md` | non-obvious navigation, misleading paths, and do-not-touch areas |
| `PROJECT_STATUS.md` | current health, risks, and priorities |
| `PROJECT_LOG.md` | append-only project history |

Setup reuses existing sources and establishes navigation and current status for the agreed scope. Git projects do not create a LOG by default; existing history and project-specific logging agreements remain in force.

Use `architecture-docs` to decide whether architecture documentation is needed and reuse an existing source when available. It records module responsibilities, state ownership, interfaces, dependencies, and core flows from project evidence, keeping current implementation separate from planned design. `CLAUDE_MAP.md` links to the source; code-dependency and runtime-flow diagrams have distinct meanings.

### Focused workflows

- **Governance rule placement** (`agent-workflow-governance`): inspect where project rules and reusable workflows belong—entrypoints, skills, supporting files, scripts, or hooks. Report evidence and minimal recommendations without installing hooks or changing gates.

- **Document structure** (`docs-structure`): group related documents by responsibility, keep detailed content behind concise entry points, and plan, organize, or review the structure.
- **Agent entrypoints** (`agent-entrypoints`): turn confirmed project context into actionable `AGENTS.md` / `CLAUDE.md` instructions, including requirement-reading triggers, real validation commands, and a single shared rule source.
- **Architecture documents** (`architecture-docs`): decide whether a project needs an architecture document, then create, improve, or review it against project evidence.
- **Daily document maintenance** (`docs-maintenance`): synchronize documents affected by a completed task, update stale content, consolidate duplicates, and report verification gaps.
- **Document audit** (`docs-audit`): read-only review of document navigation, freshness, organization, duplicate sources, and current versus historical material; structural review reuses `docs-structure` when available.
- **Project retrospective** (`project-retro`): review scoped conversations, logs, commits, and verification evidence across agent environment, documents, tests, collaboration, and delivery. Inspect tool costs, ineffective instructions, executable checks, and implementation/review responsibilities. Extract lessons, revalidate their effects, and promote proven practices into existing rules or checks; read-only by default.
- **PR review** (`pr-review`): understand the problem, sketch an independent solution before reading the implementation, review the solution and code, verify behavior in a separate testing step, and provide Markdown diffs for actionable fixes. Reports use Summary, Evidence, and Merge Danger. Pins base/head and reuses existing impact, contract, regression, and documentation methods; leaves the target workspace and remote PR unchanged by default.

- **Writing for agents** (`writing-for-agents`): structure Skills, agent entrypoints and documents read by AI using clear pointers, progressive disclosure and completion criteria; preserve meaning with a local final check. Includes the upstream MIT license and pinned source.
- **Living documentation**: establish the initial document system, delegate specialized maintenance, and retain read-only audits and log archiving.
- **Domain modeling** (`domain-modeling`): reuse Matt Pocock's pinned method for domain language and lightweight ADRs, with the MIT license included. Local adaptation only connects existing records, module rules and audits; `context-and-decisions` remains a compatibility entrypoint.
- **Change impact**: inspect code, data, contracts, tests, docs, deployment, and rollback before and after a risky change.
- **Contract-first collaboration**: use one machine-readable contract indexed by `CONTRACT.md` as the shared source of truth for frontend/backend or multi-service work.
- **Test collaboration**: register requirements, risks, and fixed bugs as TEST-IDs with durable evidence.
- **Module regression**: maintain downstream consumers and executable regression commands for modules that can break each other.

产品文档管理：`product-evolution` 按项目初始化、市场分析、需求调研、需求分析、原型、PRD、需求评审、研发、测试上线、运营反馈组织 docs 下的产品空间，并审查来源、基线与交付证据。参见本插件的 [产品管理入口](docs/product/README.md)。

Claude Code 的 [product-docs-manager](agents/product-docs-manager.md) 是产品文档管理员角色，调用现有 Skills 管理来源、需求编号、修订及授权；Codex / ChatGPT 直接使用 `$product-evolution` 执行同一流程。PM 四类材料索引、六类管理位置与十阶段导航共用主记录；CLAUDE 从产品入口触发按任务读取，必要条款分批核对，避免默认全量加载 PRD。

The implementation lives in `skills/documentation/` and `skills/engineering/`, including `docs-governance`, `project-retro`, `writing-for-agents`, `living-docs-governance`, `domain-modeling`, `context-and-decisions` (compatibility), `change-impact`, `contract-first`, `test-collaboration`, `module-regression`, and `loop-design-check`.

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

[MIT](LICENSE) · [qshanx](https://github.com/qshanx)

文件归位与变更审计可由项目显式启用 `.docs-governance.json`；Stop 按变更检查，提交检查暂存区，pre-push 与 PR CI 强制扫描提交快照，并按改动列出应核对文档。创建 PR 前使用同一检查入口，失败先修复。配置及安装见 [护栏说明](references/document-policy.md)。

检查通过后，由 Agent 按 [事实变化核对文档](skills/engineering/change-impact/SKILL.md#按事实核对文档)，定位正文冲突、映射外说明与重复决定；可从 [接口变更样例](skills/engineering/change-impact/examples/interface-change.md) 复跑。脚本不自动判定正文过期。

Skills are grouped under `skills/documentation/` and `skills/engineering/`. `in-progress/` and `deprecated/` are reserved and not loaded. Skill names and invocation remain unchanged.

Project health evidence collection is available through `living-docs-governance`: it inspects project entrypoints, validation commands, CI references, and explicit receipts without executing discovered commands or reading global configuration or session history. Static evidence does not establish a health pass.

## module-governance

新建核心业务模块、补齐模块文档或维护模块约定时，可按任务意图调用 [module-governance](skills/documentation/module-governance/SKILL.md)，无需点名。复用项目／模块 AGENTS、CONTEXT、契约与决策主记录；普通 Bug、样式修改不触发建档，纯审计不授权写入。生成后运行已有链接审计，断链修复后复跑。
