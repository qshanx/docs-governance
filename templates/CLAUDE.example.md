# CLAUDE.md —— 共享章程（每份不超过 200 行，细节链接出去）

> 适用于已选定 CLAUDE.md 为共享主源的项目。生成时按 agent-entrypoints Skill 的 1—8 条逐项整理与检查；只填真实事实与已确认约定，移除模板说明与未适用项，不把八条方法全文抄进入口。

## 项目与验证入口

- 用已确认材料简述项目服务谁、解决什么、主要边界；技术栈仅写已确认部分。
- 填入实际工作目录和项目已有运行／验证入口；无代码或无配置时如实说明尚未建立，不虚构可运行命令。

## 进会话读取（分级，不是全读）
默认只读：本文件全文 + `PROJECT_STATUS.md` 顶部红线块（文件存在时）。<!-- governance: optional=PROJECT_STATUS.md -->
需要定位文件或理解非显然路径时，按需读取 `CLAUDE_MAP.md`；理解整体结构或跨 Module 改动时，再读取 `ARCHITECTURE.md`（若存在）。**新建/删除/重命名文件前**读取已存在的 MAP + STATUS 删除区；**改变 Module 权责、状态、Interface、依赖或核心流转前**必读 ARCHITECTURE。普通目录结构直接 `ls`/`glob`，不要在本文件复制地图或架构正文。详细分级协议见 living-docs-governance skill。<!-- governance: optional=CLAUDE_MAP.md,ARCHITECTURE.md -->

## 硬规则（少而精：只放高杠杆的不可妥协约定）

- `AGENTS.md` / `CLAUDE.md` 每份不超过 200 行；修改后计数复验。超长细节放到对应主记录，入口保留关键约束和读取路标，不截断有效规则。

从项目证据提炼可检查的命名、依赖、改动与验证约定；写清触发条件、具体动作及真实依据。禁用项必须有项目原因，不照抄示例库、导入风格或禁止新建文件等通用禁令，不凑规则数量。没有对应事实时删除本段，缺口在交付中列出。

## 路标（一行一个，指向细节所在）
- 项目有什么、在哪找 → `CLAUDE_MAP.md`<!-- governance: optional=CLAUDE_MAP.md -->
- 当前 Module 权责、状态归属、依赖与核心流转 → `ARCHITECTURE.md`（仅当项目已启用）<!-- governance: optional=ARCHITECTURE.md -->
- 当前健康度 / 禁区 / 待删 → `PROJECT_STATUS.md`<!-- governance: optional=PROJECT_STATUS.md -->
- 历史 / 改了什么 / 为什么 → `PROJECT_LOG.md`<!-- governance: optional=PROJECT_LOG.md -->
- 稳定领域术语 → `CONTEXT.md`（仅当项目已启用）<!-- governance: optional=CONTEXT.md -->
- 架构 / 数据库等难回退决策 → `docs/adr/README.md`（仅当项目已启用）<!-- governance: optional=docs/adr/README.md -->
- 任务、负责人、阻塞与排期 → 项目已有 Issue Tracker（不要复制进 STATUS / LOG）
- 产品目标、需求、实现或验收 → 仅在已建立产品空间时，替换本行为实际产品入口链接；先定位当前主题基线，再按 `product-evolution` Skill 的“按任务读取”核对需求与受影响条款，不默认全文加载产品目录。未启用时删除本行。
