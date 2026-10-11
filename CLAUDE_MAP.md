# CLAUDE_MAP.md — 插件地图（只记 `ls` 看不出来的）

> 目录里有啥直接 `ls`；这里只记知识入口、非显然定位和易误读区。完整架构不放这里。

## 当前架构入口

- Module 权责、状态归属、代码依赖与运行时核心流转 → `ARCHITECTURE.md`
- 架构、数据库等难回退决策及理由 → `docs/adr/README.md`

- 改**方法论** → 只动 `skills/<category>/<name>/SKILL.md`，agent / command 自动继承（它们只指向、不复制）
- 改**模板** → `templates/*.example.md`
- 加**体检项** → `scripts/verify.sh`
- 改日志格式 → `scripts/logformat.py`；改归档与索引策略 → `scripts/project-log-index.py` + `docs/adr/README.md`

## 找 X 去哪

| 要找 | 去 |
|---|---|
| 本插件文档按职责查找、区分当前记录与历史资料 | [项目文档入口](docs/README.md) |
| 外部文章、方法比较与候选贡献 | [研究资料索引](research/README.md) |
| 已停用的 Skill 及替代入口 | [停用目录说明](skills/deprecated/README.md)；不用于存放普通旧文档 |
| 治理规则落点与散落工作流沉淀检查 | `skills/documentation/agent-workflow-governance/SKILL.md`；细则按需读取其 supporting-files，默认只读 |
| Agent 入口内容、共享主源选择与规则可执行性 | `skills/documentation/agent-entrypoints/SKILL.md`；来源见 [Vince 八条经验](research/2026-09-27-vincemask-agent-entrypoints.md)、[Tw93 工程实践](research/2026-09-27-tw93-claude-code-governance.md) |
| Agent 入口 200 行检查 | `scripts/check-entrypoint-length.py`，传入本次受检文件 |
| Agent 入口完整示例（项目输入 → AGENTS.md 成品） | `skills/documentation/agent-entrypoints/examples/confirmed-project.md`；虚构案例，不能作为目标项目事实 |
| 新项目／讨论后项目／已有项目统一 setup | `commands/governance-setup.md` → `agents/docs-governor.md` → `skills/documentation/living-docs-governance/SKILL.md` 的“统一 setup”；init 为兼容别名 |
| 文件位置规则与触发约定 | `.docs-governance.json`、[执行说明](references/document-policy.md) |
| 暂存文档审计与提交护栏 | `scripts/check-staged-docs.py`、`hooks/pre-commit.sh` |
| PR 前变更映射、提交快照扫描与推送门禁 | `scripts/check-pr-docs.py`、`scripts/install-pre-push.py`、`hooks/pre-push.sh` |
| 变更触发审计与规则校验 | `scripts/auto-audit.py`、`scripts/docpolicy.py` |
| 产品四类索引、十阶段导航、按任务读取与审查方法 | `skills/documentation/product-evolution/SKILL.md` |
| 产品文档管理员角色（Claude Code） | `agents/product-docs-manager.md`；Codex 直接执行 `product-evolution` |
| 本插件产品管理入口与需求基线 | [产品管理](docs/product/README.md) |
| 产品阶段入口模板 | `templates/product-index.example.md` |
| 插件总路由 | `skills/documentation/docs-governance/SKILL.md` |
| 活文档方法论 | `skills/documentation/living-docs-governance/SKILL.md` |
| 领域上下文与 ADR | `skills/documentation/context-and-decisions/SKILL.md` |
| 文档候选检索（只提供线索，仍需判读正文） | `scripts/find-doc-impact.py`；使用与限制见 `skills/engineering/change-impact/SKILL.md` |
| 变更影响分析 | `skills/engineering/change-impact/SKILL.md` |
| 文档影响的接口变更复跑与验收 | `skills/engineering/change-impact/examples/interface-change.md`；生成器在 `tests/fixtures/document-impact.py`，记录见 `TESTS.md` 的 TEST-IMPACT-001 |
| 契约方法论（含两种模式） | `skills/engineering/contract-first/SKILL.md` |
| 测试资产与必要测试点治理 | `skills/engineering/test-collaboration/SKILL.md` |
| 测试协作的原始方案、确认与评审历史 | [2026-07-12 历史方案](docs/archive/2026-07-12-test-collaboration-proposal.md)；当前方法仍看 Skill |
| 本插件实际测试资产、测试目的与缺口 | `TESTS.md` |
| 模块联动回归方法论 | `skills/engineering/module-regression/SKILL.md` |
| 架构文档的必要性判断、生成与审查 | `skills/documentation/architecture-docs/SKILL.md` |
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
| 项目健康静态证据 | `scripts/collect-project-health.py`；范围、结果解释与专项衔接见 `skills/documentation/living-docs-governance/supporting-files/project-health.md` |
| 文档确定性审计 | `scripts/audit-docs.py`（`scripts/audit-cheap.sh` 是入口） |
| 审计结果与 JSON 接口 | `references/audit-result-format.md` |
| 日志共享解析与格式错误 | `scripts/logformat.py`（审计和索引共用） |
| PROJECT_LOG 归档与索引 | `scripts/project-log-index.py` |
| 插件自身架构决策 | `docs/adr/README.md` |
| 早期上游贡献研究 | [Wayfinder 决策生命周期](research/2026-07-22-wayfinder-decision-lifecycle.md)、[Map 与长文档治理](research/2026-07-22-map-long-docs.md)；结论对应文内日期和快照 |

## 易误读（别混）

- `templates/*.example.md` 是给**用户项目**套用的空白模板，**不是本插件自己的治理文件**。本插件自己的治理文件是根目录的 `CLAUDE.md` / `CLAUDE_MAP.md` / `PROJECT_STATUS.md` / `PROJECT_LOG.md`，按需再加 `ARCHITECTURE.md` 等载体（无 `.example` 后缀）。
- `.codex-plugin/plugin.json` 与 `.claude-plugin/plugin.json` 是不同宿主的安装入口，名称和版本必须一致；方法论仍只在 `skills/` 维护。
- 根目录 `AGENTS.md` 只负责让 Codex 进入共享 `CLAUDE.md` 章程，不是第五份治理文档。
- `.governance/project-log.sqlite` 是从 Markdown 日志重建的本地派生索引，默认忽略；不能当项目排期或历史唯一来源。
