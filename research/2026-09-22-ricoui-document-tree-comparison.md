# ricouii 文档树与 docs-governance 对照研究

> 研究快照：供比较与追溯，不是正式规范，也不表示建议已采纳。当前执行依据见 [Skills 总路由](../skills/documentation/docs-governance/SKILL.md)。


> 日期：2026-09-22。范围：只读研究，不提出或实施仓库改动。
>
> 原始讨论：[ricouii 的 X 帖](https://x.com/ricouii/status/2102208311026418144)。已在登录态页面读取原帖：作者称这是其在正式开发前、沟通完成后的文档，并给出了文件树。该树包含根目录 `AGENTS / README / DESIGN / CHANGELOG / TODO`，以及 `docs/PROJECT-SPEC / ARCHITECTURE / COMPONENT-GUIDELINES / PAGE-STRUCTURE / DEVELOPMENT / REGISTRY / DEPLOYMENT`。以下不推断原帖未展示的具体正文规则。

## 结论

**可以借鉴其“让 Agent 在项目内有一张稳定工作地图”的方向，但不应把整棵目录照搬进 docs-governance。**

本插件已覆盖其中最关键的治理链条：规则入口、对外说明、当前状态、历史、架构、产品需求基线、研发与验收证据。它刻意把这些内容拆成职责单一、按需生成的载体，并把任务/排期留在既有 Tracker；这比为每个项目固定建立 13 份文档更符合自身的轻量治理定位。[`README.md`](../README.md)、[`skills/documentation/living-docs-governance/SKILL.md`](../skills/documentation/living-docs-governance/SKILL.md)、[`skills/documentation/product-evolution/SKILL.md`](../skills/documentation/product-evolution/SKILL.md)

真正值得补齐的不是一套新“标准目录”，而是一个**面向有 UI 和正式上线流程的项目的可选扩展**：在明确触发条件下沉淀设计原则、共享组件约束、页面/信息架构和部署运行手册；没有对应复杂度时不创建空壳。

## 原帖方法（从文件树可确认的部分）

原帖将项目知识显式分层：

1. 根目录放 Agent 工作约束、项目概览、设计方向、变更历史和待办；
2. `docs/` 放产品规格、技术架构、UI 组件/页面结构、开发方法、文档登记和部署知识；
3. 目的显然是让人和 Agent 不必从代码重新推导“做什么、怎么做、现在做到哪、在哪里找证据”。

这是一个很实用的 **document-driven project context** 结构。但从树本身无法确认每份文件的唯一事实源、更新时机、任务系统边界或防重复机制；这些恰是直接套用时最容易产生第二份真相的地方。

## 逐项映射

| 原帖载体 | 可推定职责 | 本插件对应物（证据） | 判断 |
|---|---|---|---|
| `AGENTS.md` | 给 Agent 的入口与行为说明 | [`templates/AGENTS.example.md`](../templates/AGENTS.example.md) 只桥接 `CLAUDE.md`、STATUS/MAP/ARCHITECTURE/LOG；本仓库也采用同一薄桥接 | 已覆盖，且更克制：不复制规则，避免双源漂移 |
| `README.md` | 人类与新协作者的产品/安装总览 | [`README.md`](../README.md) 的定位、三分钟试用、能力与开发入口 | 已覆盖 |
| `DESIGN.md` | 设计原则、视觉/交互方向 | 产品线的 [`docs/product/05-prototype.md`](../docs/product/05-prototype.md) 承接原型和用户路径；`loop-design-check` 是闭环设计方法，非 UI 设计规范 | 条件性缺口：目前没有通用 UI design-system / 体验准则载体，且当前插件本身没有 UI，不应为它补空文件 |
| `CHANGELOG.md` | 面向版本/用户的发布变更 | [`CHANGELOG.md`](../CHANGELOG.md) | 已覆盖；不要与内部历史混用 |
| `TODO.md` | 当前待办和优先级 | [`README.md`](../README.md) 与 [`skills/documentation/product-evolution/SKILL.md`](../skills/documentation/product-evolution/SKILL.md) 明确任务、负责人、阻塞和排期归现有 Issue Tracker；STATUS 仅为健康快照 | 有意不采用。固定 `TODO.md` 易成为第二个看板 |
| `docs/PROJECT-SPEC.md` | 项目/功能规格与验收 | [`templates/governance.example.md`](../templates/governance.example.md) 把模块需求/验收放入 `docs/{模块}-spec.md`；产品当前基线由 [`docs/product/06-prd.md`](../docs/product/06-prd.md) 和产品入口管理 | 已覆盖，采用“整体 PRD + 模块 Spec”的渐进拆分，而非强制单个项目规格 |
| `docs/ARCHITECTURE.md` | 模块权责、依赖与流转 | [`ARCHITECTURE.md`](../ARCHITECTURE.md)、[`templates/ARCHITECTURE.example.md`](../templates/ARCHITECTURE.example.md) | 已覆盖，且要求分别维护代码依赖图与运行时流转图 |
| `docs/COMPONENT-GUIDELINES.md` | 共享 UI 组件使用规则 | 无同名通用载体；可在组件真的被跨页面复用时，由特定 UI 项目的 Spec/设计系统文档承接 | 条件性缺口；不适合成为非 UI 仓库的默认文件 |
| `docs/PAGE-STRUCTURE.md` | 信息架构、页面职责和导航 | [`docs/product/05-prototype.md`](../docs/product/05-prototype.md) 要求关键用户路径/交互说明；`ARCHITECTURE.md` 只负责运行结构 | 条件性缺口：复杂多页面产品可补，不能塞进架构文档或 MAP |
| `docs/DEVELOPMENT.md` | 开发流程、约束和验证入口 | [`CLAUDE.md`](../CLAUDE.md) 的硬规则/路标、[`templates/governance.example.md`](../templates/governance.example.md) 的变更后四步流程、[`TESTS.md`](../TESTS.md) 的验证入口 | 已覆盖但分层保存：短硬规则在章程，执行流程在治理文档，测试证据在 TESTS |
| `docs/REGISTRY.md` | 文档/资产目录或登记表 | [`CLAUDE_MAP.md`](../CLAUDE_MAP.md) 是非显然知识入口；[`docs/product/README.md`](../docs/product/README.md) 是十阶段索引；[`docs/adr/README.md`](../docs/adr/README.md) 是 ADR 索引 | 已覆盖为多个领域索引。全仓库总 Registry 会重抄文件树，和 MAP“只写树看不出来的语义”的边界冲突 |
| `docs/DEPLOYMENT.md` | 上线、回退、环境与运行手册 | [`docs/product/09-test-release.md`](../docs/product/09-test-release.md) 记录测试/发布/上线的不同状态；[`skills/engineering/change-impact/SKILL.md`](../skills/engineering/change-impact/SKILL.md) 覆盖部署与回滚影响 | 条件性缺口：有多环境、值守/回滚要求时，需要一份项目级部署 runbook；普通库或未上线项目不应预建 |

### 原帖一对多映射中最重要的差异

| 原帖的单文件思路 | docs-governance 的拆分 | 保留拆分的理由 |
|---|---|---|
| `TODO.md` | Issue Tracker（实时执行） + `PROJECT_STATUS.md`（健康快照） + `PROJECT_LOG.md`（不可变历史） | 不让计划、状态、历史相互覆盖 |
| `PROJECT-SPEC.md` | `docs/product/README.md`（基线入口） + PRD（整体要求） + 模块 Spec（具体验收） + 需求评审 | 草案、部分批准和已生效需求可同时清楚存在 |
| `DEVELOPMENT.md` | `CLAUDE.md`（短约束） + `docs/governance.md`（操作流程） + `TESTS.md`（可执行证据） | 防止一份开发手册同时承担宪法、流程和测试台账 |
| `REGISTRY.md` | MAP / 产品入口 / ADR 索引 / CONTRACT、TESTS、REGRESSION 的各自入口 | 让每个领域登记表只记录自己负责的事实，不做一份容易腐烂的总目录 |

## 已覆盖、真实缺口与边界

### 已覆盖

- Agent 入口与共用规则：`AGENTS.md` 薄桥接到唯一章程，不复制方法论。[`AGENTS.md`](../AGENTS.md)、[`CLAUDE.md`](../CLAUDE.md)
- 项目导航、风险、历史和架构：四件套按职责分离，架构按多 Module 条件启用。[`skills/documentation/living-docs-governance/SKILL.md`](../skills/documentation/living-docs-governance/SKILL.md)
- 产品需求到交付证据：产品目录的十阶段导航、当前基线、评审与测试/发布状态都已经存在。[`docs/product/README.md`](../docs/product/README.md)、[`skills/documentation/product-evolution/SKILL.md`](../skills/documentation/product-evolution/SKILL.md)
- 变更、契约、测试和下游回归已有专门载体，而不是堆回开发文档。[`README.md`](../README.md)、[`TESTS.md`](../TESTS.md)

### 条件性缺口

1. **UI 设计系统层**：当至少两个页面共享组件、体验决策会被多名 Agent 反复解释，或有无障碍/响应式规范时，才需要 `DESIGN.md` 与组件指南。
2. **页面/信息架构层**：当有多页面导航、角色分流或关键漏斗时，才需要页面结构图或文档；简单单页流程留在功能 Spec/原型即可。
3. **部署运行层**：当存在多个环境、密钥/迁移/回滚步骤、值守责任或正式发布门槛时，才需要独立 runbook；当前插件只记录“未发布/未上线”，不能假装已有部署流程。[`docs/product/09-test-release.md`](../docs/product/09-test-release.md)

### 不应照搬的部分

- 不把 `TODO.md` 作为新的实时任务来源；它与现有 Issue/Linear 等 Tracker 冲突。
- 不建立涵盖所有文件的 `REGISTRY.md`，也不让 `CLAUDE_MAP.md` 退化成目录树镜像。MAP 的明确职责是非显然路径、误导区和禁区。[`templates/CLAUDE_MAP.example.md`](../templates/CLAUDE_MAP.example.md)
- 不为每个项目固定生成 `DESIGN`、组件、页面、部署文件；活文档方法明确要求渐进采用，空壳本身就是漂移源。
- 不把设计规则、产品需求、技术架构、部署步骤揉进同一 `PROJECT-SPEC.md`。一文一职是本插件已验证的治理边界。

## 推荐的最小产品路径

建议先做一次**无代码、只读的 UI 项目试点**，而不是先改插件模板：选择一个已有多页面/组件复用且有实际发布环境的业务项目，检查现有 Spec、原型、设计资产和部署流程。

若证据确认三个触发条件，采用最小四载体：

1. `DESIGN.md`：只写跨页面不变的体验原则、视觉 token 来源、无障碍/响应式底线和设计资产入口；不复制每页需求。
2. `docs/ui/component-guidelines.md`：仅登记共享组件的用途、状态边界、禁止用法和权威实现/Storybook/Figma 链接。
3. `docs/ui/page-structure.md`：仅登记信息架构、路由/页面职责、关键用户路径与空/错/权限状态；每页业务规则继续指向功能 Spec。
4. `docs/deployment.md` 或现有运行手册：记录环境、发布前检查、发布步骤、观测、回滚条件和责任边界；测试/发布证据仍留在 `09-test-release` 或项目既有记录。

把这些入口从 `CLAUDE_MAP.md` 挂出即可。随后观察一次真实变更：新 Agent 是否少问了重复问题、组件/页面规则是否没有重复真相、发布是否能按 runbook 恢复。证据成立后，再考虑将“触发条件 + 四载体职责”加入 `living-docs-governance` 或 `product-evolution`，而不是先造通用模板。

## 非目标

- 不替代 Figma、Storybook、CI/CD、部署平台、Issue Tracker 或现有运维手册。
- 不把文档目录完整度当作设计质量、需求批准、测试通过或实际上线。
- 不自动迁移已有项目的资料，不自动新增强制文件位置规则。
- 不为当前没有 UI/部署面的 docs-governance 插件补写虚构设计或部署事实。

## 研究证据与限制

- 原帖来源：[`https://x.com/ricouii/status/2102208311026418144`](https://x.com/ricouii/status/2102208311026418144)。本文使用其“开发前、沟通完成后的文档”这一定位及帖子展示的文件树；未获得各文件正文，故不推断其更新机制或具体规则。
- 仓库方法论：[`skills/documentation/living-docs-governance/SKILL.md`](../skills/documentation/living-docs-governance/SKILL.md)、[`skills/documentation/product-evolution/SKILL.md`](../skills/documentation/product-evolution/SKILL.md)。
- 当前实现与模板：[`README.md`](../README.md)、[`CLAUDE.md`](../CLAUDE.md)、[`CLAUDE_MAP.md`](../CLAUDE_MAP.md)、[`ARCHITECTURE.md`](../ARCHITECTURE.md)、[`templates/`](../templates/)、[`commands/`](../commands/)。
