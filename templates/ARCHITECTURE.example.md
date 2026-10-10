# ARCHITECTURE.md —— 当前架构契约

> 使用前按 `skills/architecture-docs/SKILL.md` 判断是否需要。以下模块、分层和约束仅为示例，替换为项目事实，删除不适用部分。
> 本文只写“当前架构是什么”。为什么这样选 → `docs/adr/`；Interface 字段与错误码 → `CONTRACT.md` 或代码 Interface；下游回归命令 → `REGRESSION.md`；知识入口 → `CLAUDE_MAP.md`。
> 当前实现引用真实代码或配置证据；尚未实现的确认设计单独标为计划。证据不足标“未验证”。

## 1. 架构摘要

用一到三句话说明当前架构的组织方式、已确认的依赖约束，以及这套结构保护什么。

## 2. Module 权责与状态归属

| Module | 唯一职责 | 拥有并修改的状态 | 对外 Interface | 允许依赖 | 禁止依赖 |
|---|---|---|---|---|---|
| UI | 接收输入、展示结果 | 页面临时状态 | `submit()` | Application | 数据库 Adapter、Domain 内部实现 |
| Application | 编排一次业务流程 | 当前任务状态 | `run()` | Domain、外部 Interface | UI |
| Domain | 执行核心业务规则 | 业务实体状态 | `decide()` | 无 | UI、基础设施实现 |
| Infrastructure | 接入数据库或外部系统 | 连接状态 | 实现对应 Interface | Domain 定义的 Interface | UI |

> 只登记真正需要协作者记住的关键 Module。如实记录状态拥有者与实际读写路径；与已确认约束冲突的情况另列。

## 3. 代码依赖图

```mermaid
flowchart LR
    UI["UI Module"] --> APP["Application Module"]
    APP --> DOMAIN["Domain Module"]
    APP --> PORT["外部 Interface"]
    ADAPTER["Infrastructure Adapter"] --> PORT
```

> 这里每条箭头只表示“左边代码依赖右边”，不是数据返回方向。实际依赖按代码记录，返回结果的方向另见运行时图。每条边都要能指向真实证据。

## 4. 运行时核心流转图

```mermaid
flowchart LR
    USER["用户"] --> UI["UI"]
    UI --> APP["Application"]
    APP --> DOMAIN["Domain"]
    APP --> PORT["外部 Interface"]
    PORT --> ADAPTER["Adapter"]
    ADAPTER --> PORT
    PORT --> APP
    APP --> UI
    UI --> USER
```

> 这里的箭头表示运行时消息、数据或结果流转，不代表代码依赖。只画一到三条不直观的主链路，普通函数调用不要全部展开。

## 5. Interface 与 Adapter 证据

| Interface / Seam | 定义位置 | 调用方 | Adapter | 约束唯一来源 |
|---|---|---|---|---|
| 模型调用 Interface | `src/domain/model.py` | Application | `src/infrastructure/deepseek.py` | 代码 Interface |
| 对外数据 Interface | `CONTRACT.md` | UI | 后端路由 | `CONTRACT.md` |

> 只有确实存在多个实现或明确替换点时才登记 Adapter；不要为了图完整制造没有消费者的假 Seam。

## 6. 更新与验证

- 新增、删除、拆分或合并 Module → 同次改动更新权责表与两张图。
- 状态拥有者、Interface、允许/禁止依赖或核心流转改变 → 同次更新本文；若属于难回退选择，再新增或更新 ADR。
- 审计时抽查真实 import、调用、注册和状态写入；文档与实现不一致时报告漂移；实现违反已确认约束时单列问题，不把二者混为一谈。
- 本文过长时拆出下级架构文档，但本文件仍保留总图和索引；不要把细节塞回 `CLAUDE_MAP.md`。
