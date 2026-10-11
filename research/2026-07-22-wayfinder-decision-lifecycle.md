# Wayfinder 决策生命周期贡献研究

研究日期：2026-07-22
上游仓库：[`mattpocock/skills`](https://github.com/mattpocock/skills)
源码快照：[`ed37663`](https://github.com/mattpocock/skills/commit/ed37663cc5fbef691ddfecd080dff42f7e7e350d)

## 结论

**存在真实的执行缺口，但不建议新建 “Preserve important Wayfinder decisions as ADRs” Issue，也不应直接提交 PR。**

原因不是这个问题没有价值，而是：

1. Wayfinder 已经把 decision ticket 及其 resolution 定义为长期保存的唯一事实位置；
2. Decision → ADR 的判断已经由 `domain-modeling` 单一负责；
3. 当前真实问题是 Wayfinder 运行时可能没有可靠调用 `domain-modeling`，或者 ADR/CONTEXT 变更滞留在并行分支；
4. 这些问题已经由上游 #500、#556、#579 直接覆盖，另开 Issue 会分散维护者正在进行的设计讨论；
5. Matt 已表示 #556 需要比“补一句激活指令”更完整的设计，甚至可能把 domain modeling 设计成新的阻塞 ticket type。现在提交一个预设答案的 PR 会越过维护者尚未确定的边界。

因此，本轮高质量贡献的正确动作是：**不制造重复 Issue；等待并参与 #556 的方向收敛，得到维护者认可后再做最小 PR。**

## 1. 当前架构理解

### 1.1 Wayfinder 保存的是什么

Wayfinder 的核心不是代码，而是消除未知后形成的 decision：

```text
Destination
  → Fog
  → Decision tickets
  → Frontier
  → Resolution
```

当前源码明确规定：

- Map 是 canonical artifact，但只是 **index，不是 store**；
- 每项 decision 只存在于对应 ticket；
- `Decisions so far` 只保存一行摘要和指针，不复制完整答案；
- ticket 完成时，把答案写成 resolution comment、关闭 ticket，再把指针追加到 map。

证据：

- [`wayfinder/SKILL.md`：map 是 canonical index，decision 只存一处](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/wayfinder/SKILL.md#L19-L25)
- [`wayfinder/SKILL.md`：resolution comment、close、context pointer](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/wayfinder/SKILL.md#L118-L128)
- [PR #419：刻意把 map 定义成 index，而不是第二个 decision store](https://github.com/mattpocock/skills/pull/419)

所以，“Wayfinder 完全没有长期保存 decision”这个假设不成立。它已经把 issue tracker 里的 ticket 作为历史决策记录。

### 1.2 ADR 由谁负责

ADR 不是 Wayfinder 自己的第二套能力。Wayfinder 在以下位置依赖 `domain-modeling`：

- Chart map 时用 `grilling + domain-modeling` 命名 destination；
- Grilling ticket 本身被定义为 `grilling + domain-modeling`；
- Work through map 时，默认建议调用 `grilling + domain-modeling`。

证据：

- [`wayfinder/SKILL.md`：ticket type 与 domain-modeling](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/wayfinder/SKILL.md#L73-L80)
- [`wayfinder/SKILL.md`：chart 与 resolve 阶段调用 domain-modeling](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/wayfinder/SKILL.md#L107-L126)

`domain-modeling` 已经定义了严格的 ADR 门槛：

1. hard to reverse；
2. surprising without context；
3. result of a real trade-off。

缺一项就不写 ADR。这个判断标准应继续只存在于 `domain-modeling`，不应复制到 Wayfinder 形成第二份规则。

证据：

- [`domain-modeling/SKILL.md`：ADR 三项门槛](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/domain-modeling/SKILL.md#L66-L74)
- [`ADR-FORMAT.md`：ADR 可以只有一段，价值在记录决定及原因](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/domain-modeling/ADR-FORMAT.md#L7-L15)

### 1.3 Wayfinder 如何进入实现流程

Wayfinder 是大型、模糊项目的 on-ramp，不是默认主流程。地图清晰以后，它应交给 `to-spec` 汇总，再进入 `to-tickets → implement → code-review`。

证据：

- [`ask-matt/SKILL.md`：Wayfinder 清图后交给 to-spec](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/ask-matt/SKILL.md#L42-L46)
- [`docs/engineering/wayfinder.md`：Wayfinder 是 big-idea on-ramp](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/docs/engineering/wayfinder.md#L42-L44)

## 2. 三个候选方向验证

### 方向 A：Decision → ADR handoff

判断：**概念上已存在，执行可靠性仍有缺口，但不构成新的 Issue。**

已解决的部分：

- ticket resolution 是长期历史记录；
- map 是决策索引；
- `domain-modeling` 已拥有 ADR 判断规则；
- Wayfinder 的设计意图已经包含 `domain-modeling`。

真实缺口：

- Wayfinder 的最终 resolution 步骤只明确要求 issue comment、close 和 map pointer，没有明确验证 `domain-modeling` 是否真正运行；
- 非 Grilling ticket 也可能产生 ADR-worthy decision，但不一定触发 ADR 判断；
- 即使生成 ADR，它也可能滞留在 ticket 的 worktree/branch，没有进入后续 session 读取的 canonical base。

这个缺口已被下列 Issue 覆盖：

- [#500：Wayfinder 是否替代或补充 grill-with-docs](https://github.com/mattpocock/skills/issues/500)——已经直接提出 Wayfinder 没有产出 ADR/CONTEXT，评论也建议显式保持 `domain-modeling` 并链接产物；
- [#556：Chart map 经常跳过 domain-modeling](https://github.com/mattpocock/skills/issues/556)——与本假设最接近；Matt 回复说问题不只是激活措辞，可能需要新的 domain-modeling ticket type；
- [#579：跨 ticket 分支/worktree 协调 durable context](https://github.com/mattpocock/skills/issues/579)——完整覆盖 ADR/CONTEXT 被滞留、分叉和无法进入 canonical base 的问题。

维护者此前还两次把类似提案导回现有能力，而不是增加下游 ADR sweep：

- [#407](https://github.com/mattpocock/skills/issues/407)：Matt 对 “to-prd 未把决定提升为 ADR” 的答复是使用 `/grill-with-docs`；
- [#305](https://github.com/mattpocock/skills/issues/305)：Matt 对 “Persisted Design Decisions” 的答复是 ADR 已由 `/grill-with-docs` 处理。

结论：**不新建 Issue；#556 是最合适的现有讨论入口。**

### 方向 B：Prototype decision capture

判断：**当前版本已经明确解决，不建议贡献。**

现有规则要求：

- 把 prototype 回答的问题和 verdict 持久记录在 issue 或 commit；
- runnable prototype 作为 primary source 保留在 throwaway branch；
- 从 implementation issue 留下指向该分支的 context pointer；
- 主分支只保留验证后的 decision，不合并 throwaway code。

证据：

- [`prototype/SKILL.md`：capture answer 与 primary source](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/prototype/SKILL.md#L19-L26)
- [`docs/engineering/prototype.md`：长期答案与实验原始证据的分工](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/docs/engineering/prototype.md#L34-L38)
- [已合并 PR #488](https://github.com/mattpocock/skills/pull/488)

### 方向 C：Wayfinder map lifecycle governance

判断：**不建议以 archive/summarize 为新贡献。**

Map 已经是 issue tracker 上的持久 canonical index；ticket 是 decision 的唯一存储。再生成归档摘要会形成第二个 store，直接违背 “map is an index, not a store”。

Wayfinder 过去甚至专门删除了每轮固定 Handoff ceremony，因为它增加持续 token 成本，而下一轮重新打开 map 已足以继续。PR #425 留下的开放问题只是是否需要极轻的终止信号，不支持重新引入完整治理流程。

证据：

- [PR #425：删除 Wayfinder Handoff ceremony](https://github.com/mattpocock/skills/pull/425)
- [#492：Wayfinder 与 to-spec 的交接限制已经单独讨论](https://github.com/mattpocock/skills/issues/492)

真正有价值的不是再做一个 map archive，而是确保 tracker decision 对应的 durable repository context 能被后续 session 读取；这已经由 #579 处理。

## 3. 为什么不应强行创建 Issue

仓库 README 把项目哲学定义为 small、easy to adapt、composable。对这个仓库而言，高质量贡献不仅要发现问题，还要避免：

- 重复已有 skill 的职责；
- 复制同一判断标准；
- 新增每轮都要支付 token 成本的 ceremony；
- 为同一个问题创建多个 Issue，迫使维护者重新合并上下文。

证据：

- [`README.md`：small、adaptable、composable](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/README.md#L15-L20)
- [#299：规划阶段 ADR 可能污染当前架构真相，ADR 生命周期本身仍未完全解决](https://github.com/mattpocock/skills/issues/299)

特别是 #299 说明：简单要求 Wayfinder 产生更多 ADR 可能扩大“计划中的决定被误当成已实施架构”的问题。任何补丁都必须等待维护者先确定 ADR lifecycle 与 domain-modeling ticket 的边界。

## 4. 推荐的贡献入口

### 推荐 Issue

不创建新 Issue。继续关注并优先参与：

1. [#556：wayfinder: Chart the map often skips /domain-modeling](https://github.com/mattpocock/skills/issues/556)
2. [#579：reconcile durable context documents across ticket branches and worktrees](https://github.com/mattpocock/skills/issues/579)

#556 决定“何时、以什么 ticket 形式运行 domain-modeling”；#579 决定“产生的 ADR/CONTEXT 如何进入 canonical base”。两者先于 PR。

### 可备用的补充评论草稿（未发布）

当前不建议立刻发布，因为 #556 已有足够上下文。若维护者继续追问 ADR 边界，可使用下面这段：

> The ADR part looks more like a completion criterion owned by `domain-modeling` than a second decision store in Wayfinder. Wayfinder already keeps the full resolution in the decision ticket and the map only indexes it. The runtime gap is that a ticket can still close without the resolved decision being assessed by `domain-modeling`, especially outside a grilling ticket. If domain modeling becomes its own blocking ticket, should that ticket own both terminology updates and ADR promotion, with the resolution comment linking any ADR it creates? I can prepare a minimal patch once that boundary is settled.

## 5. 如果维护者认可，最小 PR 应如何实现

在 #556 得到方向认可后，候选 PR 只应修改：

1. `skills/engineering/wayfinder/SKILL.md`
   - 在 ticket close 之前增加一个明确 completion criterion；
   - 调用而不是复制 `domain-modeling` 的 ADR 判断；
   - 如果产生 ADR，从 resolution comment 链接它；
   - 如果没有达到 ADR 门槛，ticket resolution 继续作为唯一历史记录；
   - 不自动生成 ADR，不引入新的文档层级。
2. `docs/engineering/wayfinder.md`
   - 按仓库规则同步行为变化，但不复制 SKILL 的完整步骤。
3. `.changeset/<slug>.md`
   - 记录行为变化。

只有当 Wayfinder 在整体流程中的位置发生改变时，才更新 `skills/engineering/ask-matt/SKILL.md`；仅强化 completion criterion 不需要重画路由。

### 验收标准

- Wayfinder 不复制 ADR 三项标准，`domain-modeling` 仍是唯一规则源；
- 普通 decision 只保留 issue resolution，不被强制升级为 ADR；
- ADR-worthy decision 不会在 ticket close 时静默丢失；
- 新增流程成本只发生在 ticket resolution 边界；
- 文档页与 changeset 同步；
- 维护者对 #556 的设计方向已经明确。

## 最终判断

这次研究发现了真实问题，但没有发现一个尚未被上游提出、又适合立即实现的独立贡献点。

**不建议贡献新的 Issue 或 PR。** 现在最符合维护者利益的做法，是避免重复，把研究结论对齐到 #556/#579，并等待维护者确定 domain-modeling ticket 与 ADR lifecycle 的边界后再实现。
