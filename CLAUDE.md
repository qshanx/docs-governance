# CLAUDE.md — docs-governance 插件自治理（用自己的方法论治自己）

面向长期 AI 协作项目的文档治理插件，维护项目规则、知识、决策与验证证据，支持后续 Agent 接手。

> 进会话读取（分级）：本文件全文 + `PROJECT_STATUS.md` 红线块；MAP / ARCHITECTURE / LOG 按需。
> 本插件**刻意保持轻量治理**——它自己的 skill 写着"别给小项目过度治理"，这套四件套就是个**薄示范**，别往里堆。

## 硬规则
- **方法论唯一源在 `skills/*/SKILL.md`**；agent / command 只指过去，**不复制方法论**（防插件自己内部漂移）。
- 生成、修改或审查 Agent 入口时执行 `skills/agent-entrypoints/SKILL.md` 的八条检查；`AGENTS.md` / `CLAUDE.md` 每份不超过 200 行，细节下沉后保留路标。
- 改任何文件后、提交前：在仓库根目录激活已有 `.venv`，运行 `bash scripts/verify.sh`，**绿了才提交**；首次环境准备见 [TESTS.md](TESTS.md)。
- 创建或更新 PR 前：提交完本轮改动后运行 `python3 scripts/check-pr-docs.py --base <实际目标分支>`；失败先修复，并按输出核对关联文档。推送与 PR CI 再检查同一提交快照。
- 文件名 kebab-case；治理正文默认中文，现有英文文档、代码标识及技术术语保留原语言。
- commit message 用英文；`git push` 等小磊说。

## 路标
- 路径导航 / 误导清单 / 别动区 → `CLAUDE_MAP.md`
- 当前 Module 权责、状态归属、依赖与核心流转 → `ARCHITECTURE.md`
- 当前健康 / 待办 → `PROJECT_STATUS.md`
- 改了什么 → `PROJECT_LOG.md`
- 调用治理能力、未指定专项 Skill → 先读 `skills/docs-governance/SKILL.md`，按意图选择对应 Skill，不全量加载。
- 架构 / 数据库决策 → `docs/adr/README.md`
- 涉及产品目标、需求、实现或验收 → 先从 [产品管理入口](docs/product/README.md) 定位当前基线，再按 `skills/product-evolution/SKILL.md` 的“按任务读取”核对当前需求和受影响条款；不默认全文加载产品目录。
- 文件归位与触发条件 → `.docs-governance.json`，说明见 `references/document-policy.md`
- 给用户怎么用 → `README.md` / `使用说明.md`
