# PROJECT_STATUS.md — 插件健康仪表盘

> 红线块每次进会话必读；指标按需。

## 🔴 红线块（每次必读 —— 删除区 + 未决 P0）

### 删除区（故意删的，别重建）
| 路径 | 原因 | 日期 | 替代物 |
|---|---|---|---|
| `README.en.md` | 英文概览统一回主入口 | 2026-09-05 | `README.md` |

### 未决 P0
- 暂无已确认 P0；普通验证缺口和范围决策见下文。

## 验证缺口与待确认范围（按需读）

- `product-evolution` 已完成 11 个登记项目只读适配评估；全文件指纹、子目录根定位及存量告警阻断等推广障碍尚未修复，PR #12 保持草稿。业务项目安装试点及运营效果未验证，见 [跨项目评估](docs/audits/2026-09-22-cross-project-feasibility.md)。

- `/governance-init` 的 Codex 共享流程已在真实空项目首跑；Claude Code 原生 slash command 尚未验证（证据见 `docs/audits/2026-08-13-governance-init-empty-project.md`）。
- `test-collaboration` 已在本插件完成首次测试资产盘点，并把两项审计误报归入 `TEST-AUDIT-001`；仍待业务项目完成试点（首选：经营报表加工系统）。
- `loop-design-check` skill 与两条主线主题不合（小磊已确认"没关系"），挪出待拍板。

## 📥 Backlog（方法论优化，2026-07-02 小磊逐条批准；等 dogfood 撞到或排期再做，不抢跑）

1. **审计事实层下沉成脚本（部分完成）**：✅ `audit-docs.py` 已查路径/链接、LOG 活跃+归档完整性、ADR 索引、TEST-ID 和孤儿文档并按退出码短路；⏳ STATUS 可量化指标自动生成尚未做。
2. ✅ **commit 前固化核对**（2026-07-02 已做：templates/pre-commit.example + 两命令接入 + 四段测试）：staged 含代码改动 → PROJECT_LOG.md 必须同批 staged；豁免=只改 tests//docs//治理文件 或 --no-verify；做成 templates/pre-commit.example，/governance-init 自动装。只拦这一条最小可判定不变量，MAP/STATUS 不在 commit 关口硬卡（防狼来了）。
3. **LOG 消费端（部分完成）**：✅ 超过 200 条事件可归档并生成 SQLite 类型/模块/引用索引；⏳ audit 自动输出 fix 热点统计尚未做。
4. **四件套并发约定**：LOG append-only 各写各行；STATUS/MAP 指定"谁拥有谁改"（同契约线"谁改契约谁是主任"）。
5. **文档复利三动作**（skill 加一节"文档作为再生产资料"）：① 跑通即存 references/ ② LOG fix 热点 ≥2 次的坑升级成 CLAUDE.md 硬规则 ③ ≥2 项目重复的 spec/references/placeholder 回流模板母版。
6. ✅ **模块回归审计**（2026-07-03 首版：module-regression skill + regression-auditor agent + /regression-audit 命令 + REGRESSION.example 模板；⚠️ 未在真项目实测，首选试点=经营报表）
7. ✅ **测试协作治理 v1**（2026-07-12：test-collaboration skill + TESTS.example 模板；判定点职责从 REGRESSION.md 迁为 TEST-ID 引用；2026-07-24 补同一机器契约驱动消费者/提供者/联调测试证据；不新增 agent/command/脚本；⚠️ 待真实项目试点）
8. ✅ **Codex 总路由 + CONTEXT / ADR / 变更影响**（2026-08-02：新增 docs-governance、context-and-decisions、change-impact；成功标准留在 Spec/Issue，实施后对照实际 diff，难回退决策一项一 ADR）
9. ✅ **PROJECT_LOG 结构化归档**（2026-08-02：按事件计数，>200 经确认归档，Markdown 保持事实源，SQLite 默认忽略且可重建；脚本单测覆盖计数、幂等、确认门和完整保留）
10. ✅ **文档审计范围化**（2026-08-02：spine/context/adr/artifacts/full；确定性失败短路，语义层负责术语/决策/成功标准与重复真相；默认只读）

## 指标（按需读）

| 指标 | 现在 | 阈值 | 状态 |
|---|---|---|---|
| `scripts/verify.sh` | 通过 | 通过 = 绿 | 🟢 |
| Claude / Codex 双端 manifest | 名称与版本一致，skills 共用 | 一致 = 绿 | 🟢 |
| Skill 路由与用户文档 | 9 个 skill 均进入总路由、README、使用说明 | 无漏登 = 绿 | 🟢 |
| Python 单元测试 | 54 个（含位置规则、暂存快照与 Stop 行为） | 全过 = 绿 | 🟢 |
| 自动 CI | 完整 verify 与日志基线比较已在 PR #4 的 dad0dd2 验证；后续提交逐次核对 checks（证据见 [本轮验证](docs/audits/2026-09-05-shared-audit-results.md)） | PR / push 成功运行 = 绿 | 已接通；结果按提交核对 |
| skill / agent 内部去重 | 是（方法论仅 skill 一处） | 唯一源 | 🟢 |
| 真实项目 dogfood | 4（经营报表审计、礼仪 demo 审计+修复、本插件自治理、audit-blog 审计） | ≥2 | 🟢 |
| 可发布底座 | git / LICENSE / CHANGELOG / .gitignore / verify 齐 | 齐 = 绿 | 🟢 |
| README 安装/样例 | 市场安装命令 + 验收命令 + 真实审计样例（2026-07-02 补） | 齐 = 绿 | 🟢 |
