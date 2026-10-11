# `mattpocock/skills` 贡献机会研究

研究日期：2026-07-24
上游仓库：[`mattpocock/skills`](https://github.com/mattpocock/skills)
核对快照：[`ed37663`](https://github.com/mattpocock/skills/commit/ed37663cc5fbef691ddfecd080dff42f7e7e350d)

## 结论先行

从阿磊现有的 `docs-governance` 与 `dbskill` 方法论中，能提炼出 **4 个真实的上游贡献方向**。但只有其中 1 个已经具备“小补丁、范围稳定、实现完成”的 PR 条件；另外 3 个都已经有准确的上游 Issue，应继续在原 Issue 中等待维护者确认，不能再开同义 Issue，也不应抢跑提交实现。

| 优先级 | 机会 | 当前入口 | 判断 |
|---|---|---|---|
| 1 | `CONTEXT.md` 的 “curate, don't append” 更新规则 | [#130](https://github.com/mattpocock/skills/issues/130) | **可直接 PR，但受仓库权限阻塞**；补丁已完成 |
| 2 | `/implement` 收尾前的 documentation impact gate | [#560](https://github.com/mattpocock/skills/issues/560) | **应先等 Issue 方向确认**；已有他人 fork 实现，不要做竞争补丁 |
| 3 | review-only 的 agent-context / docs alignment audit | [#307](https://github.com/mattpocock/skills/issues/307) | **应先等 Issue 方向确认**；真实需求已有第二位用户案例 |
| 4 | 按领域边界拆分超长 `CONTEXT.md` | [#321](https://github.com/mattpocock/skills/issues/321) | **应先等 Issue 方向确认**；不能用行数或 monorepo 作为唯一判据 |
| 暂缓 | Wayfinder durable context / ADR lifecycle | [#556](https://github.com/mattpocock/skills/issues/556)、[#579](https://github.com/mattpocock/skills/issues/579) | **暂不建议 PR**；维护者已明确认为设计大于一句提示 |

仓库当前还限制外部创建 Issue/PR：GitHub 页面显示 “Issue creation is restricted” 和 “New Pull request creation is restricted”；开放的 5 个 PR 均来自维护者或机器人，而不是外部 fork。因此，“可直接 PR”在本文中表示**产品与补丁范围已经就绪**，不表示当前账号具备上游创建权限。[开放 PR 列表](https://github.com/mattpocock/skills/pulls)

按下一步动作归类：

- **可立即参与现有 Issue**：#130、#560、#307、#321；阿磊已经分别留下了有边界的方案，其中 #130 还有完整补丁。
- **需要先积累真实案例**：#639 对应的 skill 安全审查方向；至少先用阿磊的 `dbs-skill-cleaner` 对当前上游做一次可复现、人工复核过的扫描，不能凭第三方工具的一张报告提规则。
- **不建议**：新增 Wayfinder/ADR Issue、重复实现 #558、移植完整四文件治理、迁移/bridge 系统或隔离工具。

## 1. 判断标准

### 1.1 上游真正重视什么

上游 README 明确把这些 skills 定义为：

- small；
- easy to adapt；
- composable；
- 不接管用户的完整开发流程。

证据：[`README.md`](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/README.md#L15-L20)。

当前 `writing-great-skills` 又把可预测性建立在几条纪律上：

- 一个意义只有一个权威位置；
- 通过 context pointer 做 progressive disclosure；
- 新的 skill 或分支必须挣得它增加的 context/cognitive load；
- completion criterion 要小、可检查，防止 premature completion。

证据：[`writing-great-skills/SKILL.md`](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/productivity/writing-great-skills/SKILL.md)。

此外，[PR #650](https://github.com/mattpocock/skills/pull/650) 正把 `writing-great-skills` 重构为更通用的 `writing-for-agents`，覆盖 skill、`AGENTS.md` / `CLAUDE.md` 以及它们指向的文档。这意味着 agent instruction 治理更符合上游方向，但也意味着此处不应在 v1.2 重构尚未落定时另起一套平行规则。

### 1.2 阿磊的方法论里可移植的是什么

可移植的不是固定四件套，而是这些小规则：

1. **当前真相与历史记录分离**：当前权威文档可改写，历史交给 Git、Issue、ADR 或 append-only log。
2. **一文一职与单一真相源**：同一事实不在多处重复维护。
3. **按需读取与渐进披露**：入口保持瘦，细节通过指针按需加载。
4. **review-first**：先给证据、影响、置信度与最小修复，不自动重写。
5. **收尾影响检查**：实现完成时，明确判断哪些长期事实应回到长期权威来源。
6. **确定性检查优先**：路径、死链、重复等廉价检查先跑，LLM 只判断模糊语义。

本地证据：

- [`living-docs-governance/SKILL.md`](../skills/documentation/living-docs-governance/SKILL.md)：渐进式采用、分级读取、防腐规则、阶段收尾与“一文一职”。
- [`governance-audit.md`](../commands/governance-audit.md)：只读、便宜层先行、证据化分级报告。
- 外部本地材料 `dbs-agent-migration/SKILL.md`（未随本仓库分发）：多宿主规则文件审计、真源与 bridge 分离。
- 外部本地材料 `dbs-skill-cleaner/SKILL.md`（未随本仓库分发）：只读扫描、证据分级、用户确认后才执行。

其中“四份固定文件”“项目健康仪表盘”“通用项目地图”“全量迁移流程”都不适合直接移植到上游。

## 2. 机会一：`CONTEXT.md` 应 “curate, don't append”

### 当前缺口

`domain-modeling` 已明确规定 `CONTEXT.md` 只保存 glossary，不保存实现细节、spec 或 scratch material；但它同时要求术语一旦确认就 “update it right there”。当前 [`CONTEXT-FORMAT.md`](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/domain-modeling/CONTEXT-FORMAT.md) 还没有要求 Agent 在新增前先搜索、合并、改写或删除旧定义。

这会把“及时捕获当前真相”执行成“持续追加新条目”。[#130](https://github.com/mattpocock/skills/issues/130) 已有多名用户报告：

- `CONTEXT.md` 被写成 PRD/plan；
- 每轮 grilling 都继续增长；
- implementation details 渗入 glossary。

Matt 已在 [#130 的评论](https://github.com/mattpocock/skills/issues/130#issuecomment-4430175711) 中明确表示应 harden skill 内的 guidance。

### 最小解决办法

只新增一个更新语义：

> **Curate, don't append.** Before adding a term, search for the existing concept. Update or merge the canonical definition, and remove obsolete or duplicate entries. `CONTEXT.md` describes the current domain language; Git and ADRs preserve history.

它不增加文件、不增加 skill、不设武断行数上限，也不会把 `CONTEXT.md` 变成新的治理框架。

### 重复核对与当前状态

阿磊已经：

- 在 [#130 提交提议](https://github.com/mattpocock/skills/issues/130#issuecomment-5047515253)；
- 完成分支 [`agent/curate-context-glossary`](https://github.com/Seekers2001/skills/tree/agent/curate-context-glossary)；
- 完成 [commit `6a15d2e`](https://github.com/Seekers2001/skills/commit/6a15d2e)；
- 将权限阻塞与 compare 链接回贴到 [#130](https://github.com/mattpocock/skills/issues/130#issuecomment-5053634048)。

上游没有对应开放 PR；当前只是外部 fork 上的完整补丁。

### 判断

**这是当前唯一已经适合直接进入 PR 的方向。**

建议动作：不再追加解释，不再重做分支。等待维护者开放权限、邀请 collaborator 或直接 cherry-pick；一旦权限开放，使用现有分支创建 PR。

## 3. 机会二：`/implement` 的 documentation impact gate

### 当前缺口

当前 [`implement/SKILL.md`](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/implement/SKILL.md) 只要求：

```text
implement → tdd → code-review → commit
```

它没有在 commit 前核对：本次改动形成的长期事实是否已经进入仓库自己的长期权威来源。于是 spec/issue 可以正确记录交付历史，但新的领域术语、架构取舍或用户可见行为仍只留在历史交付物中。

这正是 `docs-governance` “阶段收尾同步”的可移植核心，但不能把四文件结构搬进上游。

### 最小解决办法

在 `/code-review` 与 commit 之间增加一个 bounded completion criterion：

1. 列出本次实现改变的 durable facts；
2. 找到仓库**已有的**长期权威来源；
3. 每项要么更新该来源，要么写一行 `N/A: <reason>`；
4. 所有项目被 accounted for 后才结束。

`CONTEXT.md`、ADR、产品/用户文档只是示例，不是强制文件名。没有 durable impact 的改动只支付一行 `N/A` 的成本。

### 重复核对与当前状态

阿磊已创建 [#560](https://github.com/mattpocock/skills/issues/560)，并在 [评论中进一步收窄实现范围](https://github.com/mattpocock/skills/issues/560#issuecomment-5018668875)。

另一位贡献者已经给出 [fork commit `f508bc1`](https://github.com/sridhar-3009/skills/commit/f508bc1)。阿磊又在 [review 评论](https://github.com/mattpocock/skills/issues/560#issuecomment-5030334989) 中指出了三个上游化缺口：

- 不能把 `CONTEXT.md` 写成强制真源；
- 要同步 human-facing docs；
- 要带 changeset。

### 判断

**应先 Issue，不应现在另做竞争分支。**

这是真实且很小的改进，但维护者尚未确认“默认 gate”是否值得所有 `/implement` 使用者支付。最合适的下一步是等待 Matt 对 #560 的产品判断；若认可，再由现有实现者或阿磊补齐完整三文件 patch。

## 4. 机会三：review-only 的 agent-context audit

### 当前缺口

上游已有：

- `domain-modeling`：主动维护 glossary / ADR；
- `code-review`：审查代码 diff；
- `research`：读取一手来源并留下 cited Markdown；
- `setup-matt-pocock-skills`：初始化 issue tracker、labels 和 domain doc layout。

但没有一个 on-demand、review-only 的流程去判断：

- `AGENTS.md` / `CLAUDE.md` 是否包含过期项目阶段和旧依赖；
- root 与 nested instruction 是否互相冲突；
- 历史、draft、rejected 文档是否被当成当前 authority；
- 是否发生 excessive context fan-out；
- 文档中的可检查陈述是否与代码、配置、测试冲突。

这是 `docs-auditor` 最有价值、也最容易上游化的一层；“生成四件套”不属于这个贡献。

### 最小解决办法

把 [#307](https://github.com/mattpocock/skills/issues/307) 的第一版进一步保持在 **agent-context review**：

1. 发现现有 instruction surfaces 与它们的 context pointers；
2. 区分 current authority 与 historical/draft/rejected/superseded material；
3. 用代码、配置、依赖、测试和 accepted decisions 验证关键陈述；
4. 每项只报告 exact instruction、evidence、agent-behavior impact、confidence 与 smallest remediation；
5. 停在 review，不自动改文件。

可采用“便宜检查先行”的原则，但不必在 v1 强制写脚本；否则一个小 review skill 会膨胀成框架。

### 重复核对与当前状态

阿磊已经在 [#307 提交窄版实现边界](https://github.com/mattpocock/skills/issues/307#issuecomment-5018670239)。

随后另一位 Codex 用户提供了 [真实失败案例](https://github.com/mattpocock/skills/issues/307#issuecomment-5066545301)：过期的 `AGENTS.md`、历史架构决定与广泛 context fan-out 使 Codex 给出“逻辑一致但基于旧状态”的答案。阿磊又在 [最新回复](https://github.com/mattpocock/skills/issues/307#issuecomment-5067084895) 中把第一版收敛为 agent-context review。

当前没有关联分支或 PR，也没有维护者方向确认。

### 判断

**应先 Issue，等待维护者确认。**

这是比 #560 更大的新 skill，涉及 invocation、README、plugin manifest、OpenAI metadata、human docs、`ask-matt` routing 和 changeset。没有维护者确认前直接实现，容易在 PR #650 的 `writing-for-agents` 重构完成后发生职责重叠。

## 5. 机会四：用领域边界而不是文件长度决定 context 拆分

### 当前缺口

上游已经支持：

- 单 context：根 `CONTEXT.md`；
- 多 context：根 `CONTEXT-MAP.md` 指向各自 `CONTEXT.md`。

证据：[`domain-modeling/SKILL.md`](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/domain-modeling/SKILL.md) 与 [`CONTEXT-FORMAT.md`](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/domain-modeling/CONTEXT-FORMAT.md)。

缺口不是文件格式，而是何时从一个不断增长的 `CONTEXT.md` 迁移到多个 contexts。与此同时，`setup-matt-pocock-skills` 当前只把 monorepo 信号当作提供 multi-context 选项的前提；仓库拓扑并不等于领域边界。

证据：[`setup-matt-pocock-skills/SKILL.md`](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/setup-matt-pocock-skills/SKILL.md)。

### 最小解决办法

先 prune，再决定 split：

- 删除一般编程词汇；
- 合并重复概念；
- 收紧定义；
- 对自然聚类先使用小标题。

只有当词汇群：

- 有独立 ubiquitous language 或 invariants；
- 可以局部独立理解；
- 与其他群的关系值得在 `CONTEXT-MAP.md` 命名；

才拆成独立 context。不能设置固定行数阈值，也不能仅因 monorepo 就拆。

### 重复核对与当前状态

准确 Issue 已存在：[#321](https://github.com/mattpocock/skills/issues/321)。其现有 acceptance criteria 已要求说明何时保持单文件、何时拆分、如何保留唯一入口与 ownership。

阿磊已在 [#321 留下 domain-boundary test 提议](https://github.com/mattpocock/skills/issues/321#issuecomment-5053627161)。上游尚未确认该产品判断，也没有关联 PR。

### 判断

**应先 Issue，等待维护者确认。**

如果认可，才修改 `CONTEXT-FORMAT.md`、必要时修改 setup skill 的探测规则，并同步 human docs + changeset。不要把 `CLAUDE_MAP.md` 改名后塞进 `CONTEXT-MAP.md`：两者职责不同，混合会制造第二个真相源。

## 6. 暂缓方向：Wayfinder map / ADR / durable context lifecycle

### 为什么问题真实

Wayfinder 的 map 是 canonical index，decision 的完整答案只存在对应 ticket；ticket resolution 后，map 只保存摘要和链接。这一设计已经解决“决策历史是否存在”，但并未完全解决 ticket resolver 在独立 branch/worktree 中产生的 `CONTEXT.md`、ADR 等 durable repository changes 如何进入后续 session 可见的 canonical base。

证据：

- [`wayfinder/SKILL.md`](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/wayfinder/SKILL.md)；
- [#556：经常没有真正启动 domain-modeling](https://github.com/mattpocock/skills/issues/556)；
- [#579：durable context stranded/divergent across worktrees](https://github.com/mattpocock/skills/issues/579)。

Matt 已在 [#556 评论](https://github.com/mattpocock/skills/issues/556#issuecomment-4961644804) 中指出，改动应比“显式调用 skill”更大，甚至可能需要 domain-modeling 成为新的 blocking ticket type。

### 为什么现在不能 PR

- 把 ADR 三项门槛复制进 Wayfinder 会破坏 `domain-modeling` 的单一真相源；
- map archive 或 map summary 会把 index 变成第二个 decision store；
- 直接强制更多 ADR 可能把“规划中的决定”误装成“已实施架构”；
- durable context 的跨 worktree 合并机制尚未由维护者决定。

### 判断

**暂不建议提交新的 Issue 或 PR。**
继续关注 #556/#579；等维护者确定 ticket type 与 canonical durable-context 机制后，才可能有一个最小的 completion criterion 补丁。

## 7. 阿磊其他 skills：哪些不适合往上游搬

### `dbs-agent-migration` / `dbs-bridge`

它们解决 Claude Code、Codex、Grok 与通用 Agents 的本地多端真源、symlink 和 bridge 管理，产品边界远大于上游的 `setup-matt-pocock-skills`。把整套迁移/桥接加入上游会：

- 引入宿主特定目录与脚本；
- 扩大维护矩阵；
- 偏离 “small, adaptable, composable”。

与其最接近的 [#558](https://github.com/mattpocock/skills/issues/558) 已由 Issue 作者完成 [harness-aware setup 分支](https://github.com/mattpocock/skills/compare/main...wushijie-ai:codex/issue-558-harness-aware-setup)。**不要重复实现。**

### `dbs-skill-cleaner`

上游 [#639](https://github.com/mattpocock/skills/issues/639) 已出现第三方扫描器把部分 skills 标为 “DO NOT USE” 的问题；但这只有一份外部工具报告，尚未形成维护者定义的 threat model、误报标准或修复目标。

阿磊的 scanner 包含联网/敏感读取/暗中推广/任务劫持、误报判定、隔离与恢复，是一个独立安全产品，而不是给 `mattpocock/skills` 增加几行即可完成的补丁。与此同时 PR #650 正在重构通用 agent-writing guidance。

**暂不建议以此创建新 skill 或 PR。** 若维护者先在 #639 确认需要一份轻量 author-side security checklist，再考虑只提炼“披露外部调用、最小授权、不得暗中改变任务”三条，不移植扫描器或隔离系统。

### 完整四文件 docs governance

`CLAUDE.md + CLAUDE_MAP.md + PROJECT_STATUS.md + PROJECT_LOG.md` 对长期项目有效，但上游已经允许用户选择自己的 domain doc layout，并强调 skills 不拥有整个项目流程。完整移植会强制文件名、增加长期维护 ceremony，并与 #307 的 repository-agnostic 边界冲突。

**不建议贡献整套框架。** 上游应只吸收已经列出的四个 portable rules。

## 8. 推荐执行顺序

1. **保持 #130 分支不动**：等权限或维护者邀请；这是唯一 PR-ready 资产。
2. **等待 #560 回复**：不要和 `f508bc1` 做第二份实现；得到认可后补齐 repo-agnostic wording、docs 与 changeset。
3. **等待 #307 回复**：如果认可，先实现 agent-context review，不从全仓库 docs rewrite 起步。
4. **等待 #321 回复**：维护者接受 domain-boundary test 后，再写拆分/迁移指导。
5. **不再新建 Wayfinder/ADR Issue**：把后续研究留在 #556/#579。
6. **不提交完整 docs-governance、bridge 或 skill-cleaner**：它们留在阿磊自己的项目中作为完整产品。

## 最终判断

阿磊的 skills 里确实还有能贡献给 `mattpocock/skills` 的内容，但应贡献的是**小规则和 completion criteria**，不是整套治理框架。

最值得提交的是：

1. `curate, don't append`；
2. documentation impact gate；
3. review-only agent-context audit；
4. domain-boundary split guidance。

当前只有第 1 项已经达到 PR-ready；第 2–4 项都应继续沿现有 Issue 获得维护者方向，不能再重复开题或提前制造分支。

## 2026-07-24 补充核对：两个尚未覆盖的方向

### A. `loop-me` 的单次运行终点与失败边界

当前 [`loop-me/SKILL.md`](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/in-progress/loop-me/SKILL.md) 已定义：

- `Trigger`；
- `Checkpoint`；
- `Push right`；
- `Brief`；
- workflow spec 自身的 definition of done。

但它没有明确要求一个 recurring workflow 说明：

- 一次运行以什么可观察信号结束；
- 失败后是重试、跳过、暂停还是升级人工；
- 如何避免同一输入被重复处理。

这和 [#498](https://github.com/mattpocock/skills/issues/498) 不同：#498 处理的是 `/implement` 内部反复 code-review 的停止条件；这里处理的是 `loop-me` 产出的工作流本身是否具有可执行的 run boundary。

最小提案不应移植完整 `loop-design-check`，也不应强制 plan/build/judge。只建议在现有 vocabulary 中增加两个按需概念：

- **Success signal**：什么证据表示本次运行已经完成；
- **Failure policy**：不能达到 success signal 时，重试上限、暂停或人工升级如何选择。

同时把 definition of done 收紧为：实现者不仅无需追问步骤，也能判断一次运行何时结束、何时不得继续。

**判断：值得起草一个新 Issue；当前尚未发现同义开放 Issue。**
先提交 Issue，不直接做 PR，因为 `loop-me` 仍在 `in-progress/`，维护者可能希望保持 vocabulary 极小。

### B. 多端并行工作的机器可验证接口契约

本地 [`contract-first/SKILL.md`](../skills/engineering/contract-first/SKILL.md) 的可移植核心是：

- 一个跨端接口只有一个机器可读的契约来源；
- 消费方可以从契约生成类型或 mock；
- 提供方用真实序列化响应做契约验证；
- 接口变更先改契约，再同步各端。

上游 [`to-spec`](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/to-spec/SKILL.md) 已允许在 Implementation Decisions 中记录 API contracts，但没有要求该契约可执行，也没有要求 consumer/provider 两侧共享同一个验证来源。

它与现有 Issue 的边界是：

- [#451](https://github.com/mattpocock/skills/issues/451) 把 ADR、accepted decisions 和 rejected alternatives 编译成一次性实现约束；
- [#265](https://github.com/mattpocock/skills/issues/265) 识别并行 slices 之间的 interface blocker；
- 本方向关注跨端接口本身如何成为可机器校验的共同边界。

不过，这个方向很容易滑向强制 `CONTRACT.md`、OpenAPI 或特定工具链，也可能与上游优先 vertical slice 的设计取向冲突。

**判断：方向真实，但现在不建议开 Issue。**
先准备一个实际前后端字段漂移案例，证明“双方局部测试都绿、集成仍失败”，再提出一个 repository-agnostic 的小规则；没有真实复现前不要用方法论推演代替证据。
