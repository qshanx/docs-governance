# module-governance 真实模块试跑

2026-10-11，阿磊要求实际建档并审计，随后确认触发应支持自然语言意图、不必点名 Skill。由当前 Agent 执行，不是独立盲测或原生宿主自动选取验证。

## 输入与隔离

来源为本地 jushuitan-inventory-costing 的按日加权计算模块。读取项目 AGENTS、CLAUDE、MAP、STATUS，及真实 weighted_average.py、原有测试和业务口径第 06 号文档。隔离目录：`/private/tmp/module-governance-real-e3CIFI`。只复制上述文件，未复制业务数据、凭据或所有项目文档；因此不宣称完成来源项目的全量文档审计。未调用客服、ERP、网络或生产写入，历史入口中的外部操作指令不是本任务范围。

模块识别依据：源码承担独立的成本计算职责，有公开函数及真实测试消费者。它是本项目计算核心，但不据此宣称它是大型系统的完整限界上下文。选择原 src 位置，不搬代码、不虚构目录架构。

原始源码 SHA-256：b8d9b9d104ae878495b12d77209f5338b55b955592ca16670759acdc00d07c04。
原始测试 SHA-256：2587c3f304ca87a1e5c2c66b3a3e232b9e76d1f4ffce8e4215d152756aa59a49。
结束时 cmp 对照来源文件均相同；修改仅为隔离副本新增 src/AGENTS.md、src/CONTEXT.md，及 MAP 增加导航。

## 实际执行与结果

在隔离根执行 `python3 src/weighted_average.py`：退出 0，最终成本 9.0，与原基准 9.0 一致。
执行 `python3 -m unittest discover -s tests -v`：建档前后均 7 项通过；覆盖出入库参与性、成本补录、分仓、负库存／负成本停算。没有更改测试或业务实现。

生成模块入口 30 行；项目入口 43 行、章程 78 行，使用 check-entrypoint-length.py 实测均通过。对隔离目录执行 audit-docs.py 的 artifacts 范围：退出 0，无 Markdown 断链。该脚本不验证术语语义，也不验证未复制的项目资料；没有伪称 full 通过。

## 按 docs-audit 的内容核对

| 检查 | 实际依据与结果 |
|---|---|
| 核心模块覆盖 | 原来 src 无局部入口／词汇表；现在 MAP → src/AGENTS → CONTEXT 路径可达，且双向引用有效 |
| 项目与模块规则 | 项目保留生产操作及推送红线，模块只补计算职责与验证；未复制项目全部规则，未扩大权限 |
| 接口唯一源 | AGENTS 指向函数及原测试，不另抄输入字段表；无持久状态及外部写入的描述与完整源码相符 |
| 实现范围 | 源码只按 warehouse 分组，不按商品分组；入口明确不能宣称自动处理混合商品，未虚构商品隔离能力 |
| 领域含义 | 五个词义对照已有业务资料与实现；舍入、线上实际分仓保持未确认，没有把 Python round 当成 ERP 已验收口径 |
| 实际发现并修复 | 初稿将“移动加权”等不同概念列进 Avoid。格式审计通过也无法发现此错；语义核对发现它们不是弃用同义词，改为“无已确认同义别名”，区别写在定义旁，同时补强 Skill 规则 |
| 文档结构 | 规则在 AGENTS，领域语言在 CONTEXT，详细业务资料原位保留；无新增空 ADR 或重复合同 |
| 入口八项 | 长度通过；禁止事项及替代方式沿用父级；验证命令实跑；渐进导航可达；局部作用域明确；不新增 hook；词义与状态分离；协作约定沿用父级。宿主加载效果未验证 |

最终 AGENTS SHA-256：0dd5798250f94424c49af32b95b6933879382e8ca8a71eed58b0f55be2fd6c5c。
最终 CONTEXT SHA-256：2afb933bc157a1f15c517826bbd8c1aad2b363e5ebcc712bb0b928cc1eff76a4。

## 意图场景复核

按新触发表逐项人工复核：新增核心模块及补齐模块文档进入流程；“考虑拆模块”仅分析；普通颜色修改不建档；纯审计发现缺失只报告；审计且明确要求补齐可进入维护。Codex policy 已设 allow_implicit_invocation 为 true。以上是规则与配置复核，不是新会话中的自动选取命中率实验。

结论：当前 Agent 在一个真实模块的隔离副本中完成了建档、执行原业务测试、内容审计和修正；不能外推到大型前后端项目、原生宿主加载或 ERP 线上行为。临时目录用于查看产物，可能被系统清理；源项目未改，本报告保存范围和证据摘要。

## 后续独立会话触发与链接复测

用户要求不点名 Skill 实测，并补强生成链接检查。首次测试目录为 `/private/tmp/module-trigger-test-88yZYj`：新建库存模块会话实际读取 module-governance 并生成模块 AGENTS／CONTEXT，10 项业务测试通过；价格显示 Bug 会话未读取该 Skill、未新增模块文档，3 项测试通过。

纠正此前回复：首次生成文件位于 `modules/inventory/`，指向根目录的 `../../AGENTS.md` 和 `../../tests/test_inventory.py` 均正确，并非少一层。原会话链接检查退出 0，本轮复用 audit-docs.py 的 artifacts 检查亦退出 0。保留正确文件，不为迎合误报改坏链接。

module-governance 补充按引用文档所在目录解析、实际调用已有 artifacts 审计、失败修复后复跑及目标语义核对。新增审计回归用例：嵌套模块的 `../AGENTS.md` 断链被定位并退出 1，改为 `../../AGENTS.md` 后退出 0；未另造检查器。

复测采用 Codex CLI 0.162.0-alpha.17.2 的独立 ephemeral 会话；隔离项目 `/private/tmp/module-link-retest-8RH3CY/new`，Skill 快照在同级 bundle，经项目 `.agents/skills` 提供。原始提示只要求新建库存模块、实现内存 reserve／release 与输入校验、补测试，未提 Skill 或链接检查，也未提供上轮错误结论。

实际执行轨迹 `events.jsonl` 显示读取 module-governance、定位快照中的 audit-docs.py，并在生成后运行 `--root . --scope artifacts`，退出 0、Markdown 无断链。根导航到模块、模块到根规则／同级 CONTEXT／源码及根测试的目标均复核正确。独立重跑 10 项库存测试全部通过，模块入口 8 行。会话另跑 full 时有缺失可选载体及无 Git 基准的未验证项，不将退出 0 解释为全量语义通过。

本插件专项审计测试 33 项、完整 verify 的 109 项测试通过，Skill 格式检查通过。仅验证这些样本，不保证所有宿主或任意生成均命中；未修改真实业务项目、未提交推送。该实测补充前文的文本场景复核，不替代大型项目试点。
