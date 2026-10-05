# 技术文档表达规则与示例

按当前问题读取对应章节。以下规则改善表达，不裁定事实或变更项目要求。示例只演示措辞，不能作为目标项目的事实来源。

## 表达判断

- 一个句子围绕一个主要动作或判断展开。出现多个独立动作、主语切换或跨层条件时，考虑拆句；紧密相连的比较、因果或限定可以留在同一句。
- 能从依据确定主体时，直接写谁执行什么；主体未知时保留原句并标出问题。不要把“系统”“管理员”当作通用补词。
- 用同一个术语指同一对象。尊重项目词汇，尤其是有业务区别的近义词；不为了避免重复而轮换名称。
- 用具体动作替换无意义的外壳，但保留必要语气、过程和范围。例如“对配置进行读取”可写成“读取配置”；“已开始读取配置”不能简化成“已读取配置”。
- 代词只有在所指对象唯一时才保留。“客户端把令牌发给服务端，它随后……”需要定位“它”的真实所指；无法定位就提出疑点。
- 句子较长时检查读者是否能追踪主语、条件和否定范围。长度不决定正确性，短句也可能歧义，连贯的长句不必拆成片段。

## 步骤与条件

操作指南首先让读者知道何时执行、由谁执行、执行什么及怎样判断结果。仅写已有依据支持的信息，不能为了凑完整步骤发明检查命令、预期输出或回滚方法。

- 单个步骤包含一个可独立完成的主要动作；保留有依赖的先后关系。列表拆分不能让后一步看起来可任选执行。
- 条件紧邻受其限制的动作，必要时放在动作前；一项条件支配多个步骤时，用清楚的引导句或分组保留范围。
- 例外、禁止条件和失败分支紧邻对应操作，不把它们移到读者容易遗漏的通用附注。
- 操作说明采用直接动词；设计说明仍可用描述句，不把描述现状改成命令。
- 保留命令、代码块、参数、占位符、路径和链接目标。疑似错误应报告核对，不能作为文字润色顺手修正。

示例：

> 原文：若缓存为空则读取源文件并重建索引，除非源文件缺失，此时返回错误。
>
> 建议：缓存为空且源文件存在时，读取源文件并重建索引。缓存为空且源文件缺失时，返回错误。
>
> 核对：缓存条件仍支配全部分支，读取先于重建，缺失分支未被删除；没有添加“检查源文件”这一新操作。

## 中文措辞

- 优先使用自然、直接的动宾表达，删除“进行”“相关”等词前先检查它们是否承担范围或过程含义。术语中的词不得按禁词表删除。
- 中文省略主语时，依据上下文判断是否唯一；不强迫每句重复主体，也不以“本系统”掩盖主体未知。
- 连续的“并”“及”“后”可能混合并列和顺序。只有依据确定关系后才拆开；“A 完成后执行 B”不能改成互不关联的两个步骤。
- 保留作者表达的要求强度。“最好”“建议”“应”“必须”不能因文风统一而互换；项目已定义这些词的规范含义时遵循该定义。

示例：

| 原文 | 保留含义的写法 | 不可采用的写法及原因 |
|---|---|---|
| 上线前最好跑一下回归测试。 | 建议在上线前运行回归测试。 | 上线前必须运行回归测试。——推荐变强制 |
| 计划在下一版本支持导出。 | 下一版本计划支持导出。 | 下一版本支持导出。——计划变确定承诺 |
| 目前尚未验证该配置在生产环境的效果。 | 该配置在生产环境的效果目前尚未验证。 | 该配置可用于生产环境。——缺失证据变肯定结论 |
| 仅当请求超时且重试次数少于 3 次时重试。 | 保留原句即可。 | 请求超时时重试，最多 3 次。——条件和次数边界改变 |

“应”在不同项目可能代表要求或建议，不能凭习惯替作者定级；有歧义时报告该句，沿用原词。

## English wording

- Prefer a direct verb and a clear subject when the evidence identifies the actor. Keep established technical vocabulary; do not force ordinary synonyms onto domain terms.
- Clarify long noun chains and pronouns only when their meaning is known. An unknown actor or relation remains a question for the author.
- Keep tense, aspect, negation and modal force. Do not turn `should` into `must`, `may` into `will`, or a planned capability into current behavior. Follow the project's definitions of normative terms.
- Use an imperative for an existing instruction, but keep descriptions as descriptions. Splitting a sentence must preserve the scope of `if`, `unless`, `only`, `before` and `after`.
- Preserve code, commands, names, numbers and units exactly. This is not an ASD-STE100 vocabulary or syntax compliance check.

Example:

> Original: Before release, you should run the regression tests unless the change affects documentation only.
>
> Rewrite: You should run the regression tests before release, unless the change affects documentation only.
>
> Check: `should` remains a recommendation under the original usage, and the exception still applies. Do not rewrite this as “Run the regression tests before every release.” If the project defines `should` differently, preserve that definition.

## 语义比对的落点

逐句比对关键变更即可，不为未修改内容新增全仓审查。特别查看拆句、删词、补主语和改成命令式的地方：这些操作最容易丢失限定或升高要求强度。

读者无需依靠原文才能看懂改写，但改写的每项事实都应能回到原文或已确认输入。遇到“更清楚”与“保留含义”冲突时，保留原文，附具体问题及可选措辞；事实未确认前不替作者选答案。
