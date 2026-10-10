---
description: 契约式前后端协作。先判断单会话多 agent 还是多终端异步两种模式，再以 CONTRACT.md 指向的机器契约为唯一来源协调各端开发、做集成对账，防字段漂移。
---

读取 `skills/engineering/contract-first/SKILL.md`，将用户参数 `$ARGUMENTS` 作为任务说明，按 Skill 判断协作模式并执行。

Claude Code 由 **contract-director** 持有契约；仅在已选择模式 A 时可使用 **frontend-dev** / **backend-dev**。角色、流程和验证边界只在 Skill 维护。
