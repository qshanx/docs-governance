# Anthropic《The AI-Native SDLC Playbook》研读

研究日期：2026-09-15

官方原文：[The AI-Native SDLC Playbook](https://claude.com/blog/the-ai-native-sdlc-playbook)（Anthropic / Claude，2026-08-21）

配套课程：[Claude Academy：The AI-Native SDLC Playbook](https://academy.claude.com/courses/ai-native-sdlc-playbook)（14 节、约 1 小时）

## 结论先行

这不是一套「多 Agent 自动写代码」的提示词配方。它提出的关键改造是：保留传统 SDLC 的控制目标，但把控制从缓慢的人工交接，改成**版本化交付物、可执行约束、连续反馈和按风险分配的人审**。

最有价值的原则是：每一阶段提交一份下一阶段可读取的产物；`intent.md`、`spec.md`、`plan.md`、代码与测试、PR 审查记录、事故记录共同形成可审计链。Agent 可以推进链条，但有判断性质的批准仍由人承担。[官方原文](https://claude.com/blog/the-ai-native-sdlc-playbook#what-is-an-ai-native-sdlc)

它面向已使用 Claude Code、且有权限调整 Git 与 CI 的工程/平台/安全负责人，尤其是受监管的大企业；因此不是应该整套照搬给小团队或小仓库的流程规定。[课程的适用对象与前提](https://academy.claude.com/courses/ai-native-sdlc-playbook)

## 六阶段与最小落地物

| 阶段 | Anthropic 的改法 | 关键产物 / 边界 |
|---|---|---|
| Plan | 用来源者的语言把需求一次捕捉为可行动的原始规格 | `intent.md`：问题、目标、约束、受影响对象、未决问题；产品负责人校正后再提交。[官方详解](https://claude.com/blog/the-ai-native-sdlc-playbook#capture-as-intentmd) |
| Design | 在同一 Agent 工作会话中把需求与设计合并，同时应用品牌、安全、合规、UX 等技能 | `spec.md`：政策冲突与风险显式标记，产品负责人批准。[官方详解](https://claude.com/blog/the-ai-native-sdlc-playbook#requirements-and-design) |
| Build | 先只读规划，批准后再实施；把团队知识变为可审查的上下文与技能 | `plan.md` 写明变更文件、顺序、风险和验证；`CLAUDE.md` 保持精简；技能承载须一致应用的政策。[官方详解](https://claude.com/blog/the-ai-native-sdlc-playbook#claude-code-plan-mode-as-the-default-starting-point) |
| Test | 让 Agent 在交给人前获得本地反馈闭环；把 Agent 配置当作待回归测试的代码 | 单命令构建/测试、UI 截图验证；真实任务构成的持续 eval，配置变更和事故都会进入 eval。[官方详解](https://claude.com/blog/the-ai-native-sdlc-playbook#continuous-evals-in-ci) |
| Deploy | Agent 做一致性审查与可自动化的准备工作；人仅聚焦意图和风险 | `REVIEW.md` 定义审查 pass；分支保护保留 code owner 批准；hooks 把必要审批变成 allow / ask / block 的硬门。[官方详解](https://claude.com/blog/the-ai-native-sdlc-playbook#hooks-as-approval-gates) |
| Maintain | 确定性监测先发现异常，Agent 再诊断或提出受限修复 | 指标越界触发 Agent；它只能走既有 PR / runbook 等受控通道，诊断重新写回 `intent.md`，形成闭环。[官方详解](https://claude.com/blog/the-ai-native-sdlc-playbook#maintenance-and-closing-the-loop) |

## 最值得借鉴的四个实践

1. **交接物，而非聊天记录，是主线。** 后续阶段不依赖上一位人的上下文，而读取被批准的 Git 产物；同时每种产物必须指定唯一事实源，Jira 等现有系统也可以继续是权威来源。[官方对交接与单一真源的要求](https://claude.com/blog/the-ai-native-sdlc-playbook#what-is-an-ai-native-sdlc)
2. **配置也是生产系统。** `CLAUDE.md`、skills、hooks 会改变 Agent 行为，故它们应版本控制、代码审查，并在变更时跑 eval；事故转化为永久回归案例。[官方指南的 eval 流程](https://claude.com/blog/the-ai-native-sdlc-playbook#continuous-evals-in-ci)
3. **机器先验，人审升级。** Agent 先跑测试、构建、截图和策略审查；人审查「是否符合意图、风险是否可接受」，而不是逐行替 Agent 重做机械验证。[官方测试反馈闭环](https://claude.com/blog/the-ai-native-sdlc-playbook#give-claude-a-feedback-loop)
4. **自治只到门前。** 确定性检测负责决定是否触发；授权边界由 hooks、沙箱、短期凭据、环境分级和分支保护决定。生产部署的最终批准不交给写代码的 Agent。[官方对 CI/CD 和人审边界的说明](https://claude.com/blog/the-ai-native-sdlc-playbook#cicd-integration-and-deployment)

## 对本仓库的对照

本仓库已覆盖指南最重要的轻量部分，且比其企业化示例更符合本插件的定位：

| Playbook 主张 | 本仓库已有物 | 判断 |
|---|---|---|
| 当前上下文与方法论版本化 | `CLAUDE.md`、`PROJECT_STATUS.md`、`skills/*/SKILL.md`，并采用渐进读取 | 已具备；继续坚持入口薄、方法论唯一源，避免把 `CLAUDE.md` 膨胀成知识库。 |
| 每次改动有计划与验证 | 全局指令要求计划与可验证成功标准，`scripts/verify.sh` 是确定性闭环 | 已具备；适合继续按改动风险保留最小计划，不必为文档小改动强制新增 `plan.md`。 |
| 团队知识操作化 | 8 个共享 skill，agent / command 仅作交互适配 | 已具备且更清晰：policy / method 在 skill，入口文件只路由。 |
| eval 配置治理 | `scripts/verify.sh`、Python 测试、CI verify | 部分具备；若未来要改 Agent 行为的自动化配置，可考虑只为高风险或高频 skill 建「真实任务 + 预期检查」回归集，而不是全仓库先造 20–50 个 eval。 |
| 反馈回写 | `PROJECT_LOG.md`、STATUS backlog、审计与测试协作方法论 | 方向一致；仍应让一次性研究、草稿与当前权威规则分开，避免历史成为隐式上下文。 |

## 不应直接照搬的部分

- **不要强制全项目 `intent.md → spec.md → plan.md`。** 官方也明确不同 play 有依赖顺序；对本仓库的单文件文档修正或小脚本修复，这会比改动本身更重。
- **不要把指标控制带、无头 Agent、生产 MCP 和强制 managed settings 当成当前缺口。** 它们需要 CI、生产环境、权限模型、预算与责任人，是 Markdown 治理插件的默认职责。
- **不要把并行度当产能指标。** 官方建议先从 2–3 个隔离 worktree 会话开始，实际上限由人能否保持审查质量决定；共享文件的任务仍应串行。[官方并行会话的边界](https://claude.com/blog/the-ai-native-sdlc-playbook#parallel-sessions-and-subagents)
- **不要相信「Agent 生成得快」天然等于更安全。** Anthropic 后续安全文章明确把威胁建模为 prompt injection / 被入侵 Agent、供应链投毒和更高量的常规漏洞；控制核心是最小权限、隔离、确定性与 Agent 审查结合、以及在高杠杆点保留人审。[Anthropic 的安全实践](https://claude.com/blog/how-anthropic-secures-its-ai-native-software-development-lifecycle)

## 若要把启发转成下一步

建议只做一个低成本试点：为「会改变 Agent 行为」的改动（`CLAUDE.md`、`skills/`、hooks 或自动化工作流）补一份真实任务回归样例，明确输入、预期结果和确定性检查；先观察它是否真能拦住回归，再决定是否发展成完整的 Agent eval CI。其余流程保持现有轻量治理，不为“AI-native”标签新增仪式。

## 来源与时效判断

- 官方博客的页面日期为 **2026-08-21**，其内容与官方 Academy 的 14 课课程结构一致；在 2026-09-15 检索到的 Anthropic/Claude 官方材料中，这是以全 SDLC 的逐阶段实操为主题、最新且最直接的指南。
- [官方博客：The AI-Native SDLC Playbook](https://claude.com/blog/the-ai-native-sdlc-playbook)
- [官方课程：The AI-Native SDLC Playbook](https://academy.claude.com/courses/ai-native-sdlc-playbook)
- [官方安全补充：How Anthropic secures its AI-native SDLC](https://claude.com/blog/how-anthropic-secures-its-ai-native-software-development-lifecycle)
