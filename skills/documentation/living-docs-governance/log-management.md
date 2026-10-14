# 日志管理

仅在日志统计、追加或归档任务中读取；环境经验提炼、复验与升级交给 `skills/engineering/project-retro/SKILL.md`。

`log: 一句话` 只追加一个标准格式事件，不启动 setup 或归档。

### 日志归档与索引

> **LOG 防腐：按事件计数 + 复盘 + 可重建索引。** `PROJECT_LOG.md` 的事件格式是 `## [日期] 类型 | 摘要`；阈值按事件数计算，不按原始行数。活跃事件不超过 200 条时只用 Markdown；超过 200 条后：
> 1. **先只读复盘**：识别重复问题和应下沉的 lint / TEST-ID / 回归保护。
> 2. **经用户确认再归档**：运行 `python3 <插件目录>/scripts/project-log-index.py archive --root <项目根> --yes`。旧事件原样进入 `PROJECT_LOG.archive.md`，活跃 LOG 默认保留最近 100 条；归档是受控压缩例外，不得手工删改历史。
> 3. **建立派生索引**：脚本从活跃 LOG + archive 重建 `.governance/project-log.sqlite`。数据库默认进 `.gitignore`，不是唯一事实源；损坏或删除后运行 `rebuild` 即可恢复。
> 4. **分类不猜**：类型取事件头；模块只在明确写出或能从真实路径解析时登记，否则为 `unclassified`；引用只提取 commit、TEST-ID、ADR、CONTRACT 和明确路径。内容哈希保证幂等。
> 5. **失败不伤原文**：解析、归档或建库失败时，不得留下被截断的 `PROJECT_LOG.md`。审计以活跃文件和 archive 的事件合集判断只追加完整性。
> 6. **目录 + 内容分层**：主 LOG 只当**目录**——每条一行（`## [日期] 类型 | 一句话`），需要长详情（完整审计报告、大段修复记录）时下沉到独立文件（如 `docs/log-details/2026-07-03-audit.md`），目录行尾挂链接。主 LOG 永远短、可整读；详情按需点开。这就是「脊柱保持瘦、血肉下沉」用在 LOG 自己身上。
> 7. **统计提供线索**：归档前按下节读取日志，统计重复错误及标准变化；环境经历使用 `/governance-retro 全量日志` 进入 project-retro；测试资产候选交给 test-collaboration。重复问题是候选，仍需核对已有保护、原因及措施效果；本文件不维护另一套经验升级流程。

### 日志统计

默认只读全量；指定起始日期时仅统计该日期起的事件。先运行 `project-log-index.py status --root <项目根>`，再读活跃 LOG；全量模式存在 archive 时一并读。索引可辅助查询，证据必须能回到 Markdown；LOG 不存在时报告缺失。

按真实类型和明确路径统计模块 fix 热点前五、出现至少两次的错误类型、标准变更的旧值/新值/理由和审计间隔；对照期间 commit 数，不凭目录名猜模块。连续放宽标准要提示；重复错误提出回归测试/lint/schema 的下沉候选，并关联 `test-collaboration`。

输出分布、重复错误、标准审查和候选线索；环境问题交给 project-retro 判读，测试资产问题交给 test-collaboration；统计次数不等于经验已复验有效。修复、补测及经确认归档是后续写入动作，不混入只读统计；不把任务排期写入 SQLite。
