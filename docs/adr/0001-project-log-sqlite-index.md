# ADR-0001：PROJECT_LOG 使用 Markdown 原文与 SQLite 派生索引

- Status: accepted
- Date: 2026-08-02

## Context

`PROJECT_LOG.md` 必须保持 Git 可读、只追加并可追溯，但事件超过 200 条后，按类型、模块、引用和时间复盘的成本会明显上升。若直接把数据库作为唯一事实源，会失去普通 diff、代码审查和无工具环境下的可读性。

## Decision

保留 Markdown 事件作为唯一事实源。活跃事件超过 200 条后，经用户确认，把旧事件原样移入 `PROJECT_LOG.archive.md`，活跃文件保留最近 100 条；同时从活跃文件与归档重建 `.governance/project-log.sqlite`。

SQLite 只包含事件哈希、日期、类型、摘要、模块、源位置及引用，不提交进 Git，也不存放排期和任务状态。

## Alternatives

- 只保留单一 Markdown：最简单，但长期分类、统计和引用查询成本过高。
- 数据库成为唯一事实源：查询方便，但失去 Git 原生审阅与可恢复性。
- 每次按季度手工拆文件：可读，但容易重复、漏项且无法保证幂等。

## Reason

Markdown 原文提供可审阅、可移植的事实层；SQLite 提供可丢弃、可重建的查询投影。内容哈希去重使重复执行保持幂等，数据库损坏时可从 Git 中的两份 Markdown 完整恢复。

## Consequences

- 收益：长期日志可按时间、类型、模块和引用查询，原始证据仍可直接审阅。
- 代价：增加一个标准库脚本和对应测试；归档属于受控的 LOG 压缩例外。
- 可逆性：删除 `.governance/project-log.sqlite` 后运行重建命令即可恢复；归档事件可原样合并回活跃 LOG。
- 不可逆部分：无。

## Status

accepted

## Related

- `scripts/project-log-index.py`
- `skills/documentation/living-docs-governance/SKILL.md`
- `commands/governance-retro.md`

## Supersedes

None
