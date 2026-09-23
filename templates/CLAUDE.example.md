# CLAUDE.md —— 宪法（保持短，细节链接出去；超过一页就把内容挪进对应文档，原处只留路标）

## 进会话读取（分级，不是全读）
默认只读：本文件全文 + `PROJECT_STATUS.md` 顶部红线块（文件存在时）。<!-- governance: optional=PROJECT_STATUS.md -->
需要定位文件或理解非显然路径时，按需读取 `CLAUDE_MAP.md`；理解整体结构或跨 Module 改动时，再读取 `ARCHITECTURE.md`（若存在）。**新建/删除/重命名文件前**读取已存在的 MAP + STATUS 删除区；**改变 Module 权责、状态、Interface、依赖或核心流转前**必读 ARCHITECTURE。普通目录结构直接 `ls`/`glob`，不要在本文件复制地图或架构正文。详细分级协议见 living-docs-governance skill。<!-- governance: optional=CLAUDE_MAP.md,ARCHITECTURE.md -->

## 硬规则（少而精：只放高杠杆的不可妥协约定）

> 经验值：前 10–15 条规则边际收益最大；规则越堆越没人遵守，宪法臃肿本身就是一种腐烂。够用就停，别凑数。
- 文件编码一律 UTF-8
- 只用绝对导入，禁止 `from . import xxx`
- 禁止新建文件，除非明确要求（改 main.py，不建 main_v2.py）
- （按项目补充：命名约定、提交信息格式、测试要求……）

## 路标（一行一个，指向细节所在）
- 项目有什么、在哪找 → `CLAUDE_MAP.md`<!-- governance: optional=CLAUDE_MAP.md -->
- 当前 Module 权责、状态归属、依赖与核心流转 → `ARCHITECTURE.md`（仅当项目已启用）<!-- governance: optional=ARCHITECTURE.md -->
- 当前健康度 / 禁区 / 待删 → `PROJECT_STATUS.md`<!-- governance: optional=PROJECT_STATUS.md -->
- 历史 / 改了什么 / 为什么 → `PROJECT_LOG.md`<!-- governance: optional=PROJECT_LOG.md -->
- 稳定领域术语 → `CONTEXT.md`（仅当项目已启用）<!-- governance: optional=CONTEXT.md -->
- 架构 / 数据库等难回退决策 → `docs/adr/README.md`（仅当项目已启用）<!-- governance: optional=docs/adr/README.md -->
- 任务、负责人、阻塞与排期 → 项目已有 Issue Tracker（不要复制进 STATUS / LOG）
- 产品目标、需求、实现或验收 → 仅在已建立产品空间时，替换本行为实际产品入口链接；先定位当前主题基线，再按 `product-evolution` Skill 的“按任务读取”核对需求与受影响条款，不默认全文加载产品目录。未启用时删除本行。
