---
description: 为已有项目首次接入 docs-governance：先只读探测现有规则、文档、Tracker 与验证入口，给出最小接入草案；用户确认后才写入。
argument-hint: "[目标项目或接入约束]"
---

读取 `skills/living-docs-governance/SKILL.md`，执行“已有项目首次接入”模式。

用户参数：`$ARGUMENTS`。将参数作为目标项目、已知约束或接入范围传入；探测、确认、写入与验证边界以 Skill 为唯一来源。

Claude Code 可由 **docs-governor** 承担此模式；传入目标项目根目录、参数与已有证据，不复制流程。
