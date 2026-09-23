# Changelog

本插件的版本变更记录。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

## [Unreleased]

### 新增
- `product-docs-manager` 产品文档管理员角色，复用共享 Skills；六类资料位置与十阶段导航共用主记录，补充来源登记、稳定需求编号、状态／修订及已授权写入边界。
- PR 前变更扫描与 pre-push 钩子：按来源提交快照执行 full 审计，沿模块映射列出应核对文档；PR Actions 复用同一入口，断链、关联文档缺失和执行错误阻止继续。
- 项目级文件位置配置，约束必需文件、PRD 主标题／文件名和脚本目录；变更触发 Stop 审计、真实暂存区提交检查与原 CI 共用规则，不增加定时任务。
- `product-evolution` 共享 Skill、产品入口模板和本插件十阶段产品管理示例，覆盖需求来源、PRD 基线、评审、交付证据与运营反馈；接入总路由与阶段同步。

### 修复
- Stop 与直接自动审计共用治理根定位：支持子目录、显式根和独立子项目配置，尊重 Git／worktree 边界；定位失败明确提示，避免静默漏审。
- 日志审计与归档索引共用同一事件解析器，格式错误携带来源及行号，保持历史原文与现有归档行为。
- 自动评审写回前校验文件版本，评审期间编辑或删除的正文不会被旧快照覆盖，也不保存过期通过状态。
- 文档审计精确定位删除区并区分替代物，支持引用式链接和显式可选引用，清除依赖本机相邻仓库的活动链接。
- 日志审计支持显式基线；PR / push CI 比较原始基线，默认 verify 接入 full 审计。日志事件格式统一，错误格式不再静默漏计。
- 治理、契约和回归共享流程统一归入 Skill；commands / agents 仅保留宿主入口与角色边界。
- 契约模板改为单一 OpenAPI 定义与 Markdown 索引，增加标准格式校验和序列化响应正反例；第三方校验器只作为开发依赖。

### 变更
- 审计新增 `--format json`，从同一结果渲染文字和机器输出，携带范围、Git 上下文与证据，区分文档失败、未验证、提示和执行错误；执行错误退出码为 2。
- 治理层引用项目已有代码审查与测试证据；区分文档、机器契约和实际运行记录的权威来源，健康快照在相关变更后待复验。
- 治理风险按实际影响分级，行数和覆盖率仅作检查线索；STATUS 模板分开紧急风险与普通缺口，阶段日志聚焦有意义的结果。
- 补充英文项目概览、三分钟只读试用路径和贡献规范；新增 Bug / 工作流提案 / PR 模板，方便外部用户复现问题、讨论方法论与提交最小改动。
- 新增独立、按需创建的 `ARCHITECTURE.md` Module 架构契约：权责与状态归属表、代码依赖图、独立的运行时核心流转图；`CLAUDE_MAP.md` 只保留导航入口，治理、审计、变更影响和阶段同步共同维护架构文档与真实代码的一致性。
- 新增本插件自己的 `TESTS.md`，公开现有测试、存在理由、TEST-ID、执行证据与缺口；收紧 TEST-ID 审计，避免把 skill 名、复数说明和显式示例误判成登记断链。
- 新增 GitHub Actions 自动运行 `scripts/verify.sh`；更新 SVG/PNG 展示图，使双宿主、总路由、全部专项 Skill、确定性执行与 Markdown 事实源和当前架构一致。
- 明确产品定位：面向长期 AI 协作项目治理知识、决策与验证证据，把优秀 Agent 的一次性工作沉淀为可继承、可验证、可持续演进的项目集体能力；同步总路由、双语 README、使用说明和双端 manifest。

## [0.7.0] - 2026-08-02

### 新增
- 新增 `docs-governance` 总路由、`context-and-decisions` 与 `change-impact` 三个 Skill；Codex 可从一个入口按需进入 CONTEXT、ADR、契约、测试、回归和治理同步。
- 新增 CONTEXT / ADR 模板，并用 `docs/adr/` 记录本插件的 PROJECT_LOG SQLite 索引决策。
- 新增 `scripts/project-log-index.py`：按事件计数，超过 200 条后经确认归档旧事件，并从 Markdown 原文重建本地 SQLite 索引。
- 新增 `scripts/audit-docs.py` 及 spine/context/adr/artifacts/full 审计范围，检查断链、ADR 索引、LOG 完整性、TEST-ID 和孤儿文档。

### 变更
- 文档架构明确为“根脊柱 = 当前导航、可选文档 = 持久知识、Issue Tracker = 任务排期、SQLite = 机器投影”，所有目录按需懒创建。
- 成功标准留在 Spec/Issue 唯一来源；TESTS 关联证据，变更影响在实施前后核对迁移、回滚、实际 diff 和文档同步。
- `verify.sh` 新增总路由/README/使用说明一致性、派生数据库忽略、Python 编译和单元测试检查。

## [0.6.0] - 2026-08-02

### 新增
- 新增 `.codex-plugin/plugin.json`，将现有 skills 打包为 Codex / ChatGPT 可安装插件。
- 新增根目录 `AGENTS.md` 与 `templates/AGENTS.example.md` 薄桥接，让 Codex 读取共享 `CLAUDE.md` 章程而不复制规则。

### 变更
- 活文档、契约协作与模块回归 skills 增加 Codex 直接执行和宿主 agent 降级说明。
- README、使用说明与 day-0 初始化流程补充 Codex 安装、调用和 AGENTS 生成方式。
- 结构自检增加 Claude / Codex manifest 名称、版本和 skills 路径一致性检查。

## [0.5.0] - 2026-07-12

### 新增
- **第四条线·测试协作治理**（`test-collaboration` skill + `templates/TESTS.example.md`）：盘点项目现有测试资产，把需求、规则、风险和 Bug 转成 TEST-ID，维护必要、缺失、疑似重复、疑似废弃及可执行证据。v1 由当前会话直接使用 skill，不新增专用 agent、slash command 或执法脚本。

### 变更
- `module-regression` 和 `REGRESSION.example.md` 不再重复维护业务规则清单，改为引用 `TESTS.md` 的 TEST-ID；`/regression-audit` 继续只负责按台账运行本模块和下游命令并报告退出码。
- `/governance-retro` 的重复错误下沉候选改为登记到 `TESTS.md`。

## [0.4.0] - 2026-07-03

### 新增
- **第三条线·模块回归审计**（`module-regression` skill + `regression-auditor` agent + `/regression-audit` 命令 + `templates/REGRESSION.example.md`）：REGRESSION.md 台账登记每个模块的下游消费者（脚本从 import 生成、勿手改）与可执行回归验收命令（对账型优先），改完照单跑"本模块+全部下游"，退出码终审——防大项目"改一个模块悄悄弄坏其他模块"。铁律：判决=退出码 / 审计员只报不修 / 红着不准交付。

### 新增
- `templates/pre-commit.example`：pre-commit 护栏——固化"含代码改动的 commit 必须同批 staged 一行 PROJECT_LOG.md"（测试/文档/治理文件豁免，`--no-verify` 应急后门）；`/governance-init` 自动装，`/governance` 对已有 git 项目询问安装。（backlog #2）

## [0.3.0] - 2026-07-02

### 新增
- `/governance-init` 命令 + `templates/governance.example.md`：全新空项目的 day-0 治理骨架——精简 CLAUDE.md（含 Git 自动执行+硬禁单 / 失败自检三问 / references 触发规则）+ docs/governance.md（4 步检查流程 + 三层验收）+ PROJECT_LOG.md + 目录骨架。刻意不生成 MAP/STATUS（防空壳占位符出生即漂移），项目长起来后用 `/governance` 升级；与 `/governance` 双向指路。
- `loop-design-check` skill：写 loop（该不该建 → 可判定目标 → 回路类型 → plan/build/judge 骨架）+ 体检 loop（五个崩法防呆 + 判断留人红线）。英文版已被 ECC 上游合并（affaan-m/ECC #2381）。

## [0.2.0] - 2026-06-23

### 新增
- **活文档治理**（`living-docs-governance` skill + `docs-governor` / `docs-auditor` agent + `/governance` `/governance-audit` `/governance-sync` 命令）：四件套（CLAUDE.md / CLAUDE_MAP.md / PROJECT_STATUS.md / PROJECT_LOG.md）+ 分级读取协议 + 文档角色分层。
- **契约式前后端协作**（`contract-first` skill + `contract-director` / `frontend-dev` / `backend-dev` agent + `/contract` 命令）：一份 CONTRACT.md 当唯一真相源，支持单会话多 agent 与多终端异步两种模式（CDC / 契约测试）。
- `templates/`：四件套 + CONTRACT 空白模板。
- `references/governance-sync-matrix.md`：阶段收尾的查漏补缺矩阵。
- `hooks/check-on-stop.sh`：会话结束治理提醒（提醒型，未强制阻断）。
- `scripts/verify.sh`：插件结构完整性自检（JSON 可解析 / hook 可执行 / 命令→agent→skill/template/reference 不断链）。

### 改进
- `CLAUDE_MAP.md` 模板瘦身：删掉目录树镜像，只留"树看不出来"的四类（依赖方向 / 非显然定位 / 误导清单 / 别动区）。
- 分级读取协议：CLAUDE 全文常驻、STATUS 仅红线块常驻、MAP 默认按需、LOG 按需 + 改文件前必读护栏。

### 已验证
- 在真实项目「经营报表加工」「礼仪课程 demo」上跑通审计（读）与修复（写），捕获并校正 STATUS 指标漂移、脊柱职责越界、误导目录未标注等问题。
