# docs-governance

> 面向长期 AI 协作项目的知识、决策与验证治理系统。
>
> **把优秀 Agent 的一次性工作，沉淀为项目可继承、可验证、可持续演进的集体能力。**

它兼容 Claude Code、Codex 与 ChatGPT，不以增加文档数量为目标，而是让项目规则、架构、决策、测试理由与交付证据在多次任务、多个 Agent 和长期演进中持续可信。

> English README: [README.md](README.md) · 完整使用说明：[使用说明.md](使用说明.md) · 参与贡献：[CONTRIBUTING.md](CONTRIBUTING.md)

## 3 分钟试用

1. 在 Claude Code 中安装：

   ```text
   /plugin marketplace add Seekers2001/docs-governance
   /plugin install docs-governance@docs-governance
   ```

2. 在一个已有代码的项目中运行只读检查：

   ```text
   /governance-audit
   ```

   或在 Codex / ChatGPT 中输入：

   ```text
   $docs-governance 只读审计当前项目，并告诉我最该先补哪一项治理能力
   ```

3. 先看报告，不让工具直接改文件。确认后再用 `/governance` 或对应专项 Skill 更新文档。

这个插件的默认姿态是“**先审计、后决定、再修改**”：小项目不强塞四件套；已有项目也会尽量沿用现有的目录与事实来源。

## 为什么需要它

AI 让代码变得**便宜、可丢弃、可再生**。当写代码不再是瓶颈，承重的东西就上移到**意图（文档）**和**验证（测试）**——人维护的是规格和验收，代码只是规格的一次投影。

任务型工程 Skill 解决“这次怎样把事情做好”；docs-governance 解决“这次的正确做法怎样不随会话消失，而成为后续 Agent 可继承的项目能力”。

但这套范式有个最容易塌的地方：**文档会腐烂**。README 撒谎、架构图描述一次没上线的重构、AI 每次进会话都在重新摸索本该一读就懂的结构。**docs-governance 专门治这个腐烂。**

它和 Claude 生态里的 onboarding 类工具是**互补**的：`codebase-onboarding` 解决"第一次进场"，**本插件解决"几个月后那张图还为不为真"**——维护期的持续治理。

## 它怎么治

把项目文档当成一个**小系统**：四份各司其职、互不重叠的「脊柱」文档，加一套**分级读取协议**（不每次全读，省上下文），再把脊柱之外的所有文档按角色分层、按需读。

| 脊柱文档 | 唯一职责 | 进会话怎么读 |
|---|---|---|
| `CLAUDE.md` | 宪法：永久硬规则 + 指路牌 | 全文常驻 |
| `CLAUDE_MAP.md` | 地图：只记**文件树看不出来**的导航、误导清单与别动区 | 默认不读，改文件前必读 |
| `PROJECT_STATUS.md` | 健康仪表盘：指标 + 删除区 + P0 | 只有红线块常驻 |
| `PROJECT_LOG.md` | 流水账：只追加的历史 | 按需 grep |

> 关键纪律：**每个事实只有一个权威来源**（其他载体只引用）；脊柱只放索引和指路牌，细节下沉到对应层；"不读会悄悄出事"的红线常驻，其余按需。

当项目已有多个长期 Module，单靠地图不足以说明权责与流转时，按需增加独立的 `ARCHITECTURE.md`：它集中维护 Module 权责、状态唯一归属、允许/禁止依赖、代码依赖图和运行时核心流转图。`CLAUDE_MAP.md` 只保留一行入口；难回退选择的理由仍进入 ADR，Interface 字段仍进入 CONTRACT 或代码 Interface。

另配一条**契约式前后端协作**线（`contract-first`）：由 `CONTRACT.md` 指向一份前后端共用的机器契约，防字段漂移导致集成白屏——本质是轻量的**消费者驱动契约（CDC）/ 契约测试**，支持单会话多 agent 和多终端异步两种模式。

第三条线是**模块回归审计**（`module-regression`）：一份 `REGRESSION.md` 台账登记每个模块的下游消费者（脚本生成）和可执行的回归验收命令，改完照单跑"本模块+全部下游"，退出码终审——防大项目里"改一个模块悄悄弄坏其他模块"。

第四条线是**测试协作治理**（`test-collaboration`）：一份 `TESTS.md` 盘点现有测试资产，把需求、规则、风险和 Bug 登记成 TEST-ID，持续暴露必要、缺失、疑似重复和疑似废弃的测试。前后端或多服务分开开发时，同一个 TEST-ID 引用唯一机器可读契约，串起消费者、提供者和联调测试证据。它回答“应该测什么、为什么测、证据在哪”；`REGRESSION.md` 只回答“改完重跑什么”。

`docs-governance` 是 Codex/ChatGPT 的薄总路由：普通治理与当前 Module 架构进入活文档；稳定领域语言进入 `context-and-decisions` 的 `CONTEXT.md`；架构、数据库、认证、部署等难回退决定进入一项一文件的 ADR；改代码前后用 `change-impact` 核对代码、数据、契约、测试、文档、发布和回滚。

`product-evolution` 在 docs 下按十阶段组织产品管理文件，连接当前 PRD 基线、确认来源、执行任务与验收／运营证据；建立与审查均复用现有资料。本插件示例见 [产品管理入口](docs/product/README.md)。

插件还保留 `loop-design-check`：当任务本身需要设计可判定目标、反馈回路和停止条件时使用；它由总路由登记，但不把 loop 文档混入项目治理脊柱。

文档审计仍坚持“便宜层先判”：`scripts/audit-docs.py` 检查断链、ADR 索引、LOG 完整性、TEST-ID 和孤儿文档；确定性问题通过后，才由 agent 判断术语冲突、决策冲突、重复真相和成功标准证据。审计默认只读。

需要工具读取结果时，使用 `bash scripts/audit-cheap.sh full --format json`；同一结果提供检查范围、Git 信息、状态和证据，详见[审计结果接口](references/audit-result-format.md)。日志审计与归档索引共用 `scripts/logformat.py` 的事件解析规则。

`PROJECT_LOG.md` 按事件数治理：不超过 200 条只用 Markdown；超过后先复盘，经确认把旧事件原样归档，并生成 `.governance/project-log.sqlite` 本地派生索引。Markdown 始终是 Git 可读事实源；数据库可随时重建，也不负责项目排期。

## 项目文档怎么分层

| 层 | 建议载体 | 管什么 |
|---|---|---|
| 根脊柱 | `CLAUDE.md` / `CLAUDE_MAP.md` / `PROJECT_STATUS.md` / `PROJECT_LOG.md` | 规则、导航、当前健康、历史 |
| 可选根载体 | `ARCHITECTURE.md` / `CONTEXT.md` / `CONTRACT.md` / `TESTS.md` / `REGRESSION.md` | 当前架构、领域语言、接口、测试证据、下游回归 |
| 持久知识 | `docs/adr/` / `docs/specs/` / `docs/plans/` / `docs/audits/` / `docs/reviews/` / `docs/log-details/` / `docs/archive/` | 决策、规格、计划、产物和归档；有真实内容时才创建 |
| 任务与排期 | GitHub Issues / Linear / 现有 Tracker；无外部系统时可用 `.scratch/` | 负责人、状态、阻塞、项目 schedule |
| 机器投影 | `.governance/project-log.sqlite` | 大型 LOG 的分类与查询；默认 gitignored，可重建 |

`CLAUDE_MAP.md` 只负责告诉 agent“知识入口在哪里、哪些目录会骗人、哪些地方不能碰”。`ARCHITECTURE.md` 单独回答“关键 Module 谁负责什么、状态归谁、依赖与核心数据怎样流转”。依赖图和运行时流转图必须分开标注：数据可以往返，代码依赖仍尽量单向。

## 治理常见错误（dogfood 里反复撞到的）

| 错误 | 正确做法 |
|---|---|
| STATUS 撒谎（指标停在旧快照、说"无 git"其实早建了） | STATUS 只写量过的当前真相，旧事实移进 LOG |
| 血肉上浮：脊柱里混进目录树镜像 / 逐条历史 / 整篇产物 | 脊柱只留索引和指路牌，细节下沉到对应层 |
| CLAUDE_MAP 抄文件树或塞入完整架构图 | MAP 只做导航、误导清单和别动区；Module 权责与流程图放独立 `ARCHITECTURE.md` |
| 孤儿文档：有 `.md` 没人从脊柱指向它 | 挂上指路牌，否则没人读必烂 |
| 每次进会话全读四份，白占上下文 | 分级读：红线常驻，其余按需 |
| 一上来铺满四件套（小项目过度治理） | 渐进式采用，按预警信号上下一级 |
| 个人偏好塞进团队 `CLAUDE.md` | 放 `CLAUDE.local.md` / `~/.claude/` |

## 真实使用案例（dogfood，非演示）

| 项目 | 跑了什么 | 抓到什么 |
|---|---|---|
| 经营报表加工（324 个 .py） | `/governance-audit` | CLAUDE_MAP 长到 143 行、抄目录树、跟 STATUS 抢职责 |
| 礼仪课程 demo（59 个 .js，Node） | 审计 + 修复 | STATUS 三项指标漂移（style.css 标 443 实为 605）、6 个误导备份目录未标注、CLAUDE.md 指路牌指向废弃文件——全部修正，留有 git diff |
| 本插件自身 | 套自己的四件套 + `scripts/verify.sh` | 用自己的方法论治自己，结构自检全绿 |

### 审计输出长这样（节选改写自礼仪课程 demo 的真实审计记录）

```
/governance-audit

🔴 STATUS 撒谎：style.css 标 443 行，实测 605 行（wc -l 验证）
🔴 指路牌断链：CLAUDE.md 指向的部署文档已废弃，路径不存在
🟡 误导区未标注：根目录 6 个 *-备份/ 目录，MAP 没标"别动区"，
   下一个 agent 会把备份当正主读
结论：STATUS 不可信（3 项指标漂移），建议先修再交付
```

修复后复审全绿，全程留有 git diff。**审计只读不改文件**——它负责说真话，改不改你决定。

## 安装

**方式一（推荐）— Claude Code 插件市场：**

```
/plugin marketplace add Seekers2001/docs-governance
/plugin install docs-governance@docs-governance
```

**方式二 — Codex CLI：**

```bash
codex plugin marketplace add Seekers2001/docs-governance
codex plugin add docs-governance@docs-governance
```

安装后新开一个 Codex 会话，优先通过 `$docs-governance` 让总路由选择能力，也可以显式调用 `$living-docs-governance`、`$context-and-decisions`、`$change-impact`、`$contract-first`、`$test-collaboration` 或 `$module-regression`。Codex 会读取 `.codex-plugin/plugin.json`，Claude Code 继续读取原有 `.claude-plugin/plugin.json`，两端共用同一套 `skills/`。

**方式三 — Claude Code 本地软链**：`git clone` 本仓后，把 `skills/` `agents/` `commands/` 下的条目软链到 `~/.claude/` 对应目录（改源仓即时生效，适合要改内容的人）。

**装好没？** Claude Code 随便进一个项目敲 `/governance-audit`；Codex 新开会话后输入 `$docs-governance 只读审计当前项目`。看到一份只读审计报告（哪怕结论是“没治理文件”）就是装好了。

## 用法

```
# 活文档治理（以下为 Claude Code slash command）
/governance-init         # 全新空项目：day-0 治理骨架（宪法+检查流程+流水账）
/governance              # 已有代码项目：扫项目，生成/更新四件套
/governance-audit        # 只读审计：哪儿漂移了，不动文件
/governance-sync         # 阶段收尾：按矩阵查漏补缺该同步哪份文档
/governance-retro        # 复盘 LOG：哪类错误重复最多 → 输出"该下沉成 lint/测试"候选清单

# 契约式前后端协作
/contract 做订单详情页    # 先判模式，再定契约 → 各端开发 → 集成对账

# 模块回归审计（防"改 A 坏 B"）
/regression-audit init   # 首跑：扫 import 生成回归台账 REGRESSION.md 草稿
/regression-audit        # 改完就跑：本模块+全部下游验收命令，退出码终审

# 测试协作治理（v1 直接用自然语言触发 skill，没有 slash command）
盘点这个项目的测试资产，按 templates/TESTS.example.md 生成 TESTS.md
读取 Bug 清单，把缺少保护的 Bug 登记成 TEST-ID，并给出补测清单
前后端分开开发，读取唯一接口契约，把消费者、提供者和联调测试登记到同一个 TEST-ID

# Codex 总路由 / 上下文与决策 / 变更影响
$docs-governance 判断这个项目该启用哪些治理能力
$context-and-decisions 为这项数据库选型建立 ADR
$change-impact 修改订单数据模型前分析影响、迁移和回滚
```

Codex / ChatGPT 使用对应 skill + 自然语言意图，例如：

```text
$docs-governance 治理当前项目，并告诉我该走哪个专项 Skill
$living-docs-governance 只读审计当前项目
$living-docs-governance 阶段收尾同步
$context-and-decisions 统一领域术语并记录架构决策
$change-impact 分析这次修改的牵连面，实施后再对照实际 diff
$contract-first 为订单详情页建立契约并分端实现
$module-regression 按 REGRESSION.md 运行本模块与下游回归
```

## 结构

```
docs-governance/
├── AGENTS.md / CLAUDE.md / CLAUDE_MAP.md / ARCHITECTURE.md / PROJECT_STATUS.md / PROJECT_LOG.md / TESTS.md  # 插件自治理
├── .codex-plugin/plugin.json                                      # Codex / ChatGPT 插件入口
├── .claude-plugin/{plugin,marketplace}.json                       # Claude Code 插件入口
├── skills/{docs-governance,living-docs-governance,context-and-decisions,change-impact,...}/SKILL.md  # 路由与方法论唯一源
├── agents/{docs-governor,docs-auditor,contract-director,frontend-dev,backend-dev,regression-auditor}.md
├── commands/{governance-init,governance,governance-audit,governance-sync,governance-retro,contract,regression-audit}.md
├── docs/adr/                                                       # 插件自身的架构/数据库决策
├── templates/*.example.md                                          # 含 ARCHITECTURE / CONTEXT / ADR / TESTS / REGRESSION 等模板
├── references/governance-sync-matrix.md
├── hooks/{check-on-stop.sh,hooks.json}                             # 会话结束治理提醒
└── scripts/{verify.sh,audit-docs.py,project-log-index.py}          # 结构自检、文档审计、日志索引
```

> skill = 方法论（唯一源），agent = 照方法论干活的人，command = 按钮，template = 空白表格。方法论只写在 skill 里，agent 不复制——**一个防文档漂移的插件，自己内部先不漂移。**

## 开发

首次开发先创建并激活 `.venv`，运行 `python -m pip install -r requirements-dev.txt` 安装契约模板校验依赖。改任何文件后、提交前跑 `bash scripts/verify.sh`（检查 Claude/Codex manifest 一致、JSON、hook、路由与引用不断链，并执行单元测试、OpenAPI 模板验证和 full 文档审计）。本插件实际有哪些测试、为什么存在、保护哪些风险和还缺什么，统一看根目录 `TESTS.md`。关键 Skill 另用 Codex `quick_validate.py` 校验。

---
MIT · Seekers2001（小磊）· jiaxinleifm@outlook.com

产品资料采用完整十阶段入口，方法仅管理文档。项目可通过 `.docs-governance.json` 约束必需文件、PRD 标题／文件名位置与脚本目录；变更收尾、暂存区提交和 CI 共用规则。见 [文档护栏说明](references/document-policy.md)。
