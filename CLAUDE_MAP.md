# CLAUDE_MAP.md — 插件地图（只记 `ls` 看不出来的）

> 目录里有啥直接 `ls`；这里只记知识入口、非显然定位和易误读区。完整架构不放这里。

## 当前架构入口

- Module 权责、状态归属、代码依赖与运行时核心流转 → `ARCHITECTURE.md`
- 架构、数据库等难回退决策及理由 → `docs/adr/README.md`

- 改**方法论** → 只动 `skills/*/SKILL.md`，agent / command 自动继承（它们只指向、不复制）
- 改**模板** → `templates/*.example.md`
- 加**体检项** → `scripts/verify.sh`
- 改日志格式 → `scripts/logformat.py`；改归档与索引策略 → `scripts/project-log-index.py` + `docs/adr/README.md`

## 找 X 去哪

| 要找 | 去 |
|---|---|
| 文件位置规则与触发约定 | `.docs-governance.json`、[执行说明](references/document-policy.md) |
| 暂存文档审计与提交护栏 | `scripts/check-staged-docs.py`、`hooks/pre-commit.sh` |
| PR 前变更映射、提交快照扫描与推送门禁 | `scripts/check-pr-docs.py`、`hooks/pre-push.sh` |
| 变更触发审计与规则校验 | `scripts/auto-audit.py`、`scripts/docpolicy.py` |
| 产品十阶段管理与审查方法 | `skills/product-evolution/SKILL.md` |
| 产品文档管理员角色（Claude Code） | `agents/product-docs-manager.md`；Codex 直接执行 `product-evolution` |
| 本插件产品管理入口与需求基线 | [产品管理](docs/product/README.md) |
| 产品阶段入口模板 | `templates/product-index.example.md` |
| 插件总路由 | `skills/docs-governance/SKILL.md` |
| 活文档方法论 | `skills/living-docs-governance/SKILL.md` |
| 领域上下文与 ADR | `skills/context-and-decisions/SKILL.md` |
| 变更影响分析 | `skills/change-impact/SKILL.md` |
| 契约方法论（含两种模式） | `skills/contract-first/SKILL.md` |
| 测试资产与必要测试点治理 | `skills/test-collaboration/SKILL.md` |
| 本插件实际测试资产、测试目的与缺口 | `TESTS.md` |
| 模块联动回归方法论 | `skills/module-regression/SKILL.md` |
| 当前架构与核心流转 | `ARCHITECTURE.md` |
| 展示版架构图 | `diagram/architecture.svg`（PNG 预览同目录） |
| ARCHITECTURE.md 空白模板 | `templates/ARCHITECTURE.example.md` |
| TESTS.md 空白模板 | `templates/TESTS.example.md` |
| 机器接口契约与入口模板 | `templates/openapi.example.json` + `templates/CONTRACT.example.md` |
| 开发测试依赖 | `requirements-dev.txt`（插件运行时仍用标准库） |
| Codex 项目入口模板 | `templates/AGENTS.example.md` |
| 收尾同步矩阵 | `references/governance-sync-matrix.md` |
| 结构完整性自检 | `scripts/verify.sh` |
| 本地与 CI 测试入口 | `TESTS.md` + `.github/workflows/verify.yml` |
| 文档确定性审计 | `scripts/audit-docs.py`（`scripts/audit-cheap.sh` 是入口） |
| 审计结果与 JSON 接口 | `references/audit-result-format.md` |
| 日志共享解析与格式错误 | `scripts/logformat.py`（审计和索引共用） |
| PROJECT_LOG 归档与索引 | `scripts/project-log-index.py` |
| 插件自身架构决策 | `docs/adr/README.md` |

## 易误读（别混）

- `templates/*.example.md` 是给**用户项目**套用的空白模板，**不是本插件自己的治理文件**。本插件自己的治理文件是根目录的 `CLAUDE.md` / `CLAUDE_MAP.md` / `PROJECT_STATUS.md` / `PROJECT_LOG.md`，按需再加 `ARCHITECTURE.md` 等载体（无 `.example` 后缀）。
- `.codex-plugin/plugin.json` 与 `.claude-plugin/plugin.json` 是不同宿主的安装入口，名称和版本必须一致；方法论仍只在 `skills/` 维护。
- 根目录 `AGENTS.md` 只负责让 Codex 进入共享 `CLAUDE.md` 章程，不是第五份治理文档。
- `.governance/project-log.sqlite` 是从 Markdown 日志重建的本地派生索引，默认忽略；不能当项目排期或历史唯一来源。
