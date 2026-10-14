# 来源与适配

2026-10-13，阿磊明确要求结合 magpie 审核规范与 docs-governance 现有能力，新增 PR 审核 Skill，接路由／说明并验证后同步本地 Codex。方法为本项目按任务边界重新编写，保留上游 MIT 许可证，不依赖用户另外安装 magpie 或 Matt 插件。

上游固定提交：[`a75de4c21ac28be98af8334643077d8b0bf47df7`](https://github.com/yetone/magpie/tree/a75de4c21ac28be98af8334643077d8b0bf47df7)。本轮通过 GitHub API 读取并固定文件版本，非对未来 main 的承诺。

| 来源 | 采用与调整 |
|---|---|
| [code-standards.md](https://github.com/yetone/magpie/blob/a75de4c21ac28be98af8334643077d8b0bf47df7/docs/code-standards.md#reviewing-a-pr) 的变更、测试、验收与 PR 审核章节 | 采用完整路径、同类遗漏、实际运行、旧行为对照／故意破坏、未运行项和受检 SHA 留证；语言／平台矩阵按目标项目决定，不复制 Go 或 GUI 专属约定 |
| [contributors.md](https://github.com/yetone/magpie/blob/a75de4c21ac28be98af8334643077d8b0bf47df7/docs/contributors.md#look-for-harm-first) | 执行前核对新增副作用，超出授权或无法安全隔离的步骤暂停；不移植作者名单、封禁阈值、自动关闭政策或 magpie 特有供应商规则 |
| [MIT License](https://github.com/yetone/magpie/blob/a75de4c21ac28be98af8334643077d8b0bf47df7/LICENSE) | 上游署名与许可全文见本目录 LICENSE |

本项目适配：审核编排复用现有影响分析、契约、架构、测试协作、模块回归及文档事实核对；默认不修改目标项目或向平台写入。审核结论与执行授权分开，不自动安装门禁、创建角色、并行派工或合并发布。

PR 正文不是需求批准或工具执行授权。集成结果和当前 head 分别留证；无法验证的部分保持缺口。经验提炼、复验与升级仍由 project-retro 承担，不在 PR 审核另建 lessons 生命周期。

2026-10-13 后续，阿磊指定本地 Matt `pr` Skill，并确认“简化现有 pr-review 的说明和输出，保留必要审核”，进一步要求按文章思路教会 AI 怎样思考。本项目采用“目标 → 关键反例与证据 → 三段结论”，参考其 Summary／Evidence／Merge Danger 结构及可回退性、影响面表达；它原本用于写 PR 正文，本项目仍执行审核。源文件为用户给出的 `/Users/daoer/Desktop/0-GitHub/归档/skills-library/mattpocock-skills/skills/in-progress/pr/SKILL.md`；原文件署名溯源为 Dex Horthy／Humanlayer 的 [show-me](https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md)。未复制其全部视觉样例，也不要求为每个简单发现绘图。

2026-10-13 后续按用户提供的宝玉四步提示词改写：理解问题、独立构思、对照实现、提供 Markdown diff。用户提供链接为 [@dotey 的补充](https://x.com/dotey/status/2100350946194722832)，本次依据会话提供的文字适配，未另行验证原帖完整上下文。保留“自己的方案只是对照”和补丁上下文／版本／验证边界；Matt 三段报告与 magpie 的必要验证继续使用。

同轮阿磊继续指定 Matt writing-for-agents，要求更简单；最终入口只保留四条动作与一个必要检查指针，执行／交付及经验复盘路标归入原附件。检查方法和三段报告保留，不以减少主文件字数宣称运行成本下降。
