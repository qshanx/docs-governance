# awesome-design-md 对 docs-governance 的适配评估

> 研究快照：供比较与追溯，不是正式规范，也不表示建议已采纳。当前执行依据见 [Skills 总路由](../skills/documentation/docs-governance/SKILL.md)。


日期：2026-09-24。调研对象：[VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)，证据固定在调研时的提交 [`f696123`](https://github.com/VoltAgent/awesome-design-md/tree/f6961238d5cddcf8042a74a70fc400ec67181abb)。本次为一手材料的只读比较；没有安装其工具、复制其设计文件，或修改任何现有方法论。

## 结论

**可借鉴的是“为单一、可验证的消费场景准备一份小而结构化的 Markdown 约束”的表达方式；不应把其 `DESIGN.md` 集合接入为 docs-governance 的通用治理层。**

它解决的是“让 AI 生成的 UI 保持同一视觉语言”，而本插件解决的是长期项目的知识、决策与验证证据不漂移。两者处在不同职责层：上游 README 自己把 `AGENTS.md` 定义为“如何构建”，把 `DESIGN.md` 定义为“外观与感受”；这恰好支持本插件继续将方法论留在 `skills/<分类>/<名称>/SKILL.md`、入口桥接保持薄的边界，而不是把视觉范例混入治理章程。[上游 README：两种文件的职责划分](https://github.com/VoltAgent/awesome-design-md/blob/f6961238d5cddcf8042a74a70fc400ec67181abb/README.md#L23-L38)

## 一手材料观察

| 上游事实 | 对本插件的含义 |
|---|---|
| 仓库是按品牌分目录的 `DESIGN.md` 集合；README 要求把某一份文件放入项目根供 AI 使用，而不是提供项目状态、决策或变更审计机制。[README：定位与使用](https://github.com/VoltAgent/awesome-design-md/blob/f6961238d5cddcf8042a74a70fc400ec67181abb/README.md#L23-L38)；[目录](https://github.com/VoltAgent/awesome-design-md/tree/f6961238d5cddcf8042a74a70fc400ec67181abb/design-md) | `DESIGN.md` 是面向一次具体 UI 语言的输入，不是项目治理脊柱的替代品。 |
| README 归纳每份文件的九类信息：视觉氛围、颜色角色、字体、组件、布局、层级、Do/Don't、响应式和 agent 提示。[README：内容结构](https://github.com/VoltAgent/awesome-design-md/blob/f6961238d5cddcf8042a74a70fc400ec67181abb/README.md#L170-L190) | 这是一种可读且可执行的“受限领域说明书”结构；尤其适合未来真正需要 UI 方向时，减少 agent 把视觉偏好留在口头提示中的漂移。 |
| 实际样例在 Markdown 前置元数据中声明 token、排版、圆角、间距与组件；组件状态独立命名，并通过 token 引用避免在每处写死颜色。[Claude 样例：tokens 与 components](https://github.com/VoltAgent/awesome-design-md/blob/f6961238d5cddcf8042a74a70fc400ec67181abb/design-md/claude/DESIGN.md#L1-L295)；[迭代规则](https://github.com/VoltAgent/awesome-design-md/blob/f6961238d5cddcf8042a74a70fc400ec67181abb/design-md/claude/DESIGN.md#L510-L517) | 可借鉴“名称可复用、状态显式、禁止项明确”的写法；它比“做得高级一点”更可复核。 |
| 样例把响应式断点、折叠策略、触控目标写成明确规则，并单列 `Known Gaps`，不把未提取的动效、表单状态或产品面假装成已定义。[Claude 样例：响应式与缺口](https://github.com/VoltAgent/awesome-design-md/blob/f6961238d5cddcf8042a74a70fc400ec67181abb/design-md/claude/DESIGN.md#L487-L524) | 可借鉴“已知缺口必须可见”的诚实边界；与本插件 `PROJECT_STATUS.md` 对未验证项的处理一致。 |
| 上游维护者要求贡献者对照真实站点，修正 token 时同步 preview，并给出变更前后理由；同时声明不会接收新的 `DESIGN.md` 文件，以维持精选质量。[CONTRIBUTING.md](https://github.com/VoltAgent/awesome-design-md/blob/f6961238d5cddcf8042a74a70fc400ec67181abb/CONTRIBUTING.md#L7-L18) | 可借鉴“来源—变更理由—可视化核验”的证据链；但不能据此把静态设计审美当作自动验收结论。 |

## 值得借鉴的最小原则

1. **分离构建规则与视觉规则。** 上游把 agent 工作约束和 UI 语言拆为 `AGENTS.md`／`DESIGN.md`；本插件已经以 `AGENTS.md` 薄桥接、`CLAUDE.md` 路标、`skills/<分类>/<名称>/SKILL.md` 方法论唯一源实现了同一类职责分离。若将来出现真实 UI 设计任务，视觉约束应是一个按需载体，而不是扩写根章程或复制进总路由。
2. **以 token、组件、状态和反例取代形容词。** 上游把默认／active／disabled 等变体分开，并写明 Do/Don't；这可成为任何项目级视觉 brief 的最低信息密度，而非引入完整品牌模板。
3. **让范围与未知项可审计。** 可声明适用页面、已核对的视口、来源和未覆盖交互；这与本插件“未测量不背书”的原则一致，也避免设计文件被误读为全产品设计系统。

## 不能直接采纳的部分

| 不能直接采纳 | 原因与本插件边界 |
|---|---|
| 把上游任一品牌 `DESIGN.md` 复制为默认模板或项目根必备文件 | 这些是对公开网站的品牌分析；上游明确说明不拥有各站视觉身份，文件按“as is”提供。[README：权利与免责声明](https://github.com/VoltAgent/awesome-design-md/blob/f6961238d5cddcf8042a74a70fc400ec67181abb/README.md#L206-L210) 即使仓库采用 MIT 许可，也不等于适合把第三方品牌语言作为客户项目默认视觉。更重要的是，本插件面对的项目未必有 UI。 |
| 将 `DESIGN.md` 升格为第五份固定治理脊柱，或在 `CLAUDE.md`／command／agent 中复制其细节 | 这与当前“轻量治理、按需创建”和“方法论只在 skill”的硬边界冲突；会让本插件从治理能力路由变成强制设计系统，并制造第二真相源。 |
| 将上游的 YAML/Markdown 内容当成机器可判定的设计验收或直接接入提交护栏 | 上游样例确有结构化 token，但没有本插件所要求的来源授权、需求成功标准、运行测试、回归证据或审计退出码。其自身的迭代建议提到设计 lint，不能证明所有上游文件已经过该检查。[Mintlify 样例：迭代建议与已知缺口](https://github.com/VoltAgent/awesome-design-md/blob/f6961238d5cddcf8042a74a70fc400ec67181abb/design-md/mintlify/DESIGN.md#L836-L852) |
| 以公开 CSS／截图推断产品的完整可访问性、交互行为或资产许可 | 上游样例自己明确排除或标注动效、特定状态和部分产品界面；因此只能作为灵感或临时视觉参考，不能代替真实设计来源、品牌授权和移动端验收。[Claude 样例：Known Gaps](https://github.com/VoltAgent/awesome-design-md/blob/f6961238d5cddcf8042a74a70fc400ec67181abb/design-md/claude/DESIGN.md#L518-L524) |

## 最小试点建议（不在本次实施）

仅在**已有明确 UI 交付、且项目所有者确认可用视觉来源**的业务项目做一次非生产页面试点；不要在 docs-governance 插件本体或无 UI 的仓库预建文件。

1. 选一个单页或单组件改动，先在现有 Spec/Issue 中写清用户路径和成功标准；不从上游品牌文件直接复制视觉身份。
2. 由该业务项目维护一份按需 `DESIGN.md`（或等价的设计 brief），只记录：适用范围、来源/授权、少量 token、目标组件及状态、响应式要求、明确 Do/Don't、已验证页面和 Known Gaps。它从项目现有入口链接，不能替代 `skills/<分类>/<名称>/SKILL.md`、`PROJECT_STATUS.md` 或验收记录。
3. 实现后以真实页面在约定桌面与移动视口的截图/人工走查作为证据；把“通过了哪些页面、哪些状态未测”记录在原有验收或审计产物中。不要为试点新增全仓 hook、每日任务、独立指标台账或强制 lint。
4. 复盘维护成本、agent 是否更少追问视觉决策、以及是否出现复制漂移；只有有正反证据后，再决定是否在 `product-evolution` 或 UI 专项 skill 中补充最小方法，而不是先改总路由。

## 判断

上游最有价值的启发是：**约束要贴近消费者、足够具体，并把“不该做什么”和“尚不知道什么”写出来。** 对 docs-governance 而言，正确落点是未来按需的 UI 视觉 brief，而不是把设计收藏库、第三方品牌 token 或又一份固定根文档纳入治理体系。当前轻量治理、方法论唯一源和 STATUS 的未验证边界均应保持不变。
