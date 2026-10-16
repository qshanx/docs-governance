# 来源与适配

2026-10-14 的范围确认：阿磊确认 project-retro 只复盘 Agent 项目工作环境，沿 Matt 的七个观察方向补充四个方向；交付有证据的建议，安装和启用不属于默认复盘动作。测试资产记录与专项复盘继续在 [Issue #49](https://github.com/qshanx/docs-governance/issues/49) 讨论，PR 审核保持现有五步流程。

2026-10-16 阿磊在本会话确认增加人与 AI 的协作复盘，并要求先提交 Issue、再修改本地 Skill 和关联文档并测试，见 [Issue #51](https://github.com/qshanx/docs-governance/issues/51)。目标理解、分工决策、沟通反馈、验证交付与有效协作五个环节及证据归因原则为本项目此次适配，不归为 Matt 或 Tw93 原文；覆盖此前“只复盘工作环境”的范围限制，不追认 Issue #49 的测试资产草案。

此前整体改写（已由下述纠正取代）：2026-10-16 阿磊要求教会 AI 思考和自我复核，将清单下沉为按需参考，并提醒减少流程负担。主文件改为理解经历、解释原因、自我复核和选择最小改进四段短引导；原有七加四个环境方向及五个协作环节移到 observation-prompts.md。证据反驳、替代解释、当时信息／授权和反事实检验为此次本地适配；不把反事实或自我复核当成实际效果验证。沿用 [Issue #51](https://github.com/qshanx/docs-governance/issues/51)，其他 Skill 的方法及 Issue #49 的讨论状态保持。

2026-10-16 最新纠正：阿磊明确“原来也要，只是加一个人机复盘的流程”。恢复原有环境复盘的取证、七加四个环境方向和建议交付，新增独立的人机协作流程，仅人机流程采用思考与自我复核引导，五个协作观察环节留作按需参考。两条流程共用取证与交付，按问题选择，同事件与经验不重复计数；不以统一推理流程替换原环境方法。

- [Matt retro 固定版](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/in-progress/retro/SKILL.md)：七个观察方向、按严重程度交付建议、实现与审查分工。原文 SHA-256：`33fbc28568e3146f20fd908b12998bc0ab30aa4f4c87288199a40793efa94696`；中文适配，MIT [许可证](LICENSE) 随包保留。保留现有 Skill 调用策略，不照搬上游固定上下文假设。
- [Tw93《你不知道的 Claude Code：架构、治理与工程实践》](https://tw93.fun/2026-03-12/claude.html)：参考上下文延续、Skills／工具／Hooks 的职责、权限控制与任务隔离；本项目据此整理新增四个方向，非作者原文的四项清单。不采用固定工具配置或成本数字；宿主差异按目标环境核实。[既有研究](../../../research/2026-09-27-tw93-claude-code-governance.md)。
- [Vince 入口文章](../../../research/2026-09-27-vincemask-agent-entrypoints.md)：入口具体规范继续复用 agent-entrypoints，不在本 Skill 重写。
- [WquGuru magpie 分析](https://x.com/wquguru/status/2109650264601117141)：经验提炼、复验和升级保留为按需分支，方法在 lessons.md；三次独立有效复验后给清单是此前已确认的本地适配，不作为普通环境复盘的必经流程。

2026-10-16 最终确认：阿磊阅读主文件与人机观察提示全文后，明确“原来的环境复盘保留，新增人机协作流程，观察提示按需读取，就按现在这个版本”，随后授权本地提交并将 Issue #51 更新为已确认。独立提交不包含其他待提交 Skill；对 pr-review／test-retro 保留可选名称引用，避免把未随包提交的能力作为硬链接依赖。
