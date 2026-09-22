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
