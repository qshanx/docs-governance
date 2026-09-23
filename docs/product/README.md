# 产品管理入口

本目录管理 docs-governance 插件自身的产品要求与演变。方法论唯一源仍是 [product-evolution](../../skills/product-evolution/SKILL.md)，这里保存本项目事实。

## 十阶段文件导航

按阿磊指定顺序管理；状态以各阶段记录及其证据为准。未开展或不适用均明确说明，不以目录齐全代表工作完成。

1. [项目初始化](01-project-init.md)
2. [市场分析](02-market-analysis.md)
3. [需求调研](03-user-research.md)
4. [需求分析](04-requirements-analysis.md)
5. [原型](05-prototype.md)
6. [PRD](06-prd.md)
7. [需求评审](07-requirements-review.md)
8. [研发](08-development.md)
9. [测试上线](09-test-release.md)
10. [运营反馈](10-operations-feedback.md)

## 产品与当前基线

产品定位以 [中文项目概览](../../README.zh-CN.md) 为准：面向长期 AI 协作项目，沉淀可继承、可验证的知识、决定和交付证据。技术结构见 [ARCHITECTURE](../../ARCHITECTURE.md)。

| 主题 | 唯一主记录／修订 | 确认范围与来源 | 待决或未验证 |
|---|---|---|---|
| 产品文档管理 | [能力规格 r2](06-prd.md) | 2026-09-22 确认管理空间和护栏；2026-09-23 在当前会话确认管理员角色、六类资料及授权边界（来源 PDM-20260923） | 业务项目实际试点及发布后效果未验证 |

## 资料位置与来源

本项目复用现有资料：原始输入与确认见下表；产品认知与规划见阶段 01—04；需求池沿用 Issue #11，单需求主记录为能力规格；版本沿用 CHANGELOG 和 Git；验收复盘见阶段 07、09、10。十阶段导航链接这些记录，不再复制六套目录。

| 来源标识 | 原始位置 | 提供者 | 材料／收录日期 | 适用范围 |
|---|---|---|---|---|
| PDM-20260923 | 本 Codex 任务 01a0c6b2-dc2c-7d32-8e1c-12101c7bfc1d 中的三条管理建议、角色设计回复及随后“可以”的确认 | 阿磊 | 2026-09-23／2026-09-23 | 新增管理员角色及现有 Skill／模板／路由修改；更新 PR #12。未授权业务项目迁移或需求验收 |

本需求沿用 `qshanx/docs-governance#11`，执行状态只在 Issue 维护；本地能力规格用 r1、r2 记录文档修订，发布版本归 CHANGELOG。本轮没有导出交付物，未新增发布或业务验收状态。

本次只登记新增能力，不代表既有全部功能已完成 PRD 基线整理。既有能力从 [使用说明](../../使用说明.md) 导航。

## 交付与变化

本轮范围和验收条件见能力规格。任务状态沿用项目的 [GitHub Issues](https://github.com/Seekers2001/docs-governance/issues)，本轮评审由 [Issue #11](https://github.com/qshanx/docs-governance/issues/11) 与 [草稿 PR #12](https://github.com/qshanx/docs-governance/pull/12) 承接，未调整看板。历史变更见 [PROJECT_LOG](../../PROJECT_LOG.md)，待发布变化见 [CHANGELOG](../../CHANGELOG.md)。

本轮新增产品管理入口、可复用 Skill 和模板，原因是已有治理缺少需求来源、当前基线与交付反馈的连续管理。没有替代既有技术治理规则，也没有追认历史草案。

## 验收与审查

本轮文档与插件结构验收记录见 [需求评审](07-requirements-review.md) 与 [测试上线](09-test-release.md)。业务项目试点尚未执行，未宣称已验证跨项目使用效果。

## 文档护栏

项目规则在 [位置配置](../../.docs-governance.json)，执行方式见 [护栏说明](../../references/document-policy.md)。按阿磊确认，仅按变更与提交触发，CI 复验；不增加每日定时审计。

## 接入可行性

[跨项目评估](../audits/2026-09-22-cross-project-feasibility.md)已补充。自身检查通过不代表可直接推广，强制启用前须核对项目范围、既有 hooks、规则误报和历史问题；已发现的推广障碍尚待修正。
