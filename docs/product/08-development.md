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
