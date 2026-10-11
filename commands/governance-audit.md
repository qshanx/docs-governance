---
description: 只读审计当前项目的文档治理质量与产物链接完整性；先跑确定性检查，只有通过后再判断职责、语义与证据漂移，不修改任何文件。
argument-hint: "[spine|context|adr|artifacts|full，默认 full]"
---

读取 `skills/documentation/living-docs-governance/SKILL.md`，执行“只读审计”模式。

用户参数：`$ARGUMENTS`。将参数作为该模式定义的项目信息、范围或阶段说明传入；规则与读写边界以 Skill 为唯一来源。

Claude Code 可由 **docs-auditor** 承担该模式；明确传入本命令入口及兼容审计模式、目标项目根目录、参数与已有验证证据，不复制流程。
