---
name: living-docs-governance
description: >-
  为新项目或尚未建立文档管理体系的已有项目，规划并建立文档入口、资料分工和维护方式。
  用户要求“建立文档管理体系”“首次配置文档治理”时使用；暂保留只读文档审计、日志统计与归档。
  单独优化 Agent 入口、日常同步或执行复盘，交给对应 Skill。
metadata:
  origin: ECC
---

# 首次建立文档管理体系

为尚未建立体系的项目确定：需要哪些文档、各自放什么、变化后更新哪里。一次性脚本通常不需要。

## 统一 setup

了解项目 → 整理并补齐 docs → 建立 MAP、STATUS → 接入 Agent 入口并检查。

1. **了解项目。** 定位项目根，读取现有入口、相关对话和已确认需求；有代码时核对实现与配置，并确认是否使用 Git。区分现状、计划与未知项，需求与代码冲突分别记录，关键缺口先澄清。

2. **整理并补齐 docs。** 读取[记录范围与模板](record-scope.md)，调用 `docs-structure` 按职责组织现有资料。按实际需要补齐数据库、需求、设计、接口和验证文档，下表有对应专项 Skill 时调用；提供项目根、确认来源与范围，核对返回的路径和缺口。复用现有主记录，不编造内容，不为凑目录创建空文档。

3. **建立导航和状态。** 建立或完善 `CLAUDE_MAP.md`，写清任务对应的资料入口、非显然位置和误导目录；建立或完善 `PROJECT_STATUS.md`，记录当前风险、阻塞、待办、待验证项和删除提醒。已有同类载体就复用。使用 Git 的项目不默认新建或要求维护 LOG；已有历史保留，不删改，后续维护沿用已确认约定。无 Git 时按追溯需要决定是否建立 LOG。

4. **接入并检查。** 由 [agent-entrypoints](../agent-entrypoints/SKILL.md) 在共享入口写入实际路径和读取要求：开始任务先读 MAP 导航与 STATUS 风险／阻塞，再按任务下钻正文；采用本插件开发流程时指向总路由的“模块变更流程”，按 `docs-maintenance` 接好收尾维护约定。沿真实任务检查能否找到需求、实现与验证资料，核对职责、引用和重复主记录，执行入口检查及下方命令。交付实际路径、维护方式、验证结果与缺口，重复执行复用已有来源、编号与路径。

```sh
python3 <插件目录>/scripts/audit-docs.py --root <目标根> --scope full
```

非零先区分实际问题与检查器布局限制；旧检查器因未建 LOG 等报错时说明限制，不为通过检查补建文件。专项不可用时报告缺口，不递归启动 setup；未测宿主加载或自动触发时标明未验证，部分配置不称完整完成。

| 本次需要 | 读取并执行 |
|---|---|
| 产品需求、来源与基线 | [product-evolution](../product-evolution/SKILL.md)，仅处理已确定范围 |
| 判断是否需要架构文档并完善说明 | [architecture-docs](../architecture-docs/SKILL.md) |
| 领域术语与重要决策 | [context-and-decisions](../context-and-decisions/SKILL.md) |
| 跨端接口契约 | [contract-first](../../engineering/contract-first/SKILL.md) |
| 测试资产与验证证据 | [test-collaboration](../../engineering/test-collaboration/SKILL.md) |
| 资料落实后的 Agent 入口 | [agent-entrypoints](../agent-entrypoints/SKILL.md) |

复用已有授权，仅讨论方案时保持只读。setup 不包含业务实现，也不自动授权 Git 初始化、提交、推送、依赖安装或 Hook／CI 配置。获准安装 Hook 时检查 `core.hooksPath`，否则用 `git rev-parse --git-path hooks/pre-commit` 定位，不覆盖既有 Hook。

`docs-structure` 由 [PR #36](https://github.com/qshanx/docs-governance/pull/36) 提供；未安装时报告目录规划步骤未完成，不冒充已调用。

## 其他任务入口

当前 Agent 按任务读取对应流程，首次 setup 不展开以下审计和日志管理。宿主调用方式见[使用说明](../../../使用说明.md)。

### 已有项目治理

尚未建立体系时执行[统一 setup](#统一-setup)；已有体系的增量整理读取 [docs-maintenance](../docs-maintenance/SKILL.md)，传入本次变化与范围。仅追加 `log: 一句话` 时读取[日志管理](log-management.md)。

### 阶段同步

读取 [docs-maintenance](../docs-maintenance/SKILL.md)，传入阶段说明、相关会话与实际 diff。采用 PR 护栏时，再执行[阶段同步的 PR 护栏](audit.md#阶段同步的-pr-护栏)。

### 只读审计

读取并执行[文档审计](audit.md)，按指定范围检查并报告，默认不写文件。

### 日志归档与索引

读取[日志管理](log-management.md#日志归档与索引)，按事件数量判断是否需要归档，沿用既有确认要求。

### 日志复盘

日志统计读取[日志复盘](log-management.md#日志复盘)；从执行经历中提炼经验，读取 [docs-retro](../docs-retro/SKILL.md)。两者默认只读。
