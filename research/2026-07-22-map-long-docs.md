# mattpocock/skills：Map 与长文档治理贡献研究

研究日期：2026-07-22
上游快照：`ed37663cc5fbef691ddfecd080dff42f7e7e350d`

## 结论

存在真实贡献机会，但需要拆成两个边界清晰的方向：

1. **`CONTEXT.md` 的持续精简规则**：这是当前最小、最稳的 PR 机会。准确议题已经存在于 [#130](https://github.com/mattpocock/skills/issues/130)，Matt 明确认可继续 harden skill guidance。可补充 “curate, don't append”：更新前先找现有术语，优先改写、合并或删除过时与重复条目；历史交给 Git/ADR。
2. **`CONTEXT.md` 的拆分与 `CONTEXT-MAP.md` 迁移规则**：值得继续研究，但准确议题已经存在于 [#321](https://github.com/mattpocock/skills/issues/321)，不应新建重复 Issue。最有价值的补充是把拆分条件定义为“出现多个可独立理解的领域边界”，而不是简单按行数或 monorepo 结构判断。这个方向涉及现有 artifact 语义，必须先得到维护者确认。
3. **通用项目文档地图与长文档防腐**：问题真实，但不属于现有 `CONTEXT-MAP.md`。它更接近 [#307 Documentation Review & Alignment Skill](https://github.com/mattpocock/skills/issues/307)，而 Seekers2001 已经在该 Issue 下提出了一个窄版、review-only 的实现边界。应等待维护者反馈，不另开同义 Issue。

因此，本轮不创建新 Issue。最优路线是先在 #130 给出具体的最小补丁边界并等待确认；#321 先确认产品语义；#307 等待现有提案得到维护者认可。

## 1. 当前设计

`domain-modeling` 的 `CONTEXT.md` 不是通用项目说明，而是项目特有领域词汇的 glossary。现有规则要求定义简短、排除一般编程概念，并在自然聚类出现时使用小标题。

- [CONTEXT-FORMAT：内容规则](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/domain-modeling/CONTEXT-FORMAT.md#L25-L30)
- [domain-modeling：CONTEXT.md 只保存 glossary](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/domain-modeling/SKILL.md#L60-L64)

仓库已经支持多个领域上下文：根目录 `CONTEXT-MAP.md` 只列出各 context 的位置和相互关系，每个 context 拥有自己的 `CONTEXT.md`。

- [CONTEXT-FORMAT：single vs multi-context](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/domain-modeling/CONTEXT-FORMAT.md#L32-L60)
- [domain-modeling：多 context 文件结构](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/domain-modeling/SKILL.md#L10-L40)

但 setup skill 只检查 monorepo 信号，并且只在发现 monorepo 时提供 multi-context 选项。这把“代码仓库拓扑”当成了“领域边界”的近似指标。

- [setup：只检查 monorepo signals](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/setup-matt-pocock-skills/SKILL.md#L19-L36)
- [setup：仅 monorepo 提供 multi-context](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/setup-matt-pocock-skills/SKILL.md#L59-L61)

## 2. 已有用户证据

- [#190](https://github.com/mattpocock/skills/issues/190)：用户报告反复运行后 `CONTEXT.md` 过大；Matt 的建议是让 `/grill-with-docs` 将文件变得更简洁。这表明“文件长”本身首先是 pruning 问题，不自动构成拆分理由。
- [#130](https://github.com/mattpocock/skills/issues/130)：多名用户报告 `CONTEXT.md` 被当成 spec/plan 并持续膨胀。Matt 已明确表示可以继续 harden skill guidance，并保持 Issue 开放。现有修复只强化了“glossary only”，还没有写明更新时应合并、替换和删除，而非只追加。
- [#321](https://github.com/mattpocock/skills/issues/321)：一个 bounded context 的 `CONTEXT.md` 超过 1000 行，Issue 仍开放；triage 已把目标整理为说明何时保持单文件、何时允许 sub-domain split，以及如何保持唯一入口和所有权。
- [#396](https://github.com/mattpocock/skills/issues/396)：用户的 `CONTEXT.md` 达到 3000 行，最终自行按照现有 context-map guidance 拆分后关闭 Issue。说明机制存在，但缺少明确的迁移决策规则。
- [#370](https://github.com/mattpocock/skills/issues/370)：进一步质疑 glossary 是否会成为可变的伪真相和维护负担。任何改进都应降低而不是扩大治理面。

## 3. 真正的缺口

最小缺口是持续更新语义：现有文字强调 “update it right there”，却没有同时要求先检索现有概念并改写、合并或删除旧定义。这会让 Agent 把“及时捕获”执行成“只追加”。`CONTEXT.md` 应保存当前语言；历史应由 Git 和真正满足门槛的 ADR 保存。

缺的不是 `CONTEXT-MAP.md` 文件格式，而是从一个不断增长的 `CONTEXT.md` 迁移到多 context 结构时的判断规则：

- “超过 N 行”不是领域边界，不能作为硬阈值。
- monorepo 也不等于多个 bounded contexts；单仓库同样可以包含多个领域边界。
- 如果内容只是同一领域的词汇变多，应先去重、收紧定义、删除非领域词汇并分小标题。
- 只有当词汇集合具有独立不变量、可以在局部独立理解、并且与其他集合存在可说明的关系时，才应拆为独立 context。
- 拆分后根 `CONTEXT-MAP.md` 仍只是入口和关系图，定义只保存在各自 `CONTEXT.md`，避免第二份真相。

这与项目现有的 single source、progressive disclosure 和最小流程哲学一致，也直接回答 #321，而不引入新的治理系统。

## 4. 推荐贡献

### 首选：参与现有 #130

不新建 Issue。先在 #130 提供如下窄版提议并等待维护者确认：

> A small remaining gap appears to be update semantics rather than another artifact or a length limit. The current guidance clearly says that `CONTEXT.md` is glossary-only, but “update it right there” can still bias an agent toward append-only growth. I propose hardening the format with one rule: **curate, don't append** — before adding a term, search for the existing concept; update or merge the canonical definition, and remove obsolete or duplicate entries. `CONTEXT.md` should describe the current domain language; Git and ADRs preserve history. If this matches the intended fix for #130, I can send a small documentation-only PR with the rule, the public docs sync, and a changeset.

这个提议不设置武断行数上限、不增加新 artifact，也不重复已有 “glossary only” 修复。

已于 2026-07-22 提交该提议：[Seekers2001 在 #130 的评论](https://github.com/mattpocock/skills/issues/130#issuecomment-5047515253)。当前状态：等待维护者确认，不提前创建 PR。

2026-07-23 更新：按用户授权完成了三文件实现并推送到 fork：

- [分支 `agent/curate-context-glossary`](https://github.com/Seekers2001/skills/tree/agent/curate-context-glossary)
- [commit `6a15d2e`](https://github.com/Seekers2001/skills/commit/6a15d2e)
- [与上游 main 的 compare](https://github.com/mattpocock/skills/compare/main...Seekers2001:skills:agent/curate-context-glossary)

GitHub 拒绝创建上游 PR：`Seekers2001 does not have the correct permissions to execute CreatePullRequest`。已将实现和权限阻塞回贴到 [#130](https://github.com/mattpocock/skills/issues/130#issuecomment-5053634048)，等待维护者开放/邀请外部贡献权限或直接采用 commit。

维护者认可后的最小 PR 文件范围：

1. `skills/engineering/domain-modeling/CONTEXT-FORMAT.md`
   - 增加 “curate, don't append” 规则。
2. `docs/engineering/domain-modeling.md`
   - 同步公开行为说明。
3. `.changeset/<slug>.md`
   - 记录 patch 级文档行为修正。

### 次选：参与现有 #321

不新建 Issue。先在 #321 提供一个窄的实现提议，并等待维护者确认：

> I think the missing rule is not a line-count threshold but a domain-boundary test. A large `CONTEXT.md` should first be pruned and grouped. It should become multiple contexts only when the clusters have distinct invariants, can be understood independently, and have relationships worth naming in `CONTEXT-MAP.md`. This also suggests setup should not use monorepo structure as the only signal for offering multi-context docs. If that direction matches the intended model, I can prepare a small documentation-only PR covering the decision rule and migration path, without adding a new artifact or command.

这段回复比新建 Issue 更合适，因为 #321 的 acceptance criteria 已经覆盖了目标。

已于 2026-07-23 提交：[Seekers2001 在 #321 的评论](https://github.com/mattpocock/skills/issues/321#issuecomment-5053627161)。该方向保持独立，尚未实现，等待维护者确认领域边界判据。

### #321 获认可后的小型 PR

建议只修改：

1. `skills/engineering/domain-modeling/CONTEXT-FORMAT.md`
   - 增加“先 prune/group，再按领域边界 split”的决策规则。
   - 明确不采用固定行数阈值。
   - 给出从根 `CONTEXT.md` 到 `CONTEXT-MAP.md` + per-context files 的最小迁移步骤。
2. `skills/engineering/setup-matt-pocock-skills/SKILL.md`
   - 不再把 monorepo 作为唯一 multi-context 信号；增加已存在多个稳定领域边界这一信号。
3. 对应的人类文档与 changeset
   - 仅同步实际行为变化，不增加新 skill、command 或 artifact。

是否需要修改 `domain-modeling/SKILL.md`，应以维护者对 #321 的反馈为准；如果 `CONTEXT-FORMAT.md` 已足以承载规则，则不要多改一个文件。

## 5. 不建议的贡献

### 不把 `CLAUDE_MAP.md` 改名后塞进 `CONTEXT-MAP.md`

两个 map 回答不同问题：

- 上游 `CONTEXT-MAP.md`：有哪些领域上下文，它们如何关系。
- docs-governance 的 `CLAUDE_MAP.md`：代码树无法直接表达的导航、依赖方向、误导路径和禁区。

混合后会让 glossary map 同时承担项目导航，破坏现有 artifact 边界。

### 不向 #321 塞入完整长文档治理

文档与代码漂移、孤儿文档、重复权威和 instruction bloat 已由 [#307](https://github.com/mattpocock/skills/issues/307) 覆盖。Seekers2001 已在该 Issue 提出 review-only、repository-agnostic 的 `/review-docs` v1，并明确不强制文件名和目录结构。下一步应等待维护者回应，而不是再提交一个 `CLAUDE_MAP.md + PROJECT_STATUS.md + PROJECT_LOG.md` 框架。

### 不直接开 PR

该仓库的开放 Issue 已经表现出明显的 issue-first 流程，而且 #321 仍缺维护者产品决策。没有认可前直接改 setup 行为，容易把合理研究变成未经请求的产品选择。

## 最终判断

- **Map 可以贡献**：贡献的是 bounded-context 拆分判断与迁移指导，不是通用目录地图。
- **长文档治理可以贡献**：通过现有 #307 的文档审计方向推进，不把整套 docs-governance 搬进去。
- **现在最值得推进的是 #130**：Matt 已明确认可 harden guidance，且可以形成三文件的文档级最小 PR。
- **Map 的下一步是 #321**：先确认“领域边界，而非长度/monorepo”这个判断是否符合维护者意图。
- **当前不创建新 Issue，不直接开 PR**：先在现有 Issue 中获得维护者方向。
