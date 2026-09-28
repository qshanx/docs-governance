# 研发

适用主题：产品需求与迭代治理 r1。记录日期：2026-09-22。阶段状态：已完成（本轮本地文件实现）。

## 输入来源

[PRD r1](06-prd.md) 与本次会话授权。

## 产出

实现入口：[Skill](../../skills/product-evolution/SKILL.md)、[模板](../../templates/product-index.example.md)、[总路由](../../skills/docs-governance/SKILL.md)。具体实现见 [草稿 PR #12](https://github.com/qshanx/docs-governance/pull/12)，分支为 codex/product-docs-management，待外部评审。

## 未解决事项与下一步

本轮关联 [Issue #11](https://github.com/qshanx/docs-governance/issues/11)，实时任务继续由项目 Issue Tracker 管理；本文件只挂产出与阶段证据，检查结果见 [测试上线](09-test-release.md)。

新增 [位置校验](../../scripts/docpolicy.py)、[收尾审计](../../scripts/auto-audit.py) 与 [暂存区检查](../../scripts/check-staged-docs.py)，统一复用现有审计结果接口。

PR 前强制扫描入口为 [check-pr-docs.py](../../scripts/check-pr-docs.py)，由 [pre-push](../../hooks/pre-push.sh) 与 PR Actions 共同调用；变更到文档的映射保存在项目规则中，不迁移业务项目现有文档。

2026-09-23 按能力规格 r2 增加 [产品文档管理员](../../agents/product-docs-manager.md)，扩展原 Skill 和模板并接入总路由、用户说明与架构入口。Agent 保持薄角色适配，规则继续由 Skill 唯一维护；没有改动审计脚本或业务项目。

2026-09-23 按能力规格 r3 扩展共享 Skill 的 PM 四类索引与按任务读取协议；产品入口模板增加主记录章节、依赖和分批审查信息，CLAUDE 及模板保留简短触发路标，Agent 引用共享协议。未增加扫描器、修改业务项目或复制规则到 AGENTS。

2026-09-27 按能力规格 r4 新增 [已有项目首次接入命令](../../commands/governance-setup.md)，其探测、草案、确认、最小写入与验证边界只写入 [活文档治理 Skill](../../skills/living-docs-governance/SKILL.md)。总路由、日常治理命令、双语说明、地图、架构与变更记录同步更新；`scripts/verify.sh` 增加所有 command 必须委托共享 Skill 的结构检查。未修改业务项目、现有 Tracker、hook 或宿主配置。

2026-09-27 r5 在包含 product-evolution 的当前工作区新增 [agent-entrypoints](../../skills/agent-entrypoints/SKILL.md) 与[文章来源整理](../../research/2026-09-27-vincemask-agent-entrypoints.md)。接入总路由、活文档与产品读取入口，模板移除会被误用为普适规则的导入风格／禁建文件示例。原 PR #14 基于更早主线，尚未含该产品体系及本轮工作；统一 setup 的重做和合并未完成。

同日按阿磊纠正，将规范改为与原文 1—8 同序号的执行要求和检查项；补入每份入口 ≤200 行的硬验收及计数命令，同步共享章程、模板和调用方，消除“仅作复核信号”的冲突表述。没有新增自动门禁、修改宿主配置或扩大到 setup 编排实现。

2026-09-28 按 r7 修复统一 setup：复用 [docs-governor](../../agents/docs-governor.md) 编排，setup 与 init 进入同一共享模式；识别新项目、讨论后项目与已有项目，先处理产品主记录，再处理入口，统一验证。`product-evolution` 增加编排调用的返回边界，避免重复更新入口或递归 setup。去掉旧 init 隐含的 Git 初始化、首提及 hook 安装授权。实现与入口规范仍在本地工作区，未推送或合并；PR #14 的产品能力依赖 PR #12，远端关系待确认。
