# 项目适配（本插件补充）

领域建模方法和格式只使用 [Matt 的 domain-modeling](SKILL.md)、[CONTEXT 格式](CONTEXT-FORMAT.md)与 [ADR 格式](ADR-FORMAT.md)。本文件仅处理它与已有项目治理的衔接。

## 现有主记录与授权

- 沿用当前上下文的词汇表、导航和 ADR 布局。已有 GLOSSARY、共享 CONTEXT、表格或 CONTEXT-MAP 时复用，不按代码目录数建档，不为换格式迁移或复制主记录；业务上下文不等于代码模块。
- 上游“确认即记录”只在当前任务已有文档写入授权时执行；纯讨论或审计返回建议。场景假设、未确认歧义与代码矛盾交负责人确认，不据此改代码或标决策已批准。`_Avoid_` 只列同一概念的已确认别名，不把不同业务概念列成禁用词。
- 模块 AGENTS 只链接术语定义；项目级和模块级规则的主源与读取方式交给 [agent-entrypoints](../agent-entrypoints/SKILL.md)。术语含义变化的下游检查交给 [change-impact](../../engineering/change-impact/SKILL.md)，接口字段继续由唯一契约／代码定义。

## 决策落点

保留既有 ADR 主记录。项目已采用模块入口内联时，短小且仅影响该模块的决策可以留在 AGENTS 决策节，带稳定标识、真实确认依据及必要链接，仍按上游判断是否值得记录；不强制填写八个章节。长决策、跨模块决策或导致入口超过 200 行时，下沉到既有 ADR 空间并留引用。保留旧历史，替代关系明确指向新／旧记录，不为“两份文档”删除历史。

ADR 的索引、状态和附加章节按实际需要使用；没有状态不代表 accepted。项目已有索引时继续登记，已有更严格的团队政策仍按该政策核对。只把负责人已确认的决定标 accepted。重要决策事件按[历史主源约定](../living-docs-governance/record-scope.md)登记；已有 LOG 继续追加，否则复用 Git／PR／Issue，不新造流水。任务状态与排期仍归已有 Tracker。

## 审计衔接

运行 `python3 <插件目录>/scripts/audit-docs.py --root <项目根> --scope adr`，链接核对使用 `--scope artifacts`。ADR 检查覆盖项目与各上下文的 `docs/adr/`：索引、状态缺省不阻断；显式非法状态、已有索引漏登／断链、ADR 本地断链及不存在的替代目标仍失败。支持 `superseded by ADR-NNNN`，编号在本 ADR 目录解析。没有状态标未验证，不推断批准；缺索引时导航覆盖仍需人工核对。

脚本不验证业务决定、理由是否充分、内联决策语义或项目自定义政策；这些由 Agent 对照来源只读检查。AGENTS、CONTEXT 和 ADR 是开发规则、业务语言与决策理由的载体，不代替领域模型实现或业务验收。
