# TESTS.md — docs-governance 测试资产与必要测试点

> 本文件回答三个问题：项目已经有哪些测试、每组测试为什么存在、证据从哪里运行。
> 测试代码仍是可执行事实；这里按能力和风险聚合，不手抄每个测试函数。
> 最近一次全量盘点：2026-09-05。

## 一、测试入口

首次开发先准备隔离环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

仅机器契约模板测试使用第三方校验库；插件的审计、日志和提醒脚本仍只用标准库。


| 执行组 | 命令 | 何时运行 | 外部依赖 |
|---|---|---|---|
| 默认验证 | `bash scripts/verify.sh` | 改任何文件后、提交前、CI | Bash、Python、Git、开发测试依赖 |
| Python 测试 | `python3 -m unittest discover -s tests -p 'test_*.py'` | 修改 `scripts/*.py` 或 `tests/*.py` 后 | Python、Git、开发测试依赖 |
| 文档确定性审计 | `bash scripts/audit-cheap.sh full` | 治理文档或引用变化后 | Bash、Python、Git |
| 空项目初始化 E2E | 按 `commands/governance-init.md` 在临时空仓执行 | 初始化流程或模板变化后 | Git；由 Claude Code / Codex 执行流程 |

## 二、测试资产地图

受控层级：`单元`、`集成`、`契约`、`E2E`、`冒烟`。

受控用途：`规则保护`、`关键链路`、`回归保护`、`专项保护`。

| 模块或流程 | 层级 | 用途 | 为什么存在 / 保护风险 | 执行组 | 外部依赖 | 测试位置 | 当前判断 |
|---|---|---|---|---|---|---|---|
| 文档确定性审计 | 集成 | 规则保护、回归保护 | 防止断链、ADR 漏登记、TEST-ID 漂移和 LOG 历史被悄悄改写 | Python 测试 | 临时目录、Git | `tests/test_audit_docs.py` | 必要 |
| PROJECT_LOG 归档与索引 | 集成 | 规则保护、回归保护 | 防止按行误计数、重复建库、未确认归档或归档丢事件 | Python 测试 | SQLite、临时目录 | `tests/test_project_log_index.py` | 必要 |
| 双 Agent 文档评审循环 | 集成 | 回归保护 | 防止正文未变化时重复付费评审，或评审状态无法落盘 | Python 测试 | fake Claude / Codex 命令 | `tests/test_dual_agent_review_loop.py` | 必要 |
| 插件结构与发布前验证 | 冒烟 | 关键链路 | 防止 manifest、hook、Skill 路由、路径引用或 Python 测试断裂后仍被发布 | 默认验证 | Bash、Python、Git | `scripts/verify.sh` | 必要 |
| 空项目治理初始化 | E2E | 关键链路 | 防止 `/governance-init` 只在文案上成立，实际生成空壳、漏 hook 或无法首提 | 空项目初始化 E2E | Git、宿主 Agent | `commands/governance-init.md` | 必要 |
| 首次接入命令适配 | 冒烟 | 关键链路、回归保护 | 防止 `/governance-setup` 脱离共享方法论，或被误用为日常维护／空项目初始化 | 默认验证 + 文本场景审阅 | Bash、Git、宿主 Agent | `commands/governance-setup.md`、`scripts/verify.sh` | 必要 |
| 机器契约模板 | 契约 | 规则保护、回归保护 | 防止模板不可解析，或序列化后的字段名、ID、枚举和时间错误被放过 | Python 测试 | jsonschema、openapi-spec-validator | `tests/test_contract_template.py` | 必要 |
| Stop hook 行为 | 集成 | 回归保护 | 防止提醒脚本误阻断会话，或漏报相对时间和未记 LOG | 待补 | Bash、Git | `hooks/check-on-stop.sh` | 缺失 |

当前汇总：必要 7 项，缺失 1 项，疑似重复 0 项，疑似废弃 0 项。

## 三、跨端契约证据

本项目不包含需要联调的前后端或多服务接口，当前不适用。Claude Code 与 Codex 的插件发现边界由双端 manifest 和 `scripts/verify.sh` 校验，不把它伪装成业务接口契约测试。

## 四、必要测试点

### TEST-AUDIT-001：确定性文档审计拒绝可机械证明的漂移

- 状态：已覆盖
- 用途：规则保护、回归保护
- 来源：`skills/living-docs-governance/SKILL.md` 的“便宜层先判”规则及 `references/audit-result-format.md` 的结果接口；2026-08-13 发现的 TEST-ID 误识别和删除区越界两项 Bug
- 模拟输入：临时项目中的断链、漏登记 ADR、未登记 TEST-ID、ARCHITECTURE 路径断裂、LOG 归档、示例 TEST-ID 和 P0 中的现存路径
- 业务预期：文档违规退出码 1，执行失败为 2，无确定性失败或执行错误为 0；文字与 JSON 复用同一结果，未验证及提示保持可识别；历史事件原样进入归档时仍判为只追加
- 层级：集成
- 执行组：Python 测试
- 边界：真实文件系统和 Git；不调用外部网络
- 测试文件：`tests/test_audit_docs.py`
- 测试节点：`AuditDocsTest`
- 执行命令：`python3 -m unittest tests.test_audit_docs -v`
- 证据：2026-09-05 使用真实 STATUS 模板复现删除区漏报/替代物误报、提交后历史改写、可选桥接误报和引用式断链；增加独立目录审计、JSON / Shell 结果、Git 上下文、读取失败、日志来源行号，以及损坏 Git、子项目基线和循环链接回归，见 `docs/audits/2026-09-05-shared-audit-results.md`。

### TEST-LOG-001：日志索引可重建且受控归档不丢事件

- 状态：已覆盖
- 用途：规则保护、回归保护
- 来源：`docs/adr/0001-project-log-sqlite-index.md`
- 模拟输入：20、201 条日志事件，含路径、TEST-ID 引用及多行中文和代码块详情
- 业务预期：按标准格式事件计数；错误事件格式失败且原文不变；重复重建幂等；未确认不归档；确认后活跃与归档事件合计不变
- 层级：集成
- 执行组：Python 测试
- 边界：真实 SQLite 与临时文件系统；无外部服务
- 测试文件：`tests/test_project_log_index.py`
- 测试节点：`ProjectLogIndexTest`
- 执行命令：`python3 -m unittest tests.test_project_log_index -v`
- 证据：2026-09-05 实跑通过，新增真实 Git 基线下多行事件归档后完整性审计，见 `docs/audits/2026-09-05-shared-audit-results.md`

### TEST-REVIEW-001：双 Agent 评审只在正文变化后重新运行

- 状态：已覆盖
- 用途：回归保护
- 来源：`TEST_COLLABORATION_PROPOSAL.md` 的双 Agent 讨论调度需求
- 模拟输入：首次评审、正文未变化、正文变化、评审期间正文被编辑或文件被删除
- 业务预期：首次调用双方；未变化时跳过；变化后重跑。评审期间编辑或删除时停止写回，不保存过期通过状态；新正文可重新评审。
- 层级：集成
- 执行组：Python 测试
- 边界：Claude / Codex 使用本地 fake 命令，不验证真实模型质量或认证
- 测试文件：`tests/test_dual_agent_review_loop.py`
- 测试节点：`DualAgentReviewLoopTest`
- 执行命令：`python3 -m unittest tests.test_dual_agent_review_loop -v`
- 证据：2026-09-05 实跑通过，见 `docs/audits/2026-09-05-governance-fixes.md`

### TEST-VERIFY-001：发布前入口覆盖插件结构与全部单测

- 状态：已覆盖
- 用途：关键链路
- 来源：`CLAUDE.md` 的提交前硬规则
- 模拟输入：当前插件工作区
- 业务预期：JSON、双端 manifest、hook 权限、Skill 路由、路径引用、忽略规则、Python 编译、单测、契约模板和 full 文档审计全部通过才返回 0
- 层级：冒烟
- 执行组：默认验证
- 边界：只检查仓库内确定性资产；语义正确性仍由审计和评审负责
- 测试文件：`scripts/verify.sh`
- 测试节点：十段结构验证
- 执行命令：`bash scripts/verify.sh`
- 证据：2026-09-05 本地标准入口包含 full 审计；`.github/workflows/verify.yml` 对推送前提交和 PR 基线做日志比较，远端结果见对应 PR checks。

### TEST-INIT-001：空项目初始化能形成最小、可提交的治理骨架

- 状态：开发中
- 用途：关键链路
- 来源：`commands/governance-init.md` 与 `PROJECT_STATUS.md` 原未决 P0
- 模拟输入：无业务代码的临时 Python 项目，项目名 `governance-init-smoke`
- 业务预期：生成 `CLAUDE.md`、`AGENTS.md`、`{目标项目}/docs/governance.md`、`PROJECT_LOG.md` 和可执行 pre-commit hook；不生成空壳 MAP、STATUS、ARCHITECTURE、TESTS 或 REGRESSION；首提成功
- 层级：E2E
- 执行组：空项目初始化 E2E
- 边界：当前 Codex 已按共享流程真实生成并提交；Claude Code 原生 slash command 的联网调用因未获得私有仓库数据出境授权而未执行
- 测试文件：`commands/governance-init.md`
- 测试节点：完整 day-0 流程
- 执行命令：按 `commands/governance-init.md` 在临时 Git 仓执行
- 证据：`docs/audits/2026-08-13-governance-init-empty-project.md`；2026-09-05 按更新后的 Skill 复跑，见 `docs/audits/2026-09-05-governance-fixes.md`

### TEST-SETUP-001：已有项目首次接入在确认前不写入，且命令只委托共享方法论

- 状态：已覆盖（结构）；宿主端到端待试点
- 用途：关键链路、回归保护
- 来源：`skills/living-docs-governance/SKILL.md` 的“已有项目首次接入”模式
- 模拟输入：已有规则、Tracker、hook 与部分治理文档的项目；以及尚无治理文档的已有代码项目
- 业务预期：先只读探测并分别列出保留、建议写入和明确不创建；未确认不写入，确认后仅修改获准载体；不替换 Tracker、hook 或团队规则；`/governance-setup` 与 `/governance-init`、`/governance` 职责分开
- 层级：冒烟
- 执行组：默认验证 + 文本场景审阅
- 边界：`scripts/verify.sh` 检查每个 command 都显式委托现有共享 Skill；它不能实际加载 Claude Code slash command，宿主调度与业务项目端到端接入待真实试点
- 测试文件：`commands/governance-setup.md`、`skills/living-docs-governance/SKILL.md`、`scripts/verify.sh`
- 测试节点：命令适配完整性与首次接入流程场景
- 执行命令：`bash scripts/verify.sh`

### TEST-HOOK-001：Stop hook 只提醒、不误阻断

- 状态：待补
- 用途：回归保护
- 来源：`hooks/check-on-stop.sh` 的提醒型边界
- 模拟输入：无治理文件、有相对时间、当天无 LOG、当天已有 LOG 四种临时仓状态
- 业务预期：需要时输出提醒，不需要时静默；所有提醒场景都保持退出码 0
- 层级：集成
- 执行组：待补
- 边界：真实 Bash 和临时目录；不调用宿主应用
- 测试文件：待补
- 测试节点：待补
- 执行命令：待补
- 证据：待补

### TEST-CONTRACT-TEMPLATE-001：同一机器契约校验响应边界

- 状态：已覆盖
- 用途：规则保护、回归保护
- 来源：`skills/contract-first/SKILL.md` 的机器契约单源规则
- 模拟输入：OpenAPI 模板和经 JSON 序列化的订单响应；字段改名、数字 ID、非法枚举、时间和金额精度
- 业务预期：标准 OpenAPI 校验通过；合法响应通过；非法响应被同一机器定义拒绝
- 层级：契约
- 执行组：Python 测试
- 边界：真实 OpenAPI / JSON Schema 标准校验器；不启动消费方或提供方服务，不证明业务联调
- 测试文件：`tests/test_contract_template.py`
- 测试节点：`ContractTemplateTest`
- 执行命令：`python3 -m unittest tests.test_contract_template -v`
- 证据：`templates/openapi.example.json` 被同一套测试加载并校验

## 五、人工验收出口

| 来源 | 无法自动化的理由 | 人工步骤 | 通过证据 | 负责人 |
|---|---|---|---|---|
| `diagram/architecture.svg` | 文字溢出、层级清晰度和视觉密度不能仅靠退出码判断 | 渲染 PNG，检查边界、文字、箭头、图例及与 `ARCHITECTURE.md` 的一致性 | `diagram/architecture.png` | 当前变更执行者 |

## 六、本轮缺口与动作

| 优先级 | TEST-ID 或资产 | 缺口 | 下一步 | 状态 |
|---|---|---|---|---|
| P1 | TEST-HOOK-001 | Stop hook 只有可执行权限检查，没有行为回归测试 | 增加临时仓 Shell 集成测试并接入默认 runner | 待补 |
| P2 | TEST-INIT-001 | Codex 共享流程已跑通，Claude Code 原生命令尚未执行 | 获得明确的数据出境授权后，用当前插件目录在临时空仓复跑 | 开发中 |

## 七、维护触发器

- 测试目录、配置、CI 或标准入口变化：重扫受影响区域。
- 新增需求、规则、风险或 Bug：新增或关联 TEST-ID。
- 修改审计、日志索引、评审循环或 hook：更新对应 TEST-ID 并重跑默认验证。
- 阶段交付前：核对本次涉及的 TEST-ID、命令退出码和人工证据。
- 只有测试体系整体重构或地图明显失真时，才重新全量盘点。
