---
name: docs-governance
description: >-
  作为面向长期 AI 协作项目的知识、决策与验证治理总入口，把优秀 Agent 的一次性工作沉淀为可继承、可验证、可持续演进的项目集体能力；根据用户意图把任务路由到活文档、领域上下文与 ADR、变更影响、接口契约、测试资产、模块回归或闭环设计能力，并在大型变更中组织正确顺序。用于用户只说“文档治理”“项目治理”“帮我整理项目知识”“改完怎么收尾”而未指定具体 Skill，或需要跨多项治理能力时。English triggers: docs governance router, project knowledge governance, documentation workflow, governance workflow.
---

# 文档治理总路由

## 定位

> **把优秀 Agent 的一次性工作，沉淀为项目可继承、可验证、可持续演进的集体能力。**

本插件不是让 Agent 多写文档，而是治理长期 AI 协作中的项目知识、关键决策与验证证据：让后续 Agent 能恢复上下文、沿用已确认约束、复核结果，并把新的有效做法继续沉淀回项目。

先判断意图，再读取并执行对应 Skill。不要在本路由复制各 Skill 的方法论。

## 单项路由

| 用户意图 | 路由到 |
|---|---|
| 产品文档管理员、来源登记、需求池／编号／版本、十阶段管理与产品审查 | `product-evolution`；Claude Code 可由 `product-docs-manager` 执行 |
| 初始化、维护、阶段同步、LOG 管理或复盘 | `living-docs-governance` |
| 当前 Module 权责、状态归属、依赖图或核心流转图 | `living-docs-governance` 的 `ARCHITECTURE.md` 路线 |
| 领域术语、`CONTEXT.md`、架构或数据库决策、ADR | `context-and-decisions` |
| 修改前判断牵连面、迁移、回滚、实施后对照 | `change-impact` |
| 前后端或服务间接口 | `contract-first` |
| 测试资产、成功标准证据、Bug→TEST-ID | `test-collaboration` |
| 修改后验证本模块及下游 | `module-regression` |
| 只读文档审计、链接完整性、孤儿文档 | `living-docs-governance` 的审计模式 |
| 设计可判定目标和反馈回路 | `loop-design-check` |

## 大型变更顺序

需求不清、基线冲突或需要产品过程管理时，先进入 `product-evolution`，明确已确认范围与成功标准，再进入工程变更。

按需执行，未触发的步骤直接跳过：

1. 用 `change-impact` 形成有证据的影响清单。
2. 若涉及难回退的架构、数据库、认证或部署决策，先用 `context-and-decisions` 建立或更新 ADR。
3. 若影响跨端接口，先用 `contract-first` 更新唯一契约源。
4. 实施后用 `test-collaboration` 将成功标准、Bug 或风险关联到 TEST-ID 与证据。
5. 用 `module-regression` 执行本模块与下游命令。
6. 用 `living-docs-governance` 做阶段同步，再运行只读文档审计。

## 边界

- 让 `CLAUDE_MAP.md` 管项目知识位置，让 `ARCHITECTURE.md` 管当前 Module 结构；本 Skill 只管插件能力路由。
- 让 Spec/Issue 管业务成功标准，Issue Tracker 管任务状态和排期；不要复制进路由或数据库。
- 不因为用户说“治理”就一次性创建所有可选文档和目录。先发现现有事实载体，再按预警信号懒创建。
