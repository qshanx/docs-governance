# PROJECT_STATUS.md — 插件健康仪表盘

> 红线块每次进会话必读；指标按需。

## 🔴 红线块（每次必读 —— 删除区 + 未决 P0）

### 删除区（故意删的，别重建）
| 路径 | 原因 | 日期 | 替代物 |
|---|---|---|---|
| `README.en.md` | 英文概览统一回主入口 | 2026-09-05 | `README.md` |
| `research.md` | 研究资料归位，不在根目录重建 | 2026-10-10 | [Wayfinder 研究](research/2026-07-22-wayfinder-decision-lifecycle.md) |
| `research-map-long-docs.md` | 研究资料归位，不在根目录重建 | 2026-10-10 | [Map 与长文档研究](research/2026-07-22-map-long-docs.md) |
| `TEST_COLLABORATION_PROPOSAL.md` | 已实施方案保留为评审历史，不在根目录重建 | 2026-10-10 | [测试协作历史方案](docs/archive/2026-07-12-test-collaboration-proposal.md) |
| `skills/documentation/docs-retro/SKILL.md` | 复盘方法合并，文档管理作为检查面，不重建并列入口 | 2026-10-13 | [project-retro](skills/engineering/project-retro/SKILL.md) |
| `skills/engineering/test-retro/SKILL.md` | 复盘方法合并，测试作为检查面，不重建并列入口 | 2026-10-13 | [project-retro](skills/engineering/project-retro/SKILL.md) |

### 未决 P0
- 暂无已确认 P0；普通验证缺口和范围决策见下文。

## 验证缺口与待确认范围（按需读）

- PH-20261011：项目健康静态采集与 15 项回归已接入；静态候选不代表整体健康通过。不同基线的实跑、独立复核与 PR 验证见 [验证记录](docs/product/09-test-release.md#ph-20261011项目健康采集实跑)。

- 文档按事实核对已补接口字段切片、固定样例和已知场景复核；独立盲测、其他事实类型及真实项目成本尚未验证，见 [TEST-IMPACT-001](TESTS.md#test-impact-001事实变化后的文档核对)。Issue #5 保持打开，不把该切片当作完整自动语义检测能力。

- `writing-for-agents` 替代未发布的 technical-doc-writing；上游来源与许可证随包保留，含义核对为本地补充。原 r8 试跑仅证明旧方法，不能证明新 Skill 的宿主调用或业务效果。

- 统一 setup 已在本地接上三类项目识别、产品文档与 Agent 入口 Skill；init 为兼容别名。`agent-entrypoints` 保留八项规范和逐文件 200 行检查，并区分稳定规则与单次授权；未新装门禁。实际验证范围见 [r7 测试记录](docs/product/09-test-release.md)。PR #14 本地工作树已整合 PR #12 并解决冲突，修复尚未推送；原生宿主与业务效果未验证，不能据旧 PR 绿色结果合并。

- `product-docs-manager` 已新增角色与共享规则，来源、编号、状态、授权及按任务读取场景已做文本复核；Claude Code 原生角色调度、实际上下文节省和业务项目实际试点仍未验证，见 [角色审查](docs/product/07-requirements-review.md)。

- `product-evolution` 已完成 11 个登记项目只读适配评估；Stop 全文件指纹及存量告警阻断等推广障碍尚未修复，PR #12 保持草稿。Stop 子目录根定位已按评审修复并验证显式根、独立子项目和 worktree；PR 前扫描已通过独立提交快照和本地真实 push 阻断测试。宿主原生事件、业务项目安装试点及运营效果未验证，见 [跨项目评估](docs/audits/2026-09-22-cross-project-feasibility.md)。

- `/governance-init` 旧独立流程的空项目首跑证据保留在 `docs/audits/2026-08-13-governance-init-empty-project.md`；现已改为统一 setup 别名，旧结果不证明新流程通过。原生 slash command 尚未验证。
- `test-collaboration` 已在本插件完成首次测试资产盘点，并把两项审计误报归入 `TEST-AUDIT-001`；仍待业务项目完成试点（首选：经营报表加工系统）。
- `loop-design-check` skill 与两条主线主题不合（小磊已确认"没关系"），挪出待拍板。

## 📥 Backlog（方法论优化，2026-07-02 小磊逐条批准；等 dogfood 撞到或排期再做，不抢跑）

1. **审计事实层下沉成脚本（部分完成）**：✅ `audit-docs.py` 已查路径/链接、LOG 活跃+归档完整性、ADR 索引、TEST-ID 和孤儿文档并按退出码短路；⏳ STATUS 可量化指标自动生成尚未做。
2. ✅ **commit 前固化核对**（2026-07-02 已做：templates/pre-commit.example + 两命令接入 + 四段测试）：staged 含代码改动 → PROJECT_LOG.md 必须同批 staged；豁免=只改 tests//docs//治理文件 或 --no-verify；做成 templates/pre-commit.example。旧 init 自动安装已被 r7 统一 setup 的明确授权边界替代。只拦这一条最小可判定不变量，MAP/STATUS 不在 commit 关口硬卡（防狼来了）。
3. **LOG 消费端（部分完成）**：✅ 超过 200 条事件可归档并生成 SQLite 类型/模块/引用索引；⏳ audit 自动输出 fix 热点统计尚未做。
4. **四件套并发约定**：LOG append-only 各写各行；STATUS/MAP 指定"谁拥有谁改"（同契约线"谁改契约谁是主任"）。
5. **文档复利三动作**：① 跑通的有效做法按主记录留证据；② 2026-10-13 按阿磊本次确认，以 project-retro 的“提炼 → 独立复验 → 升级”替代“LOG fix ≥2 次直接升入口规则”，落点按规则用途选择；③ ≥2 项目重复的 spec/references/placeholder 回流模板母版仍为待办。
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
| Skill 路由与用户文档 | 20 个活动 Skill 均进入总路由、README、使用说明；新增 pr-review，复盘仍统一为 project-retro（2026-10-13 工作区检查） | 无漏登 = 绿 | 🟢 |
| Python 单元测试 | 本 PR 隔离分支结果见[提交验证](docs/product/09-test-release.md#pr-20261014隔离提交与验证)；共享工作区历史 127 项不替代本分支结果 | 全过 = 绿 | 🟢 |
| 自动 CI | 完整 verify 与日志基线比较已在 PR #4 的 dad0dd2 验证；后续提交逐次核对 checks（证据见 [本轮验证](docs/audits/2026-09-05-shared-audit-results.md)） | PR / push 成功运行 = 绿 | 已接通；结果按提交核对 |
| skill / agent 内部去重 | 是（方法论仅 skill 一处） | 唯一源 | 🟢 |
| 真实项目 dogfood | 4（经营报表审计、礼仪 demo 审计+修复、本插件自治理、audit-blog 审计） | ≥2 | 🟢 |
| 可发布底座 | git / LICENSE / CHANGELOG / .gitignore / verify 齐 | 齐 = 绿 | 🟢 |
| README 安装/样例 | 市场安装命令 + 验收命令 + 真实审计样例（2026-07-02 补） | 齐 = 绿 | 🟢 |
