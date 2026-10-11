---
description: 模块回归审计——改完代码后照 REGRESSION.md 台账跑"本模块+全部下游"的验收命令，退出码终审，防"改一个模块悄悄弄坏其他模块"。带 init 参数时扫 import 关系生成台账草稿。
argument-hint: "[init | 模块名 | 留空=按 git 改动自动定位]"
---

读取 `skills/engineering/module-regression/SKILL.md`，把 `$ARGUMENTS` 作为 init、模块名或默认工作区模式。

Claude Code 的普通审计由 **regression-auditor** 执行；init 由当前会话按 Skill 创建台账。不要让只读审计角色承担写入。
