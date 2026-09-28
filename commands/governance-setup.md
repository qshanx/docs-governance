---
description: 统一配置新项目、讨论后项目或已有项目的产品文档包与 Agent 入口；先识别资料与授权，再编排专项 Skill，保留现有主源。
argument-hint: "[目标项目、讨论资料或配置范围]"
---

读取 `skills/living-docs-governance/SKILL.md`，执行“统一 setup”模式。

用户参数：`$ARGUMENTS`。将参数作为目标项目、已知约束或接入范围传入；探测、确认、写入与验证边界以 Skill 为唯一来源。

Claude Code 可由 **docs-governor** 承担此模式；传入目标项目根目录、参数与已有证据，不复制流程。
