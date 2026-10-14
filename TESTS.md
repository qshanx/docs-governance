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
| 面向 AI 的文档写作试跑 | 按 writing-for-agents 在隔离目录改写 Skill，核对结构、读取指针与含义；另做只读审查 | 写作 Skill 或调用边界变化后 | 宿主 Agent；不需联网 |
| setup 场景执行 | 按 `living-docs-governance` 统一 setup 在三个隔离项目执行，并复跑与只读探测 | 编排、初始化流程或模板变化后 | 宿主 Agent；不需联网或 Git 初始化 |
| 文档影响场景审查 | [接口变更场景](skills/engineering/change-impact/examples/interface-change.md) | 按事实核对文档的方法变化后 | 当前 Agent、Python、隔离 Git；无外部业务服务 |

## 二、测试资产地图

受控层级：`单元`、`集成`、`契约`、`E2E`、`冒烟`。

受控用途：`规则保护`、`关键链路`、`回归保护`、`专项保护`。

| 模块或流程 | 层级 | 用途 | 为什么存在 / 保护风险 | 执行组 | 外部依赖 | 测试位置 | 当前判断 |
|---|---|---|---|---|---|---|---|
| 文档确定性审计 | 集成 | 规则保护、回归保护 | 防止断链、ADR 漏登记、TEST-ID 漂移和 LOG 历史被悄悄改写 | Python 测试 | 临时目录、Git | `tests/test_audit_docs.py` | 必要 |
| Agent 入口长度 | 集成 | 规则保护 | 防止 200 行边界误判、多文件漏检及读取失败被当成通过 | Python 测试 | 临时目录 | `tests/test_entrypoint_length.py` | 必要 |
| PROJECT_LOG 归档与索引 | 集成 | 规则保护、回归保护 | 防止按行误计数、重复建库、未确认归档或归档丢事件 | Python 测试 | SQLite、临时目录 | `tests/test_project_log_index.py` | 必要 |
| 双 Agent 文档评审循环 | 集成 | 回归保护 | 防止正文未变化时重复付费评审，或评审状态无法落盘 | Python 测试 | fake Claude / Codex 命令 | `tests/test_dual_agent_review_loop.py` | 必要 |
| 插件结构与发布前验证 | 冒烟 | 关键链路 | 防止 manifest、hook、Skill 路由、路径引用或 Python 测试断裂后仍被发布 | 默认验证 | Bash、Python、Git | `scripts/verify.sh` | 必要 |
| init 兼容入口 | 冒烟 | 回归保护 | 防止旧命令残留另一套初始化流程或隐含 Git／hook 授权 | 默认验证 + 适配层审阅 | Bash、宿主 Agent | `commands/governance-init.md` | 必要 |
| 统一 setup 编排 | 集成 | 关键链路、回归保护 | 防止只写入口空模板、丢失 PRD／Spec 主源、越权写入或重复建档 | 默认验证 + setup 场景执行 | Python、宿主 Agent、隔离文件系统 | `commands/governance-setup.md`、`skills/documentation/living-docs-governance/SKILL.md` | 必要 |
| 面向 AI 的文档写作试跑 | 按 writing-for-agents 在隔离目录改写 Skill，核对结构、读取指针与含义；另做只读审查 | 写作 Skill 或调用边界变化后 | 宿主 Agent；不需联网 |
| 机器契约模板 | 契约 | 规则保护、回归保护 | 防止模板不可解析，或序列化后的字段名、ID、枚举和时间错误被放过 | Python 测试 | jsonschema、openapi-spec-validator | `tests/test_contract_template.py` | 必要 |
| 文档位置、暂存护栏与 Stop | 集成 | 规则保护、回归保护 | 防止错放漏报、正文误报、未暂存修复掩盖提交、缓存重复或钩子误阻断 | Python 测试 | Bash、临时 Git | `tests/test_document_policy.py` | 必要 |
| PR 前扫描、推送门禁与文档影响样例 | 集成 | 规则保护、关键链路 | 防止工作区修复掩盖提交、漏掉变更影响或失败仍能推送；保留可复跑的语义审查输入 | Python 测试 + 文档影响场景审查 | 本地临时 Git、bare remote、jsonschema | `tests/test_pr_docs.py`、`tests/fixtures/document-impact.py` | 必要 |
| PR 审核工作流 | 集成 | 关键链路、回归保护 | 核对受检版本、完整路径、隔离行为证据及审核权限，区分工作区修复、旧 CI 与当前结论 | 隔离实际任务试用 + 默认验证 | 宿主 Agent、Python、临时 Git；不需业务账号 | `skills/engineering/pr-review/SKILL.md`、本节 TEST-PR-REVIEW-001 | 必要 |

当前汇总：必要 12 项，缺失 0 项，疑似重复 0 项，疑似废弃 0 项。

## 三、跨端契约证据

本项目不包含需要联调的前后端或多服务接口，当前不适用。Claude Code 与 Codex 的插件发现边界由双端 manifest 和 `scripts/verify.sh` 校验，不把它伪装成业务接口契约测试。

## 四、必要测试点

### TEST-AUDIT-001：确定性文档审计拒绝可机械证明的漂移

- 状态：已覆盖
- 用途：规则保护、回归保护
- 来源：`skills/documentation/living-docs-governance/SKILL.md` 的“便宜层先判”规则及 `references/audit-result-format.md` 的结果接口；2026-08-13 发现的 TEST-ID 误识别和删除区越界两项 Bug
- 模拟输入：临时项目中的断链、漏登记 ADR、未登记 TEST-ID、ARCHITECTURE 路径断裂、LOG 归档、示例 TEST-ID 和 P0 中的现存路径
- 业务预期：文档违规退出码 1，执行失败为 2，无确定性失败或执行错误为 0；文字与 JSON 复用同一结果，未验证及提示保持可识别；历史事件原样进入归档时仍判为只追加
- 层级：集成
- 执行组：Python 测试
- 边界：真实文件系统和 Git；不调用外部网络
- 测试文件：`tests/test_audit_docs.py`
- 测试节点：`AuditDocsTest`
- ADR 兼容回归：轻量无状态／无索引记录、上下文子目录、忽略目录、显式非法／空状态、编号替代目标和无索引断链；旧索引漏登及 Supersedes 目标保护继续保留。对应 2026-10-12 的 domain-modeling 复用授权。
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
- 来源：[测试协作历史方案](docs/archive/2026-07-12-test-collaboration-proposal.md)的双 Agent 讨论调度需求
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

### TEST-INIT-001：init 兼容入口委托统一 setup

- 状态：结构已覆盖；当前宿主原生命令待验证
- 用途：关键链路
- 来源：`commands/governance-init.md`、能力规格 GSU-1；替代旧 day-0 独立流程
- 模拟输入：与 setup 相同的目标、材料与授权参数
- 业务预期：与 setup 委托同一模式、角色与参数，未保留旧独立流程；不隐含 Git 初始化、首提或 hook 安装
- 层级：冒烟
- 执行组：默认验证 + 适配层审阅
- 边界：核对命令与 Skill 结构，不等于 Claude Code 已加载命令；旧空项目首提证据不证明新流程通过
- 测试文件：`commands/governance-init.md`
- 测试节点：兼容入口与 GSU-1
- 执行命令：`bash scripts/verify.sh`，人工比较 init 与 setup 适配层
- 证据：当前验证见 [r7 测试记录](docs/product/09-test-release.md)；旧流程历史证据保留在 `docs/audits/2026-08-13-governance-init-empty-project.md` 与 `docs/audits/2026-09-05-governance-fixes.md`

### TEST-SETUP-001：统一 setup 按约定范围接通资料与 Agent 入口

- 状态：r7 仅证明当时产品包场景，保留历史范围；新版按需 setup 的宿主端到端待试点
- 用途：关键链路、回归保护
- 来源：`skills/documentation/living-docs-governance/SKILL.md` 的“统一 setup”模式及能力规格 GSU-1—GSU-5
- 模拟输入：仅目标／范围的新项目；有确认记录但未实现的项目；有 AGENTS 主源、现有 Spec、测试与 hook 的项目；后者再复跑和只读探测；另用未配置项目验证“仅建议、不写入”
- 业务预期：本次需要的主记录、导航、状态与维护入口接通；产品包和十阶段导航仅为按需子场景；必要步骤标明完成／不适用／待处理／未验证及依据，保留来源、主源与未知项；不覆盖规格、Tracker、代码或 hook；每份入口 ≤200 行；复跑不重复建档，只读前后文件不变
- 层级：集成
- 执行组：默认验证 + setup 场景执行
- 边界：实际 Agent 读取 Skill 并在隔离目录生成文档，运行显式目标根审计与行数检查；不验证 Claude Code slash command 加载、业务项目推广或业务验收
- 测试文件：`commands/governance-setup.md`、`skills/documentation/living-docs-governance/SKILL.md`、`scripts/verify.sh`
- 确定性复核（2026-10-12）：隔离 Git 项目中，未采用 LOG 返回 0；策略要求 LOG 却缺失、断链、删除已提交 LOG 历史分别返回 1；四例前后文件哈希不变。此结果不代表宿主 setup 行为通过。
- 测试节点：三场景、重复执行、只读权限和受保护文件
- 执行命令：`bash scripts/verify.sh`；按共享 Skill 逐场景执行并比较文件哈希，证据见 [r7 测试记录](docs/product/09-test-release.md)

### TEST-HOOK-001：位置与触发规则在真实文件和暂存快照上生效

- 状态：已覆盖
- 用途：规则保护、回归保护
- 来源：[文件护栏约定](references/document-policy.md)、[产品文档规格](docs/product/06-prd.md)
- 模拟输入：PRD 主标题错放、正文与围栏提及、模板例外、脚本错放、缺失文件、错误配置、软链接、暂存区未修复而工作区已修复、变更及重复 Stop
- 业务预期：按约定返回确定性失败／执行错误，暂存违规阻止提交，Stop 只报告；通过且内容不变时静默，不以配置错误冒充通过
- 层级：集成
- 执行组：Python 测试
- 边界：真实临时文件、Git 暂存区和 Bash；不验证宿主是否实际派发事件，也不代替语义审查
- 测试文件：`tests/test_document_policy.py`
- 测试节点：`DocumentPolicyTest`
- 执行命令：`python3 -m unittest discover -s tests -p 'test_document_policy.py' -v`
- 证据：2026-09-22 本地 13 个行为场景通过；整体 54 个测试及 verify 通过，见 [测试记录](docs/product/09-test-release.md)
- 2026-09-23 追加 8 个根定位回归：同配置／缓存、子项目优先、显式根及无效根、嵌套 Git 边界、非 Git 与旧四件套、直接 CLI、损坏配置及 linked worktree。验证真实 Bash 钩子和审计器，不代替宿主事件验证。

### TEST-PR-001：PR 前扫描检查真实来源提交并阻断失败推送

- 状态：已覆盖
- 用途：关键链路、规则保护
- 来源：[PR 护栏约定](references/document-policy.md)
- 模拟输入：代码变更、删除／重命名、关联文档缺失、已提交断链及未提交修复、日志改写、错误基线和本地 bare remote
- 业务预期：扫描 PR 共同祖先到来源提交的完整差异，映射文档并执行 full 审计；失败阻止推送，修复后放行，不修改源仓库 index 与 HEAD
- 层级：集成
- 执行组：Python 测试
- 边界：临时 Git、真实 pre-push、linked worktree；不验证远端必需检查配置，不判定业务语义
- 测试文件：`tests/test_pr_docs.py`
- 测试节点：`PrDocsTest`
- 执行命令：`python3 -m unittest tests.test_pr_docs -v`
- 证据：2026-09-22 10 个集成测试通过，全套 64 个通过，见 [测试记录](docs/product/09-test-release.md)
- 2026-09-28 追加 3 个安装回归，13 个集成测试通过：真实推送覆盖旧分支、linked worktree 与断链拦截；已有 hook 默认保留、明确替换先备份，外部 hooksPath 可用、工作树内路径被拒绝。

### TEST-CONTRACT-TEMPLATE-001：同一机器契约校验响应边界

- 状态：已覆盖
- 用途：规则保护、回归保护
- 来源：`skills/engineering/contract-first/SKILL.md` 的机器契约单源规则
- 模拟输入：OpenAPI 模板和经 JSON 序列化的订单响应；字段改名、数字 ID、非法枚举、时间和金额精度
- 业务预期：标准 OpenAPI 校验通过；合法响应通过；非法响应被同一机器定义拒绝
- 层级：契约
- 执行组：Python 测试
- 边界：真实 OpenAPI / JSON Schema 标准校验器；不启动消费方或提供方服务，不证明业务联调
- 测试文件：`tests/test_contract_template.py`
- 测试节点：`ContractTemplateTest`
- 执行命令：`python3 -m unittest tests.test_contract_template -v`
- 证据：`templates/openapi.example.json` 被同一套测试加载并校验

### TEST-IMPACT-001：事实变化后的文档核对

- 状态：样例自动回归通过；当前 Codex 已知场景语义复核通过，独立盲测与业务试点未验证
- 用途：规则保护、回归保护
- 来源：[Issue #5](https://github.com/qshanx/docs-governance/issues/5#issuecomment-6075874052)；本轮授权实施接口字段变化切片
- 模拟输入与预期：见唯一的 [场景与验收清单](skills/engineering/change-impact/examples/interface-change.md)，不在台账复制逐项规则
- 层级：集成；执行组：Python 测试 + 文档影响场景审查
- 边界：真实文件、Git 与序列化响应；合成接口不启动 HTTP 服务。单测只证明样例和确定性边界，语义结论必须由实际 Agent 核对，已知场景不当作盲测
- 测试文件：[生成器](tests/fixtures/document-impact.py)、[自动回归](tests/test_pr_docs.py) 的 `DocumentImpactFixtureTest`
- 执行命令：`python3 -m unittest tests.test_pr_docs.DocumentImpactFixtureTest -v`；Agent 执行方式见场景入口
- 证据：2026-10-09 新增 3 项回归通过，标准 `scripts/verify.sh` 通过（82 项单测）。当前 Codex 以 `6999501892de87a6446610aba1306857f2e0a22f` 为样例基线，分别审查 interface 的 `cf7a0b2f9afa6a4a13164fe145b91a0073d5a13f` 与 internal 的 `81bcb6a411e6e4367953ed0b4d70fdd493933be4`；这些是隔离样例提交，复跑时使用新输出的 SHA。
- 语义复核：定位三份指南第 3 行的旧调用（含映射外说明），以及 FAQ 第 3 行对当前决定的复制；三类反例与内部修复均无需改写。执行旧订单调用报 `KeyError: 'total'`，库存同名字段正常；两例回执输入哈希均匹配。范围为两份样例的真实 diff、入口、相关文档及其契约／实现／回执，修改样例文件 0 份；语义审查耗时未计量。
- 局限：执行者参与构造且已读验收清单，本次只证明已知切片可执行，不证明方法修改带来检出率提升。原始发现及后续交付记录沿上述 Issue 引用，不复制测试回执；真实业务项目试点尚未开展。

候选检索的自动化覆盖见 `tests/test_doc_impact.py`：接口变化及反例候选、提交快照与工作区隔离、同标识符行为变化、删除路径／跳过文件／无效基线。外部插件绝对路径及真实缺失路径由 `tests/test_audit_docs.py` 验证。检索退出 0 只表示完成，不代表文档全部正确。

2026-10-10 隔离试验：独立 Agent 只收到“导出默认脱敏”的功能要求，从项目入口进入完整流程，查到默认调用与显式关闭脱敏的两个消费者；基线 4 项通过，新增后先失败再修复，最终 7 项通过，主执行者复跑通过。API／用法／Spec／客服说明四份同步，历史／账单／纯引用三份未改；无回归台账也完成本轮验证。临时项目未进入正式仓库。此前维护单独试验还验证了真实断链时停止候选检索和文档同步。以上仅为隔离样例，未验证真实业务成本、原生宿主强制触发或跨模型稳定性。

示例与命令验证：`python3 -m unittest tests.test_doc_examples -v` 直接读取隔离样例的三处行内调用和一条文档命令。接口变更后四处均失败，只修临时副本文档后四处通过；内部重构无需改文档；退出 0 但输出错误也会判失败。实现、契约和历史哈希保持不变。范围为本地 Python 示例，不覆盖 HTTP／部署。复跑说明见 [接口样例](skills/engineering/change-impact/examples/interface-change.md#示例与命令验证)。

### TEST-WRITING-001：技术表达改写保持含义与只读边界

- 用途：回归保护
- 来源：[能力规格 r8](docs/product/06-prd.md#r8技术文档表达)，TWR-2、TWR-3
- 层级：集成；实际 Agent 执行共享 Skill，不代替宿主自动发现
- 输入：本仓库真实技术文档的隔离副本；另以只读请求检查指定文档
- 预期：保持语言、事实、结构、代码、链接、条件、例外和要求强度；只读场景文件哈希不变
- 执行：独立 Agent 读取新 Skill 后按真实请求执行，执行者和审阅者分开；原文件与临时产物逐项比较
- 证据与实际结果：[r8 测试记录](docs/product/09-test-release.md#r8技术文档表达2026-10-05)
- 未验证：宿主跨会话发现、Claude Code 原生调用和业务项目使用效果

## 五、人工验收出口

| 来源 | 无法自动化的理由 | 人工步骤 | 通过证据 | 负责人 |
|---|---|---|---|---|
| `diagram/architecture.svg` | 文字溢出、层级清晰度和视觉密度不能仅靠退出码判断 | 渲染 PNG，检查边界、文字、箭头、图例及与 `ARCHITECTURE.md` 的一致性 | `diagram/architecture.png` | 当前变更执行者 |
| TEST-IMPACT-001 | 当前说明、历史与无关同名字段的判别不由确定性脚本代判 | 按接口变更场景交给 Agent 只读审查，再对照验收清单 | 见该测试点的语义复核与局限 | 当前变更执行者 |

## 六、本轮缺口与动作

| 优先级 | TEST-ID 或资产 | 缺口 | 下一步 | 状态 |
|---|---|---|---|---|
| P2 | TEST-HOOK-001 | 脚本行为已验证，宿主原生 Stop 事件派发仍需真实会话观察 | 插件加载后核对实际触发与提示 | 待验证 |
| P2 | TEST-INIT-001、TEST-SETUP-001 | 统一 setup 与 init 的 Claude Code 原生命令加载尚未执行 | 获得适用授权后，在宿主加载插件并用无私有数据的临时项目复跑 | 待验证 |
| P2 | TEST-IMPACT-001 | 未做独立盲测、真实业务项目成本与漏报评估 | 沿 Issue #5／#10 做只读试点，区分确定性结果与语义发现 | 待验证 |

## 七、维护触发器

- 测试目录、配置、CI 或标准入口变化：重扫受影响区域。
- 新增需求、规则、风险或 Bug：新增或关联 TEST-ID。
- 修改审计、日志索引、评审循环或 hook：更新对应 TEST-ID 并重跑默认验证。
- 阶段交付前：核对本次涉及的 TEST-ID、命令退出码和人工证据。
- 只有测试体系整体重构或地图明显失真时，才重新全量盘点。

### TEST-HEALTH-001：项目健康证据采集边界

- 状态：已覆盖；静态证据不代表真实业务验证。
- 用途：防止体检越界、隐式执行项目命令、空壳检查与旧结果被误当通过。
- 测试位置：`tests/test_project_health.py`；采集器为 `scripts/collect-project-health.py`。
- 覆盖：无 Makefile 的脚本入口与 CI 字面对应、空壳提示与不执行、越界和符号链接、旧回执与会话排除、源文件指纹变化、缺失和无效记录、Make／package 候选、无效根、动态路径不误报、复合命令不误判空壳、Git filter 不被触发及显式会话路径拒绝。
- 执行：`python3 -m unittest discover -s tests -p test_project_health.py`；项目实跑与独立复核见 [验证记录](docs/product/09-test-release.md)。

TEST-HEALTH-001 补充 PR #40 回归：直接脚本／根目录脚本／带空格路径在文档与 CI 中的采集、指纹与字面对应；纯赋值和环境前缀执行的区分；未知 CI 命令缺口；带引号越界与私有路径拒绝。专项共 20 项，含参数化场景，不执行 fixture 内的验证命令。

### TEST-RETRO-001：测试复盘定位原因并保持职责与只读边界

本条保留 TR-20261013 的历史测试记录；当前统一入口为 project-retro，测试检查面及经验生命周期的当前验证见 TEST-PROJECT-RETRO-001。

- 来源：[TR-20261013](docs/product/06-prd.md#tr-20261013测试复盘)。
- 状态：本地三个隔离场景已执行并由当前 Agent 复盘；独立盲测、宿主原生调用与业务项目效果未验证。
- 用途：专项保护；执行组为隔离场景与人工语义核对，不新增匹配 Skill 文案的单元测试。
- 模拟输入：正常输入测试全绿但漏负数；测试断言要求全大写但规格要求保留大小写；已有负数检查未被默认 runner 收集。
- 预期：从规格、测试与运行证据定位原因，提出具体修改草稿和验证办法；缺少检查时补候选，已有检查未执行时优先接通；目标文件不变，不直接修业务实现或扩成环境／文档管理复盘。
- 执行方式：在临时目录构造三个小项目，运行真实 unittest 与目标输入；当前 Agent 按 `test-retro` 复盘并核对前后 SHA-256。固定输入、结果与限制见[验证记录](docs/product/09-test-release.md#tr-20261013测试复盘验证)。

### TEST-PROJECT-RETRO-001：统一复盘与 lessons 生命周期

- 来源：[PR-20261013](docs/product/06-prd.md#pr-20261013统一项目复盘与经验生命周期)。
- 保护对象：环境、文档和测试回顾合并后仍从真实来源提炼经验；对话权限、事件去重、措施复验及升级主源边界保持。
- 执行组：隔离场景、当前 Agent 的语义执行与文件指纹核对；不以 Skill 文案匹配测试代替实际场景。
- 核对输入：对话中的纠正／Agent 自述、同一事故的 LOG 和 commit 引用；测试漏检、误报、未收集；单次复验与两个独立任务；反例、失效证据和升级权限。
- 预期：只有一个当前复盘入口，默认只读；来源同一事件合并，多次真实有效复验与授权落地后才能升级，候选经验与目标规则不持有两份现行正文；不足条件保留建议和缺口。
- 当前结果与运行证据见[统一复盘验证](docs/product/09-test-release.md#pr-20261013统一项目复盘验证)；旧 TEST-RETRO-001 保留原范围，不能替代新流程验证。
- 后续独立试用：新 Agent 实际完成只读提炼、反证退役、授权升级及真实项目只读复盘，写入白名单与仓库指纹检查通过；详见[独立试用](docs/product/09-test-release.md#pr-20261013独立-agent-功能试用)。这证明显式读取 Skill 的任务路径，不代表宿主自动发现或长期效果。
- PR-7 三次清单：独立 Agent 在四个隔离项目实际核对有效复验，分别首次交付清单、重复回执只计一次、取消 CI 不计第三次、已有相同清单不重发；只读文件指纹保持。详见[文案与三次清单验证](docs/product/09-test-release.md#pr-20261013文案与三次清单验证)。
- PR-8 保护输入：指定会话中的截断／重复检索、缺失日志、无效指令候选、已存在但未接通的 lint、没有执行保护的项目、规范与实现／审查交接。预期定位真实缺口、复用已有检查、区分候选与已证实，不因只读复盘安装或删改。当前场景执行结果见[检查点补全验证](docs/product/09-test-release.md#pr-20261013检查点补全与经验落盘)。

### TEST-PR-REVIEW-001：当前变更审核与执行证据

- 来源：[PRR-20261013](docs/product/06-prd.md#prr-20261013pr-审核)。
- 保护对象：固定 PR／分支的提交范围，按需求／规范和真实路径审核；隔离对照与当前版本证据对应，审核不越权修改目标或平台。
- 执行组：独立 Agent 的隔离 Git 实际任务与文件／index／HEAD／refs 指纹核对，插件结构及 full 文档审计；不以关键词匹配代替语义。
- 核对输入：已提交候选与工作区修复不同、只修一条公开入口、完整修复、base 前移、旧绿色／当前取消回执、缺需求及有外发副作用的检查脚本。
- 预期：定位真实缺陷和同类遗漏；正确实现也能给出有范围的结论。回退须是目标断言失败，恢复后通过；已审读且无外部副作用的本地检查在外置副本执行，未运行列出。旧回执或未提交修复不能证明当前 head，来源中的批准自述不授权外发、修复或合并。
- 真实平台 API、审核期间 head 前移、真实账号／跨平台行为和生产合并效果的覆盖以实际记录为准，不因隔离试用自动视为已测。
- 当前运行证据见[审核验证](docs/product/09-test-release.md#prr-20261013pr-审核验证)。
- PRR-8 改写保护：以相同原始 Git 候选重新完成实际审核，保留提交／工作区区分、关键反例、隔离证据与缺资料边界；交付三段报告且包含回退代价／影响面，不以固定模板文本匹配代替判断。当前结果见[简化验证](docs/product/09-test-release.md#prr-20261013简化思路与报告)。
- PRR-9 改写保护：独立方案形成先于候选代码读取；对明确缺陷给基于受检版本的建议 diff，检查补丁可应用性及相关行为，原 PR 阻塞与补丁结果分别判断；正确但实现不同不误报、缺规格不造规则。证据见[四步验证](docs/product/09-test-release.md#prr-20261013四步审核与建议补丁)。

### TEST-ENV-RETRO-001：环境建议与职责边界

- 来源：[ENV-RETRO-20261014](docs/product/06-prd.md#env-retro-20261014环境建议的七加四方向)，取代 TEST-PROJECT-RETRO-001 的普通复盘职责；旧经验生命周期结果仍保留其范围。
- 保护意图：让 Agent 从经历提出环境改进建议，保留七加四观察方向，不将提示误作安装清单或业务测试设计。
- 验证：Skill 格式、十一方向与已确认输入的含义核对、只读／专项边界审查、完整仓库检查；结果及未测范围见[环境建议验证](docs/product/09-test-release.md#env-retro-20261014环境建议验证)。
- 限制：静态与当前 Agent 核对不证明宿主加载、独立 Agent 行为或真实任务收益。
