# 来源与适配

2026-10-14 阿磊确认 project-retro 只复盘 Agent 项目工作环境，沿 Matt 的七个观察方向补充四个方向；交付有证据的建议，安装和启用不属于默认复盘动作。测试资产记录与专项复盘继续在 [Issue #49](https://github.com/qshanx/docs-governance/issues/49) 讨论，PR 审核保持现有五步流程。

- [Matt retro 固定版](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/in-progress/retro/SKILL.md)：七个观察方向、按严重程度交付建议、实现与审查分工。原文 SHA-256：`33fbc28568e3146f20fd908b12998bc0ab30aa4f4c87288199a40793efa94696`；中文适配，MIT [许可证](LICENSE) 随包保留。保留现有 Skill 调用策略，不照搬上游固定上下文假设。
- [Tw93《你不知道的 Claude Code：架构、治理与工程实践》](https://tw93.fun/2026-03-12/claude.html)：参考上下文延续、Skills／工具／Hooks 的职责、权限控制与任务隔离；本项目据此整理新增四个方向，非作者原文的四项清单。不采用固定工具配置或成本数字；宿主差异按目标环境核实。[既有研究](../../../research/2026-09-27-tw93-claude-code-governance.md)。
- [Vince 入口文章](../../../research/2026-09-27-vincemask-agent-entrypoints.md)：入口具体规范继续复用 agent-entrypoints，不在本 Skill 重写。
- [WquGuru magpie 分析](https://x.com/wquguru/status/2109650264601117141)：经验提炼、复验和升级保留为按需分支，方法在 lessons.md；三次独立有效复验后给清单是此前已确认的本地适配，不作为普通环境复盘的必经流程。
