# 文档治理变更影响矩阵

阶段收尾或用户说"同步一下 / 整理一下 / 收尾 / 新人能接手"时，用这张表判断本次改动应同步哪些治理文件。

核心纪律：`PROJECT_LOG.md` 是历史，只追加；`CLAUDE_MAP.md` / `ARCHITECTURE.md` / `PROJECT_STATUS.md` / `CLAUDE.md` 是当前真相，要修正旧事实、合并重复、删除过期内容。

## 代码 / 项目变化 -> 治理文件

| 本次发生的事 | 必须检查 / 更新 |
|---|---|
| 新增、删除、改名顶层目录或核心 Module | `CLAUDE_MAP.md` 路径与入口；`ARCHITECTURE.md`（若已启用）的 Module 权责、依赖图与相关核心流转；`PROJECT_LOG.md` 追加结构变更 |
| 新增入口文件、命令、脚本、服务端口 | `CLAUDE_MAP.md` 入口表；README 运行说明；`PROJECT_LOG.md` 追加 |
| 新增或改变测试方式 | `PROJECT_STATUS.md` 测试健康指标；`CLAUDE.md` 验证硬规则（仅当成为长期规则）；`PROJECT_LOG.md` 追加 |
| 指标越过阈值（行数、覆盖率、测试缺失、依赖风险） | 核对实际影响，按 Skill 的风险规则更新 `PROJECT_STATUS.md`；有意义的发现或处置结果才记入 `PROJECT_LOG.md`，不按单一数值自动定为 P0 |
| 故意删除文件、废弃模块、清理备份目录 | `PROJECT_STATUS.md` 删除区（路径、原因、日期、替代物）；`PROJECT_LOG.md` 追加 cleanup |
| 文件归位或自动审计触发约定变化 | 项目位置配置、`references/document-policy.md`、对应测试与入口说明；确认仅约束文档／文件，不代作业务决策 |
| 新增硬规则、编码约束、不可违背流程 | `CLAUDE.md`；必要时链接到 docs；`PROJECT_LOG.md` 追加 governance |
| README、docs、代码结构互相矛盾 | 修正当前真相所在文件；不要只在 LOG 里解释；`PROJECT_LOG.md` 可追加 audit/fix |
| 新增环境变量、密钥配置、部署参数 | `CLAUDE.md` 或 README 的配置指路；`PROJECT_STATUS.md` 风险项（如密钥/公网）；`PROJECT_LOG.md` 追加 |
| 新增业务流程、用户动线、页面或视图 | `CLAUDE_MAP.md` 找 X 去这里；若跨 Module 主链路或状态归属改变，同步 `ARCHITECTURE.md` 核心流转图；README 演示/运行说明（如面向人类用户）；`PROJECT_LOG.md` 追加 |
| 新增 API / 路由 / 前后端字段变化 | `CONTRACT.md` 指向的机器契约及版本（若存在）；`CLAUDE_MAP.md` 前端入口 / API 封装 / 后端路由位置；`PROJECT_LOG.md` 追加 contract |
| 新增接口但项目尚无 `CONTRACT.md` | 报告建议创建 `CONTRACT.md`；不要把字段细节塞进 `CLAUDE_MAP.md` |
| 领域术语、概念关系或采用口径变化 | `CONTEXT.md`（若已启用）；证据未确认时只列待确认，不改代码口径 |
| 架构、数据库、认证、部署、数据模型或 API 版本等难回退决策 | `docs/adr/` 新建/更新单项 ADR；`docs/adr/README.md` 更新索引；MAP 只挂索引入口；LOG 追加 decision |
| 产品阶段产物、当前生效要求或迭代范围变化 | 按 `product-evolution` 核对产品目录十阶段入口；更新唯一需求主记录、确认来源和受影响阶段，评审后更新基线；运营反馈回到调研／分析，不复制任务状态 |
| 成功标准、需求或 Bug 变化 | 原始 Spec/Issue 保持唯一来源；`TESTS.md` 关联 TEST-ID/人工出口；不要复制标准 |
| Module 权责、状态归属、Interface 或代码依赖方向变化 | `ARCHITECTURE.md` 的权责表与依赖图；MAP 只检查入口；必要时 ADR；`PROJECT_LOG.md` 追加结构变更 |
| Module 行为或下游依赖变化 | `REGRESSION.md` 的下游与执行命令；相关 TEST-ID；实施后跑本 Module 和下游 |
| 数据迁移、破坏性接口或高风险发布 | 变更影响报告中的兼容期、迁移/恢复/回滚和不可逆部分；必要时 ADR / CONTRACT |
| 任务负责人、阻塞或项目排期变化 | Issue Tracker；STATUS 只在健康风险变化时更新，LOG 数据库不存排期 |

## 四件套与可选载体职责回查

| 文档 | 收尾时问自己 |
|---|---|
| `CLAUDE.md` | 本次是否产生长期硬规则？是否有细节应挪到 MAP/STATUS/LOG？ |
| `CLAUDE_MAP.md` | 新人是否能从这里找到入口、测试、关键文件和 `ARCHITECTURE.md`？是否避免复制架构正文？ |
| `ARCHITECTURE.md`（可选） | Module 权责、状态归属、代码依赖图和运行时核心流转是否与真实代码一致？ |
| `PROJECT_STATUS.md` | 当前风险、健康指标、待删区是否有来源？验证版本、环境和范围是否匹配，相关变化后是否标待复验？ |
| `PROJECT_LOG.md` | 本次有意义的变更是否追加一行？是否避免改旧历史？ |
| `CONTRACT.md` | 是否登记唯一机器契约、版本和生成/校验入口，字段是否只在机器契约定义？ |
| `CONTEXT.md`（可选） | 是否只写稳定领域语言，且与代码/契约证据一致？ |
| `docs/adr/`（可选） | 难回退决策是否一项一文件、状态与索引一致、写明可逆性？ |
| 产品管理入口（可选） | 十阶段是否可导航，生效范围和确认来源是否明确，需求、任务、验收与效果是否可追溯？ |
| `TESTS.md`（可选） | 成功标准是否链接回 Spec/Issue，证据是否关联 TEST-ID？ |
| `REGRESSION.md`（可选） | 实际受影响模块及下游是否有可执行命令并已运行？ |

## 收尾同步流程

1. 盘点本次改动：优先看会话记录、`git status -s`、最近修改文件、用户明确说过的完成项。
2. 对照上表列出"应更新文档"。
3. 对每份治理文件判断：已同步 / 需要更新 / 需要用户确认。
4. 能确定的当前真相直接更新；不能确定的列入交付摘要的"待确认"。
5. 故意删除或废弃的东西必须进 `PROJECT_STATUS.md` 删除区，避免下个 agent 重建。
6. 最后按需追加 `PROJECT_LOG.md`，记录本次有意义的阶段成果和理由；重复核对且没有新结果时不另记一条。
7. 若有变更影响分析，对照实际 diff，报告超范围改动、未验证项和临时兼容逻辑。

## 不要做

- 不要把所有内容都追加到 `CLAUDE.md`；它只放硬规则和路标。
- 不要把 Module 表或流程图放进 `CLAUDE_MAP.md`；当前架构放 `ARCHITECTURE.md`。不要把接口字段细节放进 ARCHITECTURE；字段契约放 `CONTRACT.md`。
- 不要用 `PROJECT_LOG.md` 替代当前状态修正；LOG 只解释历史。
- 不要为了"看起来完整"编造没量过的指标。
- 不要把排期和任务状态搬进 STATUS、LOG 或 SQLite；沿用项目已有 Issue Tracker。
