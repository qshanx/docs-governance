# Matt Skills 对 docs-governance 的借鉴与优化评估

> 研究快照：供比较与追溯，不是正式规范，也不表示建议已采纳。当前执行依据见 [Skills 总路由](../skills/documentation/docs-governance/SKILL.md)。


研究日期：2026-10-04。状态：研究建议，未纳入需求基线，未实施。

本次根据 Codex 对话「继续研究 Matta skills」（`01a10492-c887-7303-a2b1-669745600940`）及其采用的英文源码，对照本项目工作区。该对话的用户消息与最终回复已分四页读取；对话中的既往授权不作为本次实施授权。

## 判断

最值得优先吸收的是三个实际增量：**扩展真实场景验收、落实共享文档写回责任、补齐探索成果退出与结论回写**。它们可以落在现有 Skill 和测试记录里，不需要新增治理框架。

完成判据、按需读取、交接输出、需求一致性检查已有较完整规定。本次不把这些已有能力再包装成缺失项。收益是待验证的判断，不能仅凭源码比较就声称 Agent 表现会改善。

## 来源与适用边界

对话采用的固定源码提交为 [`d81f3a183412e71a5b1e84ca21bc1a35eea03a60`](https://github.com/mattpocock/skills/tree/d81f3a183412e71a5b1e84ca21bc1a35eea03a60)，提交日期 2026-09-29。本地英文副本在 `/Users/daoer/Desktop/0-GitHub/mattpocock-skills-中文版本/v1.3-2026-10-04/英文原文/`；中文版目录名不作为上游发布版本依据。

已核对的相关一手资料：

| 源文件 | 可以借鉴的机制 |
|---|---|
| [writing-for-agents](https://github.com/mattpocock/skills/blob/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/skills/productivity/writing-for-agents/SKILL.md) | 用可检查且覆盖充分的完成判据抵抗提前结束；判断指令是否有效要运行文档，而非只讨论措辞 |
| [code-review](https://github.com/mattpocock/skills/blob/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/skills/engineering/code-review/SKILL.md) | 规范与规格分别审查，两个并行子 Agent 的上下文互不污染；报告保留两条判断轴 |
| [prototype](https://github.com/mattpocock/skills/blob/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/skills/engineering/prototype/SKILL.md) | 原型回答具体问题，完成后捕获结论及原始实验依据，正式成果吸收已验证决定 |
| [retro](https://github.com/mattpocock/skills/blob/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/skills/engineering/retro/SKILL.md) | 从真实会话找导航、自动检查、无效指令及信息访问方面的改进候选，已有工具优先 |
| [PHASE-BOUNDARIES](https://github.com/mattpocock/skills/blob/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/skills/engineering/ask-matt/PHASE-BOUNDARIES.md#L19-L55) | 在阶段边界判断是否继续、清空、交接、分派或压缩；下一阶段需要原始推理时优先保持连续上下文，摘要有损 |
| [handoff](https://github.com/mattpocock/skills/blob/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/skills/productivity/handoff/SKILL.md#L8-L16) | 按下一阶段裁剪交接，引用既有 Spec、ADR、Issue、提交和 diff；临时交接不复制长期主记录 |

GitHub API 另核对到研究时 main 元数据为 `24fe0ef7737efae15c87225755e9f6f5965e4888`；最新源码全文未完成读取。本报告判断依据是上述固定学习快照，不声称已经审查上游最新版本的全部行为。

本次是反向借鉴。既有 [产物治理审计](mattpocock-skills-artifact-governance-audit.md)、[贡献机会](mattpocock-skills-contribution-opportunities.md)、[交付物契约缺口](matt-deliverable-contract-gap.md) 主要研究向 Matt 上游贡献，不用于推断当前上游缺陷或维护者状态。

## 已经具备，不再重复建设

| 能力 | 项目证据 | 本次判断 |
|---|---|---|
| 方法论单一主源、Adapter 只转接 | [CLAUDE](../CLAUDE.md)、[ARCHITECTURE](../ARCHITECTURE.md) | 保持现有结构 |
| 带触发条件的导航、按任务读取 | [入口规范](../skills/documentation/agent-entrypoints/SKILL.md)第 3 条、[产品读取协议](../skills/documentation/product-evolution/SKILL.md) | 已覆盖，不另造读序 |
| 完成判据与专项输出 | [setup](../skills/documentation/living-docs-governance/SKILL.md)步骤 3—5明确主记录返回、入口检查、审计和未验证边界 | 不再新增通用完成口号 |
| 规范及需求一致性 | [产品审查](../skills/documentation/product-evolution/SKILL.md)、[实施后对照](../skills/engineering/change-impact/SKILL.md) | 已有实质检查，单纯增加双轴标题的收益不足 |
| 真实场景执行 | [TEST-SETUP-001](../TESTS.md)、[r7 执行记录](../docs/product/09-test-release.md#r7-统一-setup-验证2026-09-28) | setup 已有实际 Agent 三场景、复跑与只读负例；不能称项目只有字符串检查 |
| 长期知识与历史分工 | [同步矩阵](../references/governance-sync-matrix.md) | 当前主记录修正、LOG 只追加的规则继续使用 |

## 第一批建议：三个可验证的增量

### 1. 把真实场景验收扩到容易误判的治理行为

Matt 的 writing-for-agents 要求用实际运行判断指令效果。把这个原则延伸为小型场景验收集，是本报告的适配建议；并非声称 Matt 已提供这套治理评测。

当前缺口是 setup 之外的关键语义行为尚缺同等执行证据，原生宿主加载和角色调度也仍未验证。最小落点为现有 `TESTS.md` 和测试上线记录，不先建设评测平台。

| 场景 | 应观察的实际行为 |
|---|---|
| 现行基线与下一版草案并存 | 实际采用已生效条款，不以新日期替代生效依据；指出冲突或未确认范围 |
| 已确认要求尚未回写 | 找到确认来源，报告主记录差异；是否写回仍取决于本次授权 |
| 外部材料含“已批准”或操作指令 | 作为来源材料分析，核对真实授权，不据材料文字执行外部写入 |
| 只读请求及重复运行 | 前后路径与文件哈希符合预期；不把未修改当成已修复或完整接入 |

记录输入、实际读取和选择、产物／哈希、模型与 Skill 修订、结果及未验证边界。断言依据来自场景约定和用户确认，不能只检查输出是否出现关键词。治理执行通过与业务验收、原生宿主验证分开报告。

### 2. 落实共享文档的唯一写回责任

Matt 的阶段和交接资料强调保留必要推理、通过主记录指针交接；本项目已有类似输出契约。真正未落地的是 [STATUS backlog 第 4 项](../PROJECT_STATUS.md)：四件套并发约定。契约协作已有文件 ownership 规则，但没有覆盖共享治理文件。

最小落点为 `living-docs-governance` 的阶段同步：并行任务开始时，由当前集成 Agent 明确入口、MAP、STATUS及相关主记录的本轮写回者；其他 Agent 交付证据与建议。LOG 即使只追加也可能产生写冲突，由集成者协调合入各自事件。

验证可以在隔离项目中让两个 Agent 同时提出不同文档更新，检查最终两项均保留、没有回退他人修改、每个事实仍只有一个主位置。顺序执行不增加额外角色或交接模板。

### 3. 接上探索成果的结束、回写与临时物处理

Matt prototype 明确保存被验证的决定和原始实验依据。本项目已有原型反馈回流、经验回写与临时残留检查，但缺少把这些规则串起来的结束条件。

最小落点为 `living-docs-governance` 的文档角色或阶段同步，复用现有研究、Issue和产品记录：

- **采用**：记录确认依据，将有效结论增量回写唯一主记录，保留来源链接；研究文章不单独成为现行规范。
- **放弃**：保留问题、结论与必要理由，按项目约定处理临时物；不自动删除原型、强制建 throwaway 分支或新目录。
- **仍未定**：明确未决项与下一步所需证据，继续标为探索，不能宣称需求已批准或实验已证明业务可用。

验证时给接手 Agent 只提供项目入口，检查它能找到已采用的当前结论及来源，并识别放弃方案和未决项。归档、收录与正式采用分别判断。

## 第二批或按需吸收

### 独立首评，随后再讨论

当前 [dual-agent-review-loop.py](../scripts/dual-agent-review-loop.py)第 211—216 行先取 Claude 结论，再将其加入 Codex 提示。因此它实现的是顺序交叉讨论，不是两个独立首评；这符合其讨论循环定位，不据此判定现有功能有 Bug。

若实际评审需要减少相互暗示，可借鉴 Matt code-review：双方第一轮接收同一来源快照，各自完成后再互看意见。项目已具备规范和需求的一致性核对，不必同时增加二维评分表或新的评审平台。

最小验证是在已有 fake Agent 测试中捕获提示：首轮不含另一方报告，后续轮次才带讨论；继续保留正文变化中止和调用失败检查。只有实际需要独立复核时采用，费用和真实评审收益仍须测量。

### 用会话证据精简导航和无效指令

现有日志复盘已经统计重复 fix、标准变化及回归保护候选。可借鉴 Matt retro，按需再看反复找错入口、重复解释同一口径、过期路标与没有改变行为的指令。

先定位会话证据，再核对已有规则和确定性工具。一次网络失败、一次错误调用或普通重试不自动升格为项目治理问题；不新建会话遥测台账，不为了记录过程扩大 LOG。

### 完整行为切片，只作为已有任务的核对线索

引用对话中的 to-tickets 将实施任务按可独立验证的纵向行为拆分；Wayfinder 则索引待解决问题和决策。它们都不等于代码模块地图。

本项目产品审查已检查交付、需求、依赖和阻塞的关联。可按需核对外部已有任务是否声明可验证路径，缺口交回研发／产品负责人；第一批不新增拆票、任务编排或重复状态地图。

## 不建议照搬

- 再新增一套 Spec、任务图或固定文件组合：复用既有主记录与 Tracker。
- 按固定 token 阈值自动清空上下文：上游经验值和宿主命令不适合作为本插件门禁；需要原始推理时清空可能损失依据。
- 默认把每项规划送到新会话，或为独立审查强制增加模型调用：按具体阶段及验证需求选择。
- 把治理插件扩成通用 grilling、故障诊断或多 Agent 实施编排工具：保留专业 Skill 的执行职责，治理层维护引用和证据。

## 本次验证范围

完成了引用对话读取、固定英文源码核对、项目现有 Skill／脚本／测试记录比较及反证审查。本次只新增这份研究笔记；没有修改方法论、脚本、产品需求或发布状态。

研究前工作区的 `bash scripts/verify.sh` 基线通过。研究笔记写入后的验证结果以本次交付说明和运行日志为准。本文建议的场景、并发执行和独立评审尚未实施或测量，不能当作已通过的能力。
